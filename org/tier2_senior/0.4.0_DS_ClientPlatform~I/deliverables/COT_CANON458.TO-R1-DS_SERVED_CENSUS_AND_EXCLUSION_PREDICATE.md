# COT_CANON458.TO-R1-DS — THE SERVED CENSUS + THE EXCLUSION PREDICATE

**seat:** `0.4.0_DS_ClientPlatform~I` · **issuer:** `2.0.0_SA_COO` · **TO:** `COT_CANON458.TO-R1-DS` @`54f06627e6`
**decomp:** `workflows/atom_decomposition/runs/cot-458m-canonical/20260825T032500Z/DECOMP.md` (cells `COT-a-1..4`, `COT-b-1..3`, `COT-inv-3/4/5` — 10 of 23)
**measurement window:** 2026-08-25T10:06:31Z – 10:52:27Z (UTC; every timestamp below is the `s3api`/boto3 plane)
**MEASUREMENT ONLY. NOTHING HERE PUBLISHED, EMITTED, OR MOVED A SERVED BYTE.**

---

## 0. THE THREE FINDINGS THAT MATTER, BEFORE THE DETAIL

1. **THE CANONICAL FIGURE IS SERVED NOWHERE TODAY.** `458,053,742.19` occurs **0 times across all 21
   served leaf types**. Positive control on the same matcher: `488,460,108.95` occurs **73 times across
   12 leaf types**. This is a *controlled* zero, not a search that failed.
2. **THE EXCLUSION PREDICATE CANNOT BE APPLIED AT THE SERVED PLANE TODAY — for TWO independent reasons,
   and either one alone is disqualifying.** `D_05`'s series **ends 2026-08-19**; every served leaf is
   `data_as_of` **2026-08-21**. There is no 08-21 row to apply. And `D_05` is explicitly **DataMining-plane**
   with a self-declared **−$8,697,205.48** gap to the plane the served headline sits on.
3. **APPLYING IT ANYWAY REPRODUCES THE NUMBER ANDREW CALLED WRONG, AND I MEASURED THAT RATHER THAN
   INHERITING IT.** `D_05.firm_daily[-1].aum_supervised` @2026-08-19 = **`449,733,561.36`**. That is the
   449.7M. The decomp predicted it; this is the figure read off the live artifact.

---

## 1. CANR1DS-AC1 — THE CENSUS, WITH ITS DENOMINATOR

**Prefix (named, per `COT-inv-4`): `s3://opal-data-cot/platinum/`**

| measure | value |
|---|---|
| objects | **1,125** |
| distinct leaf NAMES (basename) | **20** |
| distinct served-leaf TYPES (shape × leaf) | **21** |
| measured at | **2026-08-25T10:06:31Z** |

**Method:** `aws s3api list-objects-v2 --bucket opal-data-cot --prefix platinum/` — auto-paginated,
projection-only `--query`, **no `--no-paginate`, no `length()`**, count taken client-side over the
materialised list.

**Controls.** Independent instrument (`aws s3 ls --recursive --summarize`) → `Total Objects: 1125` — agrees.
Negative control (`platinum_zzz_no_such_prefix_9999/`) → `None`; the probe discriminates.
Determinism: two runs, **0 diff lines, identical md5 `b4c6fd9a…`** *after CRLF normalisation* — see §6.

**⛔ THE 1,125 IS THE SAME NUMBER THE DECOMP RECORDED AT ~03:25Z, AND THAT IS AN OBSERVATION, NOT AN
INHERITANCE.** I re-measured because the cell says to; the count happens not to have moved in ~6.7h.
**Stating it as "unchanged" is only legitimate because both endpoints were measured** — had I skipped the
re-measure, the identical digit would have been indistinguishable from a copy.

### 1a. The mandated plane proof, run on ONE object

| tool | rendering of `platinum/firm/header_metrics.json` LastModified |
|---|---|
| `aws s3 ls` | `2026-08-24 07:35:36` (LOCAL, **no marker**) |
| `aws s3api head-object` | `Mon, 24 Aug 2026 11:35:36 GMT` (UTC) |

**Offset = exactly 4h (EDT).** Every figure in this document is the UTC plane.

### 1b. Structure — where the 1,125 live

