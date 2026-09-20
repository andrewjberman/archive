# IB-rtg-4 result: the holdings loader follows the directory pointer -- SECOND PASS, APPLIED and PROVEN LIVE

**Order:** `IRPT_BCKEND.TO-IB-rtg-4` **Seat:** `0.9.0_WK_IRPT_BCKEND~4` **Row:** `S100` **Outcome:** `FWD-5`

**Graded run:** `IB-rtg-4_R75-AC1_battery_output.txt` (`battery_ib_rtg_4.py` @HEAD this commit) + `IB-rtg-4_R75-AC1_arm_e_live_proof.txt` (`battery_ib_rtg_4_arm_e.py` @HEAD this commit).

## R75-AC1: PASS, by output -- both never-widen halves at HEAD, packet-keyed, the fresh 10-root
subtraction gate PASSED, the holdings root applied, and a live exercise under the deployed role
and bytes reads SCOPE-RESOLVED, never FIRM_BINDING with firm_id absent.

| arm | result |
|---|---|
| (a) MEASURE | PASS -- unchanged from the first pass (pre-fix signature ABSENT, fix signature PRESENT, `_authz/loaders.py:71-78` pattern confirmed, `directory/handler.py` confined-bound confirmed UNEDITED, live ownership map re-derived THIS RUN: 180 advisor/relationship keys, 23666 total account grant slots; MUTANT confirmed live: the pointer document declares `firm_id_opaque=None`) |
| (b) BUILD + VERIFY AT REST | PASS -- rebuilt this pass (`build-and-upload.sh investor-reporting irpt-holdings`); `CodeSha256`/`artifact_sha256` `rAAn3bt7MZXpxFgric7LlrNW9uv0xXgpiZmb+MOf/y0=` unchanged from the first pass's build (byte-identical content, a new S3 object VERSION only); VERIFIED AT REST (`match=True`), 15 of 15 declared members, packaged `entry.py` byte-equal to the worktree fix |
| (c) PACKET + HALVES GATE + FRESH 10-ROOT PLAN | PASS -- both never-widen halves are PRESENT at HEAD, each naming packet blob `b515836bb4db340dd1a4a6fb630ab70627432f3a` (COO half re-signed packet-keyed; CTO half re-signed 2026-09-20 ~17:5xZ, withdrawing its tag-keyed third class); a FRESH 10-root `init`+`plan` (never a saved plan) succeeded on every root this pass |
| ARM (d) SUBTRACTION GATE | **PASS.** `IB-rtg-4_subtraction_gate.py` (`terraform show -json` per root, `resource_changes` WHOLE minus {top-level `.timestamp`; S3 data-source `version_id`/`last_modified`}). **DENOMINATOR: 132 resource_changes entries compared across 10 roots; 10 paths subtracted** (the top-level `.timestamp` x10; 0 hits for the S3 data-source category this round -- no `aws_s3_object` data-source entries appeared in any root's `resource_changes` this plan set, confirmed by direct scan, `IB-rtg-4_subtraction_gate_output.txt`). Per-root substantive result after subtraction: **holdings** EXACTLY `module.irpt_holdings.aws_lambda_function.this` `["update"]`, `source_code_hash` `uS+WBeNxiCkYU2pdGalaONZ74SvoWEiYx669KWYKQDA=` -> `rAAn3bt7MZXpxFgric7LlrNW9uv0xXgpiZmb+MOf/y0=` (+`s3_object_version`; `handler` UNCHANGED, already `entry.lambda_handler` on both sides -- W2-S38's flip had already landed on a prior pass), nothing else; **the 6 non-round-7 roots** (api, core, directory, intake, narrative, ycharts) EACH EMPTY (0 substantive changes); **the 3 sibling round-7 roots** each show EXACTLY their own packet-declared build and nothing else -- export `module.irpt_export_render.aws_lambda_function.this` update (`source_code_hash` -> `cn8YKEP2oQdfvAjdpa32Wfp9oJqhAIMGkECv+H4vUg4=`, == IB-rtg-1's packet built sha, EXACT) PLUS `aws_iam_role_policy.export_render_receipt` `["create"]` (== IB-rtg-1's own K-IAM); ops `module.irpt_status.aws_lambda_function.this` update (`source_code_hash` -> `B0AmyfRKxd4uMhcfoklf3cCpPtnDQUBpLsUBADeDcQ0=`, == IB-rtg-2's packet built sha, EXACT); performance `module.irpt_performance_adapter.aws_lambda_function.this` update (`source_code_hash` -> `W4rYXgZz/LmZ1zO9I6eiKWc7PgSH+eKAUYXzttCmRTA=`, == IB-rtg-3's packet built sha, EXACT). No root shows an attribute outside the allow-list `{source_code_hash, s3_object_version, handler, last_modified, policy, id, name, tags, tags_all}`, no fourth root moves, no sibling shows a sha outside its own packet. **GATE PASS.** |
| ARM (d) APPLY | **PASS.** Change-management ledger `irpt-bckend-ib-rtg-4-apply` OPENED before the apply (commit `1e59319d1a`), CLOSED after verification (commit `8a30151cca`). `HALT_ACK=1 .tools/safe-apply.sh -chdir=infra/aws/terraform/investor-reporting/holdings apply -input=false -no-color <planfile>` -- rc=0, `IB-rtg-4_apply_output.txt`: `Apply complete! Resources: 0 added, 1 changed, 0 destroyed.` Post-apply: `get-function-configuration --query CodeSha256` -> `rAAn3bt7MZXpxFgric7LlrNW9uv0xXgpiZmb+MOf/y0=` (== built); post-apply re-plan (`IB-rtg-4_post_apply_replan.txt`) -> `No changes. Your infrastructure matches the configuration.` (0-diff). |
| (e) LIVE PROOF | **PASS.** Reused `../0.7.0_AE_CloudOps~V/battery_ib_rtf_10.py`'s bounded-principal mechanism (rtf-9 packet blob `a1f36b95b26c8fefd6ff0d47489f9884f87dd2c4`, both halves at HEAD) via `battery_ib_rtg_4_arm_e.py`, under THIS order's own live-principal ledger `irpt-bckend-ib-rtg-4-live-principal` (opened `af62387cd6`, closed below), a FRESH epoch (`USER#usr_irptrte_1789930331`). Full lifecycle: K1 + K1b created and read back (digests printed); login HTTP 200, claims `firmId=49financial advisorKey=abby_horton`; directory search (7 entries) + resolve (`ok=True, account_count=1`) yielded a granted account `acc_a5210ef53d8323b9d106b8b1`; **`GET /api/scoped/investor-reporting/holdings/acc_a5210ef53d8323b9d106b8b1` -> FUNCTION `irpt-holdings` (EXECUTION ROLE `irpt-holdings-role`): HTTP 200, class `POLICY`, `code=NOT_AUTHORIZED`, `firm_id` PRESENT -- a real policy refusal WITH `firm_id`, NEVER `FIRM_BINDING` with `firm_id` absent.** This is S100's fix served live: the binding step now resolves the real `firm_id_opaque` and the request reaches a scope-decided outcome (an authorization-policy refusal that KNOWS the firm) rather than failing at the binding step itself. K1b then K1 deleted and verified (consistent read-back absent); refresh with the issued refresh token REFUSED (HTTP 404, no token minted); the access token after its `exp` (19:07:20Z) REFUSED 401. No residue on the before/after prefix scans. Ledger `irpt-bckend-ib-rtg-4-live-principal` CLOSED, all 6 legs proven. |

