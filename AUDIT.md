# Rainforest Audit — 860 annotations (709 source docs)

Scored by `audit.py` against the **six** client-ready criteria. A record is NOT
client-ready if any is true:

1. `logic_validation_failed: true`
2. `ai_probability > 0.50`
3. fewer than 4 solution steps, or subheaders not separated by `\n`
4. ambiguous question/answer, inconsistent scale, or missing units
5. any factual inaccuracies / incorrect data
6. clear signs of AI-generated content

## Correction to the prior audit
The earlier version scored an invented **"page-number" criterion** (metadata
`page_numbers` completeness + prose page citations). That is **not** in the
rubric, so it was removed. Page/figure grounding is still useful, but only as a
**tool for criterion #5** (verifying cited data against the filing) — not a gate
on its own.

## Mechanical criteria (1-3) — exactly scored
| Criterion | Failing |
|---|---|
| #1 logic_validation_failed | 146 |
| #2 ai_probability > 0.50 | 118 |
| #3 structure (<4 steps / bad `\n` subheader) | 2 |

**Pass criteria 1-3: 621 / 860.** This is an **upper bound** on true
client-readiness, because criteria 4-6 are not yet verified.

### Overlap among the 1-3 failures (239 total)
| logic | ai | struct | count |
|---|---|---|---|
| T | F | F | 119 |
| F | T | F | 93 |
| T | T | F | 25 |
| T | F | T | 2 |

## Review criteria (4-6) — NOT auto-scored
These need content/filing review and cannot be auto-passed:
- **#5 factual accuracy** — all 860 must be checked against the source 10-K
  (the figures/answers must match the filing). This is the big unmeasured gate.
- **#4 units/scale/ambiguity** — advisory signal flags **130** answers that are
  a bare number with no unit/currency token, plus **3** empty answers, as
  candidates for "missing units". Not definitive.
- **#6 AI-tells** — textual judgement, all 860 pending review (the GPTZero
  probability in #2 is a separate mechanical signal).

## Bottom line
True client-ready ≤ **621**. The real remediation gates are **logic (146)** and
**AI (118)**; structure is trivial (2). Criteria #4-#6 still need a verification
pass before any final count is trustworthy.

## Infra
- Source 10-K PDFs (firebase) are reachable and text-extractable via `pymupdf` —
  feasible for the #5 fact-check.
- Network is open (GPTZero / OpenRouter reachable), but no API keys are set in
  this environment, so #2 cannot be re-scored here without a GPTZero key.
