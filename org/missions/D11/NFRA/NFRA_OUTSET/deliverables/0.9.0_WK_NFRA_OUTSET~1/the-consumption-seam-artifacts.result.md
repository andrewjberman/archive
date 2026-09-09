# NFRA_OUTSET.TO-OS-s-10 -- RESULT: THE CONSUMPTION SEAM

**Assignee:** `0.9.0_WK_NFRA_OUTSET~1` (L7 worker subagent of `2.0.0_SA_COO`, spine v3)
**Branch:** `wk-OUTSET-1` (linked worktree `C:\tmp\wk-OUTSET-1`) · **Base:** `6dcd8c92eb`
**Cell:** `OS-s-10` · **outcome_ref:** FWD-3 · **verb:** build · **depends_on:** `OS-s-1`, `OS-s-4`

---

## 0. THE HEADLINE, BECAUSE THIS CELL CARRIED A STOP CONDITION

**The seam is built, demonstrated on real bytes, and PRD s.3's falsifier DID NOT FIRE AS STATED --
but it did not come back clean either, and the difference matters.** The falsifier asks one
question; the world gave a two-armed answer:

| arm | cadence for the 09:00 window? | measured |
|---|---|---|
| an outset tool whose inputs are **cloud-reachable** | **YES** | `served/comp_learns_status.json` written 04:01:03Z today, **0.18 d old**, on its own `cron(0 4 * * ? *)`, ~9 h before the window |
| an outset tool that is **git-history-shaped** (comp-heat `freshness`, `drift`) | **NO PRODUCER EXISTS** | 0 of 142 EventBridge rules; the estate's one such artifact (`code_heat`) frozen **51 days**; CTO revert 2026-07-16 says the shape "can NEVER resolve in the Fargate derive" |

I did **not** file the falsifier's BLOCKING row, and the reason is a distinction I want on the
record: **"cannot be produced" is not what I measured. I measured "is not produced, and no cell owns
producing it."** Inflating the second into the first would be as wrong as softening it. `O10-AC2`
is `judgment="true"` precisely so that call is not mine — the full measurement is recorded, with no
verdict, in `NFRA_OUTSET-W1-S20`.

## 1. WHAT I MEASURED BEFORE BUILDING

- **The window is real.** EventBridge **Scheduler** (not Rules — a different API, and the Rules
  sweep alone would have read as "no estate-report schedule"): 18 schedules, `estate-report-0900et`
  `cron(0 9 * * ? *)` tz `America/New_York`, **ENABLED**, targeting the orchestrator Lambda. The
  runner's own code agrees (`:63-64`).
- **The runner declares group A UNAVAILABLE for want of a workspace** — PRD s.7's claim column,
  confirmed at `_stratum_propagation`.
- **The pattern to copy already exists**: three nightly Fargate producers on `opal-globgrph`, one of
  which (`comp-learns`) publishes a **comp-tool status artifact** to `served/`. That is the closest
  precedent to what this cell needs, and it works.
- **The runner's IAM cannot reach any seam location.** Read on the **APPLIED** plane
  (`iam:GetRolePolicy`), not inferred from Terraform: `estate-report-runner-role` grants
  `s3:GetObject` on exactly `opal-estate-report/{daily/*, code/*, manifest/*}` plus the single exact
  key `kuzu_nessie_db` — and nothing at all on the globgrph bucket. The Terraform for that same Sid
  already warns why an action-level check would miss this: *"comp-iam models (action), never
  (action, resource), so an action-level check would have reported this GRANTED."*

## 2. WHAT I BUILT -- and why it is in two files rather than one

**`org/modules/heatmap/outset_seam.py` (new) -- the PRODUCER half.** Runs a tool, wraps what it
answered, publishes to one destination the caller names.
**`estate_report_runner.py` (edited) -- the CONSUMER half**, inside `_stratum_propagation`.

**The split is forced by the world, not chosen.** The report host's systemd unit pulls **exactly one
file** from S3 (`code/estate_report_runner.py`, `instance.tf:215`) and has no estate workspace, so
it *cannot* import the producer module. That is one implementation of each half — not two of the
same — and the thing they share is the artifact **schema**, which battery arm B checks as a real
contract test in both directions rather than trusting matching comments.

