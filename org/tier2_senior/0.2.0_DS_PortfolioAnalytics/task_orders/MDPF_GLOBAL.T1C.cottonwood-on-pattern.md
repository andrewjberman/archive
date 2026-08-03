<task_order>
<to_id>MDPF_GLOBAL.T1C.cottonwood-on-pattern</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
<date>2026-08-03</date>
<status>staged</status>
<priority>P1 (second wave on the s.C.4 spine; unblocked by the T2.B ruling @440d16e018; you hold the freshest chain mechanism context from your T2.A close)</priority>

<title>T1.C: Cottonwood on-pattern -- restructure the cottonwood MDPF leg to the canonical revamp chain pattern (49F/inflection parity)</title>

<context>
MDPF_GLOBAL PRD Addendum C s.C.4 T1.C row, unblocked 2026-08-03 20:59Z by the CTO T2.B ruling
@440d16e018 (full text PRD s.C.3). The ruling's terms bind this TO:
(1) canonical serving lineage = revamp/hyphen family (opal-data-assets silver -> revamp gold ->
    accrual bridge -> publisher -> platinum/mdpf/{scope}/);
(2) canonical frontier = T-1 settled close, declared in served _provenance;
(3) freeze fix = dedicated daily schedule on the PRODUCING tree (revamp rebuild) timed after T-1
    silver close; INF event demoted to accelerator-only (T2.C implements the clock);
(4) underscore plane + runner chain retire at T5 conditional on a delta census.

YOUR T2.A DIAGNOSIS IS THE MAP: you source-confirmed the accrual chain as an ungated
content-derived copy whose global axis rides the 49F frontier. T1.C brings the COTTONWOOD leg to
the same pattern as 49F/inflection under that canonical chain: dedicated schedule, same rules,
same timing, same manifest/provenance emission.

