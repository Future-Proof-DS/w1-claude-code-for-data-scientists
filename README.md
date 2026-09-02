# Workshop 1: Claude Code for Data Scientists

Run your first real analysis with an AI analyst, in this repo.

## What you leave with

Claude Code running against local files, one messy churn dataset taken end-to-end, a chart in `./outputs/`, and a findings memo shaped by the team skill.

## Setup

1. Open this folder in VS Code.
2. Create and activate a local venv (don’t install packages globally):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Data: `data/ecommerce_churn.csv`
4. Leave `outputs/` empty before the live run (keep `.gitkeep` and `archive/`).
5. In the integrated terminal: `claude`

## Layout

```
AGENTS.md                             # standing rules for every agent in this repo
checks/review_outputs.py              # pass/fail review of ./outputs (agent runs this)
data/ecommerce_churn.csv
web/upload/                           # CSV sample for Web Claude
web/prompts/                          # browser prompt(s)
outputs/                              # live chart + memo from Claude Code
outputs/archive/                      # known-good backup after a dry run
.claude/skills/data-summary/SKILL.md  # team audit + memo format (/data-summary)
requirements.txt
```

## Review check

After the agent writes chart + memo:

```powershell
.\.venv\Scripts\python.exe checks/review_outputs.py
```

Expect `passed`. To verify the checker against the archive backup:

```powershell
.\.venv\Scripts\python.exe checks/review_outputs.py --outputs outputs/archive
```

## Dataset

E-commerce customer churn from Kaggle (Anagha Paul), ~5.6k rows. Missing values and inconsistent labels (e.g. `"CC"` vs `"Credit Card"`) are part of the point.

https://www.kaggle.com/datasets/anaghapaul/e-commerce-dataset
