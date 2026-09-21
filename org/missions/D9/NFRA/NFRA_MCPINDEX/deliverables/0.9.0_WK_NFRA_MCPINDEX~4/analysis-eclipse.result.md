# NFRA_MCPINDEX.TO-MX-a-5 -- Eclipse (Inflection) silver analysis

**Worker:** `0.9.0_WK_NFRA_MCPINDEX~4`. **Cell:** `MX-a-5` (S8, FWD-4). **Run:** 2026-09-21, ~09:0xZ-09:1xZ UTC.
**Bucket under analysis:** `opal-data-inf` (live; confirmed via `HeadBucket` at run time; the SAME bucket
`MX-a-4` (Orion) reads -- Eclipse is a SECOND vendor's silver tier in it, prefix `silver/eclipse/`). **Instrument:**
boto3 `s3:ListObjectsV2` (paginated) for every census, `pyarrow` `read_metadata` (column-projected) for
object-level reads, all live at run time. Probe: `probes/mx_a_5.py` (dispatch `AC1`..`AC9`; `AC10` is judgment,
no probe).

## Layout difference from MX-a-4/Orion (a finding, not repaired -- s.9 bounds item 9)

Orion's silver tables each own a DISTINCT sub-prefix (`silver/api_dims/positions_mv/`,
`silver/transactions/`, ...). Eclipse's four tables (`portfolios_simple`, `portfolios_full`, `models`,
`model_composition`) are all SIBLING FILES under the SAME `silver/eclipse/{date}/` folder, distinguished by
FILENAME, not by a table-specific path segment (`convert_eclipse_portfolios_to_silver.py:3-11`, MEASURED
live against 570 objects). So this cell's `classify()` matches by filename suffix, not folder prefix, and
the AC8 read fence is necessarily ONE prefix (`silver/eclipse/`) covering all four tables -- no S3 prefix
can isolate one Eclipse table from the other three.

## AC1 -- live silver listing, denominators (PASS)

Live `ListObjectsV2` over `s3://opal-data-inf/silver/eclipse/`: **570 objects** at run time. Four tables,
one shared EXCLUDED sentinel class:

| table | filename | objects | bytes | newest |
|---|---|---:|---:|---|
| portfolios_simple | `portfolios_simple.parquet` | 114 | 7,331,276 | 2026-09-20 |
| portfolios_full | `portfolios_full.parquet` | 114 | 12,313,002 | 2026-09-20 |
| models | `models.parquet` | 114 | 2,971,955 | 2026-09-20 |
| model_composition | `model_composition.parquet` | 114 | 4,282,653 | 2026-09-20 |

EXCLUDED (named, AC8): 114 objects (`_meta/silver_complete.json` sentinels), 51,870 bytes. 0 unclassified
keys across all 570 objects at this run -- unlike `MX-a-4`, this cell's classify() matched every live
object on its first run, with no FAIL-then-fix iteration (see the mutant-control note below).

## AC2 -- grain, freshness field, latest value (PASS)

Every table's grain and freshness field is cited to its producer's own docstring (file:line printed by the
probe, not grepped for), cross-checked against the live gold-chain dispatch table
(`data/inf/scripts/gold/orion-gold-dispatch.sh:315`, `INF_ECLIPSE_SILVER`). Every table's "latest value" is
the date folder name; none of the four tables carries a per-row date column (unlike several of Orion's
tables). Two findings surfaced by this cell's own live pyarrow reads, cross-checked against the module
docstring:

- **Two of the four tables' docstring row counts are STALE against the live partition.** The module
  docstring (`convert_eclipse_portfolios_to_silver.py:7-8`) states `portfolios_simple.parquet` carries 835
  rows and `portfolios_full.parquet` carries 842 rows. This cell's live `pyarrow.read_metadata` on the
  2026-09-20 partition measured **844** and **858** rows respectively -- the docstring's counts are a
  snapshot from an earlier pull, not a live invariant. `models.parquet` (18 rows) and `model_composition.parquet`
  (9 rows) DID match the docstring exactly at this run. This cell reports the LIVE counts as authoritative,
  per Rule 22's DESIRED-vs-APPLIED distinction, and does not repair the docstring (out of this cell's
  `<paths>` grant).
