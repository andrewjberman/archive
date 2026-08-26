# ADVI_PERFRP TO-R1-AE · AC4 — the projection stage EXERCISED by ad-hoc QA run

**author:** `0.7.0_AE_CloudOps~K` · **fired** 2026-08-26T16:31:48Z · **ran** 16:32:20–16:34:32Z
**authority:** Andrew-direct ~16:2xZ relayed by `2.0.0_SA_COO` 72541 — *"If we are waiting on a
scheduled run, run an ad-hoc/QA run to test, do not wait."* COO's standing no-ad-hoc-invoke WITHDRAWN
in the same message. Re-framed 08-27 bar from `3.0.0_SA_CVO` 72546 read before firing.

⛔ **AN AD-HOC ARTIFACT IS NEVER PRODUCTION EVIDENCE. AC4's ACCEPTANCE REMAINS THE 2026-08-27 12:45Z
SCHEDULED FIRE.** This is a QA instrument and is reported as one.

---

## RESULT — the stage executes, and it classifies correctly

```
CHAIN START date=2026-08-25 mode=production workdir=/tmp/49f_chain_work stages=17
...
STAGE OK c04_validation rc=0 wall=0.6s
  WOULD_PUBLISH  perfrp_activity_relationship    -> platinum/advi/49financial/perfrp_activity_relationship.json
  WOULD_PUBLISH  perfrp_activity_account         -> platinum/advi/49financial/perfrp_activity_account.json
  WOULD_PUBLISH  perfrp_performance_relationship -> platinum/advi/49financial/perfrp_performance_relationship.json
  WOULD_PUBLISH  perfrp_performance_account      -> platinum/advi/49financial/perfrp_performance_account.json
  WOULD_PUBLISH  perfrp_allocation_relationship  -> platinum/advi/49financial/perfrp_allocation_relationship.json
  WOULD_PUBLISH  perfrp_allocation_account       -> platinum/advi/49financial/perfrp_allocation_account.json
  EMITTER_REFUSED perfrp_gainloss_relationship
  EMITTER_REFUSED perfrp_gainloss_account
  EMITTER_REFUSED perfrp_transactions_relationship
  EMITTER_REFUSED perfrp_roster_relationship
  EMITTER_REFUSED perfrp_book_advisor
STAGE OK perfrp_projection rc=0 wall=9.5s families=11 attempted=11 built=6 refused=5 hard_fail=0
  (publisher rc=1; refusals are a DECLARED round-1 state, not a failure)
CHAIN OK date=2026-08-25 wall=130.3s
```

**This is the code's own pre-registered expectation, met exactly.** The source comment at
`_run_perfrp_projection` states *"MEASURED 2026-08-25: rc=1 with status census {would_publish: 6,
emitter_refused: 5}"* — 6 built, 5 refused, and the five refusing families are precisely the five the
comment names (gainloss rel+acct, transactions, roster, book_advisor).

### ⛔ THE THING THIS RUN ACTUALLY PROVED, AND IT IS NOT "THE STAGE RAN"

**The wrapper correctly classified `publisher rc=1` as SUCCESS.** That is `b9915d8271`, and it is the
fix whose absence would have been catastrophic — `~G`'s own commit subject reads *"MY OWN STAGE WOULD
HAVE ABORTED THE 49F CHAIN ON EVERY SCHEDULED FIRE."* Five of eleven round-1 families refuse **by
design**, and `d_publisher_port` folds `emitter_refused` into the same `bad` bucket as real errors, so
a bare `rc != 0 -> abort` aborts the entire 49F chain every day on the *expected* state.

**Until this run that fix had never executed anywhere but a test.** `CHAIN OK` is the evidence that a
deployed, never-executed stage does not take the chain down with it.

**Fail-closed ordering confirmed on a real run:** `STAGE OK c04_validation` precedes the projection in
the log. The projection having run *implies* c04 ran and passed — the invariant is total, exactly as
the placement ruling required.

---

## POST-FIRE VERIFICATION — what the run did NOT touch

| check | baseline (16:29:44Z) | after | verdict |
|---|---|---|---|
| served plane key count | 12 | **12** | UNCHANGED |
| served `perfrp*` keys | 0 | **0** | **nothing published** |
| `twr_daily` 08-25 ETag | `4d01d0c4e0db653bf9d660d17264fed8` | **identical** | **byte-identical rebuild** |
| `twr_daily` census | 6415 / 923 / 10 | **6415 / 923 / 10** | AC1 deliverable stands |
| 12:45Z scheduled chain log | 9,404 B @12:47:38Z | **unchanged** | not overwritten |

**BUILD-ONLY IS PROVEN, NOT ASSERTED.** Every one of the six built families printed `WOULD_PUBLISH`
against its exact platinum key and **not one of those keys exists.** The stage is guarded twice
independently — the invocation carries no `--publish`, and `d_publisher_port` separately requires
`OPAL_ADVI_PUBLISH_GRANT=1` — so the served plane cannot move from here. The 49F flip hold
(Andrew-direct 2026-08-21) is untouched, and one-producer-per-served-key holds.

