<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R20-PROD2.synthetic-filer-files-and-coordinator-confirms-a-meeting-request-on-the-prod-site-tv2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-17</date>
    <status>staged</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>20</round>
<workstream>PRODFIX</workstream>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R20.md</decomp_doc> (round 20): the PROD journey of cell `R20-rv-3` (the CTO's msg 10499 after the CVO's `ADJUDICATION_v13`).
<owned_cells>R20-rv-3</owned_cells>
</decomp_ref>

  <objective>
    STAGED. No GO until the CTO has signed his half of run-pair AMENDMENT 8 and the issuer writes the GO, all blobs MEASURED with `git hash-object`, AND it is a WEEKDAY (Monday 2026-10-19 or later, on or before Friday 2026-10-23) OUTSIDE THE FIRE WINDOWS. On the GO, run the FWD-11 journey ONCE on the PROD site `https://opalinvest.dev`: a synthetic filer FILES one Meeting Request, a synthetic coordinator CONFIRMS it inside one routing window, the filer reads the confirmed line and its pixel contrast is printed as a number; then the synthetic ticket and both identity rows are removed by key and read ABSENT.
  </objective>

  <context>
    The procedure is run-pair AMENDMENT 8 (`org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_RUN/R18_RUN_PAIR.md`); the models are `TO-R20-RV` (the DEV journey, `RUN-OK (render)`) and `TO-R20-PROD` (the PROD read, `RUN-OK (prod)`). Why: the CVO graded the PROD read MET and FWD-11 NOT REALIZED on PROD (`ADJUDICATION_v13`): the filing and the confirm were never driven on the PROD page; the CTO ruled (msg 10499) to run them once, by 2026-10-23, outside the fire windows; "Andrew's word covers synthetic deletes". Andrew's tickets (`TCK-20261017-5af976ff`) and the earlier synthetic ticket (`TCK-20261017-da2a1987`) are NOT touched by any step. Your inbox watcher missed two GOs today (rows `TCKT_VNEXT-D2-S58` and `S60`): run `check-inbox` before you conclude there is no GO.
  </context>

  <go>
    AMENDMENT 1 (issuer 2.0.0_SA_COO~V2, 2026-10-19 ~16:39Z; gate limb: none graded, a tier-2 applier order with a pipeline-override; no placeholder, no path widened). THE GO. Authority: run pair `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_RUN/R18_RUN_PAIR.md`, blob `0b2978bfea1a870f14a6ba7ddf61e2c97de9c106`, carrying AMENDMENT 8 and AMENDMENT 9 (COO half; use their step list as AMENDMENT 9 revises it); the CTO half `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/R18_RUN_PAIR_CTO_HALF.md`, blob `e7a33cf976ccb396e4976c4177a826ef39d767c1` (its AMENDMENTS 8 and 9 SIGNED; AMENDMENT 9 at 41d46ae367, msg 10754); the check `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/r20_prodjourney_check_v2.py` at blob `9ff30a5d385320379c04a742eed6029ac854f8ff`. MEASURE the three with `git hash-object` first; a mismatch is a STOP. These are blobs, not commits. The state read at the GO: `origin/PROD` is `9107d48ae3d2b72882e4988473f6e19f2d9c71b5` (ls-remote read); confirm with your own git reads that it carries `2a64d211` AND the TO-DB-b-336 release (AMENDMENT 9 start gate item 1: TicketCenter.tsx no longer filters `trade_request`, `TradeFormOpen` imported), the promote's CI run a success.
    THE CTO'S CONDITIONS (msgs 10499, 10502 and 10754), binding: (1) a Trade Request option in the New Ticket list is RECORDED, not a STOP (Andrew lifted the hold 2026-10-19; AMENDMENT 9); no Trade Request ticket is filed or opened; (2) PRINT THE PIXEL CONTRAST AS A NUMBER from your own saved PNG (I measure it independently); (3) FWD-11 is REALIZED only on the CVO's grade of `R20PROD2-AC2J`; (4) the whole run, mint to removal, fits outside 11:30Z to 14:15Z; (5) the receipt PRINTS the check's self-test (`python .../r20_prodjourney_check_v2.py --self-test` reads `R20-PRODJOURNEY-SELFTEST-OK`: the Trade Request document reads GOOD, 21 of 21 other mutants caught) BESIDE the run's verdict.
    Then follow the pair's AMENDMENT 8 steps 0 to 5 exactly. FIRST run `check-inbox` (a seat's watcher missed two GOs, rows `TCKT_VNEXT-D2-S58` and `S60`). Open the NEVER-2 ledger FIRST and send its SLUG to `2.0.0_SA_COO~V2` and `2.0.0_SA_COO~Y2`; ask the CTO and IB2 for the day's fire windows and print the answer; the start gate; mint TWO identities; the routing window; the journey on `https://opalinvest.dev`; removal by key (ticket record saved first); `r20_prodjourney_check_v2.py` `RUN-OK (prodjourney)` (the v2 file, not the v1 named in AMENDMENT 8); close the ledger only after that; the result `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_prod2/R20_PROD2_RESULT.json`; the proof instance; flip this order; report once to `2.0.0_SA_COO~V2`. A PROD head that moves after the start gate is a STOP. If a STOP fires: close the routing window FIRST, remove the rows after `exp`, remove the ticket by key if it was created, report the world as left.
  </go>
  <go_superseded>
    STAGED (superseded by AMENDMENT 1 above). The earlier text:
    NOTE (issuer, 2026-10-17 ~10:4xZ, after the CTO's half msg 10502; gate limb: none graded, no placeholder, no path widened): the CTO NAMED THE FIRE BAND as the start gate's answer: on a weekday NO STEP runs between 11:30Z and 14:15Z (the 49 Financial reporting-gold fire 11:41Z; the holdings-performance and Cottonwood fires 12:15Z and 12:45Z; the filled-report fan-out band 12:05Z to 13:15Z; the directory refresh 13:30Z with its 13:40Z retry; the MDPF fire 13:30Z). RUN at 15:00Z or later, or before 11:00Z, on 2026-10-19 to 2026-10-23; the whole run (mint to removal, about 30 minutes with the token wait) must fit outside the band. IB2 confirms its own queue at the gate. The CTO's CTO-half blob at this note is `2aa0b32dbb6ccc84ae516eb9d942efdeb8885f3c`; the GO written on the day of the run names the blob measured THEN.
    STAGED. The GO is an AMENDMENT to this order citing the signed pair's AMENDMENT 8 at its blob (COO half and CTO half, both measured) and the check `r20_prodjourney_check.py` at its blob, written on the day of the run. Then, in order: the pair's AMENDMENT 8 steps 0 to 5 (open the ledger FIRST and send the slug to `2.0.0_SA_COO~V2` and `2.0.0_SA_COO~Y2`; ask the CTO and IB2 for the day's fire windows and print the answer; the start gate; mint TWO identities; the routing window; the journey on `https://opalinvest.dev`; the removal by key, the ticket record saved first; `r20_prodjourney_check.py` `RUN-OK (prodjourney)`; close the ledger only after that). If a STOP fires: close the routing window FIRST, remove the rows after `exp`, remove the ticket by key if it was created, report the world as left. Report once to `2.0.0_SA_COO~V2`.
  </go_superseded>

  <bounds>
    The blast radius is the pair's AMENDMENT 8: one `opal-tickets` item created then deleted by key; two `opal-users-v2` rows created and deleted; the Lambda `ROUTING_MATRIX` changed for the window then restored; no S3 object, IAM, code or route change; mail none. No Trade Request action. No other ticket, ever.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="R20PROD2-AC1" cell_refs="R20-rv-3"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/r20_prodjourney_check_v2.py</invocation><expect>^RUN-OK \(prodjourney\)</expect></criterion>
  <criterion id="R20PROD2-AC2J" cell_refs="R20-rv-3" judgment="true"/>
</proof_of_spec>
`R20PROD2-AC1` at the issuance: FAIL as expected (`RUN-BAD cannot read the result file`: no result file). The check holds the world's side: the synthetic ticket and both rows ABSENT, the routing restored, the two protected tickets present, the shots PNGs at the PROD origin by the right viewers, Trade Request listed or not (AMENDMENT 9), a printed contrast of at least 4.5. `R20PROD2-AC2J` (judgment, graded at L9 by `3.0.0_SA_CVO`, with the issuer's pixel measurement as evidence): the filer filed on the PROD page; the coordinator confirmed on it; the filer reads the confirmed line readable, no control.

<preflight>
comp-schedule: RUN-AS-A-READ -- the fire windows are asked of the CTO and IB2 at the start gate; the run starts only outside them. comp-iam: DECLARED-NOT-APPLICABLE -- the identity rows are written and deleted with the operator's own credentials under the pair; the key read is reported after the fact through `0.0.0_AB_MSTR~DELL2`. comp-adversary: the lens: the routing window left open or the synthetic coordinator left as the sole primary (the window is closed first on any STOP), a delete by a wrong key (the ticket id is printed and the item saved before the delete), Andrew's tickets touched, a fire window opening mid-run, a Trade Request option on PROD. BLIND to: the GO text (not yet written).
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R20-rv-3, PROD journey): a live run under a signed never-widen pair; not a worker cell (it holds credentials a worker subagent does not).
</task_order>
