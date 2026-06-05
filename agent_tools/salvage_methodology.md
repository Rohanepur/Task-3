# Salvage Methodology — re-examine quarantined entries for a recoverable solution

The 38 entries in `quarantine.json` were marked for removal because they looked structurally broken or ungroundable. Your job: spend REAL effort on each to determine whether a correct, filing-grounded solution actually exists after all. Recovering even a few adds good entries. Working dir: /home/user/Task-3.

## Inputs
- `quarantine.json` — list of `{id, rec, ann, reason}`. Process EVERY entry.
- Inspect: `python3 agent_tools/fv.py show <rec> <ann>` (question/answer/solution/logic_issue), `find <rec> "needle"...`, `page <rec> <phys>`, `around <rec> <phys> "needle"`.

## Approach per entry
Read the quarantine `reason`, then actively try to disprove it by digging into the filing:
- **"Graph-only / no data table"** → search the WHOLE document for a numeric table of the values (performance-graph tables are sometimes pages away from the graph, or in an exhibit). Try `find` on plausible values and labels.
- **"Requested year/date absent"** → check whether the needed figure appears anywhere (5-year selected-financial-data tables, segment notes, MD&A, prior-period columns).
- **"Wrong entity/document"** → check whether the filing actually does contain the asked entity's standalone statements in a separate section.
- **"Underspecified projection"** → see if the filing supplies the missing assumption (e.g., a disclosed margin/rate) that makes a single correct answer computable.
- **"Nonexistent segment / metric"** → confirm it truly doesn't exist, or find the correct corresponding disclosure.
- **"Empty source entry"** (no question/answer/solution) → genuinely unrecoverable; confirm and move on.

A salvage is only valid if you can VERIFY the answer from the filing (cite page + exact figures). Do not invent or guess. If it stays ambiguous/ungroundable, keep it quarantined.

## Output — write ONLY to `patches/salvage.json`
JSON array, one object per quarantined entry:
```json
{"rec": 81, "ann": 0, "id": "VVPR_2023", "verdict": "keep_quarantined", "reason": "confirmed: filing has no 2024 column anywhere"}
```
or, when recoverable:
```json
{"rec": 277, "ann": 1, "id": "CARS_2023", "verdict": "salvageable",
 "answer": "$47",
 "solution": ["plain-style step 1 ...", "step 2 ...", "..."],
 "verification": "data table on page 81 lists CARS 12/31/18=100.00 and 12/31/20=53.xx; high-low = ~47, grounded"}
```
Notes:
- Write the proposed `solution` in the PLAIN, declarative style from `agent_tools/ai_methodology.md` (these were AI-flagged too), so it can pass GPTZero later.
- Prefer precision: only mark `salvageable` when the figures are unambiguously in the filing.
- Do not edit any master file — only `patches/salvage.json`.
