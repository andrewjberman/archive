# `battery_ib_s_8.result.md` -- S8-AC1, six arms, 6 of 6

**TO:** `IRPT_BCKEND.TO-IB-s-8` | **cell:** `IB-s-8` (PRD cell B8) | **assignee:** `0.9.0_WK_IRPT_BCKEND~3`
**Branch:** `wk-irpt_bckend-1-3` | **worktree:** `/c/tmp/wk-irpt-1-3` | **base:** `7d7f33569a`

**Invocation (the one the task order names):**
```
timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/battery_ib_s_8.py
```
**rc 0. Last line: `IBS8-RUNNER-BUILT`. Full verbatim output:
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/IB-s-8_S8-AC1_battery_output.txt`.**

---

## The arms

### (a) THE FIVE SURFACES WORK AGAINST THE REPLAY -- `5 of 5`

| surface | verdict | deciding evidence |
|---|---|---|
| `probeSession` on a stale bundle | PASS | `authenticated=False reason=DISTURBED http=403`, legs `identity=PASS cookie=PASS probe=FAIL` |
| `acquireSession` through the replayed login | PASS | steps `CH-SIGNIN_FORM -> CH-AUTHENTICATED`; probe `http_status 200 state LIVE` |
| `persistSession` | PASS | `secret_id=ycharts/session/current fence=1 previous_fence=None puts=1` |
| `getSession` | PASS | `present=True cookies=['ycsessionid','csrftoken','aws-waf-token'] fence=1` |
| `withAuthenticatedPage` | PASS | callback ran on `/dashboard`, `app_shell_elements=1`, work POST `201 CREATED_201` |

**Precondition, and it is the measured one:** `getSession` on the real state of `ycharts/session/current`
returns `present=False reason=NO_AWSCURRENT_VERSION`. That secret exists and has no version; a library that
threw there would be dead on its first real run, so ABSENT is a value in this API and the battery proves it
before it proves anything else.

**Identity evidence is REDACTED by construction:** cookie NAMES, a `sha256_12` prefix and a length. No cookie
value, no credential and no signed URL is printed, logged, screenshotted or written to any artifact.

### (b) NO OTP BRANCH -- two instruments, both non-zero-capable

- **Structural census (handler rows), denominator 4:** `0 of 4 challenge handlers handle a one-time code`.
  `CH-SIGNIN_FORM` / `CH-BLOCKING_OVERLAY` / `CH-AUTHENTICATED` / `CH-UNEXPECTED`, every row
  `handles_one_time_code=False`. The table is MECE by SUBTRACTION: `CH-UNEXPECTED` is *the complement of the
  first three*, so there is no fifth branch to forget.
- **Injected challenges, denominator 5:** `5 of 5 injected unexpected challenges produced an EXPLICIT failure
  record with retried=false` -- `one_time_code -> CHALLENGE_ONE_TIME_CODE_UNSUPPORTED`,
  `captcha -> CHALLENGE_CAPTCHA_UNSUPPORTED`, `waf -> CHALLENGE_WAF_INTERSTITIAL`,
  `password_reset -> CHALLENGE_FORCED_PASSWORD_RESET`, `unrecognised -> CHALLENGE_UNRECOGNISED_SCREEN`.
  **`credential_submits_during_attempt = 1` for every one of the five** -- the measurement that the refusal is
  not a retry loop, taken from the replay's own request log rather than from the library's self-report.
- **Source token census (SECOND instrument, different question), denominator 17 hits across 1000 lines:**
  `{"BLOCK-COMMENT": 11, "LINE-COMMENT": 2, "HANDLER-TABLE": 1, "SIGNATURE-TABLE": 1, "RECORD-FIELD": 2,
  "CODE": 0}`. **CODE-band hits = 0.** The two declarative table ranges are located by reading the source
  (`CHALLENGE_HANDLERS` 191-222, `UNEXPECTED_CHALLENGE_SIGNATURES` 237-242), not assumed.
  An independent third read agrees on the denominator:
  `comp-read infra/aws/ec2/investor-reporting-ycharts/ycharts_session.js --enumerate '(?i)one[- ]?time|otp|verification code|2fa|two[- ]factor'`
  -> `ENUMERATE-END: 17 hit(s) | 7 whole | 10 sub`.

### (c) EVICTION IS BOUNDED -- the difference control

`N` is **declared as 1** (`YC_MAX_REACQUISITIONS`, echoed in every record the library returns).

- **with eviction injected on the work route:** `class=SEAT_EVICTED reacquisitions_used=1 allowed=1
  terminal=True`, replay served 2 evictions.
- **without it, same code path, one variable changed:** `reacquisitions_used=0 work_status=201`.

The injection is route-scoped on purpose: the cheap probe still passes and the runner discovers the seat is
gone on its own work request, which is the shape a person taking the seat actually makes.

### (d) LEASE AND FENCING

- **Two concurrent runners:** `1 of 2 runners holds the lease`. Runner 1 `ok=true fence=1`; runner 2
  `ok=false reason=CONDITIONAL_CHECK_FAILED (lease held by another runner and not expired)` -- the same
  condition the default port issues as a DynamoDB `UpdateItem` against `irpt-jobs`.
- **The fenced-out runner refuses to persist at all:** `class=LEASE_NOT_HELD`.
- **The real fencing case:** runner 1's lease expires mid-session, runner 2 takes it, advances the fence and
  persists; runner 1 returns holding a valid-looking FRESH bundle and a STALE fence, and the WRITE refuses it
  -- `fence 1 write refused against stored fence 2; session secret writes = 1`, `class=FENCED my_fence=1
  stored_fence=2`. One write, not two: the winner's session was not overwritten.

### (e) NOTHING LEFT THE MACHINE

`netguard: 0 external of 1 connection attempts during the suite; replay logged 35 requests; adapter hosts =
127.0.0.1:<ephemeral>`. Non-loopback hosts: `[]`. The replay's request log, denominator 35:
`GET /login/ 10`, `POST /login/ 10`, `GET /indices/table_data 7`, `GET /dashboard 4`,
`POST /custom_pdf_reports/1 4`.

**POSITIVE CONTROL, because a guard that cannot go non-zero is a constant:** the suite then deliberately
attempts `https://ycharts.com/indices/table_data` through the same `https` module the library's default port
uses. `refused=True reached_vendor=False`, guard external count `0 -> 1`, refusal message
`NETGUARD: refused external connection to ycharts.com:443`. The guard can fire, and the zero above is a
measurement rather than a silence.

