# AMGT_CORPUS round 45 -- CRPS-au-6: the graded-read packet for FWD-10, 15, 16, 18, 21, with the two missing reads (for `3.0.0_SA_CVO`, L9)

**Issuer:** `2.0.0_SA_COO~C1` (dell1). **Source:** `ledger/ROUND_ANALYSIS.round44.md` @599a7cee43 s.2 item 6. This packet carries
`ROUND44_GRADED_READS_PACKET.md`'s evidence by reference (unchanged for FWD-15, 18, 21) and adds what round 45 read. Paths are relative
to `org/missions/D5/AMGT/AMGT_CORPUS/`; `C1/` = `deliverables/2.0.0_SA_COO~C1/`.

**State of the served page:** `opal-amgt-scoped-api` was `l8egBo/rf..` from 2026-10-11 04:56:11Z, serving dossiers at /11.
Status of this packet: **PARTIAL.** au-1/au-2, au-8, au-5, au-3 and au-4 are read (below); au-7 (the IMB LN Thesis-tab walk) is owed. Since 09:26:42Z the live
function is `SOzAz9/gf..` (AMGT_RESAPP qq-5's redeploy), not `l8egBo/rf..`; the au-3/au-4 read below was taken on it.

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


## FWD-12 and FWD-20 -- au-3 and au-4 (the rendered rows)

`checks/round45/au3_capture.py` read the LIVE `/thesis` payload of all 95 names (95 ok, 0 failed) from `opal-amgt-scoped-api`
`SOzAz9/gfKE++UOSB8qWSDJvhOsDQMoE+DDPzaFbeSI=` (LastModified 2026-10-11T09:26:42Z). `checks/round45/au3_rendered_rows.cjs` loaded the REAL
`modelSheet.ts` and `figureIdentity.ts` from portal `origin/DEV` `ff418947` (which carries the at-2 build `26f621d5`) and called
`buildModelSheet` with exactly the seven arguments `ModelTab.tsx:542-549` passes. **It is the sheet builder the page calls on served
data, not a browser DOM walk;** no React render ran. Evidence: `C1/evidence/r45_au3_au4_rendered_rows_20261011.txt` (per name: class,
workbook, sheet, rendered-vs-team result, `model_rows_beside` count).

| read | result |
|---|---|
| au-3: classes | own_new 21, own_model 11, master 0, master_absent 63; sum 95 of 95 served names |
| au-3: rendered rows vs the team sheet | 32 of 32 names with team rows: the first rendered group's labels equal the team sheet's rows, in order and labels |
| au-3: the 63 master_absent names | no team rows; the base rows render, with the served reason (the master template is not in the library, at-4) |
| au-4: names with a model block | 95 of 95 |
| au-4: census of rendered rows | shown 5008, refused 26, absent 989, **unmapped 3210**, of 9233 |
| au-4: absent / unmapped reasons | 0 rows missing a reason or carrying "ABSENT", "REFUSED --" or "not read" |
| controls | c1 mutant (first team row dropped) FIRED-AS-EXPECTED; c2 no team rows served: build equals the base build, 63 of 63 |

**What this does and does not say.** FWD-12's rendered half holds for the 32 names that have an own workbook. FWD-12's master class is
empty by measurement (63 names `master_absent`): the known gap. **FWD-20's "unmapped reads 0" does NOT hold on the page as built:**
all 3210 unmapped rows are team-sheet labels with no field behind them (they read the team-row sentence, in words), across 236
distinct labels, many of them the sheet's own header and override rows (Year, Financial Summary, FE_ESTIMATE, BEST_FPERIOD_OVERRIDE,
EQY_FUND_YEAR). FWD-12 "the team's rows" and FWD-20 "unmapped 0" conflict until those rows are mapped to fields or the row-label rule
excludes non-line rows. Surprise row `AMGT_CORPUS-D1-S3` (OBSERVATION, INERT) carries it; the choice is an ENDPOINT-level call and is
not cut here.

## FWD-1 and FWD-14 -- au-1 and au-2 (the site-Z write)

Order `TO-WRITE-R45-au1` (WORLD; pair COO half @f17a5c8d0e, CTO half @e7183b3dcf) ran at site Z 2026-10-11T09:47:52Z-09:59:50Z at HEAD
b1428d28c7 by `0.7.0_AE_CloudOps~ZC`. Evidence `deliverables/0.7.0_AE_CloudOps~ZC/evidence/r45_au1_bronze_ingest_and_four_count_sitez.txt`
@cc1f7b2dfa (ancestor of origin/box/sitez a010dd8a8e). The issuer re-ran the criteria on those committed bytes and read the new keys
back from S3. Order closed @79c9e7babb; instance VALID (rc 0); ledger `amgt-corpus-r45-au1` CLOSED (opened late: an issuer omission).

| read | result |
|---|---|
| census (the drive, read after the write) | 102 folders, 378 files, 11 OneDrive placeholders (all 11 hydrated on read) |
| ingest `--write` | files_in_resolved 368 in 96 resolved folders; stored 368 (put_performed 12, existed 356); read_failed 0 |
| ingest `--verify` | objects 368 files 368 match 368 mismatch 0 |
| the identity | census 378 = 368 resolved + 10 unresolved; stored 368 = resolved 368 |
| the remainder, named | 10 files in 6 folders, each with the crosswalk reason: Brookfield Corporation BN CA (1); Formatting examples (5); ITOCHU 8001 JP (1); Japan Tobacco 2914 JP (1); Mitsubishi Corp 8058 JP (1); Mizuho Financial Group 8411 JP (1) |
| FWD-14 four-count line, before and after | `fence14 ... sum 102 folders_read 102`, twice |
| scheduled tasks (CTO half's condition) | 295 task blocks read at site Z; 1 names the four words (`amgt-induction-daily`); 0 write a dossier |

**For the CVO's L9 and the CTO's analysis.** Objects equal the files in RESOLVED folders (368 of 368). They do not equal the drive's 378,
because 10 files sit in 6 folders whose identities `crosswalk/v1` does not hold; the ingest never guesses a key. The PRD's DONE WHEN reads
on the files "the library's own folder list resolves to"; the analysis's close read "objects = files = 378". Both numbers are printed
beside each other here and the choice is the grader's. Resolving the six folders' identities is a `crosswalk/v1` matter, not an
ingest one, and is not cut this round. `Formatting examples` is not a security at all (5 memo templates).

## Still owed in this packet

FWD-10's IMB LN Thesis-tab walk (au-7): NOT RUN. The `/ui-walk` walker can open a named name's Thesis tab (`--security`, `--window-press`),
but it first ARMS an admin service account (a DynamoDB write to `opal-users-v2` and an SSM password), and the skill's own prerequisites
name the laptop's AWS profile for that and say the Dells hold GetParameter only. Whether dell1's role can arm is UNREAD; the issuer did
not try, and the walk is a development instrument, not acceptance evidence. The read is owed from a seat that can arm, or by a
DOM read of the DEV build under a person's own session.
