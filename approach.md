# Approach — Original → Remediated (Rainforest-860)

## Objective
Take 860 financial-QA annotations (question + answer + step-by-step solution, each grounded in a company 10-K) and produce a client-ready dataset where every delivered record satisfies the quality rubric:
- `logic_validation_failed = false`
- `ai_probability < 0.50` (current GPTZero model)
- ≥ 4 solution steps, each a `## subheader\n body`
- unambiguous question/answer, consistent scale + units
- no factual inaccuracies; grounded in the cited filing
- no AI-generated "tells"

---

## 1. Triage & classification
Every annotation was bucketed by defect type from its metadata (`logic_validation_failed`, the prior `final_gptzero_check`, page/answer presence). Critically, addressing was done on the **`(record, annotation)` index — never the `id`** (139 ids repeat across the set). Buckets: logic-only, ai-only, logic+ai, structure/page, empty, and clean. This produced disjoint work queues and prevented cross-contamination.

## 2. Logic remediation (146 logic-flagged)
Each entry was re-derived from its source filing:
1. Read the `logic_issue`, which usually names the correct value/method.
2. **Fetch the actual 10-K PDF** (pymupdf) and **verify every figure on the cited page** — the single most important control. (Repeatedly, the stored `answer` field was wrong while the solution was right, or vice-versa; the filing was the source of truth, not either field.)
3. Apply the minimal correct fix (answer + the erring step(s)), preserving everything else.
4. Set `logic_validation_failed = false`.

Outcome: **107 fixed & verified, 36 quarantined, 3 out-of-scope.** Where the `logic_issue` itself was wrong (false positive — e.g. it cited a figure not in the filing), the original answer was confirmed and the flag cleared.

## 3. AI-humanization (whole set, current GPTZero)
The dataset's AI flags came from an **older** model. Re-scoring on the live model (`2026-05-11-base`) showed ~30% of *previously-"clean"* solutions now flag as AI — so the AI track expanded to the whole set, not just the original 118.

**Key empirical discovery (counterintuitive):** the current model flags **fluent, polished** prose as AI and passes **plain, declarative, slightly-mechanical** prose as human. Proven by polishing a *passing* solution → it flipped from `human 0.001` to `ai 1.0`. So humanization = make it **flatter, not fancier**:
- Short declarative sentences; mechanical, mildly repetitive register.
- `## subheader\n body` on every step; ≥ 4 steps.
- No chatty voice, no smooth transitions, no em-dashes.
- **Every figure, unit, citation, and the final answer preserved verbatim** — prose style only.

Each solution was run in a closed loop against the live API (`gz.py`) and iterated until `predicted_class != "ai"` (`ai_prob < 0.50`). Outcome: **332 rewritten + 434 already-clean on the current model = 766 pass**; 52 deferred.

## 4. Quarantine (36, removed not edited)
Entries that are broken at the source — wrong entity/document, requested year/date absent from the filing, performance-graph values with no data table, nonexistent segment, empty source, undefined non-GAAP metric — were flagged for removal in `quarantine.json` and **left byte-identical to the original** (verified). A dedicated salvage pass re-examined all 36 and **recovered 2** (PRU, CVX) by finding the data deeper in the filing.

## 5. Scale: parallel agent fleets
Work was sharded across disjoint `(rec,ann)` slices and run by **up to 14 agents in parallel**. Hard rule: **agents write only their own patch file; the master JSON is merged centrally** — eliminating write races. Every merge re-validated each entry independently before applying it.

---

## QA STRATEGY (defense in depth — 5 rounds)
1. **Inline filing verification** — every logic figure checked against the 10-K at fix time.
2. **Central merge gate (programmatic, every change)** — re-score `ai_prob < 0.50`; assert ≥4 `##/\n` steps; assert all large source figures + the answer value still present (scale-aware tolerance); assert answer field unchanged by AI rewrites. Failing entries are **held back, not shipped** (e.g. 41 AI rewrites held because they dropped a figure or didn't actually re-score under 0.5).
3. **Independent QA-agent fleets** — separate agents re-derived the math, re-checked grounding, and confirmed the GPTZero pass on every changed entry, writing flag verdicts only.
4. **Understandability QA** — a dedicated pass checking the rewrites read as coherent, self-contained solutions: no cryptic token-lists, no unexplained numbers (e.g. an "× 0.78" with no "= 1 − 22% tax"), consistent units. Genuine issues were fixed; logic concerns were **collected to `logic_flags.json` and not actioned** (per instruction).
5. **Global artifact sweeps** — dataset-wide scans removed leftover AI-refusal text ("I can't access external documents…") and surfaced foreign-language fragments (Catalan/Lithuanian/Italian/Albanian) and AI meta-notes.

Final automated audit of all 818 delivered entries (3,952 steps): **0 entries < 4 steps; 0 steps missing the `## head\n body` form; 0 `logic_validation_failed=true`.**

## SPOT-CHECK PROTOCOL
- **Random sampling** (fixed seed) from the changed set, surfacing the **full before/after solution text** plus the **live GPTZero before→after** for AI entries.
- Each spot-check verifies: answer preserved (or change attributable to a logic fix), every figure/citation intact, math reproduces the answer, structure (≥4 `##/\n` steps), and the score crossed below 0.50.
- Example (NVDA_2024): solution restyled from uniform prose (`ai 1.0`) to plain `## Numbers / ## Change / ## Percentage` steps (`human 0.156`); figures $34,621M / $18,704M and answer 85.10% identical. (Full set in `spot_check_v2.md`.)

---

## Tooling & audit trail
- `agent_tools/fv.py` — filing fetch + page/figure search; `gz.py` — live GPTZero scorer; methodology docs encoding the proven technique.
- `remediation_log.json`, `ai_remediation_log.json` — before/after for every logic fix and humanization.
- `quarantine.json` (36 to drop, with reasons), `logic_flags.json` (31 for human review), `presentation_summary.md`, `spot_check_v2.md`.

## Result
**766 client-ready** (logic correct + grounded, `ai < 0.50`, structured, figures intact) · **36 quarantined** for removal (unchanged) · **52 deferred** (factually correct, still AI-flagged) · **31 logic concerns** surfaced for review.
