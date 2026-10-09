# L8 drain end -- IRPT_BCKEND rounds 94-96, workstream ~P (adds to the rounds 92-94 packet @c087bc3893)

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-09 ~04:3xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD |
**Judgment criteria:** 0 | round-close: round 95 MAY-CLOSE (3 of 3); round 94 open on IB-pr-383.

## Round 94

- **IB-pr-382 (custody ports 1/3/4 for release 6; worker ~190): COMPLETE**, 3/3 PASS, drained @3998906069.
  - The ports wrap the admitted `intake/custody_interpreter`; default COT only.
  - The read set went to ~Y2. Rows W190-S2 (`current_authority`) and W190-S3 (pyarrow, ARMED, owner ~Y2) were handed to the release-6
    owner.
- **IB-pr-383 (the ONE directory release; applier): OPEN.**
  - A1 refresh is live at `6eOFTopG` and B1 bundle at `OxaIJns0` (sha `2e3e6648`), proven @627f6fa99e.
  - Steps S1/S2 (seeding) and V1 (after-read) are BLOCKED on `ssm:SendCommand` to the runner host i-02448edb624a7a7cf (row D2-S25). MSTR
    has routed it to the laptop as a host-access grant; the host stays running (MSTR msg 2396). The ledger stays RED until the remaining
    steps run.
  - Row D2-S22 (stale root header) was resolved by D2-S23. Deadline: cottonwood OVER_AGE 2026-10-12.

## Round 95 (CTO msg 2351: code-only cells cut now, releases after 383) -- all COMPLETE

- **IB-pr-384 (~195): the runner refuses a build that drops a source entry.** 2/2 PASS (4 `refuse_drop` tests; runner suite 368 of 369
  with the S71 red excused), drained @1895f16a0b.
  - The refusal applies to writing calls; a dry run records it and returns 1 (row W195-S1, accepted).
  - The stale `main.tf` header is removed, comment-only.
- **IB-pr-385 (~196): `svc-custody-statement` firm-bound admission.** 2/2 PASS (23 tests; `_authz` 291), drained @dd02e66933.
  - Row W196-S1 was resolved by D2-S26: both host zips already package `opal_naming` and the registry.
- **IB-pr-386 (~197): `svc-commentary` read surface.** 3/3 PASS (10 tests; reports 141; surface file), drained @c3d6d3ea16.
  - The callee is the direct-invoke Lambda `irpt-commentary-composition-read-lambda`; the caller holds InvokeFunction only. owner is
    stripped. The Terraform is DESIRED and was sent to ~T2.

## Round 96 issued (@89fe99c780, drained @669ab7d677)

- **IB-pr-387 (~198):** the profile-row allowedFirmIds narrowing at `served.py` extends to internal callers (CTO msgs 2363 and 2368;
  ~V2 msg 2389). A non-list value or a lookup error fails closed, and ALL never admits. It is chained after IB-pr-385, the same file.

## Queued after IB-pr-383 closes

H1 (READY-event hookup; checks and order pre-written), then the release pairs of 384, 385, 386 and 387.

**Push state:** LOCAL on box/dell2 (MSTR pushes :18/:48).
