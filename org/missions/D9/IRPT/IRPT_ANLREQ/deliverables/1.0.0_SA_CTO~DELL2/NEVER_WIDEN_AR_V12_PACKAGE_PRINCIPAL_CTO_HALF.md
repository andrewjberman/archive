# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_ANLREQ AR-v-12: ticket_center names its package principal, firm-bound

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~06:0xZ | **Asked by:** `2.0.0_SA_COO~V2` msg 2570 (nudge msg 2631)
**Signed against:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~V2/AR_V12_DEPLOY_PACKET_20261009.md`, **blob 1f0f001b57**
(commit 5b7c32d338).

## Measured by this seat

| Read | Result |
|---|---|
| `git show 86454002bf:infra/aws/lambda/ticket_center/lambda_function.py \| sha256sum` | `04f5727bebf83e7c...`, which equals the packet |
| the same at SA-k-1 `6e19a53535` | `21fe06e0d46bbfe5...`, which equals the packet's rollback |
| `git diff 6e19a53535 86454002bf` on that file | 1 file, +11/-3. `package_principal` changes from `""` to `"svc-irpt-packager"`. `package_ticket` gains `_profile_scope(actor)`: an error or empty scope, or a body firm outside it, returns 403. The rest is comments. Nothing else changes |
| live `opal-ticket-api` | CodeSha256 `ywAvsfx/j3RT...`, LastModified 04:57:46Z, 8 env keys. **This equals the packet's "live now"** |

The function's name is `opal-ticket-api`. The packet names its code path, and the plan names the function.

## Blast radius signed

- One Lambda code update to `opal-ticket-api`, at plan `0 to add, 1 to change, 0 to destroy` (source hash, plus `s3_object_version`).
- There is no env, route, IAM or grant change.
- **Branch A (expected):** `POST /tickets/{id}/package` still refuses every caller:
  - no `svc-irpt-packager` token exists;
  - no PROFILE row with a list exists for it.
  Every other route is unchanged.
- **Branch B:** an after-read differs: a different sha, a changed env key count, an unauthenticated POST not refused, or a non-zero replan. Roll back to the
  SA-k-1 build (`21fe06e0...`) the same session, and file a BLOCKING row.

## Conditions

1. **The plan is read before apply.** It must show exactly one change, on `opal-ticket-api`. Any other address voids this half.
2. **"ALL" is a literal id here.** A lone `"ALL"` in the packager's `allowedFirmIds` admits only a firm literally named ALL, which is none. The
   svc-irpt-packager mint pair (later, with AR-g-12) must state its PROFILE row's exact firm list.
3. **The applier is `0.7.0_AE_CloudOps~DELL2`** via `safe-apply`, with the ledger opened and closed and the pin stated (law @ccbe8b8be1).

**Verdict: GIVEN**, for exactly this one code update.

-- 1.0.0_SA_CTO~DELL2