- **Day-over-day size stability confirms a FULL daily re-pull, not an incremental delta**, grounding AC4
  rule 1/2: `models.parquet` is BYTE-IDENTICAL (25,029B) across the 2026-09-19 and 2026-09-20 partitions;
  `portfolios_simple`/`portfolios_full` sizes move by <0.2%/<0.05% day-over-day. This is consistent with
  `pull_eclipse_portfolios.py`'s own top-of-file warning: `--date` is an OUTPUT FILENAME LABEL, not a query
  parameter -- "ALL pulls fetch TODAY'S live state", never a historical delta.

## AC3 -- scope rule per table (PASS)

None of the 4 tables' S3 keys (filename or the shared `{date}/` folder) carry a firm-prefix segment; scope
is unreadable from the key for all 4, named as such. The scope token is `inflection` (FIRM); `eclipse` is a
MONOLITH VENDOR key under `scopes.json[inflection].monolith_scopes.eclipse = ["inflection"]`, not its own
scopes.json row -- Eclipse is entirely Inflection-scoped, the same shape `MX-a-4` measured for Orion.

**Row-level scope mechanism -- an open verification gap, named not resolved (same shape as `MX-a-4` AC3
finding (c)):** `convert_eclipse_portfolios_to_silver.py` imports `coerce_silver_ids` from
`_orion_api_silver_lib.py` (dtype coercion only, MEASURED at `_orion_api_silver_lib.py:283-298`, no scope
filter inside it) but contains **0 calls** to `filter_to_inflection()` (`_orion_api_silver_lib.py:301-311`,
the INFGRD rep_id allowlist Orion's tables use). Whether the Eclipse VENDOR CONNECTION itself is already
Inflection-exclusive (a single-tenant integration, so no in-pipeline filter is needed) was not verified by
this cell. Indirect evidence toward that reading: `pull_eclipse_portfolios.py`'s own docstring describes its
endpoints as returning "all firm portfolios" (singular firm), and `scopes.json` lists exactly one scope
under `monolith_scopes.eclipse`.

## AC4 -- never-sum rules (PASS, 7 rules)

1. `portfolios_simple`/`portfolios_full` fields never summed across `{date}` partitions (cross-date --
   MEASURED full-daily-repull pattern, see AC2).
2. `models`/`model_composition` fields never summed across dates (cross-date -- same reasoning, MEASURED
   stable row counts across two dates).
3. `portfolios_full.total_value` never summed together with `model_composition.model_aum` into one combined
   AUM figure (non-additive / different basis -- the gold tier keeps them side by side and computes an
   explicit `aum_variance` diagnostic, `INF_E_00.eclipse_model_portfolios.py:19-23,303`, precisely because
   they are meant to be COMPARED, never combined).
4. Rows outside `OPAL_ECLIPSE_MODEL_IDS {3,5,6,7,8,9,10,28,29}` never summed into an "Opal-managed AUM"
   total read directly from silver (wrong layer -- MEASURED at this run: of 844 live `portfolios_simple`
   rows, 567 Opal-model, 95 non-Opal-model, 182 null model_id -- 33% would be wrongly included unfiltered;
   the Opal-model filter is applied at GOLD, `INF_E_00.py:151`, not silver).
5. `is_deleted=1` rows never summed into a live AUM total read directly from silver (wrong layer -- gold's
   defensive filter, `INF_E_00.py:153-154`; MEASURED 0 of 844 live rows currently flagged, so not materially
   exercised today, but the column and the gold-layer filter both exist).
6. Eclipse's silver tables never summed with Orion's (`MX-a-4`'s property, same bucket) without the explicit
   `accounts_v2` crosswalk join (cross-vendor -- different id spaces, `eclipse_account_id_*` vs Orion's
   `accountId`; `INF_E_00.py:13-14` names `silver/api_dims/accounts_v2/` as the one sanctioned join target).
7. Eclipse's silver tables never summed with Black Diamond's (`MX-a-3`) or any future partner firm's data
   (cross-firm -- same shared-bucket, key-prefix-scoped isolation model as `MX-a-4` AC4 rule 7, PRD C7).

## AC5/AC6 -- common questions, table+fields+source, assignment (PASS, 10 questions)

10 questions numbered 1-10 (probe AC5 output), each naming its table, fields and source (producer code, a
re-use of a pattern already implemented in `INF_E_00.eclipse_model_portfolios.py`, or reasoning grounded in
this cell's own live measurement); none presented as measured user demand -- this cell read no query log or
usage telemetry. 9 of 10 assigned to the typed query (C6); 1 (Q2, the model-headline-AUM-vs-live-portfolio-
AUM variance question) assigned to a proposed tool, because it requires filtering to the Opal-model set
(AC4 rule 4), excluding deleted rows (AC4 rule 5), summing within that filter, reading a SEPARATE table's
cached figure, and disclosing the variance -- business logic beyond C6's single-table filter/group-by/
aggregate scope, and a pattern already implemented once at gold (`INF_E_00.py:283-304`).

## AC7 -- tool name validated against C3 (PASS)

One proposed tool: `eclipse_summarize_aum_variance`. `eclipse` is a live `systems.json` key (VENDOR class);
`summarize` is a base-form verb in this cell's recognized set; no scope token (`scopes.json`'s 9 keys,
including `inflection`) appears folded into the name -- scope is an explicit call argument. Validated
programmatically by the probe against the live registries, not asserted. Determinism control: AC7 invoked
twice back to back, outputs byte-identical after stripping the vintage timestamp line.

## AC8 -- read fence (PASS)

ONE exact prefix proposed (`s3://opal-data-inf/silver/eclipse/`), covering all 4 canon tables (per the
layout-difference finding above -- no finer S3 fence is possible without also excluding sibling tables). 1
exclusion named within the prefix (`_meta/silver_complete.json` sentinels), plus every other top-level/
sibling bucket prefix (including Orion's own tables, named individually per `MX-a-4`'s own AC8) named with a
reason.

## AC9 -- presence antecedent (PASS)

570 objects / ~25.7 MB live under `silver/eclipse/` at run time -- Eclipse HAS live data, so the criterion's
"says so, proposes no tool" branch does not bind; 10 questions were correctly proposed under a TRUE
antecedent.

## AC10 -- judgment (left to the CVO)

Not graded here. `status_reason`: graded by `3.0.0_SA_CVO` at L9 per the task order's own instruction.

## Controls

- **Mutant (offline + live).** `probes/_mutant_control.py` imports `classify()` from `mx_a_5.py`, plants a
  synthetic key under `silver/eclipse/` matching neither a `CANON_TABLES` filename nor an `EXCLUDED_SUFFIXES`
  entry, confirms it is flagged unclassified (engaged), then confirms a clean list flags nothing
  (disengaged). Both arms fired as expected (`engaged_ok=True disengaged_ok=True`). LIVE, naturally
  occurring: unlike `MX-a-4`, this cell's first AC1 run against the real 570 objects already returned 0
  unclassified with no fix cycle -- so the live control here is a clean positive rather than a
  FAIL-then-PASS pair; the offline synthetic plant is this cell's primary discriminator for the
  UNCLASSIFIED path.
- **Determinism.** AC7 run twice back to back; outputs byte-identical apart from the vintage line.

## Surprise filed

None filed by this cell. This cell's own read of the prior-cell file
(`org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~4/analysis-orion.result.md`,
present in this worktree at cut `60464dd3f8`) confirms `NFRA_MCPINDEX-W4-S2` (filed by this same worker on
`MX-a-4`) already covers the MX-a-3-drain-carry gap; nothing new of that shape surfaced here.

## Instrument notes

- Every AWS read in this cell is a READ verb only (`ListObjectsV2`, `GetObject`, `HeadBucket`), boto3, live
  at run time -- no write to any AWS resource.
- `infra/logic/registry/systems.json` and `scopes.json` read live from the worktree at HEAD, not grepped for
  a remembered value.
- The row-count cross-check against the module docstring (AC2) and the gold-chain dispatch-table citation
  (`orion-gold-dispatch.sh:315`) are two independent instruments; both are printed with their own source
  label, and neither is upgraded past what it actually shows (docstring counts reported STALE, not wrong;
  the row-level scope mechanism reported as an open gap, not resolved).
