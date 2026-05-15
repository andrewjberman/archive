<task_order>
  <metadata>
    <id>ADVI_INFFIN.026</id>
    <slug>ds-rate-emit-augment-conditional</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~? (route at conditional dispatch)</issued_to>
    <date>2026-05-14</date>
    <status>not-applicable</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>PATH A CONFIRMED (INFFIN.025 RAVC2 4187ebec): detail.json accounts[].fee fields already present on S3. No DS emit augment needed for fee rates. This TO will never fire. §3.6a also already working (zero FE changes). CLOSED without execution.</dispatch_unblock_condition>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P1 conditional — Fee Summary table rate-emit augment if gold script gap</priority>
    <sla>~1-2h wall actual (if dispatched)</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFFIN_UX_FIXES_BATCH.md §3.6b (CTO `23fdaac67`)</ref>
    <ref type="parent_investigation">ADVI_INFFIN.025 Phase 1 rate-emit investigation</ref>
    <ref type="andrew_direct">Andrew 2026-05-14 ~23:0XZ: "clearly we know the rates on all the accounts so not sure why that is not being populated in the fee summary table"</ref>
  </references>

  <context>
    Conditional TO — only fires if INFFIN.025 Phase 1 confirms rate-emit-gap on platinum books artifact. Andrew said "clearly we know the rates" — so source has rate; if emit doesn't include rate, gold script augment needed.

    Per CLAUDE.md Rule 13+14+15: DS owns commit→QA-deploy cycle; ds-commit-gate.sh + `from __future__ import annotations`.
  </context>

  <objective>
    Augment Inflection books gold script emit to include account-level rate fields (Fee/Total bps/Split bps). FE consumer (INFFIN.025 Phase 3 Path B) wires post this RAVC.
  </objective>

  <scope>
    <files>
      <file action="modify">data/orion/scripts/gold/{Inflection books gold script} — augment emit with rate fields</file>
      <file action="readonly_reference">source rate data location (per INFFIN.025 Phase 1 investigation finding)</file>
    </files>
  </scope>

  <phase id="1" when="implementation">
    <step>
      <run>Augment Inflection books gold script: emit Fee / Total(bps) / Split(bps) per account; preserve existing emit fields</run>
      <expect>Gold script delta ~30-50 LOC; rate fields emitted; sentinel _meta extended.</expect>
    </step>
    <step>
      <run>ds-commit-gate.sh: py_compile + ds-precommit-check.py + ruff py39 0.15.11</run>
      <expect>All 3 PASS.</expect>
    </step>
  </phase>

  <phase id="2" when="commit + deploy">
    <step>
      <run>safe-deploy.sh per Rule 13: commit → push → S3 upload → comp-pipescript deployed MATCH</run>
      <expect>SHA-MATCH; deploy clean.</expect>
    </step>
    <step>
      <run>SSM dispatch re-run; verify platinum Inflection books artifact now includes rate fields</run>
      <expect>Empirical rate emit verification PASS.</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + RD 0.4.2 (INFFIN.025 Phase 3 Path B consumer) + DT 0.4</run>
      <expect>Evidence-bearing close.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: Gold script emits Fee/Total(bps)/Split(bps) per account
    AC2: Existing emit fields preserved (no regression)
    AC3: 49F regression PASS (same gold script may serve both partners; verify Inflection-specific addition doesn't leak)
    AC4: ds-commit-gate.sh PASS
    AC5: safe-deploy.sh PASS + S3 upload + comp-pipescript deployed MATCH
    AC6: SSM re-run + empirical platinum verification
    AC7: No emoji per CLAUDE.md
    AC8: RAVC2 to COO + CC CTO + RD 0.4.2 + DT 0.4
  </acceptance_criteria>

  <compiler_tools_mandate>ds-commit-gate.sh + safe-deploy.sh per Rule 13+14.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: ADVI_INFFIN.025 Phase 1 Path B confirmation.
    PARALLEL-OK: All other INFFIN.019-028 sibs (independent gold script edit).
    DOWNSTREAM: INFFIN.025 Phase 3 Path B consumer wires post this RAVC.
    DS SUB-AGENT ROUTING: route at conditional dispatch time per bench-clear state.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <reprocess_scope>Inflection books artifact re-emit current-date forward + 1-day backfill.</reprocess_scope>
  </data_reprocess_scope>

  <deliverables>
    1. Gold script rate emit augment
    2. ds-commit-gate + safe-deploy + S3 SHA-MATCH
    3. Platinum verification
    4. RAVC2
  </deliverables>

  <ravc>DS RAVC2 to COO + CC CTO + RD 0.4.2 + DT 0.4 on AC1-8 PASS.</ravc>

  <notes>
    **Author identity:** sub-agent route at conditional dispatch; `--author="0.4.0_DS_ClientPlatform~? <0.4.0_DS_ClientPlatform~?@opal.agent>"`.

    **Conditional-fire:** if INFFIN.025 Phase 1 finds rate already emitted (Path A), this TO is superseded — set status=superseded with deletion note.

    **No emoji per CLAUDE.md.**
  </notes>
</task_order>
