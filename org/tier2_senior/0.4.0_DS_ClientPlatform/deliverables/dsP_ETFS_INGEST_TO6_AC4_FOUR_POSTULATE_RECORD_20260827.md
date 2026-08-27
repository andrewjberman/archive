# ETFS_INGEST.TO-6 `INGEST-TO6-AC4` — the four-postulate record for the gold-row GICS act

**Seat:** `0.4.0_DS_ClientPlatform~P` · **Cell:** `INGEST-T3-6` · **Decomp:**
`workflows/atom_decomposition/runs/etfs-ingest/20260824T2010Z/DECOMP.md @fcdf042972`
**Vintage of every measurement below:** HEAD + served artifacts read 2026-08-27T17:5xZ.

AC4 requires the gold holding row to carry the finer GICS field "as a **Rule 24 authoring act** with
its four-postulate record — a SECOND schema act at a DIFFERENT GRAIN from T2's row, and **the two MAY
NOT SHARE AN AXIS**."

> ⛔ **I AM NOT EMITTING THE FIELD YET, AND THE REASON IS AC4'S OWN CONSTRAINT.**
> Running the four postulates is what AC4 asks for, and postulate (iii) **fails before the field is
> added** — not because of anything this TO does, but because the axis AC4 forbids sharing is
> **already occupied**. Emitting first and recording second would have produced a clean-looking
> record for a collision that was there the whole time. The measurement is below; the act waits on a
> ruling that is not mine to make.

---

## THE MEASUREMENT THAT DRIVES EVERYTHING BELOW

`classify()` (`data/etfs/scripts/gold/etf_positioning_gold.py:749-771`) returns, for a non-cash row:

```
    return ASSET_CLASS_EQUITY, val        # val IS the GICS SECTOR NAME, validated against GICS_SECTORS
```

So **`sub_asset_class` on the gold holding row already carries the GICS sector for equity rows.**
Not a paraphrase of it — the sector name itself.

**CONFIRMED ON THE SERVED ARTIFACT**, not inferred from the code
(`gold/holding/date=2026-08-26/holding.parquet`, written 2026-08-27T13:01:23Z, **189 rows, 29 cols**):

| `sub_asset_class` value | rows | vocabulary it belongs to |
|---|---|---|
| Information Technology · Financials · Health Care · Industrials · Consumer Staples · Communication Services · Consumer Discretionary · Utilities · Energy · Materials | **180 of 189** | **GICS sector** |
| Ultra Short Duration | 8 | asset-class / duration |
| (null) | 1 | unmapped, deliberately not bucketed |

`asset_class=Equity` spans **10 distinct** `sub_asset_class` values; `asset_class=Fixed Income` spans **1**.
**Columns matching gics/sector/industry emitted today: ZERO** — the sector is served *only* through
`sub_asset_class`, under a name that does not say so.

---

## THE FOUR POSTULATES

### (i) MECE over a DECLARED domain — **HOLDS, and by construction rather than by discipline**

The declared domain is *"every row in the gold holding table."* `classify()` evaluates `is_cash`
**first**, so a row is never offered a GICS sector and a cash value in the same pass; the two
vocabularies cannot both apply. The uncovered member was hunted and is **handled**: an unmappable row
returns `None`, **not** an `Other` bucket, and the caller counts the nulls into the manifest. That is
the right call — `Other` would make the enum trivially exhaustive and convert *"we could not
classify this"* into a category that looks deliberate. Measured: exactly **1 of 189** null.

### (ii) SAME GRAIN — ⛔ **ALREADY FAILS, before this TO adds anything**

`sub_asset_class` holds values from **two different vocabularies at two different grains**:
a GICS **sector** (180 rows) and a duration/asset-class bucket (8 rows). These are not two members of
one taxonomy; they are members of two taxonomies sharing a column. Adding
`gics_industry_group` would introduce a **third** grain — GICS *industry group* is the **child of
GICS sector** — with the parent living inside `sub_asset_class` and the child in a sibling field.

### (iii) INTENT COHERENCE — ⛔ **THIS IS THE ONE AC4 NAMES, AND IT IS ALREADY VIOLATED**

AC4 says the two schema acts **MAY NOT SHARE AN AXIS**. Measured, they *would*:

```
  AXIS "what kind of asset is this"      -> asset_class            (Equity / Fixed Income / Cash)
  AXIS "what sector of the economy"      -> ** sub_asset_class **  <- for 180 of 189 rows, GICS SECTOR
  AXIS "what sector, more finely"        -> gics_industry_group    <- what AC4 asks me to add
```

