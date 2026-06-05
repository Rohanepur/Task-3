#!/usr/bin/env python3
"""Authoritative re-audit of the Rainforest dataset against the six client-ready criteria.

Emits per-annotation flags + a categorical breakdown, and writes audit_results.json.
"""
import json, re, sys
from collections import Counter

DATA = "Rainforest_860.json"
AI_THRESHOLD = 0.50

page_pat = re.compile(r"pages?\s+(\d+)", re.I)


def sol_ai_prob(a):
    return ((a["metadata"].get("final_gptzero_check") or {}).get("solution") or {}).get("probability")


def q_ai_prob(a):
    return ((a["metadata"].get("final_gptzero_check") or {}).get("question") or {}).get("probability")


def audit_one(a):
    m = a["metadata"]
    sol = a.get("solution") or []
    flags = {}

    # 1. logic validation
    flags["logic"] = m.get("logic_validation_failed") is True

    # 2. AI risk (solution and/or question prob > 0.50)
    sp = sol_ai_prob(a) or 0
    qp = q_ai_prob(a) or 0
    flags["ai_solution"] = sp > AI_THRESHOLD
    flags["ai_question"] = qp > AI_THRESHOLD
    flags["ai"] = flags["ai_solution"] or flags["ai_question"]

    # 3. structure: >=4 steps AND each step subheader separated by \n
    n_steps = len(sol)
    flags["too_few_steps"] = n_steps < 4
    flags["bad_subheader"] = any(("\n" not in s) or (not s.lstrip().startswith("#")) for s in sol)
    flags["structure"] = flags["too_few_steps"] or flags["bad_subheader"]

    # 4/5/6 partially captured via page grounding + logic; deeper factual checks need the filing.
    # Page grounding: compare pages cited in prose vs metadata.
    meta_pages = set(p for p in (m.get("page_numbers") or []) if isinstance(p, int))
    prose = " ".join(sol)
    prose_pages = set(int(x) for x in page_pat.findall(prose))
    flags["page_meta_empty"] = (not m.get("page_numbers")) or (None in (m.get("page_numbers") or []))
    flags["page_no_citation"] = len(prose_pages) == 0          # solution cites no page at all
    flags["page_prose_not_in_meta"] = bool(prose_pages - meta_pages)  # prose cites page absent from metadata
    flags["page_meta_not_in_prose"] = bool(meta_pages - prose_pages)  # metadata page never referenced
    flags["page"] = (flags["page_meta_empty"] or flags["page_no_citation"]
                     or flags["page_prose_not_in_meta"])

    # bookkeeping
    flags["humanized"] = m.get("humanization_attempts") is not None
    flags["humanization_attempts"] = m.get("humanization_attempts")
    flags["sol_prob"] = round(sp, 4)

    # overall client-ready?
    flags["client_ready"] = not (flags["logic"] or flags["ai"] or flags["structure"] or flags["page"])
    return flags


def main():
    data = json.load(open(DATA))
    rows = []
    for ri, r in enumerate(data):
        for ai_idx, a in enumerate(r["annotations"]):
            f = audit_one(a)
            f["_rec"] = ri
            f["_ann"] = ai_idx
            f["id"] = r["id"]
            f["company"] = r["company"]
            rows.append(f)

    n = len(rows)
    print(f"Total annotations: {n}\n")

    def cnt(key):
        return sum(1 for x in rows if x[key])

    print("=== Individual criteria (counts of annotations failing each) ===")
    for k in ["logic", "ai", "ai_solution", "ai_question", "structure", "too_few_steps",
              "bad_subheader", "page", "page_meta_empty", "page_no_citation",
              "page_prose_not_in_meta", "page_meta_not_in_prose"]:
        print(f"  {k:24} {cnt(k)}")

    ready = cnt("client_ready")
    print(f"\nCLIENT-READY (page=strict): {ready}   NOT-READY: {n-ready}")

    # Page definition is the disputed one — show counts under each interpretation
    print("\n=== Page-issue under different definitions ===")
    print(f"  meta empty/None only          : {cnt('page_meta_empty')}")
    print(f"  prose cites page not in meta  : {cnt('page_prose_not_in_meta')}")
    print(f"  solution cites NO page at all : {cnt('page_no_citation')}")
    print(f"  meta page never cited in prose: {cnt('page_meta_not_in_prose')}")

    # Cross-tab on the three substantive axes (logic / ai / page-strict)
    print("\n=== Cross-tab (logic, ai, page) among NOT-ready ===")
    c = Counter()
    for x in rows:
        if x["client_ready"]:
            continue
        c[(x["logic"], x["ai"], x["page"], x["structure"])] += 1
    print("  logic  ai     page   struct  count")
    for k, v in sorted(c.items(), key=lambda kv: -kv[1]):
        print(f"  {str(k[0]):6}{str(k[1]):6} {str(k[2]):6} {str(k[3]):6}  {v}")

    # Humanization reality among AI-flagged
    aih = [x for x in rows if x["ai"]]
    print(f"\n=== AI-flagged ({len(aih)}) humanization attempts ===")
    print("  attempts distribution:", dict(Counter(x["humanization_attempts"] for x in aih)))
    probs = sorted(x["sol_prob"] for x in aih)
    if probs:
        import statistics
        print(f"  sol prob: min {probs[0]:.2f} median {statistics.median(probs):.2f} max {probs[-1]:.2f}")
        print(f"  >=0.90: {sum(1 for p in probs if p>=0.9)}  0.5-0.9: {sum(1 for p in probs if 0.5<p<0.9)}")

    json.dump(rows, open("audit_results.json", "w"), indent=2)
    print("\nWrote audit_results.json")


if __name__ == "__main__":
    main()
