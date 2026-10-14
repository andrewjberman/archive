# NFRA_MCPINDEX round 10 -- the issuer's drain-end packet for L8/L9 (2.0.0_SA_COO~MI, 2026-10-14 ~00:1xZ)

Addressed to `3.0.0_SA_CVO~Z`.
- **Source:** `ledger/CTO_RULING_ROUND10_Z4_ONE_SHORT_ROUND_20261013.md` (msg 33704), on PRD v0.9 @e581c26ab4 ADMITTED.
  This is direction Z4, one short round. Issuance @0fa3174d89: 2 cells, fan-out 1 of 1 chains.
- **State:** 2 of 2 orders are COMPLETE and drained. `round-close-check.py --round 10` reads 2 complete, proof_ok 2,
  verdict MAY-CLOSE.
  - Under standing clause 2, read that verdict beside the suite's 12 known failures: the 5 from Z-S97 and the 7
    base-failing IDs from Z-S107.
- **No judgment criterion: every check is mechanical.** Section 3 asks for the plausibility read, including your carried
  note: is each member classified from its definition?

## 1. Orders -- graded on box/sitez (issuer re-run after each drain)

| order | FWD | status | mechanical (issuer re-grade) |
|---|---|---|---|
| MX-c-8 catalog writer | FWD-20, FWD-21 | complete, drained @212f2370a3. Re-opened by A1 and drained again @972e25715e | c8.AC1 partition a=11 b=44 c=12, sum 67 of N=67, definitions located 67 of 67; c8.AC2 16 of 16 harvest prefixes, 0 WITHHOLD rows; c8.AC3 discover 3 of 3; proof VALID |
| MX-r-11 release | FWD-20, FWD-21 live | complete. Ledger `nfra-mcpindex-r10-catalog-release` CLOSED on 5 legs @598047ef2f | v1 `ad2acc0a93` on base `64b3e54658`, then a v2 fix-forward `7eff14b2e6` (catalog only, 5 lines). Issuer's live re-run: r11.AC1 PASS (14 of 14 sentinels); r11.AC2 PASS (ssm b7d0e9cb: /health 200, partition 67 of 67, definitions 67 of 67, discover 3 of 3); r11.AC3 PASS (etfs_get_positioning freshness AGREE, depth absent CONFIRMED). Halves: v1 COO @a5587c3dbe + CTO @98ce8d9ff1; v2 COO @25fc8b5aaa + CTO @62e8f7d19f |

## 2. The one real run of each outcome, 2026-10-14 ~00:0xZ, through this seat's opalgateway session (served host `7eff14b2e6`)

- **FWD-21:**
  - "harvested news articles and chatter": catalogued, 5 matches, all on channel `harvest_datasets`
    (`article_security_mention`, `article_sentiment`, `chatter_daily`, `chatter_event`, `chatter_window`). Each says
    `servable: false`, `next_tool: null`, `gap.owner: NFRA_OPLGTW`.
  - "security analysis research pack": catalogued, 1 match, `harvest_packs`, with the same gap.
  - Schwab control "Schwab account positions": catalogued, 8 matches, 3 servable silver datasets (unchanged).
  - **Before the round both harvest subjects read `catalogued: false`.**
- **FWD-20:** the live partition, read on the host in-process under its own venv and `.env` (r11.AC2): N=67 served tools,
  a=11 name their index, b=44 read data with no index yet, c=12 are not data reads. 67 of 67 definitions are located in
  the deployed tree. At the base, 10 of 67 tools had an index link and 0 carried depth or freshness.

## 3. What L9 is asked to judge (no criterion holds it; this is the plausibility read)

- **FWD-20 depth:** `history_depth` reads `absent` on 11 of 11 (a) tools, each with a reason. Every served portal object
  is one overwritten file with no dated key, and every silver row is live-queried (row Z-W33-S1). DONE WHEN asks for
  the "earliest served date"; ACCEPT admits "absent is said, never blank". Does absent-on-all REALIZE FWD-20, or is
  that a NOT_REALIZED needing dated history (object versions or dated keys) that no portal producer keeps today?
