# TO MDPF_REMED.RP-W2 — CROSS-FIRM UNLINK: sever the FRONTIER, keep the CALENDAR

<task_order id="MDPF_REMED.RP-W2" project="MDPF_REMED">
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-10T23:4xZ</issued>
<status>staged</status>
<priority>P0 — with or after RP-W1. Same file, same owner; do not let it land BEFORE RP-W1.</priority>

<references>
  <ref type="plan">org/tier1_exec/1.0.0_SA_CTO/deliverables/MDPF_REMEDIATION_PLAN_20260810.md @dbbbfa9cd3 (W2, D-1)</ref>
  <ref type="evidence">org/projects/MDPF_PIPELINE_TRUTH.json @5ba751ed88</ref>
</references>

## NAMING NOTE
RP-Wn = §2 workstreams of MDPF_REMEDIATION_PLAN_20260810; distinct from the earlier MDPF_REMED.W1-x
register wave. (RP-W2 is unrelated to MDPF_REMED.W2-1 consumer census.)

## SCOPE — SMALLER THAN IT LOOKS. DO NOT SCOPE A REWRITE.
The fix is two lines: `:2682-2683` of `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py`
hands 49F's `dates` to `build_inflection_artifact`. `_model_leg_eclipse` (`:885`, dispatch `:932`)
ALREADY self-derives when passed `axis=None`, and cottonwood's `self_derived_axis` is the ratified
pattern. Follow the pattern; do not build a new mechanism.

## THE SEMANTIC RULING — carried verbatim because it decides the shape (Andrew asked for it explicitly)
The **CALENDAR** is legitimately shared — `canonical_trading_axis()` → `lib/_trading_day_calendar`,
NYSE days, a LIBRARY not a firm. **The FRONTIER is the violation** — read live from 49F's own vendor
data, so 49F's CONTENT decides where inflection's series ends. **Each firm derives its OWN frontier
from its OWN legs, then feeds the SAME canonical calendar.** Canonical shape kept; data link severed.
⛔ An executor who "removes the shared axis" wholesale BREAKS THE CALENDAR. If your diff touches
`canonical_trading_axis` or `lib/_trading_day_calendar`, you have left scope — STOP and surface.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-find "build_inflection_artifact" data/mdpf</run>
      <expect>Call site at/near :2682-2683 receiving a 49F-derived `dates`; DEF elsewhere in the same file. Denominator printed.</expect>
      <if_mismatch>STOP. If the call site moved or multiplied since @dbbbfa9cd3, re-ground the two-line claim before editing; surface a changed premise to COO.</if_mismatch>
    </step>
    <step>
      <run>comp-blast build_inflection_artifact (fall back: comp-pydeps consumers build_inflection_artifact if the kuzu node is code-plane-only)</run>
      <expect>Consumers limited to the mdpf gold chain / consolidated build. No consumer outside dim_mdpf_aggregate_aua_timeseries.py's own flow.</expect>
      <if_mismatch>STOP. Document the new consumer and message its owning agent before writing.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-validate dim_mdpf_aggregate_aua_timeseries --artifact &lt;standalone --firm inflection QA build output&gt;</run>
      <expect>PASS/WAIVED; NO_CONFIG = UNVALIDATED, surface it.</expect>
      <if_mismatch>STOP until ERROR clean.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>comp-pipescript deployed dim_mdpf_aggregate_aua_timeseries.py</run>
      <expect>MATCH after your deploy leg.</expect>
      <if_mismatch>Finish the deploy leg or surface — committed-but-not-deployed is the defect class of record.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Same file as RP-W1, same owner. RP-W1 lands first or same commit series. No other agent edits this
file during your window (checked: no other active TO touches it).
</cross_domain_coordination>

<acceptance_criteria>
EXERCISED, not asserted (Rule 22a):
1. A standalone `--firm inflection` build produces the SAME axis as the consolidated one (show both
   axis frontiers side by side).
2. **NO READ OF `smartx/**` OCCURS IN AN INFLECTION BUILD** — exercised: run the inflection build
   with read-tracing (or an instrumented S3 client / access log read) and show zero smartx keys
   touched. A grep of the code is NOT acceptance; the exercise is.
3. Each firm's frontier derives from its OWN legs (show inflection's frontier moving independently of
   a 49F content change, or the equivalent decisive read).
4. Session log Compiler Tools section reproduces every &lt;run&gt; with observed output + pass/fail
   vs &lt;expect&gt;. Missing rows = REWORK.
</acceptance_criteria>
</task_order>
