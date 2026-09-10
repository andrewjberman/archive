# NFRA_OUTSET.TO-OS-s-22 -- THE PER-DEVICE CONSUMER: result (INTERIM -- one arm not yet readable)

**Assignee:** `0.7.0_AE_CloudOps~W` · **Issuer:** `2.0.0_SA_COO` · **Cell:** `OS-s-22` ·
**Written:** 2026-09-10T15:0xZ. **The order is NOT flipped.**

---

## THE ONE-LINE ANSWER

**Five of six arms pass. One cannot be read until 2026-09-11 13:00Z**, and the battery FAILS rather
than printing its token, because a criterion that cannot be read yet must not print a word that
says it passed.

## THE ARM THAT WAITS, AND WHY THE WAIT IS QUALIFIED RATHER THAN CONVENIENT

**Arm (e), the DISCLOSURE arm** -- the CTO's ruling on `NFRA_OUTSET-S36` clause (v). It must read a
per-device state **out of the SERVED bytes**. That state lives in the stratum's **denominator**,
and rows `S40`/`S41` measured that **no served artifact carried the denominator at all** -- four
artifacts, five literals, 0 hits each, against a positive control at 2.

`TO-OS-s-27` is **TERMINAL and DEPLOYED** (`@20d5c41567`; runner VersionId
`8pG9vs5I4CSGNVC8OcUy2Q9ARArGgumx`) and now serializes `stratum_denominator`. **Its own bound
forbids backfilling**, so the first artifact carrying the field is tomorrow's scheduled fire.

⛔ **AND NO AD-HOC RUN IS FIRED TO MANUFACTURE ONE.** After 13:00Z today the runner's
schedule-mark rule (`estate_report_runner.py:219-226`) dates a report **2026-09-10**, so a manual
run now would **rewrite today's served keys** -- the act that produced the `S34` rollback, and the
act `TO-OS-s-27`'s bound forbids. That is the named evidence the ad-hoc would destroy, not a
preference.

**What can be said today, and it is not the accept:** the served bytes contain `AccessDenied`
**0 times**, against **3** on the manual served day. **The served falsehood is gone** even though
the disclosure is not yet readable.

## THE FIVE ARMS THAT PASS

### (a) EACH DEVICE BY NAME, WITH ITS VINTAGE
All **3** rostered devices are named in the served composition, and the reporting one carries its
own produced-instant:

```
A_propagation@laptop: comp-heat drift produced 2026-09-09T23:58:09Z ... age 13.1 h
site-z: UNREAD (s3://opal-estate-report/outset/site-z/comp_heat_drift.json)
_os22_probe_device: comp-heat drift (OS-s-22 PROBE FIXTURE) produced 2026-09-09T15:55:15Z ... age 21.1 h
```

### (b) SILENCE IS PER DEVICE
One device reads UNREAD/SILENT while another renders its own vintage **in the same composition** --
so one device past its ceiling does not blank the group.

### (c) THE SECOND ROW NEVER MERGES INTO THE FIRST'S n
Two planted devices, `n=7` over 100 and `n=11` over 200, run through the **served** composition:
`n=7` present, `n=11` present, **`n=18` (the sum) present nowhere.**

### (d) THE SINGLE-KEY READ IS RETIRED, TOKEN BY TOKEN WITH A CONTROL EACH

| token | prior | now | verdict |
|---|---|---|---|
| `prefix.rstrip("/") + "/comp_heat_drift.json"` | **1** | **0** | **RETIRED** |
| `OUTSET_DEVICES` | 0 | 3 | ADDED |
| `_outset_device_fields` | 0 | 2 | ADDED |
| `OUTSET_DRIFT_KEY` | 0 | 2 | ADDED |
| `OUT-OF-CORPUS` | 0 | 4 | ADDED |

The retired token's **prior count of 1** is what makes this a measurement (`W1-S27`): a token
reading 0 on both sides would have discriminated nothing.

### (f) THE NEGATIVE ARMS, AND A PLANTED MUTANT THAT FIRES

| fixture | counts |
|---|---|
| `tracked_total=0` | quiet 0, silent 0, **out-of-corpus 1** |
| no `device` field | quiet 0, silent 0, **out-of-corpus 1** |
| well-formed (**positive control**) | quiet 0, silent 0, **out-of-corpus 0** |

**THE PLANTED MUTANT:** anchor uniqueness asserted first (**exactly 1** occurrence in the served
runner), then a copy of the runner is mutated to sum devices into one `n`. The mutant **does**
produce `n=18`, so arm (c)'s assertion is proven able to catch the drift it exists for.

⛔ **TWO CHECKS IN THIS BATTERY WERE WRONG AND WERE FIXED BEFORE THE PASS,** both recorded because
both looked fine:

1. A `"QUIET" in denominator` test fired on the runner's **OUT-OF-CORPUS explanation**, which ends
   *"(never read as QUIET)"*. **A check that greps a producer's prose reads the producer, not the
   world.**
2. A "first parenthesised group" regex latched onto `device(s)` in the headline and **silently
   dropped the `quiet` count** while returning the other three -- a partial parse that reads
   exactly like a complete one.

Both now read the **declared state names** directly, and the arm asserts counts as numbers.

---

## WHAT THIS RESULT DOES NOT CLAIM

- **That O22-AC1 passes.** It does not; the battery FAILS on arm (e) by design.
- **That the disclosure works.** It is built, deployed and exercised offline under `O27-AC1`; the
  unproven hop is the last one, the state appearing in a SERVED artifact.
