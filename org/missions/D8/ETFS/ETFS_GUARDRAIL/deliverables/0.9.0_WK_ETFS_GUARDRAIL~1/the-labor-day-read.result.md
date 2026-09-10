# EG-s-16 -- THE LABOR DAY READ: criteria verbatim, with rc and denominator

**Worker:** `0.9.0_WK_ETFS_GUARDRAIL~1` · **Branch:** `wk-etfs_guardrail-2-1` · **Face:** the RE-CUT
`ETFS_GUARDRAIL.TO-EG-s-16` @`005667015a` · **Reads:** EG-s-15's run (request id
`9fbc33e0-174c-4c82-b392-2b1dafe4a835`, 01:19:02Z→01:20:28Z) and **fires nothing**

## 0. THE HEADLINE

**FWD-4 holds on real data: the deployed classifier told a real closed-market day apart from a hole, and
this system backfilled nothing against it.**

`2026-09-07` is Labor Day. For **3 of 3** partners taken from the artifact's own list, the class-A count
equals the non-trading-day count this battery **enumerated from the calendar**, `trading_days` equals the
trading count, the date is in **no** partner's holes, and every hole list is identical with the date
removed. The month's only holes are `2026-09-09`, class **D** — so the verdict demonstrably *can* mark a
hole, and did, two days after the target.

**Read-only throughout.** No invocation of `etfs-reports-orchestrator` in any mode. I verified the face
against Andrew's standing constraint myself before starting.

## 1. CRITERIA

| id | status | rc | deciding line |
|---|---|---|---|
| S16-AC1 | **PASS** | 0 | `ARMS 6 of 6 PASS` → `EGS16-LABOR-DAY-CLASS-A` |
| S16-AC2 | **RECORDED (judgment)** | n/a | graded by `3.0.0_SA_CVO` at L9 — **no worker verdict** |

### S16-AC1 — PASS, 6 of 6 arms
`timeout 300 python .../test_egs16_labor_day.py` → rc=0. Re-run **once** against the re-cut arms.

**(a) PASS** — `is_trading_day(2026-09-07)` → **False**; positive control `is_trading_day(2026-09-08)` →
**True**.

**(b) PASS (re-cut on `W1-S30`)** — partners taken **from the artifact**:
`['49financial','cottonwood','inflection']`, 3 of 3 (denominator). The verdict's own window is **derived
from the artifact**, not hand-coded: the six class counts sum to **9** per partner → `2026-09-01..09-09`,
agreeing with `_month_dates` ("an in-progress month runs to yesterday UTC"; the run was 09-10 UTC). The
calendar is then **enumerated by the battery** over those 9 days:

    2026-09-01 Tue True   2026-09-05 Sat FALSE   2026-09-08 Tue True
    2026-09-02 Wed True   2026-09-06 Sun FALSE   2026-09-09 Wed True
    2026-09-03 Thu True   2026-09-07 Mon FALSE  <- Labor Day
    2026-09-04 Fri True
    -> 3 non-trading, 6 trading

| partner | A vs enumerated | trading_days vs enumerated | holes | target in holes |
|---|---|---|---|---|
| 49financial | 3 vs 3 ✓ | 6 vs 6 ✓ | `['2026-09-09']` | False |
| cottonwood | 3 vs 3 ✓ | 6 vs 6 ✓ | `['2026-09-09']` | False |
| inflection | 3 vs 3 ✓ | 6 vs 6 ✓ | `[]` | False |

**The limit, printed in those words:** *"the artifact carries NO per-date classification — the literal
2026-09-07 appears 0 time(s) in the whole 2705-byte document — so this arm proves THE COUNT and THE
ABSENCE, never the per-date label."*

