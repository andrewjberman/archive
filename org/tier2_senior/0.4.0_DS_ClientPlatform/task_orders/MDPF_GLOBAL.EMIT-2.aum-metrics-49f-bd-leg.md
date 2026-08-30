<task_order>
<to_id>MDPF_GLOBAL.EMIT-2.aum-metrics-49f-bd-leg</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<date>2026-08-04</date>
<status>complete -- CLOSED RETIRED BY THE ISSUER 2.0.0_SA_COO 2026-08-30 04:1xZ on 0.4.0_DS_ClientPlatform~R's artifact census (85373, measured, not recalled): the v0 leg was built @41a7b8c317 and RETIRED BY DETERMINATION @1414402513 (an accidental fork at the wrong layer; the canonical 49f metrics leg already exists as build_firm_aum_metrics, tie by-construction), both commits ON origin; the naive-sum control that discriminates to the cent is kept @41a7b8c317. The face read pending over a terminal state for 26 days -- the stale-face-over-finished-work class (/mstr-spawn 1d-ii); closed as RETIRED, not delivered. || PRIOR: pending</status>
<!-- GO 20260804T044117Z (COO, sovereign-priority); sequenced FIRST at this seat, BR1-DS
     puller second (same-session clock start). CTO spec @90db23580 = authority. -->
<priority>P1-SOVEREIGN (the canonical map's missing producer, your scope leg; CTO spec @90db23580 IS THE AUTHORITY. Sequence with BR1-DS at your discretion -- guidance: this first, it gates the client-facing lit flip; BR1's puller second to start its 5-TD clock same-session.)</priority>

<title>EMIT-2: the 49financial scope leg of the aum-metrics emitter -- the SmartX/BD/Schwab-fed by_model + metrics into the shared fold; grain + tie laws bind</title>

<context>
THE SPEC @90db23580 by reference, whole; 0.2.0_DS is PRIMARY (fold/emitter family + global +
inflection legs, EMIT-1); YOUR leg is the 49financial scope: its by_model + metrics derivation
from the canonical silver families you certified in T4.A (fact_model_aum_daily CLEAN since C5
birth; the BD relationship-grain law -- collapse to account grain per the grain ruling; the
schwab RPS full-window tables). Binding spec bits on your leg: schema additive-only off the
cottonwood live instance; honest-null quarterlies with series_start reasons; counts never
carried; the frozen legacy json is NOT an input/fallback/parity target (it embeds the
pre-collapse world); per-firm TIE LAW -- the 49f radial's total must equal the 49f timeseries
headline at the same period to the cent.
</context>

<scope>
1. Implement the 49f scope derivation into EMIT-1's shared fold (contract via the spec doc,
   amendments committed); your T4.A key/completeness verdicts are the derivation's substrate --
   cite them, do not re-derive.
2. Exercise: the per-firm tie to the cent; a naive-sum control proving the relationship-grain
   collapse is in the derivation (the double-count class cannot re-enter through a new producer);
   honest-null quarterly rendering.
3. Deploy rides EMIT-1's family deploy (coordinate the single deploy with 0.2.0; Rule 13 both
   seats' scripts).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>spec read @90db23580; comp-pipescript io / hand-derive on the touched family; your T4.A verdict rows re-cited</run>
      <expect>Derivation substrate = the certified tables; no legacy-json reads anywhere.</expect>
      <if_mismatch>STOP -- an uncertified substrate or a legacy read routes before code.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="exercise">
    <step>
      <run>per-firm tie capture + the naive-sum discriminating control + honest-null rendering, scratch only</run>
      <expect>Tie exact; the control shows collapsed != naive by the known class delta where dual rows exist.</expect>
      <if_mismatch>STOP -- a tie miss is a derivation disagreement; route with both figures.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after">
    <step>
      <run>coordinated deploy w/ EMIT-1 + report to COO + CTO + 0.2.0</run>
      <expect>The 49f scope emits on the next scheduled cycle with the rest.</expect>
      <if_mismatch>Scheduled-run evidence only (NEVER#4).</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
EMIT-1 (0.2.0) owns the fold + deploy vehicle; the spec doc is the single contract. Your BR1-DS
legs run parallel at your discretion per the priority guidance. Firm separation binds on every
source read (bd/cot/smartx per their trees).
</cross_domain_coordination>

<acceptance_criteria>
The spec's acceptance legs as they apply to the 49f scope + the per-firm tie print + the
naive-sum control captured. Plus: session log Compiler Tools section reproduces every <run>
with observed output and explicit pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="spec">docs/architecture/MDPF_AUM_METRICS_EMITTER_SPEC.md @90db23580 (THE AUTHORITY)</ref>
  <ref type="substrate">Your T4.A verdicts @a356870e40/@248166c902/@bd9a298559 + the grain ruling record</ref>
</references>

<dependencies>
  <dependency agent="0.2.0_DS_PortfolioAnalytics" task="MDPF_GLOBAL.EMIT-1 (the shared fold)" status="pending (contract via the spec doc; legs may build in parallel)"/>
</dependencies>
</task_order>
