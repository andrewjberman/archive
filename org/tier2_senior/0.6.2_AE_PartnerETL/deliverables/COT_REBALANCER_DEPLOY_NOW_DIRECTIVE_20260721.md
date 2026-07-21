# Andrew-direct: DEPLOY cot-rebalancer-runner NOW + test (no stubs) + confirm + issue to CVO

**Recorded by:** 0.6.2_AE_PartnerETL · **Channel:** Andrew-direct, this session (Claude Code terminal)
**Time:** 2026-07-21T223948Z (~18:39 ET / EDT)
**XXX.md compliance:** durable record + broadcast (COO/CTO/MSTR), same turn.

## VERBATIM (Andrew, sovereign)

> "I want it deployed now and after it is done and tested (make sure none are stubs) then i want a
> confirmation from you this is the case and have you issue your work to CVO to check"

## What this directs

1. **DEPLOY NOW** -- WS-1 (cot-rebalancer-runner Lambda) + WS-5 (role/schedule TF @bc9f2585a). Overrides
   0.7.0's "sequence behind the MDPF cutover" deferral -- Andrew wants it live now.
2. **TEST after deploy, verify NO STUBS** -- exercise the deployed Lambda (a real live pull under the standing
   egress) and confirm the resources are REAL + FUNCTIONAL (real bronze pages/accounts/model-detail + the
   complete-stamp actually land), not placeholder stubs. Rule 22a: BEHAVIOR -> EXERCISE the path.
3. **CONFIRM to Andrew** once deployed + tested-not-stub.
4. **ISSUE my work to CVO** for an independent check.

## Constraints that still bind (deploying now does not lift these)

- Terraform-only apply via safe-apply (Rule 1/18); commit -> build-and-upload -> source-map -> plan -> apply
  -> 0-diff -> tag. CTO gates the apply.
- The WS-5 TF is in the **monolith opal-assets state (0.7.0's lane, mid-MDPF-cutover)** -> the apply must be
  SEQUENCED by 0.7.0 (NO concurrent applies on shared TF state) -- surfaced to 0.7.0/CTO.
- Read-only cookie-rider (GetSecretValue-only); firm-clean (never blackdiamond/49f); Rule-22a exact-ARN IAM
  verify on the LANDED role (post-apply).

## Disposition

Driving now: source-map entry + build-and-upload (my parts); coordinating the apply with 0.7.0 (owns the
monolith apply) + CTO (apply gate). Post-apply: 0-diff + Rule-22a verify + a real test invocation (no-stub
proof) -> confirm to Andrew -> issue to CVO.
