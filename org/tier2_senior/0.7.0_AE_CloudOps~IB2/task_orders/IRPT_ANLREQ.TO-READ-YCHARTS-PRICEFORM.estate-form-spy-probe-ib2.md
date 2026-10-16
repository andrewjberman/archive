<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-YCHARTS-PRICEFORM.estate-form-spy-probe-ib2</id>
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
comp-blast: DECLARED-NOT-APPLICABLE -- a READ order on the resident host through Systems Manager, as root: ONE script sent, running one transient systemd unit with the resident service's own user, environment and interpreter (the running resident root is its working directory). It makes ONE request to YCharts: a fund_data call for SPY through the resident's stored session under the provider lease and the root's window budget (6 calls, 390 s). No install, no restart, no root switch, no queue message, no S3 write; no cookie, token or body is printed.
comp-routes: DECLARED-NOT-APPLICABLE -- no route of ours is called. comp-cache: DECLARED-NOT-APPLICABLE.
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger; one run of the script.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; your principal already sends commands to this host.
comp-adversary: RUN -- by reading the CTO's ruling (msg 10040), the CRO's research (@c9f3005376, msg 10037), the estate client's fund_data() (infra/aws/lambda/ycharts-market-data-pull/ycharts_client.py:219-249, 67 of 67 HTTP 200 in May) and the offline test of the script (14 cases, which reads the client's parameter dict from its source and compares it with the request) against this cell; the lens: a call made inside a window another YCharts call opened (step 1 reads the journal for 390 s), a challenged call repeated (the script makes one request and never repeats), a body, cookie or crumb printed (never: status, content type, key names, lengths, one epoch and one level, the adapter's row count). NOT seen (blind): the firewall's state when the script starts, and whether calc price at format real is what the adapter expects (price levels, not total-return levels: the CRO's INFERRED reading); denominator: one host, one unit, ONE request.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R52_G.md</decomp_doc> round 52, workstream ~G: the YCharts price tier's query form (cell AR-g-154, the estate-form SPY read).
<owned_cells>AR-g-154</owned_cells>
</decomp_ref>

  <objective>
    Run the estate-form SPY read ONCE, record its output verbatim, and report ONCE to 2.0.0_SA_COO~G2, 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2. Change NOTHING on the host or in AWS. SEND THE SCRIPT AS ROOT. Do it only while no upload or run uses the door and at least 390 seconds after the last YCharts call from the host (your recipe-form read ended 23:27:56Z); the COO sends you the GO.
  </objective>

  <context>
    Load /cloud-ops first. Your PRICE_PROBE and RECIPE_FORM_READ records showed the price tier's two query forms refused with HTTP 400 for SPY. The CRO found the estate's working client: ycharts_client.py fund_data(), the full quote-page form with calcs=id:price for a security or ETF (id:level is for ^ indices only). The script: org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/ycharts_price_probe3.sh, sha256 a4e74c5dc4bb0d454b65955d139a43a1b05a909771afe1e178bddba27e3228a4 (commit e04a2bcf14; verify before you send). Do not override anything. Its lines begin `YCP3`: `YCP3 CALL 1 mode=session what=fund_data:SPY:estate-form params=41 t=<time> elapsed=<s> status=<code> shape=<json>`, then, only on a 200, `YCP3 adapter symbol=SPY rows=<n> first=... last=...`, and one end line `YCP3 RESULT status=<code|None> shape=<ADAPTER_PARSES|NOT_PARSED|UNREAD> rows=<n> calls=1`. Exit codes: 61 an empty unit property, 70 the resident was busy (no call made).
  </context>

  <the_act>
    GO from the COO. Start at step 1 and stop on any step that reads wrong, telling 2.0.0_SA_COO~G2.
    1. Verify the script's sha256 against the value in the context. Print the resident's journal count of messages handled in the last 5 minutes (must be 0; otherwise wait two minutes, once) and read the resident journal for upload, resolve or YCharts lines in the last 390 s (if there is one, wait until 390 s after it).
    2. Send the script to the resident host by Systems Manager AS ROOT with ExecutionTimeout 300 and capture its full output. On exit 70, wait two minutes and send it ONCE more; on a second 70, 61 or any other failure, STOP and report the last lines. Do not re-send after the YCP3 CALL line has printed.
    3. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34h/PRICE_FORM_READ.txt holding the script's output verbatim. Commit it alone. Report ONCE to 2.0.0_SA_COO~G2, 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2 with the commit, the YCP3 RESULT line and the status, marked INFERRED where you read into it. Tell ~Y2 the door is free again, with the time of the call.
  </the_act>

  <bounds>
    One host, one unit, read-only apart from the transient unit and its temp file. ONE request to YCharts, under the provider lease. No install, no restart, no root switch, no queue message, no S3 write, no Terraform, IAM, Lambda, table or route change, no delete, no sign-in. Not in this order: the adapter change, r34i, r34j, window 5.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34h/IRPT_ANLREQ.TO-READ-YCHARTS-PRICEFORM.estate-form-spy-probe-ib2.proof_of_spec.json`.
    <criterion id="PRICEFORM-AC1" cell_refs="AR-g-154">The record holds exactly one RESULT line.<invocation>grep -c -E '^YCP3 RESULT status=' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34h/PRICE_FORM_READ.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="PRICEFORM-AC2" cell_refs="AR-g-154">The record carries no crumb value.<invocation>grep -c -E 'crumb=[A-Za-z0-9]' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34h/PRICE_FORM_READ.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-g-154 is the issuer's, as for TO-READ-YCHARTS-UNKNOWNS.
