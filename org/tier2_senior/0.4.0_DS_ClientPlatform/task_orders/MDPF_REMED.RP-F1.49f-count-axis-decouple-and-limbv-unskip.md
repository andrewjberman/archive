# TO MDPF_REMED.RP-F1 — 49F COUNT-AXIS DECOUPLE + limb-(v) un-skip (SEQUENCED PACKAGE) ⛔ STAGED: AFTER the atomic window LANDS AND PROVES

<task_order id="MDPF_REMED.RP-F1" project="MDPF_REMED">
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-11T00:1xZ</issued>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "MDPF_REMED" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged</status>
<priority>FOLLOW-ON, not a window change (CTO ruling 001216Z). GO comes from COO only after the
RP-W1/W2/W3 atomic window lands and proves on a scheduled cycle. This is a SCOPE-ADD ruled by CTO:
the 49F COUNT-axis decouple is NOT in RP-W1/W2 as written (W2 = the FRONTIER unlink; same word
"axis", two different couplings).</priority>

<dependencies>
  <dependency agent="2.0.0_SA_COO" task="atomic window (RP-W1+W2+W3) landed AND proved on a scheduled cycle" status="pending"/>
</dependencies>

<references>
  <ref type="ruling">CTO 20260811T001216Z (item-3 deferral + D-5 re-scope) — inbox record + plan artifact</ref>
  <ref type="plan">org/tier1_exec/1.0.0_SA_CTO/deliverables/MDPF_REMEDIATION_PLAN_20260810.md @dbbbfa9cd3 (W5 item 3, D-5 as re-scoped)</ref>
</references>

## SCOPE — one sequenced package, all in data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py (your lane, Rule 13)
1. **THE DECOUPLE (the real defect per the code's own words :1545-1549/:1608):** 49F's COUNT leg
   reads the legacy served import (`count_source="served_import"`, FIRM_BUILD_CONFIG :1003) instead
   of its own value's feed. Repoint count to share the value leg's feed so count and value genuinely
   share a source.
2. **THE UN-SKIP, same commit series:** flip `same_source=True` for 49F; retire the measured-skip
   else-branch (:1599-1619) and the enumerated exempt list per its own :1510 RETIRE note — clause
   (v) then evaluates real coverage instead of structural absence.
3. **FORECAST, so nobody meets it cold (CTO):** the deployed skip currently measures **205 per-band
   disagreements across 33 dates** — that figure sizes what the decouple will surface. A RED on
   first post-decouple run is the EXPECTED shape if the decouple is incomplete; a clean run means
   the decouple worked. Neither is a surprise.

⚠ Until this TO completes: the 49F gate PASS is NEVER cited as a control (CTO standing strike), and
the deployed skip is understood as the design's honest accommodation — printed exposure every run —
not a silent defect.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript io dim_mdpf_aggregate_aua_timeseries.py --pipeline mdpf ; comp-find "served_import" data/mdpf</run>
      <expect>count_source="served_import" localized to the 49F config row; the value leg's feed identified as the repoint target. Denominators printed.</expect>
      <if_mismatch>STOP; if the coupling moved since @a7281ae8e0, re-ground before editing.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-validate dim_mdpf_aggregate_aua_timeseries --artifact &lt;QA build, all four scopes&gt;</run>
      <expect>PASS/WAIVED; 49F clause (v) EVALUATES (no skip branch); emission does NOT halt on the QA build — or the RED is characterized against the 205/33 forecast with a named residual.</expect>
      <if_mismatch>A RED exceeding/deviating from the forecast = surface to COO+CTO with the delta before commit; do not ship a halt into the scheduled cycle.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>comp-pipescript deployed dim_mdpf_aggregate_aua_timeseries.py + one SCHEDULED cycle observed</run>
      <expect>MATCH; scheduled cycle emits 12/12 with clause (v) live for 49F.</expect>
      <if_mismatch>Roll back per deploy-ledger discipline; a daily-halt regression is the exact cost CTO's deferral was priced against.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Same file as RP-W1/W2 — sequence strictly AFTER the atomic window (this TO's gate). AE holds the
retired item-3 context (RP-W5) and the window mechanics; no AE edit here (Rule 13). Coordinate with
COO before the deploy leg as usual.
</cross_domain_coordination>

<acceptance_criteria>
1. Count and value legs share a feed (shown at source + exercised: a count/value read on one date
   from one feed).
2. Clause (v) evaluates for 49F on a scheduled cycle without halting emission (or the RED is
   characterized against the 205/33 forecast and ruled before serve).
3. Measured-skip branch + exempt list retired per :1510; no new skip introduced.
4. Session log Compiler Tools section reproduces every &lt;run&gt; + output + pass/fail.
</acceptance_criteria>
</task_order>
