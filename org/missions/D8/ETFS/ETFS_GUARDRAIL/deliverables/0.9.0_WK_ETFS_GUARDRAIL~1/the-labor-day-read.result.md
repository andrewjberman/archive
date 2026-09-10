# EG-s-16 -- THE LABOR DAY READ: criteria verbatim, with rc and denominator

**Worker:** `0.9.0_WK_ETFS_GUARDRAIL~1` · **Branch:** `wk-etfs_guardrail-2-1` · **Face:**
`ETFS_GUARDRAIL.TO-EG-s-16` @`3ee6b6e0d0` · **Reads:** EG-s-15's run (request id
`9fbc33e0-174c-4c82-b392-2b1dafe4a835`, 01:19:02Z→01:20:28Z) and **fires nothing**

## 0. THE HEADLINE

**The substance of FWD-4 holds on real data, and the criterion still cannot pass — because two of its arms
name evidence the served artifact does not carry.** That is a cut defect, filed as `W1-S30`, not a defect
of the world.

**What holds, measured:** the deployed classifier told a real closed-market day apart from a hole. Every
partner reads `A = 3`, exactly matching the calendar's **three** non-trading days (09-05 Sat, 09-06 Sun,
09-07 Labor Day). `2026-09-07` is in **no** partner's holes (3 of 3), and each hole list is identical with
the date removed. The month's only holes are `2026-09-09`, class **D** — so the verdict demonstrably *can*
mark a hole, and did, two days after the target.

**What does not:** the served `coverage_verdict.json` contains the literal string `2026-09-07` **zero
times**. It carries per-class *counts* plus a `holes` date list — no per-date class map. And
`expected_empty` is the class **B** count by the classifier's own docstring, so it structurally cannot
carry a class-**A** date.

**And a finding the criterion could not have caught (`W1-S31`):** a daily slice **does** exist on the
closed day — for the one partner arm (d) does not enumerate.

## 1. CRITERIA

| id | status | rc | deciding line |
|---|---|---|---|
| S16-AC1 | **FAIL** | 1 | `EGS16-NOT-ESTABLISHED -- failing arms: b, c` (`ARMS 4 of 6 PASS`) |
| S16-AC2 | **RECORDED (judgment)** | n/a | graded by `3.0.0_SA_CVO` at L9 — **no worker verdict** |

### S16-AC1 — FAIL (on artifact shape, not on the world)
`timeout 300 python .../test_egs16_labor_day.py` → rc=1

**PASSING (4):**

- **(a)** `is_trading_day(date(2026,9,7))` → **False**; positive control `is_trading_day(date(2026,9,8))`
  → **True**. Every non-trading day 09-01..09-09: `['2026-09-05','2026-09-06','2026-09-07']` — **3 of 9**.
  *Measured, not assumed:* there are **three**, not one and not two; that count is what corroborates `A=3`.
- **(d)** `daily/cottonwood/` **0 of 62** keys name the date; `daily/49financial/` **0 of 89**. Positive
  controls present: the 09-08 slices (1,345 B and 1,305 B).
- **(e)** `COVERAGE-ABSENT` printed for the CloudTrail limb (no data-event selector covers
  `opal-data-etfs`; versioning disabled, `W1-S12`). After the run: 0 keys name the date under both
  prefixes and **0 of 62 / 0 of 89** keys carry a LastModified inside the run window. Producer logs:
  **14** and **11** lines scanned, **0** naming the date, **0** containing `wrote`.
- **(f)** The verdict object's `2026-09-10T01:20:20Z` falls inside EG-s-15's window.

**FAILING (2), both row `W1-S30`:**

- **(b)** *Readable and true:* the date is in no partner's holes (3 of 3) and `A == 3` for 3 of 3 partners.
  *Not readable:* the object names the date **0 times**; `per_partner` entries carry only
  `['summary','coverage_line','holes']`. A **count is not a per-date classification**, and reporting it as
  one would be a grain error.
- **(c)** *The hole-count limb holds* — the hole list is identical with and without the date for 3 of 3
  partners. *The "carries" limb cannot:* `classifier.py:168-170 @c866edd324` defines `expected_empty` as
  `(= B)` and `:178` sets `expected_empty = counts["B"]`; measured, `expected_empty == B == 0` for 3 of 3.
  The face's equivalent-field hatch was exercised: the only per_partner field carrying dates is `holes`.

