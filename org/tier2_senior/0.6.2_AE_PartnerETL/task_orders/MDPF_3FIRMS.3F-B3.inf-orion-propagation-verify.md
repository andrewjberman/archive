<task_order>
<id>MDPF_3FIRMS.3F-B3</id>
<title>INF/Orion bronze leg — verify the repaired 07-11..07-15 propagates to monolith bronze+silver on the SCHEDULED pass, faithfully</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-B (Bronze)</workstream>
<issued_to>0.6.2_AE_PartnerETL~A</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-22T20:19Z</issued_at>
<status>staged</status>
<authorization>LD-0333 amendment 1 @2eef569d2 (Andrew cascade GO) -> CTO cascade 200805Z -> COO decomposition. Andrew confirmed direct at the COO terminal 20:16Z (@f526334e0).</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_3FIRMS_PRD.md</ref>
  <ref type="prd_section">§2.2 six-leg table (INF-AUA row); §4 WS-B table row 3F-B3; §8 constraints</ref>
  <ref type="ledger">org/tier0/ledger/LD-0333.md (+ amendment 1 @2eef569d2)</ref>
  <ref type="andrew_direct">org/tier1_exec/2.0.0_SA_COO/andrew_direct_20260722T2016Z_backfill_hold_is_cottonwood_only_inflection_july_in_scope.md @f526334e0</ref>
  <ref type="prior_work">your own @b47d2ff10 — orion source repair 5/5, root cause "raw producer died after 07-10", roster bug in _hh_universe latest_hh_rep_map_key</ref>
</references>

<scope>
Verify that the SCHEDULED mirror pass (~14:15Z) and orion silver sweep (16:00Z) propagate the
already-repaired raw 07-11..07-15 Orion assets into monolith bronze AND silver, faithfully.

**THIS IS A VERIFICATION TO, NOT A REPAIR TO.** The source repair is already done and proven (yours,
@b47d2ff10: raw .jsonl.gz present in opal-data-inf for 07-11..07-15 with as-of rosters
318/318/318/319/319; faithfulness proven against the same-day 07-16 capture). What is NOT yet done is
PROPAGATION into the monolith — today's mirror pass preceded the repair.

