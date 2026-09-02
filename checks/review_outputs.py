"""Check live demo outputs against the workshop review bar."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DEFAULT_OUTPUTS_DIR: Path = Path("outputs")
CHART_NAME: str = "churn_tenure.png"
MEMO_NAME: str = "data_summary_memo.md"


def has_nonempty_file(file_path: Path) -> bool:
    """True when the path exists and is not an empty file."""
    return file_path.is_file() and file_path.stat().st_size > 0


def extract_metric_breakdown(memo_text: str) -> str:
    """Return the payment-mode breakdown section from the memo."""
    section_match: re.Match[str] | None = re.search(
        r"##\s*3\.\s*Metric breakdown(.*?)(?:\n##\s*|\Z)",
        memo_text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if section_match is None:
        return ""
    return section_match.group(1)


def has_tenure_missingness_flagged(memo_text: str) -> bool:
    """True when Tenure gaps are reported, not treated as clean."""
    tenure_audit_row: re.Pattern[str] = re.compile(
        r"\|\s*Tenure\s*\|[^|\n]*\|[^|\n]*\|[^|\n]*\|\s*([1-9]\d*)\s*\|",
        flags=re.IGNORECASE,
    )
    has_nonzero_tenure_missing: bool = tenure_audit_row.search(memo_text) is not None

    has_tenure_should_review: bool = bool(
        re.search(r"Tenure[\s\S]{0,80}SHOULD_REVIEW", memo_text, flags=re.IGNORECASE)
    )
    has_plain_language_flag: bool = bool(
        re.search(
            r"Tenure.{0,120}(missing|missingness|null|gap)",
            memo_text,
            flags=re.IGNORECASE | re.DOTALL,
        )
    )
    claims_tenure_is_clean: bool = bool(
        re.search(r"\|\s*Tenure\s*\|[^\n]*\|\s*IS_CLEAN\s*\|", memo_text, flags=re.IGNORECASE)
    )

    return (
        not claims_tenure_is_clean
        and (has_nonzero_tenure_missing or has_tenure_should_review or has_plain_language_flag)
    )


def has_silent_tenure_impute_sold_as_clean(memo_text: str) -> bool:
    """True when the memo sells imputed Tenure as if the chart used complete data."""
    return bool(
        re.search(
            r"(median[- ]imput|imput(?:ed|ation).{0,40}Tenure|Tenure.{0,40}imput)",
            memo_text,
            flags=re.IGNORECASE | re.DOTALL,
        )
        and not has_tenure_missingness_flagged(memo_text)
    )


def has_cc_merged_with_credit_card(memo_text: str) -> bool:
    """True when the breakdown keeps Credit Card and does not list bare CC."""
    breakdown_text: str = extract_metric_breakdown(memo_text)
    if not breakdown_text:
        return False

    has_credit_card_row: bool = bool(
        re.search(r"\|\s*Credit Card\s*\|", breakdown_text, flags=re.IGNORECASE)
    )
    has_bare_cc_row: bool = bool(
        re.search(r"\|\s*CC\s*\|", breakdown_text)
    )
    return has_credit_card_row and not has_bare_cc_row


def run_review(outputs_dir: Path) -> list[tuple[str, bool, str]]:
    """Build the ordered review checks for one outputs folder."""
    chart_path: Path = outputs_dir / CHART_NAME
    memo_path: Path = outputs_dir / MEMO_NAME
    has_memo: bool = has_nonempty_file(memo_path)
    memo_text: str = memo_path.read_text(encoding="utf-8") if has_memo else ""

    tenure_is_flagged: bool = has_memo and has_tenure_missingness_flagged(memo_text)
    silent_impute_is_sold: bool = has_memo and has_silent_tenure_impute_sold_as_clean(
        memo_text
    )
    payment_aliases_are_collapsed: bool = has_memo and has_cc_merged_with_credit_card(
        memo_text
    )

    return [
        ("chart on disk", has_nonempty_file(chart_path), str(chart_path)),
        ("memo on disk", has_memo, str(memo_path)),
        (
            "tenure missingness flagged",
            tenure_is_flagged,
            "memo must report Tenure gaps" if has_memo else str(memo_path),
        ),
        (
            "no silent tenure impute",
            has_memo and not silent_impute_is_sold,
            (
                "do not sell imputed Tenure as clean"
                if has_memo
                else str(memo_path)
            ),
        ),
        (
            "cc merged with credit card",
            payment_aliases_are_collapsed,
            (
                "breakdown must keep Credit Card and drop bare CC"
                if has_memo
                else str(memo_path)
            ),
        ),
    ]


def print_review(checks: list[tuple[str, bool, str]]) -> bool:
    """Print one line per check. Return True when every check passed."""
    all_passed: bool = True

    for check_name, is_ok, detail in checks:
        status: str = "ok" if is_ok else "fail"
        if is_ok:
            print(f"{check_name}: {status}")
        else:
            all_passed = False
            print(f"{check_name}: {status} ({detail})")

    print("")
    print("passed" if all_passed else "failed")
    return all_passed


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI args for the outputs folder to review."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Review workshop demo outputs."
    )
    parser.add_argument(
        "--outputs",
        type=Path,
        default=DEFAULT_OUTPUTS_DIR,
        help="Folder with churn_tenure.png and data_summary_memo.md",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the review and exit 0 on pass, 1 on fail."""
    args: argparse.Namespace = parse_args(argv)
    outputs_dir: Path = args.outputs
    checks: list[tuple[str, bool, str]] = run_review(outputs_dir)
    did_pass: bool = print_review(checks)
    return 0 if did_pass else 1


if __name__ == "__main__":
    sys.exit(main())
