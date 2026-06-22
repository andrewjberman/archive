<to_id>ADVI_COTETL.CLEANUP</to_id>
<project>ADVI_COTETL</project>
<title>cot bd-fork hygiene cleanup (post-$24M-close): retire the dead account_gains/C_00/C_02 lots-path + per-class cot-gold ruff cleanup</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (COTETL closeout; CTO-flagged 171350Z + 140130Z)</issued_by>
<issued_date>2026-06-22</issued_date>
<status>staged</status>
<!-- NON-URGENT, post-P0. NOT GO'd: DS just carried the 5-layer $24M P0 -- pick up on your capacity-signal. Both items are NON-CORRECTNESS hygiene (the served data is right + certified); neither blocks anything. -->

<objective>
Two same-class bd-fork hygiene items surfaced by the COTETL $24M served-AUA fix (5c80bf6ca, CVO-certified). Both are NON-CORRECTNESS, cot-path-scoped, DS-lane (gold-script Rule-13). The served firm-AUA is CORRECT + certified ($395.30M/06-18); this is debt-cleanup so the dead-fork remnants don't mislead a future toucher.
</objective>

<the_fix>
1. RETIRE/QUARANTINE the dead lots-FIFO path for cot: account_gains (B_03) -> C_00 canonical_performance -> C_02 client_performance are now UNCONSUMED for cot (the C_03/C_01 snapshot-wire bypassed them; D_00 uses C_03-primary, C_02-fallback never fires; account_gains stays frozen-06-09 harmlessly). GROUND the consumer-map first (comp-blast/comp-pipescript io -- re-confirm 0 LIVE cot consumers, per the cert finding), THEN either (a) cot-conditional skip the dead B_03/C_00/C_02 build for cot (don't waste the run + don't emit a stale-dated artifact), or (b) snapshot-wire C_00/C_02 too (if any future cot surface will want client_performance). CTO architect-confirms the (a)-vs-(b) call before implement (same pattern as the C_03 fix). This is the "C_02 follow-on" CVO/DS referenced.
2. cot-gold per-class RUFF cleanup: C_01 carries 8 pre-existing bd-fork ruff violations (all OUTSIDE the C00SNAPSHOT change; RULE15 gate-note-bypass documented in 5c80bf6ca). Clean them per-class MANUALLY (py_compile + AST + ruff --select FA must stay green), NOT a `ruff --fix` bundle on the live script (banked: bd-fork ruff debt on a live cot gold script). Sweep the broader C_01/C_03 bd-fork debt in the same pass if cheap.
</the_fix>

<compiler_tools_mandate>
  <step><run>comp-blast account_gains + comp-pipescript io C_00/C_02 (cot)</run><expect>0 LIVE cot consumers of the dead path (re-confirm the cert finding) before retiring</expect></step>
  <step><run>ds-commit-gate (py_compile + ds-precommit-check + ruff FA) per touched script</run><expect>PASS; the per-class ruff cleanup makes C_01 ruff-clean WITHOUT a --fix bundle</expect></step>
  <step><run>safe-commit (cot-tree only) + comp-pipescript deployed (firm-sep)</run><expect>49F/bd ZERO-touch (firm-separated, like the C00SNAPSHOT fix)</expect></step>
</compiler_tools_mandate>

<acceptance_criteria>
1. Dead account_gains/C_00/C_02 cot path retired-or-snapshot-wired per CTO's (a)/(b) confirm; comp-blast re-confirms no live cot consumer left dangling.
2. C_01 (+ C_03 if swept) ruff-clean WITHOUT a --fix bundle (per-class manual); ds-commit-gate PASS.
3. Firm-separated (cot-tree only; 49F/bd untouched, comp-pipescript deployed MATCH).
4. Served firm-AUA UNCHANGED at $395.30M/06-18 post-cleanup (this is hygiene, must not move the certified number) -- verify on the next nightly's served artifact, no ad-hoc gold run.
5. Session-log reproduces the comp-runs; RAVC2 COO + CTO.
</acceptance_criteria>
