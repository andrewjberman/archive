# EG-s-4 -- the coverage classifier: four kinds of empty day told apart

**TO:** `ETFS_GUARDRAIL.TO-EG-s-4` · **Worker:** `0.9.0_WK_ETFS_GUARDRAIL~1` · **Worktree HEAD:** `48a39eb98b` (branch `wk-ETFS_GUARDRAIL-1`) · **Verb:** classify (new module, no other surface touched).

## Module built

- `data/etfs/scripts/coverage/__init__.py`
- `data/etfs/scripts/coverage/classifier.py` -- public API: `classify_month(partner, month, *, s3=None, probe=None, series=None) -> dict`, `summarize(classes) -> dict`, `coverage_line(partner, summary) -> str`, plus a CLI (`--partner`, `--month`, `--no-probe`). ASCII only, stdlib + boto3 only.
- `data/etfs/scripts/coverage/tests/__init__.py`, `data/etfs/scripts/coverage/tests/test_classifier.py` -- ZERO AWS calls (every arm supplies `series`/`probe` directly).

## 1. S4-AC1 -- the battery, all eight arms

**Invocation:**
```
python -m pytest data/etfs/scripts/coverage/tests/test_classifier.py -q
```
**Output (rc=0):**
```
8 passed in 1.11s
```
Arms: (a) COVERED slice-exists, (b) Saturday -> A, (c) probe present+priced=0 -> B, not in `holes`, in `expected_empty`, (d) probe present+priced=5 + no slice -> C, (e) probe partition=False -> D, (f) no probe -> UNKNOWN never B/C/D, (g) the August fixture with 5 holes (`16/21 trading days; 5 carried for missing data`), (h) the same fixture with 0 holes (`21/21 trading days; 0 carried for missing data`) -- both arms of the empty/non-empty pair present.

## 2. S4-AC2 -- live read, cottonwood August 2026, `--no-probe`

**Invocation:**
```
python data/etfs/scripts/coverage/classifier.py --partner cottonwood --month 2026-08 --no-probe
```
**Output (rc=0):**
```
CLASSIFY: partner=cottonwood month=2026-08 trading_days=21 COVERED=21 A=10 B=0 C=0 D=0 UNKNOWN=0
21/21 trading days; 0 carried for missing data
```
`UNKNOWN=0` -- every one of the 21 August trading days has a slice today, consistent with the 09-01 repair this project's queue has already landed elsewhere.

## 3. S4-AC3 -- live read, inflection August 2026, `--no-probe`

**Invocation:**
```
python data/etfs/scripts/coverage/classifier.py --partner inflection --month 2026-08 --no-probe
```
**Output (rc=0):**
```
CLASSIFY: partner=inflection month=2026-08 trading_days=21 COVERED=21 A=10 B=0 C=0 D=0 UNKNOWN=0
21/21 trading days; 0 carried for missing data
```
A and COVERED do not collide: the classifier checks `is_trading_day` FIRST (non-trading calendar days are always `A`, whether or not a slice happens to exist that day -- the taxonomy table's own definition: "COVERED = a slice exists for the trading day"); only trading days are eligible for `COVERED`. `A=10` (August 2026's 10 weekend days), `COVERED=21` (every trading day), sum = 31 = the full calendar month, with no day counted twice.

## 4. S4-AC4 -- no committed calendar copy

**Invocation:**
```
python -c "import os; print('COMMITTED_CAL_COPY=%s' % os.path.exists('data/etfs/scripts/coverage/trading_calendar.py'))"
```
**Output (rc=0):**
```
COMMITTED_CAL_COPY=False
```

## 5. S4-AC5 -- commit gate clean

**Invocation:**
```
bash .tools/commit-gate.sh data/etfs/scripts/coverage/classifier.py data/etfs/scripts/coverage/__init__.py data/etfs/scripts/coverage/tests/test_classifier.py
```
**Output (rc=0):**
```
OK: pre-commit gate clean for 3 of 3 file(s)
```

## 6. S4-AC6 -- no firm bucket named, by bytes

