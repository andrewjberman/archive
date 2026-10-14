# MDPF_CANON round 9 -- ADDENDUM 1 to `NEVER_WIDEN_PAIR_R9_CN_P_1.md`: the ONE-TIME publish of the Trend groups onto the as-of-2026-10-13 dated objects, tonight

**COO half SIGNED (below); CTO half OWED.** Issuer `2.0.0_SA_COO~D1`, 2026-10-14 ~23:2xZ. The pair itself is unchanged and signed by both halves (COO `54da2eb87d`, CTO `d996228e93`); its deploy (D2 and D4) is DONE (CloudOps `0.7.0_AE_CloudOps~DELL1`, 22:50Z, pin `8e2dd0fb369043d5f23dca2d02dba7d51cfabd6f`, D4 green with `errors` empty). This addendum covers ONE act the pair did not: writing the new fields onto objects that already exist.

**Authority.** Andrew-direct ~22:5xZ (CTO record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261014_225xZ_MDPF_PUBLISH_TREND_TONIGHT_OVERWRITE_OK.md` @44eac4d919): an explicit OK to overwrite today's served as-of 2026-10-13 MDPF objects so the Trend groups are on PROD tonight; CTO msg 5945 asks for this addendum. The PRD's write-once rule (A8) is overridden by that word for the eight keys below, once.

## 1. How write-once is bypassed: it is NOT, and the lambda is not the writer

MEASURED by reading `mdpf_gold_consolidator.py` at the pin (`conditional_put`, lines 2498-2579; `lambda_handler`, 3423-3464): a production invoke has NO flag, input or switch that overwrites a dated key. A business-different body at an existing dated key is recorded `conflict` and NOT written; a same-as-of re-run tonight would therefore write nothing and would only log eight conflicts. It would also re-derive the CN-h-1 frontier counts from the A4 map, moving client-visible counts tonight that the signed pair places at the first scheduled fire. So the act is NOT a re-run. It is:

- **The bodies** are built by the issuer's instrument `round9/checks/build_publish_bodies.py` (read-only; writes nothing to AWS): for each scope, the EXISTING newest dated `aggregate-aua-timeseries` body plus exactly the keys the merged CN-p-1 code adds, computed by the code's own `apply_global_trend_groups` (the four keys; Global `meta.trend_groups`), and the EXISTING `category-views` body minus the `muni` member of `SMA > ALT Strategies`. The script REFUSES (exit 1) if any other path of any body differs. MEASURED 2026-10-14 ~23:1xZ against S3: every existing body round-trips byte-equal through the producer's canonical serializer (`canon_round_trip_equal` true on all 8), so the new body is the old body plus the new keys and nothing else; `r9_trend_groups_readback.py read --dir` over the eight bodies reads R1-R8, R10 and R11 PASS (R9 is the run-manifest arm and has no manifest tonight: N/A).
- **The writer** is the CloudOps seat's `put_object` of those eight bodies to their existing dated keys (the bucket is versioned: each put creates a new version; the prior version stays). Nothing is deleted.
- **Provenance, stated:** the new bodies carry the original `_provenance` (producer, process time, trigger of the 2026-10-13 run) unchanged; the Trend keys were added by an issuer-instrument splice authorised by Andrew, not by a scheduled run. The first scheduled fire carrying the code (2026-10-15 13:30Z) writes the as-of 2026-10-14 objects by the lambda itself and is the production evidence; tonight's objects are NOT production evidence of the lambda.
- **The publisher** (`opal-assets-mdpf-portal-publisher`) then copies gold to the served plane `s3://opal-data-portal-v2/platinum/mdpf/<scope>/<type>.json` by sha256 compare (it is the existing path, hand-run once with the schedule's own input). Expected: the eight pairs `published`, every other pair `unchanged`.

## 2. Blast radius: the eight gold keys, the eight served keys, nothing else

| scope | type | gold key (`portal/gold/mdpf/`) | prior VersionId | prior sha256 (12) | new bytes |
|---|---|---|---|---|---|
| global | aggregate-aua-timeseries | `global/aggregate-aua-timeseries/2026-10-13.json` | `VfcEmemcvHWpldKQD3tCsfhgxwAkOkT.` | `a3f6f68ad042` | 661224 |
| global | category-views | `global/category-views/2026-10-13.json` | `.AsAt8150OacIoKPbEPIomg7FyxbeTGa` | `43793137acfd` | 6540 |
| 49financial | aggregate-aua-timeseries | `49financial/aggregate-aua-timeseries/2026-10-13.json` | `xU0goe_C8i6G7sLpZ7qkbH_iDHHrFzm9` | `cf7de49a7611` | 467922 |
| 49financial | category-views | `49financial/category-views/2026-10-13.json` | `q3sz1iMKZepYuWzEcZnhny4sgvF2Zm.6` | `a408ca0cd43d` | 6069 |
| inflection | aggregate-aua-timeseries | `inflection/aggregate-aua-timeseries/2026-10-13.json` | `GsFdLfEIeWW76qNRzboTPNF_fm2M0NmH` | `37aec897cffb` | 127480 |
| inflection | category-views | `inflection/category-views/2026-10-13.json` | `DstOQ31op6amTLpd6_mVarE.7idR52OF` | `ea8c401238fe` | 5811 |
| cottonwood | aggregate-aua-timeseries | `cottonwood/aggregate-aua-timeseries/2026-10-13.json` | `0HG3poRwF177VPMYrXqW95DwOGtUYNd3` | `3d1c2c94437c` | 517495 |
| cottonwood | category-views | `cottonwood/category-views/2026-10-13.json` | `4CXDNRDfB60TzcgZDZYqG4VvgrON7Z9x` | `88ccfda5ccab` | 6074 |

(The prior VersionIds are the pair's section 6 baseline, re-measured unchanged by the builder at ~23:1xZ; the order re-reads them at its start and STOPS if one moved. New sizes are as built tonight; the builder is re-run by the order, so a later SMArtX partition changes `meta.trend_groups.smartx_partition` and the bytes, which is why the order verifies by the readback and not by a pinned hash.)

- **What moves, per object:** the four timeseries keys on each timeseries (three arrays and `carried_dates`; Global only: values, and `meta.trend_groups`; the three firm scopes: all-None and `[]`); one member row (`muni`, `aum: null`, $0.00) fewer on each category-views. The served-plane copies of the same eight follow through the publisher.
- **What cannot move:** every other key of every one of the eight bodies (the builder refuses otherwise): `opal_aggregate_aua`, `point_class`, `model_aua`, `non_model_aua`, every `by_model` value and COUNT, `account_count_total`, `meta.frontier_count`; the as-of; the aum-metrics and account-distribution objects (not written); the gold parquet partitions (write-once, NOT touched: the 2026-10-13 partition does not gain the three columns; the first fire's partition does); the staged runner objects; the publisher's code. The CN-h-1 and CN-l-1 count moves stay at the 2026-10-15 13:30Z fire, as the signed pair places them, so the disjointness table of the pair section 4 holds unchanged.
- **N writers (this act):** the Trend keys on these eight objects have ONE writer tonight, the CloudOps `put_object` of the builder's bodies; the scheduled lambda is not a writer of as-of 2026-10-13. The served-plane copies have ONE writer, the publisher.
- **Client-visible:** the PROD `/portfolios` Global Trend is the page in question. The new keys are read by the portal only once CN-p-2 lands (it is not on PROD); on PROD today nothing reads them, so the visible change tonight is NONE until the portal candidate lands, and the Muni member removal is not read by any portal page (pair section 6). The point of the act is that the data CN-p-2 reads is served.
- **Window:** while the objects are mid-change a reader sees either the old or the new version of a key (S3 is atomic per key); the gold put and the publisher copy are separated by minutes, so the served plane and gold may disagree for that interval; neither plane is ever absent.

## 3. Every branch, read from the rules

- **The builder refuses** (a body differs outside the allowed paths, a `muni` member is absent, no SMArtX partition read): exit 1, nothing is put, the order stops and reports.
- **A put fails midway** (a key not written): the other keys already written are rolled back by their prior version (section 4); the order does not leave a mixed set. Mixed Global (timeseries new, category-views old) is harmless to the portal (it reads named fields) but the order restores it anyway.
- **The publisher reports a failed pair:** the gold keys stay new; the publisher is re-run once; if it still fails the served plane is restored per key (section 4) and the order reports.
- **The CloudFront cache** may serve the old served-plane body for its TTL; the order reads the cache headers and states them; it does NOT invalidate (not authorised by this addendum).

## 4. Rollback per key (a copy of the prior version, never a delete)

Per gold key: `copy-object` of the recorded prior VersionId onto the same key (the prior version becomes the current version), read back by sha256 equal to the recorded prior sha256. Per served key: the same, from the served key's own prior VersionId recorded before the publisher run, or one publisher run after the gold keys are restored. Per change: the Trend publish is independent of the signed deploy; reverting it does not touch the lambda, CN-h-1 or CN-l-1. A revert of the lambda deploy is the pair's section 4 and is a separate act.

## 5. Acceptance

By the order: the eight gold keys read back sha256 equal to the built bodies; `r9_trend_groups_readback.py read --dir <built>` and then the same readback over the S3 objects: R1-R8, R10, R11 PASS (R9 N/A tonight); the served-plane Global timeseries carries the four keys; the publisher response lists the eight pairs `published` and nothing else changed. By the issuer: the 5174 render (the page the CRO and Andrew are smoking) over the real served object once the portal candidate lands.

## COO half -- SIGNED

`2.0.0_SA_COO~D1`, 2026-10-14 ~23:2xZ, on the bytes above: signed for the blast radius of section 2 (eight gold keys and their eight served copies; the four timeseries keys, `meta.trend_groups` on Global, one member row), every branch of section 3, the rollback per key of section 4 with each prior VersionId recorded in section 2, and the stated provenance of section 1 (a splice authorised by Andrew's word, not a run; not production evidence of the lambda). On the conditions that the CTO half is signed on these bytes, that the order's before-print reads the eight prior VersionIds unchanged, and that the issuer's written GO naming the pin precedes the first put.

## CTO half -- OWED (`1.0.0_SA_CTO~DELL1`)

Sign, or refuse naming what is missing; a signature is a line in a commit by that seat, and no message carries it.
