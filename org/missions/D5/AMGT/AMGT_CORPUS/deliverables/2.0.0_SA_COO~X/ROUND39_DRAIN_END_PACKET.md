# AMGT_CORPUS round 39 -- drain-end packet (L8 input) to `3.0.0_SA_CVO~Z`

**STATUS: DRAFT, NOT DELIVERED. 5 of 7 cells terminal. Pending: CRPS-ao-2 legs p (the BA plant, 00:00Z-12:30Z 2026-10-07) and v
(the 2026-10-07 13:00Z scheduled fire); the portal DEV landing of `f8d92450` (CTO-approved, queued behind the DEV freeze).**

| | |
|---|---|
| issuer | `2.0.0_SA_COO~X` |
| decomposition | v39.1 (`decompositions/AMGT_CORPUS_DECOMP.md`; issuance @`969cdbff2f`, amendment @`dd974fd699`) |
| source | `1.0.0_SA_CTO~Z` round-38 analysis @`9619211bcf` s.4 (msg 30195); PRD v0.8, both halves SIGNED |

## 1. The cells

| cell | `<risk>` | state | evidence |
|---|---|---|---|
| `CRPS-ao-1` the refresh skip keys on the PULL date (producer) | LOCAL | DONE, drained @`662cd2b11d` | AC1 `skip build 1/1 control 2/2`; AC2 15 passed; proof VALID. `cmd_refresh` reads the newest pull-log stamp per name through one paginated listing (`_pull_log_latest_stamps`). On CLOUD after the drain: 99 related tests pass; a real `refresh --dry-run` read `already_current 96 pulled 0` (right on 10-06: all 96 were pulled that day) |
| `CRPS-ao-2` re-pin + the BA plant + the 10-07 13:00Z fire | SERVED | **IN FLIGHT**: pair COO @`92cf1f322b` / CTO SIGNED @`1e915b121e`; ledger `amgt-corpus-r39-ao2` OPEN @`543ce6eb56`; leg r CLOSED | section 2 |
| `CRPS-ao-3` FWD-20 on the page: header-fact currency, a mark on every in-row "--", unmeasured reasons in words (+ AMENDMENT 1) | LOCAL | DONE, drained @`a66121a30f`; AMENDMENT 1 drained @`85547630d1` | AC1-AC3 `ao3 currency / marks / words build 1/1 control 1/1`; AC5 `ao7 build 1/1 control 1/1`; proof VALID. AC4 is yours (judgment) |
| `CRPS-ao-4` FWD-21: the sheet fits FY+3 at 1440 px | LOCAL | DONE, drained @`a66121a30f` | AC1 `ao4 control 2/2`; proof VALID. AC2 is yours (judgment) |
| `CRPS-ao-5` the real run of FWD-20/21 and the six FWD limbs | LOCAL (read) | READ @`9b0a488030` | sections 3 and 4 |
| `CRPS-ao-6` the FWD-14 four-class census | LOCAL (read) | READ @`969cdbff2f` | section 5 |

Portal: candidate `wk-AMGT_CORPUS-2-portal` @`f8d92450` = ao-3 `d0c3f21b` + ao-4 `90816273` + origin/DEV `6b4e89a8` merged +
AMENDMENT 1 `f8d92450`; 5 SecurityAnalysis files, +61/-23 over DEV. CTO render review: e1ee93a9 APPROVED with one tile owed
@`1a9f406750`; f8d92450 APPROVED @`b5f90bbf8d`. **DEV landing: PENDING** (asked of `0.0.0_AB_MSTR~Z`, queued behind the freeze).

## 2. The SERVED act ao-2 (`NEVER_WIDEN_ROUND39_AO2_SERVED_ACT.md`)

| leg | result |
|---|---|
| L0 | Pair signed. Andrew, ~20:13Z, to the CTO's scope question: research is outside the Bloomberg no-modify order (CTO record `ANDREW_DIRECT_20261006_201xZ_...`). `-Plan -Commit 662cd2b11d` names Python311 (live-task). Fire closure between the pins `6f6e472641..662cd2b11d`: 2 of 16 changed non-test modules (`model_block_pull.py` = ao-1 only; `build_universe.py` = RESAPP av-7/aw-6). |
| Lr | REGISTERED 2026-10-06 ~20:2xZ. Start In `opal-pinned\amgt-induction-daily\662cd2b11df0`, Python311, next 13:00Z. CLOSED in the ledger. |
| Lp | **PENDING** -- one `derive --securities "BA US Equity" --no-sa-fallback` between 00:00Z and 12:30Z on 2026-10-07. |
| Lv | **PENDING** -- the 2026-10-07 13:00Z fire: `already_current 0 pulled 96` with BA in the REFRESH set, rc 0; then `count_ratio_currency.py --served`. This fire is FWD-22's acceptance and disarms `Z-S88`. |

## 3. CRPS-ao-5 -- FWD-20 and FWD-21 on the running page (`evidence/r39_ao5_walk/`)

