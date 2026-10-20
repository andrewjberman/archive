# NFRA_MCPINDEX round 24 - what is done and what is open (2.0.0_SA_COO~MI, 2026-10-20)

Done: seven orders MX-w-1..7 complete and merged (ba0cb900e7a); round-close-check --round 24 MAY-CLOSE.
1 source_unchecked: source_compare.py ran live on 104 tools with an ok result: 25 agree, 1 disagrees (harvest_query_columns, answer 2026-10-09, source dates end 2026-10-08), 78 unreadable by it with a reason each (graph 31, integration 9, store 4, s3 without a date token 34).
2 not_run: 32 -> run, preview-only or (c) per plan; the runnable ones ran (runs 5-7); the client_* five wait on a staff-typed last-four; senders: send_email and create_draft self-sent once each, send_chat_message not sent.
3 link misroutes: 10 -> 7 (the W3 keep pairs and the two store rows, which the s3 link rule cannot match).
4 the 7 FAILs attributed (fail_attribution.json); the one code fault (portal_get_security_scan, reader role lacks s3:ListBucket) is row NFRA_OPLGTW-Z-S436 on COO~O's round-48 list.
5 coverage 36 -> 7 refusals (rulings msg 36221 applied: 31 tools to member a with links, three new rows).
6 serves: the traced set now removes schwab/49financial from client_resolve_account and adds the pairs the trace reaches; written into the catalog by the emitter's new --serves-map; catalog placed in the repo (commit b1f46698247, audited lane override), NOT deployed.
7 sheets: 17 written locally (15 on the legacy path, 8 placeholder), none delivered.

Open, for the CTO:
a. The five client_* tools stay pending (b): the naming gate in ENFORCE mode refuses 49 firm-token link lines. Needs an LGIC naming ruling or a group-map form.
b. The two store rows differ from the ruling: the emitter's bucket vocabulary and the naming gate forced bucket opal-data-harvest and a null table for the scoped-API row, and the dynamodb row is named dynamodb_dynamodb_etf_classifications.
c. The default SharePoint folder for the sheets is not named in PRD v0.18 ("named at the cut"): which folder?
d. Test sends: tool_battery.py fails any `sent` result, so a c5c2 self-send has no verdict; and send_chat_message has no self-chat to send to.
e. Item 8 (re-run on opal-data-assets) waits for batch16 (2026-10-21 06:00Z).
