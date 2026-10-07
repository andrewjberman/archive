# Intake batch 1: the fetch list derived from the dependency closure

Derived by `org/devices/intake/intake_closure.py fetchlist` from `org/devices/intake/closure_cp314_win_amd64.json`
(saved 2026-10-07T18:59:24Z), INTAKE-CLOSURE target=cp314-win_amd64 lines=67 closure=162 dependencies_added=95 pure=114 fits=11 needs_fetch=37 unknown_not_installed=0 specifier_conflicts=2 fixed_point=True ok=True.

**Whether any file named below exists on the index is UNREAD: nothing was asked.** Each name follows the wheel
specification's normalisation (runs of `-`, `_`, `.` in the project name become `_`, lower case; the version is the
normalised installed version) with the tag `cp314-cp314-win_amd64`. A project may publish its Python 3.14 file under a
different tag (for example a stable-ABI `cp3NN-abi3` name), or not publish one: the fetch step's own check reads the
index by exact name and is the real control. The version is the one installed on this laptop.

Approval is read from `org/tier1_exec/4.0.0_SA_CRO/deliverables/PACKAGE_INTAKE_ASSESSMENT_BATCH_1_30_PACKAGES_20261007.md` (30 names assessed; CTO msg 106363: 26 approved, and pyarrow, pyiceberg, hdbscan and kuzu not approved at their pins). A row is APPROVED only when the assessed version equals the closure's.

## Counts

- Closure members whose installed copy is compiled for another Python only: **36**
- APPROVED: **25**
- NOT-YET-APPROVED: **4**
- NEW-REQUEST: **7**
- Closure members that need a copy for another reason (no wheel metadata, editable, no RECORD), listed after the table: **1**

## The files (compiled for another Python only)

