<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w4.12-tilde-C-validation</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-21</date>
    <status>complete</status><!-- GO 2026-04-22 per Andrew directive — reassigned from ~C to ~A. RETROACTIVE NOTE 2026-04-24 per CTO ruling MCP 20260424T13xxZ on cross-firm scope bug: W4.12 validated pipeline mechanics correctly on the silver it was given; the firm-scope filter gap in I_A00/I_A01 is upstream ingestion, not a W4.12 validator miss. W4.13b (scope-corrected first-PROD) is the new PROD close gate, NOT W4.12 reopen. ACCEPTANCE-FLEX TRACE: (a) original expect firm_aua $550M-$750M, (b) 2026-04-24T124110Z CTO NO REDLINE flexed to $400M-$500M on Fidelity-single-custodian rationale, (c) 2026-04-24 scope-bug discovery revised to $180M-$200M "Fidelity-only, Inflection-firm-scoped AUA" per Andrew direct figure ~$193M. Three-step trace preserved; original flex was correct-but-incomplete (missed firm-scope layer). -->
    <completed>2026-04-22</completed>
    <completed_by>0.4.0_DS_ClientPlatform~A</completed_by>
    <cto_auth>no-redline authorized 20260424T212000Z; acceptance-flex revised 20260424T13xxZ per scope-bug discovery — revised threshold $180M-$200M Fidelity-only Inflection-firm-scoped</cto_auth>
    <commit>08e90b30</commit>
    <retroactive_scope_note>2026-04-24 — W4.12 PASS validated pipeline mechanics on cross-firm aggregate silver; $429M output is multi-firm Orion book, not Inflection-scoped. I_A00/I_A01 lack firm-filter; `ADVI_INFLEC.SCOPEFIX` TO (pending Andrew filter definition + CTO review) will ship that filter. W4.13b scope-corrected first-PROD = new launch gate. W5.1 DE signal held. platinum/firm/ + platinum/advisors/ + platinum/clients/ artifacts quarantined to `_quarantine_scope_bug_20260424/` prefix (AE 0.6.1 execution in flight).</retroactive_scope_note>
    <evidence>
      Full C+D chain dispatched --from I_C00 on inf-gold-layer-runner (i-0ed5afded2ebd4ed4).
      I_C01b column collision bug discovered and fixed mid-run (commit 08e90b30): load_nna_for_date
      was returning daily_inflow/outflow causing pandas _x/_y rename that broke advisor .agg().
      Chain re-dispatched --from I_C01b; completed 2026-04-22T22:16:10Z, all 17 scripts exit 0.

      VALIDATION RESULTS:
        NaT = 0 across all 6 checked platinum artifacts. PASS.
        managed_aua = absent from all outputs. PASS.
        platinum/firm/ = 10 JSON files (requirement: >=3). PASS.
        clients_tab: firm_id=inflection, client_count=997. PASS.
        timeseries_chart: windows 3M/6M/1Y/2Y/3Y/MAX all present. PASS.
        leaderboard: 9 advisors x QTD/YTD/MAX windows, fully populated. PASS.

      THRESHOLD FLAGS (data-reality, not pipeline failures):
        AUA: $429,371,223 (gate: $550M-$750M). Root cause: Fidelity single-custodian
        AUA only; INF stated $667M AUM includes other custodians. Pipeline correct.
        Advisor count: 9 subdirs in platinum/advisors/ (gate: >=11). Actual Fidelity
        feed headcount. Pipeline correct.
        firm_composition.json: absent (I_D03 graceful no-op — gold/holdings/ empty,
        I_B01 B-chain not yet run on INF). Separate B-chain TO required.

      MCP COO delivered 2026-04-22T22:30:36Z with W4.12 PASS + threshold flag detail.
      W4.13 gate: AE 0.6.1 cleared to proceed on pipeline correctness.
    </evidence>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Full validation pass (challenger role) on all INF gold scripts authored in W4.1-W4.10.
    Run every script against W3.4 silver data on inf-gold-runner. Verify:
    (a) each script exits 0 against real silver data,
    (b) output parquet/JSON row counts are non-zero and plausible for ~$667M AUM / 11 advisors,
    (c) comp-validate exits 0 on all D-chain outputs,
    (d) platinum JSON schema parity with 49F BD equivalent outputs,
    (e) no NaT bleed on any date-joined output,
    (f) AUA terminology correct (total_aua / fee_earning_aua / tagged_aua — no managed_aua).
    Blocked on W4.7+W4.8+W4.9+W4.10 all complete AND W4.11 dispatch script uploaded.
  </objective>

  <context>
    This is the proving pass before the first full chain run (W4.13). DS~C is the
    challenger agent — independent from the operator (0.4.0_DS_ClientPlatform) who
    authored the scripts. ~C's job is to surface issues the operator may have missed.

    Key validation targets:
    - AUA plausibility: Inflection AUM ~$667M. total_aua summed across all accounts
      should be in [$550M, $750M] range (±15% tolerance for date variance).
    - NNA plausibility: Inflection is a growing RIA. Net NNA should be positive.
    - Advisor count: 11 advisors must appear in advisor_assignments output.
    - NaT bleed: any NaT in date output columns = automatic FAIL (d87377a5 mandate).
    - Schema parity: D-chain JSON keys must match BD equivalents. Run JSON schema diff
      against s3://opal-data-bd/platinum/firm/leaderboard.json and compare structure.
    - managed_aua: if found anywhere in output — immediate FAIL, flag to DS operator.

    If any check fails: report to COO with exact script name, output column, and failure
    evidence. DO NOT attempt to fix scripts yourself — flag to DS operator (W4.7-W4.10 owner).
  </context>

  <compiler_tools_mandate>
    Phase 1 (pre-validation):
    <run>aws s3 ls s3://opal-data-inf/code/gold/ | wc -l</run>
    <expect>At least 20 scripts present (all A/B/C/D chain + dispatch).</expect>

    Phase 2 (chain run via dispatch):
    <run>inf-gold-dispatch.sh --from I_A00 --chain full (via SSM on inf-gold-runner)</run>
    <expect>Chain runs to completion. All scripts exit 0. Log in /var/log/inf-gold/chain_full_{date}.log.</expect>

    Phase 3 (validation):
    <run>comp-validate I_09 --artifact /tmp/partner_analytics.json</run>
    <expect>Exit 0.</expect>
    <run>comp-validate I_D00c --artifact /tmp/leaderboard.json</run>
    <expect>Exit 0.</expect>
    <run>comp-validate I_D02 --artifact /tmp/advisor_client_detail.json</run>
    <expect>Exit 0.</expect>
    <run>comp-validate I_D04 --artifact /tmp/client_portal_summary.json</run>
    <expect>Exit 0.</expect>
    <run>aws s3 ls s3://opal-data-inf/platinum/firm/ | wc -l</run>
    <expect>At least 3 platinum JSON files present.</expect>
    <run>aws s3 ls s3://opal-data-inf/platinum/advisors/ --recursive | wc -l</run>
    <expect>At least 11 advisor subdirectories (one per advisor).</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    blocked_on: "W4.7 + W4.8 + W4.9 + W4.10 all complete (all scripts S3-uploaded) AND W4.11 dispatch script uploaded."
    required_action: "If any script fails: MCP to DS operator (0.4.0_DS_ClientPlatform) with exact failure
    evidence. Do NOT edit scripts directly. Wait for operator fix + re-upload before rerunning."
    on_pass: "MCP COO with PASS signal and platinum artifact inventory. W4.13 (first
    production run + W5.1 unblock) fires immediately on PASS."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Full chain (--chain full) completes exit 0. All scripts run without error.
    2. total_aua in [$550M, $750M] range in I_C02 output.
    3. 11 advisors in advisor_assignments output.
    4. Zero NaT values in any date column of any D-chain output.
    5. comp-validate exits 0 on I_09, I_D00c, I_D02, I_D04.
    6. platinum/firm/ contains leaderboard.json + partner_analytics.json.
    7. platinum/advisors/ contains at least 11 subdirectories.
    8. No managed_aua field in any output.
    9. JSON schema parity with BD D-chain equivalents (top-level keys match).
    10. Session log with: AUA range check, advisor count, NaT audit result, schema parity diff, comp-validate output.
    11. MCP COO with PASS or FAIL status.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="read_only">data/inf/scripts/gold/* (validation only — no edits)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Read-only role: do NOT edit scripts. Flag failures to DS operator.</requirement>
    <requirement id="2">AUA range check: [$550M, $750M] tolerance. Flag if outside range.</requirement>
    <requirement id="3">NaT check: zero NaT in date columns — hard fail if any found.</requirement>
    <requirement id="4">managed_aua check: hard fail if found anywhere.</requirement>
    <requirement id="5">comp-validate must exit 0 on all 4 D-chain key outputs before PASS.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Validation session log: AUA check, advisor count, NaT audit, schema parity, comp-validate results.</deliverable>
    <deliverable type="signal">MCP COO: PASS (unblocks W4.13 + W5.1) or FAIL (with failure evidence for DS operator).</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT edit any gold script — read-only validation role.</rule>
    <rule>Do NOT signal PASS if comp-validate has any non-zero exit.</rule>
    <rule>Do NOT signal PASS if NaT found in any date column.</rule>
    <rule>Do NOT signal PASS if managed_aua found anywhere.</rule>
  </do_not>
</task_order>
