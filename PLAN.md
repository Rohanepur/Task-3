# Automated Power BI → Excel Model Refresh

## Goal

Eliminate the manual data-handling around a client (mining, Utah) Power BI model
while keeping the analysis in a transparent, auditable, consulting-style Excel
workbook. Replace three manual steps with a scheduled job that runs on the VM
that already holds the Power BI permissions.

## Problems being solved

1. **Tedious manual re-update.** Today: download the bulky source Excel, copy-paste
   into the formula workbook. → Automate the data refresh into the workbook.
2. **Views missing from the Excel.** Some views only exist in Power BI and are
   pulled by hand. → Query the semantic model directly so every view comes along.
3. **Refresh trapped on a privileged account.** Today: refresh on a special
   account, zip, email to Bain, download. → Run the extractor *on the VM* that
   already has the permissions; the email/zip chain disappears.

## Design principles

- **Excel stays the brain.** All business logic lives in visible Excel formulas
  (`INPUT → CALC → OUTPUT → DASHBOARD`). That chain is the audit trail. Python
  carries no business logic — it only moves data.
- **Auditable at two levels.** Within a run, trace formulas cell-by-cell. Across
  runs, every refresh saves a dated snapshot + a log, so number movements are
  diffable.
- **Fluid.** Analysts tweak logic in Excel, never in code.
- **Lean inputs.** Targeted DAX pulls only needed columns/rows — fixes the "bulky"
  workbook complaint.

## Architecture

```
ON THE VM (Windows, Excel + Power BI access)

  Power BI semantic model
        |  targeted DAX queries
        v
  Extractor (Python)
        |  writes into INPUT tables via xlwings
        v
  THE WORKBOOK  (your model, unchanged)
    - INPUT_*    Excel Tables; data lands here
    - CALC_*     your formulas (audit trail)
    - OUTPUT_*   final tables
    - DASHBOARD  charts off OUTPUT
        |  recalc + refresh + save
        v
  /snapshots/YYYY-MM-DD.xlsx   dated copy per run
  /logs/run.log                query, row counts, timestamp

  Task Scheduler runs it on a cadence.
```

## Extraction method (decide on the VM by license tier)

- **Premium / PPU / Fabric** → XMLA endpoint. Full DAX, no real row limits.
  Tools: `pyadomd`, or `sempy` if Fabric.
- **Pro only** → Power BI REST `executeQueries`. Works, but ~100k rows/query, so
  chunk the large tables.

## Excel write strategy

- **`xlwings`** (primary) drives real Excel on the VM: preserves formulas, charts,
  formatting; triggers real recalc; refreshes pivots; saves.
- **`openpyxl`** (fallback only) if Excel isn't available — riskier with rich
  workbooks, no recalc.
- Data lands in **named Excel Tables (ListObjects)** so formulas reference them by
  structured/named ref and never break when row counts change.

## Open items to confirm on the VM

1. **License tier** of the workspace — Premium/PPU/Fabric vs Pro (→ XMLA vs REST).
2. **Access level** — does Bain own/admin the model or only read it.
3. **Table sizes** — how bulky, for chunking + storage decisions.
4. **The formula workbook** — needed to map INPUT/CALC/OUTPUT tabs and the named
   ranges the extractor must target.

## Phasing

1. **Spike** — one DAX query against the model returns rows on the VM. Proves
   access end-to-end. (~half day)
2. **Extractor** — pull all needed tables, including PBI-only views, into the
   INPUT tables.
3. **Wire-up** — point the formula model's inputs at the INPUT tables; validate
   OUTPUT matches the current dashboard numbers exactly.
4. **Snapshots + logging** — dated copy and run log each refresh.
5. **Schedule + hand off** — Task Scheduler job; surface failed refreshes.

## Out of scope (for now)

- Moving the dashboard to Power BI or a web app. Excel output chosen for
  auditability and team adoption; revisit later if needed.
