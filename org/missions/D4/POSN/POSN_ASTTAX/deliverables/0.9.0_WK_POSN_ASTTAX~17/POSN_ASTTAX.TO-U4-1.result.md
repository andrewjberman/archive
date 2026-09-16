# POSN_ASTTAX.TO-U4-1 -- THE RETAG MEMBER SET, SETTLED BY SUBTRACTION

**Worker** `0.9.0_WK_POSN_ASTTAX~17` - **Cell** `AT4-s-4` (round 4) - **Serves** FWD-1
**Worktree** `C:/tmp/wk-posn-u4`, branch `wk-posn_asttax-4-4`, base HEAD `72f2417499`
**RECORD ONLY.** Nothing here retags anything. `TO-T6-1` remains NO-GO and unspawned.

---

## THE ANSWER, FIRST

| | |
|---|---|
| DENOMINATOR | **285** rows -- every row of `dynamodb://etf-classifications` |
| SUBTRACTED | **273** rows, in four named bands, each with its reason |
| **DERIVED MEMBER SET** | **12** |
| STANDING FIGURE | 11 (carried from round 3, `AT3-s-5` / `TO-T5-1`) |
| **DELTA** | **+1. PRESENT-BUT-UNEXPECTED: `VNQ`. EXPECTED-BUT-ABSENT: NONE.** |
| ALSO RECORDED | `BIPC`, a 13th candidate whose target is **UNDETERMINED** and is NOT counted |
| DOMAIN FALSIFICATION | **THE SUBTRACTION IS NOT VOID** -- zero members lie outside the domain. **The domain is NOT the only classification store**, and that is a separate finding, below. |

**ELEVEN WAS TESTED, NOT REPRODUCED.** The eleven were never used as an input: the ladder was
read off the PRD, applied to all 285 rows, and the standing set was loaded only at the very end
to difference against. The eleven all survive; a twelfth joins them.

---

## U4-AC1 -- THE DENOMINATOR

**Named invocation, run verbatim:** `timeout 300 comp-find 'asset_class' --all --files` -> rc 0

```
DENOMINATOR: 1885 hit(s) across 3272 file(s) scanned in scope [corpus=all] | 2 EPHEMERAL-FLOOR,
NOT searched (--corpus raw reads these) | 30426 UNREADABLE, NOT searched | 35 BINARY, NOT searched
BANDS (true totals, not this page): HEAD=12 DEF=37 SURFACED=611 CONFIG=729 DOC=496
PAGE 1 of 1  (showing 100 of 100)
```

**THAT IS NOT THE DENOMINATOR THE SUBTRACTION RUNS OVER, AND SAYING SO IS THE POINT.** It counts
FILES THAT MENTION A TOKEN. A retag member set is subtracted from the population that HOLDS THE
CLASSIFICATIONS, and that population is a served store, not the repo. Two separate defects in
using it as the domain:

1. **Wrong object.** 3,272 files that mention `asset_class` is a census of mentions; the retag's
   members are ticker rows.
2. **Wrong coverage, silently.** This worktree is a sparse cone of six directories. comp-find's
   own line prints **30,426 UNREADABLE** -- it can read about **10%** of the tracked corpus. A
   subtraction over that sweep would arrive with a printed denominator and read as MEASURED.

**THE DENOMINATOR USED: 285 rows.** Instrument, vintage and controls:

| | |
|---|---|
| store | `dynamodb://etf-classifications`, us-east-1, acct 313476888478 |
| key schema | `ticker` HASH, single attribute -> one row per ticker |
| instrument 1 | full `scan`, client-side count |
| **read at** | **2026-09-13T05:41:40Z** |
| page check | `len(Items) == Count == ScannedCount == 285`, **no `LastEvaluatedKey`** -- a page would have one |
| instrument 2 | `scan --select COUNT` -> `Count 285 ScannedCount 285` (server-side, independent of the client merge) |
| instrument 3 | `describe-table` -> `ItemCount 285`. **Recorded as corroboration only** -- ItemCount is a ~6-hourly cache, not a measurement. |
| distinct tickers | 285 (0 duplicates) |
| rows with no `asset_class` | 0 |
| negative control | rows keyed `ZZZ_NO_SUCH_TICKER`: 0 |
| positive control | `GLD` and `VXX`, the two tickers the PRD names by hand at s.4: both present |

