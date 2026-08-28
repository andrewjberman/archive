# ADVI_PERFRP TO-R1-DE — PRF-d-1 CONTROL CALLER CENSUS

**Author:** `0.4.0_DE_ClientPlatform~D` · **Measured at:** portal `@9957410e` (published on
`origin/DEV`, ls-remote read at this seat 2026-08-28 17:2xZ)
**Requested by:** `2.0.0_SA_COO` 78391 item 3, as an **acceptance READ**, not a monitor.
**Cell:** `PRF-d-1` · **Feeds:** `PRFR1DE-AC2` denominator.

---

## 0. Why this exists

The same defect shape hit this TO **twice**:

| # | control | built | wired | found by |
|---|---|---|---|---|
| 1 | CSV export (`PerfrpCsvExport` + `perfrpTableToCsvRows`) | yes, and a suite leg (L26) was GREEN over the projection | **no** — 0 production callers | a census, after the criterion's stated wait went stale |
| 2 | Manage Table (`PerfrpManageTable` + `usePerfrpColumnVisibility`) | yes | **no** — 0 call sites, 0 hook consumers | running the SAME census against the rest of the set |

⛔ **Neither was visible to any gate, because AN ABSENT BUTTON IS NOT AN ERROR.** Typecheck passes,
the suite passes, the render looks finished. The only instrument that sees it is a caller census,
so the census is written down here rather than remembered.

---

## 1. The census

Method: JSX use sites anywhere in `portal/src`, then resolve the chain to a mounted surface.

| control | JSX uses | reachability | verdict |
|---|---|---|---|
| `PerfrpPeriodPicker` | 1 | `PerfrpControlBar` → `PerfrpBookControlPanel` → `AdvisorBookView` | MOUNTED, read on render |
| `PerfrpLevelSwitch` | 1 | same chain | MOUNTED, read on render |
| `PerfrpGroupBy` | 1 | same chain | MOUNTED, read on render |
| `PerfrpExpandCollapse` | 1 | same chain | MOUNTED, read on render |
| `PerfrpManageTable` | 2 | `PerfrpColumnPicker` → roster + client table | MOUNTED `@9957410e` (was 0) |
| `PerfrpColumnPicker` | 2 | `PerfrpAccountRoster`, `PerfrpBookView` | MOUNTED, read on render |
| `PerfrpCsvExport` | 4 | roster, client table, control bar, shared table | MOUNTED, read on render |
| `PerfrpFootnotes` | 3 | `PerfrpBookView`, `PerfrpCardGrid` | MOUNTED, read on render |
| `PerfrpControlBar` | 1 | `PerfrpBookControlPanel` | MOUNTED |
| `PerfrpBookControlPanel` | 1 | `AdvisorBookView` | MOUNTED |
| `usePerfrpColumnVisibility` | 2 call sites | roster, client table | LIVE (was 0) |
| `PerfrpTable` | **0** | — | **UNMOUNTED — OPEN GAP** |
| `PerfrpPeriodUnavailable` | **0** | — | **UNMOUNTED — SUPERSEDED, not a gap** |

**Denominator: 13 exported controls/hooks. 11 mounted. 2 zeros.**

---

## 2. ⛔ A ZERO IS NOT A VERDICT — the two zeros take OPPOSITE verdicts

The census answers *"is anything calling this?"* It does **not** answer *"is there a hole?"* That
needs a second question — **is the behaviour otherwise served?** — and reporting both zeros as one
number would have manufactured a defect that does not exist.

- **`PerfrpTable` — REAL GAP.** Its purpose (the shared table behind the card tables and the L2
  list) is served by nothing else. It is correctly waiting on the DS `b-series` leaves. Its CSV
  wiring is therefore **preventive, not delivered to a reader** — and because `csvFilenameStem` is
  now a REQUIRED prop, the eventual mount **cannot** reintroduce a table without an export.
- **`PerfrpPeriodUnavailable` — SUPERSEDED.** The behaviour it exists to guarantee *is*
  implemented, inline, at the call site: `AdvisorBookClientDetail.tsx:189` renders
  *"Fee Summary has no decomposition for the selected period. Choose QTD or YTD to see it."*
  when `rfsWindow` is null. This is **dead code / duplication for the issuer to retire**, not a
  hole.

**EXERCISED, not argued.** `PERIOD_TO_LEGACY_WINDOW` maps `1Y / 3Y / SI / custom` → `null`.
Rendering L3 and selecting **Period 1Y** replaces the Fee Summary panel with that honest notice
instead of substituting a window — read on the PNG. That is `PRFR1DE-AC7`'s mechanism working on a
live surface.

---

## 3. ⛔ THE CENSUS INSTRUMENT WAS WRONG ON ITS FIRST RUN

My first version excluded the **defining module** from the search, to avoid counting definitions as
uses. That also excluded **intra-module composition** — so it reported **0 call sites** for
`PerfrpPeriodPicker`, `PerfrpLevelSwitch`, `PerfrpGroupBy` and `PerfrpExpandCollapse`: four
controls I had **just read on a render**, composed inside `PerfrpControlBar` in the same file.

Had I published it, it would have reported four false gaps in the same message that reported two
true ones — and the true ones would have been discounted with them.

> **A census that cannot see composition measures FILE BOUNDARIES, not wiring.**
> The correction is not "be careful": it is that the exclusion which makes a census precise about
> *definitions* is the same exclusion that makes it blind to *composition*. Count uses everywhere,
> then resolve the chain.

---

## 4. Second instrument trap, same session, worth the same warning

Exercising §2 I first ran `--click "1Y"`. It reported `CLICKED: 1Y`, `rc=0` — and landed on the
**Assets Overview** window toggle, a *different control with the same label*, while Performance
Controls still read QTD. **A silent wrong click is byte-identical to a successful one in the
harness output.** Only the re-run with `--clicktext '1Y#1'` (disambiguating by occurrence) is
evidence; the first run is discarded.

This is the trap the `--clicktext` flag's own comment already warned about, written by this lane —
and it still caught me, because the warning was about `--clicktext` and I was using `--click`.

---

## 5. Named open gaps against PRF-d-1 (recorded, not hidden behind a status)

1. **Manage Table presentation.** Mounted as the ruled MINIMUM — an inline column-visibility list
   off the existing hook. A richer picker (column ordering, persistence, popover) is **NEXT ROUND**.
   The presentation is an implementation decision explicitly **open to the issuer's revision at
   round close**, so the frozen spec's authority is intact.
2. **`PerfrpTable` unmounted.** See §2. Waiting on the producer, not on this lane.
3. **`PerfrpPeriodUnavailable` dead code.** Retire or wire — issuer's call, zero behavioural
   consequence either way.

---

## 6. The detector, for reuse

For every exported UI control in a cell, an acceptance row asserting **use sites > 0 on a surface
that is reachable from a mount** — plus, for every zero, the second question in §2. Not a monitor
(CLAUDE.md standing moratorium); a **criterion**. Routed to `3.0.0_SA_CVO` when that seat is live;
banked by `1.0.0_SA_CTO` (78389 item 3) and `2.0.0_SA_COO` (78391 item 3) meanwhile.
