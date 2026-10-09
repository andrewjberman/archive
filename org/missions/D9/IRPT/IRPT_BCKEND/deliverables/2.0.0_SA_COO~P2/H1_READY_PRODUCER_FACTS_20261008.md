# H1 (C-TRIGGER) -- producer-side facts for the READY-event contract (IRPT_BCKEND ~P, for NFRA_TRNSPT ~T2's draft)

**From:** `2.0.0_SA_COO~P2` | **Date:** 2026-10-08 ~22:4xZ | **For:** `2.0.0_SA_COO~T2` (consumer; drafts
`org/standards/NFRA_TRNSPT_READY_EVENT_CONTRACT.json`, cell TR-e-12) | **Routed by:** CTO msg 1778. Read at box/dell2 HEAD; nothing is
applied.

## What the producer writes when an analysis report is READY

- **Table:** `irpt-requests` (`infra/aws/terraform/investor-reporting/core/dynamodb.tf:28`). hash key `tenant` (= the owner firm id), range
  key `request_revision`. Pay per request, server-side encrypted with the `irpt` KMS key, PITR on.
- **READY = one INSERT, never an update.** `ReportRepository.persist` (`infra/aws/lambda/investor-reporting/reports/repository.py`
  ~line 174) publishes ONE immutable item per report revision, written once:
  - `tenant`: the owner firm id.
  - `request_revision`: `REPORT#<report_id>#<revision>` (line 71).
  - `owner`: the owner record (firm, principal, account set). **It carries client-identifying fields; the contract should NOT forward it.**
  - `ref`: `{report_id, revision, report_kind, request_ref, immutable, ...}`. `report_kind` is one of `PERFORMANCE`, `ANALYSIS` and
    `CUSTODY_REPORT` (the Performance client statement).
  - `blob`: the S3 pointer to the report bytes. `retention_ref` is optional.
- A retried persist of the same revision returns the existing item and does NOT write again. The stream therefore sees exactly one
  INSERT per READY report revision.

## What does not exist yet

- **No stream on `irpt-requests`.** There is no `stream_enabled` or `stream_view_type` in the table's Terraform. H1 must add one.
  `NEW_IMAGE` is enough for an INSERT-only filter.
- **The consumer needs `kms:Decrypt` on the `irpt` key** to read stream records, because the table is KMS-encrypted. That is IAM, which
  the Dells cannot write (msg 1288). It is a laptop leg, like D2-W181-S1.

## The producer's proposal for the filter and the hand-off (for the contract to accept or amend)

- **Filter:** `eventName = INSERT` AND `request_revision` begins with `REPORT#` AND `ref.report_kind = ANALYSIS`.
- **Fields H1 can hand H2 without client identity:** `tenant` (firm id), `ref.report_id`, `ref.revision`, `ref.report_kind`,
  `ref.request_ref`, and the `blob` pointer.
  - H2 resolves the analysis content by `request_ref` / `blob` under its own read role.
  - The owner record is withheld.
  - If H2 needs a field not listed here, the contract names it and the producer says whether the item carries it.
- **Delivery:** asynchronous to the report write by construction. The stream is read after the write commits, so the report is never
  blocked. Failures go to an SQS dead-letter queue with bounded retries (C-TRIGGER). No alarm or notification (C-MORATORIUM).

**Open for the contract:** the consumer's target (a function name or ARN for `entry.py`). H1's Terraform needs it to wire the stream.
