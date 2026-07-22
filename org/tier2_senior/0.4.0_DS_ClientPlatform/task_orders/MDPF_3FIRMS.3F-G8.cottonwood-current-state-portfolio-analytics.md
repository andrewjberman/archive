<task_order>
<id>MDPF_3FIRMS.3F-G8</id>
<title>Cottonwood CURRENT-STATE Portfolio-Analytics pair — account-distribution + aum-metrics at 49F/INF schema parity (Path A)</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-G (Gold) — DEPENDENCY-SCOPED GATE, not the all-legs barrier</workstream>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<advisory>4.0.0_SA_CRO — holds the exact (account, model, size) wiring + the proof notebook. REQUEST THEM; do not re-derive.</advisory>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-22T20:29Z</issued_at>
<status>staged</status>
<authorization>Andrew-direct via CRO 202532Z, VERBATIM: "Make sure that CTO scopes Path A as a build for MDPF_3FIRMS." -> CTO ruling 202722Z -> PRD v1.5 @43128f6cb.</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_3FIRMS_PRD.md v1.5 @43128f6cb, §4 WS-G row 3F-G8</ref>
  <ref type="brief">org/tier1_exec/4.0.0_SA_CRO/briefs/COTTONWOOD_OPERATIONAL_SHAPE_BRAINSTORM_20260722.md</ref>
</references>

<gate priority="READ FIRST">
⚠ **THIS TO'S GATE IS NARROWED AND IT IS A DELIBERATE CTO DECISION — DO NOT APPLY THE ALL-LEGS WS-G
BARRIER HERE.** 3F-G8 starts when **3F-B5 + the 3F-B6 LIVENESS portion + 3F-S3** are green — the
acceptances covering the exact silver this TO reads. It does NOT wait for Orion / Eclipse / Schwab
verification, because it does not read them; chaining it to those serves no dependency.
**The rest of WS-G keeps the all-legs gate unchanged.**
⚠ 3F-S3 is in the gate because **the MDPF runner currently cannot read Cottonwood silver at all**
(RF-10). Without that grant this TO cannot execute regardless of code.
</gate>

<scope>
**Path A — point the EXISTING distribution-producer family at Cottonwood's monolith facts.**
- Producers: `dim_mdpf_account_distribution.py` / `compute_per_firm_account_distribution.py` contract.
- Membership: `fact_model_assignment` + `fact_model_roster`. Size: `fact_holdings` + `fact_allocations`.
  Crosswalk: `fact_model_blend`.
- Emit `json/mdpf/cottonwood/{account-distribution,aum-metrics}.json` at **49F/INF SCHEMA PARITY**.
- Daily holdings count from `fact_holdings` folds in (CRO Path C, trivial).

**WIRE, DO NOT AUTHOR.** Reuse the WS-3 blend decomposition
(`data/assets/scripts/gold/build_dim_model_portfolio.py`) — **never re-derive the satellite->archetypal
decomposition.** Three independent computations already converge to the dollar; a fourth derivation is
a divergence risk, not a check.

**Apply the standing rulings AT THE SLICE:** `Opal - Income` -> non-model residual (the dim as built
07-21/22 predates the ruling and still carries it as an `is_opal` row); sleeves stay
`is_opal=false`-visible; `by_model` keys on the **archetypal ladder post-crosswalk, NEVER raw
`strategyName`**.

