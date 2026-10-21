<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-RUN-COMMENTARY-E2E-7N.overview-with-breit-and-zqxwvk-kept-the-swap-leg-on-r34t-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-21</date>
    <status>complete</status><!-- flipped by issuer 2.0.0_SA_COO~Y2 2026-10-21 (round hygiene, CTO msg ~15:10Z): every criterion invocation re-run by the issuer and matched; the proof instance reads VALID rc 0 -->
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>43</round>
<workstream>ZZ155</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc>
<owned_cells>AR-y-496</owned_cells>
<decomp_context>Round 43, cell AR-y-496: run 7N, ONE Overview filing (no comparables) that carries TWO kept unknown tickers, BREIT (a real, non-traded REIT the estate does not register: it exercises the C-SWAP model leg) and ZQXWVK (a nonsense ticker the model must NOT classify: it stays NOT_ANALYSED), on the r34t resident, alone on IB2, after G2's run 7M (CTO msg 11988): reads the swap leg, the new left-out line (CTO msg 11980) and the page-21 Risk Info tables from one saved Overview.</decomp_context>
</decomp_ref>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is run 5B's and run 7f's: one synthetic actor and advisor, one upload, one ticket, one request, one job row and their artifacts, every created key recorded at creation and deleted after the last read where the principal can; no Terraform, no IAM change, no code change, no mail.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE.
comp-iam: DECLARED-NOT-APPLICABLE -- the grants stand; this order adds none.
comp-adversary: RUN -- by reading run 5B's order and driver (e2e5b_run.py), run 7f's order and receipt and G2's msg 11972 against this order; the lens: a second unknown row beyond ZQXWVK (the holdings carry exactly one), the Keep sent for any finding but TICKER_NOT_FOUND of ZQXWVK, a retry after a red hop, a token, password, URL or signature written into any file or message (forbidden), a saved PDF that is committed, pasted or read for its text beyond one literal count, the r34t root not the live one, the 7N request left in the queue (read the main queue and the dead-letter depth), Andrew's tickets touched. NOT seen (blind): what the swap pass does with the kept row on r34t (the run reads it; the answer may be a clean refusal with a reason); denominator: one request.
</preflight>

  <objective>
    Run 7N is RUN 5B's mechanics (API driver `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e5b/e2e5b_run.py`, order `IRPT_ANLREQ.TO-RUN-COMMENTARY-E2E-5B.keep-repost-no-second-unknown-row-ib2.md` in this folder) with run 7f's Overview route and the save for Andrew (order `IRPT_ANLREQ.TO-RUN-COMMENTARY-E2E-7F.overview-filing-on-the-r34p-resident-for-andrew-ib2.md`, receipt `irpt_anlreq_commentary_e2e7f/A_E2E7F.txt`), on the r34t resident, as the REPLACEMENTS below: ONE synthetic request whose holdings carry the unknown ticker ZQXWVK, kept through the door's Keep re-post (the browser instrument never presses Keep), submitted as an OVERVIEW with no comparables, stopping at the first red hop. THIS ORDER STARTS ONLY ON MY GO MESSAGE. Read run 5B's order and driver and run 7f's order in full first: their steps, ledger legs, R0 gates and receipt apply unchanged except where the REPLACEMENTS say.
  </objective>

  <context>
    WHY: run 7L (S220 closed, row S256) showed a kept nonsense ticker stays NOT_ANALYSED. r34t ships the C-SWAP model leg (AR-y-492/493/494: kimi-k3 classification bound to the pool vocabulary, a bounded proposals call, the 0.80 flag); this run is its first live read, with a REAL unregistered name (BREIT), plus ZQXWVK as the negative control, in ONE Overview whose saved PDF G2 reads for the new left-out line (CTO msg 11980) and the page-21 Risk Info tables. The resident is r34t (IB2's receipt irpt_anlreq_r34t/A_AFTER_R34S.txt, V2S OK).
    THE REPLACEMENTS. (R0) every run 5B and 7f R0 read stands, plus: the resident root equals the root in IB2's r34t receipt and its ledger is CLOSED with V2S OK; `irpt-status` CodeSha256 is read and printed (7f's value B4R0dZqBRhclmQLOiBHp3Ft/wNbMomNZhUflCCRfEyE= unless a later release moved it: if it moved, name which closed ledger moved it, else STOP); outside 11:30Z-14:15Z on a weekday and the gateway window; no other IB2 act. A red R0 mints NOTHING.
    (A) THE HOLDINGS BYTES, ASCII, LF, a trailing newline: `Ticker,Dollars,Acct Market Value` / `SPY,127,26000000` / `AGG,223,32000000` / `TIMXX,61,5000000` / `BREIT,45,5000000` / `ZQXWVK,50,5000000` (five data rows; BREIT and ZQXWVK are the ONLY unknown rows). Its sha256 must be `e012d9ea3853fef28a565b5b1fb0572dc69d1c8649d0350911e584c6fee9755c` and must differ from every earlier run's holdings hash recorded in the state files of runs 4 to 7M (print that you compared; a match is a STOP before anything is minted).
    (A2, L, U, T) as run 5B/7L: one synthetic advisor, login, the upload RE-POSTED while RESOLVING with 5B's backoff, and the KEEP RE-POST as the driver does it, adapted to TWO unknown rows: the door answers NEEDS_CORRECTION with a TICKER_NOT_FOUND finding for BREIT and for ZQXWVK (and nothing else; any other finding code, or a finding for any other symbol, is a STOP before any Keep); the re-post carries one correction {finding_code TICKER_NOT_FOUND, from_value X, to_value X} for EACH of the two. If the door answers NEEDS_CORRECTION again with a TICKER_NOT_FOUND finding for only one of the two, send ONE more Keep re-post for that one; at most TWO Keep re-posts in all; then the ticket. U ALSO PRINTS THE REASON THE FILER IS SHOWN for each of the two: the finding `code` and `message` as the NEEDS_CORRECTION answer carried them, and whether the door offered a `suggestion` for BREIT (the symbol only, a public ticker).
    (S) SUBMIT as an OVERVIEW with NO comparables: `POST /api/scoped/investor-reporting/analysis` with the body exactly as the portal's analysisBody sends it for an Overview report type with no comparison keys and no commentary request that the page does not send (read portal/src/pages/TicketCenter/analysisRequest.ts and run 7f's captured calls; not variant multicomp, no comparison_keys). One submit; no second after a red hop.
    (P) poll as 5B (20 s step, 30 minutes): P1 the job row; P4 the packager outcome line(s) from the resident journal; P6 THE KEPT ROWS (read-only; closed values only, no amount): the request's frozen composition rows for BREIT and ZQXWVK (`resolution` and `method`), and the swap pass's record for each from the request's retained run document: `status` (REPLACED / NO_REPLACEMENT / NOT_ANALYSED), `proxy` ticker (a public ticker) when REPLACED, `method`, `confidence`, `low_confidence`, `classified_by`, `sources`, `candidates_priced`, `dropped_reasons` (the counts by reason), `pool_stale`. Expected, not required: BREIT REPLACED by a class-matched, Yahoo-priced security with `classified_by` MODEL (and `low_confidence` true or false as the model said); ZQXWVK NOT_ANALYSED. Any other outcome is the ANSWER: write it, do not retry. A job that never reaches READY with a read reason is an ANSWER too (`RUN-DONE ANSWER`); go to R5 as `NOT-RUN`, then D.
    (R) THE OVERVIEW ROUTE, only when READY: `GET .../analysis/requests/{REQ}/pdf`; PDF as in 7f; (R3) save it UNCHANGED to `C:/dev/andrew_samples/Opal_Overview_sample_post_r34t.pdf` (a NEW name: do not overwrite the r34p sample), size, sha256 (12 hex) and page count only; (R5) THE PLACEHOLDER READ: with `pypdf` if importable (else write `R5 NOT-READ pypdf absent`), count the pages of the saved PDF whose extracted text contains the literal string `{portfolio_name}`; print ONLY that count and the page total; no other text from the PDF is read, printed or stored.
    (DLQ) the main queue and the dead-letter depth BEFORE and AFTER (irpt-generation and irpt-generation-dlq): the request's own message, if it is still in flight or dead-lettered, is NOT touched or deleted by you; name it by the REQ id and tell me and 2.0.0_SA_COO~G2: G2 issues the delete.
    (D) delete only keys recorded at creation; for this run's residue your principal cannot delete, list each exact key and VersionId in `irpt_anlreq_commentary_e2e7n/residue_7n.json` (bucket, key, version_id, size) and file the row.
    THE RECEIPT: write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7n/A_E2E7N.txt with EXACTLY one line per tag, each answered or `NOT-RUN <the hop where the run stopped>`: `R0 ...`, `A mint ...`, `A2 advisor ...`, `L login ...`, `U upload keep=<sent n=1|sent n=2|not-needed> reason=<code>:<message> for each of the two rows`, `T ticket ...`, `S submit ...`, `P1 job ...`, `P4 packager ...`, `P6 kept-rows BREIT=<status proxy classified_by low_confidence> ZQXWVK=<status>`, `R overview-route ...`, `R3 pdf=<size> sha256=<12 hex> pages=<n> saved=outside-repo` or `R3 NOT-RUN <why>`, `R5 placeholder pages=<n> of <total>` or `R5 NOT-RUN <why>` or `R5 NOT-READ pypdf absent`, `DLQ ...`, `D ...`, then the closing line `RUN-DONE PASS` (READY and R and R3 passed) or `RUN-DONE ANSWER <reason code>` (the job did not reach READY and the reason is read: this closes S220) or `RUN-DONE STOP at <hop> code=<code>` (a red hop that is not that answer).
  </context>

  <the_act>
    GO only on my message (it names the trunk commit and the r34t root, says G2's run 7M is terminal and nothing else is running on IB2, and is not sent before r34t is installed, which waits for 14:15Z by the CTO's msg 11991). Start at run 5B's step 1 (ledger irpt-commentary-e2e-7n-20261021, legs A mint, U upload and keep (two Keeps), S submit, P poll, R route read, D delete; commit it; the open-deploys denominator as there) and go on only while each step reads green. Report ONCE to 2.0.0_SA_COO~Y2 and 2.0.0_SA_COO~G2 (cc 1.0.0_SA_CTO~DELL2) with the receipt path, the closing line, the U reasons, the P6 answers for both rows, the R3 and R5 lines, and the path of the saved Overview PDF if there is one.
  </the_act>

  <bounds>
    One synthetic actor, one advisor, one upload (re-posted while RESOLVING, plus the one Keep re-post), one ticket, one request, no second filing after a red hop. No Terraform, IAM, queue, route, secret or code change. Delete only keys recorded at creation. Andrew's tickets TCK-20261017-5af976ff and TCK-20261020-b1d61f80 and every client object are not touched. No token, password, URL, signature, bearer or non-synthetic email in any file or message. The saved PDF lives outside the repository and is never committed or quoted beyond the one literal count of R5.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7n/IRPT_ANLREQ.TO-RUN-COMMENTARY-E2E-7N.overview-with-breit-and-zqxwvk-kept-the-swap-leg-on-r34t-ib2.proof_of_spec.json`.
    <criterion id="E2E7N-AC1" cell_refs="AR-y-496">The record holds all fifteen tagged lines, each answered or marked not run.<invocation>grep -c -E '^(R0|A|A2|L|U|T|S|P1|P4|P6|R|R3|R5|DLQ|D) ' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7n/A_E2E7N.txt</invocation><expect>^15$</expect></criterion>
    <criterion id="E2E7N-AC2" cell_refs="AR-y-496">The run is honest about its ending (a pass, a read answer with a reason, or a stop at a named hop).<invocation>grep -c -E '^RUN-DONE (PASS|ANSWER [A-Z0-9_]+|STOP at [A-Z0-9]+ code=[A-Z0-9_]+)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7n/A_E2E7N.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="E2E7N-AC3" cell_refs="AR-y-496">The ledger irpt-commentary-e2e-7n-20261021 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/20261021T1500Z_irpt-commentary-e2e-7n-20261021_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 CloudOps seat under ADDENDUM 9 as the CTO's msgs 11508, 11510, 11512, 11521 and 11970 carry it (run 7N on run 5B's and run 7f's terms), not a worker cell; the cell AR-y-496 is the issuer's, as for TO-RUN-COMMENTARY-E2E-7F.
