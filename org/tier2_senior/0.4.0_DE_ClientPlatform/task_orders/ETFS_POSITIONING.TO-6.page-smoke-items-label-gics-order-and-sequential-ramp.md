# TO ETFS_POSITIONING.TO-6 — Andrew's page smoke: the label, canonical GICS ordering, and the sequential colour ramp

**Issued:** 2026-08-24T23:35Z by `2.0.0_SA_COO~Z`
**Executor class:** DE (frontend) — `0.4.0_DE_ClientPlatform~Z`
**Basis:** **ANDREW-DIRECT ~23:2xZ** (visual smoke of the live page), relayed verbatim by
`1.0.0_SA_CTO~Z` (5760). Covers his **items 4, 5, 6**.
**Runs in parallel with** the 13:00Z provenance/conventions work — **this TO touches no producer.**

## HIS WORD, the clauses this TO covers

```
"Also don't need "# of ETFs" on frontend, should be "# of Securities". Also still need to figure out
GICS + order by canonical Sector/GICS ordering (see how the frontend handles it in "Portfolio
Management" (Yang was very adamant on how secrots should be ordered), then this order should be
lighter to darker in color on the "Sub-Asset" Field."
```

## Not in this TO

**Item 1** (DIVZ/IDVZ holdings) needs nothing — T-1 = Friday; they populate at the 13:00Z fire.
**Item 2** (performance) is **NOT a build** — `history_topup` IS feeding, the series is 2 days deep,
and `0/114` on WTD+ is the producer's own documented correct output. **Routed to Andrew as a
spend fork, not to a lane.**
**Item 3** (yield) resolved by read — the nulls are non-payers.

---

## THE ITEM-5 LANDSCAPE — THREE LISTS, measured by `0.4.0_DE_ClientPlatform~Z` (5829)

> **SUPERSEDES my own first read.** I issued this TO naming TWO lists and located the trap on the
> ordering mechanism. **DE~Z found a THIRD, and it is the one with a proven ordering consumer** — so
> my trap is real but fires on the FILTER list, not on the ordering path. Their measurement governs.

```
1. SECTORS          PortfolioManagement/constants.ts   "Sector list for filtering"
     Technology / Healthcare / ...        CONSUMERS: 0 (COO~Z found, DE~Z reproduced)
     -> WRONG SPELLING on our two biggest buckets. The trap is REAL and it is on THIS list.
2. SECTOR_INDICES   lib/dataLoader.ts:236            CANONICAL GICS ASCENDING, 11 names
     CONSUMERS: dataLoader:290, :352
     -> SPELLING MATCHES THE ETF DATA EXACTLY (`Health Care`, `Information Technology`).
        NAME-KEYED: no bridge needed.
3. ECONOMY_ORDER    PortfolioManagement/constants.ts:104   numeric codes
     [25, 45, 40, 10, 15, 20, 50, 35, 30, 55, 60, 65, 90, 95]
     CONSUMERS: TradeTab.tsx:255-262 (SORTS), utils/factorOrder.ts:6 (mirrors)
     -> THIS IS PM'S ACTUAL ORDERING BEHAVIOUR -- what Andrew pointed at.
```
**PM sorts by numeric `economy` code and pairs `economyName` FROM THE DATA, so the ordering path
never touches a sector-name string** — which is why the `Technology`/`Healthcare` collision cannot
fire there. **Correct trap, wrong list to fear it on.**

## ⛔ THE FORK — ANDREW'S OWN SENTENCE CARRIES BOTH HALVES AND THEY PULL APART

```
"order by canonical Sector/GICS ordering"                  -> SECTOR_INDICES (GICS ascending)
"see how the frontend handles it in Portfolio Management
 (Yang was very adamant on how sectors should be ordered)" -> ECONOMY_ORDER  (a chosen sequence)
```
**`ECONOMY_ORDER` starts 25, 45, 40, 10 — deliberately NOT ascending. `SECTOR_INDICES` is textbook
GICS. These are different orders and only one can be built.**
⚠ **AND THE COST RUNS THE WRONG WAY: `SECTOR_INDICES` is nearly free (name-keyed, exact spelling);
`ECONOMY_ORDER` needs a sector-name -> code bridge that DOES NOT EXIST and is UNVERIFIED** (PM's own
header says *"Yang's original economy names and codes, no GICS remapping"* — **do not assume
45 = Information Technology**). **The cheap option is the one that may be the wrong order, which is
exactly when a seat picks it and calls it reuse.**
>> **CARDED TO ANDREW. DE~Z reads the second half as governing — "adamant" only means something if
the order is not the obvious one — and I forward that reading AT THEIR STRENGTH: a reading of his
words, not a determination. AC2 is discharged by HIS ANSWER, cited; not by either of us picking.**
⛔ **THE LABEL CRITERION DOES NOT WAIT ON THIS FORK — execute it now. This TO is not a hold on the
label, and treating the fork as one would be a gate nobody asked for.**

## TWO THINGS THAT BIND WHICHEVER ORDER WINS (DE~Z)

- **`ALL` and `Other` are UI sentinels, not sectors — never colour-ramp a sentinel.**
- **`Cash & Cash Equivalents` (4 rows) and the `None` row (TPG) are not GICS sectors** and appear in
  neither ordered list. **PM's own convention is `indexOf === -1 -> 999`, i.e. sorted last** — a
  reusable answer rather than a new one (build-ladder rung 2).

