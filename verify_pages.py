#!/usr/bin/env python3
"""Phase-1 pipeline PILOT: verify pages cited in a solution against the source 10-K.

For a page-only entry, the solution names pages that aren't in metadata.page_numbers.
We fetch the filing, then for each cited page confirm grounding two ways:
  (a) printed-page mapping: does the PDF's physical layout label that page?
  (b) value check: do the dollar/number tokens stated near the citation appear on
      that page (allowing a small physical<->printed offset)?
Outputs a proposed corrected page_numbers set + a confidence note. No data is mutated.
"""
import json, re, sys, urllib.request, io
import fitz  # pymupdf

page_pat = re.compile(r"pages?\s+(\d+)", re.I)
# numbers like 1,234 or 1,234.5 or 251,400 — the figures solutions cite
num_pat = re.compile(r"\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b")


def fetch_pdf(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(req, timeout=40).read()
    return fitz.open(stream=data, filetype="pdf")


def printed_to_physical(doc):
    """Map printed page label (int found bottom/standalone) -> physical index."""
    m = {}
    for i in range(doc.page_count):
        txt = doc[i].get_text()
        # last standalone number on the page is often the printed folio
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        for l in lines[-3:]:
            if l.isdigit():
                m.setdefault(int(l), i)
    return m


def verify_entry(rec, ann, doc):
    sol = " ".join(ann["solution"])
    cited = sorted(set(int(x) for x in page_pat.findall(sol)))
    meta = sorted(set(p for p in (ann["metadata"].get("page_numbers") or []) if isinstance(p, int)))
    extra = [p for p in cited if p not in meta]
    p2phys = printed_to_physical(doc)
    results = []
    for pg in extra:
        # candidate physical pages: exact printed match, else printed +/- small offset guesses
        cands = []
        if pg in p2phys:
            cands.append(("printed-label", p2phys[pg]))
        for off in range(0, 12):
            idx = pg - 1 + off  # filings often offset by cover/TOC
            if 0 <= idx < doc.page_count:
                cands.append((f"phys+{off}", idx))
        # which figures does the solution state near this page mention?
        figs = num_pat.findall(sol)
        best = None
        for label, idx in cands:
            ptext = doc[idx].get_text()
            hits = sum(1 for f in set(figs) if f in ptext)
            if best is None or hits > best[2]:
                best = (label, idx, hits)
        results.append({"printed_page": pg, "best_match": best[0],
                         "physical_idx": best[1], "figure_hits": best[2],
                         "n_figs_in_sol": len(set(figs))})
    return {"id": rec["id"], "company": rec["company"], "cited": cited,
            "meta": meta, "extra": extra, "pdf_pages": doc.page_count,
            "checks": results}


def main():
    data = json.load(open("Rainforest_860.json"))
    rows = json.load(open("audit_results.json"))
    po = [r for r in rows if r["page"] and not r["logic"] and not r["ai"] and not r["structure"]]
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    for r in po[:n]:
        rec = data[r["_rec"]]
        ann = rec["annotations"][r["_ann"]]
        print("=" * 70)
        try:
            doc = fetch_pdf(rec["doc_link"])
            out = verify_entry(rec, ann, doc)
            print(f"{out['id']}  {out['company'][:34]}  ({out['pdf_pages']}pp)")
            print(f"  metadata pages : {out['meta']}")
            print(f"  cited in prose : {out['cited']}   -> unlogged: {out['extra']}")
            for c in out["checks"]:
                conf = "HIGH" if c["figure_hits"] >= 2 else ("LOW" if c["figure_hits"] == 0 else "MED")
                print(f"    page {c['printed_page']}: {c['figure_hits']}/{c['n_figs_in_sol']} stated figures "
                      f"found on physical idx {c['physical_idx']} ({c['best_match']})  -> grounding {conf}")
            doc.close()
        except Exception as e:
            print(f"  ERROR {r['id']}: {e}")


if __name__ == "__main__":
    main()
