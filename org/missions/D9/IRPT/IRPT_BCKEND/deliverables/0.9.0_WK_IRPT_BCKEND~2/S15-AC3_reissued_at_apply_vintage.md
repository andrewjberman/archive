# S15-AC3 REISSUED AT THE APPLY VINTAGE

**Closes slug row C-S77 (CTO ruling 8, `../../ledger/ROUND_ANALYSIS.round1.md` @`0d57ceb2f9`).**
**Reissued by:** `0.9.0_WK_IRPT_BCKEND~2`, cell `IB-rt-1`, 2026-09-11T12:30Z.
**Supersedes:** the S15-AC3 judgment text in
`IRPT_BCKEND.TO-IB-s-15.scoped-routes-opal-principal-and-the-cloudfront-behavior.proof_of_spec.json`
(same directory), which was written **before the apply** and said so: *"THERE WAS NO APPLY, and the
plan is the evidence."*

**Apply vintage:** `a7659fa6af` (the worker's COMPLETE commit on `wk-irpt_bckend-1-2`) merged to
`CLOUD` at `ac202969e8`. Distribution `EVTSA9VEHNZVH`, `LastModified 2026-09-11T09:45:02.857Z`,
Status `Deployed`.

---

## WHY A REISSUE RATHER THAN A CORRECTION

The original judgment was not wrong. It was **correctly dated to a world that no longer exists**:
it was written while the cell's own STOP was standing, and its central answer -- *"what does the
unauthenticated probe prove?"* -- was *"nothing yet, because it was not obtained"*. The apply
then landed under the CTO's ruling 95933, the probe WAS obtained, and a reader arriving at the
record today would read a pre-apply judgment as a statement about live infrastructure.

**A judgment is a claim about a vintage.** Editing the original would destroy the only artifact
that shows the STOP was taken before the act; leaving it alone leaves a stale claim as the only
record. So it is reissued here, dated, with the original left exactly as it was.

**THE HISTORIC STOP IS HISTORY, NOT CURRENT STATE.** The first plan named three resources, this
cell refused to apply it, and the refusal produced the measurement the sign-off was written on.
That is a completed episode. Nothing below is conditional on it.

---

## THE THREE THINGS THE RULING NAMES, DISTINGUISHED

The ruling requires these three to be told apart, because the apply changed **two** resources and
only **one** of them was this cell's intent. Reading them as one act would credit this cell with a
change it did not author, and would hide a recurring artifact that belongs to another owner.

### 1. THE INTENDED CLOUDFRONT BEHAVIOR

**What this cell meant to do, and did.** ONE `ordered_cache_behavior` appended to
`infra/aws/terraform/portal-auth/cloudfront-distribution.tf`: `path_pattern`
`/api/scoped/investor-reporting/*` -> origin `APIGateway-portal`, one `viewer-request` association
to `auth-validator-edge`, caching disabled.

| axis | measured |
|---|---|
| source diff | commit `d0a61c6acb`: **38 insertions, 0 deletions** on that file -- an append, and the numstat is the proof that the 27 pre-existing blocks were not re-written |
| plan | `Plan: 0 to add, 2 to change, 0 to destroy`; on the distribution, exactly **1** `+ ordered_cache_behavior`, **0** removed, **0** modified |
| apply | `Apply complete! Resources: 0 added, 2 changed, 0 destroyed.` -- distribution 47s |
| live before | `get-distribution-config EVTSA9VEHNZVH`: **27** ordered behaviors, ETag `E1R4W4GM4O06ET`, `investor-reporting` **absent** |
| live after | **28** ordered behaviors (+1 default = 29 total); the new pattern is **LAST** and is the **only** investor-reporting behavior; `diff(declared order, live order) = 0 lines` |
| convergence | the post-apply plan of the root names the distribution **not at all** |

**This is the whole of what this cell intended to change on the served surface.** No existing
behavior, origin or route was edited.

**INSTRUMENT LIMIT, STATED.** The pre-apply pattern-LIST file from the first window did not survive
the worktree re-cut. The pre-state of record is the first ledger entry's (27 behaviors, that ETag,
investor-reporting absent). The claim *"the prior 27 are unchanged IN ORDER"* therefore rests on
**two** instruments -- the git numstat (0 deletions) and the declared-vs-live order equality (0
lines) -- and **not** on a stale local file. Said here because the reader cannot re-derive it.

### 2. THE CLASSIFIED WAF NORMALISATION

**What this cell did NOT author and could not avoid.** `aws_wafv2_web_acl.opal_cloudfront_protection`
was the second resource in the plan and the second changed by the apply. It is **not** an
investor-reporting change and **nothing about it serves this project**.

