# Web Claude beat

This folder is the **browser path** for the workshop: export a slice, upload it, paste a prompt, get a good answer in chat.

That is exactly the friction we are upgrading away from.

## What this shows

1. You leave the normal project flow and prepare an upload package (`upload/`).
2. You paste a prompt from `prompts/` into claude.ai.
3. Web Claude can still do useful work (clean, chart, memo in the chat product).
4. Then look at the real repo: `../outputs/` is still empty. Those artifacts did not land next to `../data/`.

The point is not that the browser is weak. The point is: chat artifacts ≠ files in this project. To get them here, you’d download/copy/paste and babysit paths. You’re the bridge.

## Live steps

1. Open claude.ai (new chat).
2. Upload `upload/ecommerce_churn_sample.csv`.
3. Paste `prompts/01_churn_brief.md`.
4. Let it produce a chart + short memo in the chat.
5. Flip to VS Code and show local `outputs/` (should be empty aside from `archive/` / `.gitkeep`).
6. Say the upgrade line, then switch to Claude Code on the full repo dataset.

## Files

```
web/
  upload/ecommerce_churn_sample.csv   # 500-row slice with Tenure nulls + CC vs Credit Card
  prompts/01_churn_brief.md           # paste into Web Claude
```

Do not put browser results into `outputs/`. That folder is reserved for the Claude Code demo.
