<to_id>ADVI_COTETL.CHAIN-FIX</to_id>
<project>ADVI_COTETL</project>
<title>Fix broken cot bronze->silver->gold auto-chain: rewrite 3 cot *-complete EventBridge rules to inf's S3-sentinel pattern (invalid SSM detail-type)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (from AE morning-review RAVC2 anomaly-2, 20260611T132445Z)</issued_by>
<issued_date>2026-06-11</issued_date>
<status>active -- GREENLIT, sequenced AFTER NFRA_DTAFLP P1 + TO-2. Low customer-impact (cot served stale 06-09, no corruption); fixes cot freshness.</status>

ROOT CAUSE (AE-diagnosed): the 3 cot event-chain rules (cot-session-complete / cot-bronze-complete / cot-silver-complete) use EventBridge detail-type "EC2 Run Command Result" which is NOT a valid SSM detail-type (real one: "EC2 Command Invocation Status-change Notification"). Result: cot-session-complete fires 0 times -> bronze never auto-dispatches -> the whole bronze->silver->gold chain has never fired in prod; only the cron session-fetch works. cot bronze EMPTY, served platinum frozen 06-09.

FIX: Terraform rewrite of the 3 cot *-complete rules to MIRROR inf's proven house pattern = S3-sentinel "Object Created" events (NOT merely correcting the SSM detail-type string — the sentinel pattern is the standard + also closes the secondary BD-session-TTL 401 gap by firing bronze seconds after session, well inside the ~30-60min real TTL). terraform/cot-pipeline. safe-apply (HALTGT checkpoint). Coordinate with DS (0.4.0) on the sentinel-object write in the cot bronze/silver .py scripts (DS owns those per Rule 13; AE owns the EventBridge rules). RAVC2 -> COO + CTO. Verify: trigger a real session-fetch, confirm bronze auto-dispatches via CloudWatch Invocations + fresh bronze object lands.
