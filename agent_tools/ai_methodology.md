# AI-Humanization Methodology (read fully before starting)

You rewrite AI-flagged `solution` text in a financial-QA dataset so it reads as genuinely human-written and **passes GPTZero**, WITHOUT changing any facts, numbers, citations, or the final answer. This is hard: most of these solutions already failed 3 automated humanization passes. Superficial edits will NOT work and will be rejected on spot-check.

## Absolute rules
1. **Key on `(rec, ann)`**, never `id` (ids repeat).
2. **Preserve all substance**: every figure, page citation, table name, intermediate calculation, and the final answer must remain exactly correct and consistent with the filing. You are changing *how it reads*, not *what it says*. Do not alter the `answer` field or the numbers.
3. **Score the real artifact.** The dataset scores the solution as the steps joined by newlines. Use the helper: `python3 agent_tools/gz.py entry <rec> <ann>` scores the current solution in `Rainforest_860_remediated.json`. To score a candidate rewrite, write the joined text to a temp file and `python3 agent_tools/gz.py score - < /tmp/cand.txt`.
4. **One at a time. Loop until PASS.** Do not move to the next entry until `gz.py` returns `"PASS": true` (predicted_class == 'human'). Aim for an AI/`completely_generated_prob` comfortably low (≤ ~0.15), not just barely over the line.
5. **Write ONLY your patch file** `patches/ai_<your_name>.json`. Never edit master files or another agent's patch.

## Why these read as AI (and what to change)
GPTZero keys on **low perplexity** (predictable word choice) and **low burstiness** (uniform sentence length/structure). These solutions are templated: every step is "## Step N: [imperative]. Navigate to page X, locate the table titled "Y", find the value Z. The units are stated as ...". That uniformity is the tell.

To genuinely raise perplexity and burstiness you must **restructure**, not paraphrase:
- **Vary sentence length hard.** Mix very short sentences (3–6 words) with longer, winding ones. Burstiness comes from real variance, not average length.
- **Break the template.** Don't start every step the same way. Drop some "## Step" scaffolding or merge steps; let the reasoning flow as a person explaining their work would — sometimes terse, sometimes elaborating the *why*.
- **Kill formulaic connectives** ("Additionally", "Furthermore", "Moreover", "It is important to note", "In order to", "Thus,"). Use plainer, less predictable transitions or none.
- **Concrete over hedged.** Replace generic filler ("the necessary data", "relevant information", "we can proceed") with specific, direct statements.
- **Asymmetry is human.** Real analysts don't perfectly parallel every clause. Avoid balanced/parallel list phrasing.
- **Keep the numbers and citations verbatim**, but you can change the prose around them freely.
- Do NOT inject typos, slang, or errors to game the detector — that fails spot-check and corrupts the data. The goal is clean, natural, varied expert prose.

## Loop per entry
1. `python3 agent_tools/fv.py show <rec> <ann>` — read the question, the current solution steps, and the answer. (For P2 entries, the logic has already been fixed in the remediated file; pull the CURRENT solution from there — see helper note — so you humanize the corrected version.)
2. Identify the facts/numbers/citations that must be preserved.
3. Rewrite the solution as a list of steps (you may change the number of steps). Substantive restructuring per the guidance above.
4. Score it. If not PASS, diagnose: is it still too uniform? too templated? Revise structure (not just words) and re-score. Keep iterating.
5. When PASS, record the patch object with the full new `solution` array and the GPTZero result.

## Patch format
JSON array, one object per assigned entry:
```json
{"rec": 80, "ann": 0, "id": "BRBR_2022", "kind": "P3_ai_only", "action": "humanized",
 "solution": ["full new step 1 text", "full new step 2 text", "..."],
 "gptzero": {"predicted_class": "human", "prob": 0.07},
 "iterations": 3}
```
If after many genuine attempts (say ≥ 8 substantive restructurings) an entry still won't pass, record `"action": "stuck"` with your best `solution` so far and the lowest score achieved, and move on.

## Notes
- The current solution to humanize lives in `Rainforest_860_remediated.json` (it has logic fixes already merged). Read it from there, not the original. Helper: `python3 -c "import json;print('\n'.join(json.load(open('Rainforest_860_remediated.json'))[REC]['annotations'][ANN]['solution']))"`.
- Be mindful of GPTZero rate limits; if you hit 429 the helper backs off automatically.
- Preserve the markdown `##` heading style only where it still reads naturally — you don't have to keep it on every step.
