<task_order>
<to_id>MDPF_CANRTE.W2R.modelb-spine-port</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<date>2026-08-04</date>
<status>complete -- CLOSED 2026-08-05 ~2350Z (2.0.0_SA_COO). Executed + swapped 2026-08-04 (ledger CLOSE @5efb01ed03: round-2 E2E GREEN); FIRST FULL SCHEDULED CYCLE VERIFIED CLEAN 2026-08-05 (org/projects/MDPF_CANRTE.json). Surfaced by 0.4.0_DS_ClientPlatform's backlog triage.</status>
<priority>P1 (the re-scoped W-2, per ANDREW-DIRECT no-shadow verbatim (AE terminal ~1825Z) + CTO adjudication 184443Z + converged release 184538Z; supersedes MDPF_CANRTE.W2.modelb-spine-shadow, deprecated-as-shaped)</priority>

<title>MDPF_CANRTE W-2R: the Model-B spine builder ports DIRECTLY -- build correctly the first time, then the dispatch re-point in a serve-quiet window with same-window rollback. No shadow, no comparator, no standing verification machinery.</title>

<context>
Andrew's method, as ruled (CTO adjudication against the fuller verbatim): build correctly the
first time, then port. The shadow-emission model and the comparator are BOTH vetoed ("The
comparator is ALSO a horrible idea... it just muddies the water even further"; "the ONLY thing
that is supposed to happen here is the collective spine"). NOBODY manufactures a replacement
verification gate -- the port rides build-correctness + rollback, full stop.

SURVIVORS you build on: your committed spine builder (the collective spine) and W-1's
route_bindings_tieout (a build-time exercised control on the binding table -- CTO's explicit
carve, not a standing comparator).
</context>

<scope>
1. BUILD-CORRECTNESS at your seat, the normal Rule-13 QA at build time: tests, the W-1 tie-out,
   and an AD-HOC QA READ of the builder's output (run-and-read per the standing 07-24 ad-hoc-QA
   rule -- one invocation, read the artifact, nothing standing, nothing durable staged outside
   your normal build flow). Your existing per-model tie-law read is the content bar.
2. THE DIRECT PORT: the plan's single dispatch re-point (stages 6a/6d step (3) -> the
   consolidated builder writing the CANONICAL staging keys), executed in the serve-quiet window
   (~17:30Z -> 11:30Z) with the change-management ledger opened at step start and SAME-WINDOW
   ROLLBACK (revert the dispatch step; incumbents stay deployed until W-4/W-5 exactly as the
   plan states).
3. Post-port: the next SCHEDULED cycle's artifacts are the production evidence (NEVER#4);
   read them as part of that cycle's normal reads -- not as a new gate.
4. NO shadow writes anywhere, NO comparator in any mode, NO new verification machinery.
   Timing of the port window (tonight's quiet window vs tomorrow's) is yours + CTO's call
   against the plan's freeze rules.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before the port">
    <step>
      <run>build QA: suite green + W-1 tie-out green + the ad-hoc QA read of the builder output (run-and-read, per-model tie to the spine's own content bar)</run>
      <expect>All three captured; the ad-hoc artifact is QA evidence only, never production.</expect>
      <if_mismatch>STOP. Build-correctness IS the method now -- a defect found here is fixed here, not ported.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="the port">
    <step>
      <run>the dispatch re-point in the quiet window; ledger entry opened at step start, closed at verify; comp-pipescript deployed MATCH post-port</run>
      <expect>One-step change, ledger discipline per the half-landed NEVER rule; rollback path stated in the ledger before firing.</expect>
      <if_mismatch>Same-window rollback, no exceptions.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after the next scheduled cycle">
    <step>
      <run>read the scheduled cycle's artifacts in the normal cycle read; report to me + CTO</run>
      <expect>Production evidence per NEVER#4; the TO closes on it.</expect>
      <if_mismatch>Rollback + report -- the incumbents are still deployed by construction.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
The dispatch script is the shared seam (AE infra family) -- coordinate the re-point commit with
AE as the plan's W-2 always specified. GRF + the two-spec acct-dist seam ride their own threads.
comparator deletion + deprecation marks per the converged instruction are part of this TO's
Phase-1 cleanup (your owned paths).
</cross_domain_coordination>

<acceptance_criteria>
1. Build QA captured (suite + tie-out + the ad-hoc read).
2. The port executed with ledger discipline; deployed MATCH post-port; rollback path pre-stated.
3. The next scheduled cycle read as production evidence; TO closes on it.
4. Zero shadow writes, zero comparator, zero new gates -- the absence is itself checkable.
Plus: session log Compiler Tools section reproducing every run. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="authority">ANDREW-DIRECT no-shadow verbatim (AE terminal ~1825Z; memory/feedback_no_shadow_channels_veto_build_correctly_and_port.md; CLAUDE.md law landing at CTO) + CTO adjudication 184443Z + converged release 184538Z</ref>
  <ref type="predecessor">MDPF_CANRTE.W2.modelb-spine-shadow (deprecated-as-shaped, in-file note) -- the builder work it produced is this TO's surviving core</ref>
  <ref type="plan">@c68f238e5 (the wave structure + quiet-window + rollback rules stand; only the verification model changed)</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
