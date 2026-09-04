# EG-s-3 result -- the PORT SOURCE verified

**TO:** `ETFS_GUARDRAIL.TO-EG-s-3` | **Worker:** `0.9.0_WK_ETFS_GUARDRAIL~2` | **Source (read-only, unmodified):**
`infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/lambda_function.py` (317 lines) @HEAD `5376ecaa8bdbf0f775cb347c2ba849bfba67afb9`

---

## 1. The battery's output

**Invocation (S3-AC1):** `python -m pytest infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/test_catchup_scan.py -q`

```
=================================== ERRORS ====================================
_ ERROR collecting infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/test_catchup_scan.py _
infra\aws\lambda\inf-pipeline\inf-etf-ownership-daily\test_catchup_scan.py:85: in <module>
    _, lf = _run(None, [])
            ^^^^^^^^^^^^^^
infra\aws\lambda\inf-pipeline\inf-etf-ownership-daily\test_catchup_scan.py:59: in _run
    lf = importlib.import_module("lambda_function")
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
...
infra\aws\lambda\inf-pipeline\inf-etf-ownership-daily\lambda_function.py:77: in <module>
    ASSETS_BUCKET = os.environ["ASSETS_BUCKET"]
                    ~~~~~~~~~~^^^^^^^^^^^^^^^^^
E   KeyError: 'ASSETS_BUCKET'
=========================== short test summary info ===========================
ERROR infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/test_catchup_scan.py - KeyError: 'ASSETS_BUCKET'
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 3.85s
```

**rc=2.** Denominator: 0 of 4 checks executed (both fixture (a) checks, both fixture (b) checks) -- the module fails
at IMPORT, before `_catchup_missing_dates` is ever called. This is **NOT** "passed"; **S3-AC1 is FAIL by output.**

