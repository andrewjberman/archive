# Never-widen CTO half -- resident r34p (r34o minus the registry change)

**Seat:** 1.0.0_SA_CTO~DELL2, 2026-10-21 ~00:45Z.
**Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_RESIDENT_R34P_R34O_MINUS_THE_REGISTRY_CHANGE_20261021.md`
- git blob `b945271a46421b823728ce54f0f34c115133ea0d`, sha256 `946371fa9b71744378d608cb14bfae65b010c0c876461b6487cf50c6aca745f3`, commit b1f5a914f5.
- Package pin 919bb891fa, tar sha256 4991c7bcba0f..., 323 members, 3 changed against r34o, 0 added or removed.

## What was read here
- **Ruling A conditions met.**
  - The registry is byte-equal to r34n's. The release checker also requires every reporting_policy() hash to equal r34n's, and it refuses the r34o tarball.
  - Census: IB2 A_CENSUS.txt (2506 items, 709 hashed rows) finds 10 rows under the two revisions, all on the r34n hash, and 0 on an r34o hash. r34p strands nothing and makes all 10 valid again, Andrew's 9 included.
- **This seat's own read of the trunk (box/dell2 HEAD):**
  - irpt-anlreq-x10-v1 and irpt-dashbd-x10-v1 equal their rows at 1c277930e66^ (dict-equal).
  - ANALYSIS_AUDIT now lives only in irpt-anlreq-audit-x10-v1 (PENDING_ENFORCEMENT, enforcement_ref null, ruling_commit 88ae067327). That row is NOT in r34p, so the audit address is refused by name and the attach stands. This is the intended dormant state.
- **Blast radius (section 3):**
  - one root on the resident host;
  - no IAM, Lambda, queue, table or vendor path.
- **Rollback (section 5):** to r34o, with r34n kept on the host.
- **Gate:** V2S OK, else rollback in the same session.

## Both branches
- **V2S OK:** the resident runs r34p. The next acts are run 7e's Overview repeat (Andrew's sample) and run 7f (Multi-Comp), one filing at a time.
- **Not OK:** roll back to r34o and report. No retry.

## Conditions on the apply
- Outside the weekday no-deploy band, 11:30Z to 14:15Z.
- No other IB2 act is open.
- TCKT_VNEXT.TO-R22-DL1 (TV2) is a separate IAM act on a different principal. It may run beside this host install, because the two share no resource. The audit policy apply still waits for r34p live.

## Signature
SIGNED, CTO half, bound to the packet blob and sha256 above.
