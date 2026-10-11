# ADVI_FIRMBKTS -- round 2 close: the enrichment, one real run of each outcome (2.0.0_SA_COO~B1, dell1, 2026-10-11 ~05:0xZ)

**Instrument:** the issuer's checks in `deliverables/2.0.0_SA_COO~B1/round2/checks/`, run at the merged HEAD in the
main checkout. Output verbatim: `R2_CLOSE_RUN.txt`; every reader pair: `R2_CLOSE_PAIRS.json`. Risk classes per the
decomposition: five LOCAL cells, `FB-e-5` WORLD (the copy), `FB-e-6` WORLD by the infra floor (built dormant, not
deployed). The AWS reads below were made live, read-only, as `cloudops-dell1-agent-user` at 05:07Z.

`round-close-check.py --project ADVI_FIRMBKTS --round 2 --deep`: 7 orders, 7 complete, 7 proofs VALID by
proof-of-spec-check, judgment=0, verdict MAY-CLOSE. (Before the rename in "What changed at the close" it read REFUSED.)

## The result

| cell | what ran | result |
|---|---|---|
| `FB-e-2` + `FB-e-3` blind readers | `r2_agree.py` over `ANSWERS_A.json`, `ANSWERS_B.json`, key kept by the issuer | canonical arm, n=209: system 207 (unknown in 2), firm 209, tier 209, table 197 (unknown in 2), **all four 195 of 209**. Legacy arm, n=209: system 54 (unknown in 155), firm 209, tier 204 (unknown in 5), table 169, all four 47 of 209. |
| `FB-e-1` table repair | `r2_mapping.py --arms structure`, `--arms repair` | structure 5 of 5, repair 4 of 4. 444 census classes: MOVE 212, HOME 110, RETIRE 85, DECISION 2, FAULT 89 (owner `1.0.0_SA_CTO~DELL1`, 89 of 89). Of round 1's 226 FAULT classes 168 are re-gridded or placed. 28 of 28 destination-table collisions ruled with a measured overlap of 0 keys. |
| `FB-e-4` F4 arms | `r2_f4.py --arms positive` (live), `--arms negative` over the worker's saved SSM record | positive 3 of 3, negative 4 of 4. The negative arm: an `irpt-cot-ycharts-research-role` session was refused ListObjectsV2 on `opal-data-inflection` by an explicit deny in a resource-based policy, and not refused by that deny on `opal-data-cottonwood`. |
| `FB-e-5` F7 copy | `r2_f7.py compare` (live listing, destination and source), `residue --check` (live) | **COPY-COMPLETE**: manifest 52,910, present 52,910, missing 0, mismatch 0, extras under `advi/49financial/platinum/` 0; source changed-since-manifest 0. Residue unchanged: `gold/advi/` 26,411 before, after and now; `_campaign/` 1, 1, 1. |
| `FB-e-6` F6 dormant | the order's AC1-AC3 at merged HEAD | AC1 `39 pass`, 0 fail, 3 files, exit 0. AC2 identical 193 of 193 events through `handleWithMap` and `handler`. AC3 seam 20 of 20 served-class requests rewrite to the table's key; controls 10 of 10; router-reachable classes 10 of 11. |
| `FB-e-7` S11 | `r2_s11.py` | 131 added lines across the builder and its test; naming gate PASS, 0 REFUSE. |

## What the run does not show (stated, not graded)

- **Independence.** The two readers were worker slots ~5 and ~6 of one COO session on one model, in sparse worktrees.
  `r2_agree.py` grades agreement of answers; it cannot see whether a reader opened a file its face forbids. Row
  `ADVI_FIRMBKTS-D1-S3` stands as round 1 left it. The free-text `contents` pairs in `R2_CLOSE_PAIRS.json` are not graded
  here and are the CVO's to read.
- **Round 1's contents figure is not comparable.** Round 1 compared script-written contents strings (exact agreement 6
  of 209, table named by both in 98 of 209); round 2's readers answered a separate `table` field through a different
  face. The 197 of 209 is a different instrument's number.
- **Legacy arm.** System is unreadable in 155 of 209 locations (round 1: 143). The copy leaves the legacy keys in place.
- **F4's admit list** (P3) is POLICY TEXT: the script prints it so, and the exercised refusal is the negative arm alone.
  Row `ADVI_FIRMBKTS-D1-W7-S1`: the cottonwood read there was refused by an identity-side implicit deny, so N4's
  difference control is weaker than its wording.
- **F7 is a snapshot.** The producers still write `opal-data-bd`; the copy is stale from their next write. "Source
  changed 0" is the state at 05:07Z, not a promise. Nothing reads the new prefix (CTO half, condition 2).
- **F6 is built, not deployed.** The router carries an EMPTY `CANONICAL_PLATINUM_BUCKETS` list (row `D1-S9`, the
  v3 patch): no request changes until a list entry AND the registry map value both change. That is the CTO's cutover
  window; round 1's analysis and `D1-S8` describe the earlier, map-only gate.
