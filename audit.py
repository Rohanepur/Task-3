#!/usr/bin/env python3
"""Audit the Rainforest dataset against the SIX client-ready criteria.

A record is NOT client-ready if any of these is true:
  1. logic_validation_failed: true
  2. ai_probability > 0.50
  3. fewer than 4 solution steps, or subheaders not separated by '\\n'
  4. ambiguous question/answer, inconsistent scale, or missing units
  5. any factual inaccuracies / incorrect data
  6. clear signs of AI-generated content

Criteria 1-3 are MECHANICAL (fully determined by the data) and scored exactly.
Criteria 4-6 require content/filing review and CANNOT be auto-passed here:
  - #5 needs the source 10-K to verify the cited figures.
  - #4 and #6 need reading judgement (LLM/human).
This audit scores 1-3 definitively and emits advisory signals for 4-6, so the
mechanical pass count is an UPPER BOUND on true client-readiness.
"""
import json, re
from collections import Counter

DATA = "Rainforest_860.json"
AI_THRESHOLD = 0.50


def ai_probs(a):
    g = a["metadata"].get("final_gptzero_check") or {}
    sp = ((g.get("solution") or {}).get("probability")) or 0
    qp = ((g.get("question") or {}).get("probability")) or 0
    return sp, qp


# ---- Criterion #3: structure ----
def structure_fail(sol):
    if len(sol) < 4:
        return True, "fewer_than_4_steps"
    for s in sol:
        if "\n" not in s:                       # subheader and body not separated
            return True, "subheader_no_newline"
        if not s.lstrip().startswith("#"):      # step lacks a markdown subheader
            return True, "no_subheader"
    return False, ""


# ---- Criterion #4 advisory: units / scale (NOT a hard auto-pass) ----
unit_pat = re.compile(r"\$|%|\b(million|billion|thousand|percent|per\s+share|days?|years?|"
                      r"shares?|units?|ratio|times|bps|basis points)\b", re.I)


def units_signal(answer):
    """Advisory: a final answer that is a bare number with no unit/currency token
    is a candidate for 'missing units'. Not definitive."""
    a = (answer or "").strip()
    if not a:
        return "empty_answer"
    if re.fullmatch(r"[-+]?\d[\d,]*\.?\d*", a) and not unit_pat.search(a):
        return "bare_number_no_unit"
    return ""


def audit_one(a):
    m = a["metadata"]
    sol = a.get("solution") or []
    sp, qp = ai_probs(a)

    c1 = m.get("logic_validation_failed") is True
    c2 = sp > AI_THRESHOLD or qp > AI_THRESHOLD
    c3, c3_reason = structure_fail(sol)

    f = {
        "c1_logic": c1,
        "c2_ai": c2,
        "c3_structure": c3,
        "c3_reason": c3_reason,
        "sol_prob": round(sp, 4),
        "q_prob": round(qp, 4),
        # advisory-only signals for the review criteria:
        "c4_units_signal": units_signal(a.get("answer")),
        "c5_needs_filing_check": True,   # every entry's data must be verified vs the 10-K
        "c6_needs_ai_review": True,      # textual AI-tells need reading judgement
    }
    # MECHANICAL pass = passes criteria 1-3. Upper bound on true readiness.
    f["mechanically_ready"] = not (c1 or c2 or c3)
    return f


def main():
    data = json.load(open(DATA))
    rows = []
    for ri, r in enumerate(data):
        for ai_idx, a in enumerate(r["annotations"]):
            f = audit_one(a)
            f.update({"_rec": ri, "_ann": ai_idx, "id": r["id"], "company": r["company"]})
            rows.append(f)

    n = len(rows)
    cnt = lambda k: sum(1 for x in rows if x[k])
    print(f"Total annotations: {n}\n")

    print("=== Mechanical criteria (exactly scored) ===")
    print(f"  #1 logic_validation_failed : {cnt('c1_logic')}")
    print(f"  #2 ai_probability > 0.50   : {cnt('c2_ai')}")
    print(f"  #3 structure               : {cnt('c3_structure')}")
    print("     structure reasons        :",
          dict(Counter(x["c3_reason"] for x in rows if x["c3_structure"])))
    mech = cnt("mechanically_ready")
    print(f"\n  PASS criteria 1-3 (upper bound): {mech}   FAIL 1-3: {n - mech}")

    # overlap of the three mechanical fails
    print("\n=== Overlap among the 1-3 failures ===")
    c = Counter()
    for x in rows:
        if not x["mechanically_ready"]:
            c[(x["c1_logic"], x["c2_ai"], x["c3_structure"])] += 1
    print("  logic  ai     struct  count")
    for k, v in sorted(c.items(), key=lambda kv: -kv[1]):
        print(f"  {str(k[0]):6} {str(k[1]):6} {str(k[2]):6} {v}")

    print("\n=== Review criteria 4-6 (NOT auto-scored — require content/filing review) ===")
    print(f"  #4 advisory 'bare number, no unit' answers : "
          f"{sum(1 for x in rows if x['c4_units_signal']=='bare_number_no_unit')}")
    print(f"  #4 advisory 'empty answer'                 : "
          f"{sum(1 for x in rows if x['c4_units_signal']=='empty_answer')}")
    print(f"  #5 entries needing filing fact-check       : {n}  (all)")
    print(f"  #6 entries needing AI-tell reading review  : {n}  (all)")
    print("\n  => True client-ready <= mechanical pass; pending 4-6 review.")

    json.dump(rows, open("audit_results.json", "w"), indent=2)
    print("\nWrote audit_results.json")


if __name__ == "__main__":
    main()
