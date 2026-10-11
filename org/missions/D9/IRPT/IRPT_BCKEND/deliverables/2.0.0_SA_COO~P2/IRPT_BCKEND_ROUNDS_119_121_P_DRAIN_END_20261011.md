# L8 drain end -- IRPT_BCKEND rounds 119, 120 and 121, workstream ~P (adds to the round 118 packet @6eaa44414b)

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-11 ~09:4xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD |
**Judgment criteria:** 0 | **round-close:** rounds 119, 120 and 121 each read MAY-CLOSE (`round-close-check.py`: orders=1, judgment=0)

## Why these three rounds exist

The DSGN_IRPTV1 FWD-1 walk of 2026-10-11 07:30Z broke at Performance. This seat placed the refusal from the adapter's logs:
`performance/authorization.py:90`, the operator-installed one-use vendor plan (4 of 4 admitted requests, `VendorEgressRefused`, public
code OBJECT_NOT_COVERED). The CTO ruled the gate retired by Andrew-direct 2026-10-09 (egress open except Bloomberg; msgs 4416, 4488,
4509). One release, one pair: COO half @468df7baa4, CTO half @7a01aa805a.

## Round 119 (issuance @fb3bae3b99): 1 of 1 COMPLETE

- **IB-pr-421** (`~282`, WORLD, build only): the plan requirement removed from the vendor path; six kept behaviours each with a named
  test; the adapter rebuilt from one commit (cd833e66cb), built twice identical, `OF+8j4ucXsxwJ195NKEQZnma22T8bYVUriw9YP859RU=`; 5
  changed members, all in `performance/`. Issuer re-grade at box/dell2: AC1, AC2, AC3 PASS, proof VALID. Drained @416ead492f.
- The issuance's first commit attempt was REFUSED by the gate: its preflight said `comp-iam: RUN` for a tool the issuer had not run.
  Corrected to DECLARED-NOT-APPLICABLE before the commit landed.

## Round 120 (issuance @0311c5f85d): 1 of 1 COMPLETE

- **IB-pr-422** (`~283`, WORLD, plan only): the adapter role's two session-read policies ungated from the plan variable in
  `retained.tf`. The first session STOPPED correctly on CTO condition 3: the untargeted plan read 2 add, 1 change, the deferred Lambda
  line caused by `lambda.tf:62-65` (row D2-W283-S1). CTO ruled a targeted plan (AMENDMENT 1 @99d71afa7b); the slot was re-seated
  (the stopped subagent could not be resumed). Targeted plan: 2 add, 0 change, 0 destroy; naming limb PASS. Issuer re-grade: AC1, AC2,
  AC3 PASS, proof VALID. Drained @311ed8c55c.

## Round 121 (issuance @a29b86ba86): 1 of 1 COMPLETE

- **IB-pr-423** (`0.7.0_AE_CloudOps~IB2`, WORLD): the release applied in one sitting under one ledger entry (CLOSED, 5 of 5 legs,
  @b424a3c4a1). Source map re-pinned @f5d33c7aa9; the two policies by a targeted apply (2/0/0); the zip on the full root (0/1/0).
  - **Read by the issuer after the close:** live adapter CodeSha256 `OF+8j4uc...859RU=` (modified 09:19:10Z); the live role holds 9
    inline policies and each session policy is ONE statement granting only `secretsmanager:GetSecretValue` on its ONE signed ARN
    (IB121-1-AC2, a live read); AC1, AC2, AC3 PASS and proof VALID on the issuer run.
  - Per `~IB2`, not re-run here: the live call answered 200 with a typed NOT_AUTHORIZED 16 s after the promote, 0 TypeError and 0
    AccessDenied of 6 events; no vendor reached, read on eight log indicators all 0; four planted mutants each failed its criterion.

## The one real run of the outcome -- ABSENT, by design

**APPLIED, UNEXERCISED.** The pair forbids any agent making a vendor call to test the release, so no admitted fresh vendor request has
run on these bytes. The outcome's one real run is the laptop's re-walk of DSGN_IRPTV1 FWD-1, asked through the managers now that the
ledger is closed. Until that walk reads a performance figure the Performance hop is not graded.

## Rows for the compile

- **D2-W282-S1** (role lacked the secret read): met by IB-pr-422 and IB-pr-423; the resolving row is owed by this seat.
- **D2-W282-S2** (an identical repeat of a vendor request is refused `RetainedVendorFigureRefused`): OPEN, not held by this release; it
  will show in a re-walk that repeats a request.
- **D2-W282-S3** (one calendar-fallback test fails; it imports none of the changed modules): OPEN; "pre-existing" is inferred until it
  is run on the pre-change tree (CTO half condition 4).
- **D2-W283-S1** (the deferred Lambda plan line): ruled by AMENDMENT 1; the resolving row is owed by this seat.
- **D2-S71** (`~IB2`): the IB-pr-421 packet says IAM is a surface the Dells cannot write; the apply from dell2 shows that claim false
  as a general statement. A defect of the signed packet's wording, with no effect on the act.
- **D2-S72** (`~IB2`): `build-and-upload.sh` restores pinned members from HEAD after a build; twice the restore met `.git/index.lock`
  from another seat's commit, printed a WARN and exited 0. A shared-worktree build can leave a tracked file carrying staged content with
  no error. For the round-N analysis: a build in a linked worktree, or a failing exit on a failed restore.
- Left for a later cell: `var.approved_performance_plan`, `local.performance_plan_firm` and the two plan environment variables.

## Carried

- **IB-pr-413** L4 and **IB-pr-404** L6: the Monday 2026-10-12 14:15Z 49F fire.
- The walk's second break, `FIRM_BINDING` at `_authz/served.py:1214` (the reporting-read firm map), is IRPT_DASHBD's cell
  (`2.0.0_SA_COO~D2`, msg 4458), not this lane's.

**Push state:** LOCAL on box/dell2 (MSTR box-sync pushes); re-measured in the send.
