<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-RUN-COMMENTARY-E2E-7C.staff-filing-and-the-report-opens-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-20</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>43</round>
<workstream>ZZ124</workstream>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is run 7b's: one synthetic request filed through the PROD portal page by a minted synthetic staff user, every created key recorded at creation and deleted after the last read where the principal can; no Terraform, no IAM change, no code change. Run 7b's receipt (A_E2E7B.txt) and rows S231 and S232 are the base.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE.
comp-iam: DECLARED-NOT-APPLICABLE -- the grants stand (ledger irpt-status-opal-report-read-20261020 CLOSED before this run); this order adds none.
comp-adversary: RUN -- by reading run 7b's receipt and the CTO's rulings (msgs 11459, 11475) against this order; the lens: a status grant that applied but did not cover the exact key family the route reads (the route would answer UNEXPECTED again: STOP at R, read the log, no retry), a second denial deeper in the route (a new row), the report PDF read as proof the Overview is correct (Andrew judges that, FWD-9), a copy of the PDF that carries a real name or figure (the holdings are synthetic), run 7b's seven leftover objects (row S232) and run 7's (row S229) mistaken for this run's, a second filing after a red hop. NOT seen (blind): what the route does after the PDF read; denominator: one request.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 43, workstream ZZ124: run 7c (cell AR-y-465).
<owned_cells>AR-y-465</owned_cells>
</decomp_ref>

  <objective>
    Run 7c is RUN 7b (order `IRPT_ANLREQ.TO-RUN-COMMENTARY-E2E-7B.staff-filing-through-the-advisor-required-form-on-prod-ib2.md`, in this folder; receipt `irpt_anlreq_commentary_e2e7b/A_E2E7B.txt`, which stopped at R) ON THE SAME TERMS, with the REPLACEMENTS below: one synthetic request filed through the PROD portal page by an unseeded synthetic staff user whose form Advisor is left AS THE PAGE PRE-FILLS IT, going on past R to read the route, the sections, and the Opal report PDF the ticket opens, stopping at the first red hop. THIS ORDER STARTS ONLY ON MY GO MESSAGE. Read run 7b's order and receipt in full first: its steps, ledger legs, R0 gates and eighteen-line receipt apply unchanged except where the REPLACEMENTS say.
  </objective>

  <context>
    WHY: run 7b filed through the page and went green through the four attachments, then stopped at R because `irpt-status-role` was denied `s3:GetObjectVersion` on the retained Opal report PDF. The grant is applied by IRPT_ANLREQ.TO-APPLY-STATUSGRANT (ledger irpt-status-opal-report-read-20261020, receipt irpt_anlreq_statusgrant/A_AFTER_STATUSGRANT.txt, G2 line allowed on the 7b key). This run re-runs the filing and reads what 7b could not.
    THE REPLACEMENTS. (R0) every 7b R0 read stands (PROD tip 234cddba2d83 unless the DT's walk record names a later promote; root `0485393f3a-r34n`; the CodeSha256 values; the DLQ depth before), plus: the status grant's receipt reads all six lines as written and its ledger CLOSED. A red R0 mints NOTHING. (A) mint with a non-empty synthetic NAME exactly as 7b did (print it). (B) the instrument is the re-proved script under `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~325/` as in 7b, with a NEW synthetic holdings file whose sha256 differs from every earlier run's (print it); ONE press, no Keep, no second filing. (R) the route read `GET analysis/requests/{REQ}/commentary-pdf` must now answer a PDF; read its closed code and, when it answers, the PDF's size and the first four bytes (`%PDF`); if it answers a closed refusal code, STOP, read the irpt-status log for the denied action and key (counts and the key shape only), write the row, no retry, no IAM change. (R2) as 7b. (R3, new) the OPAL OVERVIEW SAMPLE FOR ANDREW (FWD-9): when R answers a PDF, save that PDF unchanged to `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7c/Opal_Overview_sample_E2E7C.pdf` (the holdings are synthetic: household `E2E7 SYNTHETIC`, tickers `SYNTH-*`, so no client data is in it), print its size and sha256, and open its first page text with any PDF reader already on the box to print the number of pages and whether the page text names `E2E7 SYNTHETIC` (counts and the yes/no only; do not paste its text). If R fails there is no R3 line: write `R3 NOT-RUN R`. (D) delete only keys recorded at creation; the leftover objects of runs 7 and 7b stay and are not this run's; if this run's own upload leaves objects your principal cannot delete, record keys by creation (the page makes the upload BEFORE a ticket id exists, so identify it by the synthetic address AND this run's unique holdings hash) and, for the delete pass, list each exact key and its VersionId from list-object-versions in `irpt_anlreq_commentary_e2e7c/residue_7c.json` (bucket, key, version_id, size) and file the row. THE RECEIPT: write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7c/A_E2E7C.txt with run 7b's eighteen lines (each answered or `NOT-RUN <the hop where the run stopped>`), then the line `R3 pdf=<size> sha256=<12 hex> pages=<n> names_synthetic=<yes|no>` or `R3 NOT-RUN R`, then the closing line `RUN-DONE PASS` or `RUN-DONE STOP at <hop> code=<code>`.
  </context>

  <the_act>
    GO only on my message (it names the status grant's closed receipt and the DT or 7b PROD sha). Start at run 7b's step 1 (with the ledger irpt-commentary-e2e-7c-20261020, legs A mint, B browser, P poll, R route read, D delete; commit it; the open-deploys denominator as there) and go on only while each step reads green. A red hop is a STOP. Report ONCE to 2.0.0_SA_COO~Y2 (cc 1.0.0_SA_CTO~DELL2) with the receipt path, the closing line, and the path of the saved PDF if there is one.
  </the_act>

  <bounds>
    One request, one press, no Keep, no second filing after a red hop. No Terraform, IAM or code change. No ticket other than this run's own synthetic one is touched, and Andrew's ticket TCK-20261017-5af976ff is not. Runs 7 and 7b leftover objects stay. The synthetic user and everything this run created are deleted after the last read, except what the principal cannot delete (recorded with VersionIds and filed as a row). The saved PDF is a deliverable file of this order only.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7c/IRPT_ANLREQ.TO-RUN-COMMENTARY-E2E-7C.staff-filing-and-the-report-opens-ib2.proof_of_spec.json`.
    <criterion id="E2E7C-AC1" cell_refs="AR-y-465">The record holds all nineteen lines, each answered or marked not run.<invocation>grep -c -E '^(R0|A|A2|L|B1|B2|B3|P1|P2|P3|P4|P5|P7|R|R2|R3|DLQ|D) |^RUN-DONE (PASS|STOP at )' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7c/A_E2E7C.txt</invocation><expect>^19$</expect></criterion>
    <criterion id="E2E7C-AC2" cell_refs="AR-y-465">The run is honest about its ending (a pass, or a stop at a named hop).<invocation>grep -c -E '^RUN-DONE (PASS|STOP at [A-Z0-9]+ code=[A-Z0-9_]+)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7c/A_E2E7C.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="E2E7C-AC3" cell_refs="AR-y-465">The ledger irpt-commentary-e2e-7c-20261020 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-commentary-e2e-7c-20261020_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 CloudOps seat under ADDENDUM 9 as the CTO's msgs 11459 and 11475 carry it (run 7c on run 7b's terms), not a worker cell; the cell AR-y-465 is the issuer's, as for TO-RUN-COMMENTARY-E2E-7B.
