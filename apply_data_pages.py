#!/usr/bin/env python3
"""Add genuine DATA-source pages that are cited (with a value) in the solution but
missing from metadata.page_numbers — and add the matching grounding element so the
page<->element pairing stays intact.

A prose page mention is a DATA citation (vs a navigational pointer) when a financial
value is stated next to it OR the stated figures appear on that page in the filing.
Only entries where EVERY missing prose page is a DATA citation are touched, so each
applied entry becomes client-ready. Navigational-only / ambiguous entries are left
for separate review.
"""
import json, re, sys

DATA = "Rainforest_860.json"
ROWS = "audit_results.json"

pg_pat = re.compile(r"\b(?:pages?|pg)\b\.?\s*(?:nos?\.?|numbers?|num|#)?\.?\s*(\d+)", re.I)
val_pat = re.compile(r"\$\s?\d|\b\d{1,3}(?:,\d{3})+|\b\d+(?:\.\d+)?\s?(?:million|billion|%)", re.I)

# grounding for page-figure verification (reuse remediate_pages helpers if present)
try:
    from remediate_pages import fetch_pdf, page_texts, salient_figures, fig_in_texts
    HAVE_PDF = True
except Exception:
    HAVE_PDF = False


def windows(sol, pg):
    # generous trailing window: the cited value often follows the page mention
    # by a clause ("...on page 42 where the 7/31/2022 value amounts to $257.30").
    pat = re.compile(r".{0,60}\b(?:pages?|pg)\b\.?\s*(?:nos?\.?|numbers?|num|#)?\.?\s*"
                     + str(pg) + r"\b.{0,90}", re.I)
    return pat.findall(sol)


def classify(sol, pg, grounds):
    data = grounds
    for w in windows(sol, pg):
        if val_pat.search(w):
            data = True
    return "DATA" if data else "OTHER"


def elem_for(sol, pg):
    for w in windows(sol, pg):
        if re.search(r"chart|graph", w, re.I):
            return "Chart"
    return "Table"


def rebuild(meta, adds):
    """adds: list of (page, elem). Merge into existing pairing, sort by page."""
    pn = meta.get("page_numbers") or []
    ge = meta.get("grounding_elements") or []
    pairs = list(zip(pn, ge))
    for p, e in adds:
        pairs.append((p, e))
    seen = {}
    order = []
    for p, e in pairs:
        if p not in seen:
            seen[p] = e
            order.append(p)
    order.sort()
    meta["page_numbers"] = order
    meta["grounding_elements"] = [seen[p] for p in order]


def main():
    apply = "--apply" in sys.argv
    data = json.load(open(DATA))
    rows = json.load(open(ROWS))
    targets = [r for r in rows if r["page"] and not r["logic"] and not r["ai"]
               and not r["structure"] and r["page_prose_not_in_meta"]]

    # optional filing grounding cache per doc
    ground_cache = {}

    def grounds(url, sol, pg):
        if not HAVE_PDF:
            return False
        try:
            if url not in ground_cache:
                doc = fetch_pdf(url)
                ground_cache[url] = page_texts(doc)
                doc.close()
            texts = ground_cache[url]
            figs = salient_figures(sol)
            # check page (printed pg-1 .. +11 window) for any figure
            for off in range(0, 12):
                idx = pg - 1 + off
                if 0 <= idx < len(texts) and any(fig_in_texts(f, texts, idx) for f in figs):
                    return True
        except Exception:
            return False
        return False

    applied = []
    skipped = []
    for r in targets:
        rec = data[r["_rec"]]
        ann = rec["annotations"][r["_ann"]]
        sol = " ".join(ann["solution"])
        meta = [p for p in (ann["metadata"].get("page_numbers") or []) if isinstance(p, int)]
        cited = sorted(set(int(x) for x in pg_pat.findall(sol)))
        extra = [p for p in cited if p not in meta]
        cls = {p: classify(sol, p, grounds(rec["doc_link"], sol, p)) for p in extra}
        if extra and all(v == "DATA" for v in cls.values()):
            adds = [(p, elem_for(sol, p)) for p in extra]
            applied.append((r["id"], r["_ann"], adds))
            if apply:
                rebuild(ann["metadata"], adds)
        else:
            skipped.append((r["id"], cls))

    print(f"Targets: {len(targets)}")
    print(f"DATA-only entries to flip ({len(applied)}):")
    for id_, ann_i, adds in applied:
        print(f"  {id_:14} add {adds}")
    print(f"\nLeft for review ({len(skipped)}): nav/ambiguous mentions")
    for id_, cls in skipped:
        print(f"  {id_:14} {cls}")

    if apply:
        json.dump(data, open(DATA, "w"), indent=2)
        mm = sum(1 for rr in data for a in rr["annotations"]
                 if len(a["metadata"]["page_numbers"]) != len(a["metadata"]["grounding_elements"]))
        print(f"\nAPPLIED {len(applied)} entries -> {DATA}. Pairing mismatches: {mm}")
    else:
        print("\nDRY RUN — re-run with --apply to write.")


if __name__ == "__main__":
    main()
