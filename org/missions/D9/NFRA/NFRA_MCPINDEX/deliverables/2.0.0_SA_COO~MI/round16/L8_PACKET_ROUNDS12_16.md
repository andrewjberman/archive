# NFRA_MCPINDEX rounds 12 to 16 -- the issuer's drain-end packet for L8/L9 (2.0.0_SA_COO~MI, 2026-10-15 ~08:3xZ)

Addressed to `3.0.0_SA_CVO~Z`.
- **Source:** PRD v0.11 to v0.16 ADMITTED (FWD-22: the one catalog at TABLE grain, from the CRO's gateway data contracts G1 to G6 and G5r), on Andrew-direct 2026-10-14 ~12:4xZ (gateway live with census tables by Friday 2026-10-16). Round 12's release MX-r-13 is the tail of all five rounds.
- **State:** every order of rounds 12 to 16 is COMPLETE. `round-close-check.py` reads MAY-CLOSE for rounds 12, 13, 14, 15 and 16 (orders 2, 2, 2, 1, 2; proofs ok).
- **The gateway serves `1b18b94979`** (previous `ee23dd004c`), landed 2026-10-15T07:54:33Z, ledger `nfra-mcpindex-r12-catalog-release-v2` CLOSED. A first attempt (`d020bee315`) deployed 06:3xZ, read `r13.AC2` FAIL and was rolled back as both halves directed (verified); the causes were the issuer's and are fixed (rows Z-S118, Z-S119; MX-r-13 A5).

## 1. Orders -- graded on box/sitez (issuer re-run)

| order | serves | status | mechanical (issuer re-grade) |
|---|---|---|---|
| MX-c-10 depth on every (a) tool | FWD-20 | complete @8c74d1d902 | c10.AC1 11 of 11, AC2 7 of 7, AC3 17 of 17 measured, anchors 2 of 2 |
| MX-c-11, MX-c-12 harvest rows at table grain (78) | FWD-22 | complete | c11.AC1-4, c12.AC1-3 PASS |
| MX-c-13, MX-c-14, MX-c-15 silver table rows (216, clean + fork registry), loader and writer | FWD-22 | complete (MX-c-14 reopened for A8 to A13: the registry's entity names and the catalog land through the worker, lane gate) | c14.AC1-3 PASS (216 of 216; 1080 of 1080), c15.AC1-2 PASS (216 of 216 joined; 10 of 10 defects refused) |
| MX-c-16 the three certified-channel corrections | FWD-22 | complete | c16.AC1-3 PASS; the CVO's difference control (your read @2a8a025031): 390 pairs, deny->serve 0, serve->deny 1 (the aum row, opal-internal) |
| MX-c-17 the G5r rival-fund enrichment (14 rows) | FWD-22 | complete | c14.AC2 216 of 216, c17.AC2 PASS, c14.AC3 5 of 5 |
| MX-r-13 the catalog release | FWD-20, FWD-21, FWD-22 live | complete: deployed `1b18b94979`; proof VALID | r13.AC1 to AC4 PASS, re-run by the issuer against the host 08:1xZ: AC2 sum 93 of 93, definitions 93 of 93; AC3 depth 11 of 11, answer-time 17 of 17, anchors 2 of 2; AC4 host md5 = tree md5, v0.5, 78 / 216 / 216 / 5, 29 named read_tools all served |

## 2. The one real run of each outcome, 08:2xZ, through this seat's opalgateway session (served `1b18b94979`, catalog v0.5)

- **Table grain and G5r:** "What does the PFOE rival fund peer group hold, and what is the latest report date for a rival fund?" The two servable matches (etfs positioning, peers) come FIRST; the three rival-fund tables follow as GAPS (`servable: false`, `next_tool: null`, `gap.owner: NFRA_OPLGTW`). `canonical_shape` states the fund keys, the identifier fill rates, the newest-part rule and that a fund's latest report is read from it, not from the coverage table (Z-S124). `peer_group_map` states the groups measured 2026-10-14 (IDVZ with five rivals, PFOE with six; DIVZ and PFDE none).
- **A live typed tool on a harvest row (FWD-21):** `opal_describe harvest_article_sentiment` answers `servable: true` with `next_tool: harvest_search_articles` and the tone-not-a-quantity caveats. Before the release the same row read `read_tool: null`.
- **Depth and freshness:** the etfs positioning match carries `history_depth` 2026-10-13, claim measured, read from the served object at answer time, beside `served_written_at` 2026-10-14T13:01:42Z.

## 3. What L9 is asked to judge

- **FWD-22 at table grain:** 216 client, ETFs, news, portal and mdpf tables and 78 harvest tables are rowed with key template, fork keys, lag and the not-served marks; the commit-time naming gate admits their tokens only as strings held in the registry at HEAD (the catalog branch, `.tools/naming-gate.py` @df822c81b3, under the laptop CTO's seven conditions). Is the one catalog now at table grain as v0.11 to v0.16 ask?
- **The three certified-channel corrections** (your pre-issue read). Ask: does anything widen a partner firm's read? The difference control says no (390 pairs).
- **The release path:** a first deploy rolled back on a check the issuer had not updated for MX-c-10's per-link claim; nothing was lost (verified), and the re-cut passed all four criteria.

## 4. Rows these rounds, and the issuer's rulings

| row | standing | ruled by |
|---|---|---|
| Z-W36-S5 and the round 13 worker rows | OBSERVATION/INERT | carried |
| Z-W38-S9 to S11 (retired_reason wording, "exactly four", the quoted token in prose) | BLOCKING/OBSERVATION | MX-c-14 A7 |
| Z-W38-S16 (no CATALOG-EXEMPT line on a prose-only diff) | BLOCKING | benign: the gate grades only added literals (MX-c-14 record) |
| Z-W40-S1 to S3, Z-W41-S1, S2 | OBSERVATION/BLOCKING | MX-c-16 and MX-c-17 order records (the index link to the denied aum row removed; the AC2 denominator was the issuer's error) |
| Z-S118 (release rolled back on r13.AC2) | BLOCKING | MX-r-13 A5: both causes the issuer's and fixed |
| Z-S119 (AC2 reads 67 of 93 on the base) | OBSERVATION | MX-r-13 A5: the order's "PASS now" was stale |

## 5. Carried to the L10 slug

1. **The readers for the rival-fund, client and ETFs tables** are NFRA_OPLGTW's (OG-ap-20 for G5 wave A and category-views; the rest queued): until each lands the rows read `gap` with the owner.
2. **`json-tiered/` stated authenticated-only** waits on Z-S114 (not in these rounds).
3. **The depth claims go stale at every daily publish** (a measured `snapshot-asof` equals the object until the next write): the release procedure re-measures at the cut. A standing re-measure belongs to a later round, not a monitor (the standing moratorium).
4. **`r13.AC2` is an after-release check** (a regression guard that cannot pass on the base once the live tool set moves).
5. **The lane gate refuses the project's COO `infra/logic/registry/` and `infra/aws/ec2/opal-gateway/`**: those writes went through a worker under the order's `<paths>` (MX-c-14 A8 to A13). Worth one line in the cut template for any catalog round.
