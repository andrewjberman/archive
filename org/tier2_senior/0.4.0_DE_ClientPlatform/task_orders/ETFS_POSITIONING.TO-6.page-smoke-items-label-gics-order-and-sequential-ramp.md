# TO ETFS_POSITIONING.TO-6 — Andrew's page smoke: the label, canonical GICS ordering, and the sequential colour ramp

<status>complete -- all 6 criteria PASS, exercised; proof-of-spec VALID rc=0, 6 rows, 0 violations.
Portal DEV @de32bacb (build) + @36599dec (Andrew's two colour corrections).

**`<status>` TAG ADDED 2026-08-28 ~07:5xZ by `2.0.0_SA_COO~Z` (issuer). THE VERDICT IS UNCHANGED;
ONLY THE CARRIER IS.** This TO recorded its state ONLY as a prose `**Status:** COMPLETE` header,
which `to-check.py` cannot read -- **so it appeared in NO class: not ACTIVE, not PENDING, not even
`[??]`. It was absent from the board's DENOMINATOR entirely**, and every in-scope count this office
reported tonight was short by it. The prose header is preserved below.</status>


**Issued:** 2026-08-24T23:35Z by `2.0.0_SA_COO~Z`
**Executor class:** DE (frontend) — `0.4.0_DE_ClientPlatform~Z`
**Basis:** **ANDREW-DIRECT ~23:2xZ** (visual smoke of the live page), relayed verbatim by
`1.0.0_SA_CTO~Z` (5760). Covers his **items 4, 5, 6**.
**Runs in parallel with** the 13:00Z provenance/conventions work — **this TO touches no producer.**
**Status:** COMPLETE -- all 6 criteria PASS, exercised. Portal DEV @de32bacb (build) + @36599dec
(Andrew's two colour corrections), LANDED LOCAL, on no remote branch; DE commits portal, DT pushes.
proof-of-spec VALID rc=0, 6 rows, 0 violations.

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

## ✅ THE FORK IS ANSWERED — ANDREW-DIRECT ~23:44Z. **AC3–AC6 ARE RELEASED.**

```
"If you have access to economy code for these securities we can order based on that instead of
GICS, i really dont care if its official gics or some general economy/sector thing, whatever we
can get."
```

⭐ **WE DO HAVE IT AND IT COSTS NOTHING NEW.** `ECONOMY_ORDER` **is GICS codes** (its own comment,
`constants.ts:103`: *"Canonical sector/economy ordering (GICS codes)"*), and our `sub_asset_class`
values are GICS sector NAMES already pulled in `GICS_SECTOR_NAME`. **`1.0.0_SA_CTO~Z` mapped it:
10 of 10 of our sectors resolve.** No new Bloomberg field, no second source.

### THE RULED ORDERING CONTRACT (`1.0.0_SA_CTO~Z`, on Andrew's word)

1. **Sort key = `GICS_SECTOR_NAME` → GICS code → `ECONOMY_ORDER.indexOf(code)`.** Matches PM's actual
   behaviour (`TradeTab.tsx:255-262, :286-287`), **so a user moving between Models and ETFs sees ONE
   order** — which is what his pointing at PM was for.
2. ⛔ **THE MAP IS A DECLARED CONSTANT, NOT AN INFERENCE.** 11 rows, in code, testable. **Never
   derive a code from a name at runtime by string-munging.** ⛔ **And key it on the spelling OUR DATA
   USES** — `Health Care`, `Information Technology` (i.e. `SECTOR_INDICES`' spelling, **NOT**
   `SECTORS`' `Healthcare`/`Technology`). **That is the collision, arriving where it actually
   matters.**
3. **`Cash & Cash Equivalents` and unmapped values APPEND AFTER the ten, DECLARED.** `ECONOMY_ORDER`
   carries trailing `65, 90, 95` which are not GICS sectors — **if those have known meanings in PM,
   USE them (rung 2); if not, append and say so.** ⛔ **Do NOT invent a code for Cash to make the
   sort uniform. An identifier that means nothing is worse than a declared exception.**
4. **The `None` row (TPG) sorts LAST and stays VISIBLY unlabelled.** It is a real defect with an
   owner — **hiding it inside a sort order is the safe-and-invisible conversion we keep refusing.**

**Item 6's dependency on item 5 is DISCHARGED.** Ramp technique and colour families from the Models
ramp (`SUB_ASSET_CLASS_COLORS`), ORDER from (1). **Two inputs, still not a port** — the key sets do
not overlap, so it is a new table built to the same construction rule.

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

> ⛔ **POST-VALIDATION CORRECTION 00:41Z — `AC5` AND `AC4` WERE BOTH DEFECTIVE AS I WROTE THEM.**
> Andrew found two colour defects **after** my 6/6 validation. Recorded as **PASSED-WITH-FINDING**,
> not silently re-passed, and the defects were in the CRITERIA:
>
> **`AC5` was a PROHIBITION where the requirement was DISCRIMINABILITY.** I wrote *"must not silently
> take a ramp colour that implies a sector."* `0.4.0_DE_ClientPlatform~Z` complied **exactly** — and
> the existing colour **was** `ASSET_CLASS_COLORS['Equity']`, so an **unclassified** row rendered in
> the identical tone of a **classified** one. **A prohibition constrains the ARTIFACT; the property
> that matters lives in the READER.** It should have read: ***"an unclassified row must be visually
> DISTINGUISHABLE from every classified one — shown."*** *(Fixed at `36599dec`: `gray900`, **5.2×
> darker by relative luminance**, a dark NEUTRAL **off the ramp**, so it cannot read as "the last
> sector." That is discriminability, and it is stronger than a darker blue.)*
>
> **`AC4`'s "EXERCISED (rendered)" GROUNDING WAS UNSOUND** — it was discharged by the author
> rendering and reading their own work, which is **self-comparison on the one axis the author is
> least able to see.** ⛔ **A colour or layout claim cannot be discharged by its author. Name a
> DIFFERENT renderer, or state the claim is unverifiable at this seat.** *(Also caught: ramp index 4
> resolved to `PALETTE.blue500`, which **IS** `ASSET_CLASS.equity` — the IDENTICAL hex, not a
> near-miss. No criterion forbade a ramp step colliding with an asset-class chip, and I would not
> have thought to write one.)*
>
> ⭐ **THE CLASS, three instances on this page in one night:** a correct **null** indistinguishable
> from a fetch failure · a correct **fallback** indistinguishable from a styling gap · a correct
> **unclassified** row indistinguishable from a classified one. **The value is right and the reader
> cannot tell it from a different meaningful state — and NO GATE IN THIS ESTATE CAN SEE ANY OF IT.**

> **AC6 is the load-bearing one.** A ramp built from the sectors that happen to be present looks
> perfect today and **re-colours the entire column the first day a sector drops out** — and nobody
> would attribute that to the ramp.

## Standing constraints

- **Your categorical-colour ruling is NOT overturned** — you ruled against **categorical** colour
  over ~24 **unordered** values against an 8-slot palette, and that reasoning was right. He is
  specifying a **sequential ramp over an ORDERED axis**, a different encoding that tolerates many
  values precisely because order carries the meaning. **Your analysis is out of scope for what he
  asked, not wrong.**
- ⛔ **THE RAMP'S SUCCESS CONDITION IS WHAT TRIGGERS THE FAILURE — `0.4.0_DE_ClientPlatform~Z`,
  5878, binding on AC4+AC5:** *"a light→dark ramp GENERATES LIGHT VALUES BY CONSTRUCTION, and
  `getSubAssetTextColor` (`chartColors.ts:307-313`) picks text colour from an 8-entry allowlist — any
  new light step omitted ships WHITE-ON-LIGHT, invisible to grep and to typecheck, visible only in a
  render."* **Updating that allowlist is PART OF THE CHANGE, NOT A FOLLOW-UP.**
  ⚠ **No instrument in the commit path can see this** — typecheck passes, grep passes. **Which is
  why AC4's grounding is EXERCISED (rendered) and must never be discharged from SOURCE.**
- **The 4-site blast radius** you measured still binds.
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
