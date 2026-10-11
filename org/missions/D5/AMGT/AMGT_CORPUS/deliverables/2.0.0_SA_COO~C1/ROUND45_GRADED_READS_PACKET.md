# AMGT_CORPUS round 45 -- CRPS-au-6: the graded-read packet for FWD-10, 15, 16, 18, 21, with the two missing reads (for `3.0.0_SA_CVO`, L9)

**Issuer:** `2.0.0_SA_COO~C1` (dell1). **Source:** `ledger/ROUND_ANALYSIS.round44.md` @599a7cee43 s.2 item 6. This packet carries
`ROUND44_GRADED_READS_PACKET.md`'s evidence by reference (unchanged for FWD-15, 18, 21) and adds what round 45 read. Paths are relative
to `org/missions/D5/AMGT/AMGT_CORPUS/`; `C1/` = `deliverables/2.0.0_SA_COO~C1/`.

**State of the served page:** the live `opal-amgt-scoped-api` is `l8egBo/rf..` (applied 2026-10-11 04:56:11Z), serving dossiers at /11.
Status of this packet: **PARTIAL.** au-8 is read (below); au-7 (the IMB LN walk) waits on the walk with au-3.

| outcome | missing read (round 44 packet) | state | evidence |
|---|---|---|---|
| FWD-16 | the census on the written /10 | **READ**, on /10 and on the served /11 beside it | `C1/evidence/r45_au8_fwd16_census_v10_20261011.txt`, `..._v11_20261011.txt` |
| FWD-10 | IMB LN Thesis-tab walk, one pillar opened to its passage | OWED (au-7, the walk) | -- |
| FWD-11 | (analysis item 4, `CRPS-at-5`) officer comparison, SAP GY and BABA US | **READ** (au-5) | `C1/evidence/r45_au5_roster_compare_20261011.txt` |

## FWD-16 -- PRD:521-523 -- au-8

`ap8_fwd16_census.py` (round 40, unchanged) run through `checks/round45/au8_fwd16_census.py`, which sets `dossier.METHOD_VERSION` and
then runs it. 95 names resolved, 95 compared, 0 without a base. The /10 and /11 outputs are identical line for line (115 lines each).

| slot | PDF shape (48 names) | docx shape, the control (25 names) | mixed (4) | no pack (18) |
|---|---|---|---|---|
| pillars | KEPT 32, NONE 16 | KEPT 10, NONE 15 | KEPT 4 | NONE 18 |
| management | KEPT 29, CHANGED 3, NONE 16 | KEPT 7, CHANGED 2, LOST 2, NONE 14 | KEPT 4 | NONE 18 |
| cases | KEPT 32, NONE 16 | NONE 25 | KEPT 2, NONE 2 | NONE 18 |

- **The /9 defect is gone on /10 and /11:** round 44's /9 census read cases LOST 3->0 on six PDF names (row D1-S2); both runs read cases
  KEPT 32 on PDF and LOST 0.
- **The docx control still recovers what it did:** pillars KEPT 10 with none LOST. LOST 2 is management on `8306_JP_Equity` and
  `8316_JP_Equity`, the round-40 Z-S89 removals (absent with a reason), unchanged between /9, /10 and /11.
- NONE means the slot was empty at the base date and is empty now; it is not a loss.
- This reads the STORED dossiers the served reader picks at the named method. The rendered page is au-3's.

## FWD-11 -- PRD (round-39 ruling 5) -- au-5

`checks/round44/at5_roster_compare.py`, run unchanged 2026-10-11. Per name, the served `scoped_amgt.read_management(key)["officers"]`
against `roster.derive_roster(...)` of the persisted filing, by content, and each served name against the filing text verbatim.

| name | served | filing parse | same names | same roles | in text | order |
|---|---|---|---|---|---|---|
| SAP GY | 6 | 6 | 6 | 6 | 6 | same |
| BABA US | 7 | 7 | 7 | 7 | 7 | differs (printed, not graded: the served list leads with the CEO) |

`at5 unchanged 2/2`. **Limit, stated:** `scoped_amgt` ran as the local module at this checkout's HEAD against the store, not the live
function. The live function's build is the pin a943b1b412; this read does not exercise it. The outcome is the CTO's to grade.

## Still owed in this packet

FWD-10's IMB LN walk (au-7) and, for FWD-12 and FWD-20, the rendered reads (au-3, au-4): the DEV build is `ff418947`, which carries the
at-2 build `26f621d5` (measured 2026-10-11).
