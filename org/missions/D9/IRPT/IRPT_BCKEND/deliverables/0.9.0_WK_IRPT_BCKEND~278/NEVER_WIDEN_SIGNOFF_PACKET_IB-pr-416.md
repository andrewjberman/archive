# Never-widen sign-off packet -- IB-pr-416: irpt-performance-adapter, irpt-narrative and irpt-status rebuilt from ONE commit so every served.py call fits its packaged callee

Prepared by 0.9.0_WK_IRPT_BCKEND~278 for 2.0.0_SA_COO~P2 (COO half) and 1.0.0_SA_CTO (CTO half), on row `IRPT_BCKEND-D2-S60` (ruled by `IRPT_BCKEND-D2-S61`; TO-IB-pr-416 AMENDMENTS 1, 2 and 3). Nothing here was uploaded, deployed or applied: BUILD_ONLY from a committed tree, offline replays against SYNTHETIC data with in-memory fakes, AWS reads only (the live zips, their layers, CodeSha256, S3 version, CloudWatch counts). No client data is in this packet or its files: counts, sha256 and reason codes only.

**READ THIS FIRST.**

1. **irpt-performance-adapter is the FIRST apply, and it is FAILING live now.** Its `Enforcer(load_report_owner=)` call raises `TypeError` (the packaged `enforce.py` predates that parameter) on every `performance-report` request that reaches the Enforcer, and the request fails closed. CloudWatch, `/aws/lambda/irpt-performance-adapter`, every page counted client-side, window 2026-10-09T15:41:00Z to 2026-10-11T02:50:45Z (re-run at the time of writing, so the window ends at the current time): **5 performance-report requests refused** (5 `irpt_error` lines, public reason code UNEXPECTED x5; 5 `irpt_internal` lines with exception_type TypeError), first 2026-10-09T15:41:08Z, last 2026-10-09T17:20:16Z (3 pages read). Counts only (`IB117-1_adapter_refusals.json`).
2. **No rollback branch for the adapter restores the older `5nyq8P6v`** (it would undo IB-pr-395's narrowing). The adapter's Branch B is **hold on the current live version `o/643qVE...`** (CodeSha256 `o/643qVECx5UU4Z9sknDp5yUJZb81Zfvp873yDNsc1w=`).
3. **irpt-status's apply WAITS on IRPT_ANLREQ release 1** (2.0.0_SA_COO~Y2). Live irpt-status is rev 3 (`t6OJTCcmOnWGVl8iglcvfGoYb3PbPJqJYqsSgJBpGdI=`, last modified 2026-10-09T18:02:51.000+0000); rev 5 (`DZOdwUOG`) was rolled back after its R3 read caught `RetentionPolicy.reference() takes 3 positional arguments but 4 were given` (CTO half AMENDMENT 7). **This build is the ONE-TREE release that ruling orders for irpt-status**: it carries release 1's line (`status_installed.py` 3e59dc5d6e, `composition.py` and `repository.py`, `resident_installed.py`) with every sibling taken from the same commit, so no member is out of step with the one that calls it. It must not be applied before the release-1 pair has cleared.
4. **The source map is NOT edited** (outside this order's grant). The three zips are built from `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~278/candidate_source_map.json` (a map holding only these three functions, every other key verbatim), via `BAU_SOURCE_MAP_OVERRIDE`; the apply amendment must land those three entries into `infra/aws/lambda/ci/lambda-source-map.json` first, or the real-map build reproduces the split and its sha256 will differ (row `IRPT_BCKEND-D2-W278-S2`, ARMED, disarm owner 2.0.0_SA_COO~P2).
5. **The one tree (AMENDMENT 2) is commit `361c44fa9d40992c8cacfd625cc789536f84b920`.** Every staged row of the three functions whose repo path is under `infra/aws/lambda/investor-reporting/` (and the two gold `data/assets/scripts/gold/investor_reporting/` scripts of the adapter, whose blobs are identical at the old and new pin, so that move changes no byte) is re-pinned to it, its sha256 recomputed from `git show`; each re-pin (member, old pin, new pin, sha256 prefixes) is named per function below and in the census (`repins`). The investor-reporting tree at that commit is byte-equal to box/dell2's at the time of writing (`git diff 361c44fa9d box/dell2 -- infra/aws/lambda/investor-reporting` is empty), so it holds release 1's rows as IRPT_ANLREQ shipped them. Rows OUTSIDE investor-reporting (`lib/`, `org/standards/`, `infra/logic/registry/`, silver scripts, `firm_registry.json`, `_vendor`, `jwt_freshness.py`) keep the map's pins and are listed under `_kept_IB_pr_416` in the candidate map. No member is held at an older pin for a reason in a packet (row `IRPT_BCKEND-D2-W278-S1`).
6. **What rides, said plainly.** One commit means the members that lagged now arrive with the commits in between. The census names every changed member with its owning commits. Beyond the three split callees (`interactive_access.py`, `prospect.py`, `enforce.py`) this includes `served.py` at its HEAD blob (IB-pr-405 adds `analysis-request-read` to svc-custody-statement's operations), irpt-status's `repository.py` and `retention.py` at their HEAD blobs (3fc99be70f, the commits IRPT_ANLREQ AMENDMENT 9 had chosen to drop) and `resident_installed.py`, `owned_report.py`, `entry.py`, `durable_job.py`. The CTO half signs these as one tree (CTO half AMENDMENT 7) and the replay below is the grade, not a member-count limit.

## The closure limbs and the zip census

Instruments (each reads the zip's own bytes; run at its own path, `python <instrument> <zip>`; the packet carries ALL of them beside the zip census, CTO msg 3732):
- `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r2/signature_closure.py` -- ~Y2's original, untouched: the name limb (`from <packaged module> import f`; `f(...)`).
- `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~278/signature_closure_attr.py` (sha256 prefix `a73a3753824fc074`) -- the same with the ATTRIBUTE limb added: `module.f(...)` / `module.Cls(...)` where `module` is a packaged module, and a `**name` unpack resolved statically when `name` is a local dict literal with constant-key stores (this is what reads the adapter's `Enforcer(**render)` split). Last line ends `attr_checked=<k> attr_mismatched=<m>`.
- `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~278/method_call_limb_416.py` (sha256 prefix `4d0412db3aefa214`) -- the METHOD-call limb (AMENDMENT 2; CTO half AMENDMENT 7): `obj.method(...)` checked against EVERY packaged class method of that name; last line `method_call checked=<k> ... mismatched=<m>`. Its negative control is the rev-5 pairing (HEAD `repository.py` 2aa217ec58 with the older `retention.py` 80a79a7462): **2 mismatches, `.reference(4 positional)` against `RetentionPolicy.reference(owner,family,logical_id)`**, exactly the live rev-5 failure.
- `replay/method_call_runner_416.py` -- the dynamic METHOD-call arm, in the replay section below; `replay/live_call_runner_416.py` -- the call sites row D2-S60 names.
- the LIVE-CALL arm of the release-1 half AMENDMENT 5 (one GET answering 200 within a minute of the promote), in its own section below.

| function | pin / tree | built sha256 (CodeSha256 form) | live sha256 | built twice identical | live: name / attr / method mismatches | built: name / attr / method mismatches | attr calls checked (built) | untested import pairings live -> built | bytes |
|---|---|---|---|---|---|---|---|---|---|
| `irpt-performance-adapter` | `687ad3c083` / `361c44fa9d` | `9kYLdR64P0p2TEbDXcQu1hrpQ9KtqjPNnFDpoE/W31A=` | `o/643qVECx5UU4Z9sknDp5yUJZb81Zfvp873yDNsc1w=` | YES | 1 / 1 / 0 | **0 / 0 / 0** | 114 | 23 -> 0 | 445438 |
| `irpt-narrative` | `687ad3c083` / `361c44fa9d` | `x0SqAx2US8UXLnn7Xqy5l3Ttd0Iv1TZQ2jlxgCQtflU=` | `iEwSFL34JQJbihTmChB79GkjXwJaEl9WzMJY2sBEs4k=` | YES | 1 / 2 / 0 | **0 / 0 / 0** | 53 | 9 -> 0 | 220045 |
| `irpt-status` | `687ad3c083` / `361c44fa9d` | `6idtFvAmYk73wJdr5DPRIyEPrLeWgzjlqbdNr5f1wxc=` | `t6OJTCcmOnWGVl8iglcvfGoYb3PbPJqJYqsSgJBpGdI=` | YES | 1 / 0 / 0 | **0 / 0 / 0** | 60 | 21 -> 0 | 361122 |

Last lines of the instruments on each built zip:
- `irpt-performance-adapter`: `signature_closure calls=186 checked=186 skipped_unpack=0 mismatched=0 attr_skipped_unpack=0 attr_checked=114 attr_mismatched=0` | `method_call checked=272 skipped_unpack=8 not_packaged_method=2725 mismatched=0`
- `irpt-narrative`: `signature_closure calls=41 checked=41 skipped_unpack=0 mismatched=0 attr_skipped_unpack=0 attr_checked=53 attr_mismatched=0` | `method_call checked=76 skipped_unpack=0 not_packaged_method=901 mismatched=0`
- `irpt-status`: `signature_closure calls=129 checked=129 skipped_unpack=0 mismatched=0 attr_skipped_unpack=0 attr_checked=60 attr_mismatched=0` | `method_call checked=243 skipped_unpack=18 not_packaged_method=2406 mismatched=0`

Negative control (the live zips): 
- `irpt-performance-adapter`: `signature_closure calls=184 checked=184 skipped_unpack=0 mismatched=1 attr_skipped_unpack=0 attr_checked=113 attr_mismatched=1`
- `irpt-narrative`: `signature_closure calls=41 checked=41 skipped_unpack=0 mismatched=1 attr_skipped_unpack=0 attr_checked=52 attr_mismatched=2`
- `irpt-status`: `signature_closure calls=121 checked=121 skipped_unpack=0 mismatched=1 attr_skipped_unpack=0 attr_checked=60 attr_mismatched=0`

The adapter's Enforcer split reads on the attribute limb alone (the name limb on the live adapter reports only `InteractiveAccess(profile_reader=)`); the live narrative also reads `enforce.Request(path_ids=)` on the attribute limb (row `IRPT_BCKEND-D2-W278-S5`). The live irpt-status (rev 3) reads the `profile_reader` split on the name limb. **The untested import pairings column is `pin_coherence.py`'s skew count** (`IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r2/pin_coherence.py`, run on the real map at box/dell2 for the live column, on the candidate map for the built column; live irpt-status: 21): a pairing nobody has run is a skew; one tree leaves 0, 0 and 0.

The built zips were built twice with `TMPDIR=<scratch> BAU_SOURCE_MAP_OVERRIDE=<candidate> BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting <function>` from a tree whose investor-reporting paths are committed, and are byte-identical across the two runs; the zips stay in scratch, outside the worktree.

## Per function

### 1. `irpt-performance-adapter`  -- THE FIRST APPLY (failing live)

- **Live sha256** (CodeSha256): `o/643qVECx5UU4Z9sknDp5yUJZb81Zfvp873yDNsc1w=`, last modified 2026-10-09T07:41:59.000+0000; it equals the `content-sha256` metadata of the LATEST S3 version of `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-performance-adapter.zip`: **yes**.
- **Built sha256** (CodeSha256 form): `9kYLdR64P0p2TEbDXcQu1hrpQ9KtqjPNnFDpoE/W31A=` (hex `f6460b751eb83f4a764c46c35dc42ed61ae943d2adaa33cd9c50e9a04fd6df50`, 445438 bytes), built twice identical: YES.
- **Changed members vs live: 13** (live 71 members, built the same count):
  - changed `canonical_profile_reads.py` (built `30c8a05ad674`, live `0ec4a717f2aa`): 8540c9dd8f
  - changed `composition.py` (built `5b896004af77`, live `6d2c3696d030`): 2aa217ec58, f60e6f1d2a
  - changed `data/custodian_key_seam.json` (built `541c2d8acdf6`, live `87f2f92f3c71`): e962a5cb81
  - changed `enforce.py` (built `f5681952cb09`, live `4245b5f8aded`): 8d08ee54e4, 7605bbf5ab
  - changed `ids.py` (built `43acb10d9895`, live `f1659861d469`): 11ba48fdc7, e962a5cb81
  - changed `interactive_access.py` (built `c28d9a74c9af`, live `bba07a3f4eeb`): c101699a71
  - changed `loaders.py` (built `72f22ea3a43c`, live `93f2f02a1bd4`): 2a56d11744
  - changed `maintained_sources.py` (built `29c35dbfba72`, live `774eca9bde60`): 8e6011bda1, bb255c4cb2
  - changed `repository.py` (built `d94dc2c74c75`, live `f255335beb26`): 3fc99be70f, 589aee38f0, 20534db618, 2aa217ec58 +2
  - changed `request_composition.py` (built `15b622b7a5f3`, live `b82c1ad7d7c9`): bb255c4cb2, f8c72944f3
  - changed `retained_input_authorizer.py` (built `f87ed11a3805`, live `928f44e5ad9c`): 8540c9dd8f
  - changed `retention.py` (built `9da406b7d6e4`, live `bdd74e5f9b90`): 3fc99be70f, 20534db618, f60e6f1d2a
  - changed `served.py` (built `ada9bf5bcfd1`, live `87d9ecc49747`): 1cb1c965f3
- **Re-pins (52 rows; 13 change the packaged bytes):**
  - `accepted_custody.py`: b905df2c60 -> 361c44fa9d (`748d54550cba` -> `748d54550cba`) [pin only, same bytes]
  - `authz_dispatch.py`: b905df2c60 -> 361c44fa9d (`fdc0091fa3be` -> `fdc0091fa3be`) [pin only, same bytes]
  - `bd_adapter.py`: b905df2c60 -> 361c44fa9d (`437b5b3827a5` -> `437b5b3827a5`) [pin only, same bytes]
  - `bd_live.py`: b905df2c60 -> 361c44fa9d (`c815a8ca2b5d` -> `c815a8ca2b5d`) [pin only, same bytes]
  - `bd_selected.py`: f360e6c80e -> 361c44fa9d (`1852662806b6` -> `1852662806b6`) [pin only, same bytes]
  - `canonical_profile_reads.py`: f9a00f732c -> 361c44fa9d (`0ec4a717f2aa` -> `30c8a05ad674`)
  - `composition.py`: b905df2c60 -> 361c44fa9d (`6d2c3696d030` -> `5b896004af77`)
  - `currency_authority.py`: b905df2c60 -> 361c44fa9d (`83f7fe0311b5` -> `83f7fe0311b5`) [pin only, same bytes]
  - `custody.py`: b905df2c60 -> 361c44fa9d (`23cda6b0e3dd` -> `23cda6b0e3dd`) [pin only, same bytes]
  - `custody_binding.py`: b905df2c60 -> 361c44fa9d (`a01c31283506` -> `a01c31283506`) [pin only, same bytes]
  - `data/assets/scripts/gold/investor_reporting/cot_account_mapping.py`: b905df2c60 -> 361c44fa9d (`c2012a4bc693` -> `c2012a4bc693`) [pin only, same bytes]
  - `data/assets/scripts/gold/investor_reporting/source_inputs.py`: b905df2c60 -> 361c44fa9d (`267228c6bb36` -> `267228c6bb36`) [pin only, same bytes]
  - `data/custodian_key_seam.json`: b905df2c60 -> 361c44fa9d (`87f2f92f3c71` -> `541c2d8acdf6`)
  - `enforce.py`: b905df2c60 -> 361c44fa9d (`4245b5f8aded` -> `f5681952cb09`)
  - `entry.py`: b15f0ed7df -> 361c44fa9d (`d19c0386176b` -> `d19c0386176b`) [pin only, same bytes]
  - `error_path_census.py`: b905df2c60 -> 361c44fa9d (`258d06efe289` -> `258d06efe289`) [pin only, same bytes]
  - `errors.py`: b905df2c60 -> 361c44fa9d (`b60f25ccaa70` -> `b60f25ccaa70`) [pin only, same bytes]
  - `global.py`: b905df2c60 -> 361c44fa9d (`a097f820caa4` -> `a097f820caa4`) [pin only, same bytes]
  - `handler.py`: b905df2c60 -> 361c44fa9d (`9ac98cb98560` -> `9ac98cb98560`) [pin only, same bytes]
  - `ids.py`: b905df2c60 -> 361c44fa9d (`f1659861d469` -> `43acb10d9895`)
  - `installed.py`: 89b5a85abe -> 361c44fa9d (`8e42e8b24596` -> `8e42e8b24596`) [pin only, same bytes]
  - `interactive_access.py`: b905df2c60 -> 361c44fa9d (`bba07a3f4eeb` -> `c28d9a74c9af`)
  - `keys.py`: b905df2c60 -> 361c44fa9d (`56ee3cc22e80` -> `56ee3cc22e80`) [pin only, same bytes]
  - `loaders.py`: 0642c9d004 -> 361c44fa9d (`93f2f02a1bd4` -> `72f22ea3a43c`)
  - `maintained_sources.py`: f9a00f732c -> 361c44fa9d (`774eca9bde60` -> `29c35dbfba72`)
  - `normalize.py`: b905df2c60 -> 361c44fa9d (`203fddcd3393` -> `203fddcd3393`) [pin only, same bytes]
  - `orion_adapter.py`: b905df2c60 -> 361c44fa9d (`3ea1d42e73cc` -> `3ea1d42e73cc`) [pin only, same bytes]
  - `owner_reads.py`: b905df2c60 -> 361c44fa9d (`f21d26dcce7c` -> `f21d26dcce7c`) [pin only, same bytes]
  - `prospect.py`: b905df2c60 -> 361c44fa9d (`f556b0997dfa` -> `f556b0997dfa`) [pin only, same bytes]
  - `raw_keys.json`: b905df2c60 -> 361c44fa9d (`f81db571b5d9` -> `f81db571b5d9`) [pin only, same bytes]
  - `repository.py`: b905df2c60 -> 361c44fa9d (`f255335beb26` -> `d94dc2c74c75`)
  - `request_composition.py`: b905df2c60 -> 361c44fa9d (`b82c1ad7d7c9` -> `15b622b7a5f3`)
  - `resolve.py`: b905df2c60 -> 361c44fa9d (`24b407fa00ff` -> `24b407fa00ff`) [pin only, same bytes]
  - `retained.py`: 259b6c6745 -> 361c44fa9d (`ab73f5261095` -> `ab73f5261095`) [pin only, same bytes]
  - `retained_input_authorizer.py`: b905df2c60 -> 361c44fa9d (`928f44e5ad9c` -> `f87ed11a3805`)
  - `retention.py`: b905df2c60 -> 361c44fa9d (`bdd74e5f9b90` -> `9da406b7d6e4`)
  - `routetable.py`: f9a00f732c -> 361c44fa9d (`fbd20fb97a64` -> `fbd20fb97a64`) [pin only, same bytes]
  - `selection.py`: b905df2c60 -> 361c44fa9d (`7ba910b85e2f` -> `7ba910b85e2f`) [pin only, same bytes]
  - `selection_store.py`: b905df2c60 -> 361c44fa9d (`583507a70e3a` -> `583507a70e3a`) [pin only, same bytes]
  - `served.py`: 74a62fb46c -> 361c44fa9d (`87d9ecc49747` -> `ada9bf5bcfd1`)
  - `tenants.py`: b905df2c60 -> 361c44fa9d (`38812b9686ec` -> `38812b9686ec`) [pin only, same bytes]
  - `transport.py`: b905df2c60 -> 361c44fa9d (`4714482707b9` -> `4714482707b9`) [pin only, same bytes]
  - `units.py`: b905df2c60 -> 361c44fa9d (`1a21813a964c` -> `1a21813a964c`) [pin only, same bytes]
  - `authorization.py`: b905df2c60 -> 361c44fa9d (`346be20736ba` -> `346be20736ba`) [pin only, same bytes]
  - `runtime.py`: bb09a3467c -> 361c44fa9d (`935d563346c2` -> `935d563346c2`) [pin only, same bytes]
  - `f49_engine.py`: 57a58117fb -> 361c44fa9d (`07ce5fffb20f` -> `07ce5fffb20f`) [pin only, same bytes]
  - `orion_selected.py`: a7e9f51c77 -> 361c44fa9d (`2e02eedc34bb` -> `2e02eedc34bb`) [pin only, same bytes]
  - `orion_account_mapping.py`: a7e9f51c77 -> 361c44fa9d (`e300069ebdc6` -> `e300069ebdc6`) [pin only, same bytes]
  - `orion_live.py`: a7e9f51c77 -> 361c44fa9d (`c39bca88128e` -> `c39bca88128e`) [pin only, same bytes]
  - `grant.py`: c4fedd31c5 -> 361c44fa9d (`51785ed4b834` -> `51785ed4b834`) [pin only, same bytes]
  - `report_owner.py`: c4fedd31c5 -> 361c44fa9d (`610982ce5bdd` -> `610982ce5bdd`) [pin only, same bytes]
  - `holdings_gold.py`: 0642c9d004 -> 361c44fa9d (`d41e861212a7` -> `d41e861212a7`) [pin only, same bytes]
- **Branch A (land it):** from a clean tree at P `687ad3c083` (or a descendant whose `narrative/`, `ops/`, `performance/`, `reports/`, `_authz/` ... trees and the three candidate entries are unchanged) with the three candidate entries landed in the source map, `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-performance-adapter` and compare the printed sha256 to `9kYLdR64P0p2TEbDXcQu1hrpQ9KtqjPNnFDpoE/W31A=` (ABORT if different), then the same without BUILD_ONLY, then the module's Terraform path (`s3_object_version` + `source_code_hash` only). No IAM, route, schedule, layer or environment change.
- **Branch B (hold):** there is no rollback to restore. **Hold on the current live version `o/643qVECx5UU4Z9sknDp5yUJZb81Zfvp873yDNsc1w=`** (S3 version `P2.k8l8dqM7nlKcd8O1.Hzo5ugCCceiR`, re-read at apply: `get-function-configuration` CodeSha256 and the version still the latest). `5nyq8P6v` is NOT a rollback target (IB-pr-395's narrowing).

### 2. `irpt-narrative`

- **Live sha256** (CodeSha256): `iEwSFL34JQJbihTmChB79GkjXwJaEl9WzMJY2sBEs4k=`, last modified 2026-10-09T14:48:05.000+0000; it equals the `content-sha256` metadata of the LATEST S3 version of `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-narrative.zip`: **yes**.
- **Built sha256** (CodeSha256 form): `x0SqAx2US8UXLnn7Xqy5l3Ttd0Iv1TZQ2jlxgCQtflU=` (hex `c744aa031d944bc5172e79fb5eacb99774ed77422fd53650da397180242d7e55`, 220045 bytes), built twice identical: YES.
- **Changed members vs live: 9** (live 27 members, built the same count):
  - changed `canonical_profile_reads.py` (built `30c8a05ad674`, live `0ec4a717f2aa`): 8540c9dd8f
  - changed `data/custodian_key_seam.json` (built `541c2d8acdf6`, live `87f2f92f3c71`): e962a5cb81
  - changed `enforce.py` (built `f5681952cb09`, live `18f04af84b9c`): 8d08ee54e4, 7605bbf5ab, 755c13bc19, fe854ce6f1
  - changed `ids.py` (built `43acb10d9895`, live `f1659861d469`): 11ba48fdc7, e962a5cb81
  - changed `loaders.py` (built `72f22ea3a43c`, live `b84bb2918fc1`): 2a56d11744, 8540c9dd8f, 8e6011bda1, 8e9ed1b539 +4
  - changed `maintained_sources.py` (built `29c35dbfba72`, live `774eca9bde60`): 8e6011bda1, bb255c4cb2
  - changed `owner_reads.py` (built `f21d26dcce7c`, live `f9e1f5d3274e`): 4ec461a2e9
  - changed `prospect.py` (built `f556b0997dfa`, live `b7e5c9335caa`): 4ec461a2e9
  - changed `served.py` (built `ada9bf5bcfd1`, live `87d9ecc49747`): 1cb1c965f3
- **Re-pins (16 rows; 9 change the packaged bytes):**
  - `enforce.py`: bc3727b3a3 -> 361c44fa9d (`18f04af84b9c` -> `f5681952cb09`)
  - `errors.py`: 74a62fb46c -> 361c44fa9d (`b60f25ccaa70` -> `b60f25ccaa70`) [pin only, same bytes]
  - `resolve.py`: bc3727b3a3 -> 361c44fa9d (`24b407fa00ff` -> `24b407fa00ff`) [pin only, same bytes]
  - `data/custodian_key_seam.json`: c28c728a30 -> 361c44fa9d (`87f2f92f3c71` -> `541c2d8acdf6`)
  - `ids.py`: c28c728a30 -> 361c44fa9d (`f1659861d469` -> `43acb10d9895`)
  - `raw_keys.json`: 47f21dab95 -> 361c44fa9d (`f81db571b5d9` -> `f81db571b5d9`) [pin only, same bytes]
  - `loaders.py`: bc3727b3a3 -> 361c44fa9d (`b84bb2918fc1` -> `72f22ea3a43c`)
  - `served.py`: 74a62fb46c -> 361c44fa9d (`87d9ecc49747` -> `ada9bf5bcfd1`)
  - `selection.py`: bc3727b3a3 -> 361c44fa9d (`7ba910b85e2f` -> `7ba910b85e2f`) [pin only, same bytes]
  - `selection_store.py`: bc3727b3a3 -> 361c44fa9d (`583507a70e3a` -> `583507a70e3a`) [pin only, same bytes]
  - `prospect.py`: bc3727b3a3 -> 361c44fa9d (`b7e5c9335caa` -> `f556b0997dfa`)
  - `owner_reads.py`: bc3727b3a3 -> 361c44fa9d (`f9e1f5d3274e` -> `f21d26dcce7c`)
  - `custody.py`: bc3727b3a3 -> 361c44fa9d (`23cda6b0e3dd` -> `23cda6b0e3dd`) [pin only, same bytes]
  - `keys.py`: 48946e7972 -> 361c44fa9d (`56ee3cc22e80` -> `56ee3cc22e80`) [pin only, same bytes]
  - `canonical_profile_reads.py`: 2704705672 -> 361c44fa9d (`0ec4a717f2aa` -> `30c8a05ad674`)
  - `maintained_sources.py`: 15b9f85eb3 -> 361c44fa9d (`774eca9bde60` -> `29c35dbfba72`)
- **Branch A (land it):** from a clean tree at P `687ad3c083` (or a descendant whose `narrative/`, `ops/`, `performance/`, `reports/`, `_authz/` ... trees and the three candidate entries are unchanged) with the three candidate entries landed in the source map, `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-narrative` and compare the printed sha256 to `x0SqAx2US8UXLnn7Xqy5l3Ttd0Iv1TZQ2jlxgCQtflU=` (ABORT if different), then the same without BUILD_ONLY, then the module's Terraform path (`s3_object_version` + `source_code_hash` only). No IAM, route, schedule, layer or environment change.
- **Branch B (rolled back):** redeploy the prior artifact through the same Terraform path (never a console edit): S3 object version `Tuz7VAl4qh0fd6c_7OcSTNY.PRgBCsc3` (its CodeSha256 is the live value above). Re-read at apply: `get-function-configuration` CodeSha256 unchanged and the version still the latest.

### 3. `irpt-status`  -- apply waits on IRPT_ANLREQ release 1

- **Live sha256** (CodeSha256): `t6OJTCcmOnWGVl8iglcvfGoYb3PbPJqJYqsSgJBpGdI=`, last modified 2026-10-09T18:02:51.000+0000; it equals the `content-sha256` metadata of the LATEST S3 version of `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-status.zip`: **yes**.
- **Built sha256** (CodeSha256 form): `6idtFvAmYk73wJdr5DPRIyEPrLeWgzjlqbdNr5f1wxc=` (hex `ea276d16f026624ef7c0976be433d123210facb7968338e5a9b74daf97f5c317`, 361122 bytes), built twice identical: YES.
- **Changed members vs live: 13** (live 49 members, built the same count):
  - changed `composition.py` (built `5b896004af77`, live `6d2c3696d030`): 2aa217ec58, f60e6f1d2a
  - changed `data/custodian_key_seam.json` (built `541c2d8acdf6`, live `87f2f92f3c71`): e962a5cb81
  - changed `durable_job.py` (built `afba08fefbbc`, live `b5192fa2a1d4`): 3acafb3f45
  - changed `entry.py` (built `4a5dd2e887cb`, live `0a9875d45e72`): 1cb1c965f3
  - changed `ids.py` (built `43acb10d9895`, live `f1659861d469`): 11ba48fdc7, e962a5cb81
  - changed `interactive_access.py` (built `c28d9a74c9af`, live `bba07a3f4eeb`): c101699a71
  - changed `loaders.py` (built `72f22ea3a43c`, live `93f2f02a1bd4`): 2a56d11744
  - changed `owned_report.py` (built `542047cf584f`, live `819e3694f7b3`): aff85bff09, 9489a0fed0, 1cb1c965f3
  - changed `repository.py` (built `d94dc2c74c75`, live `f255335beb26`): 3fc99be70f, 589aee38f0, 20534db618, 2aa217ec58 +2
  - changed `resident_installed.py` (built `380eb1f846ca`, live `7e69601a8bfd`): f9daebcb8e, 2c721e21f2, bfed18a189
  - changed `retention.py` (built `9da406b7d6e4`, live `bdd74e5f9b90`): 3fc99be70f, 20534db618, f60e6f1d2a
  - changed `served.py` (built `ada9bf5bcfd1`, live `87d9ecc49747`): 1cb1c965f3
  - changed `status_installed.py` (built `326fed4f54b4`, live `59853db310e6`): 3e59dc5d6e, 2a69da80ec
- **Re-pins (32 rows; 11 change the packaged bytes):**
  - `enforce.py`: 80a79a7462 -> 361c44fa9d (`f5681952cb09` -> `f5681952cb09`) [pin only, same bytes]
  - `errors.py`: 80a79a7462 -> 361c44fa9d (`b60f25ccaa70` -> `b60f25ccaa70`) [pin only, same bytes]
  - `resolve.py`: 80a79a7462 -> 361c44fa9d (`24b407fa00ff` -> `24b407fa00ff`) [pin only, same bytes]
  - `keys.py`: 80a79a7462 -> 361c44fa9d (`56ee3cc22e80` -> `56ee3cc22e80`) [pin only, same bytes]
  - `handler.py`: 80a79a7462 -> 361c44fa9d (`3865775e75f8` -> `3865775e75f8`) [pin only, same bytes]
  - `checkpoint.py`: 80a79a7462 -> 361c44fa9d (`ba19eec556e9` -> `ba19eec556e9`) [pin only, same bytes]
  - `data/custodian_key_seam.json`: 80a79a7462 -> 361c44fa9d (`87f2f92f3c71` -> `541c2d8acdf6`)
  - `ids.py`: 80a79a7462 -> 361c44fa9d (`f1659861d469` -> `43acb10d9895`)
  - `raw_keys.json`: 80a79a7462 -> 361c44fa9d (`f81db571b5d9` -> `f81db571b5d9`) [pin only, same bytes]
  - `loaders.py`: 0642c9d004 -> 361c44fa9d (`93f2f02a1bd4` -> `72f22ea3a43c`)
  - `served.py`: 74a62fb46c -> 361c44fa9d (`87d9ecc49747` -> `ada9bf5bcfd1`)
  - `selection.py`: 80a79a7462 -> 361c44fa9d (`7ba910b85e2f` -> `7ba910b85e2f`) [pin only, same bytes]
  - `selection_store.py`: 80a79a7462 -> 361c44fa9d (`583507a70e3a` -> `583507a70e3a`) [pin only, same bytes]
  - `prospect.py`: 80a79a7462 -> 361c44fa9d (`f556b0997dfa` -> `f556b0997dfa`) [pin only, same bytes]
  - `owner_reads.py`: 80a79a7462 -> 361c44fa9d (`f21d26dcce7c` -> `f21d26dcce7c`) [pin only, same bytes]
  - `custody.py`: 80a79a7462 -> 361c44fa9d (`23cda6b0e3dd` -> `23cda6b0e3dd`) [pin only, same bytes]
  - `status_installed.py`: 3e59dc5d6e -> 361c44fa9d (`326fed4f54b4` -> `326fed4f54b4`) [pin only, same bytes]
  - `resident_installed.py`: 80a79a7462 -> 361c44fa9d (`7e69601a8bfd` -> `380eb1f846ca`)
  - `composition.py`: 2aa217ec58 -> 361c44fa9d (`5b896004af77` -> `5b896004af77`) [pin only, same bytes]
  - `repository.py`: 2aa217ec58 -> 361c44fa9d (`f01fcf549e8e` -> `d94dc2c74c75`)
  - `retention.py`: 80a79a7462 -> 361c44fa9d (`bdd74e5f9b90` -> `9da406b7d6e4`)
  - `acceptance.py`: 1eed34a8c0 -> 361c44fa9d (`06425d4731b7` -> `06425d4731b7`) [pin only, same bytes]
  - `durable_job.py`: 80a79a7462 -> 361c44fa9d (`b5192fa2a1d4` -> `afba08fefbbc`)
  - `submission.py`: 1eed34a8c0 -> 361c44fa9d (`82c47bd021c5` -> `82c47bd021c5`) [pin only, same bytes]
  - `interactive_access.py`: 80a79a7462 -> 361c44fa9d (`bba07a3f4eeb` -> `c28d9a74c9af`)
  - `canonical_profile_reads.py`: 0642c9d004 -> 361c44fa9d (`30c8a05ad674` -> `30c8a05ad674`) [pin only, same bytes]
  - `maintained_sources.py`: 0642c9d004 -> 361c44fa9d (`29c35dbfba72` -> `29c35dbfba72`) [pin only, same bytes]
  - `entry.py`: eb70303e8f -> 361c44fa9d (`0a9875d45e72` -> `4a5dd2e887cb`)
  - `owned_report.py`: 62880e9bfc -> 361c44fa9d (`819e3694f7b3` -> `542047cf584f`)
  - `status.py`: 80a79a7462 -> 361c44fa9d (`cb3b2ea620f8` -> `cb3b2ea620f8`) [pin only, same bytes]
  - `grant.py`: 80a79a7462 -> 361c44fa9d (`51785ed4b834` -> `51785ed4b834`) [pin only, same bytes]
  - `report_owner.py`: 80a79a7462 -> 361c44fa9d (`610982ce5bdd` -> `610982ce5bdd`) [pin only, same bytes]
- **Branch A (land it):** from a clean tree at P `687ad3c083` (or a descendant whose `narrative/`, `ops/`, `performance/`, `reports/`, `_authz/` ... trees and the three candidate entries are unchanged) with the three candidate entries landed in the source map, `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-status` and compare the printed sha256 to `6idtFvAmYk73wJdr5DPRIyEPrLeWgzjlqbdNr5f1wxc=` (ABORT if different), then the same without BUILD_ONLY, then the module's Terraform path (`s3_object_version` + `source_code_hash` only). No IAM, route, schedule, layer or environment change.
- **Branch B (rolled back):** redeploy the prior artifact through the same Terraform path (never a console edit): S3 object version `iDIQPfNUQM8EH4pjrG.codFMMaR071yi` (its CodeSha256 is the live value above). Re-read at apply: `get-function-configuration` CodeSha256 unchanged and the version still the latest.
- **Order:** this apply waits on IRPT_ANLREQ release 1 (2.0.0_SA_COO~Y2). Apply it only with or after that pair.
- **Two after-reads for the apply leg (AMENDMENT 3), both run by `~G2` in an sr1 window, with the 5xx and TypeError counts of the R3 read printed beside them:**
  1. REQ-5e4149d2's owner read (status-job + analysis-report) answers with **no RetentionRefused and no TypeError**;
  2. one GET `.../analysis/requests/{id}/original` answers, and **the count stays 1** (the read does not write).
- **Release 1's last two irpt-status reads are deferred to this build** (they cannot run on rev 3, which lacks the reader members).

## Blast radius

- **Functions:** irpt-performance-adapter, irpt-narrative, irpt-status; no other function, layer, IAM, route, schedule, environment or table changes.
- **Members:** the per-function lists above. Shared code in the repo is unchanged by this cell (the cell edits no product source); the packaged bytes are the blobs of commit `361c44fa9d`.
- **Effect on served bytes:** the adapter's `performance-report` stops failing on `Enforcer(load_report_owner=)` (it reaches the Enforcer with the retained-owner port, as IB-pr-293 intended); the narrative's prospect path stops raising on `guard_prospect(authorize_owner=, resolve_owner=)` and `enforce.Request(path_ids=)` fits; the status internal-caller CREATE path stops raising on `InteractiveAccess(profile_reader=)`; irpt-status serves the owned-history readers of release 1 on one consistent set. Authorization decisions on the arms below are identical live vs built except where an arm is marked expected-diff and names the live TypeError.

## The ADDENDUM 18 red list

`pytest _contracts -rf` from `infra/aws/lambda/investor-reporting/` at the pin: **2 failed, 198 passed in 7.67s**. The FAILED node ids (2):
- `_contracts/tests/test_seam_paired.py::test_every_declared_route_has_a_response_contract_whose_refs_resolve`
- `_contracts/tests/test_seam_paired.py::test_control_a_known_good_document_conforms_and_a_known_bad_one_does_not[analysis-request-original]`

Their targets are the response contracts / fixtures of `analysis-request-original` and the declared-route response refs. This cell changes 12 paths vs its base (all under its deliverables folder); the packaged members' source paths number 20. Intersection with the red tests' target surface (`infra/aws/lambda/investor-reporting/_contracts/`, `docs/contracts/investor-reporting/`) and with any path naming a red operation: **0 changed, 0 member, 0 naming** -- STOP = **no**. `analysis-request-original` is a route irpt-status declares; none of its changed members is that route's contract, fixture or handler. This packet does not cite "suite green".

## The replay (offline; live zip against built zip; `IB117-1_replay.json`)

AMENDMENT 2 grades each build by a REPLAY OF EVERY ROUTE plus the LIVE-CALL arm plus a METHOD-call arm. Each tree is extracted (`python -I`, flat layout, the function's live layers beside it) and the zip's own `entry.ENTRY` is driven by IB-pr-409's `authz_case_runner.py` (unchanged: every route of the function, six binding cases each), `replay/scope_runner_416.py` (row D2-S48's method, route per host), `replay/live_call_runner_416.py` (the three split call sites: the LIVE-CALL arm at the code level) and `replay/method_call_runner_416.py` (the METHOD-call arm: the real Entry's `handle` called for EACH route, two principals, synthetic event, in-memory fake clients, a `sys.settrace` hook that records every call-arity TypeError raised in the zip even when the code catches it). The NEGATIVE CONTROL tree is the built tree with `interactive_access.py`, `prospect.py` and `enforce.py` put back to the LIVE bytes. Verdicts are exactly `identical` or `expected-diff`: 47 arms, none UNEXPECTED.

| function | arm | verdict | negative control | detail |
|---|---|---|---|---|
| `irpt-performance-adapter` | prospect arm prospect_internal_no_row_CREATE_INPUT: built does not raise TypeError | expected-diff | no | live: recorded=['TypeError'] escaped=None code=UNEXPECTED compute_reached=False / built: recorded=[] escaped=None code=None compute_reached=True |
| `irpt-performance-adapter` | NEGATIVE CONTROL prospect arm prospect_internal_no_row_CREATE_INPUT: the built tree with interactive_access.py, prospect.py and enforce.py put back to the LIVE bytes | expected-diff | yes | control: recorded=['TypeError'] escaped=None code=UNEXPECTED compute_reached=False / live: recorded=['TypeError'] escaped=None code=UNEXPECTED compute_reached=False |
| `irpt-performance-adapter` | prospect arm prospect_internal_no_row_OWNED_INPUT: built does not raise TypeError | identical | no | live: recorded=['ProspectOwnershipRefused'] escaped=None code=NOT_AUTHORIZED compute_reached=False / built: recorded=['ProspectOwnershipRefused'] escaped=None code=NOT_AUTHORIZED compute_reached=False |
| `irpt-performance-adapter` | NEGATIVE CONTROL prospect arm prospect_internal_no_row_OWNED_INPUT: the built tree with interactive_access.py, prospect.py and enforce.py put back to the LIVE bytes | identical | yes | control: recorded=['ProspectOwnershipRefused'] escaped=None code=NOT_AUTHORIZED compute_reached=False / live: recorded=['ProspectOwnershipRefused'] escaped=None code=NOT_AUTHORIZED compute_reached=False |
| `irpt-performance-adapter` | prospect arm prospect_firm_user_CREATE_INPUT: built does not raise TypeError | identical | no | live: recorded=[] escaped=None code=None compute_reached=True / built: recorded=[] escaped=None code=None compute_reached=True |
| `irpt-performance-adapter` | NEGATIVE CONTROL prospect arm prospect_firm_user_CREATE_INPUT: the built tree with interactive_access.py, prospect.py and enforce.py put back to the LIVE bytes | identical | yes | control: recorded=[] escaped=None code=None compute_reached=True / live: recorded=[] escaped=None code=None compute_reached=True |
| `irpt-performance-adapter` | prospect arm prospect_firm_user_OWNED_INPUT: built does not raise TypeError | identical | no | live: recorded=[] escaped=None code=None compute_reached=True / built: recorded=[] escaped=None code=None compute_reached=True |
| `irpt-performance-adapter` | NEGATIVE CONTROL prospect arm prospect_firm_user_OWNED_INPUT: the built tree with interactive_access.py, prospect.py and enforce.py put back to the LIVE bytes | identical | yes | control: recorded=[] escaped=None code=None compute_reached=True / live: recorded=[] escaped=None code=None compute_reached=True |
| `irpt-performance-adapter` | enforcer build with the load_report_owner port: built constructs the Enforcer | expected-diff | no | live: escaped=TypeError built_enforcer=False / built: escaped=None built_enforcer=True |
| `irpt-performance-adapter` | NEGATIVE CONTROL enforcer build: the built tree with enforce.py put back to the LIVE bytes | expected-diff | yes | control: escaped=TypeError / live: escaped=TypeError |
| `irpt-performance-adapter` | no_row_internal_enforcer_scope (+ row-listed): class, roster and permitted set, live vs built | identical | no | no_row_no_selection live=OPAL_GLOBAL/['ops@opalinvest.com']/2 built=OPAL_GLOBAL/['ops@opalinvest.com']/2; no_row_selecting_other live=OPAL_GLOBAL/['ops@opalinvest.com']/2 built=OPAL_GLOBAL/['ops@opalinvest.com']/2; row_listed_no_selection live=OPAL_GLOBAL/['ops@opalinvest.com']/2 built=OPAL_GLOBAL/['ops@opalinvest.com']/2 |
| `irpt-performance-adapter` | binding cases (userOwn, userSelOther, userClaimOther, noRow, rowCotCot, rowCotInf) through the real entry.ENTRY, live vs built | identical | no | 6 cases over 1 route(s); differing: none; HARNESS_* on built: none, on live: none |
| `irpt-performance-adapter` | method-call arm performance-report: built handler raises no call-arity TypeError | expected-diff | no | built arity errors=0 escaped=none codes={'firm_user_own': 'FIRM_BINDING', 'internal_row_listed': 'FIRM_BINDING'} functions_entered(firm_user_own/internal_row_listed)=54/56 / live arity errors=4 codes={'firm_user_own': 'UNEXPECTED', 'internal_row_listed': 'UNEXPECTED'} |
| `irpt-performance-adapter` | NEGATIVE CONTROL method-call arm performance-report: the LIVE zip reads arity errors | expected-diff | yes | live arity errors=4 at ['served:1255', 'served:856'] |
| `irpt-narrative` | prospect arm prospect_internal_no_row_CREATE_INPUT: built does not raise TypeError | identical | no | live: recorded=['ModuleNotFoundError'] escaped=None code=UNEXPECTED compute_reached=False / built: recorded=['ModuleNotFoundError'] escaped=None code=UNEXPECTED compute_reached=False |
| `irpt-narrative` | NEGATIVE CONTROL prospect arm prospect_internal_no_row_CREATE_INPUT: the built tree with interactive_access.py, prospect.py and enforce.py put back to the LIVE bytes | identical | yes | control: recorded=['ModuleNotFoundError'] escaped=None code=UNEXPECTED compute_reached=False / live: recorded=['ModuleNotFoundError'] escaped=None code=UNEXPECTED compute_reached=False |
| `irpt-narrative` | prospect arm prospect_internal_no_row_OWNED_INPUT: built does not raise TypeError | identical | no | live: recorded=['ModuleNotFoundError'] escaped=None code=UNEXPECTED compute_reached=False / built: recorded=['ModuleNotFoundError'] escaped=None code=UNEXPECTED compute_reached=False |
| `irpt-narrative` | NEGATIVE CONTROL prospect arm prospect_internal_no_row_OWNED_INPUT: the built tree with interactive_access.py, prospect.py and enforce.py put back to the LIVE bytes | identical | yes | control: recorded=['ModuleNotFoundError'] escaped=None code=UNEXPECTED compute_reached=False / live: recorded=['ModuleNotFoundError'] escaped=None code=UNEXPECTED compute_reached=False |
| `irpt-narrative` | prospect arm prospect_firm_user_CREATE_INPUT: built does not raise TypeError | expected-diff | no | live: recorded=['TypeError'] escaped=None code=UNEXPECTED compute_reached=False / built: recorded=[] escaped=None code=None compute_reached=True |
| `irpt-narrative` | NEGATIVE CONTROL prospect arm prospect_firm_user_CREATE_INPUT: the built tree with interactive_access.py, prospect.py and enforce.py put back to the LIVE bytes | expected-diff | yes | control: recorded=['TypeError'] escaped=None code=UNEXPECTED compute_reached=False / live: recorded=['TypeError'] escaped=None code=UNEXPECTED compute_reached=False |
| `irpt-narrative` | prospect arm prospect_firm_user_OWNED_INPUT: built does not raise TypeError | expected-diff | no | live: recorded=['TypeError'] escaped=None code=UNEXPECTED compute_reached=False / built: recorded=[] escaped=None code=None compute_reached=True |
| `irpt-narrative` | NEGATIVE CONTROL prospect arm prospect_firm_user_OWNED_INPUT: the built tree with interactive_access.py, prospect.py and enforce.py put back to the LIVE bytes | expected-diff | yes | control: recorded=['TypeError'] escaped=None code=UNEXPECTED compute_reached=False / live: recorded=['TypeError'] escaped=None code=UNEXPECTED compute_reached=False |
| `irpt-narrative` | enforcer build with the load_report_owner port: built constructs the Enforcer | expected-diff | no | live: escaped=TypeError built_enforcer=False / built: escaped=None built_enforcer=True |
| `irpt-narrative` | NEGATIVE CONTROL enforcer build: the built tree with enforce.py put back to the LIVE bytes | expected-diff | yes | control: escaped=TypeError / live: escaped=TypeError |
| `irpt-narrative` | no_row_internal_enforcer_scope (+ row-listed): class, roster and permitted set, live vs built | identical | no | no_row_no_selection live=UNKNOWN/None/0 built=UNKNOWN/None/0; no_row_selecting_other live=UNKNOWN/None/0 built=UNKNOWN/None/0; row_listed_no_selection live=OPAL_GLOBAL/['ops@opalinvest.com']/2 built=OPAL_GLOBAL/['ops@opalinvest.com']/2 |
| `irpt-narrative` | binding cases (userOwn, userSelOther, userClaimOther, noRow, rowCotCot, rowCotInf) through the real entry.ENTRY, live vs built | identical | no | 6 cases over 1 route(s); differing: none; HARNESS_* on built: none, on live: none |
| `irpt-narrative` | method-call arm narrative-packet: built handler raises no call-arity TypeError | expected-diff | no | built arity errors=0 escaped=none codes={'firm_user_own': 'FIRM_BINDING', 'internal_row_listed': 'FIRM_BINDING'} functions_entered(firm_user_own/internal_row_listed)=58/61 / live arity errors=6 codes={'firm_user_own': 'UNEXPECTED', 'internal_row_listed': 'UNEXPECTED'} |
| `irpt-narrative` | NEGATIVE CONTROL method-call arm narrative-packet: the LIVE zip reads arity errors | expected-diff | yes | live arity errors=6 at ['entry:177', 'served:1255', 'served:856'] |
| `irpt-status` | prospect arm prospect_internal_no_row_CREATE_INPUT: built does not raise TypeError | expected-diff | no | live: recorded=['TypeError'] escaped=None code=UNEXPECTED compute_reached=False / built: recorded=[] escaped=None code=None compute_reached=True |
| `irpt-status` | NEGATIVE CONTROL prospect arm prospect_internal_no_row_CREATE_INPUT: the built tree with interactive_access.py, prospect.py and enforce.py put back to the LIVE bytes | expected-diff | yes | control: recorded=['TypeError'] escaped=None code=UNEXPECTED compute_reached=False / live: recorded=['TypeError'] escaped=None code=UNEXPECTED compute_reached=False |
| `irpt-status` | prospect arm prospect_internal_no_row_OWNED_INPUT: built does not raise TypeError | identical | no | live: recorded=['ProspectOwnershipRefused'] escaped=None code=NOT_AUTHORIZED compute_reached=False / built: recorded=['ProspectOwnershipRefused'] escaped=None code=NOT_AUTHORIZED compute_reached=False |
| `irpt-status` | NEGATIVE CONTROL prospect arm prospect_internal_no_row_OWNED_INPUT: the built tree with interactive_access.py, prospect.py and enforce.py put back to the LIVE bytes | identical | yes | control: recorded=['ProspectOwnershipRefused'] escaped=None code=NOT_AUTHORIZED compute_reached=False / live: recorded=['ProspectOwnershipRefused'] escaped=None code=NOT_AUTHORIZED compute_reached=False |
| `irpt-status` | prospect arm prospect_firm_user_CREATE_INPUT: built does not raise TypeError | identical | no | live: recorded=[] escaped=None code=None compute_reached=True / built: recorded=[] escaped=None code=None compute_reached=True |
| `irpt-status` | NEGATIVE CONTROL prospect arm prospect_firm_user_CREATE_INPUT: the built tree with interactive_access.py, prospect.py and enforce.py put back to the LIVE bytes | identical | yes | control: recorded=[] escaped=None code=None compute_reached=True / live: recorded=[] escaped=None code=None compute_reached=True |
| `irpt-status` | prospect arm prospect_firm_user_OWNED_INPUT: built does not raise TypeError | identical | no | live: recorded=[] escaped=None code=None compute_reached=True / built: recorded=[] escaped=None code=None compute_reached=True |
| `irpt-status` | NEGATIVE CONTROL prospect arm prospect_firm_user_OWNED_INPUT: the built tree with interactive_access.py, prospect.py and enforce.py put back to the LIVE bytes | identical | yes | control: recorded=[] escaped=None code=None compute_reached=True / live: recorded=[] escaped=None code=None compute_reached=True |
| `irpt-status` | enforcer build with the load_report_owner port: built constructs the Enforcer | identical | no | live: escaped=None built_enforcer=True / built: escaped=None built_enforcer=True |
| `irpt-status` | NEGATIVE CONTROL enforcer build: the built tree with enforce.py put back to the LIVE bytes | identical | yes | control: escaped=None / live: escaped=None |
| `irpt-status` | no_row_internal_enforcer_scope (+ row-listed): class, roster and permitted set, live vs built | identical | no | no_row_no_selection live=OPAL_GLOBAL/['ops@opalinvest.com']/2 built=OPAL_GLOBAL/['ops@opalinvest.com']/2; no_row_selecting_other live=OPAL_GLOBAL/['ops@opalinvest.com']/2 built=OPAL_GLOBAL/['ops@opalinvest.com']/2; row_listed_no_selection live=OPAL_GLOBAL/['ops@opalinvest.com']/2 built=OPAL_GLOBAL/['ops@opalinvest.com']/2 |
| `irpt-status` | binding cases (userOwn, userSelOther, userClaimOther, noRow, rowCotCot, rowCotInf) through the real entry.ENTRY, live vs built | identical | no | 42 cases over 7 route(s); differing: none; HARNESS_* on built: none, on live: none |
| `irpt-status` | method-call arm analysis-request-history: built handler raises no call-arity TypeError | identical | no | built arity errors=0 escaped=none codes={'firm_user_own': 'NOT_AUTHORIZED', 'internal_row_listed': None} functions_entered(firm_user_own/internal_row_listed)=47/55 / live arity errors=0 codes={'firm_user_own': 'NOT_AUTHORIZED', 'internal_row_listed': None} |
| `irpt-status` | method-call arm analysis-request-read: built handler raises no call-arity TypeError | identical | no | built arity errors=0 escaped=none codes={'firm_user_own': 'NOT_AUTHORIZED', 'internal_row_listed': 'NOT_AUTHORIZED'} functions_entered(firm_user_own/internal_row_listed)=47/59 / live arity errors=0 codes={'firm_user_own': 'NOT_AUTHORIZED', 'internal_row_listed': 'NOT_AUTHORIZED'} |
| `irpt-status` | method-call arm analysis-request-original: built handler raises no call-arity TypeError | identical | no | built arity errors=0 escaped=none codes={'firm_user_own': 'NOT_AUTHORIZED', 'internal_row_listed': 'NOT_AUTHORIZED'} functions_entered(firm_user_own/internal_row_listed)=47/59 / live arity errors=0 codes={'firm_user_own': 'NOT_AUTHORIZED', 'internal_row_listed': 'NOT_AUTHORIZED'} |
| `irpt-status` | method-call arm analysis-request-pdf: built handler raises no call-arity TypeError | identical | no | built arity errors=0 escaped=none codes={'firm_user_own': 'NOT_AUTHORIZED', 'internal_row_listed': 'NOT_AUTHORIZED'} functions_entered(firm_user_own/internal_row_listed)=47/59 / live arity errors=0 codes={'firm_user_own': 'NOT_AUTHORIZED', 'internal_row_listed': 'NOT_AUTHORIZED'} |
| `irpt-status` | method-call arm analysis-report: built handler raises no call-arity TypeError | identical | no | built arity errors=0 escaped=none codes={'firm_user_own': 'NOT_AUTHORIZED', 'internal_row_listed': 'NOT_AUTHORIZED'} functions_entered(firm_user_own/internal_row_listed)=47/67 / live arity errors=0 codes={'firm_user_own': 'NOT_AUTHORIZED', 'internal_row_listed': 'NOT_AUTHORIZED'} |
| `irpt-status` | method-call arm status-summary: built handler raises no call-arity TypeError | identical | no | built arity errors=0 escaped=none codes={'firm_user_own': 'UNEXPECTED', 'internal_row_listed': 'UNEXPECTED'} functions_entered(firm_user_own/internal_row_listed)=38/39 / live arity errors=0 codes={'firm_user_own': 'UNEXPECTED', 'internal_row_listed': 'UNEXPECTED'} |
| `irpt-status` | method-call arm status-job: built handler raises no call-arity TypeError | identical | no | built arity errors=0 escaped=none codes={'firm_user_own': 'NOT_AUTHORIZED', 'internal_row_listed': 'NOT_AUTHORIZED'} functions_entered(firm_user_own/internal_row_listed)=47/59 / live arity errors=0 codes={'firm_user_own': 'NOT_AUTHORIZED', 'internal_row_listed': 'NOT_AUTHORIZED'} |

Reading the arms: the **no-row-internal** arm (`no_row_internal_enforcer_scope`) is identical live vs built on all three hosts (the narrative classes UNKNOWN as on its live 409 build; the adapter and status class OPAL_GLOBAL on both sides, unchanged by this cell). The **prospect** arms show the live TypeError where the call site has the split and none on built; the narrative's internal-caller prospect arms read ModuleNotFoundError on BOTH sides because that zip packages no `interactive_access.py` (row `IRPT_BCKEND-D2-W278-S4`, INERT: the host declares no prospect or owner-read mode). The **enforcer build** arm shows the adapter's and the narrative's live TypeError on `load_report_owner` and the built Enforcer constructed. The **method-call** arms show 0 call-arity errors on every built route; the live narrative and adapter read arity errors there (the negative control), and the live irpt-status (rev 3) reads 0, as it carries no split of that class.

**Limits of the method-call arm, stated:** the stores are in-memory fakes that answer empty or not-found, so the call goes as deep as an empty store lets it (`functions_entered` in each detail cell counts the distinct functions of the zip entered); the narrative and adapter built routes stop at `FIRM_BINDING` for the synthetic principals before compute, so their Enforcer build is covered by the `enforcer build` arm and the static limb, not by the route call. The static method-call limb (0 mismatches on every built zip, 2 on the rev-5 pairing control) is what catches the `.reference(...)` class without seeded data. ABSENT != EXERCISED-AGAINST: this packet does not claim the retained-record paths ran on real rows.

## The live-call arm (IRPT_ANLREQ release 1 half AMENDMENT 5, CTO msg 3732)

Carried beside the zip census, unchanged in meaning: *a LIVE-CALL arm sits before the ledger closes: ONE real GET answering 200 on a non-49F request within a minute of the promote; a 500 means immediate Branch B.* It is standard in the CTO seat's halves for every served Lambda release. Per function, rerun at apply (UNEXERCISED until then; ABSENT != EXERCISED-AGAINST):
- `irpt-performance-adapter`: one GET `/api/scoped/investor-reporting/performance/{accountSetId}` as a caller outside the 49F case; expect a typed answer, never 500 and never `TypeError` in the group. Branch B is the hold above (there is no previous version to promote), so a 500 means STOP and escalate, not a re-promote.
- `irpt-narrative`: one GET `/api/scoped/investor-reporting/narrative/{reportId}` as a firm user; expect 200 or a typed refusal, one `irpt_error` line at most and no `TypeError`; a 500 means immediate Branch B.
- `irpt-status`: one GET `/api/scoped/investor-reporting/status` for a non-49F caller within a minute of the promote; a 500 means immediate Branch B; PLUS the two after-reads named in its section (REQ-5e4149d2's owner read; one GET `/original`, count stays 1). Do not start until IRPT_ANLREQ release 1 has cleared.

## Rows

`IRPT_BCKEND-D2-W278-S1` (the one tree is 361c44fa9d; what rides is named; INERT), `-S2` (source map not edited, candidate map in deliverables; ARMED, 2.0.0_SA_COO~P2), `-S3` (live irpt-status is rev 3 and still carries the `profile_reader` split; the release-1 after-reads are deferred to this build; INERT), `-S4` (irpt-narrative packages no interactive_access.py; INERT), `-S5` (attribute limb also reads enforce.Request(path_ids=) on live narrative; the red list now reads 2 failed; INERT), `-S6` (the method-call arm is an instrument this order did not specify beyond one sentence; its limits; INERT).

Files beside this packet: `IB117-1_signature_census.json`, `IB117-1_replay.json`, `IB117-1_red_list.json`, `IB117-1_adapter_refusals.json`, `candidate_source_map.json`, `signature_closure_attr.py`, `method_call_limb_416.py`, `pin_coherence_candidate_416.py`, and the writers (`make_candidate_map.py`, `make_census_416.py`, `make_packet_416.py`, `cw_refused_count_416.py`, `replay/`).