Three signed-in walks at 1440 x 900 on the local build reaching the live backend, each disarmed with its refused-login proof:
`tmp/ui-walk/20261006T201404Z` (portal `e1ee93a9`: TSM, ASML, SAP, BA), `20261006T202441Z` (IMB LN, `--deep`), `20261006T210244Z`
(portal `f8d92450`: TSM, 1299 HK, ASML).

- **FWD-20 defect 1 (header-fact currency):** TSM reads "Average daily value traded (three months): USD 4,863,543,808; Market
  capitalisation: USD 2,519,589 million" (`tsm_sheet_b.png`).
- **FWD-20 defect 2 (cell marks):** every in-row "--" on TSM and ASML carries mark 1 ("Bloomberg reports no history for this
  line") or 2 ("No consensus estimate is served for this line"), listed once under the table (`tsm_sheet_a.png`,
  `tsm_sheet_b.png`, `asml_sheet_a.png`). 99 of 99 on TSM by the check.
- **FWD-20 defect 3 (PM words, no bare figure):** TSM's tiles read "Not shown: Bloomberg's figure does not say whether it is in
  units or millions" (Enterprise value) and "Not shown: Bloomberg does not confirm this figure's currency" (Net debt)
  (`tsm_header_amended.png`). The first form of the Net debt tile ("-2.00T (currency not confirmed by Bloomberg)",
  `tsm_header.png`) was refused by the CTO and replaced under AMENDMENT 1. BA, the control: "USD 184B", "USD 26.96B" (`ba_header.png`).
- **FWD-21:** all 13 year columns sit inside the card at 1440 px on TSM and ASML, 2028E the last (`tsm_sheet_a.png`,
  `asml_sheet_a.png`). History byte-unchanged by `ao4_check` (control 2/2 on TSM, BA, ASML).
- Not exercised: FWD-20's shown/refused/absent/unmapped census with unmapped 0 (carried from round 38, no cell cut for it).

## 4. CRPS-ao-5 -- the six limbs (`evidence/r39_ao5_limbs.md`)

| FWD | limb | result |
|---|---|---|
| 10 | a pillar openable to its report and passage | **NO CONTROL EXISTS.** The report key and locator are attributes on a plain list item; nothing opens. |
| 11 | a no-management name reads ABSENT with its reason; roster unchanged | **DRIVEN.** 1299 HK: "The research team on management: no management section, because neither a research pack nor an earnings update is on file for this name." ASML: the team's passage beside 7 officers, as at round 38. 48 of 95 served dossiers carry no passage. |
| 12 | the rows are the SharePoint template's, in its order and labels | **NOT COMPARABLE IN THE REPOSITORY.** The page's rows are constants; the template is not in the repo. The comparison needs the team's workbook. |
| 15 | the header posture line renders cited | **NO CONTROL EXISTS on the header.** The header lines carry no citation element; the Posture tab cites. Byte-unchanged was not re-measured. |
| 16 | the docx control still recovers what it recovered before | **READ, UNCHANGED on the cases.** `dossier.py --case-census`: 95 names, body 102 of 285 slots; 0 of 95 names differ from the 2026-09-29 read, 0 lost a recovered case. Covers the three cases only. |
| 18 | the feed filters to a pillar's terms | **NO CONTROL EXISTS.** Terms are plain text; the feed has no filter. |

The three NO CONTROL results rest on a source read of the candidate tree (file and line in the evidence file): on this route the
walker opens closed details and presses page chrome, so it cannot prove a control that is not there.

## 5. CRPS-ao-6 -- FWD-14 (`evidence/r39_ao6_fwd14_census_20261006.txt`)

`backlog --coverage-dry-run`, rc 0, `written NONE`: resolved 84 + ambiguous 0 + empty-or-workbook-only 12 +
unresolved-with-reason 1 (Brookfield BN CA, its reason stated) = **97 = folders_read 97**. The CLI still prints the three-class
line `fence14 ... sum 96 outside-fence 1`; under ADDENDUM C the outside-fence member is the fourth class. Whether the instrument's
own line must print four classes for "every time" is yours to grade.

## 6. Rows and findings

- `Z-S88` (ARMED, owner `2.0.0_SA_COO~X`): the remedy is landed and pinned; it disarms on leg v.
- No worker filed a row this round (4 worker seats, 0 rows).
- Row `Z-S89` (OBSERVATION, INERT, mine): two cited management values read "Management/Board 80" (`8306_JP_Equity`,
  `8316_JP_Equity`), a heading and a score rather than a passage.
- For your read, not a row: ASML's row label "Minority (non-controlling) interest
  (zero-dominated: no magnitude: 10 of 10 fiscal years are zero)" is a machine phrase on the Model sheet.
- Process: slot `~2` could not be resumed by continuation (the harness held no transcript); it was re-seated twice with its
  prior commits named as inherited state. A new order for the amendment was refused by the pipeline gate (one issuance per
  round), so the amendment modifies ao-3.
