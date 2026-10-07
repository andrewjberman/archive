# AMGT_RESAPP round 77 -- GROUP E draft notes (measurement, deploy, pulls, walk), `2.0.0_SA_COO~Z`, 2026-10-07 ~00:5xZ

Drafted from the CTO's round-76 analysis @c8bbeeac10. Nothing here is committed by the drafting fork; the parent assembles s.85.

## 1. Cells

| id | cell | slot / seat | wave | risk | order file |
|---|---|---|---|---|---|
| AMGT-ba-19 | the chatter phase-COVERAGE read (ruling 4, Z-S360) | ~285 | 0 | LOCAL (a read) | `AMGT_RESAPP.TO-AMGT-ba-19.chatter-phase-coverage-read.md` |
| AMGT-ba-25 | the research-pull driver (segments, officers), on fakes | ~287 | 0 | LOCAL | `AMGT_RESAPP.TO-AMGT-ba-25.research-pull-driver.md` (ADDED by this group: no segment producer exists) |
| AMGT-ba-26 | row Z-S242, the LF re-commit | 0.7.0_AE_CloudOps~A | 0 (staged, no dependency) | WORLD by the infra/ floor; applies nothing | `AMGT_RESAPP.TO-AMGT-ba-26.etf-classifications-lf-recommit.md` |
| AMGT-ba-20 | the round-77 code redeploy | 0.7.0_AE_CloudOps~A | after every build cell drains + its pair | WORLD | `AMGT_RESAPP.TO-AMGT-ba-20.the-code-redeploy.md` |
| AMGT-ba-21 | the segment pull, 83 names (ruling 8, Z-W240-S1) | the issuer's paired act (NO order) | after ba-25 drains; after the 07:00 ET vehicle | SERVED | section 2 |
| AMGT-ba-22 | the officer pull, 84 names (Z-W227-S1) | the issuer's paired act (NO order) | after ba-21 is read | SERVED | section 2 |
| AMGT-ba-23 | FWD-2's first uncovered-name pull | the issuer's paired act (NO order) | after ba-22 is read | SERVED | section 2 |
| AMGT-ba-24 | the walk on DEV | ~286 | last: after ba-20, the portal DEV push and ba-21's read | LOCAL (a read) | `AMGT_RESAPP.TO-AMGT-ba-24.the-walk-on-dev.md` |

