# IRPT_BCKEND.TO-IB-rtj-1 -- result, by `0.9.0_WK_IRPT_BCKEND~13`

**State: TERMINAL on the mechanical criteria (R101-AC1, R101-AC2); AC3 recorded for `3.0.0_SA_CVO~B`
(not self-graded).** First pass STOPPED arm (f)'s S3 publish/ledger sub-step because neither half was
at HEAD naming this packet's blob, exactly as the order and DELIVERABLE section anticipate. **SECOND
PASS (2026-09-22 ~01:3xZ):** both halves are now at HEAD naming the same packet blob
(`2450320a688a4740af81d3a72f281b2a06f05b23` -- `2.0.0_SA_COO~B` @`5b67db0397`, `1.0.0_SA_CTO`
@`088669b331`), re-verified unchanged from when originally re-derived. Arm (f) executed in full: see
the updated "Arm (f)" section below.

## Arm (a) -- baseline reproduction (BEFORE any edit, at pre-repair HEAD)
Ran `IRPT_BCKEND_R9_CAPTURE_REDIRECT_DIAGNOSTIC.cjs` and `IRPT_BCKEND_R8_CAPTURE_DIAGNOSTIC.cjs`
UNCHANGED against the UNCHANGED source. C-S153 reproduced exactly as the order states: case
"initial foreign hop returns to portal" -> `writes=1, success=true` (the counterexample); case
"verification foreign hop returns control" -> refuses (already repaired by `IB-rti-1`). R8's three
cases behaved as `IB-rti-1` left them (all refuse via `INSTANCE_ID_MISSING_OR_INVALID` /
`ORIGIN_NOT_ALLOWED`, since the diagnostic supplies no instance id). Outputs:
`IB-rtj-1_baseline_r9_redirect_diagnostic.json`, `IB-rtj-1_baseline_r8_diagnostic.json`.

