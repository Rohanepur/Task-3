# Logic-Remediation Methodology (read fully before starting)

You are remediating a financial-QA dataset. Each entry is a `(question, answer, solution[], metadata)` annotation grounded in a company SEC filing (10-K / annual report). A prior validator flagged a **logic** defect (`metadata.logic_validation_failed == true`, with an explanation in `metadata.logic_issue`). Your job: for each assigned entry, either **fix** the logic error (and verify the fix against the actual filing) or **quarantine** it if the question is structurally broken.

## CRITICAL RULES (do not violate)

1. **Key on `(rec, ann)` — NEVER on `id`.** Ids are NOT unique (139 ids repeat across the dataset). Always address an annotation as `data[rec]['annotations'][ann]`.
2. **Do NOT modify any master file.** Read `Rainforest_860.json` (original) only. Write your results ONLY to your assigned patch file `patches/<your_name>.json`. Never touch `Rainforest_860_remediated.json`, `remediation_log.json`, `quarantine.json`, or another agent's patch.
3. **The `answer` field is NOT trustworthy.** In many entries the stored `answer` is wrong/stale while the `solution` already computes the right value (the validator often flagged the answer, not the reasoning). The reliable sources of the correct value are: (a) `metadata.logic_issue` (it usually names the correct number/method), and (b) the actual filing. When the solution already arrives at the value `logic_issue` endorses, the fix is just to sync the `answer` field (no solution edit needed).
4. **Verify every corrected figure against the filing** (this is mandatory, "criterion #5"). Use the helper to fetch the PDF and confirm the numbers you put in the answer/solution actually appear on the cited pages (or find the correct page and update `page_numbers`). If `logic_issue` cites a value you cannot find in the filing, treat the entry as `needs_review` (do not invent).
5. **Fix latent issues too.** While fixing the logic, also clean: foreign-language solution steps (translate to English), `answer`/solution arithmetic mismatches, and obviously broken internal references. Keep edits surgical and in the same plain style as the surrounding steps.
6. **Minimal, grounded edits.** Only change the step(s) that carry the error plus the final `answer`. Don't rewrite a whole solution unless necessary. Don't add flourish. Match the existing tone.

## How to fix a logic entry

1. Read the full entry (use `fv.py show <rec> <ann>`): question, answer, every solution step, `logic_issue`, `page_numbers`, `doc_link`.
2. Understand the error from `logic_issue` — it usually states the correct value and/or method.
3. Fetch the filing and verify the relevant numbers (`fv.py find <rec> "needle1" "needle2" ...` lists pages; `fv.py page <rec> <physical_page>` dumps text; note physical page is usually printed page − 1).
4. Decide the corrected `answer` and which solution step(s) to edit. Recompute carefully; show the corrected arithmetic in the step.
5. Record a `fix` entry in your patch (format below), including a one-line `verification` note of what you confirmed in the filing.

## When to QUARANTINE instead of fix

Quarantine (do NOT edit, do NOT clear the flag) when the question is structurally broken / ungroundable in the attached filing. Established categories (match these):
- **Wrong document/entity:** the attached filing is a different company/entity than the question asks about (e.g., parent vs. subsidiary), so the needed figures aren't here.
- **Requested period absent:** the question asks about a year/date the attached filing doesn't contain (e.g., a 2024 figure when the filing only covers FY2023/2022/2021; or a Dec-31 balance sheet for a May-31 fiscal-year company).
- **Graph-only value:** the answer depends on reading a precise value off a performance/return *graph* and the filing has **no numeric data table** for it (if there IS a data table with the values, it's fixable, not quarantine).
- **Nonexistent construct:** asks about a segment/line item that doesn't exist for that company/year.
- **Undefined non-GAAP metric:** asks for a non-GAAP metric (e.g., "Adjusted EBITDA") that the filing never defines/reconciles, so the adjustments are arbitrary.
- **Underspecified projection:** a "what-if" that needs a cost/margin assumption the question doesn't provide and `logic_issue` gives no uniquely-correct value.

## When to mark NEEDS_REVIEW

If `logic_issue` and the filing genuinely conflict (e.g., the issue's "correct" number isn't in the filing and you can't determine the right one), or the case is ambiguous in a way these rules don't cover — record `needs_review` with a clear note. Do not guess.

## Patch file format

Your patch file is a JSON array. One object per assigned `(rec,ann)` — process ALL of them. Use exactly these shapes:

Fix:
```json
{"rec": 53, "ann": 1, "id": "GRBK_2021", "kind": "P1", "action": "fix",
 "answer": "$230,534 thousand",
 "page_numbers": [67, 70],
 "solution_steps": {"3": "full replacement text for step index 3", "6": "full replacement text for step index 6"},
 "verification": "IBT 256,986, other income 9,483, equity income 19,713 on p67; D&A 2,744 on p70 — all confirmed"}
```
- `page_numbers` and `solution_steps` are OPTIONAL — include `page_numbers` only if you changed them; include only the step indices you changed (keys are stringified integer indices; values are the FULL new text of that step).
- For an answer-field-only sync (solution already correct), include just `answer` (+ `verification`).

Quarantine:
```json
{"rec": 97, "ann": 0, "id": "NEP_2024", "kind": "P1", "action": "quarantine",
 "reason": "Attached file is NextEra Energy, Inc. (parent) annual report; question concerns NextEra Energy Partners, LP, whose standalone figures aren't in this filing."}
```

Needs review:
```json
{"rec": 254, "ann": 0, "id": "CAT_2016", "kind": "P1", "action": "needs_review",
 "reason": "logic_issue says R&D should be $1,853M but filing shows $1,951M; cannot determine correct input."}
```

For any entry whose `kind` is `P2`, add `"ai_pending": true` to the object (its AI/humanization defect is handled in a separate pass — you only fix the logic here).

## Notes
- The PDF cache is shared at `/tmp/rf/`; fetching is idempotent.
- Use the unicode minus/operators sparingly; plain ASCII in math is fine.
- Write your patch file at the very end (and you may overwrite it as you go to checkpoint). Make sure it is valid JSON and contains one object for every assigned entry.
- Be precise with arithmetic. Double-check every division/percentage.