⛔ **CURRENT-STATE ONLY. The AUM-tab TIMESERIES is NOT this TO** — it remains inside the Cottonwood
backfill DEVELOPING SUBJECT (Andrew's hold is Cottonwood-scoped and this is the held firm). No history,
no probe dependency.

⚠ **SAME-DAY VINTAGE BINDING (CRO caveat, 200920Z):** the monolith facts are forward-accruing daily
snapshots that exist only from ~07-21. **The distribution's account set MUST tie to the SAME day's
roster partition.** Never assume a longer-lived membership table. This is the TWO-DATES law applied
here: `date=` is the ASSIGNMENT date, `value_date` states what the dollars are as-of. Conflating them
presents Monday's dollars as Wednesday's.

⛔ **DEPLOY-MAP HAZARD, LOAD-BEARING:** these scripts live under `data/assets/` and **MUST NOT move to
`data/cot/scripts/gold/`** — `safe_deploy_core.PIPELINE_MAP` auto-deploys `data/cot` gold on push, which
would publish **past a co-sign gate BY CONSTRUCTION.**
⛔ **NO HARDCODED SERIES START** (§8.1). Cottonwood is mid-migration; the series must extend on its own.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript io dim_mdpf_account_distribution.py (and the compute_* sibling)</run>
      <expect>READS/WRITES enumerated; COLUMN GAPS empty; portal consumers listed.</expect>
      <if_mismatch>Fix the load list before writing. ⚠ KNOWN GAP: `io` misses cross-bucket served imports inside helper functions — read the source too, do not treat a clean manifest as proof of no coupling.</if_mismatch>
    </step>
    <step>
      <run>comp-blast on the distribution producer family</run>
      <expect>Consumers limited to the MDPF page family; no unexpected downstream.</expect>
      <if_mismatch>STOP; MCP the owning agent of any new consumer before writing.</if_mismatch>
    </step>
    <step>
      <run>Request CRO's (account, model, size) wiring + proof notebook</run>
      <expect>Received and used as the join spec.</expect>
      <if_mismatch>Do NOT re-derive the join. CRO proved 296/296 independently; a second derivation is a divergence risk.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/commit-gate.sh on every .py touched</run>
      <expect>py_compile + ds-precommit-check + ruff clean; `from __future__ import annotations` present.</expect>
      <if_mismatch>STOP. Do not commit.</if_mismatch>
    </step>
    <step>
      <run>comp-surface-check (BY HAND — it cannot block)</run>
      <expect>Read the output yourself. `ModelPortfolios` is SEV1 (CRITICAL on model_portfolios.headline + .benchmark).</expect>
      <if_mismatch>⚠ SILENCE IS NOT A PASS and an unblocked commit is NOT a clearance — it is advisory-only and structurally blind to portal/ submodule surfaces.</if_mismatch>
    </step>
    <step>
      <run>comp-validate &lt;script&gt; --artifact &lt;emitted json&gt;</run>
      <expect>PASS or WAIVED.</expect>
      <if_mismatch>⛔ NO_CONFIG or ZERO_CHECKS means UNVALIDATED — never signal SAFE on it. ADVISORY means read the WARNs.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Verify both artifacts appear in the NIGHTLY-EMITTED staged set</run>
      <expect>Present, schema-identical to the 49F/INF equivalents.</expect>
      <if_mismatch>⛔ Do NOT trigger an ad-hoc gold run to validate (NEVER#4) — validate on the scheduled nightly's artifacts.</if_mismatch>
    </step>
    <step>
      <run>comp-blast on the emitted artifacts</run>
      <expect>Same consumer set as Phase 1.</expect>
      <if_mismatch>Surface to COO — another agent likely committed a consumer mid-flight.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <no_reprocess_needed>Current-state only, forward-emitting from first availability (~07-21). No
  historical partition is rewritten and no backfill is performed — the timeseries stays in the
  developing subject. Emission begins from the first date the facts exist, with NO hardcoded start.</no_reprocess_needed>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="build_dim_model_portfolio.py + data/assets placement" shared_with="0.4.0_DS (3F-G3)">
    G3 wires the Cottonwood MDPF slice from the same dim. Same file family — coordinate to avoid two
    edits to one function (the serialization error COO made and DE corrected on 07-22).
  </resource>
  <resource path="runner IAM grant" shared_with="0.7.0_AE_CloudOps (3F-S3)">
    Hard prerequisite. Without the grant this cannot read its inputs.
  </resource>
  <resource path="join spec + proof notebook" shared_with="4.0.0_SA_CRO">
    CRO advisory. Request; do not re-derive.
  </resource>
</cross_domain_coordination>

<dependencies>
  <dependency agent="0.6.2_AE_PartnerETL~A" task="MDPF_3FIRMS.3F-B5" status="staged" blocking="true"/>
  <dependency agent="0.6.2_AE_PartnerETL~A" task="MDPF_3FIRMS.3F-B6 (liveness portion only)" status="staged" blocking="true"/>
  <dependency agent="0.7.0_AE_CloudOps" task="MDPF_3FIRMS.3F-S3" status="staged" blocking="true"/>
</dependencies>

<acceptance_criteria>
1. Both artifacts present in the **nightly-emitted** staged set, **schema-identical** to the 49F/INF
   equivalents (field-by-field comparison committed).
2. **Account bridge 296/296 — LOUD on any drop**, never a silent one.
3. Distribution buckets reconcile to `dim_model_portfolio` membership.
4. **Roster + holdings partitions used are the SAME DATE, asserted per run** (same-day vintage binding).
   Both `date=` (assignment) and `value_date` (dollars as-of) ride the output.
5. `model_aua + non_model_aua == firm total` per day, wired as a per-run check that FAILS LOUD.
6. Rulings applied at the slice: Income -> non-model, archetypal keys (never `strategyName`), sleeves
   visible as `is_opal=false`.
7. Scripts remain under `data/assets/` — **not moved to `data/cot/`** (deploy-map hazard).
8. No hardcoded series start; current-state only; no timeseries emitted.
9. **Session log Compiler Tools section reproduces every `<run>` with observed output and pass/fail vs
   `<expect>`. Missing rows = REWORK.**
</acceptance_criteria>

<escalation>Report to 2.0.0_SA_COO; CTO holds the design gate. Escalate if the 296/296 bridge drops or if the same-day vintage binding cannot be satisfied from available partitions.</escalation>
</task_order>
