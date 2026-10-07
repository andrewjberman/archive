# OPAL_BBGTML.TO-GUARD-3 -- REPORT 2 of 2: the first live read is PASS on both arms. CLOSED.

**From:** `0.7.0_AE_CloudOps~RV` **To:** `2.0.0_SA_COO~Z` **At:** 2026-10-07 ~11:34Z
**Order:** `org/tier2_senior/0.7.0_AE_CloudOps~RV/task_orders/OPAL_BBGTML.TO-GUARD-3.checker-series-compare-and-tripwire-recency.md`
**Report 1:** `.../deliverables/TO_GUARD_3_REPORT_1_MERGE_LANDED_20261007.md` @`2e50c18d45`
**Verdict: CLOSED, not REVERTED.** The `<status>` flip is the issuer's.

---

## 1. The two live reads

The order's first live read is "the next 07:00 ET vehicle's tripwire result and the next 07:30 ET
checker result, both PASS on current data." Because the merge landed at 09:54Z, 36 minutes before
the 10:30Z exclusion, that read is **today's** two fires rather than tomorrow's.

### ARM 1 -- the 07:00 ET vehicle, fired 2026-10-07 07:00:01 local = 11:00Z

Log: `C:\Users\Opal Bloomberg\opal_bbg_logs\bbg_tplus1_20261007_070002.log`

```
  :9   PRECONDITION: PASS -- DAPI UP, an entitled session answered a real refdata request.
  :24  TRIPWIRE: vintage 20261006
  :34        custom CIX series graded: 13 of 84 tickers in return_daily (71 vendor series
             are not custom and are not graded here); as-of 2026-10-06
  :35  OK:   data.return_daily: all 13 custom CIX series reach the as-of 2026-10-06
  :45  RESULT: PASS -- both PKLs safe to send (/bbg-send).
  :61  PULL EXIT CODE: 0
```

**Line 34 is the new limb running in the real scheduled vehicle, with its denominator, on data
nobody staged for it.** Line 35 is the verdict: 13 of 13 current, no false alarm on good data.

**The precondition line matters as much as the verdict.** Report 1 flagged that if today's fire
repeated the 2026-10-06 DAPI-down run (row `OPAL_BBGTML-Z-S11`, `LastTaskResult 267014`, pull never
attempted), the tripwire would never execute and this arm would be **NOT RUN**, never PASS. DAPI was
up, the pull ran, the tripwire ran. **The arm is RUN.**

### ARM 2 -- the 07:30 ET checker, fired 07:30:01 local = 11:30Z

Log: `C:\opal-elev\freshness_check.log`. Exactly one line is stamped today, and it is the whole read:

```
2026-10-07T11:30:02Z  PASS: data_as_of=2026-10-06 expected_frontier=2026-10-07
  trading_days_behind=1 (healthy T-1; <=1 passes -- weekend behind=0 is fresher, not stale);
  per-series: served data_as_of=2026-10-06. series graded=10. every graded series ends ON
  data_as_of.
```

That is the merged PASS line: the pre-existing prefix and operands unchanged, with the per-series
detail appended. Exit 0.

## 2. Corroboration, and the controls on the read itself

**A second instrument, because a log line is the producer's own account.**
`Get-ScheduledTaskInfo` reads, independently of either log:

| task | LastRunTime (local) | LastTaskResult | the day before |
|---|---|---|---|
| `OPAL_BBGTML_daily_pull` | 2026-10-07 07:00:01 | **0** | 267014 (Z-S11) |
| `OPAL_BBGTML_freshness_check` | 2026-10-07 07:30:01 | **0** | 2 (STALE) |

**A negative control on the summons path.** A PASS must summon nobody, and an unexercised silence
proves nothing on its own -- so it was checked on both carriers the summons writes to:
`C:\opal-elev\freshness_ESCALATION.txt`'s last line is still **yesterday's**
`2026-10-06T11:30:02 STALE`, and **zero** `freshness_checker` inbox files are dated `20261007` in
either recipient directory. Nothing was appended today. The summons path stayed quiet because the
check passed, not because it is inert -- yesterday's entry in the same file is the proof it writes
when it should.

