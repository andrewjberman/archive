# PDF_ROUTE_READ -- AR-y-471 (0.9.0_WK_IRPT_ANLREQ~345, branch wk-IRPT_ANLREQ-345)

Question: does `GET analysis/requests/{REQ}/pdf` (route `analysis-request-pdf`, method `pdf`) accept an Opal Overview report built the way the real writers build it? Every cite below was re-read in this worktree at the line given. Cites are repo-relative to the worktree root `C:/dev/wk-irpt-anlreq-345`.

## S1 release.protected_pdf_ref: where it is set, from writer to read

- Route: `infra/aws/lambda/investor-reporting/ops/entry.py:245` maps the `.../pdf` path to `analysis-request-pdf`, and `infra/aws/lambda/investor-reporting/ops/entry.py:250` binds that operation to `pdf`.
- The route reads the ref at `infra/aws/lambda/investor-reporting/ops/owned_report.py:316-317` and refuses with ANALYSIS_PDF_NOT_RETAINED at `infra/aws/lambda/investor-reporting/ops/owned_report.py:321-322` when it is not a dict with `server_only` true.
- The Opal writer builds the document at `infra/aws/lambda/investor-reporting/ycharts/research/opal_producer.py:590-601`. Its release is `{"released_revision": None}` at `infra/aws/lambda/investor-reporting/ycharts/research/opal_producer.py:600`. Nothing in that function writes a `protected_pdf_ref`.
- The document is passed to `persist` at `infra/aws/lambda/investor-reporting/ycharts/research/opal_producer.py:602`. The same dict is the run_opal `metadata` at `infra/aws/lambda/investor-reporting/ycharts/generate/resident_worker.py:575-576`.
- The publisher's Opal branch is selected at `infra/aws/lambda/investor-reporting/ycharts/generate/publisher.py:231-233`. It deep-copies metadata into `report` at `infra/aws/lambda/investor-reporting/ycharts/generate/publisher.py:190`, validates at `infra/aws/lambda/investor-reporting/ycharts/generate/publisher.py:191`, and persists it unchanged at `infra/aws/lambda/investor-reporting/ycharts/generate/publisher.py:199-202`.
- The schema does not require the ref. The opal_engine release requires only `released_revision` (`infra/aws/lambda/investor-reporting/_contracts/AnalysisReport.v2.schema.json:857-859`), so the document without it validates.
- Read returns the stored document unchanged: the report is fetched at `infra/aws/lambda/investor-reporting/ops/owned_report.py:204-205` and returned as a `_CheckedReport` copy at `infra/aws/lambda/investor-reporting/ops/owned_report.py:225-227`.
- The only writers of `protected_pdf_ref` in the tree are vendor-form: `infra/aws/lambda/investor-reporting/ycharts/generate/resident_worker.py:517-518` (beside `vendor_artifact` at `infra/aws/lambda/investor-reporting/ycharts/generate/resident_worker.py:512`) and `infra/aws/lambda/investor-reporting/ycharts/generate/job.py:557-562` (beside `extraction_validation` at `infra/aws/lambda/investor-reporting/ycharts/generate/job.py:544`). No Opal-path writer exists.
- Hand-built Opal shapes do carry the ref: `infra/aws/lambda/investor-reporting/_contracts/fixtures/AnalysisReport.v2.opal.valid.json:79-86` has one, `infra/aws/lambda/investor-reporting/ops/tests/test_owned_report.py:248-252` loads that fixture, and `infra/aws/lambda/investor-reporting/ops/tests/test_owned_report.py:337-345` passes only on it. The publisher's own test world overwrites release to the real shape at `infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_publisher.py:213`.

## S2 opal_artifact: where set

