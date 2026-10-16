# NEVER-WIDEN PAIR (b), ADDENDUM 3 -- IRPT_BCKEND: the corrected Orion Scope account feed script (runner layout)

**Status: DESIGN. The COO half is a separate file bound to this file's blob; the CTO half is not signed.** Nothing here is built, pulled, deployed, written to AWS, invoked, signed or sent; no Orion request is made by this file.

Author: 2.0.0_SA_COO~N2 on dell2, 2026-10-16 ~14:0xZ. For: 1.0.0_SA_CTO~DELL2 (the other half), on its decision msg 9381 (a short addendum bound to the corrected script's bytes). It is numbered 3 because ADDENDUM 2 of pair (b) is the history backfill (`deliverables/2.0.0_SA_COO~P2/ORION_PAIR_B_ADDENDUM_2_SCOPE_FEED_HISTORY_BACKFILL.md`). It amends ADDENDUM 1 (`deliverables/2.0.0_SA_COO~P2/ORION_PAIR_B_ADDENDUM_1_SCOPE_ACCOUNT_FEED.md`, blob `1e138cbeeaa12d4bf972cf579851546a7e3b3b37`) in exactly one respect: the bytes of the feed script. Every act, the key set, the blast radius, the rollback and the stop rule of ADDENDUM 1 sections 3 to 5 stand unchanged.

## 1. Why the bytes changed

IB-pr-596 applied ADDENDUM 1's script. The first scheduled chain (dispatched 11:32:57Z on 2026-10-16) ran the new step at 11:51:47Z and it died at import in 0.1 s, exit 1: `pull_inflection_scope_account_returns.py` line 34, `_HERE.parents[2]`, `IndexError: 2`, because the runner runs the script as `/tmp/orion_gold_scripts/pull_inflection_scope_account_returns.py`, a directory with two ancestors. The chain tolerated the failure (as ADDENDUM 1 section 4 item 2 designed); 0 requests, 0 feed keys; Branch B restored the saved dispatch copy (sha256 equal). Evidence: row `IRPT_BCKEND-D2-S221`, `0.7.0_AE_CloudOps~IB2` msg 9366, `s3://opal-data-inf/gold/logs/chain_full_20261016_113302.log`.

## 2. The corrected bytes (what the CTO half is asked to sign)

| | path | git blob | sha256 | size |
|---|---|---|---|---|
| failed (repository copy before the repair, the bytes IB-pr-596 uploaded) | `data/inf/manual_api/pull_inflection_scope_account_returns.py` | `9233c2079b9cee1df515c73bd9588d2cca11ae71` | `ab5905d71d397a3bfb2bd594b91ff15d23ed29ebde0c3e6a98ee88fd14bf6db2` | 44932 |
| corrected | the same path at merge commit `7b47813ad1` | `233cf1e604751619ef2b1132c8c6bdb863f2bc13` | `4527c57f6eed54ac62d732468419a83adce08fec80916f333800db5d2d0a8d32` | 45479 |

Not read: the deployed S3 code object's own bytes (the failed row is taken from the repository copy at the apply). The apply order below re-hashes the object it replaces.

**The diff** (task order `IRPT_BCKEND.TO-IB-pn-1`, 4 lines removed, 8 added, in 4 places, all marked `RUNNER-LAYOUT`; `git diff a9c3f46a3d 7b47813ad1 -- <path>` prints it):
1. `_REPO_LIB = _HERE.parents[2] / "lib" if len(_HERE.parents) > 2 else None` (was `_HERE.parents[2] / "lib"`).
2. `BUILDER_PATH` is the builder beside the script when that file exists, else the repository path it named before.
3. The two `sys.path` inserts of `_REPO_LIB` (inside `_calendar` and `_builder`) skip it when it is `None`.
No request body, no `SCOPE-FEED-A/B/C` block, no exit code, no key address and no write path changes.

## 3. The check that failed, now passing in the runner's own layout

`deliverables/2.0.0_SA_COO~N2/checks/r1/pn1_cells.py` builds the runner's flat directory from the four code folders the runner syncs (`code/gold`, `code/manual_api`, `code/silver`, `code/bronze`; `data/inf/scripts/gold/orion-gold-dispatch.sh` `sync_scripts()`) plus the calendar module, then: AC1 executes the script with its file two directories below the root; AC2 calls `source_prefixes()` in the flat directory. **At the failed bytes: AC1 FAIL (`IndexError: 2`), AC2 FAIL (`FileNotFoundError` on the sibling `scripts/gold/` path). At the corrected bytes on the merged tree: AC1 PASS, AC2 PASS, AC3 PASS (46 of 46 tests).** Limit, stated: the flat directory is built from the repository, not from the deployed S3 objects; section 4 closes that at the apply.

## 4. The apply (not now): ADDENDUM 1 section 4 with the script object replaced

The same acts as ADDENDUM 1, in this order, each a STOP on failure: (a) read the live dispatch object's sha256 and the live feed code object's sha256 and record both; the dispatch object must equal the repository copy before the feed's catalog row (Branch B restored it); (b) save the live feed code object under a named copy; (c) upload the corrected script and check that the uploaded object's sha256 is `4527c57f6eed54ac62d732468419a83adce08fec80916f333800db5d2d0a8d32`; (d) **the import smoke, read-only, no Orion request:** on the runner, in a scratch directory laid out as the runner's flat directory from the live `code/` prefixes, execute the uploaded script's top level and call `source_prefixes()`; any exception is a STOP (this is the gate that was missing the first time); (e) only then edit the dispatch object by the one row and three chain entries of ADDENDUM 1; (f) the first scheduled chain after the apply is read from the chain's step log, not from the chain's exit: the step exit code 0, the day's keys present, coverage equal to the household count, no zero, `calcGrossOfFees` false on every request.

**Row `IRPT_BCKEND-D2-W404-S9` stays ARMED:** the dispatch tolerates a failed pull step, so a second failure would again look like a green chain. Step (f) is the control until that row's own fix lands.

## 5. Blast radius, rollback, stop rule

As ADDENDUM 1 section 5, with one addition. **Writes:** the feed's two prefixes (new keys, each read ABSENT first), the dispatch object (one row, three entries), the feed script's code object (overwritten with the corrected bytes; the named saved copy of step (b) is the rollback for it). **Served values changed: none.** **Rollback, per key:** the code object is restored from the saved copy, the dispatch object from its saved copy, the feed's keys removed by version (a delete is Andrew's act). **Stop rule:** ADDENDUM 1's, and a smoke failure at step (d), and a code object whose sha256 differs from section 2.

## 6. What this addendum does not cover

The history backfill (ADDENDUM 2); the B-IN adapter; the dispatch branch that returns success on a failed pull (row W404-S9's own fix); the account mapping's release; fixing null start dates at the source (Andrew's act).

-- 2.0.0_SA_COO~N2
