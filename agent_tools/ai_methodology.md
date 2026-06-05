# AI-Humanization Methodology v2 (READ FULLY — supersedes any earlier version)

You rewrite an AI-flagged `solution` so it passes GPTZero (`predicted_class != "ai"`), WITHOUT changing any fact, number, citation, or the final answer. The technique below was empirically validated against the live GPTZero model (`2026-05-11-base`). Follow it exactly — intuition about "humanizing" is WRONG here.

## The counterintuitive core finding (proven)
GPTZero's current model flags **fluent, polished, well-crafted** prose as AI, and passes **plain, declarative, slightly-mechanical** prose as human. We confirmed this by polishing a passing solution — it flipped from human 0.001 to ai 1.0. So:

- **DO write plain, flat, declarative sentences** that state where a value is and what it is. Example that PASSES: "The Consolidated Statements of Cash Flows for Acadia Realty Trust appears on page 112 of the 10-K. The statement reports net cash provided by operating activities of $140,448 thousand for the year ended December 31, 2024."
- **DO keep repetitive / templated structure.** Repeating a stem like "The same statement on page X reports..." across steps is GOOD here. Do NOT de-template.
- **DO NOT** make it conversational/chatty ("Here's what's going on...", "Let's...", "in other words"). Chatty style scored ai 1.0 every time.
- **DO NOT** add smooth transitions ("Furthermore", "Moreover", "Additionally", "Thus", "Notably"), rhetorical flourish, or "voice." Polished prose = AI.
- **DO NOT** use em dashes (—) or en dashes (–). Use periods or commas. Use straight quotes. Write "minus"/"negative" instead of a dash before a number where natural.
- Keep sentences short and factual. Mild repetition and a slightly mechanical register are exactly what passes.
- Preserve EVERY number, page citation, table name, and the final answer verbatim. You are changing prose style only, never the facts or the answer field.

## Realistic expectation
This reliably flips **borderline** entries (your assigned ones). If an entry simply will not pass after your attempts, mark it `stuck` (see below). Do not degrade into gibberish or insert errors to force a pass — that fails spot-check and corrupts data.

## Per-entry loop (one at a time, do not move on until PASS)
1. Read the current solution from the REMEDIATED file (it has logic fixes already merged):
   `python3 -c "import json;a=json.load(open('Rainforest_860_remediated.json'))[REC]['annotations'][ANN];print(a['question']);print('ANS:',a['answer']);[print(i,repr(s)) for i,s in enumerate(a['solution'])]"`
2. Note every fact/number/citation to preserve.
3. Rewrite the solution as a list of steps in the PLAIN style above. Keep roughly the same step structure; keep headings simple (`## ...`) or drop them — both fine, but plain.
4. Score it: write the steps joined by newline to a temp file and run
   `python3 agent_tools/gz.py score - < /tmp/yourfile.txt`
   PASS = `"PASS": true` (predicted_class is not "ai"). Aim for ai_prob well under 0.5.
5. If not PASS, make it PLAINER and FLATTER (not fancier): shorter declarative sentences, more mechanical phrasing, remove any lingering smooth/transitional language. Re-score. Iterate up to ~6 times.
6. On PASS, record the patch object. If still failing after ~6 genuine attempts, record `stuck` with your best version and lowest ai_prob.

## Patch format — write ONLY to `patches/ai_<your_name>.json` (never touch master files)
JSON array, one object per assigned entry:
```json
{"rec": 60, "ann": 1, "id": "AKR_2024", "action": "humanized",
 "solution": ["full step 1 text", "full step 2 text", "..."],
 "ai_prob": 0.026, "predicted_class": "human", "iterations": 2}
```
For an entry you cannot pass:
```json
{"rec": 80, "ann": 0, "id": "BRBR_2022", "action": "stuck",
 "solution": ["best attempt steps..."], "ai_prob": 0.83, "iterations": 6}
```

## Hard constraints
- Write ONLY your own patch file. Never edit Rainforest_860_remediated.json or others' files.
- Never change the `answer` or any number/citation. Verify your rewrite contains the same figures as the original.
- Be frugal with scoring calls: only score complete candidate solutions, not fragments.

## Refinements that worked on harder entries (use these)
- **Drop the `## headings` entirely** and write the solution as a few short plain PARAGRAPHS. Heading-segmented short blocks sometimes still score AI; continuous plain paragraphs do better.
- **Use bare arithmetic in words**: "140,448 minus 155,758 equals negative 15,310" rather than a formatted formula line.
- **Delete concluding "formula" sentences** ("The calculation requires dividing X by Y..."). State the numbers and the result directly.
- For CONFIDENT-AI entries (start at ai≈1.0): expect 4-10 iterations. Make each attempt PLAINER and FLATTER. Plain declarative sentences beat both fluent prose AND bare fragment lists (fragments can bounce back to AI).
- It is acceptable for predicted_class to be "mixed" (that still passes, since not "ai"); aim for ai_prob under 0.5.
