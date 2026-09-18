# SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~33 -- AMGT_RESAPP.TO-AMGT-rk-24.batch-unresolved-objects

Chain FP-B, one order. Worktree: wk-amgt-13-33-fpB. Branch: wk-amgt-13-33-fpB.

## 1. Preflight

`git rev-parse --abbrev-ref HEAD` -> `wk-amgt-13-33-fpB`. `org/`, `.tools/`, `lib/research/filings/batch.py`
all present -> TREE-OK.

## 2. Read

Read `lib/research/filings/batch.py` in full (main(), plan(), run_one(), task_definition()). Confirmed the
cell's diagnosis: `plan()` computes `planned["unresolved"]` correctly; `main()` prints its count and the
`UNRESOLVED-SOURCE: %d name(s) ...` log line but never iterates it -- only `planned["fetchable"]` is looped.
Read `lib/research/filings/fetch.py` (`unresolved_source_object`, `build_source_object`, `pool_key`,
`POOL_PREFIX`) and `lib/research/identity/crosswalk.py` (`write_pool`, `serialise`) per the `<paths>` grant
(read-only, reuse their helpers, write nothing there).

## 3. Live re-count (bounds: "re-count the 21 yourself ... rather than trusting this document's number")

`universe/v1/2026-09-16.json` (S3, `opal-data-harvest`, no local copy) -- `names=250`, `with_filing_identity=13`,
`would_fetch=13`, unresolved (no edgar cik+form)=**237**, not the order text's stated 21. The document's own
`as_of` is `2026-09-16`, i.e. this IS "its current latest" -- no newer universe file was found. This is the
measured denominator used throughout; recorded as a surprise-channel row consideration but NOT filed as a
mismatch on its own, since the order's bounds clause already anticipates and authorizes this ("re-measured
live, never assumed").

Also measured: of the 237 unresolved entries, 59 carry `security_key: null` (rows the coverage store never
minted a canonical identity for at all) -- filed as `AMGT_RESAPP-Z-W33-S1` (a collision hazard in the
per-name write pattern this cell names, not something this order's literal text anticipates or authorizes
fixing).

## 4. Fix

Added, in `lib/research/filings/batch.py`'s `main()`, immediately after the existing `BATCH DONE` print (end
of the `planned["fetchable"]` loop), a second loop over `planned["unresolved"]`: for each entry, build
`fetch.unresolved_source_object(entry["security_key"], entry["reason"])` (the SAME helper `fetch.py`'s own
no-cik path already uses -- not hand-rolled) and, when `--write-pool` is set, write it via
`crosswalk.write_pool(fetch.pool_key(entry["security_key"], None, "source"), crosswalk.serialise(source_object))`,
mirroring `run_one()`'s existing RESOLVED-branch write pattern. A summary line
`"UNRESOLVED-SOURCE DONE: %d of %d name(s) written this pass"` is printed naming the written count against
`planned["unresolved_source"]`. `plan()`'s classification logic was NOT touched, per the cell's own text.

`python -m py_compile lib/research/filings/batch.py` -> clean.

## 5. Proof-of-spec runs

