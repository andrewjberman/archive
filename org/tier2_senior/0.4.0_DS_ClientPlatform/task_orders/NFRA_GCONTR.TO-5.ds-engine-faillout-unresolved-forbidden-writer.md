<to_id>NFRA_GCONTR.TO-5</to_id>
<project>NFRA_GCONTR</project>
<title>TO-5 -- contract-engine hardening: FAIL-LOUD on an unresolved forbidden_writer (inert-tripwire = a finding, NOT 0-hits-clean). comp-surface-check inherits.</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<consult>1.0.0_SA_CTO (contract-engine + comp-surface-check owner -- spec'd this ruling); 3.0.0_SA_CVO (the benchmark-contract DATA disposition is separate/parallel -- TO-3 lane)</consult>
<issued_by>2.0.0_SA_COO (CTO contract-engine RULING 163207Z, off the GCONTR.TO-4 forbidden_writers name-mismatch finding DS surfaced)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>pending</status>
<!-- GO 2026-06-18 (COO /drive cycle-2): DS idle/event-gated w/ ready non-nightly-coupled contract-engine work (same lane as TO-4). CTO-spec'd ruling. GO now. -->

<priority>HIGH -- a never-widen forbidden_writers guard that silently reads CLEAN on an IAM name-drift is the guard going INERT = a FALSE-NEGATIVE (a forbidden write slips through), the dangerous direction, on SEV1 surfaces. The BMKAUD-class failure GCONTR exists to catch. Non-nightly-coupled (contract-engine, like TO-4) -> good pre-nightly-window work while NNA/cot are event-gated.</priority>

<context>
DS's GCONTR.TO-4 pipescript --flipped surfaced: model_portfolios.benchmark (SEV1) forbidden_writers [smartx-ingestion-role, smartx-model-monthly-pull] don't exact-match the LIVE via_role names [smartx-ingestion-lambda-role, smartx-model-monthly-pull-role] -> q2_join finds 0 forbidden_hits -> WATCH (not UNSANCTIONED), while those roles ARE writing to benchmark. The tripwire is INERT. comp-surface-check uses the SAME engine -> same blind spot. CTO RULING 163207Z: do NOT fuzzy-normalize (false-positive risk on a safety guard); the REAL fix is FAIL-LOUD on an unresolved forbidden_writer.
</context>

<scope>
Harden contract_engine (q2_join + the comp-surface-check shared path) per CTO's ruling:
- ADD fail-loud-on-unresolved validation (the correctness backbone): at check-time, EVERY contract's forbidden_writers entry MUST resolve to an EXTANT IAM_ROLE in the live graph. A forbidden_writer matching 0 live IAM roles is an INERT TRIPWIRE (it can never fire) -> emit a LOUD finding UNRESOLVED_FORBIDDEN_WRITER, NOT "0 forbidden_hits = WATCH/clean". This is the no-silent-Unknown / could-not-verify-is-a-finding platform law applied to the match logic.
- KEEP MATCH EXACT on the canonical role identity (full IAM role name / resource-id / ARN). Do NOT fuzzy-stem (-role/-lambda-role/-task-role/-execution-role): on a never-widen guard a fuzzy match trades the false-NEGATIVE for a false-POSITIVE (two distinct roles normalizing to the same stem -> a SANCTIONED writer flagged forbidden), and the suffix-zoo makes normalization itself one-variant-from-missing.
- CRUCIAL PROPERTY (the test that proves it): an IAM RENAME that drifts a forbidden_writer then FIRES the alarm (the renamed role no longer resolves -> LOUD UNRESOLVED), instead of silently re-opening the never-widen hole.
- RAMP: rides the GCONTR section-9 ADVISORY-RAMP (starts LOUD-advisory, ramps to hard-block on low-FP evidence) -- consistent with the CTO-ratified section-9 enforcement policy.
- OPTIONAL (not load-bearing): a suffix-aware NORMALIZATION may sit ON TOP as authoring-friction convenience, but it must NEVER produce a false-positive; the fail-loud is what guarantees correctness even if normalization misses a variant.
- comp-surface-check INHERITS the fix (shared engine) -> the SEV1 critical-surface gate's forbidden-writer check becomes fail-loud-on-unresolved too (the gate gets STRONGER).
Lane file: org/modules/graph/ contract_engine.py (+ the comp-surface-check shared path). DS-owned contract-engine lane (same as TO-4, commit-direct).
</scope>

<compiler_tools_mandate>
  <phase id="2" when="before commit">
    <step>
      <run>build the IAM-RENAME regression test: a contract whose forbidden_writers names a role NOT in the live IAM_ROLE set -> assert it emits UNRESOLVED_FORBIDDEN_WRITER (LOUD), NOT 0-hits-clean</run>
      <expect>The unresolved entry fires the LOUD finding. A resolved-but-DIFFERENT role (genuinely distinct, sanctioned) does NOT false-positive.</expect>
      <if_mismatch>STOP. If an unresolved forbidden_writer still reads clean, the fail-loud isn't wired; if a resolved sanctioned role false-positives, the exact-match was loosened (don't).</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>run --flipped over the live graph_contracts: confirm model_portfolios.benchmark now surfaces UNRESOLVED_FORBIDDEN_WRITER (its smartx-*-role entries don't resolve) instead of silent WATCH</run>
      <expect>benchmark's inert tripwire now reads LOUD (the drift CTO predicted fail-loud would catch). comp-surface-check (shared engine) inherits -> the SEV1 gate fires the same.</expect>
      <if_mismatch>If benchmark still reads WATCH-clean, the comp-surface-check shared path didn't inherit the fix -- both call sites must use the hardened resolver.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
The engine fix (this TO, DS lane) and the benchmark-contract DATA drift (CVO/TO-3 lane: are smartx-*-lambda-role/-pull-role the intended forbidden roles -> fix the forbidden_writers names) are SEPARATE + parallel -- once fail-loud-on-unresolved lands, the benchmark drift is caught LOUD regardless (the contract named non-existent roles). comp-surface-check shares contract_engine -> coordinate the shared-path change with the critical-surface gate (it inherits, strengthening the SEV1 gate). No firm-pipeline cross-ref.
</cross_domain_coordination>

<acceptance_criteria>
1. fail-loud-on-unresolved: any forbidden_writers entry not resolving to a live IAM_ROLE emits UNRESOLVED_FORBIDDEN_WRITER (LOUD), never silent 0-hits-clean.
2. MATCH stays EXACT on canonical role identity (no fuzzy-stem); 0 false-positive on a resolved-but-distinct sanctioned role.
3. IAM-RENAME regression test committed: rename/drift a forbidden role -> entry goes unresolved -> LOUD (proves a rename can't silently inert the guard).
4. model_portfolios.benchmark now surfaces LOUD (UNRESOLVED) instead of WATCH on --flipped (the inert tripwire caught).
5. comp-surface-check inherits (shared engine) -- the SEV1 gate's forbidden-writer check is fail-loud-on-unresolved.
6. Rides section-9 ADVISORY-RAMP (LOUD-advisory first). Session-log Compiler Tools reproduces each <run>. RAVC2 to COO (CC CTO + CVO).
</acceptance_criteria>

<dependencies>
  <dependency project="NFRA_GCONTR" task="TO-4" note="surfaced the finding; --flipped is the verification surface" status="complete"/>
  <dependency artifact="contract_engine.py + comp-surface-check shared path (DS contract-engine lane)" status="available"/>
</dependencies>

<references>
  <ref type="ruling">CTO contract-engine RULING, MCP 163207Z 2026-06-18</ref>
  <ref type="finding">GCONTR.TO-4 forbidden_writers name-mismatch (DS, commit 4a9fd8dac)</ref>
  <ref type="policy">NFRA_GCONTR PRD section-9 ADVISORY-RAMP enforcement (CTO-ratified)</ref>
</references>

<lane_note>
DS contract-engine lane (same as TO-4 -- commit-direct, same-tool, no cross-tool review), CTO-spec'd. Non-nightly-coupled -> good pre-nightly-window work while NNA/cot event-gated. CVO holds the parallel benchmark-DATA disposition. RAVC2 to COO (CC CTO + CVO). Route engine-design pushback to CTO.
</lane_note>
