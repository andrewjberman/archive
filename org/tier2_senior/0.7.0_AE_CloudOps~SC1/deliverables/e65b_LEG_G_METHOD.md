# e65b leg G -- the method, and why it waits

Ledger: `secclass-e65b-namekey-ship-dell1-20261009`, leg G, the one leg still open.
Order: `MDPF_SECCLASS.TO-SC-e65b` step 5. Condition: CTO half @7f68da7051 condition 3.

Kept here and not appended to the ledger entry on purpose: row `MDPF_SECCLASS-D1-S3` records that
`deploy_ledger.py` regenerates an entry and silently deletes prose a seat appended to it.

## What leg G must show

The FIRST BD E_18 run after the 02:4xZ ship plans no `NAME::` key that is not a whole cash phrase as
cash/Cash, and still plans `NAME::CASH` / `Cash` as cash. A violating row triggers rollback of the key AND
deletion of the row.

## Why an ad-hoc run is refused rather than merely skipped

CLAUDE.md requires naming the evidence or the wait is the defect. Three reasons, any one sufficient:

1. An E_18 run WRITES new-security rows. This order's `<bounds>` is "no table write". The ad-hoc is out of
   bounds, not merely unattractive.
2. Leg G's subject is "the FIRST BD E_18 run after this ship". An ad-hoc run would itself BECOME that run
   and consume the discriminator the leg exists to read.
3. The order's own step 5 names "the next BD gold run".

## When

- `bd-gold-nightly-fallback` is `cron(0 23 ? * MON-SAT *)`, ENABLED. 2026-10-09 is a Friday, so it fires
  tonight 23:00Z. Logs land about 2h15m later.
- The second daily run is NOT a cron. There is no 04:00Z EventBridge rule on bd-gold -- the only other
  bd-gold rule, `bd-gold-layer-monthly-trigger`, is DISABLED. It is data-arrival driven: a price PUT to
  silver writes `gold/trigger-pending.json` and the trigger fires. So the next run time is upstream-data
  dependent, not predictable from a schedule. The order's "BD fires 04:00Z and 23:00Z" is the observed
  pattern, not a schedule entry.
- Detector armed (Monitor): instance state transitions on `i-01003b035d2988dfb`, new E_18 telemetry under
  `logs/gold-layer/telemetry/bd-gold-layer-runner/E_18/`, and new `logs/gold-layer/gold_incremental_*` run
  logs. It emits on read failures too, so silence means "nothing changed", never "the run passed".

## How to read it, in priority order

1. **Plan lines, preferred carrier: on the instance WHILE IT IS UP.**
   `/var/log/gold-layer-runner.log` via SSM, with a last-block awk so an append-only log cannot yield an
   older run. Read E_18's own block: the Detection summary ("Scheduled rows written / refused"), the
   WARNING queue line, and `E_18 done (rc=N)`.
   QUALIFIER, carried from the predecessor leg: E_18 is in `NONFATAL_IDS` (`gold_dispatch.sh:165`), so a
   non-zero exit is logged without aborting the chain. Read rc from E_18's own block; never infer it from
   the chain surviving.

2. **Plan lines, durable fallback if the instance has stopped.**
   `s3://opal-data-bd/logs/gold-layer/gold_incremental_<date>_<stamp>.log`. It is large (the 10-09 01:15Z
   one is 632 MB), so filter rather than read whole.

3. **The absent-is-not-exercised-against control -- the reason this leg is not just a row count.**
   A zero from stale code reads identically to a zero from new code. So prove the bytes that RAN:
   - Preferred: md5 on the instance via SSM of BOTH
     `/tmp/gold_layer_scripts/lib/_shared/etf_classification_scheduled.py` and
     `/home/ubuntu/gold-layer/scripts/lib/_shared/etf_classification_scheduled.py`.
     Each must read `40ffa3fac380551704637adc8a3b6ff3` (35,100 B was the OLD size; the new bytes differ).
   - Fallback if the instance is already down: the ordering argument. The S3 key's LastModified is 02:4xZ
     2026-10-09; a run that STARTS after that necessarily pulls those bytes, since nothing else moves the
     key. State it as an ordering argument, not as an on-instance measurement -- they are not the same
     claim and the weaker one must not be reported as the stronger.

4. **Do NOT use the predecessor's table-side corroboration.** Row `MDPF_SECCLASS-D1-S17` (this seat,
   02:56Z) records why: no row in `etf-classifications` carries an `input` attribute, so a scan filtered
   `input=cash_token` returns 0 for every value including `bd-securities`, `gics` and `schwab`. It is a
   wrong-domain census, not a measurement.

   The sound table-side read, if one is wanted, keys on what the table DOES persist: rows whose `ticker`
   begins `NAME::` and whose `asset_class` is `cash`. Before the next run that census reads **331 of
   11,361**, of which 330 have names that are not whole cash phrases (writers: scheduled 313, model 18).
   Those are NOT condition-3 violations -- the module is put-on-absence and "never replaces or edits an
   existing row", so condition 3 governs only what the next run PLANS. The naive reading of that same
   census says "330 violations" and is wrong; it is written down here so the next reader does not make it.

## Already proven, so leg G is the last thing owed

- Both keys at `40ffa3fa`, AC1 `E65-SHIPPED ok=True ... control=MATCH` (base was `ok=False`).
- 10 of 10 watch keys unmoved on BOTH ETag and VersionId, STOPS=0, 12-key denominator printed.
- The SERVED bytes were pulled back out of S3 and `cash_token_match()` exercised in them: 9 of 9 across a
  LANDS arm, a NEGATIVE arm and 2 controls.
- Narrowing-only confirmed on LIVE data, not just by reading the diff: OLD bytes from git @03f7f8fb5c
  (md5 verified `3f1e6be8`, equal to the measured pre-act ETag) vs the served NEW bytes, both evaluated
  over all 331 real `NAME::`-keyed cash keys -- OLD-yes/NEW-no = 8, **OLD-no/NEW-yes = 0**.

## Rollback, still live and unused

Nothing is owed. If leg G ever needs it, copy each key back from its pre-act VersionId:
`opal-data-bd` `5BZygWLxJfYjc.0hzSKkxUM_l0enmtKn`, `opal-data-cot` `0e4OsubYyRdw4RnmCvfMYM0SZtLLM9z9`
(both at ETag `3f1e6be8910952f33c88bf100c610ab6`), and delete any offending planned row by its key.
