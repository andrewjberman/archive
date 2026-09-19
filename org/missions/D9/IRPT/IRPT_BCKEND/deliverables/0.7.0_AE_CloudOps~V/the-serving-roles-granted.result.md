# IB-rtf-10 result (first pass): the census, the packet and the plans -- STOP at the halves, as the face expects

**Order:** `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtf-10.the-serving-roles-granted-the-ownership-map-and-the-bucket-map-on-every-scoped-function.md` @4ceb7f8361.
**Seat:** `0.7.0_AE_CloudOps~V`, worktree `/c/tmp/wk-irpt-6-ae1`, branch `wk-irpt_bckend-6-ae1` (fast-forwarded to CLOUD @4ceb7f8361).
**The packet:** `NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-10.md`, **blob `4e7ba624fa592ea74b2649d194303ca4fc6a3b43`**, committed @9f21dedfd8. The halves sign against this blob.
**The Terraform edits:** 11 files under `infra/aws/terraform/investor-reporting/`, committed @9f21dedfd8. **NOTHING APPLIED.**

## What the first pass did

- **(a) The census** of the 7 serving functions:
  - the ownership map is readable on **0 of 21** role x firm pairs;
  - the bucket map is present on **1 of 7** functions;
  - **directory read is 0 of 3 firms for 4 roles** (S93);
  - **inflection's ownership map is ABSENT** (S94);
  - holdings binds `_no_grant` by design and needs no map.
- **(b) The packet.** K-OM (6 roles) and K-ENV (6 functions), both derived from `data/firm_registry.json`, with the declared writers `W` per role. The policy names are the naming builder's output: `name("irpt", None, <function>, "policy", "ownership-map-read")`, graded CONFORMANT.
  - The commit-time naming gate (LGIC_ENFORCE DEC-6, ENFORCE) **refused the first spelling** (6 names without the `policy` kind).
  - The names were regenerated from the builder and the plans re-taken. The gate then passed 6 of 6.
- **(c) The plans.** 7 of 7 roots, **0 to destroy**, 13 changes. **But the roots are not at rest (S95):**
  - 4 function updates also carry a CODE change from artifacts uploaded at 07:29-07:31Z and never deployed (status, narrative, export-render, performance-adapter);
  - 2 carry an object-version bump with the same hash;
  - only ycharts is env-only.
  - `terraform fmt -check`: the new lines are clean. The fmt deltas the check prints in these files are pre-existing and untouched ("never fix a neighbouring defect").
- **(d) The halves.** ABSENT, so this is a truthful STOP. Arms (e) and (f) did not run.

## R67-AC1: FAIL at (d), by output (the face's expected first-pass outcome)

The battery ran at worktree HEAD 9f21dedfd8, rc 1. Deciding lines from `IB-rtf-10_R67-AC1_battery_output.txt`:

- (a) `ownership map readable: 0 of 21; directory readable: 9 of 21; bucket map present: 1 of 7`. Both packet census lines read EQUAL; the controls read positive allowed, negative implicitDeny.
- (b) The packet blob at HEAD equals the worktree (`4e7ba624fa...`), and the keys line is `K-OM 6; K-ENV 6`.
- (c) `roots planned without destroy: 7 of 7; total destroy 0; total changes 13; lambda updates carrying a CODE change 4 (row S95)`. **All 7 canonical digests re-take EQUAL to the packet's table**, so the digest is stable across plans and is the comparable identity at the apply.
- (d) `halves: 0 of 2`, so `STOP at (d)`.
- `RESULT: R67-AC1 FAIL -- 3 of 6 arms hold`.

## R67-AC2: JUDGMENT, recorded for 3.0.0_SA_CVO and not self-graded

**1. The object-scoped read from the serving roles, or the map published to a directory-readable prefix by its producer?**

- **The packet declares the object-scoped read, as the issuer's recommendation asks:** one object per client firm, GetObject only, derived from the registry.
- **What it keeps:**
  - the producer stays unchanged, with one writer and one location;
  - the rest of each firm's `platinum/` tier stays unreadable;
  - the cross-firm fence is the object key, which on the shared `opal-data-bd` is the only fence there is.
