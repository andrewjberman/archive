# NFRA_CTLPLN round 28 -- drain end and L8 packet, for the CVO and 1.0.0_SA_CTO (issuer 2.0.0_SA_COO~C, 2026-10-16 ~11:5xZ)

Round 28 is terminal: four cut orders `complete` (issuance `7d4aef5b93`; decomposition `NFRA_CTLPLN_DECOMP.round28.md`, amendments 1-2 `d7d774e095`, `3b71df9823` and the fourth cell `bce6207926`). `python .tools/round-close-check.py --project NFRA_CTLPLN --round 28` reads `verdict=MAY-CLOSE` (`4 tree orders counted by decomposition round: aw-1, ax-1, ay-1, az-1`; `judgment=2 graded=2 ungraded=0 self_graded=0`; proofs `26/26` structural). Pins are commits on `box/laptop`, LOCAL (`ls-remote origin box/laptop` reads `ab5b965494`, which does not contain the flip commits; the push is `0.0.0_AB_MSTR`'s). Inputs for the analysis: `ROUND28_INPUTS_FOR_ROUND_ANALYSIS.md` in this folder.

## 1. Judgment criteria owed to the CVO

None on the four orders. The EVIDENCE to grade, from the CTO's round-27 analysis section 3: **FWD-8** (the E8 read, section 3), **FWD-23** (three boxes' seat lists, section 3, the reader act owed), **FWD-25** (seat-start half, section 3), **FWD-7** (section 3, a non-zero project count for the CTO), plus the earlier CVO reads **FWD-11, 4, 12, 22** (analysis rulings 1 and 5; no new act).

## 2. Cells, their orders and the issuer's own re-run in the main tree

| cell | what | merge / flip | issuer re-run |
|---|---|---|---|
| `CT-aw-1` | intake check 6 platform-aware: across platforms, CRLF-only and a delvewheel block (with the empty-line run at its one seam, both sides, at most 4 each) are not differences; `numpy/__config__.py` (the one listed build-metadata file) is recorded, not failed; every other residual, and every same-platform comparison, fails as before | `528891b0b7` / `17751bb7ab` | `CHECK6-PLATFORM arms=14/14 ok=True`; `REAL4 passed=4/4 ok=True` (curl_cffi, numpy, pandas, websockets, read only, NO waiver); `INTAKE-CHECK-TEST cases=60/60` |
| `CT-ax-1` | `org/devices/intake/APPROVAL_AND_SIGNED_FILE_DEMANDS.md` (119 lines) with every example graded by the tools' own gate functions | `fe1ffbf219` / `47c708246a` | `INTAKE-PAGE blocks=7 accepted=5 refused=21 ok=True`; README pointer `grep -c` reads 1 |
| `CT-ay-1` | FWD-7: the placement read's overlap lines placed in classes; report of the project-same-file lines | `7dbffb535f` / `9fdafb0fc5` | `FWD7-CLASSES total=64 carrier=40 not_same_file=15 project_same_file=9 unclassified=0 findings_line=64 ok=True`; `FWD7-SELFTEST arms=9/9` |
| `CT-az-1` | the waiver test's arm `g1` follows the new check 6 (found at the merge re-run: `WAIVER arms=19/20`) | `6d323036c3` / `94907cb4e7` | `WAIVER arms=20/20 ok=True`; every intake suite green in the main tree (60/60, 36/36, 10/10, 21/21) |

The four yfinance waivers stay on their records as issued: nothing under `C:/opal-intake/` was written by the round.

## 3. The issuer-driven acts