| 2nd-level prefix | objects | distinct leaves | grain |
|---|---|---|---|
| `platinum/clients/{client_id}/` | 1,109 | 5 | per-client (**222** client dirs) |
| `platinum/firm/` | 12 | 12 | firm |
| `platinum/advisors/{advisor}/` | 3 | 3 | advisor (**1** dir: `cottonwood_capital_advisors`) |
| `platinum/cottonwood/` | 1 | 1 | firm |
| **total** | **1,125** | — | — |

`221` × `composition.json` vs `222` for the other four client leaves: **one client dir (`z09305728`) carries
4 leaves, not 5.** Every other client dir carries exactly 5. Reported as measured; not diagnosed (out of scope).

### 1c. ⛔ THE GRAIN CORRECTION — 20 IS A LEAF-NAME COUNT, NOT A LEAF COUNT

`summary.json` exists under **two** shapes — `platinum/advisors/{a}/` and `platinum/clients/{id}/` — and they
are **different artifacts with different producers' payloads at different grains.** So:

- **20** = distinct leaf NAMES
- **21** = distinct served-leaf TYPES (the classifiable population)

**Classifying on the bare leaf name would fuse an advisor-grain artifact with a client-grain one under one
verdict** — the same shape as the issuer's own `30 of 64` fusion, one axis over. **AC2 below is classified on
the 21, and the 20 is retained only as the name-count it actually is.**

---

## 2. CANR1DS-AC2 — CLASSIFICATION ON TWO FIELDS

**Field (i): does it carry a firm total? Field (ii): on which basis?**
Bases: **ALL-ASSETS** · **COTTONWOOD-SUPERVISED** (the canonical 458M) · **OPAL-SUPERVISED** · **UNDETERMINED**.

### 2a. ⛔ A LEAF CAN CARRY THE FIRM TOTAL WITHOUT CARRYING A TOTAL *FIELD*

This is the finding that changes the shape of the answer, and a field-scan alone would have missed it in
**both** directions.

| leaf | mechanism | measured |
|---|---|---|
| `firm/client_directory.json` | **no total field at all** — 222 households, each `{household_id, display_name, aua}` | `SUM(aua)` = **488,460,108.90** — the headline **less $0.05** (rounding) |
| `firm/cumulative_chart.json` | segment rows, no total field | `geo`/`adv`/`ofc` last row each sum to **488,460,108.95**, delta **0.00** |

**So "carries a firm total" is a property of what the leaf *determines*, not of what it *names*.** A census
keyed on total-shaped field names marks `client_directory` as carrying no total — and it would be silently
wrong, because **excluding held-away from the headline while leaving 222 household rows unadjusted leaves the
directory summing to 488M beside a 458M headline.** That is the adjacency-lies class on a client-facing surface.

### 2b. The classification (21 types, MECE, printed both ways)

**CARRIES A FIRM TOTAL — 14 of 21. Basis ALL-ASSETS on all 14** (matched exactly against `488,460,108.95`,
or summing to it):

| # | served-leaf type | where the total sits | basis |
|---|---|---|---|
| 1 | `platinum/firm/header_metrics.json` | `.total.aua` | ALL-ASSETS |
| 2 | `platinum/firm/dashboard.json` | `.headline.total_aua` (+7 more) | ALL-ASSETS |
| 3 | `platinum/firm/clients-tab-slim.json` | `.headline.total_aua`, `.tax.taxable` | ALL-ASSETS |
| 4 | `platinum/firm/leaderboard.json` | `.windows.1Y.summary.total_aua` | ALL-ASSETS |
| 5 | `platinum/firm/partner_analytics_annual.json` | `.views.aua.current.donut.total` | ALL-ASSETS |
| 6 | `platinum/firm/partner_analytics_monthly.json` | `.views.aua.current.donut.total` | ALL-ASSETS |
| 7 | `platinum/firm/partner_analytics_quarterly.json` | `.views.aua.current.donut.total` | ALL-ASSETS |
| 8 | `platinum/firm/timeseries_chart.json` | `.aua.quarterly.data[1].NMEC` | ALL-ASSETS |
| 9 | `platinum/firm/timeseries_overview.json` | `.aua.quarterly.data[1].NMEC` | ALL-ASSETS |
| 10 | `platinum/firm/cumulative_chart.json` | **implicit** — `geo`/`adv`/`ofc` segments sum to it | ALL-ASSETS |
| 11 | `platinum/firm/client_directory.json` | **implicit** — 222 household `aua` sum to it | ALL-ASSETS |
| 12 | `platinum/advisors/{a}/summary.json` | `.book.total_aua` | ALL-ASSETS |
| 13 | `platinum/advisors/{a}/timeseries.json` | `.data[99].total_aua` (historical series) | ALL-ASSETS |
| 14 | `platinum/firm/mix_summary.json` | `.composition.total_market_value` | ⛔ **UNDETERMINED** — see 2c |