**Invocation:**
```
python -c "import re; s=open('data/etfs/scripts/coverage/classifier.py').read(); print('FIRM_BUCKET_REFS=%d' % len(re.findall(r'opal-data-(?:assets|inf|cot|bd|schwab)', s)))"
```
**Output (rc=0):**
```
FIRM_BUCKET_REFS=0
```
**Note (self-correction, not a row):** the module's first draft's own docstring named `opal-data-assets` in prose explaining what it does NOT read, which the byte-level regex correctly caught (`FIRM_BUCKET_REFS=1`) -- exactly what the criterion says: "the etfs-only principal is a property of the bytes, not a promise." Reworded to describe the constraint without the literal bucket string; re-ran to `FIRM_BUCKET_REFS=0` and re-ran the full battery + commit gate clean afterward (both still pass, shown above).

## 7. The resolver's two paths (evidence for S4-AC7)

**Path 1 -- repo layout (`from lib import trading_calendar`), exercised live by every invocation above:**
```
python -c "import sys; sys.path.insert(0,'data/etfs/scripts/coverage'); import classifier; print(classifier.tcal.__file__); print(classifier.tcal.calendar_source())"
-> C:\...\wk-ETFS_GUARDRAIL-1\lib\trading_calendar.py
-> NYSE/pandas_market_calendars
```

**Path 2 -- flat sibling (deploy-time copy beside the package), demonstrated in `.scratch/` only (never committed to the package):**
```
cp data/etfs/scripts/coverage/classifier.py .scratch/flat_sibling_test/classifier.py
cp lib/trading_calendar.py .scratch/flat_sibling_test/trading_calendar.py
python -c "import sys; sys.path.insert(0,'.scratch/flat_sibling_test'); import classifier; print(classifier.tcal.__file__)"
-> C:\...\wk-ETFS_GUARDRAIL-1\.scratch/flat_sibling_test\trading_calendar.py
```
The flat-sibling `import trading_calendar` succeeds first when a sibling copy is present (as EG-s-6's build-time artifact upload will place on the reporter box); it fails over to `from lib import trading_calendar` when none is present (this repo's own layout, confirmed by S4-AC4's `COMMITTED_CAL_COPY=False`). Neither path is committed inside `data/etfs/scripts/coverage/`.

## 8. S4-AC7 -- THE ANSWER (judgment; recorded, no verdict)

- **Class B is EXPECTED, never a hole (property 4):** test arm (c) asserts `summary["holes"] == 0` and `summary["expected_empty"] == 1` for a B-classified date in the same call; `summarize()`'s `holes` formula is literally `C + UNKNOWN + D` with B excluded by construction, and `expected_empty` is literally `B` -- there is no code path that can add a B day to `holes`.
- **The ZERO-vs-MISSING contract is untouched:** the classifier never writes to S3 (`No fabrication: the module writes nothing to S3, ever`, enforced by inspection -- no `put_object`/`upload_*` call anywhere in `classifier.py`) and a `priced == 0` day (B) is classified and left alone, never backfilled or "fixed."
- **UNKNOWN is never guessed:** `classify_month` returns `UNKNOWN` exactly when (i) no probe is supplied (`probe is None`, arm (f) and every `--no-probe` CLI run) or (ii) the supplied probe returns `None` for that date -- in both cases no B/C/D verdict is ever produced without a probe answer (arm (f) asserts `class not in ("B","C","D")`).
- **MECE over "a calendar day of the month":** `_month_dates(month)` enumerates every calendar day from the 1st to the month cap with no gaps or duplicates (a plain `date + timedelta(i)` walk); each day passes through exactly one branch of a single if/elif chain (`is_trading_day` -> A; else `date_str in series` -> COVERED; else `probe is None` -> UNKNOWN; else `probe(...)` is None -> UNKNOWN; else `not partition` -> D; else `priced == 0` -> B; else -> C) -- six mutually exclusive classes covering every day, demonstrated live: `A=10, COVERED=21` summing to 31 = August's full calendar length with zero overlap (S4-AC2/AC3), and the fixture arms (g)/(h) summing `COVERED + holes (+ B, 0 here)` to the full 21 trading days with zero double-count.

## 9. Push state (measured at report)

```
git ls-remote origin refs/heads/CLOUD
```
