# ETFS_RIVALS -- the backfill gaps, as demand rows for MDPF_DEMQUE (not kept open in this project)

Issuer 2.0.0_SA_COO~V1, 2026-10-14. Authority: Andrew-direct ~18:5xZ 2026-10-14 as relayed by 1.0.0_SA_CTO~DELL1 msg 5712, VERBATIM: "ETFS_RIVALS is done now, all it needs is its backfill sorted out in DEMQUE";
record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261014_185xZ_ETFS_RIVALS_DONE_BACKFILL_TO_DEMQUE.md`. Receiver: `2.0.0_SA_COO~Q1` (msg 5712). Every figure below is MEASURED by a read-only S3 read on
2026-10-13 and 2026-10-14 (page day 2026-10-13, as-of 2026-10-12); none is a vendor-quoted cell count. Sources: `round30_prep/RIVALFUNDS_PAGE_HISTORY_NEEDS_MEASURED_20261013.md` (@a100e2490e), `round30_prep/owed_size.py`
and its 2026-10-14 run, `round30_prep/xe3_live_delta.py`. Andrew's earlier word on the first two rows (VERBATIM, CTO msg 5197): "C1 yes, approved in that order" (field-matched, 30 then 90 then 365 days), recorded in the DEMQUE form
`org/tier1_exec/1.0.0_SA_CTO/deliverables/DEMQUE_QUEUE_FORM_ANDREW_20261013.md`.

What the page reads (the reason for each row): the holding rankings (best and worst 10, 30d/90d/365d) read each held security's day total return `DAY_TO_DAY_TOT_RETURN_GROSS_DVDS`, else a close ratio, else the fund's implied price; the
security dialog price curves read the close `PX_LAST` only. No component reads a fund-level price. Nothing else on the page needs vendor history.

## Row 1 -- total return on each fund's held days (the rankings)

- Fields: `DAY_TO_DAY_TOT_RETURN_GROSS_DVDS`. Securities: every holding of the 13 funds (BASG, BIDD, CGIC, ETFT, GQGU, IDVZ, INEQ, PCLG, PFOE, SCHY, TSEL, TXUE, WCMG), on the trading days a fund held them.
- Dates and units (owed = no stored close; as-of 2026-10-12): 30d from 2026-09-12: 7,652 held-owed units; 90d from 2026-07-14: 30,714; 365d from 2025-10-12 (first trading day 2025-10-13): **123,933** units over 753 securities.
- Per fund, 365d held days owed (a security held by two funds counts for each): BASG 8,049; BIDD 11,090; CGIC 44,653; ETFT 6,025; GQGU 916; IDVZ 7,385; INEQ 24,654; PCLG 6,151; PFOE 3,994; SCHY 25,243; TSEL 6,476; TXUE 11,844; WCMG 4,247.
- Order Andrew approved: 30d, then 90d, then 365d (newest period first).

## Row 2 -- the close on the days a dialog curve draws (the price curves)

- Field: `PX_LAST`. Securities: the holdings that get a security dialog on the page (the top 10 best and worst of the 30d and 365d rankings and the buying trend's top 10 into and away): 402 dialogs on the 2026-10-13 page,
  375 matched to securities (29 keys did not map to a security id and are not counted).
- Units: 30d 5,537 chart-owed; 90d 21,275; 365d **89,717** (the 2026-10-14 read; 89,216 on 2026-10-13). Combined with Row 1: 213,650 cells at 2026-10-14 (213,149 on 10-13), against a 20,000-cell run cap: about 11 runs.
- The standing request `ETFS_RIVALS-HISTORY-OWED-DAILY` (filed by Q1, close only, 365 days, 20,000 cells a run) already queues the close for ALL 742 securities (183,649 units on 2026-10-14); Row 2 is the part of it the page reads.
  The 36,705 units outside every held day and every dialog are not drawn.

## Row 3 -- corporate actions (dividends and splits) for securities with no row of any kind

- Field: `DVD_HIST_ALL` (with `DVD_CRNCY`), 365 days. Securities: **71** of the 794 in the security universe have no `corporate_actions` row of any kind in the live store (11 plain pulls, 9,354 event rows, 724 securities covered);
  the daily leg's latest pull holds only 33 securities. The 71 (key spelling as stored, spaces as underscores): 2269_HK_Equity, 3491_TT_Equity, 6857_JP_Equity, AAF_LN_Equity, AAPL_US_Equity, ABT_US_Equity, ACGL_US_Equity, ACN_US_Equity, ADBE_US_Equity, AJG_US_Equity, AMD_US_Equity, AXON_US_Equity, BAB_LN_Equity, BG_US_Equity, BKD_US_Equity, BSX_US_Equity, CACI_US_Equity, CB_US_Equity, CMG_US_Equity, CRS_US_Equity, CVNA_US_Equity, DASH_US_Equity, DGVXX_US_Equity, DT_US_Equity, DXCM_US_Equity, EBAY_US_Equity, EFX_US_Equity, GDDY_US_Equity, GENI_US_Equity, GRAB_US_Equity, HAL_US_Equity, HLN_US_Equity, IBKR_US_Equity, ICE_US_Equity, INTU_US_Equity, JAN_US_Equity, KB_US_Equity, LTMC_IM_Equity, MCK_US_Equity, MICC_LN_Equity, MSCI_US_Equity, MTD_US_Equity, MU_US_Equity, NBIS_US_Equity, NET_US_Equity, NKE_US_Equity, NTES_US_Equity, OTP_HB_Equity, PAYC_US_Equity, RARE_US_Equity, RBLX_US_Equity, RGA_US_Equity, ROL_US_Equity, SNDK_US_Equity, SNPS_US_Equity, SONY_US_Equity, SPHR_US_Equity, TEAM_US_Equity, TEVA_IT_Equity, THC_US_Equity, TPR_US_Equity, TTD_US_Equity, UMG_NA_Equity, VG_US_Equity, VLO_US_Equity, VLTO_US_Equity, VRSK_US_Equity, WDC_US_Equity, XYZ_US_Equity, ZTS_US_Equity, nan.
- Why: the price curves and the trade schedule apply splits and flows from these rows; a security with no row is read as having no action, not as unpulled (the RIV-xe-2 cell, not cut, was to give such a security one
  365-day pull; the CTO ruled it waits on the union reader, now deployed).

## Not a row

- The history-owed SWITCH (`RIVALFUNDS_HISTORY_OWED`) stays OFF; no producer change ships with these rows. The producer side (the leg's trading-day gate and queue-state reader, ACWI/IWM removal) is merged on box/dell1
  (RIV-xe-1 @47530f3817, RIV-xf-1 @03dbf4b128) and its site-Z deploy is under `1.0.0_SA_CTO~Z`'s half; the vehicle's checkout must carry `data/mdpf/scripts/demque/` (row W41-S1).
- Not measured: held days after each fund report that holds a security (a fund whose reports skip a day is understated); the dramatic-move window beyond its constant.

## Correction (2026-10-14 ~19:0xZ, from 2.0.0_SA_COO~Q1 msg 5733, confirmed against my own two runs)

Row 3 is **70** securities, not 71. The 71st key in the list above is `nan`: a null `security_id` in the universe table that my set built as the string "nan" (the first run, which dropped nulls with `dropna()` on the other side, counted 70). The dividend request is 70 securities. DQ-t-63 (`org/missions/D8/MDPF/MDPF_DEMQUE/task-orders/MDPF_DEMQUE.TO-DQ-t63.etfs-rivals-backfill-intake.md` @9b7d894bcb, Q1's) files the three rows.
