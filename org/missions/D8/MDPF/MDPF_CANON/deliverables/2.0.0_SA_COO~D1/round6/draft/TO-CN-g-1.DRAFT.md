# DRAFT -- NOT ISSUED, AND BLOCKED AT DRAFT BY A MEASURED FINDING (read the record face, "BLOCKER", before any cut).
# Target path if it is ever cut: org/missions/D8/MDPF/MDPF_CANON/task-orders/MDPF_CANON.TO-CN-g-1.non-model-assets-reads-the-gold-tier.md
# The checks below move from round6/draft/checks/ to round6/checks/ (same file names) at issuance.

# MDPF_CANON task order -- `CN-g-1` -- THE NON-MODEL-ASSETS BUILDER READS THE GOLD-TIER AGGREGATES (M4, fourth slice, FWD-5)

<!-- ===================== WORKER FACE -- this is the WHOLE of the worker's context ===================== -->

<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_CANON/decompositions/MDPF_CANON_DECOMP.md</decomp_doc>
<owned_cells>CN-g-1</owned_cells>
</decomp_ref>
<issued_to>0.9.0_WK_MDPF_CANON~17</issued_to>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<placeholders>NONE</placeholders>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- no cron, alarm, monitor or cadence is added or changed; the script is edited, not scheduled.
comp-iam: DECLARED-NOT-APPLICABLE -- reads only, two scopes' partitions at the builder's address; no grant is added.
comp-adversary: RUN by the issuer (2.0.0_SA_COO~D1) on DELL1 at box/dell1 -- r6_cn_g_1.py reader 1 of 5 (arm DERIVE-UNCHANGED is a control), seam 2 of 3 (the other two arms are controls) and r6_cn_g_1_census.py 1 of 4 (arm C4 is a control) at base; a reference copy reads 5 of 5, 3 of 3 (497 rows DELTA=0 on the real vintage) and 4 of 4; a planted wrong column turns reader and seam red (25 unequal rows).
EGRESS CLASS, declared: NONE (the worker writes no AWS).
</preflight>

## 1. THE CELL -- `CN-g-1` (round 6, decomposition v6)

`data/mdpf/scripts/gold/dim_mdpf_non_model_assets.py` builds the non-model-assets series: `build(global_uri, inflection_uri, precutover_uri,
cutover)` takes `dates`, the enterprise total and `model_aua` from the GLOBAL aggregate, and the inflection `non_model_aua` from the INFLECTION
aggregate. It reads both from the OLD staging tree through two default constants (`DEFAULT_GLOBAL_URI`, `DEFAULT_INFLECTION_URI`, about lines
101-104; loaders `load_global_aggregate` about line 240 and `load_inflection_nm` about line 263). The same arrays are written, one partition per
day, at the builder's address. Repoint the two reads to that, and change nothing else about what the script computes.

The builder's address for a scope and a day is wrapped by a sibling module, `mdpf_gold_parquet.py` (`partition_uri(scope, artifact, date)`;
read it, do NOT edit it):

```
partition_uri("global", "aggregate_aua_timeseries", "2026-10-09")
  -> s3://opal-data-mdpf/mdpf/global/gold/aggregate_aua_timeseries/date=2026-10-09/data.parquet      (type no bucket or key)
```

The parquet is WIDE: one row per axis date (494 rows for global, 485 for inflection at 2026-10-09; the newest partition carries the whole axis).
A null is NaN. The columns you need, measured on the real partitions:

| scope | column | dtype | becomes |
|---|---|---|---|
| global | `date` | string `YYYY-MM-DD` | `dates` (as `str(x)[:10]`, row order) |
| global | `base_excluding_tax_aua` | float64, NaN on 9 dates | `enterprise` (NaN -> `None`) |
| global | `model_aua` | float64 | `model` (NaN -> `None`) |
| inflection | `date`, `non_model_aua` | string, float64 | `{date: value}`, NaN dropped |

**THE ONE TRAP, MEASURED:** the enterprise array is `base_excluding_tax_aua`, NOT `opal_aggregate_aua`. The staged `opal_aggregate_aua` the script
reads today equals the gold tier's `base_excluding_tax_aua` on 494 of 494 dates (the 9 None dates included). The gold tier's own
`opal_aggregate_aua` is the SERVED total, which adds `tax_additive_aua` and `sma_additive_aua`: it differs on 25 dates (2026-08-26 .. 2026-10-09;
at 2026-10-09 by 29,345,854.15 = 28,934,133.62 + 411,720.53). Reading it would put those additive terms into the non-model series. The
`etf_public_residual_total` field is absent from both the staged and the gold artifact (absent -> 0.0 on both), so no column is needed for it.

