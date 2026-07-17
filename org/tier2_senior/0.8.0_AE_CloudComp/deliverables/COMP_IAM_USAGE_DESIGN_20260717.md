# comp-iam-usage -- design (decommission research, thread 2/3)

**Author:** 0.8.0_AE_CloudComp · **Date:** 2026-07-17 · **Thread:** Andrew-direct decommission research (thread 2 of 3; comp-debris ext = thread 1 done @f921f9e97, resource_heat_snap = thread 3 queued)
**Status:** RESEARCH / DESIGN + validated prototype. Extends the IAM signal past comp-iam's Terraform-DESIRED plane. Building lands at `org/modules/graph/` (ANY_EXEC) -> build lane/CTO.
**Source:** `DECOMMISSION_TOOLING_ASSESSMENT_20260717.md` Part A @890e66375 · **Steer:** Andrew 2026-07-17 ("go ahead with comp-iam expansion").

---

## 0. TL;DR

`comp-iam` answers a **deploy-time correctness** question: *does this role have the perms this call needs?*
(Terraform-DESIRED, `(action)`-mostly-not-`(action,resource)`, plus one live `simulate` mode). The
decommission question is a **different one on the same substrate**: *is this grant / role / resource still
USED, and who else still reaches it?* That is a **lifecycle** question -> a **sibling `comp-iam-usage`**
(assessment lean b: separation of concerns; keep the deploy-time tool focused).

Its core signal -- **`RoleLastUsed`** -- is live, populated, and the **identity-plane twin of comp-debris
invocation coldness**, so it reuses `comp_debris.classify()` VERBATIM (same bands, same three refinements).
A role unused 90+ days is the single cleanest "nobody uses this" signal, and comp-iam captures NONE of it.

**The Rule-22a MANDATE (CTO, this lane):** comp-iam-usage must **FIX-OR-EXPLICITLY-CARRY** comp-iam's three
named limits, never silently inherit them: (1) `(action)`-not-`(action,resource)`; (2) DESIRED-not-APPLIED;
(3) an unparsed Deny reads as silence. The `who-can-reach <arn>` mode is the APPLIED-plane fix for limit 2
on the resource side.

---

## 1. Grounding (live, this session -- 2026-07-17)

- **`iam_cli.py`** (the comp-iam engine) modes: `gaps`/`roles`/`services`/`service`/`role`/`stats` (all
  Terraform-DESIRED) + `simulate` (the one live-AWS mode: `get_role` + `simulate_principal_policy`, the
  APPLIED `(action,resource)` check Rule-22a leans on). **No usage / last-used / resource-policy / trust /
  Access-Advisor mode exists.**
- **209 IAM roles** in the account.
- **`RoleLastUsed` is live + populated:** `inf-accounts-v2-daily-role` -> LastUsed 2026-07-17T13:22Z (today),
  Created 2026-05-07. (Note: `ListRoles` does NOT populate `RoleLastUsed`; `GetRole` does -> per-role fetch,
  or Access Advisor bulk.)
- **Access Analyzer: NONE configured** (`list-analyzers` = `[]`) -> AWS's native unused-access finding is NOT
  available today. The tool must COMPUTE coldness (RoleLastUsed + Access Advisor); enabling an analyzer is a
  recommendation, not a dependency.
- **Resource policies readable:** `opal-data-inf` carries a bucket policy (CloudFront OAI `s3:GetObject`
  grants) -> the `who-can-reach` mode is viable via `get-bucket-policy` / `get-key-policy` / etc.

---

## 2. The signal table (assessment Part A, with live availability)

