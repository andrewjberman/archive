# SEGMENT_CENSUS -- AMGT-av-4 (round 72)

Source: `read_segment_breakdown` (`lib/research/api/scoped_amgt.py`), run local over every covered name against the stored filing analyses at `filings/v1/<key>/*.analysis.json` (S3 read with the operator's credentials, no write).

Totals: covered names 95; names serving segment rows 12; names serving a plain reason 83; rows served 116.

Rows are the filing's own sentences about each segment (prose with a cite), NOT a numeric segment table. No stored numeric segment data exists (0 of 95 model blocks, 0 of 117 Bloomberg bronze fields).

## Names serving rows

| name | rows | form | filed | accession |
|---|---|---|---|---|
| ASML_NA_Equity | 5 | 20-F | 2026-02-25 | 000162828026011378 |
| BABA_US_Equity | 11 | 20-F | 2026-05-20 | 000119312526231755 |
| BA_US_Equity | 11 | 10-K | 2026-01-30 | 000162828026004357 |
| COST_US_Equity | 10 | 10-K | 2025-10-08 | 000090983225000101 |
| HAL_US_Equity | 12 | 10-K | 2026-02-06 | 000004501226000015 |
| HD_US_Equity | 10 | 10-K | 2026-03-18 | 000162828026019436 |
| INTU_US_Equity | 9 | 10-K | 2026-09-09 | 000089687826000037 |
| KMB_US_Equity | 9 | 10-K | 2026-02-12 | 000162828026007567 |
| NU_US_Equity | 10 | 20-F | 2026-04-08 | 000129281426002166 |
| PBR_US_Equity | 8 | 20-F | 2026-04-09 | 000129281426002168 |
| SAP_GY_Equity | 11 | 20-F | 2026-02-26 | 000110465926020058 |
| VLO_US_Equity | 10 | 10-K | 2026-02-25 | 000162828026011499 |

## Names serving a plain reason (no segments)

Reason served to all of these: `No filing analysis is stored for this name yet, so no segment breakdown is shown. A segment table with figures needs a separate segment data pull.`

| name |
|---|
| 1299_HK_Equity |
| 2317_TT_Equity |
| 8035_JP_Equity |
| 8306_JP_Equity |
| 8316_JP_Equity |
| 8766_JP_Equity |
| 939_HK_Equity |
| 9433_JP_Equity |
| 992_HK_Equity |
| ADBE_US_Equity |
| AI_FP_Equity |
| AMD_US_Equity |
| AMXB_MM_Equity |
| AZN_LN_Equity |
| BATS_LN_Equity |
| BBSE3_BZ_Equity |
| BNP_FP_Equity |
| BP/_LN_Equity |
| BZLFY_US_Equity |
| CDNS_US_Equity |
| CELH_US_Equity |
| CLX_US_Equity |
| CNR_CN_Equity |
| CPA_US_Equity |
| ENEL_IM_Equity |
| GOOGL_US_Equity |
| GPN_US_Equity |
| GSK_LN_Equity |
| HEI_US_Equity |
| HSBA_LN_Equity |
| IBE_SM_Equity |
| ICICIBC_IN_Equity |
| ICT_PM_Equity |
| IDXX_US_Equity |
| IMB_LN_Equity |
| ISP_IM_Equity |
| ISRG_US_Equity |
| JD_US_Equity |
| KOFUBL_MM_Equity |
| KPN_NA_Equity |
| LLY_US_Equity |
| MA_US_Equity |
| MELI_US_Equity |
| MER_PM_Equity |
| ML_FP_Equity |
| MNST_US_Equity |
| MSCI_US_Equity |
| NESN_SW_Equity |
| NFLX_US_Equity |
| NG/_LN_Equity |
| NKE_US_Equity |
| NOKIA_FH_Equity |
| NOVN_SW_Equity |
| NOW_US_Equity |
| OMAB_MM_Equity |
| ORA_FP_Equity |
| PWR_US_Equity |
| QXO_US_Equity |
| RIO_LN_Equity |
| RKT_LN_Equity |
| RMS_FP_Equity |
| ROG_SW_Equity |
| RWE_GR_Equity |
| SAN_FP_Equity |
| SHOP_CN_Equity |
| SLB_US_Equity |
| SNPS_US_Equity |
| SPOT_US_Equity |
| SSE_LN_Equity |
| ST_SP_Equity |
| TSM_US_Equity |
| TTE_FP_Equity |
| UBER_US_Equity |
| UBSG_SW_Equity |
| ULVR_LN_Equity |
| UNH_US_Equity |
| UNVGY_US_Equity |
| VIVT3_BZ_Equity |
| V_US_Equity |
| WALMEX*_MM_Equity |
| WDAY_US_Equity |
| ZTS_US_Equity |
| ZURN_SW_Equity |

Distinct reasons among the 83: 1.

## Row for Andrew: Bloomberg segment pull (a vendor use, NOT performed)

The 83 names above carry no segment prose and no numeric segment data. A numeric segment table for them needs a Bloomberg segment pull, which is a vendor use and waits on Andrew's word. Names listed above under 'plain reason'.
