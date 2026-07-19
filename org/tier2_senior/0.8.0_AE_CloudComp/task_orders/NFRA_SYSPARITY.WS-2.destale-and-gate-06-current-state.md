<task_order>
<id>NFRA_SYSPARITY.WS-2.destale-and-gate-06-current-state</id>
<project>NFRA_SYSPARITY</project>
<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<priority>P1 -- LOAD-BEARING control fix (PRD S3/S4). [CTO ARCH-GATE at build.] Part (a) de-stale is independent of WS-1; part (b) the gate mechanism is CTO-arch-gated. Context-reallocation of ~D (comp-tools lane) per Andrew-direct idle-reallocation-by-context.</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_SYSPARITY_PRD.md @8f0b596f4 (WS-2 = S3 second bullet)</ref>
  <ref type="charter">org/tier0/ledger/LD-0318.md</ref>
</references>

<objective>
Make `06_current_state` a live-cadence CONTROL instead of a hand-passed doc that has lapsed (250 commits stale):
(a) DE-STALE: run `comp-system` to clear the SYSTEM STALE state. CVO's live fire-2 confirmed the exact drift target:
    ledger 80->82, tools 59->61, cse_schema 0.4->0.5 -- regenerate 06_current_state.{md,json} so `comp-system --check`
    reports SYSTEM CURRENT.
(b) GATE it fail-closed so 06 cannot silently rot again. **Arch-gate mechanism (mirrors the NESTEDABSTRACT drift-gate ruling
    this session -- coordinate with ~A's drift-gate pattern):** the gate must (i) FAIL-CLOSED on a real staleness (nonzero
    exit / hard signal, NOT a printed advisory -- Rule-20 "cannot block = not a gate"), (ii) be STALENESS-CONDITIONED (fire
    on genuine drift, not on wall-clock idle -- the false-Monday/NEVER#1 class), (iii) be EXERCISED both directions (seed a
    stale 06 -> watch it fire; a fixed 06 -> watch it clear), (iv) respect the consolidation ALERT-SUSPENSION -- prefer
    on-demand / HEAD-advance-auto-regen over a NEW scheduled CI cadence (a stateless CI sweep needs a persisted marker =
    unattended bot-commits to CLOUD, same reasoning as the drift-gate's P2.5 deferral).
</objective>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-system --check</run>
      <expect>SYSTEM STALE (CVO-confirmed: ledger 80/tools 59 vs live 82/61). Capture the exact staleness signal the gate will key on.</expect>
      <if_mismatch>If already CURRENT, the drift self-cleared -- verify + surface to COO (the WS-2 (a) premise moved).</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-system (regenerate) then comp-system --check</run>
      <expect>--check = SYSTEM CURRENT after regen (ledger 82 / tools 61 / cse_schema 0.5 reflected). EXERCISED, not a config read.</expect>
      <if_mismatch>STOP -- if --check still STALE after regen, the regen is incomplete; do not claim de-staled.</if_mismatch>
    </step>
    <step>
      <run>exercise the fail-closed gate BOTH directions (seed a stale 06 -> fire; fixed 06 -> clear)</run>
      <expect>Gate fires (nonzero/hard signal) on the seeded staleness AND clears on the fixed 06 -- proven by exercise, not asserted. Staleness-conditioned (does not fire on idle).</expect>
      <if_mismatch>STOP -- an unexercised or advisory-only gate is not a control (WS-2's whole thesis). Fix before commit.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. `comp-system --check` = SYSTEM CURRENT (ledger 80->82 / tools 59->61 / cse_schema 0.4->0.5 regenerated) -- CVO verifies this EXERCISED (its fire-2 bar), not a config read.
2. A fail-closed gate exists that (i) hard-signals on real staleness, (ii) is staleness-conditioned (no false-Monday), (iii) is EXERCISED both directions, (iv) is alert-suspension-clean (on-demand/HEAD-advance preferred over new CI cadence).
3. CTO ARCH-GATE on the gate mechanism (mirrors the drift-gate ruling) -- ping CTO at the build gate before landing.
4. LD-0318 CVO-VERIFIED GATE: the de-stale + the fail-closed gate are CVO-verified per PRD S7 (cron 02d90dce). Ping CVO on land.
5. Session log with Compiler Tools section reproducing each <run> vs <expect>.
</acceptance_criteria>

<cross_domain_coordination>
- COORDINATE the gate mechanism with ~A's NESTEDABSTRACT drift-gate (same fail-closed / staleness-conditioned / exercised / alert-suspension-clean pattern; reuse the shape, don't re-derive). The COO (drift-gate cadence-owner) can broker the pattern-share.
- Part (a) de-stale is independent of WS-1; the parity-metric (WS-1) will CONSUME the CURRENT 06 -- so de-staling early unblocks honest measurement.
- CTO-arch-gate flagged -- COO pings CTO at the WS-2 build gate.
</cross_domain_coordination>

<notes>
Context-reallocation of ~D per Andrew-direct (2026-07-19): ~D's prior thread = NFRA_COMPSIMILAR (comp-tools engine work);
comp-system is comp-tools infrastructure -- a natural adjacent fit, and the fail-closed-gate mechanism reuses the exact
drift-gate discipline the fabric just landed (which ~D watched COO drive). PH1 stays HELD (its KUZUSPLIT-P1 + CTO plan-gate
are unchanged); WS-2 is ~D's active work now.
</notes>
</task_order>