### 2.1 What an artifact carries, and every value carries its claim

```
answer_state + answer_state_claim   vintage{answer_produced_utc, tool_reported, claim}   denominators{..., claim}
```

Two honesty problems surfaced while wiring real tools, and both are in the artifact rather than
hidden by it:

- **Not every comp-tool emits an `answer_state`.** Measured: `comp-heat drift --json` has no such
  key at all, and `comp-heat freshness --json` emits `"answer_state": null` on a *healthy* answer.
  Reading either as OK is an **inference**, so it is carried as one:
  `"answer_state_claim": "inferred (the tool emitted no answer_state and returned rc=0 with a
  parseable JSON answer)"`. A consumer can reject on the claim; it cannot reject on a value that
  quietly pretends the tool said it.
- **A null denominator is worse than no field.** `denominators` is never null: it is the tool's own
  `denominator`/`summary` objects, every top-level scalar it published, and Rule T's terminal line
  (which *is* a denominator — "scanned N of N"). A tool that reported none says
  `{"claim": "absent", "reason": ...}`.

### 2.2 The consumer's three failure modes, and the third fact

`a failed publish reads FAILED, never absent` is the cell's load-bearing property. The reader has
**ABSENT / UNREADABLE / STALE**, each returning a non-OK stratum with its reason.

