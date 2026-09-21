# NFRA_MCPINDEX.TO-MX-a-6 -- SmartX silver analysis

**Worker:** `0.9.0_WK_NFRA_MCPINDEX~4`. **Cell:** `MX-a-6` (S8, FWD-4). **Run:** 2026-09-21, ~09:5xZ-10:0xZ UTC.
**Bucket under analysis:** `opal-data-assets` (live; confirmed via live listing at run time), prefix
`smartx/platform/silver/`. **Instrument:** boto3 `s3:ListObjectsV2` (paginated) for every census, `pyarrow`
`read_metadata` (column-projected) for object-level reads, `HeadBucket` for bucket-existence checks, live JSON
parses of `infra/logic/registry/{systems,scopes}.json` and `data/mdpf/config/partner_roster.json` at HEAD,
all live at run time. Probe: `probes/mx_a_6.py` (dispatch `AC1`..`AC9`; `AC10` is judgment, no probe).

## Which bucket is "the property" -- a finding, not repaired (bound 9)

Three candidate SmartX locations exist live; only one is measured canonical:

1. **`s3://opal-data-assets/smartx/platform/{bronze,silver}/` -- the property this cell reads.** Confirmed by
   four independent carriers: `workflows/vendor_watch/README.md`'s live-vs-mirror table names it "genuinely
   lives in the monolith" (unlike Eclipse/Orion/Black Diamond, it carries NO stale-mirror caveat);
   `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/smartx_runtime.py:34` defaults
   `MONOLITH_BUCKET` to `opal-data-assets`; `key_mapping.py`'s ruled grammar (CTO gate 2026-07-14, "PERMANENT
   in bronze") builds exactly this path; `data/mdpf/config/partner_roster.json` and `route_bindings.yaml`
   both wire MDPF's live SmartX feeds to `bucket: opal-data-assets, prefix: smartx/platform/silver/fact_*`.
2. **`s3://opal-data-bd/smartx/`** -- MEASURED live this run: 2,967 objects / ~64,664,996 bytes (also filed as
   `NFRA_MCPINDEX-W4-S1` by this worker on `MX-a-3`), sub-prefixes `bronze/`, `jwt/`, `raw/`. Named in NO
   canonical carrier above. Excluded (AC8).
3. **`s3://opal-data-smartx/`** -- the bucket `data/smartx/docs/smartx_data_info.md` describes (an Excel/API
   dashboard product, `consolidated/smartx_allocations.parquet`, never called "silver" in that doc). MEASURED
   live this run: `HeadBucket` on `opal-data-smartx` returns **404 NotFound** -- the bucket does not exist at
   this cell's run time. Excluded (AC8/AC9 aside).

## AC1 -- live silver listing, denominators (PASS)

Live `ListObjectsV2` over `s3://opal-data-assets/smartx/platform/silver/`: **757 objects** at run time. 11
canon tables, all with a 2026-09-20 newest partition, plus 2 pre-naming-law DRAFT objects (excluded):

| table | objects | bytes | newest |
|---|---:|---:|---|
| fact_allocation_positions | 69 | 217,296,809 | 2026-09-20 |
| fact_allocation_valuation | 69 | 79,189,581 | 2026-09-20 |
| fact_allocation_account_map | 68 | 36,413,004 | 2026-09-20 |
| fact_model_aum_daily | 69 | 5,622,132 | 2026-09-20 |
| fact_model_allocation_roster | 69 | 39,288,173 | 2026-09-20 |
| fact_account_allocations | 68 | 2,470,769 | 2026-09-20 |
| fact_nonzerosleeve | 68 | 920,276 | 2026-09-20 |
| fact_account_detail | 68 | 999,998 | 2026-09-20 |
| fact_model_holdings | 69 | 1,759,674 | 2026-09-20 |
| fact_model_performance | 69 | 21,984,732 | 2026-09-20 |
| fact_model_changerequests | 69 | 4,943,752 | 2026-09-20 |

EXCLUDED (named, AC8): 2 objects (`allocation_positions/`, `allocation_valuation/` -- pre-naming-law DRAFT,
one 2026-07-14 partition each), 4,177,438 bytes. **0 unclassified keys across all 757 objects** at this run --
this cell's first `classify()` run matched every live object (see mutant-control note below).

## AC2 -- grain, freshness field, latest value (PASS)

