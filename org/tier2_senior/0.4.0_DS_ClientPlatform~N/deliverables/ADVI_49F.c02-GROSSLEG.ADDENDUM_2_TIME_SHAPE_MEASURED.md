# ADVI_49F.c02-GROSSLEG — ADDENDUM 2: the time-shape, MEASURED

**Author** `0.4.0_DS_ClientPlatform~N` · **Written** 2026-08-30 ~01:3xZ · **TO** `ADVI_49F.c02-GROSSLEG`
**Answers** `2.0.0_SA_COO` 84022 item 2 (the one-line dispatch-path ask) · **Corrects** ADDENDUM 1's served-object citation

---

## Why this exists

`2.0.0_SA_COO` 84022 asked this seat for ONE line: *which dispatch path runs `c02_twr_engine` today, and
does the 04:35Z session touch it?* — and stated that until that line lands, **"not tonight" is INFERRED,
not measured**, with the earliest reachable fire believed to be **MON 08-31 22:20Z**.

**That belief is wrong in the direction that matters, and the correction is time-critical.** The next fire
that reaches `c02` is **TODAY, SUN 2026-08-30 at 12:45Z** — measured, not inferred — and it does not append
a new partition, it **overwrites an existing served one**.

---

## 1. THE ANSWER — c02's dispatch path

**`c02_twr_engine.py` has exactly ONE invoker.** Census: `comp-find 'c02_twr_engine'`, **489 hits across
130,910 files scanned, `--corpus all`**, no census headed. The only place it is *executed* is:

```
data/assets/scripts/gold/runners_49f/chain_49f_entrypoint.py:181-186
    ("c02_twr_daily", [sys.executable, "c02_twr_engine.py", "--date", date] + u + m + ...)
```

`c04_validation_battery.py:162` (`from c02_twr_engine import load_policy`) is an IMPORT, not a run.

**And that entrypoint's trigger is NOT any `bd-49f-*` EventBridge RULE.** It is an EventBridge
**Scheduler** schedule — a different API surface, which is why a rules-plane sweep does not see it:

```
aws_scheduler_schedule  advi-49f-gold-floor  (group: default)
    State                 ENABLED
    ScheduleExpression    cron(45 12 * * ? *)   UTC   <- day fields "* * ? *" = EVERY DAY, incl. weekends
    Target                lambda advi-49f-gold-dispatch
    Input                 {"run_class":"production","source":"advi.49f.scheduled-floor"}
    DLQ                   advi-49f-floor-dlq
        |
        v  advi-49f-gold-dispatch (thin Lambda: start host -> wait -> SSM)
        v  SSM doc advi-49f-chain-dispatch  ->  host i-01003b035d2988dfb (bd-gold-layer-runner)
        v  python3 chain_49f_entrypoint.py --production
        v  stage c02_twr_daily
```

- **APPLIED**, read live 2026-08-30T01:2xZ: `aws scheduler get-schedule --name advi-49f-gold-floor
  --group-name default` → the block above.
- **DECLARED**: `infra/aws/terraform/opal-assets/advi_49f_floor.tf:279-291`.
- **APPLIED == DECLARED** on expression, state and target. (STATE axis: this is EXERCISED, not merely
  desired — see §3, where a fire is observed in the artifact.)

## 2. THE 04:35Z SESSION DOES NOT TOUCH c02

Both `bd-49f-*-session-daily` rules target the SAME Lambda, with these live payloads
(`aws events list-targets-by-rule`):

```
bd-49f-insurance-session-daily  cron(35 4 * * ? *)     -> bd-49f-session-trigger  {"mode":"session-refresh","runner":"insurance"}
bd-49f-fees-session-daily       cron(20 22 ? * MON-FRI *) -> bd-49f-session-trigger  {"mode":"session-refresh","runner":"fees"}
```

`bd-49f-session-trigger` is the **Black Diamond cookie re-auth chain head**, not a gold dispatcher
(`infra/aws/lambda/bd-pipeline/bd-49f-session-trigger/lambda_function.py:1-27, 370-375`). Its three modes
are `session-refresh` / `runner-run` / `session-check`, and `runner-run` **invokes the `bd-49f-runner`
Lambda** (BD bronze ingest reading the freshly-minted cookie). **Neither `c02_twr_engine` nor
`chain_49f_entrypoint` appears anywhere in that file.**

> **So the answer is: no. The 04:35Z insurance session cannot reach c02** — and the argument does not
> depend on reading that Lambda exhaustively, because §1 established that the ONLY executor of c02 is
> `chain_49f_entrypoint.py`, which this Lambda never invokes.

## 3. ⛔ THE NEXT FIRE IS TODAY 12:45Z, NOT MON 22:20Z

**First, the weekday.** 84022 says *"Today is SAT 2026-08-30"*. **2026-08-30 is a SUNDAY.**

```
2026-08-28  Friday      2026-08-29  Saturday      2026-08-30  Sunday (TODAY)      2026-08-31  Monday
```

**The floor fires daily including weekends, and this is OBSERVED, not read off a cron:**

```
gold/advi/canonical/twr_daily/date=2026-08-28/data.parquet   LastModified 2026-08-29T12:47:01Z   301,833 B
```

`date=2026-08-28` was written at **12:47:01Z on SATURDAY 2026-08-29** — the 12:45Z floor firing on a
weekend, +2 min of chain runtime. The weekend fence lives in the CHAIN's date derivation, never in the
cron, so a weekend fire still runs; it just resolves to a weekday date.

**Time from this writing (01:3xZ Sun 08-30) to the next fire: ~11 hours.**

