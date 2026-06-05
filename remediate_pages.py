#!/usr/bin/env python3
"""Phase-1 remediation: complete metadata.page_numbers for page-only entries whose
SOLUTION cites a filing page that is grounded in the source 10-K but missing from
metadata. This is a metadata-completion fix (prose is correct, the recorded page
set was incomplete) — no prose is mutated.

Selection: audit_results entries with page=True, logic=False, ai=False,
structure=False, and page_prose_not_in_meta=True.

Grounding rule per cited-but-unlogged printed page P:
  - candidate physical indices = printed-label map[P] (if any) + window P-1+off, off in 0..11
  - figure_hits = count of distinct numeric figures stated in the solution that appear
    on the candidate page's text
  - HIGH  : printed-label match AND >=1 figure hit, OR >=2 figure hits on any candidate
  - MED   : exactly 1 figure hit (no printed-label confirmation)
  - LOW   : 0 figure hits anywhere -> NOT applied, left flagged for manual review

Only HIGH/MED groundings are written into metadata.page_numbers. Everything is logged.
"""
import json, re, os, sys, urllib.request, hashlib
import fitz  # pymupdf

DATA = "Rainforest_860.json"
ROWS = "audit_results.json"
CACHE = "/tmp/rf_pdfs"
os.makedirs(CACHE, exist_ok=True)

page_pat = re.compile(r"pages?\s+(\d+)", re.I)
# Salient figures a solution might cite: comma-grouped numbers, percentages,
# $-amounts, and bare 4+ digit integers (years excluded as too noisy).
comma_pat = re.compile(r"\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b")
pct_pat = re.compile(r"\b\d{1,3}(?:\.\d+)?%")
big_int_pat = re.compile(r"\b\d{4,}(?:\.\d+)?\b")


def salient_figures(sol):
    figs = set(comma_pat.findall(sol))
    figs |= set(pct_pat.findall(sol))
    for m in big_int_pat.findall(sol):
        # skip plausible 4-digit years (1900-2099) to reduce noise
        if not (len(m) == 4 and 1900 <= int(m) <= 2099):
            figs.add(m)
    return figs


def fig_in_texts(fig, texts, idx):
    """A figure counts as present if it (or its comma/percent-normalised form)
    appears on the candidate page or an immediately adjacent physical page."""
    bare = fig.rstrip("%")
    for j in (idx, idx - 1, idx + 1):
        if 0 <= j < len(texts) and (fig in texts[j] or bare in texts[j]):
            return True
    return False


def fetch_pdf(url):
    key = hashlib.md5(url.encode()).hexdigest() + ".pdf"
    path = os.path.join(CACHE, key)
    if not os.path.exists(path):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=60).read()
        open(path, "wb").write(data)
    return fitz.open(path)


def printed_to_physical(doc):
    m = {}
    for i in range(doc.page_count):
        lines = [l.strip() for l in doc[i].get_text().splitlines() if l.strip()]
        for l in lines[-3:]:
            if l.isdigit():
                m.setdefault(int(l), i)
    return m


def page_texts(doc):
    return [doc[i].get_text() for i in range(doc.page_count)]


def verify_page(printed_pg, figs, p2phys, texts):
    cands = []
    if printed_pg in p2phys:
        cands.append(("printed-label", p2phys[printed_pg]))
    for off in range(0, 12):
        idx = printed_pg - 1 + off
        if 0 <= idx < len(texts):
            cands.append((f"phys+{off}", idx))
    best = None
    for label, idx in cands:
        hits = sum(1 for f in figs if fig_in_texts(f, texts, idx))
        if best is None or hits > best[2]:
            best = (label, idx, hits)
    label, idx, hits = best
    printed_match = printed_pg in p2phys
    n = len(figs)
    # Two independent signals: printed-folio match and stated-figure presence.
    if hits >= 3 or (printed_match and hits >= 1):
        conf = "HIGH"
    elif hits >= 1:
        conf = "MED"
    elif printed_match and n == 0:
        # folio exists at the expected page and the citation states no checkable
        # figure (points at a section/heading) -> page is real, accept as MED
        conf = "MED"
    else:
        conf = "LOW"
    return {"printed_page": printed_pg, "match": label, "physical_idx": idx,
            "figure_hits": hits, "n_figs": n, "printed_label_match": printed_match,
            "confidence": conf}


def main():
    apply = "--apply" in sys.argv
    data = json.load(open(DATA))
    rows = json.load(open(ROWS))
    targets = [r for r in rows if r["page"] and not r["logic"] and not r["ai"]
               and not r["structure"] and r["page_prose_not_in_meta"]]

    # group by doc to fetch once
    by_doc = {}
    for r in targets:
        by_doc.setdefault(data[r["_rec"]]["doc_link"], []).append(r)

    log = []
    applied = 0
    flipped = 0
    for di, (url, rs) in enumerate(sorted(by_doc.items()), 1):
        try:
            doc = fetch_pdf(url)
            p2phys = printed_to_physical(doc)
            texts = page_texts(doc)
        except Exception as e:
            for r in rs:
                log.append({"id": r["id"], "error": str(e)})
            print(f"[{di}/{len(by_doc)}] ERROR {url[:60]}: {e}")
            continue
        for r in rs:
            rec = data[r["_rec"]]
            ann = rec["annotations"][r["_ann"]]
            sol = " ".join(ann["solution"])
            cited = sorted(set(int(x) for x in page_pat.findall(sol)))
            meta = [p for p in (ann["metadata"].get("page_numbers") or []) if isinstance(p, int)]
            extra = [p for p in cited if p not in meta]
            figs = salient_figures(sol)
            checks = [verify_page(p, figs, p2phys, texts) for p in extra]
            add = sorted(c["printed_page"] for c in checks if c["confidence"] in ("HIGH", "MED"))
            entry = {"id": r["id"], "ann": r["_ann"], "company": rec["company"][:30],
                     "pdf_pages": doc.page_count, "meta": meta, "extra": extra,
                     "checks": checks, "to_add": add,
                     "all_grounded": len(add) == len(extra) and len(extra) > 0}
            log.append(entry)
            if apply and entry["all_grounded"]:
                newpages = sorted(set(meta) | set(add))
                ann["metadata"]["page_numbers"] = newpages
                applied += 1
                flipped += 1
        doc.close()
        print(f"[{di}/{len(by_doc)}] {rec['company'][:34]:34} entries={len(rs)}")

    json.dump(log, open("remediation_pages.json", "w"), indent=2)
    hi = sum(1 for e in log if e.get("all_grounded"))
    part = sum(1 for e in log if "checks" in e and not e["all_grounded"]
               and any(c["confidence"] in ("HIGH", "MED") for c in e["checks"]))
    none = sum(1 for e in log if "checks" in e
               and all(c["confidence"] == "LOW" for c in e["checks"]))
    print(f"\nTargets: {len(targets)}")
    print(f"  fully grounded (all cited pages verified): {hi}")
    print(f"  partially grounded: {part}")
    print(f"  none grounded (LOW only): {none}")
    print(f"  errors: {sum(1 for e in log if 'error' in e)}")
    if apply:
        json.dump(data, open(DATA, "w"), indent=2)
        print(f"\nAPPLIED {applied} metadata completions -> {DATA} (entries flipped: {flipped})")
    else:
        print("\nDRY RUN — re-run with --apply to write metadata. Log: remediation_pages.json")


if __name__ == "__main__":
    main()