**Root of the divergence (dateable, from history, not asserted):** `test_catchup_scan.py` was landed at
`288bfe8378` (2026-08-01 15:50:34 -0400) against the PRE-repoint source shape (env vars `INF_BUCKET`/
`HOLDINGS_PREFIX`; helpers `_holdings_key_for`, `_holdings_exists`; `_compute_and_write_slice(src_key, universe)`
two-arg; `_catchup_missing_dates(universe, skip_date)` two-arg). The repoint landed at `001a73530a`
(2026-08-03 18:01:50 -0400, "complete the stranded COMMIT leg of the half-landed inf-etf deploy") introduced
`ASSETS_BUCKET`/`FACT_POSITIONS_PREFIX`/`META_DEDUP_PREFIX`, `dedup_core.py`, and the current three-arg
`_catchup_missing_dates(universe, all_dates, skip_date)` / four-arg `_compute_and_write_slice(day, df, universe,
determination)`. The test was never re-vendored across that repoint and has been dead (collection error, not a
graded assertion failure) for ~32 days. **Filed as `ETFS_GUARDRAIL-W2-S1`** (OBSERVATION / ARMED, disarm routed
to `3.0.0_SA_CVO` -- this TO's bound is READ-ONLY on the port source, so re-vendoring the test is out of this
order's write lane). This TO does not modify the test or the source; the port contract below is built from a
direct read of the live bytes, not from the broken battery's assumptions.

---

## 2. Helper census

All six helpers named in the deliverable spec exist at HEAD (`grep -n "^def " lambda_function.py`, verified
`S3-AC3` for five of them mechanically):

| helper | line | signature |
|---|---|---|
| `_load_universe` | 88 | `_load_universe() -> list[str]` |
| `_list_all_partitions` | 101 | `_list_all_partitions() -> list[str]` |
| `_partition_exists` | 112 | `_partition_exists(day: str) -> bool` |
| `_output_exists` | 120 | `_output_exists(day: str) -> bool` |
| `_process_date` | 241 | `_process_date(day, all_dates, universe) -> dict` |
| `_catchup_missing_dates` | 274 | `_catchup_missing_dates(universe, all_dates, skip_date) -> list[dict]` |

(`S3-AC3`'s own invocation checks the five it names -- `_catchup_missing_dates`, `_list_all_partitions`,
`_output_exists`, `_partition_exists`, `_process_date` -- and prints all five present; `_load_universe` is
listed in the deliverable's own helper census and confirmed present by the same `grep -n "^def "` sweep above.)

Not named in the deliverable spec but load-bearing to the loop: `_load_partition` (128, loads the parquet for a
date), `_compute_determination` (134, the dual-axis dedup/freeze verdict), `_compute_and_write_slice` (188, the
ZERO-vs-MISSING guard + the write), `lambda_handler` (296, wires `_process_date` on the latest partition then
`_catchup_missing_dates` on the schedule-fired, no-explicit-date path).

`CATCHUP_WINDOW_DAYS = 10` at line 271 (`S3-AC2`, confirmed). `_catchup_missing_dates` spans 274-295;
`lambda_handler` begins at 296 and the file ends at 317 -- the TO's cited bound `271-316` is the constant
through the end of `lambda_handler`'s body (316 is the last populated line before EOF at 317).

---

## 3. THE PORT CONTRACT

### (a) Ported VERBATIM in shape (the two receiving orders, `EG-s-1` cot / `EG-s-2` bd-49f, build this exact shape)

The per-date loop over the window, driving the SAME `_process_date`-equivalent path per date:

```python
for date_str in window_dates:
    if date_str == skip_date:          # 1. skip the date just processed by the ordinary run
        continue
    if _output_exists(date_str):       # 2. skip if output already exists (IDEMPOTENT)
        continue
    if date_str not in all_dates / not _partition_exists(date_str):  # 3. skip if upstream ABSENT
        continue                        #    (can never fabricate)
    try:
        result = _process_date(date_str, ...)
        result["catchup"] = True
        results.append(result)
        print("CATCHUP: processed %s (...)" % date_str)
    except Exception as exc:            # per-date failure is caught, NEVER fatal to the sweep
        print("CATCHUP-SKIP: %s failed (%s)" % (date_str, str(exc)[:120]))
        results.append({"status": "catchup-failed", "date": date_str, "catchup": True, "error": str(exc)[:200]})
```

- The three skips, in this order: (1) `date_str == skip_date`, (2) `_output_exists(date_str)`, (3) upstream
  partition absent (`date_str not in all_dates` in the source; the two receiving producers use their own
  `_partition_exists(day)` head_object since they do not carry a pre-enumerated `all_dates` list the way the
  source's `_list_all_partitions()`-fed sweep does -- functionally identical: never process a date whose
  upstream is not there).
- The try/except around the per-date call that NEVER raises out of the sweep -- one bad date reports itself in
  the return, the sweep continues.
- The log line shapes: `"CATCHUP: processed %s (...)"` on success, `"CATCHUP-SKIP: %s failed (%s)"` on a
  caught per-date exception.
- The return-key shape `catchup_processed` / `catchup_failed`, built by `lambda_handler` from the per-date
  results (source `lambda_function.py:314-315`): `catchup_processed` = dates whose status was `"ok"` or
  `"skipped-duplicate-partition"` (an intentional non-write is still "processed", not a failure);
  `catchup_failed` = dates whose status was `"catchup-failed"`.
- The scheduled (no-explicit-date) run always does today's/latest partition FIRST via the ordinary path, THEN
  the catch-up sweep, `skip_date` = the date just processed -- exactly the source's `lambda_handler:311-317`.

### (b) REPLACED: the window itself

`CATCHUP_WINDOW_DAYS = 10` (line 271) and the walk-back `[(today - timedelta(days=d)).isoformat() for d in
range(1, CATCHUP_WINDOW_DAYS + 1)]` (line 276) are **NOT ported**. PRD ruling 1 (s.6): *"Reconcile every trading
day from the start of the prior month until that month's report has shipped. A day-count window is explicitly
NOT TAKEN and is not to be re-proposed."* Ruling 2: *"The window's terminus is a SHIPPED SIGNAL, not a date."*

The replacement, `_window_dates(today)`:
1. Terminus test: `_report_shipped(month)` = `head_object` on
   `s3://opal-data-etfs/platinum/reports/<YYYY-MM>/etf_ownership.pdf` -> bool. A denied/errored read counts as
   **NOT shipped** and is logged `WARN:` -- it must never silently end the window (a blocked render must not
   silently end the very reconciliation that would unblock it, per ruling 2's own reasoning).
2. Start: the 1st of the **PRIOR** calendar month if `not _report_shipped(prior_month)`; else the 1st of the
   **CURRENT** calendar month.
3. Span: every **TRADING DAY** (never a calendar day) from that start through **yesterday UTC**, via the
   vendored `trading_calendar.py`'s `trading_days_between(start, end)` (present in the source tree at
   `infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/trading_calendar.py:123`, byte-identical vendor target
   per `lib/trading_calendar.py` -- the two receiving TOs vendor their own copy and prove the sha256 pair, `S1-AC3`/`S2-AC3`).
4. No day count is computed or stored anywhere in the replacement; `CATCHUP_WINDOW_DAYS` must be ABSENT from
   the ported module (`S1-AC2` / `S2-AC2` check `'CATCHUP_WINDOW_DAYS' in s` is `False`).

### (c) INVARIANTS that must survive the port unchanged

1. **Skip-on-absent-upstream-partition** -- never fabricate. A date with no upstream partition is never passed
   to the per-date compute path, in the source or the port.
2. **Skip-on-existing-output** -- idempotent. A date already written is never recomputed by the sweep.
3. **The ZERO-vs-MISSING contract, untouched.** Source: `priced == 0` -> `status: "skipped-no-valued-source"`,
   NO slice written, excluded from the average rather than averaging a fabricated zero (`lambda_function.py:197-201`).
   `EG-s-1`'s cot producer carries the same shape as `"skipped-no-valued-source"`; `EG-s-2`'s bd-49f shell as
   `"skipped-empty-source"` (`diag["rows"] == 0`). **An unpriced day writes no slice in either port** -- this
   is the property PRD acceptance-property 4 names ("classified expected, not a hole, and no backfill is
   attempted against it") and it is a property of the PRODUCER's compute path, which the catch-up sweep merely
   calls into unmodified.
4. **Per-date failures are never fatal to the sweep.** One date's exception is caught, reported in
   `catchup_failed`, and the loop continues to the next date -- exactly the source's try/except at
   `lambda_function.py:288-294`.

### (d) NEW: the non-writing PROBE mode (an ADDITION beside the port, not present in the source and not ported from anywhere)

The source has no probe path -- `lambda_handler`'s only two branches are the explicit-date path
(`event.get("date")`) and the scheduled path (latest partition + catch-up), and the explicit-date path always
calls `_process_date`, which always writes on a non-skip verdict. **Neither receiving TO ports this from the
inf source; both TOs add it new:**

- Trigger: `event == {"date": d, "probe": true}`.
- Response: `{"status": "probe", "date": d, "partition": <bool>, "priced": <int>, "output_exists": <bool>}`.
- `partition` = whether the upstream partition for `d` exists (the same head_object `_partition_exists` uses).
- `priced` = the same count the ordinary compute path uses to discriminate ZERO-vs-MISSING when the partition
  exists (cot: `Market Value > 0` rows; bd-49f: `diag["rows"]` from `compute_slice`), else undefined/0 when the
  partition is absent.
- `output_exists` = the same `_output_exists(d)` the sweep uses.
- **Writes nothing**: no `put_object` reachable on the probe branch. This is why the classifier cell (`EG-s-4`,
  see `ETFS_GUARDRAIL-S1` in this project's investigation row) can call the firm-scoped producers for their own
  discrimination without the ETFS layer ever holding a firm-bucket S3 grant (NEVER#1) -- the producer answers
  for itself, over its OWN already-least-privilege role, via `lambda:InvokeFunction`, and nothing is written on
  that path.

### (e) The 49F tail: the test arm the ports must carry

The brief's lag table: 49 Financial mostly 1-5 days late, tail observed at 6, 7, 8, **12, 13** days (Schwab is
ad-hoc-batch; "do not pick a number"). `CATCHUP_WINDOW_DAYS = 10` in the source would **not** find a partition
that lands on day 12 or 13 (`today - timedelta(days=d)` for `d` in `1..10` never reaches `-12` or `-13`) --
this is PRD acceptance-property 2, "the property a straight port fails while passing review." The
reporting-obligation window (b) does not exclude it by construction: as long as the trading day in question
falls after the 1st of the (prior-or-current, by ruling 2's shipped test) month, it is IN the window regardless
of how many calendar days late the partition arrives -- the window's boundary is a calendar date plus a shipped
signal, never a lag count.

**The test arm (`EG-s-2`'s battery, arm (i) plus its negative control (j)):**
- **(i) THE TAIL, positive:** a trading day `D` whose upstream partition does not exist until `D+13`
  (`_partition_exists` stubbed to return `True` only for dates `>= D+13`'s clock), with "today" stubbed to
  `D+14` and the prior month's report stubbed NOT shipped (so the window starts at the 1st of the prior month
  and easily contains `D`) -> the real `_catchup_missing_dates`/`_window_dates` **must return `D`** and the
  per-date compute path must be called for it exactly once.
- **(j) THE NEGATIVE CONTROL:** the SAME fixture (same `D`, same `D+13` late arrival, same `today = D+14`), but
  with the source's `CATCHUP_WINDOW_DAYS = 10` day-count semantics simulated instead of the reporting-obligation
  window -> `D` is **NOT found** (`today - timedelta(days=d)` for `d in 1..10` does not reach `D`, which is 13
  calendar days back). This is the discriminating fixture: it proves the test can tell the two designs apart,
  so a silent regression back to a day-count window would fail (j)'s assertion that the two are DIFFERENT
  (i.e. if a future edit reintroduces a 10-day window, arm (i) itself starts failing, and (j) stops being able
  to show a contrast -- the pair is what keeps this property live rather than a fixture that would pass either
  way). `EG-s-1`'s cot producer does not need this arm on its own battery (COT's tail is not documented as
  exceeding 10 days in the brief's lag table), but the reporting-obligation window it ports is the SAME
  mechanism, so its arm (c)/(d) (prior-month-not-shipped vs shipped) exercises the same window-boundary logic
  the 49F tail depends on.

---

## 4. Acceptance criteria, verbatim with rc and denominator

| id | invocation | output (deciding line) | rc | denominator | verdict |
|---|---|---|---|---|---|
| S3-AC1 | `python -m pytest .../test_catchup_scan.py -q` | `KeyError: 'ASSETS_BUCKET'` / `1 error during collection` | 2 | 0 of 4 checks reached | **FAIL** (not "passed") |
| S3-AC2 | `python -c "...CATCHUP_WINDOW_DAYS..."` | `CATCHUP_WINDOW_DAYS=10` | 0 | 1 of 1 constant matched | PASS |
| S3-AC3 | `python -c "...HELPERS=..."` | `HELPERS=_catchup_missing_dates,_list_all_partitions,_output_exists,_partition_exists,_process_date` | 0 | 5 of 5 named helpers present | PASS |
| S3-AC4 | `git diff --stat HEAD -- infra/.../inf-etf-ownership-daily/` | (empty) | 0 | 0 of 0 lines changed | PASS (empty diff as expected) |
| S3-AC5 | judgment | see s.3 above (the full port contract) | -- | -- | RECORD; NO VERDICT (CVO grades at L9) |
