# ADVI_FIRMBKTS -- round 3 close: the first window act applied, the rest built dormant and parked (2.0.0_SA_COO~B1, dell1, 2026-10-11 ~10:4xZ)

**Instrument:** the issuer's checks in `deliverables/2.0.0_SA_COO~B1/round3/checks/`, each complete order's recorded
criteria re-run from the order file at the merged HEAD of the main checkout (`R3_CLOSE_RUN.txt`, verbatim: 17 of 17
PASS), plus read-only live AWS reads at 10:1xZ as `cloudops-dell1-agent-user`. Risk classes per the decomposition: eight
LOCAL or built-dormant cells, `FB-f-8` WORLD (a deploy, applied on the laptop), `FB-f-12` WORLD (an IAM role and an
account SMS preference, executed by the laptop lane), `FB-f-9`, `FB-f-10`, `FB-f-11`, `FB-f-13` WORLD by floor.

`round-close-check.py --project ADVI_FIRMBKTS --round 3`: 13 orders, 8 complete, proofs 8 of 8 structurally OK, judgment=0,
verdict MAY-CLOSE (FB-f-9, -10, -11, -13 `parked` with owner and conditions; FB-f-12 not complete, outside the verdict:
see "What is open").

## The result

| cell | what ran | result |
|---|---|---|
| `FB-f-1` compare instrument | `r3_f7.py compare` live (destination and source apart) and its mutant arms | LIVE 3 of 3, MUTANT 2 of 2. Round 2 manifest: present 52,910, missing 0, mismatch 0, extras 0; DEST-VS-MANIFEST EQUAL while SOURCE-VS-MANIFEST reads DRIFTED 49,110 (the producers still write the old home): the two lines are now separate, which is the point of the cell |
| `FB-f-2` table repair under the grain ruling | `r3_mapping.py --arms structure`, `--arms repair` | structure 5 of 5, repair 5 of 5. 3,444 rows: MOVE 349, HOME 2,916, RETIRE 93, DECISION 2, FAULT 84 (was 89; owner `1.0.0_SA_CTO~DELL1` on all 84) |
| `FB-f-3` + `FB-f-4` blind readers | `r3_reader.py` structure arms; `r3_agree.py` over `ANSWERS_A/B.json`, key held by the issuer | reader A 3 of 3, reader B 3 of 3 (each directory holds only `LOCATIONS.json` and its answers file, the list byte for byte the issuer's cut). Canonical arm n=209: system 208, firm 209, tier 209, table 185, **all four 184 of 209**; legacy arm all four 1 of 209 (system unreadable in 155) |
| `FB-f-5` F4's own-firm admit | `r3_f4.py` | OWNFIRM 4 of 4; round 2's POSITIVE 3 of 3 re-read. The other firm's bucket refused the role by the fence's resource-policy deny; an ungranted own-firm key was refused by the identity side |
| `FB-f-6` producer census | `r3_census.py` | 3 of 3: 11 classes, 66 writer lines in 14 scripts, 52,910 objects; the seam's importer count re-read 46 (was 45: the FB-f-13 parity test imports it) |
| `FB-f-7` advTenant remedy, dormant build | router gate, guard suite, F6 diff, dormancy grid, the Rule-24 record | router 51 pass, guard 46 pass, F6 DIFF identical 193 of 193 events through `handleWithMap` and `handler`, dormancy grid router 88 of 88 and guard 396 of 396 identical to base, record 3 of 3 |
| `FB-f-8` window act 1, the advTenant deploy (**APPLIED**) | the pair (both halves and their addenda), the laptop CloudOps lane's apply 08:21Z-08:23Z, the CTO's exercised read, the issuer's live re-read | router **v27 x5**, guard **v6 x5**; `CodeSha256` `cOG/BuFh...` and `YIgGtFj...` equal the built artifacts; the distribution `Deployed`, ETag `E1OAC26XEP0FDI` -> `ELAAK8OWYOWV1`, exactly 10 of 40 associations differ; ACL 6 of 6 rules identical, three groups Count, `LockToken` unchanged. CTO: Branch A (v27 = v26 on 8 of 8 events, v6 = v5 on 4 of 4, live no-session request 401, deployed bytes ASCII). Condition 4 waived for the ACL churn only |
| `FB-f-9` phases A, A2, A3, A4 (dormant, **merged**) | `r3_producers`, `r3_rotation`, `r3_reads`, `r3_dispatch` and the seam's unit tests | seam: 52,910 of 52,910 manifest keys identity in `legacy`, F7 placement in `canonical`; rotation and sentinel 3 of 3; read census 127 sites ROUTED 88, NOT-SERVED 36, EXEMPT 3, UNROUTED 0; dispatcher export 8 of 8, gate 3 of 3, 0 bytes above 127 |
| `FB-f-13` phase A (dormant, **merged**) | `r3_reads.py --files` over the two Lambdas, the parity class, `targets` | 9 sites ROUTED 8, EXEMPT 1 (the probe, routed by the client wrapper), UNROUTED 0; 6 parity tests; `targets` exit 0 (17 targets, lambda plane 4) |

## What the run does not show (stated, not graded)

- **No served byte has moved.** Act 1 changed code and associations, not data; the producers still write `opal-data-bd`
  and the router still serves it. `FB-f-1` reads the copy as a snapshot (49,110 of 52,910 sources changed since).
- **Act 1's behavior under a real user session is not exercised.** The CTO's read used guard events and one no-session
  request; no firm, alias or staff session was in hand. The CTO's own test published three SEV1 messages to the shared
  alert topic by a wrong served bucket (row `D1-S15`).
- **Reader independence** is by construction (two project-free directories, sparse worktrees), not by a seat outside the
  issuing session; the 184 of 209 is an agreement of answers, not proof that no file was opened off the face.
- **The census is a measure, not a promise:** 45 of 46 dynamic-key sites it cannot resolve carry no served-prefix literal;
  non-Python readers were found by reading (two in this round), not by instrument.
- **Dormancy of the producers' build rests on the seam's identity in `legacy` and on static arms**, not on a run of each of
  the 14 scripts; the first production chain with the new code is the first run.
- **The 19 `.py` objects of the build are not yet at `code/gold/`**: the push hook ships them at the next CLOUD push
  (`comp-pipescript deployed`: the 12 catalog writers STALE at S3). `gold_dispatch.sh` carries the switch and is never
  deployed by the hook.

## The round

| order | cell | executor | delivered at | criteria |
|---|---|---|---|---|
| `TO-FB-f-1` | compare instrument | ~11 | merged round 3 drain | AC1, AC2 PASS |
| `TO-FB-f-2` | table repair | ~12 (+ re-seat) | merged, FAULT 89 -> 84 | AC1, AC2 PASS |
| `TO-FB-f-3`, `-4` | blind readers A, B | ~13, ~14 | merged | AC1 PASS each |
| `TO-FB-f-5` | F4 own-firm | ~15 | merged | AC1, AC2 PASS |
| `TO-FB-f-6` | producer census | ~16 | merged; census re-read at `c42ce14860` | AC1 PASS |
| `TO-FB-f-7` | advTenant dormant build | ~17 | `e6ec8ce6e4` | AC1-AC5 PASS |
| `TO-FB-f-8` | act 1 deploy | `0.7.0_AE_CloudOps~FBL` (laptop) | `3a96b7d81f`, ledger closed `554a933b9c`, on CLOUD `818605e9e8` | AC1-AC4 PASS, CTO Branch A |
| `TO-FB-f-9` | act 2 producers | ~16, ~19, ~20, ~21, ~23 (A to A4) | `b0eebb018d`, `628d9f241b`, `19fb066b50`, `2018982711` | phases A-A4 PASS; phase B **parked** |
| `TO-FB-f-10` | act 3 delta copy | -- | tool `0223c09037` | **parked** |
| `TO-FB-f-11` | act 4 router flip | -- | -- | **parked** |
| `TO-FB-f-12` | SMS delivery-status logging | `0.7.0_AE_CloudOps~FBL` | on CLOUD, `pending` | see below |
| `TO-FB-f-13` | acts 4b/4c phase A | ~22 | `23133da0fb` | AC1-AC3 PASS; the two acts **parked** |

## What changed at the close (the issuer's acts)

1. Three orders' `<to_id>` now name the stem their proof instances carry (`4614b6c692`; the shape row `D1-W7-S3` recorded in
   round 2). Four orders `parked`, each with its owner and un-park conditions (`4b68512fd9`, repaired at `e251fed0d1`).
