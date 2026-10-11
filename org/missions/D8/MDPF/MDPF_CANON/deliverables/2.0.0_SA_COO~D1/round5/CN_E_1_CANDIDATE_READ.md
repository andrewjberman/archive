# MDPF_CANON round 5, CN-e-1 -- the next M4 reader: candidate read (fork of 2.0.0_SA_COO~D1, 2026-10-11 ~07:4xZ)

Input: `ledger/ROUND_ANALYSIS.round4.md` section 3 item 5 ("the next reader from `READER_CENSUS.md` in dependency order, on `/seams`").
Everything below was measured read-only on the real partitions at the builder's address, latest date 2026-10-08. Nothing was written.

## Outcome: B for `verify_mdpf_revamp_conditions.py`; a feasible alternative exists and is measured (section 3)

## 1. Why `verify_mdpf_revamp_conditions.py` cannot be repointed without a logic change

The verifier reads four staged JSON keys (`:33-38`) and its conditions consume nested shapes. The builder's address holds all four
artifacts for the three scopes it needs (`global`, `49financial`, `inflection`: `aggregate_aua_timeseries` 42/51/50 partitions and
`aum_metrics` 33/42/41, latest 2026-10-08), but the aggregate artifact's parquet is WIDE and carries only per-date series
(`mdpf_gold_parquet.py:26-29`: "Lists of objects, and scalar metadata, are not series and are not carried here"). Cell by cell:

| condition | cell it reads (verifier line) | in the parquet? |
|---|---|---|
| (i) fee-basis | `radial.meta.fee_basis_components.*.{value,fee_scope,basis}`, `radial.total.aum` (:64-67) | YES: global `aum_metrics` is LONG leaves; 23 `meta.fee_basis_components.*` leaves, `total.aum` 2147378054.74 |
| (ii) count composition | `radial.total.account_count`, "distinct" in `radial.meta` (:77-82) | YES: `total.account_count` 8264.0; `meta` text carries "distinct" |
| (iii)-pre | `g.opal_aggregate_aua`, `a49.partner_custody_total`, `inf.model_aua` series (:88-96) | YES (series columns) |
| (iii)-taint | `g.cohort_provenance` (a list of OBJECTS) and `g.point_class` (:89-110) | `point_class` YES; **`cohort_provenance` ABSENT** (no column) |
| (iv) radial sourcing | `a49.meta.latest_cross_section.partner_custody_total` (:114-115) | **ABSENT** (scalar metadata) |
| (v)-sma | `g.by_model.<sma>.count_as_of` (a scalar under the entry) (:123-127) | **ABSENT** (the only `count_as_of` column is a different, top-level series) |
| (v)-interval | `a49.meta.count_coverage_end`, `g.meta.count_coverage_end` (:128-132) | **ABSENT** (scalar metadata) |
| (vi) no-partial-total | `g.account_count_total`, `g.count_provenance`, `g.by_model.*.account_count` (:140-165) | YES (series columns) |

Four of the eight cells the five (six, with W-7) conditions read are not in the artifact at the builder's address: (iii)-taint, (iv),
(v)-sma and (v)-interval. A loader cannot rebuild them, so a repoint must either drop those conditions (a logic change, and the verifier's
whole value is those pre-sign conditions) or add the objects and scalars to the parquet. The second is a change to the ONE gold writer
`mdpf_gold_parquet.py` (a PRD contract: "the gold artifact"), and its `write_partition` returns "conflict" on an existing date whose bytes
differ, so the new columns would appear only on new dates and the verifier would read a mixed history. That is a CTO ruling on the artifact's
shape, not a cell. Not feasible as a cell.

## 2. The next census rows, in dependency order

The census's note 1 holds: the writers are still live and every row that feeds a served key takes a never-widen pair with a before and
after of each leaf. Reader rows, assessed:

