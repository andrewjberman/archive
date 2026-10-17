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
    STAGED. The GO is an AMENDMENT to this order citing the signed pair's AMENDMENT 8 at its blob (COO half and CTO half, both measured) and the check `r20_prodjourney_check.py` at its blob, written on the day of the run. Then, in order: the pair's AMENDMENT 8 steps 0 to 5 (open the ledger FIRST and send the slug to `2.0.0_SA_COO~V2` and `2.0.0_SA_COO~Y2`; ask the CTO and IB2 for the day's fire windows and print the answer; the start gate; mint TWO identities; the routing window; the journey on `https://opalinvest.dev`; the removal by key, the ticket record saved first; `r20_prodjourney_check.py` `RUN-OK (prodjourney)`; close the ledger only after that). If a STOP fires: close the routing window FIRST, remove the rows after `exp`, remove the ticket by key if it was created, report the world as left. Report once to `2.0.0_SA_COO~V2`.
  </go>

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
  <criterion id="R20PROD2-AC1" cell_refs="R20-rv-3"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/r20_prodjourney_check.py</invocation><expect>^RUN-OK \(prodjourney\)</expect></criterion>
  <criterion id="R20PROD2-AC2J" cell_refs="R20-rv-3" judgment="true"/>
</proof_of_spec>
`R20PROD2-AC1` at the issuance: FAIL as expected (`RUN-BAD cannot read the result file`: no result file). The check holds the world's side: the synthetic ticket and both rows ABSENT, the routing restored, the two protected tickets present, the shots PNGs at the PROD origin by the right viewers, Trade Request absent, a printed contrast of at least 4.5. `R20PROD2-AC2J` (judgment, graded at L9 by `3.0.0_SA_CVO`, with the issuer's pixel measurement as evidence): the filer filed on the PROD page; the coordinator confirmed on it; the filer reads the confirmed line readable, no control.

<preflight>
comp-schedule: RUN-AS-A-READ -- the fire windows are asked of the CTO and IB2 at the start gate; the run starts only outside them. comp-iam: DECLARED-NOT-APPLICABLE -- the identity rows are written and deleted with the operator's own credentials under the pair; the key read is reported after the fact through `0.0.0_AB_MSTR~DELL2`. comp-adversary: the lens: the routing window left open or the synthetic coordinator left as the sole primary (the window is closed first on any STOP), a delete by a wrong key (the ticket id is printed and the item saved before the delete), Andrew's tickets touched, a fire window opening mid-run, a Trade Request option on PROD. BLIND to: the GO text (not yet written).
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R20-rv-3, PROD journey): a live run under a signed never-widen pair; not a worker cell (it holds credentials a worker subagent does not).
</task_order>
