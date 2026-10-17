<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R20-RV2.filer-re-reads-the-completed-meeting-ticket-on-the-fixed-dev-build-tv2</id>
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
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R20.md</decomp_doc> (round 20, AMENDMENTS 1 and 2): the re-shot of cells `R20-pt-5` and `R20-rv-3`.
<owned_cells>R20-rv-3</owned_cells>
</decomp_ref>

  <objective>
    STAGED. No GO until the issuer appends the CTO's signature of run-pair AMENDMENT 6 and writes the GO below, both blobs MEASURED with `git hash-object`. On the GO, re-read the SAME completed meeting ticket `TCK-20261017-da2a1987` on the FIXED DEV build as one synthetic filer: move the CTO's 5174 server (the worktree `C:/dev/smoke-template-5174`) to the named DEV sha that carries the contrast fix (`539b1ee70ba1b2a9b0c562a9169d9fcca1b7c18e`, or a descendant carrying it, at or past `8ecad4a5fb`) under the CTO's msg 10441, take ONE screenshot (`filer_completed`), remove the one identity row, write one result file.
  </objective>

  <context>
    The procedure is run-pair AMENDMENT 6 (`org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_RUN/R18_RUN_PAIR.md`); the model is `TO-R20-RV` (it ran `RUN-OK (render)`, ledger `tckt-vnext-r20-rv-20261017`). Why a re-shot: the PART 3 shots showed the outcome line at 1.25:1 (row `TCKT_VNEXT-D2-S59`); the fix is merged on DEV (row `dell2-20261017T085342Z-3fed`). Your inbox watcher missed the PART 3 GO for 55 minutes (row `TCKT_VNEXT-D2-S58`): run `check-inbox` before you conclude there is no GO.
  </context>

  <go>
    STAGED. The GO is an AMENDMENT to this order citing the signed pair's AMENDMENT 6 at its blob (COO half and CTO half, both measured) and the check `r20_reshot_check.py` at its blob. Then, in order: the pair's steps 0 to 4 (open the ledger first and send the slug to `2.0.0_SA_COO~V2` and `2.0.0_SA_COO~Y2`; the start gate; name the sha BEFORE moving the server; move it and tell the CTO the sha; mint ONE identity; the read and the ONE shot; removal after `exp`; `r20_reshot_check.py` `RUN-OK (reshot)`; close the ledger only after that). If a STOP fires, remove the row first after `exp` and report the world as left. Report once to `2.0.0_SA_COO~V2`.
  </go>

  <bounds>
    The blast radius is the pair's AMENDMENT 6: ONE `opal-users-v2` row created and deleted; `opal-tickets` NO write; no routing window, no Lambda change, no S3 object, no mail; the 5174 server moves to the named sha at the CTO's word and is not otherwise touched.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="R20RV2-AC1" cell_refs="R20-rv-3"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/r20_reshot_check.py</invocation><expect>^RUN-OK \(reshot\)</expect></criterion>
  <criterion id="R20RV2-AC2J" cell_refs="R20-rv-3" judgment="true"/>
</proof_of_spec>
`R20RV2-AC1` at the issuance: FAIL as expected (`RUN-BAD cannot read the result file`: no result file). `R20RV2-AC2J` (judgment, graded at L9 by `3.0.0_SA_CVO`, with the issuer's pixel measurement of the line's contrast as evidence): the filer's own completed ticket shows the confirmed outcome line readable on the board row, no control.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- the identity row is written and deleted with the operator's own credentials under the pair; the key read is reported after the fact through `0.0.0_AB_MSTR~DELL2`. comp-adversary: the lens: a server moved to a sha that is not the named one or a descendant without the fix, an origin other than `http://localhost:5174`, a filer row left behind, a ticket write the read does not need, a screenshot of the old build. BLIND to: the GO text (not yet written).
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R20-rv-3, re-shot): a live read under a signed never-widen pair; not a worker cell (it holds credentials a worker subagent does not).
</task_order>