- The member is built at `infra/aws/lambda/investor-reporting/ycharts/research/opal_producer.py:593-594` as `{"sha256": run_doc["report"]["sha256"], "byte_length": len(pdf), ...}`.
- The sha is `hashlib.sha256(pdf_bytes)` at `infra/aws/lambda/investor-reporting/ycharts/research/layout_overview.py:1376`, called from `infra/aws/lambda/investor-reporting/ycharts/research/opal_producer.py:541` on the `pdf` rendered at `infra/aws/lambda/investor-reporting/ycharts/research/opal_producer.py:530`.
- The same bytes are retained at `infra/aws/lambda/investor-reporting/ycharts/research/opal_producer.py:549-552` (artifact port) or written at `infra/aws/lambda/investor-reporting/ycharts/research/opal_producer.py:554` (objects port).
- The publisher re-checks the receipt against the retained bytes at `infra/aws/lambda/investor-reporting/ycharts/generate/publisher.py:184-187`.
- The route takes this member as the artifact at `infra/aws/lambda/investor-reporting/ops/owned_report.py:319-320`, and compares its sha and byte_length at `infra/aws/lambda/investor-reporting/ops/owned_report.py:324-326` (ANALYSIS_PDF_BINDING).

## S3 same or counterexample

Verdict: NOT the same pair. The route compares `release.protected_pdf_ref.sha256` with `opal_artifact.sha256`. For an Overview from `opal_producer.py` the first operand is never written.

- Value A, `opal_artifact.sha256`: the sha256 of the rendered Overview bytes, from `infra/aws/lambda/investor-reporting/ycharts/research/layout_overview.py:1376` through `infra/aws/lambda/investor-reporting/ycharts/research/opal_producer.py:593`. It is the retained PDF's sha. The run in S4 confirms it: the assertion `document["opal_artifact"]["sha256"] == sha256(pdf)` passed before the route was called.
- Value B, `release.protected_pdf_ref.sha256`: ABSENT. Counterexample: `infra/aws/lambda/investor-reporting/ycharts/research/opal_producer.py:600` writes `{"released_revision": None}`, and no later Opal writer adds the ref (S1).
- The route stops at `infra/aws/lambda/investor-reporting/ops/owned_report.py:321-322` with ANALYSIS_PDF_NOT_RETAINED, so the comparison at `infra/aws/lambda/investor-reporting/ops/owned_report.py:324-326` never runs for a real Opal report. The CTO's static reading (both shas from the same retained PDF) holds for value A; value B does not exist.

## S4 test and result

- Test file: `infra/aws/lambda/investor-reporting/ops/tests/test_pdf_route_real_shapes.py` (offline; no AWS, no network).
- The report is built by the real writer, `opal_producer.produce`, run on the producer's own fakes (`infra/aws/lambda/investor-reporting/ycharts/research/tests/test_opal_producer.py:115` make_stores). The one fake is `read`, which returns the stored document the way `infra/aws/lambda/investor-reporting/ops/owned_report.py:225-227` does. The publisher leg is not run (see NOT-READ).
- The positive test calls `pdf()` on that document with a recording signer. The two controls add `release.protected_pdf_ref` by hand, using the real `opal_artifact` sha (control) or a different sha (negative case).
- Invocation: `python -m pytest infra/aws/lambda/investor-reporting/ops/tests/test_pdf_route_real_shapes.py -v -p no:cacheprovider`
- Output, deciding lines: `FAILED ...::test_status_route_pdf_accepts_the_report_the_real_opal_writers_store - owned_report.AnalysisUnavailable: ANALYSIS_PDF_NOT_RETAINED` and `1 failed, 2 passed`. The control test and the negative test PASSED.
- The negative case raises ANALYSIS_PDF_BINDING as the cell requires, so the binding check itself works. The real shape fails one step earlier, because the ref is absent.

RESULT: FAIL the real Opal writers set opal_artifact.sha256 (opal_producer.py:593) but never write release.protected_pdf_ref (opal_producer.py:600), so pdf() refuses ANALYSIS_PDF_NOT_RETAINED (owned_report.py:321-322) and never compares the two shas.

Surprise row: IRPT_ANLREQ-D2-W345-S1 (BLOCKING, ARMED; disarm owner 2.0.0_SA_COO~Y2).

NOT-READ: the CTO messages 11508 and 11510 (broker messages, not in the tree); the live artifact index and any retained Overview PDF (no AWS, by order); the repository's `persist` and `get` and `FencedReportIndex` (called at publisher.py:199 and owned_report.py:204, not followed into their modules); the publisher's `_publish_opal` leg was not executed offline (its test world needs the full repository fake, so the stored document comes from the producer's real persist call and the publisher's unchanged persist at publisher.py:199-202 is read, not run); the body of `PdfSigner.sign` beyond `infra/aws/lambda/investor-reporting/ops/pdf_link.py:91-99`.