**VINTAGE IS THE READ TIME, NOT `last_updated`.** The rows' own `last_updated` maxes at
`2026-08-25T17:48:57Z`, which would suggest nothing has touched the table since August. It has:
`TO-S4-1` (deliverables/`~8`) filled three `sub_asset_class` values by conditional `update_item`
in September and states in its own instance that it left `last_updated` **untouched**. A September
write sits under an August stamp, so that field cannot carry a vintage. (This also re-grounds a
stale PRD figure: s.4 says "282 of 285 populated"; **285 of 285 carry a non-empty
`sub_asset_class` today**.)

*Artifact: `u4_ac1_denominator.py`.*

---

## U4-AC2 -- THE SUBTRACTION

### The rule ladder, read off the spec rather than recalled

PRD `org/missions/D4/POSN/POSN_ASTTAX/prd/POSN_ASTTAX_PRD.md` @`ae66157381`
(blob `bd9f9d1f93836878351540c53c20b84ec8dcb34b`, **byte-identical at HEAD** `72f2417499`).

| rule | statement | source |
|---|---|---|
| R1 | `sub_asset_class == 'Volatility'` -> **Structured** | `:168-179` C-VOL-HEDGE-STRUCTURED; `:132` s.3 |
| R2 | `asset_class == 'hedge'` AND sub in {Gold,Silver,Oil,Commodities} -> **Commodities** | `:168-179` |
| R3 | `sub_asset_class == 'Commodities'` at ANY asset_class -> **Commodities** | `:168-170`; `:133` s.3 |
| R4 | crypto signal -> **Commodities** | `:133` s.3 Commodities *holds* "physical (gold, nickel, silver), **crypto**, and commodity indices" |
| R5 | real-estate signal -> **Alternatives** | `:134` s.3 Alternatives *holds* "real assets (not commodities), private equity, private credit, **real estate**" |

Which of the five classes the ladder can REACH, written as a subtraction rather than a list:
`the five MINUS the classes no rule targets` = {Structured, Commodities, Alternatives}.
**UNREACHED: Fixed Income / Cash, Equity** -- correct, because those two are where un-moved rows
already sit; they are the ladder's fall-through, never its target.

### E0 -- the exclusion made BEFORE the ladder runs, and it is a choice

**0 of 285 rows carry a ratified five-class label as their stored string.** The stored vocabulary
is `equity` / `fixed_income` / `hedge`. On a STRING reading -- "a retag is any row whose stored
value is not a ratified label" -- **the member set is all 285 rows.** That reading is EXCLUDED
here with its reason: the serving layer maps the legacy lowercase vocabulary to the ratified
labels, so `equity`->`Equity` is a RENDERING, not a membership change, and this cell settles which
members the retag would TOUCH -- rows whose CLASS MEMBERSHIP moves. **The competing reading is
named rather than suppressed because it changes the answer by 273.**

### The subtraction

```
  START                                                         285
  MINUS E2   212 rows  served equity and NO rule in the ladder reaches it: not Volatility,
                       not a commodity sub, no crypto/real-estate signal in name or sector.
                       PRD:131 class 2 holds 'equities only', so it is already in its class.
    remainder                                                    73
  MINUS E1    61 rows  served fixed_income and NO rule reaches it: sub is not Volatility, not
                       a commodity sub, name/sector carry no crypto or real-estate signal.
                       PRD:130 class 1 holds 'fixed income and cash'.
    remainder                                                    12
  MINUS E3     0 rows  a legacy value with NO ratified image that no rule reaches.
                       AN EMPTY BUCKET HERE IS THE CLAIM THAT EVERY 'hedge' ROW IS ACCOUNTED FOR.
    remainder                                                    12
  MINUS E4     0 rows  a rule reaches it but the target EQUALS the class it is already served as.
    remainder                                                    12
  ------------------------------------------------------------------
  SURVIVING RETAG MEMBER SET                                      12
  ARITHMETIC CLOSES: 273 excluded + 12 members == 285 denominator
```