| row (census) | feeds a served key? | pair needed | note |
|---|---|---|---|
| `dim_mdpf_aum_timeseries.py` (:53, :54, :291) | NO: its staging write is RETIRED (:284-297, "read-only identity instrument only") | no | **candidate**, section 3 |
| `dim_mdpf_aum_metrics.py` (:55, :74, :176) | yes: stages `aum_metrics`, which the publisher serves | yes | writer coupling |
| `dim_mdpf_non_model_assets.py` (:86, :95, :102) | yes: stages `non_model_assets` | yes | writer coupling |
| `build_portal_gold_accrual.py` (:88 SOURCE_PREFIX) | yes: builds the served accrual bundle | yes | |
| `build_mdpf_spine.py` (:114) | yes: Stage 6 entry, feeds the revamp producers | yes | |
| `opal-assets-daily-emitter/channel_sources.py` (:69) | channel emitter (outside the MDPF chain) | CTO call | not examined |
| config readers (`route_bindings.yaml`, `served_freshness_config.yaml`, ...) | gates, not output | no pair, but the freshness config sits under the alert/monitor moratorium | not examined |

## 3. Recommendation: `data/mdpf/scripts/gold/dim_mdpf_aum_timeseries.py` is the cheapest honest candidate

Measured, not inferred:
- It is a read-only identity instrument: `main` builds a document, validates its internal identity and prints; `--upload` is a logged SKIP
  (retired 2026-07-29). No caller in the dispatch chain or the Lambda package (grep of `infra/aws/ec2/mdpf-daily-runner` and `data/mdpf`).
- It reads ONE staged key, `gold/mdpf_revamp/global/aggregate_aua_timeseries.json` (`AGG_GLOBAL_KEY` :53), and consumes only:
  `agg["dates"]` and, for the five core keys, `by_model[k]["model_value"]`, `["account_count"]` (series) and `["cohort_class"]` (a scalar, :121).
- Parquet at `global/aggregate_aua_timeseries/date=2026-10-08`: 493 rows, columns `date`, `by_model.<k>.model_value`,
  `by_model.<k>.account_count` for every core key. `cohort_class` has NO column.
- **DELTA=0:** the script's own `build_aum_timeseries` run on a dict rebuilt from that partition equals the same function run on the staging
  JSON read the same minute (staging LastModified 2026-10-09T13:31Z, 493 dates 2024-11-01..2026-10-08): the document is equal, 2958 of 2958
  cells (493 aggregate rows plus five core keys x 493), 0 differ.
- **The one named substitution:** the FATAL guard `node.get("cohort_class") != "model"` reads an artifact scalar the parquet does not carry.
  The loader supplies `cohort_class` from the producer's own model registry (`mdpf_category_registry.entry_for_key(key).cohort_class`, the
  source the aggregate writer uses), so the guard keeps its meaning and its raise. The cell must say this in its face and a judgment
  criterion must grade it; it is not a silent default.
- Loader contract, as in CN-d-4: list the global scope's `date=` partitions with `Delimiter="/"`, take the greatest date starting `20`, RAISE
  naming the scope if none, read `partition_uri("global", "aggregate_aua_timeseries", <D>)`, rebuild `{"dates", "by_model": {k:
  {"cohort_class", "model_value", "account_count"}}}` (NaN to None, counts int); all S3 through the file's `_s3()`; replace `AGG_GLOBAL_KEY`
  and every `gold/mdpf_revamp` string; leave `STAGING_KEY`'s retired-write text as history only if the census row keeps naming it (decide in the
  face: simplest is to delete the constant and reword the retirement note to "the gold tier").
- Suggested arms (at most three mechanical): AC1 reader (no old-tree text; the adapter returns the dict above on a fake `_s3`; absence raises
  with no fallback), AC2 seam (real partition: built document equals the staging-built document, cells compared and printed), AC3 judgment
  (`/seams`, including the registry-sourced `cohort_class`). Grant in `<paths>`: the script, the order file, `READER_CENSUS.md` (with an
  explicit step splitting its row 15 and updating the line cites, so the declarative arm cannot fail as CN-d-4's did), the worker's
  deliverables directory, the investigation file.

Hazards: the cross-firm fence reads literals, and `partition_uri` types none (CN-d-4 passed it with two NAMING-GATE WARNs on `"inflection"` and
`"49financial"` literals; this candidate reads `global` only and needs none). Fork for the issuer: whether a retired never-canonical
instrument is worth a census-row move at all; it moves a reader row off the staging tree at near-zero risk and no served output, which is
the whole of M4's current honest supply. Anything beyond it needs a pair.
