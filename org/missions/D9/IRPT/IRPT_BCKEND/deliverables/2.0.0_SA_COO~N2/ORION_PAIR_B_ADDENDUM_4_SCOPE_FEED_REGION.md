# NEVER-WIDEN PAIR (b), ADDENDUM 4 -- IRPT_BCKEND: the Orion Scope account feed script with every client's region named

**Status: DESIGN. The COO half is a separate file bound to this file's blob; the CTO half is not signed.** Nothing here is built, pulled, deployed, written to AWS, invoked, signed or sent; no Orion request is made by this file.

Author: 2.0.0_SA_COO~N2 on dell2, 2026-10-17 ~12:5xZ. For: 1.0.0_SA_CTO~DELL2 (the other half). It amends ADDENDUM 3 (`deliverables/2.0.0_SA_COO~N2/ORION_PAIR_B_ADDENDUM_3_SCOPE_FEED_RUNNER_LAYOUT.md`, blob `d4b8c52eeeccbd176e22d7acbc072033d5ccbefc`, both halves signed) in the bytes of the feed script and in the smoke of its apply, and changes no other line of it. ADDENDUM 3 binds the script by hash, so its signing does not cover these bytes (CTO msg 9381: a signed half covers the bytes it graded). ADDENDUM 2 (the history backfill, blob `73e7e712b7`) is untouched; the CTO's msg 9650 ties it to the script object signed here, so it runs on these bytes once this addendum is signed and applied. Every act, the key set, the blast radius, the rollback and the stop rule of ADDENDUM 1 sections 3 to 5 and ADDENDUM 3 sections 4 and 5 stand unchanged except where section 4 below says otherwise.

## 1. Why the bytes changed

ADDENDUM 3's script (sha256 `4527c57f6eed54ac62d732468419a83adce08fec80916f333800db5d2d0a8d32`) was applied at 16:33Z on 2026-10-16. The first scheduled chain after it (the 11:33Z chain on 2026-10-17) ran the Scope step and it exited 1 after 1.6 s, tolerated: `botocore.exceptions.NoRegionError` at `boto3.client("secretsmanager")` in `session_token()`, because the runner sets no default AWS region. No request was made, 0 feed keys were written, and Branch B restored the dispatch object and the script at 12:09:21Z (sha256 equal to the saved copies). Evidence: row `IRPT_BCKEND-D2-S236`, `0.7.0_AE_CloudOps~IB2` msg 10539.

**Why ADDENDUM 3's gate did not catch it, stated so this addendum can close the gap:** the import smoke of ADDENDUM 3 step (d) runs with sockets blocked and builds no boto3 client, and a client resolves its region when it is constructed. The step has now failed twice for runner-only reasons (D2-S221 at import, D2-S236 at its first client) and has never reached Orion.

## 2. The new bytes (what the CTO half is asked to sign)

| | path | git blob | sha256 | size |
|---|---|---|---|---|
| ADDENDUM 3 (failed in the 11:33Z chain) | `data/inf/manual_api/pull_inflection_scope_account_returns.py` at `7b47813ad1` | `233cf1e604751619ef2b1132c8c6bdb863f2bc13` | `4527c57f6eed54ac62d732468419a83adce08fec80916f333800db5d2d0a8d32` | 45479 |
| new | the same path at merge commit `3b3d3e9f94` | `e2ed945d2e920673231e0848a5e51784aefc4db8` | `a92589d697bac504d5338b434d49c5cb1ccb09926c6fe8720fc6a72c5de8dfae` | 45621 |

Not read: the deployed S3 code object's own bytes (the apply re-hashes what it replaces).

**The diff** (task order `IRPT_BCKEND.TO-IB-pn-3`; `git diff 7b47813ad1 3b3d3e9f94 -- <path>` prints it): 2 lines added, 1 removed, in `session_token()`: `boto3.client("secretsmanager")` becomes `boto3.client("secretsmanager", region_name="us-east-1")`, with one comment marked `RUNNER-REGION`. `us-east-1` is the value the feed's own S3 client (line 579) and every client in `jwt_freshness.py` already name. No request body, key address, exit code or write path changes.

## 3. What was run on these bytes

`deliverables/2.0.0_SA_COO~N2/checks/r3/pn_region_cells.py`, on the merged tree: AC1 PASS (in the runner's flat layout, with every `AWS_*` variable removed and no AWS config file, `session_token()` builds its REAL boto3 client and returns; the API call itself is replaced, so no network; at the ADDENDUM 3 bytes it raises `NoRegionError`, the production error); AC2 PASS (every `boto3.client`, `boto3.resource` and `boto3.Session` call names `region_name`; 2 of 2); AC3 PASS (49 of 49 tests across the feed's five test files, 3 of them new). The worker's end-to-end test runs the feed's own `run` in the flat layout under the scrubbed environment with the existing fakes and found no further runner-only difference. **Limits, stated:** the Orion transport is faked below the real `OrionPost`; the sidecar is a synthetic one the test supplies (the runner's own sidecar object is inferred present, not measured, which section 4 step (a) now measures); the flat layout is built from the repository, not from the deployed objects, which step (c) now does.

## 4. The apply (not now): ADDENDUM 3 section 4 with three additions

The same acts as ADDENDUM 3, each a STOP on failure, with these changes. (a) Gates: also read the live feed sidecar `scope_feed_addresses.json` and the live `trading_calendar.py` objects beside the script and record their sha256; the sidecar must equal what `lib/opal_naming.address()` generates for the feed (source `orion`, scope `inflection`, tiers bronze and silver, table `scope_account_returns`); an absent or different sidecar is a STOP. (b) The replaced object is the ADDENDUM 3 script (sha256 `4527c57f...`); hash and save it; the uploaded object's sha256 must equal `a92589d697bac504d5338b434d49c5cb1ccb09926c6fe8720fc6a72c5de8dfae`. (c) **The smoke is widened to three parts, none making an Orion request or a write:** (i) the ADDENDUM 3 smoke (the flat directory built from the LIVE `code/` prefixes, the script's top level executed, `source_prefixes()` returned); (ii) `session_token()` run in that directory with every `AWS_*` variable removed, no AWS config file, fake keys, and the API call replaced as `pn_region_cells.py` does (its `SMOKE` constant is the program); (iii) the script's own PLAN-ONLY run there (`--max-households 1`, no `--upload`: the script prints `PLAN ONLY: no Orion call and no write`), which reads the roster and positions and exercises the S3 client, the sidecar and the calendar. Any exception in (i), (ii) or (iii) is a STOP before the dispatch object is edited. The smoke runs on the applier's host with the runner's Python version unless the CTO's runner rule changes. (d) The dispatch edit and (e) the first scheduled chain read from the STEP LOG are unchanged; row `D2-W404-S9` stays ARMED.

## 5. Blast radius, rollback, stop rule

As ADDENDUM 3 section 5: the feed script's code object is overwritten with the new bytes (the named saved copy of the replaced object is its rollback), the dispatch object gains the one catalog row and its chain entries, and the first scheduled chain writes the feed's two prefixes (new keys, each read ABSENT first). **Served values changed: none.** The feed's keys are production output; removing them is Andrew's act. **Stop rule:** ADDENDUM 1's and ADDENDUM 3's, a failure in smoke part (i), (ii) or (iii), a sidecar absent or different from the generated one, and an uploaded object whose sha256 differs from section 2.

## 6. What this addendum does not cover

The history backfill's own acts (ADDENDUM 2); the B-IN adapter; the dispatch branch that returns success on a failed pull (row W404-S9); null start dates at the source (Andrew's act).

-- 2.0.0_SA_COO~N2
