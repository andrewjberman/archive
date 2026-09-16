# POSN_ASTTAX.TO-U2-1 -- ONE COLOUR PER CLASS, THE SAME COLOUR EVERYWHERE

**Cell** `AT4-s-2` (round 4) - **Outcome** FWD-4 - **Worker** `0.9.0_WK_POSN_ASTTAX~18`
**Worktree** `C:/tmp/wk-posn-u2` branch `wk-posn_asttax-4-2` - **Date** 2026-09-13

**VINTAGES -- every citation in this document resolves to one of these three:**

| object | pin | how it was read |
|---|---|---|
| portal source | `e85f6eb84f` (the gitlink at this worktree's HEAD) | `git show e85f6eb84f:<path>` -- **by CONTENT, never from a working tree** |
| POSN_ASTTAX PRD v0.6 | `ae66157381` | `git show ae66157381:.../POSN_ASTTAX_PRD.md` |
| this worktree | `e622962cf53e51f9791ced0744f7adbf7de2325c` | `git rev-parse HEAD` |

> ⛔ **THE PORTAL WAS NOT WRITTEN. ZERO BYTES.** The portal is FROZEN by Andrew's word and this
> order's `<paths>` grant holds no portal path. This cell produced a census and a price.

> **WHY THE WORKING TREE WAS NOT READ, re-measured at this worker's own grain.** The shared tree's
> `portal/` checkout is at `30ca034bba`; the gitlink at this worktree's HEAD is `e85f6eb84f`
> (`git ls-tree e622962cf5 portal` -> `160000 commit e85f6eb84f3a...`). `git diff --name-only`
> between them = **126 files**, and `src/App.tsx` hashes differ (`8621071d` vs `31408870`) -- so the
> **negative control on the vintage instrument FIRES**. Of the 12 files cited in this document,
> **0 of 12 differ** between the two commits, so the finding below is vintage-stable. That is a
> MEASUREMENT, not an assumption, and it does not license reading the working tree: every citation
> here was taken by `git show` at `e85f6eb84f`. (Hazard `POSN_ASTTAX-Z-W15-S1`.)

---

## THE DOMAIN -- INHERITED, NOT DERIVED

`AT4-s-1` is terminal (`TO-U1-1` `<status>complete</status>`). **Its reader census IS the denominator
of this cell and was not re-derived and not widened.** Source:

```
org/missions/D4/POSN/POSN_ASTTAX/deliverables/0.9.0_WK_POSN_ASTTAX~15/
  POSN_ASTTAX.TO-U1-1.derive-the-readers-and-grade-the-five-class-bar.proof_of_spec.json
  POSN_ASTTAX.TO-U1-1.result.md
```

**11 readers across 4 surface families**, subtracted from **484 `src/` code files** at the pin, plus
**1 shared dependency** (`src/lib/chartColors.ts`) that the census marks explicitly as *"graded
separately, not a reader"*. This cell honours that: the shared registry is enumerated in full but is
**not** counted as a reader in any uniqueness or agreement grade.

**The five ratified classes and their agreed colours**, read from the PRD at `ae66157381` s.3 (not
retyped from the order): Fixed Income / Cash = **green**, Equity = **blue**, Structured = **pink**,
Commodities = **gold**, Alternatives = **orange**. `C-FIVE-CLASSES` binds the decomposition to them.

**FWD-4 has TWO clauses and both were graded.** From the PRD endpoint block:
> `DONE WHEN` APPLIED -- the agreed color for each class is used on every place that shows the classes
> `ACCEPT` **The same class is the same color everywhere it appears**, and **no place shows a class
> in a color another uses for something else.**

---

## U2-AC1 -- EVERY PER-CLASS COLOUR BINDING

**Invocation:** `timeout 300 python .scratch/grade_one_colour.py`
**DENOMINATOR: 11 of 11 readers in the AT4-s-1 census, plus 1 shared dependency graded separately.**
**62 binding rows. 94 citations RE-READ AT THE PIN at run time. 0 anchor mismatches.**

Every cited line is re-read by `cite(path, lineno, anchor)` at execution time and checked against an
anchor string; a transcription error prints `<<< ANCHOR MISMATCH` instead of passing silently.

### Kinds

| kind | meaning |
|---|---|
| **NAMED** | an explicit key for that class maps to that colour |
| **SUBASSET** | the key exists only at SUB-ASSET grain, nested under a DIFFERENT class |
| **FALLBACK** | no key for the class; it reaches a catch-all colour |
| **NONE** | this reader binds no colour to any class -- colour is not a function of class there |

### The (reader, class, colour token) table

| reader | class | kind | token | hex | definition site @ `e85f6eb84f` |
|---|---|---|---|---|---|
| A1 | Fixed Income / Cash | NAMED | green500 | `#10b981` | `HoldingsTab.tsx:216` `'Fixed Income': ASSET_CLASS.fixedIncome` |
| A1 | Fixed Income / Cash | NAMED | **amber500** | `#f59e0b` | `HoldingsTab.tsx:218` `'Cash': ASSET_CLASS.cash` |
| A1 | Equity | NAMED | blue500 | `#3b82f6` | `HoldingsTab.tsx:217` |
| A1 | Structured | FALLBACK | gray500 | `#6b7280` | `HoldingsTab.tsx:231` `|| PALETTE.gray500` |
| A1 | Commodities | **SUBASSET** | **blue950** | `#172554` | `chartColors.ts:308` via `HoldingsTab.tsx:222` |
| A1 | Alternatives | FALLBACK | gray500 | `#6b7280` | `HoldingsTab.tsx:231` |
| A2 | Fixed Income / Cash | NAMED | green500 | `#10b981` | `PositioningSummary.tsx:70`, used `:91` |
| A2 | Equity | NAMED | blue500 | `#3b82f6` | `PositioningSummary.tsx:71`, used `:92` |
| A2 | Structured / Commodities / Alternatives | FALLBACK | *transparent* | n/a | `PositioningSummary.tsx:95` `return 'transparent'` |
| B1 | all five | **NONE** | -- | -- | `AssumptionsTable.tsx:120` every header `text-white` |
| B2 | Fixed Income / Cash | NAMED | green500 | `#10b981` | `ExpectationsTab.tsx:99` |
| B2 | Fixed Income / Cash | NAMED | green500 | `#10b981` | `ExpectationsTab.tsx:98` `'Cash': ASSET_CLASS.fixedIncome` |
| B2 | Equity | NAMED | blue500 | `#3b82f6` | `ExpectationsTab.tsx:100` |
| B2 | Structured | FALLBACK | **orange500** | `#f97316` | `ExpectationsTab.tsx:105` `DEFAULT_COLOR = ASSET_CLASS.alternatives` |
| B2 | **Commodities** | NAMED | **orange500** | `#f97316` | `ExpectationsTab.tsx:102` `'Commodities': ASSET_CLASS.alternatives` |
| B2 | Alternatives | NAMED | orange500 | `#f97316` | `ExpectationsTab.tsx:101` |
| B3 | all five | **NONE** | -- | -- | `OpalViewsTab.tsx:213` every `<option>` shares `SURFACE.dropdown` |
| C1 | Fixed Income / Cash | NAMED | green500 | `#10b981` | `holdings-shared.tsx:68`, called `SelectionTab.tsx:359` |
| C1 | Fixed Income / Cash | NAMED | **amber500** | `#f59e0b` | `holdings-shared.tsx:70` |
| C1 | Equity | NAMED | blue500 | `#3b82f6` | `holdings-shared.tsx:69` |
| C1 | Structured | FALLBACK | gray500 | `#6b7280` | `holdings-shared.tsx:109` |
| C1 | Commodities | **SUBASSET** | **blue950** | `#172554` | `holdings-shared.tsx:101` via `SelectionTab.tsx:374` |
| C1 | Alternatives | FALLBACK | gray500 | `#6b7280` | `holdings-shared.tsx:109` |
| C2 | FI / Cash, Equity | NAMED | green500 / amber500 / blue500 | | `holdings-shared.tsx:68-70`, used `AssetAllocationSummary.tsx:206` |
| C2 | Structured / Commodities / Alternatives | FALLBACK | gray500 | `#6b7280` | `AssetAllocationSummary.tsx:206` |
| C3 | FI / Cash, Equity | NAMED | green500 / amber500 / blue500 | | `holdings-shared.tsx:68-70`, used `StylePolicyComparison.tsx:255` |
| C3 | Structured / Commodities / Alternatives | FALLBACK | gray500 | `#6b7280` | `StylePolicyComparison.tsx:255` |
| D1 | all five | **NONE** | -- | -- | `PerfrpAllocation.tsx:130` colour keys on RESIDUE-ness, never on class |
| D2 | Fixed Income / Cash | NAMED | green500 | `#10b981` | `chartColors.ts:403` (MIX_PIE), used `PartnerAnalytics.tsx:1682` |
| D2 | Fixed Income / Cash | NAMED | **amber500** | `#f59e0b` | `chartColors.ts:408` |
| D2 | Equity | NAMED | blue500 | `#3b82f6` | `chartColors.ts:401` |
| D2 | Alternatives | NAMED | orange500 | `#f97316` | `chartColors.ts:405` |
| D2 | Structured / Commodities | FALLBACK | **undefined** | -- | `PartnerAnalytics.tsx:1682` -- **no key AND no fallback** |
| D3 | Fixed Income / Cash | NAMED | green500 | `#10b981` | `chartColors.ts:403`, used `ConsolidatedOverviewPanel.tsx:412` |
| D3 | Fixed Income / Cash | NAMED | **amber500** | `#f59e0b` | `chartColors.ts:408` |
| D3 | Equity | NAMED | blue500 | `#3b82f6` | `chartColors.ts:401` |
| D3 | Alternatives | NAMED | orange500 | `#f97316` | `chartColors.ts:405` |
| D3 | Structured / Commodities | FALLBACK | gray500 | `#6b7280` | `chartColors.ts:415` `mixPieColor` fall-through |

### `S*` -- the shared registry, graded separately (NOT a reader)

`src/lib/chartColors.ts @ e85f6eb84f` defines **five** class->colour maps, not one:

| map | lines | consumed by census readers? |
|---|---|---|
| `ASSET_CLASS` | `:113-120` | A1, A2, B2 (and re-exported via `holdings-shared` for C1/C2/C3) |
| `FIRM_MIX` | `:151-156` | **0 of 11** |
| `SUB_ASSET_COLORS` | `:284-309` | A1 (`:222`); duplicated in `holdings-shared.tsx:77-102` for C1 |
| `CMA_CATEGORY` | `:375-381` | **0 of 11** |
| `MIX_PIE` | `:400-411` | D2 (`:67`), D3 (`:66` via `mixPieColor`) |

`ASSET_CLASS` holds **6 keys and neither `structured` nor `commodities`**:
`fixedIncome green500 / equity blue500 / cash amber500 / alternatives orange500 / realEstate orange500
/ other gray500`.

> ⛔ **THE LEVERAGE SITE IS TWO FILES, NOT ONE.** The census names `chartColors.ts` as the single
> shared dependency. The **entire Attribution family (C1, C2, C3) binds colour through a SECOND
> registry the census does not name**: `src/pages/Attribution/constants/holdings-shared.tsx:67-110`.
> Over the 21 sub-asset keys the two registries share, **1 has already drifted** -- `'International'`
> is `blue600` at `holdings-shared.tsx:97` and `blue700` at `chartColors.ts:304`. A colour fix landed
> only at `chartColors.ts` would silently miss 3 of 11 readers. Filed as `POSN_ASTTAX-Z-W18-S2`.

---

## U2-AC2 -- ONE COLOUR PER CLASS (uniqueness WITHIN a class)

Counted over NAMED + SUBASSET bindings on the **11 readers**. A FALLBACK is **not** a binding of the
class -- it is a catch-all -- and is listed separately because it still paints pixels.

| # | class | agreed | distinct tokens bound | values | verdict |
|---|---|---|---|---|---|
| 1 | Fixed Income / Cash | green | **2** | `green500 #10b981` (A1,A2,B2,C1,C2,C3,D2,D3) · `amber500 #f59e0b` (A1,C1,C2,C3,D2,D3) | **FAIL** |
| 2 | Equity | blue | **1** | `blue500 #3b82f6` (A1,A2,B2,C1,C2,C3,D2,D3) | **PASS** |
| 3 | Structured | pink | **0** | -- | **ABSENT** |
| 4 | Commodities | gold | **2** | `blue950 #172554` (A1,C1) · `orange500 #f97316` (B2) | **FAIL** |
| 5 | Alternatives | orange | **1** | `orange500 #f97316` (B2,D2,D3) | **PASS** |

**Class 1 pins, both values:** `green500` at `HoldingsTab.tsx:216`, `PositioningSummary.tsx:70`,
`ExpectationsTab.tsx:98`, `ExpectationsTab.tsx:99`, `holdings-shared.tsx:68`, `chartColors.ts:403`;
`amber500` at `HoldingsTab.tsx:218`, `holdings-shared.tsx:70`, `chartColors.ts:408` -- all
@`e85f6eb84f`. The ratified class is literally named **"Fixed Income / Cash"** and holds *"fixed
income and cash"*, so a Cash holding in amber beside a Fixed Income holding in green is **two colours
inside one ratified class**, not two classes.

**Class 4 pins, both values:** `blue950` at `chartColors.ts:308` and `holdings-shared.tsx:101`;
`orange500` at `ExpectationsTab.tsx:102`.

### The two round-3 candidates -- CHECKED, not assumed

1. **"a Commodities colour aliased to Alternatives" -- CONFIRMED, and it is worse than one site.**
   `ExpectationsTab.tsx:102` reads `'Commodities': ASSET_CLASS.alternatives,` and `:101` reads
   `'Alternatives': ASSET_CLASS.alternatives,`. **The same reader paints two ratified classes the
   same pixel colour**, and `:105 DEFAULT_COLOR = ASSET_CLASS.alternatives` sends Structured and every
   unrecognised category to that colour too. Separately, `chartColors.ts:308` binds `'Commodities'` to
   `PALETTE.blue950` inside the block commented `// Equity - Blue gradient` at `:296` -- so on the
   Positioning and Attribution holdings tables a commodity reads as a **shade of Equity**.
2. **"`'Structured'` against `'Structured Credit'` " -- CHECKED, and the suspicion does not hold in the
   form it was raised.** They are **different keys at different grains**, not an alias pair.
   `'Structured Credit'` is a **Fixed-Income SUB-asset** coloured `PALETTE.green700` inside the FI green
   gradient (`chartColors.ts:292`, `holdings-shared.tsx:85`). The ratified top-level class
   `'Structured'` has **no key in any registry**. The real hazard is the inverse of the one suspected:
   a retag that moves a holding to class `Structured` does **not** inherit green700 -- different map,
   different grain -- it falls to `gray500` (A1, C1, C2, C3, D3), `orange500` (B2) or `undefined` (D2).
   The nearest thing to a `Structured` key anywhere is `MIX_PIE.structured_notes` at
   `chartColors.ts:404`, which is `PALETTE.orange500` -- **the Alternatives colour again**.

---

## U2-AC3 -- THE SAME COLOUR EVERYWHERE (agreement ACROSS readers)

**`ABSENT` and `AGREE` are different values and are kept apart.** `ABSENT` is taken from AT4-s-1's
FWD-6 reader x class table (inherited, not re-measured): the class cannot reach that reader's screen
at all, so it has no colour there and cannot agree about one.

```
RDR  READER                         FI / Cash     Equity    Structured  Commodities  Alternatives
---------------------------------------------------------------------------------------------------
A1   HoldingsTab.tsx                amber+green   blue500   ABSENT      blue950*     ABSENT
A2   PositioningSummary.tsx         green500      blue500   ABSENT      ABSENT       ABSENT
B1   AssumptionsTable.tsx           NO-BIND       NO-BIND   NO-BIND     NO-BIND      NO-BIND
B2   ExpectationsTab.tsx            green500      blue500   ABSENT      orange500    orange500
B3   OpalViewsTab.tsx               NO-BIND       NO-BIND   NO-BIND     NO-BIND      NO-BIND
C1   SelectionTab.tsx               amber+green   blue500   ABSENT      blue950*     ABSENT
C2   AssetAllocationSummary.tsx     amber+green   blue500   ABSENT      ABSENT       ABSENT
C3   StylePolicyComparison.tsx      amber+green   blue500   ABSENT      ABSENT       ABSENT
D1   PerfrpAllocation.tsx           NO-BIND       NO-BIND   NO-BIND     NO-BIND      NO-BIND
D2   PartnerAnalytics.tsx           amber+green   blue500   ABSENT      ABSENT       orange500
D3   ConsolidatedOverviewPanel.tsx  amber+green   blue500   ABSENT      ABSENT       orange500
---------------------------------------------------------------------------------------------------
  *  = bound only at SUB-ASSET grain, nested under a different class
  NO-BIND = the reader colours nothing by class (it renders the class, in the same chrome as every other)
  ABSENT  = the class cannot reach that reader's screen at all (AT4-s-1's FWD-6 table)
```

| class | binders | no-bind | cannot-render | verdict |
|---|---|---|---|---|
| Fixed Income / Cash | 8/11 | 3 | 0 | **DISAGREE** -- `amber500`+`green500` on A1,C1,C2,C3,D2,D3 vs `green500` only on A2,B2 |
| Equity | 8/11 | 3 | 0 | **AGREE** on `blue500 #3b82f6` |
| Structured | **0/11** | 3 | 8 | **ABSENT** |
| Commodities | 3/11 | 3 | 5 | **DISAGREE** -- `blue950` (A1,C1) vs `orange500` (B2) |
| Alternatives | 3/11 | 3 | 5 | **AGREE** on `orange500 #f97316` |

> ⛔ **STRUCTURED IS `ABSENT`, AND THAT IS NOT A PASS.** Zero of eleven readers bind any colour to it.
> The three readers that **can** render it -- B1, B3, D1 -- bind **no colour to any class at all**
> (B1 renders every category header `text-white`; B3 gives every `<option>` the same
> `SURFACE.dropdown`; D1 colours by residue-ness, not class). The other eight cannot render it at all.
> **So Structured is not "agreeing" -- there is nothing to agree about**, and grading this cell as a
> pass would be the defect FWD-6 was nearly graded on, reproduced one outcome over.

> ⚠ **THE `AGREE` VERDICTS ARE NARROW AND ARE STATED AS SUCH.** Equity agrees across 8 readers;
> Alternatives agrees across **3**. Both figures exclude the three NO-BIND readers, on which the class
> renders with no colour of its own. **An `AGREE` here means "every reader that binds a colour binds
> the same one", never "the class is coloured everywhere it appears."** On the DONE WHEN clause --
> *the agreed color is used on every place that shows the classes* -- only Equity and Alternatives use
> their ratified colour at all:

| class | agreed | bound | agreed colour used? |
|---|---|---|---|
| Fixed Income / Cash | green | `amber500`, `green500` | **PARTLY** -- and also amber |
| Equity | blue | `blue500` | **YES** |
| Structured | pink | *(none)* | **NO** -- nothing is bound at all |
| Commodities | gold | `blue950`, `orange500` | **NO** -- bound to dark blue and orange instead |
| Alternatives | orange | `orange500` | **YES** |

### FWD-4 ACCEPT clause 2 -- colour EXCLUSIVITY

**(a) NAMED/NAMED -- one token explicitly keyed to two ratified classes:**
`orange500 #f97316` is keyed to **Alternatives** (B2, D2, D3) **and Commodities** (B2).
**On B2 those are the same reader** -- `ExpectationsTab.tsx:101` and `:102`, two ratified classes, one
pixel colour.

**(b) ANY-KIND -- what actually reaches the screen:** `gray500 #6b7280` and `orange500 #f97316` each
paint **3 different ratified classes** (Structured, Commodities, Alternatives).

**(c) family collisions a token comparison cannot see:** `blue950` sits **inside** the Equity blue
gradient by construction (`chartColors.ts:296`), so Commodities reads as a shade of Equity even though
the token differs; and `amber500` -- the only amber/gold base in the palette -- is already Cash.

---

## U2-AC4 -- THE PRICE, PER FAILING CELL, WITH THE FREEZE BOUNDARY MARKED

| # | failing cell | at `file:line` @ `e85f6eb84f` | smallest change | side |
|---|---|---|---|---|
| 1 | Commodities is EQUITY-BLUE (A1, C1) | `chartColors.ts:308` | re-key `'Commodities'` out of the Equity blue gradient onto the ratified gold | **FROZEN** |
| 2 | same, the DUPLICATE copy (C1) | `holdings-shared.tsx:101` | same edit on the second copy, or delete the copy and import `SUB_ASSET_COLORS` | **FROZEN** |
| 3 | Commodities ALIASED to Alternatives (B2) | `ExpectationsTab.tsx:102` | point `'Commodities'` at a Commodities token, not `ASSET_CLASS.alternatives` | **FROZEN** |
| 4 | Structured has no colour: `ASSET_CLASS` is 2 keys short | `chartColors.ts:113-120` | add `structured: PALETTE.pink500` and a `commodities` gold key | **FROZEN** |
| 5 | same, Attribution's copy | `holdings-shared.tsx:67-71` | add the same two keys, or delete the copy | **FROZEN** |
| 6 | `MIX_PIE` has only `structured_notes`, = Alternatives orange | `chartColors.ts:404` | give Structured its own token | **FROZEN** |
| 7 | Structured falls to the ALTERNATIVES orange on the CMA scatter | `ExpectationsTab.tsx:105` | `DEFAULT_COLOR` must not be a ratified class's own colour | **FROZEN** |
| 8 | Cash splits its own ratified class (amber on 6 readers, green on B2) | `chartColors.ts:116` + `ExpectationsTab.tsx:98` | one ruling: Cash takes the FI green, or Cash leaves class 1 | **FROZEN** |
| 9 | Alternatives is `violet500` in `CMA_CATEGORY` | `chartColors.ts:380` | reconcile or retire `CMA_CATEGORY` (0 of 11 readers import it) | **FROZEN** |
| 10 | `'Intl Equity'` is `green500` -- the FIXED INCOME colour | `chartColors.ts:377` | reconcile or retire `CMA_CATEGORY` | **FROZEN** |
| 11 | `'Fixed Income'` is `amber500` -- the CASH colour | `chartColors.ts:378` | reconcile or retire `CMA_CATEGORY` | **FROZEN** |
| 12 | **PALETTE has NO gold** (0 of 65); the amber base is already Cash | `chartColors.ts:16-106` | mint gold from `amber400`/`amber600`/`yellow500` (none bound to a ratified class) or add a token -- **`amber500` is NOT available** | **FROZEN** |
| 13 | D2 has **no catch-all**: `FIRM_MIX_COLORS[cls]` is `undefined` for structured/commodities | `PartnerAnalytics.tsx:1682` | add the keys, or a fallback -- `fill={undefined}` is not a colour | **FROZEN** |
| 14 | the two registries have already DRIFTED (`'International'`, 1 of 21 keys) | `holdings-shared.tsx:97` vs `chartColors.ts:304` | delete the duplicate registry; import the one in `chartColors` | **FROZEN** |

**TOTAL PRICED CELLS: 14 -- FROZEN (under `portal/`): 14 -- OWNED: 0.**

**Every priced cell is under `portal/`.** The portal is FROZEN by Andrew's word, this order's
`<paths>` grant holds no portal path, and **nothing was written**. The OWNED count is zero not because
the work is small but because the entire surface sits behind the freeze.

> ⚠ **ROW 12 IS NOT A WIRING FIX AND IS THE ONE THAT CANNOT BE CUT AS WRITTEN.** Every other row says
> *point this key at the right token*. For Commodities **there is no right token to point at**: the
> palette holds 65 named tokens and 0 are gold; the family base `amber500 #f59e0b` is already Cash at
> `:116`/`:408` and reaches 6 of the 11 readers, so taking it would put two ratified classes on one
> colour -- the exact ACCEPT clause 2 this cell is grading. Structured's pink, by contrast, exists
> (`PALETTE.pink500 #ec4899` at `:61`) and is bound to no ratified class. Filed as
> `POSN_ASTTAX-Z-W18-S5`; the disarm is a named hex in PRD s.3, or Andrew's word, **before** an
> FWD-4 remediation cell is cut.

> ⛔ **THIS CELL COVERS FWD-4. IT DOES NOT SERVE IT. FWD-4 IS NOT GRADED REALIZED.**

---

## U2-AC5 -- JUDGMENT (readings only; graded by `3.0.0_SA_CVO~Z` at L9)

**The question:** whether one colour per class, held the same across readers, is sufficient for FWD-4
as the PRD states it, or whether the outcome also requires the colour to be legible to a person on the
rendered page.

**READINGS, offered without a verdict:**

**1. The PRD's own text contains both readings and does not choose.** `DONE WHEN` is stated as
`APPLIED` -- *"the agreed color for each class is used on every place that shows the classes"* -- which
is a **source-state** bar this cell can and did grade. But the ACCEPT paragraph beside it is written
from a viewer's position: *"The same class is the same color everywhere it appears, and no place shows
a class in a color another uses for something else."* *"Appears"* and *"shows"* are rendering verbs.
A token census satisfies the first and can only approximate the second.

**2. This cell's own evidence shows the two bars can disagree, in both directions.** `blue950
#172554` and `blue500 #3b82f6` are different tokens and the token instrument scores them as
distinct -- yet `chartColors.ts:296` places `blue950` deliberately **inside** the Equity gradient, so
to a person a commodity reads as dark Equity. That is a token PASS and a legibility FAIL. Conversely
`ExpectationsTab.tsx:101`/`:102` bind Alternatives and Commodities to the **identical** token, which
fails both bars -- so the distinction is not academic, it is the difference between catching one of
these two and catching both.

**3. A third state exists that neither bar names: the class with no colour at all.** Structured is
`ABSENT` on every reader; B1, B3 and D1 render classes in uniform chrome. Under a strict token reading
"each class has one colour" is arguably *vacuously* satisfiable where nothing is bound -- the reading
this cell refused to take. Under a legibility reading it is plainly unmet. **The outcome's wording
does not distinguish "one colour" from "no colour", and this cell had to choose; it chose ABSENT.**

**4. What a legibility bar would cost, named so the trade is visible.** It cannot be graded from
source at a pin. It needs a rendered page, real holdings carrying all five classes, and a contrast
judgment -- and the portal is FROZEN, so no such page can be produced in this round. Adopting the
wider reading makes FWD-4 ungradable until the freeze lifts; keeping the narrower one makes it
gradable now, at the cost of a bar that `blue950`-inside-the-blue-gradient passes.

**5. The instrument's own limit, stated against this cell's grades.** Everything above is a
**source-token** measurement. It cannot see CSS cascade, opacity modifiers (`text-amber-300/70` on
D1), theme variables (`hsl(var(--primary))`, used on C1/C3), or what a chart library does with an
`undefined` fill (D2:1682). Where the source binds nothing, this cell reported `NO-BIND` or `ABSENT`
rather than inferring a rendered colour.

---

## CONTROLS

**1. MUTANT CONTROL on the citation instrument -- does `cite()` read bytes at the pin, or echo the
anchor it was handed?** Positive arm: 3 real (line, anchor) pairs -> all `True`. Negative arms: the
same anchor at 4 NEIGHBOURING lines (`ExpectationsTab.tsx:100,101,103,104`) -> all `False`; an anchor
naming a colour that is not on the line (`PALETTE.amber500` at `chartColors.ts:308`, `PALETTE.pink500`
at `:114`) -> both `False`; out-of-range line -> `LINE-OUT-OF-RANGE`; missing file -> `FILE-UNREADABLE`.
**The instrument discriminates on every axis.** Across the full run: **94 citations, 0 mismatches.**

**2. NEGATIVE CONTROL on the vintage instrument.** 126 files differ between the shared checkout
`30ca034bba` and the pin `e85f6eb84f`, and `src/App.tsx` hashes differ -- so a same-hash verdict is
capable of failing. Of the 12 files cited here, 0 differ. The SAME verdict is therefore a measurement.

**3. DISCRIMINATION on the grade itself -- the table is not uniform on either axis.** Across classes:
2 PASS, 2 FAIL, 1 ABSENT on AC2; 2 AGREE, 2 DISAGREE, 1 ABSENT on AC3. Across readers: 8/11 bind
Equity, 3/11 bind Alternatives, 0/11 bind Structured. A grader that returned the same answer for every
cell would be visible here, and does not appear.

**4. THE WRONG-ZERO CHECK, which changed the answer.** A first pass scanning for a class token and a
colour token **on the same line** returned **0 hits for 7 of the 12 files** (B1, C1, C2, C3, D1, D2,
D3). Rather than record that as "no binding", each zero was probed for colour carriers of ANY kind.
**5 of those 7 zeros were instrument misses, not absences**: C1 binds through `getAssetClassBgColor`
imported at `SelectionTab.tsx:15`; C2/C3 through `ASSET_CLASS_COLORS` imported at `:17`; D2 through
`FIRM_MIX_COLORS = MIX_PIE` at `:67`; D3 through `colorFor = mixPieColor` at `:66`. Only B1 and D1
were true absences, each confirmed by reading the render path. **The one-line instrument would have
reported 5 of 11 readers as binding no colour, and every one of those would have been wrong** -- the
same single-line-vs-block failure AT4-s-1 disclosed on its own vocabulary filter.

---

## SURPRISE ROWS FILED

| id | class | hazard | disarm owner | what |
|---|---|---|---|---|
| `POSN_ASTTAX-Z-W18-S1` | OBSERVATION | ARMED | `2.0.0_SA_COO~Z` | the order's own SURPRISE ROWS section names the bare id form `POSN_ASTTAX-W18-S<k>`; `surprise-row-gate.py:104/:1162/:1171` derives fabric FROM the id and refuses a bare id carrying `fabric: site-z`. 64 of 64 existing rows use the `Z-` form. This worker used `Z-` and recorded the deviation. |
| `POSN_ASTTAX-Z-W18-S2` | OBSERVATION | ARMED | `2.0.0_SA_COO~Z` | the colour leverage site is TWO registries, not one: C1/C2/C3 bind through `holdings-shared.tsx:67-110`, which the census does not name, and it has already drifted from `chartColors.ts` on 1 of 21 shared keys. |
| `POSN_ASTTAX-Z-W18-S3` | OBSERVATION | ARMED | `2.0.0_SA_COO~Z` | `chartColors.ts:375-381 CMA_CATEGORY` contradicts `ASSET_CLASS` in the same file (`'Fixed Income'`->amber500, `'Intl Equity'`->green500, `'Alternatives'`->violet500); 0 of 11 census readers import it, and its consumers outside the census were deliberately NOT enumerated. |
| `POSN_ASTTAX-Z-W18-S4` | OBSERVATION | INERT | -- | B3 is graded PASS 5/5 on free-text render and also carries a hardcoded three-option view selector at `OpalViewsTab.tsx:212-214` naming only equity and fixed-income. Filed as a qualifier, not a refutation. |
| `POSN_ASTTAX-Z-W18-S5` | OBSERVATION | ARMED | `1.0.0_SA_CTO~Z` | the ratified Commodities **gold does not exist**: 0 of 65 palette tokens are gold and the amber base is already Cash on 6 readers. FWD-4 for Commodities needs a colour decision no cell owns. |

---

## VERDICT

**FWD-4 IS NOT MET, AND IT FAILS ON BOTH OF ITS CLAUSES.**

- **ONE COLOUR PER CLASS (AC2): 2 of 5 classes PASS.** Fixed Income / Cash carries 2 tokens,
  Commodities carries 2, **Structured carries 0**.
- **THE SAME COLOUR EVERYWHERE (AC3): 2 AGREE, 2 DISAGREE, 1 ABSENT** -- and both AGREE verdicts are
  narrow (8 of 11 binders for Equity, **3 of 11** for Alternatives; 3 readers bind nothing at all).
- **EXCLUSIVITY (ACCEPT clause 2): VIOLATED.** `orange500` is explicitly keyed to two ratified classes
  on one reader (`ExpectationsTab.tsx:101`/`:102`), and `gray500` and `orange500` each paint three
  different ratified classes once fallbacks are counted.
- **THE AGREED COLOUR IS USED FOR 2 OF THE 5 CLASSES.** Structured has no colour anywhere;
  Commodities is dark-blue or orange, never gold; Cash splits its own class.

**The price is 14 edit sites and every one is FROZEN. OWNED: 0.** One of the fourteen
(`chartColors.ts:16-106`, the missing gold) is not a wiring change at all and cannot be cut as a
worker task until the colour is named.

**FWD-4 is COVERED by this cell and is NOT graded REALIZED.**
