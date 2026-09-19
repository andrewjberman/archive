# RESULT -- IRPT_BCKEND.TO-IB-rtf-8 (holdings' forked enforcer folded onto the shared module)

Worker `0.9.0_WK_IRPT_BCKEND~1`. Full verbatim run:
`IB-rtf-8_R65-AC1_battery_output.txt` (this commit). Summary below; every count is re-derived by
the battery on each run, never carried by hand.

## Arm (a) -- the diff before the delete

`holdings/enforce.py` (blob `8f849457be`) vs `_authz/enforce.py` (blob `79c9d9dee1`, HEAD):
21 lines only-in-fork, 66 lines only-in-shared, 143 diff lines total. Re-derived independently:
`holdings/enforce.py`'s committed bytes were **byte-identical** to `_authz/enforce.py` as it stood
at commit `28ccac62c9eed361c669dada2aa36eee5d2a65c8` (`git hash-object` on that blob ==
`8f849457be`), which **pre-dates** the CTO's project-first inversion at `@61627f39f9`. Every
fork-only item is either (1) dead prose (the superseded refusal-order docstring), (2) the
superseded refusal LOGIC itself (refuse on any `UNPROJECTED-ID` gap before checking whether the
result is empty), or (3) the ABSENCE of the `unprojected_grant` disclosure machinery entirely (a
strict subset, never a divergent feature). None of it is load-bearing for the holdings route: no
holdings-specific caller (`snapshot.py`, `entry.py`) names a requirement for the stricter refusal,
and CTO ruling S82 (`@b37fdfd5cd`) names this exact gap as the defect the fold closes. NO STOP.

## Arm (b) -- the fold

- `holdings/enforce.py` deleted.
- `holdings/stage.py`'s `MEMBERS` tuple no longer stages `enforce.py` as a committed flat copy;
  `STAGE_MANIFEST.json`/`BUILD_MANIFEST.json` re-derived (4 -> 3 committed members, `enforce.py`
  dropped; `stage.py --check` reports `4 of 4` for the remaining staged contract + 3 modules
  byte-equal to their pins).
