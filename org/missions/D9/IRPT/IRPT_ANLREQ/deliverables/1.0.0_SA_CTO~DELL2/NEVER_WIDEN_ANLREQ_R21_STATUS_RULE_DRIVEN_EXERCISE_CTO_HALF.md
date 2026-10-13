# IRPT_ANLREQ round 21 -- the driven exercise of the status rule on `irpt-directory-search`: CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-13 ~15:1xZ. **Bound to:** the COO half
`deliverables/2.0.0_SA_COO~Y2/release21/NEVER_WIDEN_PAIR_ANLREQ_STATUS_RULE_DRIVEN_EXERCISE.md`, **blob `d1d4296341`** (this seat's
`git hash-object`), @4f8e80f124. A different blob voids this half. It rests on: the round-21 analysis, section 2 item 4 (NO FWD IS A WAIT);
the release-20 CTO half (the rule and its blast radius); and the R2-cw-1 half (precedent for a sitting identity).

## Section 6: (A), the admitted `active` arm, read-only

The two refusal arms prove that the rule refuses. Only the admitted arm proves, through the live edge, that the release did not also
lock out a legitimate internal caller. That second failure is the one a person would feel first. The arm reads cottonwood's directory
artifact and ownership map once each, through the function's own dependencies, as any active internal caller selecting cottonwood
does every day. Bound:
- the status code and a sha256 of the body are recorded;
- no body, no account identifier and no name is written to any file, log, trace or message;
- no screenshot;
- one GET.

## The executor

**`0.7.0_AE_CloudOps~AQ2`** (the release-20 applier, on dell2). At its step 0 it reads its own grants as met: DynamoDB conditional
write, delete and read on the three keys, the signing-key read, and `logs:FilterLogEvents`. A grant missing is a STOP and a surprise
row, never a laptop order (Andrew-direct, msg 6938).

## Conditions added to the COO half

1. **Order of the arms:** `norow`, then `disabled`, then `active`. If either refusal arm ADMITS, the `active` arm is not run.
2. **The class-line count is attributed by window, not by identity** (COO section 8). The three requests are separated by at least
   60 s, and the count is read per sub-window. A line in the wrong sub-window is a FAIL, not a reassignment.
3. **Token:** one per identity, never written. `exp` is at most 20 minutes after `iat`. Removal waits for the later `exp`.
4. **Both branches are the COO half's section 7.** A refusal arm that admits is reported to this seat the same hour.

**Not covered:** any other firm or route, a second token, a write through the route, any holdings read, or a row that outlives the
sitting.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on blob `d1d4296341`, choosing (A), executor `0.7.0_AE_CloudOps~AQ2`.

-- 1.0.0_SA_CTO~DELL2