### S16-AC2 — RECORDED (judgment), NO VERDICT
The full table, the calendar beside it, the split answer on backfill, and the three places round-1's
fixture proofs would have been blind, are in the instance's `S16-AC2` row.

## 2. THE FINDING ARM (d) COULD NOT SEE — `W1-S31`

`daily/inflection/2026-09-07.json` — **1 of 122** keys — 1,209 B, written **2026-09-07T15:00:41Z**, four
priced ETF rows, `account_count 562`, `source_as_of 2026-09-07`, citing
`s3://opal-data-inf/gold/canonical/holdings_2026-09-07.parquet`. So it asserts an as-of date on which the
US market was shut. 09-05 (Sat) and 09-06 (Sun) exist too.

A sha256 over each file's `(ticker, ownership_value, account_count)` tuples:

    2026-09-04  e4cb7e34a31c
    2026-09-05  41d1124f75c3   <- identical
    2026-09-06  41d1124f75c3   <- identical
    2026-09-07  41d1124f75c3   <- identical  (Labor Day)
    2026-09-08  41d1124f75c3   <- identical

Carried-forward duplicates, not independently priced days. **Not written by EG-s-15's run** — its
LastModified is three days earlier — so this is standing behaviour of inflection's own producer.

**Why nothing will ever flag it:** `classifier.py:122-125 @c866edd324` returns class A and `continue`s
**before** the `if date_str in series` slice check at `:128`. The classifier never examines whether a slice
exists on a non-trading day, for any partner, in any month. And arm (d) enumerates the **two clean**
partners — so the arm passes while the phenomenon FWD-4 forbids sits in the uncovered third member.

The battery **prints** inflection beside the graded partners with its denominator, so the reading is
visible without widening the criterion.

## 3. ROWS FILED (2)

| id | class / hazard | one line |
|---|---|---|
| W1-S30 | **BLOCKING** / ARMED | the served verdict carries counts, not a per-date class map; `expected_empty` is class B — arms (b) and (c) are unsatisfiable against the named artifact for **any** month |
| W1-S31 | OBSERVATION / ARMED | a slice exists on the closed day for the unenumerated partner; the classifier is structurally blind to it |

Both carry `disarm_owner: 2.0.0_SA_COO`. Row gate: `2 new row(s) of 57 total checked`, rc=0; corpus
baseline clean.

`W1-S30` names two disarm paths for the issuer: **(1)** re-cut (b)/(c) onto the evidence the artifact does
carry — "in no partner's holes", "hole list identical with and without the date", "A count == the
calendar's non-trading-day count", all of which this battery already measures and prints; or **(2)** a code
cell persisting the per-date class map beside the counts, which would make FWD-4 auditable after the fact
for every future month.

## 4. WHAT I DID NOT DO

**No invocation of `etfs-reports-orchestrator` in any mode** — Andrew's standing constraint and this
order's own `READ-ONLY on the plane` bound. I verified the face against the constraint myself before
starting rather than relying on the relayed read; no arm requires an invocation. I did **not** re-derive
the per-date class map by running the classifier locally to rescue arms (b)/(c) — that substitutes a
different instrument for the one the criterion names, and choosing the instrument is the issuer's act. I
did not grade inflection under arm (d), did not investigate its producer (outside this project's surface),
edited no code, wrote nothing to the plane, and re-worded no criterion.

## 5. AN INSTRUMENT NOTE FOR THE NEXT READER

`s3api head-object` renders `LastModified` in **RFC-1123** (`Thu, 10 Sep 2026 01:20:20 GMT`) while
`list-objects-v2` renders **ISO-8601** (`2026-09-10T01:20:20.000Z`). Both UTC. My first parser branched on
`"T" in value` — which matches the **T** of "**T**hu" and silently truncated the string, failing arm (f)
against a true world. Fixed by discriminating on *shape*; the note is left in the battery's source.

## 6. PROOF-OF-SPEC AND STATUS

`proof-of-spec-check ... S16-AC1,S16-AC2` → **`VALID (rc=0)`**, 2 of 2 surprises resolving to channel rows.

**`<status>` NOT flipped.** The face is explicit: *flip only when S16-AC1 PASSES by output.* It does not.
A VALID instance is not a met order; `ETFS_GUARDRAIL.TO-EG-s-16` stays open and this is its final report.

## 7. PUSH STATE (MEASURED)

`git ls-remote origin refs/heads/wk-etfs_guardrail-2-1` → **empty**: LOCAL, never pushed.
