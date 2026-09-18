# IB-rtd-8 -- THE FIRM CHECK RESTORED ON THE OPERATIONS-VIEWER BRANCH -- RESULT

**Cell:** IB-rtd-8, round 4. **Worker:** `0.9.0_WK_IRPT_BCKEND~1`. **Row:** IRPT_BCKEND-W1-S16.

## The premise correction (row IRPT_BCKEND-W1-S19)

The task order's own face, quoting the issuer's Rule-22 census, states the advisor-axis defect
sits in **two independently-broken copies** of `Enforcer.covers()`:
`_authz/enforce.py:351 @5c59f68d70` and `holdings/enforce.py:319 @5c59f68d70`.

Reading `_authz/enforce.py` at that exact pin (`.scratch/authz_enforce_5c59f68d70.py`, this
turn) shows the branch **already fixed**: the firm-membership check (lines 342-349) runs before
the FIRM_OPERATIONS/OPAL_GLOBAL branch at line 351, refusing any advisor id not in the verified
firm's own ownership map for every principal class. The fix landed at commit `49035683d1`
(IB-rt-2, round 2) -- an ancestor of both the cited pin `5c59f68d70` and this branch's own HEAD
(`git merge-base --is-ancestor`, both rc=0, this turn).

`holdings/enforce.py` was never a second, hand-maintained implementation: `holdings/stage.py`
and `STAGE_MANIFEST.json` show it is a **pinned, committed-blob copy** of `_authz/enforce.py`,
staged from `git show <pin>:<path>` — and the recorded pin, `2a42c9563f0b31f983bc955285ba4a0d5f3385f8`,
pre-dates the IB-rt-2 fix. So there was one canonical defect, one canonical fix, and one stale
pin — not two branches to hand-edit in parallel.

## The fix

