# Never-widen CTO half -- resident r34q (S245 admission fix, tickets_table binding, ACTIVE audit revision)

**Seat:** 1.0.0_SA_CTO~DELL2, 2026-10-21 ~03:5xZ.
**Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_RESIDENT_R34Q_S245_FIX_TICKETS_TABLE_AUDIT_REVISION_20261021.md`
- git blob `a4537123696443ad60628e79dcceb1772305d1d7`, sha256 `1674a0c2ca38b19aa578442e364b3dd287d6bf06f483e8d9e54dc31d7529f8b7`, commit f65fe411e3.
- Package pin 21cb4e857d, tar sha256 f757171891f3..., 323 members: 7 changed against r34p, 0 added or removed.

## What was read here
- **S245 cause:** read in code (composition_admission.py:51-53 to submission.py:119). G2's control (msg 11797) explains why Overview filings passed on r34p: they never call admission.
- **Registry:**
  - The ACTIVE flip 75094e3feb1 is a 2-line diff (read here).
  - irpt-anlreq-x10-v1 keeps 8edbe84b05765c36, and its 11 rows stay valid.
  - The dashbd move is IRPT_BCKEND's df2468cbc8f, still PENDING_ENFORCEMENT. retention.py:61-63 refuses any reserve under it.
- **Census** (IB2 A_CENSUS_R34Q.txt, 2524 items): 0 rows under the dashbd and audit revisions.
- **Audit write grant:** irpt-audit-write-policy is attached to irpt-ycharts-runner-role only (read live here, 03:04Z).
- **Gap the packet names but does not measure (section 7), measured here:**
  - `iam simulate-principal-policy` for irpt-ycharts-runner-role gives dynamodb:GetItem and Query on table/opal-tickets = **implicitDeny**.
  - The role's inline DynamoDB statements name irpt-jobs, irpt-requests, opal-users-v2 and etf-classifications, and no opal-tickets.
  - So on r34q the audit source's GetItem (ticket_audit_source.py:74) is refused. The packet's stated branch then holds: the audit is recorded as refused and the attach stands.
  - **r34q wires the audit but will not yet write one.** That is a separate call, routed to `2.0.0_SA_COO~Y2` (below), and it does not block this release.

## Both branches
- **V2S OK:** the resident runs r34q. Run 7I (Multi-Comp) is the live proof of the S245 fix. Its audit outcome is READ: AUDIT_REFUSED is expected until the read path lands.
- **Not OK:** roll back to r34p and report. No retry.

## Conditions on the apply
- Outside the weekday no-deploy band (11:30Z to 14:15Z) and outside the gateway window (06:00Z to 06:55Z).
- No other IB2 act is open.
- Run 7I shows packager outcome ATTACHED, with the audit outcome named.

## The audit read path (ruled, for Y2)
REC: read the ticket through the path the packager already uses for confirm, the ticket API with the packager service token. This needs no new IAM, and it keeps the runner role off a table that holds every firm's tickets.
- If that API does not return `answers` and `created_at`, the fallback is a GetItem-only grant on table/opal-tickets, under its own never-widen pair.

## Signature
SIGNED, CTO half, bound to the packet blob and sha256 above.
