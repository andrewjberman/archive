# Never-widen ask -- OG-bf-1 leg Y, the 49F dispatcher date gate (deploy by 0.7.0_AE_CloudOps~Z)

By: `0.9.0_WK_NFRA_OPLGTW~41` (PHASE C, build only: no deploy, no apply), 2026-10-09. Order:
`org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-bf-1.closure-marker-backfill-13m.md`, amendment A1.
Design ruled by `1.0.0_SA_CTO~O`: `deliverables/1.0.0_SA_CTO~O/NEVER_WIDEN_HALF_CTO_OG-bf-1_20261009.md` @f9b1f1fd31
section 2. First ask: `NEVER_WIDEN_ASK_OG-bf-1.md` (sections 3 and 5 give the reason).

**Halves owed on the deploy leg:** `1.0.0_SA_CTO~O` and `2.0.0_SA_COO~O`, against THIS file at its commit. The design
is already ruled; these halves sign the act (the apply and its blast radius).

## 1. The change (one Lambda, code only)

`advi-49f-gold-dispatch` (`module.advi_49f_gold_dispatch`, `infra/aws/terraform/opal-assets/advi_49f_floor.tf:186`).

| member | before | after |
|---|---|---|
| `lambda_function.py` | 14017 bytes, sha256 `5b91c217532ea032b2fed5ea4278f77b5d262ace2ec3db54693a13377c815a42` (at HEAD) | 16904 bytes, sha256 `a524977a86caff1463c2c306f683fba40286dd44ddb8fbe6f62eb1ed0bec9990` |
| `trading_calendar.py` | absent | 12897 bytes, sha256 `8ec8e43def5854f67a0dadcef7c735906f44aa07ae5916b2fc62c4c81ca9a3a8`, a byte copy of `lib/trading_calendar.py` (a test pins the equality) |

**The rule, inside the existing accelerator branch, after the qualified check and before any EC2 or SSM call.** Parse
`date=YYYY-MM-DD` from the decoded key of the exact marker version. Compare it with
`trading_calendar.prev_trading_day(now UTC)`, the expression `chain_49f_entrypoint.py --production` uses at
`:534`. If they differ, return `dispatched: false` with
`skip_reason: "accelerator marker date=<D> is not the production T-1 <T>; historical record, not dispatched"` and print
`SKIP:`. A key with no date, or a calendar that cannot answer (not loadable, or `CalendarCoverageError`), also SKIPs.
The calendar loads by path beside `lambda_function.py` inside a `try`, so a missing or broken calendar can never stop the
floor path from importing the module.

**Behaviour, by event class (the third row is the daily case; rows 4 and 5 are new SKIPs of what used to dispatch):**

| event | before | after |
|---|---|---|
| floor (`source: advi.49f.scheduled-floor`) | dispatches | unchanged; never reaches the gate |
| accelerator, record not `qualified` | SKIP | unchanged; SKIPs on the qualified check first |
| accelerator, qualified, date == production T-1 | dispatches | dispatches (the daily case) |
| accelerator, qualified, date != production T-1 | dispatches today's T-1 chain | **SKIP** |
| accelerator, calendar unreadable or key undated | dispatches | **SKIP** |

