# ADVI_COTBKF.TO-CB-ao-1 -- deploy the cot gold `_ff_worker` carry-forward stamp

**archetype:** DEPLOY

**Seat:** `0.7.0_AE_CloudOps~CB2` | **Issuer:** `2.0.0_SA_COO~C2` | **Round:** 41 | **Cell:** `CB-ao-1`
**Risk class:** SERVED | **Date:** 2026-10-09 | **Order at:** @7179ea76bd (AMENDMENT 1, RELEASED)
**Criterion:** `CB41ao1-AC1` -- **PASS** | **Proof:** VALID (rc=0)
**Ledger:** `.../20261009T1413Z_advi-cotbkf-ff-worker-deploy-cb-ao-1-20261009_deploy_completion.md`,
opened @7ba4bf0ecf, 4 legs, CLOSED all proven.

---

## What this closes

This is the hazard **this seat surfaced** at CB-aj-2's gate C2 and the CTO sent to COTBKF's enrichment
list as its own cell. `_ff_worker` in the cot gold chain carried prior-day prices forward with **no claim
field** -- it logged only above 10% fallback, so a small carry was silent, and after the 49F rewrite it
would have re-injected the removed bond prices on exactly the three CUSIPs that rewrite existed to clean.

Round 39 fixed it: every carried price now carries `price_basis`, `price_source_date` and `source_firm`,
and a price whose `source_firm` is present and not Cottonwood is **never carried**. This order deployed
that fix to the bytes the gold run actually syncs.

**One key, one new version.** `s3://opal-data-cot/code/gold/B_00.canonical_holdings.py`:
`BMqu7SNCbx2f3bQ_Tr56xMBCvtMe3van` (65,249 B, sha `6dbf6a86...`) -> `hU7ZrZTD5NDlVvuSo9aBMUd1hKUg_lAe`
(67,281 B, sha `45fbbd92...d74c08d`), written 14:19:29Z. **Prior version kept; nothing deleted.**

## The census, and two stated figures that were wrong

The baseline was **proven, not inherited**: the deployed object was fetched *at its prior VersionId* and
hashes `6dbf6a86...`, exactly the pair's value, and is byte-identical to `git show 88e7452955~1` -- the
half's own claim that the served bytes equal the repo file before round 39. The repo HEAD file is
byte-identical to `a46b8507d7`, round 39's content commit, so **nothing touched the file after round 39**
and the deploy carried no rider.

The diff: **added 26, removed 1**, 2 hunks. Every changed line is inside `_ff_worker` -- added lines at
HEAD 1358-1403 and the single deleted line at HEAD position 1358, against a function running 1339-1424
measured by indentation.

Two figures in the paperwork are off. Both benign, both recorded rather than smoothed over:

1. **"+25/-1" is really +26/-1.** The order and the COO half say +25/-1 and the CTO half signs "exactly
   round 39's +25/-1". Git's own `numstat` for the round-39 commit on this file reads `26 1`, matching my
   diff. A one-line transcription slip. It does not weaken the sign-off: the substantive claim -- the
   deploy moves exactly round 39's change inside `_ff_worker` and nothing else -- is true and verified
   byte-for-byte in both directions. Worth noting that a naive `grep -c '^+'` reads **27**, because it
   counts the `+++` header; that is how an off-by-one enters a census.
2. **The order's `_ff_worker` range is narrow.** Step 3 glosses it as "lines 1339-1395 at HEAD", but the
   function runs to 1424 and the changed lines reach 1403. Read against that parenthetical the census
   would STOP. The **binding** condition is the CTO half's, and it carries no line range at all -- "any
   line outside `_ff_worker` means STOP" -- so the signed gate is satisfied on its own terms with no
   interpretation. The two wordings agree on the subject; only the order's gloss is stale. Nothing was
   adjudicated.

## The write

The key list was printed **before** the write and **asked of the tool**, not hand-built:
`safe_deploy_core.upload_plan()` -- the same function the deploy loop and the deployed-layout check read
-- returned **exactly one** entry, the granted key. A reconstruction could have disagreed with the tool;
this cannot.

Condition 1's version re-read was the **gate**, not a preceding observation: the re-read and the deploy
ran in one invocation with the deploy behind a conditional, so a moved version would have exited before
`safe-deploy.sh` was reached. Live read `BMqu7SNC...` = expected, so the write was authorized.

