<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-APPL-SUGGEST.why-the-door-gave-appl-no-suggestion-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-20</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>READ</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- READ ONLY: no write, no deploy, no delete, no upload, no queue send; the only write is the record file. No ledger.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: RUN-AS-A-READ -- one policy simulation for one role and one secret ARN (names and allowed or denied only); no IAM change.
comp-adversary: RUN -- by reading the CTO finding (msg 11186: the door gave APPL no suggestion; C-FILING-HINT should offer "Did you mean AAPL"), your receipt A_E2E5.txt (run 5: five findings, none with a suggestion), the code (`ycharts/generate/resident_worker.py` `_check_gate`, which journals `IRPT_RESIDENT_SUGGEST asked= suggested= verified= unasked= elapsed_s=` and the Kimi port's `IRPT_RESIDENT_KIMI` telemetry; `intake/upload_suggestions.py`: the advisory failing, or a suggestion the same provider read does not answer FOUND, leaves the finding without one) against this cell; the lens: a printed secret value (forbidden: the key is read by NAME and never printed), a printed URL or token, a second upload or post (forbidden), a delete (forbidden). NOT seen (blind): the live journal and the secret until the steps run; denominator: three reads and one closing line.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 43, workstream ZZ93: why the live door gave the typo APPL no suggestion (cell AR-y-434).
<owned_cells>AR-y-434</owned_cells>
</decomp_ref>

  <objective>
    Establish, by reads, why the live door answered run 5's typo `APPL` with no suggestion: whether the resident asked the advisory, what it got, and whether the advisory's secret is present and readable by the resident's role. Report ONCE to 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2 with the file path and the lines. Read only. THIS ORDER STARTS ONLY ON MY GO MESSAGE (after run 5B's ledger closes).
  </objective>

  <context>
    Load /cloud-ops first. Run 5 (your receipt `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e5/A_E2E5.txt`): U first post 2026-10-20T02:04:30Z, the answer at 02:05:17Z carried `TICKER_NOT_FOUND` for `APPL` (row 5) and `ZQXWVK` (row 6) with `suggestion=no`. In the resident, `_check_gate` builds the advisory from the session's `kimi_advisory()` (Kimi key read BY NAME from Secrets Manager: secret id `astn/kimi/api-key`, `ycharts/generate/kimi_port.py`) and asks it about each NOT_FOUND row (at most `MAX_SUGGESTED_ROWS`, a per-upload deadline of 240 s); a suggestion is shown only when the SAME provider read answers FOUND for it. THE RULE: print closed words, UPPER_SNAKE codes, counts, times and key NAMES; never a secret value, URL, signature, token or email.
  </context>

  <the_act>
    GO on my GO message. Each step is independent; a DENIED or ERROR on one is written and the next step runs. Never delete, upload, post, redrive or send.
    1. R1 (the resident journal, run 5): from the resident service's journal between 2026-10-20T02:03:30Z and 02:06:30Z print the window and the lines scanned, then every line containing `IRPT_RESIDENT_SUGGEST` (all fields) and every line containing `IRPT_RESIDENT_KIMI` (all fields, `tokens=` included; these lines carry closed words and counts only), and the COUNT of lines containing `IRPT_RESIDENT_RESOLVE`. Line: `R1 window=<first>..<last> scanned=<n> suggest=<line or none> kimi=<n lines: outcome fields> resolve=<n>`.
    2. R2 (the same for run 5B): the same reads for the window 2026-10-20T02:33:00Z to 02:34:30Z (run 5B carries only ZQXWVK as a NOT_FOUND row). Line: `R2 window=<first>..<last> scanned=<n> suggest=<line or none> kimi=<n lines: outcome fields>`.
    3. R3 (the advisory's secret and the role): (a) `aws secretsmanager describe-secret --secret-id astn/kimi/api-key`: print only Name, LastChangedDate, DeletedDate present or absent, and the rotation flag (never `get-secret-value`); (b) `aws iam simulate-principal-policy` for the resident host's instance role (read it from the instance profile of the resident instance; print the role NAME) on `secretsmanager:GetSecretValue` against that secret's ARN: print allowed or denied and the matching statement id if any. Line: `R3 secret=<present|absent> changed=<UTC> deleted=<yes|no> role=<name> get_secret_value=<allowed|denied|ERROR code>`.
    4. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_appl_suggest/A_APPL_SUGGEST.txt with the lines R1 to R3 (each answered, denied or `NOT-RUN <why>`) and a closing line `READS-DONE <n> of 3 answered`. Commit it. Report ONCE as in the objective: the file path and the lines, nothing more. No ledger.
  </the_act>

  <bounds>
    Read only. No post, no upload, no delete, no redrive, no queue send, no `get-secret-value`, no write other than the record file; no deploy; no IAM change. Nothing about Andrew's ticket TCK-20261017-5af976ff is read.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_appl_suggest/IRPT_ANLREQ.TO-READ-APPL-SUGGEST.why-the-door-gave-appl-no-suggestion-ib2.proof_of_spec.json`.
    <criterion id="APPLS-AC1" cell_refs="AR-y-434">The record holds the three answer lines and the closing line, each answered, denied or not run.<invocation>grep -c -E '^(R1 |R2 |R3 |READS-DONE [0-9]+ of 3 answered)' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_appl_suggest/A_APPL_SUGGEST.txt</invocation><expect>^4$</expect></criterion>
    <criterion id="APPLS-AC2" cell_refs="AR-y-434">No line holds a token, a URL, a signature or an email address (the leak control).<invocation>grep -c -E 'eyJ[A-Za-z0-9_-]{10,}|https?://|Bearer |X-Amz-|[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[a-z]{2,}' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_appl_suggest/A_APPL_SUGGEST.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-y-434 is the issuer's, as for TO-READ-NEEDS-CORRECTION and TO-READ-DLQ-WHY.
