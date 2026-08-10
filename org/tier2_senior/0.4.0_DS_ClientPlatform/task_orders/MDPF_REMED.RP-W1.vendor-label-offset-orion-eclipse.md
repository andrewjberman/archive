# TO MDPF_REMED.RP-W1 — VENDOR LABEL OFFSET (orion + eclipse ONLY) — served numbers are wrong TODAY

<task_order id="MDPF_REMED.RP-W1" project="MDPF_REMED">
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-10T23:4xZ</issued>
<status>staged</status>
<priority>P0 — FIRST of the seven. Nothing else in the plan lands before or without this.</priority>

<references>
  <ref type="plan">org/tier1_exec/1.0.0_SA_CTO/deliverables/MDPF_REMEDIATION_PLAN_20260810.md @dbbbfa9cd3 (W1, §1, §5)</ref>
  <ref type="evidence">org/projects/MDPF_PIPELINE_TRUTH.json @5ba751ed88 — cite ONLY MEASURED cells as fact</ref>
</references>

## NAMING NOTE
RP-Wn task codes = §2 workstreams of MDPF_REMEDIATION_PLAN_20260810. Deliberately DISTINCT from the
earlier MDPF_REMED.W1-x register TOs (W1-1 custody repoint, W1-2 retired-superseded, W1-4, W1-5) —
same project, different wave. Do not cross-read the numbering.

## SCOPE — TWO VENDORS ONLY, NAMED. THE OTHER TWO ARE HEALTHY.
Apply the vendor label offset so a served date means the day it claims:
- **orion**: `orion_normalize_as_of = prior_trading_day` EXISTS, is SEALED (2026-07-02), and is
  NEVER CALLED — zero occurrences in the 2,734-line gold builder
  (`data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py`). Wire it in; do not re-derive it.
  Normalizer source: `data/inf/scripts/silver/_orion_vendor_asof.py:126-136` (walks back weekends AND
  NYSE holidays; hardcoded closed-dates table 2025–2027 — carried maintenance bound, not yours to fix).
- **eclipse**: run-date key, T-1 offset. Four independent derivations already on record (producer
  source · weekday census · value tie-out · TWR-factor ratio 0.07bp vs 101bp for same-day).

⚠ **SCHWAB AND BLACKDIAMOND LABELS ARE ACCURATE — the normalizer is explicitly Orion-only. Applying
an offset there CORRUPTS TWO HEALTHY LEGS.** Any change that touches a schwab or blackdiamond label
path is out of scope and is a STOP-and-surface.

Also in scope: `lag_vs_as_of_days` must stop asserting 0 when it isn't (D-4/D-10: served Wednesday
08-05 = $209,431,383.43, which is Tuesday 08-04's custody, declared `lag_vs_as_of_days: 0`).

## WHY YOU ARE FIRST — D-19, measured (carried verbatim so the sequencing survives to the executor)
Move the floor later OR the pulls earlier ON ITS OWN and the frontier becomes 2026-08-07, which
eclipse HAS. 08-06 stops being the frontier, both legs go None, they agree, and limb (v) STOPS
FIRING. Under the run-date ruling that cycle then PUBLISHES ONE TRADING DAY MISLABELLED INSTEAD OF
REFUSING. **The guard is currently the only thing keeping a wrong number off the served plane. Your
label fix is what makes the cadence fix (RP-W3, AE, staged) safe to apply. RP-W3 does not move until
this TO is complete.**

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript io dim_mdpf_aggregate_aua_timeseries.py --pipeline mdpf</run>
      <expect>READS include gold/mdpf_revamp/* + monolith silver fact_* set (fact_assets, fact_model_allocation_roster, fact_model_aum_daily, fact_portfolios_full, fact_rps_s2). No COLUMN GAPS attributable to your change plan.</expect>
      <if_mismatch>STOP. A read you did not expect means the offset touches a leg you have not scoped. Surface to COO before writing.</if_mismatch>
    </step>
    <step>
      <run>comp-find "orion_normalize_as_of" data</run>
      <expect>DEF in data/inf/scripts/silver/_orion_vendor_asof.py; ZERO call sites in data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py (the sealed-never-called state, re-confirmed at your HEAD before you change it).</expect>
      <if_mismatch>If a call site already exists, the plan's premise moved — STOP and surface to COO+CTO; do not double-apply an offset.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-validate dim_mdpf_aggregate_aua_timeseries --artifact &lt;your QA artifact&gt;</run>
      <expect>PASS or WAIVED. NO_CONFIG/ZERO_CHECKS = UNVALIDATED — never signal SAFE on it.</expect>
      <if_mismatch>STOP. Do not commit until ERROR clean; surface NO_CONFIG to COO as a gap finding.</if_mismatch>
    </step>
    <step>
      <run>.tools/commit-gate.sh (via safe-commit)</run>
      <expect>Gate passes. `from __future__ import annotations` present.</expect>
      <if_mismatch>Fix before commit. --force does not bypass a gate failure.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>comp-pipescript deployed dim_mdpf_aggregate_aua_timeseries.py</run>
      <expect>MATCH after your deploy leg completes (DS owns the commit→QA-deploy cycle for data/*/scripts/gold per Rule 13).</expect>
      <if_mismatch>STALE/MISSING = the served plane still runs old code; finish the deploy leg or surface the blocker. A committed-but-not-deployed label fix is the exact class this project exists to kill.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Same file as RP-W2 (dim_mdpf_aggregate_aua_timeseries.py) — SAME OWNER (you). Sequence: RP-W1 lands
first or in the same commit series; do not interleave with any other agent's edits.
⛔ ATOMIC-DEPLOY RE-CUT (Andrew ruling ~2334Z, Call 1 route (b); CTO relay 234031Z): RP-W1 + RP-W2 +
AE's RP-W3 cadence change GO LIVE IN ONE COORDINATED WINDOW — build, QA, and COMMIT your work now,
but the DEPLOY LEG (aws s3 cp to the served plane) fires ONLY inside the COO-called joint window
with AE's apply; NEITHER SHIPS ALONE. Deploy-completion ledger entry opened at window start; if
either leg fails, both roll back in-window. Report BUILD-READY (committed + QA'd + validated) to
COO; that report is what lets COO call the window.
</cross_domain_coordination>

<acceptance_criteria>
EXERCISED, not config-read (Rule 22a):
1. A served point labelled D contains D's close, TIED OUT against the vendor artifact for D — one
   orion date and one eclipse date, values shown, in the session log.
2. `lag_vs_as_of_days` asserts a nonzero value on a run where lag exists (exercise it; show the run).
3. NEGATIVE CONTROL: one schwab and one blackdiamond served label shown UNCHANGED pre/post.
4. Session log Compiler Tools section reproduces every &lt;run&gt; above with observed output and
   explicit pass/fail vs &lt;expect&gt;. Missing rows = REWORK.
Completion bar context (plan §5): the WORKSTREAM completes only when the scheduled cycle emits with
correct labels — your TO completes on the above, but do not report the PIPELINE fixed; that is 12/12
A4 objects on one unattended scheduled cycle, adjudicated by COO.
</acceptance_criteria>
</task_order>