- **What it costs:**
  - **The absent-map case breaks (S94).** Without ListBucket, a missing object reads AccessDenied, and `_authz/loaders.py:106-114 @4ceb7f8361` re-raises it. The designed "absent map = empty map" branch (`:94-99`) is then unreachable for inflection. The object-scoped design is only complete if the producer publishes a map, even an empty one, for every client firm.
  - **Six roles now read a `platinum/` object**, where before only producers did.
- **What the alternative would cost:**
  - Publishing the map under `investor-reporting/directory/` would make it readable by every role that already reads the directory, **including `irpt-holdings-role`, whose design grants nothing** (`holdings/entry.py:17-25 @4ceb7f8361`).
  - It would put a second copy of an entitlement artifact in a second place, which is the dual-writer and staleness shape.
  - It would need a producer change and an S3 write.
- **The CTO's ruling on this packet is the authority, and it is not yet issued at this pass** (the halves are absent). So there is no difference to state yet. The recommendation stands on the packet's side, with S94 as its precondition.

**2. Why every earlier live proof passed, and what an acceptance instrument must do so this class cannot recur.**

- **The earlier proofs never ran under the deployed role.** IB-rtf-2's arm (e) "SERVED k=21" and IB-rtf-8's arm (e) both drove the REAL `served.Entry` / `enforcer_for` IN-PROCESS, as the IB-rtf-10 face itself records. The in-process harness runs under the operator's AWS credentials, which can read every firm's map and every directory object.
  - **The code was the real code, but the identity was not the deployed identity.** Bound 12 ("never a copy the battery wraps") was satisfied for the code and silently not for the principal.
  - **The environment was not the deployed one either.** An in-process run reads `IRPT_DIRECTORY_BUCKET_MAP` from the harness's own process or defaults, never from the function's configuration. So S90's second cause could not appear in-process at all.
- **What the instrument must do: a served-path proof runs UNDER THE DEPLOYED ROLE, WITH THE DEPLOYED CONFIGURATION, or it is not a served-path proof.** In practice, one of:
  - (i) **the real HTTP path with a real bounded principal**, as the IB-rtf-3 lifecycle did. This is the only arm that also covers the edge and the authorizer.
  - (ii) at minimum, `aws lambda invoke` of the DEPLOYED function, which runs under its role and its environment but bypasses the edge.
  - **The in-process run stays useful only as a MECHANISM test, and must be labelled so.**
- **And the proof must carry its own pre-grant negative control, measured under the same role.** For this cell that is S90's 12 of 12 UNEXPECTED @e7da534cc6. Otherwise a pass cannot be told apart from a path that was never exercised.

**3. S91's `None` sink is the reason the outage was invisible.**

- `_authz/served.py:628, 649, 662 @4ceb7f8361` record every internal error to a `None` sink, so the exception behind all 12 UNEXPECTED refusals never reached CloudWatch (S91, `1.0.0_SA_CTO`).
- Combined with the estate's standing no-monitor rule, **nothing could have surfaced S90 except a live authenticated request.** No operator could see it, and no dashboard existed to read.
- Rows S93, S94 and S95 were found by the same method, measuring the deployed plane directly: IAM simulation, head-object, the plan. None of them would have been found in-process either.

## Rows filed

- `IRPT_BCKEND-S93`: BLOCKING, ARMED, `2.0.0_SA_COO~B`. 4 roles have no directory read, a third cause.
- `IRPT_BCKEND-S94`: BLOCKING, ARMED, INFERRED, `2.0.0_SA_COO~B`. inflection's map is absent, so the object-scoped grant reads AccessDenied.
- `IRPT_BCKEND-S95`: BLOCKING, ARMED, `2.0.0_SA_COO~B`. The roots are not at rest; 4 plans carry undeployed code.

## What the re-hand needs

1. Both halves at HEAD naming the packet blob, and the CTO's ruling on the design.
2. A decision on S95: sequence the undeployed artifacts first, or sign the combined apply naming the four code changes.
3. A decision on S93: amend the face so the packet carries a directory-read key for the four roles, or cut it separately.
4. A decision on S94: publish an inflection map, or rule on a key-scoped ListBucket.

Then (e) the apply under a ledger, with the canonical digest re-compared, and (f) the path proven under the deployed roles with the bounded principal: the rtf-9 packet blob `a1f36b95b2`, a new epoch, and the IB-rtf-3 lifecycle.
