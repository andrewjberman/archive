# EG-s-19 -- THE CATCH-UP BRANCH DRIVEN, NOT AWAITED

**Worker:** `0.9.0_WK_ETFS_GUARDRAIL~5` · **TO:** `ETFS_GUARDRAIL.TO-EG-s-19` · **cell:** `EG-s-19` · **outcome_ref:** FWD-1
**Branch:** `wk-etfs_guardrail-3-5` (worktree `/c/tmp/wk-etfs-3-5`, cut from CLOUD at `ea47e92a72`) · **never pushed**
**Face proved against:** the AMENDED face @`b6adbaf70c` (arms (d) and (g) re-cut on rows `W5-S3` and `W5-S1`)

---

## THE HEADLINE

**The catch-up branch ran, and it found the hole by itself.** It had never once run in this estate.
`EG-s-17` filled the only real hole that existed and closed honestly with `CATCHUP-BRANCH-NOT-EXERCISED`,
because that hole was the NEWEST priced partition and `_catchup_missing_dates` skips the newest as
`skip_date`. So the recovery mechanism FWD-1 rests on had never been observed working.

One served slice was archived, deleted on Andrew's own word, and the producer -- fired in its own rule's
scheduled shape, with no `date` key -- walked its reporting-obligation window, found the gap, and refilled
it. The log's own line, at 03:45:38.391Z:

```
CATCHUP: processed 2026-09-03 (status=ok)
```

and the response carried `catchup_processed: ["2026-09-03"]` while its own `date` field read `2026-09-08`,
so the recovery was on the CATCH-UP path and not the main path. **The restored slice is byte-identical to
the one that was deleted** -- source, archive and restored all carry sha256
`060188a6e76b2275538e9cb2de0244023600ccfaa713fa738d6f24e2eb757cc8`.

---

## WHAT I MEASURED, WITH DENOMINATORS

| quantity | value | instrument |
|---|---|---|
| `opal-data-etfs` versioning | **DISABLED** -- `get-bucket-versioning` returns EMPTY at rc 0 | re-derived, not inherited |
| non-trading days 2026-08-28..09-10 | **3**, not 2: 09-05 (Sat), 09-06 (Sun), 09-07 (Labor Day) | `lib/trading_calendar.py` `is_trading_day`, 14 of 14 days enumerated |
| upstream `fact_holdings` partitions | 68; newest = **2026-09-08** | `list-objects-v2 --delimiter /` |
| `daily/cottonwood/` slices | **62 before, 62 after** | `s3api list-objects-v2` |
| `daily/` (both partners, every key) | 273 before, 274 after (+1 = my archive) | same |
| keys whose CONTENT changed under `daily/` | **0 of 273** compared on both sides | ETag + Size, per key |
| keys removed | **0 of 273** | same |
| rule targets | **1 of 1**, with all 3 of 3 override keys ABSENT | `list-targets-by-rule` |
| `START RequestId` in the fire window | **1 of 1** over 7 events, 1 request id | `filter-log-events`, read BY TIME |
| SES sends in the run window | **0 datapoints, Sum 0 on 3 of 3 metrics** | `AWS/SES` Send / Delivery / Reputation.BounceRate |
| mailer tokens in the DEPLOYED bytes | **0 hits** | package download + regex census |
| `ses:` actions on the producer role | **0** across 3 of 3 policies | `iam get-role-policy` |

---

## THE CHOICE OF DATE -- and the dates I REJECTED

The issuer's own hand-listed set of non-trading days was incomplete and said so, so I enumerated the
calendar myself rather than inheriting it from anyone.

