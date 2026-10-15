# CB-cj-2 run record (0.9.0_WK_ADVI_COTBKF~177), round 88

The same figures as `JOB_RECORD.json` in this folder. No CRM value, name, account number or dollar is written here.

- Session: `cotbkf-crm-match-177`. Role: `arn:aws:iam::313476888478:role/cloudops-cot-crm-match-role`.
- Started `2026-10-15T20:03:49Z`, ended `2026-10-15T20:03:51Z`.
- Key: the one granted key in bucket `opal-data-cottonwood` (`s3://opal-data-cottonwood/commonwealth/cottonwood/bronze/crm/date=2026-06-23/CRM_CottonwoodCapitalAdvisors.zip`).
- Assume_role: succeeded (one call). head_object: one call, refused with `ClientError` code `403`, message `Forbidden`.
- `landed`: **false**. No `get_object`, no read, no `CRM_LINKS.csv` written. `ContentLength`: none.
- Members and header columns: none (no read). Columns used: none. Output columns: `commonwealth_account`, `bd_account_id`, `rule`, `tier`.
- Rows: 0. Counts: deterministic 0, candidate 0, ambiguous 0. Rules: none.
- Over the 219: reachable 219; deterministic 0; candidate-only 0; unlinked 219; matched 0; unmatched 219.
- Commonwealth accounts touched: 0 of 1,533 in the served crosswalk (the denominator read through the shell identity: 1,533 distinct accounts).
- Black Diamond side read through the shell identity: 3 most recent holdings partitions with the custodian column.
- `scratch_disk_write`: false. `cloudtrail_data_event_read`: false (the withdrawal order reads the data events; this job did not).
- Not established: whether the 403 means an absent key (AWS returns 403 for a missing key when the role lacks ListBucket) or a refused read; AssumeRole events for the role (condition C1, read by the withdrawal order); the bucket question (surprise row ADVI_COTBKF-D1-W177-S1).
