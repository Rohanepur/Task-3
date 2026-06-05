# QA Methodology — verify changed entries against source filings

You independently QA entries we remediated, checking each against the actual SEC filing. Be skeptical and thorough: your job is to CATCH problems, not rubber-stamp. Working dir: /home/user/Task-3.

## Inputs
- Your assignment: `patches/qa_assign_<YOURNAME>.json` — list of `{rec, ann, kinds, ans_changed}`. `kinds` is `["logic"]`, `["ai"]`, or `["logic","ai"]`.
- Original (pre-remediation): `Rainforest_860.json`
- Remediated (current): `Rainforest_860_remediated.json`
- Inspect a filing: `python3 agent_tools/fv.py show <rec> <ann>` (shows ORIGINAL), `find <rec> "needle"...`, `page <rec> <phys>`, `around <rec> <phys> "needle"`. Physical page ≈ printed page − 1.
- Score AI text: `python3 agent_tools/gz.py entry <rec> <ann>` scores the CURRENT remediated solution. PASS = predicted_class != "ai".

To see original vs new for an entry:
`python3 -c "import json;o=json.load(open('Rainforest_860.json'));n=json.load(open('Rainforest_860_remediated.json'));O=o[REC]['annotations'][ANN];N=n[REC]['annotations'][ANN];print('Q:',O['question']);print('OLD ANS:',O['answer']);print('NEW ANS:',N['answer']);print('--- OLD ---');[print(i,repr(s)) for i,s in enumerate(O['solution'])];print('--- NEW ---');[print(i,repr(s)) for i,s in enumerate(N['solution'])]"`

## What to check

### For `logic` changes (answer and/or reasoning corrected)
1. **Grounding**: every figure in the new solution must actually appear in the filing on the cited page(s). Spot-check the key numbers with `fv.py find`/`around`.
2. **Math**: recompute the arithmetic yourself. Does it produce the stated NEW answer?
3. **Answer consistency**: the NEW `answer` field must match what the solution computes, and must be the correct, grounded value.
4. **Question fit**: the solution actually answers the question asked (right entity, right year, right line item).

### For `ai` changes (solution restyled to pass GPTZero)
1. **Figures preserved**: every number, page citation, table name, and the final answer from the ORIGINAL solution must still be present (allowing formatting differences like 27,103 vs 27103, or 0.04 vs 4%). The `answer` field must be UNCHANGED from the version before humanization.
2. **No math/logic altered**: the rewrite must not change the calculation or introduce new/inconsistent numbers.
3. **Still passes**: run `gz.py entry <rec> <ann>` — confirm predicted_class != "ai".
4. **Readability/spot-check**: the prose must read as a legitimate, coherent solution — no gibberish, no contradictions, no leftover AI-refusal text, no broken sentences. (Plain/mechanical is fine and expected; incoherent is not.)

### For `logic,ai` (both): apply both sets of checks.

## Output — write ONLY to `patches/qa_<YOURNAME>.json`
JSON array, one object per assigned entry:
```json
{"rec": 53, "ann": 1, "id": "...", "verdict": "pass", "checked": "figures 256,986/9,483/19,713/2,744 confirmed on p67/p70; 256,986-9,483-19,713+2,744=230,534 matches answer"}
```
or
```json
{"rec": 12, "ann": 0, "id": "...", "verdict": "flag", "severity": "high|low",
 "issue": "specific problem, e.g. 'new answer 1,042.15 but solution divides by wrong base; recompute gives 1,038.9' or 'AI rewrite dropped the $148.2M prepaid figure' or 'gz.py still returns ai 0.91'"}
```
Process EVERY assigned entry. Be specific in `issue` so it can be fixed without re-deriving. Do not edit any master file — only your QA patch.

## UNDERSTANDABILITY-FOCUSED QA (for rewritten solutions)
For each rewritten entry, the bar is not just "passes GPTZero" — it must read as a clear, correct, self-contained solution. FLAG (severity low/high) if any of these:
- A number appears with no explanation of where it came from (e.g. "times 0.78" without saying it is 1 minus the 22% tax rate; or a derived figure with no source).
- The steps are cryptic, fragmented to the point of being hard to follow, or read like a list of tokens rather than reasoning.
- Any figure, unit ($/thousands/millions/%/shares), citation, or the final answer differs from the original or is internally inconsistent.
- Fewer than 4 steps, or a step missing `##` + `\n`.
- The math shown does not actually produce the stated answer.
- Any leftover AI-refusal text or contradiction.
Otherwise mark `pass`. Include a one-line `checked` note (what you verified) or a specific `issue`.
