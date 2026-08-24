# ETFS_INGEST.TO-2 — THE CANONICAL CONSTITUENT ROW: four conventions as Rule-24 acts + the superset ruling

**Author:** `0.4.0_DS_ClientPlatform~Z` · **Issued by:** `2.0.0_SA_COO~Z` · **GO:** msg 4930, 2026-08-24T20:29Z
**Cells:** `INGEST-T2-3` · `INGEST-T2-4` · `INGEST-CONV-1` · `INGEST-CONV-2` · `INGEST-CONV-3`
**Criteria:** `INGEST-TO2-AC1..AC5`
**Decomp:** `workflows/atom_decomposition/runs/etfs-ingest/20260824T2010Z/DECOMP.md` @`4bf13f9d68`

> ⛔ **DISCLOSURES THAT TRAVEL ON THIS DOCUMENT'S FACE.** The decomp this TO derives from is a
> **REDUCED-COHORT** run — **one independent perspective, its author's**. It was **CERTIFIED** at
> `fcdf042972` (cert @`422bdb431b`) *after* the TOs were cut, and **a certifier is the SECOND READER,
> NOT THE COHORT**: nobody has independently re-enumerated the operative surfaces. Premise-oracle
> verification in that certification was **a SAMPLE, NOT A CENSUS** — 3 of 36 re-run, 3 of 3
> reproducing; the other 33 are unverified and not asserted by the certificate. **My reading the run
> does not convert it into a fan-out.**

> **SCOPE — THIS IS A SCHEMA-AUTHORING DELIVERABLE, NOT A CONVERTER EDIT.** It rules four
> conventions and the superset decision that frames them. **It changes no code.** The implementation
> is `ETFS_INGEST.TO-4`, deliberately downstream, so the code is written against a decided shape
> rather than deciding it. **`INGEST-T3-6` (the gold row) is a SECOND Rule-24 act at a DIFFERENT
> GRAIN and may not share an axis with these** — it is not mine and I have not pre-empted it; where a
> convention here has a gold-side counterpart I name the boundary rather than legislate across it.

**Evidence planes used, split so one banner does not launder mixed classes:**

| plane | what was read | vintage |
|---|---|---|
| **SOURCE** | `infra/aws/lambda/etfs-pipeline/etfs-netassets-daily/lambda_function.py` (working tree), `integrations/bloomberg/pipeline/etf_daily_pull.py`, `etf_constituents_pull.py` | working tree @ `071f059b32`+ |
| **DATA** | `s3://opal-data-etfs/silver/holdings/*.parquet` — **all 72 partitions, 7,892 rows**, explicit token walk | read 2026-08-24 ~20:40–20:55Z |
| **DATA (issuer)** | `research_transcripts/analysis/source_{divz,idvz}_holdings_20260731.csv` | as committed |
| **EXERCISED** | parquet round-trip of the mixed `is_cash` population through the estate's own `_parquet_bytes` shape; the real `etf_daily_pull.py:88` expression | this session |

---

## §0 — PREMISES RE-DERIVED. Three corrections; all three ACCEPTED by the issuer.

Andrew's posture for this stage is *"validate SOT"*. I re-derived rather than inherited. **Five of
five headline oracles CONFIRMED**; three statements underneath them did not survive.

**CONFIRMED AS WRITTEN:** 17-column shape identical *and ordered* · `is_cash` 4 True / 110 False on
08-23 · BBGID `BBG01Y2F01K3` in the `cusip` column on the TPG row · pct-points, PFDE 100.01 /
PFOE 99.99 · three live consumers at source.

| # | correction | status |
|---|---|---|
| **A1** | **"both [issuers] carry `SALXX`" is FALSE.** SALXX matched **0 of 114** silver rows; the four `is_cash=True` rows are `FXFXX` ×2 and the literal `Cash&Other` ×2. SALXX is on the **TrueShares** oracle CSVs (`source_divz…:2`, `source_idvz…:2`). "Both" was true of **DIVZ+IDVZ, the two TrueShares FUNDS** — a referent that widened to "both issuers" across three faithful copies. **A cash convention written against "the SALXX line" covers ZERO of today's live rows.** | **ACCEPTED**, PRD s.5 @`6e79b8d58e` |
| **A2** | **The as-of cell is TWO CLOCKS, not "four readings".** `date` and `data_as_of` are assigned **the same expression** (`h["data_as_of"]`, `:902`/`:917`) — measured equal on **7,892 of 7,892** rows across all 72 partitions. The issuer's own `Date` **IS** that value (`:612`→`:665`→`:838`). So T2-4's owed *"store the issuer's date verbatim beside it"* is **already satisfied, twice over**. **THE REAL GAP IS THE MIRROR: no column carries the RUN date.** | **ACCEPTED**, T2-4 re-pointed |
| **A3** | **The TO's dropped-column list is wrong in BOTH directions.** It names `SharesOutstanding` and `MoneyMarketFlag` as dropped — **both are consumed** (`:662`→`fund_shares_outstanding`, 114/114 non-null; `:631`→`is_cash`, 114/114 non-null). And it **misses** TrueShares' own `Date`, which *is* dropped. | filed here, §1 |