| date | trading day | slice present | upstream partition / priced (the producer's OWN probe) | newest? | outcome |
|---|---|---|---|---|---|
| **2026-09-03** | True | yes, 1345 B @ `2026-09-05T10:30:30.000Z` | `partition: true`, `priced: 11947` | no | **TAKEN** |
| 2026-09-08 | True | yes | `partition: true`, `priced: 12016` | **YES** | **REJECTED** -- `_latest_partition()` returns it, so it is `skip_date` and the catch-up loop `continue`s past it at `:268-269`. This is exactly the dead end `EG-s-17` closed on; deleting it would have reproduced that null result. |
| 2026-09-05 | **False** | no | `partition: false`, `priced: 0` | no | **REJECTED** -- not a trading day, so its absence is CORRECT. Nothing to delete and nothing to prove. |
| 2026-09-09 | True | no | `partition: false`, `priced: 0` | no | **REJECTED** -- upstream has not landed (D+1 race, class D). The producer **could not re-derive it**, so a hole there would be permanent damage against a bucket with versioning disabled. |
| 2026-09-04 | True | yes, 1345 B | `partition: true`, `priced: 12033` | no | **ELIGIBLE, NOT TAKEN** -- deliberately kept intact to serve as the 200 positive control beside the 404, and 09-03 sits further from the newest partition so the exclusion is unambiguous. |

**The window the run actually used**, re-derived rather than assumed: `_window_dates` starts at the PRIOR
month's 1st only while that month's report has NOT shipped. I measured
`s3://opal-data-etfs/platinum/reports/2026-08/etf_ownership.pdf` -> rc 0, 252393 B, `2026-09-10T00:24:48Z`
= **SHIPPED**, so the window started `2026-09-01` and ran through `today-1`. Note **UTC was already
2026-09-10** when the producer ran (local was 09-09), so `today-1` = `2026-09-09`, giving
`['2026-09-01','2026-09-02','2026-09-03','2026-09-04','2026-09-08','2026-09-09']` -- 6 dates. 2026-09-03 is
in the window on EITHER branch of the shipped test, so the choice is robust to it.

---

## THE ACT, IN THE SPINE v3.9 ORDER

| # | act | UTC | evidence |
|---|---|---|---|
| 1 | change-management entry **OPENED** | 03:40:42Z | `20260910T0340Z_etfs-guardrail-egs19-catchup-driven-20260910_deploy_completion.md`, 6 legs |
| 2 | slice read, sha256'd | 03:45:20Z | `060188a6...757cc8`, 1345 B |
| 3 | **ARCHIVE** copied, read BACK, verified byte-equal | 03:45:22-26Z | archive sha256 identical |
| 4 | **DELETE** (exactly one object) | 03:45:26Z | rc 0 |
| 5 | 404 on the hole beside 200 on the neighbour | 03:45:31-34Z | rc 255 `(404) ... Not Found` / rc 0 |
| 6 | **FIRE** in the rule's scheduled shape, no `date` key | 03:45:34Z | StatusCode 200, RequestId `fdc655fd-08fd-4b1b-b58f-ad6199f9396e` |
| 7 | slice RESTORED | 03:45:39Z | poll **1 of a 30-poll / 15-minute bound** |
| 8 | entry **CLOSED**, all 6 legs proven | 03:48:57Z | `deploy_ledger.py close` rc 0 |
| 9 | carried detail appended (row `W1-S16`: after the final ledger mutation) | 03:5xZ | +6346 B |
| 10 | entry + evidence **COMMITTED** | -- | `abba4a2d68` |
| 11 | **then** the grading reads | 04:02Z onward | this battery |

**The rollback was NOT needed and NOT run.** The archive is RETAINED as the standing rollback:

```
.tools/aws s3api copy-object --bucket opal-data-etfs \
  --key daily/cottonwood/2026-09-03.json \
  --copy-source opal-data-etfs/daily/_archive/cottonwood/2026-09-03.20260910T034042Z.json
```

---

## EACH CRITERION -- INVOCATION AND OUTPUT

### S19-AC1 -- PASS by output

**Invocation:**
```
timeout 900 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~5/test_egs19_catchup_driven.py
```
**rc 0.** Deciding output, verbatim:
```
  ARMS PASSED: 8 of 8

EGS19-CATCHUP-BRANCH-DRIVEN
```
Denominator: **8 of 8 arms**, (a)-(h), every one printed with its own evidence and denominator.

Per-arm deciding lines (full transcript in the battery's own output):

- **(a) THE CHOICE** -- 14 of 14 calendar days enumerated, 3 non-trading; 68 upstream partitions, newest
  `2026-09-08`; four properties printed for the taken date and for 4 rejected/held-back dates.
- **(b) THE ARCHIVE** -- source and archive sha256 IDENTICAL; entry opened `20260910T034042Z` < delete
  `20260910T034526Z`; entry closed with all 6 legs proven.
- **(c) THE HOLE EXISTED** -- `rc 255`, stderr verbatim
  `An error occurred (404) when calling the HeadObject operation: Not Found` at 03:45:31Z, beside
  `rc 0` on `2026-09-04` at 03:45:34Z in the same call sequence.
- **(d) THE FIRE IS THE RULE'S SHAPE** -- (d-i) 1 of 1 target, `Input`/`InputPath`/`InputTransformer` each
  printed ABSENT; (d-ii) payload 9 of 9 default-envelope fields, 0 extra, no `date` key; (d-iii)
  branch-equivalence quoted at `lambda_function.py:300-312 @ea47e92a72`; 1 of 1 `START RequestId`.
- **(e) THE BRANCH RAN AND FOUND IT ITSELF** -- exactly one `CATCHUP:` line, and it names `2026-09-03`;
  `catchup_processed == ["2026-09-03"]` while `date == "2026-09-08"`; catch-up write 446 ms after the
  main-path write.
- **(f) THE SLICE IS BACK** -- head-object 200, 1345 B; a second independent reader counts 4 non-zero rows;
  restored == archived == original on sha256, **0 of 32 field-level differences**.
- **(g) NOTHING ELSE MOVED** -- 0 of 273 keys changed content, 0 removed, 1 added (my own archive); the 1
  necessarily re-PUT key enumerated by name with both ETags EQUAL; `daily/cottonwood/` 62 -> 62.
- **(h) ZERO SES SENDS** -- three independent instruments, all zero (below).

### S19-AC2 -- RECORDED (judgment), NO VERDICT

`judgment="true"`; graded by `3.0.0_SA_CVO` at L9. Evidence, with vintage:

1. **Did the catch-up branch recover a hole it discovered itself?** The log's own lines,
   `/aws/lambda/cot-etf-ownership-daily` read BY TIME over `[1789011904244, 1789012204244]`, request
   `fdc655fd-08fd-4b1b-b58f-ad6199f9396e`:
   - `03:45:37.943Z OK: wrote s3://opal-data-etfs/daily/cottonwood/2026-09-08.json (4 ETF slices, total_ownership=53641351.75, source_as_of=2026-09-08, ...)` -- the MAIN path on the newest partition.
   - `03:45:38.389Z OK: wrote s3://opal-data-etfs/daily/cottonwood/2026-09-03.json (4 ETF slices, total_ownership=53750650.53, source_as_of=2026-09-03, ...)`
   - `03:45:38.391Z CATCHUP: processed 2026-09-03 (status=ok)`
   The date was never supplied to the producer: the payload carried no `date` key, so the explicit-date
   branch at `:304-308 @ea47e92a72` was unreachable and the date was DISCOVERED by `_catchup_missing_dates`
   walking its window and finding `_output_exists("2026-09-03")` false with `_partition_exists` true.
2. **What does the restored slice differ in?** **Nothing.** sha256 equal across original, archive and
   restored; 0 differences over 4 tickers x 8 fields; ETag `212d7da63d847fd3f25facd6a651b481` on all three.
   This is a byte-identical re-derivation, not merely an equivalent one -- which is the strongest available
   answer to "faithful re-derivation or drift", and it is what one expects from `_process_date`, whose
   output is a pure function of the partition and the universe config (no `generated_at` in the rows; the
   timestamp appears only in the log line).
3. **What would the branch have done had the upstream partition been absent?** It would have skipped the
   date silently and written nothing: `_catchup_missing_dates` at `:272-273` does
   `if not _partition_exists(date_str): continue` -- the "never fabricate" skip. I did not have to reason
   about this hypothetically: **`2026-09-09` is exactly that case in the same window**, and the run's own
   response proves the behaviour -- `catchup_processed: ["2026-09-03"]`, `catchup_failed: []`,
   `catchup_skipped_unpriced: []`, with 09-09 appearing in none of the three lists. A date with no upstream
   partition is not merely unprocessed; it is INVISIBLE in the response, which is worth the CVO's attention
   because a silent skip and a healthy day are indistinguishable to any consumer reading only that response.
4. **What this exercise still does NOT prove.** Named honestly:
   - **A MULTI-DAY GAP.** Exactly one date was deleted, so the loop was exercised with one recoverable
     member. Nothing here shows behaviour when several dates are missing at once -- in particular whether a
     `_process_date` failure mid-loop leaves later dates unattempted (the `try/except` at `:274-281` says
     it should not, but that is a code read, not an observation).
   - **A MULTI-PARTNER GAP.** Only `cottonwood` was exercised. `bd-49f-etf-ownership-daily` is a separate
     function with its own ported loop; nothing here transfers to it by measurement.
   - **THE SCHEDULED FIRE ITSELF.** I invoked the producer directly with the rule's envelope shape. The
     rule's own 10:30Z cron delivery was not observed; what is proven is that the target carries no payload
     override, so the delivered envelope is the default one, and that the handler's branch selection depends
     only on the absence of `date`/`probe`.
   - **A GAP OLDER THAN THE WINDOW.** The window began `2026-09-01` because August's report has shipped. A
     hole in a shipped month is outside the window by design and would not have been found.
   - **RECOVERY UNDER CONTENTION.** One fire, one hole, no concurrent producer run.

---

## ANDREW'S ~02:5xZ CONSTRAINT -- PROVEN ON THREE INDEPENDENT INSTRUMENTS, NOT ASSERTED

His word was *"Call 1, yeah try it but make sure no test run hits aj's email, that is not appropriate."*
Both halves bind. The delete has his word. The no-mail half is proven on three planes that fail
independently:

1. **THE DEPLOYED BYTES.** `get-function` -> the package holds **1 of 1** file, `lambda_function.py`,
   sha256 `667c2c720268da03b215cf47b7520e3e2445d9a041715a40ed1bd7f423e63e1c`, **byte-identical** to the repo
   source (LF-normalised). Mailer-token census over those deployed bytes
   (`ses|sesv2|send_email|send_raw_email|sns|boto3.client('ses`): **0 hits**. This producer has no mailer on
   any path -- it contains no send call at all.
2. **THE ROLE**, a different plane from the code. `cot-etf-ownership-daily-role` carries 1 managed
   (`AWSLambdaBasicExecutionRole`, logs only) + 2 inline (`cloudwatch-metrics`, `s3-etf-ownership`) =
   **3 of 3 policies with 0 `ses:` actions**. It could not send if the code tried.
3. **THE WINDOW ITSELF.** `AWS/SES` `Send`, `Delivery`, `Reputation.BounceRate`, Sum, period 300, over
   03:35:34Z-03:50:44Z: **0 datapoints and Sum 0 on 3 of 3**, both at act time and on a live re-read.

**WHAT I DID NOT DO:** I did not invoke `etfs-reports-orchestrator` -- the one component whose mailer
reaches aj@ -- in any mode, at any point, for any reason. I made no code change and no deploy; the producer
ran AS DEPLOYED. I deleted exactly one object and made no second delete of any kind. I built no alarm,
monitor, topic or schedule. I did not push, merge or rebase.

---

## CONTROLS

**MUTANT -- FIRED.** A passing assertion never mutated has never been tested. The battery was copied to
`.scratch/mutant_battery.py` with one constant changed: `HOLE = "2026-09-03"` -> `"2026-09-02"`, a slice that
was never deleted and never recovered by the catch-up path. Result: **rc 1, ARMS PASSED 5 of 8, `TOKEN
WITHHELD -- 3 arm(s) failed`**; arms **e, f, g** flipped to FAIL. The token is therefore not a constant --
the battery can and does return non-zero on a false claim.
**Stated limit of this mutant:** arms b, c and d still PASSED under it, because they resolve against the
evidence ledger's own recorded key names rather than against the `HOLE` constant. So this mutant
discriminates the three arms that carry the cell's actual claim (the branch ran, the slice is back, nothing
else moved) and does NOT exercise the three ledger-keyed arms. Naming that is more useful than a mutant
that appears to test everything.

**DETERMINISM -- STABLE.** Two full runs of the final battery, diffed with only the `run at <UTC>` header
line excluded: **`diff` rc 0, 0 lines of difference**.

**DISCRIMINATION ON THE `1 of 1 START` CLAIM.** The fire window showed one unmatched `INIT_START` at
03:48:44Z with no `START` beside it, which could have meant a second, unaccounted invoker. I widened the
read to 03:00Z-04:10Z (49 events, 4 streams) rather than leaving it: every other `START` in the hour is one
of my own probe invokes (7 at 03:31, 1 rehearsal at 03:43, 5 from the battery at 04:02), and the 03:48:44Z
line is a bare execution environment that initialised and never served an invocation. An `INIT_START` is
not an invocation, and **no invoker other than this seat touched the function in that hour.**

---

## SURPRISE ROWS FILED -- three, all at `fa48ac5a0e`

All three were found by reading the producer's source, not by failing an arm. **The issuer re-cut the face
on two of them** (@`b6adbaf70c`) and ruled the third; this document proves against the AMENDED face.

- **`ETFS_GUARDRAIL-W5-S1`** (OBSERVATION / INERT) -- arms (d) and (g) were **jointly unsatisfiable**. Arm
  (d) mandates the rule's own shape; arm (g) forbade any other `daily/` key from changing. But the handler
  ALWAYS re-computes and re-PUTs the newest slice at `:310-311` BEFORE `_catchup_missing_dates` at `:312`,
  so a second key is written on every scheduled-shape fire by construction. Measured:
  `daily/cottonwood/2026-09-08.json` ETag `5da999e2fbfadfe302df35ef24407372` and Size 1345 identical on both
  sides -- a timestamp touch on identical bytes. **Issuer's ruling: cut defect, arm (g) re-cut to measure
  CONTENT and to require the re-PUT keys be enumerated by name.**
- **`ETFS_GUARDRAIL-W5-S2`** (OBSERVATION / INERT) -- the face reasons no census can see the archive prefix.
  True for every producer and consumer measured (the producer's role cannot even LIST it), but a repo census
  (16 hits across 153,347 files) found one bare-`daily/` enumerator on this bucket inside this project --
  `0.9.0_WK_ETFS_GUARDRAIL~1`'s round-1 battery, whose printed denominator moved 273 -> 274. Recorded INERT
  because that battery's only ARM filters `LastModified` on a `2026-09-10T01:` prefix and the archive is
  stamped 03:45:24Z. **Issuer's ruling: INERT accepted on this reasoning; carried to the CTO and CVO as a
  PERMANENT condition, since versioning is disabled and the archive cannot be removed.**
- **`ETFS_GUARDRAIL-W5-S3`** (OBSERVATION / INERT) -- "byte-equal to the rule's delivered envelope" is
  unsatisfiable for any payload: EventBridge stamps a per-delivery UUID `id` and `time`, so two deliveries
  of the same rule are not byte-equal to each other, and the producer never logs its `event`. I refused to
  write "byte-equal" into a proof-of-spec line where it would have been false and proved the reachable
  property instead. **Issuer's ruling: cut defect, arm (d) re-cut to three measured facts.**

---

## ARTIFACTS

| path | what |
|---|---|
| `org/critical_paths/change_management/20260910T0340Z_etfs-guardrail-egs19-catchup-driven-20260910_deploy_completion.md` | the NEVER-2 entry: 6 legs, all proven; slice, archive, both sha256s, the rollback; carried detail appended after `close` |
| `.../deliverables/0.9.0_WK_ETFS_GUARDRAIL~5/egs19_evidence.json` | the act driver's verbatim record: 17 commands with argv, rc, stdout, stderr and UTC; the payload fired; the poll trail; before/after inventories |
| `.../deliverables/0.9.0_WK_ETFS_GUARDRAIL~5/test_egs19_catchup_driven.py` | the S19-AC1 battery, 8 arms |
| `.../deliverables/0.9.0_WK_ETFS_GUARDRAIL~5/egs19_daily_etag_census.json` | every key under `daily/` with its before/after ETag, Size and LastModified -- so arm (g-i)'s "every key" is literally available, not merely counted |
| `.../deliverables/0.9.0_WK_ETFS_GUARDRAIL~5/the-catch-up-branch-driven.result.md` | this document |
| `s3://opal-data-etfs/daily/_archive/cottonwood/2026-09-03.20260910T034042Z.json` | the standing rollback (RETAINED) |

## PUSH STATE

`git ls-remote origin refs/heads/CLOUD` -- measured and stated in the worker report. Everything above is
**LOCAL** on `wk-etfs_guardrail-3-5`. This worker never pushed, merged or rebased.
