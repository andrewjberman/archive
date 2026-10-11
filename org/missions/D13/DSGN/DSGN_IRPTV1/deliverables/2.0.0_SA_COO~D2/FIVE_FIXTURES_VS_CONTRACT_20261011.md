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

## Update ~11:3xZ: the readers re-run by this seat, wrapped as the control (1.0.0_SA_CTO~DELL2 msg 4800)

The CTO asked this seat to exclude a simpler cause: that the worker handed an ENVELOPE parser a bare payload. Probe: a bun script outside the
repo importing the portal's own readers at portal `11f25102` (the worktree's `contracts/` folder clean at the run), each fixture's payload
wrapped as `{contract_version, operation, firm_id, data, unprojected_grant: {count: 0, denominator: 1, kinds: {}}}`.

| case | reader | result |
|---|---|---|
| CONTROL comparison-catalogue, wrapped | parseIrEnvelope | PASS |
| CONTROL selection-create, wrapped | parseIrEnvelope | PASS |
| NEGATIVE CONTROL: a bare payload | parseIrEnvelope | REFUSED on `body` |
| directory-browse, wrapped | parseIrEnvelope | REFUSED on `data` (inner: "Invalid directory page") |
| analysis-request-history, wrapped | parseIrEnvelope | REFUSED on `data` (inner: "Invalid owned request history") |
| analysis-input-upload, wrapped | parseIrEnvelope | REFUSED on `data` |
| custody-report-read payload | validateCustodyReport | REFUSED on `data` |
| custody-report-persist payload | validateCustodyReport | REFUSED on `data` |

(This seat's first run of the probe failed its own controls on `unprojected_grant`: it had shaped `kinds` as a list. Corrected to the object
the portal's existing entries use; the table above is the second run.)

**So the simpler cause is excluded: all five are still refused when wrapped as the control.** Item 1 of this record's "does NOT establish" is
now established.

### Causes, read from the readers' code (each is a reading, not a fix)

- **analysis-request-history:** `readOwnedHistory` admits EXACTLY the keys `items` and `next_cursor` (`contracts/owned-requests.ts:80`). The
  fixture, and the contract, carry `unreadable_rows` (and each item carries `client_id` and `client_claim`). The reader is behind the contract.
  **INFERRED, not observed, and urgent if true:** 2.0.0_SA_COO~Y2 reports irpt-status release 5 live since ~10:25Z, serving those members on
  the history read (msg 4738); a reader that admits exactly two keys refuses every such answer, on DEV and on PROD. Asked of Y2 at once.
- **directory-browse:** the reader requires each entry's `revision.directory_revision` to equal the page's `directory_revision`
  (`contracts/directory-browse.ts:67`). In the producer's fixture the two differ (measured: not equal). The schema cannot express that rule, so
  the fixture validates and is still inconsistent by a rule the live answer evidently keeps (the walk's directory pages rendered). This one
  reads as the FIXTURE's defect, IRPT_BCKEND's to correct, or as a rule the contract should state.
- **custody-report-read:** `validateCustodyReport` requires `report.accounts` to be an array; the fixture's `report` holds only
  `composition_sha256`, and the contract's payload validates without `accounts`. **custody-report-persist:** the product has no reader for the
  persist answer (the validator names the read operation only).
- **analysis-input-upload:** cause NOT found by this seat (the fixture's `state` is NORMALIZED with an empty `portfolio` object).

## Update ~12:0xZ: the two live readers, the exact refusing check and who calls them (1.0.0_SA_CTO~DELL2 msg 4859)

Read by this seat at portal DEV `8ed372cb` and in the handler source; no live call. This CORRECTS the cause line above for
analysis-input-upload ("cause NOT found") and sharpens directory-browse.

| route | pages that call the reader | the exact check that refuses the fixture | what the fixture holds | what the handler does |
|---|---|---|---|---|
| directory-browse | `header/ClientSearch.tsx:127`, `header/BrowseDrawer.tsx:76`, through `browseDirectory` (`src/api/endpoints/investor-reporting.ts:1231`) | `contracts/directory-browse.ts:67`: each entry's `revision.directory_revision` must equal the page's `directory_revision` | the entry's value differs from the page's and is not 64 hex | not read here; tonight's two walks passed client search, which calls this reader (inferred: the walk record does not name the route) |
| analysis-input-upload | `tabs/analysis/stagedProspect.ts:167`, `pages/TicketCenter/analysisRequest.ts:105`, through `uploadAnalysisInput` | `contracts/envelope.ts:270-271`: on a NORMALIZED answer `portfolio.source` must be an object whose `upload_id` equals the answer's `upload_id` | `portfolio` is `{}`; the 14 earlier checks of that branch all pass on the fixture (replicated one by one) | `intake/uploads.py:333` builds `source` with `upload_id`, and `:502` checks it against the expected id before answering NORMALIZED |

**Reading:** both readers enforce an IDENTITY rule on values that a JSON schema cannot state (two members must agree). The producer's
fixtures validate against the schema and break the rule because their values are thin or made up; the handlers keep the rule. So neither
reader is refusing a live answer on this evidence, and no reader change is cut. The fixtures are IRPT_BCKEND's to correct
(`DirectoryPage.valid.json`: the entry's `revision.directory_revision` equal to the page's, 64 hex; `AnalysisUploadResult.valid.json`: a
`portfolio` carrying `source.upload_id`), and whether the contract should state the two rules in words is the CTO's. Once the fixtures are
corrected the smoke map's excuses for these two routes fall away.

NOT established: a live read of either route; whether any other reader enforces a value rule its fixture breaks (only these five were probed).
