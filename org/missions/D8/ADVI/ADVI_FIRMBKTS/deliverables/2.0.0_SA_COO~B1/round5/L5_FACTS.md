# ADVI_FIRMBKTS round 5 -- L5 ground truth (2.0.0_SA_COO~B1, dell1, 2026-10-13 ~06:5xZ)

Each fact states its instrument and read time. Claims: M = measured by this seat now, H = held (a cited record).

| # | fact | claim | source |
|---|---|---|---|
| 1 | The round-4 analysis names 6 items; item 7 (D1-S28) came at msg 4653. Round 5 is ONE issuance by this seat. | H | `ledger/ROUND_ANALYSIS.round4.md` section 3; CTO msg 4653 |
| 2 | FWD-1 canonical arm: 139 of 150 agree on all four fields; the 11 are 8 table-grain choices and 3 unknown tables; 0 date conflicts; legacy arm 0 of 150. | M | `round4/checks/r4_agree.py` re-run 06:2xZ over `C:/dev/wk-firmbkts-r4-reader-{a,b}`; CVO `D1-C-S29` |
| 3 | Every one of the 11 follows ONE rule: the table is the component immediately after the tier. 6 are `state/parity/<name>/` (key `parity`), 1 `gold/cache/` (reader B unknown), 2 `code/` (both unknown, key `gold`), 1 `platinum/49financial/` (B read the file name), 1 `bronze/orion/` (B read a deeper directory). | M | `FWD1_R4_DISAGREEMENTS.json`; `round4/READING_KEY.json` |
| 4 | The round-4 readers' face stated the grammar `{source}/{scope}/{tier}/{table}/{partition}` and no component rule. | M | `task-orders/ADVI_FIRMBKTS.TO-FB-g-4.reader-a.md` section 1a |
| 5 | `auth-validator-edge` spec `tests/ownership_key.spec.mjs`: 5 pass, 1 fail at HEAD (test (i), `expect(...includes(cfg.bucket)).toBe(false)` reads `true`). The generated `CANONICAL_PLATINUM_BUCKETS` is exactly `['opal-data-49financial']`; `OWNERSHIP_KEYS['49financial']` legacy `platinum/49financial/ownership_map.json`, canonical `advi/49financial/platinum/49financial/ownership_map.json`. With the list emptied in a copy the unfixed spec still passes (fail=0). | M | `bun test tests/` and `r5_checks.py mutant` at HEAD 06:3xZ; `_shared/firm-config.mjs:95-106` |
| 6 | The validator's decision: non-admin caller, `map.advisors[advisorId].accounts` or `.relationships` includes the id; the map read is `getOwnershipMap` (60 s cache), key from `ownershipMapKey(firmId, bucket)`; admin bypass before any read; verification is RS256 through `getJwtKeySlots` / `verifyWithSlots`. `export const handler`. | M | `auth-validator-edge/index.mjs:73-79, 160-195, 334, 451-530` |
| 7 | The dispatcher emits `Source bd-pipeline.gold-chain`, `DetailType chain-complete` on the default bus, and tests success by `grep -q '"FailedEntryCount": 0'` over the CLI's merged stdout and stderr; on failure it prints WARN and returns 0, so the CLI's error text is never kept. | M | `data/black_diamond/scripts/gold/gold_dispatch.sh:835-855, 1450-1458` |
| 8 | The generator has not run since 2026-05-03; `exec-summary-trigger` is an event pattern with no schedule; TriggeredRules none since 2026-09-01 (FB1's read 04:50Z). | H | row `D1-S40`, `0544e1aa11` |
| 9 | **Item 6 (act 2's first scheduled chain read), run at the cut:** `r3_act2_reads.py new-home --since 2026-10-13T03:30:00Z`: 11 of 11 served classes written since (objects 44, 8574, 779, 18230, 17, 10, 1, 7586, 988, 16802, 17). `old-home --since 2026-10-12T06:22:08Z`: 0 keys of 11 classes modified. | M | read 06:20Z today by this seat |
| 10 | The canonical ownership map was rewritten by the producers 2026-10-13T05:24:07Z (the legacy copy is frozen); whether the two are still byte-equal is NOT measured here: `FB-h-3` measures it. | H | CVO `D1-C-S36` |
| 11 | S32-S34 are on a pipeline FIRMBKTS moved, not defined; owner of the pricing rules: none active (CTO). Code lines cited by the rows: `bd_price_update.py:263-271, 344, 265`, `B_01.holdings_lots.py:331-361`, `B_03.account_gains.py:327`. | H | `INVESTIGATION_v1.md` D1-S32..S34 |
| 12 | The fence instrument at HEAD ends in `UnicodeEncodeError` (cp1252) with no environment override. | M | `check_fence_scoped_rows.py` run 06:3xZ |
| 13 | PRD v1.4 @1e5dcef9cb is ADMITTED (ratified-text SIGNED CVO; brief SIGNED CRO, current by ENDPOINT hash). | M | `prd-signoff.py status ADVI_FIRMBKTS` 06:3xZ |
| 14 | The reader worktrees `C:/dev/wk-firmbkts-r5-reader-{a,b}`: one parentless commit `110cfbe34b98`, `LOCATIONS.json` alone, sha256 `168c5016...d10e`, 22 locations (11 + 11). | M | `r5_fwd1.py build` output |

## Base dry-runs (each check a file under `round5/checks/` or `round4/checks/`)

| order | criterion | base |
|---|---|---|
| FB-h-1, FB-h-2 | AC1 reader | FAIL as expected (0 of 4; 4 of 4 on a full fixture answers file; 3 of 4 with one extra file) |
| FB-h-3 | AC1 harness | FAIL as expected (harness absent); AC2 record: FAIL as expected (absent); AC3 scope: FAIL as expected (nothing changed) |
| FB-h-4 | AC1 suite | FAIL as expected (5 pass 1 fail); AC2 mutant: FAIL as expected (fail=0: the old test passes on an emptied list); AC3 scope: FAIL as expected |
| FB-h-5 | AC1 live record | FAIL as expected (absent; a planted fetch_failed reads FAIL; a planted write verb in `calls` reads FAIL; a good fixture reads PASS) |
| FB-h-6 | AC1 diagnosis shape | FAIL as expected (absent; planted `put-events` call FAIL; good fixture PASS); AC2 scope: FAIL as expected |
| FB-h-7 | AC1 quantification shape | FAIL as expected (absent; planted recommendation `NOT_MATERIAL` over a non-zero count FAIL; good fixture PASS); AC2 scope: FAIL as expected |
| FB-h-8 | AC1 instrument | FAIL as expected (UnicodeEncodeError); AC2 ASCII bound: PASS as expected (control) |

## Items not cells of this round

- Item 6 is executed in this file (fact 9); no order, so the CVO re-reads it at L9.
- The PRD v1.4 sequencing items R3 (the `mdpf/{firm}/platinum/*` serving grant) and R4 (the joint reader census) are named by the
  CTO in earlier analyses and are NOT in the round-4 analysis's list; they are not cut here and are asked of the CTO in one line.
- Portal `ROUTER_FIRM_SUFFIX` (49financial -> bd): a client-facing module; PROD waits on Andrew; not in the list.
