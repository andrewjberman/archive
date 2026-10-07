# FLOW_MEASURED_E1 -- counts only

Task order IRPT_DASHBD.TO-DB-b-31, worker 0.9.0_WK_IRPT_DASHBD~16. Claim: measured. Zero vendor calls; S3 reads only.

Method: Modified Dietz over BD's Account-level bmv, emv and netAdditions (bronze pull=20261004), each Opal dated flow
(gold `account_return_daily`, column `external_flow`, 564 date partitions) weighted by the fraction of the segment remaining
after its date. Negative control: the same Dietz with every flow at the midpoint. Verdict MEASURED_FLOW_TIMING only when
flows_match and the Dietz gap is at most 0.35 pp.

| Count | Value |
|---|---|
| FLOW_TIMING segments (round 19, inferred) | 226 |
| flows_match true (Opal flow sum agrees with netAdditions) | 226 |
| measured (MEASURED_FLOW_TIMING) | 22 |
| returned_unexplained | 204 |
| negative control within 0.35 pp (flows at midpoint) | 19 |
| UNEXPLAINED on a measured basis (3,053 + 204) | 3,257 |

Reading: the flow totals agree on every segment, so the flows are real, but only 22 of the 226 reproduce BD's gross return
once the flows are dated; the other 204 return to UNEXPLAINED.
