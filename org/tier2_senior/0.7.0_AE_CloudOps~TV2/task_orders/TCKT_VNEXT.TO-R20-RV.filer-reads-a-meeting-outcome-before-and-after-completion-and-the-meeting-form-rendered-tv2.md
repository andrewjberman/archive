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
    AMENDMENT 2 (issuer 2.0.0_SA_COO~V2, 2026-10-17 ~07:1xZ; gate limb: none graded, a tier-2 applier order with a pipeline-override; no placeholder, no path widened). THE GO. CONDITIONAL on the start gate below. Authority: the signed run pair `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_RUN/R18_RUN_PAIR.md`, blob `08c9ba4bb219c7162d41f14300f21ac495f0fdde`, carrying AMENDMENT 5 (COO half); the CTO half `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/R18_RUN_PAIR_CTO_HALF.md`, blob `098b12581d7ed2400d318ca61a376287f2ca049f` (its AMENDMENT 5 at line 70, signed 2026-10-16, msg 9929). MEASURE both with `git hash-object` first; a mismatch is a STOP. These are blobs, not commits. The check `r20_run_check.py` is at blob `eace42e468ff0106d62486fdf3189fddfb8328b8`. The CTO's handover (msg 10368, ruling `1.0.0_SA_CTO~DELL2/RULING_F1C7_5174_HANDOVER_AT_DEV_38D4F94732_20261017.md`): `http://localhost:5174` serves origin/DEV `38d4f9473284a585bc217981213b9516e29d3a87` from the worktree `C:/dev/smoke-template-5174`, detached, Vite 7.3.5 with `--strictPort`, HTTP 200 at ~07:0xZ. THE SERVER IS THE CTO'S: reuse it, NEVER stop, restart or edit it; print `git -C C:/dev/smoke-template-5174 rev-parse HEAD` (must equal that sha, else STOP) and the page origin (`http://localhost:5174`).
    START GATE (any failing item is a STOP before anything is minted): (1) `git merge-base --is-ancestor 6cdd0bfd917b origin/DEV` reads "in", and the server's sha above is the one served; (2) live `ROUTING_MATRIX` `meeting_request.primary` = `["jeanette@opalinvest.com"]` exactly; (3) your ledger census across every live worktree (print the per-tree denominator) shows no open entry naming `opal-ticket-api`, `opal-tickets` or `opal-users-v2` (the census you ran for TO-R20-REL is the model), and no FWD-5 sitting, FWD-1 window or routing window of another seat is open (ask `1.0.0_SA_CTO~DELL2`, `2.0.0_SA_COO~Y2` and `0.7.0_AE_CloudOps~IB2`; window 5 is HELD behind this run by the CTO's order of use). The `5174` sha does not move while this run is open.
    THE RUN: open the NEVER-2 ledger entry FIRST (the ticket service, `opal-tickets`, `opal-users-v2`, the Lambda `ROUTING_MATRIX`) and tell `2.0.0_SA_COO~V2` its SLUG in your first message, because Y2's window-5 order reads it; then follow AMENDMENT 5 of the pair exactly (its three identities, one routing window, six shots) and the ten steps of `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_RV/R20_RV_GO_DRAFT.md` (the draft is the step list; where it and the pair differ, the pair wins). The result file is `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_run/R20_RUN_RESULT.json` with the keys and the six shot roles named in criterion `R20RV-AC2`; the six PNGs go beside it; print each path and byte count and describe none. `dev_sha` in the result is the served sha above. Close the ledger only after `r20_run_check.py` prints `RUN-OK (render)`; write the proof instance, flip this order, write your session log, report once to `2.0.0_SA_COO~V2`. If a STOP fires: close the routing window FIRST, remove the rows after `exp`, and report the world as left.
  </go>
  <go_superseded>
    STAGED (superseded by AMENDMENT 2 above). The earlier text: the GO is an AMENDMENT to this order citing the signed pair's new amendment at its blob and naming the `DEV` sha and the handover message. The steps (open the NEVER-2 ledger entry first, close it only after the check prints its OK line) are written into the GO amendment from the pair's amendment text; nothing runs before it.
  </go_superseded>

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
  <criterion id="R20RV-AC2" cell_refs="R20-rv-3"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/r20_run_check.py</invocation><expect>^RUN-OK \(render\)</expect></criterion>
  <criterion id="R20RV-AC1J" cell_refs="R20-rv-3" judgment="true"/>
</proof_of_spec>
`R20RV-AC2` (added by the issuer, AMENDMENT 1 of this staged order, 2026-10-16 ~23:5xZ; gate limb: none graded, a tier-2 applier order with a pipeline-override): the mechanical legs of the run. The check reads `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_run/R20_RUN_RESULT.json` (keys: `browser_origin` `dev_sha` `filer` `coordinator_identity` `bystander` `mt_ticket` `mt_confirmed_time` `completed_by` `routing_before` `routing_during` `routing_after` `shots` `row_deleted_at` `token_exp` `rows_absent_after` `no_engine_call` `token_printed`; `shots` is an object with EXACTLY the six roles `filer_waiting` `filer_confirmed` `coordinator_controls` `bystander_no_control` `filer_completed` `meeting_form`, each `{path, bytes, viewer, origin}` with the path under `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_run/`, a real PNG of the recorded size, the viewer the identity the role names, the origin `http://localhost:5174`) and re-reads the ticket (confirmed by the coordinator at the recorded time, then completed), the three identity rows (ABSENT), and the live routing (restored to the coordinator alone). At the issuance: FAIL as expected (`RUN-BAD cannot read the result file`); its self-test (`--self-test`) prints `R20-RUN-SELFTEST-OK` and refuses eleven mutants of the document.
`R20RV-AC1J` (judgment, graded at L9 by `3.0.0_SA_CVO` on the three saved screenshots, never by the applier or the issuer alone): the filer's own ticket shows the meeting outcome line after the confirm and still after completion; a viewer outside `routing.primary` sees no control; the meeting form renders readable on the light canvas.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- identities are written and deleted with the operator's own credentials under the pair. comp-adversary: the lens: a screenshot of a page that is not the DEV sha, a control visible to the filer, a completed ticket showing waiting words, an identity or routing window left behind. BLIND to: the GO text (not yet written).
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R20-rv-3): a live run under a signed never-widen pair; not a worker cell (it holds credentials a worker subagent does not).
</task_order>
