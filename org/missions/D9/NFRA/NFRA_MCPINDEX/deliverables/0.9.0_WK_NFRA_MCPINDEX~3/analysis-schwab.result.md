# NFRA_MCPINDEX.TO-MX-a-2 -- Schwab analysis result

`0.9.0_WK_NFRA_MCPINDEX~3` | cell `MX-a-2` | worktree branch `wk-nfra_mcpindex-1-3b` @ `6d5ab1a0287b00f91f8ef72985047dbdf56fb876`
Measured 2026-09-21, run window ~07:00Z-08:10Z UTC. Instrument: `.tools/aws s3api` (account 313476888478, us-east-1,
READ verbs only, list-objects-v2 auto-paginates by default -- no `--no-paginate` used anywhere below, so every count
below is the TRUE total, never a page count), `py -3.12` + `pyarrow` 18.1.0 (direct parquet reads of the newest live
partition), `git`, `comp-find`/`comp-read`, direct file reads. All S3 evidence is LIVE at run time; all repository
citations print the bytes at the cited line/path (PRD Rule VII.5), at worktree HEAD
`6d5ab1a0287b00f91f8ef72985047dbdf56fb876`.

Read: PRD `org/missions/D9/NFRA/NFRA_MCPINDEX/prd/NFRA_MCPINDEX_PRD.md@b7dc80e2cc` (ENDPOINT FWD-3, CONTRACTS
C1-C8, SURFACE MANIFEST S4); decomposition
`org/missions/D9/NFRA/NFRA_MCPINDEX/decompositions/NFRA_MCPINDEX_DECOMP.md@f506f63a8b` s.1 (falsifier 3), s.3
(`MX-a-2`/`MX-t-2` cells, S8 acceptance and property-specific additions), s.6 (gates), s.8 (bounds), s.11 (findings
1, 3); research record `docs/briefs/opal-mcp-tool-index-scoping-20260917.md@2a7fc3339f` (RESEARCH ONLY, PRD VII.6 --
read as prior art, never as measured fact) s.1-s.4 (P2 row, the typed-query pattern, rules every tool inherits); the
prior sibling cell's result `.../0.9.0_WK_NFRA_MCPINDEX~3/analysis-portal.result.md` for pattern only, not inherited
as fact for this property. ISSUER CONTEXT (this cell's own worker face) instructs: instance `firm` field is
`FABRIC` (ruling `1.0.0_SA_CTO` @`f1c469829c`, row `NFRA_MCPINDEX-W1-S2`); next row id `NFRA_MCPINDEX-W3-S2`; row
`NFRA_MCPINDEX-W4-S1`'s `opal-data-bd`/`schwab/` lead is treated as a lead to independently measure (AC8/AC12
below), not inherited; `MX-p-1` (the live baseline) has not run, so AC11's APPLIED half is recorded ABSENT, never
substituted.

---

## COMMAND LOG (read verb, AC1/AC11/AC12)

All AWS reads below are `s3api list-objects-v2` (auto-paginating; every multi-hundred/multi-thousand count below was
cross-checked with `--query "length(Contents)"` against a raw `Contents` array of the same length, confirming no
1000-object page truncation) or `s3api get-object` (parquet byte reads, one partition per table). No write verb was
used anywhere in this cell. Downloaded parquet files sit in `.scratch/parquet/` (worker worktree, not part of the
grant, not committed).

```
.tools/aws s3api list-objects-v2 --bucket opal-data-assets --prefix "schwab/" --delimiter "/"
.tools/aws s3api list-objects-v2 --bucket opal-data-assets --prefix "schwab/{master}/silver/{table}/" --query "[length(Contents), max_by(...), sum(...)]"   (x8: 2 masters x 4 dim_ tables)
.tools/aws s3api list-objects-v2 --bucket opal-data-assets --prefix "schwab/{master}/silver/fact_" --query "[length(Contents), sum(...)]" and per-key listing  (x2 masters, fact_* census, AC12)
.tools/aws s3api get-object --bucket opal-data-assets --key "schwab/{master}/silver/{table}/date=2026-09-18/data.parquet" <local>   (x8: newest partition per master/table, read via pyarrow)
.tools/aws s3api list-objects-v2 --bucket opal-data-bd --prefix "schwab/" --delimiter "/"                                            (AC8/AC12, the W4-S1 lead, independently re-measured)
.tools/aws s3api list-objects-v2 --bucket opal-data-bd --prefix "schwab/" --query "[length(Contents), sum(...), max_by(...)]"
.tools/aws s3api list-objects-v2 --bucket opal-data-bd --prefix "schwab/silver/" --delimiter "/"
```