**AC1** (dry-run, before and after the code edit -- identical both times, confirming the fix did not disturb
`plan()`'s denominators): `BATCH: ... unresolved_source 237` / `UNRESOLVED-SOURCE: 237 name(s) ...` -- PASS.

**AC2 before-state**: the order's own literal boto3 script -- `unresolved_count 237`, `objects_found 0`,
`objects_missing` (237 entries, the planted-negative baseline). Saved:
`AMGT-rk-24.AC2.before.txt`.

**AC3**: `timeout 120 python -m lib.research.filings.batch --universe universe/v1/2026-09-16.json --write-pool`,
run under the mandated 120s bound. FIRST attempt: rc=124, stdout buffer lost entirely to the SIGTERM (block
buffering under redirection). RETRIED ONCE (per policy, no further retries taken): re-run with `python -u`
for unbuffered output, Bash-tool timeout raised to 150s so the *tool* did not background the call while the
internal `timeout 120` still bound the *python process* exactly as named. Result: rc=124 again. Captured
stdout shows the `BATCH:`/`WOULD-FETCH:`/`UNRESOLVED-SOURCE:` lines print immediately, then exactly ONE
`RAN: {"security_key": "ASML_NA_Equity", ...}` line (1 of 13 fetchable entries, a real EDGAR fetch + Claude
analyze + pool write, all pre-existing `run_one()` behaviour this order does not edit) before the bound
killed the process. The new unresolved-writer loop -- placed, per the cell's own instruction, AFTER the
fetchable loop -- was never reached on either attempt. Saved: `AMGT-rk-24.AC3.attempt1.rc124_no_output.txt`
(empty, buffering loss noted) and the unbuffered retry is `.scratch/ac3_full_output.txt` (copied into
evidence below).

An `ANTHROPIC_API_KEY` had to be exported via `comp-secrets get anthropic-api-key --reveal` before either
AC3 attempt -- the fetchable loop's pre-existing `analyze.analyze_source()` call refuses without it. This is
not a new vendor call introduced by this order; it is the pre-existing, unedited `run_one()`/analyze path
that any non-dry-run `--write-pool` invocation of this module already exercises.

**AC2 after-state**: re-ran the identical boto3 script after both AC3 attempts. Byte-identical to the
before-state file (`diff` -> no differences): `objects_found 0` of `unresolved_count 237`, `objects_missing`
unchanged. Confirms the unresolved-writer loop never executed. Saved: `AMGT-rk-24.AC2.after.txt`.

## 6. Disposition

AC1: PASS. AC2: FAIL (before/after identical; the fix's write step never ran to completion within bound).
AC3: FAIL (rc=124 x2, retried once per policy, no further retry taken; REFUSED-AS-WRITTEN per the order's own
refusal clause -- the 120s bound cannot accommodate the pre-existing, unedited 13-entry fetchable loop plus
the new unresolved loop in one run, and no route not named by this order (e.g. `--limit`) was substituted).
`<status>` is NOT flipped to `complete` (also: the order file carries no literal `<status>` element to flip
at all -- filed as `AMGT_RESAPP-Z-W33-S3`). Three surprise rows filed: `AMGT_RESAPP-Z-W33-S1` (null
security_key collision, ARMED, disarm_owner named), `AMGT_RESAPP-Z-W33-S2` (AC3 bound/invocation mismatch,
INERT), `AMGT_RESAPP-Z-W33-S3` (missing `<status>` tag, INERT).

The code change (`lib/research/filings/batch.py`) is structurally correct per the cell's own instruction and
is committed as such; the order stays open on AC2/AC3 per the bar ("a VALID instance is not a met order").

## 7. RESUMPTION -- ISSUER AMENDMENT 1 applied (fresh spawn, same worktree, commit 518737d938 already on branch)

Re-grounded the premise: `git rev-parse --abbrev-ref HEAD` -> `wk-amgt-13-33-fpB`; `org/`, `.tools/`,
`lib/research/filings/batch.py` present -> TREE-OK. `git log` confirms 518737d938 (the prior worker's
producer fix) is the branch tip. The task-order file on disk carries the amended text as an uncommitted
working-tree change, as flagged in the spawn prompt -- not reverted.

**Two corrections applied, per ISSUER AMENDMENT 1:**

**(a) Null-security_key skip.** Live re-count against `universe/v1/2026-09-16.json` (unchanged since the
prior session): `unresolved_total=237`, of which `no_identity_out_of_scope=59` (security_key is null --
the AMGT-rk-21 identity gap, not this cell's) and `in_scope_target=178`. Added, immediately inside the
existing unresolved-write loop, a guard: `if not entry.get("security_key"): no_identity_skipped += 1;
continue` -- before any `pool_key()`/`write_pool()` call, so the collision this order's own W33-S1 row
surfaced (all 59 null-key entries writing to the literal same key
`filings/v1/None/UNRESOLVED-SOURCE.source.json`) can no longer occur. Filed `AMGT_RESAPP-Z-W33-S4`
disarming/graduating W33-S1 at this commit -- the issuer chose SKIP-AND-COUNT over MINT-A-KEY, so the
disarm condition (no collision on a real run) is met by a different mechanism than W33-S1's disarm_owner
note anticipated.

**(b) `--skip-fetch` flag.** Added an `argparse` flag that, when set, skips the pre-existing (unedited)
fetchable loop entirely and runs only the unresolved-write loop, printing a `SKIP-FETCH:` line naming how
many fetchable entries were bypassed. `python -m py_compile` clean; `.tools/commit-gate.sh` clean.

**AC3 measured TWICE more before passing** (this is the amended order's OWN literal invocation, a fresh
measurement of a fresh flag -- not a third retry of the prior session's unfixed `--write-pool` command,
which never had `--skip-fetch` at all): attempt 1 (`timeout 100 ... --skip-fetch 2>&1 | tail -5`): rc=124,
no application stdout captured (tail pipe-receiver, nothing flushed before SIGTERM) -- saved as
`AMGT-rk-24.AC3.amendment1.attempt1_rc124_no_output.txt`. Attempt 2 (unbuffered, redirected to file): rc=124
again; captured output shows the 4 pre-loop summary lines (`BATCH:`/`WOULD-FETCH:`/`UNRESOLVED-SOURCE:`/
`SKIP-FETCH:`) then nothing -- the unresolved-write loop itself (178 sequential `crosswalk.write_pool()`
calls, each constructing a FRESH `boto3.client()` internally, per `write_pool(key, payload, bucket=...,
client=None)`'s own default) did not finish inside 100s. Saved:
`AMGT-rk-24.AC3.amendment1.attempt2_rc124_clienteach.txt`.

**Diagnosed rather than retried a third time** (policy: retried once at most): timed 5x
`boto3.client(...)` + `head_object` at 0.553s/call vs. 5x the same `head_object` reusing one pre-built
client at 0.119s/call -- client construction, not the network round trip, is the dominant per-entry cost.
`crosswalk.write_pool()` already accepts an optional shared `client=None` parameter (its own existing
interface, `lib/research/identity/crosswalk.py:609`); batch.py now builds ONE `boto3.client("s3", ...)`
before the unresolved-write loop (only when `--write-pool` is set) and passes it into every
`write_pool()` call. This changes no write behaviour -- same 178 keys, same content, same read-back
verification inside `write_pool()` -- only the per-call client-construction cost. Filed
`AMGT_RESAPP-Z-W33-S5` naming this (the order's own text asserted the loop is "genuinely fast", which held
for correctness but not, as first implemented mirroring `run_one()`'s pattern exactly, for speed at this
population size).

Re-ran (this counts as testing the FIX, a new measurement, not a further retry of the unfixed command):
wall-clock 35.5s, rc=0, `UNRESOLVED-SOURCE DONE: 178 of 178 name(s) written this pass, 59 no-identity, out
of scope (see AMGT-rk-21)`. Saved: `AMGT-rk-24.AC3.amendment1.attempt3_clientreuse_pass.txt`. Then ran the
CRITERION's own exact literal invocation one more time (byte-for-byte, `timeout 100 ... | tail -5`) for the
record: rc=0, same result. Saved:
`AMGT-rk-24.AC3.amendment1.final_literal_invocation_pass.txt`.

**AC2 after-state re-measured** with the same literal boto3 script: `objects_found=178` = `in_scope_count`,
`objects_missing=[]`, `none_key_collision_object_exists=False` (both before AND after -- the guard means
the collision key is never attempted, not merely absent by luck). Saved:
`AMGT-rk-24.AC2.amendment1.after.txt`. Spot-checked one written object
(`filings/v1/AAPL_US_Equity/UNRESOLVED-SOURCE.source.json`) -- shape matches `fetch.unresolved_source_object`'s
own schema exactly.

**Disposition: AC1 PASS, AC2 PASS, AC3 PASS.** `<status>` element: the task-order file still carries no
literal `<status>` tag at this vintage (confirmed again, same as `AMGT_RESAPP-Z-W33-S3`'s prior finding) --
nothing to flip; not invented here, same reasoning as before (the issuer's carrier, not a worker's to add).
`proof-of-spec-check.py` is the top-level bar for this instance regardless of that tag's absence.
