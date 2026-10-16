<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-YCHARTS-RECIPEFORM.recipe-form-price-probe-ib2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-16</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- a READ order on the resident host through Systems Manager, as root: ONE script sent, running one transient systemd unit with the resident service's own user, environment and interpreter (the running r34h root is its working directory). It makes at most FOUR requests to YCharts (fund_data calls through the resident's stored session and one signed-out, or, only if the first is refused, one sessionless lookup and its typed-id repeats), every one through the provider lease under the root's window budget (6 calls, 390 s). No install, no restart, no root switch, no queue message, no S3 write; no cookie, token or body is printed.
comp-routes: DECLARED-NOT-APPLICABLE -- no route of ours is called. comp-cache: DECLARED-NOT-APPLICABLE.
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger; one run of the script.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; your principal already sends commands to this host.
comp-adversary: RUN -- by reading the CTO's ruling (msg 9991), your PRICE_PROBE record (HTTP 400 on the id:TICKER form, signed in and out), the CRO's captured map (overview_map.json call benchmark_level_series) and the offline test of the script (19 cases) against this cell; the lens: a call made inside a window another YCharts call opened (the script's busy guard reads only the last 60 s of resident messages, so step 1 of the act also reads the journal and your own record for any YCharts call in the last 390 s), a challenged call repeated (the script makes no more than four and stops its branches on a refusal), a body, cookie or crumb printed (never: only status, key names, lengths, one epoch and one level, the adapter's rows and, in branch B, the public lookup id fields). NOT seen (blind): the firewall's state when the script starts, and whether the recipe form answers a plain ticker; denominator: one host, one unit, at most four requests.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R52_G.md</decomp_doc> round 52, workstream ~G: the YCharts price tier's query form (cell AR-g-151, the read).
<owned_cells>AR-g-151</owned_cells>
</decomp_ref>

  <objective>
    Run the recipe-form read ONCE, record its output verbatim, and report ONCE to 2.0.0_SA_COO~G2, 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2. Change NOTHING on the host or in AWS. SEND THE SCRIPT AS ROOT. Do it only while no upload or run uses the door and at least 390 seconds after the last YCharts call from the host; the COO sends you the GO.
  </objective>

  <context>
    Load /cloud-ops first. Your PRICE_PROBE record showed the tier's query `securities=id:<TICKER>,include:true,&zoom=max` is refused with HTTP 400 text/plain, signed in and signed out. The CRO's captured working series call (overview_map.json, benchmark_level_series) is `securities=id:^SPXTR,include:true,,` with `calcs=id:level,include:true,,`, `zoom=max`, `maxPoints=100000`, `partner=basic_2000`. The script: org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/ycharts_price_probe2.sh, sha256 08daec715df3e5950822c6c35c8cd17510f670239a9e6524b3aa48a9b8829282 (commit 5b3d245789; verify before you send). Do not override anything. Its lines begin `YCP2`: `YCP2 CALL <n> mode=<session|sessionless> what=<...> t=<time> elapsed=<s> status=<code> shape=<json>`, `YCP2 adapter symbol=<S> rows=<n> first=... last=...`, in branch B `YCP2 LOOKUP SPY row_keys=... id_fields=...`, and one end line `YCP2 RESULT form=<RECIPE_PLAIN|RECIPE_TYPED|NONE> plain=<...> typed=<...> shape=<...> second_symbol=<...> signed_out=<...> calls=<n>`. Exit codes: 61 an empty unit property, 70 the resident was busy (no call made).
  </context>

  <the_act>
    GO from the COO. Start at step 1 and stop on any step that reads wrong, telling 2.0.0_SA_COO~G2.
    1. Verify the script's sha256 against the value in the context. Print the resident's journal count of messages handled in the last 5 minutes (must be 0; otherwise wait two minutes, once) and the time of the last YCharts call from the host that you know of (your PRICE_PROBE run ended 22:58:18Z; ~Y2 may have started a call since: ask no one, read the resident journal for upload or resolve lines in the last 390 s; if there is one, wait until 390 s after it).
    2. Send the script to the resident host by Systems Manager AS ROOT with ExecutionTimeout 600 and capture its full output. On exit 70, wait two minutes and send it ONCE more; on a second 70, 61 or any other failure, STOP and report the last lines. Do not re-send after any YCP2 CALL line has printed.
    3. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34h/RECIPE_FORM_READ.txt holding the script's output verbatim. Commit it alone. Report ONCE to 2.0.0_SA_COO~G2, 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2 with the commit, the YCP2 RESULT line and each call's status, marked INFERRED where you read into it. Tell ~Y2 the door is free again.
  </the_act>

  <bounds>
    One host, one unit, read-only apart from the transient unit and its temp file. At most FOUR requests to YCharts, all under the provider lease. No install, no restart, no root switch, no queue message, no S3 write, no Terraform, IAM, Lambda, table or route change, no delete, no sign-in. Not in this order: the adapter change, r34i, window 5.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34h/IRPT_ANLREQ.TO-READ-YCHARTS-RECIPEFORM.recipe-form-price-probe-ib2.proof_of_spec.json`.
    <criterion id="RECIPEFORM-AC1" cell_refs="AR-g-151">The record holds exactly one RESULT line.<invocation>grep -c -E '^YCP2 RESULT form=' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34h/RECIPE_FORM_READ.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="RECIPEFORM-AC2" cell_refs="AR-g-151">The record carries no crumb value.<invocation>grep -c -E 'crumb=[A-Za-z0-9]' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34h/RECIPE_FORM_READ.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-g-151 is the issuer's, as for TO-READ-YCHARTS-UNKNOWNS.