`holdings/enforce.py`'s `enforce.py` member is re-staged, byte-for-byte, to the fixed
`_authz/enforce.py` content (sha256 `69808e78...`, 34707 bytes). `STAGE_MANIFEST.json` and
`BUILD_MANIFEST.json` are updated for **that one member only** — pin `28ccac62c9` (the latest
commit touching `_authz/enforce.py`; a no-diff merge, content unchanged since `49035683d1`).
`errors.py`, `resolve.py` and `handler.py` are left at their original pin because their content
is byte-identical at HEAD; the packaged contract (`HoldingsSnapshot.schema.json`) is left
untouched because its content *does* differ since the old pin, and this order forbids a
contract change. `BUILD_MANIFEST.json`'s `source_vintage` is advanced to this branch's own HEAD
(`ebf5eae0c8`), where all four declared `vendored_modules` are index-equal (verified by
`manifest-index-check.py`'s own ran-sentinel this build).

## Deploy (row IRPT_BCKEND-W1-S20)

`build-and-upload.sh` refuses to build `irpt-holdings` out of the box: `lambda-source-map.json`
declares `served.py`/`loaders.py` in `files[]`, both are genuinely packaged and served in
production, and neither exists anywhere in the repository (a second, independent instance of the
untracked-production-source-file class `memory/feedback_structural_over_cultural_pattern.md`
item 6 already names). Worked around, in scope: both files were extracted **unchanged** from the
currently-deployed zip, materialized in the worktree for the duration of the build only, and
removed again before any commit — the served bytes for those two members never moved. Filed as
row W1-S20 rather than repaired (fixing it permanently is a `holdings/`-scoped code change this
order's bound does not authorize).

Rebuilt via `infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-holdings`
(`HALT_ACK=1`, routine checkpoint, 0 STOP-class messages, per `.tools/halt-gate-check.sh`'s own
classifier), uploaded, `terraform apply` under ledger `irpt-bckend-rtd8-holdings-advisor-fix`
(`0 to add, 1 to change, 0 to destroy`), re-plan `No changes`. Served `CodeSha256`
`UllXBBuvOzO+7SMQIUUsld1IlClqkk2cOAy8UxHx8h0=` == built == `lambda-source-map.json`'s recorded
value. Live download post-apply: `enforce.py` member hashes to the fixed content; every other
member (`served.py`, `loaders.py`, `snapshot.py`, `errors.py`, `resolve.py`, `handler.py`,
`entry.py`, `stage.py`, the contract) is byte-identical to what was already being served — only
`enforce.py` moved.

Deploy census (arm c): of the 7 functions `lambda-source-map.json` declares packaging
`enforce.py`, the OTHER six (irpt-directory-search, irpt-narrative, irpt-performance-adapter,
irpt-ycharts-generate, irpt-export-render, irpt-status) already served the FIXED `_authz`
content **before this order started** (their `enforce.py` member hashed to `69808e78...` on the
very first live read this turn, pre-dating any change here) — because they flat-copy
`_authz/enforce.py` at build time and were rebuilt at some point after `49035683d1` landed.
Only `irpt-holdings` was stale. `N of N` = 7 of 7 now verified fixed live.

## Live-route proof (arm d)

`M of M` = **0 of 7** — VACUOUS, measured this run, not assumed. Read fresh: the API Gateway
integration (`infra/aws/terraform/investor-reporting/api/integrations.tf`) is HTTP API v2 with
`payload_format_version = "2.0"` and no request template, so a real Lambda event never carries a
top-level `object_kind` key unless AWS itself sets one (it does not — HTTP API v2's own event
shape is fixed). A source census of every real `enforcer.guard(...)` call site in the repository
this run (`export/download.py` -> `"pdf"`, `holdings/snapshot.py` -> `"account"`,
`export/handler.py` -> `"report"`, `ops/status.py` -> `"firm"`, `_authz/served.py`'s generic
dispatcher -> whatever `event.get("object_kind")` is, which is always `None` through a real
request) finds zero call sites naming `"advisor"`. No live route can reach the branch this cell
fixed. The mechanism itself is proven directly against the real `Enforcer` class by arm (b)'s
six-swap census (12 of 12, both copies), with a mutant reproducing the pre-fix branch proven to
flip exactly the two cross-firm arms per copy (4 of 4) — the discriminator the criterion asks
for.

## R48-AC2 (judgment, answered for `3.0.0_SA_CVO`, no verdict taken here)

- **Should the two enforcer copies be one module?** They already effectively are: `holdings/enforce.py`
  is a pinned mirror of `_authz/enforce.py`, not an independent implementation, per
  `holdings/stage.py`'s own docstring (`infra/aws/lambda/investor-reporting/holdings/stage.py:10-15`
  @`ebf5eae0c8`). The remaining defect is PROCESS, not code: nothing re-runs `stage.py` when its
  upstream source changes, so the pin goes stale silently (this cell's own finding, row W1-S19/S20).
  Consolidation into a single physical file is unnecessary if the staging mechanism is exercised on a
  cadence; a cheaper fix is a CI check that fails when a staged member's pin is not the source's
  latest touching commit. Ownership: IRPT_BCKEND (the project that owns both `_authz/` and
  `holdings/`).
- **Does any route make an advisor id load-bearing today beyond an audit line?** No, measured 0 of 7
  this run (arm d above) — the `advisor` `object_kind` is reachable in-process (direct
  `Enforcer.covers()` / `Enforcer.serve()` calls, as this cell's own six-swap census does) but not
  through any deployed route's real dispatch path.
- **Is FWD-2/FWD-11's cross-firm bar closed on the advisor axis, or only narrowed?** Closed on the
  advisor axis specifically: both code paths that can reach `covers(..., "advisor", ...)` now check
  firm membership for every principal class (verified live, 7 of 7 functions). The bar as a whole
  (every object kind, every route) is outside this cell's scope to re-certify.

## Artifacts

- `battery_ib_rtd_8.py`, `IB-rtd-8_R48-AC1_battery_output.txt` (this run, rc=0, token
  `IBR48-FIRM-CHECK-RESTORED-ON-BOTH-ENFORCERS`).
- Deploy ledger: `org/critical_paths/change_management/20260918T1242Z_irpt-bckend-rtd8-holdings-advisor-fix_deploy_completion.md`
  (CLOSED, 2 of 2 legs proven).
- Surprise rows: `IRPT_BCKEND-W1-S19` (the premise correction), `IRPT_BCKEND-W1-S20` (the
  untracked served.py/loaders.py gap).