2. The producer census's importer count 45 -> 46 (`c42ce14860`), lane check overridden with the issuer's lane, audited.
3. Two cells added to the frozen decomposition mid-round by the CTO's orders (its amendments 1 and 2): `FB-f-12` (the SMS
   logging) and `FB-f-13` (the Lambda seams). A third, `FB-f-14` (the ownership carve-out), was drafted and NOT cut: the CTO
   withdrew the carve-out before it was spawned (ADDENDUM 7).

## Why the window moved to round 4 (the CTO's ADDENDA 4 to 7, in order)

The carrier of the mode is one export in `gold_dispatch.sh` (built). Three things the instruments and the readers found
make the window one act larger than round 3 could hold: the dispatcher's own freshness gate and two deployed services
(exec-summary, the partners API) read the legacy home (built dormant, parked as acts 4b/4c); the ownership map, the
authorization data of `auth-validator-edge` and the investor-reporting consumers, is the one key of its class and was
missed by both instruments (row `D1-S17`); and the registry's ROUTED bucket alias feeds the router, the guard, the
validator, `data/firm_registry.json` (so IRPT's bucket map at its next apply) and three gold runners, so act 4 cannot flip
only the router. The producers' role also holds no grant on the new prefix (row `D1-S18`).

## What is open

- **`TO-FB-f-12`** is with the laptop lane; its read (the first reason line after the next organic publish) is the CTO's.
  The round does not close until it is terminal.
- **The producers' role grant** (`D1-S18`), the act-4 readers' own dormant cuts and pairs, the registry change for a
  serving-route bucket separate from the routed alias, and the exec-summary and partners-API acts: round 4.
- **The 19 objects' shipment and `gold_dispatch.sh`'s deliberate deploy**: the window's first leg, after the GO.

## Rows at this close

| class | rows | the issuer's reading |
|---|---|---|
| BLOCKING | `D1-S11`, `D1-S12`, `D1-S13`, `S12` | act 1's four stops (non-ASCII in the bundled file; the WAF ACL rider; the explicit Dell deny; the post-apply plan line): each ruled in an amendment of `TO-FB-f-8` and closed by its Branch A |
| BLOCKING | `D1-W16-S10`, `D1-W16-S16`, `D1-W21-S1`, `D1-W23-S1` to `S5` | the naming gate's refusal of the first view, the JSON view's lane refusal, and the non-ASCII bound conflict: ruled in `TO-FB-f-9` amendments 3, 6 and 9, merged |
| BLOCKING | `D1-W22-S4` | the probe's literal: ruled in `TO-FB-f-13` amendment 1 (a client wrapper), merged |
| BLOCKING | `D1-S18` | the producers' role grant: OPEN, carried to round 4 as its own act |
| BLOCKING | `D1-W7-S3`, `D1-W8-S1`, `D1-W10-S1`, `D1-W9-S3` to `S5`, `D1-W11-S1`, `D1-W15-S2` | flip-gate, proof-instance naming and write-grant rows of earlier cells: resolved as in round 2 and in this round's drain (the flips landed; the instance names carry the stem) |
| BLOCKING | `D1-W4-S1`, `D1-W12-S1`, `D1-W12-S4`, `S1` | the cot `positions_cube` collision and the marker-class rows: FAULT, owner `1.0.0_SA_CTO~DELL1`; `S1` (card3 read-logging, an unrelated plan line) is not this project's |
| ARMED | `D1-S4`, `D1-S7` | the stale-copy and staff-proxy hazards: carried by the pair of acts 3 and 4 (ADDENDA 4 to 7); `D1-S17` (the ownership map) is the CTO's tripwire, disarmed at act 4 |
| ARMED | `D1-W16-S2`, `D1-W17-S1`, `D1-W17-S5`, `D1-W21-S2`, `D1-W23-S6`, `D1-W9-S2` | D_00f's literal bucket (closed by phase A), the alias directory dormancy break (ruled: one equivalence class), the gate's `lib/` search order (ruled in amendment 8; the wrapper path holds, a direct call falls back to the legacy read), the `cd` trap (patch merged) |
| ARMED | `C-S2`, `S2`, `S10` | not this project's rows (worktree exposure, an import into shared-infra state, the AWS corpus's zero): owners `0.0.0_AB_MSTR` and `1.0.0_SA_CTO` |

Whether each is DISPOSITIONED in the channel's sense is the CVO's to write; this table is the issuer's evidence.

## For the round-4 analysis (the issuer's reading, not a cut)

1. **Order of the window:** the producers' role grant (laptop, IAM write); the act-4 readers cut dormant (auth-validator-edge
   and the router through the laptop identity, the IRPT consumers, three gold runners); the serving-route field in the
   builder; then acts 2, 3, 4, 4b and 4c in one window, each with its pair and entry.
2. **A reader census over the whole estate by key, not by prefix literal:** the next one must include `.mjs`, `.sh`, `.yaml`
   and Terraform, and resolve template-literal keys; two readers of the authorization data were missed by both instruments.
3. **The SEV1 page path delivers nothing** (rows `D1-S15`, `D1-S16`): `FB-f-12` enables the reason; the remedy is read from
   the first reason line and goes to Andrew if it costs money.
4. **The FAULT 84** (owner CTO) and the worktrees `wk-firmbkts-4` and `-9` (submodule disagreement) are unchanged.
