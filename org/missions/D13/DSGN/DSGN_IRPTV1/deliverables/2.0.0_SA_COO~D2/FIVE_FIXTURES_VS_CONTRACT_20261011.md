# DSGN_IRPTV1 -- the five producer fixtures the portal's readers refuse, validated against the ratified v1 contract

**Author:** 2.0.0_SA_COO~D2, direct read, 2026-10-11 ~11:2xZ. **Ordered by:** 1.0.0_SA_CTO~DELL2 msg 4790, item 2 ("validate each of the five
producer fixtures against its v1 response schema with a schema validator, and print PASS or the failing path"). **Row:** DSGN_IRPTV1-D2-W53-S4.
Read-only: no file edited, no AWS call, no live request.

## Method

`jsonschema` 4.26.0 with a `referencing` registry over the 46 schema files under `docs/contracts/investor-reporting/v1/` and
`v1/responses/` (each registered by its file URI and its `$id`), at box/dell2 HEAD. Fixtures from
`infra/aws/lambda/investor-reporting/_contracts/fixtures/`.

**What a producer fixture IS (measured):** each `<Name>.valid.json` is a wrapper `{_expect, _fixture, _source, instance}`; `instance` is the
PAYLOAD (the `data` member of a response), not a whole response envelope. The response schema of each route is the envelope
`{contract_version, operation, firm_id, data, [unprojected_grant], [status]}` whose `data` member is a `$ref` to the payload's schema. So the
question "is the fixture valid against its response schema" is answered on the `data` member.

## Result: 5 of 5 PASS

| route | fixture | payload vs its type schema | payload vs the response schema's `data` member | control: the `.invalid` fixture |
|---|---|---|---|---|
| directory-browse | DirectoryPage.valid.json | PASS | PASS | FAIL (as it must) |
| analysis-request-history | OwnedAnalysisRequestHistory.valid.json | PASS | PASS | FAIL |
| analysis-input-upload | AnalysisUploadResult.valid.json | PASS | PASS | FAIL |
| custody-report-read | custody-report-read.response.valid.json | (no separate type schema) | PASS | not run on `data` |
| custody-report-persist | custody-report-persist.response.valid.json | (no separate type schema) | PASS | not run on `data` |

Positive control for the method: `comparison-catalogue`, a route the portal DOES read, PASSES the same way. Negative control: the three
`.invalid` type fixtures FAIL their type schema.

**By the CTO's rule (msg 4790 item 2): the fixtures are valid, so the portal's reader is the side that is wrong and moves, on all five.**

## What this does NOT establish

1. **How the worker fed the fixtures to the readers.** Worker 0.9.0_WK_DSGN_IRPTV1~53 reported the refusals ("response envelope field 'data'
   does not satisfy the v1 contract"); this seat did not re-run them. The message names `data`, which is consistent with the payload having
   been placed in an envelope correctly; four other fixtures passed through the same generator. Not re-measured here.
2. **Item 3 of msg 4790: whether the LIVE answer of each route has the fixture's shape.** NOT ESTABLISHED. This seat made no live request and
   holds no authorized session for the served routes. What is known: tonight's two walks passed directory SEARCH, which is route
   `directory-search`, a different route from `directory-browse`; neither walk record names a read of the history, upload or custody routes.
   Who can settle it: the laptop's walk with its network capture on those three pages, or 2.0.0_SA_COO~P2 from the producer's side.
3. **WHY each reader refuses.** Not read. For the two custody routes the worker's read is that `validateCustodyReport` requires
   `report.accounts` to be an array while the contract's `CustodyReportRead` payload validates without it, and that the persist answer has no
   reader of its own. The three envelope routes' failing member inside `data` is not known.

## What follows in this lane

- The smoke map lands at 16 with six excuses by name (msg 4790 item 1): order IV-e-95, AMENDMENT 3.
- The reader fix is a PRODUCT change on client-facing pages (three live routes), one cell per reader family, each a candidate for the CTO. It
  is cut on the CTO's word after item 3 is read, because a reader that refuses a live answer is the urgent one and changes the order.
