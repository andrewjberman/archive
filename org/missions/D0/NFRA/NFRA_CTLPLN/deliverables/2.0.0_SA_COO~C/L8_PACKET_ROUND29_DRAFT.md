# NFRA_CTLPLN round 29 -- L8 packet DRAFT (issuer 2.0.0_SA_COO~C, 2026-10-16 ~13:5xZ); NOT SENT. Replaced by `L8_PACKET_ROUND29.md` when `CT-ba-1` is merged.

Status at writing: four of five cut orders `complete` (`CT-bb-1`, `CT-bc-1`, `CT-bd-1`, `CT-be-1`); `CT-ba-1` (one writer per box for cross-box call files) is in its second seating after a neighbouring suite its change turned red (`test_apply_who_and_crossbox.py` 51/100, row `W139-S3`; amendment 1, commit `7e29ed4adc`). Issuance `833181d311`; decomposition `NFRA_CTLPLN_DECOMP.round29.md` (amendments: `CT-be-1` `98eba74fb5`, `CT-ba-1` `7e29ed4adc`).

## Cells, merges and the issuer's own re-run in the main tree

| cell | what | merge / flip | issuer re-run (main tree) |
|---|---|---|---|
| `CT-bc-1` | `placement-check.py` exits 3 with `ERROR:` when `org/missions` or `org/projects` is absent or the live project count is short of the register's; findings keep exit 0 | `430e2d1615` / `f7ff1d04bf` | `PLACEMENT-LOUD arms=7/7 ok=True`; the real tool reads `register rows with a tree home: 30 | live projects read: 30 | match=True`, rc 0 |
| `CT-bd-1` | the seat-rules table follows Andrew's 2026-10-13 ruling (the Dell Deny `DenyProtectedFunctions` was removed on purpose; three Denies kept); the slow probe has its own bound; per-kind report | `7ba72f2e61` / `ce00b4cdac` | `SEAT-RULES ... probes_pass=60 probes_fail=0 probes_unread=0 ok=True` (base 56 pass, 1 fail, 1 unread); `validate problems=0`; suite 26/26 |
| `CT-be-1` | `round-close-check.py` takes the grade of record (the latest CVO-kind non-doer row), site Z call `XB-20261016T121809Z-95c2` | `9a570bb671` / `e223ecd5d3` | `GRADE-OF-RECORD arms=8/8 ok=True` (base 4/8); `ROUND-CLOSE-SELFTEST 30/30`; neighbouring suites green; reply `XB_95C2_REPLY_TO_CTO_Z.md` (`d9af371f09`) |
| `CT-bb-1` | the `lambda-source-map.json` consumer census and per-function layout proposal (stage 1; read-only) | `20ed36c47d` / `78f2f10849` | `SOURCEMAP-CENSUS files=2528 grep_files=2528 reconciled=True map_functions=240 ... ok=True`; `SOURCEMAP-SELFTEST 9/9` |
| `CT-ba-1` | PENDING (second seating) | | |

## For the CTO (decisions and readings)

1. **The source-map proposal** (`deliverables/0.9.0_WK_NFRA_CTLPLN~140/PROPOSED_LAYOUT_AND_MIGRATION.md`): folder `infra/aws/lambda/ci/function-map/`, one file per function (240), no aggregate; three Terraform roots read by `fileset`; one shared reader `lib/opal_lambda_map.py`; one atomic commit (live readers, writers, the deleted map, `.owned-paths.yaml`, four silent readers made loud); no deploy between the additive step and the atomic commit; only that step changes a Terraform plan, checked by plan, never apply. Decisions owed: (a) the atomic set and the deploy freeze; (b) `_last_deploy_recorded` has no function home, so the proposal drops it; (c) `record-terraform-deploy.sh`: 14 owner and 13 non-owner commits (12 code, 1 data); the one-owner declaration is a lane entry, which is not this seat's file.
2. **FWD-25:** forbidden-act probes 60 of 60 PASS per kind; seat-start: seven kinds by MSTR (MSTR kind started with every loop banned in the hint, its own report), the WORKER kind by this seat; MSTR's honest limit: it shows the seat can state its role and stay out of loops when told, not what an MSTR seat does at start with no ban.
3. **W143-S1:** a grade of record of NOT MET still counts as graded: the CVO's rule.

## Open

FWD-8 window read after `CT-ba-1` merges, every box carries the tool, and the `LAYOUT` switch is committed; FWD-11, 4, 12, 22 with the CVO; Andrew's acts (FWD-2, 6, 14, 27); FWD-10 and FWD-21(a) held.
