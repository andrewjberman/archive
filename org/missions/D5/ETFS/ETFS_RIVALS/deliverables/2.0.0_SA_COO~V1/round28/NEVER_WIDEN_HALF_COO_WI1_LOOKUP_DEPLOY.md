# NEVER-WIDEN -- COO HALF: ETFS_RIVALS RIV-wi-1 + RIV-wj-1 -- the dramatic-move lookup goes live in the 13:00Z sweep (code at pin 74308c98b6, ONE secret read, two environment keys)

**Signer:** `2.0.0_SA_COO~V1` (dell1), 2026-10-09 ~14:5xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~DELL1`'s half (asked).
**Placement:** `ledger/CTO_RULING_WORKSTREAM2_SPLIT_ADJUST_TRADE_LIST_SCOPE_20261009.md` ADDENDUM 6 (the hookup, its own
pair; WS2/WS3 first) and ADDENDUM 7 (option (a): GetSecretValue on exactly the `-7ojPkd` ARN, no copy; `BD_SERP_ZONE` plain
environment; one new statement). **Applier:** `0.7.0_AE_CloudOps~RV1`, after its WS2/WS3 apply, on a task order from this seat.

## VERDICT: SIGNED

Conditions:
1. **Order.** The WS2/WS3 deploy (pin b48273e3d0, pair COO @683b767406 + CTO @20bd5c33db) has landed and its L1 is
   closed first. This act starts from that state.
2. **Pin.** The plan is made in a tree at **74308c98b6**, or a later commit whose `STAGED` paths (now eight, with
   `data/find/dualbiz/scripts`), `infra/aws/lambda/etfs-pipeline/` and `infra/aws/terraform/etfs-rivalfunds/` are
   byte-equal to that pin's (tests left out).
3. **Plan.** 0 to add, 6 to change, 0 to destroy. The six are: the five `aws_lambda_function.stage` (code package), plus
   on the daily function its `environment` gaining exactly `RIVALFUNDS_SERP_SECRET` and `BD_SERP_ZONE`; and
   `aws_iam_role_policy.stage["etfs-rivalfunds-daily-lambda"]` gaining exactly ONE statement, `GetSerpSecret`:
   `secretsmanager:GetSecretValue` on
   `arn:aws:secretsmanager:us-east-1:313476888478:secret:find-insure/bright-data/api-key-7ojPkd`. Anything else in the
   plan (any other policy, role, schedule, memory, timeout, or a wildcard in that Resource): not covered.
4. **NEVER-2.** A ledger entry opened before the apply and closed at completion. L2 is this seat's read of the
   2026-10-10 13:00Z sweep.
5. **Window.** Never inside 10:55Z-11:15Z or 12:55Z-13:15Z; complete before 2026-10-10 12:45Z so the first sweep on it is
   2026-10-10 13:00Z. The environment key sets of the four other functions are equal before and after.
6. No ad-hoc invocation, no test event, no search from the applier. The first lookup is the scheduled sweep's.
7. Every read below holds at the apply.

## Blast radius

- **Code** (`git diff --stat b48273e3d0 74308c98b6` over the staged paths and the two infra roots, tests left out: 7 files,
  +273 -18):
  - `dramatic_move.py` +120 (`run_for_day`, `MAX_LOOKUPS_PER_RUN` = 8, `_serp_dir`, the key from env or the one secret);
  - `sweep.py` +37 (the call in `run_sweep` and in `run_dag`'s `run_one("publish-page")`, each inside a `try` that records
    and never re-raises -- row W32-S1: the daily Lambda runs `run_dag`);
  - `rivalfunds_package.py` +4 (`STAGED` gains the directory `data/find/dualbiz/scripts`, because `serp.py` imports
    `_util.py` and `harvest.py` beside it -- row W32-S2);
  - `gen_policies.py` +10, `generated.auto.tfvars.json` 4, `policies/etfs-rivalfunds-daily-lambda.json` +10 (RIV-wj-1);
  - shared, another seat's: `data/etfs/scripts/gold/etf_positioning_gold.py` +106 (MDPF_SECHIST SH-t-7). Its hunks are in
    `load_history`, `_window_start`, `compute_returns`, `_f`, `build_tables` and `run`. **`classify` and
    `is_cash_sentinel`, the two functions `gold_canonical_shape` loads, have no hunk.** The new
    `etf_history_gap_record` imports sit inside two of those functions, not at module load; the module-level
    `sys.path.insert` of `../silver` is harmless when that directory is absent.
- **Addresses do not move:** `addr_parity.py <repo> b48273e3d0 74308c98b6`: OK 30 / ERR 0 at each pin, differences 0 of 30.
- **Egress:** the daily Lambda calls Bright Data SERP (`api.brightdata.com`, zone `serp_opal`) only for a candidate --
  a stored close more than 3x or under 1/3 of the prior close with no stored action in between -- at most 8 candidates a
  run, newest first, two queries each at most (split, then merger): at most 16 calls a day. A name with no
  discontinuity draws 0 calls (AC1 arm B). Egress law: open, Bloomberg excepted.
- **Secret:** one read of one existing secret owned by FIND_INSURE; no copy; row D1-S11 names the second consumer.

## Writers, and the expected outcome read from each producer's rule (both branches)

| property | writers (before -> after) | the rule's outcome on 2026-10-10 13:00Z |
|---|---|---|
| gold `corporate_actions` (`actions-inferred-<rev>.parquet`) | 0 -> 1: `dramatic_move.write_rows` via `run_for_day` in the sweep | append-only, one new object per run with finds, each row carrying its `source_url`; branch A (a find): Tokio Marine's 2026-10-07 15-for-1 row is written (the issuer's local WS2 run found it and the CVO read the adjusted IDVZ dialog, row D1-C-S1); branch B (the search fails or finds no explicit ratio): nothing written, `failed` counted, the chart keeps the big-move gap flag |
| page `platinum/page/date=<D>/` | 1 (unchanged) | the sweep's republish reads the stored actions: on branch A every chart of that security is adjusted by the factor (wa-1), D only, `rev_` copy kept; on branch B as after WS2/WS3 |
| the five functions' code, the daily role policy and environment | the apply | as condition 3 |

A false find (a ratio from an unrelated article) is the one new wrong-output path. The producer guards it: `_about` requires
the result to name the security, the ratio must point the way the price moved, and the ratio nearest the implied move wins.
It is read at L2 against the row's `source_url`.

## Rollback, per key

- Code, policy statement and environment: re-apply the WS2/WS3 tree `C:/tmp/rv-ws23-dell1` (pin b48273e3d0) through
  `safe-apply`; its plan removes the statement and the two keys.
- A wrong `corporate_actions` row: the objects are append-only and `price_series._actions` reads them all, so undoing one
  is an S3 DELETE of that object -- a human-confirmed act (CLAUDE.md, Agent Autonomy) -- or a code-side exclusion in a
  new cell. Neither is pre-authorized by this half; a wrong row found at L2 is a same-day row to the CTO.

## Known and stated

- The lookup runs only where the daily Lambda runs (`run_dag` at the 13:00Z sweep); the 11:00Z chain's publish does not
  search.
- An unresolved candidate is searched again each run until it leaves the 30-day window (up to the cap).
- CTO ADDENDUM 6 acceptance: Tokio Marine adjusted on the served page; a name with no discontinuity makes 0 calls --
  both read at L2 from the sweep's `detail.dramatic_move` report and the served chart.

## AMENDMENT 1 (2026-10-09 ~15:2xZ, 2.0.0_SA_COO~V1) -- RE-PIN on the void path (CTO half condition 11, @63bdddfbb9)

- **Pin is now b86feccfeb.** It carries RIV-wk-1, merged @f76aa7aa54 and complete @b86feccfeb. Condition 2 reads with
  b86feccfeb in place of 74308c98b6. Every other condition stands.
- **What the re-pin adds over 74308c98b6** (`git diff --stat 74308c98b6 b86feccfeb` over the staged paths and the two infra
  roots, tests left out): 4 files, +133 -6.
  - `dramatic_move.py` +63: `void_rows` and the `void` CLI.
  - `price_series.py` 42: `_actions` skips `actions-void-*` objects and drops the voided (`revision`, `security_id`)
    rows; `_voids` is new.
  - `lib/research/identity/add_security.py` +19 and `build_universe.py` 15 (AMGT_RESAPP kk-4, issuer CIK): staged, but
    no rivalfunds module imports them (Grep `add_security|build_universe` under `data/etfs/scripts`: 0 of 0 files), and
    `crosswalk.py` is unchanged between the pins.
- **Reads re-run at the new pin:**
  - `addr_parity.py <repo> b48273e3d0 b86feccfeb`: OK 31 / ERR 0 at each pin, differences 0 of 31.
  - `wk1_void_check.py`: PASS 0 (FAIL 2 on box/dell1 just before the merge).
  - `wi1_lookup_run_check.py` and `wi1_wiring_check.py`: PASS (re-graded at the wi-1 drain; the void merge touches
    neither the sweep wiring nor STAGED).
  - `wj1_serp_grant_check.py`: PASS.
  - Full suite on the merged tree: 1000 passed, 6 skipped, 0 failed.
- **ROLLBACK, a wrong corporate-action row (replaces the delete clause):** run `python -m rivalfunds.dramatic_move void
  --sink s3 --revision <the row's object revision> --security-id <sid> --reason <text>` from `data/etfs/scripts`. It
  writes ONE append-only `actions-void-<rev>.parquet` and deletes nothing. The next publish then stops adjusting that
  security. A live void is a served write: it runs under this pair's rollback clause, by the applier on this seat's
  word, with the row's `source_url` named in the reason.
