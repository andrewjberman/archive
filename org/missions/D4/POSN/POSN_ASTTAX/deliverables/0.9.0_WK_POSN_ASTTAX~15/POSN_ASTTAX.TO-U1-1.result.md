# POSN_ASTTAX.TO-U1-1 -- THE READER CENSUS AND THE FIVE-CLASS BAR

**Cell** `AT4-s-1` (round 4) - **Outcome** FWD-6 - **Worker** `0.9.0_WK_POSN_ASTTAX~15`
**Worktree** `C:/tmp/wk-posn-u1` branch `wk-posn_asttax-4-1` - **Date** 2026-09-13

**VINTAGES -- every citation in this document resolves to one of these two:**

| object | pin | how it was read |
|---|---|---|
| portal source | `e85f6eb84f` (the gitlink at this worktree's HEAD) | `git show e85f6eb84f:<path>` from the portal repo -- **by CONTENT, never from a working tree** |
| POSN_ASTTAX PRD v0.6 | `ae66157381` | `git show ae66157381:.../POSN_ASTTAX_PRD.md` |
| this worktree | `72f241749946d2956d03bee23e917dfe2305fcd5` | `git rev-parse HEAD` |

> ⛔ **WHY THE PORTAL WAS NOT READ FROM THE WORKING TREE.** The shared tree's portal checkout is at
> `30ca034bba` on branch `DEV` -- **14 commits BEHIND the gitlink pin** (`git rev-list --count
> HEAD..e85f6eb84f` = 14; `merge-base --is-ancestor e85f6eb84f HEAD` rc=1, with the positive control
> `--is-ancestor HEAD HEAD` rc=0 firing beside it). Reading those files and stamping them
> `@e85f6eb84f` would have been a citation false by 8 days and 126 files. Filed as
> `POSN_ASTTAX-Z-W15-S1`. **The finding did not change** -- measured, not assumed: the set of `src/`
> files matching the asset-class term is byte-identical at both commits (59 at the pin, 59 at the
> checkout, `comm` empty in both directions).

**THE PORTAL WAS NOT WRITTEN.** This cell produced a census and a price. Zero bytes under `portal/`
were modified in either tree.

---

## THE FIVE RATIFIED CLASSES

Read from the PRD at `ae66157381` s.3 *"The five classes -- the ratified taxonomy (BINDS the
decomposition)"*, not retyped from the order:

| # | class | color | holds |
|---|---|---|---|
| 1 | Fixed Income / Cash | green | fixed income and cash |
| 2 | Equity | blue | equities only -- volatility and hedge REMOVED to Structured |
| 3 | Structured | pink | options, VIX futures, volatility overlays, VXX and the like |
| 4 | Commodities | gold | physical (gold, nickel, silver), crypto, commodity indices |
| 5 | Alternatives | orange | real assets (not commodities), PE, private credit, real estate |

---

## U1-AC1 -- THE READER SET, BY SUBTRACTION, WITH ITS DENOMINATOR

### The census, denominator printed

```
comp-find [content] 'assetClass'            (run in the portal repo, --all --files)
  DENOMINATOR: 580 hit(s) across 1048 file(s) scanned in scope [corpus=all]
             | 39207 EPHEMERAL-FLOOR, NOT searched | 89 BINARY, NOT searched
  BANDS: DEF=46 SURFACED=359 CONFIG=2 DOC=173        PAGE 1 of 1 (showing 56 of 56)

comp-find [content] 'asset[_ -]?class' -i   (the UNSCOPED widening -- Rule 24)
  DENOMINATOR: 1636 hit(s) across 1048 file(s) scanned in scope [corpus=all]
  BANDS: HEAD=36 DEF=99 SURFACED=774 CONFIG=42 DOC=685   PAGE 1 of 1 (showing 144 of 144)
```

⚠ **`comp-find` runs against the WORKING TREE, which is not the pin.** So the census was re-run at
the pin itself and every number below is a pin-time number:

```
git ls-tree -r --name-only e85f6eb84f            -> 1201 files in the tree
git ls-tree -r --name-only e85f6eb84f -- src     ->  557 files under src/
  of which .ts/.tsx/.js/.jsx/.css                ->  484 CODE files   <- the domain
```