| Signal | Source | Availability | Decommission use |
|---|---|---|---|
| **RoleLastUsed** (last assume) | `get-role.RoleLastUsed` | **live, populated** | role unused 90d = clean "nobody uses this" (the headline) |
| Service last-accessed (**Access Advisor**) | `generate-`/`get-service-last-accessed-details` | available (async 2-step) | WHICH services a role actually used -> prune unused *service* grants (finer than whole-role) |
| **Access Analyzer** unused-access | `list-findings` | **ABSENT** (no analyzer) -> recommend enabling | AWS-native "this role/key/permission is unused" |
| **who-can-reach `<arn>`** (resource policies) | `get-bucket-policy`/`get-key-policy`/`get-queue-attributes`/`get-topic-attributes`/lambda `get-policy` | readable | "does ANYTHING still have access to this resource" (the resource side comp-iam lacks) |
| **Trust / assume-role graph** | `get-role.AssumeRolePolicyDocument` | readable | a role nothing can assume is dead; a role trusting a decommissioned service is dead |
| Managed-policy attachments -> grant set | `list-attached-role-policies` + `get-policy-version` | readable | fold into the REAL grants (comp-iam under-counts standalone policies) |

---

## 3. Architecture -- reuse the coldness engine, add the resource side

1. **`role-cold` (the headline) = `comp_debris.classify()` on the identity plane.** RoleLastUsed.LastUsedDate
   -> `last_activity_day`; role CreateDate -> creation; the SAME bands + 3 refinements. A role created but
   never assumed is STILLBORN-OR-GUARD (a break-glass / emergency role is NOT debris), never ranked cold.
   `signal_basis = iam-role-last-used`. **Prototype validates this end-to-end.**
2. **`service-access <role>`** = Access Advisor (generate/get-service-last-accessed-details) -> the services
   a role has NOT touched in 90d = prunable service grants (grant-level, finer than whole-role retirement).
3. **`who-can-reach <arn>`** (APPLIED-plane, the Rule-22a limit-2 fix) = the resource's own policy principals
   UNION every identity policy referencing the ARN -> the full reach set. Empty reach on a live resource, or
   reach only from dead roles, is a decommission tell.
4. **`trust`** = the assume-role graph (who/what can assume each role) -> orphan-trust detection.

---

## 4. Honesty controls (reuse comp_debris; add the IAM-specific ones)

1. **NEVER-USED != COLD** (refinement 1): a never-assumed role splits by CreateDate (TOO-YOUNG vs
   STILLBORN-OR-GUARD) -- a break-glass role is a rare-event guard, not debris.
2. **UNKNOWN IS A BAND** (refinement 2): a role with absent RoleLastUsed (never used, or predating the
   tracking) is UNKNOWN -- blind, not cold.
3. **HOLD-AWARE** (refinement 3): `_HELD_RX` on the role name (inf-chain / sovereign roles excluded).
4. **Rule-22a: FIX-OR-CARRY comp-iam's 3 limits, never inherit them silently** --
   (a) `who-can-reach` is APPLIED (reads LIVE resource policies), not DESIRED -> fixes limit 2 on the
   resource side; (b) a resource with an unreadable policy is UNKNOWN, never "no reach" (limit 3: an
   unparsed Deny / unreadable policy is not silence); (c) reach is `(action,resource)`-grounded via
   `simulate-principal-policy` on the exact ARN when a verdict is asserted (limit 1) -- ONE `--resource-arns`
   per call + a separately-run positive control (Rule 22a's two false-deny modes).
5. **ADVISORY, never deletes**: the identification column feeds OPAL_LCLRPO's existing CTO-gated,
   Andrew-delete-word path. No second disposal path.

---

## 5. Recommendation for the gate

- **Ship as a SIBLING `comp-iam-usage`** (not a comp-iam mode) -- the lifecycle question is orthogonal to
  deploy-time correctness; overloading comp-iam risks the deploy-time tool answering a usage question with a
  DESIRED-plane read (exactly the class Rule 22a warns about).
- **Enable an account unused-access Access Analyzer** (Andrew/CTO) -- it is purpose-built for this cleanup and
  currently absent; the tool consumes `list-findings` when present, computes from RoleLastUsed + Advisor when
  not. Low cost, AWS-native corroboration for the reap tail.
- **Boundaries:** read-only (`list-roles`/`get-role`/`get-*-policy`/`generate`+`get-service-last-accessed`);
  building lands at `org/modules/graph/` (ANY_EXEC) -> build lane/CTO (same split as comp-similar + comp-debris).
