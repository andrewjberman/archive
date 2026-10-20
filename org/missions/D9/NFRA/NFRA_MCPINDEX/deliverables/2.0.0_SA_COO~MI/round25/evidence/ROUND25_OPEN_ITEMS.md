# NFRA_MCPINDEX round 25 - what is done and what is open (2.0.0_SA_COO~MI, 2026-10-20 ~17:5xZ)

Done: six orders MX-y-1..6 complete and merged (51a7514f237). round-close-check --round 25 reads orders 6/6 complete, proofs 6/6 valid, verdict REFUSED ONLY because no reviewer seat is on the box (reviewer=ABSENT; liveness.json lists one registered seat while the agent-comms broker is disconnected). dep_stage stays EXECUTING until MAY-CLOSE.
1 source compare by class: by-key rule live: 106 tools with an ok result: agrees 30, disagrees 1 (harvest_query_columns), unreadable 75 (graph 33, s3 undated 29, integration 9, store 4). The probes path (--probes) is merged; independent reads for graph, integration and store need a read route outside the gateway: none exists in this session, so those 46 stay source_unchecked with their reasons.
2 harvest_query_columns: attributed (MX-y-5): code, app/harvest_figures.py:168-171 (_stamp_of reads the part write stamp before the date= partition); filed as row NFRA_OPLGTW-Z-S438 for 2.0.0_SA_COO~O (b5ba135803e).
3,4 group links and store words: merged (MX-y-3); the five client_* tools are member a with exact row-list groups (link_groups_client.json: the key-only form over-linked them to 101-120 rows each, so the groups file takes an explicit rows list); store rows renamed (dynamodb_*), scoped-API row amgt-scoped-api. Coverage 2 refusals (opal_describe, opal_discover), 94 explained; routing link 0, code 3.
5 test-send grading: merged (MX-y-2); send_email and create_draft PASS on the owner's own read-back; send_chat_message PREVIEW-ONLY. Battery PASS 51, EMPTY-CORRECT 4, PREVIEW-ONLY 2, FAIL 70 of 127.
6 link rule: merged (MX-y-4); link misroutes 7 -> 0 on candidate d.
7 sheets: the upload manifest is merged (MX-y-6); the 17 sheets are NOT uploaded (below).
Catalog: candidate d (md5 cf9c1329027716ee6f45549721d30609) placed in the repo under the audited lane override (ec8fb1d6ff4); NOT deployed: it rides 2.0.0_SA_COO~O's next batched release, to be named in the ask to it.

Open:
a. SHEETS FOLDER: the ruling says "Opal Gateway Cheat Sheets" in upload_text_to_site's default site, but that tool has no default site (required site_id, no overwrite, no delete tool in the gateway). Candidate sites (find_sharepoint_site "Opal"): OpalOCIO, OpalCapital, OpalConsulting, OpalCIOOfficefor49Financial, OpalTradeSubmissionsandApprovals501, 49Financial. A team site's members can read the folder, so choosing one is the delivery decision Andrew holds, and a written file cannot be removed from here. Which site_id?
b. The agent-comms broker (opal-agent-comms) disconnected this session: no mail could be sent to the CTO or COO~O, and the reviewer seat is not listed live. The L10 slug waits on it.
c. Item 8 (re-run the battery and routing on opal-data-assets) waits for batch16 (2026-10-21 06:00Z).
d. The 46 graph/integration/store source checks need an independent read route (or the CTO accepts the reasons as the verdict).
e. The catalog deploy (COO~O's batched release).
