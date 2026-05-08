<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFETL.CHAININC</id>
    <project>ADVI_INFETL</project>
    <title>Billing + Tax dims must be on the daily chain (CHAIN_FULL) — close GAP-7 from MDR</title>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>closed</status><!-- CLOSED 2026-05-08T~14:15Z by COO RAVC2 ACK. Phase 0/1 ran 2026-05-07 (DS~A canonical resync `e2d958fba` + AE 0.7 deploy bundle v1.7.36/v1.7.37 — Lambda canonical confirmed via Guard B bound `[$150M, $300M]`). Phase 2 empirical 2026-05-08 chain summary observed: 1-ok/6-fail with 3 distinct gap classes routed — Class 1 orchestrator timing race (AE 0.7 lane), Class 2 bronze gaps geo_verify+performance_dim (DS~A lane), Class 3 Guard B fails (RETIRED in `c481b7518` 2026-05-08) + accounts_v2 $0 (DS~A `cd77523b5` fix; tomorrow's chain summary is the empirical test). No further AE 0.6.1 action. -->
    <priority>high</priority>
    <estimated_effort>~0.5-1d (depending on root cause depth)</estimated_effort>
  </metadata>

  <references>
    <ref type="finding">DS~A MDR (85977d68a) GAP-7: "billing/tax silver OFF_CHAIN — not in CHAIN_FULL; daily chain doesn't get fresh billing/tax"</ref>
    <ref type="andrew_directive">2026-05-07: "billing and tax definitely need to be included in chain, give that task to 0.6.1_AE"</ref>
    <ref type="andrew_earlier">"make sure that all pipelines are running daily, that our gold runner is running daily, and that we have proper separation between gold and platinum"</ref>
    <ref type="ae_0_6_1_context">AE 0.6.1 shipped v1.7.31 + v1.7.32 today fixing billing silver builder. Owns billing pipeline domain expertise. Same canonical lane as inf-api-txn (v1.7.30). Lambda code is your authorial pattern.</ref>
    <ref type="related">INFETL.LAMBDA-DIMS — the comprehensive per-dim daily Lambda TO. CHAININC closes the immediate gap; LAMBDA-DIMS is the long-term home.</ref>
  </references>

  <context>
    DS~A's MDR audit surfaced that billing + tax silvers are NOT in the daily chain
    (CHAIN_FULL). Today's empirical: AE 0.6.1 had to manually retry 4 billing dates +
    push 71 historical sentinels via SSM scripts because the daily chain has no
    mechanism to keep billing fresh. Tax has the same gap.

    This is the structural class of bug Andrew flagged earlier: "all pipelines should
    be running daily." Bronze pulls (orchestrator.py DIMS list) DO include billing +
    tax. But the silver chain doesn't process them automatically when bronze lands —
    or the bronze itself isn't running daily for these dims.

    Investigation needed:
    1. Are billing + tax in the bronze orchestrator's DAILY run? (orchestrator.py
       DIMS list includes them, but is the orchestrator dispatched daily for these
       specific dims?)
    2. Does inf-silver-chain Lambda (or whatever silver trigger exists) process
       billing + tax silver builders when bronze sentinels land?
    3. If both bronze + silver triggers fire, why does AE 0.6.1 always have to
       manually re-fire billing dates?

    Once root cause identified, fix the missing trigger so daily refresh works
    automatically — no more manual SSM dispatches for routine billing/tax updates.
  </context>

  <scope>
    <step>
      Phase 0 — diagnose:
        a. Trace daily orchestrator dispatch flow for billing + tax. Does the EOM
           orchestrator dispatch include them? If not, why?
        b. Check inf-silver-chain Lambda (or equivalent) — does it react to billing
           + tax bronze sentinels and run convert_orion_api_to_silver --dim billing
           and --dim tax?
        c. Check billing's "monthly EOM" semantics: is the dim only refreshed at month
           end? If yes, that's intentional cadence — but the chain needs a monthly
           cron or the daily chain needs to be aware "billing = monthly".
        d. Same for tax — daily? quarterly? understand the intended cadence.
        e. RAVC0 with diagnosis + recommended fix path.
    </step>
    <step>
      Phase 1 — fix per Phase 0 diagnosis. Likely paths:
        Option A: Add billing + tax to inf-silver-chain Lambda's dim list so when
                  bronze sentinels land, silvers run automatically.
        Option B: Per-dim daily Lambda for billing + tax (forward-looking — fits
                  INFETL.LAMBDA-DIMS architecture). Fastest if you can mirror
                  inf-api-txn pattern directly.
        Option C: Hybrid — short-term silver-chain fix + long-term LAMBDA-DIMS as
                  separate work.
      
      Coordinate with AE 0.7 if Terraform changes needed (Lambda function or rule
      additions).
    </step>
    <step>
      Pre-commit gate + commit + push + S3 upload (per CLAUDE.md rule 13 if any DS
      gold scripts change). Tag inf-pipeline-v1.X.Y.
    </step>
    <step>
      Empirical: trigger a daily run, verify billing + tax silver land automatically
      without manual SSM dispatch. If they're EOM-only, verify next EOM date or simulate
      via overrideable date param.
    </step>
    <step>
      RAVC to COO: root cause + fix commit + empirical evidence (CW logs of automatic
      silver builder fires for billing + tax) + tag bump.
    </step>
  </scope>

  <compiler_mandate>
    <tool>comp-routes trace inf-silver-chain (or equivalent silver Lambda) — confirm dim list</tool>
    <tool>comp-pipescript io build_billing + build_tax — verify silver builder I/O</tool>
    <tool>comp-blast bronze/orion-api/{date}/billing.csv + tax_*.csv — reverse cover (who reacts when bronze lands)</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Diagnosis RAVC0 landed identifying root cause (bronze not daily / silver-chain missing dim / cadence mismatch / etc.)</criterion>
    <criterion id="AC2">Fix shipped — billing + tax silvers refresh automatically when bronze lands (or on appropriate cadence cron for EOM dims).</criterion>
    <criterion id="AC3">Empirical: tomorrow's daily run produces fresh billing + tax silvers without manual intervention.</criterion>
    <criterion id="AC4">No regressions on bronze chain (sentinels still fire correctly; orchestrator chain semantics preserved).</criterion>
    <criterion id="AC5">Tag bump + record-terraform-deploy if Terraform touched.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>None — independent investigation.</upstream>
    <downstream>INFETL.LAMBDA-DIMS may absorb the long-term Lambda implementation if you go Option B. Coordinate with AE 0.7 on lane.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~19:18Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Andrew direct: "billing and tax definitely need to be included in chain." You have the domain context from today's v1.7.31/32 work. Phase 0 diagnosis first, fix path your call. RAVC0 with diagnosis before shipping fix.</message>
  </go_signal>
</task_order>
