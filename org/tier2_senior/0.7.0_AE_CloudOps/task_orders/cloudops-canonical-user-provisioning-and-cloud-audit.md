# Ad-Hoc TO — Canonical opal-users-v2 Provisioning Script + Prompt Embed + Full Cloud Audit (0.7.0_AE_CloudOps)

**Type:** Ad-hoc (no project) — Andrew direct directive 2026-05-28
**Issued to:** 0.7.0_AE_CloudOps
**Author:** 1.0.0_SA_CTO 2026-05-28T~22:10Z (Andrew explicitly directed CTO to author this ad-hoc TO)
**Authority anchor:** Andrew direct 2026-05-28 — "make a standard script for adding users to opal-users-v2 in canonical form... include the script and process in their system prompt like the convert-and-upload schwab rps for 0.6.1_AE_PartnerETL... then do an entire audit of the cloud, updating compiler graph and scanning for security issues."
**AMENDMENT 2026-05-28T~22:30Z (Andrew direct):** the old `create_user.py` is **deprecated** — build from the CURRENT state of opal-users-v2 + the partner tables. Provisioning is **firm-branched**: partner firms carry different scoped permissions that vary by the structure of their business, so the canonical process must apply the firm-appropriate scope. Phase 1 reframed below (was "canonicalize the old script" → now "deprecate it; reverse-engineer the live per-firm model + build firm-aware provisioning").

<status>complete</status>

## Sequencing (STRICT — Andrew said "once it is done... after that is done")

This is a **3-phase sequence**, gated and ordered. **It is LOWER priority than your active ADVI_INFMVP F3 deploy and the LD-0131 L1 halt-gate fix** (both this-session targets). Finish/close those first, then execute this sequence. Do NOT context-switch off F3 or LD-0131 L1 to start Phase 1 here.

- **Phase 1** → **Phase 2** (gated on Phase 1 ship) → **Phase 3** (gated on Phase 2 ship). RAVC2 to COO at each phase boundary; CC CTO.

---

## Phase 1 — Canonical, FIRM-AWARE user-provisioning for opal-users-v2