**This narrows the accelerator; it widens nothing.** What it can newly withhold is a daily dispatch for a record that
lands more than a trading day late (for example Monday's date landing on Wednesday). Before, that record ran Tuesday's T-1
chain, not Monday's; the floor `cron(45 12 * * ? *)` is untouched and remains the production trigger (the notification
block's own comment: the accelerator is "an accelerator only"). The T-1 is computed at dispatch; the chain computes its
own up to a few minutes later when the host starts, so a record dispatched within minutes of 00:00Z could disagree. The
daily markers are written about 09:46Z, so this is not reached in practice.

**What this ask does NOT change:** the notification set, the Lambda permission, the IAM role, the environment (5 keys:
`POLL_BUDGET_S`, `HOST_INSTANCE_ID`, `SSM_DOCUMENT_NAME`, `CHAIN_LOG_BUCKET`, `CHAIN_LOG_PREFIX`), the timeout (900),
memory (256), the SSM document, the schedules, any gold object.

## 2. Evidence built here (Phase C)

- Tests: `infra/aws/lambda/opal-assets/tests/test_advi_49f_gold_dispatch_dategate.py`, `test_ogbf1y_ac01` to `ac04`, plus
  `test_packaged_calendar_is_byte_copy`. EC2, SSM and S3 are mocked; "now" is pinned. They cover: a far-historical and a
  recent historical qualified record SKIP with no `describe_instances`, `start_instances`,
  `describe_instance_information` or `send_command` call; the production T-1 (a Monday morning, so a weekend between) and a
  mid-week T-1 dispatch once; both unreadable-calendar arms SKIP; an `incomplete` record SKIPs on the qualified check with
  the gate never consulted; the floor path dispatches with the calendar absent and the gate never consulted.
- The existing `tests/test_advi_49f_gold_dispatch_remedy.py`: 0 tests removed or renamed, no assertion changed. One test
  needed a fixture: `test_qualified_marker_dispatches_once` failed unpinned (its marker date 2026-09-25 is not today's
  T-1; `send_command` count 0 != 1). The fix is one added patch in `setUp` pinning the module's `_utcnow` to
  2026-09-28 09:50Z (production T-1 = 2026-09-25) plus its import line. The other 5 pass unpinned.
- Run: both files together, 11 passed (`python -m pytest ... -q`).

## 3. Before and after, and the rollback

- **Before (live, read 2026-10-08):** `CodeSha256 TjIWGFWkbUswLkA+mUac9NS+LRZ1q7o6lR1iQLb0kI4=`, 5513 bytes, last modified
  2026-09-29T03:12:40Z, S3 artifact `opal-313476888478-lambda-artifacts/opal-assets/advi-49f-gold-dispatch.zip`
  version `AQ2rQSyBdPpB0sWozwovunpWoL9TWVYA` (latest). That version IS the rollback artifact.
- **After:** the built zip's `CodeSha256`. **I did not build it:** the builder
  (`infra/aws/lambda/ci/build-and-upload.sh`) refuses a top-level `.py` that is not in
  `functions["advi-49f-gold-dispatch"].files` of `infra/aws/lambda/ci/lambda-source-map.json` (the ADHC_DRIFTD.002 parity
  check, lines 412-458), and a build rewrites that file; neither is in my write grant. The deploy leg registers
  `trading_calendar.py` there (a one-entry edit, in its own commit), builds, and records the printed `CodeSha256` here as
  the "after". The two member hashes above are what the zip's members must equal.
- **Rollback:** point the function back at artifact version `AQ2rQSyB...` (hash `TjIWGFWk...`) by the same Terraform
  path (`s3_object_version` and `source_code_hash`), then read `CodeSha256` back equal to `TjIWGFWk...`. Nothing else
  changed, so nothing else needs undoing.

## 4. The deploy path (for `0.7.0_AE_CloudOps~Z`, not for me)

1. Register `trading_calendar.py` in the source map's `files[]`; build (`--build-only` first); confirm the zip holds
   exactly `lambda_function.py`, `trading_calendar.py` (plus the builder's `BUILD_MANIFEST.json`) and that both member
   hashes equal section 1.
2. Open a NEVER-2 ledger (`.tools/deploy_ledger.py open --lambda advi-49f-gold-dispatch ...`), commit the entry and sentinel.
3. Plan through `module.advi_49f_gold_dispatch`: expect 1 resource changed, only `source_code_hash`,
   `s3_object_version` and `last_modified`; the 5-key environment unchanged. Any other row is a stop. Apply through
   `.tools/safe-apply.sh`, never `aws lambda update-function-code`.
4. Read back `CodeSha256` equal to the built hash, `State Active`, `LastUpdateStatus Successful`, a post-apply plan reading
   `No changes`. Close the ledger and commit before any proof.

## 5. The proof, both arms on the deployed function

- **Arm 1 (historical SKIPs), on demand, no host effect.** Invoke the deployed function once with a synthetic S3-shaped
  event naming an existing QUALIFIED historical version, for example
  `schwab/08335338/meta/complete/date=2026-09-15.json` at VersionId `ReevhBJRXCWNerbIirOWCfJG5G_Ewqc1` (the OG-c-2
  record; the dispatcher role may read it). Expect `dispatched: false`, `skip_reason` ending "is not the production T-1
  <T>; historical record, not dispatched". The function's own log for that RequestId carries `SKIP:` and no
  `dispatched: doc=` line; `ssm list-commands` for the document and the host's state are unchanged across the call. The
  record is read, nothing is written.
- **Arm 2 (the daily T-1 record dispatches as today).** Offline, `test_ogbf1y_ac02` already covers it. On the deployed
  function, the organic proof is the next daily marker: about 09:46Z the producer writes the previous trading day's
  record, and the dispatcher log for the qualified version must read `OK: accelerator fire on marker key=...date=<T-1>` and
  `dispatched: doc=advi-49f-chain-dispatch`. If the halves want it on demand instead, a synthetic event naming the newest
  qualified T-1 record would run the production chain once, which is a served-output move the same as a floor fire; that
  needs its own line in the signed halves. I recommend the organic read.

## 6. What this unlocks

With the gate live, a qualified record for a historical date on `schwab/08335338/meta/complete/` hits the SKIP branch, so
the 08335338 backfill (Phase D) causes no host start, no SSM command, and no gold write per record. Phase D still needs its
own pair of halves on the 08335338 write set, as the CTO half says.

## 7. Halves

**COO -- owed:** `2.0.0_SA_COO~O`. **CTO -- owed:** `1.0.0_SA_CTO~O`. Each should name: that the "after" `CodeSha256` is
recorded by the leg, not known here; the Arm 2 choice in section 5; and that the source-map registration is part of the
leg.
