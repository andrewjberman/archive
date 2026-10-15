# MDPF_CANON round 10 -- drain-end packet (2.0.0_SA_COO~D1), DRAFT 2026-10-15 ~16:4xZ

To `3.0.0_SA_CVO` (L8/L9). **STATUS: INTERIM, sent 2026-10-15 ~21:4xZ on the CVO's wait (its roster line names this packet owed). Gradable NOW: CN-l-2 AC3 of round 7 (section 3). Gradable ONLY AFTER section 4 is read (the first scheduled fire carrying the code, 2026-10-16 13:30Z gold, 13:50Z publisher): CN-r-1 AC4. A FINAL revision with section 4's read follows ~13:45Z 2026-10-16; no AC4 grade is asked before it.** Input: the CTO's round-9 analysis `ledger/ROUND_ANALYSIS.round9.md` @ff1e47f079, PRD v2.22, msg 6047. Decomposition v10, two orders, one issuance.
`round-close-check.py --project MDPF_CANON --round 10` (16:33Z): 2 of 2 orders complete, proofs 2 of 2 structurally valid, 1 JUDGMENT criterion ungraded (CN-r-1 AC4), verdict REFUSED on that one only (CN-r-2 carries no judgment criterion).

## 1. Orders, merges and evidence (MEASURED by the issuer at the merged tree)

| order | worker | merge | mechanical result | judgment owed |
|---|---|---|---|---|
| CN-r-1 the gold Trend groups carry a missing Dividend, Growth or sleeve leg only where the carried row still partitions the served Total within 0.011 (WORLD) | ~29 | `b6352de8f8` | pure 11, seams 4, oracle 11; CN-p-1 regression 7/7/7; pytest canon 49 passed; ruff clean | AC4 |
| CN-r-2 the publisher role may read `platinum/mdpf/*` (WORLD) | ~30 | `3df2f0851a` | statement 5, rest 4, eval 5; one added inline policy `s3:GetObject` | none |

## 2. WORLD acts and their evidence

- **CN-r-1 deploy** (`ADHOC.canon-r10-gold-carry-deploy`, CloudOps DELL1, ledger CLOSED 6 of 6): pair `NEVER_WIDEN_PAIR_R10_CN_R_1.md` signed by both halves (COO `5437fda3de`, CTO `9b9408fce1`); DELTA 0 of 497 cells on the real 2026-10-14 object. The issuer read the live function at 16:3xZ: `mdpf-gold-lambda` CodeSha256 `vNRXwWymIRmgptYv8+PEyFWH73IpIVHOpdT5mL/B7uk=`, modified 2026-10-15T16:18:35Z, `MDPF_GOLD_COMMIT` = the pin `b6352de843...`. D4 dry run: status green, `errors` [], `a4_objects_built` 16.
- **CN-r-2 deploy** (`ADHOC.canon-r10-publisher-latest-read-deploy`, CloudOps DELL1, ledger CLOSED 6 of 6, pin `3df2f0851a`): pair `NEVER_WIDEN_PAIR_R10_CN_R_2.md` signed by both halves (COO `5437fda3de`, CTO `9b9408fce1`). CloudOps reports plan 1/0/0, applied; one hand-run `published=0 unchanged=18 failed=0`, 22 of 22 served VersionIds equal, `latest.json` advanced 13:51Z to 16:33Z. The issuer read the role at 16:4xZ: four inline policies, the new one `mdpf-publisher-live-serve-read-policy` holds exactly `s3:GetObject` on `arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/*`. Delete is implicit-deny, UNPROVEN by the simulator (the CTO accepted this as stated). The scheduled 13:50Z fire of 2026-10-16 is the L5 read (section 4).
- **E4** (`ADHOC.canon-r10-e4-reader-measure`): 11 request-metrics filters live since 15:59Z; the 24 h read is due 2026-10-16 16:05Z. A measurement record, not a grade input.

## 3. The real run (the issuer looked at the page)

`round10/ITEM6_RENDERS_20261015.md` (words only): (A) the Other Models card in three planted states (pool, carried "as of", no pool) for CN-l-2 AC3 of round 7; (B) the `demo` Global Trend. Note (B): by Andrew's word (CTO msg 6082) a demo Global session moves to Variant 1 in round 11; after your msg 6133 PRD v2.23 @1fb9ac96ab ALSO repairs Variant 2 in round 11 (the Models band never carries on or after `per_model_detail_begins`), so a no-firmId non-internal Global session keeps the partition. Neither is a round-10 criterion.

## 4. The first scheduled fire carrying the code (TO READ 2026-10-16 ~13:45Z)

`python round10/checks/r9_trend_groups_readback.py read --pin b6352de843f3726ad5c51c650d9035ca8336db` (the copy with the amended R5), then the CTO's two asks: name the unchanged pairs, and state whether any reader keys freshness on a served `written_at`.

## 5. Rows and what is the CVO's

`MDPF_CANON-D1-S29` (ARMED; remedy: demo Global uses Variant 1 and Variant 2's Models-band carry is repaired, both land on DEV in round 11 (draft `round11/draft/ROUND11_RECTANGLE_DRAFT.md` @74a1baefb4), disarms when both are on DEV). CN-p-2 AC4 was regraded NOT MET by the CVO (v17 @29414f832d) and is carried by that remedy.
