<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-RUN-COMMENTARY-E2E-7D.staff-filing-and-both-report-pdfs-open-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-20</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>43</round>
<workstream>ZZ135</workstream>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is run 7c's: one synthetic request filed through the PROD portal page by a minted synthetic staff user, every created key recorded at creation and deleted after the last read where the principal can; no Terraform, no IAM change, no code change. Run 7c's receipt (A_E2E7C.txt) and rows S233 and S234 are the base.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE.
comp-iam: DECLARED-NOT-APPLICABLE -- the grants stand (ledgers irpt-status-opal-report-read-20261020 and irpt-status-r37-20261020 CLOSED before this run); this order adds none.
comp-adversary: RUN -- by reading run 7c's receipt, the CTO's rulings (msgs 11508, 11510, 11512, 11521) and the two route fixes against this order; the lens: the r37 apply not closed or not the expected CodeSha256 (R0 reads red, nothing is minted), the Overview route answering a refusal that is neither of the two route names (read the log, no retry), a saved PDF that is committed or pasted (it is saved OUTSIDE the repository and only its size, sha256 and page count are written down), the Overview PDF read as proof that it is correct (Andrew judges that, FWD-9), the commentary route's answer taken as the Overview's, leftover objects of runs 7, 7b and 7c mistaken for this run's, a second filing after a red hop. NOT seen (blind): what the signed links resolve to for a human in a browser; denominator: one request.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 43, workstream ZZ135: run 7d (cell AR-y-476).
<owned_cells>AR-y-476</owned_cells>
</decomp_ref>

  <objective>
    Run 7d is RUN 7c (order `IRPT_ANLREQ.TO-RUN-COMMENTARY-E2E-7C.staff-filing-and-the-report-opens-ib2.md`, in this folder; receipt `irpt_anlreq_commentary_e2e7c/A_E2E7C.txt`, which stopped at R) ON THE SAME TERMS, with the REPLACEMENTS below: one synthetic request filed through the PROD portal page by an unseeded synthetic staff user whose form Advisor is left AS THE PAGE PRE-FILLS IT, going on to read BOTH report-PDF routes of the status Lambda and saving the Opal Overview PDF for Andrew's FWD-9 read, stopping at the first red hop except where a replacement says otherwise. THIS ORDER STARTS ONLY ON MY GO MESSAGE. Read run 7c's order and receipt in full first: its steps, ledger legs, R0 gates and receipt apply unchanged except where the REPLACEMENTS say.
  </objective>

  <context>
    WHY: run 7c went green through the four attachments and the sections read, then stopped at R: the commentary route refused COMMENTARY_PDF_BINDING (the PDF's sha was compared with the draft's), and the Overview route (`/pdf`) was never read; worker 345 then found that route refuses every real Opal report. Both are fixed in owned_report.py (AR-y-470, AR-y-472) and released by IRPT_ANLREQ.TO-APPLY-R37.irpt-status-two-pdf-routes-ib2 (CodeSha256 B4R0dZqBRhclmQLOiBHp3Ft/wNbMomNZhUflCCRfEyE=, receipt irpt_anlreq_r37/A_AFTER_R37.txt).
    THE REPLACEMENTS. (R0) every 7c R0 read stands, plus: `get-function irpt-status` CodeSha256 equals B4R0dZqBRhclmQLOiBHp3Ft/wNbMomNZhUflCCRfEyE=, and the r37 receipt reads its six lines as written with its ledger CLOSED. A red R0 mints NOTHING. (A, A2, L, B1, B2, B3, P1-P5, P7, R2) as 7c: new unique holdings hash, non-empty synthetic filer name, ONE press, no Keep.
    (R) THE OVERVIEW ROUTE: `GET /api/scoped/investor-reporting/analysis/requests/{REQ}/pdf` (route `analysis-request-pdf`). Read its closed code and, when it answers a link, follow the link with a plain GET: the response must be a PDF (first four bytes `%PDF`); print the size and sha256 and the page count of the PDF; never print the URL. If it answers a refusal code, STOP at R (no R3, no R4 stop): read the irpt-status log for the refusal name and the key shape only, write the row, no retry, no IAM change.
    (R3) THE OVERVIEW FOR ANDREW (FWD-9): when R answers a PDF, save it UNCHANGED to `C:/dev/andrew_samples/Opal_Overview_sample_E2E7D.pdf` (create the folder; it is OUTSIDE the repository: do NOT commit this file or paste its text anywhere), and write only its size, sha256 (12 hex) and page count into the receipt and the message. If R fails there is no R3 line: write `R3 NOT-RUN R`.
    (R4) THE COMMENTARY ROUTE: after R (whether it passed or not, unless R stopped on a log-read reason you cannot continue past), `GET .../analysis/requests/{REQ}/commentary-pdf`: the closed code or, when it answers a link, a plain GET whose first four bytes are `%PDF`: size and sha256 (12 hex), page count. A refusal here does NOT change the closing line if R passed: it is its own row (`R4 REFUSED <closed code>`), the run still reaches D.
    (D) delete only keys recorded at creation; the leftover objects of runs 7, 7b and 7c stay and are not this run's; for this run's own residue that your principal cannot delete, list each exact key and its VersionId from list-object-versions in `irpt_anlreq_commentary_e2e7d/residue_7d.json` (bucket, key, version_id, size) and file the row.
    THE RECEIPT: write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7d/A_E2E7D.txt with run 7c's eighteen lines (each answered or `NOT-RUN <the hop where the run stopped>`), then `R3 pdf=<size> sha256=<12 hex> pages=<n> saved=outside-repo` or `R3 NOT-RUN R`, then `R4 commentary pdf=<size> sha256=<12 hex> pages=<n>` or `R4 REFUSED <closed code>` or `R4 NOT-RUN <why>`, then the closing line `RUN-DONE PASS` (R and R3 passed) or `RUN-DONE STOP at <hop> code=<code>`.
  </context>

  <the_act>
    GO only on my message (it names the r37 receipt's closed lines and the CodeSha256 read). Start at run 7c's step 1 (with the ledger irpt-commentary-e2e-7d-20261020, legs A mint, B browser, P poll, R route read, D delete; commit it; the open-deploys denominator as there) and go on only while each step reads green. A red hop is a STOP. Report ONCE to 2.0.0_SA_COO~Y2 (cc 1.0.0_SA_CTO~DELL2) with the receipt path, the closing line, and the path of the saved Overview PDF if there is one.
  </the_act>

  <bounds>
    One request, one press, no Keep, no second filing after a red hop. No Terraform, IAM or code change. No ticket other than this run's own synthetic one is touched, and Andrew's ticket TCK-20261017-5af976ff is not. Runs 7, 7b and 7c leftover objects stay. The synthetic user and everything this run created are deleted after the last read, except what the principal cannot delete (recorded with VersionIds and filed as a row). The saved PDF lives outside the repository and is never committed or quoted.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7d/IRPT_ANLREQ.TO-RUN-COMMENTARY-E2E-7D.staff-filing-and-both-report-pdfs-open-ib2.proof_of_spec.json`.
    <criterion id="E2E7D-AC1" cell_refs="AR-y-476">The record holds all twenty lines, each answered or marked not run.<invocation>grep -c -E '^(R0|A|A2|L|B1|B2|B3|P1|P2|P3|P4|P5|P7|R|R2|R3|R4|DLQ|D) |^RUN-DONE (PASS|STOP at )' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7d/A_E2E7D.txt</invocation><expect>^20$</expect></criterion>
    <criterion id="E2E7D-AC2" cell_refs="AR-y-476">The run is honest about its ending (a pass, or a stop at a named hop).<invocation>grep -c -E '^RUN-DONE (PASS|STOP at [A-Z0-9]+ code=[A-Z0-9_]+)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7d/A_E2E7D.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="E2E7D-AC3" cell_refs="AR-y-476">The ledger irpt-commentary-e2e-7d-20261020 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-commentary-e2e-7d-20261020_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 CloudOps seat under ADDENDUM 9 as the CTO's msgs 11508, 11510, 11512 and 11521 carry it (run 7d on run 7c's terms), not a worker cell; the cell AR-y-476 is the issuer's, as for TO-RUN-COMMENTARY-E2E-7C.