Steps (the file keeps its line endings; read it first, and the sibling `dim_mdpf_aum_timeseries.py` whose `latest_gold_aggregate` is the pattern
this cell follows):

1. Imports. Add `import io` and `from urllib.parse import urlsplit`, and, in the style of the existing sibling import of
   `mdpf_calendar_binding`, `from mdpf_gold_parquet import partition_uri  # noqa: E402`. Import `pandas` inside the new function (the file
   does not import it at module level today).
2. Constants. DELETE `DEFAULT_GLOBAL_URI` and `DEFAULT_INFLECTION_URI` and the comment above them. Add `GOLD_ARTIFACT = "aggregate_aua_timeseries"`
   with a short comment naming the column map in the table above. Leave `STAGING_BUCKET`, `STAGING_KEY`, `FROZEN_PRECUTOVER_KEY` and
   `FROZEN_PRECUTOVER_URI` exactly as they are (the script still WRITES `STAGING_KEY`, which `build_portal_gold_accrual.py` reads, and still
   READS the frozen pre-cutover snapshot, which is a non-derivable one-off capture).
3. Add `_gold_partition(scope, columns) -> (DataFrame, latest_date)`:
   - take the bucket and the key prefix from `partition_uri(scope, GOLD_ARTIFACT, "2000-01-01")`, cut the key at `"/date="` and add a
     trailing `/`; list it with `Delimiter="/"` through `_s3().get_paginator("list_objects_v2")`; collect the `date=<D>` tokens that start
     with `20`;
   - if there is none, RAISE `SystemExit` naming the scope (`FATAL: no dated partition of scope 'global' ...`); no fallback to any other
     place, ever;
   - read the greatest date's `data.parquet` from `partition_uri(scope, GOLD_ARTIFACT, <D>)` with `pandas.read_parquet(io.BytesIO(...),
     columns=columns)`. ALL S3 access goes through the file's existing `_s3()` (the issuer's check replaces it with a fake).
4. `load_global_aggregate(global_uri=None)`: when `global_uri is None`, read `["date", "base_excluding_tax_aua", "model_aua"]` from the
   GLOBAL partition and return `{"dates": [...], "enterprise": [...], "model": [...], "etf": None}` (NaN -> `None`, else `float`), logging the
   partition date. When a URI IS passed, the body is today's JSON read, unchanged (an explicit caller override; it is not a fallback and
   nothing selects it by default).
5. `load_inflection_nm(inflection_uri=None)`: when `None`, read `["date", "non_model_aua"]` from the INFLECTION partition and return
   `{date: float}` for the non-NaN rows; a passed URI keeps today's JSON read. `build(...)` keeps its signature (its two URI arguments may be
   `None`). In `main`, the `--global-uri` and `--inflection-uri` arguments default to `None` (help text: "override; default reads the gold
   tier") and the `INFO` log line prints `gold tier` when the global URI is `None`.
6. Add the test file `data/mdpf/tests/canon/test_non_model_assets_gold_tier.py` (new): with a fake `_s3` serving two synthetic partitions per
   scope, assert the column map of step 4 and 5 (the newest partition is read; `base_excluding_tax_aua` and not `opal_aggregate_aua`; NaN ->
   `None`; the raise on no partition). Run `python <the file> --self-test` and your test yourself and report both (not criteria).
7. Do not change anything else: `derive_row`, `build`'s body, `validate`, `_self_test`, `write_out`, `STAGING_KEY` and the printed lines.
8. **The census.** `org/missions/D8/MDPF/MDPF_CANON/deliverables/0.9.0_WK_MDPF_CANON~4/READER_CENSUS.md` has one row whose first cell begins
   `gold/mdpf_revamp/ -- dim_mdpf_non_model_assets.py` (about line 16). Replace that ONE row with TWO rows, and edit nothing else:
   - `| gold tier at the builder address -- dim_mdpf_non_model_assets.py (repointed by CN-g-1; reads the newest global and inflection aggregate_aua_timeseries partitions through partition_uri) | reader | data/mdpf/scripts/gold/dim_mdpf_non_model_assets.py:<L1>; data/mdpf/scripts/gold/dim_mdpf_non_model_assets.py:<L2> | live |`
     where `<L1>` is the line of `def _gold_partition` and `<L2>` the line of its `partition_uri(scope, ...)` read, in the file AS YOU LEAVE IT;
     this row must not contain the text `gold/mdpf_revamp/`;
   - `| gold/mdpf_revamp/ -- dim_mdpf_non_model_assets.py (stages non_model_assets; reads the frozen pre-cutover snapshot) | both | data/mdpf/scripts/gold/dim_mdpf_non_model_assets.py:<L3>; data/mdpf/scripts/gold/dim_mdpf_non_model_assets.py:<L4> | live |`
     where `<L3>` is the line of `STAGING_KEY = ...` and `<L4>` the line of `FROZEN_PRECUTOVER_KEY = ...`.
   If the census's own header counts rows, add one.

## 2. BOUNDS

1. **No AWS write of any kind**: no put, no copy, no delete, no invoke, no apply. Read-only `get`/`head`/`list` is allowed (the seam arm of the
   issuer's check reads the two partitions, the two staged JSONs and the frozen snapshot). No install, no push. REFUSE, do not rescue.
2. Only the files in section 3 change (plus your deliverables and the surprise channel). Do NOT edit `mdpf_gold_parquet.py`, `lib/opal_naming.py`,
   the issuer's checks, `build_portal_gold_accrual.py`, `mdpf-daily-dispatch.sh`, or any of: the shared router, the guard, the CloudFront
   behaviours, `data/mdpf/config/bronze_homes.json`, `firm-config.mjs`, the portal-auth WAF rider (they belong to ADVI_FIRMBKTS until its flip
   receipt).
3. **Never** (PRD DEC-14) add a fallback to the old tree, a dual read as a default, a comparison against the old JSON, or a standing comparator:
   the default reads the gold tier only.
4. **Every address comes from the builder** through `partition_uri`. Type no bucket and no key. A refusal from a gate (the naming limb, or
   `ds-precommit`) is a BLOCKING row with the gate's text and a stop on that criterion: never a workaround.
5. The staging WRITE (`STAGING_KEY`) and the frozen pre-cutover READ stay. Retiring them is another cell.
6. **CLIENT DATA:** the script prints aggregates only; never print an account id.
7. No non-ASCII. Use the Edit tool. Keep each file's line endings as you find them (read them first).
8. If an item cannot be met within your paths, file a row and stop on that criterion.

## 3. SURFACES

<paths>
data/mdpf/scripts/gold/dim_mdpf_non_model_assets.py
data/mdpf/tests/canon/test_non_model_assets_gold_tier.py
org/missions/D8/MDPF/MDPF_CANON/deliverables/0.9.0_WK_MDPF_CANON~4/READER_CENSUS.md
org/missions/D8/MDPF/MDPF_CANON/task-orders/MDPF_CANON.TO-CN-g-1.non-model-assets-reads-the-gold-tier.md
org/missions/D8/MDPF/MDPF_CANON/deliverables/0.9.0_WK_MDPF_CANON~17/
org/missions/D8/MDPF/MDPF_CANON/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

Read-only: the whole repository, in particular `data/mdpf/scripts/gold/mdpf_gold_parquet.py` (`partition_uri`),
`data/mdpf/scripts/gold/dim_mdpf_aum_timeseries.py` (the pattern), and the issuer's checks
`org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round6/checks/r6_cn_g_1.py` and `r6_cn_g_1_census.py` (never edit them; read what
each arm asserts).

## 4. PROOF OF SPEC (literal; timeout 120 per invocation)

<proof_of_spec>
  <criterion id="AC1" cell_refs="CN-g-1"><invocation>cd "$(git rev-parse --show-toplevel)" &amp;&amp; python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round6/checks/r6_cn_g_1.py" reader; echo "exit=$?"</invocation><expect>ROUND 6 READER: 5 of 5 arms -- and exit=0</expect></criterion>
  <criterion id="AC2" cell_refs="CN-g-1"><invocation>cd "$(git rev-parse --show-toplevel)" &amp;&amp; python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round6/checks/r6_cn_g_1.py" seam; echo "exit=$?"</invocation><expect>ROUND 6 SEAM: 3 of 3 arms -- and exit=0</expect></criterion>
  <criterion id="AC3" cell_refs="CN-g-1"><invocation>cd "$(git rev-parse --show-toplevel)" &amp;&amp; python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round6/checks/r6_cn_g_1_census.py"; echo "exit=$?"</invocation><expect>ROUND 6 CENSUS: 4 of 4 arms -- and exit=0</expect></criterion>
</proof_of_spec>

## 5. WHEN YOU ARE DONE

Write the instance at
`org/missions/D8/MDPF/MDPF_CANON/deliverables/0.9.0_WK_MDPF_CANON~17/MDPF_CANON.TO-CN-g-1.non-model-assets-reads-the-gold-tier.proof_of_spec.json`
(beside the order's own file stem, which is the name the pipeline gate searches for). **Flip this order's `<status>` to `complete` in the SAME
commit as your proof instance**, and only when every mechanical criterion passes.

A row id on this project carries the dell1 infix: `MDPF_CANON-D1-W17-S<k>`, with `surfaced_at` taken from `date -u +%FT%TZ` at filing.
Report once: the diff (one line per file), the output line of every criterion, the self-test and test lines, the census rows before and after,
the commit hash, and any row.

<!-- ===================== RECORD FACE -- does NOT travel to the worker ===================== -->

**BLOCKER (measured at draft, 2026-10-12 ~18:1xZ; this order is NOT to be cut as written):** the script runs INSIDE the daily dispatch,
`infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:504-524`, as stage 6c ("reads the staged global+inflection aggregate ... MUST follow
6a"). Stage 6a (`build_mdpf_spine.py`) writes the staged aggregate in that same run. The gold-tier partition for as-of D is written only by the
consolidator, i.e. by the gold lambda's 13:30Z fire AFTER the dispatch of that morning: the partition `date=2026-10-09` carries S3
LastModified 2026-10-12T13:31Z, after Monday's dispatch completed (12:54:22Z, CloudOps msg 4453). So at the moment 6c runs, the gold tier is
one fire behind the staged aggregate, and a repointed 6c would build the non-model series through the PREVIOUS trading day while it builds
through T-1 today. That staged `non_model_assets.json` feeds `build_portal_gold_accrual.py:64` and the served non-model series. The seam
arm proves DELTA=0 only at a fixed, equal vintage (arm SAME-VINTAGE); it cannot prove the in-dispatch ordering, and the cell cannot fix
it inside its own paths (the ordering lives in the dispatch script and in what the gold lambda emits). CN-e-1 and CN-d-4 were safe because
they are read-only instruments that run after the fire; every reader inside the dispatch's stage 6 shares this property.

**Options for the CTO (the question this draft puts):** (a) leave stage 6 reading the staged aggregate until the dispatch chain itself retires
(M10/M12); (b) move the non-model build into the gold lambda after `emit_gold_parquet` in the consolidator (a larger SERVED cell with its own
never-widen pair, and the dispatch's 6c retires); (c) accept a one-trading-day lag on the staged non-model series (a served regression: not
recommended). REC: (a), and name in the PRD that M4's reader repoints are complete for every reader that runs after the fire.

- **Why this one was the candidate:** `ROUND6_INPUTS_READ.md` section 2: reader and writer of the staging tree, EQUAL on the runner, touches none
  of the six R2 files.
- **Measured at the cut (issuer, 2026-10-12):** the gold-tier arrays equal the staged arrays on the real vintage: `date` 494 of 494,
  `base_excluding_tax_aua` 494 of 494 (None on 9), `model_aua` 494 of 494, inflection `non_model_aua` 485 of 485; `build()` from the gold tier
  equals `build()` from the staged JSON, 497 rows, DELTA=0, latest 2026-10-09. The served `opal_aggregate_aua` differs on 25 dates.
- **The frozen snapshot stays a staging-tree READ:** `non_model_assets_precutover_frozen.json` is a one-off verbatim capture of the legacy served
  rows (pre-cutover history is not derivable); the census therefore keeps one staging row for this file (kind both). The cell does NOT make this
  file free of the tree; AC3 is worded to match.
- **Risk and class:** SERVED. The cell's own acts are code and tests (LOCAL by the spine's definition), but the file is executed by the dispatch
  chain, so the served non-model series moves when the `code/` sync lands it; that sync is a WORLD order with its own never-widen pair (it names
  `non_model_assets.json` and the accrual bridge). `worker-light`: about 70 lines added, 25 deleted, one new test file.
- **Hazards:** none in the paths; `etf_public_residual_total` absent on both sides (no column needed); the `--global-uri` override stays as a
  caller-chosen source, not a default; the file is not touched by CN-d-1's deploy, so it needs its own code/ sync with `build_portal_gold_accrual.py`
  DIFFERING on the runner (that file's sync comes first).
- **Fanout:** one cell, one chain, slot ~17; independent of CN-f-1 (disjoint files). Base box/dell1.

<status>pending</status>
<round>6</round>
<to_id>MDPF_CANON.TO-CN-g-1</to_id>
<slot>~17</slot>
<fabric>dell1</fabric>
<risk>SERVED</risk>
<worker_class>worker-light</worker_class>
