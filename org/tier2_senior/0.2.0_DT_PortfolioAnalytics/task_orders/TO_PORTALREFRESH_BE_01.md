# TO_PORTALREFRESH_BE_01 — DataRefresh rollback backend: F1 ID-namespace seam join + server-side already-running guard + F3 emoji cleanup

**Project:** OPAL_PORTALREFRESH  **Issuer:** 1.0.0_SA_CTO  **Assignee:** 0.2.0_DT_PortfolioAnalytics
**Status:** ACTIVE  **Issued:** 2026-07-17T13:40Z  **Priority:** P1 — SEQUENCED BEHIND your P0 residual (Bloomberg .ST CIX fix + validated 07-17 re-upload). Do not preempt it.

## Why (grounded — MSTR investigation, brief 20260717T133342Z)

**F1 — ID-NAMESPACE SEAM (source-confirmed both ends, live-verified 07-17):** `handle_rollback`
reads `{archivePath}outputs-manifest.json` keyed by the API's `exec-{hex}` ID
(`infra/aws/lambda/data_refresh/lambda_function.py:1135` @ CLOUD HEAD), while the manifest writer
`yang-capture-output-versions` keys by the Step Functions UUID. Live today: manifest landed at
`archive/e14770af-b842-.../outputs-manifest.json` (23,577B, 12:59:31Z, non-null VersionIds for the
whole json/ tree) while rollback read `archive/exec-c14fb8176125/` (inputs only). Every rollback
invocation logged "No outputs manifest found - falling back to re-processing" — **100% fallback
rate; the version-based exact-restore path CANNOT fire.** Today's rollback = "re-process old
inputs with CURRENT generator code," not a state restore.

**F2 — SILENT MULTI-FIRE:** no server-side already-running guard. Andrew's ~6 clicks each re-fired
the whole pipeline (6 execs racing the same served keys). The FE lockout (DE's TO) is UX;
**the BE guard is the control** — defense-in-depth, both land.

**F3 —** deployed Lambda prints emoji glyphs (broke a charmap CloudWatch pull mid-investigation).
CLAUDE.md no-emoji law; cleanup in the same touch.

## Deliverables

1. **F1 seam join — ARCH RULING (mine, binding):** rollback resolves the SFN UUID from the
   execution record already in DynamoDB (the `executionArn` sitting on the upload/exec row) and
   reads the manifest at the UUID-keyed path. Rationale: reader-side fix is additive and
   backward-compatible with every EXISTING archive entry, whereas re-keying the writer orphans all
   history written to date and touches the SFN input contract. If you find the DDB row does NOT
   reliably carry the executionArn, surface that to me before improvising a third shape — do not
   dual-write keys silently. Fallback-to-reprocess stays as the explicit degraded path, but a
   successful version-restore must LOG which path served the rollback.
2. **Server-side already-running guard:** reject (409-class, explicit machine-readable status)
   any rollback request while one is RUNNING for the same pipeline. Reject, not queue — a queued
   rollback executes against state the operator never saw. The rejection payload is part of the
   FE contract cell (below).
3. **F3:** replace emoji/non-ASCII prints with `OK:`/`WARN:`/`ERROR:` in the same deploy.
4. **F4 — "Triggered By" identity (Andrew-direct 2026-07-17 ~13:5xZ, added by CTO amendment):**
   Upload History (uploads AND rollback events) must record the real logged-in user, not
   `dev@test.com`. **Mechanism MEASURED live from Andrew's 07-17 rollback events** (CloudWatch
   `/aws/lambda/opal-data-refresh-api` 12:55:31–44Z): the authorizer WORKS — every request
   carries `requestContext.authorizer.lambda.email = andrew@opalinvest.com` — but
   `validate_user_type` (`lambda_function.py:~100`) reads `authorizer_context.get('email')` at
   the WRONG DEPTH (API GW v2 nests Lambda-authorizer context under the `lambda` key), misses,
   and falls to the Method-3 fallback (`:136` → `dev@test.com`). The Lambda's own log prints the
   identity inside the very warning that claims no context was found. This is the SECOND
   wrong-location fix on this field (2026-01: `authorizer.claims.email` → `authorizer.email`;
   truth is `authorizer.lambda.email`) — so the acceptance test is behavior-grade, not a code
   read: a real authenticated request must produce a DDB row with the real email. Fix: resolve
   context as `authorizer.get('lambda', authorizer)` before the existing Method-1 read; keep
   userType gating semantics identical. Rollback rows get the same treatment (`triggeredBy` at
   `:1290` already flows from `validate_user_type`; extraction is the only break). ALSO in this
   touch: line ~918's docstring example says `yang@opalcapital.com` — a domain WE DO NOT OWN
   (CLAUDE.md Rule 23); change to an `opalinvest.dev` example. History rows already stored with
   `dev@test.com` stay as-is (true record of what was captured; do not rewrite history).

## Law that binds

- Terraform-only Lambda deploy; commit → TF → source map → plan → safe-apply → 0-diff → tag →
  push --follow-tags (CLAUDE.md Deployment Rules 1–6, Rule 18 safe-apply HALTGT).
- Rule 22a on the verify: the seam fix is a BEHAVIOR claim — exercise it (a real rollback on a
  non-served/test-safe target or a controlled window, showing the version-restore path actually
  firing with the exec id in the log), never a config read. A DESIRED-only claim is INFERRED.
- Deploy-completion ledger entry (`org/critical_paths/change_management/`) opened at deploy-start.

## Cross-domain contract cell (named)

The rollback POST response (`method`/`newExecutionId`/`status`), the status-polling payload, and
your new rejection status are consumed by `portal/src/hooks/useDataRefreshState.ts` (DE's
TO_PORTALREFRESH_FE_01). Any shape change or new status value is a named contract change —
message DE by MCP before it lands, and version the change in your closure note.

## Acceptance

- Exercised both ways: (a) a rollback whose outputs-manifest EXISTS restores via VersionId (log
  line proves the path); (b) concurrent second rollback is rejected with the machine-readable
  status; (c) fallback path still works when no manifest exists (pre-fix archive entries).
- 0-diff terraform after apply; source map current; no non-ASCII in deployed prints.
- Closure to 1.0.0_SA_CTO + CC 0.2.0_DE (contract) + CC 2.0.0_SA_COO (ledger close).