**CARRIES NO FIRM TOTAL — 7 of 21. NOT A GAP; MUST NOT BE "FIXED".**

| # | served-leaf type | what it carries instead |
|---|---|---|
| 15 | `platinum/clients/{id}/summary.json` | client grain; `detail.total_aua` is one client. **No firm denominator present** (checked) |
| 16 | `platinum/clients/{id}/views.json` | client grain, period mix |
| 17 | `platinum/clients/{id}/composition.json` | client grain, holdings |
| 18 | `platinum/clients/{id}/concentration.json` | client grain, holdings |
| 19 | `platinum/clients/{id}/mix_timeseries.json` | client grain, mix series |
| 20 | `platinum/advisors/{a}/nna_clients.json` | `total_nna` = **11,463,447.19** — an **NNA flow** total, not an AUM firm total |
| 21 | `platinum/cottonwood/ownership_map.json` | advisor structure only (107 B), no monetary value |

**DENOMINATORS: 21 classified / 21 in the population. Carries-a-total 14 · carries-none 7. Basis ALL-ASSETS 13 ·
UNDETERMINED 1 · COTTONWOOD-SUPERVISED 0 · OPAL-SUPERVISED 0. Unclassified 0.**

### 2c. ⛔ THE ONE UNDETERMINED, AND WHY I AM NOT ASSIGNING IT

`platinum/firm/mix_summary.json` serves a firm-level total of **`485,982,064.49`** — **$2,478,044.46 BELOW the
headline**, at the **same `data_as_of` (2026-08-21)**.

- Internally consistent: `mix.{equity, fixed_income, alternatives}` sum to it **to the cent** (delta `0.00`).
- **`unclassified` is `{count: 0, market_value: 0.0}`** — so the gap is **NOT** "unclassified excluded", which
  is the obvious explanation and is **measurably false**.
- Its `mix[*].pct` values (0.8660 / 0.1299 / 0.0041) are computed against **485,982,064.49**, not the headline.

**I cannot determine from the artifact which population this covers** (a holdings-priced market value vs an
account-level AUA figure is the plausible read — and "plausible" is exactly what AC2 forbids recording).
**Reported UNDETERMINED.** Per the TO's own worthlessness test: a leaf confidently mis-assigned reconciles,
and nobody looks again.

### 2d. Rule 24 four-postulate record for this axis

**Axis: "does this served-leaf type carry a firm total, and on what basis" · grain: one served-leaf TYPE.**

| postulate | verdict |
|---|---|
| **(i) MECE** | Field (i) is boolean over the 21; field (ii) is exhaustive over the three declared bases **+ UNDETERMINED**, which is what makes it collectively exhaustive without guessing. 14 + 7 = 21, no overlap. |
| **(ii) SAME GRAIN** | **This postulate is why §1c exists.** The bare-leaf-name axis (20) mixes an advisor-grain and a client-grain `summary.json` on one value; the shape×leaf axis (21) does not. Classified on the 21. |
| **(iii) INTENT COHERENCE** | One intent per field, deliberately split into two: carries-a-total (structure) and basis (semantics). Fusing them is the defect the cell names — a single "is it 458M-ready?" axis would carry both. |
| **(iv) STATE COHERENCE** | ⛔ **FAILS, AND IT MUST BE NAMED.** The 13 ALL-ASSETS leaves move on one remedy (apply the exclusion). **`mix_summary` (UNDETERMINED) does not** — its total is not the headline, so an exclusion applied to the headline leaves it on a third number. **And the 2 IMPLICIT-total leaves (`client_directory`, `cumulative_chart`) do not move on a headline change at all** — they move only if their *component rows* are adjusted. **A remedy that edits the total-bearing fields silently covers 11 of 14.** |

---

## 3. CANR1DS-AC3 — PRODUCERS (BY BUILD INPUT) + DERIVED FIGURES

### 3a. ⛔ THE FILENAME TRAP FIRED, EXACTLY AS THE CRITERION WARNED