| # | File name that would be asked for | Status | Kind | Reached through |
|---|---|---|---|---|
| 1 | `aiohttp-3.14.1-cp314-cp314-win_amd64.whl` | APPROVED | dependency | aiobotocore, s3fs |
| 2 | `catboost-1.2.10-cp314-cp314-win_amd64.whl` | APPROVED | line | (a line) |
| 3 | `cffi-2.0.0-cp314-cp314-win_amd64.whl` | APPROVED | dependency | cryptography, curl-cffi |
| 4 | `charset_normalizer-3.4.4-cp314-cp314-win_amd64.whl` | APPROVED | dependency | pdfminer-six, requests |
| 5 | `contourpy-1.3.3-cp314-cp314-win_amd64.whl` | APPROVED | dependency | matplotlib |
| 6 | `coverage-7.13.5-cp314-cp314-win_amd64.whl` | APPROVED | dependency | pytest-cov |
| 7 | `duckdb-1.5.0-cp314-cp314-win_amd64.whl` | APPROVED | line | (a line) |
| 8 | `fonttools-4.63.0-cp314-cp314-win_amd64.whl` | APPROVED | dependency | matplotlib |
| 9 | `frozenlist-1.8.0-cp314-cp314-win_amd64.whl` | NEW-REQUEST | dependency | aiohttp, aiosignal |
| 10 | `greenlet-3.3.2-cp314-cp314-win_amd64.whl` | APPROVED | dependency | playwright |
| 11 | `hdbscan-0.8.41-cp314-cp314-win_amd64.whl` | NOT-YET-APPROVED | line | (a line) |
| 12 | `jiter-0.13.0-cp314-cp314-win_amd64.whl` | APPROVED | dependency | anthropic, openai |
| 13 | `kiwisolver-1.5.0-cp314-cp314-win_amd64.whl` | APPROVED | dependency | matplotlib |
| 14 | `kuzu-0.11.3-cp314-cp314-win_amd64.whl` | NOT-YET-APPROVED | line | (a line) |
| 15 | `lxml-6.0.2-cp314-cp314-win_amd64.whl` | APPROVED | line | python-docx, python-pptx |
| 16 | `markupsafe-3.0.3-cp314-cp314-win_amd64.whl` | NEW-REQUEST | dependency | jinja2 |
| 17 | `matplotlib-3.11.1-cp314-cp314-win_amd64.whl` | APPROVED | line | catboost |
| 18 | `mmh3-5.2.1-cp314-cp314-win_amd64.whl` | APPROVED | dependency | pyiceberg |
| 19 | `multidict-6.7.1-cp314-cp314-win_amd64.whl` | NEW-REQUEST | dependency | aiobotocore, aiohttp, yarl |
| 20 | `numpy-2.4.2-cp314-cp314-win_amd64.whl` | APPROVED | line | awswrangler, catboost, contourpy, exchange-calendars, hdbscan, matplotlib, model2vec, pandas, scikit-learn, scipy, sentence-transformers, transformers, yfinance |
| 21 | `pandas-2.3.3-cp314-cp314-win_amd64.whl` | APPROVED | line | awswrangler, catboost, exchange-calendars, pandas-market-calendars, yfinance |
| 22 | `pillow-12.1.1-cp314-cp314-win_amd64.whl` | APPROVED | line | matplotlib, pdfplumber, python-pptx |
| 23 | `propcache-0.5.2-cp314-cp314-win_amd64.whl` | NEW-REQUEST | dependency | aiohttp, yarl |
| 24 | `pyarrow-18.1.0-cp314-cp314-win_amd64.whl` | NOT-YET-APPROVED | line | awswrangler |
| 25 | `pydantic_core-2.41.5-cp314-cp314-win_amd64.whl` | NEW-REQUEST | dependency | pydantic |
| 26 | `pyiceberg-0.9.1-cp314-cp314-win_amd64.whl` | NOT-YET-APPROVED | line | (a line) |
| 27 | `pywin32-311-cp314-cp314-win_amd64.whl` | APPROVED | line | mcp |
| 28 | `pyyaml-6.0.3-cp314-cp314-win_amd64.whl` | APPROVED | line | awscli, huggingface-hub, transformers |
| 29 | `regex-2026.2.28-cp314-cp314-win_amd64.whl` | APPROVED | dependency | transformers |
| 30 | `rpds_py-0.30.0-cp314-cp314-win_amd64.whl` | APPROVED | line | jsonschema, referencing |
| 31 | `scikit_learn-1.8.0-cp314-cp314-win_amd64.whl` | APPROVED | line | hdbscan, sentence-transformers |
| 32 | `scipy-1.17.1-cp314-cp314-win_amd64.whl` | APPROVED | line | catboost, hdbscan, scikit-learn, sentence-transformers |
| 33 | `torch-2.10.0-cp314-cp314-win_amd64.whl` | APPROVED | line | sentence-transformers |
| 34 | `websockets-16.0-cp314-cp314-win_amd64.whl` | APPROVED | line | yfinance |
| 35 | `wrapt-2.2.2-cp314-cp314-win_amd64.whl` | NEW-REQUEST | dependency | aiobotocore |
| 36 | `yarl-1.24.2-cp314-cp314-win_amd64.whl` | NEW-REQUEST | dependency | aiohttp |

## New requests (compiled, in the closure, not among the 30 assessed; NOT approved by this cell)

- `frozenlist` (1.8.0), reached through aiohttp, aiosignal
- `MarkupSafe` (3.0.3), reached through jinja2
- `multidict` (6.7.1), reached through aiobotocore, aiohttp, yarl
- `propcache` (0.5.2), reached through aiohttp, yarl
- `pydantic_core` (2.41.5), reached through pydantic
- `wrapt` (2.2.2), reached through aiobotocore
- `yarl` (1.24.2), reached through aiohttp

## Not yet approved (assessed, not approved at this pin, or assessed at another version)

- `hdbscan` 0.8.41: assessed 0.8.41, recommendation NO
- `kuzu` 0.11.3: assessed 0.11.3, recommendation NO
- `pyarrow` 18.1.0: assessed 18.1.0, recommendation NO
- `pyiceberg` 0.9.1: assessed 0.9.1, recommendation NO

## Needs a copy for a reason other than compiled-for-another-Python

- `click` 8.3.1 (NO-METADATA): editable install (no wheel can be re-packed from it) -- APPROVED

## Assessed names that this closure does not list as compiled

- none

