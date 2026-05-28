# Ad-Hoc TO — Canonical opal-users-v2 Provisioning Script + Prompt Embed + Full Cloud Audit (0.7.0_AE_CloudOps)

**Type:** Ad-hoc (no project) — Andrew direct directive 2026-05-28
**Issued to:** 0.7.0_AE_CloudOps
**Author:** 1.0.0_SA_CTO 2026-05-28T~22:10Z (Andrew explicitly directed CTO to author this ad-hoc TO)
**Authority anchor:** Andrew direct 2026-05-28 — "make a standard script for adding users to opal-users-v2 in canonical form... include the script and process in their system prompt like the convert-and-upload schwab rps for 0.6.1_AE_PartnerETL... then do an entire audit of the cloud, updating compiler graph and scanning for security issues."

<status>pending</status>

## Sequencing (STRICT — Andrew said "once it is done... after that is done")

This is a **3-phase sequence**, gated and ordered. **It is LOWER priority than your active ADVI_INFMVP F3 deploy and the LD-0131 L1 halt-gate fix** (both this-session targets). Finish/close those first, then execute this sequence. Do NOT context-switch off F3 or LD-0131 L1 to start Phase 1 here.

- **Phase 1** → **Phase 2** (gated on Phase 1 ship) → **Phase 3** (gated on Phase 2 ship). RAVC2 to COO at each phase boundary; CC CTO.

---

## Phase 1 — Canonical user-provisioning script for opal-users-v2

### Pre-authoring finding (CTO, already done — do NOT greenfield)
A script **already exists** at `users/scripts/create_user.py` (plus siblings `users/tools/list_users.py`, `users/tools/view_config.py`). This Phase is **verify + canonicalize the existing script into THE standard**, not author-from-scratch. The existing script is functional but has defects:
1. **EMOJI VIOLATION (must fix):** it prints emoji characters (✅ ⚠️ ❌ 🚀 📋 🔑 📧). This violates CLAUDE.md "No emojis in code" — they break CloudWatch log queries on Windows (charmap codec) and log-parsing tools. Replace ALL with ASCII prefixes (`OK:`, `WARN:`, `ERROR:`, etc.).
2. Authored "Systems Architect" 2026-02-17, pre-org-system; not registered in the compiler graph; no canonical-contract documentation.

### Objective
Produce ONE canonical, ASCII-only, auditable script that is the single standard mechanism for adding a user to `opal-users-v2` in canonical form. "Canonical form" = the exact item shape the **production auth path actually consumes**, not merely what the old script happened to write.

### Requirements
- **(a) Verify the canonical item contract empirically.** Before locking the schema, confirm what the live runtime requires: read the auth/login path (`auth-validator-edge` `index.mjs`, `infra/aws/lambda/portal_authorizer/`, and the login handler that issues the RS256 JWT) to enumerate every field + exact casing the runtime reads off a `opal-users-v2` PROFILE item. Cross-check against the migration scripts (`infra/aws/auth/migration/001_create_users_v2_table.py`, `002_migrate_users.py`) and a live `get-item` sample. Document the contract in the script header.
- **(b) Canonical item shape** (confirm/correct against (a)): `PK=USER#{userId}`, `SK=PROFILE`, `email-index` GSI; fields `userId, email, name, passwordHash (bcrypt), role, tier, firmId, status, mustChangePassword, regionId, officeId, createdAt, updatedAt, createdBy`. Org-defaults pattern (`FIRM#{firm}` / `CONFIG#defaults`) retained.
- **(c) ASCII-only.** Zero Unicode > U+007F anywhere — prints, docstrings, comments.
- **(d) Idempotent + safe.** Existing-user guard via `email-index` (already present — keep + harden). `--force` overwrite path stays explicit and logged. No destructive default.
- **(e) bcrypt hashing retained; SES verify stays behind a flag (`--no-ses` opt-out).**
- **(f) Deterministic, auditable output** — print the resulting userId + canonical field set written, in ASCII, so an operator run is self-documenting.
- **(g) Canonical location + name.** Keep `users/scripts/create_user.py` as the canonical path OR rename to an unambiguous canonical name (your call; if renamed, leave no orphaned duplicate). One script, one path — delete/supersede any near-duplicate so there is exactly one standard.

### Compiler mandate (Phase 1)
- Phase 1 (before): `comp-pii audit` — opal-users-v2 holds PII (email, name); confirm the field set you write matches the pseudonymization/cleartext policy. Enumerate the boto3 call surface (`dynamodb:PutItem`, `dynamodb:Query` on email-index, `ses:VerifyEmailIdentity`) — this runs under operator creds (local-runtime admin script, not a Lambda), so note the required operator-IAM actions in the header rather than a Lambda role.
- Phase 3 (after): re-run `comp-pii audit`; register the canonical script as a node in the compiler graph (`comp-build`).

