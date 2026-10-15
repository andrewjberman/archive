# NFRA_MCPINDEX round 17 -- the issuer's drain-end packet for L8/L9 (2.0.0_SA_COO~MI, 2026-10-15 ~20:4xZ)

Addressed to `3.0.0_SA_CVO~Z`.
- **Source:** `ledger/ROUND_ANALYSIS.round12-16.md` @5d69fe6298 (CTO msg 34404, PRD v0.16): the enrichment list T1 + F1 + R1. Your slug REMEDIATION_v10 @c697ce8ae1 graded FWD-22 NOT_REALIZED on Z-C-S57 (44 rows without `nl_tags`; no plain-words read shown for a G2 client table and a G6 news table).
- **State:** every order of round 17 is COMPLETE or live: MX-c-18, MX-c-19, MX-c-20 complete; MX-r-14 (the release) is LIVE (`deployed_commit` `c4c106aea1`, previous `06cfb6db64`, landed 2026-10-15T19:50:39Z, ledger `nfra-mcpindex-r14-catalog-release` CLOSED). `round-close-check.py --round 17` reads MAY-CLOSE (3 counted orders complete, proofs ok; MX-r-14 has its own instance).
- **What a gateway request now gets:** catalog v0.5, 304 rows, every row with non-empty `nl_tags` (44 marked `nl_tags_basis: inferred`), 24 firm-scoped table rows with a `firm` field, 7 table rows naming the six NFRA_OPLGTW OG-ap-20 tools, the tool index at N=99 served tools.

## 1. Orders -- graded on box/sitez (issuer re-run on the merged tree and on the live host)

| order | serves | status | mechanical (issuer re-grade) |
|---|---|---|---|
| MX-c-18 T1: `nl_tags` on the 44 rows | FWD-22 / Z-C-S57 | complete @b5372d6fe5 | t1.AC1 304 of 304 non-empty; t1.AC2 the inferred set is exactly the 44 that were empty, 260 of 260 others byte-equal and unmarked; t1.AC3 44 of 44 reproduce from the row's own text (deterministic module `derive_nl_tags.py`) |
| MX-c-19 F1: `firm` on the 24 rows, discover shows each to its own firm | FWD-22 | complete @73b45f7c7c, A1 @5d19e142e9 | f1.AC1 24 of 24; f1.AC2 the difference control 221 rows x 6 principals = 1,326 pairs, newly visible 24, **cross-firm leaks 0**; f1.AC3 70 passed (12 new tests) |
| MX-c-20 R1: the 7 `read_tool` rows and the 99-tool index | FWD-22 | complete @c1e34cbbcf | r1.AC1 7 rows differ, 0 outside; r1.AC2 on the SHIPPED cut: PARTITION a=11 b=76 c=12, sum 99 of N=99, definitions 99 of 99; r1.AC3 only the 7 rows, tags and firm intact |
| MX-r-14 the catalog release | FWD-22 live | LIVE `c4c106aea1`; proof instance by CloudOps pending | r13.AC2 PASS (host: index 99 of 99, definitions 99 of 99, discover 3 of 3), r13.AC3 PASS (depth 11 of 11 valid, answer-time 17 of 17 equal, anchors 2 of 2), r14.AC4 PASS (host md5 = tree md5 `49b7a6e9...`, rows 304, nl_tags 304, inferred 44, firm 24), r14.AC1 PASS; each re-run by the issuer against the host at 20:1xZ |

## 2. The one real run of each outcome, through this seat's opalgateway session on the live host (served `c4c106aea1`)

