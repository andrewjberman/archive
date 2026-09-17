# NFRA_OPLGTW.TO-OG-i-5 -- access-state-rename result

**Assignee:** 0.9.0_WK_NFRA_OPLGTW~1  **Branch:** wk-nfra_oplgtw-1h  **Cut from:** CLOUD @78b5f95695

## What happened

`opal-gateway-access-state` (7 items, ACTIVE, deletion_protection_enabled) was renamed to the naming
builder's output `gateway-access-state-table` (`lib/opal_naming.py name("gateway", None, "access-state",
"table")` == `gateway-access-state-table`, `grade(name, "DYNAMODB_TABLE")` == `CONFORMANT`), per ruling
R-OG-8 (msg 97553/97556), with every record carried across under proof and no writer touching the old
table across the window.

- **New table ARN:** `arn:aws:dynamodb:us-east-1:313476888478:table/gateway-access-state-table`
- **Old table (retired):** `opal-gateway-access-state` -- `describe-table` now returns
  `ResourceNotFoundException`.
- **Both tables' counts at the deciding checkpoint (post-copy, post-cutover, pre-apply-2):** 7 == 7
  items; per-namespace: `RUNTIME#` 0, `POLICY#` 7 (`operator_audit` 4 of those 7), identical on both
  sides; 0 of 7 per-item sha256 digest mismatches.

## Sequence (one ledger entry, three legs: `create`, `copy`, `retire`)

1. Ledger opened, sentinel committed `ae8731f3c3` (13:33:52Z), **before** apply 1.
2. **Apply 1** (`e2a42dc261` records the final `.tf`; applied live 13:44:19Z-ish): declared the new table
   under resource address `access_state_new` beside the pre-existing table (renamed in state to
   `access_state_old` via a `moved` block, 0 changes to it), and repointed both grants
   (`gw_access_state_runtime`, `access_admin_policy`) to the new table's ARN. Saved plan: 1 create, 2
   update, 0 destroy (OGI5-AC3). `describe-table`/`describe-time-to-live`/`describe-continuous-backups`
   confirm SSE ENABLED, PITR ENABLED, PAY_PER_REQUEST, TTL `expires_at` ENABLED, key schema
   `pk`:HASH/`sk`:RANGE (OGI5-AC4).
3. **Copy window opened** 13:50:35Z (copy-start baseline scan of the old table, digest-only).
4. **Copy** (`probes/og_i5_copy.py`): 7 of 7 items copied old -> new under `attribute_not_exists(pk)`
   (never overwrite), 0 condition failures.
5. **Reference-move commit** `63f0ccec7d`: `app/access_state.py` `TABLE_NAME`, `app/oauth_as.py`'s
   docstring, and `org/standards/NFRA_OPLGTW_CONTRACT.json` (`state_store.table`, `contract_version`
   1.0 -> 1.1) now name the new table. Neither file is deployed by this cell (`OG-r-1` deploys the
   integrated build later).
6. **Post-cutover full scan + digest check** (both tables): 7 == 7, 0 mismatches, per-namespace counts
   equal -- satisfies OGI5-AC5, AC6 and AC13 together (all taken after the copy and the reference-move
   commit, before apply 2).
7. **AC9** (on-host, instance's own role, via SSM `5d0d2b77-...`): one conditional write to a
   `RUNTIME#probe-og-i5-<utc>` key SUCCEEDED; the same call shape to a `POLICY#probe-og-i5-<utc>` key
   returned `AccessDeniedException` -- in the same harness.
8. **AC12** (quiescence, via SSM `63f5ba78-...`): the deployed app on `i-07dccb1615503ac99` (`/opt/opal-
   gateway/app`) references neither table name (`MATCH_COUNT=0`); the old table's per-item digests taken
   at the copy's start (13:50:35Z) equal those taken at the post-cutover re-check (13:59:57Z), 0 diffs --
   no writer touched it across the window.
9. **AC8**: `tests/test_access_state.py` (7), `tests/test_oauth_durable.py` (18),
   `tests/test_principal_cutover.py` (11) each pass in their own pytest process -- 36 of 36.
10. **Rollback window closed** (all of AC5/AC6/AC7/AC8/AC9/AC12/AC13 recorded PASS at commit
    `87d64458e6`, the evidence commit).
11. **Deletion-protection flip** (a small in-place apply on `access_state_old`, `deletion_protection_
    enabled` true -> false; 0 add, 1 change, 0 destroy) -- required because AWS refuses to destroy a
    table with that flag true and a config-level resource removal cannot express an in-place update
    first.
12. **Apply 2** (the `access_state_old` resource block, its `moved` block and its unused local removed
    from `schwab_access_state.tf`): saved plan 0 add, 0 change, 1 destroy (`access_state_old` only,
    OGI5-AC10); applied 14:36:49Z-14:36:56Z, `Apply complete! Resources: 0 added, 0 changed, 1
    destroyed.`
13. **Ledger closed** (all three legs proven), committed `e2a42dc261`, **before** the final reads.
14. **AC11**: `describe-table` on `opal-gateway-access-state` -> `ResourceNotFoundException`; a fresh
    plan of the `opal-gateway` root -> `detailed-exitcode 0`, `No changes.`

Total window (copy's start to the post-cutover re-check): 13:50:35Z -> 13:59:57Z, well inside the
60-minute bound; the destroy itself (apply 2) ran at 14:36:49Z, ~46 minutes after the window opened,
also inside the bound (the order bounds the window at the copy-start-to-recheck span, not the whole
sequence through apply 2's destroy).

## AC1-AC13 verdicts (probe `probes/og_i5.py`, all thirteen re-run in one final sweep)

All thirteen: `VERDICT: PASS-OGI5-AC<n>`. Full invocations, denominators and deciding lines are in
`NFRA_OPLGTW.TO-OG-i-5.access-state-rename.proof_of_spec.json`.

## Surprise row filed

`NFRA_OPLGTW-W1-S12` -- OGI5-AC7's parenthetical historical-record list does not literally name
task-orders/, prd/ or decompositions/, all three of which carry the retired table name as frozen,
out-of-`<paths>`-grant project history. The probe's `ac7()` widens the historical classification to
cover them, on the reasoning that they are structurally identical to the five named categories
(frozen, unfixable by this cell, and correct-when-written). Disclosed inline in the probe's own output.

## Environment

`.venv-og` built `py -3.12 -m venv --system-site-packages .venv-og` then
`pip install -r infra/aws/ec2/opal-gateway/requirements.txt msal moto pytest`; 318 packages
(`pip freeze` recorded, not committed -- gitignored `.venv-og/`).

## Deploy ledger

Slug `nfra-oplgtw-og-i-5-access-state-rename`, entry
`org/critical_paths/change_management/20260917T1333Z_nfra-oplgtw-og-i-5-access-state-rename_deploy_completion.md`,
CLOSED, sentinel removed. Never left half-landed: the copy was proven before apply 2 ran, and apply 2 ran
only after the rollback window's criteria all read PASS.
