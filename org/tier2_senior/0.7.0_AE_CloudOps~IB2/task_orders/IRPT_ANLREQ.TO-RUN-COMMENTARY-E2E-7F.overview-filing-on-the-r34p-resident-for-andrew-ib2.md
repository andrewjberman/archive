<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-RUN-COMMENTARY-E2E-7F.overview-filing-on-the-r34p-resident-for-andrew-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-20</date>
    <status>staged</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>43</round>
<workstream>ZZ141</workstream>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is run 7d's: one synthetic request filed through the PROD portal page by a minted synthetic staff user, every created key recorded at creation and deleted after the last read where the principal can; no Terraform, no IAM change, no code change. Run 7c's receipt (A_E2E7C.txt) and rows S233 and S234 are the base.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE.
comp-iam: DECLARED-NOT-APPLICABLE -- the grants stand (ledgers irpt-status-opal-report-read-20261020 and irpt-status-r37-20261020 CLOSED before this run); this order adds none.
comp-adversary: RUN -- by reading run 7d's receipt, the CTO's rulings (msgs 11508, 11510, 11512, 11521) and the two route fixes against this order; the lens: the r37 apply not closed or not the expected CodeSha256 (R0 reads red, nothing is minted), the Overview route answering a refusal that is neither of the two route names (read the log, no retry), a saved PDF that is committed or pasted (it is saved OUTSIDE the repository and only its size, sha256 and page count are written down), the Overview PDF read as proof that it is correct (Andrew judges that, FWD-9), the commentary route's answer taken as the Overview's, leftover objects of runs 7, 7b and 7c mistaken for this run's, a second filing after a red hop. NOT seen (blind): what the signed links resolve to for a human in a browser; denominator: one request.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 43, workstream ZZ141: run 7f (cell AR-y-482).
<owned_cells>AR-y-482</owned_cells>
</decomp_ref>

  <objective>
    Run 7f is RUN 7d (order `IRPT_ANLREQ.TO-RUN-COMMENTARY-E2E-7D.staff-filing-and-both-report-pdfs-open-ib2.md`, in this folder; receipt `irpt_anlreq_commentary_e2e7d/A_E2E7D.txt`, RUN-DONE PASS) ON THE SAME TERMS, with the REPLACEMENTS below: one synthetic request filed through the PROD portal page by an unseeded synthetic staff user whose form Advisor is left AS THE PAGE PRE-FILLS IT, going on to read BOTH report-PDF routes of the status Lambda and saving the Opal Overview PDF for Andrew's FWD-9 read, stopping at the first red hop except where a replacement says otherwise. THIS ORDER STARTS ONLY ON MY GO MESSAGE. Read run 7d's order and receipt in full first: its steps, ledger legs, R0 gates and receipt apply unchanged except where the REPLACEMENTS say.
  </objective>

  <context>
    WHY: run 7d passed on the r34n resident (RUN-DONE PASS, Overview 39 pages, saved as Opal_Overview_sample_E2E7D.pdf). Run 7e (r34o resident) stopped at the packager with RetentionRefused (row S239; CTO ruling msg 11640): r34o had edited a registry row in place. The resident is now r34p (r34o minus that registry edit; root as G2 reports it and IB2's r34p receipt shows, V2S OK), which keeps the price pages; Andrew reads THE OVERVIEW AFTER r34p for FWD-9 (CTO msgs 11621, 11640). This is one synthetic Overview filing (no comparables) through the PROD page, the Overview saved for his read, and the page count reported.
    THE REPLACEMENTS. (R0) every 7d R0 read stands, plus: the resident root equals the root in IB2's r34p receipt (not r34n or r34o), the r34p ledger is CLOSED with V2S OK, and `irpt-status` CodeSha256 still equals B4R0dZqBRhclmQLOiBHp3Ft/wNbMomNZhUflCCRfEyE=. A red R0 mints NOTHING. (A, A2, L, B1, B2, B3, P1-P5, P7, R2) as 7c: new unique holdings hash, non-empty synthetic filer name, ONE press, no Keep.
    (R) THE OVERVIEW ROUTE: `GET /api/scoped/investor-reporting/analysis/requests/{REQ}/pdf` (route `analysis-request-pdf`). Read its closed code and, when it answers a link, follow the link with a plain GET: the response must be a PDF (first four bytes `%PDF`); print the size and sha256 and the page count of the PDF; never print the URL. If it answers a refusal code, STOP at R (no R3, no R4 stop): read the irpt-status log for the refusal name and the key shape only, write the row, no retry, no IAM change.
    (R3) THE OVERVIEW FOR ANDREW (FWD-9): when R answers a PDF, save it UNCHANGED to `C:/dev/andrew_samples/Opal_Overview_sample_post_r34p.pdf` (create the folder; it is OUTSIDE the repository: do NOT commit this file or paste its text anywhere), and write only its size, sha256 (12 hex) and page count into the receipt and the message. If R fails there is no R3 line: write `R3 NOT-RUN R`.
    (R4) THE COMMENTARY ROUTE: after R (whether it passed or not, unless R stopped on a log-read reason you cannot continue past), `GET .../analysis/requests/{REQ}/commentary-pdf`: the closed code or, when it answers a link, a plain GET whose first four bytes are `%PDF`: size and sha256 (12 hex), page count. A refusal here does NOT change the closing line if R passed: it is its own row (`R4 REFUSED <closed code>`), the run still reaches D.
    (D) delete only keys recorded at creation; the leftover objects of runs 7, 7b and 7c stay and are not this run's; for this run's own residue that your principal cannot delete, list each exact key and its VersionId from list-object-versions in `irpt_anlreq_commentary_e2e7f/residue_7f.json` (bucket, key, version_id, size) and file the row.
    THE RECEIPT (also: print the PAGE COUNT of the saved Overview and whether it is longer than run 7d's 39 pages; do not read or quote its text): write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7f/A_E2E7F.txt with run 7d's lines (each answered or `NOT-RUN <the hop where the run stopped>`), then `R3 pdf=<size> sha256=<12 hex> pages=<n> saved=outside-repo` or `R3 NOT-RUN R`, then `R4 commentary pdf=<size> sha256=<12 hex> pages=<n>` or `R4 REFUSED <closed code>` or `R4 NOT-RUN <why>`, then the closing line `RUN-DONE PASS` (R and R3 passed) or `RUN-DONE STOP at <hop> code=<code>`.
  </context>

  <the_act>
    GO only on my message (it names the r37 receipt's closed lines and the CodeSha256 read). Start at run 7d's step 1 (with the ledger irpt-commentary-e2e-7f-20261021, legs A mint, B browser, P poll, R route read, D delete; commit it; the open-deploys denominator as there) and go on only while each step reads green. A red hop is a STOP. Report ONCE to 2.0.0_SA_COO~Y2 (cc 1.0.0_SA_CTO~DELL2) with the receipt path, the closing line, and the path of the saved Overview PDF if there is one.
  </the_act>

  <bounds>
    One request, one press, no Keep, no second filing after a red hop. No Terraform, IAM or code change. No ticket other than this run's own synthetic one is touched, and Andrew's ticket TCK-20261017-5af976ff is not. Runs 7, 7b and 7c leftover objects stay. The synthetic user and everything this run created are deleted after the last read, except what the principal cannot delete (recorded with VersionIds and filed as a row). The saved PDF lives outside the repository and is never committed or quoted.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7f/IRPT_ANLREQ.TO-RUN-COMMENTARY-E2E-7F.overview-filing-on-the-r34p-resident-for-andrew-ib2.proof_of_spec.json`.
    <criterion id="E2E7F-AC1" cell_refs="AR-y-482">The record holds all twenty lines, each answered or marked not run.<invocation>grep -c -E '^(R0|A|A2|L|B1|B2|B3|P1|P2|P3|P4|P5|P7|R|R2|R3|R4|DLQ|D) |^RUN-DONE (PASS|STOP at )' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7f/A_E2E7F.txt</invocation><expect>^20$</expect></criterion>
    <criterion id="E2E7F-AC2" cell_refs="AR-y-482">The run is honest about its ending (a pass, or a stop at a named hop).<invocation>grep -c -E '^RUN-DONE (PASS|STOP at [A-Z0-9]+ code=[A-Z0-9_]+)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7f/A_E2E7F.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="E2E7F-AC3" cell_refs="AR-y-482">The ledger irpt-commentary-e2e-7f-20261021 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-commentary-e2e-7f-20261021_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 CloudOps seat under ADDENDUM 9 as the CTO's msgs 11508, 11510, 11512 and 11521 carry it (run 7f on run 7d's terms), not a worker cell; the cell AR-y-482 is the issuer's, as for TO-RUN-COMMENTARY-E2E-7C.

<!-- 7F NOTE (2.0.0_SA_COO~Y2, 2026-10-21): this order IS run 7e re-run on the r34p resident (r34o = r34p plus the registry edit that made run 7e refuse, row S239; ruling CTO msg 11640). R0 must read the resident root G2 reports for r34p (its receipt) and V2S OK, replacing the r34o root; everything else stands. Starts only on my GO after r34p is live. Page count compared with run 7d's 39. -->
