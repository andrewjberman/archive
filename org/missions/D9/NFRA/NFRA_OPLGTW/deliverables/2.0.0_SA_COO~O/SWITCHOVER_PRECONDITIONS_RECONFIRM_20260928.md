# Switchover sitting: the four preconditions re-confirmed after the reboot

By: `2.0.0_SA_COO~O`, 2026-09-28 ~20:1xZ (first post-reboot session).
Asked by: `1.0.0_SA_CTO~O` in message 20260928T180506Z (Andrew-direct call 2, "A is fine", record @d4d8c33fe2).
Runbook: `org/missions/D6/NFRA/NFRA_OPALAI/deliverables/1.0.0_SA_CTO~O/ANDREW_SWITCHOVER_RUNBOOK.md`.

**Verdict: ALL FOUR MET.** Every item below was measured this session. None is copied from the runbook's 2026-09-26 status.

| # | Precondition | Measured | Result |
|---|---|---|---|
| (a) | Round-1 code merged into `opal_ai` DEV and PROD | `git ls-remote https://github.com/Opal-Capital/opal_ai.git`: DEV `fd8ab8a57f`, PROD `fd8ab8a57f` | MET, unchanged since 09-25 |
| (b) | `runtime.config.json` written outside every repo | `C:\opal_runtime\runtime.config.json`, 204 B, mtime 09-25; keys `checkout_dir`, `state_dir`, `workspace_probe_file`, `prod_ref`=`PROD` | MET |
| (c) | NFRA_MCPORTAL gateway release live | **CORRECTED 2026-09-28 ~21:0xZ: the served release is `6a98a0553a`, not `fe94911257`.** The five files below are identical in both commits, so they cannot tell the two apart. The discriminator is the `.env` the deploy template writes: `6a98a0553a`'s template (the only diff to `deploy-to-ec2.sh`) adds `SPRINT_VIEW_ALLOWED_EMAILS`, and the live `.env` carries that key (SSM `3f1bce17-6694-4ecf-8d52-92a2b14c9856`, count 1, written 2026-09-27 22:17:26Z). `fe94911257`, `1f7128201a`, `df724ef284` and `c5f8099440` are all ancestors of `6a98a0553a`. ORIGINAL TEXT, superseded: SSM `ae9fe242-a208-4781-99ae-f50623737d54` on `i-07dccb1615503ac99`, status Success: 5 of 5 files in `/opt/opal-gateway` (`app/identity_scope.py`, `app/data_entitlement.py`, `app/admin_grants.py`, `app/asker_scope.py`, `identity_tool_allowlist.txt`) match `fe94911257` by md5. `1f7128201a` (MCPORTAL), `df724ef284` (OA-g-2) and `c5f8099440` (OA-f-2) are all ancestors of `fe94911257`. Service `active` since 2026-09-27 22:17:27Z; `/health` `{"ok":true}` | MET |
| (d) | Upload restricted to the operator's client (row Z-S19) | Live `identity_tool_allowlist.txt:19`: `opalbloomberg@opalinvest.com opal_data_refresh_upload client=mcp-iLcAi35L7ueDQvPN7Ikp9w`. One client is bound. | MET. The runtime-side refusal is still confirmed after step 5 by counting refresh families, per the runbook. |

## What changed since the runbook's status

1. **The served gateway release is newer.** (CORRECTED: it is `6a98a0553a`, OG-s-1's sprint-owner release; see (c).) Original, superseded: It is `fe94911257`, NFRA_OPLGTW OG-e-2's narrow email-deny release from
   2026-09-27, and no longer `df724ef284`. It contains every release the runbook depends on (see (c)). Only
   `app/data_entitlement.py` differs from `df724ef284`.
2. **`C:\opal_runtime\opal_ai` already exists as an EMPTY directory** (created 2026-09-28 11:23 local). Step 0's
   `git clone ... C:\opal_runtime\opal_ai` still works, because git clones into an empty directory. If the directory
   is not empty when Andrew sits down, remove it first.
3. **Not a precondition, but carried:** row NFRA_OPALAI-Z-S20 says `opal_ai` CI is red on DEV=PROD `fd8ab8a57f`
   (ruff, missing pytest). The launcher fast-forwards to PROD whatever its CI state, so this does not block the
   sitting. It is still an open FWD-13 gap for NFRA_OPALAI.

Not re-measured: whether Alyssa Keith's portal-only grant (Part C, step 6) is still ACTIVE. That is a Part C input, not
one of the four preconditions. Check it before step 6.
