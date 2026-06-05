# Action Buckets — 860 submissions

**621 clean** (pass criteria 1-3) · **239 need work** · factual accuracy (#5) still
to be verified across all 860.

Segmented by defect tag **and** the sub-state that picks the remediation path.
A submission needs *every* defect in its set fixed (see the combination matrix).

---

## Bucket A — LOGIC (146) → re-derive the calculation against the filing
`logic_validation_failed: true`. Each carries a `logic_issue` describing the error.

| Sub | What | Count | Remediation |
|---|---|---|---|
| A1 | logic-only, **has answer** | 117 | Re-derive; the stated answer + `logic_issue` pinpoint the fix |
| A2 | logic, **no answer** | 3 | Must also *compute* the answer (these are the TARS/TIF/SON trio below) |
| A3 | logic **+ AI** | 25 | Re-derive **and** de-AI the prose |
| A4 | logic **+ page_missing** | 4 | Re-derive **and** populate `page_numbers` |
| A5 | logic **+ structure** | 2 | Re-derive **and** reformat steps |

(A1+A3+A4+A5 overlap by tag; see matrix for the disjoint per-submission counts.)

## Bucket B — AI RISK (118) → de-AI the solution prose
`ai_probability > 0.50` on the final GPTZero check.

| Sub | What | Count | Remediation |
|---|---|---|---|
| B1 | **never humanized** (`ai_content_fixed` unset) | 4 | Cheapest: run a first humanization pass |
| B2 | **humanized but still failing** | 114 | Humanization is exhausted → **re-author from the filing**, not re-humanize |
| └ by attempts | 3 attempts / 2 / 1 | 110 / 1 / 3 | 110 already tried 3× and still fail |
| severity | prob 0.5–0.9 / ≥0.9 | 39 / 79 | 79 are near-certain AI (≥0.90) |

**Pure AI-only (no other defect): 93.** Blocker: no GPTZero key in this env, so
rewrites **cannot be re-scored here** — need the key or external scoring.

## Bucket C — PAGE / FACTUAL
| Sub | What | Count | Remediation |
|---|---|---|---|
| C1 | `page_numbers` **MISSING** (empty) | 4 | Identify the source page(s) from the filing, add + grounding element |
| C2 | `page_numbers` **INCORRECT** | TBD | Needs filing verification (cited page ≠ where the data is) |
| C3 | **factual data errors** | TBD | Needs filing verification — figures/answer must match the 10-K (criterion #5) |

C1 entries (all are also logic-tagged): TARS_2023, KIRK_2023, TIF_2018, SON_2024.
C2/C3 are a verification pass — not readable from tags.

## Bucket D — STRUCTURE (2) → reformat
`<4` steps or subheader not `\n`-separated. Trivial fix.

---

## Combination matrix (full checklist per submission)
| Count | Defect set | Remediation checklist |
|---|---|---|
| 117 | `logic` | re-derive |
| 93 | `ai` | de-AI / re-author |
| 23 | `ai + logic` | re-derive + de-AI |
| 2 | `logic + structure` | re-derive + reformat |
| 2 | `ai + logic + page_missing` | re-derive + de-AI + add pages + (compute answer) |
| 2 | `logic + page_missing` | re-derive + add pages |

## Worst-case trio (author near-from-scratch)
**TARS_2023, SON_2024** (ai+logic+page_missing, **no answer**) and **TIF_2018**
(logic+page_missing, no answer): empty answer, empty `page_numbers`, logic-failed,
2 of 3 also AI-flagged. Highest effort per unit.

## Suggested order (cheap/high-confidence → hard)
1. **D structure (2)** — mechanical reformat.
2. **C1 page_missing (4)** — add pages from filing (still needs the entangled logic fix to fully clear).
3. **B1 AI never-humanized (4)** — quick humanization attempt.
4. **A1 logic-only w/ answer (117)** — re-derive; answer + `logic_issue` make these verifiable.
5. **A3 logic+AI (23)** — re-derive then de-AI.
6. **B2 AI humanized-but-failing (114)** — full re-author; the hard core (blocked on GPTZero scoring).
7. **Cross-cutting: C3 factual verification (#5)** over all entries.