Per-rule tally, summing to the member count: **R1 4 | R2 6 | R3 1 | R4 0 | R5 1 = 12.**

### The delta against the standing figure

```
  standing set size : 11        derived set size : 12        intersection : 11
  PRESENT-BUT-UNEXPECTED : ['VNQ']
  EXPECTED-BUT-ABSENT    : NONE
```

**`VNQ` -- Vanguard Real Estate ETF.** Served `asset_class=equity`; its own `sector` field reads
the literal string **`Real Estate`**, which is the literal phrase in class 5's *holds* column at
PRD `:134`. It is reached by R5 and by nothing else, which is exactly why round 3 did not see it:
`AT3-s-5`'s derivation keyed only on `sub_asset_class` and the `hedge` bucket, and VNQ's
`sub_asset_class` is `US Large Cap`.

**WHY VNQ IS COUNTED IN RATHER THAN CARRIED AS A CANDIDATE.** Round 3 counted `UVXY`, `QBER` and
`PDBC` into its eleven while calling them "DERIVED CANDIDATES, not a ruling". Holding VNQ to a
STRICTER standard than the three candidates already inside the standing figure would be
reproducing a remembered number by looking for it. Same standard, same treatment.

**AND `Alternatives` IS AN EMPTY CLASS WITHOUT IT.** Under the standing eleven, the served
registry reaches four of the five ratified classes and no row anywhere targets Alternatives. The
one row whose own field says "Real Estate" is the only thing in the registry that reaches it.

### The arm that was NOT applied, printed so the narrow reading can be falsified

| probe | hits of 285 | rows |
|---|---|---|
| R5-WIDE real assets (infrastructure / timber / farmland / midstream / MLP) | 1 | `BIPC` Brookfield Infrastructure Corp, equity/Utilities |
| R5-WIDE private equity / private credit | 0 | -- |
| R4 crypto | 0 | -- |

`BIPC` is **NOT** counted. R5 fires on the literal phrase "real estate", which is written verbatim
in s.3's Alternatives row AND is the literal value of VNQ's own `sector` field -- that is the spec
speaking. "Infrastructure" appears in **no** class's *holds* text, so calling it a real asset
would be an EDGE RULE, and C-MEMBERSHIP-AT-L5 (`:332-334`) reserves edge rules to L5. It is
recorded UNDETERMINED in the U4-AC3 table rather than guessed or dropped.

### Substring trap, disclosed

A case-insensitive `gold` over the name column returns **3** rows: `GLD`, `GS`, `IAU`. `GS` is
"The Gold**man** Sachs Group Inc" -- a substring hit, not a commodity. It never enters the set
because R2/R3 key on stored fields, not names; only R4/R5 read names and neither pattern matches
it. Printed because a silent substring hit is how a wrong member enters a set that otherwise
looks derived.

*Artifact: `u4_ac2_subtraction.py`.*

---

## U4-AC3 -- EVERY MEMBER, WITH PROVENANCE ON BOTH COLUMNS

**CURRENT** is read on a SECOND instrument -- `batch-get-item` point reads by key, **not** sliced
out of the scan the subtraction ran over, so the two columns of this table do not share one
retrieval. `UnprocessedKeys` verbatim: `{}`. 13 of 14 requested keys resolved; the 14th,
`ZZZ_NO_SUCH_TICKER`, is a negative control and correctly did not resolve. Read at
**2026-09-13T06:01:08Z**. **Cross-instrument control: 13 of 13 rows agree; 0 disagreements.**

