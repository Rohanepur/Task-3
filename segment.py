#!/usr/bin/env python3
"""Action-bucket segmentation of the 860 submissions.

Groups every NOT-client-ready submission by its full defect set AND the
sub-state that determines the remediation path:
  - logic     -> has_answer vs no_answer (no_answer must also be computed)
  - ai        -> humanization history (never tried / tried-but-failing) + severity band
  - page      -> missing (page_numbers empty) vs incorrect (needs filing check)
  - structure -> trivial reformat
Factual accuracy (criterion #5) is a verification pass over ALL entries and is
listed as its own action, since it can't be read off the tags.
"""
import json
from collections import Counter, defaultdict

DATA = "Rainforest_860.json"


def sol_prob(a):
    return ((a["metadata"].get("final_gptzero_check") or {}).get("solution") or {}).get("probability") or 0


def q_prob(a):
    return ((a["metadata"].get("final_gptzero_check") or {}).get("question") or {}).get("probability") or 0


def defects(a):
    m = a["metadata"]
    sol = a.get("solution") or []
    d = set()
    if m.get("logic_validation_failed") is True:
        d.add("logic")
    if sol_prob(a) > 0.50 or q_prob(a) > 0.50:
        d.add("ai")
    if len(sol) < 4 or any(("\n" not in s) or (not s.lstrip().startswith("#")) for s in sol):
        d.add("structure")
    pn = m.get("page_numbers")
    if (not pn) or (None in (pn or [])):
        d.add("page_missing")
    return d


def has_answer(a):
    return bool((a.get("answer") or "").strip())


def ai_state(a):
    m = a["metadata"]
    if not m.get("ai_content_fixed"):
        return "never_humanized"          # fresh — try humanization first
    return "humanized_still_failing"      # attempts exhausted — needs re-authoring


def main():
    data = json.load(open(DATA))
    ann = [(ri, ai, a) for ri, r in enumerate(data) for ai, a in enumerate(r["annotations"])]

    rows = []
    for ri, ai, a in ann:
        d = defects(a)
        rows.append({
            "rec": ri, "ann": ai, "id": data[ri]["id"], "company": data[ri]["company"],
            "defects": sorted(d),
            "has_answer": has_answer(a),
            "ai_state": ai_state(a) if "ai" in d else None,
            "ai_attempts": a["metadata"].get("humanization_attempts"),
            "sol_prob": round(sol_prob(a), 3),
            "page_numbers": a["metadata"].get("page_numbers"),
        })

    n = len(rows)
    clean = [r for r in rows if not r["defects"]]
    dirty = [r for r in rows if r["defects"]]
    print(f"Total {n}  |  clean (criteria 1-3): {len(clean)}  |  needs work: {len(dirty)}\n")

    # ---- LOGIC bucket ----
    L = [r for r in dirty if "logic" in r["defects"]]
    print(f"=== BUCKET A — LOGIC ({len(L)}) : re-derive calc vs filing ===")
    print(f"  A1 logic, has answer (verify+correct derivation) : "
          f"{sum(1 for r in L if r['has_answer'] and r['defects']==['logic'])}  (logic-only)")
    print(f"  A2 logic, NO answer  (derive answer too)         : "
          f"{sum(1 for r in L if not r['has_answer'])}")
    print(f"  A3 logic + AI        (re-derive AND de-AI)        : "
          f"{sum(1 for r in L if 'ai' in r['defects'])}")
    print(f"  A4 logic + page_missing (re-derive AND add pages) : "
          f"{sum(1 for r in L if 'page_missing' in r['defects'])}")
    print(f"  A5 logic + structure (re-derive AND reformat)     : "
          f"{sum(1 for r in L if 'structure' in r['defects'])}")

    # ---- AI bucket ----
    A = [r for r in dirty if "ai" in r["defects"]]
    print(f"\n=== BUCKET B — AI RISK ({len(A)}) ===")
    print(f"  B1 never humanized (try humanization 1st pass)    : "
          f"{sum(1 for r in A if r['ai_state']=='never_humanized')}")
    bh = [r for r in A if r["ai_state"] == "humanized_still_failing"]
    print(f"  B2 humanized but STILL failing (needs re-author)  : {len(bh)}")
    print(f"       by attempts: {dict(Counter(r['ai_attempts'] for r in bh))}")
    print(f"  severity: 0.5-0.9 prob {sum(1 for r in A if 0.5<r['sol_prob']<0.9)}  "
          f">=0.9 prob {sum(1 for r in A if r['sol_prob']>=0.9)}")
    print(f"  pure AI-only (no other defect): {sum(1 for r in A if r['defects']==['ai'])}")

    # ---- PAGE / FACTUAL bucket ----
    P = [r for r in dirty if "page_missing" in r["defects"]]
    print(f"\n=== BUCKET C — PAGE / FACTUAL ===")
    print(f"  C1 page_numbers MISSING (empty) — identify+add    : {len(P)}")
    for r in P:
        print(f"       {r['id']:12} defects={r['defects']}")
    print(f"  C2 page_numbers INCORRECT — needs filing check    : (verify pass)")
    print(f"  C3 factual data errors  — needs filing check      : (verify pass, all 860)")

    # ---- STRUCTURE ----
    S = [r for r in dirty if "structure" in r["defects"]]
    print(f"\n=== BUCKET D — STRUCTURE ({len(S)}) : reformat steps/subheaders ===")

    # ---- combination matrix (a submission needs ALL its defects fixed) ----
    print("\n=== Defect-set combinations (full remediation checklist per submission) ===")
    for combo, c in Counter(tuple(r["defects"]) for r in dirty).most_common():
        print(f"  {c:4}  {combo}")

    json.dump(rows, open("buckets.json", "w"), indent=2)
    print("\nWrote buckets.json")


if __name__ == "__main__":
    main()
