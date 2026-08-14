# MDPF_TRGALN.TO-5 — Inflection atom_decomp truth table (served empty/hollow dates)

**Executed by:** 4.0.0_SA_CRO (atom_decomp method home) · **GO:** 2.0.0_SA_COO 20260814T053939Z
**PRD:** docs/architecture/MDPF_TRGALN_PRD.md v1.2 @cebdae6cd8 (§8.2 scope, §7 proof schema)
**All reads 2026-08-14 05:21–05:45Z.** Served baseline is PRE-tonight-refresh (AE refresh started ~05:39Z);
every historical-gap census below is refresh-invariant (the refresh cannot write historical vendor
run-dates — grounding in §4). Machine-readable proof: `proof_TO-5.json` beside this file.

## §0 Baseline document (vintage-pinned)

`s3://opal-data-portal-v2/platinum/mdpf/inflection/aggregate-aua-timeseries.json`
- LastModified `2026-08-13T14:20:51Z` · ETag `7d1807ec4903ca927620b8ac079d0335` · 72,459 B
- Read `2026-08-14T05:21:40Z` (PRE-refresh); local copy md5 == ETag (byte-verified)
- `_provenance.source_keys` = gold `portal/gold/mdpf/inflection/aggregate-aua-timeseries/2026-08-11.json` (pure projection)
- 443 dates 2024-11-01→2026-08-11. Measured: **7 fully-empty** (model AND non_model null),
  **383 model==0**, **53 model nonzero** (first nonzero 2026-05-15). 383+53+7 = 443.
  (PRD §8.2's "390 zero" = 383 true-zeros + 7 nulls; the truth pass separates them — absent is not zero.)

## §1 THE MECHANISM (one mechanism, seven dates; source-confirmed)

**Layer 1 — vendor data gaps.** Eclipse `fact_portfolios_full` silver partitions are ABSENT at
run-dates `{2026-05-21, 06-01, 07-01, 07-13, 07-14, 07-15, 08-06}` (full census: 76 partitions
2026-05-15..2026-08-13 diffed against `lib/trading_calendar`, read 05:33Z). Bronze↔silver parity is
exact (0 diffs both directions), and the same 7 day-folders are absent in BOTH bronze homes —
monolith `opal-data-assets/eclipse/inflection/bronze/` AND vendor-side `opal-data-inf/bronze/eclipse/`
(78 folders, read 05:39Z). Orion `fact_assets` is absent at run-date `{2026-08-06}` only
(2,298 partitions 2020-04-28..2026-08-13, read 05:33Z).

**Layer 2 — the label mapping.** The RP-W1 vendor label offset (@bf74d031c1, 0.4.0_DS, committed
2026-08-11T00:32Z) makes axis label D read the partition whose run-date normalizes to D
(`_partitions_by_label` / `prev_trading_day`; orion+eclipse partitions are run-date-keyed carrying the
prior NYSE trading day's close — sealed semantics, `data/inf/scripts/silver/_orion_vendor_asof.py:20-31`,
re-exercised 2026-08-03 @15d0326c80). **Therefore each missing run-date P nulls exactly one label:
prev_trading_day(P).** The 7 missing eclipse run-dates map to labels
`{05-20, 05-29, 06-30, 07-10, 07-13, 07-14, 08-05}` — **exactly the 7 served empty dates, no more, no
fewer** (my census 05:33Z; independently, the gold artifact's own `meta.honest_none.model_absent_dates`
lists the same 7 and `custody_absent_dates=[2026-08-05]` — two independent derivations agree).

**Layer 3 — null propagation.** `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py:1050`
(HEAD @bf74d031c1): `non_model = custody − model` under a both-operand honest-None ternary — a
model-leg null propagates into non_model. That is why 6 dates with custody data PRESENT still serve
fully-empty. 08-05 is additionally custody-null (orion run-date 08-06 absent at the monolith).

**Deployed-code grounding (Rule 22a):** deployed builder `s3://opal-data-mdpf/code/scripts/gold/
dim_mdpf_aggregate_aua_timeseries.py` LastModified `2026-08-11T08:41:47Z`, `comp-pipescript deployed
--pipeline mdpf` = MATCH vs repo HEAD (read 05:30Z). First null-bearing gold build: as-of-08-07
snapshot, `generated_at 2026-08-11T08:41:30Z`, S3 write 08:41:35Z — the same atomic deploy window
(12–17s ordering skew between artifact write and code PUT is recorded honestly; the artifact's content
carries the offset signature either way: nulls at exactly the offset-predicted labels).

## §2 WHEN each hole appeared (document-grain bisect over all 9 surviving gold snapshots)

| gold snapshot (as-of) | built (generated_at) | 05-20 | 05-29 | 06-30 | 07-10 | 07-13 | 07-14 | 08-05 |
|---|---|---|---|---|---|---|---|---|
| 2026-07-27 | 07-29T00:33Z | FULL | FULL | FULL | FULL | NULL | NULL | absent |
| 2026-07-28 | 07-29T21:09Z | FULL | FULL | FULL | FULL | NULL | NULL | absent |
| 2026-07-29 | 07-30T15:05Z | FULL | FULL | FULL | FULL | NULL | NULL | absent |
| 2026-07-30 | 07-31T15:00Z | FULL | FULL | FULL | FULL | NULL | NULL | absent |
| 2026-08-03 | 08-04T16:00Z | FULL | FULL | FULL | FULL | NULL | NULL | absent |
| 2026-08-05 | 08-07T03:52Z | FULL | FULL | FULL | FULL | NULL | NULL | FULL |
| **2026-08-07** | **08-11T08:41Z** | NULL | NULL | NULL | NULL | NULL | NULL | NULL |
| 2026-08-10 | 08-11T15:13Z | NULL | NULL | NULL | NULL | NULL | NULL | NULL |
| 2026-08-11 | 08-12T15:12Z | NULL | NULL | NULL | NULL | NULL | NULL | NULL |

- **Class A (05-20, 05-29, 06-30, 07-10, 08-05):** flipped FULL→NULL at the 08-11T08:41Z build — the
  RP-W1 offset deploy. **The pre-flip "values" at these labels were the PRIOR trading day's close
  mislabeled** (RP-W1's own source-confirmed finding: pre-fix, label D read partition D, which carries
  D-1's close). The flip made pre-existing data gaps VISIBLE as honest-Nones; it did not destroy
  correct data. "Did not used to be here" is TRUE at display grain and the display was wrong-dated.
- **Class B (07-13, 07-14):** NULL in every surviving snapshot (earliest build 07-29T00:33Z) — under
  pre-offset semantics their OWN run-date partitions (07-13/14) were the absent ones. Same underlying
  eclipse gap family, visible earlier because the gap run 07-11→07-15 covers both keying schemes.

## §3 PER-DATE TRUTH VERDICTS

Verdict grammar per TO: `TRUE-ZERO | MISSING-AT-SURFACE-X | REGRESSION-INTRODUCED-AT-COMMIT/CUTOVER-Y`.

### The 7 fully-empty dates — ALL are MISSING-AT-VENDOR-PULL (model leg); NONE is TRUE-ZERO
(model program live with nonzero values on adjacent trading days for all 7; custody nonzero adjacent for all 7)

| served label | verdict | missing input (run-date grain) | custody leg | first-null | model-leg recoverable? |
|---|---|---|---|---|---|
| 2026-05-20 | MISSING-AT-VENDOR-PULL (eclipse) | eclipse run-date 05-21 | PRESENT | Class A (08-11 build) | NO — permanently unfillable |
| 2026-05-29 | MISSING-AT-VENDOR-PULL (eclipse) | eclipse run-date 06-01 | PRESENT | Class A | NO |
| 2026-06-30 | MISSING-AT-VENDOR-PULL (eclipse) | eclipse run-date 07-01 | PRESENT | Class A | NO |
| 2026-07-10 | MISSING-AT-VENDOR-PULL (eclipse) | eclipse run-dates 07-11/12/13 | PRESENT | Class A | NO |
| 2026-07-13 | MISSING-AT-VENDOR-PULL (eclipse) | eclipse run-date 07-14 | PRESENT | Class B (≤07-29 build) | NO |
| 2026-07-14 | MISSING-AT-VENDOR-PULL (eclipse) | eclipse run-date 07-15 | PRESENT | Class B | NO |
| 2026-08-05 | MISSING-AT-VENDOR-PULL (eclipse) **+ MISSING-AT-INGEST-MIRROR (orion)** | eclipse run-date 08-06 (absent everywhere) · orion run-date 08-06 (absent at monolith ONLY) | ABSENT at monolith; **data EXISTS in-estate**: `opal-data-inf/bronze/positions/2026-08-06.parquet` (1,231,196 B, LastModified 2026-08-06T13:40:38Z, read 05:44Z) | Class A | model NO · **custody YES (surgical, zero-egress: convert/mirror the existing parquet)** |

**Display-regression attribution (Class A):** REGRESSION-INTRODUCED-AT-COMMIT `bf74d031c1`
(RP-W1 vendor label offset), deployed 2026-08-11T08:41:47Z — with the explicit qualifier that RP-W1
is a CORRECTNESS fix (labels now true); the regression is in VISIBILITY, not in data. Reverting it
would re-serve wrong-dated values and is not a remedy.

### The 383 model==0 dates — ALL TRUE-ZERO (program ramp), by exact partition

- Axis 2024-11-01..2026-08-11 = 443 trading days; model era (≥ `INFLECTION_MODEL_LAUNCH` 2026-05-15)
  = 60 trading days. 53 nonzero + 7 null = 60, **therefore zero model==0 dates exist inside the model
  era** — every one of the 383 zeros is pre-launch. Grounding: first eclipse partition = 2026-05-15
  (census 05:33Z); builder's launch filter (`load_inflection_model_history`, post = dates ≥ launch);
  first served nonzero model date = 2026-05-15. TRUE history, not missing data.

## §4 CUTOVER CORRELATION (criterion 3 — tested, both directions)

**REFUTED as cause:** the platinum-cutover carry-forward union logic is NOT the mechanism of the
08-05 hole. The gold artifact's own honest_none marker names SOURCE-PARTITION ABSENCE (deliberately
narrow: "a date whose partition is PRESENT but whose component is None is NOT covered"), my
independent partition census confirms both feeds absent at run-date 08-06, and the per-firm surface
carries nothing by design (meta.channel_participation: "NOTHING IS CARRIED on a per-firm surface").
**CONFIRMED as temporal correlate:** run-date 08-06 IS the cutover night. The ingest partially
failed exactly then: inf-tree orion positions has parquet-only for 08-06 (its `.jsonl.gz` sibling —
present every adjacent day — is absent for 08-06 alone; mirror-miss cause INFERRED from that
observable), and eclipse's otherwise-continuous daily pull has 08-06 as its only post-07-15 gap.
So: cutover → one-night ingest disruption → missing run-date 08-06 → (via the offset) empty label
08-05. Cutover CARRY LOGIC → hole is REFUTED; cutover NIGHT OUTAGE → hole is CONFIRMED.

## §5 UNFILLABILITY OF THE ECLIPSE MODEL LEG (the decision-carrying claim, three independent groundings)

1. **API capability, source-confirmed 3-party:** `data/inf/scripts/bronze/pull_eclipse_portfolios.py`
   docstring (0.6.2 found, COO confirmed @b0cad1965 2026-07-22, DS re-confirmed independently): all 4
   consumed endpoints are CURRENT-STATE; `eclipse_get()` has NO date parameter; `--date` is an output
   LABEL that fabricates if used for backfill; across the vendor's 493-path surface, date params exist
   only on `/auditlog/*`. Docstring's own verdict: gaps "RECORDABLE AND PERMANENTLY UNFILLABLE."
2. **Auditlog reconstruction attempted and empty:** `eclipse/inflection/bronze/_history/auditlog_model/
   2026-07-13_2026-07-15/model_*.json` (18 files, written 2026-07-17T03:30Z) are ALL 2 bytes — empty.
   The portfolio auditlog (376–796 B files, sampled 05:43Z) carries status-change events only, no
   valuations. The one date-parameterized endpoint family cannot reconstruct AUM.
3. **No rawer in-estate copy exists:** the 7 run-date folders are absent in the vendor-side bronze
   (`opal-data-inf/bronze/eclipse/`, 78 folders) and the monolith bronze alike (censuses 05:37–05:39Z).

Consequence for TO-6: **surgical backfill is IMPOSSIBLE for the model leg on all 7 dates.** Per PRD
§8 verbatim, roll-forward is the fallback and **requires Andrew's explicit word**. The custody leg of
08-05 alone is surgically fillable in-estate (zero egress). Note: even after filling orion 08-06, label
08-05 remains fully-empty at serve until the model leg is resolved (the :1050 ternary propagates) —
the custody fill is real but not display-visible by itself.

## §5a ADDENDUM 2026-08-14 ~15:15Z (Andrew-prompted at the CRO terminal) — a RATIFIED THIRD PATH exists between surgical-measured and roll-forward

§5's "surgical backfill IMPOSSIBLE" holds for MEASURED values and is unchanged. But the fork is not
binary: **the ECLIPSE VINTAGE RECONSTRUCTION emitter** (0.2.0_DS_PortfolioAnalytics, 2026-08-10 —
`ECLIPSE_VINTAGE_RECONSTRUCTION_T0_D1_D2_20260810.md` + `_D3_SPEC_20260810.md`, CTO brief
@7b76f32562) is a specced, CTO-prefix-ratified DERIVED path: eclipse portfolio values rolled from a
flanking measured partition via orion per-client `fact_performance` factors (a TRUE full-history
table), flow-adjusted from orion `fact_transactions` (Step 3, the one unbuilt piece). Measured
accuracy flow-unadjusted: +15.78bp aggregate / 19.30bp value-weighted / worst cell +136bp
(gate-FAIL-not-relax, ratified). Properties: `point_class: "reconstructed"` never `measured`,
distinct opt-in prefix `eclipse/inflection/reconstructed/vintage=…`, **Andrew-ruled INTERNAL-ONLY
until he says otherwise** (~2334Z 08-10). Execution vehicle: TO `MDPF_REMED.RP-W7` @09b57a6278,
**staged, no GO**, sequenced behind pipeline-functional (12/12 A4 unattended cycle, COO adjudicates).
Spec scope was ONE vintage (08-05); the six historic holes are out of scope **absent an Andrew/CTO
word** (D3 §1) — extending is a sovereign call, not an engineering gap.
**New measurement (this addendum, 15:10Z):** orion `fact_performance` @ partition date=2026-08-14
(full-history redelivery, 464,104 rows, 2,272 data-dates) carries vendor-computed factors at ALL
SEVEN hole dates — 05-20: 309 · 05-29: 309 · 06-30: 310 · 07-10: 311 · 07-13: 311 · 07-14: 311 ·
08-05: 313 clients (of 314 total) — and every hole is bracketed by measured eclipse partitions. The
emitter's inputs exist for every hole on data already in S3 (zero new vendor calls).

## §6 Residuals surfaced, not chased (one line each)

- Gold as-of-08-11 snapshot: S3 LastModified 2026-08-13T14:10:48Z but `meta.generated_at`
  2026-08-12T15:12:09Z — an 08-13 re-put carrying an 08-12 generation stamp; not adjudicated here.
- The `.tools/aws` shim passed a `/cygdrive/c/...` destination through as a literal relative path
  (`C:\cygdrive\...` tree created; file recovered, md5-verified); empty stray tree left at
  `C:\cygdrive\` for cleanup.
- `pull_eclipse_portfolios.py` "--date must REFUSE past dates" class fix: routed to CTO 07-22, still
  prose-only (the docstring says so itself); TO-6's executor should not touch `--date` regardless.

## Compiler Tools

comp-pipescript deployed --pipeline mdpf (MATCH verdict, §1) · comp-find ×4 (builder/producer
localization, denominators quoted) · comp-to (TO context) · lib/trading_calendar (all trading-day
math, NEVER wall-clock) · comp-which routing honored via HUD. Raw aws reads were operational
data-plane (s3 ls/cp/head-object on owned buckets) per the rail's carve-out.
