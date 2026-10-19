# Ruling -- row D2-S239: Cottonwood's directory refresh wedged since 2026-10-14

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-19 ~13:5xZ. **Answers:** `2.0.0_SA_COO~P2` msg 10698, row `IRPT_BCKEND-D2-S239`
(`org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md:42238`).

## Read at ruling

`infra/aws/lambda/investor-reporting/directory/refresh.py:845-853`: when the previous manifest names a command whose status
is neither in flight nor Success, the fire raises `DispatchError("BUILD_ENDED_UNSUCCESSFUL")` and does not re-dispatch.
The failure manifest it writes carries no command id, so every later fire walks back to the same 2026-10-14 command.

## (a) The 6 clients the drop guard refused -- READ FIRST, never assumed

They are not carried TERMINATED on a guess. The runner's guard (IB-pr-384) worked as designed: it refused a build that
drops entries still present in the source snapshot.

`~P2` cuts ONE read-only cell. It names the build stage that drops the 6 (the join or filter, file:line) and counts what
they share (for example a missing advisor or account mapping). Hashed ids and counts only; no client data.
- **If it is a build fault:** its own fix cell and pair.
- **If it is a genuine source removal:** the documented path the guard admits, under a pair, with the evidence that the
  source itself ended them.

Note: the Cottonwood account-to-advisor map is PARKED for want of a source. The read should check that link first.

## (b) The wedge -- YES, cut the fix cell

A failed build must not block every later fire. The fix:
- the failure manifest records the failed command's id and status;
- the next fire treats that command as terminal and re-dispatches ONCE for its own fire date, never in a loop within a
  fire;
- an in-flight command still blocks, as today.

Acceptance, on fixtures:
- a Failed previous command re-dispatches exactly once;
- an in-flight command still returns without dispatch;
- a Success path is byte-equal to today.

The release is a Lambda change through Terraform, with its own never-widen pair, applied outside the 11:30Z to 14:15Z band.

## What the served directory does meanwhile

Until (a) is resolved, the unwedged fire will re-dispatch, and the guard will refuse each Cottonwood build again. That
is correct. Cottonwood's served directory stays as-of 2026-10-12 and reads `DIRECTORY_OVER_AGE` (STALE), which is the
honest state. No one forces a build past the guard.
