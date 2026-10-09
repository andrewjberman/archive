# ETFS_RIVALS -- L8 packet, WORKSTREAMS 2 and 3 (first issuance) -- 2.0.0_SA_COO~V1 to 3.0.0_SA_CVO~RV1

**Compiled:** 2026-10-09 ~07:2xZ. **Orders:** 5 of 5 terminal (RIV-wa-1, wb-1, wc-1, wc-2, wd-1). **Merges on box/dell1:**
wa-1 718a8f6c4e, wb-1 98c5ba6d31, wd-1 67f42b7329, wc-1+wc-2 ccf53a8f16; hookup 7a25a44c24. **Drain suite** on the merged
tree: `962 passed, 6 skipped`. **Nothing deployed** (WS2 guard 1: no deploy before the round-28 reads at 11:00Z and 13:00Z).

## The real run (the artifact for every J1 below)

`deliverables/2.0.0_SA_COO~V1/ws2/real_run_local.py`, record `real_run_local_2026-10-08.json` (@48753709ed). Live S3 reads,
LOCAL writes only under `C:/tmp/ws2-real-run/layer/` (control: S3 head-object on the inferred row = 404; live page
LastModified unchanged 2026-10-08T13:08:16Z). Page date 2026-10-08, served on this box by
`deliverables/2.0.0_SA_COO~V1/ws2/serve_local.py` (gateway-shaped routes):
- page: http://127.0.0.1:8765/rivalfunds/2026-10-08
- audit: http://127.0.0.1:8765/rivalfunds/2026-10-08/audit
- chart object: http://127.0.0.1:8765/rivalfunds/2026-10-08/chart/IDVZ
If the server is down: `python deliverables/2.0.0_SA_COO~V1/ws2/serve_local.py C:/tmp/ws2-real-run/layer/opal-data-etfs/rivalfunds/etfs/platinum/page/date=2026-10-08 8765`.

## Judgment criteria to grade

| order | J1 (verbatim from the face) | what the run shows (issuer's read) |
|---|---|---|
| RIV-wa-1 | the dialog for Tokio Marine (IDVZ) ... reads a continuous 30d curve near 3.3 across 2026-10-07 and names the 15-for-1 split, the factor coming from a stored row | IDVZ.json TKOMY points 09-30..10-07: 3.537 i, 3.367 i, 3.329 i, 3.306 m, 3.367 m, 3.330 m; `adjustment` [split 15.0, ex 2026-10-07, INFERRED, https://finance.biggo.com/news/cc22fde9-8667-4623-84c8-7c1309d31835]; the factor read from the stored (local) row RIV-wb-1 wrote. NOTE: the J1 says "the first page published with this code"; this is a local render, so grade it as the pre-deploy read or hold the grade for the published page |
| RIV-wc-1 | ... the dialog's trade list is closed by default, its heading names the selected window, and on 30d it lists only the last 30 days' trades | open any security dialog, toggle 30d/90d/365d |
| RIV-wc-2 | ... the header carries no Period row, the ranking panels still switch periods, and the audit's exclusion line names the excluded line apart from the trade table | header `class="rf-periods"` markup count 0; audit: "Left out: 1 money-market line traded (CAPITAL GROUP CNTRL CSH-M, $6.2m): cash management, not a holding decision." |
| RIV-wd-1 | on the issuer's real run over CGIC's 2026-09-28..2026-10-06 windows, no unchanged-count row and no sub-20-bps row is shown as a trade, and no trade sits on a day the calendar marks repeat | unchanged-count and sub-20bps: CGIC 09-30..10-02 shows 1 trade (was 16). REPEAT: NOT MET as worded -- the calendar still marks 10-02/10-05/10-06 repeat while their windows carry trades; row ETFS_RIVALS-D1-S4 shows the LABELS are stale (canonical_shape holds new reports), so the remedy is the calendar, cut in WS3's second issuance |

RIV-wb-1 has no judgment criterion.

## Rows (this workstream; file `surprise-channel/investigations/INVESTIGATION_v1.dell1.md`)

D1-S2 (BLOCKING, ARMED; disarmed by the switch held unset; ruled @c5fb809173), D1-S3 (crossbox lane), D1-S4 (stale repeat
labels), D1-W23-S1, D1-W24-S1 (ruled: names from the frame), D1-W25-S1..S4 (S1/S2 repaired by wc-2's AMENDMENT 1),
D1-W26-S1 (ARMED, disarm owner this seat: publish_page half done 7a25a44c24; ai_accounts half after the 13:00Z read).

## ADDENDUM 1 (~08:5xZ) -- the repeat clause of RIV-wd-1's J1, corrected; three more WS3 orders terminal

- **Correction.** The packet's reading of wd-1's repeat clause (rows D1-S4, then D1-S5) is superseded by row
  ETFS_RIVALS-D1-S7 (@ba1667dea2): canonical_shape partitions are ALREADY the vendor's claimed as-of (a dry run over
  18,000+ rebuilt Bloomberg rows: as-of != partition in 0 rows), so CGIC's trade windows were dated right all along. The
  defect was the calendar comparing a claim with the REQUESTED day, which read a one-day-lagged daily fund as `repeat`.
- **The fix, RIV-wf-1** (merged 451b193828; CTO ADDENDUM 4 msg 2128): the calendar compares each claim with the previous
  capture's: newer `new`, equal `repeat`, older `regressed`. Local calendar run on live data (replay 09-28..10-08, local
  writes): CGIC 10-05 new (10-02), 10-06 new (10-05), 10-07 new (10-06); 10-01 and 10-02 repeat (09-30), both captures
  carrying the same 09-30 report -- genuine repeats. So wd-1's repeat clause can be graded MET on this artifact once the
  page is rebuilt with wf-1, or held for the served page.
- RIV-we-1 (ba92996a72) and RIV-we-2 (598173c0fa) are merged and are no-ops on real data (D1-S7); RIV-we-1's
  `delivered_on` now takes the requested date (wf-1). ADDENDUM 3's history rebuild is WITHDRAWN.
- None of we-1, we-2, wf-1 carries a judgment criterion. Merged suite: 977 passed, 6 skipped.
