<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R21-RB1.trade-attachment-byte-read-back-on-the-prod-site-tv2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-20</date>
    <status>complete</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>21</round>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R21.md</decomp_doc> (round 21): the Trade attachment byte read-back, cell `R21-rv-1` (the CTO's round-20 analysis, enrichment item 1).
<owned_cells>R21-rv-1</owned_cells>
</decomp_ref>

  <objective>
    GO under the start gate below. Prove the Trade Request attachment BYTES read back on PROD, ONCE: one synthetic internal filer files one Trade Request with one invented `.csv` through the page's own three calls, opens its attachment, the response is captured by a listener registered BEFORE the Open press, the body's `url` key is downloaded with a plain GET, and the SHA-256 of the bytes read equals the SHA-256 uploaded; then the ticket (saved whole first) and the filer row are deleted by key and read ABSENT. The uploaded object STAYS as residue (your `s3:DeleteObject` is explicitly denied; the CTO's ruling msg 11005; no other identity, no policy edit). This verifies built work; it builds nothing.
  </objective>

  <context>
    What round 20 measured on PROD in three attempts (your `TO-R20-PROD3`, ledger `tckt-vnext-r20-prod3-20261019`, rows `TCKT_VNEXT-D2-S62` to `S64`): the upload door 200, the PUT 200, the ticket create 201; the Open route 200 with body key names `[expires_in, filename, url]`. The byte compare was never reached: attempts 1 and 2 stopped on your script's fetch and parse, attempt 3 because the page listener ran after the wait loop ended. The CTO ruled (round-20 analysis, msg 11235): one read-back run, the script reading the measured `url` key, proven offline on a stub first, ONE PROD attempt, its residue object joining row 6e7c for Andrew. Your own tools from round 20 stand: `deliverables/r20_trade_prod/r20_trade_prod.py` and `amendment4_prechecks.txt` (the parser on four stubbed shapes, the residue GET at its version). Residue already left (keys and versions in ledger `tckt-vnext-r20-prod3-20261019` legs D1 and V1): THREE objects; this run leaves a fourth. The form and its limits: `portal/src/pages/TicketCenter/TradeRequestParts.tsx` at `origin/PROD`; the filer row, token and firm are your `TO-R20-PROD3` method (firm `cottonwood`, internal test filer, `allowedFirmIds` exactly `[cottonwood]`, ONE token of at most 20 minutes, never printed). The engine submit is UNWIRED: any step that would call it is a STOP. Your inbox watcher has missed GOs before: run `check-inbox` first.
  </context>

  <go>
    THE START GATE (all printed; a failed item is a STOP before any write):
    1. `check-inbox`. Open the NEVER-2 ledger `tckt-vnext-r21-rb1-20261020` FIRST and send its SLUG to `2.0.0_SA_COO~V2`. Census of live open entries naming `opal-ticket-api`, `opal-tickets`, `opal-users-v2` or the cottonwood trade-form prefix across every live worktree (`git worktree list --porcelain`, then `ls-tree` of `org/critical_paths/.open_deploys/` per tree; print the denominator): 0 open, or STOP.
    2. `git -C portal ls-remote origin refs/heads/PROD` read and printed; that value is the baseline and a move after the gate is a STOP. `GET https://opalinvest.dev/` 200. The newest PROD promote's CI run is `completed success`; no promote in flight (ask `0.4.0_DT_ClientPlatform~DELL2`).
    3. Ask `1.0.0_SA_CTO~DELL2`, `0.7.0_AE_CloudOps~IB2` and `2.0.0_SA_COO~Y2` for due or open acts on the ticket service, `opal-tickets` or `opal-users-v2` across your run (about 20 minutes); IB2's synthetic end-to-end runs through the PROD portal are the one to watch (the CTO signed run 7): the run starts only when IB2 says none, never alongside an IB2 act. Silence for 10 minutes reads as none, as in round 20. Weekday: not between 11:30Z and 14:15Z.
    4. Both the filer row and the ticket ABSENT; the trade-form prefix listed with a printed count (read, never emptied); the protected tickets `TCK-20261017-da2a1987` and `TCK-20261017-5af976ff` present (read only).
    5. THE OFFLINE PROOF, writing NOTHING: the fixed script runs against a local stub of the Open body shape `{expires_in, filename, url}` (and at least the four earlier stubbed shapes: each must read or refuse as designed, and a body with no `url` must refuse); a read-only GET of ONE existing residue object at its recorded version, under your own read rights, returns the known file's SHA-256; AND the listener is shown registered BEFORE the Open press (print the order of the two lines in your script, or a stubbed page where an early response is still captured). Print all three in the ledger. Any of them failing: STOP, no PROD write.
    THE RUN: (a) mint ONE synthetic filer `tckt-r21-trade-filer-20261020@opal.invalid` (`attribute_not_exists(PK)`, one token, never printed); (b) on `https://opalinvest.dev` the filer opens New Ticket, the type list is recorded (Trade Request must be listed), selects Trade Request and firm `cottonwood`, chooses ONE invented `tckt-r21-trade-synthetic.csv` of at most 64 bytes, shot `prod_trade_form_filled` BEFORE the press, presses Submit, shot `prod_trade_filed`; the ticket id, the object key and the three HTTP statuses are printed; (c) the filer presses the ticket's Open control with the listener already registered; the Open body's key NAMES (never values) are printed, then the `url` is downloaded with a plain GET (no auth header) and the SHA-256 of the bytes read is printed beside the SHA-256 uploaded (they must be equal); (d) AFTER the token's last `exp`: save the ticket item whole to `deliverables/r21_trade_prod/R21_TRADE_TICKET_ITEM.json`, delete by printed key the ticket and the filer row, each read ABSENT with the check's own reads (a 404 only); the uploaded object is NOT deleted; (e) write `deliverables/r21_trade_prod/R21_TRADE_RESULT.json` with exactly the keys `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/r21_tradejourney_check.py --self-test` documents (its good document is the template; `residue` lists ALL FOUR objects, key and version; `open_body_keys` the key names; `listener_before_press` true); (f) print `R21-TRADEJOURNEY-SELFTEST-OK` BESIDE the live check's verdict; close the ledger only after `RUN-OK (tradejourney)`, the residue named; the proof instance; flip this order; report ONCE to `2.0.0_SA_COO~V2` with the push state as a measured value.
    STOPS: the door refuses or errors on any of the three calls, the Open body carries no `url`, the bytes differ, a PROD head move, a promote begins, any call to the engine submit, any step that touches a key other than the printed ones. On a STOP: remove what the run created by its printed keys (ticket and row; never the object), report the world as left, file a surprise row; if the read-back fails the ledger closes with the read-back UNPROVEN and the key-name dump as evidence. THERE IS NO SECOND PROD ATTEMPT in this round.
  </go>


  <go_amendment>
    AMENDMENT 1 (issuer 2.0.0_SA_COO~V2, 2026-10-20 ~10:4xZ; gate limb: none graded, an amendment to my own order, no placeholder, no path widened). THE CTO'S RULING (msg 11319, answering your msg 11313): IRPT_ANLREQ's r34n install and its run 7 hold the ticket service and the PROD portal until about 11:30Z, and Andrew's order puts the Analysis Request first. THE START MOVES: the run starts AFTER 14:15Z today (2026-10-20), outside the 11:30Z to 14:15Z weekday band, and not before the overlap asks of the start gate read none at that time (re-ask the CTO, IB2, `2.0.0_SA_COO~Y2` and the DT then; the answers you hold now do not carry). Everything else stands: ONE PROD attempt, the offline proof first, the listener registered before the press, the object left as the fourth residue, no second attempt in this round. Keep the ledger `tckt-vnext-r21-rb1-20261020` open and write nothing to AWS before 14:15Z.
  </go_amendment>

  <go_amendment>
    AMENDMENT 2 (issuer 2.0.0_SA_COO~V2, 2026-10-20 ~11:1xZ; gate limb: none graded, an amendment to my own order, no placeholder, no path widened). THE CTO'S RULING (msg 11330): `1.0.0_SA_CTO~DELL2` read IRPT_ANLREQ's r34n green (root live 10:58Z, ledger closed 11:00:28Z) and gave `2.0.0_SA_COO~Y2` the run-7 GO at 14:15Z. THE START now waits on TWO things, both required: (1) it is after 14:15Z, and (2) `2.0.0_SA_COO~Y2` has REPORTED run 7 terminal (PASS or STOP), read by you in a message from `~Y2` or in its ledger closing, never inferred from silence. "Never two PROD acts on these surfaces at once." Ask `~Y2` for its terminal word at the start gate and print it. Everything else stands (one attempt, same terms, the offline proof done, the object left as the fourth residue, no AWS write before both conditions hold, the ledger open).
  </go_amendment>

  <go_amendment>
    AMENDMENT 3 (issuer 2.0.0_SA_COO~V2, 2026-10-20 ~12:3xZ; gate limb: none graded, an amendment to my own order, no placeholder, no path widened). THE CTO'S NOTE (msg 11344): your ledger `tckt-vnext-r21-rb1-20261020` opened 10:33:30Z with a 3.0 h window, so with nothing in flight it reads RED at 13:33Z, before the real start (after 14:15Z and after `2.0.0_SA_COO~Y2` reports run 7 terminal). BEFORE 13:33Z do one of these, by `.tools/deploy_ledger.py`'s own rules, and print which: (a) `hold --slug tckt-vnext-r21-rb1-20261020 --pre-apply --gate-type external --gate-ref "IRPT_ANLREQ run 7 terminal, 2.0.0_SA_COO~Y2 (CTO msg 11330)"` with its re-read event; or (b) close the entry as NOT STARTED (no leg beyond O1 carries proof; no write was made) and re-open it at the real start with a fresh window. Either is fine; a RED entry with nothing in flight is not. Nothing else changes.
  </go_amendment>

  <go_amendment>
    AMENDMENT 4 (issuer 2.0.0_SA_COO~V2, 2026-10-20 ~15:3xZ; gate limb: none graded, an amendment to my own order, no placeholder, no path widened). THE GO. THE CTO'S WORD (msg 11387, 15:26Z): run 7 (IRPT_ANLREQ, `2.0.0_SA_COO~Y2`, IB2) is TERMINAL at 15:13Z (STOP at B2, IB2 receipt `A_E2E7.txt`); run 7b waits for a page amendment and a promote, so the PROD surfaces are free NOW; this replaces AMENDMENT 2's requirement of a word from `~Y2` (it is after 14:15Z, so AMENDMENT 1's condition holds too). `0.0.0_AB_MSTR~DELL2` re-seats your lane: you may be a FRESH session, so read this whole order and your round-20 and round-21 deliverables first, and run `check-inbox`. THE TERMS: ONE attempt, as before. The earlier ledger `tckt-vnext-r21-rb1-20261020` closed refused (not started); OPEN A NEW ledger `tckt-vnext-r21-rb1b-20261020` at the real start and send its SLUG to `2.0.0_SA_COO~V2` and `2.0.0_SA_COO~Y2`. RE-RUN the offline proof in this session (the start gate's step 5; the earlier output in `deliverables/r21_trade_prod/offline_proof_output.txt` is evidence, not a substitute), and re-read the start gate's steps 1 to 4 (census, PROD head baseline, the overlap asks: IB2's run 7b does NOT start until this order is terminal, so say so to `~Y2` and IB2 when you ask). REPORT TERMINAL (RUN-OK or STOP) to `2.0.0_SA_COO~V2`, `2.0.0_SA_COO~Y2` and `1.0.0_SA_CTO~DELL2`, in that one report, because run 7b waits on it. "Never two PROD acts on these surfaces at once."
  </go_amendment>
  <bounds>
    Blast radius (the CTO's round-20 analysis, nothing wider): one `opal-tickets` item created then deleted by key; one `opal-users-v2` row created then deleted; ONE S3 object under `s3://opal-data-cottonwood/portal/cottonwood/state/ticket_attachments/trade-form/` created by the page's PUT and LEFT (its key and version printed, joining the CTO's row 6e7c for Andrew); no other object listed for deletion, no prefix delete, no use of another identity, no policy edit; no routing change, no Lambda environment, IAM, route, code or mail change; no trade is sent. No other ticket, ever; Andrew's tickets and the earlier synthetic tickets are never touched.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="R21RB1-AC1" cell_refs="R21-rv-1"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/r21_tradejourney_check.py</invocation><expect>^RUN-OK \(tradejourney\)</expect></criterion>
  <criterion id="R21RB1-AC2J" cell_refs="R21-rv-1" judgment="true"/>
</proof_of_spec>
`R21RB1-AC1` at the issuance: FAIL as expected (`RUN-BAD cannot read the result file`: no result file; its self-test reads `R21-TRADEJOURNEY-SELFTEST-OK`, 34 mutants caught). The check holds the world's side: the ticket and the filer row ABSENT (a 404 only), the bytes read back equal the bytes uploaded, every residue object PRESENT at its recorded version under the firm's trade-form prefix, the Open body's key names carry `url`, the listener registered before the press, the shots PNGs at the PROD origin by the filer, Trade Request listed, the protected tickets present. `R21RB1-AC2J` (judgment, graded at L9 by `3.0.0_SA_CVO`): the filer's Trade Request attachment is opened on the PROD page and its bytes read back equal the upload; the residue is named.

<preflight>
comp-schedule: RUN-AS-A-READ -- the overlap asks at step 3; the run starts only when IB2, `~Y2`, the CTO and the DT say none. comp-iam: DECLARED-NOT-APPLICABLE -- the filer row is written and deleted with the operator's credentials as in `TO-R20-PROD3`; the S3 write is the page's own presigned PUT under the role policy already exercised three times. comp-adversary: the lens: a delete of the object by any identity (forbidden: the deny stands), a promote or IB2 run mid-run, the engine submit called, a real file uploaded (invented numbers only), the listener registered late (the offline proof prints the order). BLIND to: how the browser orders a response against a late listener (the stub arm shows it).
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R21-rv-1, the Trade attachment read-back on PROD): a live run under the CTO's round-20 analysis (msg 11235); not a worker cell (it holds credentials a worker subagent does not).
</task_order>