And a **fourth** distinction that the runner's own docstring demands ("no report", "AI half failed"
and "nothing to propose" must never render alike): **NOT CONFIGURED is not FAILED.** With no seam
source configured the group reads `INSTRUMENT_UNAVAILABLE` exactly as it always has ("nothing was
expected"); only a configured-but-missing artifact reads `INSTRUMENT_FAILED`.

**`ESTATE_OUTSET_SEAM_PREFIX` is unset by default, so production behaviour is byte-unchanged** until
both a producer cadence and the IAM grant land. That is deliberate: pointing the seam at a location
the role cannot read would produce `INSTRUMENT_FAILED` every day, and an AccessDenied is
indistinguishable from an absent publish in the reader's own vocabulary — by design.

### 2.3 One hole I found in my own control

Staleness is a **one-sided** test: a future-dated artifact can never trip it, so a producer with a
skewed clock could publish something dated tomorrow and have it read fresh for days. Added a
future-date refusal with its own arm (F2).

## 3. ACCEPTANCE

### O10-AC1 -- PASS-by-output
`<invocation>` `python .tools/tests/test_os10_seam.py` · `<expect>` `PASS`

```
[PASS] A-ONE-ARTIFACT-PER-OUTSET-TOOL-WITH-STATE-VINTAGE-DENOMINATORS -- published 2 of 2 declared producer(s), each carrying answer_state(+claim), vintage.answer_produced_utc and a denominators object with its own claim: [('comp_heat_freshness_tools', 'OK'), ('comp_heat_drift', 'OK')]
[PASS] B-PRODUCER-AND-CONSUMER-DECLARE-THE-SAME-DOMAIN -- producer-only=[] ; consumer-only=[] ; 6 state(s) map into 3 runner status(es) all within the runner's own vocabulary=True ; seam tag agrees=True
[PASS] C-RUNNER-READS-A-REAL-PUBLISHED-ARTIFACT -- stratum status=OK row_count=4 | vintage=comp-heat drift produced 2026-09-05T08:49:03Z (tool vintage: none reported) | denominator=comp-heat drift -- tool_scalars.n=4; tool_scalars.n_modified=1; tool_scalars.n_untracked=3; budget_terminal=WITHIN BUDGET...
[PASS] D-FAILED-PUBLISH-READS-FAILED-NEVER-ABSENT -- status=INSTRUMENT_FAILED row_count=None ; rendered LOUDLY=True ; not rendered as a clean zero=True
[PASS] E-NOT-CONFIGURED-IS-NOT-THE-SAME-AS-FAILED -- unconfigured=INSTRUMENT_UNAVAILABLE vs absent-publish=INSTRUMENT_FAILED -- three facts, three renderings
[PASS] F-STALE-ARTIFACT-READS-FAILED-NOT-TODAYS-ANSWER -- artifact STALE ... age 51.0 h > ceiling 26.0 h
[PASS] F2-FUTURE-DATED-ARTIFACT-IS-REFUSED-NOT-TRUSTED -- a 9 h-ahead artifact would NEVER trip the staleness ceiling, so it is refused
[PASS] G-UNMAPPED-ANSWER-STATE-IS-REFUSED -- answer_state 'SOMETHING_THE_SEAM_NEVER_DECLARED', outside the seam's declared domain
[PASS] H-A-FAILING-PRODUCER-PUBLISHES-FAILED-NOT-SILENCE -- producer answer_state=FAILED -> stratum INSTRUMENT_FAILED
[PASS] I-RED-MUTANT-FAILED-PUBLISH-READS-ABSENT-AND-IS-CAUGHT -- mutant: a MISSING artifact renders status=OK row_count=0 and the report says 'zero rows -- this is a RESULT' ; production on the SAME missing artifact: INSTRUMENT_FAILED
[PASS] J-MUTATION-ANCHOR-UNIQUE
[PASS] K-S3-PUBLISH-PATH-EXERCISED-WITHOUT-WRITING-A-BUCKET -- stub received Bucket='not-a-real-bucket' Key='outset/comp_heat_drift.json' ; a keyless s3 URI is REFUSED
OS10-SEAM BATTERY: 12/12 PASS (denominator 12; 0 AWS calls, 0 network)
```
**rc=0. 12 of 12 arms PASS.** Also under pytest: `1 passed in 2.63s`.

**The RED mutant the criterion names** is arm I, and it is the defect stated exactly: the consumer's
ABSENT branch is replaced, in a temporary copy of the runner, with a clean empty result. Under the
mutant a **missing artifact renders `status=OK, row_count=0`** and the report prints *"zero rows --
this is a RESULT, the instrument ran and found nothing"* — a failed publish reading as ABSENT, which
the model would narrate with full confidence. Production on the same missing artifact:
`INSTRUMENT_FAILED`. Without it, arms C-H would be vacuous.

### O10-AC2 -- JUDGMENT (`judgment="true"`) -- RECORDED, NO VERDICT

**Limb 1 -- one real published artifact and the runner reading it.** Real, not a fixture:

```
$ python org/modules/heatmap/outset_seam.py --tool .tools/comp-heat --out-dir <dir>
comp_heat_freshness_tools     answer_state=OK  published=True bytes=62844
comp_heat_drift               answer_state=OK  published=True bytes=1514
SEAM PUBLISH: 2 of 2 producer(s) published a non-FAILED artifact
```
and the runner's own `_stratum_propagation` against that directory:
```
status   : OK
vintage  : comp-heat drift produced 2026-09-05T08:45:19Z (tool vintage: none reported), age 0.0 h @PIN123
denom    : comp-heat drift -- tool_scalars.n=4; tool_scalars.n_modified=1; tool_scalars.n_untracked=3; budget_terminal=WITHIN BUDGET: scanned 3 of 3 files...
row_count: 4
```
Beside it, the same call with no artifact: `INSTRUMENT_FAILED`, *"artifact ABSENT ... the publish
FAILED or never ran. This is a FAILED stratum, never an omitted one."*

**What this demonstration is NOT.** It is the runner's own reader code on real bytes; it is **not**
the runner's *role* reading from S3. It cannot be: that role has no grant on any location a producer
could write (s.1). Demonstrating a read with my own credentials would prove nothing about the host —
the wrong-principal trap — so I did not stage one.

**Limb 2 -- the falsifier.** Measured in full in s.0 and `W1-S20`. It does not fire as stated. What
is true instead: the publishing step PRD s.3 names as this shape's cost **has no owner** — I read
all 17 rows of the manifest and none says produce, schedule or own the publisher, and PRD s.5 does
not place it out of scope either.

**I also did not publish to a real S3 bucket**, and that was a decision rather than an omission: the
runner's role could not read it, it would create an unscheduled unowned object in a shared `served/`
prefix — the exact half-landed shape `OS-s-7` found at 51 days — and NEVER-AUTO-DELETE means I could
not remove it afterwards. The `s3://` code path is proven instead by arm K against a stub.

## 4. REGRESSION + GATES

| check | result |
|---|---|
| `python .tools/tests/test_os10_seam.py` | `12/12 PASS`, rc=0 |
| `python -m pytest -q .tools/tests/test_os10_seam.py` | `1 passed in 2.63s`, rc=0 |
| `test_os1_budget_battery.py` | `21/21 PASS`, rc=0 |
| `test_os2_path_grain.py` | `10/10 PASS`, rc=0 (x3) — **after s.5** |
| `test_os4_federated_vintage.py` | `9/9 PASS`, rc=0 |
| `test_os5_sql_bound.py` | `10/10 PASS`, rc=0 |
| `test_comp_heat_battery.py` | `Ran 2 tests ... OK`, rc=0 |
| `bash .tools/commit-gate.sh` on the 3 touched files | `OK: pre-commit gate clean for 3 of 3 file(s)`, rc=0 |

The gate's non-ASCII WARN names lines 1173-1175 of the runner; **those pre-exist at HEAD** (verified
with `git show HEAD:`) and are not mine, so I left them — fixing a neighbouring defect is not this
cell's business.