The second and third rows are **the same axis at two grains**, and the second is wearing a name from
the *first* axis's vocabulary. So the proposed field does not collide with `sub_asset_class`'s
*name* — it collides with what that column **actually contains**.

⛔ **A DECLARATION CANNOT FIX THIS.** Writing *"`sub_asset_class` is the asset-class axis and
`gics_industry_group` is the GICS axis"* into a record does not make it so; 180 served rows would
still carry a GICS sector under the asset-class name. **That is Rule 24(iii) applied INSIDE a value,
which this estate has banked as a recurring defect** — the axis claims to measure one thing and its
values measure another.

### (iv) STATE COHERENCE — **which values one remedy does NOT move**

| remedy | moves | does NOT move |
|---|---|---|
| Emit `gics_industry_group` as a sibling field | adds the finer grain | **nothing about the 180 rows** serving a GICS sector as `sub_asset_class` |
| Rename/split `sub_asset_class` into an explicit `gics_sector` | fixes the axis | **breaks every consumer** — this is a SERVED field (`comp-find -i sub_asset_class`: 24 code-file hits incl. portal components) |
| Do nothing | — | the collision persists and the next finer-grain request re-derives it |

**No single remedy moves both**, which is exactly what (iv) exists to surface.

---

## TOKEN-HYGIENE CENSUS (AC4-required), denominators printed, two instruments

```
comp-find -i "GICS_INDUSTRY_GROUP_NAME"
  DENOMINATOR: 36 hit(s) across 27,229 files scanned | 1 UNREADABLE | 1,820 BINARY, not searched
  BANDS (true totals, not this page): SURFACED=2  CONFIG=10  DOC=24
  SURFACED (first-party source), both of them:
    integrations/bloomberg/pipeline/etf_daily_pull.py:227   <- my own AC1 comment
    integrations/bloomberg/pipeline/etf_daily_pull.py:239   <- my own AC1 field
```

**SECOND INSTRUMENT** (raw grep over `*.py|*.ts|*.tsx|*.js`, `.git`/`.runtmp` excluded), because a
band is one instrument and Rule 22 forbids re-running the same one:
`GICS_INDUSTRY_GROUP_NAME` -> **`etf_daily_pull.py` only**.
**POSITIVE CONTROL** `GICS_SECTOR_NAME` -> **4 files**
(`etf_positioning_gold.py`, `test_etf_positioning_upgrade_forward.py`,
`etfs_positioning_pull.py`, `etf_daily_pull.py`) — so the sweep can find this shape of token, and the
single hit is a real result rather than a broken read.

⚠ **A TRAP I HIT AND AM RECORDING:** `comp-find -i "gics_industry_group"` and
`comp-find -i "GICS_INDUSTRY_GROUP_NAME"` returned the **identical** denominator (36). That is not
corroboration — the former is a case-folded **substring** of the latter, so `-i` substring matching
makes them the same query. Two numbers agreeing because they are the same measurement is not two
measurements.

**VERDICT: the token is FREE in code.** Its only occurrences are my own AC1 edit; every other hit is
a TO, the decomp, or a deliverable. No naming collision to resolve.

---

## RECOMMENDATION — routed, not taken

**AC4 is BLOCKED on a taxonomy ruling that is not this lane's to make**, because the resolution
changes a **served** field. My recommendation, offered with no preference between the last two:

1. ⭐ **Emit `gics_industry_group` as its own field AND record `sub_asset_class`'s equity values as a
   KNOWN, NAMED axis defect** — cheapest, ships AC4's data, and stops the collision being
   rediscovered. It does **not** repair (ii)/(iii); it makes them legible.
2. **Emit `gics_sector` explicitly alongside `gics_industry_group`**, leaving `sub_asset_class`
   byte-unchanged. The GICS axis then lives entirely in fields that say GICS, and the duplication
   with `sub_asset_class` is deliberate and declared. Costs one redundant column; breaks nothing.
3. **Split `sub_asset_class`.** Correct, and **out of scope for TO-6** — it is a served-contract
   change with 24 code-file consumers including portal components, and TO-6 says one variable at a
   time.

⛔ **What I will not do is emit the field and let the record assert an axis separation the served
data contradicts.** Whichever way this is ruled, AC4's four postulates are now measured rather than
asserted, and the ruling has the numbers it needs.

**Owner of the call:** `2.0.0_SA_COO~Z` (TO author) with `1.0.0_SA_CTO~Z` on the served-contract half.
**Nothing else in TO-6 is blocked on this** — AC1/AC2/AC5 are done; AC3/AC6 wait on the
2026-08-28T11:00Z scheduled fire.