`grep SERVED_KEY` over `data/cot/scripts/gold/` returns **7 declarations / 6 distinct keys**, and
`platinum/firm/header_metrics.json` is declared **TWICE** —
`runners_cot/d01_cot_firm_header_metrics.py:46` and `runners_cot/d02_cot_value_overlay.py:33`.

**Resolving the producer from that constant would have named the wrong producer for every total-bearing leaf.**
**NEITHER FILE WRITES TO S3.** `grep put_object|upload_file|boto3` returns **zero hits in both.** `d01`'s own
docstring says it outright:

> *"QA ONLY in this act: `--output-root` emission + run-and-read diff vs the live object. **NO S3 writes**
> (the port is a later, sequenced act; base holds cot deploy windows)."*

`d02` is a **value-parity comparator** (pre-registered bands, `--qa-emitted … --out <path>`), not a producer.
**The whole `runners_cot/d*` family is an unported parallel re-implementation.** `SERVED_KEY` there names the
**subject of comparison**, not a write target — a constant whose name reads like provenance and is not.

### 3b. The producers of the LIVE bytes, resolved on the artifact itself

**Discriminator: `CacheControl`, which the two live producers set differently and which is readable off every
served object.**

| producer | `CacheControl` it writes | live objects carrying it |
|---|---|---|
| `D_04.client_portal_summary.py` (`_write_json_to_s3:239`) | `no-store, no-cache, must-revalidate` | **20 of 21** |
| `D_00.portal_aggregates.py` (via `lib/s3_layout.py:186`) | `public, max-age=300, s-maxage=3600` | **1 of 21** — `platinum/cottonwood/ownership_map.json` |

**So `D_04.client_portal_summary.py` is the producer of 20 of the 21 served-leaf types, including all 14
total-bearing ones.** This is resolved from the deployed object's own headers, not from a filename.

### 3c. ⛔ A GENUINE TWO-PRODUCER OVERLAP ON 3 SERVED KEYS

`D_01.partner_analytics.py:2643-2650` **also** `put_object`s `platinum/firm/partner_analytics_{granularity}.json`
— the same 3 keys `D_04` writes. Its own comment:

> *"TEMPORARY direct-write; the fast-follow wires the standard gold/artifacts->platinum publish + chains D_01."*

**The fast-follow has not landed.** Today the live objects carry `D_04`'s header, so `D_04` wrote last — but
that is **last-writer-wins ordering, not a design**, and the two producers disagree about the object's cache
policy. **One logical served key, two independently-editable writers** — flagged, not adjudicated.

### 3d. Declared write targets that produce NOTHING served

Checked against the materialised 1,125-key list **and** re-checked live. Positive control on the same probe
shape (`platinum/firm/header_metrics.json`) → **1 hit**, so the probe discriminates.

| declared in `D_04` | census hits | live |
|---|---|---|
| `platinum/firm/fee_efficiency.json` | 0 | **404** |
| `platinum/firm/leaderboard.prior_week.json` | 0 | **404** |
| `platinum/advisors/{aid}/positions.json` | 0 | **404** |
| `platinum/advisors/{aid}/mix.json` | 0 | — |
| `platinum/accounts/{acct}/summary.json` | 0 (no `platinum/accounts/` prefix exists) | — |

**Denominator for every probe: 1,125 keys, materialised 2026-08-25T10:06:31Z, prefix named.**
Reported as measured; whether each is gated-off or dead code is **not** diagnosed here.

### 3e. `COT-a-4` — DERIVED FIGURES, AND WHOSE DENOMINATOR MOVES

**Denominator = THE FIRM TOTAL — these move when the total moves:**

| leaf | field | measured |
|---|---|---|
| `firm/partner_analytics_{a,m,q}.json` | `.views.aua.*.donut.segments[*].aua_pct` | **80 / 313 / 160** occurrences; segments sum to the total exactly (delta `0.00`) |
| `firm/partner_analytics_{a,m,q}.json` | `.views.geo.current.donut.unassigned_pct` | `5.1301` |
| `firm/partner_analytics_{a,m,q}.json` | `.views.ofc.current.donut.segments[*].pct_of_firm_clients` | count-based |
| `firm/header_metrics.json` | `.by_architect[0].aua_pct` | `100.0` |
| `firm/leaderboard.json` · `advisors/{a}/summary.json` | `role_breakdown.*.pct_of_tagged` | 5 each |
| `firm/dashboard.json` | `.headline.fee_rate_pct`, `.income_yield_pct`, `…aua_growth_pct` | placeholder zeros today |
| `firm/cumulative_chart.json` | every `geo`/`adv`/`ofc` segment | **the segments ARE the decomposition of the total** |
| `firm/client_directory.json` | every household `aua` | **the rows ARE the decomposition of the total** |