### The subtraction -- written as denominator MINUS what is excluded, never as a forward list

| step | rule applied | count |
|---|---|---|
| **DOMAIN** | src/ code files at `e85f6eb84f` | **484** |
| minus | no match for `asset[_ -]?class` **and** no match for any of the five ratified class literals | -395 |
| = | **candidates** | **89** |
| minus | carries no multi-class vocabulary anywhere in a 6-line window -- a file that never names two class concepts near each other cannot enumerate a taxonomy | -43 |
| = | **vocabulary carriers** | **46** |
| minus | **not a renderer**: no JSX and no value reaching the DOM (type unions, API contracts, config, colour registries, adapters) | -23 |
| minus | **not this taxonomy**: the match is a MARKET-DATA segmentation (`'equities' \| 'fixedIncome' \| 'commodities'` keyed on INDEX names via `dataLoader.ts:289 getAssetClass(indexName)`), a FACTOR-TILT description (`'Equity vs Fixed Income'`), or marketing prose -- none groups a HOLDING by class | -12 |
| = | **THE READER SET** | **11** |

> ⛔ **THE FILTER THAT WOULD HAVE LOST THE ANSWER, DISCLOSED BECAUSE IT NEARLY DID.** The first cut
> of the vocabulary filter required two class concepts **on ONE line** and returned 38 files.
> Widening it to a 6-line window returned 46 -- **and the 8 it recovered included
> `src/lib/chartColors.ts`, the colour registry EVERY Positioning/Attribution/CMA reader imports,
> and `PerfrpAllocation.tsx`, the single reader that PASSES all five.** Both write one class per
> line, so the single-line filter could not match them by construction. A vocabulary is not a line;
> it is a block, and a one-line instrument silently subtracts exactly the shared dependency Rule 22
> says to check on its own.

### The reader set -- 11 renderers, 4 surface families

| id | surface family | file @ `e85f6eb84f` |
|---|---|---|
| A1 | **Positioning** (PRD S3 surface 1) | `src/pages/Positioning/tabs/HoldingsTab.tsx` |
| A2 | **Positioning** | `src/pages/Positioning/panels/PositioningSummary.tsx` |
| B1 | **Philosophy/CMA** (PRD S3 surface 2) | `src/pages/CapitalMarketAssumptions/components/AssumptionsTable.tsx` |
| B2 | **Philosophy/CMA** | `src/pages/CapitalMarketAssumptions/tabs/ExpectationsTab.tsx` |
| B3 | **Philosophy/CMA** | `src/pages/CapitalMarketAssumptions/tabs/OpalViewsTab.tsx` |
| C1 | **Attribution** -- *named by no PRD surface row* | `src/pages/Attribution/tabs/SelectionTab.tsx` |
| C2 | **Attribution** | `src/pages/Attribution/components/AssetAllocationSummary.tsx` |
| C3 | **Attribution** | `src/pages/Attribution/components/StylePolicyComparison.tsx` |
| D1 | **AdvisorIntelligence** -- *named by no PRD surface row* | `src/pages/AdvisorIntelligence/_shared/perfrp/PerfrpAllocation.tsx` |
| D2 | **AdvisorIntelligence** | `src/pages/AdvisorIntelligence/_shared/components/PartnerAnalytics.tsx` |
| D3 | **AdvisorIntelligence** | `src/pages/AdvisorIntelligence/_shared/panels/ConsolidatedOverviewPanel.tsx` |
| S* | **SHARED DEPENDENCY beneath A1, A2, B2, C2, C3** -- graded separately, not a reader | `src/lib/chartColors.ts` |

**MY SET HAS ELEVEN MEMBERS, NOT TWO, SO THE "how did you exclude the third" CLAUSE DOES NOT BIND.**
The order's premise was that the world holds *at least three*. It holds at least eleven, across
**four** surface families -- and the two families the PRD's `C-TWO-SURFACES` never names
(**Attribution**, **AdvisorIntelligence**) hold **6 of the 11**. Filed as `POSN_ASTTAX-Z-W15-S2`.

