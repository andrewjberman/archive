# Log census: status-job reads refused SECTION_DATE_CENSUS_INVALID (CTO~DELL2 msg 4194)

**By:** `2.0.0_SA_COO~G2`, read-only, 2026-10-11 05:38Z. Replaces the count the `kms:Decrypt` fence blocked (row `IRPT_YCDGEN-D2-S38`).

## Denominator

- Log group `/aws/lambda/irpt-status`, us-east-1. Created 2026-09-11T07:38:13Z, retention 14 days, storedBytes 1,189,916.
- Earliest status-job internal event the group still returns: 2026-09-27T16:38:15Z. Latest: 2026-10-11T05:29:50Z.
- Every read used `filter-log-events --start-time 0`, auto-paginated; `nextToken` absent on all three.

## Result

| filter | events | distinct request ids |
|---|---|---|
| `"SECTION_DATE_CENSUS_INVALID"` | 1 | 1 |
| `"status-job" "INVALID_INPUT"` (the public code; wider) | 6 | not derivable (see limits) |
| `"irpt_internal" "status-job"` (every internal refusal) | 29 | not derivable |

The one `SECTION_DATE_CENSUS_INVALID` event: 2026-10-11T05:29:50Z, correlation `corr-62e36c245412`. It is this seat's own
window-7 read of `REQ-5e4149d2863aea31cc87d660` on tenant 49financial (same second; record
`R6_STATUS_JOB_OPT_IN_REV6_20261011.json` @220bbcfa95). That id was minted by this project's F1 run: a TEST request.

**Per tenant: 49financial 1 (test), cottonwood 0, inflection 0. Non-test request ids refused: 0.**

Positive control: the census returns the one refusal this seat caused, so the filter sees the string when it is logged.

The 29 internal status-job refusals by text: DATE_SOURCE_OWNER_BINDING 10, IdRefused (unregistered firm token) 8,
INVALID_REQUEST_ID 5, RetentionRefused "invalid retention reference" 3, AccessDenied 1, TypeError 1,
SECTION_DATE_CENSUS_INVALID 1.

## Limits

- The log line carries a correlation id and an operation, not a request id or a tenant. The one event is tied to its request
  by time and by this seat's own record, not by a field in the log.
- 14 days of retention: a refusal before 2026-09-27 is not visible. The Opal producer first published after 2026-10-05.
- A READY Opal report nobody has status-read with the opt-in is latent and is not counted here (msg 4194 says so).
- Off-task, not investigated: one `AccessDenied` on `s3:GetObjectVersion` for `irpt-status-role` on a cottonwood
  `original_holdings` object, 2026-09-28T00:29:29Z, `corr-597c5f061a79`, status-job. Single event, 13 days old.