`safe-deploy.sh` rc 0, `OK: safe-deploy gate PASS -- all 1 file(s) deployed and verified`. Its own
accounting confirms the blast radius: "1 path(s) to deploy (1 script, 0 bundle-member)" with three
declared-for-this-layer files explicitly `[not shipped] ... S3 keeps its served bytes`.

**No bypass.** `--allow-stale` was not passed and this run wrote no entry to
`org/safe-deploy-bypass-audit.log`. The lane admitted it (`APPLY-WHO ... verdict=ADMITTED`), so the
order's stop-on-refusal branch never fired. Noted and **not leaned on**: APPLY-WHO is WARN-only in this
wrapper by ruling 106858, so ADMITTED is not a gate's pass -- the authority for this seat applying is the
CTO half's condition 2 naming it.

## AC1, and the control that makes it mean something

`python -m pytest data/cot/scripts/gold/tests/test_b00_ff_carry_claim.py -q` -> **3 passed**, rc 0.

Run in a detached scratch worktree at HEAD whose `B_00.canonical_holdings.py` had been overwritten with
the **fetched served bytes** and re-hashed **in place** to `45fbbd92...` before the run -- so the bytes
under test are the bytes S3 serves, verified at the point of use rather than at download. The import path
(CTO condition 3 asks it be printed) is
`C:/dev/wk-cb-ao-1-proof-141930/data/cot/scripts/gold/B_00.canonical_holdings.py`; the test resolves it
itself (`GOLD = dirname(dirname(abspath(__file__)))`, loaded via `spec_from_file_location`).

**A passing test says nothing about which file it read** -- which is the whole point of condition 3. So I
planted a mutant: the first `price_basis` literal in the file under test renamed, nothing else touched.
The suite went to **2 failed, 1 passed, rc 1, `KeyError: 'price_basis'`**. Had the test been reading the
repo copy or an installed module, mutating that file could not have moved the verdict. The served bytes
were then restored, re-hashed to `45fbbd92...`, and the suite re-run clean at 3 passed.

The worktree was removed with `git worktree remove` (no `rm -rf` -- a recursive delete is a
human-confirmed act), and the **shared tree was verified untouched** afterwards: its own copy still
hashes `45fbbd92...` with `git status` empty for that path.

**What this criterion does not cover.** It proves the stamp on a **synthetic** day, which is the only arm
available, because `_ff_worker` is unreachable for cot today (`schwab/silver/rps/` empty, the measurement
I made at CB-aj-2 against a positive control reading 90). The live arm is CTO condition 4 -- the next
scheduled cot gold run read for an unchanged output fingerprint -- which the order assigns to the issuer
and I do not claim.

## Compiler Tools

| tool | invocation | result |
|---|---|---|
| `safe-deploy.sh` | one file, `--author` this seat, no bypass flags | rc 0, gate PASS, 1 path, its own `comp-pipescript deployed` VERIFY OK; APPLY-WHO ADMITTED (WARN-only), CROSSBOX CLEAR |
| `safe_deploy_core.upload_plan()` | imported, called on the one file before the write | exactly one key, the granted one -- the tool's own answer |
| `deploy_ledger.py` | `open` / `close-leg` x4 / `close` | 4 legs before the write; CLOSED all proven; sentinel removed; nothing left staged |
| `proof-of-spec-check.py` | `<instance> CB41ao1-AC1` | INVALID first pass -- I had pinned the ledger row to the *previous* order's commit and git refuted the (commit, path) pair; re-pinned to its real open commit @7ba4bf0ecf -> **VALID (rc=0)** |
| `git worktree` / `diff` | detached worktree at HEAD for the proof, then removed; prior-version bytes vs repo HEAD for the census | census +26/-1 all inside `_ff_worker`; worktree gone, shared tree clean |

**What failed / gaps.** (1) The proof instance was INVALID on first run because I pinned the ledger
artifact to `e5eb80c75f`, the commit from the *previous* order -- the checker caught a (commit, path) pair
git refutes, which is exactly its job. (2) A first attempt at the worktree used `rm -rf` for cleanup and
was correctly denied; I switched to a fresh path plus `git worktree remove`, which is the right tool
anyway. (3) The AC1 expect is the bare word `passed`, which a partial run could also satisfy; the real
bar is 3 of 3 and rc 0, and both hold.

## Push state

MEASURED at write time -- see the final report line; re-measure at read time.