### Pre-authoring finding + AMENDMENT (CTO + Andrew direct 2026-05-28T~22:30Z)
The existing `users/scripts/create_user.py` (+ `users/tools/list_users.py`, `view_config.py`) is **DEPRECATED — reference only, do NOT build on it.** It writes a flat `FIRM#/CONFIG#defaults` map that does not reflect the current per-firm permission model. The `infra/aws/auth/migration/00*.py` scripts are likewise **stale** — migration `003_create_firms.py` still has only `opal-capital` uncommented; 49financial / inflection / cottonwood are LIVE in prod but absent from it. **Derive the canonical process from the LIVE state of the table + partner tables, NOT from these scripts.** Archive/supersede the old script so there is no ambiguity about what is canonical. (The emoji defect in the old script is moot once it's retired — the new script is ASCII-only from the start.)

### Core requirement (Andrew direct): provisioning is FIRM-BRANCHED
Adding a user is **not one-size-fits-all** — the correct permission scope depends on which firm the user belongs to, and **partner firms carry different scoped permissions that vary by the structure of their business.** Current-state (empirical, confirm + extend at discovery):
- **opal-capital** (internal, tier=internal): sees everything; no allowlist restriction.
- **49financial** (tier=advisor): full advisor hierarchy — regions / offices / advisors; allowlist incl. advisor-intelligence + trade-submission; region/office scoping applies.
- **inflection**: advisor-intelligence (Distribution + Books, no per-advisor drill); NO trade-submission; simpler structure; no region/office hierarchy.
- **cottonwood**: NO advisor-intelligence; trade-submission yes; identity-and-allowlist only (no data pipeline).
- **demo**: pseudonymized clone; full canonical path set.

A user's scope is assembled across **multiple LIVE layers** the process must read and apply coherently:
1. **opal-users-v2** — `USER#{id}/PROFILE` (user) + `FIRM#{firmId}/META` (firm: tier, status, domain) + `FIRM#{firmId}/MEMBER#{userId}` (membership). GSIs: email-index (login), firmId-index (list-by-firm).
2. **firmAccess.ts** (`portal/src/lib/firmAccess.ts`) — `FIRM_ALLOWED_PATHS` per-firm page allowlist + `FIRM_EMAIL_DOMAINS` per-firm email domain (provisioning should validate the new user's email domain matches their firm; deny-by-default on unknown firm, mirroring `isPathAllowedForFirm`).
3. **JWT claim contract** — firmId, role, advisorId/advisorRole, tier (issued at login, read by `auth-validator-edge`).
4. **Partner tables** — `opal-partners-data` (partner API), `opal-partner-cottonwood` (cottonwood-specific), any other `opal-partner-*` — the partner-specific scoped-permission structures.
5. **TenantLayoutConfig** (`portal/src/pages/AdvisorIntelligence/_shared/types/TenantLayoutConfig.ts`) — per-tenant layout/feature/data-source primitive.

### Objective
Produce **(a)** a documented **per-firm provisioning scope-profile map** — "what a user at firm X gets" across all the layers above, for each live firm — and **(b)** a canonical, firm-aware, ASCII-only provisioning script that branches on `--firm` and applies the correct scope (PROFILE fields incl. tier/role/region-office applicability, the `FIRM#/MEMBER#` write, email-domain validation, partner-table linkage where required), refusing unknown firms deny-by-default.

### Requirements
- **(a) Empirical current-state discovery FIRST (before writing the script).** Scan the LIVE `opal-users-v2` (enumerate `FIRM#*/META` records + a sample `PROFILE` per firm to see the real field set each firm's users carry); read the partner tables (`opal-partners-data`, `opal-partner-cottonwood`, any `opal-partner-*`); read the portal scoping layers (firmAccess.ts, TenantLayoutConfig, the JWT-issuing login path). Capture the **per-firm scope-profile map** as a deliverable doc (`docs/reference/user-provisioning-firm-scope-profiles-20260528.md` or dated equivalent).
- **(b) Firm-branched script.** Takes `--firm`; applies that firm's scope profile — correct tier, the role set valid for that firm, region/office fields only where the firm's structure has them (49F yes; inflection/cottonwood no), the `FIRM#/MEMBER#` relationship write, email-domain validation against FIRM_EMAIL_DOMAINS, and partner-table linkage where the firm requires it. Unknown / unprofiled firm → refuse (deny-by-default).
- **(c) Canonical item contract verified against the production auth path** — read `auth-validator-edge index.mjs`, `infra/aws/lambda/portal_authorizer/`, the RS256-JWT login handler, plus a live `get-item` sample, to confirm the exact field set + casing the runtime reads off a PROFILE item. Document in the script header.
- **(d) ASCII-only** — zero Unicode > U+007F anywhere (the old script's emojis are a CLAUDE.md violation; the new one is ASCII from line 1).
- **(e) Idempotent + safe** — existing-user guard via email-index; `--force` explicit + logged; no destructive default; bcrypt retained; SES behind `--no-ses` opt-out.
- **(f) One canonical script, one path** — supersede/archive the deprecated `create_user.py`; no orphaned duplicate. Deterministic ASCII output (userId + canonical field set + firm scope applied) so an operator run is self-documenting.

### Compiler mandate (Phase 1)
- Before: `comp-pii audit` — opal-users-v2 + partner tables hold PII (email, name); confirm the field set you write matches the pseudonymization/cleartext policy. Enumerate the boto3 surface (`dynamodb:PutItem/Query/GetItem/Scan` across users + partner tables, `ses:VerifyEmailIdentity`) — runs under operator creds (local-runtime admin script, not a Lambda); note required operator-IAM actions in the header.
- After: re-run `comp-pii audit`; register the canonical script + the scope-profile doc as nodes in the compiler graph (`comp-build`).

### Acceptance criteria (Phase 1)
- **AC1.** Per-firm scope-profile map documented for every live firm (opal-capital / 49financial / inflection / cottonwood / demo), grounded in empirical live-table + partner-table reads (not the stale migration scripts).
- **AC2.** Canonical script is firm-branched: provisioning a user at firm X applies X's correct scope, verified for at least 2 structurally-different firms (e.g. 49financial WITH region/office + trade-submission vs inflection WITHOUT). Unknown firm refused (deny-by-default).
- **AC3.** Item the script writes is read successfully by the production auth path (empirical test-user create/verify/cleanup on a DISPOSABLE email — never a real human's account).
- **AC4.** Zero non-ASCII bytes (`grep -P '[^\x00-\x7F]'` returns nothing). Idempotency guard verified. Exactly one canonical script; deprecated `create_user.py` archived/superseded. Canonical contract documented in header.

### RAVC2 (Phase 1)
`[RAVC2-Request] cloudops-user-provisioning Phase 1 — firm-aware canonical provisioning` to COO; CC CTO. Body: the per-firm scope-profile doc + script path + commit hash + the canonical field contract + comp-pii output + the 2-firm provisioning verify evidence + test-user create/verify/cleanup.

---

## Phase 2 — Embed the script + process into your own prompt.md (sole-ownership section)

Gated on Phase 1 RAVC2-accept. **Mirror the pattern Andrew cited** — the same way `0.6.1_AE_PartnerETL` carries the schwab-convert/upload responsibility and `0.6.0_AE`'s "Gold Script Deploy Ownership" section codifies a sole-owned recurring task (canonical reference: CLAUDE.md Rule 13, the DS deploy-cycle ownership).

### Action
Add a dedicated section to **your own** `org/tier2_senior/0.7.0_AE_CloudOps/prompt.md` — title it e.g. `## User Provisioning Ownership (opal-users-v2)`. It must contain:
- The canonical script path + the exact command forms, including the `--firm` branch (one example per live firm class).
- The **per-firm scope-profile summary** from Phase 1 (what a user at each firm gets — tier, allowlist, region/office applicability, partner-table linkage) + a pointer to the full scope-profile doc.
- The canonical item contract (field set + casing) from Phase 1.
- The explicit statement that **0.7.0_AE_CloudOps is solely responsible** for opal-users-v2 user provisioning going forward — new-user requests route here, this is the only sanctioned mechanism (no console-direct PutItem, no ad-hoc one-off scripts).
- The PII/least-privilege note + the existing-user guard + deny-by-default-on-unknown-firm behavior.

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

`<scoped>` — Phase 1 touches `users/` (identity-infra, CloudOps/security domain — your lane) + writes a scope-profile doc under `docs/reference/`, and READS the partner tables + `portal/src/lib/firmAccess.ts` + TenantLayoutConfig (read-only — do not edit portal source). If owned-paths blocks the `users/` commit, coordinate with the registered owner or flag to CTO. Phase 2 is your own prompt.md. Phase 3 is read-mostly audit (graph refresh writes comp-graph artifacts + the brief; any infra *change* surfaced is a follow-on TO, not in-scope here — audit FINDS, it does not FIX). Do not deploy remediations under this TO without a separate GO.

## Notes
- "Short" intent (per Andrew's "short ad hoc TO"): the SCRIPT stays lean, but Phase 1 is now a genuine build grounded in live-state discovery (the old script is deprecated, not a base) — the firm-branched logic + the per-firm scope-profile doc are the substance. Keep the script tight; if it balloons well past the old ~290-line script's size, flag back to CTO (dispatch-with-size-guard discipline).
- The per-firm scope-profile map is the load-bearing deliverable — the script implements it. Get the profiles right (empirical, from live tables) before coding the branches.
- Phase 3 "entire audit of the cloud" is real but bounded by the 4 axes above — if you find the scope materially larger than ~1 session, surface a phased follow-on to CTO rather than running indefinitely.

— 1.0.0_SA_CTO (Andrew-directed ad-hoc) 2026-05-28T~22:10Z
