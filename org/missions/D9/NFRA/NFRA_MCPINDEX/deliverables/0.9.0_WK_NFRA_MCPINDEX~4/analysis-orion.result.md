# NFRA_MCPINDEX.TO-MX-a-4 -- Orion (Inflection) silver analysis

**Worker:** `0.9.0_WK_NFRA_MCPINDEX~4`. **Cell:** `MX-a-4` (S8, FWD-4). **Run:** 2026-09-21, ~07:3xZ.
**Bucket under analysis:** `opal-data-inf` (live, DESIRED-plane home Orion's own producer scripts write
and the deployed router's target; env override `INF_S3_BUCKET`). **Instrument:** boto3
`s3:ListObjectsV2` (paginated) for every census, `pyarrow` `read_metadata`/`read_table`
(column-projected) for object-level reads, all live at run time. Probe:
`probes/mx_a_4.py` (dispatch `AC1`..`AC9`; `AC10` is judgment, no probe).

## Canonical bucket vs live bucket (a finding, same shape MX-a-3 found for Black Diamond)

`infra/logic/registry/scopes.json[inflection].bucket` = `opal-data-inflection`
(`bucket_provisioned: true`), the Rule-30/LGIC canonical address. The registry's own alias entry for
`opal-data-inf` says "opal-data-inflection does not exist yet" -- a DECLARED claim. This cell's own
live `HeadBucket` probe on `opal-data-inflection` returned **403 Forbidden**, not 404; per CLAUDE.md's
AWS/S3 trap catalogue ("S3 403 not 404"), a 403 does not confirm absence (S3 also returns 403 for a
bucket that exists outside the caller's `ListBucket` grant). So this cell reports the registry's
DECLARED non-existence and its own MEASURED-but-ambiguous 403 side by side, and does not upgrade
either into a stronger claim. The live producer code (`convert_orion_api_to_silver.py:89`,
`INF_S3_BUCKET`/`opal-data-inf`) and the gold dispatch table (`orion-gold-dispatch.sh:64`) both target
`opal-data-inf`, so this cell fences its read to that live bucket (Rule 30's own non-application
clause: migration is a separate project's, not a rider here).

## AC1 -- live silver prefixes, denominators (PASS)

Live `ListObjectsV2` over `s3://opal-data-inf/silver/`: **16,973 objects** at run time. Twelve tables
classified as this property's canonical set (object count / bytes / newest partition date, all
2026-09-20 except the single-file `canonical_prices.parquet`):

| table | prefix | objects | bytes | newest |
|---|---|---:|---:|---|
| positions_mv | `silver/api_dims/positions_mv/` | 2,341 | 1,901,999,986 | 2026-09-20 |
| transactions | `silver/transactions/` | 1,635 | 5,142,540,918 | 2026-09-20 |
| assets_v2 | `silver/assets_v2/` | 2,337 | 1,896,120,829 | 2026-09-20 |
| performance | `silver/performance/` | 114 | 743,283,293 | 2026-09-20 |
| api_dims_billing | `silver/api_dims/billing/` | 1,636 | 14,422,939 | 2026-09-20 |
| api_dims_tax_realized | `silver/api_dims/tax_realized/` | 2,150 | 100,736,553 | 2026-09-20 |
| api_dims_tax_unrealized | `silver/api_dims/tax_unrealized/` | 2,179 | 110,555,508 | 2026-09-20 |
| api_dims_accounts_v2 | `silver/api_dims/accounts_v2/` | 139 | 11,012,607 | 2026-09-20 |
| api_dims_household_rep_mapping | `silver/api_dims/household_rep_mapping/` | 140 | 813,493 | 2026-09-20 |
| api_dims_performance | `silver/api_dims/performance/` | 134 | 8,151,201 | 2026-09-20 |
| api_dims_representatives | `silver/api_dims/representatives/` | 140 | 1,847,526 | 2026-09-20 |
| canonical_prices | `silver/prices/canonical_prices.parquet` | 1 | 8,198,865 | (single file; see AC2) |

14 excluded prefixes within `silver/` (4,027 objects, 97,077,510 bytes) and every other top-level bucket
prefix named with a reason (AC8). Zero unclassified keys at this run (one, `silver/historical_prices.parquet`,
was found and named on the first pass -- see AC8).

## AC2 -- grain, freshness field, latest value (PASS)

Every table's grain and freshness field is cited to its producer's own docstring (file:line printed by
the probe, not grepped for) and cross-checked against the live gold-chain dispatch table
(`data/inf/scripts/gold/orion-gold-dispatch.sh:240-316`, the `INF_API_SILVER_*`/`INF_S_00` rows), which
names the CURRENT writer independently of anything this cell assumed. Two notable findings surfaced by
this cross-check:

- **`transactions` is a full-history re-pull, not an incremental daily delta.** The 2026-09-19 and
  2026-09-20 partitions are 43,462,194 and 43,547,893 bytes (<0.2% day-over-day growth) and the
  2026-09-20 file carries 1,478,763 rows (`pyarrow` `ParquetFile.metadata.num_rows`) -- consistent with
  the producer's own docstring calling itself "the REST full-history spine". This directly grounds AC4
  rule 2.
- **Two tables share the name "performance" with different grains.** Root `silver/performance/` is
  `convert_performance_to_silver.py`'s per-client weekly TWR-factor table with a precomputed
  `cumulative_twr`; `silver/api_dims/performance/` is `convert_orion_api_to_silver.py`'s per-account
  3-year-window snapshot, which additionally carries a DEFER-guard that can silently carry forward a
  stale partition up to N=2 trading days on a bronze SKIP (`:1044-1058`). This grounds AC4 rule 5.

## AC3 -- scope rule per table (PASS)

None of the 12 tables' S3 keys carry a firm-prefix segment; scope is unreadable from the key for all
12, named as such. The scope token is `inflection` (FIRM, `scopes.json`). The ROW-LEVEL mechanism that
actually enforces it differs by table, measured rather than assumed uniform:

- **(a)** INFGRD `rep_id` allowlist `{3, 6, 10, 11, 12}` via `filter_to_inflection()`/`apply_aua_guard()`
  (`_orion_api_silver_lib.py:113,301-313`) -- billing, tax_realized, tax_unrealized,
  household_rep_mapping.
- **(b)** custodian-code allowlist (`custodian IN Fidelity_Inflection, Fidelity_LH`) -- `accounts_v2`
  (`convert_orion_api_to_silver.py:407-412`), a genuinely different mechanism from (a).
- **(c)** an unconditional `advisor_firm='inflection_wealth_management'` stamp with **no** in-function
  rep_id/custodian filter visible in this cell's read of the producer code -- positions_mv,
  transactions, assets_v2, root performance, api_dims/performance, representatives. **Named as an open
  verification gap, not resolved here:** whether the upstream bronze PULL for this group is already
  Inflection-scoped (so no silver-side filter is needed) was not measured by this cell.

## AC4 -- never-sum rules (PASS, 7 rules)

1. `positions_mv.current_value` never summed across `snapshot_date` (cross-date -- point-in-time
   holdings snapshot).
2. `transactions.trans_amount` never summed across date partitions (cross-date -- MEASURED full-history
   re-pull, see AC2).
3. `tax_realized` and `tax_unrealized` never summed together (non-additive / different basis -- the
   producer's own docstring says JOIN, never sum).
4. `billing.is_fee_earning` never read from silver to compute a fee-earning total (wrong layer -- RETIRED
   FROM SILVER, the single derivation home is gold's `fee_classification.py`).
5. `api_dims/performance` and root `performance` never merged despite the near-identical name (different
   grain/basis -- table-identity hazard, see AC2).
6. `canonical_prices.price` never summed across ticker or date (non-additive field -- a per-unit value).
7. Inflection's tables never summed with Eclipse's (`silver/eclipse/`, MX-a-5's property) or any future
   partner firm (cross-firm -- the extension mechanism is documented in
   `convert_orion_to_silver.py:92-100`, live proof the bucket already tolerates more than one firm).

## AC5/AC6 -- common questions, table+fields+source, assignment (PASS, 10 questions)

10 questions numbered 1-10 (probe AC5 output), each naming its table, fields and source (producer code,
or for Q7 a re-use of a pattern already implemented elsewhere in the codebase); none presented as
measured user demand -- this cell read no query log or usage telemetry. 9 of 10 assigned to the typed
query (C6); 1 (Q7, "who is the advisor of record and how was that derived") assigned to a proposed tool,
because it requires a two-table JOIN with an explicit fallback order and must disclose which source
resolved the answer -- business logic beyond C6's filter/group-by/aggregate scope.

## AC7 -- tool name validated against C3 (PASS)

One proposed tool: `orion_resolve_rep_of_record`. `orion` is a live `systems.json` key (VENDOR class);
`resolve` is a base-form verb; no scope token (`scopes.json`'s 9 keys, including `inflection`) appears
folded into the name -- scope is an explicit call argument. Validated programmatically by the probe
against the live registries, not asserted.

## AC8 -- read fence (PASS)

12 exact prefixes proposed (table above). 14 exclusions named within `silver/` (each cross-checked
against BOTH the S3 staleness measurement AND absence from the live gold-chain dispatch table -- two
independent instruments agreeing), plus every other top-level bucket prefix named with a reason. A
migration-gap finding (canonical bucket `opal-data-inflection` vs live `opal-data-inf`) is recorded as a
NOTE, not folded into the fence.

## AC9 -- presence antecedent (PASS)

16,973 objects / ~10.0 GB live under `silver/` at run time -- Orion HAS live data, so the criterion's
"says so, proposes no tool" branch does not bind; 10 questions were correctly proposed under a TRUE
antecedent.

## AC10 -- judgment (left to the CVO)

Not graded here. `status_reason`: graded by `3.0.0_SA_CVO` at L9 per the task order's own instruction.

## Surprise filed

`NFRA_MCPINDEX-W4-S2` (OBSERVATION, ARMED, `disarm_owner: 2.0.0_SA_COO~M`): the prior MX-a-3
(Black Diamond) drain merge (`0c46bec859`) does not carry that worker's four deliverable files or the
task order's status flip into the merged tree reachable from this worktree's cut (`8fd757cca8`), though
the merge commit's own message claims "order complete" / "proof VALID". Filed because this cell's own
issuer-context preamble named that file as readable prior work in this slot, and it is not present.
Does not block this cell's own criteria (none read that file).

## Instrument notes

- Every AWS read in this cell is a READ verb only (`ListObjectsV2`, `GetObject`, `HeadObject`,
  `HeadBucket`), boto3, live at run time -- no write to any AWS resource.
- `infra/logic/registry/systems.json` and `scopes.json` read live from the worktree at HEAD, not
  grepped for a remembered value.
- The dispatch-table cross-check (`orion-gold-dispatch.sh`) is a SECOND, independent instrument from the
  S3 staleness measurement; both agree on every exclusion in AC8's set, which is the corroboration this
  cell relies on rather than either instrument alone.