**NO HAND-FIRES.** Validate on the artifacts the scheduled pass emits. Do not invoke the mirror, the
sweep, or any gold run to make this verifiable sooner (CLAUDE.md NEVER#4 + the no-ad-hoc-gold-runs law).
If the scheduled pass has not yet run when you pick this up, the correct state is BLOCKED-ON-SCHEDULE
and you report that — a scheduled gate is not slippage.
</scope>

<andrew_direct_context priority="HIGH" carrier_ruling="PENDING CTO">
**Andrew-direct 2026-07-22 ~20:16Z, VERBATIM — recorded @f526334e0. He named YOU.**

> "the backfill is just a hold for Cottonwood, there is some backfill and verification that needs to be
> done for Inflection with 0.6.2 because some numbers are very contentious there. Like I saw a jump on
> july 6 that dropped july 7 then came back on july 10 or a little later jumped back up again; that is
> just questionable and to me smells like changing methodology, so that is something I want addressed
> and validated, potentially repulling July for Inflection."

**READ THIS CAREFULLY — three separations that matter:**
1. **The backfill developing-subject hold is COTTONWOOD-ONLY.** Inflection backfill/verification is
   affirmatively IN SCOPE and wanted.
2. **"smells like changing methodology" is ANDREW'S HYPOTHESIS, not a finding.** Rule 22: it cannot
   authorize a fix until source-confirmed. Test it; do not assume it.
3. **"POTENTIALLY repulling July" — the word is POTENTIALLY. A repull is NOT ordered here.** It is
   downstream of the validation and is not authorized by this TO.

**WHICH TO CARRIES THE 07-06/07-07/07-10 ANOMALY INVESTIGATION IS A PENDING CTO RULING** (candidates:
this TO amended, 3F-B4, or 3F-G7's spike census). It is surfaced to CTO and NOT yet assigned. Do not
self-assign it. **But note your existing acceptance below already requires a July gap census — if that
census surfaces anything at 07-06/07-07/07-10, report it and STOP; do not expand scope on your own.**

⚠ **A TRAP THE PRD NAMES EXPLICITLY (RF-11):** a partial root cause for these exact dates is already
banked — the LEGACY served date axis carries market-closed days and omits real trading days (07-06
corrected to 122,866,034/474). **That is a DIFFERENT MECHANISM than Andrew's methodology-change
suspicion, and it must NOT be used to wave his off.** The PRD's own words: "residual spikes need a
census, not assumed covered." A found class root cause is the most seductive way to close a still-open
case.
</andrew_direct_context>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-freshness</run>
      <expect>The orion/inflection downstream artifacts resolve on the TRADING-DAY frontier (freshness_basis: trading-day-frontier). Entry present for the leg.</expect>
      <if_mismatch>If the entry lacks freshness_basis: trading-day-frontier it silently falls back to flat-hours and WILL false-alarm. Record the gap, do NOT treat a flat-hours FAIL as a staleness finding (NEVER#1). Surface to COO.</if_mismatch>
    </step>
    <step>
      <run># rail-checked: EventBridge applied-truth is not modeled by any comp tool
aws events describe-rule --name opal-assets-ingest-mirror-inf-daily</run>
      <expect>State ENABLED; ScheduleExpression cron(15 14 * * ? *). Cite verbatim.</expect>
      <if_mismatch>STOP. A DISABLED or re-scheduled mirror changes the entire propagation premise. Report to COO before proceeding.</if_mismatch>
    </step>
    <step>
      <run>aws s3api list-objects-v2 --bucket opal-data-inf --prefix &lt;orion assets raw prefix&gt; --query 'Contents[].{K:Key,S:Size,T:LastModified}'</run>
      <expect>07-11..07-15 raw objects PRESENT with explicit-Z timestamps and the byte sizes you verified at @b47d2ff10.</expect>
      <if_mismatch>STOP — the source repair is the premise of this TO. NEVER use bare `aws s3 ls` for a load-bearing timestamp (it prints LOCAL time with no TZ marker; 5 hits / 4 agents).</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>aws s3api list-objects-v2 --bucket opal-data-assets --prefix orion/inflection/silver/fact_assets/ --query 'Contents[].Key'</run>
      <expect>Partitions date=2026-07-11 .. date=2026-07-15 PRESENT after the scheduled sweep.</expect>
      <if_mismatch>If the scheduled pass has not yet run: report BLOCKED-ON-SCHEDULE with the next fire time. Do NOT hand-fire. If it ran and the partitions are absent: that is a propagation DEFECT — report LOUD to COO + CTO, do not repair unilaterally.</if_mismatch>
    </step>
    <step>
      <run>Row-count comparison: monolith silver fact_assets 07-11..07-15 vs opal-data-inf source</run>
      <expect>EXACTLY 34,935 / 34,935 / 34,935 / 34,942 / 34,942 (PRD §4 3F-B3 acceptance).</expect>
      <if_mismatch>STOP. A row-count divergence is a faithfulness failure, not a rounding issue. Report the per-date delta with both denominators printed.</if_mismatch>
    </step>
    <step>
      <run>July mid-series gap census over orion/inflection/silver/fact_assets/ — enumerate expected trading days from lib/trading_calendar.py, diff against present partitions, PRINT THE DENOMINATOR</run>
      <expect>Gap census = 0 over July. The expected-day set is derived from the trading calendar, never from wall-clock.</expect>
      <if_mismatch>Report every missing date with the denominator ("N of M expected trading days present"). If a gap lands on 07-06 / 07-07 / 07-10, flag it explicitly to COO and STOP — that is Andrew's window and its carrier is a pending CTO ruling.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Re-run the partition census with denominators printed</run>
      <expect>Same counts as Phase 2 — no drift during the write window.</expect>
      <if_mismatch>Surface to COO; likely another producer wrote mid-flight.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <no_reprocess_needed>This TO patches NO script. It verifies that an already-repaired SOURCE
  propagates through EXISTING scheduled machinery. No converter logic changes, so there is no
  historical-partition reprocess question. If propagation FAILS, the fix is a separate TO with its own
  reprocess scope — not an in-flight expansion of this one.</no_reprocess_needed>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="opal-data-assets/orion/inflection/silver/fact_assets/" shared_with="0.4.0_DS_ClientPlatform (3F-S2 silver completeness census)">
    DS's 3F-S2 runs a silver partition census over the same table. MCP DS before committing any census
    artifact so the two denominators are reconciled rather than published in conflict.
  </resource>
  <resource path="gold spike census" shared_with="0.4.0_DS_ClientPlatform (3F-G7)">
    3F-G7 enumerates day-over-day moves >=5% on the staged trends. Your July gap census is an INPUT to
    it. Do not perform G7's work; hand it the census.
  </resource>
</cross_domain_coordination>

<dependencies>
  <dependency type="schedule" name="opal-assets-ingest-mirror-inf-daily ~14:15Z + orion silver sweep 16:00Z" status="pending">
    A scheduled gate, not slippage. BLOCKED-ON-SCHEDULE is a valid and expected interim report.
  </dependency>
</dependencies>

<acceptance_criteria>
1. Monolith silver `fact_assets` carries partitions 07-11..07-15 with row counts EXACTLY
   34,935 / 34,935 / 34,935 / 34,942 / 34,942, evidenced by `s3api` output with explicit-Z timestamps.
2. July mid-series gap census = 0, with the DENOMINATOR PRINTED (N of M expected trading days, expected
   set derived from `lib/trading_calendar.py`).
3. Propagation is evidenced on SCHEDULED-pass artifacts only. Any hand-fire invalidates the TO.
4. The EventBridge mirror rule is cited verbatim (name + state + cron) as applied truth.
5. **Session log includes a Compiler Tools section reproducing EVERY `<run>` above with observed output
   and an explicit pass/fail against its `<expect>`. Missing rows = REWORK, not COMPLETE.**
6. Any observation touching 07-06 / 07-07 / 07-10 is reported to COO and NOT acted on — carrier pending
   CTO ruling.
</acceptance_criteria>

<escalation>
Report to 2.0.0_SA_COO. A propagation failure, a row-count divergence, or anything landing in Andrew's
07-06/07-07/07-10 window is escalated LOUD and immediately — do not batch it to a session log.
</escalation>
</task_order>
