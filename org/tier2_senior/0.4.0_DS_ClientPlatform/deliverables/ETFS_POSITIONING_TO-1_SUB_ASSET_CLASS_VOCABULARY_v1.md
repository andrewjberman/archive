# ETFS_POSITIONING TO-1 / cell `ETFS-d-2` -- the `sub_asset_class` VOCABULARY ACT (v1)

**Owner:** `0.4.0_DS_ClientPlatform` | **TO:** `ETFS_POSITIONING.TO-1` | **Cell:** `ETFS-d-2`
**Criterion:** `ETFS-TO1-AC6` | **Grounding layer:** DECLARATIVE
**decomp_ref:** `workflows/atom_decomposition/runs/etfs-positioning/20260821T194927Z/DECOMP.md`
**Decomp status:** UNCERTIFIED ON ITS FACE (issuer-disclosed, COO 65669) -- carried forward, not re-litigated.
**Authority:** PRD s.4.4 (the two-grains hazard), AE CONTRACT v1 (field names fixed, values deliberately open),
CLAUDE.md Rule 24 as widened 2026-08-20.

---

## 0. THE HEADLINE: THIS IS AN **ADOPTION**, NOT A MINT. 12 OF 12 VALUES ALREADY EXIST IN-ESTATE.

I came to this cell expecting to mint an enum. **The build ladder's rung 2 fired and the answer changed:
the estate already carries this exact vocabulary, and it carries it in a form that matches our Bloomberg
source byte-for-byte.** So the act is ADOPTION -- which Rule 24's widening is explicit is still an
AUTHORING ACT ("ADOPTION IS AN AUTHORING ACT -- the measured propagation vector: an externally-proposed
4-value enum was adopted untested") -- and therefore still carries the full four-postulate test below.

**The enum (12 values):** the 11 GICS sectors exactly as spelled by `portal/src/lib/dataLoader.ts:236-249`
(`SECTOR_INDICES`), plus `Cash & Cash Equivalents` exactly as spelled by this project's own PRD s.2.5:147.

```
Energy | Materials | Industrials | Consumer Discretionary | Consumer Staples | Health Care
Financials | Information Technology | Communication Services | Utilities | Real Estate
Cash & Cash Equivalents
```

**Why adoption beats minting here, one line each:**

1. **It is byte-identical to the source.** Bloomberg `GICS_SECTOR_NAME` in
   `bbg/{date}/characteristics.parquet` emits these exact strings -- measured, 10 of the 11 present in the
   round-1 data, all 10 matching `SECTOR_INDICES` character-for-character. **The producer therefore needs
   NO mapping table** (build ladder rung 6: it can be a passthrough). A minted synonym set would have
   required a translation layer whose only job is to undo my own renaming.
2. **It is byte-identical to the portal's existing COLOR MAP.** `dataLoader.ts:471` `SECTOR_COLORS` keys
   all 11. A value I spell differently renders with **no color** -- so the spelling has a live, checkable
   consequence on the page, not merely an aesthetic one.
3. **`Cash & Cash Equivalents` is named in THIS PROJECT'S OWN PRD** (s.2.5:147, as an
   `Investment Type Desc` value from AJ's daily feed), and in
   `data/black_diamond/scripts/silver/build_bd_assets_dim.py:68` and
   `docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md:37,119`.
   Re-coining `Cash & Equivalents` beside it would have been exactly the duplicate the build ladder's
   rung-2 granularity amendment names.

**I DO NOT REUSE THE 10-VALUE MODEL `sub_asset_class` VOCABULARY** (`Ultra Short Duration, Short Duration,
Intermediate, High Yield, Structured Credit, US Large Cap, US Mid Cap, Developed, EM, Volatility`).
PRD s.4.4 and COO 65717 both name why; postulate (ii) below carries the test.

---

## 1. THE DECLARED LAYER -- named FIRST, because postulate (i)'s CE half is evaluated against it

> **LAYER: one row in `holdings[]` of an Opal ETF book on the Positioning page -- i.e. ONE SINGLE
> SECURITY (or cash position) held by one of the four ETFs in `config/etf_universe.json`
> (DIVZ, IDVZ, PFDE, PFOE), at one `data_as_of` date.**

Stating the layer is what makes the CE half falsifiable. It is deliberately NOT "every security in the
estate" and NOT "every holding of every Opal product" -- those are wider layers this enum does not claim
to cover, and a later sweep must not read it as claiming them.

**Grain of the axis:** `sub_asset_class` is SUBORDINATE to `asset_class`. It partitions WITHIN an asset
class -- the shape the live artifact already uses (`Equity` -> `US Large Cap`,
`Fixed Income` -> `Short Duration`). Our mapping:

| `asset_class` | `sub_asset_class` domain |
|---|---|
| `Equity` | the 11 GICS sectors |
| `Cash` | `Cash & Cash Equivalents` (single member) |

---

## 2. THE FOUR-POSTULATE RECORD

### (i) MECE -- mutually exclusive, collectively exhaustive over the declared layer

**Mutually exclusive: YES, and it is exclusive BY CONSTRUCTION rather than by discipline.**
GICS assigns exactly one sector per issuer -- it is a partition, not a tag set. The one place two values
could collide is a cash instrument that is also an operating company, and that is made *inexpressible* by
evaluating the discriminator in a fixed order: the producer tests the upstream `is_cash` boolean FIRST;
only an `is_cash == False` row is ever offered a GICS sector. **A row cannot receive two values because it
is never asked twice.**

**Collectively exhaustive: HUNTED -- and the hunt FOUND AN UNCOVERED MEMBER.** Measured, denominators
printed, source `silver/holdings/2026-08-20.parquet`:

```
114 holding rows total
  4  is_cash == True   -> Cash & Cash Equivalents   (tickers: FXFXX, Cash&Other)
110  is_cash == False
     106 unique non-cash tickers
     105 join to bbg characteristics AND carry a GICS_SECTOR_NAME  (105/105 non-null)
       1 DOES NOT JOIN  <-- THE UNCOVERED MEMBER
```

**The uncovered member is real and I name it: `2602335D`** (security_name `TPG Inc`, cusip
`BBG01Y2F01K3`, price 0.00, market_value 0.00, weight_pct 0.00, fund PFDE) -- a placeholder-ticker row with
no Bloomberg characteristics record and therefore no GICS sector.

**HOW IT IS HANDLED, and why NOT with an `Other` bucket:** the row emits `sub_asset_class: null` and the
run manifest carries a `sub_asset_class_unmapped` COUNT. **An `Other` catch-all would have made the enum
trivially exhaustive and destroyed the signal** -- it converts "we could not classify this" into a category
that looks deliberate, which is precisely the failure mode `holdings_status` exists to prevent one field
over. `null` is the absence marker, not a member; the manifest count is the control that makes the absence
visible. This mirrors the estate's own `UNDECLARED` precedent in the lifecycle registry ("the one enum
value an OBSERVER may write -- it records that no producer has asserted").

**Named residual, so it is not discovered later as a gap:** the layer today contains only equities and cash
because all four books are equity ETFs. A fixed-income security, a derivative, a preferred, or an
ETF-of-ETF entering one of these four books would be an uncovered member -- it would land as `null` and be
COUNTED, loudly, rather than silently bucketed. **That is designed behavior, not an oversight.**

### (ii) SAME GRAIN -- every value classifies exactly one security

All 12 values classify **one security at one point in time**. None is a fund-level, book-level, or
cohort-level property.

**This is the postulate the obvious alternative FAILS, and that failure is the entire reason this cell
exists.** The model `sub_asset_class` values (`US Large Cap`, `Developed`, `Short Duration`, ...) classify
**an ETF** -- a fund. The model books hold ETFs; an ETF book holds single securities. Reusing them here
would put a FUND-grain value on a SECURITY-grain row: two grains on one axis, postulate (ii) failed on
arrival. PRD s.4.4 stated the hazard; this is the measurement of it.

*Note the near-miss: `portal/src/pages/Positioning/constants/etf-categories.ts` maps `DIVZ`/`PFDE` ->
`US Large Cap`. That file is CORRECT at ITS grain (an ETF as a holding of a model book) and would be WRONG
at mine (a stock inside that ETF). Same page, same field name, different grain -- reusing it would have
been the easy error.*

### (iii) INTENT COHERENCE -- one axis, one intent

**The single intent: the economic sector of the issuer's underlying business, or cash-equivalence.**

What this axis deliberately does NOT encode, each because it already has its own field:

| Not encoded here | Lives at |
|---|---|
| display grouping / ordering / color | `SECTOR_COLORS` (portal-side presentation) |
| country or region | `segment.geography` |
| active vs passive management | the per-holding `active` field |
| data availability / producer state | `holdings_status` (AE's enum) |
| fund-level style or duration bucket | the model books' own `sub_asset_class`, a different grain |

No value mixes two of these. `Cash & Cash Equivalents` is the row worth challenging -- it reads as a
*security-type* rather than a *sector*. It is retained because the axis's honest intent is "the economic
category of this position **within its asset class**", and under `asset_class: Cash` that category has
exactly one member. It smuggles in no handling policy and no state.

### (iv) STATE COHERENCE -- the stability frame

**State axis: OBSERVABLE vs UNOBSERVABLE for a given book** (do constituent rows exist to classify).

- **Today:** all 12 values are equally OBSERVABLE for PFDE/PFOE, and all 12 are equally UNOBSERVABLE for
  DIVZ/IDVZ -- those books have zero constituent rows (`DIVZ 0 / IDVZ 0`, measured).
- **ONE remedy moves every value together:** the TrueShares constituent capture landing (`ETFS-c-1`, gated
  on Andrew's egress word, explicitly NOT in this TO). When those rows arrive, all 12 values become
  observable for DIVZ/IDVZ simultaneously. No value requires a different remedy.
- **PASSES. Nothing fails to move** -- stated explicitly because the postulate requires naming which values
  do not move, and here the answer is "none".

**One distinction worth pinning, because it looks like a state failure and is not:** `Real Estate` has
**zero weight** in the current data (10 of 11 GICS sectors present; Real Estate absent). That is a
DATA-CONTENT fact -- no REIT is currently held -- not a state of the value. The value is fully observable;
it simply has no members today. **Zero-weight is not unobservable**, and conflating the two is how a
correct enum gets trimmed to fit one day's holdings.

---

## 3. TOKEN-HYGIENE CENSUS -- run with `comp-find -i`, per the TO

Run with `-i` on every token. `comp-find` is case-sensitive by default and its denominator counts FILES
SCANNED, never pattern coverage. **The dangerous mode is the UNDERCOUNT, not the zero:** a zero prints a
guard that names `-i`; a partial case-miss returns a confident non-zero count with **no caveat at all**.

**Scope:** `portal/src docs/architecture` -- **874 files scanned, 1 UNREADABLE and NOT searched**
(carried, not hidden).

| Proposed value | `-i` hits | Read |
|---|---|---|
| Energy | 29 | sector use AND a commodity `subType` (`ExecutiveSummary.tsx:66`) -- different axis, no conflict |
| Materials | 7 | sector use |
| Industrials | 7 | sector use |
| Consumer Discretionary | 9 | sector use |
| Consumer Staples | 7 | sector use |
| Health Care | 5 | sector use |
| Financials | 14 | sector use + `tickerRegistry.ts:67` sector INDEX ticker |
| Information Technology | 7 | sector use |
| Communication Services | 8 | sector use |
| Utilities | 50 | **HOMONYM -- see below** |
| Real Estate | 11 | sector use + one asset-class-axis use (`AdvisorIntelligence/_shared/types.ts:1287`) |
| Cash & Cash Equivalents | 5 | BD classification + **this project's own PRD s.2.5:147** |

**`Utilities` (50) is the one result that needed READING rather than counting.** The large majority are a
HOMONYM at an unrelated meaning -- `@layer utilities` (Tailwind), `dateUtils.ts`, "UTILITIES LAYER -
CUSTOM CLASSES", "Tailwind ring utilities". **This is not a vocabulary collision** (no competing
*classification axis* claims the token), but it IS a token-hygiene fact worth recording: any future
text-census of `Utilities` over this repo will be dominated by CSS/JS noise and must read its hits, not
count them. **A count I had not read would have reported a 50-hit "collision" that does not exist.**

*Method note, self-caught and recorded because the failure was mine:* my first census pass piped
`comp-find` through `grep -c "^"` and returned **7 for all twelve tokens**. I was counting the tool's own
frame lines, not its hits. **Identical counts across twelve different tokens is an instrument that could
not have said otherwise** -- the tell was in the output, not in the method. The real numbers come from
`comp-find`'s own `DENOMINATOR:` line, which is the frame it prints for exactly this reason.

---

## 4. `comp-estate --definitions` CHECK (build ladder rung 2, one layer up)

Run. **Denominator: 65 ratified terms**, SYSTEM_DEFINITIONS v3.18. The registry is the estate-ONTOLOGY
vocabulary (Estate, Substrate, C0-C4, Plane, Scope, Lifecycle_Stage, ...). **Zero of the 65 is a financial
asset-class or sector term**, so no proposed value collides with a ratified term at a different meaning.
No naming act is required against that registry.

---

## 5. SURFACED, NOT CHASED -- a pre-existing disagreement this census exposed

**The portal carries TWO disagreeing spellings of this same axis.** I am recording it, not touching it
(outside `ETFS-d-1`/`ETFS-d-2`, and Andrew's scope clause holds the rest of this seat):

| Source | Spelling |
|---|---|
| `portal/src/lib/dataLoader.ts:236` `SECTOR_INDICES` + `:471` `SECTOR_COLORS` + `portal/src/pages/Correlation/constants.ts:101` | GICS-canonical: `Information Technology`, `Health Care` |
| `portal/src/pages/PortfolioManagement/constants.ts:36-50` `SECTORS` | **`Technology`**, **`Healthcare`** -- plus `ALL` and `Other` |

The second also mixes a **filter sentinel (`ALL`) with classification values on one axis** -- a Rule-24
intent-coherence defect on that enum, independent of this cell.

**Class: OBSERVATION / INERT.** No disarm owner needed -- nothing is armed; it is a latent inconsistency
that predates this project and that my adoption of the `dataLoader` spelling does not worsen. Filed to
`3.0.0_SA_CVO`'s channel. **I am not editing either file.**

---

## 6. WHAT THE PRODUCER (`ETFS-d-1`) DOES WITH THIS

```
row.is_cash == True                      -> "Cash & Cash Equivalents"   (asset_class "Cash")
row.is_cash == False, GICS present       -> GICS_SECTOR_NAME verbatim   (asset_class "Equity")
row.is_cash == False, GICS absent/unjoin -> null + manifest count       (asset_class "Equity")
```

No mapping table. **The Bloomberg string IS the emitted string** -- the property that makes this adoption
worth more than a mint.

**`segment.sector`** (book level) is the weight-sum of the same axis over the book's holdings, so the
book-level and holding-level sector vocabularies are **THE SAME SET by construction** -- they cannot drift.

---

**v1. Cell `ETFS-d-2` COMPLETE at this document.** `ETFS-TO1-AC6` satisfied: vocabulary shipped WITH its
four-postulate record, its `-i` token census (denominators printed; the homonym read, not counted), and
its `comp-estate --definitions` check.
