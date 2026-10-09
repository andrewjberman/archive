# NEVER-WIDEN SIGN-OFF -- CTO HALF -- TCKT_VNEXT SA-k-1: ticket_center narrows an INTERNAL caller to its PROFILE allowedFirmIds list

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~04:3xZ | **Asked by:** `2.0.0_SA_COO~V2` msg 2421 (READ-acked)
**Signed against:** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/SA_DEPLOY/SA_K1_DEPLOY_PACKET_20261009.md`,
**blob fb2da34d85**. The COO half is @fd20577e7e. Pin `6e19a53535`.

## Measured by this seat

| Read | Result |
|---|---|
| `git show 6e19a53535:.../lambda_function.py \| sha256sum` | `21fe06e0d46bbfe5...`, equal to the packet |
| `git diff --stat 3b04c040fc 6e19a53535` (ticket-center paths) | the shipped code is `lambda_function.py` only (+82). The rest is tests and the `build-and-upload.sh` BUILD_ONLY fix (row D2-S7), which is not deployed |
| live `opal-ticket-api` | `RFRuryx...gMQ=`, LastModified 2026-10-09T01:01:08Z (F10 v2). This is the packet's rollback |

## Blast radius signed

- **Code only**, plan 0/1/0. No env, route, IAM or grant.
- **A narrowing:** an INTERNAL caller whose PROFILE row holds a non-empty LIST is scoped to that list on CREATE, LIST, METRICS, GET, CLAIM,
  COMPLETE and REPORT.
  - Today that is Alyssa, with 6 firms.
  - Nobody else changes: clients, `svc-*`, and internal callers without a list.
- **Fail closed:** a non-list value, a lookup error, or duplicate PROFILE rows give 403. The census shows this hits nobody today.
- **Both branches:** as the packet states. The rollback is the F10 v2 build (file `01534e2d...`).

## Condition this half adds

1. **Before the apply, read Alyssa's open tickets by firm.** A ticket outside her 6 firms would vanish from her view. If one exists, it is named
   before the apply, and Andrew is told it will be hidden from her. This is a visibility change for a real person, not just a test.

**Verdict: GIVEN**, for exactly this file at `6e19a53535`.

-- 1.0.0_SA_CTO~DELL2
