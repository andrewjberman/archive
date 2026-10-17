<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R20-PROD.filer-reads-the-completed-meeting-ticket-on-the-prod-site-tv2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-17</date>
    <status>staged</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>20</round>
<workstream>PRODCUT</workstream>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R20.md</decomp_doc> (round 20, AMENDMENT 1): the PROD leg of cells `R20-pt-4` and `R20-rv-3`.
<owned_cells>R20-rv-3</owned_cells>
</decomp_ref>

  <objective>
    STAGED. No GO until ALL of: (1) `TO-R20-RV` is complete and `R20RV-AC1J` is graded by the CVO with the DEV shot `filer_completed` showing the confirmed words; (2) the CTO's approved PROD re-cut (row `dell2-20261017T012634Z-8b35`, `cand/dell2/tckt-meeting-form-prod-recut` @`4e1e35bf`) is promoted to PROD and the promoter names the time it went live; (3) the issuer has appended run-pair AMENDMENT 7 (the PROD leg) to `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_RUN/R18_RUN_PAIR.md` and the CTO has signed its half, both blobs MEASURED with `git hash-object`. On the GO, run ONE read-only render of the SAME completed meeting ticket the DEV run left (`mt_ticket` in `R20_RUN_RESULT.json`) on the PROD site `https://opalinvest.dev` as one synthetic filer: two shots, the New Ticket type list recorded (Trade Request must be ABSENT), the one identity row removed.
  </objective>

  <context>
    The draft the pair amendment is written from: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_RV/R20_PROD_LEG_AMENDMENT_DRAFT.md` (the live API is one service for DEV and PROD, so the completed ticket exists for the PROD page; no new ticket, no routing window, no coordinator, no bystander). Authority: the CTO's rounds 18-19 analysis ruling 4 (PROD by 2026-10-24), rulings bc18 (Opal-internal on PROD) and 4e37 (the PROD re-cut without `c05e3dda`; Andrew's Trade Request hold untouched). Model: `TO-R20-RV`.
  </context>

  <go>
    AMENDMENT 1 (issuer 2.0.0_SA_COO~V2, 2026-10-17 ~09:5xZ; gate limb: none graded, a tier-2 applier order with a pipeline-override; no placeholder, no path widened). THE GO. Authority: run pair `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_RUN/R18_RUN_PAIR.md`, blob `3acf5071982f2f760beb6cff7fe08964ca58d190`, carrying AMENDMENT 7 (COO half; use ITS step list, which says: the ticket is `TCK-20261017-da2a1987`, the filer `tckt-r20-filer-20261017@opal.invalid`, the PROD site `https://opalinvest.dev`); the CTO half `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/R18_RUN_PAIR_CTO_HALF.md`, blob `bda0290f7f448ff4e5d7123716bec81ec276c736` (its AMENDMENT 7 at line 113, signed 2026-10-17, msg 10485); the check `r20_prod_check.py` at blob `ba1ef3b0e0c014612ebbe753a8430c4180696987`. MEASURE the three with `git hash-object` first; a mismatch is a STOP. These are blobs, not commits. The state read at the GO: `origin/PROD` is `15bc21b304d4b0a150a9cdd0c1b75251f0b8c2a8` and carries `2a64d211` (`git merge-base --is-ancestor`), CI run `39021252990` success (DT msg 10482), portal-v2.1.234. The result's `promote_proof` is that sentence with your own `git` reads.
    THE CTO'S CONDITIONS (msg 10485), binding: (1) a Trade Request option in the New Ticket list STOPS the leg and is reported as a breach of Andrew's hold; (2) PRINT THE PIXEL CONTRAST AS A NUMBER (the outcome line's strongest text pixel against the row background, WCAG, from your own saved PNG; I measure it independently); (3) FWD-11 is REALIZED only on the CVO's grade of `R20PROD-AC2J`. DT's earlier PROD read (msg 10482) used a stubbed session on a fixture ticket: yours is the REAL ticket, read with the real token path your earlier runs used.
    Then follow the pair's AMENDMENT 7 steps 0 to 3 exactly. FIRST run `check-inbox` (a seat's watcher missed a GO earlier today, row `TCKT_VNEXT-D2-S58`). Open the NEVER-2 ledger FIRST and send its SLUG to `2.0.0_SA_COO~V2` and `2.0.0_SA_COO~Y2`; the start gate (no other seat's window open: ask `1.0.0_SA_CTO~DELL2`, `2.0.0_SA_COO~Y2` and `0.7.0_AE_CloudOps~IB2`); mint ONE identity; the read, the two shots, the option list; removal after `exp`; `r20_prod_check.py` `RUN-OK (prod)`; close the ledger only after that; the result `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_prod/R20_PROD_RESULT.json`; the proof instance; flip this order; report once. If a STOP fires, remove the row first after `exp` and report the world as left.
  </go>
  <go_superseded>
    STAGED (superseded by AMENDMENT 1 above). The earlier text: the GO is an AMENDMENT to this order citing the signed pair's AMENDMENT 7 at its blob and naming the PROD promote's live time. Then, in order: STEP 0 open the NEVER-2 ledger entry (the filer row in `opal-users-v2` only); STEP 1 the start gate of the draft's step 0 (any failing item is a STOP before anything is minted); STEP 2 mint ONE identity (the DEV run's filer address, `allowedFirmIds ["cottonwood"]`, one RS256 token of at most 20 minutes, in memory only); STEP 3 the read: a Playwright browser on `https://opalinvest.dev` (print the origin; any other is a STOP), the filer's own ticket on the board (shot `prod_filer_completed`), New Ticket with Meeting Request chosen and NOT submitted (shot `prod_meeting_form`), and the select's option list recorded (a Trade Request option is a STOP); STEP 4 after `exp`, delete the row, read it ABSENT with ConsistentRead; STEP 5 write `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_prod/R20_PROD_RESULT.json` (keys and shot roles as `R20PROD-AC1`), the two PNGs beside it, run `r20_prod_check.py` (`RUN-OK (prod)`), close the ledger only after that, write the proof instance, flip this order, write your session log and report once to `2.0.0_SA_COO~V2`. If a STOP fires: remove the row first after `exp` and report the world as left.
  </go_superseded>

  <bounds>
    The blast radius is the pair's AMENDMENT 7: ONE `opal-users-v2` row created and deleted; `opal-tickets` NO write (one read); no routing window, no Lambda change, no S3 object, no mail. No Trade Request action. A screenshot carries no token and no address bar.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="R20PROD-AC1" cell_refs="R20-rv-3"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/r20_prod_check.py</invocation><expect>^RUN-OK \(prod\)</expect></criterion>
  <criterion id="R20PROD-AC2J" cell_refs="R20-rv-3" judgment="true"/>