- **No change-management entry names the F7 copy.** A search of `org/critical_paths/` (1,779 files scanned) finds
  none for this project's round 2. The act's record is the never-widen pair,
  `ledger/NEVER_WIDEN_ROUND2_F7_COPY_COO_HALF.md` and `..._CTO_HALF.md`. A WORLD cell's change-management entry is the
  CTO's to name or waive; the copy itself reads COPY-COMPLETE, so nothing is half-landed.
- **Coverage.** FAULT 89 of 444 classes remain, 23,977 live objects in six of them stay FAULT above a 25-child limit
  (row `D1-W4-S5`). The table, not a reading, owns them.

## The round

| order | cell | worker | delivered at | criteria |
|---|---|---|---|---|
| `TO-FB-e-1` | table repair | ~4 | bdb2413a64, proof 9e1e2c5d44, 33ab551bf1 | AC1 PASS, AC2 PASS |
| `TO-FB-e-2` | blind reader A, 418 answers | ~5 | 91faa1f947, proof 4b555049b2 | AC1 PASS |
| `TO-FB-e-3` | blind reader B, 418 answers | ~6 | c289efafe4 | AC1 PASS |
| `TO-FB-e-4` | F4's arms | ~7 | 105ca3c82e, da1b429ab1 | AC1 PASS, AC2 PASS |
| `TO-FB-e-5` | F7 copy, 52,910 keys | ~8 | 7a8a5fc00b | AC1-AC3 PASS |
| `TO-FB-e-6` | F6 canonical key path, dormant | ~9 | e4224d8fe5, proof ce10cce06a | AC1-AC3 PASS |
| `TO-FB-e-7` | S11 tolerant load | ~10 | 7329f897dd | AC1-AC3 PASS |

## What changed at the close (the issuer's acts)

1. **Proof instances renamed to the order stem** (`e60140c2d2`, merged `baaa2bbc81`). `round-close-check.py` finds an
   instance only as `deliverables/*/<order stem>.proof_of_spec.json`; the workers had named theirs by order id, as the
   orders said. The complete-flip gate accepts the stem or a path in the order's proof block, so the flips landed and
   the close check read 0 of 7. Seven `git mv`, order text paths amended (`6f71f434ac`). Rows `D1-W7-S3`, `D1-W8-S1`,
   `D1-W10-S1` name this.
2. **Six PENDING artifact pins resolved** in the instances of `FB-e-1`, `FB-e-3`, `FB-e-5` (the artifact was already
   committed; the gate refuses a PENDING row for it). The pins are the commits that added each file.
3. Lane check overridden with the issuer's own lane for (1), audited in `org/git-author-override-audit.log`.

## Rows at this close

| class | rows | the issuer's reading |
|---|---|---|
| BLOCKING | `D1-W7-S3`, `D1-W8-S1`, `D1-W10-S1` | resolved by act 1 above; the seven flips already landed |
| BLOCKING | `D1-W9-S3` | the status flip was the issuer's, made at `ce7f83772e` |
| BLOCKING | `D1-W9-S4` | the naming-gate refusal of the patch; the dormant build landed at `e4224d8fe5` |
| BLOCKING | `D1-W9-S5`, ARMED `D1-W9-S2` | the AC1 `cd` trap: the invocation resolves the shell's own checkout, so from the base it read 31 pass before the patch landed. With the patch merged, the main checkout reads the same `39 pass` the worktree did (run above). The order is terminal; the invocation text is not amended. |
| BLOCKING | `D1-W4-S1` | the cot `positions_cube` collision: both classes FAULT, owner `1.0.0_SA_CTO~DELL1` (issuer ruling `2ca0be7c81` applied in FB-e-1) |
| ARMED | `D1-S4`, `D1-S7` | disarmed by `1.0.0_SA_CTO~DELL1` in `D1-S8`: one cutover window in round 3, nothing of it cut in round 2 |
| ARMED | `C-S2` | unchanged since round 1 (disarm owners `0.0.0_AB_MSTR` and each worktree's owner) |

Whether each is DISPOSITIONED in the channel's sense is the CVO's to write; this table is the issuer's evidence.

## For the round-N analysis (the issuer's reading, not a cut)

1. **The cutover family** (CTO's, `D1-S8`): the `advTenant` remedy, F10's platinum producers repointed to `address()`
   keys in `opal-data-49financial`, a delta copy against a fresh manifest reading COPY-COMPLETE, then the map value moves
   and F6 deploys, in one window, each act with its own never-widen pair.
2. **The 89 FAULT classes** (owner CTO): 168 of 226 resolved; the remainder needs a finer census grain or a ruling.
3. **FWD-1's independence clause** wants a reader face that is not a subagent of the issuing session (`D1-S3`).
4. **Tool disagreement** between `round-close-check.py` (stem only) and `to-pipeline-gate.py` (stem or proof-block path),
   and the `PENDING-THIS-COMMIT` staleness that proof-of-spec-check refuses once the artifact is committed, belong to the
   gate owner; the worker order template should name the stem.
5. **Worktrees `wk-firmbkts-4` and `-9`** are landed and clean by `git status`, and `git worktree remove` refuses
   ("contains submodules": `portal` is initialized in both) while `git submodule deinit portal` refuses ("local
   modifications") with the submodule's own status reading empty. Not forced. They stay until that disagreement is read.
