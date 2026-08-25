<to_id>NFRA_ALERTSUB</to_id>
<project>NFRA_ALERTSUB (infra-alerting follow-up, NEW low-pri)</project>
<title>opal-infrastructure-alerts SNS topic has NO subscriber -> paging inert; wire an endpoint</title>
<assigned_to>0.7.0_AE_CloudOps (any AE/infra lane; captured from base-AE pre-offline)</assigned_to>
<issued_by>2.0.0_SA_COO (captured from base-AE summary before Andrew took it offline 2026-06-11)</issued_by>
<issued_date>2026-06-11</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "NFRA_ALERTSUB (infra-alerting follow-up," resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: open -- LOW-PRI, NOT blocking (monitoring gap, not a live break). Captured so it isn't lost when base-AE went offline.</status>

Base-AE flagged (pre-offline): the opal-infrastructure-alerts SNS topic has NO subscriber -> any alarm publishing to it pages NOWHERE (inert) until an endpoint is wired. This is a monitoring/alerting gap (alarms fire but no human/channel receives them).

WHEN WORKED: wire a subscriber to opal-infrastructure-alerts (email / Slack-webhook Lambda / PagerDuty endpoint — per the fabric's standard alerting channel). Verify with a test-publish that the alert reaches the endpoint. Low-pri; fold into the next AE/infra session. Not urgent (no live incident depends on it today), but the gap means infra alarms are currently silent — worth closing before relying on any opal-infrastructure-alerts alarm.
