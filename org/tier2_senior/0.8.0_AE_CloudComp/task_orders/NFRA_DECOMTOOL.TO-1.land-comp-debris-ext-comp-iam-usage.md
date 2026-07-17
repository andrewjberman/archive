<task_order>
<to_id>NFRA_DECOMTOOL.TO-1</to_id>
<title>Land base-0.8.0's two arch-ratified decommission-identification tools: comp-debris-ext + comp-iam-usage (org/modules/graph, ANY_EXEC) with CTO's hard carry-requirements</title>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.8.0_AE_CloudComp~B</issued_to>
<!-- STAFFING (COO 2026-07-17 ~2238Z): ~B assigned as fill-in during its CTO-gated taxonomy idle window
     (DC-5 CLOSED, W1 lints HELD on CTO enforce-flip). base-0.8.0 built+live-validated these (Andrew-reserved
     research lane, LD-0305 — NOT a builder); ~D is loaded on KUZUSPLIT P1 + COMPSIMILAR (do not pull). -->
<date>2026-07-17</date>
<status>pending</status>
<!-- GO LIVE 2026-07-17 ~2238Z (COO), ~B ACK'd + STARTING @223947Z. Arch RATIFIED by CTO (msg to base 0.8.0
     ~2231xZ). NON-URGENT: advisory/hold-aware decommission-identification tools, no time-sensitive trigger. -->
<priority>P3 (OPAL_CONSOLIDATION cleanup). NON-URGENT — queue BEHIND the live wave (KUZUSPLIT P1 / COMPSIMILAR / freshness-teardown / TAXSMA WS-1) and behind any taxonomy reactivation.</priority>

<authority>
Andrew-direct handoff via base-0.8.0's decommission-tooling research (DECOMMISSION_TOOLING_ASSESSMENT_20260717.md
@890e66375). CTO ARCH-RATIFIED both packages (msg to base 0.8.0 ~2231xZ; details there). base built + live-validated
them; CTO routed the landing to COO for a build lane. This TO formalizes the durable acceptance criteria ~B requested.
</authority>

<gate>
Arch-gate CLEARED — CTO arch-ratified both tools. NON-URGENT standing condition (COO): this is fill-in work for
~B's CTO-gated taxonomy idle window. PIVOT RULE (~B ACK'd): if a taxonomy reactivation trigger lands mid-build
(CTO's enforce-flip word, or a W2/W3 ruling reactivating a DC-lint build), taxonomy takes PRECEDENCE and this
landing pivots to 1.0.0_SA_CTO as fallback owner (CTO's standing offer). Surface the pivot explicitly, never silently.
</gate>

<scope>
Land TWO build-ready, arch-ratified tools at org/modules/graph (ANY_EXEC lane):
  1. comp-debris-ext — the comp-debris extension (per-type activity adapters / decommission-debris identification).
  2. comp-iam-usage — the access-side usage signal extending comp-iam.
Pull the package internals from base-0.8.0's deliverables (org/tier2_senior/0.8.0_AE_CloudComp/deliverables/:
DECOMMISSION_TOOLING_ASSESSMENT + the comp-debris-ext / comp-iam-usage design docs) + CTO's ~2231xZ arch-ratification.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Read base's deliverables + CTO's ~2231xZ arch-ratification; comp-which "how do I register a new comp tool" to reconfirm the NFRA_COMPCLOSE registration surface (tools_index + curated comp-which rule + routing-test + comp-manifest-check).</run>
      <expect>Registration surface confirmed; both tools' design + CTO's hard carry-requirements understood before writing.</expect>
      <if_mismatch>STOP — do not land a comp-* executable that will fail comp-manifest-check's registration invariant.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-manifest-check (registration invariant) + comp-which routing-test on BOTH new executables.</run>
      <expect>PASS on both: each comp-* executable is registered-or-excluded; comp-which routes to each. A commit is BLOCKED otherwise.</expect>
      <if_mismatch>STOP — register (tools_index + curated comp-which rule) before commit.</if_mismatch>
    </step>
    <step>
      <run>comp-debris-ext: EXERCISE it against a KNOWN-HEALTHY T-1 pipeline (a weekend/holiday-adjacent reading) — the false-outage mutant test.</run>
      <expect>The healthy T-1 pipeline is NOT flagged as dead/debris. Proves lib/trading_calendar + cadence-aware windowing are folded (NEVER#1).</expect>
      <if_mismatch>STOP — a debris tool that false-flags a healthy T-1 pipeline is the false-outage hazard; do not land it.</if_mismatch>
    </step>
    <step>
      <run>comp-iam-usage: name in the log how each of comp-iam's 3 named 22a limits is FIXED-or-CARRIED — (a) (action,resource) blindness, (b) 2+-ARN implicitDeny poisoning, (c) Condition-block false-deny. If carried (not fixed), the tool must SAY SO in its own output, never inherit silently.</run>
      <expect>Each of the 3 limits explicitly handled; if the tool leans on simulate-principal-policy, ONE --resource-arns per call + a SEPARATE positive control.</expect>
      <if_mismatch>STOP — a comp-iam derivative that silently inherits comp-iam's fails-GREEN modes is worse than no tool.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
comp-debris-ext ties directly to ~B's own comp-debris metric-adapter prototype work (base 0.8.0 lane) — reconcile so
there is ONE comp-debris family, not a fork. ALERT-SUSPENSION (Andrew-direct, standing): the Access Analyzer enable
that comp-iam-usage's design references is HELD — do NOT enable it, and add no SES/SNS/CloudWatch leg. These are
READ/scan advisory tools (never-delete, hold-aware) — clear of the suspension otherwise. Disposal stays OPAL_LCLRPO
(no second disposal path). Feeds the NFRA_COMPSIMILAR decommission column (the overlap/superseded axis).
</cross_domain_coordination>

<acceptance_criteria>
1. Both comp-debris-ext + comp-iam-usage LANDED at org/modules/graph + REGISTERED: comp-manifest-check PASS + comp-which
   routing-test resolves each (machine-checkable — the registration invariant blocks commit otherwise).
2. comp-debris-ext false-outage mutant test PASSES: a known-healthy T-1 pipeline (weekend/holiday-adjacent) is NOT
   flagged as debris — evidencing the lib/trading_calendar + cadence-aware windowing fold (NEVER#1).
3. comp-iam-usage: each of comp-iam's 3 named 22a limits explicitly FIXED-or-CARRIED and NAMED in the log/tool output —
   never silently inherited.
4. Access Analyzer NOT enabled (alert-suspension); no new SES/SNS/CloudWatch leg.
5. Session log Compiler Tools section reproduces each mandate run + observed vs expect. Ping COO + CTO at landing with
   the registration-invariant PASS evidence.
</acceptance_criteria>

<references>
  <ref type="assessment">org/tier2_senior/0.8.0_AE_CloudComp/deliverables/DECOMMISSION_TOOLING_ASSESSMENT_20260717.md</ref>
  <ref type="andrew-direct">org/tier2_senior/0.8.0_AE_CloudComp/deliverables/ANDREW_DIRECT_20260717_compiam-heat-decommission.md</ref>
  <ref type="sibling-project">org/projects/NFRA_COMPSIMILAR.json (the decommission-doctrine sibling)</ref>
  <ref type="registration">NFRA_COMPCLOSE registration invariant (comp-manifest-check)</ref>
</references>
</task_order>
