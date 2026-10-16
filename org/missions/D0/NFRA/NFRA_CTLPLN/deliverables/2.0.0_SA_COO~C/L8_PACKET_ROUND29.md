# NFRA_CTLPLN round 29 -- drain end and L8 packet, for the CVO and 1.0.0_SA_CTO (issuer 2.0.0_SA_COO~C, 2026-10-16 ~15:4xZ)

Round 29 is terminal: six cut orders `complete` (issuance `833181d311`; decomposition `NFRA_CTLPLN_DECOMP.round29.md`, amendments 1-5 `98eba74fb5`, `7e29ed4adc`, `41f01e24e9`, `e275fc60c8`, `7443597a0c`). `python .tools/round-close-check.py --project NFRA_CTLPLN --round 29` reads `verdict=MAY-CLOSE` (`29 orders, 28 complete; 6 tree orders counted; proofs 28/28 ok; judgment=2 graded=2 ungraded=0 self_graded=0`; it first read REFUSED with `PROOF-BAD` on four orders because the issuer typed the long slug into `<to_id>`: fixed `d40c5712a7`). Pins are commits on `box/laptop`, LOCAL (`ls-remote origin box/laptop` read `c47546f03c9d` at 15:4xZ; the merges up to `9a570bb671` and `dc80d4540d` are on origin, the later ones are not). Inputs for the analysis: `ROUND29_INPUTS_FOR_ROUND_ANALYSIS.md` in this folder.

## 1. Judgment criteria owed to the CVO

None on the six orders. EVIDENCE to read: **FWD-8** (the crossbox split is live; the window read below), **FWD-7** (the placement tool fails loud; the census), **FWD-25** (the forbidden-act probes 60 of 60; seven seat kinds started by MSTR, the WORKER kind by this seat) and, unchanged, FWD-11, 4, 12, 22.

## 2. Cells, their orders and the issuer's own re-run in the main tree

| cell | what | merge / flip | issuer re-run (main tree) |
|---|---|---|---|
| `CT-ba-1` | cross-box call files: ONE writer per box (from-side `XB-<id>.json`, schema `crossbox/2`; one `XB-<id>.<box>.json` per answering box); one reader; `crossbox/1` files read and write as before; a committed `LAYOUT` switch; the tool's stale suite case repaired; the deploy-gate suite fixture (a neighbour the change turned red) repaired | `dc80d4540d` / `a62838bb37` | `CROSSBOX-SPLIT 13/13`; `CROSSBOX-SELFTEST 40/40`; `CROSSBOX-TEST 76/76` (base 69/70); `APPLY-GATES-TEST 100/100` (51/100 after the first seating); `CROSSBOX-MATRIX-SELFTEST 7/7`; `OPEN-CALLS-TEST 19/19`; `XBOX-DELIVER 16/16`; `ROUND13-BATCH 15/15`; `HYGIENE-MERGE 5/5` |
| `CT-bb-1` | the `lambda-source-map.json` consumer census and per-function layout proposal (stage 1; read-only) | `20ed36c47d` / `78f2f10849` | `SOURCEMAP-CENSUS files=2528 grep_files=2528 reconciled=True map_functions=240 ... ok=True`; `SOURCEMAP-SELFTEST 9/9` |
| `CT-bc-1` | `placement-check.py` exits 3 with `ERROR:` on a missing `org/missions` or `org/projects` or a short project count; findings keep exit 0 | `430e2d1615` / `f7ff1d04bf` | `PLACEMENT-LOUD 7/7`; the real tool: `register rows with a tree home: 30 \| live projects read: 30 \| match=True`, rc 0 |
| `CT-bd-1` | the seat-rules table follows Andrew's 2026-10-13 ruling; the slow probe has its own bound; per-kind report | `7ba72f2e61` / `ce00b4cdac` | `SEAT-RULES ... probes_pass=60 probes_fail=0 probes_unread=0 ok=True` (base 56 / 1 / 1); `validate problems=0`; suite 26/26 |
| `CT-be-1` | `round-close-check.py` takes the grade of record (latest CVO-kind non-doer row) | `9a570bb671` / `e223ecd5d3` | `GRADE-OF-RECORD 8/8` (base 4/8); `ROUND-CLOSE-SELFTEST 30/30` |
| `CT-bf-1` | the same checker: SOURCE PRIORITY (an adjudication-file grade outranks an investigation-file grade; the latest within a source) so a defect-reporting investigation row cannot win | `6958e599d9` / `6bc10150f8` | `GRADE-NOT-A-MENTION 7/7`; selftest 30/30 with the original fixture; sweep of 232 runs in 9 real projects against `9a570bb671`: 0 flips, 0 changed readings, 5 source-only changes at equal dates |

