# AMGT_RESAPP round 104 -- drain-end packet SKELETON (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: SKELETON, 2026-10-14 ~00:3xZ. NOT SENT.** Section 1 holds what is measured at this commit; every cell marked `PENDING` is filled from a read, never from a plan. The packet is renamed
`DRAIN_END_PACKET.md` and sent when every order of the round (all workstreams: this seat's workstream-less key and `LAND`, and `~R2`'s `AIFILL`) is terminal.

## 1. Orders, cells and the issuer acts

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-bk-1` | the overlay prints sub-phase lines; its top band reuses the feed rows | complete, merged | 13 `AMGT_SUBPHASE` lines; byte-equal arms |
| `AMGT-bk-4` | the served fiscal P/E is price over reported EPS of the same year (same currency, or a minor unit scaled by 100) | complete, merged | `r104_pe_check.py` 6 of 6 arms; names 95: 464 derived, 154 withheld with a reason |
| `AMGT-bk-3` | USD prints `$`; every dash tile shows its reason (portal candidate `3dcbb6ef`) | complete | portal `624e2533f6` on `cand/dell1/amgt-sa-header-money-and-dash-reasons` |
| `AMGT-bk-6` (LAND) | the bk-3 feature cut from PROD `10e7664d`, registered, merged forward | complete @2953d068a7 | worker ~417; AC1-AC3 re-run by the issuer; row `dell1-20261014T001511Z-633a` CLOSED APPROVED (CTO msg 5289); DEV `5e40e54119` (MSTR msg 5293); PROD promote PENDING (no DT live; CTO to name the serial) |
| `AMGT-bk-2` | the redeploy carrying bk-1 and bk-4 from pin `d7a79c766a`, and the first cold request | applied 00:07:07Z by RA1 (`Wkt48Y6v...`); first cold request `26780d80`, handler 2,910.88 ms, Init 675.26 ms; AC1-AC3 re-read by the issuer PENDING (RA1 holds readers) | `deliverables/0.7.0_AE_CloudOps~RA1/BK2_FIRST_COLD_REQUEST.txt` |
| `AMGT-bk-5` | census re-run (93 names) and the ten-name walk after bk-2 and the bk-6 promote | PENDING (not cut) | cut after bk-2 is released and bk-6 is on PROD |

## 2. The issuer's real runs

PENDING: bk-2 split table (`r104_split_table.py --id-file BK2_FIRST_COLD_REQUEST.txt`); bk-5 census and walk (`r103_section_census_v2.py`, `r103_walk_draw.py`, `r104_walk_classes.py`).

## 3. WHAT THE READINGS SAY

PENDING. FWD-40 (b) is graded by the CVO; the first cold handler 2,910.88 ms is below the 3,000 ms line the round-103 packet used (`--handler-max-ms 3000`) on ONE request, not yet on the split.