FIRM SEPARATION BINDS (CLAUDE.md NEVER#2 + Rule 13): cot is a COMPLETELY separate firm pipeline
from bd -- gate-blocked at commit + IAM Deny at runtime. Nothing in this restructure references
another firm's bucket from the cot tree; the MDPF aggregation layer consumes cot outputs at the
opal-data-assets/platinum boundary per the canonical lineage, exactly as it does 49F/inflection.

SEQUENCING NUANCE: your parity work (route shape, rules, feeder/gold restructure, provenance
emission) starts NOW. The SCHEDULE leg's timing values come from T2.C's declared clock
(0.7.0_AE_CloudOps, queued behind their T1.A) -- coordinate by MCP when their clock declaration
lands; do not invent a cadence window locally. Acceptance's 3-consecutive-cycle evidence
necessarily follows the schedule being live.
</context>

<scope>
1. Ground the current cottonwood MDPF leg: how it is triggered/produced today vs the 49F/inflection
   pattern under the canonical revamp chain -- enumerate every parity gap (schedule presence,
   cadence window, route shape, manifest/provenance emission, rules).
2. Build the pattern-parity checklist (the acceptance instrument): one row per pattern element,
   graded green/red vs 49F/inflection, each row evidence-cited.
3. Implement the restructure on the DS-owned surfaces (feeder/gold code, provenance emission).
   Schedule/trigger infra legs: coordinate with 0.7.0_AE_CloudOps (T2.C owner) -- their clock, your
   consumer; any Terraform-side change routes to the AE lane, not yours.
4. Evidence: cottonwood served artifacts advance to frontier on 3 consecutive SCHEDULED cycles
   (scheduled-run evidence only; no hand-runs in the evidence window).
5. DS deploy discipline binds: gold/silver edits via .tools/commit-gate.sh + safe-deploy per
   Rule 13/14; from __future__ import annotations on every touched script (Rule 15); silver stays
   dedup+dtype only (Rule 17) if any silver surface is touched.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-estate mdpf ; comp-estate cottonwood (or the cot vertical comp-estate --list names)</run>
      <expect>Both chains rendered for mdpf; cot leg's current production path enumerated -- seeds the parity-gap list. Note the known rendering gap (accrual family as C0 fact, not a chain block -- your own T2.A finding).</expect>
      <if_mismatch>STOP. If the estate map contradicts the T2.B canonical lineage, surface to CTO before restructuring anything.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io --pipeline mdpf on every feeder/gold script you will touch (your T2.A note: the --pipeline flag is required post-07-30-hardening; dispatch-staged writes are extractor-invisible)</run>
      <expect>READS/WRITES per script; column gaps + portal consumers enumerated; extractor-invisible writes cross-checked by hand against mdpf-daily-dispatch.sh staging.</expect>
      <if_mismatch>STOP. An unmapped write surface before a restructure is how silent consumers break.</if_mismatch>
    </step>
    <step>
      <run>comp-blast on every touched fn</run>
      <expect>Downstream consumers enumerated; HOLD claims read if any fire.</expect>
      <if_mismatch>STOP. Message the owning agent of any unexpected consumer before writing.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>re-run comp-blast on touched fns + comp-surface-check by hand (MP surfaces = must-always-be-right)</run>
      <expect>No new consumers appeared mid-write; surface-check output READ, not inferred from silence; any SEV1 = STOP.</expect>
      <if_mismatch>STOP on SEV1; surface to COO+CTO.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>scheduled-run evidence collection: 3 consecutive scheduled cycles, timestamps read live vs lib/trading_calendar.py frontier</run>
      <expect>Cottonwood served artifacts at expected frontier all 3 cycles; parity checklist all-green; zero hand-runs in the window.</expect>
      <if_mismatch>A red cycle = diagnose before the clock restarts; report the mechanism, not just the miss.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <no_reprocess_needed>Restructure targets the production PATTERN (trigger/schedule/emission), not
  historical content. If the restructure changes any emitted artifact SHAPE for past dates, STOP
  and surface to COO -- that widens this into a reprocess TO and needs an explicit scope amendment.
  </no_reprocess_needed>
</data_reprocess_scope>

<cross_domain_coordination>
SHARED SPINE with T2.C (0.7.0_AE_CloudOps): their declared clock is your schedule's timing source
-- MCP-coordinate before any schedule value lands anywhere; neither seat invents the window alone.
Firm-separation gates bind on every cot-tree path. The accrual/publisher chain surfaces carry the
T2.A-era HOLDs -- producer edits only within this TO's enumerated scope, nothing opportunistic.
T1.A (same AE base seat) is censusing triggers concurrently -- if your restructure plan needs a
trigger created/modified, that lands AFTER their census commits (they need a stable baseline) and
via the AE lane.
</cross_domain_coordination>

<acceptance_criteria>
Verbatim s.C.4 (CTO validates at close):
1. Pattern-parity checklist all-green vs 49F/inflection (schedule present, same cadence window,
   same route shape, same manifest/provenance emission).
2. Cottonwood served artifacts advance to frontier on 3 consecutive scheduled cycles.
Plus standing norms: scheduled-run evidence only; every causal claim cites file:line @ commit or
is labeled INFERRED; no new alarms/monitors.
Plus: session log includes a Compiler Tools section reproducing every <run> from
<compiler_tools_mandate> with observed output and explicit pass/fail vs <expect>. Missing rows =
REWORK, not COMPLETE.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/MDPF_GLOBAL_PRD.md (s.C.3 T2.B ruling @440d16e018 + s.C.4 T1.C row)</ref>
  <ref type="evidence">Your T2.A diagnosis @0b5acf3148 (the chain mechanism map)</ref>
  <ref type="go">Andrew-direct GO @3e2b23ebb3; CTO T2.B ruling msg 20260803T205937Z</ref>
</references>

<dependencies>
  <dependency agent="1.0.0_SA_CTO" task="T2.B producer-unification ruling" status="complete"/>
  <dependency agent="0.7.0_AE_CloudOps" task="MDPF_GLOBAL.T2C declared clock (timing values only -- parity work starts now)" status="pending"/>
</dependencies>
</task_order>