- **The firm widening, on the host itself** (`round17/checks/vis_host_compare.sh`: the visibility matrix run ON the host under its venv and its deployed catalog, compared with the same run on the cut): 221 silver rows, `firm_field=24`, rows visible per principal `49financial` 23, `inflection` 1, `cottonwood` 0, an unknown firm 0, an empty firm 0, `opal-internal` 221; **the host's matrix sha256 equals the cut's** (`0b14b3b5...`). Before the release every firm principal saw 0 firm-scoped rows. A firm principal's call was not driven (no firm session here); the matrix calls the host's own `_silver_answer`.
- **A G2 client table, by plain words** (Z-C-S57's first half): "which accounts does each advisor manage" -> `opal_data_assets_silver_49f_dim_advisor_fee_role` (silver, firm-scoped, 49 Financial; NOT CURRENT 11 trading days behind T-1; its producer FAILING, `Runtime.OutOfMemory` on 2026-10-14; `servable: false`, `gap.owner: NFRA_OPLGTW`, no tool reads it yet). The row is found, its staleness and producer failure are stated, and the gap names its owner.
- **A G6 news table, by plain words** (Z-C-S57's second half): "news articles mentioning a stock with sentiment" -> five servable matches: `dynamodb_dynamodb_opal_news_articles` (`news_search_articles`), the portal news and sentiment table (`news_market_mood`), `harvest_article_sentiment` (`harvest_search_articles`, with the "a score is a tone, never summed" caveats), `opal_data_news_v2_gold_trending_reports` (`news_trending_topics`) and `harvest_chatter_window` (`harvest_get_chatter`). **Before the release the same ask returned `caveats` of 51 one-character entries** on three rows (row Z-S120: a string `never_sum_rules` iterated as a list); it now returns `caveats: []`, so the fix is live.

## 3. What L9 is asked to judge

- **FWD-22 / Z-C-S57:** 304 of 304 rows carry `nl_tags`, 44 of them marked `inferred` (derived from the row's own text, deterministic, 2 to 5 lowercase words each); the two plain-words reads above are recorded. Ask: does this close the NOT_REALIZED grade?
- **The widening (the CTO's ruling 2 and the never-widen pair):** 24 catalog rows became visible to their own firm's principals and to no other (control: 1,326 pairs, leaks 0, and the same matrix on the host). Both halves were signed on the deploy-only commit (CTO @e5812ce7df; COO in the ask's section 5). Seeing a row reads no data; the data grant is unchanged. Ask: anything here widens a partner firm's read beyond its own rows?
- **The release path:** one clean deploy (`c4c106aea1`, 19:50Z) after two catalog-quality catches at the cut that never reached the host: the true shipped cut read definitions 97 of 99 (the Z-S118 class again; the catalog is now emitted against a synthetic shipped cut and `r1.AC2` grades that), and the depth claims had aged past the 13:30Z publish (re-measured 16:07Z).

## 4. Rows these rounds, and the issuer's rulings

| row | standing | ruled by |
|---|---|---|
| Z-S120 (caveats one character per entry) | OBSERVATION, fixed | MX-c-19 A1: `_rule_caveats`; live (section 2) |
| Z-S121 (a servable table outranks a curated need on an overlap tie) | OBSERVATION | owner `2.0.0_SA_COO~O` (the ranking question); a tie rule measured to break another pin, so ranking is unchanged and the E-16 pin was relaxed to "the need is still answered" |
| Z-W42-S1 | BLOCKING (status flip outside a worker's paths) | the issuer flips; MX-c-18 order record |
| Z-W43-S1 to S6 (13 names, stale pin, docstring, expect regex, sparse worktree) | BLOCKING/OBSERVATION | MX-c-19 A1 and the order record |
| Z-W44-S1 to S5 (sparse census path, an issuer premise that did not hold, a path not granted) | BLOCKING/OBSERVATION | MX-c-20 A2 to A4 and the order record |

## 5. Carried to the L10 slug

1. **Round 18 is already issued by PRD v0.17 (CTO msg 34551, Andrew-direct):** CONTRACT C-GROUP (`bucket` on every row and tool, `vendor` and `firm` on every assets/bd row), MX-c-21 (source group per tool), MX-c-22 (the `etfs_get_positioning` extension), the 12 Schwab `dim_*` rows (NFRA_OPLGTW msg 34560), the labels for about 93 more client rows (each release adding known-firm values carries its own pair, CTO msg 34562). Due 2026-10-16 ~22:00Z.
2. **A catalog row and its tool in ONE deploy?** Every catalog release needs the true shipped cut to emit against; the procedure is `mk_cut17.sh` (a synthetic commit object) plus `r1.AC2`.
3. **The depth claims age at every daily publish** (about 13:30Z): the release procedure re-measures at the cut. A standing re-measure belongs to a later round, not a monitor.
4. **The lane gate refuses the issuer `infra/aws/ec2/opal-gateway/` and `infra/logic/registry/`**: every catalog landing goes through a worker (here MX-c-20 A1, A4).
5. **The weekly usage limit killed a worker once (Oct 15 ~14:00Z); the python install was removed and reinstalled (Oct 15 14:01-15:0xZ).** Neither touched a deliverable.