**TARGET** is cited to the spec line that rules it, at `@ae66157381`.

Store and key for every CURRENT cell: `dynamodb://etf-classifications`, key `{ticker: <MEMBER>}`.

| member | served value | CURRENT class | TARGET class | rule | target cited to | mgmt_style |
|---|---|---|---|---|---|---|
| DBC | `hedge` | **NONE** -- `hedge` is not one of the five | Commodities | R2 | PRD:168-179 | passive |
| GLD | `hedge` | **NONE** | Commodities | R2 | PRD:168-179, :343-345 | passive |
| GSG | `hedge` | **NONE** | Commodities | R2 | PRD:168-179 | passive |
| IAU | `hedge` | **NONE** | Commodities | R2 | PRD:168-179 | passive |
| SLV | `hedge` | **NONE** | Commodities | R2 | PRD:168-179 | passive |
| USO | `hedge` | **NONE** | Commodities | R2 | PRD:168-179 | passive |
| PDBC | `equity` | Equity | Commodities | R3 | PRD:168-170, :133 | active |
| VXX | `equity` | Equity | Structured | R1 | PRD:168-179, :132, :343-345 | passive |
| VIXY | `hedge` | **NONE** | Structured | R1 | PRD:168-179 | passive |
| UVXY | `equity` | Equity | Structured | R1 | PRD:168-179, :132 | passive |
| QBER | `fixed_income` | Fixed Income / Cash | Structured | R1 | PRD:168-179, :132 | active |
| **VNQ** | `equity` | Equity | **Alternatives** | R5 | PRD:134 | **`unknown`** |
| *BIPC* | `equity` | Equity | **UNDETERMINED** | R5-WIDE | PRD:134 + :332-334 | **`unknown`** |

**COUNTED MEMBERS 12 | UNDETERMINED CANDIDATES NOT COUNTED 1 | TABLE ROWS 13 | BLANK CELLS 0.**

Six of the twelve are in **no class at all today**: `hedge` is not one of the five ratified
classes, so those rows have no ratified image to be rendered into.

### The ARMED half of C-RETAG-SAFETY, re-counted rather than quoted

PRD `:250-255` predicts GLD/IAU/SLV/USO/DBC/GSG all carry the truthy `management_style="unknown"`
placeholder the default-to-passive guard cannot fire on. **They do not, today** -- `TO-S5-1` set
them. Re-measured at the moment of acting:

> **members whose `management_style` is the truthy `unknown` placeholder: `VNQ` and `BIPC`.**

