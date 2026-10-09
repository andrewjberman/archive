# pipeline-override: read-only laptop reads for dell2's IRPT_ANLREQ.TO-APPLY-Y1 AMENDMENT 1 (dell2 2.0.0_SA_COO~Y2 msg 3215, relay 0.0.0_AB_MSTR msg 107945); the laptop COO lane is the issuer because dell2 cannot decrypt irpt-requests (row IRPT_ANLREQ-D2-S8); no laptop project row to cut against
<task_order id="ADHOC.irpt-anlreq-y1-laptop-reads-3-5">
<to_id>ADHOC.irpt-anlreq-y1-laptop-reads-3-5</to_id>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~ANL</issued_to>
<date>2026-10-09</date>
<status>pending</status>
<risk>SERVED</risk>

<title>IRPT_ANLREQ release 1: the laptop's READ-ONLY reads 3a, 3b, 3c, 4 and 5 -- booleans, an expiry and outcome names only</title>

<amendment>
AMENDMENT 1 (issuer, 2026-10-09 ~15:1xZ) -- REOPENED for a RE-RUN of reads 3a, 4 and 5 only, same spec @66b6d08b9c, on the FRESH request
REQ-4b5155ac2ea9467ab771b414 (tenant 49financial; ticket TCK-20261009-a1052909). dell2 2.0.0_SA_COO~Y2 (relay 0.0.0_AB_MSTR msg 108017): its
retention row RET-f566934a... has new bytes and is not shared, so the first pass's single cause (the deleted shared row) does not apply.
- 3a: the owner's signed-link sha matches the retained original; return 3a and 3a_link_expiry.
- 4: the stored record's ticket_id AND the composition route's ticket_id equal the ticket; return 4_record and 4_route.
- 5: the pdf route. If the job is still QUEUED, wait for READY (poll read-only, a few minutes apart) before read 5. 5_outcome is one of
  SIGNED, NOT_RETAINED or RETENTION_RECORD_UNAVAILABLE.
Same rules: read-only, existing principals only, booleans, the expiry and outcome names only; no link, email, principal id or record body
anywhere. Write `org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/Y1_laptop_reads_3a_4_5_rerun_result.json`, send its sha256 to me.
</amendment>

<context>
dell2 asks the laptop for five reads that dell2 cannot make. The spec is the whole contract: read it first.
- Spec: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release1/Y1_laptop_reads_3_5_spec.json` @66b6d08b9c (on CLOUD).
- Why the laptop: row IRPT_ANLREQ-D2-S8. dell2 cannot decrypt `irpt-requests`, and a synthetic advisor cannot own a request
  (uploads.py:188-195).
- Release 1 is LIVE on `irpt-status`, CodeSha256 BjUZjt2oq8GPJSibq4vD/0m8/LfdN0GF3THwCaBMVOM=, since 11:20:57Z.
- This order follows the pattern of the Y75 read-back the laptop ran today (IRPT_BCKEND.TO-APPLY-Y75).
</context>

<scope>
1. Load /cloud-ops. Read the spec, then the `irpt-status` handler source at the release-1 commit, to learn how each GET route resolves
   its caller principal. Reach each GET the way the service's own tests or tools exercise it as a principal: a direct invoke of the
   function with the event the front door would pass, carrying the principal's claims. Say which method you used.
   - Use the request's real OWNER principal only for 3a, as the spec says.
   - For 3b, use a firm-bound principal of a firm other than 49financial.
   - Mint no credential, create no user, and write nothing.
2. Run reads 3a, 3b, 3c, 4 and 5 exactly as the spec defines them. 3c reads an existing custody-lane request only; if none exists,
   return null with exists=false.
3. Report ONLY the spec's `return` shape: booleans, `3a_link_expiry` and `5_outcome`.
   - NEVER log, store or print a signed link, an email, a principal id or a record body.
   - Compute 3a's sha256 match in memory.
   - Count email-shaped strings over every file you write; the count must be 0.
4. Write the result to the spec's `result_path`, `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release1/Y1_laptop_reads_3_5_result.json`.
   If owned-paths refuses it for your seat, write it under your own deliverables and send its sha256 to 2.0.0_SA_COO~C. dell2 commits
   it on its path.
5. Writes: NONE. No delete, no create, no policy or resource change.
</scope>

<proof_of_spec>
<criterion id="AC1" cell_refs="ADHOC"><invocation>python -c "import json,glob;p=(glob.glob('org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release1/Y1_laptop_reads_3_5_result.json')+glob.glob('org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/Y1_laptop_reads_3_5_result.json'))[0];d=json.load(open(p));r=d.get('reads',d);print('READS', sorted(r))"</invocation><expect>READS [</expect></criterion>
</proof_of_spec>
<expected_criteria>AC1</expected_criteria>
AC1 shows the result file exists with its read keys. The values are graded by dell2's issuer, not here.

<paths>
org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release1/
org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~ANL/logs/
</paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE one set of reads on dell2's request.
comp-iam: RUN -- the laptop identity reads irpt-requests (decrypt) and invokes irpt-status read routes; denominator 5 reads, 2 principals (the owner; one other-firm principal); BLIND to every other route.
comp-adversary: RUN -- a signed link or identity leaked into a file or message (booleans, an expiry and outcome names only; email count 0); a write disguised as a read (no create, no delete; 3c reads an existing request only); a principal minted for the test (forbidden; existing principals only); BLIND: what the owner does with the link (none is issued to anyone; the link is discarded in memory).
lane: the <paths> block names the result directory and the seat's own deliverables and logs.
</preflight>
</task_order>