Edges: ba-25 -> ba-21 -> ba-22 -> ba-23 (one at a time, Andrew's condition); every build cell -> ba-20 -> ba-24; ba-21 -> ba-24
(AMD re-read); ba-21 -> the served segment read (NOT in this group: the cell that owns `read_segment_breakdown` and ruling 7's
refusal must read the new `segments` bronze, or FWD-1 on AMD cannot change). ba-19 and ba-26 have no edge.

## 2. The three pulls are ISSUER PAIRED ACTS, with no order file

- **Precedent, measured:** AMGT_CORPUS runs its Bloomberg research pulls as "the issuer's paired act (no order)"
  (`decompositions/AMGT_CORPUS_DECOMP.md:15,110`, CRPS-ao-2; round 38's an-3 entry
  `org/critical_paths/change_management/20261006T1318Z_amgt-corpus-r38-an3-pull_deploy_completion.md`, "Authored by: 2.0.0_SA_COO~X",
  legs L0 probe (blp.health, no data call) / Lp pull / Lv verify; 96 names, `bloomberg_calls 768`, rc 0). The L6 gate refuses an
  `<issued_to>` naming a Tier-1 seat, so the COO's own act carries a SERVED_ACT half
  (`deliverables/2.0.0_SA_COO~X/NEVER_WIDEN_ROUND39_AO2_SERVED_ACT.md` is the shape) and a NEVER-2 entry, not an order.
- **Authority:** `ANDREW_DIRECT_20261006_211xZ_ALL_RECS_APPROVED_CTOZ_OPEN_CALLS_FOUR_CARDS.md` ruling 1 (three named pulls, not a
  standing word); conditions in `ledger/ROUND_ANALYSIS.round75.md` ADDENDUM 3 item 2: after the 7:00 AM ET vehicle on the day; ONE
  AT A TIME, each read before the next; each states its Bloomberg call count before it runs; a capacity refusal stops the sequence
  and is not retried that day; scripted pulls under `integrations/bloomberg/research/`; no agent signs in (a signed-out Terminal
  is Branch C, nothing is pulled).
- **research/ is outside the no-modify order:** `ANDREW_DIRECT_20261006_201xZ_BLOOMBERG_NO_MODIFY_IS_POSITIONING_AND_ETFS_VIEW_RESEARCH_OUTSIDE_OPEN_SEASON.md`
  ("Research is outside it ... and you have egress"). The order still covers `integrations/bloomberg/pipeline/`, the vehicle and
  the sign-in scripts.
- **"After the 7:00 AM ET vehicle" binds to:** the Windows scheduled task `OPAL_BBGTML_daily_pull`, daily at 07:00
  America/New_York wall clock, running `scheduled_daily_pull.cmd`, logs in `%USERPROFILE%\opal_bbg_logs\`
  (`integrations/bloomberg/pipeline/README.md:210-212`; `integrations/bloomberg/README.md:59`). The act's precondition read: the
  task's last run time is today's local date and the task is not running. AMGT_CORPUS's own task `amgt-induction-daily` fires at
  09:00 local (13:00Z) (`ledger/NEVER_WIDEN_ROUND39_AO2_CTO_HALF.md`): start a RESAPP pull after it has finished too, so two
  research pulls never overlap (this is the issuer's addition, stated in the half; Andrew's condition names only the 07:00 run).
- **Sign-in rule:** `integrations/bloomberg/READ_HERE.md` section 2: `fill` costs nothing, `submit` spends one of a 2-attempt
  budget, and a sign-in is Andrew's act (CTO fix-route ADDENDUM 1). A pull's L0 is `blp.health` only; health false = stop.
- **Output addresses** (builder output, `lib/research/harvest/bloomberg.bronze_write` -> `store.entity_partition`):
  officers `bloomberg/harvest/bronze/exec_officers/security_key=<safe>/<stamp>.json` (`lib/research/management/bloomberg_fallback.py:13,68`;
  5 names stored today); segments the same grammar under a NEW `segments` request (ba-25 adds it to `BRONZE_REQUESTS`,
  `lib/research/harvest/bloomberg.py:40`); the uncovered name through the existing queue consumer.

### ba-21 -- segments, 83 names (SERVED, pair to 1.0.0_SA_CTO~Z)
Legs: L0 `blp.health` (no data call) and the vehicle read; Lprobe ONE name (AMD US Equity) with `research_pulls.py run segments
--probe`, its call count stated first, the response READ and the fields confirmed in `research_pull_fields.json` (`probed: true`)
before any other name; Lp `plan segments` printed (names 83, calls M) then `run segments --confirm-calls M`; Lv the bronze count
equals the pulled count, and the served read (the FWD-1 cell's reader) on AMD. Both branches: fields refuse (BAD_FLD or not
entitled) -> STOP after the probe, ONE row, no fan-out; capacity refusal -> STOP, report, not retried that day. Writers of the
`segments` bronze: N = 1 (this driver). Rollback: bronze is write-once and additive; nothing served reads it until the reader
cell deploys, so no served value moves in this act.

### ba-22 -- officers, 84 names (SERVED, its own pair)
After ba-21 is read. `plan officers` (names 84, 1 call each = 84 calls) then `run officers --confirm-calls 84`. Lv: the stored
count under `exec_officers` rises 5 -> 5 + pulled; `exec_roster_chain.run_chain` on 3 names now serves officers from the Bloomberg
leg, labelled as such. EMPTY (a well-formed zero-entry response) is a result, not a failure (`bloomberg_fallback.py:32`). Writers of
`exec_officers` bronze: N = 2 code writers (this driver, and `enrich.py:646` on its own path); the half reads both.

### ba-23 -- FWD-2's first uncovered name (SERVED, its own pair)
After ba-22 is read. The carrier exists: the page's enqueue route and the box-side consumer
`integrations/bloomberg/research/pull_consumer.py --once` (PRD C-ROUND12-PULL-WIRED, `prd/AMGT_RESAPP_PRD.md:1388`; the consumer's
CADENCE is reserved to Andrew, so this is ONE hand run, not a schedule). The name is one the firm has never covered: the CVO or the
CTO names it in the pair, not the issuer. Lv: the page for that name reads "being fetched now" then the assembled pack (FWD-2
DONE WHEN, `prd:504`). Call count: stated from `model_block_pull`'s per-name count (8 per name at CORPUS's 768 / 96).

## 3. Row Z-S242

Placed as its OWN order ba-26 to `0.7.0_AE_CloudOps~A`, not folded into ba-20. Lane measured at HEAD: AE~A PERMIT, COO~Z REFUSED
(negative control). The file is `infra/aws/terraform/yang-pipeline/etf-classifications.tf`, blob d9f082f9d7, 82 CR, `eol: lf`.

## 4. Provision facts

- Portal origin/DEV head at the draft: `13509c52` (fetched 2026-10-07 ~00:3xZ); it carries `6de76f05` (/freshness).
- `lib/research/api/tests` still reads a portal fixture (`test_print_format_rich.py:7`), so a cell whose criterion runs that suite
  still needs `--portal-ref`. ba-19 and ba-25 run neither; they need none. ba-24 needs the DEV head the GO names.

## 5. The c59 repair (row Z-S361), `round75/checks/r75_served.py`

`--burst N` (default 40); the Lambda client's connection pool sized to the burst; an EMPTY cold list prints `UNMEASURED C2 ...` and
the verdict `R75 C59 SERVED: UNMEASURED` with exit 2 (a slow or failed cold invoke stays NO, exit 1). C1 and C3 unchanged. One run
on deployed OVpDhfwD at 00:31:58Z: C1 PASS 302 of 302; C2 PASS, 32 cold of 40, bar 2000; C3 PASS 807 ms; `R75 C59 SERVED: YES`,
exit 0 (`round77/checks/base_r75_c59_burst40.txt`).

## 6. Base lines for the issuance commit

- ba-19 AC1 base: FAIL as expected; ba-19 AC2 base: FAIL as expected
- ba-20 AC1 base: NO CELLS LISTED exit 2 (FAIL as expected); AC2 base: PASS as expected; AC3 base: PASS as expected (not re-run by this draft: AE~A's az-5 proof @5e9c95ad86)
- ba-24 AC1 base: FAIL as expected; AC2 base: PASS as expected
- ba-25 AC1, AC2, AC3 base: FAIL as expected
- ba-26 AC1 base: FAIL as expected (82 CR); AC2 base: PASS as expected

## 7. Open for the parent

1. The served reader of the `segments` bronze belongs to the FWD-1 / ruling-7 cell in another group; without it ba-21 moves no page.
2. ba-20's AC1 list `round77/checks/r77_deployed_cells.txt` does not exist yet: the issuer writes it at the GO, one deployed check
   per drained build cell. A round-77 ruling that changes what r76 c62 reads (ruling 5, the news-day rule) must be named in the pair
   or c62's C2 may read differently; ba-20's AC2 expect allows for that in words, which is soft.
3. ba-21's segment mnemonics are UNPROBED until the one-name probe. If the Terminal does not serve segment fields over
   ReferenceData, ba-21 stops at its probe and FWD-1 for the 83 goes back to the CTO.
4. ba-23's name must be named by a grading seat.
5. One project per Tier-2 seat: AE~A holds ba-26 and ba-20, both AMGT_RESAPP.
