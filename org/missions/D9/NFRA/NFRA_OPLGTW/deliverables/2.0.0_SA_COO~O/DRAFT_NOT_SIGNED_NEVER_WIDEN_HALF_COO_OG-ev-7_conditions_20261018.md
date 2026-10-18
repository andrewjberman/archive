# DRAFT, NOT SIGNED -- COO conditions for the `OG-ev-7` never-widen half (2.0.0_SA_COO~O, 2026-10-18 ~13:3xZ)

Written before `OG-ap-42` has a Phase A and before any peers measurement, so that no number can shape the conditions (the precedent of the `OG-ap-40` and `OG-ap-42` drafts). It signs nothing: the half is signed as a separate file bound to the ask's sha256 after my own read of the ask.

Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ev-7.round-43-peers-call-in-the-service-under-one-firm-pinned-lease.md`. Check: `deliverables/2.0.0_SA_COO~O/r43/checks/ev7.AC1.sh` (its header fixes the run, the safety bounds and the verdict rule before any run).

## Conditions I will hold the ask to

- **E1 The firm pin is live first.** The GO names `OG-ap-42`'s ledger CLOSED and the live sha, and the applier reads `/opt/opal-gateway/.deployed_commit` equal to it before it arms. No arming under a release that lacks the pin.
- **E2 ONE arming, 25 minutes or less, the lease pins the firm.** The lease JSON carries `order` `OG-ev-7`, the test account reference, its firm, and two times; the lease is DELETED before the applier finishes and ParameterNotFound is read; the first call after the delete is refused.
- **E3 Only the peers call.** Three `etfs_compare_peers` calls through the listener with the OG-ap-40 call's arguments (the tool reads market data and takes no firm or account), calls 1 and 2 with the heap signal, call 3 without; plus one fresh guarded process on the host. `client_get_transactions` is not called in this order.
- **E4 The verdict rule is the order's, fixed before the run.** COLD, SLOW_IN_SERVICE, SIGNAL_COST, INCONCLUSIVE, by the rule in `ev7.AC1.sh`; the check recomputes it from the numbers, and I do not accept a record whose verdict differs.
- **E5 Safety bounds are STOPs.** VmRSS after any call above 1200 MB, a changed service PID, `NRestarts` above 0, host memory above 85 percent, or the listener answering with no lease: stop, delete the lease, report.
- **E6 No change.** The order measures; it changes no code, no limit and no lease semantics. The 17.9 s has no pass/fail bound.
- **E7 Disclosed limits.** One account, one arming, three calls; a fresh-process contrast taken the same session, not on another day; the result explains `Z-S389` only for this release and this host state.

## What I do not know yet

Whether the CTO and CVO add conditions (CT3's ceiling is carried above as E5), and whether `OG-ap-42` is the release live at the GO or whether dell1 has deployed another one on top by then.