**The PRD's disclosed non-owned ETF publisher was SUBTRACTED, with its proof:**
`infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py` is a **data
producer, not a renderer** -- it emits JSON, owns no DOM, and appears in no row of the table below.
Its disclosure in the PRD cites *"source lines 469-472"*; at this worktree's HEAD those lines are
inside `serve_s3_json_nocache()` and the class vocabulary is at `:1012-1034`/`:1491-1492`. Filed as
`POSN_ASTTAX-Z-W15-S3`.

---

## U1-AC2 -- WHAT EACH READER CAN SAY, IN ITS OWN BYTES

Every line below was re-read at `e85f6eb84f` by the grader at run time (`.scratch/grade_five_class.py`,
`cite()`), not transcribed.

```
A1  src/pages/Positioning/tabs/HoldingsTab.tsx
    :1392  const assetClassOrder = ['Fixed Income', 'Equity']
    :215   const ASSET_CLASS_COLORS: Record<string, string> = {      (keys: Fixed Income, Equity, Cash)
    :1381  const displayClass =                                      (:1382-83 Cash->Fixed Income, Hedge->Equity)

A2  src/pages/Positioning/panels/PositioningSummary.tsx
    :124   const isColoredRow = ['Fixed Income (%)', 'Equity (%)'].includes(rowLabel)
    :545   { label: 'Fixed Income (%)', values: getFixedIncomeValues(), unit: '' },
    :546   { label: 'Equity (%)', values: getEquityValues(), unit: '' },

B1  src/pages/CapitalMarketAssumptions/components/AssumptionsTable.tsx
    :5      * - Collapsible category headers (Cash, Fixed Income, Equities, Alternatives, Commodities)
    :104   {groupedAssumptions.map(({ category, items }, _groupIndex) => {     (data-driven)
    -- constrained upstream by  CapitalMarketAssumptions/types.ts:10
       category?: 'Cash' | 'Fixed Income' | 'Equities' | 'Alternatives' | 'Commodities'

B2  src/pages/CapitalMarketAssumptions/tabs/ExpectationsTab.tsx
    :97    const CATEGORY_COLORS: Record<string, string> = {
    :99      'Fixed Income': ASSET_CLASS.fixedIncome,
    :100     'Equities': ASSET_CLASS.equity,
    :102     'Commodities': ASSET_CLASS.alternatives,
    :105   const DEFAULT_COLOR = ASSET_CLASS.alternatives

B3  src/pages/CapitalMarketAssumptions/tabs/OpalViewsTab.tsx
    :136   label={labelKey === 'pair' ? (view as { pair: string }).pair : (view as { assetClass: string }).assetClass}
    -- NO VOCABULARY AT ALL: free text straight from the payload.

C1  src/pages/Attribution/tabs/SelectionTab.tsx
    :321   const assetClassOrder = ['Fixed Income', 'Equity']
    :322   const orderedGroups = assetClassOrder

C2  src/pages/Attribution/components/AssetAllocationSummary.tsx
    :92    const requiredAssetClasses = ['Fixed Income', 'Equity']
    :94    return requiredAssetClasses.map(name => {

C3  src/pages/Attribution/components/StylePolicyComparison.tsx
    :156   const requiredAssetClasses = ['Fixed Income', 'Equity']
    :158   return requiredAssetClasses.map(name => {

D1  src/pages/AdvisorIntelligence/_shared/perfrp/PerfrpAllocation.tsx
    :36     * Display labels for the classes we can name. A class NOT in this map still renders --
    :41    const CLASS_LABELS: Readonly<Record<string, string>> = {   (equity, fixed_income, alternatives, cash)
    :48    function classLabel(assetClass: string): string {
    :54    return assetClass                                          (raw-token fallback)

D2  src/pages/AdvisorIntelligence/_shared/components/PartnerAnalytics.tsx
    :1644  equity: 'Equity', fixed_income: 'Fixed Income',
    :1645  alternatives: 'Alternatives', cash: 'Cash',
    -- fed by composition.ts:32  CANONICAL_CLASSES = ['equity', 'fixed_income', 'alternatives']
       and composition.ts:100    if (!classes.includes(item.asset_class)) continue

D3  src/pages/AdvisorIntelligence/_shared/panels/ConsolidatedOverviewPanel.tsx
    :399   {['cash', 'fixed_income', 'equity', 'alternatives']

S*  src/lib/chartColors.ts   -- THE SHARED COLOUR REGISTRY
    :112   /** Asset class colors used across Positioning, Attribution, and heatmaps */
    :113   export const ASSET_CLASS = {
    :114     fixedIncome:  PALETTE.green500,
    :115     equity:       PALETTE.blue500,
    :116     cash:         PALETTE.amber500,
    :117     alternatives: PALETTE.orange500,
    :118     realEstate:   PALETTE.orange500,
    :119     other:        PALETTE.gray500,
    :308   'Commodities':            PALETTE.blue950,     <- inside the EQUITY blue gradient
```

