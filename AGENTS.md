# AGENTS.md

This repo is a churn workshop: messy e-commerce CSV in `./data/`, chart and memo in `./outputs/`.
Job-specific recipes live under `.claude/skills/`.

## Workflow

- Say the plan in 3 steps before you edit anything.
- Change only what this task needs.
- Read inputs from `./data/`. Write charts and memos to `./outputs/`.
- If the active skill names a done-check, run it with `.\.venv\Scripts\python.exe` and fix until it passes.

## Style

- Run Python with `.\.venv\Scripts\python.exe`, not a global install.
- Typehints on new variables. Short docstrings (how/why, not what).

```python
def has_nonempty_file(file_path: Path) -> bool:
    """True when the path exists and is not an empty file."""
    return file_path.is_file() and file_path.stat().st_size > 0
```

## Safety

- Ask before adding packages.
- Never commit `.env`, keys, or large raw extracts.
- Don’t overwrite files under `./data/`.
- Don’t modify files under `./outputs/archive/`.
