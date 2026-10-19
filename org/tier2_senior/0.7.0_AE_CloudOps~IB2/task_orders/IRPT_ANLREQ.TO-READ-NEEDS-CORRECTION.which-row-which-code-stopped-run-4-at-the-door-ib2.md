<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-NEEDS-CORRECTION.which-row-which-code-stopped-run-4-at-the-door-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-19</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>READ</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- READ ONLY: no write, no deploy, no delete, no upload, no queue send; the only write is the record file. No ledger.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- your principal's existing read reach, or the step is written DENIED.
comp-adversary: RUN -- by reading the CTO ruling (msg 11099: read from the door's response and the resident journal which row and which reason code produced NEEDS_CORRECTION; send the key and version of the one leftover original-holdings object, row S217), your receipt A_E2E4.txt (U: 6 posts in 35 s, the resident resolved READY at 23:10:58Z, the door answered NEEDS_CORRECTION at 23:11:07Z) and PRD v0.15 item 3 (a kept unknown symbol files as UNRESOLVED; the Keep is a correction re-post whose from_value equals its to_value, AR-g-68) against this cell; the lens: a re-post or any second upload (forbidden), a printed client value (the bytes are synthetic; print only closed words, the synthetic ticker and row numbers), a printed URL, signature or token, a delete (forbidden). NOT seen (blind): whether your run kept the door's response body; this order says what to read if it did not; denominator: three reads and one closing line.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 43, workstream ZZ83: which row and which code stopped run 4 at the door (cell AR-y-424).
<owned_cells>AR-y-424</owned_cells>
</decomp_ref>

  <objective>
    Establish, by reads, which row and which closed code made the door answer NEEDS_CORRECTION to run 4's sixth post, and whether the live door carries the AR-g-68 keep-as-typed change, and send the CTO the key and version of the one leftover original-holdings object (row S217). Report ONCE to 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2 with the file path and the lines. Read only. Nothing reruns before 07:00Z Tuesday (CTO msg 11099).
  </objective>

  <context>
    Load /cloud-ops first. Your receipt `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e4/A_E2E4.txt` (commit 44f03e79fa) ends `U` at NEEDS_CORRECTION; the holdings bytes were the five-row file (Dollars of SPY changed to 101) which includes the deliberate unknown ticker ZQXWVK. The door's answer for an unknown ticker is a finding with the code `TICKER_NOT_FOUND`, its row, and a `suggestion`; the filer's Keep is a re-post carrying a correction `{finding_code, from_value, to_value}` with equal values (AR-g-68: `intake/portfolio.py` `template_corrections` and `freeze_template_portfolio`; marker literal `KEPT_AS_TYPED` and resolution `UNRESOLVED`). THE RULE: print closed words, UPPER_SNAKE codes, row numbers, the synthetic ticker, counts, times and S3 key NAMES; never a URL, signature, token, email or a value from a real client's file.
  </context>

  <the_act>
    GO now. Each step is independent; a DENIED or ERROR on one is written and the next step runs. Never delete, upload, post, redrive or send.
    1. R1 (the door's response, from your own run files): from the run-4 files you kept (the response of the sixth post or the run's log), print for the NEEDS_CORRECTION answer: its `state`, and for EACH finding its closed `finding_code`, its row number (or index), the symbol if it is the synthetic ZQXWVK or SPY/AGG/TIMXX/APPL, whether a `suggestion` member is present (boolean; print its value only if it is an UPPER-CASE ticker of at most 6 letters) and any `hints` count. If you kept no response body, print `R1 NOT-KEPT` and read step 2. Line: `R1 state=<STATE|NOT-KEPT> findings=<n> <code>@row<k>:<symbol>:suggestion=<yes|no>,...`.
    2. R2 (the resident journal): from the resident service's journal between 2026-10-19T23:09:30Z and 23:12:00Z print the window and the lines scanned, then the COUNT and the closed fields (`state=`, `code=`) of every line containing `IRPT_RESIDENT_RESOLVE`, and the counts of lines containing `RETAINED`, `NEEDS_CORRECTION`, `TICKER_NOT_FOUND`, `UNRESOLVED` and `KEPT_AS_TYPED` (counts only). Line: `R2 window=<first>..<last> scanned=<n> resolve=<n> pairs=<STATE/CODE:n,...|none> needs_correction=<n> ticker_not_found=<n> unresolved=<n> kept_as_typed=<n>`.
    3. R3 (is the keep-as-typed change live in the door): `get-function-configuration` of `irpt-ycharts-generate` for `CodeSha256` and `LastModified`; download the CURRENT package (read-only, to a private temp folder, deleted after) and print whether the file `intake/portfolio.py` inside it contains the literal `KEPT_AS_TYPED` (yes or no), whether `ycharts/generate/normalized_input.py` contains the literal `UNRESOLVED` (yes or no) and the sha256 of its `intake/portfolio.py` member. Line: `R3 codesha=<12 chars> modified=<UTC> kept_as_typed_in_portfolio=<yes|no> unresolved_in_normalized_input=<yes|no> portfolio_py_sha256=<12 chars>`.
    4. R4 (the leftover object, row IRPT_ANLREQ-D2-S217): print the S3 bucket name, key and VersionId of the one original-holdings object run 4 left (from your run records, confirmed by `head-object` and `list-object-versions` on that key), its size in bytes and its last-modified time; the key names a synthetic upload (print it as is; it holds no client name). Line: `R4 bucket=<name> key=<key> version=<VersionId> bytes=<n> modified=<UTC> versions=<n>`.
    5. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_needs_correction/A_NEEDS_CORRECTION.txt with the lines R1 to R4 (each answered, denied or `NOT-RUN <why>`) and a closing line `READS-DONE <n> of 4 answered`. Commit it. Report ONCE as in the objective: the file path and the lines, nothing more. No ledger.
  </the_act>

  <bounds>
    Read only. No post, no upload, no delete, no redrive, no queue send, no write other than the record file and one private temp folder you create and remove; no deploy; no IAM change. Nothing about Andrew's ticket TCK-20261017-5af976ff is read.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_needs_correction/IRPT_ANLREQ.TO-READ-NEEDS-CORRECTION.which-row-which-code-stopped-run-4-at-the-door-ib2.proof_of_spec.json`.
    <criterion id="NEEDC-AC1" cell_refs="AR-y-424">The record holds the four answer lines and the closing line, each answered, denied or not run.<invocation>grep -c -E '^(R1 |R2 |R3 |R4 |READS-DONE [0-9]+ of 4 answered)' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_needs_correction/A_NEEDS_CORRECTION.txt</invocation><expect>^5$</expect></criterion>
    <criterion id="NEEDC-AC2" cell_refs="AR-y-424">No line holds a token, a URL, a signature or an email address (the leak control).<invocation>grep -c -E 'eyJ[A-Za-z0-9_-]{10,}|https?://|Bearer |X-Amz-|[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[a-z]{2,}' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_needs_correction/A_NEEDS_CORRECTION.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-y-424 is the issuer's, as for TO-READ-DLQ-WHY.