**Exit codes 4 and 5 were NOT exercised live, and that is the correct outcome, not a gap.** The data
is healthy, so the new paths must not fire; a live 4 or 5 today would have meant a real defect. They
are proved on real archived bodies by AC1 (report 1, section 2), which is the only way to exercise
them without planting bad data into production.

## 3. What the same log measured about row `OPAL_BBGTML-Z-S12`, in production

The vehicle log carries **two** tripwire blocks, because `scheduled_daily_pull.cmd` runs the pull leg
(the **tplus1** copy, via `run_daily_pull.py`) and then the send leg (`publish_to_portal.py`, which
at line 64 deliberately invokes the **tzero** copy). The second block, lines 67-87:

```
  :77  OK:   data.return_daily: all 5 model portfolios have a bar ON the as-of 2026-10-06
       ... and NO "custom CIX series graded" line anywhere in the block
  :87  RESULT: PASS -- both PKLs safe to send (tzero vintage).
```

**So the send gate ran today with no per-series CIX coverage at all.** That is row `Z-S12`'s residual,
measured live in production rather than argued from reading the code -- and it is exactly what
TO-GUARD-4 closes on branch `rv-bbgtml-guard4` (`d328b0d5fe` + `3b65362444`, `GUARD-4: PASS`, NOT
MERGED, awaiting Andrew's word). It also matches GUARD-4 proof arm C5: tzero's own presence check
grades the 5 MODELS and structurally cannot see the 8 benchmark/ETF series.

## 4. No revert, and why that is the order's own rule rather than my preference

The order: "A FAIL on CURRENT data means revert the merge the same hour. A FAIL because the data
really is behind is the build working: report it, do not revert." **Neither branch applies -- there
was no FAIL.** Both arms PASS on current data, on two instruments each, with the summons path
verified silent. Nothing was reverted and nothing is stranded.

## 5. The NEVER-2 entry is CLOSED

`org/critical_paths/change_management/20261007T0949Z_bbgtml-guard3-checker-tripwire-merge-20261007_deploy_completion.md`

| leg | closed with |
|---|---|
| M1 `git` | the merge `80bcd69f78` at 09:54Z; merged blobs equal the proved blobs; AC1/AC2/AC3 and the battery re-run from the shared tree |
| V1 `verify` | the two live reads above, both arms, both instruments, plus the summons negative control |

**CLOSED -- all 2 legs proven; sentinel removed.** Close commit `d75142de44`;
`deploy_ledger.py check` no longer lists the slug as OPEN. Opened 09:49Z, closed ~11:33Z, inside its
5.0h window.

## 6. Final state and push state

Both edits are live in the shared working tree and have now each been exercised by their own
scheduled task on real data:

| file | live blob | exercised by |
|---|---|---|
| `integrations/bloomberg/pipeline/freshness_check.py` | `cfebeaf6af` | the 11:30Z checker, exit 0 |
| `integrations/bloomberg/pipeline/tplus1/tools/bbg_pkl_tripwire.py` | `b0551c6a59` | the 11:00Z vehicle, pull exit 0 |

**Push state, MEASURED at report time:** everything from this order is **LOCAL**.
`git ls-remote origin CLOUD` is re-read at send time and stated in the covering message; this seat
commits and never pushes, so the push waits on `0.0.0_AB_MSTR~Z` and Andrew's word.

## 7. What remains, and with whom

- **`2.0.0_SA_COO~Z`:** the `<status>` flip on TO-GUARD-3 (and on TO-GUARD-4), and the disposition of
  `OPAL_BBGTML-Z-S12`, whose last unmeasured claim is now measured twice -- by GUARD-4 proof arm C5
  and by section 3 above, in production.
- **Andrew, via `1.0.0_SA_CTO~Z`:** the word that lets the tzero port merge. Until then the hand-run
  send path is covered only by ADDENDUM 7's reading discipline -- run the **tplus1** tripwire on the
  same files first and read its exit code.
- **`0.0.0_AB_MSTR~Z`:** the push; CLOUD is diverged and everything here is local.
- **This seat: nothing owed on TO-GUARD-3.** Both reports are delivered and the ledger is closed.
