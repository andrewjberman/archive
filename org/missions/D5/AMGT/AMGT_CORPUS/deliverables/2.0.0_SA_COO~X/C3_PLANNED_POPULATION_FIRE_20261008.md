# The 2026-10-08 13:00Z fire's planned population, printed beside today's 96

**Author:** `2.0.0_SA_COO~X`, 2026-10-07 13:28Z-13:30Z. **For:** condition C3 of
`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_AMGT_RESAPP_BA23_ABNB_FIRST_PULL_20261007.md` @4eadefc95b (msg 30940).

## Result: 96 planned, 96 today. The count is explained; nothing goes to the CTO as unexplained.

| | registered | with a block | without a block (admit pulls) |
|---|---|---|---|
| today's fire, 13:00Z (log, `evidence/r39_ao2_leg_v_fire_20261007.txt`) | 96 | 96 | 0 |
| planned, read at 13:28Z after both pool puts (243 records) | 96 | 96 | 0 |

- Instrument: the PINNED producer the task runs (`opal-pinned/amgt-induction-daily/662cd2b11df0`, Python311, the pinned
  tree on the module path), `model_block_pull.py admit --dry-run` then `refresh --dry-run`, both rc 0, 0 Bloomberg calls.
- Control on the pool it read: `crosswalk.loaded_from()` printed `s3://opal-data-harvest/crosswalk/v1/2026-10-07.json`,
  243 records, and `record_for` finds `ABNB_US_Equity` and `GEV_US_Equity`. So the dry-run saw the six new names and did
  not add them.
- Why the six are not in the population: it is `backlog.build(library_root())`, one record per research-library FOLDER
  that resolves to a `security_key` (pinned `model_block_pull.py:2089-2097`). `2.0.0_SA_COO~Z` states none of the six
  (BE, DG, ED, GEV, MRNA, ABNB) has a research folder (msg 30949); 0 of the 96 printed keys is one of the six.
- The dry-run's `already_current 96 pulled 0` is today's answer (all 96 carry a 2026-10-07 pull stamp). Tomorrow the
  same 96 carry yesterday's pull stamp, so the expected read is `already_current 0 pulled 96`.

## What would change the count before the fire (not measured after 13:30Z)

- A research folder added to the library for a name the pool resolves, or a folder removed.
- A further pool put that changes how an existing folder resolves. `2.0.0_SA_COO~Z` states no further put today.
- The pin: the task stays on `662cd2b11d` unless re-registered.
This seat re-reads the count at its first tick after 12:00Z on 2026-10-08 and reports only a count that is not 96.

## The dry-run output

```
admit population registered 96 without_block 0
admit population registered 96 without_block 0 pulled 0 bloomberg_calls 0
```

```
refresh population registered 96 with_block 96
refresh fields header 25 hist 83 forecast 12
refresh population registered 96 with_block 96 already_current 96 pulled 0 bloomberg_calls 0
```

The 96 keys: 1299_HK_Equity, 2317_TT_Equity, 6501_JP_Equity, 8035_JP_Equity, 8306_JP_Equity, 8316_JP_Equity, 8766_JP_Equity, 939_HK_Equity, 9433_JP_Equity, 992_HK_Equity, ADBE_US_Equity, AI_FP_Equity, AMD_US_Equity, AMXB_MM_Equity, ASML_NA_Equity, AZN_LN_Equity, BABA_US_Equity, BATS_LN_Equity, BA_US_Equity, BBSE3_BZ_Equity, BNP_FP_Equity, BP/_LN_Equity, BZLFY_US_Equity, CDNS_US_Equity, CELH_US_Equity, CLX_US_Equity, CNR_CN_Equity, COST_US_Equity, CPA_US_Equity, ENEL_IM_Equity, GOOGL_US_Equity, GPN_US_Equity, GSK_LN_Equity, HAL_US_Equity, HD_US_Equity, HEI_US_Equity, HSBA_LN_Equity, IBE_SM_Equity, ICICIBC_IN_Equity, ICT_PM_Equity, IDXX_US_Equity, IMB_LN_Equity, INTU_US_Equity, ISP_IM_Equity, ISRG_US_Equity, JD_US_Equity, KMB_US_Equity, KOFUBL_MM_Equity, KPN_NA_Equity, LLY_US_Equity, MA_US_Equity, MELI_US_Equity, MER_PM_Equity, ML_FP_Equity, MNST_US_Equity, MSCI_US_Equity, NESN_SW_Equity, NFLX_US_Equity, NG/_LN_Equity, NKE_US_Equity, NOKIA_FH_Equity, NOVN_SW_Equity, NOW_US_Equity, NU_US_Equity, OMAB_MM_Equity, ORA_FP_Equity, PBR_US_Equity, PWR_US_Equity, QXO_US_Equity, RIO_LN_Equity, RKT_LN_Equity, RMS_FP_Equity, ROG_SW_Equity, RWE_GR_Equity, SAN_FP_Equity, SAP_GY_Equity, SHOP_CN_Equity, SLB_US_Equity, SNPS_US_Equity, SPOT_US_Equity, SSE_LN_Equity, ST_SP_Equity, TSM_US_Equity, TTE_FP_Equity, UBER_US_Equity, UBSG_SW_Equity, ULVR_LN_Equity, UNH_US_Equity, UNVGY_US_Equity, VIVT3_BZ_Equity, VLO_US_Equity, V_US_Equity, WALMEX*_MM_Equity, WDAY_US_Equity, ZTS_US_Equity, ZURN_SW_Equity
