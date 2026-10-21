<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-PAGEFILED.analysis-tickets-filed-from-the-page-since-the-v024-promote-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-20</date>
    <status>complete</status><!-- flipped by issuer 2.0.0_SA_COO~Y2 2026-10-21 (round hygiene, CTO msg ~15:10Z): every criterion invocation re-run by the issuer and matched; the proof instance reads VALID rc 0 -->
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>READ</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- READ ONLY: one query or one filtered read of the tickets table, ticket ids, creation times and closed-word fields only; no write, no delete, no ticket opened, edited or notified, no queue action. The only writes are the record file and a private temp file you create and remove. No ledger.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- your principal's existing read reach, or the step is written DENIED.
comp-adversary: RUN -- by reading the CTO's ask (msg 11333: count the analysis_request tickets filed from the page since 09:28:44Z, ids and counts only, each is a ticket with no analysis behind it) and the v0.24 finding (the page's analysis submit is refused by its own client guard, so a filing creates the ticket and records no request id) against this cell; the lens: a printed title, name, email, household, answer value, upload content, token or URL (forbidden: ids, counts, times and closed words only), a write of any kind, a read of Andrew's ticket TCK-20261017-5af976ff (it was filed before 09:28:44Z; if it appears in the window, STOP and say so), a full-table dump left in a file. NOT seen (blind): whether the table has an index on ticket type and creation time (use what exists; a filtered paginated read counted client-side is acceptable, with the denominator printed); denominator: the table's item count scanned or the index's key count read.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 43, workstream ZZ115: the analysis tickets filed from the page since the v0.24 promote (cell AR-y-456).
<owned_cells>AR-y-456</owned_cells>
</decomp_ref>

  <objective>
    List, by ids and counts only, the tickets of type analysis_request created at or after 2026-10-20T09:28:44Z (the PROD live minute of the v0.24 page) in the tickets table, and say for each whether a request id / report reference was recorded on it. Report ONCE to 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2 with the file path and the four lines. GO NOW.
  </objective>

  <context>
    Load /cloud-ops first. Background: from 09:28:44Z the PROD page files an Analysis Request in four writes (upload, ticket create, analysis submit, report id recorded on the ticket) but the third write never reaches the network (the page's own client guard refuses the body), so a ticket filed through the page exists with no request id and no report reference. The CTO wants the list to re-submit after the fix. The tickets table is the one the ticket service uses (`opal-tickets`, key `ticket_id`; the item members you read in earlier orders: type, creation time, creator, the `package` map, the report reference member). Runs 1 to 6 were filed through the API before 09:28:44Z; run 7 has not started. THE RULE: print closed words, ids of the shape TCK-YYYYMMDD-8hex, counts and UTC times; never a title, name, email, household, answer value, token or URL.
  </context>

  <the_act>
    GO now.
    1. Read the tickets table for items of type analysis_request whose creation time is at or after 2026-10-20T09:28:44Z (use the index or key schema the table has; if it has none for this, use a paginated filtered read and count client-side, printing the pages and the item count scanned as the denominator). Print the UTC time of the read.
    2. T lines (ids and counts only): `T1 count=<n> since=09:28:44Z read_at=<HH:MM:SSZ> scanned=<denominator>`; `T2 ids=<comma list of ticket ids, or none>`; `T3 report_ref_held=<n> not_held=<n>` (the ticket's report/request reference member held or not, booleans counted; for the tickets that hold one print the ids in a second list `T3b held_ids=<list or none>`); `T4 creators synthetic=<n> staff=<n> other=<n>` (classed by the creator's address domain: `opal.invalid` = synthetic, `opalinvest.com` = staff, anything else other; never print an address).
    3. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_pagefiled/A_PAGEFILED.txt with the lines T1, T2, T3, T3b, T4 and a closing line `READS-DONE <n> of 4 answered`. Commit it. Report ONCE as in the objective. Remove any temp file.
  </the_act>

  <bounds>
    Read only. No write to any table, no ticket opened or edited, no notification, no queue action, no delete, no deploy, no IAM change. Nothing about Andrew's ticket TCK-20261017-5af976ff is read (if it falls in the window, STOP).
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_pagefiled/IRPT_ANLREQ.TO-READ-PAGEFILED.analysis-tickets-filed-from-the-page-since-the-v024-promote-ib2.proof_of_spec.json`.
    <criterion id="PGF-AC1" cell_refs="AR-y-456">The record holds the answer lines and the closing line.<invocation>grep -c -E '^(T1 |T2 |T3 |T3b |T4 |READS-DONE [0-9]+ of 4 answered)' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_pagefiled/A_PAGEFILED.txt</invocation><expect>^[5-6]$</expect></criterion>
    <criterion id="PGF-AC2" cell_refs="AR-y-456">No line holds a token, a URL, a signature or an email address (the leak control).<invocation>grep -c -E 'eyJ[A-Za-z0-9_-]{10,}|https?://|Bearer |X-Amz-|[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[a-z]{2,}' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_pagefiled/A_PAGEFILED.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-y-456 is the issuer's, as for TO-READ-PACKAGER-403.
