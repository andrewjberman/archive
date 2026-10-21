<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-RUN-FWD10-MULTICOMP-7I.multicomp-filing-on-the-r34q-resident-ib2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-21</date>
    <status>not_met</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>60</round>
<workstream>~GREL5</workstream>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is run 7e's: one synthetic request filed through the PROD portal page by a minted synthetic staff user, every created key recorded at creation and deleted after the last read where the principal can; no Terraform, no IAM change, no code change. The two differences from 7e: the request is a MULTI-COMP (two Opal models ticked on the form) and its holdings are four public ETF tickers (the household stays synthetic, no client data), so the resident reads the two model objects of opal-data-portal-v2 (grant live) and prices the holdings through the estate, yfinance and ycharts tiers under the same lease and budget (a few price reads).
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE.
comp-iam: DECLARED-NOT-APPLICABLE -- the grants stand; this order adds none.
comp-adversary: RUN -- by reading run 7e's order and receipt, the r34o receipt and the AR-g-179 instrument against this order; the lens: a filing that is an Overview because no comparable was ticked (the closed line `B2 request variant=multicomp comparison_keys=2` must read as written BEFORE you accept the press; it prints after the press, so read it from the instrument's output and STOP the run at B2 if it reads otherwise, no second filing), a holdings file other than fwd10_holdings_7i.csv (its sha256 is in the context), a saved PDF that is committed or pasted (it is saved OUTSIDE the repository, only size, sha256 and page count are written down), the PDF read as proof that the numbers are right (the issuer recomputes them), the run overlapping another IB2 act, the resident role or another run on the same keys. NOT seen (blind): what the comparison section says; denominator: one request.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R60_G.md</decomp_doc> round 60, workstream ~GREL5: the one real run of FWD-10 (the issuer's step after the r34q release of cell AR-g-181, with the instrument of cell AR-g-179).
<owned_cells>AR-g-181</owned_cells>
</decomp_ref>

  <objective>
    Run 7I is RUN 7H (receipt irpt_anlreq_fwd10_multicomp_7h/A_E2E7H.txt: RUN-DONE STOP at P1 code=NOT_READY, row S245: the r34p resident refused the Multi-Comp composition at admission) re-run on the r34q resident with a NEW HOLDINGS FILE, itself RUN 7e (order `IRPT_ANLREQ.TO-RUN-COMMENTARY-E2E-7E.overview-filing-on-the-r34o-resident-for-andrew-ib2.md`, in this folder; receipt `irpt_anlreq_commentary_e2e7e/A_E2E7E.txt`) ON THE SAME TERMS, with the REPLACEMENTS below: one synthetic MULTI-COMP request filed through the PROD portal page by an unseeded synthetic staff user whose form Advisor is left AS THE PAGE PRE-FILLS IT, with two Opal models ticked, going on to read the Overview-style report PDF route and saving the PDF for the issuer's page-by-page read of FWD-10's comparison section, stopping at the first red hop. THIS ORDER STARTS ONLY ON MY GO MESSAGE. Read run 7e's order and receipt in full first: its steps, ledger legs, R0 gates and receipt apply unchanged except where the REPLACEMENTS say.
  </objective>

  <context>
    WHY: the resident (root 0485393f3a-r34q, V2S OK; r34q fixes the admission refusal of run 7H, row S245, and wires the audit through the tickets_table binding) carries FWD-10's comparison section. The CTO asked for one synthetic Multi-Comp filing after run 7e (msg 11622). The live comparison catalogue holds the five Opal models only (no ETF entry), so the comparables are two Opal models; the ETF comparable is proved offline.
    THE REPLACEMENTS. (R0) every 7e R0 read stands EXCEPT the root: the resident root reads `0485393f3a-r34q` (r34q closed per your report, receipt irpt_anlreq_r34q/A_AFTER_R34Q.txt with its sixteen lines and ledger CLOSED; r34p is no longer running), plus the irpt-status CodeSha256 and PROD tip as in 7e, plus: nothing else is open on the resident role or the stack, and `irpt-generation` holds 0 visible and 0 in flight. A red R0 mints NOTHING.
    (A, A2, L, P1-P5, P7, R2) as 7e. (B) THE INSTRUMENT is the copy under `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~335/run7_browser_leg.mjs` (cell AR-g-179, merged to this branch; read its PAGE_NOTES.md "Run 7h changes" first) with `--holdings org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/fwd10_holdings_7i.csv` (four public ETF tickers in the page's accepted format `Ticker,Dollars,Acct Market Value`: SPY 420, AGG 280, IWM 150, EFA 150; its sha256 starts 3125b93613e2 and differs from run 7H's file (1c20745eff0e) so that no leftover of 7H can answer for it; THE REASON FOR THIS RE-RUN: run 7H reached the resident and was refused at admission (S245), fixed in r34q. If the page refuses THIS file, read the page's own review findings (counts and words, not file content) BEFORE the delete pass and write them in the receipt) and `--comparables "Opal Short-Term,Opal Long-Term"`; household stays the synthetic one; ONE press, no Keep, no second filing. The instrument prints `B2 comparables ticked=2` and `B2 request variant=multicomp comparison_keys=2`; any other value is a STOP at B2 (write the row; the one request already filed, if any, is read to the end of what it can answer and then deleted as in D).
    (R) the report PDF route `GET /api/scoped/investor-reporting/analysis/requests/{REQ}/pdf` as run 7e: the closed code, a plain GET of the link, first four bytes `%PDF`, size, sha256, page count; never print the URL. The resident may take longer than for an Overview (it reads two S3 objects and prices four holdings): poll as 7e does, up to its budget, then STOP at P with the closed state (no retry).
    (R3) THE MULTI-COMP SAMPLE FOR THE ISSUER'S READ: save the PDF UNCHANGED to `C:/dev/andrew_samples/Opal_MultiComp_sample_FWD10.pdf` (outside the repository: do NOT commit it or paste its text), and write only its size, sha256 (12 hex) and page count into the receipt and the message. Also record the filing's own facts for the issuer's recomputation, as closed lines in the receipt (no content): the request id, the ticket id, the filing time, the holdings sha256, and the sections route's counts (`GET .../analysis/requests/{REQ}/sections`: the number of sections and, per status, VALUE / NOT_AVAILABLE counts, and whether any section id begins `opal.compare.`: yes/no).
    (R4) not read in this run (no commentary asked). (U) THE CTO'S TWO NAMED OUTCOMES (msg 11854): after the PDF read, report by NAME the packager outcome (as run 7F reported it: ATTACHED, or the closed refusal code) and the audit outcome (the closed word the resident records for the audit on this request: the written marker, or AUDIT_REFUSED:<code>, or AUDIT_PORTS_UNWIRED). The CTO measured that the runner role's GetItem on opal-tickets reads implicitDeny, so on r34q the audit is expected to be wired but refused and the attach stands; read it, do not assume it. Words and codes only, never a record body. (D) as 7e; residue list in `irpt_anlreq_fwd10_multicomp_7i/residue_7i.json`.
    THE RECEIPT: write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_fwd10_multicomp_7i/A_E2E7I.txt with run 7e's lines up to R (each answered or `NOT-RUN <the hop where the run stopped>`), then `B2 comparables ticked=<n> variant=<v> comparison_keys=<n>`, then `R3 pdf=<size> sha256=<12 hex> pages=<n> saved=outside-repo` or `R3 NOT-RUN R`, then `S sections=<n> value=<n> not_available=<n> compare_sections=<yes|no>`, then `F request=<REQ> ticket=<TCK> filed_at=<time> holdings_sha256=<12 hex>`, then `U packager=<word> audit=<word>`, then the closing line `RUN-DONE PASS` (R and R3 passed) or `RUN-DONE STOP at <hop> code=<code>`.
  </context>

  <the_act>
    GO only on my message (it names r34q's closing line and the instrument's merge commit f283bc1ae1c; run it outside 06:00Z-06:55Z and 11:30Z-14:15Z). Start at run 7e's step 1 (with the ledger irpt-fwd10-multicomp-7i-20261021, legs A mint, B browser, P poll, R route read, D delete; commit it; the open-deploys denominator as there) and go on only while each step reads green. A red hop is a STOP. Report ONCE to 2.0.0_SA_COO~G2 (cc 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2) with the receipt path, the closing line, and the path of the saved PDF if there is one.
  </the_act>

  <bounds>
    One request, one press, no Keep, no second filing after a red hop. No Terraform, IAM or code change. No ticket other than this run's own synthetic one is touched, and Andrew's tickets are not. Earlier runs' leftover objects stay. The synthetic user and everything this run created are deleted after the last read, except what the principal cannot delete (recorded with VersionIds and filed as a row). The saved PDF lives outside the repository and is never committed or quoted. Never alongside another IB2 act or another filing.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_fwd10_multicomp_7i/IRPT_ANLREQ.TO-RUN-FWD10-MULTICOMP-7I.multicomp-filing-on-the-r34q-resident-ib2.proof_of_spec.json`.
    <criterion id="F10-7I-AC1" cell_refs="AR-g-181">The run is honest about its ending (a pass, or a stop at a named hop).<invocation>grep -c -E '^RUN-DONE (PASS|STOP at [A-Z0-9]+ code=[A-Z0-9_]+)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_fwd10_multicomp_7i/A_E2E7I.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="F10-7I-AC2" cell_refs="AR-g-181">The filing was a Multi-Comp of two models and the saved sample is recorded.<invocation>grep -c -E '^(B2 comparables ticked=2 variant=multicomp comparison_keys=2|R3 pdf=[0-9]+ sha256=[0-9a-f]{12} pages=[0-9]+ saved=outside-repo)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_fwd10_multicomp_7i/A_E2E7I.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="F10-7I-AC3" cell_refs="AR-g-181">The ledger irpt-fwd10-multicomp-7i-20261021 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-fwd10-multicomp-7i-20261021_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a RUN order to a tier-2 CloudOps seat under ADDENDUM 9 as the CTO's msg 11622 carries it (run 7I on run 7e's terms), not a worker cell; the cell AR-g-181 is the issuer's, as for TO-RUN-COMMENTARY-E2E-7E.