> **A3 is the direction nobody audits.** An undercount announces itself; an **overcount of what is
> lost** does not, because a column that appears correctly in your own output is never re-checked.
> Two of the three errors here inflate the loss and one hides it.

> ⛔ **I ALMOST FILED A1 OFF THE SILVER READ ALONE.** The silver zero was **real**; the conclusion
> would have been **false**. A silver-layer absence is not an issuer-layer absence. I went to the
> issuer plane before writing it down.

---

## §1 — `INGEST-T2-3`: THE SUPERSET ROW — **RULED: ADOPT the PRD's recommendation** (AC3)

**The tension:** *"unified parquet"* at silver vs **Rule 17's "silver never slims fields."**

### The dropped-column enumeration — DERIVED as a set difference, per issuer, with denominators

Mapping transcribed from the deployed converter (filepoint `:610-632`, TrueShares `:464-473`); the
script asserts map-vs-header identity both directions before reporting, so a transcription slip
raises rather than silently shrinking a denominator.

| issuer | vendor header | consumed | **DROPPED** |
|---|---|---|---|
| filepoint `ETF_Holdings.csv` | **13** | 11 of 13 | **2 of 13** — `Account`, `CreationUnits` |
| TrueShares holdings sheet | **10** | 7 of 10 | **3 of 10** — `Date`, `Account`, `Net Assets` |

**UNION: 4 distinct vendor column names dropped across 2 issuers** — `Account` (both),
`CreationUnits` (filepoint), `Date` (TrueShares), `Net Assets` (TrueShares).

### THE RULING

**The unified silver row is a SUPERSET: the 17 canonical spine columns + every dropped vendor column
verbatim, null where a vendor lacks it. 17 + 4 = 21. ADDITIVE ONLY.**

**Why adopt rather than overturn:** it satisfies Andrew's *"unified"* and Rule 17's *"never slims"*
with **no second path** — which is the shape the shadow-channel veto requires. The 17-column base is
an **ADOPTION** (build-ladder rung 2): both issuers already normalise into it (`:159`), so nothing is
minted. **Adoption is still an authoring act**, which is why it carries this record.

**Additive-only, stated explicitly as AC3 requires:** no existing column is renamed, re-typed, moved
or removed; no existing consumer's column set changes. `opal-data-etfs/silver/holdings/` has **three
live consumers** (`etf_daily_pull.py:88`, `etf_constituents_pull.py:213`, the TO-1 gold producer) and
**none of them selects `*`**; each names its columns. **This design implies NO move, rename or
re-tier** — had it, I would have stopped and routed it rather than deciding it.

⚠ **Two vendor columns collide on the name `Date`/`Net Assets` across issuers with different
meanings.** Vendor columns are therefore stored **issuer-namespaced** (`vendor_filepoint_Account`,
`vendor_trueshares_Date`, …), never merged on bare name — merging them would be the same
two-grains-on-one-axis failure T2-4 records below, imported into the superset.

---

## §2 — `INGEST-CONV-1`: THE CASH LINE → **`cash_basis`** (AC1)

### The four-postulate record