The two instruments here are genuinely different: the replay log is POSITIVE (what arrived) and is
structurally blind to a request that went elsewhere; the guard sits on the process's own egress and sees
exactly that case.

### (f) SECRETS BY NAME, HOST STOPPED, LEDGER CLOSED

`describe-secret` -- version STAGES only, no value read or printed, denominator 3 of 3 names:

| secret | state |
|---|---|
| `ycharts/login/credentials` | `versions 1, stages ["AWSCURRENT"]` |
| `ycharts/session/current` | `versions 0, stages [], NO_AWSCURRENT_VERSION` |
| `astn/kimi/api-key` | `versions 1, stages ["AWSCURRENT"]` |

`describe-instances i-0167fd745ad906a66 -> State.Name = stopped`, as `aws_ec2_instance_state.runner`
declares. Ledger `20260911T0004Z_irpt-bckend-s8_deploy_completion.md`: `CLOSED=True`, `0` open-leg markers,
sentinel absent from disk. Sentinel and entry commits: `ded9f9741b` (the close, which REMOVES the sentinel --
that removal is the close's own mechanism) and `ff12d98c4d` (the apply, which committed the sentinel in its
OPEN state so the open window is in the record, not only the outcome).

---

## Controls

**MUTANT.** The central claim of arm (b) is `one_time_code_handlers === 0`. Flipping exactly one field in a
copy of the library -- `CH-UNEXPECTED.handles_one_time_code` false -> true -- moves it:

```
BASELINE structural census: denominator=4 one_time_code_handlers=0
MUTANT   structural census: denominator=4 one_time_code_handlers=1
arm-b structural predicate one_time_code_handlers===0 -> false
```

The assertion is therefore tested, not merely satisfied. A second, unplanned mutant fired during development
and is worth recording: the first build of the source token census banded a prose string inside the handler
table as `CODE`, arm (b) read `FAIL`, and the battery WITHHELD `IBS8-RUNNER-BUILT`. The banding was then made
structural (table ranges read out of the file) rather than the threshold being relaxed.

**DETERMINISM.** Two full runs of the battery, compared on the 23 deciding lines: **22 identical, 1 differing
only in the ephemeral loopback port** the replay binds (`127.0.0.1:53895` vs `127.0.0.1:60226`). Every arm
verdict, every denominator and every count is stable. The other deliberately non-stable values -- timestamps
and the `sha256_12` label of a freshly minted fixture cookie -- are excluded from the deciding set by
construction, and are named here rather than left to be discovered.

## What this battery does NOT establish

- **It does not run a real browser.** Playwright is not installed and installing it is egress this order does
  not authorize. Row `IRPT_BCKEND-W3-S1`.
- **It does not replay a captured login.** No supplied HAR contains one. Row `IRPT_BCKEND-W3-S2`.
- **It makes no live vendor call**, by construction and by guard. The live arm is the CTO's L10 read on
  Andrew's explicit per-use word.
