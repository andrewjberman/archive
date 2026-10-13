# Round 103, workstream V1 -- the per-security pull census, by name (FWD-40 (c), PRD v0.44)

**Source:** `deliverables/0.9.0_WK_AMGT_RESAPP~409/run/pull_census.json` (worker `~409`, merged; 95 of 95 names, 8 shards, then one overlay per name on the live function `AaACnKtr..`).
Each cell is CALLS over the six routes the page makes per name (overlay, thesis, peers, coverage, versions, ledger), in-process on the live pool. The last two columns are the
DEPLOYED overlay's handler time and Init (Lambda, one request per name, in order: one cold container start, 1299_HK_Equity).

**How to read the counts.** The census runs 12 names per process in sequence, so a name's counts carry the process's warm caches (the served cache, the held-name index, the gold snapshot):
the first name of a shard pays what the later ones do not. The counts say WHAT a name pulls and in what proportion; they are not a cold-container figure (the worker's row S1: ASML_NA's 134
calls on the issuer's single-name run read 116 here). The time that transfers to Lambda is the last two columns.

| name | corpus | filings | management | news | price | scanner | posture | peers | scores | drafting | coverage | other | local ms | Lambda handler ms | Init ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1299_HK_Equity | 47 | 2 | 1 | 7 | 16 | 3 | 2 | 4 | 1 | 0 | 1 | 16 | 7896 | 2422 | 704 |
| 2317_TT_Equity | 59 | 3 | 2 | 7 | 16 | 44 | 4 | 4 | 2 | 0 | 1 | 1 | 17752 | 1202 |  |
| 8035_JP_Equity | 35 | 2 | 1 | 7 | 16 | 3 | 2 | 4 | 1 | 0 | 1 | 16 | 6951 | 559 |  |
| 8306_JP_Equity | 34 | 2 | 1 | 7 | 16 | 3 | 2 | 4 | 1 | 0 | 1 | 16 | 6358 | 620 |  |
| 8316_JP_Equity | 34 | 2 | 1 | 7 | 16 | 3 | 2 | 4 | 1 | 0 | 1 | 16 | 6659 | 606 |  |
| 8766_JP_Equity | 34 | 2 | 1 | 7 | 16 | 3 | 2 | 4 | 1 | 0 | 1 | 16 | 6817 | 628 |  |
| 939_HK_Equity | 42 | 2 | 1 | 7 | 16 | 3 | 2 | 4 | 1 | 0 | 1 | 16 | 7234 | 641 |  |
| 9433_JP_Equity | 35 | 3 | 1 | 7 | 16 | 5 | 4 | 4 | 2 | 0 | 1 | 18 | 7181 | 708 |  |
| 992_HK_Equity | 46 | 3 | 1 | 6 | 2 | 44 | 4 | 4 | 2 | 0 | 0 | 5 | 14706 | 673 |  |
| ADBE_US_Equity | 51 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 16 | 6151 | 689 |  |
| AI_FP_Equity | 42 | 2 | 1 | 6 | 2 | 44 | 2 | 4 | 1 | 0 | 0 | 3 | 14386 | 625 |  |
| AMD_US_Equity | 51 | 3 | 1 | 6 | 2 | 4 | 2 | 4 | 1 | 0 | 0 | 5 | 6880 | 763 |  |
| AMXB_MM_Equity | 32 | 2 | 1 | 6 | 2 | 44 | 2 | 4 | 1 | 0 | 0 | 3 | 15193 | 564 |  |
| ASML_NA_Equity | 46 | 5 | 2 | 6 | 2 | 44 | 4 | 4 | 2 | 1 | 0 | 0 | 15774 | 795 |  |
| AZN_LN_Equity | 45 | 2 | 1 | 6 | 2 | 44 | 2 | 4 | 1 | 0 | 0 | 3 | 16096 | 822 |  |
| BABA_US_Equity | 40 | 5 | 4 | 6 | 2 | 41 | 4 | 4 | 2 | 1 | 0 | 0 | 14624 | 974 |  |
| BATS_LN_Equity | 47 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 6365 | 705 |  |
| BA_US_Equity | 51 | 7 | 4 | 8 | 2 | 1 | 4 | 4 | 2 | 1 | 0 | 2 | 7893 | 1330 |  |
| BBSE3_BZ_Equity | 33 | 3 | 1 | 6 | 2 | 2 | 4 | 4 | 2 | 0 | 0 | 5 | 6240 | 578 |  |
| BNP_FP_Equity | 34 | 2 | 1 | 6 | 2 | 44 | 2 | 4 | 1 | 0 | 0 | 3 | 10826 | 575 |  |
| BP/_LN_Equity | 32 | 3 | 1 | 6 | 2 | 3 | 4 | 4 | 2 | 0 | 0 | 5 | 6118 | 982 |  |
| BZLFY_US_Equity | 32 | 3 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 5 | 5530 | 538 |  |
| CDNS_US_Equity | 51 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 7449 | 611 |  |
| CELH_US_Equity | 33 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4757 | 628 |  |
| CLX_US_Equity | 31 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4564 | 656 |  |
| CNR_CN_Equity | 37 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4812 | 643 |  |
| COST_US_Equity | 39 | 5 | 4 | 8 | 2 | 1 | 4 | 4 | 2 | 1 | 0 | 2 | 5902 | 735 |  |
| CPA_US_Equity | 31 | 3 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 5 | 5028 | 551 |  |
| ENEL_IM_Equity | 45 | 3 | 1 | 6 | 2 | 2 | 4 | 4 | 2 | 0 | 0 | 5 | 6317 | 649 |  |
| GOOGL_US_Equity | 32 | 3 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 5 | 4625 | 724 |  |
| GPN_US_Equity | 31 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4780 | 531 |  |
| GSK_LN_Equity | 41 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 5412 | 726 |  |
| HAL_US_Equity | 31 | 5 | 4 | 6 | 2 | 1 | 4 | 4 | 2 | 1 | 0 | 0 | 4687 | 663 |  |
| HD_US_Equity | 39 | 5 | 4 | 9 | 2 | 1 | 4 | 4 | 2 | 1 | 0 | 3 | 5653 | 810 |  |
| HEI_US_Equity | 35 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4712 | 665 |  |
| HSBA_LN_Equity | 41 | 3 | 1 | 6 | 2 | 2 | 4 | 4 | 2 | 0 | 0 | 5 | 5554 | 882 |  |
| IBE_SM_Equity | 43 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4818 | 661 |  |
| ICICIBC_IN_Equity | 32 | 3 | 1 | 6 | 2 | 2 | 4 | 4 | 2 | 0 | 0 | 5 | 4714 | 625 |  |
| ICT_PM_Equity | 37 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4618 | 627 |  |
| IDXX_US_Equity | 33 | 3 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 5 | 4863 | 532 |  |
| IMB_LN_Equity | 35 | 3 | 1 | 6 | 2 | 2 | 4 | 4 | 2 | 0 | 0 | 5 | 4782 | 707 |  |
| INTU_US_Equity | 53 | 5 | 4 | 6 | 2 | 1 | 4 | 4 | 2 | 1 | 0 | 0 | 6325 | 830 |  |
| ISP_IM_Equity | 35 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4393 | 573 |  |
| ISRG_US_Equity | 35 | 3 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 5 | 4527 | 608 |  |
| JD_US_Equity | 34 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4612 | 675 |  |
| KMB_US_Equity | 39 | 5 | 2 | 6 | 2 | 1 | 4 | 4 | 2 | 1 | 0 | 3 | 5413 | 600 |  |
| KOFUBL_MM_Equity | 41 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4936 | 640 |  |
| KPN_NA_Equity | 31 | 3 | 1 | 6 | 2 | 2 | 4 | 4 | 2 | 0 | 0 | 5 | 4576 | 582 |  |
| LLY_US_Equity | 53 | 3 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 5 | 6542 | 831 |  |
| MA_US_Equity | 45 | 3 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 5 | 5171 | 759 |  |
| MELI_US_Equity | 40 | 3 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 5 | 5163 | 602 |  |
| MER_PM_Equity | 41 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4840 | 643 |  |
| ML_FP_Equity | 31 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4140 | 556 |  |
| MNST_US_Equity | 41 | 3 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 5 | 4831 | 614 |  |
| MSCI_US_Equity | 37 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4560 | 546 |  |
| NESN_SW_Equity | 41 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 5021 | 698 |  |
| NFLX_US_Equity | 43 | 3 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 5 | 5285 | 748 |  |
| NG/_LN_Equity | 43 | 3 | 1 | 6 | 2 | 3 | 4 | 4 | 2 | 0 | 0 | 5 | 5264 | 739 |  |
| NKE_US_Equity | 35 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4289 | 741 |  |
| NOKIA_FH_Equity | 37 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4583 | 722 |  |
| NOVN_SW_Equity | 53 | 3 | 1 | 6 | 2 | 2 | 4 | 4 | 2 | 0 | 0 | 5 | 6991 | 882 |  |
| NOW_US_Equity | 43 | 3 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 5 | 5690 | 682 |  |
| NU_US_Equity | 33 | 5 | 4 | 6 | 2 | 1 | 4 | 4 | 2 | 1 | 0 | 0 | 5342 | 661 |  |
| OMAB_MM_Equity | 37 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4281 | 607 |  |
| ORA_FP_Equity | 32 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4617 | 597 |  |
| PBR_US_Equity | 44 | 5 | 2 | 6 | 2 | 2 | 4 | 4 | 2 | 1 | 0 | 3 | 5989 | 814 |  |
| PWR_US_Equity | 45 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4895 | 745 |  |
| QXO_US_Equity | 33 | 3 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 5 | 4608 | 592 |  |
| RIO_LN_Equity | 43 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4849 | 670 |  |
| RKT_LN_Equity | 40 | 3 | 1 | 6 | 2 | 2 | 4 | 4 | 2 | 0 | 0 | 5 | 5213 | 722 |  |
| RMS_FP_Equity | 33 | 3 | 1 | 6 | 2 | 2 | 4 | 4 | 2 | 0 | 0 | 5 | 4696 | 710 |  |
| ROG_SW_Equity | 49 | 3 | 1 | 6 | 2 | 2 | 4 | 4 | 2 | 0 | 0 | 5 | 5750 | 966 |  |
| RWE_GR_Equity | 40 | 3 | 1 | 6 | 2 | 2 | 4 | 4 | 2 | 0 | 0 | 5 | 5440 | 710 |  |
| SAN_FP_Equity | 41 | 2 | 1 | 6 | 3 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 5218 | 761 |  |
| SAP_GY_Equity | 41 | 5 | 4 | 6 | 2 | 1 | 4 | 4 | 2 | 1 | 0 | 0 | 5204 | 702 |  |
| SHOP_CN_Equity | 53 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 6469 | 749 |  |
| SLB_US_Equity | 35 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4365 | 634 |  |
| SNPS_US_Equity | 51 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 5975 | 707 |  |
| SPOT_US_Equity | 45 | 3 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 5 | 6236 | 716 |  |
| SSE_LN_Equity | 35 | 3 | 1 | 6 | 2 | 2 | 4 | 4 | 2 | 0 | 0 | 5 | 4566 | 699 |  |
| ST_SP_Equity | 37 | 3 | 1 | 6 | 14 | 2 | 4 | 4 | 2 | 0 | 1 | 5 | 5477 | 767 |  |
| TSM_US_Equity | 57 | 3 | 1 | 6 | 13 | 2 | 2 | 4 | 1 | 0 | 1 | 5 | 7792 | 817 |  |
| TTE_FP_Equity | 42 | 2 | 1 | 6 | 3 | 2 | 2 | 4 | 1 | 0 | 1 | 3 | 5414 | 739 |  |
| UBER_US_Equity | 43 | 3 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 1 | 5 | 5916 | 730 |  |
| UBSG_SW_Equity | 37 | 2 | 1 | 6 | 14 | 2 | 2 | 4 | 1 | 0 | 1 | 3 | 5924 | 862 |  |
| ULVR_LN_Equity | 42 | 3 | 1 | 6 | 14 | 2 | 4 | 4 | 2 | 0 | 1 | 5 | 6538 | 698 |  |
| UNH_US_Equity | 43 | 3 | 1 | 6 | 14 | 2 | 2 | 4 | 1 | 0 | 1 | 5 | 5833 | 742 |  |
| UNVGY_US_Equity | 32 | 3 | 1 | 6 | 3 | 2 | 2 | 4 | 1 | 0 | 0 | 5 | 4705 | 607 |  |
| VIVT3_BZ_Equity | 41 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 5895 | 619 |  |
| VLO_US_Equity | 35 | 5 | 4 | 6 | 2 | 1 | 4 | 4 | 2 | 1 | 0 | 0 | 5329 | 693 |  |
| V_US_Equity | 45 | 3 | 1 | 6 | 13 | 2 | 2 | 4 | 1 | 0 | 0 | 5 | 6525 | 745 |  |
| WALMEX*_MM_Equity | 41 | 3 | 1 | 6 | 14 | 2 | 4 | 4 | 2 | 0 | 0 | 5 | 6462 | 602 |  |
| WDAY_US_Equity | 41 | 3 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 5 | 5594 | 665 |  |
| ZTS_US_Equity | 33 | 2 | 1 | 6 | 2 | 2 | 2 | 4 | 1 | 0 | 0 | 3 | 4814 | 638 |  |
| ZURN_SW_Equity | 37 | 3 | 1 | 6 | 2 | 2 | 4 | 4 | 2 | 0 | 0 | 5 | 5555 | 678 |  |
| **all 95** | 3786 | 269 | 126 | 585 | 387 | 527 | 256 | 380 | 128 | 12 | 15 | 444 | 600310 | | |

**Lambda overlay, warm (94 names) and the one cold start:** handler median 682 ms, p95 974, max 2422; the cold start (1299_HK_Equity, Init 704 ms): handler 2,422 ms (feed 1,370, peers 272, identity 161, axis_reads 174, model_block 121, top_band 104). ASML_NA_Equity's driven first request on the new package (RA1, 18:56Z): handler 3,770 ms, Init 534, feed 1,776, peers 1,001: ASML's peer set is large, 1299_HK's is small, which is where the 1.3 s between the two cold readings sits.

**What this table does not say:** it does not grade FWD-40 (c); the six pulls the PRD names are corpus, filings, management, news, price, scanner, and the instrument also prints posture, peers, scores, drafting, coverage and `other` (444 calls, 135 prefixes: the silver `filing_source` prefixes and the bronze `exec_officers` objects, the worker's row S2) rather than fold them. `scanner` here is the Bloomberg `refdata` and `segments` objects and the classification tables (the mapping is stated in `r103_pull_census.py`).