Every table's grain and freshness field is cited to `silver.py`'s own docstrings/constants (file:line printed
by the probe, not grepped for). Every table's "latest value" is the `{date}` partition folder
(`date=YYYY-MM-DD`, the daily converter's `run_date`); several tables additionally carry a per-row date
column (`day` for `fact_model_aum_daily`/`fact_model_performance`, `as_of` for the allocation-atom pair) that
diverges in meaning from the partition date (see below). All 11 tables' latest live partition is
**2026-09-20**.

**Two findings surfaced by this cell's own live pyarrow reads:**

- **`run_date` (partition date) is NOT the same axis as the per-row observation date for 4 of 11 tables.**
  `fact_model_aum_daily` and `fact_model_performance` explode a FULL HISTORY series into per-row `day` values
  standardized from the vendor's own date; `fact_allocation_positions`/`fact_allocation_valuation` carry a
  per-row `as_of` snapshot date. Conflating "latest partition" with "latest observation" for these four tables
  is a reading error, not this cell's to repair -- named for AC4/AC6 callers.
- **4 of 11 tables' latest (2026-09-20) partition landed 0 rows.** Live `pyarrow.read_metadata`:
  `fact_allocation_account_map` 0 rows, `fact_account_allocations` 0 rows, `fact_nonzerosleeve` 0 rows,
  `fact_account_detail` 0 rows -- all four are the **account-tier** family. `smartx_conversion.py`'s own
  `_build_account_platform_tables` docstring (:190-196) states this is a LEGITIMATE EMPTY FRAME: the
  account-tier bronze is bundle-credentialed and "may be absent when the account tier did not run ... an
  ordinary daily opal7-grant pull lands NO account-tier bronze ... so on those days every probe below is a
  legitimate miss." This cell reports the live 0-row reading as-measured (Rule 22 DESIRED-vs-APPLIED), and
  does not assert whether 2026-09-20 was or was not a bundle-credentialed run -- that determination needs the
  day's conversion manifest (`smartx/platform/meta/conversions/`), out of this cell's grant.

## AC3 -- scope rule per table (PASS)

None of the 11 tables' S3 keys (subdir or the shared `{date}=` folder) carry a firm-prefix segment; scope is
unreadable from the key for all 11, named as such. **Registry gap, named not repaired:** live
`infra/logic/registry/scopes.json` parse shows `smartx` absent from every one of 9 scope rows'
`monolith_scopes` (only `blackdiamond` and, for Inflection, `orion`/`eclipse` are registered there) -- unlike
every other `MX-a-k` vendor this project analyses, SmartX has no scopes.json monolith-vendor entry at all.
**Firm scope is instead read from `data/mdpf/config/partner_roster.json`**, live-parsed: exactly 2 smartx-vendor
feed rows, both registered under `firm_id: "49financial"` -- the same firm Black Diamond (`MX-a-3`) serves,
consistent with `smartx_bd_join_disposition.yaml`'s "49F account universe" join target.

**Row-level scope mechanism -- NOT independently verified by this cell**, named as an open gap (same shape as
`MX-a-4`/`MX-a-5`'s AC3 findings): no producer-code read of a firm/tenant filter inside
`smartx_conversion.py`/`silver.py` was performed here; whether the SmartX vendor connection itself is
single-tenant (49financial-exclusive, needing no in-pipeline filter) was not checked.

## AC4 -- never-sum rules (PASS, 8 rules)

1. `fact_model_aum_daily.closing_equity` never summed across `run_date` partitions for the same (rmid, day)
   (cross-date -- each `run_date` partition re-delivers the FULL HISTORY series, `silver.py:211-215`).
2. `fact_model_performance`'s market-value/pnl fields never summed across `day` rows for one model
   (non-additive/state-grain -- each day-row is a snapshot, not a flow, `silver.py:960-1007`).
3. `fact_allocation_valuation`'s five AUM basis components never summed together into one total (non-additive
   field -- Andrew ruled GROSS = longEquity+cash canonical and reserved the right to change it, module
   docstring `silver.py:6-18`).
4. `fact_model_aum_daily.total_aum` never used in a total (wrong-basis -- "PRESERVED but mis-scaled -- gold
   ignores it", `silver.py:194`).
5. `fact_model_allocation_roster.value` never summed into an AUM total without filtering `status='open'`
   (wrong-layer -- inclusive of closed/workingClose rows, live census 7,125/2,381/34 of 9,540,
   `silver.py:293-296`).
6. SmartX's fact tables never summed with Black Diamond's (`MX-a-3`) without the `smartx_bd_join_disposition.yaml`
   v1.0 crosswalk (cross-vendor -- RATIFIED CTO gate 2026-08-19, MECE outcome enum 7286+16+3+0=7305).
7. SmartX's fact tables never summed with any other firm's data (cross-firm -- `partner_roster.json` names
   only `49financial`, and `scopes.json` names no second firm either, per AC3's finding).
8. `fact_allocation_positions`/`fact_allocation_valuation` rows never summed across `as_of` snapshots for one
   `allocation_id` (cross-date -- `to_frames()`'s natural-key checks key on `as_of` precisely because a second
   `as_of` is a different state, `silver.py:507-522`).

## AC5/AC6 -- common questions, table+fields+source, assignment (PASS, 10 questions)

10 questions numbered 1-10 (probe AC5 output), each naming its table, fields and source (producer code, the
ratified `smartx_bd_join_disposition.yaml` contract, or reasoning grounded in this cell's own live
measurement); none presented as measured user demand -- this cell read no query log or usage telemetry. 9 of
10 assigned to the typed query (C6); 1 (Q2, the model's GROSS AUM under Andrew's ruled basis) assigned to a
proposed tool, because it requires filtering the roster to open allocations (AC4 rule 5), joining each to its
valuation row, and summing `long_equity+cash` across that filtered, joined set -- business logic beyond C6's
single-table scope, the same shape as `MX-a-5`'s Eclipse `aum_variance` tool.

## AC7 -- tool name validated against C3 (PASS)

One proposed tool: `smartx_summarize_model_gross_aum`. `smartx` is a live `systems.json` key (VENDOR class,
25 keys total); `summarize` is a base-form verb in this cell's recognized set; no scope token (`scopes.json`'s
9 keys, including `49financial`) appears folded into the name -- scope is an explicit call argument. Validated
programmatically by the probe against the live registries, not asserted. Determinism control: AC7 invoked
twice back to back, outputs byte-identical after stripping the vintage timestamp line.

## AC8 -- read fence (PASS)

ONE exact prefix proposed (`s3://opal-data-assets/smartx/platform/silver/`), covering all 11 canon tables. 2
exclusions named within the prefix (the pre-naming-law draft objects), plus every other top-level/sibling
prefix (this bucket's other vendors, `smartx/platform/bronze/` and `smartx/platform/meta/`, and the two OTHER
candidate SmartX locations discussed above) named with a reason.

## AC9 -- presence antecedent (PASS)

757 objects / ~415.1 MB live under `smartx/platform/silver/` at run time -- SmartX HAS live data at its
canonical location, so the criterion's "says so, proposes no tool" branch does not bind; 10 questions were
correctly proposed under a TRUE antecedent.

## AC10 -- judgment (left to the CVO)

Not graded here. `status_reason`: graded by `3.0.0_SA_CVO` at L9 per the task order's own instruction.

## Controls

- **Mutant (offline + live).** `probes/_mutant_control_a6.py` (a NEW file, not an overwrite of
  `probes/_mutant_control.py`, which the issuer named as pinned by `MX-a-5`'s proof_of_spec instance by hash)
  imports `classify()` from `mx_a_6.py`, plants a synthetic key under `smartx/platform/silver/` matching
  neither a `CANON_TABLES` subdir nor an `EXCLUDED_SUBDIRS` entry, confirms it is flagged unclassified
  (engaged), then confirms a clean list (real canon + real draft keys) flags nothing (disengaged). Both arms
  fired as expected (`engaged_ok=True disengaged_ok=True`). LIVE, naturally occurring: this cell's first AC1
  run against the real 757 objects already returned 0 unclassified with no fix cycle -- the live control here
  is a clean positive rather than a FAIL-then-PASS pair; the offline synthetic plant is this cell's primary
  discriminator for the UNCLASSIFIED path.
- **Determinism.** AC7 run twice back to back; outputs byte-identical apart from the vintage line.

## Surprise filed

None filed by this cell. This cell's own read of `NFRA_MCPINDEX-W4-S1` (filed by this same worker on `MX-a-3`,
present in `org/missions/D9/NFRA/NFRA_MCPINDEX/surprise-channel/investigations/INVESTIGATION_v1.md`) already
covers the `opal-data-bd/smartx/` undocumented-location finding this cell independently re-measured and cites
in AC8; nothing new of that shape surfaced here. The `opal-data-smartx` bucket's absence (HeadBucket 404) and
the account-tier 0-row partitions (AC2) are recorded as findings in this result file rather than as new rows,
per bound 9 (a criterion satisfiable as written is not a surprise merely because it surfaces a finding).

## Instrument notes

- Every AWS read in this cell is a READ verb only (`ListObjectsV2`, `GetObject`, `HeadBucket`), boto3, live at
  run time -- no write to any AWS resource.
- `infra/logic/registry/systems.json`, `scopes.json` and `data/mdpf/config/partner_roster.json` read live from
  the worktree at HEAD, not grepped for a remembered value.
- The scope-registration cross-check (AC3: scopes.json's absence vs partner_roster.json's presence) and the
  account-tier 0-row finding (AC2) are two independent instruments; both are printed with their own source
  label, and neither is upgraded past what it actually shows (the registry gap is reported as a gap, not
  repaired; the 0-row partitions are reported as measured, not asserted to be an error).
