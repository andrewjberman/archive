# MDPF_REMED.RP-F2 — predicate-derived census: every consumer of eclipse/orion run-date partitions

**Assignee:** 0.8.0_AE_CloudComp · **Issued:** 2.0.0_SA_COO 2026-08-11T00:4xZ (CTO ruling 004403Z: census-first, predicate-not-roster) · **Executed:** 2026-08-18 ~1630–1700Z
**A CENSUS, NOT A FIX — zero code changes.** Repo vintage: HEAD `c29e2aa310` (+W1 pin reads at `bf74d031c1`). Live S3/graph reads 2026-08-18.

---

## 1. THE PREDICATE (stated, re-runnable)

A **consumer** is any HEAD-tracked executable/config file that reads (or declares a read grant on) a key in the run-date-labeled eclipse/orion family set **F**, where F was grounded on the LIVE tree (not assumed):

**F0 — vendor `date=` partitions (the RP-W1 subject):** `s3://opal-data-assets/eclipse/inflection/{bronze,silver,reconstructed}/…` (silver: fact_model_composition, fact_models, fact_portfolios_full, fact_portfolios_simple, each `date=D/`) · `s3://opal-data-assets/orion/inflection/{bronze,silver}/…` (silver: fact_assets, fact_performance, fact_positions, fact_transactions) — enumerated live via list_objects_v2 delimiter walks.
**F1 — derived run-date-labeled families:** `s3://opal-data-inf/silver/eclipse/{D}/…` (run-date keyed, 4 parquet + sentinel) · `s3://opal-data-inf/gold/eclipse/{D}/…` (INF_E_00 output, label = eclipse silver run-date) · `s3://opal-data-mdpf/mdpf/bronze/orion_model_composition/{D}/…` · `eclipse/inflection/reconstructed/vintage={V}/`.
**F2 — feeds carrying the inherited label:** `s3://opal-data-mdpf/mdpf/feeds/{artifact}/{firm}/{date}.parquet` — inflection legs only (49financial legs derive from smartx/rps, out of the eclipse/orion class).