| axis | measured |
|---|---|
| plan shape | 3 managed-rule blocks removed and the **same 3 re-added** -- `common-rule-set`, `ip-reputation`, `known-bad-inputs` |
| field diff | all 6 visible fields per block (`name`, `priority`, `metric_name`, `vendor_name`, `cloudwatch_metrics_enabled`, `sampled_requests_enabled`) -- **ZERO differing fields** |
| the one hidden attribute | `version`, `""` vs `null` -- exactly what the CTO's ruling classified it as |
| live Rules before/after | `get-web-acl`: **6** rules both times, same names **in the same order**, sorted-key JSON diff **EMPTY (0 lines)**; `LockToken` identical (`848a6d0b...`), stronger than the sign-off's exception required |
| recurrence | the post-apply plan reads `0 to add, 1 to change, 0 to destroy`, naming **only** the WAF -- it recurs every plan |

**It is a READ-NORMALISATION NO-OP: a provider representation difference, not a rule change.** The
Rules diff being empty is the discriminator -- had it been a real change, the six-rule JSON would
have moved. It did not.

**IT IS SOMEONE ELSE'S DURABLE ITEM.** Owner `0.7.0_AE_CloudOps`, as the CTO's ruling records. It
was admitted into this apply only by the bound the CTO widened **for that apply only** ("ONE change
plus the classified WAF no-op"). This cell did not fix it, and fixing it was never in scope.

### 3. THE OBSERVED REFUSAL PLANE

**What the world now does, and the precise boundary of what that proves.**

| | request | response |
|---|---|---|
| PRE (before any act) | `GET https://opalinvest.dev/api/scoped/investor-reporting/status` | **HTTP 200**, `text/html`, **1068 bytes** of `index.html` -- the SPA, because no behavior claimed the prefix |
| POST (after the apply) | the same request | **HTTP 401**, `application/json`, **51 bytes**, `{"error":"Missing or invalid Authorization header"}` |

**This is a DIFFERENCE CONTROL, not an assertion.** The same request, the same host, before and
after; the 200 is what makes the 401 mean something. It proves the prefix is now **claimed by a
behavior** and intercepted by the edge validator before reaching any handler, and that the refusal
body carries **no protected data**.

**WHAT IT DOES NOT PROVE -- unchanged from the original judgment, and still IB-rtb-1's territory:**

1. **Nothing about an AUTHENTICATED CROSS-FIRM request.** A valid JWT for firm A asking for firm
   B's client passes the edge validator **by construction** -- the validator checks a token, not an
   entitlement. Every control that matters is downstream (`FirmBinding`, the permitted-firm
   intersection, `_authz.guard`) and a 401 exercises **none** of them.
2. **Nothing about the authorizer's RESULT CACHE.** `naqxlm` returns a prior allow for its TTL, and
   that TTL is not declared in `infra/aws/terraform/partners-api/api-gateway.tf` (13 `authorizer_id`
   references, 0 caching declarations). It must be read from the live authorizer.
3. **Nothing about the two handlers that PREDATE the wrapper.** `irpt-directory-search` (IB-s-1)
   and `irpt-performance-adapter` (IB-s-11) merged before `_authz.guard()` existed. **A ROUTE
   CENSUS IS NOT A HANDLER CENSUS**, and only a deployed-route replay tells them apart.
4. **Nothing about a 403 FROM THE WRONG CAUSE.** "The edge rejected the token" and "the scope
   covered nothing" are both a 4xx to a client, distinguished only by a reason code an
   unauthenticated probe never sees.

**One thing IS now settled that was open at the original writing:** the Opal principal's class
comes from a server-side roster read **BY NAME** (`/opal/irpt/opal-principal-roster`) and **EMPTY
by default**, not from any injected claim -- `firmRole` is injected **zero** times by
`auth-validator-edge/index.mjs` (the nine injected headers are at `:383-391`), so it dies inside the
edge function. That required **no change outside this project**, which is why the roster path was
taken; the one-line edge fix remains outside this order's `<paths>` and is `0.7.0_AE_CloudOps`'s.

---

## CENSUS

Three headings, each greppable as a literal line in this file:

```
1. THE INTENDED CLOUDFRONT BEHAVIOR
2. THE CLASSIFIED WAF NORMALISATION
3. THE OBSERVED REFUSAL PLANE
```

**3 of 3** things the ruling names are present and distinguished. No verdict is offered here:
S15-AC3 is a JUDGMENT criterion, graded by `3.0.0_SA_CVO` at L9, never by its author.

---

## SOURCES

* `org/critical_paths/change_management/20260911T0940Z_irpt-bckend-s15-cloudfront-2_deploy_completion.md`
  -- CLOSED, 6 of 6 legs, each with its proof. The superseded entry
  `20260911T0855Z_irpt-bckend-s15-cloudfront...` closed on NON-EXECUTION when this cell's STOP fired.
* `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~2/battery_ib_s_15.result.md`
  -- section `S15-AC3`, the original (pre-apply) text, left unedited.
* `org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md`
  -- row `IRPT_BCKEND-W2-S12`, the STOP, closed by the CTO's ruling.
* Commits `d0a61c6acb` (the behavior), `14a0ebfb5f` (the OPEN sentinel, committed before the plan),
  `e7830e087c` (ledger CLOSED), `a7659fa6af` (IB-s-15 COMPLETE), `ac202969e8` (the drain to `CLOUD`).