## 4. ⛔ AND IT IS AN OVERWRITE, NOT AN APPEND

`--production` derives `D = prev_trading_day(now)` (`chain_49f_entrypoint.py:429-433`). Run against the
estate's own calendar (`lib/trading_calendar.py` — NEVER#1 resolved before any staleness claim):

```
fire SUN 2026-08-30 12:45Z  ->  D = 2026-08-28     <- ALREADY EXISTS
fire MON 2026-08-31 12:45Z  ->  D = 2026-08-28     <- THE SAME DATE AGAIN
fire TUE 2026-09-01 12:45Z  ->  D = 2026-08-31     <- the first NEW date
```

**`date=2026-08-28` currently has exactly ONE version** (`list-object-versions` on
`.../date=2026-08-28/data.parquet` → 1 row, `IsLatest=true`, 2026-08-29T12:47:01Z), written by the
Saturday fire **using the pre-fix code** — the fix did not reach `_code/` until 22:02Z that night.

**And the emit path has no existence guard:**

```
data/assets/scripts/gold/runners_49f/runner_common.py:123-125
    if upload:
        s3().put_object(Bucket=GOLD_BUCKET, Key=data_key, Body=payload)     <- unconditional
```

`c02_twr_engine.py`'s only `exists()` is `:401 bmv_loaded` (a BMV lookup, not a write guard).

> ⛔ **CONSEQUENCE, stated plainly: at 12:45Z today the SERVED `date=2026-08-28` partition is overwritten
> in place, its `r_gross` column flipping sign, while the other 533 stored partitions keep the inverted
> one.** This is a sharper shape than the one cell §4 was deferred against. The hazard there was *a new
> partition arrives carrying a different convention*; the actual hazard is **an existing served partition
> silently changes value**, with `schema_version` still `"1.0"` and no gross-leg vintage field to
> distinguish before from after. A consumer that read 08-28 yesterday and reads it tomorrow gets two
> different numbers under one key, with nothing in the artifact recording that anything happened.

## 5. ADDENDUM 1's SERVED-OBJECT CITATION IS NOW STALE — and reads like a revert if you diff the ETag

ADDENDUM 1 (and 84022 item 4, which carries it forward) cites the deployed code object as
**ETag `2f709fc66ed6cb2e9a853704ef0e83c6`, 2026-08-29T22:02:12Z**. Measured now:

```
                              size     md5 / ETag
s3 _code/ object  (NOW)      28,557    a82eb86bfc0a064ae8a4cce6653746a1   LastModified 2026-08-29T22:54:44Z
git blob HEAD:<engine>       28,557    a82eb86bfc0a064ae8a4cce6653746a1   <- BYTE-IDENTICAL to the served object
local worktree file          29,016    2f709fc66ed6cb2e9a853704ef0e83c6   <- what ADDENDUM 1 hashed
worktree with CRLF -> LF     28,557    == the served object exactly       (459 CR bytes; git reports the file CLEAN)
```

**The difference is line endings and nothing else.** A second deploy at 22:54:44Z replaced the CRLF
working-tree upload with the LF committed bytes. **The fix STANDS on the served plane** — verified
semantically on the downloaded bytes, both arms:

```
site 1  cf["cf_gross"] = cf["cf_net"].add(fee_cf...)      PRESENT      broken form (-fee_cf)   ABSENT
site 2  "cf_gross": fee_cf.loc[only_fee]                  PRESENT      broken form (-fee_cf)   ABSENT
```

⚠ **Why this correction is worth its space rather than a shrug:** a seat comparing the recorded ETag to
the live one gets a MISMATCH on an object whose rollback was the live question hours earlier, and the
available reading is *"someone reverted the fix."* I nearly filed that. **A digest without its
normalisation is not an identity** — record the git blob hash beside the ETag, or the record ages into a
false alarm.

## 6. WHAT THIS DOES NOT DECIDE, AND WHAT I DID NOT MEASURE

**Not mine and not decided here:** the re-emission range (cell §4, `2.0.0_SA_COO` as issuer), the
serve-gate limb (`1.0.0_SA_CTO`), and whether today's fire should be allowed to land. Halting or
re-pointing a live production schedule is an infra act in a DT/AE lane (Rule 13) and a served-output move
needing never-widen sign-off (CTO+COO) — **this seat is not proposing a gate and has implemented none.**
Andrew's ruling (*"id rather we just keep pushing forward, i dont want to rollback anything lets just push
on"*, relayed 0.0.0_AB_MSTR 83984) disarmed the rollback question; **it did not rule on the range, and it
was given before this time-shape was measured.**

**Residuals, named rather than papered over:**
1. I read the **schedule**, not the deployed bytes of `advi-49f-gold-dispatch` or the SSM document. A
   dispatcher that fails would make today's fire a no-op — I have not excluded that, and its most recent
   observed behaviour is a SUCCESS (§3).
2. The §2 conclusion rests on the **repo source** of `bd-49f-session-trigger`, not its deployed bundle.
   The §1 census makes that limb non-load-bearing, but the grain is stated.
3. Whether any surviving campaign leg on `i-01003b035d2988dfb` can run the chain off-schedule.
   `0.7.0_AE_CloudOps` owns that host.

---

**Instruments:** `comp-find` (`--corpus all`, denominators printed, no census headed) · `aws scheduler
get-schedule` / `events list-targets-by-rule` / `s3api list-objects-v2` / `s3api list-object-versions`
(UTC via `s3api`, never `s3 ls`) · `lib/trading_calendar.prev_trading_day` · `git cat-file` blob-vs-object
digest with CRLF normalisation · source read at `file:line`.