---

## U1-AC3 -- THE READER x CLASS TABLE

**Bar: can that class reach the screen on that reader?** Not "do the readers agree" -- they agree
today because four of them carry a byte-identical wrong two-class list.

```
READER                                    Fixed Incom    Equity  Structured Commodities Alternative
-----------------------------------------------------------------------------------------------
A1 Positioning > Holdings table                  PASS      PASS        FAIL        FAIL        FAIL
A2 Positioning > Summary panel                   PASS      PASS        FAIL        FAIL        FAIL
B1 CMA > Assumptions table                       PASS      PASS        FAIL        PASS        PASS
B2 CMA > Expectations scatter                    PASS      PASS        FAIL        PASS        PASS
B3 CMA > Opal Views                              PASS      PASS        PASS        PASS        PASS
C1 Attribution > Selection holdings              PASS      PASS        FAIL        FAIL        FAIL
C2 Attribution > Asset Allocation Summary        PASS      PASS        FAIL        FAIL        FAIL
C3 Attribution > Style vs Policy                 PASS      PASS        FAIL        FAIL        FAIL
D1 AI > Perfrp allocation card                   PASS      PASS        PASS        PASS        PASS
D2 AI > Partner analytics mix                    PASS      PASS        FAIL        FAIL        PASS
D3 AI > Consolidated overview                    PASS      PASS        FAIL        FAIL        PASS
-----------------------------------------------------------------------------------------------
[shared dep] chartColors.ts ASSET_CLASS          PASS      PASS        FAIL        FAIL        PASS
-----------------------------------------------------------------------------------------------
PASS per class (of 11 readers)                  11/11     11/11        2/11        4/11        6/11

DENOMINATOR: 11 readers x 5 classes = 55 cells  |  PASS 34  FAIL 21
```

### Controls -- the table discriminates on BOTH axes

- **NEGATIVE CONTROL, as required: `Equity`, the class expected to PASS on every reader. 11/11 PASS
  -> the control FIRES.**
- **CONTRAST: `Structured` passes 2/11.** The table is not uniform, so the instrument discriminates
  **across classes**.
- **READERS PASSING ALL FIVE: 2/11 -- `B3 CMA > Opal Views` and `D1 AI > Perfrp allocation card`.**
  So the instrument also discriminates **across readers**. Both pass for the same reason and it is
  the reason worth carrying into `AT4-s-2`: **they carry no vocabulary.** B3 renders
  `view.assetClass` as free text; D1's `classLabel()` at `:48-54` falls back to the producer's raw
  token, under an explicit docstring at `:36-39` -- *"A class NOT in this map still renders ...
  Absence is the one outcome this card may not produce."* **The readers that cannot break are the
  ones that never enumerated the taxonomy.**

### The mechanism per failing cell

| mechanism | sites | cells |
|---|---|---|
| **hardcoded two-class literal** `['Fixed Income','Equity']` | `HoldingsTab.tsx:1392`, `SelectionTab.tsx:321`, `AssetAllocationSummary.tsx:92`, `StylePolicyComparison.tsx:156` | 12 |
| **hardcoded two-row table body** | `PositioningSummary.tsx:545-546` | 3 |
| **hardcoded inline array** `['cash','fixed_income','equity','alternatives']` | `ConsolidatedOverviewPanel.tsx:399` | 2 |
| **type union** excluding `Structured` | `CapitalMarketAssumptions/types.ts:10` | 2 |
| **drop filter** `if (!classes.includes(item.asset_class)) continue` | `composition.ts:100` over `CANONICAL_CLASSES` at `:32` | 2 |
| **two-key-short colour map** (no `structured`, no `commodities`) | `chartColors.ts:113-120` | 2 |