**(c) PASS (re-cut on `W1-S30`)** — `expected_empty` quoted at source and **not graded** as a class-A
instrument: `classifier.py:178 @c866edd324` `expected_empty = counts["B"]`, docstring `:169-170`
"…expected_empty (= B)", beside `:122-124` class A ("market closed") and `:152-156` class B ("upstream
present, priced == 0") — **different axes**. Measured `expected_empty == B == 0` for 3 of 3, recorded not
graded. **The graded substance:** each hole list is identical with and without the date, 3 of 3.

**(d) PASS (re-cut on `W1-S31`)** — **every** partner from the artifact, 3 of 3:

| prefix | keys naming the date | denominator | positive control (09-08) |
|---|---|---|---|
| `daily/49financial/` | 0 | 89 | 1,305 B |
| `daily/cottonwood/` | 0 | 62 | 1,345 B |
| `daily/inflection/` | **1** | 122 | 1,209 B |

The one slice, adjudicated on **who wrote it and when**: `daily/inflection/2026-09-07.json`, 1,209 B,
LastModified `2026-09-07T15:00:41Z` — **inside EG-s-15's run window? FALSE**, by three days. Printed with
`rows=4`, `source_as_of=2026-09-07`, `value-sha=41d1124f75c3`, beside its neighbours (09-04
`e4cb7e34a31c`; 09-05, 09-06, 09-08 all `41d1124f75c3` — carried-forward values). **An upstream-producer
fact: named, printed, not graded** — it is not this system repairing a closed day into a number, which is
what FWD-4 forbids. `W1-S31` carries it; the issuer carries it out of this project.

**(e) PASS** — `COVERAGE-ABSENT` printed for the CloudTrail limb. 0 keys naming the date under both
prefixes, 0 of 62 / 0 of 89 keys modified in the run window; producer logs **14** and **11** lines scanned,
0 naming the date, 0 containing `wrote`. The "BEFORE" limb's limit is stated as an **inference**, not a
retrospective read.

**(f) PASS** — the verdict's `2026-09-10T01:20:20Z` lies inside EG-s-15's window.

### S16-AC2 — RECORDED (judgment), NO VERDICT
The full table with the calendar beside it, the backfill answer, and the three places round-1's fixtures
would have been blind, are in the instance's `S16-AC2` row.

## 2. ROWS (2), both ruled CUT DEFECTS by the issuer

| id | class / hazard | outcome |
|---|---|---|
| W1-S30 | BLOCKING / ARMED | arms (b)/(c) named evidence the artifact does not carry → **both re-cut**; the re-cut arms now PASS with the limit recorded |
| W1-S31 | OBSERVATION / ARMED | arm (d) enumerated 2 partners where the estate has 3 → **re-cut to every partner**, adjudicated on who wrote it and when |

Both `disarm_owner: 2.0.0_SA_COO`. Filed at the prior commit; row gate rc=0, `2 new of 57 total`.

## 3. THE CORRECTION THAT MATTERED

The issuer's hand-list named **two** non-trading dates (09-05, 09-07); there are **three** — Sunday
`2026-09-06` was missing. Because `A = 3` is the artifact's own count, the check is
`A == len(non_trading)`: taking the hand-list would have **failed the arm against a correct world**. The
re-cut arm (b) now *forbids* a hand-list and requires the battery to enumerate the calendar over the
verdict's own window — the instrument, not a transcription of it.

## 4. WHAT I DID NOT DO

No invocation of `etfs-reports-orchestrator` in any mode (Andrew's standing constraint; the order's
`READ-ONLY on the plane`). I did **not** re-derive the per-date class map with a local classifier run to
rescue the original arms (b)/(c) — that swaps the instrument the criterion names, which is the issuer's
act; refusing is why `W1-S30` exists and why the arm was re-cut rather than falsely passed. I did not grade
inflection's predating slice as a failure (the re-cut is explicit that it is an upstream fact), did not
investigate its producer, edited no code, and wrote nothing to the plane.

## 5. AN INSTRUMENT NOTE LEFT IN THE SOURCE

`s3api head-object` renders `LastModified` in **RFC-1123** (`Thu, 10 Sep 2026 01:20:20 GMT`);
`list-objects-v2` renders **ISO-8601**. Both UTC. My first parser branched on `"T" in value` — which
matches the **T** of "**T**hu" and silently truncated the string, failing arm (f) against a true world.
Fixed by discriminating on *shape*.

## 6. DETERMINISM

The battery ran three times: defective arm-(f) parser; after the fix (4 of 6, original cut); against the
re-cut arms (6 of 6). **Every measured number is identical across all three.** Only arm verdicts moved, each
with a named cause — one instrument bug of mine, and the issuer's re-cut. The world did not change.

## 7. PROOF-OF-SPEC AND STATUS

`proof-of-spec-check ... S16-AC1,S16-AC2` → **`VALID (rc=0)`**, 2 of 2 surprises resolving.
**`<status>` FLIPPED to `complete`** — S16-AC1 PASSES by output.

## 8. PUSH STATE (MEASURED)

`git ls-remote origin refs/heads/wk-etfs_guardrail-2-1` → **empty**: LOCAL, never pushed.
