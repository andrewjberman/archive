# NFRA_CTLPLN round 30 -- drain end and L8 packet, for the CVO and 1.0.0_SA_CTO (issuer 2.0.0_SA_COO~C, DRAFT 2026-10-17 ~02:5xZ; final when TO-APPLY-32's disarm read is terminal)

Round 30 holds seven build orders `complete` (decomposition `NFRA_CTLPLN_DECOMP.round30.md`, amendments 1-9) and one apply order, `TO-APPLY-32` to `0.7.0_AE_CloudOps~NFRA1`, whose last leg (the DISARM read at the 13:00Z scheduled start) is OPEN. `python .tools/round-close-check.py --project NFRA_CTLPLN --round 30` read `verdict=MAY-CLOSE` after the issuer set the short `<to_id>` in three orders (`7de4d4e1db`; the checker first read PROOF-BAD x3, the same defect as round 29). Pins are commits on `box/laptop`, LOCAL unless a push receipt says otherwise. Inputs for the analysis: `ROUND30_INPUTS_FOR_ROUND_ANALYSIS.md` in this folder.

## 1. Judgment criteria owed to the CVO

None on the build orders. EVIDENCE to read: **FWD-8** (the source-map split removes the multi-writer file; the window read of round 29 still stands), **FWD-7**, and, unchanged, FWD-11, 4, 12, 22. The WORLD cells (`CT-ca-1`, `CT-cg-1`, `CT-ch-1`) carry mechanical criteria only; the real runs are in section 3.

## 2. Cells, their orders and the issuer's own re-run in the main tree

