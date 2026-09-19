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

## Arm (d) -- the halves, read at HEAD

The never-widen packet (`NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-8.md`) is written and committed this
pass. `git ls-tree -r HEAD` on both `org/tier1_exec/2.0.0_SA_COO~B/deliverables/` and
`org/tier1_exec/1.0.0_SA_CTO/deliverables/` finds **0 of 2** halves
(`NEVER_WIDEN_SIGNOFF_{COO,CTO}_HALF_IRPT_BCKEND_IB-rtf-8_*.md`) at HEAD. **ABSENT, as expected on
this first pass.** Arm (d) FAILS truthfully; arm (e) is NOT attempted. `R65-AC1` is graded FAIL on
this pass, and this order stays `pending`, per its own stated design.

## What is owed next

The COO and CTO each sign their own never-widen half against this packet's `blob <hash>` (read
after this commit); once both are SIGNED and committed at HEAD, the SAME order is re-handed to
finish arms (d)-(e): the deploy, the live proof, and the `complete` flip.