**Denominator = `mix_summary`'s OWN total (485,982,064.49), NOT the headline — a THIRD denominator:**
`firm/mix_summary.json` `.mix.*.pct` (58 occurrences).

**Denominator = A CLIENT total — these do NOT move with a firm exclusion:**
`clients/{id}/composition.json` `.top_holdings[*].pct` (30) · `clients/{id}/concentration.json` (414) ·
`clients/{id}/summary.json` `.mix.*.pct` (20) · `clients/{id}/views.json` (24).

**Denominator = ADVISOR NNA:** `advisors/{a}/nna_clients.json` `.clients[*].pct_of_advisor_nna` (10).

⛔ **AND A COINCIDENCE THAT WILL STOP BEING ONE.** There is exactly **ONE** advisor dir and
`by_architect[0].aua_pct = 100.0`. **So advisor-grain and firm-grain denominators are the same number today** —
`advisors/{a}/summary.json .book.total_aua` **equals** the firm headline exactly. A second advisor makes these
diverge, and any rule written against today's equality would break silently at that moment. Flagged, not acted on.

---

## 4. CANR1DS-AC4 — THE EXCLUSION PREDICATE

**Mechanism (`COT-b-1`): EXISTS, LIVE, and is NOT to be rebuilt (Build Ladder rung 2).**
`data/cot/scripts/gold/D_05.supervised_split.py` (232 lines) → `s3://opal-data-cot/gold/artifacts/supervised_split.json`
(17,789 B, LastModified **2026-08-20T18:10:56Z**, `data_as_of` **2026-08-19**).

Reads (from its own docstring, source-confirmed):
`gold/timeseries/account_performance.parquet` (C_03) · `gold/dimensions/accounts_dimension_latest.parquet`
(A_00, `account_supervised`) · `silver/account_attributes/2026-08-19.parquet` (`flag_source`, stated in the artifact).

### 4a. ⛔ IT IS NOT AT THE SAME PLANE AS THE VIEW FIGURES — TWO INDEPENDENT REASONS

**(1) VINTAGE.** `firm_daily` = **98 rows, 2026-04-22 … 2026-08-19**. Probed explicitly:
`has 2026-08-19: True` · **`2026-08-20: False` · `2026-08-21: False` · `2026-08-22: False` · `2026-08-24: False`**.
**Every served leaf is `data_as_of` 2026-08-21. There is no 08-21 row to apply.**

**(2) PLANE.** The artifact declares its own gap in `meta.plane_gap_declaration`:
`gap_usd: -8,697,205.48` — *"DataMining plane … 480,056,488.78 to the penny; Dashboard reads 488,753,694.26."*
`D_05.aum_all` @08-19 = **480,056,488.78** (DataMining). The served headline is **488,460,108.95**.

**Consequence, measured not inferred:** `aum_supervised` on the latest row = **`449,733,561.36`** — **the 449.7M**.
Delta to canonical = **−8,320,180.83**.

### 4b. `COT-b-2` — RETROACTIVITY, STATED PLAINLY

**Confirmed in BOTH the source and the artifact, and it is a property to be told, not resolved.**

Source `D_05.supervised_split.py:126-128`:
```python
flags = dim[['account_id', 'account_supervised']].copy()
j = perf.merge(flags, on='account_id', how='left')
```
— the **latest** dimension snapshot joined onto **all** history by `account_id`.

Artifact `meta.notes[0]`, verbatim:
> *"TODAY'S-FLAGS CAVEAT: the supervised/unsupervised split applies the CURRENT account-attributes snapshot to
> all historical dates — an account that changed supervision status in the past misclassifies before its flip.
> Correct for dashboard AUM by design decision (CTO 63310); never point-in-time supervision truth."*

**Reading:** fine for a CURRENT-total exclusion. **Any timeseries leaf that applies this historically is serving
a non-point-in-time series** — and there are **6** total-bearing timeseries leaves (`timeseries_chart`,
`timeseries_overview`, `cumulative_chart`, `advisors/{a}/timeseries`, `partner_analytics_{a,m,q}` period views).
Stated; not resolved here.