**THE BYTE-IDENTICAL ETag IS THE INTERESTING ONE.** Before firing I diffed the version that ran at
12:45Z against the deployed one: **4 deletions, all comment/count lines; 111 additions confined to the
new stage.** I predicted the rebuild would be content-neutral for every upstream table. The ETag came
back identical — a prediction made before the act and confirmed after, rather than a hope.

---

## THE EVIDENCE-DESTRUCTION EXCEPTION — CHECKED, NOT ASSUMED

COO 72541 s.5: *"the ONE case where an ad-hoc genuinely must not fire is when it would DESTROY
evidence the scheduled run exists to produce. If you invoke that exception, name the evidence."*
**I do not invoke it, and here is the check:**

- Chain logs are **per-run timestamped keys** (`chain_20260826T163220Z.log`), so today's 12:45Z
  scheduled log cannot be overwritten — verified present and unchanged afterwards.
- Tomorrow's scheduled fire writes **date=2026-08-26**; this ad-hoc wrote **2026-08-25**. Different
  partitions, no collision with the acceptance.
- The served plane is what AC3 measures, and nothing was published.

⚠ **ONE THING I CHANGED AND AM NAMING RATHER THAN LEAVING TO BE FOUND:** the ad-hoc re-stamped
`twr_daily` date=2026-08-25 `LastModified` from 12:47:36Z to 16:34:22Z. **The bytes are identical**
(same ETag, same size, same census) so my AC1 characterisation is unaffected, but a reader diffing
mtimes rather than content would see a change where there is none.

---

## ⛔ A DUPLICATE PRODUCTION DISPATCH FIRED, AND THE MUTEX CAUGHT IT

Two SSM commands landed, **both carrying my source label** `advi.49f.adhoc-qa-perfrp-ac4`:

```
96888117-4f67-4d77-8dff-1224f09b2496   requested 16:32:20Z   -> ran, CHAIN OK
4c0f751b-f13f-4671-8d1f-1d8b9971a18d   requested 16:32:55Z   -> RC=3, REFUSED
  CHAIN REFUSED: live lock /tmp/49f_chain.lock
    holder={"pid": 1094, "since": "2026-08-26T16:32:21.840725+00:00", "date": "2026-08-25", "mode": "production"}
```

I issued **one** successful `lambda invoke` (16:31:48Z); my earlier attempt died in CLI-v1 argument
parsing before reaching AWS. The most probable mechanism is a **botocore-layer retry on a slow
synchronous invoke** — the dispatcher was waiting on a stopped `r6i.4xlarge` to boot, so the call ran
long enough to trip a client read-timeout, and the retry produced a second lambda execution and a
second `send_command`. **Stated as the probable mechanism, not a proven one:** I did not capture the
client-side timing, and `started_by_dispatcher: false` on the second is consistent with it but does not
prove it.

**THE CONTROL HELD.** `chain_49f_entrypoint` takes an atomic `mkdir` lock and *"refuses LOUD, never
steals"* — the duplicate exited rc=3 with the holder's pid, start time, date and mode printed. Two
concurrent production chain runs over one date would have been a genuinely bad outcome and the lock is
the only thing standing between an over-eager dispatch and it.

---

## AC4 STATUS AFTER THIS RUN

| axis | state |
|---|---|
| DESIRED | ✔ committed `a07fa4f35e` + `b9915d8271` |
| **APPLIED** | ✔ deployed 2026-08-26T13:38:14Z, byte-identical to HEAD, stage present in the bytes |
| **EXERCISED (QA)** | ✔ **this run** — stage executed, classified correctly, chain completed |
| **EXERCISED (scheduled)** | ⏳ **2026-08-27 12:45Z `advi-49f-gold-floor`** — the acceptance |

**I am NOT scoring AC4 PASS.** The TO puts acceptance on a scheduled fire and the standing rule that an
ad-hoc is never production evidence is unchanged. What this run removes is the *unknown*: a deployed,
never-executed stage was UNVERIFIED, and it is now verified to execute, to classify a by-design rc=1 as
success, and to leave the served plane alone. Tomorrow's fire confirms it on the production path.

**Tomorrow's read is now a one-liner:** the 12:45Z log must carry `STAGE OK perfrp_projection` with
`built=6 refused=5 hard_fail=0` for `date=2026-08-26`, and `CHAIN OK`. A `CHAIN ABORT
stage=perfrp_projection` is the failure signature and would mean the classification does not hold on a
different date's data.

## INSTRUMENT NOTE

The full log was read from **`s3://opal-data-49financial/gold/advi/_logs/chain_20260826T163220Z.log`
(10,957 B)**, not from `ssm get-command-invocation`, whose `StandardOutputContent` is capped and which
earlier today ended in a literal `--output truncated--` and nearly produced a false absence claim from
me. The SSM doc uploads the complete log to S3 on every run; **that is the durable oracle and the SSM
stdout is not.**