Round 3 recorded "**0 of 11** trip the guard" and that was true of its eleven. Of my twelve,
**1 trips** -- and it is the twelfth. **The one member the standing figure omits is also the only
member of the set that arms C-RETAG-SAFETY's `management_style` half**, so step (1) of the
round-2 retag sequence ("set the affected tickers' `management_style` to the factually-correct
value") currently has an unnamed subject.

*Artifact: `u4_ac3_member_table.py`.*

---

## U4-AC4 -- THE DOMAIN, FALSIFIED OUT LOUD

**THE CLAIM UNDER TEST:** *the population every retag member is drawn from is the 285 rows of
`dynamodb://etf-classifications`.*

### ARM 1 -- the unscoped corpus read

**Named invocation, run verbatim a second time at 06:19:36Z:** `timeout 300 comp-find 'asset_class' --all --files` -> rc 0

```
DENOMINATOR: 21249 hit(s) across 3289 file(s) scanned in scope [corpus=all] | 2 EPHEMERAL-FLOOR,
NOT searched | 30426 UNREADABLE, NOT searched | 35 BINARY, NOT searched
```

⚠ **THE SAME COMMAND READ 1,885 HITS / 3,272 FILES AT 05:5xZ AND 21,249 HITS / 3,289 FILES AT
06:19Z -- 38 MINUTES APART, +19,364 HITS.** The file-list diff names the cause exactly: **14 new
paths, every one of them written by this cell** -- eight `.scratch/` outputs (including the 3.6 MB
`bd-securities` projection, whose 9,631 rows each carry the token), five of my own deliverable
scripts, and `org/mcp/comp-which-rail.log`. `--corpus all` includes untracked and gitignored
files, **so the measuring thread landed in the corpus it measures.** Neither number is wrong;
the first is the honest "before" and both are printed rather than one being quoted.

**AND NEITHER NUMBER IS THE CORPUS.** Both runs report **30,426 UNREADABLE** -- the sparse cone.
So the unscoped read was re-taken on a cone-independent instrument, the git object store, which
does not know what is checked out:

| repo | ref | tree entries | blobs read | skipped >2MB | paths carrying `asset_class`/`assetClass` |
|---|---|---|---|---|---|
| superproject | HEAD `72f2417499` | 33,731 | 32,237 of 32,325 distinct | 88 | **684 of 33,729** |
| portal (separate clone) | pin `e85f6eb84f` | 1,201 | 1,191 of 1,191 | 0 | **87 of 1,200** |

Arithmetic closes in both (32,237 + 88 = 32,325 distinct blobs; 1,191 + 0 = 1,191).
**TOTAL POPULATION READ: 34,929 paths across 2 repos; 771 carry the classification term.**
**NON-BLOB entries NAMED, never absorbed:** `models/factor_scanner` `c59b266adf` and `portal`
`e85f6eb84f` in the superproject, `archive/dashboards/main_dashboard` `c4b68dd45f` nested inside
portal. Negative control `ZZZ_NO_SUCH_TOKEN_QQQ`: 0 paths.

### ARM 2 -- the NECESSARY-DATA population (C-SATELLITE-DATA, PRD:335-348)

The PRD makes the Cottonwood satellite components necessary data and says every one of them must
sort into exactly one of the five classes. Parsed from
`org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_SOURCE_SATELLITE_COMPONENTS_20260911.md` @HEAD:

```
component rows parsed : 228   (matches the PRD's own 228 across 9 satellites)
DISTINCT tickers      : 25
IN the domain         : 25
NOT IN the domain     : 0
positive control      : GLD and VXX, the two the PRD names by hand, both parsed and present
```

**25 of 25 inside the domain. Zero outside.**

### ARM 3/4 -- every REPO site that binds a ticker to a class

274 of the 771 term-carrying paths also carry a class literal; 37 of those bind two or more
quoted upper-case keys including at least one known ticker. The out-of-domain bound keys were
enumerated (48 distinct) and adjudicated rather than counted:

* **20 are real tickers absent from the registry**, all in the seed dict
  `infra/aws/lambda/v2_portal/_shared/etf_classification.py` and its two copies (`partners/...`,
  `yang-generate-etf-returns/...`): ACSG, BSCN, DFAC, EVNT, GARP, IBND, IXJ, JMUB, JPEM, JPMI,
  LDUR, MDY, MRSIX, SCHB, SHV, SMDV, SPLG, STIP, SYLD, WMT. **Every one is bound `equity` or
  `fixed_income`, and 0 of 20 is reached by any ratified rule.**
* `IWD` / `IWF` are real tickers bound to a **geography** value (`'IWD': 'US'`, lambda_function
  `:100-101`), not to a class.
* The rest are not tickers: horizon and period codes (`ST`,`INT`,`LT`,`ULT`,`UST`,`MTD`,`QTD`,
  `WTD`,`YTD`,`EM`,`US`,`LTC`), JSON scaffolding (`API`,`AUM`,`URL`,`SSN`,`TD`,`TE`,`TLH`,`OUB`)
  and this project's own prose tokens (`ABSENT`,`OMITS`,`HEAD`,`RAISED`,`XYZ`,`S`).
* **The two frontend taxonomies bind 36 and 55 keys and 0 of either is outside the domain**
  (`src/pages/Positioning/constants/etf-categories.ts`,
  `src/pages/Attribution/constants/etf-categories.ts`, at pin `e85f6eb84f`).

**POSITIVE CONTROL on the same predicate over the IN-domain dict entries: 12 hits --**
`DBC, DIVZ, GLD, GSG, IAU, PDBC, SLV, USO, UVXY, VIXY, VNQ, VXX`. Eleven are my members (QBER is
not in the dict at all). **`DIVZ` is a deliberate false positive and is disclosed**: its comment
reads "TrueShares **Low Volatility** Equity Income ETF", so a NAME-based predicate matches it
while R1 -- which keys on the STORED `sub_asset_class` whole value, and DIVZ's is `US Dividend` --
correctly does not. That is the argument for keying the ladder on stored fields rather than names,
made by an instrument instead of asserted.

### ARM 5 -- the live plane, because a repo census cannot answer a live-plane question

`dynamodb list-tables` -> 43 tables. **TWO carry a ticker-keyed `asset_class`.**

| | the chosen domain | the second store |
|---|---|---|
| table | `etf-classifications` | **`bd-securities`** |
| key schema | `ticker` HASH | `ticker` HASH -- **the same key space** |
| attributes | `asset_class`, `sub_asset_class` | **the same attribute names** |
| rows | 285 (`--select COUNT`) | **9,631** (`--select COUNT`; `describe-table ItemCount` reads 9,578 -- a ~6-hourly cache, 53 rows stale) |
| vocabulary | `equity` 216, `fixed_income` 62, **`hedge` 7** | `equity` 5422, `fixed_income` 2598, **`alternatives` 1596**, `cash` 15 |

`bd-securities` has an `alternatives` the domain lacks, and no `hedge`.
`data/black_diamond/scripts/classification/seed_bd_securities.py` says why in its own docstring:
*"asset_class 'hedge' remapped to 'alternatives'"*. Its sibling
`seed_canonical_securities.py` writes **both** tables (`--upload --yang`), so the second store is
not purely downstream -- it is also a WRITER of the domain.

```
tickers in bd-securities        : 9631
  also in the domain            :  267
  NOT in the domain             : 9364
rows a ratified rule would reach: 595 of 9631
  of those, NOT in the domain   :  584
```

### THE VERDICT, STATED IN BOTH DIRECTIONS

**1. IS THE SUBTRACTION VOID? NO -- and the test is the order's own:** *"a member the domain does
not hold VOIDS the subtraction."*

> **All 13 members and candidates are held by the domain. Zero lie outside it.** The satellite
> necessary-data population is 25 of 25 inside. Every out-of-domain ticker->class binding in the
> repo (the 20 seed-dict entries) is reached by **no** ratified rule -- measured with the ladder,
> not assumed, with a positive control that fires. **U4-AC2's 12 stands.**

**2. DOES EVERY CLASSIFICATION-BEARING HIT LIE INSIDE THE DOMAIN? NO, AND I SAY SO RATHER THAN
KEEPING THE TIDY ANSWER.** There are 9,364 ticker->class assignments on the same key with the
same attribute names in a second live store, 584 of them reached by a ratified rule; plus 20 in
the repo's seed dict. Under a retag scoped to "the ONE ratified source" the member set is 12;
under a retag scoped to "every store that assigns an asset class" it is not, and the subtraction
over 285 would be void at that grain. **Which scope governs is a spec question, not a worker's:
PRD C-ONE-SOURCE and C-CLASSIFIER-PURPOSE(a) assert there IS one place. The world holds two.**
Filed as a row rather than resolved.

**3. AND THE SECOND STORE DISAGREES WITH THE TARGET ON 13 OF 13:**

| ticker | bd-securities | POSN target | agrees |
|---|---|---|---|
| DBC GLD GSG IAU SLV USO | `alternatives` | Commodities | NO x6 |
| VXX VIXY UVXY QBER | `alternatives` | Structured | NO x4 |
| PDBC | `equity` | Commodities | NO |
| VNQ | `equity` (sub `US Large Cap`) | Alternatives | NO |
| BIPC | `equity` (sub `Developed`) | UNDETERMINED | NO |

**AGREEMENT 0 OF 13.** Note the shape: ten of the disagreeing rows carry **`alternatives`, which
IS one of the five ratified classes**. A check that asks only *"is the served value one of the
five?"* reads PASS on every one of them. **The value is ratified and wrong** -- the same failure
mode as FWD-6 being graded on "do the views agree" (decomp round 4 s.2).

*Artifacts: `u4_ac4_domain_falsification.py`, `u4_ac4b_second_store.py`.*

---

## WHAT THIS CELL DID NOT DO

* **It retagged nothing.** No write was issued against either table. Every AWS call was `scan`,
  `batch-get-item`, `describe-table` or `list-tables`.
* **It did not spawn, flip or touch `TO-T6-1`.** The retag is NO-GO and a settled member set does
  not imply it may run.
* **It did not rule on `BIPC`**, or on whether the retag's scope reaches `bd-securities`. Both are
  L5's under C-MEMBERSHIP-AT-L5; both are recorded.
* **It re-read `AT3-s-5`'s ten change-groups rather than re-deriving them**, per the order's
  read-dependency. They are unchanged by this cell.
* **It wrote nothing outside its `<paths>` grant.** `bd-securities` content is not copied into the
  record: only counts, the shared vocabulary and the 13 rows of the AC3 table are retained.

## THE PROOF INSTANCE SITS AT TWO PATHS, AND THAT IS DISCLOSED, NOT SILENT

`.tools/to-pipeline-gate.py:1602-1608` derives the proof instance's filename from the **task order
file's FULL stem**; this order's `<proof_of_spec>` block names the short `<to_id>` form. An
instance written at the order's own path is **VALID (rc=0) and invisible to the gate**, which
refuses the `complete` flip with *"NO proof-of-spec instance was found beside it"* -- a message
that reads as "you did not write one" rather than "it is not where I look". **10 of the 10 prior
instances on this project use the full-stem name**, so the order's line is the outlier, not the
gate. Both paths therefore carry the instance, **byte-identical**:

| path | |
|---|---|
| `POSN_ASTTAX.TO-U4-1.proof_of_spec.json` | the path the order names |
| `POSN_ASTTAX.TO-U4-1.settle-the-retag-member-set-at-eleven.proof_of_spec.json` | the name the gate derives |

`md5 5e1f4196f09c7d6b72c4270b32e904c3`, identical, `proof-of-spec-check.py` rc=0 on each. **Two
carriers of one quantity is how drift starts**, so the hash is recorded here and in row
`Z-W17-S4`, and either copy being edited alone is detectable by comparing them. The gate's own
`# pipeline-override:` escape was **deliberately not used**: routing around a gate that is
correctly protecting a terminal flip is not a worker's act.

## SURPRISE ROWS FILED

`POSN_ASTTAX-Z-W17-S1` (OBSERVATION, INERT), `-S2` (OBSERVATION, ARMED, `2.0.0_SA_COO~Z`), `-S3`
(OBSERVATION, ARMED, `1.0.0_SA_CTO~Z`), `-S4` (BLOCKING, ARMED, `2.0.0_SA_COO~Z`) -- see
`../../surprise-channel/investigations/INVESTIGATION_v1.md`. The ids carry the `Z-` fabric infix
(this project's `fabric` is `site-z`); the spawn brief stated the bare `W17` form, and the schema
at `org/surprise_channel/schemas/investigation_item.schema.json` requires the fabric coordinate to
agree with the `fabric` field, which is `site-z` for every row in this channel. The gate's own
source agrees: `surprise-row-gate.py:101`, *"the fabric coordinate Z- stays and nests first"*.