### 4c. `COT-b-3` — `aum_unflagged` RE-MEASURED, AND THE ZERO IS NOT THE ZERO IT LOOKS LIKE

**Re-measured across the whole series: `aum_unflagged` = `0.00` on `0 of 98` rows nonzero.
Latest row (2026-08-19) = `0.00`. Denominator: 98 daily rows.** The inherited zero is **confirmed by
observation**, not carried.

⛔ **BUT THE VALUE-ZERO IS NOT A POPULATION-ZERO, AND THAT IS THE WHOLE REASON THE BUCKET STAYS.**
`meta.unflagged_account_ids` = `['z0927448761']` — **the bucket has exactly ONE member and it holds $0.**
Anyone reading `aum_unflagged: 0.00` and concluding "no unflagged accounts — drop the bucket" would be wrong on
a live population. **If that account ever funds, the bucket silently starts carrying value.** No label invented.

**The assert survives — and it is IN THE CODE, not only the docstring** (`:146-151`), fail-closed:
```python
control = j.groupby('date')['total_aua'].sum()
bad = (per_date['all'] - control).abs() > 0.01
if bad.any():
    raise SystemExit(f'PARTITION ASSERT: buckets do not sum to total on {int(bad.sum())} date(s) -- refusing.')
```
⚠ **HONEST LIMIT OF THAT ASSERT, since it is the one guard here: both sides derive from the same dataframe `j`.
It is a SELF-COMPARISON — it catches a bucketing/pivot error and is structurally unable to catch a wrong
`total_aua` arriving from upstream.** Real, worth keeping, and not a value control.

---

## 5. CANR1DS-AC5 — INVARIANTS

| cell | verdict |
|---|---|
| **`COT-inv-3`** | ⛔ **NOTHING BUILT.** No schedule, trigger, alarm, SNS, monitor, freshness-checker, shadow prefix or comparator was created, proposed, or implied. This TO produced **two files** (this report + the proof-of-spec instance) and **zero** infrastructure. Standing moratorium + complete veto both honoured. |
| **`COT-inv-4`** | **Every measurement above names its full path.** `s3://opal-data-cot/platinum/` (census) · `s3://opal-data-cot/gold/artifacts/supervised_split.json` (predicate) · `silver/account_attributes/2026-08-19.parquet` (flag source, as the artifact declares) · every producer cited as `file:line`. |
| **`COT-inv-5`** | **Claims held at their measured grain, and I refused two widenings.** (a) `D_05`'s series ending 08-19 is a statement about **`gold/artifacts/supervised_split.json`** — NOT about the cot tree, NOT about the firm; the served platinum objects were **written 2026-08-24T11:35Z** and are not stale by any reading here. (b) `data_as_of: 2026-08-21` on the served leaves is **reported as the vintage stamp those artifacts carry**, and I have deliberately **NOT** rendered a staleness verdict — the currency condition is surface (c), `ADVI_COTETL`'s, and no cell in this TO reaches it. |

**⛔ NEVER#1 CHECK, STATED EXPLICITLY BECAUSE THE SHAPE INVITES THE ERROR.** Nothing in this deliverable calls
any pipeline stale, broken, frozen, or dark. The one age-shaped observation — `D_05` @08-19 vs served @08-21 —
is reported as a **plane/vintage MISMATCH BETWEEN TWO ARTIFACTS I READ**, which is a joinability fact, not a
producer verdict, and it required no trading-calendar resolution to state.

---

## 6. CONTROLS RUN

| control | result |
|---|---|
| **Positive (census)** | `aws s3 ls --recursive --summarize` → `Total Objects: 1125` — second instrument agrees |
| **Negative (census)** | `platinum_zzz_no_such_prefix_9999/` → `None` — discriminates |
| **Positive (absence probe)** | `platinum/firm/header_metrics.json` → 1 census hit — the probe shape can find a key that exists |
| **Live re-check** | 3 absent keys → **404** on `head-object`, not merely absent from a snapshot |
| **MUTANT** | The assertion "`458,053,742.19` appears 0×" re-run with target mutated to the known-present `488,460,108.95` → **73 hits. FIRED-AS-EXPECTED.** The matcher is not undiscriminating. |
| **DETERMINISM** | Census re-run 10:52:27Z: **1,125 keys, 0 diff lines, md5 identical (`b4c6fd9a…`) — STABLE** |
| **Download integrity** | 21/21 samples; byte sizes match the listing exactly (e.g. `header_metrics` 734 B, `ownership_map` 107 B) |

