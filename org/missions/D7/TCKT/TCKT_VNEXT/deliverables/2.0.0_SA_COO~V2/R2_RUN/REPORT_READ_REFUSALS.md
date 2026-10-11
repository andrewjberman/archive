# TCKT_VNEXT R2 -- refusals of the finished-report read (`analysis-report`), PROPOSED

**Status: PROPOSED.** Transcribed by `2.0.0_SA_COO~V2` on 2026-10-11 from the final report of worker `0.9.0_WK_TCKT_VNEXT~8`
(TO-R2-rn1 AMENDMENT 1, item A3), whose Write tool refused the file (row TCKT_VNEXT-D2-W8-S3). This file is that row's disposition.
The reading is the worker's, from the tree at box/dell2 HEAD. It was not checked line by line by this seat, not diffed against the
deployed bytes, and not exercised. The `R2-tr-1` run pair confirms or corrects it.

**Route:** `GET /api/scoped/investor-reporting/analysis/<REQ id>/sections`, operation `analysis-report` (`OPERATION_REPORT`).

**Denominator:** 32 rows = 31 per-request raise sites read + 1 bare re-raise. By file: `ops/entry.py` 1; `ops/owned_report.py` 11
plus the re-raise; `ops/owned_requests.py` 11; `_scope/owner_reads.py` 3; `ycharts/generate/durable_job.py` 2; `_authz/served.py`
`_owner_read_request` 3. **Not read:** the raise sites inside `reports/repository.py` and `reports/retention.py`; they reach the
caller by exception class only (`RetentionExpired` and `LeaseRefused` -> NOT_FOUND; `ReportDenied` -> NOT_AUTHORIZED; `ReportRefused`
and `RetentionRefused` -> UNEXPECTED).

**What the caller sees:** only the closed PUBLIC code, never the internal string (`_authz/served.py:874-887`, `errors.py:116-143`,
the map at `ops/entry.py:252-257`). Classification is therefore by public code.

| internal reason | file:line | public code | class |
|---|---|---|---|
| ANALYSIS_REPORT_NOT_READY (job state is not READY) | `ops/owned_report.py:119` (guard `:118`) | NOT_FOUND | NOT-READY. `entry.py:254` maps `AnalysisUnavailable` to NOT_FOUND (also the CTO's read, msg 4041) |
| REPORT_BUNDLE_ABSENT (READY and indexed, bytes not in the store) | `ops/owned_report.py:137`, class `:20-29` | NOT_READY | NOT-READY. The class declares this code itself |
| JOB_IDENTITY_MISMATCH, ACCEPTED_COMPOSITION_MISMATCH | `ycharts/generate/durable_job.py:66`, `:71` | NOT_FOUND | NOT-READY by code; a permanent mismatch looks the same |
| INVALID_REQUEST_ID | `ops/owned_requests.py:88` | INVALID_INPUT | TERMINAL |
| UNEXPECTED_OWNED_READ_QUERY | `ops/entry.py:165` | INVALID_INPUT | TERMINAL |
| the three `_owner_read_request` ValueErrors | `_authz/served.py:923`, `:932`, `:941` | INVALID_INPUT | TERMINAL |
| REQUEST_UNAVAILABLE (3 sites) | `ops/owned_requests.py:166`, `:170`, `:176` | NOT_AUTHORIZED | TERMINAL |
| VERIFIED_PRINCIPAL_REQUIRED, CONCRETE_REQUEST_DATA_FIRM_REQUIRED | `ops/owned_requests.py:96`, `:104` | NOT_AUTHORIZED | TERMINAL |
| the three `ProspectOwnershipRefused` | `_scope/owner_reads.py:33`, `:39`, `:41` | NOT_AUTHORIZED | TERMINAL |
| 5 other `owned_requests.py` bindings | `:185`, `:189`, `:196`, `:222`, `:225` | INVALID_INPUT | TERMINAL |
| 8 `owned_report.py` sites (READY_REPORT_RECEIPT_REQUIRED, REPORT_ACCEPTED_OWNER_BINDING, REPORT_RETENTION_REQUIRED, REPORT_ACCEPTED_REQUEST_BINDING, READY_REPORT_CHANGED, REPORT_INDEX_CHANGED, ANALYSIS_REPORT_PROVIDER / OPAL_FORM / VENDOR_MEMBER_ABSENT) | `:127`, `:100`, `:103`, `:145`, `:149`, `:152`, `:51`, `:64`, `:87` | INVALID_INPUT | TERMINAL |
| bare re-raise of any other store error | `ops/owned_report.py:138` | by class, usually UNEXPECTED | TERMINAL |

**The runner's set:** `NOT_READY_CODES = frozenset({"NOT_FOUND", "NOT_READY"})`. Everything else is terminal, DEPENDENCY_* and
RATE_LIMITED included (transient, but they do not mean "not generated yet").

**Two limits the run pair must carry:**
1. NOT_FOUND cannot tell not-yet-generated from failed, expired or never-generated (row D2-W8-S4). An absent or foreign request is
   stopped earlier and answers NOT_AUTHORIZED (`entry.py:226-228`, `owner_reads.py:28-33`, `served.py:985`); read, not exercised. So a
   bound reached on NOT_FOUND is recorded NOT-READY, never a pass, and the run then reads the job's state by another instrument.
2. Round 1's logs showed the internal string `INVALID_REQUEST_ID`, which HEAD would answer as `INVALID_INPUT` (row D2-W8-S5). If
   the deployed layer emits internal strings, a not-ready answer would read `ANALYSIS_REPORT_NOT_READY`, which is not in the set, and
   hop (e) would end terminal on its first poll. The pair's precheck reads which vocabulary the deployed bytes speak.
