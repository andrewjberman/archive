<task_order>
<id>NFRA_SYSPARITY.WS-7.rail-description-and-count-reconcile</id>
<project>NFRA_SYSPARITY</project>
<issued_to>0.8.0_AE_CloudComp~Z</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<priority>P2 -- ANY TIME (PRD S4: independent of WS-1's denominator; the small honest-lag fixes). Context-reallocation of ~Z (comp-which/routing/comp-tools lane) per Andrew-direct idle-reallocation-by-context.</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_SYSPARITY_PRD.md @8f0b596f4 (WS-7 = S3 seventh bullet)</ref>
  <ref type="charter">org/tier0/ledger/LD-0318.md</ref>
</references>

<objective>
Describe the COMPRAIL rail's ENFORCEMENT in the system docs + fix the small honest lags:
(a) Add the COMPRAIL enforcement subsection to infra/system/03_comp_tools.md -- the DENY-gate, the `# rail-checked: <why>`
    marker, the HUD nudge, the audit log (org/mcp/comp-which-rail.log), and `/freeform` (CLAUDE.md Rule 21). The rail's
    ENFORCEMENT mechanism is currently absent from the 03 text (the doc describes the tools, not the gate that routes to them).
(b) Correct the "tenant-neutral comp-tools" over-reach in the SDK/system text (comp-tools are Opal-specific, not tenant-neutral).
(c) Fix the SDK front-end docstring count (3 -> 4).
(d) COUNT RECONCILE: the CLAUDE.md gate number is PARTLY DONE -- CTO refreshed CLAUDE.md 62/49 -> 78/60 this session (@49dad1c83).
    Reconcile the REMAINING docs/memory copies to the live gate number (78 exec / 60 routable / 65 tools / 97 entries per
    ~Z's own TO-4 reconcile @c6abdd55e) -- grep every stale 62/49 (or other stale count) across docs/ + memory/ and correct
    to the ONE gate-maintained authority (comp-manifest-check registration invariant). Cite the source-of-truth, don't hand-count.
</objective>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-manifest-check list (or the registration-invariant count) + grep -rn "62/49\|59 tools\|49 routable" docs/ memory/ CLAUDE.md</run>
      <expect>The LIVE gate number (78/60/...) from the invariant + the full set of stale-count occurrences to reconcile. The count is GATE-MAINTAINED -- cite it, never prose-maintain.</expect>
      <if_mismatch>If the live count differs from 78/60, use the live invariant number (it is the authority) + note the delta.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>grep the COMPRAIL enforcement terms in infra/system/03_comp_tools.md + re-grep the stale counts</run>
      <expect>03 now describes the DENY-gate + marker + HUD + audit + /freeform; zero stale 62/49-class counts remain in docs/memory; the over-reach + docstring corrected.</expect>
      <if_mismatch>Add the missing enforcement description / correct the remaining stale count.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. infra/system/03_comp_tools.md describes the COMPRAIL ENFORCEMENT (DENY-gate / `# rail-checked` marker / HUD / audit log / `/freeform`), grep-provable.
2. The "tenant-neutral comp-tools" over-reach corrected; SDK front-end docstring 3->4.
3. Counts reconciled to the ONE gate-maintained authority across CLAUDE.md/docs/memory (no stale 62/49-class number remains); the source-of-truth is cited, not hand-counted.
4. LD-0318 CVO-VERIFIED GATE: the rail-description accuracy + the count reconcile are CVO-verified per PRD S7 (CVO's verify-loop cron 02d90dce). Ping CVO on land.
5. Session log with Compiler Tools section reproducing each <run> vs <expect>.
</acceptance_criteria>

<cross_domain_coordination>
- WS-7 is INDEPENDENT of WS-1's denominator (docs/rail description + count reconcile) -> proceed now, do not wait on WS-1.
- The count-reconcile follows CTO's CLAUDE.md 78/60 refresh @49dad1c83 (do NOT re-touch CLAUDE.md's count -- CTO owns CLAUDE.md law; reconcile the docs/memory COPIES to it).
- CLAUDE.md edits are CTO-arch-gated law -- if any correction needs a CLAUDE.md change, route it to CTO, do not self-edit.
</cross_domain_coordination>

<notes>
Context-reallocation of ~Z per Andrew-direct (2026-07-19): ~Z's prior thread = NFRA_COMPASSURANCE (comp-which routing/top-k/
the rail), so the COMPRAIL rail-description + comp-tool-count reconcile is its natural adjacent fit. Independent of the WS-1
denominator so it starts immediately.
</notes>
</task_order>