⛔ **THE DETERMINISM CONTROL FAILED ON FIRST READING AND THE FAILURE WAS THE INSTRUMENT.** Run 2 reported
**2,252 diff lines and a different md5 on an identical 1,125-key set.** Cause: run 2 carried `\r\n`
(native `aws.exe` via `--output text`), run 1 `\n` (through `awk`). After `tr -d '\r'`: **0 diff, identical md5.**
**A uniform difference across an entire set is an instrument signature, not a data signature** — and had I
recorded the first reading, this deliverable would carry a fabricated instability on the estate's served census.

---

## 7. WHAT I DID NOT DO

| not done | why |
|---|---|
| Emit, publish, or move any served byte | The emit is STOPPED and stays stopped. Nothing here writes. |
| Apply the exclusion | Not in this TO; and §4a measures why it cannot be applied at the served plane today anyway. |
| Assign `mix_summary`'s basis | AC2 forbids assigning by likelihood. **UNDETERMINED.** |
| Diagnose why 5 declared write targets produce nothing | Measured and reported; diagnosis is not in these 10 cells. |
| Touch surfaces (c), (d), (e), (f) or `COT-inv-1/2` | 13 of 23 cells excluded by the TO for three declared reasons. |
| Render a staleness verdict on any producer | `COT-inv-5` + NEVER#1. The currency condition is `ADVI_COTETL`'s. |

---

## 8. SURPRISE-CHANNEL ITEMS (one line each to `3.0.0_SA_CVO`, cc `2.0.0_SA_COO`)

| # | class | standing | item |
|---|---|---|---|
| S-1 | **OBSERVATION** | INERT | `D_01.partner_analytics.py:2643` and `D_04` both `put_object` the same 3 `partner_analytics_*` keys with **different `CacheControl`**; D_01's own comment calls it a "TEMPORARY direct-write" whose fast-follow never landed. One served key, two writers, resolved by ordering. |
| S-2 | **OBSERVATION** | INERT | 5 declared write targets in `D_04` produce nothing served (3 confirmed 404 live). Gated-off vs dead code undetermined. |
| S-3 | **OBSERVATION** | INERT | `runners_cot/d01`+`d02` both declare `SERVED_KEY = platinum/firm/header_metrics.json` and **neither writes S3**. A constant that reads like provenance and is not. |
| S-4 | **OBSERVATION** | INERT | `clients/{id}/views.json` sampled carries `generated_at: 2026-08-22T11:33:55Z` while its object was written 2026-08-24T11:35:28Z — content stamp ~2 days behind the write. Sampled on ONE client; **not generalised to the other 221.** |
| S-5 | **OBSERVATION** | INERT | One client dir (`z09305728`) carries 4 leaves where all 221 others carry 5 (`composition.json` absent). |

**No BLOCKING item. No ARMED item.** Nothing in this TO required a disarm owner.

---

## 9. DENOMINATORS, ALL OF THEM

- **Served set:** 1,125 objects · 20 leaf names · **21 served-leaf types** · `s3://opal-data-cot/platinum/` @2026-08-25T10:06:31Z
- **Classified:** 21 of 21. Carries-a-total **14** · carries-none **7** · unclassified **0**
- **Basis:** ALL-ASSETS **13** · UNDETERMINED **1** · COTTONWOOD-SUPERVISED **0** · OPAL-SUPERVISED **0**
- **Canonical `458,053,742.19` in the served set:** **0 occurrences / 21 types** (positive control 73 / 12)
- **`D_05.firm_daily`:** 98 rows · 2026-04-22…2026-08-19 · `aum_unflagged` nonzero on **0 of 98** · unflagged **population 1**
- **`SERVED_KEY` declarations:** 7 across 6 distinct keys; **producers among them: 0**
- **Cells:** 10 of 23 (13 excluded, three reasons, all named in the TO's `decomp_context`)
- **Samples downloaded:** 21 of 21, byte-size-verified
- **Files this TO created:** 2 (this report + the proof-of-spec instance). **Infrastructure created: 0.**

---

*`0.4.0_DS_ClientPlatform~I` · measurement-only · nothing published, emitted, or moved.*