Both checker cells answer site Z's call `XB-20261016T121809Z-95c2` (reply `XB_95C2_REPLY_TO_CTO_Z.md`, `d9af371f09`; follow-up `cd939cc4f2` answered by `CT-bf-1`; the announcement to the four boxes asked of `0.0.0_AB_MSTR`). Site Z re-runs `NFRA_OPLGTW` round 37 after box-sync and reads `TO-OG-ap-14 AC3`.

## 3. The FWD-8 window (the CTO's round-28 ruling 1)

- **Rollout read before the switch** (git blobs on `origin/box/dell1`, `dell2`, `sitez`): the five changed tools equal the merged ones on all three. `org/devices/crossbox/LAYOUT` = `2` committed `911c4273dc` (git's date display shows 10:24:04 because it prints local time: the real time is **2026-10-16 ~14:24Z**).
- **The first layout-2 call, `XB-20261016T142512Z-6441` (laptop to dell1):** body `dfbf4caebe`, file `0686932f89`; dell1 acked and closed its side at 14:30:49Z by writing exactly ONE file (`XB-20261016T142512Z-6441.dell1.json`, commit `2c42c8f1bd`); the from-side file's blob is identical on the laptop, `origin/box/dell1` and `origin/CLOUD` (`5185a9b3fe`); the laptop closed the from-side `399e0fe7de`; `status` reads CLOSED-BOTH through the reader.
- **Interim conflict read** (`E8_INTERIM_SINCE_LAYOUT2_20261016.txt`, `83e3db8586`): `python .tools/box-sync-conflicts.py --since 2026-10-16T14:24:00Z`: 22 integrator merges, 0 conflicted. Before the switch: 2 of 227 (all crossbox call files). **This is NOT the grade:** the grade needs a window in which two boxes each complete a full round. Re-run `box-sync-conflicts.py --since 2026-10-16T14:24:00Z` at the CVO's reading time: the laptop's round 29 closes in this window (this packet), and the second box is any dell round close after 14:24Z (the reader names it from `origin`).

## 4. Rulings this round

- **By the CTO:** (round-28 analysis) the crossbox one-writer layout, `lambda-source-map.json` is NOT a shared carrier and splits per function, `record-terraform-deploy.sh` is code with ONE owner `0.7.0_AE_CloudOps`, the directory-prefix class is NOT-SAME-FILE, the placement tool fails loud, FWD-25 per kind.
- **By the issuer inside its decomposition:** `CT-be-1` and `CT-bf-1` cut from the inbound call; `CT-ba-1` amendment 1 (a neighbouring suite), `CT-bf-1` amendments 1 and 2 (two rules withdrawn on the worker's own sweeps: structured-grades-only would flip 52 real grades and 27 closes; head-anchored prose would flip 7 and 3; the final rule changes no reading); the `LAYOUT` switch committed only after every box carried the tool; the stage split of the source-map work.

## 5. Rows minted (all OBSERVATION or BLOCKING-INERT; the BLOCKING ones are cleared)

`W139-S1..S4` (base suite red; a sparse tree reads green with seven SKIPs; the deploy-gate suite turned red then repaired; a stale comment in `mstr-ledger-check.sh`, outside the cell); `W140-S1..S5` (7572 lines not 7577; four live readers degrade silently when the map is absent; a closed-round battery writes the whole real map; `estate_report_runner` runs a git checkout of the map path as a read side effect; `_last_deploy_recorded` is still changed after the commit that says it stops); `W141-S1..S3` (the expectation uses the register's declared `home`; the cut lacked `org/projects`; `test_round19_register.py --fwd7` rewrites a tracked file each run); `W142-S1..S4` (one row with three probes, the checker refuses split ids; the sparse set; the count assertion moved with the retired question; the base's red crossbox suite, since repaired by `CT-ba-1`); `W143-S1` (a NOT MET grade of record still counts in `graded=`: the CVO's rule), `W143-S2`; `W144-S1..S5` (S1-S3 BLOCKING, INERT, from the two withdrawn rules; S4; S5 the five source-only changes).

## 6. Open, with owner and condition

- **The source-map stage 2** (the atomic migration commit, a deploy freeze, a Terraform plan per root): the CTO reads `PROPOSED_LAYOUT_AND_MIGRATION.md` and decides (inputs file, item 1).
- **FWD-8:** the window read at the CVO's reading time (section 3). **FWD-25:** the MSTR kind started with every loop banned in the hint (MSTR's honest limit: not shown what an MSTR seat does with no ban); the WORKER kind answered (`FWD25_WORKER_KIND_ANSWER_20261016.md`).
- **FWD-11, 4, 12, 22** (the CVO); Andrew's acts (FWD-2, 6, 14, 27); FWD-10 and FWD-21(a) held.
- Not read by this seat: site Z's real round 37 files; the live Terraform plans; whether the three kept Dell Denies are applied live.
