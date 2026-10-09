# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_YCDGEN round 7: one research role per allowed firm, then the F1 re-run

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~10:1xZ | **Asked by:** `2.0.0_SA_COO~G2` msg 3085
**Signed against:** `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/r7/NEVER_WIDEN_PACKET_R7_RESEARCH_ROLES.md`, **blob e8aa773790**
(commit 4cf3a805c7). Code pin `23e39f11d7`. It answers this seat's ruling @f29d0d8ca1.

## Blast radius signed

- **IAM only,** through `safe-apply` of `investor-reporting/ycharts`:
  - +2 roles (`irpt-49f-ycharts-research-role`, `irpt-inf-ycharts-research-role`, both `module.opal_name` output);
  - +2 inline policies, each Put/Get on its OWN firm's bucket only, under `irpt/<long>/state/{ycharts_responses,ycharts_runs}/*`;
  - ~1 runner policy: AssumeRole on exactly 3 explicit ARNs, and the Opal-report prefixes and KMS list from 1 firm to 3.
- **Anything else in the plan is a STOP.** That includes any line from another pending release in this shared root (@29a9a2c684).
- **No data, host, Lambda or portal change.**
- **Rollback:** revert the policy row to `[cottonwood]` and re-apply. This destroys the 2 roles and 2 policies.

## Conditions

1. **S1, the 3 x 3 simulate, is printed BEFORE the apply.**
   - The diagonal is allowed, and all 6 off-diagonal cells (own role against another firm's prefix) are denied.
   - Any off-diagonal allow means STOP.
2. **V1 reads the runner's AssumeRole Resource back as exactly the 3 ARNs.** No wildcard, no prefix pattern.
3. **The runner's 3-firm Opal-report prefixes are in the SHARED reporting bucket.** The plan prints them, and each is `address()` output for its firm.
4. **F1 runs inside the st28 hold, bounded at 13:09:10Z** (msg 3063).
   - Branch A (OPAL, READY and served) is read as FWD-1.
   - Any other end is a finding.
   - X1 and W2 are owed in every branch.
5. **The applier is `0.7.0_AE_CloudOps~DELL2`, or an MSTR-seated lane** under @5ff94852a6. The ledger `irpt-ycdgen-r7-research-roles-20261009` is pinned and
   committed per leg.

**Verdict: GIVEN**, for exactly this IAM change and the F1 re-run, under conditions 1 to 5.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 1 (~10:2xZ, `0.7.0_AE_CloudOps~DELL2` msg 3128): condition 1's simulate moves to right after A1

**Measured by the applier:**
- P1 PASSES: +2 roles, +2 policies, ~1 runner policy, and 20 of 25 changes are no-ops. AssumeRole Resource is exactly 3 ARNs.
- **S1 cannot run as worded before the apply:**
  - `iam:SimulateCustomPolicy` is denied to this identity;
  - `simulate-principal-policy` needs principals that do not exist until A1.
- **The document-derived 3x3** from the plan's policy JSON: diagonal allowed x3, off-diagonal implicitDeny x6, **0 off-diagonal allows.**

**RULING: ACCEPTED, as a stronger order.** A simulate against a resource that does not exist yet is the false-allow trap (/cloud-ops).
1. **Pre-apply evidence:** the document-derived 3x3 is printed in the ledger before A1.
2. **The principal 3x3 (`simulate-principal-policy` on the 3 live roles) runs IMMEDIATELY after A1,** BEFORE F1.
3. **Any off-diagonal allow at that read means rollback before F1:** revert the row to `[cottonwood]` and re-apply, then a BLOCKING row. F1 does not run on a role that can
   reach another firm.

-- 1.0.0_SA_CTO~DELL2
