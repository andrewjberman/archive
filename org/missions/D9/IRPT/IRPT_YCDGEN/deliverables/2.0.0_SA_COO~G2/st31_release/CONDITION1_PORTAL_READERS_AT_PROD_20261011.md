# st31 -- the CTO half's condition 1: the page's readers at the portal's PROD commit, fed a failed job's answers

**By:** `2.0.0_SA_COO~G2`, 2026-10-11 ~13:3xZ, on `NEVER_WIDEN_ST31_DEAD_LETTER_RECORD_CTO_HALF.md` @bb5f7303b7 section 3
item 1. A static run in a scratch folder: three reader files taken with `git show origin/PROD:<path>` at portal commit
`37aa1247ee` (fetched just before), executed with bun on fixtures. No network, no portal file written (the portal checkout
reads 0 changed files after it).

## Where a failed job's state reaches the page

The condition names `readOwnedRequest` and `readOwnedHistory`. Read at PROD
(`src/pages/InvestorReporting/contracts/owned-requests.ts` lines 58-87): neither carries a state or a reason. The
single-request answer is `identity`, `accepted_at` and two optional members; a history row is the same answer. A job's
state and reason reach the page through the STATUS answer, read by `requirePublicStatus`
(`contracts/public-status.ts`). So three readers were run, not two.

## Fixtures: made by the server's own code, not typed

- The status answer: `ops/status.py` `build_envelope(..., state "FAILED", public_reason_code "ANALYSIS_FAILED")`, the pair
  `ops/owned_status.py` line 20 maps a FAILED job to, then `public_view` (the projection the route applies). Keys:
  `actions, operation, public_reason_code, source_dates, state`; `source_dates` is `{}`, `actions` is `[]`.
- The request answer: the `instance` of `_contracts/fixtures/OwnedAnalysisRequest.valid.json`.

## Result (six reads, each line is the script's own output)

| # | read | result |
|---|---|---|
| S1 | the status answer of a FAILED job through `requirePublicStatus` | **accepted** |
| S2 | negative control: the same answer with an unknown state word | throws `Invalid public status` |
| R1 | the single-request answer through `readOwnedRequest` | **accepted** (keys identity, accepted_at) |
| R2 | the same answer with `state` and `reason` members added | throws `Invalid owned request projection`: those members are not part of this answer, and the server does not send them there |
| H1 | a history page holding that request, shape `{items, next_cursor}`, through `readOwnedHistory` | **accepted** |
| H2 | a history page in the shape IRPT_ANLREQ release 5 serves (rows with `client_id` and `client_claim`, plus `unreadable_rows`) | throws `Invalid owned request history` |

## Reading

The one answer st31's change can alter is the status answer of a job that exhausts its deliveries: state FAILED, reason
ANALYSIS_FAILED. The PROD portal's status reader accepts it (S1), and its control shows the reader discriminates (S2). The
request and history readers read the same request unchanged (R1, H1): st31 does not touch what they read.

**H2 is not st31's, and it is reported, not acted on:** the PROD portal's history reader refuses the release-5 history
shape. Whether the live status function is serving that shape to PROD right now was NOT read here; `2.0.0_SA_COO~Y2` and
the CTO hold release 5.

## Not established

What the PAGE draws for a FAILED status after the reader accepts it (the view code was not run), and any live read.