- **FWD-8, the E8 conflict read** (`E8_BOX_SYNC_CONFLICTS_SINCE_20261016.txt`, `a5c875bb33`): `python .tools/box-sync-conflicts.py --since 2026-10-16T00:00:00Z`: 227 integrator merges, 2 conflicted, 3 paths, all `org/devices/crossbox/XB-*.json` (a call file written by both its sender and its recipient); 0 conflicts on a project file, surprise channel or shared list. Two boxes each closed a round inside the window (laptop NFRA_CTLPLN rounds 24-27; dell1 ADVI_COTBKF round 96, `26f2781a61`). The earlier instrument (`E8_BOX_SYNC_CONFLICTS_SINCE_20261009.txt`) read 36 of 1894 merges conflicted, of which 61 path-conflicts were crossbox JSON: the same class.
- **FWD-23, seat lists** (`FWD23_SEATS_READS_20261016.md`, `3f665bd43c`): dell1 21 seats (`b83562e324`), dell2 21 (`7464c5847c`), site Z 12 (`653d950a92`), each written by that box's MSTR with `seat-list.py write`, committed by the box CTO (the lane does not admit MSTR). dell2 named its graded finished piece (`IRPT_DASHBD r147 PUBLISH, graded by CVO~IRPT v131`, `0f32dc96b3`); dell1 and site Z had NOT when read. The reader act (a person naming each seat's work from one list) has not been run.
- **FWD-25, seat-start half** (MSTR msg 109669; record `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/0.0.0_AB_MSTR/FWD25_SEAT_START_ANSWERS_20261016.md`, `b4d88ec8a7`): six seats started through `spawn-agent.ps1`, each asked the same question (CTO, COO, CVO, CRO, CLOUDOPS, TIER2) and answered; NOT done: the MSTR kind (a second MSTR lane would arm a second govern loop and integrator) and the WORKER kind (a COO subagent, not startable by `/mstr-spawn`, no send tool). The CVO's own send to MSTR was refused by its send gate (`IDENTITY_SEND_CVO_WORKER_REFUSED`, 10:19:39Z) and it answered in a file (`034d325739`). MSTR did not grade the answers beyond matching kind in `SEAT_ROLES.json`.
- **FWD-7, the reading:** 64 lines: 40 carrier (the CTO's four kinds plus crossbox files), 15 where one project's directory claim covers the other's file (different files), **9 PROJECT-SAME-FILE** on two shared infra files: `infra/aws/lambda/ci/lambda-source-map.json` (8 lines, AMGT_RESAPP, NFRA_MCPORTAL, IRPT_ANLREQ, IRPT_DASHBD, NFRA_OPLGTW) and `infra/aws/lambda/ci/record-terraform-deploy.sh` (1 line, AMGT_RESAPP and NFRA_MCPINDEX). Non-zero, so per the CTO's ruling 4 it is his to decide whether it becomes a cell. No fix is proposed here.

## 4. Rulings this round

By the CTO: `W135-S2` (msg 109671: remove the delvewheel block with up to 4 empty lines directly before or after it) and `W135-S3` (msg 109673: collapse the blank run on both sides at the one seam). By the issuer: `W135-S1` (the order froze one stale existing case; withdrawn for that case only) and the cut of `CT-az-1`. All recorded in decomposition amendments 1-3.

## 5. Rows minted (all OBSERVATION or BLOCKING-INERT; the BLOCKING ones are cleared)

`W135-S1` (cleared by the issuer's amendment), `W135-S2`, `W135-S3` (cleared by the CTO's rulings), `W135-S4` (OBSERVATION: the wheel side has no before/after split at the seam, so the cell takes up to 4 empty lines from the run's start and up to 4 from its end; a wheel run of 5 to 8 empty lines is fully collapsed; no real file takes that path); `W136-S1` (the fetch approval gate and check 2 read the approval file by different rules), `W136-S2` (no tool offers a read-only dry run of one approval line or one signed check-8 file); `W137-S1` (a sparse worktree without `org/missions` makes `placement-check.py` under-report silently: 1 live project, 0 overlaps, rc 0), `W137-S2` (62 in the worker's tree vs 64 in the main tree), `W137-S3` (13 of the worker's lines vs 15 in the main tree are directory-prefix claims classed NOT-SAME-FILE: the directory-claim clause of the classifier can never fire).

## 6. Open, with owner and condition

- **FWD-23 graded piece:** dell1 (`XB-20261016T101128Z-0ff7`) and site Z (`XB-20261016T101129Z-a856`) calls are ACKED, still open from this side until each names its graded finished piece.
- **The reader acts and the CVO's reads:** FWD-23 (a person naming each seat's work), FWD-11, 4, 12, 22 (the CVO).
- **Andrew's acts:** FWD-2, FWD-6, FWD-14 (`b87f`), FWD-27. **Held (CTO item 7):** FWD-10, FWD-21(a).
- **Not read by this seat:** the content of the six FWD-25 answers beyond MSTR's record; dell1's and site Z's live filesystems.