⛔ **`HoldingsTab.tsx:1392` AND `SelectionTab.tsx:321` ARE THE SAME LINE OF CODE ON TWO DIFFERENT
PAGES.** Round 2 measured the Positioning one (`W11-S1`). The Attribution twin has never been named
by a POSN cell, because no surface row reaches Attribution.

⛔ **AND AT `:1394` THE FAILURE IS SILENT BY CONSTRUCTION:** `.filter(ac => groupedHoldings[ac])`.
A group keyed `Structured` / `Commodities` / `Alternatives` is not rendered *and does not error* --
the row renders nowhere while its weight stays in the grand total. That is the exact defect the file
documents for `Cash` at `:1364-1374` (PROD v2.1.167: PFDE 90 -> 89 rows, subtotals 99.98 under a
grand total of 100.01). **The 2026-06 remedy folded only `Cash` and `Hedge`, so a retag reproduces
it with a new value.**

### Two FWD-4 observations the FWD-6 bar cannot fail on -- recorded, not graded

1. `chartColors.ts:308` colours `'Commodities'` as `PALETTE.blue950` -- **a shade of EQUITY blue**,
   inside the block commented *"Equity -- Blue gradient"*. Ratified colour is gold.
2. `ExpectationsTab.tsx:102` maps `'Commodities'` to `ASSET_CLASS.alternatives` (orange), and
   `:105 DEFAULT_COLOR` is the same orange -- so on the CMA scatter, Commodities, Alternatives and
   any unrecognised category are **the same pixel colour**. Commodities passes FWD-6's "can it reach
   the screen" and fails FWD-4's "one colour, not one another class uses" on the same cell.

---

## U1-AC4 -- THE PRICE, PER FAILURE, WITH THE FREEZE BOUNDARY MARKED

**23 failing (reader, class) rows** -- 21 across the 11 readers, plus 2 on the shared colour
registry graded separately. They collapse to **9 distinct edit sites**:

| # | smallest change that would let it render | file:line @ `e85f6eb84f` | boundary |
|---|---|---|---|
| 1 | extend the two-class literal to the five ratified classes in canonical order | `portal/src/pages/Positioning/tabs/HoldingsTab.tsx:1392` | **FROZEN** |
| 2 | emit a row per ratified class instead of two hardcoded rows | `portal/src/pages/Positioning/panels/PositioningSummary.tsx:545` | **FROZEN** |
| 3 | extend the two-class literal (twin of #1) | `portal/src/pages/Attribution/tabs/SelectionTab.tsx:321` | **FROZEN** |
| 4 | extend `requiredAssetClasses` to the five | `portal/src/pages/Attribution/components/AssetAllocationSummary.tsx:92` | **FROZEN** |
| 5 | extend `requiredAssetClasses` to the five | `portal/src/pages/Attribution/components/StylePolicyComparison.tsx:156` | **FROZEN** |
| 6 | add `'Structured'` to the `CMACategory` union (fixes B1 **and** B2) | `portal/src/pages/CapitalMarketAssumptions/types.ts:10` | **FROZEN** |
| 7 | add `structured` + `commodities` keys to `CANONICAL_CLASSES` (fixes D2) | `portal/src/pages/AdvisorIntelligence/_shared/lib/composition.ts:32` | **FROZEN** |
| 8 | extend the inline rendered array | `portal/src/pages/AdvisorIntelligence/_shared/panels/ConsolidatedOverviewPanel.tsx:399` | **FROZEN** |
| 9 | add `structured` (pink) + `commodities` (gold) keys to `ASSET_CLASS` | `portal/src/lib/chartColors.ts:113` | **FROZEN** |

```
TOTAL failing (reader,class) rows : 23
FROZEN (under portal/)            : 23
OWNED  (outside portal/)          : 0
DISTINCT EDIT SITES               :  9 across 9 file(s) -- ALL under portal/
```

> ⛔ **EVERY ROW IS FROZEN. THERE IS NO OWNED PATH TO A FIVE-CLASS SCREEN.**
> This is the number for the freeze decision: **9 files, 9 lines, 0 of them outside `portal/`.**
> No amount of work on the classifier, the DynamoDB registry, or the lambdas moves any cell of the
> table above -- the data would arrive correctly tagged and **9 of 11 readers would still not show
> it.** Site #9 (`chartColors.ts:113`) is the one with leverage beyond its own row: it is imported
> by A1, A2, B2, C2 and C3, so it is a shared dependency whose repair is a precondition for the
> *colour* half of FWD-4 across five readers at once, and whose omission would leave every repaired
> reader rendering the two new classes in `PALETTE.gray500`.
>
> ⚠ **AND THE PRICE ABOVE IS THE RENDER PRICE ONLY.** It is not a safety price. `C-RETAG-SAFETY`
> holds the retag at NO-GO for reasons upstream of every line in this table, and nothing here
> weakens that. A reader repaired at these 9 sites would display five classes; whether the *weights*
> behind them are right is `AT3-s-5`'s question, not this cell's.

---

## U1-AC5 -- THE HONEST GRAIN

```
$ timeout 120 python -c "print('COVERAGE STATED, NOT REALIZATION')"
COVERAGE STATED, NOT REALIZATION
```

**THIS CELL COVERS FWD-6. IT DOES NOT SERVE IT, AND FWD-6 IS NOT GRADED REALIZED.**

The reason is the grain, not modesty. FWD-6's DONE WHEN is **EXERCISED** -- *"the Positioning view
and the combined Philosophy / Capital-Market-Assumptions view have each been read and both show the
same classes"*. Every piece of evidence in this document is **SOURCE-AT-PIN**: bytes resolved by
`git show e85f6eb84f:<path>`. The portal is frozen, no build was run, and **this worker has no
rendered DOM** -- so it cannot reach EXERCISED by construction, and the criteria were cut to that
grain deliberately rather than cut unsatisfiable. DESIRED != APPLIED != EXERCISED. Covering and
serving are different populations.

**What this cell DOES establish, at the grain it can:** the bar fails in today's world (9 of 11
readers, 21 of 55 cells), it would pass only after a change to the world, and the change is priced.