## 5. MY OWN EARLIER FIX WAS INCOMPLETE, AND THE REGRESSION CAUGHT IT -- `NFRA_OUTSET-W1-S18`

`OS-s-2`'s arm F **failed again** in this cell's regression sweep — `9/10`, on a **git-sourced** row
(`.tools/deregister-all`, 141.7 vs 141.71), with `HEAD held during the arm`, so it was *not* the
contention mechanism `W1-S12` fixed.

**Cause:** comp-heat publishes `age_days` as `round(x, 2)`, so the value is quantised to 0.01 d
steps — and the arm's tolerance **was** 0.01. Two adjacent steps differ by exactly the tolerance and
compare as greater in float. **The tolerance equalled the quantisation.**

**Why my own falsifier could not have caught it:** `W1-S12`'s control churned an *untracked* file's
mtime. That exercises the class this fix had already moved *out* of the age comparison. The row that
failed here is *git-sourced*, whose age moves only by rounding. **A control aimed at one mechanism is
not evidence about another** — and the issuer's certification, which ran that same shape, inherits
that limit. Raised to 0.02 (two quanta, 28.8 min) with the quantum named in the arm's own printed
detail; the key set is still compared exactly over all 393 rows, so a real scoping regression (which
moves an age by *days* or drops the row) still fails. 3 of 3 clean.

## 6. ROWS FILED (45 rows at this write; 42 -> 45, append-only)

- **`W1-S18`** (OBSERVATION, INERT) — s.5, filed against my own certified fix.
- **`W1-S19`** (OBSERVATION, **ARMED**, disarm_owner `2.0.0_SA_COO`) — the runner's role cannot read
  any seam location; DESIRED and APPLIED read separately; `kuzu_nessie_db` is the precedent for the
  shape of the ask. **Not BLOCKING:** no criterion is stopped.
- **`W1-S20`** (OBSERVATION, **ARMED**, disarm_owner `2.0.0_SA_COO`) — the cadence measurement, both
  arms, and why the falsifier does not fire as stated. The uncovered member: **no cell owns the
  publishing step.**

## 7. DECLARED NON-APPLICATION

- **No Terraform, task definition, EventBridge rule or IAM change** — none is in this order's
  `<paths>`, and PRD s.5 places the runner's own infrastructure out of scope.
- **No enumeration of every outset tool.** `SEAM_PRODUCERS` is a declared registry of two comp-heat
  producers; enumerating the full set is `OS-s-12`'s census (FWD-5) and the seam must not fork a
  second one.
- **The runner's stratum status vocabulary is not widened.** That contract is SPEC s.5's and belongs
  to `OS-s-9`/`OS-s-11`; the seam maps *into* it.
- **No alarm, monitor or freshness-checker.** The staleness check is a *field on a stratum the
  report already renders*, not a watcher — it fires only when the report runs, and it notifies
  nobody.
- **Nothing deleted; no new dependency; no second implementation.**

## 8. PUSH STATE

**LOCAL.** Nothing pushed. Measured with `git ls-remote` at report time — see the WORKER REPORT.