---

## Acceptance criteria

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **`POS-TO6-AC1`** | **`# of ETFs` reads `# of Securities`.** MEASURED: exactly ONE render site, `portal/src/pages/Positioning/panels/PositioningSummary.tsx` (the `label:` in the summary rows; a second occurrence is a comment). ⛔ **And per `ETFS-f-3`, Models mode must stay BYTE-IDENTICAL** — this panel is shared. | `ETFS-f-1, ETFS-f-3` | **SOURCE + rendered** |
| **`POS-TO6-AC2`** | **The PM page's ACTUAL sector ordering behaviour is LOCATED and cited** (`file:line @ commit-ish`), not inferred from a constant's name. **If it is `SECTORS`, say what consumes it; if nothing does, say that.** | `ETFS-d-2` | **SOURCE** |
| **`POS-TO6-AC3`** | ⛔ **The vocabulary bridge is EXPLICIT and EXERCISED on the two differing names.** Show `Information Technology` and `Health Care` landing in their intended positions — **not in `Other`.** | `ETFS-d-2` | **EXERCISED** |
| **`POS-TO6-AC4`** | **Sub-Asset renders a SEQUENTIAL light→dark ramp over the ordered axis.** Reuse the located ordering — **rung 2, do not re-coin an ordering or a palette.** | `ETFS-d-2` | **EXERCISED (rendered)** |
| **`POS-TO6-AC5`** | **The unlabelled bucket is handled deliberately.** `sub_asset_class: None` is **1 row — `2602335D` / TPG Inc**, the known four-symptom row. It must not silently take a ramp colour that implies a sector. | `ETFS-d-2` | **EXERCISED** |
| **`POS-TO6-AC6`** | ⛔ **NEGATIVE CONTROL: a sector with ZERO rows.** `Real Estate` is in both lists and **absent from today's data**. Show the ramp does not shift or mis-colour when a member of the ordered axis has no rows — **a ramp computed over PRESENT values instead of the DECLARED axis changes every colour whenever a sector empties.** | `ETFS-d-2` | **EXERCISED (fixture)** |

> **AC6 is the load-bearing one.** A ramp built from the sectors that happen to be present looks
> perfect today and **re-colours the entire column the first day a sector drops out** — and nobody
> would attribute that to the ramp.

## Standing constraints

- **Your categorical-colour ruling is NOT overturned** — you ruled against **categorical** colour
  over ~24 **unordered** values against an 8-slot palette, and that reasoning was right. He is
  specifying a **sequential ramp over an ORDERED axis**, a different encoding that tolerates many
  values precisely because order carries the meaning. **Your analysis is out of scope for what he
  asked, not wrong.**
- **Your own measured constraints still bind:** the **4-site blast radius** and the
  `getSubAssetTextColor` **8-entry allowlist**.
- **No producer changes.** This TO is frontend only and must not collide with the 13:00Z work.
- **`Real Estate` absent and `None`=1 are FIELDS, not defects.** Do not "fix" the data from here.
- **No alarms, monitors, SES or freshness checkers** (standing moratorium).

<proof_of_spec>
  <!-- ISSUANCE half (COO~Z). POSITIONAL — no --expected-criteria flag:
         python .tools/proof-of-spec-check.py <instance>.json POS-TO6-AC1,POS-TO6-AC2,POS-TO6-AC3,POS-TO6-AC4,POS-TO6-AC5,POS-TO6-AC6
       CHECK THE RC, NEVER THE OUTPUT STRING; take it WITHOUT A PIPE. Coverage diff is BIDIRECTIONAL.
       The checker's `firm` enum still has no ETFS value — enter FABRIC and DECLARE it, as on
       ETFS_INGEST TO-2/TO-4/TO-7. Routed to CTO~Z as gate owner; neither of us edits a gate.
       AC2 may resolve to "nothing consumes SECTORS" — that is a PASS with a finding, not a fail. -->
  <criterion id="POS-TO6-AC1" cell_refs="ETFS-f-1, ETFS-f-3"/>
  <criterion id="POS-TO6-AC2" cell_refs="ETFS-d-2"/>
  <criterion id="POS-TO6-AC3" cell_refs="ETFS-d-2"/>
  <criterion id="POS-TO6-AC4" cell_refs="ETFS-d-2"/>
  <criterion id="POS-TO6-AC5" cell_refs="ETFS-d-2"/>
  <criterion id="POS-TO6-AC6" cell_refs="ETFS-d-2"/>
  <expected_criteria>POS-TO6-AC1,POS-TO6-AC2,POS-TO6-AC3,POS-TO6-AC4,POS-TO6-AC5,POS-TO6-AC6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/ETFS_POSITIONING.TO-6_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## How CTO~Z's zero missed item 5 — recorded because it generalises

`comp-find -i "SECTOR_ORDER|sectorOrder|SECTOR_SEQUENCE|canonicalSector"` over `portal/src` = **0
hits across 415 files.** Both constants are named for their **content** (`SECTORS`,
`SECTOR_INDICES`), and the ordering lives in **array position** — **so no identifier could ever have
carried it.** Both were found by searching for the **data** (`"Information Technology"`, 5 hits over
395 files, case-sensitive so a FLOOR). **A pattern that cannot match returns a clean, true zero, and
the only reason anyone kept looking is that CTO~Z flagged their own zero as untrustworthy.**
