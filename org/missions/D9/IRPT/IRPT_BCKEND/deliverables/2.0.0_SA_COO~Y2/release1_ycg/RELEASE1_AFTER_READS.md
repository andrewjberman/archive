# irpt-ycharts-generate RELEASE 1 -- after-reads (ledger irpt-ycg-release1-20261007, L4)

**By** `2.0.0_SA_COO~Y2` on dell2, 2026-10-08. Applied 10:06:18Z (safe-apply: 0 added, 1 changed, 0 destroyed; re-plan: No
changes). Pair `NEVER_WIDEN_PAIR_RELEASE1.md`; CTO half `@d2d2859a2a`; method ruling msgs 1133/1149.

| # | after-read | result |
|---|---|---|
| 1 | E-Y4 leg 1: the deployed zip has no fixtures | deployed zip (fetched from `get-function` Code.Location, re-hashed `ZspX0qD2bCkFVoi3X8W0cBiPlHY37utqPysuLXMeduI=`): 100 members, **0** under `fixtures/har/` -- PASS |
| 2 | E-Y4 leg 2: the fixture tests at the pin | laptop relay at `1b5afe6a49` (Python 3.12.10, PyMuPDF 1.27.1): `431 passed, 30 skipped, 32 subtests passed, offline_rc=0` (`FITZ_RELAY_REL1_1b5afe6a49.txt` @3f344dc917) -- PASS |
| 3 | E-Y4 leg 3: the trace control on the extracted deployed zip | `zip_trace.py`: **0** readers across 100 text members; with one planted reader, **1** caught across 101 -- PASS. A first run returned 0 with the plant because a shell heredoc mangled the regex; the probe was rewritten with the Write tool and the control then fired. |
| 4 | IB-pr-357: no `internal_correlation_id` | OFFLINE on the code (`envelope_keys.py`): BEFORE (live zip `uFTONal..`), the success status carried `internal_correlation_id`; AFTER (deployed zip `ZspX0qD2..`), the success and refusal status keys are both `{actions, operation, public_reason_code, source_dates, state}` and the key is absent -- PASS. LIVE no-token POST /api/scoped/investor-reporting/analysis at 11:30:38Z: HTTP 401 `{message}` from the API Gateway authorizer, no `internal_correlation_id` on the wire. **Limit:** the authorizer refused before the function ran, so this exercises the gateway, not the function's own refusal envelope; that envelope needs a token (the offline AFTER read covers it). |
| 5 | a real request, read back | Andrew's F1 retry, read back by `2.0.0_SA_COO~G2` with `f1_find_request.py` (CTO msgs 1133/1149). Until it runs, the CloudWatch read below stands in. **OPEN: it is Andrew's to run, and opens now.** |
| 6 | import closure | direct IAM invoke `{"irpt_import_census": true}`: HTTP 200, `{"irpt_import_census": {"modules": 62, "failed": {}}}` -- PASS |
| 7 | deployed equals built | live CodeSha256 `ZspX0qD2..` == built `ZspX0qD2..` == S3 version `4Pvl.mN3tY9..` content-sha256 -- PASS |
| CTO (b) | CloudWatch, hour after vs hour before | before 09:06-10:06Z: Errors, Invocations and Throttles all with no datapoint (no traffic). After 10:06-11:06Z: Errors **0**, Invocations 1 (the import census), Throttles 0. 10:06Z-now: Errors 0. **No rise, so no rollback.** |

Rollback (unused): S3 version `w031eAfDs6mh.1ZOCaAks5bHDhKj8ajT` (`uFTONal...`).
