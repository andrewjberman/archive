<task_order>
  <metadata>
    <id>ADVI_INFETL.RUNDATE-DISPATCH</id>
    <slug>ae-catalog-rundate-step-aware-dispatch</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-15</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_INFETL</project_code>
    <priority>P1 -- the catalog --run-date gap blocks any windowed --chain full and is a candidate INFGRO chain #30 blocker. Deliverable (ii) is the fast unblock decision. AE 0.7.0 has near-term capacity: the other AE 0.7.0 TO (ADVI_TXNAMG.004) is dispatch_held on ADVI_TXNAMG.003.</priority>
    <sla>Deliverable (ii) FAST -- report within ~1h (it is an inspection/confirmation, not a 70min chain run). (i) + (iii) ~3-4h wall. (iii) is a PROPOSAL only -- CTO ratifies before any code change ships.</sla>
  </metadata>

  <references>
    <ruling>CTO architectural ruling 2026-05-15 (MCP to COO) -- the --run-date step-scoped frame + owner assignment to AE 0.7.0 + the ADVI_INFETL filing. This TO operationalizes that ruling verbatim.</ruling>
    <incident>AE 0.6.1 triage 2026-05-15: an aggregator-triggered `orion-gold-dispatch.sh --chain full --run-date 2026-05-14` failed at INF_API_SILVER_REPS -- catalog --run-date token mismatch (INF_API_PULL_* catalog entries lack a {date} placeholder). The daily 06:00 cron chain was unaffected; the orphan run was reaped by AE.</incident>
    <prd>docs/architecture/ADVI_INFETL.md (PRD v0.2) -- the catalog + aggregator/dispatch are ADVI_INFETL (aggregator/dispatch) domain.</prd>
    <scope_guard_ref>ADVI_TXNAMG PRD section-7-Q5 (Andrew append-only ingestion directive 2026-05-15) -- the systemic fix (date-windowing the pulls themselves) is the section-7-Q5 addendum scope, CTO-authored, reconciled with ADVI_INFINC. THIS TO IS TACTICAL ONLY (see scope_guard).</scope_guard_ref>
    <runbook>memory/reference_inf_ssm_direct_single_script_runbook.md + reference_opal_runner_shared_telemetry.md -- for any diagnostic dispatch + status reads.</runbook>
  </references>

  <context>
    `orion-gold-dispatch.sh --chain full` accepts an optional `--run-date`. The catalog's INF_API_PULL_* steps lack a {date} placeholder, so --run-date does not substitute into them and a windowed full-chain run fails at INF_API_SILVER_REPS. CTO architectural frame: --run-date is a STEP-SCOPED date parameter. The INF_API_PULL_* steps lacking {date} are mostly full-history, date-agnostic pulls -- the REST transaction pull is the clearest, date-agnostic by construction (that property is exactly what ADVI_TXNAMG / ADVI_INFINC exist to change). Passing --run-date to a date-agnostic step is a CATEGORY ERROR: you cannot add a meaningful {date} token to a script that consumes no date. Further: `--chain full --run-date {past date}` over date-agnostic pulls would produce a MIXED-DATE artifact (current pulls + past-date gold) -- the dispatcher should REJECT that combination loudly, not silently produce it. NOTE the empirical anchor for (ii): the daily 06:00 cron chain is a plain `--chain full` (no --run-date) and runs clean -- chain_full_20260515_060048 ran exit=0 today and materialized C-tier artifacts ~07:03Z. The failure is specific to the --run-date variant.
  </context>

  <objective>
    A characterization of the catalog --run-date substitution behavior, a fast empirical answer on whether a plain `--chain full` (no --run-date) is clean, and a proposed step-aware dispatch fix for CTO ratification. NO code change ships under this TO -- (iii) is a proposal; CTO rules; any implementation is a separate TO.
  </objective>

  <scope>
    <item id="ii" priority="FIRST -- fast, report within ~1h">
      Confirm whether a plain `orion-gold-dispatch.sh --chain full` (NO --run-date) is clean end-to-end -- i.e. the INF_API_SILVER_REPS failure is specifically the --run-date substitution and a no-run-date full chain is unaffected. This is an INSPECTION/CONFIRMATION, not a fresh 70min run: the daily 06:00 cron chain is itself a plain --chain full and runs clean (chain_full_20260515_060048 today, exit=0) -- confirm an on-demand plain --chain full is equivalent (same code path, no --run-date branch). REPORT THIS FIRST via a quick MCP to COO + CC CTO + CC DE 0.4 -- it is the chain #30 unblock decision.
    </item>
    <item id="i">
      Characterize the catalog --run-date substitution mechanism: how --run-date is templated into catalog entries, and an enumeration of which INF_API_PULL_* (and any other --run-date-touched) steps are genuinely date-agnostic (full-history, consume no date) vs date-capable (consume a date window). This enumeration is the input the step-aware fix needs.
    </item>
    <item id="iii">
      Propose the step-aware dispatch fix per the CTO frame: the catalog DECLARES per-step date-parameterization explicitly; the dispatcher passes --run-date ONLY to steps that declare they consume it; date-agnostic pulls are exempt BY DECLARATION (not a silent no-op). Plus a dispatcher guard that REJECTS `--chain {mode} --run-date {date}` loudly when the run would mix date-agnostic and date-windowed steps into one incoherent artifact. Deliver this as a PROPOSAL to CTO -- CTO ratifies before any implementation.
    </item>
  </scope>

  <scope_guard>
    TACTICAL ONLY. This TO is step-aware dispatch wiring + a reject-incoherent-combination guard. It does NOT make the date-agnostic pulls themselves date-windowed -- that systemic change (making the full-history pulls incremental/append-only) is ADVI_TXNAMG PRD section-7-Q5 scope (Andrew append-only ingestion directive), CTO-authored as an addendum and reconciled with ADVI_INFINC. Do NOT let this TO drift into ADVI_INFINC / append-only ingestion work. If the fix appears to require changing what a pull script consumes, STOP and surface to COO + CTO -- that is the section-7-Q5 boundary.
  </scope_guard>

  <acceptance_criteria>
    <ac id="AC1">Deliverable (ii) reported FAST (~1h): a clear empirical YES/NO on whether a plain --chain full (no --run-date) is clean, with evidence (the daily-cron-chain code path / runner log / failing step if any).</ac>
    <ac id="AC2">Deliverable (i): the date-agnostic vs date-capable step enumeration of INF_API_PULL_* (and any other --run-date-touched steps), with the basis for each classification.</ac>
    <ac id="AC3">Deliverable (iii): the step-aware dispatch fix PROPOSAL -- per-step date-parameterization declaration + dispatcher passes --run-date only to declared-date-capable steps + reject-incoherent-combination guard -- delivered to CTO for ratification. No code shipped pre-ratification.</ac>
    <ac id="AC4">Scope guard honored -- no change to what a pull script consumes; no drift into ADVI_INFINC / append-only work.</ac>
    <ac id="AC5">No emoji in any code, log, or diagnostic output.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 (before any diagnostic dispatch): confirm the EC2 runner has the current orion-gold-dispatch.sh + catalog -- ./infra/aws/ec2/verify-ec2.sh (CLAUDE.md Rule 11). Phase 2 (status reads): use runner telemetry s3://{pipeline_bucket}/telemetry/{service}/status.json per reference_opal_runner_shared_telemetry.md, NOT raw CloudWatch/SSM. Phase 3: if (iii)'s proposal later becomes an implementation TO, that is a separate gated step with its own compiler mandate -- NOT this TO.</compiler_tools_mandate>

  <cross_domain_coordination>
    INFGRO / chain #30: deliverable (ii) is the gate. INFGRO.005 itself does NOT wait on this -- DE 0.4 is closing INFGRO.005 AC1/AC7 off AE 0.6.1's in-flight incremental leaderboard.json (COO accepted that path 2026-05-15). An on-demand mode=full ("chain #30") may therefore be unnecessary for .005; coordinate with DE 0.4 on whether an on-demand plain --chain full is still actually needed (for INFGRO.006 / pipeline health) before running one -- do not run a 70min full chain that nothing needs. If it IS needed and (ii) is YES, AE 0.7.0 owns the run, coordinated with DE 0.4 on timing.
    AE 0.7.0 capacity: the other AE 0.7.0 TO (ADVI_TXNAMG.004) is dispatch_held on ADVI_TXNAMG.003 -- no contention.
    INFETL / aggregator: the catalog + aggregator dispatch are ADVI_INFETL domain. AE 0.6.1 holds the deepest aggregator-quorum + catalog context -- MCP them if the catalog mechanics are unclear; do not guess.
    section-7-Q5 boundary: see scope_guard. CTO owns the systemic append-only addendum; this TO must not cross into it.
  </cross_domain_coordination>

  <deliverables>
    <item>Deliverable (ii) FAST report -- MCP to COO + CC CTO + CC DE 0.4: plain --chain full clean? YES/NO + evidence.</item>
    <item>Deliverable (i) date-agnostic vs date-capable step enumeration.</item>
    <item>Deliverable (iii) step-aware dispatch fix proposal to CTO for ratification.</item>
    <item>An on-demand plain --chain full run ONLY if DE 0.4 confirms it is still needed -- coordinated.</item>
    <item>Session log with Compiler Tools section + RAVC2 to COO + CC CTO.</item>
  </deliverables>

  <ravc>AE 0.7.0 RAVC2 to COO + CC CTO on AC1-5. Deliverable (ii) is reported FAST ahead of the full RAVC2 (its own quick MCP to COO + CTO + DE 0.4). The (iii) proposal closes on CTO ratification, not on this TO -- this TO delivers the proposal; CTO rules; an implementation TO (if needed) is separate.</ravc>

  <notes>
    CTO frame, verbatim basis: "--run-date is a step-scoped date parameter ... passing --run-date to a date-agnostic step is a category error ... the catalog DECLARES per-step date-parameterization, the dispatcher passes --run-date only to steps that declare they consume it ... the dispatcher should REJECT [a mixed-date] combination loud, not silently produce it." Keep the TO tactical -- the systemic fix (date-windowing the pulls) is section-7-Q5. Report (ii) FIRST: it is the fast INFGRO / chain #30 unblock decision and is an inspection, not a 70min run.
  </notes>
</task_order>