**Scan predicate P = P1 ∪ P2 ∪ P3:**
- **P1 (literal):** regex `(eclipse/inflection|orion/inflection|silver/eclipse|gold/eclipse|ECLIPSE_SILVER|ORION_SILVER|SILVER_ECLIPSE_PREFIX|GOLD_ECLIPSE_PREFIX|model_feed_prefix|custody_feed_prefix)` over every HEAD-tracked `.py .sh .ts .js .mjs .yaml .yml .json .tf` outside `org/ docs/ memory/ rcg/ .scratch* */tests/ test_*`.
- **P2 (derived-family extension):** regex `(mdpf/feeds|orion_model_composition|MDPF_FEEDS_PREFIX|FEEDER_PREFIX|eclipse/inflection/reconstructed|reconstructed/vintage=)` over the same universe. *(P2 exists because the validity gate demanded it: `mdpf_aggregate_aua` touches no F0 token — it reads the feeder's F2 keys. The predicate was extended, not the list.)*
- **P3 (graph):** comp-kuzu `MATCH (a:CloudNode)-[r:CloudEdge]->(b) WHERE node_id CONTAINS 'eclipse'/'orion/'` — corroboration + IAM/trigger edges.

**Stage-1 localization (comp-find, denominators native):** `eclipse/inflection` 627 hits/26,505 files (HEAD-band 310) · `orion/inflection` 7,501/26,505 (HEAD 7,045 — dominated by two scratch listing files) · `silver/eclipse` 224 (HEAD 50) · `gold/eclipse` 176 (HEAD 43). **Stage-2 drill-in (scripted, rail-checked):** P1 → **43 hit files** of **5,645 scanned** (of 25,204 git-tracked); P2 → **34 hit files** of the same 5,645. **P3:** kuzu 20,685 nodes / 41,306 edges, built 2026-08-18T16:03Z (provenance header read: Nessie HEAD current; graph_nodes cohort < 6h).

## 2. POSITIVE CONTROLS — all 4 known members (5 files) surfaced INDEPENDENTLY

| Known member | Surfaced by | Where |
|---|---|---|
| dim_mdpf_aggregate_aua_timeseries | P1 | `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py:439,456,476,528,545` |
| build_mdpf_wsc_inflection_feeder | P1 (+P2) | `data/mdpf/scripts/gold/build_mdpf_wsc_inflection_feeder.py:67-68,167-186,250-251` |
| mdpf_aggregate_aua | **P2** (F2 feeds — the extension the gate forced) | `data/mdpf/scripts/gold/mdpf_aggregate_aua.py:66,240-241` |
| dim_mdpf_account_distribution | P1 | `data/mdpf/scripts/gold/dim_mdpf_account_distribution.py:75,264-299` |
| wsc_inflection_held_etf | P1 | `data/mdpf/scripts/feeders/wsc_inflection_held_etf.py:24,97,169` |

**VALIDITY GATE: PASS.**

## 3. CONSUMER ROWS (file:line @ HEAD c29e2aa310 · vendor · key family · OFFSET STATE)

### 3a — Readers that INTERPRET the label (the offset-relevant set)
| # | Consumer | Vendor / family | Offset state | Evidence |
|---|---|---|---|---|
| 1 | `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py:416-545` | eclipse fact_portfolios_full + orion fact_assets + reconstructed (F0) | **CORRECTED-BY-W1** | `_vendor_label_of()/_partitions_by_label()` @bf74d031c1; **deployed too**: mdpf-gold-lambda BUILD_MANIFEST vintage 84c1fc08fd, member == HEAD (NFRA_DEPLOYCENSUS row, CURRENT) |
| 2 | `data/mdpf/scripts/gold/dim_mdpf_account_distribution.py:264-299` | eclipse fact_portfolios_full (F0) | **UNCORRECTED** | `pdate = _latest_date(...)`; period stamped = raw partition label (`:299` src records `date={pdate}`); no `_vendor_label_of`; deployed == HEAD (so deployed uncorrected too) |
| 3 | `data/mdpf/scripts/feeders/wsc_inflection_held_etf.py:158-284` | orion fact_assets (F0) | **UNCORRECTED (with explicit date-split caveat)** | carries `rps_date_used`/`positions_date` separately from `as_of` + logs roll-forward (contract §3.4) — honest about WHICH partition, but "positions valued {positions_date}" reads a RUN-date as a valuation date; no T-1 normalization |
| 4 | `data/mdpf/scripts/gold/build_mdpf_wsc_inflection_feeder.py:154-187,250-251,493-531` | inf gold/eclipse + silver/eclipse (F1) + orion_model_composition bronze (F1) | **UNCORRECTED** | `date_iso = args.date or utcnow()`; feeds stamped `as_of_date = date_iso` (run date) while sources carry T-1 close; gold/silver vintages logged (`:522`) but not applied to the stamp |
| 5 | `data/mdpf/scripts/gold/mdpf_aggregate_aua.py:240-241` | mdpf/feeds inflection legs (F2) | **INHERITED (uncorrected upstream)** | reads `as_of_date` stamps faithfully; the label defect sits at row 4's stamp — fixing here would be the wrong layer |
| 6 | `data/inf/scripts/gold/INF_E_00.eclipse_model_portfolios.py:88,350-378` | inf silver/eclipse/{D} (F1) | **UNCORRECTED** | `eclipse_date = _latest_eclipse_silver_date()` (a RUN date); `data_as_of = eclipse_date` stamped into all 3 gold artifacts + partition key — the run-date label PROPAGATES into gold/eclipse/{D} (which rows 4 and 11 then read) |
| 7 | `infra/aws/lambda/opal-assets/opal-assets-daily-emitter/channel_sources.py:243-262,368,388,421` | orion fact_assets + eclipse fact_portfolios_full (F0) | **UNCORRECTED** (freshness-gated only) | the T-1 acceptance rule (`accept latest partition <= run_date`) is a FRESHNESS gate; `"as_of": date` emits the accepted RUN-date label as the data date on the orion (`:368`) and eclipse (`:421`) legs |
| 8 | `infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/lambda_function.py:78,204` | orion fact_positions (F0) | **UNCORRECTED at HEAD; INERT at deployed** | `source_as_of = day` = the partition key (AC7) = a run date; the monolith read is committed-not-applied (CTO F2 @001a73530a; deployed env carries no FACT_POSITIONS_PREFIX — NFRA_DEPLOYCENSUS) — arms on next deploy |
| 9 | `data/smartx/scripts/generate_smartx_timeseries_and_metrics.py:87-88,448-466` (+ bundled `infra/aws/lambda/smartx_ingestion_pipeline/` copy) | mdpf/feeds (F2) | **INHERITED** | `as_of = max(as_of_date)` across feeds — faithful read of upstream stamps |
| 10 | `data/smartx/scripts/compute_account_distribution.py:63-67` + `compute_per_firm_account_distribution.py:52-57` (+ lambda copies) | mdpf/feeds model_aua_positions (F2) | **INHERITED** | re-pointed off gold/eclipse to feeds (`:51-52` records the move) |
| 11 | `infra/aws/ec2/smartx-exporter/smartx-workspace/scripts/compute_per_firm_account_distribution.py:44,218-235` | inf gold/eclipse DIRECT (F1) | **UNCORRECTED + TWO-HOMES ECHO** | the smartx-exporter WORKSPACE copy still carries the LIVE legacy `gold/eclipse` read path (walks partitions, reads gold_complete + model_portfolio_accounts) while its canonical siblings (row 10) moved to feeds — one logical computer, three repo homes, one still on the old family |

### 3b — Label-agnostic / by-construction rows (n-a-with-reason)
| Consumer | Reason |
|---|---|
| `infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:284` | sentinel EXISTENCE wait on `gold/eclipse/{RUN_DATE}/_meta/gold_complete.json` — gate, not a data-date interpretation (keyed consistently with the producer's run-date convention) |
| `data/etfs/scripts/dedup/inflection_silver_retro_dedup.py:69-70` + `run_full_sweep.py` | dedup over orion fact_positions partitions — label-agnostic row-identity work; writes only `orion/inflection/meta/dedup/` |
| `data/mdpf/scripts/gold/mdpf_revamp_count_source_audit.py:51` · `data/mdpf/scripts/feeders/verify_wsd2_clears_identity2.py:32-37` · `.claude/skills/mdpf-refresh/mdpf_refresh.py:243-244` | audit/verify/ops instruments — measure presence/counts, do not stamp data dates |
| Backfills/one-shots: `eclipse_vintage_reconstruction.py` (reconstructed writer — W1's own EVR input, vintage-explicit), `orion_0806_fact_assets_backfill.py` (surgical, single named partition), `build_legacy_compat_emit.py`, `build_mdpf_process_backfill.py`, `patch_mdpf_per_date_partitions.py`, `build_mdpf_inflection_history_from_spine.py`, `build_mdpf_wsc_inflection_nonmodel_backfill.py` | one-shot/backfill: each reads NAMED historical partitions deliberately; vintage semantics are the script's explicit subject, not an implicit assumption |
| WRITERS (label origin, not consumers): `data/assets/scripts/silver/mirror_conversion.py` + its 4 Lambda bundled copies (opal-assets-silver-{orion,eclipse,etf,blackdiamond}), `opal-assets-ingest-mirror`, `data/inf/scripts/silver/convert_eclipse_portfolios_to_silver.py`, `data/mdpf/scripts/bronze/pull_orion_model_composition.py`, inf-api-eclipse | bronze/silver mirrors key by ingest/run date BY DESIGN (bronze is raw); W1's design puts the offset at the CONSUMER, so a writer is the label's origin, not an offset defect |
| 49financial-leg feeders: `wsb_49f_smartx_model_aua.py`, `wsd_partner_held_etf.py`, `build_mdpf_wsd2_etf_netassets_feeder.py`, `build_mdpf_wse_49f_non_model_aua.py` (+ Lambda copies) | feed writers from smartx/rps sources — outside the eclipse/orion class (schwab/blackdiamond labels ruled accurate, W1 negative control) |
| Config/IAM carriers (corroborating, not consumers): `data/mdpf/config/partner_roster.json:184,212` (+ publisher bundled copy), `route_bindings.yaml:109-115`, `data/served_freshness_config.yaml:76-98`, `data/_contracts/vendor_asof_registry.yaml`, `infra/aws/terraform/mdpf-pipeline/iam.tf:294-449`, `opal-assets/emitter.tf:122-141`, `silver.tf`, `monolith.tf`, `wp5-feeder-schedules.tf`, `inf-pipeline/inf-etf-ownership-daily.tf` | declare prefixes/grants/cadences; the executable rows above are their consumers |

### 3c — The 08-08 VintageContradiction 4-link chain (named member, rowed)
`build_mdpf_wsc_inflection_feeder` (row 4, stamps run-date) → `mdpf/feeds/*/inflection/{date}` (F2) → `mdpf_aggregate_aua` (row 5, inherits) → `dim_mdpf_aggregate_aua_timeseries` (row 1, NOW corrected — the W1 fix sits at the chain's END; links 1–3 still carry run-date stamps upstream of it, which is why "W1 complete" must not be read as "the label defect is closed" — the TO's own consequence line, now with the chain's offset states measured).

## 4. SUMMARY
**Offset-relevant consumers: 11 rows** — corrected-by-W1 **1** · uncorrected **6** (rows 2,3,4,6,7,11; row 8 uncorrected-at-HEAD/inert-deployed) · inherited **3** (rows 5,9,10 — remedy belongs at row 4's stamp, not at them). n-a-with-reason: **~25 files** across 6 classes (3b). The census DENOMINATOR frame: 5,645 executable/config files scanned (of 25,204 tracked), 43 P1 + 34 P2 hit files triaged to the rows above; kuzu pass corroborated and added zero unrowed consumers.

## 5. DECLARED COVERAGE BOUNDS (what the predicate cannot see)
1. **Runtime-config-constructed keys:** a key whose family root arrives from a value NOT in the repo (live-only env var, DynamoDB config row) is invisible to P1/P2. Mitigations applied: TF env blocks scanned (caught inf-etf-ownership's env-shaped prefixes), config carriers (.json/.yaml) scanned (caught partner_roster/route_bindings), kuzu IAM edges swept (P3). Residual: a live-only construction would surface only in CloudTrail-grade observation — out of this census's read.
2. **f-string vendor iteration:** `f"{vendor}/…"` with vendor from a runtime list — P1 catches the estate's known instances via their config carriers (partner_roster feeds channel_sources; TREE-checked), but the class is declared, not proven-empty.
3. **Excluded bands:** org/, docs/, memory/, rcg/, .scratch*, tests — records/fixtures, not consumers (deliberate; a consumer living only in a doc would be a doc, not a consumer).
4. **Graph staleness instance found:** kuzu carries `opal-data-mdpf/silver/eclipse/{*}` + `gold/eclipse/{*}` template nodes — **both prefixes are EMPTY on the live bucket** (list_objects_v2, 0 CommonPrefixes). Graph-vs-live discrepancy named per Rule 21 (comp-estate/graph topology = prior under test); the census keyed on the live tree.
5. **Deployed-vs-HEAD skew:** rows are HEAD reads; deployed state is cited where load-bearing (rows 1, 2, 8, 11) from NFRA_DEPLOYCENSUS's same-day package reads rather than re-derived.

## 6. Discipline
Zero code changes. Reads: git/comp-find/comp-kuzu/list_objects_v2/get_object only. No touch of data/mdpf gold files. Remedy scoping is CTO/COO's, off this table — the obvious shape (stated, not acted): the uncorrected set splits into ONE stamp-origin fix (row 4) that discharges rows 5/9/10 by inheritance, the INF-tree convention question (row 6 — whether gold/eclipse labels SHOULD normalize or the tree declares run-date keying as its contract), and three independent leaf fixes (rows 2, 3, 7) + one retire-or-converge (row 11).
