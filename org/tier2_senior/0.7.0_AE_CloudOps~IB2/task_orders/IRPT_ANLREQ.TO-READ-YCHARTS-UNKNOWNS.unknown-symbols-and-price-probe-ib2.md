<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-YCHARTS-UNKNOWNS.unknown-symbols-and-price-probe-ib2</id>
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
comp-blast: DECLARED-NOT-APPLICABLE -- a READ order on the resident host through Systems Manager, as root: two scripts sent one after the other, each running one transient systemd unit with the resident service's own user, environment and interpreter (the running r34h root is its working directory). Script 1 makes up to TWELVE cookieless lookups (six made-up tickers and six of AAPL) to YCharts over about 21 minutes. Script 2 makes THREE fund_data calls (id:SPY and id:AAPL through the resident's stored session under the provider lease and the root's budget, id:SPY signed out). No install, no restart, no root switch, no queue message, no S3 write; the stored session is used by script 2 only and no cookie, token or body is printed.
comp-routes: DECLARED-NOT-APPLICABLE -- no route of ours is called. comp-cache: DECLARED-NOT-APPLICABLE.
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger; one run of each script.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; your principal already sends commands to this host.
comp-adversary: RUN -- by reading the CTO's conditions (msgs 9727, 9761 and 9902), the CRO's research (msg 9758), the AQ2 and IB2 reads of the paced lookup (12 of 12 clean) and the offline tests of both scripts (13 and 16 cases) against this cell; the lens: a call made while ~Y2 has a window running (both scripts share the firewall window with every other YCharts call from this host, so the order starts only on a free door and the scripts' busy guard exits 70), script 2 run too soon after script 1 (the order fixes the wait), a challenged call repeated (script 1 stops at its first challenge; script 2 makes three calls only), a body, cookie or crumb printed (never: script 2 prints the answer's key names, lengths, one epoch and one level, and the adapter's rows). NOT seen (blind): the firewall's state when script 1 starts, and whether the stored session answers; denominator: one host, one unit, at most 15 requests.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R51_G.md</decomp_doc> round 51, workstream ~G: the two r34h read conditions (cells AR-g-149 and AR-g-150).
<owned_cells>AR-g-149, AR-g-150</owned_cells>
</decomp_ref>

  <objective>
    Run the unknown-symbol paced read ONCE, then the three-unknowns measurement ONCE, record each output verbatim, and report ONCE to 2.0.0_SA_COO~G2, 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2. Change NOTHING on the host or in AWS. SEND EACH SCRIPT AS ROOT. Do it only AFTER ledger irpt-resident-r34h-20261016 reads CLOSED (your TO-APPLY-R34H) and only while ~Y2 has no window running on the host; the COO sends you the GO.
  </objective>

  <context>
    Load /cloud-ops first. CTO msgs 9761 and 9902, condition 1: these two reads run on r34h before any priced run uses the YCharts tier; the measurement never runs during a window. Script 1: org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/unknown_lookup_probe.sh, sha256 b88d5484491d4ab61018847bfb1a7a87c926560f70dd3368ce50d70d5de4f2d2. Script 2: org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/ycharts_price_probe.sh, sha256 24a941532c95c0680ca433ee1f6f9b3c1f7ec499c8c0048200ef90913baea2ef (both at commit 3a4190894c; verify both before you send). Do not override either script's defaults. Script 1 lines begin `UNK`: `UNK CALL <n> ticker=<i> kind=<LOOKUP|VERIFY> symbol=<S> t=<time> verdict=<CLEAN|CHALLENGED|EXCEPTION> ...`, then `UNK RESULT first_challenged_call=<n|none> calls=<m> unknown_lookups=<k>` and `UNK VERDICT ...`; it rests 390 s at its start, takes about 21 minutes and stops at its first challenged call. Script 2 lines begin `YCP`: `YCP CALL <n> mode=<session|sessionless> symbol=<S> ... shape=<json>`, `YCP CALL <n> adapter rows=...`, then `YCP RESULT id_form=<..> shape=<..> signed_out=<..>`; it takes under a minute. Exit codes of both: 61 an empty unit property, 70 the resident was busy (no call made).
  </context>

  <the_act>
    GO from the COO once the r34h ledger reads CLOSED and ~Y2 has no window running. Start at step 1 and stop on any step that reads wrong, telling 2.0.0_SA_COO~G2.
    1. Verify both scripts' sha256 against the values in the context. Print the r34h ledger's status (it must read CLOSED) and the resident's journal count of messages handled in the last 5 minutes (must be 0; otherwise wait two minutes, once).
    2. Send script 1 to the resident host by Systems Manager AS ROOT with ExecutionTimeout 3600 and capture its full output. On exit 70, wait two minutes and send it ONCE more; on a second 70, 61 or any other failure, STOP and report the last lines. Do not re-send after any call line has printed. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34h/UNKNOWN_READ.txt with the output verbatim and commit it alone.
    3. Wait at least 600 seconds after script 1's last line (900 seconds if its RESULT line shows a first challenged call). Then send script 2 AS ROOT with ExecutionTimeout 600 and capture its full output. Send it ONCE: on exit 70 wait two minutes and send once more; on any other failure STOP and report the last lines. Write PRICE_PROBE.txt in the same folder with the output verbatim and commit it alone.
    4. Report ONCE to 2.0.0_SA_COO~G2, 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2 with the commits, the UNK RESULT and UNK VERDICT lines, the YCP RESULT line and the first challenged call's time if any, marked INFERRED where you read into it.
  </the_act>

  <bounds>
    One host, one unit, read-only apart from the transient units and their temp files. At most TWELVE cookieless lookups and THREE fund_data calls to YCharts in all. No install, no restart, no root switch, no queue message, no S3 write, no Terraform, IAM, Lambda, table or route change, no delete, no sign-in. Not in this order: any change to the budget number, window 5, the classifier.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34h/IRPT_ANLREQ.TO-READ-YCHARTS-UNKNOWNS.unknown-symbols-and-price-probe-ib2.proof_of_spec.json`.
    <criterion id="UNKNOWNS-AC1" cell_refs="AR-g-149">The unknown read's record holds exactly one RESULT line and one VERDICT line.<invocation>grep -c -E '^UNK (RESULT first_challenged_call=|VERDICT )' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34h/UNKNOWN_READ.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="UNKNOWNS-AC2" cell_refs="AR-g-150">The price probe's record holds exactly one RESULT line.<invocation>grep -c -E '^YCP RESULT id_form=' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34h/PRICE_PROBE.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="UNKNOWNS-AC3" cell_refs="AR-g-149,AR-g-150">Neither record carries a crumb value.<invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34h/UNKNOWN_READ.txt org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34h/PRICE_PROBE.txt | grep -c -E 'crumb=[A-Za-z0-9]'</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cells AR-g-149 and AR-g-150 are the issuer's, as for TO-READ-PACING.