---

## U1-AC6 -- JUDGMENT (readings only; graded by `3.0.0_SA_CVO~Z` at L9)

*Whether the reader set derived in AC1 is genuinely the set that renders an asset-class label, or
merely the set reachable with the instruments at hand.* **No verdict is offered.**

**READINGS FOR THE GRADE:**

1. **The instrument is a TEXT MATCH, and a renderer that names no class cannot be found by it.**
   B3 and D1 are in the set only because they matched `assetClass` as an identifier -- had either
   been written with a differently-named variable and no class literal, neither census term would
   have reached it. The set is bounded by vocabulary, and the two readers that PASS are precisely
   the ones with the least vocabulary. **The instrument is weakest exactly where the world is
   healthiest.**
2. **The subtraction from 46 to 11 rests on two judgments, not measurements.** (a) "not a renderer"
   -- decided by reading for JSX and DOM-reaching values, not by rendering anything. (b) "not this
   taxonomy" -- 12 files were excluded as market-data segmentation, factor-tilt descriptions or
   prose. **If (b) is wrong about even one file, the reader count rises.** Both are stated so they
   can be overturned.
3. **The AdvisorIntelligence family (D1-D3) may or may not be one population with Positioning.**
   Its data arrives on a different lineage -- `api/endpoints/advisor-intelligence.ts:1536`
   *"4-bucket from Orion native classifier (INF_D_03 lineage)"* -- over advisor books, not Yang
   model portfolios. It renders a portfolio asset-class breakdown, which is why it is in the set;
   whether FWD-6 is graded over it is a scope question this worker does not hold and did not decide.
   Three of the 21 failing cells and 2 of the 9 edit sites are D-family.
4. **D1 and D3 have same-family siblings that were NOT graded.**
   `AdvisorAnalytics.tsx`, `InflectionInsightsPanel.tsx` and the four `_partners/*/layout.ts`
   `ordered:` arrays all carry the same 3/4-class vocabulary. They were left out because they
   duplicate D2/D3's mechanism, not because they were proven not to render. **11 is a floor.**
5. **`dist/` was excluded without argument.** The census reached 5 built bundles under
   `portal/dist/assets/`. They are build OUTPUT of the same source, so they add no reader -- but
   they are also the only artifacts in the corpus that are closer to what a browser executes than
   source is, and **no served-plane read was taken by this cell at all.**
