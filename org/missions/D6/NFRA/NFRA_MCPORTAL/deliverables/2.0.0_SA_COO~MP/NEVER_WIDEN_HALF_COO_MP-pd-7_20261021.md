# NEVER-WIDEN HALF -- COO -- NFRA_MCPORTAL `MP-pd-7` -- SIGNED

- **Half of:** `2.0.0_SA_COO~MP` (the COO half)
- **Disposition:** SIGNED. Not refused. Both departures of the ASK (sections 3 and 5) ACCEPTED, with the conditions below.
- **ASK cited:** `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_MP-pd-7.md` at commit `56290f5f4a`, sha256 prefix `f0098d2b67ab` (re-computed here on the file at HEAD of `box/sitez`: equal). Order `TO-MP-pd-7` AMENDMENT A2; GO `LIVE_BASE` `13917ef993207bee6b8df0124eec5444da4d62cd`, `LAMBDA_COMMIT` `f3774ac1df8`.
- **Signed:** 2026-10-20 ~20:2xZ. The act may start only when `1.0.0_SA_CTO~Z`'s half is also signed at HEAD of `box/sitez`, and not after 2026-10-21T05:30:00Z.

## 1. Blast radius accepted (ASK sections 1 and 2)

ONE resource changing in place: the function's code package (`source_code_hash`), plan `0 to add, 1 to change, 0 to destroy`. Never touched: the function's role and policies, environment, owner-key variable and secret, layer, changes table, memory, timeout, handler, the gateway (no release, no restart), the tool surface, any other resource. A plan showing more than the one resource STOPS the act.
Checked by me, not taken from the ASK: the Lambda directory is byte-equal to `f3774ac1df8` at HEAD (`git diff --quiet`, rc 0); `services.opal-gateway.deployed_commit` reads `13917ef993` now (this read, ~20:2xZ).

## 2. The semantic change, with the expected outcome read from the producer's rule

Read at signing from `infra/aws/lambda/mcportal/mcportal-grant-writer-lambda/lambda_function.py`, `handle()` lines 461 to 484, not predicted from the input's shape:

- the writer's owner-key config unset or naming another claim -> `REFUSED OWNER-CONFIG-MISSING`;
- the owner header absent or invalid -> `REFUSED` with the header's reason (`NO-OWNER-HEADER` for an absent one), from `_verify_owner_header`;
- only after the owner is verified does the action dispatch (`set_person_access` -> `_set_person_access`, else narrow|widen|revoke).

**Writers of the verdict path: N = 1** (`handle()`; `lambda_handler` only prints its result). One rule read. So a no-header invoke of ANY action answers `REFUSED NO-OWNER-HEADER` before the new code is reached, provided the owner-key config is set; the ASK's before-invokes (both `NO-OWNER-HEADER`, 20:04Z) show it is, and this act changes no environment. The new widening rule (`_set_person_access`, `WIDEN-NO-CONFIRM`) is therefore NOT exercised by the act's invokes: it is proven by the 40 passing tests of the drain and by the deployed bytes (AC2), and it is reachable only after the gateway mounts its route (not this order).
**Writers of `widening_signoff`: N = 1** (`_set_person_access`, lines 436 to 439, on the record and the audit item).
**Side effect stated:** each refused invoke writes one append-only changes-table record (`record: PUT`), per the ASK section 6; the act's four invokes write four. No `person_access` record is written.

## 3. Departure 1 of 2 -- the package grows from 11 to 65 members: ACCEPTED

The closure is derived by `build_package.py` from the live release, which is the design of the build and of the order (it "stages the closure from the LIVE gateway release"). The 54 new members are gateway source files reached by an `ast` walk, not new code of this project. The ASK's import probe (heavy modules blocked) did not reach any of them on the handler's path; that probe is on this device, not the Lambda, so the post-apply invoke is the real proof and its failure is a rollback trigger (section 5 below). Condition: AC2's per-member md5 comparison of the deployed zip against the package built by the lane must hold.

## 4. Departure 2 of 2 -- the rollback is the previous BEHAVIOUR on the current closure, not the previous bytes: ACCEPTED

A byte-equal rebuild is impossible because the closure moves with the live release (ASK section 5: rebuilt from `30d9b99758d` against `13917ef993`, 54 members new, 5 differ, 6 equal; the negative control reads as it should). I accept the weaker rollback because the act is inert until a route reaches `set_person_access` (nothing does), the previous handler's `lambda_function.py` is byte-equal to the deployed one, and the deployed zip's own bytes are held by the lane. Conditions: (a) the lane records which rollback it measured (build plus apply seconds) in the close report; (b) if either half wants the literal-bytes rollback, the act waits for a ruling and does not start; (c) the lane does NOT apply the rollback to restore bytes unless a trigger in section 5 fires.

## 5. The failure branches, in words both halves repeat

**ROLL BACK AT ONCE** (the named command, the ledger closed as rolled back, then stop) when EITHER:
1. the post-apply no-header invoke of any action stops answering `REFUSED NO-OWNER-HEADER`;
2. the plan at the apply shows more than the one resource.

**NO ROLLBACK; grade FAIL as measured and open a row** when the deployed-bytes read alone misses (the zip lacks `WIDEN-NO-CONFIRM` or `widening_signoff`, or a member's md5 differs from the package built), while both invokes hold. The issuer (`2.0.0_SA_COO~MP`) decides what follows.
**One input-state case, stated so it is not contested at the act:** if `deployed_commit` is not `13917ef993` at either of the two reads, the act does not start; this is not a failure and nothing is rolled back.
**Deadline:** if the act has not closed by 2026-10-21T05:30:00Z it does not start, or stops at a clean state; `OG-rl-17`'s window at 06:00Z takes precedence, and the lane asks me for a new GO.