### Acceptance criteria (Phase 1)
- **AC1.** Canonical script writes an item that the production auth path reads successfully (empirically: create a test user, confirm the field contract matches what the JWT-issuing login path expects — do NOT smoke against a real human's account; use a disposable test email and clean it up).
- **AC2.** Zero emoji / zero non-ASCII bytes in the script (`grep -P '[^\x00-\x7F]'` returns nothing).
- **AC3.** Idempotency guard verified: re-running on an existing email without `--force` refuses safely; with `--force` overwrites with an audit line.
- **AC4.** Exactly one canonical script exists (no orphaned duplicate). Canonical field contract documented in the header.

### RAVC2 (Phase 1)
`[RAVC2-Request] cloudops-user-provisioning Phase 1 — canonical create_user script` to COO; CC CTO. Body: script path + commit hash + the canonical field contract + comp-pii output + the test-user create/verify/cleanup evidence.

---

## Phase 2 — Embed the script + process into your own prompt.md (sole-ownership section)

Gated on Phase 1 RAVC2-accept. **Mirror the pattern Andrew cited** — the same way `0.6.1_AE_PartnerETL` carries the schwab-convert/upload responsibility and `0.6.0_AE`'s "Gold Script Deploy Ownership" section codifies a sole-owned recurring task (canonical reference: CLAUDE.md Rule 13, the DS deploy-cycle ownership).

### Action
Add a dedicated section to **your own** `org/tier2_senior/0.7.0_AE_CloudOps/prompt.md` — title it e.g. `## User Provisioning Ownership (opal-users-v2)`. It must contain:
- The canonical script path + the exact command to add a user (with the common flag forms).
- The canonical item contract (field set + casing) from Phase 1.
- The explicit statement that **0.7.0_AE_CloudOps is solely responsible** for opal-users-v2 user provisioning going forward — new-user requests route here, this is the only sanctioned mechanism (no console-direct PutItem, no ad-hoc one-off scripts).
- The PII/least-privilege note + the existing-user guard behavior.

This is a self-edit of your own core persona doc — permitted (Abilities: you write your own prompt + session logs). Commit under your author line.

### Acceptance criteria (Phase 2)
- **AC5.** prompt.md carries the new ownership section with script path, command forms, canonical contract, and the sole-responsibility statement. Committed under `0.7.0_AE_CloudOps` author.

### RAVC2 (Phase 2)
`[RAVC2-Request] cloudops-user-provisioning Phase 2 — prompt embed` to COO; CC CTO. Body: prompt.md diff + commit hash.

---

## Phase 3 — Full cloud audit: compiler-graph refresh + security scan

Gated on Phase 2 ship. Scope: a **structured** audit across clear axes — not boil-the-ocean. Produce a written audit brief, refresh the compiler graph, and route findings.

### Axes
1. **Resource inventory vs source-of-truth.** Enumerate live AWS (Lambda, EC2, S3, IAM roles/policies, CloudFront, DynamoDB, Secrets Manager, API GW) and reconcile against `infra/aws/lambda/ci/lambda-source-map.json`, `infra/aws/ec2/EC2_MANIFEST.json`, and Terraform state. Flag drift (resources not in TF / not in source map / orphaned).
2. **Compiler graph refresh.** `comp-build`; register missing nodes (the new canonical user script; any Lambda/role/bucket absent from the graph). Confirm the refresh is clean.
3. **Security scan.**
   - `comp-iam gaps` — full Lambda/EC2 boto3-op vs policy cross-reference; flag any missing or over-broad (`*`) permission.
   - `comp-pii audit` — pseudonymized-vs-cleartext field audit across serving artifacts.
   - `comp-routes auth-map` — confirm every portal/API path has the expected auth gate; flag any unauthenticated path that should be gated.
   - S3 public-access / bucket-policy review across all buckets (esp. the ones flagged not-in-TF: `opal-data-portal-v2`).
   - Secrets exposure check (`opal/auth/jwt-public-key` and any others not in TF).
   - Fold in the standing **Known Issues #1-#9** from your prompt.md (CloudFront not in TF, opal-portal-authorizer untracked, missing scanner Lambdas, JWT secret not in TF, etc.) — confirm current status of each.
4. **Security-sweep Lambda.** Confirm `security-sweep-comprehensive` status (in source map, no TF resource) — does it run? what does it cover? gap vs this audit.

### Compiler mandate (Phase 3)
`comp-build` (refresh first) + `comp-iam gaps` + `comp-pii audit` + `comp-routes auth-map`. Raw outputs go into the audit brief.

### Acceptance criteria (Phase 3)
- **AC6.** Audit brief delivered at `docs/briefs/cloud-security-audit-20260528.md` (or dated to delivery): inventory-vs-source drift table, security findings (severity-ranked), Known-Issues #1-#9 status, compiler-graph refresh confirmation.
- **AC7.** Compiler graph refreshed (`comp-build` clean); new canonical user script registered as a node.
- **AC8.** Findings routed: architecture/infra-design findings → CTO; work/remediation items → COO. Any **critical** security finding (exposed secret, public bucket with sensitive data, missing auth on a sensitive path, over-broad IAM with blast radius) → flag immediately to CTO + COO, do not wait for the brief.

### RAVC2 (Phase 3)
`[RAVC2-Request] cloudops-cloud-audit Phase 3 — full audit + graph + security` to COO; CC CTO.

---

## Cross-domain coordination

`<scoped>` — Phase 1 touches `users/` (identity-infra, CloudOps/security domain — your lane). If owned-paths blocks the commit, coordinate with the registered owner or flag to CTO. Phase 2 is your own prompt.md. Phase 3 is read-mostly audit (graph refresh writes comp-graph artifacts + the brief; any infra *change* surfaced is a follow-on TO, not in-scope here — audit FINDS, it does not FIX). Do not deploy remediations under this TO without a separate GO.

## Notes
- "Short script" intent: keep the canonical script lean — it's a verify-and-canonicalize of an existing ~290-line script, not a rewrite. If your work balloons past ~2x that, flag back to CTO (per dispatch-with-size-guard discipline).
- Phase 3 "entire audit of the cloud" is real but bounded by the 4 axes above — if you find the scope materially larger than ~1 session, surface a phased follow-on to CTO rather than running indefinitely.

— 1.0.0_SA_CTO (Andrew-directed ad-hoc) 2026-05-28T~22:10Z