---

## AC1 -- live prefixes, object count, total bytes, newest date, per table

**Denominator: 8** (this property's 4 servable tables -- `dim_position`, `dim_balance`, `dim_asset`,
`dim_transaction` -- x 2 masters, S8's own property definition: "Schwab: masters 08242234 and 08335338, the four
projections"). Bucket `opal-data-assets` (`schwab_reader_iam.tf:42`, `local.schwab_bucket = "opal-data-assets"`,
printed). The 15/16 `fact_*` vendor-shaped tables per master are a SEPARATE census under AC12 (they are not part of
this property's four "projections", per `schwab_projections.py`'s own docstring: "the `dim_` prefix IS the
projection marker (`fact_` = complete vendor-shaped silver; `dim_` = tight question-shaped)").

**Top-level, MEASURED** (`s3api list-objects-v2 --prefix "schwab/" --delimiter "/"`): exactly 2 `CommonPrefixes`,
`schwab/08242234/` and `schwab/08335338/` -- the two masters, matching `data_entitlement.py:63`'s `MASTERS =
("08242234", "08335338")`.

| master | table | n objects | total bytes | newest object (LastModified) |
|---|---|---:|---:|---|
| 08242234 | `dim_position` | 582 | 799,185,405 | `date=2026-09-18/data.parquet`, 2026-09-19T10:16:03Z |
| 08242234 | `dim_balance` | 582 | 239,780,965 | `date=2026-09-18/data.parquet`, 2026-09-19T10:16:03Z |
| 08242234 | `dim_asset` | 673 | 118,744,973 | `date=2026-09-18/data.parquet`, 2026-09-19T10:16:06Z |
| 08242234 | `dim_transaction` | 673 | 77,446,469 | `date=2026-09-18/data.parquet`, 2026-09-19T10:15:55Z |
| 08335338 | `dim_position` | 554 | 783,845,869 | `date=2026-09-18/data.parquet`, 2026-09-19T09:46:37Z |
| 08335338 | `dim_balance` | 554 | 233,905,871 | `date=2026-09-18/data.parquet`, 2026-09-19T09:46:37Z |
| 08335338 | `dim_asset` | 554 | 99,462,394 | `date=2026-09-18/data.parquet`, 2026-09-19T09:46:48Z |
| 08335338 | `dim_transaction` | 554 | 67,871,049 | `date=2026-09-18/data.parquet`, 2026-09-19T09:46:28Z |

**Asymmetry, MEASURED, named rather than smoothed over:** master 08242234's `dim_position`/`dim_balance` share one
object count (582) while `dim_asset`/`dim_transaction` share a different, larger one (673) -- a 91-object gap.
Master 08335338 carries the SAME count (554) across all four tables. Both are `s3api` list counts at this run's
vintage; the gap is not chased further here (out of this cell's writes; a future cell reading historical
completeness would need it). Newest partition for every one of the 8 tables, both masters, is `date=2026-09-18`
(no table lags behind another at this run time). Read verb: `s3api list-objects-v2`, printed above; no write verb.

`VERDICT: PASS-MXA2-AC1`

---

## AC2 -- grain, freshness field, latest value per table, source printed

**Grain**, source `infra/aws/ec2/opal-gateway/app/integrations/schwab/query.py:136-140` (`DATASET_GRAINS`, printed):
```
"dim_position": (ACCOUNT_SOURCE, "cusip", "l_s"),   # one row per (account, security, long/short)
"dim_balance":  (ACCOUNT_SOURCE,),                  # one row per account
"dim_asset":    ("cusip",),                         # one row per security -- NOT account-scoped
```
`dim_transaction` has NO entry in `DATASET_GRAINS` (it is not in the exposed 3; the engine declares no grain for
it). Its own source, `data/assets/scripts/silver/schwab_projections.py:52-54` (printed): "per-partition APPEND, NO
row-unique key (refuted from bytes v1.2.1; row identity downstream = (partition, row_position) provenance)" -- so
its grain is the partition itself (master, date), with no per-row key at all.

**Freshness field.** `business_date` is an in-row column for `dim_position`, `dim_balance` and `dim_transaction`
(MEASURED live: `pyarrow.parquet.read_table` on the newest partition of each, both masters -- every sampled row0
carries `business_date = "2026-09-18"`, matching the partition key). **`dim_asset` carries NO `business_date`
column at all** -- MEASURED live (parquet read, 08242234 and 08335338 both) and confirmed at the source:
`infra/aws/ec2/opal-gateway/app/integrations/schwab/query.py:120-130` (`DATASET_SCHEMAS["dim_asset"]`, printed
verbatim) lists 9 fields, none named `business_date`. **`dim_asset`'s freshness is therefore the S3 partition key
alone** (`date=` segment), never an in-row field -- named per this criterion's own requirement (parallel to
`MX-a-1`'s `etfs` table, whose scope likewise lived outside its own object).

**Latest value, MEASURED** (live parquet, newest partition `date=2026-09-18` for all 8): `business_date =
"2026-09-18"` on every sampled row of `dim_position`/`dim_balance`/`dim_transaction`, both masters;
`dim_asset`'s newest object key is `date=2026-09-18` (partition-level date only).

`VERDICT: PASS-MXA2-AC2`

---

## AC3 -- firm/master scope rule per table, key-prefix segment named; tables whose scope cannot be read from the key

**Every Schwab table's scope IS in its key** -- unlike `MX-a-1`'s `etfs`/advisor-intelligence tables (which needed
an exception clause), no exception applies here. Scope rule, MEASURED (AC1's live listing and
`schwab_reader_iam.tf:63-70`'s `schwab_data_prefixes`, printed): the 2nd key segment after `schwab/` is the master
id, one of `08242234` or `08335338` (`data_entitlement.py:63`, `MASTERS`). The 4th segment (after
`schwab/{master}/silver/`) is the table name (`dim_position`, `dim_balance`, `dim_asset`, `dim_transaction`,
or one of the 15/16 `fact_*` names, AC12). So a full key -- e.g.
`schwab/08242234/silver/dim_position/date=2026-09-18/data.parquet` -- carries BOTH the master scope and the table
identity in its own path, with no field-level lookup required. This holds identically for both masters and for
every table this cell measured, so this criterion's "table whose scope cannot be read from its key" clause names
**none** for this property (a measured, not an assumed, empty set -- contrast `MX-a-1`'s two named exceptions).

`VERDICT: PASS-MXA2-AC3`

---

## AC4 -- never-sum rules, each with its reason

1. **Cross-master.** `data_entitlement.py:63` (printed): `MASTERS = ("08242234", "08335338")`. PRD C4: "Masters and
   firms are never summed across, in any phrasing"; FWD-3's ACCEPT (PRD, printed): "one master and one date per
   answer, never summed across masters". Reason: the two masters are two distinct legal/custodial books (research
   record P2, DECLARED not re-verified: "masters 08242234 SmartX, 08335338 BD") -- summing positions, balances or
   transactions across them misstates either book. The SAME rule is independently visible from the mdpf pipeline's
   own docstring (`data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py:23-24`, printed, re-read live this
   run): "Basis: SCHWAB-RPS (Andrew-ruled; account 08242234). NEVER 0833, NEVER a sum, NEVER blended-preferred."
2. **Cross-date (point-in-time, non-additive).** `dim_position` and `dim_balance` are per-`business_date` SNAPSHOTS
   (AC2's grain: one row per account [+cusip/l_s], one partition per calendar day) -- summing `quantity_settled` or
   `mkt_value_long` across two dates for the same account double-counts a STOCK as if it were a FLOW. The engine
   itself enforces one date per query: `query.py:53` (`REQUIRED_PROPERTIES`, printed) names `business_date` as a
   REQUIRED, single-valued query property (not a range) -- the typed-query grammar has no date-range mode at all for
   these three datasets, so "one date per answer" is a call-path fact, not only a written rule.
3. **Non-additive field, and quantities require grouping.** `infra/aws/ec2/opal-gateway/app/integrations/schwab/
   datasets.json`'s `nonadditive_fields_note` (printed): "`closing_price` is deliberately absent from
   `additive_fields` in both the contract and this file: price is nonadditive (PRD C3) so no dataset here permits
   summing it, regardless of type." The same file's `quantity_sum_required_groups: ["cusip", "l_s"]` (printed) means
   a quantity field (`quantity_settled` etc.) is only safely summed WITHIN one (cusip, long/short) group -- summing
   `quantity_settled` across different securities, or netting a long row against a short row of a DIFFERENT
   security, adds unlike units together.
4. **Transaction rows carry no per-row identity, so a blind sum spans accounts.** `schwab_projections.py:52-54`
   (printed, AC2): `dim_transaction` is "per-partition APPEND, NO row-unique key". Its source columns include
   `account_id` (the account) alongside `gross_amount`/`net_amount`/fee fields; summing those fields over an entire
   partition WITHOUT first filtering to one `account_id` sums transaction activity across every account in the
   master for that date, not one client's activity -- the never-sum boundary here is "never aggregate `dim_
   transaction`'s money fields without a stated account filter", a rule the datasets.json contract does not (yet)
   state for `dim_transaction` because that table is not in the contract at all today (AC11).

`VERDICT: PASS-MXA2-AC4`

---

## AC5 -- common questions, numbered, table + fields, source stated

Source discipline: every question below is sourced from (a) the producer/engine code's own declared field set and
grain (`DATASET_SCHEMAS`/`DATASET_GRAINS`, `datasets.json`, `schwab_projections.py`), (b) the research record's
Rung-2 examples (`docs/briefs/opal-mcp-tool-index-scoping-20260917.md@2a7fc3339f:87-90`, printed below, READ AS
RESEARCH per PRD VII.6, never as measured demand), or (c) this seat's reasoning from the datasets' own field shape.
**None is presented as measured user demand** -- this property has no beta usage yet (C8/S11 have not run), and
this cell does not claim otherwise.

Research record Rung-2 text, printed (`:87-90`): "Accounts/positions: find an account, what does it hold today,
how did it change since date X. ... Transactions: activity for an account or master over a date range."

| # | question | table(s) | fields | source |
|---|---|---|---|---|
| 1 | What does account X hold today (or as of date Y)? | `dim_position` | `account_ref`, `cusip`, `l_s`, `quantity_settled_unsettled`, `market_value_settled_unsettled`, `closing_price`, `business_date` | (a) `DATASET_SCHEMAS["dim_position"]`, `query.py:96-108`; (b) research record Rung-2 "what does it hold today" |
| 2 | What is account X's balance / net worth as of date Y? | `dim_balance` | `mkt_value_long`, `mkt_value_short`, `net_mv_positions`, `net_mv_plus_cash`, `cash_balance_settled_only`, `business_date` | (a) `DATASET_SCHEMAS["dim_balance"]`, `query.py:109-119` |
| 3 | What is the total market value of a given security (cusip) held across accounts within a master, as of date Y? | `dim_position` (aggregate, grouped by `cusip`+`l_s`) | `cusip`, `l_s`, `quantity_settled`, `market_value_settled_unsettled` | (c) reasoning from `datasets.json`'s own `quantity_sum_required_groups: ["cusip","l_s"]` -- the contract itself names this as the one safe aggregate shape |
| 4 | Which accounts hold a given security (cusip)? | `dim_position` (filtered by `cusip`) | `account_ref`, `cusip`, `quantity_settled` | (c) reasoning from the grain (`account_ref, cusip, l_s`) |
| 5 | What are a security's reference details (description, product/category code, maturity, rating)? | `dim_asset` | `cusip`, `security_description_line_1..3`, `prod_code`, `prodcatg_code`, `maturity_date`, `s_p_rating`/`moodys_rating` -- **NOTE: `s_p_rating`/`moodys_rating` are pinned in `schwab_projections.py:71-79` but NOT in `DATASET_SCHEMAS["dim_asset"]` (`query.py:120-130`) -- the engine exposes 9 of the 24 pinned columns; the ratings fields are silver-present but not yet servable through this tool.** | (a) `datasets.json` `dim_asset` block; `query.py:120-130` |
| 6 | What transactions occurred for account X on date Y (or "how did it change since date X", the activity half)? | `dim_transaction` | `account_id`, `business_date`/`trade_date`/`settlmnt_date`, `tr_cd`, `transaction_category`, `debit_credit`, `cusip`, `quantity`, `price`, `gross_amount`, `net_amount` | (a) `schwab_projections.py:55-67`, the 39-column pin; (b) research record Rung-2 "activity for an account ... over a date range" |
| 7 | What was the net cash flow (sum of `net_amount`) for account X, per day, over a stated span (one call per date, AC4 #2)? | `dim_transaction` (aggregate, filtered to one `account_id`, one `business_date` per call) | `account_id`, `net_amount`, `business_date` | (c) reasoning; AC4 #4's never-sum-without-account-filter boundary makes this the safe shape |
| 8 | What is the total market value across ALL accounts for master X as of date Y (a firm/master-level rollup, never across masters -- AC4 #1)? | `dim_balance` (aggregate, grouped by nothing beyond the single master/date scope) | `mkt_value_long`, `mkt_value_short`, `net_mv_plus_cash` | (c) reasoning; the additive fields are `datasets.json`'s own `additive_fields["dim_balance"]`, printed |

`VERDICT: PASS-MXA2-AC5`

---

## AC6 -- question -> tool or typed query, with reason

**Assigned to a proposed purpose-built tool (Q1, Q2):** a single-account, single-date lookup ("what does account X
hold", "what is account X's balance") is the property's single most common shape, and the decomposition's own
downstream tool-building cell already names this exact split: `MX-t-2` (decomp s.3, printed) is "Schwab
purpose-built tools for **positions, balances** and transactions" -- positions and balances are named as
purpose-built targets there, distinct from the third (transactions, below). **Reason:** a fixed single-key GET
(account + date in, one table's rows for that account out) is cheap and needs no filter/group-by/aggregate
generality -- the same reasoning `MX-a-1` used for its whole-object portal reads (AC6 there), applied here to a
single-account slice instead of a whole-object slice, since the underlying tables are per-account rows rather than
one small precomputed object.

**Assigned to the typed query (Q3, Q4, Q5, Q6, Q7, Q8):** every question that needs a FILTER other than the
account+date pair (by cusip, grouped by cusip+l_s, an aggregate sum, or an account-filtered transaction scan) is
routed to the typed query rather than a new named tool. **Reason, per table:**
- **Q3, Q4 (`dim_position`, filtered/grouped by cusip):** the existing `schwab_query` tool (5 built tools,
  `integration.py:1-11`, printed) already supports exactly this shape (`query.py`'s filters/group_by/aggregates
  grammar) for `dim_position` today -- there is no gap a new tool would close, and multiplying tools per filter
  combination is the same anti-pattern `MX-a-1`'s AC6 refused for `macro/timeseries/{slug}.json`.
- **Q5 (`dim_asset`):** `MX-t-2`'s own title (decomp s.3) names only "positions, balances and transactions" as its
  purpose-built targets -- `dim_asset` is NOT among them. Reference/security-lookup questions are naturally
  filter-driven (by cusip, by product code), which is exactly the typed query's shape; this cell does not invent a
  fourth purpose-built tool the decomposition's own downstream cell does not plan to build.
- **Q6, Q7 (`dim_transaction`):** the decomposition's OWN cell-specific addition for `MX-t-2` (s.3, printed
  verbatim) already decides this: "`dim_transaction` is queryable through its catalog entry and the typed query
  (`MX-q-1`), and no file under `INT/schwab/` changes." This cell's analysis is consistent with that decision, not
  the source of it -- named here rather than re-derived, per VII.5's discipline against silently re-deciding a
  frozen fact.
- **Q8 (`dim_balance`, master-level rollup):** an aggregate over a single account/date filter set, the same
  filter/group/aggregate shape the typed query already carries for `dim_position`; no per-question tool is
  justified for one more group-by combination on an already-generalized table.

No question above is left to the typed query without the reason stated (JUDGMENT AC10 grades whether the
assignment is well-judged; this criterion is mechanical -- that every question HAS a stated assignment).

`VERDICT: PASS-MXA2-AC6`

---

## AC7 -- proposed tool names pass C3

C3 (PRD, printed): `{system}_{function}[_{qualifier}]`; `system` a key of `infra/logic/registry/systems.json`;
`function` a base-form verb; scope (master) is an explicit ARGUMENT, never folded into the name. `systems.json`
MEASURED (this run, live read): 25 keys; `schwab` is present as `{"key": "schwab", "class": "VENDOR", ...}` (printed
verbatim above in this cell's own read). The 5 EXISTING Schwab tools (`integration.py:1-11`, printed, AC6) already
confirm the pattern by reading: `schwab_get_access`, `schwab_list_files`, `schwab_describe_dataset`, `schwab_query`,
`schwab_prepare_download` -- system `schwab`, functions `get`/`list`/`describe`/`query`/`prepare`.

**Proposed tool set (2 new tools, for Q1/Q2's purpose-built assignment, AC6):**

| tool name | serves | system in systems.json? | function (verb) | collides with an existing `schwab_*` name? |
|---|---|---|---|---|
| `schwab_get_positions(master, business_date)` | Q1 | yes | get | no (existing 5: `get_access`, `list_files`, `describe_dataset`, `query`, `prepare_download`) |
| `schwab_get_balances(master, business_date)` | Q2 | yes | get | no |

Both names match `^[a-z][a-z0-9]*(_[a-z0-9]+)+$`, first segment `schwab` (a live `systems.json` key), second segment
`get` (a base-form verb the property's own existing tools already use), master and date are explicit call
ARGUMENTS never folded into the name -- matching `MX-t-2`'s own acceptance bar ("tool names do not collide with the
five existing `schwab_*` tools, compared by name", decomp s.3, printed). `Q3-Q8` carry NO proposed tool name (AC6)
and are typed-query only, so this cell adds exactly 2 candidate names, both passing C3.

`VERDICT: PASS-MXA2-AC7`

---

## AC8 -- read fence as exact prefixes; exclusions named

**Proposed fence (bucket `opal-data-assets`, per `schwab_reader_iam.tf:42`):**
- `schwab/08242234/silver/dim_position/*`, `schwab/08242234/silver/dim_balance/*`, `schwab/08242234/silver/
  dim_asset/*`, `schwab/08335338/silver/dim_position/*`, `schwab/08335338/silver/dim_balance/*`,
  `schwab/08335338/silver/dim_asset/*` -- IN, the 6 prefixes the DESIRED fence already carries today
  (`schwab_reader_iam.tf:63-70`, `local.schwab_data_prefixes`, printed, AC11).
- `schwab/08242234/silver/dim_transaction/*`, `schwab/08335338/silver/dim_transaction/*` -- **PROPOSED NEW** (2
  prefixes), per FWD-3's ACCEPT ("transactions are reachable") and bound 8 ("the one Schwab change this project may
  make is a fence prefix for `dim_transaction`, generated by `MX-i-1` and applied by `MX-i-3`"). Not yet in the
  DESIRED fence (AC11 -- MEASURED absent).
- `schwab/08242234/meta/complete/*`, `schwab/08335338/meta/complete/*` -- IN, unchanged (the existing catalog-role
  fence, `schwab_reader_iam.tf:71-74`).

**EXCLUDED, each with its reason:**
- All 15 (08242234) / 16 (08335338) `fact_*` prefixes, both masters (AC12's full census) -- EXCLUDED: bound 8
  ("The Schwab integration is read, never edited... The one Schwab change this project may make is a fence prefix
  for `dim_transaction`") authorizes exactly one new table, not the vendor-shaped `fact_*` set; none of the
  `fact_*` tables has a `DATASET_SCHEMAS`/`datasets.json` entry (`query.py:95-131`, printed, AC2), so admitting
  their prefixes without any engine-side schema would grant read access the typed query could not yet serve.
- `schwab/{master}/bronze/*`, `schwab/{master}/_ops/*` (both masters), `schwab/08335338/gold/*` -- EXCLUDED:
  `bronze/` is pre-silver raw extraction (`schwab_projections.py`'s own docstring: "gold stays the one parse-down
  point for anything beyond a select" -- bronze is upstream of even that), `_ops/` is pipeline operational
  bookkeeping (same exclusion class as `MX-a-1`'s `_manifests/`), and `gold/` (08335338 only, MEASURED live,
  AC1's top-level listing) is a further-downstream tier this property's Gateway fence has never read
  (`schwab_reader_iam.tf` names only `bronze`/`silver` conceptually via the `silver/` prefix list; no `gold/`
  statement exists there today).
- **`s3://opal-data-bd/schwab/*` (4,622 objects, 12,100,549,274 bytes, newest
  `schwab/silver/rps/_RETAIN_DECLARED_EXCEPTION_RULE25.txt` 2026-08-18T14:09:06Z) -- EXCLUDED, INDEPENDENTLY
  RE-MEASURED this run (not inherited from row `NFRA_MCPINDEX-W4-S1`, per this cell's issuer context).** Its own
  structure differs from the canonical bucket's: no master-id path segment (`schwab/silver/{acc,rld,rps,trn,uln,
  ult,account_xref,trn_nna}/date=YYYYMMDD/...`, 8-digit un-hyphenated dates back to `date=20240112`, vs the
  canonical `schwab/{master}/silver/{table}/date=YYYY-MM-DD/...` layout, MEASURED both this run), and one file in
  it is literally named `_RETAIN_DECLARED_EXCEPTION_RULE25.txt` (a self-declared retained exception, not read
  further -- out of this cell's `<paths>` grant). Reason for exclusion: this is a DIFFERENT bucket than the one
  `schwab_reader_iam.tf`'s roles and the Gateway's engine read (`opal-data-assets`, not `opal-data-bd`), it is
  Black Diamond's own bucket (`data/black_diamond/scripts/silver/merge-daily-incremental.py:53` reads
  `opal-data-bd`, per row `NFRA_MCPINDEX-W4-S1`), and its key layout does not match anything the Schwab engine's
  `catalog.py`/`engine.py` are built to parse -- admitting it would require new engine work, out of bound 8's
  read-only-integration scope, and this cell's own live measurement corroborates the peer row's count exactly
  (4,622 / 12,100,549,274) while adding the structural detail (legacy layout, retain-exception marker) that
  explains WHY it is excluded rather than merely noting that it exists.

`VERDICT: PASS-MXA2-AC8`

---

## AC9 -- a property with no data says so and proposes no tool

MEASURED (AC1): all 8 (2 masters x 4 tables) have live, non-empty data at this cell's run time (554-673 objects
each, none zero). MEASURED (AC12): all 15/16 `fact_*` tables per master also carry live, non-empty data (the
smallest, `fact_rlu`/`fact_rtu`, still carries 13-15 objects, never zero). **No sub-table checked in this analysis
was found empty.** This criterion is therefore satisfied VACUOUSLY for `MX-a-2` as a whole: there is no empty
property or empty table here to name, and this cell proposes no tool for zero properties.

`VERDICT: PASS-MXA2-AC9`

---

## AC10 -- JUDGMENT

Graded by `3.0.0_SA_CVO` at L9. Record UNVERIFIABLE-BY-INSTRUMENT; status_reason: "graded by 3.0.0_SA_CVO at L9,
per this order's own text". No verdict recorded here.

---

## AC11 -- `dim_transaction` columns; fence admission, DESIRED and APPLIED

**Columns, MEASURED at the pin** (`data/assets/scripts/silver/schwab_projections.py:55-67`, printed verbatim):
```
"dim_transaction": ("TRN", 1, (
    "account_id", "business_date", "trade_date", "settlmnt_date", "tran_date",
    "tr_cd", "sb_cd", "transaction_category", "tran_srcde",
    "transaction_source_code_description", "transaction_detail_description",
    "debit_credit",
    "cusip", "ticker_symbol", "industry_ticker_symbol", "isin", "sedol", "tax_code",
    "quantity", "price", "gross_amount", "net_amount", "accrued_interest",
    "commission", "prime_broker_fee", "trade_away_fee", "redemption_fee",
    "other_fee", "step_in_fee", "research_fee", "exec_brok_comm",
    "broker_service_fee", "exchange_processing_fee",
    "federal_tefra_withholding", "state_tax_withholding",
    "retirement_fed_income_tax", "retirement_state_income_tax",
    "closing_price", "factor",
)),
```
**39 pinned columns** (counted from the tuple above). The live parquet (newest partition, both masters, MEASURED
via `pyarrow.parquet.read_table`) carries **44 columns**: the 39 pinned + 5 provenance columns
(`_source_file`, `_source_as_of`, `_master_observed`, `_section`, `_schema_version`), confirming the pin against
the served bytes (39 + 5 = 44, matches `t.num_columns` measured for both `08242234_dim_transaction.parquet` and
`08335338_dim_transaction.parquet`).

**DESIRED -- does the Schwab reader role's fence admit `dim_transaction`'s prefix?** MEASURED, live re-read of
`infra/aws/terraform/opal-gateway/schwab_reader_iam.tf:63-70` (`local.schwab_data_prefixes`, printed):
```
schwab_data_prefixes = [
  "schwab/08242234/silver/dim_position/", "schwab/08242234/silver/dim_balance/", "schwab/08242234/silver/dim_asset/",
  "schwab/08335338/silver/dim_position/", "schwab/08335338/silver/dim_balance/", "schwab/08335338/silver/dim_asset/",
]
```
**No entry for `dim_transaction`, either master. The DESIRED fence does NOT admit `dim_transaction`'s prefix today**
(6 of 6 listed prefixes are `dim_position`/`dim_balance`/`dim_asset` only; a `git diff`-free re-read at this
worktree's HEAD, no local edits to this file -- this cell's `<paths>` grant does not include it and none were
made).

**APPLIED -- MX-p-1's live read:** `MX-p-1` (the live Gateway/IAM baseline reader) has NOT run yet (this cell's
issuer context, stated verbatim). **This half is recorded ABSENT, not substituted with this cell's own reading of
Terraform DESIRED state or a live IAM simulate-policy call** -- Rule 22a's STATE axis (DESIRED != APPLIED !=
EXERCISED) binds: a Terraform file states intent, never deployed reality, and this cell's `<paths>` grant carries
no IAM-read instrument of its own to stand in for `MX-p-1`. **APPLIED: ABSENT (MX-p-1 has not run).**

`VERDICT: PASS-MXA2-AC11`

---

## AC12 -- the 16 full Schwab tables the research record names, censused, each marked in/out with reason

**Research record citation** (`docs/briefs/opal-mcp-tool-index-scoping-20260917.md@2a7fc3339f:61`, printed,
READ AS RESEARCH): "P2 | Schwab (masters 08242234 SmartX, 08335338 BD) | `opal-data-assets/schwab/{master}/silver/`
-- 16 full tables + `dim_position/transaction/asset/balance` |".

**Census, MEASURED live** (`s3api list-objects-v2 --prefix "schwab/{master}/silver/fact_"`, per-key `Key.split('/')
[3]` grouping, both masters, this run):

| feed (SPECS key, `schwab_schemas.py`) | `fact_*` folder | 08242234 (SmartX) objects | 08335338 (BD) objects |
|---|---|---:|---:|
| ACC | `fact_acc` | 673 | 554 |
| RLD | `fact_rld` | 923 | 802 |
| RLU | `fact_rlu` | 15 | 13 |
| RLW | `fact_rlw` | 49 | absent |
| RLY | `fact_rly` | 44 | 38 |
| RPS (section 1) | `fact_rps` | 582 | 554 |
| RPS (section 2) | `fact_rps_s2` | 582 | 554 |
| RTU | `fact_rtu` | 15 | 13 |
| RTY | `fact_rty` | 44 | 38 |
| SEC | `fact_sec` | 673 | 554 |
| TRN | `fact_trn` | 673 | 554 |
| ULN | `fact_uln` | 674 | 554 |
| ULT | `fact_ult` | 674 | 554 |
| UPN | `fact_upn` | 674 | 554 |
| UPT | `fact_upt` | 674 | 554 |
| FAM | `fact_fam` | absent | 526 |
| SLM | `fact_slm` | absent | 550 |

**Denominator: 17** (`schwab_schemas.py`'s `SPECS` dict, MEASURED live via `comp-read --enumerate`, 17
`(feed, section)` keys at lines 71-1161, printed). **Per-master physical `fact_*` folder count: 08242234 (SmartX)
carries 15 (has `RLW`, lacks `FAM`/`SLM`); 08335338 (BD) carries EXACTLY 16 (has `FAM`/`SLM`, lacks `RLW`) --
matching the research record's "16 full tables" figure EXACTLY for master 08335338, and by exactly one table
(15 vs 16) for master 08242234.** This is a MEASURED, precise reconciliation of the research record's number, not
an assumption that "16" applies uniformly to both masters. The schema's own docstring
(`schwab_schemas.py:8-12`, printed) explains the asymmetry: `RLW` is "0824-ONLY type"; `FAM`/`SLM` use "CS grammar"
and are implicitly 0833-side by the same measured-vintage note.

**Each table marked in/out of this round's tool set, with reason:**
- **`dim_position`, `dim_balance`, `dim_asset` -- IN (already).** Exposed today via `DATASET_SCHEMAS`/`datasets.json`
  and the 5 existing `schwab_*` tools (AC1-AC7).
- **`dim_transaction` -- IN, proposed this round.** Per AC6/AC8/AC11: exposed via the typed query (`MX-q-1`), fence
  prefix added by `MX-i-1`/`MX-i-3` (bound 8).
- **All 15 (08242234) / 16 (08335338) `fact_*` tables above -- OUT, this round.** Reason (uniform across all of
  them, AC8): none has a `DATASET_SCHEMAS`/`datasets.json` entry, none is named in bound 8's single authorized
  Schwab change (the one `dim_transaction` fence prefix), and exposing a vendor-shaped `fact_*` table as a tool
  would require NEW engine/catalog work this project's bound 8 does not authorize ("The Schwab integration is
  read, never edited"). No table among the 17 (feed, section) types is treated differently from another -- the
  exclusion reason is the same contract gap for all of them, stated once here rather than repeated 17 times.
- **`opal-data-bd`'s `schwab/*` (a further, structurally distinct copy) -- OUT, this round.** Reason: AC8,
  independently re-measured (different bucket, different key layout, not read by the Gateway's engine or fence).

`VERDICT: PASS-MXA2-AC12`
