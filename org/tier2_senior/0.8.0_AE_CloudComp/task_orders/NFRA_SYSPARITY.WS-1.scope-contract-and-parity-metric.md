<task_order>
<id>NFRA_SYSPARITY.WS-1.scope-contract-and-parity-metric</id>
<project>NFRA_SYSPARITY</project>
<issued_to>0.8.0_AE_CloudComp~A</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<priority>P1 -- DO FIRST. Gates WS-2..8 (honest measurement needs the denominator first) + unblocks NFRA_ONTOCLARITY charter (PRD S8). CTO PRD S4 sequencing: WS-1 before all.</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_SYSPARITY_PRD.md @8f0b596f4 (WS-1 = S3 first bullet; scope ruling S2)</ref>
  <ref type="brief">docs/briefs/NFRA_SYSPARITY_BRIEF_20260719.md (MSTR 4-domain grounded baseline)</ref>
  <ref type="charter">org/tier0/ledger/LD-0318.md (Andrew-direct)</ref>
</references>

<objective>
Implement the PRD S2 scope ruling as an EXPLICIT, AUDITABLE scope contract + define the parity METRIC that all
WS-2..8 measurement rests on. Two deliverables:
(A) infra/system/README.md states what the /system tree COMMITS to representing (engineering / ontology / comp-tools /
    infrastructure, per Andrew's charter) AND names EVERY exclusion with a one-line "sibling knowledge class + pointer"
    (client-data pipeline estate INF/49F/COT/TAXSMA/OPAL_ASSETS; taxonomy/consolidation plane) -- so no reader can
    confuse SCOPING from OVERSIGHT (PRD S2.3). Ontology is IN scope (S2.1); the pipeline/taxonomy estates are CONFIRMED
    OUT, not widened (S2.2).
(B) A parity METRIC that is REPRODUCIBLE FROM A COMMAND, not a prose estimate: per-domain (not one number), denominator =
    the DECLARED scope with exclusions NAMED, and it must NEVER count the ~90% out-of-scope-by-design estate as a gap
    (VERIFICATION-LAW #6 wrong-axis error -- print the denominator). MSTR's baseline (comp-tools ~85% / infra ~80% /
    eng+loops ~70-75% / ontology ~40%) is the ASSUMPTION this metric must let CVO reproduce + re-ground (PRD S7).
</objective>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-system --check</run>
      <expect>Reports the current SYSTEM state (expected STALE per PRD S1 -- 06_current_state 250 commits stale). Capture the exact staleness signal + what it keys on; the metric in (B) must be consistent with / reuse this signal, not invent a parallel one.</expect>
      <if_mismatch>If comp-system --check reports CURRENT (not STALE), the PRD S1 premise moved -- STOP + surface to COO (the baseline shifted under the PRD).</if_mismatch>
    </step>
    <step>
      <run>ls infra/system/ + read infra/system/README.md (current) + the 0*_*.md section files</run>
      <expect>Enumerate what the tree currently declares vs the 4 charter domains; identify the un-declared omissions the brief flagged (the ontology's absence; any tenant-neutral over-reach). This is the gap the boundary sentences close.</expect>
      <if_mismatch>N/A -- discovery step.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>bash the metric command you define (the reproducible per-domain parity command)</run>
      <expect>Emits per-domain parity with the DENOMINATOR PRINTED + exclusions NAMED; the out-of-scope estate is NOT counted as a gap; the numbers are reproducible (re-runnable, deterministic given a HEAD). A single blended number is NOT acceptable (PRD non-goal S5).</expect>
      <if_mismatch>STOP. If the metric counts out-of-scope infra as missing, it is the wrong-axis error -- fix the denominator to the DECLARED scope before commit.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>grep the exclusion pointers in infra/system/README.md</run>
      <expect>Every out-of-scope estate (INF/49F/COT/TAXSMA/OPAL_ASSETS + taxonomy/consolidation) has a one-line sibling-class + pointer; ontology is stated IN-scope. No silent omission remains.</expect>
      <if_mismatch>Add the missing boundary sentence -- an un-declared omission is exactly what WS-1 exists to close.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. infra/system/README.md commits the tree to the 4 charter domains AND names every exclusion with a sibling-class + pointer (SCOPING-not-oversight is grep-provable). Ontology stated IN; pipeline/taxonomy stated OUT (confirmed, not widened).
2. The parity metric is REPRODUCIBLE FROM A COMMAND (not a prose estimate): per-domain, denominator = declared scope with exclusions named, out-of-scope estate never counted as a gap. Re-running it on a given HEAD is deterministic.
3. The metric reuses / is consistent with comp-system's staleness signal (no parallel invented axis).
4. LD-0318 CVO-VERIFIED GATE (in ADDITION to RAVC + CTO arch-gate): the scope ruling + metric are an ASSUMPTION until CVO re-grounds them per PRD S7 (/molecule + /verify + /prd-delta). WS-1 is NOT done until CVO verifies the denominator is the declared scope + the metric reproduces MSTR's baseline within its stated axis. Ping CVO on land.
5. Session log with a Compiler Tools section reproducing every <run> + observed result + pass/fail vs <expect>.
</acceptance_criteria>

<cross_domain_coordination>
- NFRA_ONTOCLARITY (PRD S8): WS-1 landing is the CHARTER SIGNAL for ONTOCLARITY (MSTR charters it on WS-1 land). Flag COO + MSTR when WS-1 lands so ONTOCLARITY charters + its clarified definitions can feed WS-4.
- WS-2/WS-3 (the load-bearing control fixes) consume this metric's denominator -- they cannot honestly measure until WS-1 lands. COO sequences them to start after WS-1.
- Scope ruling S2 is CTO-ratified + surfaced to Andrew as overridable (ontology-in) -- non-blocking; build to the ruled scope.
</cross_domain_coordination>

<notes>
COO decomposition of NFRA_SYSPARITY PRD v0.1 (CTO @8f0b596f4). This is the first + gating WS. The metric denominator is
the load-bearing artifact -- the whole project's "make parity a CONTROL" thesis (WS-2/WS-3 fail-closed gates) rests on an
honest, reproducible denominator, and a naive metric that scores out-of-scope infra as missing is the exact wrong-axis
error the doctrine (VL#6) warns against. ~A owns this as the system/SDK/NESTEDABSTRACT-domain lane. CVO's LD-0318
per-domain verification loop (cron 02d90dce) is armed + will re-ground the metric as you build -- coordinate with it.
</notes>
</task_order>