| postulate | statement |
|---|---|
| **(i) MECE** | Values partition **the DECLARED LAYER: every (holdings row × issuer feed) pair that can reach `silver/holdings`.** `vendor-flag` / `vendor-blank` / `vendor-silent` — mutually exclusive by construction (a feed either defines a cash-bearing field or does not; if it does, this row's cell is either populated or not). **CE tested against that layer, then the uncovered member hunted — see below.** |
| **(ii) SAME GRAIN** | Every value is at **one row of `silver/holdings`** — the same grain as `is_cash` itself, i.e. (date × fund × holding). No value is fund-level or feed-level. |
| **(iii) ONE INTENT** | The axis records **the EVIDENTIARY STATE of the vendor's cash assertion — what the feed said.** It does **not** record whether the holding *is* cash (that is `is_cash`) and it does **not** record any inference (that is gold). |
| **(iv) STATE FRAME** | All three values are determinable **at parse time, from the feed header plus this row's cell** — no network call, no judgment, no second artifact. **One remedy (read the header, read the cell) delivers all three; they move together.** PASSES. |

### ⛔ AMENDED 2026-08-24 ~22:20Z — THE VALUES BELOW WERE SUPERSEDED BY IMPLEMENTATION, AND THE CENSUS IS WHY

> **The v1 enum below is struck. It tried to read the encoding OFF A SINGLE CELL, and a single empty
> cell is genuinely ambiguous between "the vendor said no" and "the vendor said nothing" — NO PER-ROW
> RULE CAN RESOLVE THAT, because the information is not in the row.**
>
> **What falsified it (measured on live bronze, `pathfinder/filepoint/bronze/holdings/20260824/`,
> DENOMINATOR 114 data rows): `MoneyMarketFlag` = `''` ×110, `'Y'` ×4, and `'N'` ZERO TIMES.**
> Filepoint is a **PRESENCE FLAG** — it marks positives and leaves everything else empty. **Blank is
> how this vendor says NO.** Applying `vendor-blank → is_cash MUST be null` literally would have
> flipped **110 of 114 rows — 96%** — from a known `False` to NULL.
>
> **The value NAME is where it broke, and it is Rule 24(iii) inside a value's wording** — the same
> test that made me reject `name-inferred` and `none` in this very enum. `vendor-blank` asserts *"the
> vendor did not say"*; the axis measures *what the vendor said*, and **it cannot see whether an
> emptiness is silence or a negative.**
>
> ⛔ **AND I HAD READ THE EVIDENCE AGAINST MYSELF AS EVIDENCE FOR MYSELF.** I quoted
> `etf_schemas.py`'s dtype law approvingly as corroboration: *"MoneyMarketFlag STAYS STRING … mapping
> '' to False would be null-meaning judgment."* Re-read, that line says the vendor tier must not
> decide **BECAUSE `''` IS AMBIGUOUS** — i.e. the question is OPEN. I read it as the answer.
> **A source that says "this question is open" reads almost identically to one that says "and here is
> the answer", when you already have an answer.**

### The values — **AS RULED** (`1.0.0_SA_CTO~Z` msg 5380)

**THE ENCODING IS A PROPERTY OF THE FEED, NOT OF THE ROW.** Each source **DECLARES** its encoding,
the parser **ASSERTS** the declaration against the bytes it just read, and `is_cash` derives from the
declaration. `cash_basis` carries the declared encoding.

| value | the feed's alphabet | `is_cash` | declared by |
|---|---|---|---|
| `presence-flag` | emits **only positives** (`'Y'`); every other row left empty → **blank MEANS NO** | `'Y'`→True, `''`→**False** | **filepoint** |
| `tri-state` | emits `Y` **and** `N` **and** blank → **blank MEANS UNSAID** | `Y`→True, `N`→False, `''`→**null** | *(no feed today)* |
| `field-absent` | **no such column at all** → UNSAID | **null** | **trueshares** |

⛔ **DECLARED, NEVER INFERRED — and this is the load-bearing half.** The tempting implementation is
*"if the column contains no negative token, treat it as a presence flag."* **Rejected.** That makes
**the meaning of every row a function of its cohort**: the first day filepoint emits a single `N` — a
new fund, a vendor tweak, a partial file — the column becomes tri-state and **110 rows silently
re-interpret from `False` to NULL, with no error, no diff, and no event to attribute it to.** It is
the retrieval-control class in spec form: an upstream property silently redefines the domain the
downstream rule measures over, and the output is well-formed in the new domain.

**THE ASSERTION IS THE CONTROL** (`_assert_cash_encoding`): a `presence-flag` feed that ever emits a
negative token **RAISES** rather than re-interpreting every blank row. **Both controls are run and
both behaved** — today's real 114 rows do NOT fire it; the same rows plus one synthetic `'N'` DO.
*A guard nobody has seen fire is a comment.* It is a **parser guard, not alert machinery** — it fails
the run that reads bad data, and the alarm moratorium does not touch it.

*Reading of `vendor-silent`, stated so it is not misread:* it asserts **the FEED carries no such
field** — a structural fact about the header. It does **not** assert that the vendor "has no
opinion", which would be an inference about the vendor rather than a measurement of the feed.

### ⛔ I REJECT THE TO'S SKETCHED ENUM `{vendor-flag, name-inferred, none}` — and the reason is Rule 24 itself

- **`name-inferred` is a JUDGMENT, and it breaks postulate (iii) against the TO's own constraint.**
  Inferring cash-ness from a security name is precisely the gold-tier inference the TO says *"STAYS
  IN GOLD."* Placing it on a **silver provenance** axis mixes *what the vendor said* (evidence) with
  *what we concluded* (judgment) — two intents on one axis. It already has a correct home:
  `etf_positioning_gold.py:480-483 infer_is_cash()`.
- **`none` fails Rule 24(iii) INSIDE the value's wording** — it does not say what is none: no cash?
  no basis? no vendor? A value name is read by everyone who reads a cell; a footnote is not.

### The uncovered member, named rather than left implicit

**A feed that carries a cash indicator in a SHARED or TYPED field** (e.g. an `AssetClass` column
whose value is `"CASH"`) rather than a dedicated one. Under the three values above it would fall to
`vendor-silent` — **which would be wrong, because the vendor did say something.** No such feed exists
today (2 feeds, both checked). **Its arrival is a re-authoring trigger, not a silent stretch of
`vendor-silent`.**

### The live defect this convention exists to prevent — and it is measured, not hypothetical

`filepoint`'s parse is `(r.get("MoneyMarketFlag") or "").strip().upper() == "Y"` (`:631`). **A
MISSING or BLANK `MoneyMarketFlag` yields `False`, not null** — "the vendor left it blank" becomes
"the vendor said no", irreversibly, at silver. `cash_basis` makes that state **expressible**; the
converter must set `vendor-blank` + `is_cash=null` on an empty cell rather than collapsing it.

### `ETFS_INGEST-Z-S14` — the ARMED item this cell carries (BLOCKING × ARMED)

`etf_daily_pull.py:88` is `h.loc[~h["is_cash"], "holding_ticker"]`. With any `is_cash=None` row
present that **RAISES `TypeError: bad operand type for unary ~: 'NoneType'`**. Exercised at four
seats on three shapes.

- **MY DISARM (taken, this turn):** **CONV-1 rules that a null-bearing `is_cash` is INADMISSIBLE to a
  bare unary `~`**, and names `:88` as a consumer that must be adapted before T2-1 lands. Every
  consumer's null-handling becomes a **declared contract** of this convention rather than an
  accident of dtype.
- **DISARMED ≠ REMEDIATED.** The consumer edit is **not my lane** (`integrations/bloomberg/pipeline/`
  is outside Rule 13's `data/**`). Remediation owner `0.0.0_AB_MSTR~Z` under `1.0.0_SA_CTO~Z`'s
  **A5** ruling; separate clock, separate owner.
- **CTO~Z's ruled DIRECTION is adopted into this convention:** `None` → **not cash → INCLUDED** in the
  universe pull, on the asymmetric cost (an included unknown costs one refdata `NOT_APPLICABLE`; an
  excluded unknown would silently drop **every** DIVZ/IDVZ constituent).

### Second face — Rule 24(iv) state coherence, inside this cell

The **parquet TYPE of `is_cash` varies by which issuer delivered that day**: filepoint-only → `bool`,
mixed → `bool`, **TrueShares-only → `null`** (measured). So a multi-partition read is a type conflict
waiting on a delivery gap. **`cash_basis` is a plain string on every row and is therefore
type-stable where `is_cash` is not** — which is a reason to route logic through the basis rather than
through the nullable boolean.

### ⛔ How I got here: I was WRONG TWICE, and both wrong versions were more alarming AND more plausible

1. I hypothesised `None` **coerces to `False` at the parquet write**. **FALSE** — `_parquet_bytes`
   casts only `inferred` (`:889-890`), never `is_cash`; nulls survive, schema stays nullable `bool`.
   **Silver stores the tri-state correctly today.**
2. I then wrote the consumer check as `~h["is_cash"].astype(bool)` — **my paraphrase, not the
   estate's line** — and it *silently kept* the cash rows, which read as an elegant silent-corruption
   finding. **The real line has no `.astype` and RAISES.**

Had the paraphrase shipped I would have filed **silent data corruption against a fail-loud
mechanism**. The downstream tool's verdict cannot distinguish *intact* from
*corrupted-but-matched-by-luck*. **Run the real argv.**

---

## §3 — `INGEST-CONV-2`: THE IDENTIFIER SPINE → **`id_kind`** (AC1)

### The four-postulate record

| postulate | statement |
|---|---|
| **(i) MECE** | Values partition **the DECLARED LAYER: every non-null value appearing in the `cusip` column of `silver/holdings`.** Exclusive by construction (a value is tested against ordered, disjoint form predicates). **Exhaustive by a REQUIRED RESIDUAL** — see the census: the four values sum to **7,892 of 7,892**. |
| **(ii) SAME GRAIN** | One value per **holdings row** — the same grain as `cusip`. Not per security, not per fund. (The same instrument can legitimately carry different `id_kind` in different feeds; the row is the unit.) |
| **(iii) ONE INTENT** | The axis records **WHAT KIND of identifier this value is**, so a consumer routes resolution correctly. It is **not** a quality score, **not** a validity judgment, and **not** a statement about the instrument. |
| **(iv) STATE FRAME** | All four values are determinable **from the value itself** by pure form tests, offline, at parse time. One remedy delivers all four. PASSES. |

### The values — measured over **all 72 partitions, 7,892 rows**

| value | rule | count | of 7,892 |
|---|---|---|---|
| `cusip` | 9 chars **and passes the CUSIP mod-10 check digit** | **7,674** | 97.24% |
| `bbgid` | `BBG`-prefixed, 12 chars (FIGI) | **72** | 0.91% — exactly **1 per partition**, the TPG row, every day |
| `vendor-sentinel` | a vendor placeholder occupying the identifier field for a **non-security** line | **144** | 1.82% — `Cash&Other`, 2 per partition |
| `unclassified` | present, matches no known form — **the REQUIRED RESIDUAL** | **2** | 0.03% |
| | | **7,892** | **100% — exhaustive, verified as an assertion in the script** |

**Check-digit result: of the 7,674 nine-character values, 7,674 pass and 0 fail.** The check digit is
therefore a **perfect discriminator on the real population**, not merely a plausible rule — so
`cusip` is defined by the check digit, not by length alone. A BBGID can never masquerade as a CUSIP:
it is 12 chars and fails the length gate before the digit gate.

### ⛔ THE RESIDUAL EARNED ITS PLACE ON FIRST CONTACT — and this is the CE half working

`unclassified` caught **`CASHEUR`** (2 rows, PFOE, `holding_ticker='EUR'`, `security_name='EURO'`) —
**a fourth population no record in this project names.** The PRD's amended *"THREE populations"*
(CVO~Z msg 4918) was measured on **one day's 114 values**; over **72 partitions there are four**.
**Not a contradiction — a wider denominator.**

⛔ **AND `CASHEUR` MUST NOT BE CLASSIFIED AS `vendor-sentinel`, which is the tempting move.**
Measured: **`CASHEUR` carries `is_cash=False`** — the vendor did *not* flag it as a money-market
line, and it holds a real 0.06 weight. Calling it a cash sentinel would **assert what the vendor
denied**. It is a currency line with a non-identifier in the identifier field. **The residual holds
it, correctly, until someone rules what it is.** *A residual that is never populated is not a
control; this one was populated by the first data it met.*

### The two axes are ORTHOGONAL, and the data proves it rather than the argument

`FXFXX` is a **valid 9-char CUSIP** (`id_kind=cusip`) **and** `is_cash=True`. `Cash&Other` is
`id_kind=vendor-sentinel` **and** `is_cash=True`. `CASHEUR` is `unclassified` **and**
`is_cash=False`. **All three combinations occur**, so `id_kind` and `cash_basis` cannot be collapsed
onto one axis — which is exactly why they are two cells and two records.

### Boundary — stated, not legislated

**Bloomberg resolution for the enrich leg goes through the spine, not the ticker.** IDVZ's lines are
US-listed **ADR** tickers (`BBSEY`, `BNPQY`), which resolve — **but to the ADR line, not the local
line**. `id_kind` types the identifier; **it does not rule which identifier the enrich leg should
prefer.** That choice belongs to `INGEST-T3-4` (leg 3) and I have not made it here.

⚠ **`holding_ticker` has its own second population** and it is not covered by this axis:
`2602335D` on the BBGID row is not a US ticker either. Today `etf_daily_pull.py`'s `[0].isalpha()`
guard happens to exclude it — **luck with good posture, not a rule.** Filed as an observation; a
`ticker_kind` axis would be a **separate** authoring act and I have not minted one.

---

## §4 — `INGEST-CONV-3`: WEIGHT UNITS + CONSERVATION (AC1)

### (a) The unit declaration

**`weight_pct` is PERCENTAGE POINTS at silver.** The `%` is stripped at normalize
(`.replace("%","")`, `:630`/`:471`). **Discriminator, measured: global max single `weight_pct` =
10.82** — a value >1 is impossible under a fraction convention.

⛔ **DO NOT REGULARISE AGAINST PLATINUM.** `holdings[].weight` there is a **FRACTION**, while the book
percentages that aggregate those same weights are **PERCENT**. **That asymmetry is deliberate, it
preserves Models byte-parity, and DS correctly refused to tidy it once already** (ETFS_POSITIONING
Amendment F). This convention **declares the silver unit; it does not propagate it.**

### (b) The conservation check — a MANIFEST FIELD, NEVER A FILTER

| postulate | statement |
|---|---|
| **(i) MECE** | Values partition **the DECLARED LAYER: every (fund × date) partition-slice present in `silver/holdings`.** `within-tolerance` / `outside-tolerance` / `not-evaluated` — exclusive and exhaustive over that layer (a slice either has enough rows to evaluate or does not; if it does, the deviation either clears the bound or does not). |
| **(ii) SAME GRAIN** | ⛔ **Per (fund × date) — DELIBERATELY A DIFFERENT GRAIN FROM CONV-1 AND CONV-2, which are per row.** *That is precisely why it is a MANIFEST field and not a row column*: putting a fund-level verdict on a row would be a file-level value beside a row-level value on one axis — the postulate-(ii) failure this rule exists to catch. |
| **(iii) ONE INTENT** | Records **the measured relation between the weight sum and 100** for a slice. It is **not** a data-quality grade, **not** a pass/fail gate, and **it never selects rows.** |
| **(iv) STATE FRAME** | All three values are computable from the rows already in the partition. One remedy delivers all three. PASSES. |

**Values:** `within-tolerance` · `outside-tolerance` · `not-evaluated` (a shell/zero-row slice).

*Rule 24(iii)-inside-a-value applied:* I deliberately did **not** use `reconciled` / `healthy` /
`ok` — those assert a **conclusion about the data's correctness**, which this axis does not measure.
`within-tolerance` asserts only the measured relation, which is all it can see.

### The tolerance is MEASURED, not typed

Across **all 144 (fund × date) pairs** in the 72 partitions:

```
abs(sum - 100):  mean 0.0158   median 0.0100   max 0.0700
pairs > 0.10 : 0 of 144      pairs > 0.50 : 0 of 144      pairs > 1.00 : 0 of 144
```

**Declared tolerance: 0.10 pct-points**, which clears the **maximum observed deviation (0.07,
`2026-06-16` PFDE)** with headroom while sitting an order of magnitude below any plausible real
break. *An unmeasured exact constant fails closed while looking principled — so this one is derived
from the full population rather than chosen.*

### ⛔ The negative-weight finding — it changes the check, and a naive fix would be a Rule 17 violation

**44 of 7,892 rows carry a NEGATIVE `weight_pct`, and every one of them is the `Cash&Other` line**
(range **−2.83 to +1.64**). The cash line is a **net position that legitimately swings negative** (a
payable).

- **A conservation check assuming non-negative weights is wrong.**
- **Dropping negative rows would be a business-row filter — forbidden at silver by Rule 17 — and it
  would also break the very sum it was meant to protect.**
- The check is therefore a **recorded measurement over every row as delivered**, with no exclusions.

---

## §5 — `INGEST-T2-4`: THE AS-OF CONVENTION → **adopt `as_of_basis`** (AC1)

### ⛔ THIS IS AN ADOPTION, NOT A MINT — and the census is what caught it

**`as_of_basis` already exists in this estate: 619 hits, 13 in first-party source.** It is live in
`opal-assets-daily-emitter` (`:626`, `:647`, `:823`, `:1050`, `:1150`, `:1308`, `:1465`, `:1494`) and
carries exactly my intent — *which basis the as-of was read from*. **Minting a new name beside it
would have been the re-coin build-ladder rung 2 exists to prevent, and I would have shipped it blind
without AC2's census.**

⚠ **Two declared differences I am NOT papering over:**
1. **GRAIN** — existing usage is at emitter/portfolio-row grain; mine is at **holdings-row** grain.
   Same intent, different table, each declaring its own grain.
2. **DOMAIN FORM** — existing values are **free text** (`"min(etf_feeder_vintage) -- the OLDEST
   contributing feeder"`, `"none: no vouchable constituent vintage"`). Mine is a **closed enum**.
   **A consumer unioning the two would meet incompatible domains**, and that is stated here rather
   than discovered later. Reconciling them is a separate act at a higher grain; I have not done it.

### The four-postulate record

| postulate | statement |
|---|---|
| **(i) MECE** | Values partition **the DECLARED LAYER: every issuer feed that can produce a holdings row.** Exclusive (a row's as-of is read from exactly one source), exhaustive via `run-date` as the declared fallback. |
| **(ii) SAME GRAIN** | One value per **holdings row**, alongside the `date` it describes. |
| **(iii) ONE INTENT** | Records **WHERE the row's declared as-of came from.** It is not the as-of value (`date`), not the run clock (`_ingested_at`), and not a freshness verdict. |
| **(iv) STATE FRAME** | Determinable at parse time by the converter, which knows which source it read. One remedy delivers all values. PASSES. |

### The values

| value | means | today |
|---|---|---|
| `issuer-holdings-file` | the as-of came from **the holdings artifact's own date field** | **filepoint** (`:612`, `ETF_Holdings.csv` `Date`) |
| `issuer-page-netassets` | the as-of came from a **NET-ASSETS as-of on the fund page** — *not a holdings date* | **TrueShares** (`:526`, `_ts_asof_after(html, ">Net Assets<")`) |
| `run-date` | no issuer-side as-of available; the run date stands in | none today |

### ⛔ THE DEFECT THIS MAKES EXPRESSIBLE — one column, two grains, currently silent

**The two issuers reach `date` by different KINDS of source**, and both land in the same column with
no marker:

```
filepoint    :612 holdings_date = _norm_date(fund_rows[0].get("Date"))   <- a HOLDINGS-FILE date
trueshares   :526 "net_assets_as_of": _ts_asof_after(html, ">Net Assets<") <- a NET-ASSETS page as-of
   both  ->  :838 data_as_of  ->  :902 `date`  AND  :917 `data_as_of`
```

**That is a Rule 24(ii) same-grain violation living inside one column.** It is invisible today only
because DIVZ/IDVZ carry zero holdings rows — **it becomes real with tonight's 22:00Z fire.**
Worse: **the TrueShares holdings sheet's own `Date` column is DROPPED** (§1), so for those rows the
true holdings as-of is **discarded**, not merely unused. **§1's superset restores it as
`vendor_trueshares_Date`** — the two cells' remedies compose, which is a property I checked rather
than assumed.

### The mirror gap: a RUN-DATE COLUMN

Measured across all 72 partitions:
- `date` **==** `data_as_of` on **7,892 of 7,892** rows — **one value stored twice**, exactly as source predicts.
- `_ingested_at`'s date-part **==** the object key on **7,892 of 7,892** rows — **the same clock**.
- **offset (`date` − key): 0 on 5,910 · +1 on 992 · +2 on 884 · +3 on 106.** Never negative,
  **and NOT CONSTANT.**

**Therefore the run date cannot be derived from `date` by subtracting anything.** It survives only in
`_ingested_at` (a string timestamp) and in the **object key** — and **all three consumers read ROWS,
not keys**, so a consumer holding a dataframe cannot recover which run produced it.

**RULED: silver carries an explicit `run_date` column** (the run clock as a date, matching the object
key). `date` stays the declared issuer as-of; `data_as_of` is a **redundant duplicate of `date`** and
is retained unchanged **for consumer compatibility** — *removing it would be slimming, which Rule 17
forbids, and this convention has no mandate to break a consumer.*

---

## §6 — AC2: TOKEN-HYGIENE CENSUS

`comp-find -i`, word-boundary, **denominator printed for every name**. `-i` on every one: this estate
capitalises its load-bearing words, and **the dangerous case is the UNDERCOUNT** — comp-find guards a
ZERO with a warning naming `-i` itself, but a *partial* case-miss returns a confident non-zero count
with **no caveat at all**. Checked against `comp-estate --definitions` (SYSTEM_DEFINITIONS v3.22)
first, per build-ladder rung 2.

| proposed name | hits | scanned | verdict |
|---|---|---|---|
| **`as_of_basis`** | **619** (SURFACED 13 · CONFIG 596 · TEST 3 · DOC 7) | 27,968 | ⛔ **EXISTING ESTATE FIELD — ADOPTED, NOT MINTED.** See §5. |
| `cash_basis` | 4 | 27,968 | clear — no ratified-term collision |
| `id_kind` | 5 | 27,968 | clear |
| `weight_basis` | 0 | 27,968 | clear |
| `weight_sum_pct` | 0 | 27,968 | clear |
| `vendor-flag` | 7 | 27,968 | clear (incidental prose) |
| `vendor-blank` | 3 | 27,968 | clear |
| `vendor-silent` | 6 | 27,968 | clear — one prior use is a **different grain** (`PROOF_OF_SPEC_P1_COT_C…:65`, "vendor-silent externals"), same *sense*, no conflict |
| `vendor-sentinel` | 0 | 27,968 | clear |
| `issuer-holdings-file` | 0 | 27,968 | clear |
| `issuer-page-netassets` | 0 | 27,968 | clear |

**No proposed value name collides with a `SYSTEM_DEFINITIONS` ratified term.** The one collision
found is at the **field-name** level (`as_of_basis`) and is resolved by **adoption with two declared
differences** rather than by re-coining.

---

## §7 — AC4: EXERCISED ON DISCRIMINATING ROWS

⛔ **A convention validated only against rows it was written from is a test that cannot fail.** Each
row below was chosen because it **breaks** the naive form of its convention.

| convention | discriminating row | naive rule's answer | this convention's answer | verdict |
|---|---|---|---|---|
| **CONV-1** | the **`Cash&Other`** line (144 rows, `is_cash=True`, weight **−2.83…+1.64**) | a name-based rule calls it cash — a **judgment at silver** | `cash_basis=vendor-flag`; `is_cash=True` **because the vendor said so**; the inference never happens at silver | **PASS** |
| **CONV-1** | a **TrueShares row** (`is_cash=None`, `TS_HOLDINGS_HEADER` has no flag field) | `None`→`False` = "vendor said no" | `cash_basis=vendor-silent`, `is_cash=null` — **distinguishable** | **PASS** |
| **CONV-1** | **`etf_daily_pull.py:88`** against a mixed frame | bare `~` **RAISES TypeError** | null-handling is a **declared contract**; consumer named for adaptation | **PASS (armed→disarmed)** |
| **CONV-2** | the **PFDE TPG row** — `BBG01Y2F01K3` in the `cusip` column | 12 chars in a CUSIP column reads as a CUSIP | `id_kind=bbgid`; fails the length gate before the check-digit gate — **cannot masquerade** | **PASS** |
| **CONV-2** | **`CASHEUR`** (`is_cash=False`, weight 0.06) | a length-only rule → "malformed CUSIP"; a cash-name rule → "sentinel", **asserting what the vendor denied** | `id_kind=unclassified` — **the residual holds it** | **PASS — and it found a population no record named** |
| **CONV-2** | all **7,674** nine-char values | length-only accepts anything 9 chars | check digit: **7,674 pass / 0 fail** — a perfect discriminator on the real population | **PASS** |
| **CONV-3** | **PFOE's negative `Cash&Other` weight** (−2.83) | a non-negative assumption, or a filter dropping it | recorded as delivered; **no exclusion**; conservation still sums | **PASS** |
| **CONV-3** | **144 (fund × date) pairs** | an invented tolerance | max observed 0.07 → **declared 0.10, derived** | **PASS** |
| **T2-4** | **1,982 rows where `date`'s date-part ≠ the object key** (offsets +1/+2/+3) | "the key is the as-of" | `date` = issuer as-of + `as_of_basis`; **`run_date` carries the key's clock explicitly** | **PASS** |
| **T2-4** | a **TrueShares row** once tonight's fire lands | one `date` column, two source kinds, **silent** | `as_of_basis=issuer-page-netassets` makes the difference **declared** | **PASS (design; row lands 22:00Z)** |

⛔ **The last row is a DESIGN verdict, not an exercised one** — no TrueShares holdings row exists in
silver at this hour. It is marked so rather than counted as exercised.

---

## §8 — AC5: RULE 17 COMPLIANCE, STATED PER CONVENTION

| convention | field slimmed? | fillna/dropna? | business-row filter? | judgment at silver? | where the judgment lives instead |
|---|---|---|---|---|---|
| **T2-3 superset** | **No — the opposite.** 17→21, additive only; 4 vendor columns **restored** | No | No | No | — |
| **CONV-1** | No | **No** — `vendor-blank`/`vendor-silent` exist precisely so a null is **recorded**, never filled | No | **No** — records *who said what*, never what we concluded | `etf_positioning_gold.py:480-483 infer_is_cash()` |
| **CONV-2** | No | No | No | **No** — types the identifier's **form**; asserts nothing about the instrument | enrich-leg preference is `INGEST-T3-4`, not ruled here |
| **CONV-3** | No | No | ⛔ **No — and this is the load-bearing one.** The conservation check is a **recorded measurement**, never a selection. Negative weights are **kept** | **No** — records the measured relation, not a verdict on the data | any accept/reject on that measurement is gold's |
| **T2-4** | **No** — `data_as_of` is retained though redundant; removing it would be slimming | No | No | **No** — records **where the as-of came from**, not whether it is fresh | freshness/staleness verdicts are not silver's |

**No new gate, no alarm, no SNS topic, no monitor, no freshness checker was built or proposed by this
deliverable** (standing moratorium). **No code was changed. No apply was performed** (Rule 13 — I
author `data/**`; AE-class deploys).

---

## §9 — BOUNDARIES HELD, AND WHAT REMAINS OPEN

**Held:**
- **No move, rename or re-tier of `opal-data-etfs/silver/holdings/`.** The design is additive-only and implies no move. Three live consumers, none selecting `*`.
- **`PATHFINDER_FUNDS` untouched** — the filepoint/TrueShares scope asymmetry is a **field, not a defect**.
- **Platinum's fraction-vs-percent asymmetry untouched** — deliberate, preserves Models byte-parity.
- **`INGEST-T3-6` (the gold row) not pre-empted** — a second Rule-24 act at a different grain, separate cell, separate TO.
- **`ETFS_INGEST-Z-S14` disarmed at my lane, NOT remediated by me** — the consumer edit is outside `data/**`.

**Open, and owned elsewhere:**

| item | owner |
|---|---|
| `Z-S14` remediation — the one-expression null-tolerance at `etf_daily_pull.py:88` (A5-authorized) | `0.0.0_AB_MSTR~Z` |
| What `CASHEUR` **is** — the residual holds it; nobody has ruled it | routed to `2.0.0_SA_COO~Z` |
| A `ticker_kind` axis for `holding_ticker`'s second population (`2602335D`) | not minted; a separate authoring act |
| Reconciling `as_of_basis`'s free-text estate domain with this closed enum | a higher-grain act, not this TO |
| **`HOLDINGS_COLUMNS` has TWO first-party definition homes** — Lambda `:156` and `etf_netassets_watch/etf_probe.py:132` (names identical today; diffed, only comments differ). Rule 22a two-homes class | not my cell; surfaced only |
| The four disagreeing in-estate cash vocabularies (O1) — `build_inventory.py:26` vs `:76`/`:103` vs `build_etf_materiality.py:45` vs the Lambda's flag | surfaced; evidence **for** `cash_basis`, not fixed here |
| ⛔ **`proof-of-spec-check`'s own `firm` enum is NOT collectively exhaustive over the estate's live projects.** It admits `['49F','INF','COT','MDPF','FABRIC']` — **there is no `ETFS`**, so `ETFS_INGEST` cannot state its own firm. I entered **`FABRIC`** as the least-wrong value **and declare it here rather than letting a mislabel pass silently**: this instance is labelled `FABRIC` and is **not** fabric work. **That is a Rule 24(i) CE failure in the validator's own schema** — the same postulate the schema exists to enforce, failing one layer up, exactly as `INGEST-INV-1..4` did for the decomp. `phase` has the same shape (no schema-authoring value; entered `NON-BUILD-OTHER`) | routed to `2.0.0_SA_COO~Z` for the gate owner |

---

## Provenance of every number in this document

Every count above is **derived from a script run against the live artifact or the source**, never
typed from recollection and never copied from the decomp. The three scripts are in this session's
scratchpad; the reproducible reads are: the 72-partition token walk (`list_objects_v2` with explicit
`ContinuationToken`, **not** `--query length`), the full 7,892-row concat, and the `_parquet_bytes`
round-trip. **Where I reproduce a figure another seat measured, I say it is same-plane corroboration
rather than independent confirmation.**

**Commit state:** authored at `0.4.0_DS_ClientPlatform~Z`; **commits land LOCAL on this lane and are
NOT pushed** (integrator-only, LD-0367).