| cell | what | merge / flip | issuer re-run (main tree) |
|---|---|---|---|
| `CT-ca-1` | the atomic split of `lambda-source-map.json` into `infra/aws/lambda/ci/function-map/<function>.json` (240 files + README); shared reader `lib/opal_lambda_map.py`; map deleted; deploy path, gates, silent readers fail loud, lane grant; four seatings of worker `~145` (amendments 1-3); the drain regenerated one function file at the moving target | `48d660b0de` / `55616b9796` | `ATOMIC-TF roots=3 fmt_clean=3 uses_fileset=3 equal=240 ok=True`; `ATOMIC-SUITES green_at_base=13 green_after=16 red_after=5 ok=True`; `FUNCTION-MAP arms=13/13`; Terraform plans (read-only) on the branch vs same-hour main: gold-iso and account-return-daily rc 0 No changes; publish-iso the one in-place update main shows identically (live S3 artifact version) |
| `CT-cb-1` | `round-close-check` prints `not_met=<n>`; the crossbox arm repaired; the SWEEP BEFORE MERGE clause in `TASK_ORDER_PROTOCOL.md` | `069539f36a` / `0977ba815c` | (round 30 summary line reads `not_met=0`) |
| `CT-cc-1` | the intake route's npm-tarball limb (`--ecosystem npm`: fetch from `registry.npmjs.org`, two sha512 sources, lifecycle scripts listed, natives named, check 8 NATIVE/LIFECYCLE lines) | `867c77705c` / `b981bea6b2` | `INTAKE-NPM arms=13/13` |
| `CT-cd-1` | check 4 reads the packument; the bun-cache install verb | `888087920b` / `9a661f47cb` | `INTAKE-NPM-PACKUMENT 4/4`; `INTAKE-NPM-INSTALL-TEST 9/9` (dell1's own precheck as the oracle) |
| `CT-ce-1` | the real fetch of dell1's 50 npm tarballs and checks 1-7 | `0d3e64e9f9` / `f04179f9b5` | `NPM-BATCH-FETCH tarballs=50 sha512_equal=True`; five check-2 failures (tool defect) |
| `CT-cf-1` | the package root is the tarball's single top-level folder whatever its name; the five @types records re-run | `5eb73f9a03` / `a474e42df9` | `INTAKE-NPM-TOPDIR arms=12/12`; `NPM-BATCH-CHECK failed_total=0`; neighbours green |
| `CT-cg-1` | the six live follow-on readers of the retired map read the folder (graph, rcg, estate report runner, F2 p137) | `bfbdc20d40` / `323797d9b3` | `FOLLOW-READERS arms=31/31`; `ATOMIC-SPLIT ... census_other=0 live_old_path_users=0 ok=True` (base `census_other=1`) |
| `CT-ch-1` (`TO-APPLY-32`) | ONE `put-object` of the estate report runner at the pin `bfbdc20d40` | order `81a26ba7b2`; deploy `18ff9eac02` (leg PUT and READBACK closed; DISARM open) | live object re-hashed by the issuer: VersionId `HIrQD8nolfYS_30vrMXBXCZJ0_EnqqPz`, sha256 `5e693559...227d` equals the file at the pin |

## 3. The real runs of the outcomes

- **The npm batch, end to end:** CTO check 8 signed (`CTO_CHECK8_NFRA_CTLPLN_INTAKE_NPM_MCPORTAL_BUN_20261016.md` @a9b68b6612: 3 LIFECYCLE and 3 NATIVE lines, no WAIVE); 50 of 50 `verdict=checked` and released by the issuer; pack `verify` `tarballs=50 verified=50 checked=50 stray=0 ok=True`; 151 files Taildropped to dell1 (record `org/devices/intake/records/intake-20261016-npm-mcportal-bun/TAILDROP_RECORD.md`); **dell1's own receipt** (SC1, 23:51Z, `org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.7.0_AE_CloudOps~SC1/round88/cc7_cache_receipt.out` @dcab2d7a41): `SHA512_RECHECK total=50 mismatches_or_failures=0`; `INTAKE-NPM-INSTALL tarballs=50 unpacked=50 already=0 refused=0 present=50/50 ok=True`; `bun_cache_precheck` `77 of 77` rc 0. REALIZED.
- **The split's deploy path:** BLIND until the first real Lambda deploy after `48d660b0de` (the recorder writes one function file). Not yet exercised.
- **The deployed reader:** the runner's lambda hop reading `function-map/` with no WARN at the 13:00Z scheduled start (`0.7.0_AE_CloudOps~NFRA1` reads it; disarms row `NFRA_CTLPLN-W151-S2`). OPEN.

## 4. Rulings this round

- **By the CTO:** the npm limb design (ruling addenda 2 and 3), the approval of the 50 lines (@1e9f508ce9), check 8 signed, the runner upload (msg 109774), the drain rule that a cell regenerates before it merges when the map moved (round-29 ruling 1).
- **By the issuer inside its decomposition:** `CT-ca-1` amendments 1-3 (p170, `lambdamap_cli.py`, two bare `jq` calls, AC3 on `locals.tf` files, p172, p136_sourcemap, the history pins named by parts), the new cells `CT-cf-1`, `CT-cg-1`, `CT-ch-1`, the regeneration of one function file by the drain through the audited lane override (two commits, one lane each).

## 5. Rows minted (OBSERVATION unless stated)

`W145-S1..S3, S8` (BLOCKING, ruled by amendment 1), `S17`, `S18` (BLOCKING, ruled by amendment 3, disarmed by `S20`), `S19..S23`; `W150-S1`, `S2`; `W151-S1` (`rcg/charters.yaml` names the retired map: DOC, inert), `S2` (ARMED, disarm owner the issuer: the runner upload, in flight), `S3..S5` (S5: p137's AC1 and AC2 print FAIL on stale pins of its own entry, as on the pre-split map: IRPT_DASHBD's to rule).

## 6. Open, with owner and condition

- **TO-APPLY-32 disarm read:** owner `0.7.0_AE_CloudOps~NFRA1`; un-parks at the 13:00Z (09:00 ET) start of `estate-report.service`; on a RAISE the order's stop list rolls back to the recorded version `8pG9vs5I4CSGNVC8OcUy2Q9ARArGgumx`.
- **The first Lambda deploy after the split:** the live proof of the deploy path (owner: whichever CloudOps seat deploys first; the issuer reads its ledger).
- **IRPT_DASHBD F2 and D2 seats** (not live on this box): four of their check files were edited by the cell (p170, p172, p136_sourcemap, p137_repin) and the map file no longer exists; p172 AC1 and p137 AC1/AC2 FAIL on content as before the split (rows `W145-S23`, `W151-S5`). Condition: when the seat is live, it reads those rows.
- **FWD-11, 4, 12, 22** (the CVO); Andrew's acts (FWD-2, 6, 14, 27); FWD-10 and FWD-21(a) held.
- Not read by this seat: the live Terraform state beyond the three plans; the HARVST gateway deploy that follows in dell1's order (it stopped on a moved base: their row `D1-S37`).