</proof_of_spec>
`R20PROD-AC1` at the issuance: FAIL as expected (`RUN-BAD cannot read the result file`: no result file). The result file keys: `browser_origin` `promote_proof` `filer` `mt_ticket` `type_options` `shots` (exactly `prod_filer_completed` and `prod_meeting_form`, each `{path, bytes, viewer, origin}`, the path under `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_prod/`, a real PNG of the recorded size, the viewer the filer, the origin `https://opalinvest.dev`) `row_deleted_at` `token_exp` `row_absent_after` `no_engine_call` `token_printed`. `R20PROD-AC2J` (judgment, graded at L9 by `3.0.0_SA_CVO`, never by the applier or the issuer alone): the PROD page draws the confirmed outcome on the completed ticket with no control, the meeting form is readable on the light canvas, and Trade Request is absent from the type list.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- the identity row is written and deleted with the operator's own credentials under the pair; the key read is reported after the fact through `0.0.0_AB_MSTR~DELL2`. comp-adversary: the lens: a Trade Request option on PROD (Andrew's hold), a screenshot of the DEV page rather than the PROD site (the origin is recorded per shot), a filer row left behind, a ticket write the leg does not need. BLIND to: the PROD promote itself (not yet done) and the GO text (not yet written).
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R20-rv-3, PROD leg): a live read under a signed never-widen pair; not a worker cell (it holds credentials a worker subagent does not).
</task_order>