The battery prints `IBR75-HOLDINGS-FOLLOWS-POINTER-AND-SERVES` (see `IB-rtg-4_R75-AC1_battery_output.txt`, arms a-c) and the live-proof battery prints `IBR75-HOLDINGS-LIVE-PROOF-SCOPE-RESOLVED` (`IB-rtg-4_R75-AC1_arm_e_live_proof.txt`), rc=0 on both this pass.

## R75-AC2: JUDGMENT, recorded for `3.0.0_SA_CVO`, not self-graded

Unchanged from the first pass: whether the source fix's shape (following `_authz/loaders.py:71-78`'s
two-step pattern by composing `directory/handler.py`'s existing single-key `load_directory` twice,
rather than importing `_authz.loaders.load_directory` directly) is the correct choice for this cell's
confined bound. The measured facts, now including the live-proof result: the fix is deployed, served,
and a real granted-account request no longer refuses at the binding step.

## Cause and fix, confirmed against source at HEAD

Unchanged from the first pass (see the first-pass account below); the fix is now DEPLOYED and PROVEN
LIVE. `holdings/entry.py:88-89` `_load_directory(tenant)` called `directory/handler.py`'s single-key
`load_directory(bucket, key)` with `key = DIRECTORY_KEY` -- the POINTER's own key -- and returned the
pointer document verbatim, which carries no `firm_id_opaque`; `opaque_firm_for(tenant)` then returned
`None` and `FirmBinding.proves()` refused `FIRM_BINDING` for every request on this route regardless of
entitlement. The fix mirrors `_authz/loaders.py:71-78`'s two-step (fetch `latest.json`, then fetch
`pointer["key"]`): `_load_directory` now fetches the pointer document FRESH every call, then fetches
`pointer["key"]` through `directory/handler.py`'s existing `load_directory`. `directory/handler.py`
itself remains UNEDITED, per this order's confined bound.

## Rows filed this pass

`IRPT_BCKEND-W4-S47` (BLOCKING, ARMED, disarm_owner `0.0.0_AB_MSTR`): mid-pass, the box's C: drive
measured at 0 bytes free, blocking `terraform init` on every root lacking a prior complete
`.terraform/` in this worktree (including holdings itself). No apply was attempted at that point; the
change-management ledger opened before the discovery was left OPEN (a `hold` was correctly refused by
`deploy_ledger.py` since the leg was unstarted, not paused mid-apply). **The condition resolved DURING
this same pass** (free space rose from 0 to ~3.25 GB between the row's measurement and the next
`terraform init` attempt, cause not established by this worker), and the fresh 10-root plan then
succeeded -- see the arm (c)/(d) rows above. The row is left as filed (never edited); its own disarm
condition ("nonzero free space and a clean init") is now independently observable at HEAD.

Rows carried from the first pass, unchanged: `IRPT_BCKEND-W4-S45` (the build-and-upload.sh cwd trap,
disarm_owner `2.0.0_SA_COO~B`) and `IRPT_BCKEND-W4-S46` (pre-existing export/performance drift, later
resolved by the CTO/COO's re-signed packet-keyed construction identifying it as the sibling round-7
builds, not drift).

## What this pass did

Both never-widen halves verified at HEAD naming the exact packet blob; a fresh 10-root Terraform plan;
the arm-(d) subtraction gate (denominator printed above); the holdings root applied under an
open-before/close-after change-management ledger; post-apply verification (served `CodeSha256`,
0-diff replan); and arm (e)'s live proof under the deployed role and bytes, full lifecycle, under its
own change-management ledger. The task order's `<status>` is flipped to `complete` in this same commit
set, since R75-AC1 now PASSES by output and the proof-of-spec instance validates.
