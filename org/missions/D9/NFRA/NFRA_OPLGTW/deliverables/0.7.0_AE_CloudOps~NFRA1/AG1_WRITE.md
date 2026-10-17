# OG-ap-35 Phase B -- the write (record)

- Re-read at the GO (C2, C7), before the write: her profile and grant revision 4 and 4, operations describe, download_filtered, list, query, scope-without-operations hash 5f95dcbca8, the two other principals' grant hashes equal to AG1_BEFORE, her email_deny record present (hash 1c83c567ea). `AG1_REREAD_before.json`: nothing moved since Phase A.
- ONE activate, role `opal-gateway-access-admin`, approver field "Andrew Berman" (data owner per the writer's schema), source authorization the CTO ruling plus ask sha256 224a80d88a52, summary carrying the CT1 sentence. Script `ag1_activate.py`; full output off-repo.
- Result line: `ACTIVATED profile_revision=5 grant_revision=5`.
- Re-read after (`AG1_REREAD_after.json`): operations describe, list, query; scope-without-operations hash 5f95dcbca8 (equal); the two other principals' hashes unchanged; email_deny hash 1c83c567ea before and after (equal).
- Host read-back (`AG1_HOSTREAD.json`, SSM command c22f52ff, installed code, in-process, no call as her): profile 5 and grant 5, `schwab_prepare_download` refused (entitlement_denied), `schwab_list_files`, `schwab_describe_dataset` and `schwab_query` answer. 1 profile matched the pk hash in 1858 items scanned.
- No contact with her or her firm; no call as her principal.
