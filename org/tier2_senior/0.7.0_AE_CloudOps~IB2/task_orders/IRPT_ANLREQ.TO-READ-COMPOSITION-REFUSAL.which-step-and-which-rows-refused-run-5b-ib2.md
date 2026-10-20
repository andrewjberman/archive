<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-COMPOSITION-REFUSAL.which-step-and-which-rows-refused-run-5b-ib2</id>
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
comp-blast: DECLARED-NOT-APPLICABLE -- READ ONLY: no write, no deploy, no delete, no upload, no queue send, no post; the only writes are the record file and one private temp folder you create and remove. No ledger.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- your principal's existing read reach, or the step is written DENIED.
comp-adversary: RUN -- by reading the CTO ruling (msgs 11190 and 11192: read from the resident journal and the request record which gate refused and which rows lack a closed composition) and your receipt A_E2E5B.txt (P4: SubmissionRefused CLOSED_COMPOSITION_REQUIRED at 02:34:11Z and 02:49:12Z; three synthetic state objects stay: original-holdings csv, request_compositions json, normalized_portfolios json) against this cell; the lens: a printed client value (the bytes are synthetic; print only closed words, the synthetic tickers and booleans, NEVER a dollar amount or weight), a printed URL, signature, token or email, a write or delete of any object (forbidden), a re-run of the validator on anything but the retained synthetic composition. NOT seen (blind): whether the retained composition is the exact bytes the resident read; denominator: four reads and one closing line.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 43, workstream ZZ96: which step and which rows made the resident refuse run 5B's request (cell AR-y-437).
<owned_cells>AR-y-437</owned_cells>
</decomp_ref>

  <objective>
    Establish, by reads, which of the five steps of `CompositionAdmission.validate` refused run 5B's request, and which rows of its frozen portfolio fail the closed composition (the unknown row `ZQXWVK` kept UNRESOLVED, or also the three KEPT_BY_HISTORY rows `SPY`, `AGG`, `TIMXX`). Report ONCE to 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2 with the file path and the lines. Read only. GO NOW (this is the CTO's ruling, msg 11190).
  </objective>

  <context>
    Load /cloud-ops first. Run 5B (your receipt `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e5b/A_E2E5B.txt`, state file `state_e2e5b.json` in the same folder): the request REQ-84ca4dffd74c00a2e8999d01 was accepted after the Keep; the resident retained it for retry at 02:34:11Z and 02:49:12Z with `SubmissionRefused CLOSED_COMPOSITION_REQUIRED`. The code (`infra/aws/lambda/investor-reporting/ycharts/generate/composition_admission.py:40-64`) prints `COMPOSITION-REFUSED step=<n> error_class=<Class>` to the resident journal before it raises: 1 canonical, 2 schema, 3 compose, 4 bindings, 5 portfolio (`verify_frozen_portfolio`). The three synthetic state objects your run left under `irpt/49financial/state/` (one original-holdings csv, one request_compositions json, one normalized_portfolios json; rows S219 and S220) are READ-ONLY inputs for step 3. THE RULE: print closed words, UPPER_SNAKE codes, row numbers, the synthetic tickers SPY, AGG, TIMXX, ZQXWVK, booleans, counts and times; never a dollar amount, weight, price, URL, signature, token or email.
  </context>

  <the_act>
    GO now. Each step is independent; a DENIED or ERROR on one is written and the next step runs. Never delete, upload, post, redrive or send.
    1. R1 (the resident journal): from the resident service's journal between 2026-10-20T02:33:30Z and 02:50:30Z print the window and the lines scanned, then EVERY line containing `COMPOSITION-REFUSED` (all of it: it holds only a step number and an exception class), and the count of lines containing `retained_for_retry` and `SubmissionRefused`. Line: `R1 window=<first>..<last> scanned=<n> refused=<n> lines=<step=N class=C; ...|none> retained=<n>`.
    2. R2 (the rows, from the retained normalized portfolio): download the retained `normalized_portfolios` json of run 5B (the object named in your state file or found by the REQ id's input id; read-only, to a private temp folder) and print, for each row of its frozen document: the row index, the typed symbol (synthetic only), `method`, `resolution`, and booleans for `price` present, `provider_receipt_sha256` present and `analysis_dollars` present (never the values). Line per row: `R2 row<k> <SYMBOL> method=<M> resolution=<R|-> price=<yes|no> receipt=<yes|no> dollars=<yes|no>`.
    3. R3 (the real validator on the retained composition): download the retained `request_compositions` json of run 5B (read-only) and, from a throwaway checkout or the repository at trunk HEAD, run locally (offline, no AWS) the repository's own `CompositionAdmission(<docs/contracts/investor-reporting/v1>).validate(<that document>)` (module `infra/aws/lambda/investor-reporting/ycharts/generate/composition_admission.py`, with the `reports` and `intake` folders of the same tree on the path as the module itself arranges). Print the step number it prints (`COMPOSITION-REFUSED step=<n> error_class=<C>`) or `ADMITTED`, and, for step 2, the jsonschema validator keyword and the `/`-joined path of the first error (closed words, no value). Line: `R3 validate=<ADMITTED|step=N class=C> detail=<validator>@<path>|->`.
    4. R4 (the control): run the same validator on the same document with the `resolved.document` rows reduced, IN MEMORY ONLY, to the three KEPT_BY_HISTORY rows (drop the `ZQXWVK` row and nothing else; the digest fields will no longer bind, so a step-5 refusal for that reason is EXPECTED and is printed as is); print the same line shape. Its purpose is to see whether the refusal changes with the kept row. Line: `R4 without_ZQXWVK validate=<ADMITTED|step=N class=C> detail=<...>`.
    5. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_composition_refusal/A_COMPOSITION_REFUSAL.txt with the lines R1 to R4 (each answered, denied or `NOT-RUN <why>`) and a closing line `READS-DONE <n> of 4 answered`. Commit it. Report ONCE as in the objective: the file path and the lines, nothing more. No ledger. Remove the private temp folder.
  </the_act>

  <bounds>
    Read only. No post, no upload, no delete, no redrive, no queue send, no write other than the record file and one private temp folder you create and remove; no deploy; no IAM change; no write to S3 or any table. Nothing about Andrew's ticket TCK-20261017-5af976ff is read. This order may run beside nothing else of yours; run 5C is ON HOLD (my message).
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_composition_refusal/IRPT_ANLREQ.TO-READ-COMPOSITION-REFUSAL.which-step-and-which-rows-refused-run-5b-ib2.proof_of_spec.json`.
    <criterion id="COMPR-AC1" cell_refs="AR-y-437">The record holds the answer lines and the closing line, each answered, denied or not run.<invocation>grep -c -E '^(R1 |R2 |R3 |R4 |READS-DONE [0-9]+ of 4 answered)' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_composition_refusal/A_COMPOSITION_REFUSAL.txt</invocation><expect>^[5-9]$</expect></criterion>
    <criterion id="COMPR-AC2" cell_refs="AR-y-437">No line holds a token, a URL, a signature or an email address (the leak control).<invocation>grep -c -E 'eyJ[A-Za-z0-9_-]{10,}|https?://|Bearer |X-Amz-|[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[a-z]{2,}' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_composition_refusal/A_COMPOSITION_REFUSAL.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-y-437 is the issuer's, as for TO-READ-NEEDS-CORRECTION and TO-READ-DLQ-WHY.
