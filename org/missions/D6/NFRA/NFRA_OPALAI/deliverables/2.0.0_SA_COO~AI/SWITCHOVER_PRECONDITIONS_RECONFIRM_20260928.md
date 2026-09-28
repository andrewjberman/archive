# Switchover sitting, Parts A-C: preconditions re-confirmed by the project's issuer

By: `2.0.0_SA_COO~AI` (NFRA_OPALAI issuer since placement @094c84f299), 2026-09-28 20:16-20:25Z, site Z.
On: round-1 analysis `ledger/ROUND_ANALYSIS.round1.md` @a8baa4b23d, R-3 (the re-confirm passes from `~O` to `~AI` for
Parts A-C; Part D is `2.0.0_SA_COO~MP`'s).
Runbook: `deliverables/1.0.0_SA_CTO~O/ANDREW_SWITCHOVER_RUNBOOK.md` (as of @2c3e657865).
Prior read: `2.0.0_SA_COO~O` @c0030ea9db (~20:1xZ). Every row below was measured again here. Nothing is copied from that read.
All reads were read-only. Nothing was provisioned, pushed or written to AWS or the gateway.

**Verdict: the four preconditions are MET, and Part C's grant is ACTIVE. One correction to the runbook: step 0 is
ALREADY DONE. `C:\opal_runtime\opal_ai` is a full clone at PROD `fd8ab8a57f`, not the EMPTY directory the ~20:1xZ
delta reports. Andrew starts at Part A step 1.**

| # | Precondition | Command | Evidence | Result |
|---|---|---|---|---|
| (a) | Round-1 code merged into `opal_ai` DEV and PROD | `git ls-remote https://github.com/Opal-Capital/opal_ai.git` | `fd8ab8a57f... refs/heads/DEV`, `fd8ab8a57f... refs/heads/PROD` (HEAD the same; 3 refs in all) | MET |
| (a.1) | Round-1 nested commits contained | `git -C C:/opal_runtime/opal_ai merge-base --is-ancestor <c> fd8ab8a57f` | `2e48f7b` (oa-1 nested HEAD) YES; `803f699` (oa-3 nested HEAD) YES. Control: `fd8ab8a57f` vs its own parent reads NO. This matches MSTR~Z's correction @74bce7565e | MET |
| (b) | `runtime.config.json` outside every repo | read the keys; `git -C C:/opal_runtime rev-parse --show-toplevel` | keys `checkout_dir, prod_ref, state_dir, workspace_probe_file`; 204 B; `fatal: not a git repository` | MET |
| (c) | NFRA_MCPORTAL gateway release live | **CORRECTED ~22:1xZ (row Z-S38): the served release is `6a98a0553a`, not `fe94911257`.** The 6 files below are identical in both (they differ only in `deploy-to-ec2.sh`), so they cannot tell the two apart; the live `.env`'s `SPRINT_VIEW_ALLOWED_EMAILS` key is written only by `6a98a0553a`'s template (`2.0.0_SA_COO~O` @e992df46c4). `6a98a0553a` descends from `fe94911257`, so every ancestry claim below still holds. Original, superseded: | SSM `36968c10-4a45-40a0-9f36-1aa4b413335d` on `i-07dccb1615503ac99` (md5sum, systemctl, on-box /health), compared with `git show fe94911257:<file> \| md5sum` | 6 of 6 files match `fe94911257` (`identity_scope.py`, `data_entitlement.py`, `admin_grants.py`, `asker_scope.py`, `server.py`, `identity_tool_allowlist.txt`). Negative control: `data_entitlement.py` at `df724ef284` = `f370003f...`, served = `96450434...`, so they differ. `1f7128201a`, `df724ef284` and `c5f8099440` are ancestors of `fe94911257`; the reverse reads NO. `ActiveState=active`, `ActiveEnterTimestamp=2026-09-27 22:17:27 UTC`, `NRestarts=0`, `/health {"ok":true}` | MET |
| (d) | Upload restricted to the operator's client (Z-S19, OA-f-2) | same SSM, `grep -n opal_data_refresh_upload identity_tool_allowlist.txt` | `19:opalbloomberg@opalinvest.com opal_data_refresh_upload client=mcp-iLcAi35L7ueDQvPN7Ikp9w`: one client bound | MET (the runtime-side refusal is still confirmed after step 5, per the runbook) |
| A.0 | Step 0: checkout cloned | `git -C C:/opal_runtime/opal_ai rev-parse HEAD`; `status -sb`; `ls` | HEAD `fd8ab8a57f`, `## PROD...origin/PROD`, 0 porcelain lines; 7 entries (`.git .github README.md clients docs opal template`); all three scripts present | DONE. Andrew skips step 0 |
| A.1 | Step 1: the dry run prints the eight acts | `provision-account.ps1 -Config C:\opal_runtime\runtime.config.json -Plan` | exactly the eight `PLAN:` lines of the G-ACCT handoff, exit 0 | MET |
| A.2-B | Account not yet provisioned | `Get-LocalUser Opal_Agent`; `Test-Path` on the state dir, the credential file and the profile | `User Opal_Agent was not found`; `C:\opal_runtime\state` False; `%USERPROFILE%\.opal_runtime\opal_agent_cred.xml` False; `C:\Users\Opal_Agent` False. No G-ACCT run report in `org/mcp/inbox/2.0.0_SA_COO/~O/` or its `read/` | NOT STARTED (expected; Part A step 2 onward is Andrew's elevated act) |
| C.6 | Alyssa Keith's portal-only grant ACTIVE | `bash deliverables/2.0.0_SA_COO~O/round1/checks/g3.AC1.sh` and `g3.AC2.sh` (read-only DynamoDB scan) | `items=192 policy=10 active_profiles=1 portal_only_active=1 operations=[['query']]`, RESULT: PASS for both, exit 0. The check counts and prints no identifier, so the one active portal-only profile is identified as Alyssa Keith's only by OA-g-3's drain @da3a2cafbe | MET |

## Where Andrew starts

Part A step 1 (the dry run, already clean here), then step 2 elevated. Part B follows the G-ACCT handoff
(`deliverables/2.0.0_SA_COO~O/HANDOFF_G-ACCT_ELEVATED_20260928.md`): steps 5-6 use `claude setup-token` and one
relayed MFA, per Andrew-direct 2026-09-28. That handoff's report line names `2.0.0_SA_COO~O`. The project's issuer
is now `2.0.0_SA_COO~AI`.

## Not a precondition, carried

`opal_ai` CI is red on `fd8ab8a57f` (row Z-S20, now round-2 E7). The launcher fast-forwards to PROD whatever the CI
state, so the sitting is not blocked.
