#!/usr/bin/env python3
"""Repair the page_numbers <-> grounding_elements 1:1 pairing.

The earlier metadata-completion pass added pages to metadata.page_numbers but
did not extend grounding_elements, desyncing the index-wise pairing (each
page_number is paired with the grounding element — "Table"/"Chart" — that the
data was read from). This rebuilds the pairing for every annotation that differs
from the pre-remediation backup, inferring the element type for each added page
from the solution prose (Chart if it describes a chart/graph at that page, else
Table — the dominant type for financial-statement data pulls).
"""
import json, re

DATA = "Rainforest_860.json"
BAK = "/tmp/Rainforest_860.bak.json"


def elem_for_page(sol, pg):
    """Infer the grounding element type for a page from nearby prose."""
    pat = re.compile(r".{0,80}\b(?:pages?|pg)\b\.?\s*(?:nos?\.?|numbers?|num|#)?\.?\s*"
                     + str(pg) + r"\b.{0,40}", re.I)
    for w in pat.findall(sol):
        if re.search(r"chart|graph", w, re.I):
            return "Chart"
    return "Table"


def main():
    data = json.load(open(DATA))
    bak = json.load(open(BAK))
    fixed = 0
    for r, rb in zip(data, bak):
        for a, ab in zip(r["annotations"], rb["annotations"]):
            cur = a["metadata"].get("page_numbers")
            old = ab["metadata"].get("page_numbers")
            if cur == old:
                continue
            old_ge = ab["metadata"].get("grounding_elements") or []
            old_pn = [p for p in (old or [])]
            pairs = list(zip(old_pn, old_ge))  # correct original pairing
            have = set(old_pn)
            sol = " ".join(a.get("solution") or [])
            for p in cur:
                if p not in have:
                    pairs.append((p, elem_for_page(sol, p)))
                    have.add(p)
            # dedupe by page (keep first), sort by page ascending
            seen = {}
            for p, e in pairs:
                seen.setdefault(p, e)
            ordered = sorted(seen.items())
            a["metadata"]["page_numbers"] = [p for p, _ in ordered]
            a["metadata"]["grounding_elements"] = [e for _, e in ordered]
            fixed += 1
    json.dump(data, open(DATA, "w"), indent=2)

    # verify
    mm = sum(1 for r in data for a in r["annotations"]
             if isinstance(a["metadata"].get("page_numbers"), list)
             and isinstance(a["metadata"].get("grounding_elements"), list)
             and len(a["metadata"]["page_numbers"]) != len(a["metadata"]["grounding_elements"]))
    print(f"Rebuilt pairing for {fixed} annotations. Remaining length mismatches: {mm}")


if __name__ == "__main__":
    main()
