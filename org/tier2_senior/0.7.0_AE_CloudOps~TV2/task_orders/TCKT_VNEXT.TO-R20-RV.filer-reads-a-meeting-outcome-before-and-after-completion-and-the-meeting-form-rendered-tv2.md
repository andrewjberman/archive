<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R20-RV.filer-reads-a-meeting-outcome-before-and-after-completion-and-the-meeting-form-rendered-tv2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-16</date>
    <status>staged</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>20</round>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R20.md</decomp_doc> (round 20): cell `R20-rv-3`.
<owned_cells>R20-rv-3</owned_cells>
</decomp_ref>

  <objective>
    STAGED. No GO until all three hold: (1) cell `R20-pt-1` is on portal `origin/DEV` (the issuer names the sha); (2) the CTO hands the 5174 server over, carrying that sha; (3) the issuer adds a CONDITIONAL GO amendment citing a NEW run-pair amendment (R18_RUN_PAIR AMENDMENT 5, both halves signed, blobs named). On the GO, run ONE live journey of the Meeting Request (FWD-11) read in the RENDERED page: one synthetic filer files one meeting ticket, reads it after the coordinator's confirm and again after completion (two screenshots), and the meeting form is rendered and read (a third screenshot). Remove the identities. Write one result file.
  </objective>

  <context>
    Authority: the CTO's rounds 18-19 analysis (`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_TCKT_VNEXT_ROUNDS_18_19_20261016.md`, rulings 2 and 4 and enrichment items 1 and 2) and the run pair `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_RUN/R18_RUN_PAIR.md` (identities, token, routing window and removal follow its original sections and its amendments; the new amendment carries this order's blast radius). The model is `TO-R18-RUN` PART 1 and `TO-R18-CLOSE`. Screenshots are READ by a seat that did not build the page (the issuer reads them; you save them and print their paths).
  </context>

  <go>
    STAGED. The GO is an AMENDMENT to this order citing the signed pair's new amendment at its blob and naming the `DEV` sha and the handover message. The steps (open the NEVER-2 ledger entry first, close it only after the check prints its OK line) are written into the GO amendment from the pair's amendment text; nothing runs before it.
  </go>

  <bounds>
    The blast radius is the pair's new amendment, not this order. Until it exists: no live call, no identity, no ticket, no routing window, no server start. The 5174 server is the CTO's to hand over; never stop or restart a server you did not start.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="R20RV-AC1J" cell_refs="R20-rv-3" judgment="true"/>
</proof_of_spec>
`R20RV-AC1J` (judgment, graded at L9 by `3.0.0_SA_CVO` on the three saved screenshots, never by the applier or the issuer alone): the filer's own ticket shows the meeting outcome line after the confirm and still after completion; a viewer outside `routing.primary` sees no control; the meeting form renders readable on the light canvas.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- identities are written and deleted with the operator's own credentials under the pair. comp-adversary: the lens: a screenshot of a page that is not the DEV sha, a control visible to the filer, a completed ticket showing waiting words, an identity or routing window left behind. BLIND to: the GO text (not yet written).
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R20-rv-3): a live run under a signed never-widen pair; not a worker cell (it holds credentials a worker subagent does not).
</task_order>