6. **The count moved once already, in the direction of MORE.** PRD S3 says two; the round-3 analysis
   says at least three; this census says eleven across four families. Each widening came from a
   wider instrument, never from new code. **A seventh reading is that the next instrument widens it
   again** -- nothing here establishes that eleven is closed.
7. **One class of reader is structurally invisible to this cell: a non-portal renderer.** The census
   domain was `portal/src`. The PRD's disclosed ETF publisher was found and subtracted as a producer,
   but that subtraction was made by reading ONE non-portal file, not by censusing the non-portal
   estate for renderers. **The claim "all 9 edit sites are FROZEN" is therefore true of the domain
   searched, and the domain searched was the portal.**

---

## CONTROLS

| control | method | result |
|---|---|---|
| **Determinism** | grader run twice, output byte-compared | `md5 f731e3ba0f6bf7c7cf553296a7d3c9f6` both runs -- **STABLE** |
| **Mutant** | `cite()` asked for the two-class literal at the cited line (:1392) and at three lines that do not carry it (:1391, :1393, :1400), plus one out-of-range line | positive True; three negatives False; out-of-range `None` -- **FIRED-AS-EXPECTED**; the citations read real bytes rather than echoing the table |
| **Negative control (AC3, required)** | `Equity` predicted to PASS on every reader | 11/11 PASS -- **FIRES** |
| **Discrimination** | contrast class + all-pass readers | `Structured` 2/11; 2 of 11 readers pass all five -- table **not uniform on either axis** |
| **Vintage control** | pin-vs-checkout hit sets compared | 59 files at `e85f6eb84f`, 59 at `30ca034bba`, `comm` empty both directions -- **the 14-commit gap changes nothing in this cell** |

## SURPRISE ROWS FILED

| id | class / hazard | one line |
|---|---|---|
| `POSN_ASTTAX-Z-W15-S1` | OBSERVATION / **ARMED** (`2.0.0_SA_COO~Z`) | the shared portal checkout is 14 commits behind the gitlink pin, so the instructed read would have produced a false vintage |
| `POSN_ASTTAX-Z-W15-S2` | OBSERVATION / **ARMED** (`1.0.0_SA_CTO~Z`) | `C-TWO-SURFACES` binds the decomposition to two surfaces; the world holds 11 renderers across 4 families |
| `POSN_ASTTAX-Z-W15-S3` | OBSERVATION / INERT | the disclosed ETF publisher's cited lines do not resolve at HEAD, and it nests `structured_notes` under `alternatives` |
| `POSN_ASTTAX-Z-W15-S4` | OBSERVATION / **ARMED** (`2.0.0_SA_COO~Z`) | this TO's `<proof_of_spec>` block names an instance path the L6 gate cannot resolve -- the gate derives the name from the FULL TO filename stem (`to-pipeline-gate.py:1603`), and 11 of 11 sibling instances in this project already use it |

**TWO ENVIRONMENT CONDITIONS MET ON THE WAY TO THE COMMIT, BOTH ALREADY BANKED, NEITHER RE-FILED.**
The Rule-14 commit gate cannot import its modules in a cone-mode sparse worktree -- that is this
project's own `POSN_ASTTAX-Z-W2-S3`, and its banked remedy was applied verbatim: `git archive HEAD
org/modules/graph` into `.scratch/`, plus `PYTHONPATH` for the `safe-commit` call only. **No
sparse-checkout change and no repo path materialized** -- `git status --porcelain -- org/modules`
stayed at 0 lines throughout. Recorded here rather than as a new row because an existing ARMED row
already carries the class; what that row's remedy does NOT name, and this one needed, is **two
further path entries**: `org/modules/graph/compproof` (for `log_open_lint`) and `.tools` (for
`git_bash_resolver`, `msys_argv_guard`).

## VERDICT

**THE FIVE-CLASS BAR FAILS.** 9 of 11 readers cannot display all five ratified classes; 21 of 55
reader-class cells FAIL; `Structured` reaches 2 of 11 readers and `Commodities` 4 of 11. The two
readers that pass do so by carrying no vocabulary at all. The full price is **9 edit sites, all of
them FROZEN under `portal/`, none OWNED** -- so no work outside the portal can move this bar.
**FWD-6 is COVERED by this cell and is NOT graded REALIZED.**