- `infra/aws/lambda/ci/lambda-source-map.json`'s `irpt-holdings` function gained a `staged_from`
  entry for `enforce.py` (`_authz/enforce.py` pinned at `949dc88099d2032caceb3c19312899791e2df4df`,
  sha256 `d1c8e7e094676526050309a90e4035084a3365e32435feb1b759458781804e93` -- re-derived this run
  to equal the CURRENT `_authz/enforce.py` blob, `79c9d9dee1`), the SAME `staged_from` mechanism
  `served.py`/`loaders.py` already use on this function (IB-rte-4/IB-rtf-6's pattern) -- so
  `enforce.py` can no longer go stale without the PIN itself moving, unlike a committed flat copy
  someone has to remember to re-stage.
- 4 import sites under `holdings/` name `import enforce` (`snapshot.py:43`,
  `test_entry_guarded.py:38`, `test_snapshot.py:28`, `test_w1_s16_advisor_firm_bound.py:36`); NONE
  changed -- the BINDING moved (the manifest), never the statement, exactly as the other six
  routes already do (cite `ops/status.py:58`).
- `holdings/tests/test_w1_s16_advisor_firm_bound.py` updated: it used to deliberately EXCLUDE
  `_authz` from its own `sys.path` so it would load ONLY the (now-deleted) local committed copy;
  it now includes `_authz` (matching `test_snapshot.py`/`test_entry_guarded.py`'s own convention)
  and its docstring states the fold plainly.
- Suites: `_authz/tests/` 141 of 141 passed; `holdings/tests/` 35 of 35 passed; run together in
  one pytest session, 176 of 176 passed (no cross-module import collision between the two).

## Arm (c) -- the census, the acceptance instrument

`os.walk` over `infra/aws/lambda/investor-reporting/`: **7** `entry.py` files (directory, export,
holdings, narrative, ops, performance, ycharts/generate). Local `enforce.py` copies outside
`_authz/`: **0**. Every one of the 7 functions' `enforce.py` member resolves, at build time via
`staged_from`, to blob `79c9d9dee1` (the current, fixed `_authz/enforce.py`) -- **7 of 7**.

**The mutant.** A partial-grant fixture (an advisor granted 3 accounts; the directory holds 2 of
them, the third is a validly-shaped issued id simply `NOT-IN-DIRECTORY` -- a gap reason the fork's
refusal branch does NOT catch, so it proceeds to SERVE): the REAL holdings composition
(`snapshot.make_holdings_enforcer`, resolving `enforce` post-fold to the shared, fixed module)
reads `unprojected_grant.count == 1` (`> 0`, disclosed). The PRE-FOLD FORK, loaded from its own
historical blob `8f849457be` in a fresh subprocess (never written back into the tree) with the
SAME fixture, reads `unprojected_grant.count == 0` -- the false negative DEMONSTRATED: the fork's
`serve()` never populates the `unprojected_grant` key at all, so `_authz/served.py`'s own
present-at-zero default masks the real gap.

## Arm (d) -- the halves, read at HEAD (SECOND PASS)

`git ls-tree -r HEAD` on both `org/tier1_exec/2.0.0_SA_COO~B/deliverables/` and
`org/tier1_exec/1.0.0_SA_CTO/deliverables/` now finds **2 of 2** halves committed:
`NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-8_HOLDINGS_FOLD.md` (@6b35db034a) and
`NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-8_HOLDINGS_FOLD.md` (@d81cccbfe3). Both name the
packet's blob `565317d98ac2864e185533bd437e3fad756b380b` (`git rev-parse HEAD:<packet path>`
re-derived this pass matches). PRESENT -- arm (d) PASSES, arm (e) proceeds.

## Arm (e) -- the deploy and the live proof (SECOND PASS)

**The pre-build binding condition, exercised at the real deploy event (not repeatable inside the
battery, since it inherently observes a PRE-deploy state):** `irpt-holdings`' live `CodeSha256`
was re-read immediately before the build and matched the packet's recorded value
`oVv1pYw56N22WLxKUukuyqQBrhAIWXHzhK1vGDlMbKs=` exactly -- no writer had moved the served bytes
since the packet was signed, so the act proceeded per both halves' condition.

**The deploy.** Change-management ledger `ibrtf8-holdings-enforcer-fold` OPENED (commit
`360cce1255`) with two legs (`irpt-holdings` tf-lambda; `L2` verify), sentinel committed before the
act. `infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-holdings` (the single-function
mode; materializes `enforce.py`/`served.py`/`loaders.py`/`ids.py`/`data/custodian_key_seam.json`
from their `staged_from` pins, each sha256-verified) built SHA256
`78XvypHOpeybejwKd5KLCwNcgat2jbQr6O3PhdwaFSU=` and uploaded it, VERIFIED (size+content-sha256
metadata match). `.tools/terraform.exe init` + `plan` (from `infra/aws/terraform/investor-
reporting/holdings/`, the vendored binary, never a PATH substitute) showed `0 to add, 1 to change,
0 to destroy` (only `module.irpt_holdings.aws_lambda_function.this`, `source_code_hash` moving);
applied via `.tools/safe-apply.sh apply` (HALT-GATE reviewed: 25 pending fabric messages, none a
`[STOP]` to this order or its issuer, `HALT_ACK=1`). Post-apply: served `CodeSha256` ==
`78XvypHOpeybejwKd5KLCwNcgat2jbQr6O3PhdwaFSU=` == built; a second `terraform plan
-detailed-exitcode` read rc=0, `No changes` (the 0-diff replan). Ledger CLOSED (commit
`bcd772f7c9`) with both legs' proof. Per this order's BOUND 2, `lambda-source-map.json`'s
`functions.irpt-holdings.artifact_sha256` field is left EXACTLY AS FOUND
(`Bn7iLO/E/9CKYP0sz0YdneloZLHdldHkr/c3jWc25Xc=`) -- `build-and-upload.sh` writes that field as a
side effect of a normal build, and the battery reverts it to the HEAD-committed bytes every run
(verified: `git hash-object` on the reverted file == `git rev-parse HEAD:<path>`, both
`a67974d7cd235b044f74c98ddd39f9e3a2f33cdd`); its staleness relative to the live served value is row
`IRPT_BCKEND-W1-S31` (the CTO's to reconcile), not moved by this act. The battery's own
`arm_e_deploy_state_check` re-derives a fresh build every run and accepts the served bytes as
EXPLAINED when they equal either the packet-time value (not yet deployed) or this run's own fresh
build (the fold's deploy has landed) -- a third, unexplained value would STOP the arm.

**The live proof, against the REAL deployed bytes.** `holdings/entry.py`'s own wiring supplies
`_no_grant` by a DIFFERENT cell's (IB-rt-7's) deliberate decision, named in its own docstring as
"that cell's decision, not this order's" -- out of this order's BOUNDS to rewire. So the live proof
exercises the REAL production composition `snapshot.make_holdings_enforcer` directly with the REAL
`_authz.loaders` triple (S3-backed, real production ownership data for 49financial) instead of a
synthetic fixture -- the same real advisor `abby_horton` rtf-2/rte-6 already used on the other six
routes, never a copy of the subject (bound 12). Fresh this run: `abby_horton`/49financial SERVED,
`k=21` permitted accounts, `unprojected_grant={count:12, denominator:33, kinds:{UNPROJECTED-ID:12}}`
(`k+count==denominator`, self-consistent); the cross-firm swap (an advisor id 49financial's map does
not hold) REFUSED `EMPTY_GRANT`; the pre-fold fork (blob `8f849457be`, loaded fresh via `git show`
into a throwaway module, never written back to the tree) on the SAME real request REFUSED WHOLE
`UNPROJECTED_GRANT` -- read as `count=0` (the false negative: the fork's `serve()` never populates
`unprojected_grant`, so a caller downstream sees the present-at-zero default) -- the exact
load-bearing behaviour change both never-widen halves signed: an advisor with a mix of projected
and unprojected grants went from REFUSED WHOLE to SERVED-WITH-DISCLOSURE; inflection and cottonwood
(empty ownership maps at this vintage) both REFUSED `EMPTY_GRANT` on the empty branch. `R65-AC1`
PASSES on this pass: every arm (a)-(e) holds and `IBR65-HOLDINGS-ENFORCER-FOLDED-AND-GAP-REPORTED`
prints.

## Surprise filed this pass

`IRPT_BCKEND-W1-S32` (OBSERVATION, INERT): `holdings/stage.py --check` reports a raw-byte drift on
`contracts/HoldingsSnapshot.schema.json` (a stage.py MEMBER wholly outside this order's BOUNDS --
not `enforce.py`, not a holdings import, not a test, not the manifest entry) purely because this
override worktree's `core.autocrlf=true` checks the LF-committed blob out as CRLF; `git
hash-object` on the worktree file equals the pinned blob's own hash
(`9ec70af2ba0c71ea589dab48bd14407e111694a8` both), so BY CONTENT there is no drift, and the
downstream reader (`pathlib.Path.read_text()`, universal-newline text mode) normalizes CRLF back
to LF at read time regardless, so this is functionally inert. Not fixed (out of BOUNDS; a
different worktree's checkout settings, not this fold's code).
