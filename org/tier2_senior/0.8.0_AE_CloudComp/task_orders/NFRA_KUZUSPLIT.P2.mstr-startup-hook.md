<task_order>
<to_id>NFRA_KUZUSPLIT.P2</to_id>
<title>comp-kuzu-full on MSTR startup — the idempotent daily-full hook that warms the shared canonical once, so every worker rides comp-kuzu-inc thereafter</title>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<date>2026-07-17</date>
<status>staged</status>
<priority>P2 (Andrew batch 2026-07-17). GATE: NFRA_KUZUSPLIT.P1 landed (the two commands exist + registered). Follow-on to P0-P1.</priority>

<authority>
Andrew-direct verbatim: "full derive as a function of 0.0.0_AB_MSTR startup, but for the remainder of the
session, all agents should just be using incremental update pre comp tool queries." Andrew RATIFIED the
design 2026-07-17 (O-1 = serve-labeled-stale). PRD §5 P2. This TO is the startup-hook half.
</authority>

<gate>
DO NOT GO until P1 has landed (comp-kuzu-full / comp-kuzu-inc exist, registered, exercised). COO fires GO
when P1's acceptance clears. MSTR-lane owns the XXX.md Step-1b edit (Art. VI: MSTR governs the doc, does not
edit the code) — coordinate the same-wave landing so the doc never describes a hook that isn't wired.
</gate>

<scope>
Wire `comp-kuzu-full` to run ONCE at MSTR session startup (org/XXX.md Step 1b / the MSTR launcher), absorbing
the nightly-2a whole-table delta into the shared canonical so every subsequent agent that day sees only the
small 2b deltas (→ comp-kuzu-inc in ~4s).
  IDEMPOTENT GUARD (the load-bearing AC): if the canonical is ALREADY at nightly-HEAD this cycle (a marker
  says so), SKIP — never double-pay the full. A second MSTR startup in the same cycle is a no-op.
  This is a STARTUP-HOOK wiring, not an alarm — clear of the alert-suspension.
</scope>

<compiler_tools_mandate>
  <phase id="2" when="before commit">
    <step>
      <run>Exercise the idempotent guard: run comp-kuzu-full at a simulated MSTR startup (cold → full paid + marker set), then a SECOND startup same cycle (marker present → SKIP, no full)</run>
      <expect>First = full projection + HEAD marker written; second = no-op SKIP (the guard fires). A second full in the same cycle is the failure this AC exists to prevent.</expect>
      <if_mismatch>STOP. A non-idempotent hook double-pays the ~6min full every restart — do not ship until the SKIP is exercised.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
MSTR-lane (Art. VI): the org/XXX.md Step-1b startup-line edit ships IN THE SAME WAVE as this hook (MSTR
governs the doc, 0.8.0~D wires the code, CTO arch-gates). The marker semantics must agree with comp-graph
status's "last mode + behind-by-N" line (P3 docs). No alert leg.
</cross_domain_coordination>

<acceptance_criteria>
1. comp-kuzu-full runs once at MSTR startup; the idempotent guard SKIPs a same-cycle second run — EXERCISED both ways.
2. A worker's first comp-kuzu-inc after an MSTR startup sees only the small 2b delta (~4s), not a full — measured.
3. XXX.md Step-1b doc edit lands same-wave (MSTR-authored); comp-manifest-check green.
4. Session log reproduces each mandate run + observed vs expect.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/NFRA_KUZUSPLIT_PRD.md (§5 P2)</ref>
  <ref type="depends">NFRA_KUZUSPLIT.P0-P1 (must land first)</ref>
</references>
</task_order>