- **FWD-20 classification by definition (your carried note):**
  - The 12 (c) members, each with its definition line, are listed in worker ~33's report and in
    `workflows/atom_decomposition/tool_index/members.yaml`.
  - Row Z-W33-S2 records the calls the order's table did not settle:
    - `gateway_query_catalog` and `opal_asker_query` are (a) with entity `mp.04.model-portfolio-timeseries`;
    - `opal_discover` and `opal_describe` are (b), owner NFRA_MCPINDEX;
    - `whoami` is (b);
    - `graph_status` and `ycharts_freshness` are (c).
  - Please read a sample of (c) and of the Z-W33-S2 calls against their definitions.
- **FWD-21:** the rows route; nobody can READ them yet (`read_tool: null`, gap NFRA_OPLGTW). That matches FWD-21's
  DONE WHEN, which is the discover route. The asset-manager read is direction Z5, NFRA_OPLGTW's next round.

## 4. Rows this round, and the issuer's rulings

| row | class / standing | ruled by |
|---|---|---|
| Z-W33-S1 depth not listable; Z-W33-S2 classification calls; Z-W33-S5 naming gate refuses typed platinum prefixes; Z-W33-S6 plane 2 stale at PHASE A | OBSERVATION/INERT | carried to L10 (section 5) |
| Z-W33-S3 `entity` collision (tool_index repeats row ids) | OBSERVATION/ARMED | Z-S106: INERT (no app reader keys entity over the whole file) |
| Z-W33-S4 suite baseline stale (7 base failures) | OBSERVATION/ARMED | Z-S107: INERT (carried as known under clause 2) |
| Z-S105 Andrew's call 8: all 24 harvest prefixes SERVE (list v4) | OBSERVATION/INERT | drained AS CUT on v3 (CTO msg 33732); the 13 added prefixes are round 11 |
| Z-S108 first deploy attempt failed (sparse cone lacked `infra/logic/registry`); Z-S111 it is a recurrence of MX-r-10's | OBSERVATION/INERT | carried to L10 |
| Z-S109 ANNOUNCE cited box/sitez's deploy-script blob, not the base's | OBSERVATION/INERT | carried to L10 |
| Z-S110 r11.AC2 definitions 65 of 67 on v1 | BLOCKING/ARMED | Z-S112: NOT met, fix forward (v1 serving, rollback refused on measured outcomes); Z-S113: DISARMED on v2 67 of 67 |

## 5. Carried to the round-10 L10 slug (enrichment candidates)

1. **The harvest widening** (Z-S105): 13 more prefixes under list v4 @7e0da2dfee; Andrew's call 8.
2. **The asset-manager reader and grant** (direction Z5): NFRA_OPLGTW. Every harvest row names it as `gap_owner`.
3. **FWD-20 depth:** whether a dated history is wanted for the portal objects (a producer question), or absent stands.
4. **Deploy recipe** (Z-S108/Z-S111/Z-S109): the gateway deploy cone must carry `infra/logic/registry`, and the
   script's `_pf_need` pre-check must read one registry JSON, not only stat `lib/opal_naming.py`. Owner: whoever owns
   `deploy-to-ec2.sh` (the wrapper fix was ruled `2.0.0_SA_COO~O`'s in round 8). It recurred on all three MCPINDEX
   releases.
5. **Instrument lesson** (Z-S112): a census of definitions reads the tree AS SHIPPED. `tool_census.py --overlay-ref`
   now exists.
6. **Suite:** re-baseline `failing_ids_full.txt`. The six route/OIDC tests (404 vs 405) belong to the gateway routes'
   owner (Z-S107).
7. **A durable link key** for tool_index that is not the row identity (Z-S106).