## Arm (b) -- the repair (commit `bfe67b1eab`)
Added `walkRedirectHops(resp)` and `assertNoForeignHop(resp, origin, label)` to
`capture-session.cjs`, factored out of the redirect-chain walk `readinessRefusal` already ran for
the VERIFICATION navigation (`IB-rti-1`'s own S127 repair, unchanged in effect). `main()` now calls
`assertNoForeignHop` on the INITIAL navigation's response immediately after the first `page.goto`,
before the port-forward command is ever printed -- in ADDITION to the pre-existing final-URL check
(not removed, not weakened). Mechanism: every hop is read via `resp.request()` then
`.redirectedFrom()` repeatedly; a hop whose origin is not the configured origin refuses immediately,
naming the offending URL. Changed lines: `infra/aws/ec2/investor-reporting-export/capture-session.cjs`
(new functions ~ lines 125-158 by search; call site in `main()` at the first `page.goto`) @`bfe67b1eab`.
S125 (instance-id validation), S126 (marker check) and S127's vendor-list equality are untouched.

## Arm (c) -- W9-S1, the allowlist derivation-or-verification
Kept `ALLOWED_ORIGINS = ['https://opalinvest.dev']` typed (option 2 of the cell's OR), because there
is no fixed compile-time default to derive from at RUNTIME: the SSM document parameter `PortalOrigin`
(`infra/aws/terraform/investor-reporting/export/ssm.tf:35,84`) carries no `default`, and
`render_export.cjs` itself holds no allowlist of its own -- it reads `IRPT_PORTAL_ORIGIN` from its
environment at runtime (`render_export.cjs:141`, `need('IRPT_PORTAL_ORIGIN')`). Traced that env var to
its ONE literal source: `infra/aws/terraform/investor-reporting/export/main.tf:92`
(`local.portal_origin = "https://opalinvest.dev"`), wired to the controller Lambda's env
(`lambda.tf:68`, `IRPT_PORTAL_ORIGIN = local.portal_origin`) and forwarded into the render document's
own shell env by parameter substitution (`ssm.tf:84`). Added battery arm `origin` (not one of the two
gated invocations, but part of THE CELL): reads `main.tf`'s literal, asserts `ALLOWED_ORIGINS[0]`
equals it, and proves the detector is non-vacuous by mutating a copy and confirming the mismatch is
caught. No DEV/localhost origin is admitted (checked). Output: `arm_origin` in
`battery_ib_rtj_1.py --arm origin`.

## Arm (d) -- regression + single-difference pair + positive control
Re-ran the R9 diagnostic UNMODIFIED against the repaired source: all 6 cases now match intended shape
(both foreign-hop cases refuse; same-origin positive writes 1 and succeeds). R8's 3 cases are
BYTE-IDENTICAL to the pre-repair baseline (diffed programmatically in `arm_redirect`). Built
`harness_ib_rtj_1.cjs` (this worker's own -- `IB-rti-1`'s harness hardcodes a single-hop chain for the
INITIAL navigation and cannot vary it) to run: (BAD) the exact "initial foreign hop returns to portal"
shape -> refuses (0 writes, `ORIGIN_HOP` naming the foreign URL); (GOOD) the SAME shape with ONLY the
foreign hop removed -> succeeds (1 write) -- isolating the fix's exact discriminating power; (POSITIVE)
a fresh 2xx/same-origin/no-password/marker-present control -> 1 write, success. NEGATIVE CONTROL run
this session (not part of the battery's own pass/fail, run separately against the pre-fix blob via
`git show bfe67b1eab~1:...`): the SAME R9 case against the UNREPAIRED source does NOT match the
post-repair intent (`success=true` where the fix requires `false`) -- confirms the check is a real
discriminator, not a tautology. Output: `arm_redirect` in `battery_ib_rtj_1.py --arm redirect`.

## Arm (e) -- the host-delivery runbook (C-S156)
Edited `infra/aws/ec2/investor-reporting-export/README.md`'s session-establishment steps: inserted a
new step 2 (renumbering the rest) that (i) `aws s3 cp`s the two published keys under
`s3://opal-313476888478-lambda-artifacts/ec2/investor-reporting-export/` to their host paths, (ii)
runs `sha256sum` on both host files, (iii) states the exact expected hashes (git-blob bytes: `capture-
session.cjs` at commit `bfe67b1eab`, sha256 `defcb58572276f36036d610d296f53df32f86477ffb3e6b17aab00c6
f6c2d95a`; `capture-session.sh` unchanged since `IB-rti-1`, sha256 `17ae44f0d6ee0a2f30225a99446f74c33
fb82ce893026bb9852d211581ef89e0`) and instructs the operator to STOP if either does not match. A
preceding paragraph states plainly that this step is NOT optional and NOT one-time -- it runs EVERY
time before the wrapper is invoked -- and explains why the render document's own sync cannot be
relied on instead (it is a side effect of a *render* being dispatched, unscheduled, and not this
wrapper's own path). Output: `arm_runbook` in `battery_ib_rtj_1.py --arm runbook`.

## Arm (f) -- the packet, then the publish (SECOND PASS)
Wrote `IB-rtj-1_NEVER_WIDEN_PACKET.md` naming the ONE changed file's git blob and sha256 (`capture-
session.cjs` only; `capture-session.sh` is unchanged and is NOT republished, since its bytes were
already published by `IB-rti-1` and republishing byte-identical content would claim an act this cell
did not perform). Committed it. First pass STOPPED: censused, no half existed yet.

**Second pass (2026-09-22 ~01:3xZ):** both halves confirmed present at HEAD, both literally naming
this packet's blob (`2450320a688a4740af81d3a72f281b2a06f05b23`). Re-derived
`git rev-parse HEAD:.../IB-rtj-1_NEVER_WIDEN_PACKET.md` at my own HEAD (`5b82db7a31`) myself and
confirmed it still equals that value -- the packet had not drifted since signing. Then:
1. Opened the deploy-completion ledger `irpt-rtj-1-capture-tool-publish` BEFORE the act (one leg L1,
   `s3-prefix`), sentinel + entry committed at `8ff0ffc1af`.
2. Materialized the git-blob bytes (`git cat-file -p HEAD:<path>`), independently re-hashed them
   (sha256 `defcb58572276f36036d610d296f53df32f86477ffb3e6b17aab00c6f6c2d95a`, matching the packet's
   table) BEFORE upload.
3. `aws s3 cp` published those exact bytes to
   `s3://opal-313476888478-lambda-artifacts/ec2/investor-reporting-export/capture-session.cjs`
   (VersionId `llAMqS_QPopRTb3T9KWyHLX8jJvoQWS4`).
4. Read the object back via `s3api get-object` and independently re-hashed the retrieved bytes: sha256
   `defcb58572276f36036d610d296f53df32f86477ffb3e6b17aab00c6f6c2d95a` -- equals the packet's
   blob-derived table exactly.
5. Closed leg L1 with that readback proof, closed the ledger entry (sentinel removed), committed at
   `ef15e1bd45`.

`capture-session.sh` was NOT republished (byte-identical since `IB-rti-1`, per the packet's own
reasoning, unchanged). **The host remains STOPPED throughout; this cell does not start it, and no
on-host byte verification is claimed or exists** -- the S3 readback above is the only verification
this act performs or can perform.

## Nothing else regressed (feeding AC3(iii))
Re-ran `IB-rti-1`'s own `battery_ib_rti_1.py` arms `command`, `readiness`, `origin`, `diagnostic`
against the REPAIRED source (unchanged battery file, read-only): all four PASS (rc=0), matching
`R91-AC1/AC2/AC3/AC4`'s original verdicts. `R91-AC5`'s packet arm necessarily now differs (the OLD
packet names a now-stale blob for `capture-session.cjs`) -- that is not a regression, it is why this
cell writes a NEW packet (arm (f) above) rather than trying to make the old one match. Outputs:
`.scratch/rti1_arm_{command,readiness,origin,diagnostic}_post_repair.txt` (not committed -- scratch;
the verdict tokens/exit codes are quoted in the WORKER REPORT).

## Not done / not claimed
No host start/stop, no live login, no credential, no MFA automation, no real session file, no network
call to the portal -- everything exercised under stubs (VM-sandboxed real source, or static text
reads). **No on-host byte readback exists anywhere in this cell** (arm f's own text says so, both
passes) -- the second pass's S3 readback verifies the PUBLISHED OBJECT, never the host. The allowlist
was NOT changed to a DEV/localhost value, and none of S125/S126/S127's existing checks were weakened
to make a new case pass (re-verified: `IB-rti-1`'s own battery still passes in full against this
repaired source).

## Controls
Negative control on arm (d)'s exact regression case, run against the pre-fix blob (`git show
bfe67b1eab~1:...capture-session.cjs`): does NOT match post-repair intent, confirming the check
discriminates. Non-vacuity control on arm (c)'s drift detector: a mutated `ALLOWED_ORIGINS` copy is
caught as unequal to the root value. Non-vacuity control on arm (e)'s runbook check: a simulated
pre-fix README (delivery/hash block removed) is correctly reported as MISSING the required evidence
(checked interactively this session, not committed as a battery arm since the real README no longer
has that shape to test against without a temp file, which would be scratch-only).
