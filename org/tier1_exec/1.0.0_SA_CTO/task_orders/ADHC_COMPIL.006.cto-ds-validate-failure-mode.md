<task_order>
  <metadata>
    <id>ADHC_COMPIL.006.cto-ds-validate-failure-mode</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>1.0.0_SA_CTO</issued_to><!-- primary: protocol doc + CLAUDE.md -->
    <co_implementer>0.4.0_DS_ClientPlatform</co_implementer><!-- gold_validate_config.yaml inline docs -->
    <date>2026-04-27</date>
    <status>in_progress</status>
    <ravc4_cto>2026-04-29 — AC1 (COMP_VALIDATE_PROTOCOL.md) + AC3 (CLAUDE.md) shipped by 1.0.0_SA_CTO. Awaiting AC2 (gold_validate_config.yaml inline header docs) from 0.4.0_DS_ClientPlatform~B per Andrew lane assignment.</ravc4_cto>
    <project_code>ADHC_COMPIL</project_code>
    <theme>E (v2)</theme>
    <prd_ref>docs/architecture/ADHC_COMPIL_V2.md §3 (commit 653b0469)</prd_ref>
    <effort>1 week</effort>
    <gates_on>ADHC_COMPIL.003 COMPLETE — protocol doc must land in same authoring
    discipline/template as Theme C establishes</gates_on>
    <gates_for>ADHC_COMPIL.007 (Theme E stretch CLI hint)</gates_for>
  </metadata>

  <objective>
    Document comp-validate failure-mode semantics and retry policy. The tool
    works; the operator docs around what to do when it fails are thin.
    Operators currently ad-hoc WARN vs ERROR distinctions, retry decisions,
    and escalation paths — creating inconsistent handling and occasional
    false-negative signal-AE decisions.
  </objective>

  <scope>
    CTO deliverables (primary):

    1. docs/architecture/COMP_VALIDATE_PROTOCOL.md
       - Exit code semantics: 0 = pass, non-zero = fail; WARN-only fail vs ERROR fail
       - Retry policy: when to re-run the gold script, when to fix validator config,
         when to escalate
       - WARN vs ERROR distinction with worked examples from gold_validate_config.yaml
       - "Safe to signal AE" decision tree based on validator output
       - Escalation path for false-positive validator configs (DS owns config,
         change with PR review, re-run validate post-change)
       - ≥3 worked examples using real incidents (reference ADVI_STAUDT.COHORT-A
         6P/0E/2W account_count warning, and any other session logs)

    2. CLAUDE.md compiler tools table
       - Replace current single line "Must exit 0 before signaling" for comp-validate
         with a brief reference to COMP_VALIDATE_PROTOCOL.md + one-line decision rule
         for the most common case

    DS deliverable (co-implementer):

    3. gold_validate_config.yaml inline header docs (10-20 lines)
       - Schema docs: threshold format, severity level keys (WARN/ERROR),
         config shape, how to add a new validation rule
       - DS to submit these inline docs in a separate commit / DS PR
       - ds-commit-gate.sh required if any .py file is touched

  </scope>

  <acceptance_criteria>
    1. docs/architecture/COMP_VALIDATE_PROTOCOL.md exists with:
       - Retry policy
       - WARN/ERROR semantics clearly distinguished
       - "Safe to signal AE" decision tree
       - Escalation path for false-positive configs
       - ≥3 worked examples
    2. gold_validate_config.yaml has 10-20 line inline header docs covering
       threshold format, severity levels, and config schema.
    3. CLAUDE.md compiler tools table comp-validate line updated to reference
       COMP_VALIDATE_PROTOCOL.md with one-line decision rule.
    4. (Optional stretch — defer to ADHC_COMPIL.007) comp-validate CLI prints
       one-line hint on non-zero exit: "Hint: see COMP_VALIDATE_PROTOCOL.md §3
       for retry policy".
  </acceptance_criteria>

  <split_responsibility>
    CTO: AC1 (COMP_VALIDATE_PROTOCOL.md) + AC3 (CLAUDE.md update)
    DS 0.4.0: AC2 (gold_validate_config.yaml inline docs)
    Coordination: CTO ships AC1+AC3 first; DS adds AC2 in follow-on commit.
    Both RAVC4 to COO when their portion is complete.
  </split_responsibility>

  <do_not>
    <rule>Do NOT expand scope to other comp-* tools' failure modes — comp-validate only.
    Other tools get a separate ADHC_COMPIL v3 if needed.</rule>
    <rule>Do NOT start before ADHC_COMPIL.003 is complete — new protocol doc must use
    the PRD_AUTHORING_PROTOCOL.md discipline for consistency.</rule>
  </do_not>

  <deliverables>
    <deliverable type="document">docs/architecture/COMP_VALIDATE_PROTOCOL.md</deliverable>
    <deliverable type="code">CLAUDE.md compiler tools table update</deliverable>
    <deliverable type="code">gold_validate_config.yaml inline header docs (DS portion)</deliverable>
    <deliverable type="ravc">CTO RAVC4 to 2.0.0_SA_COO when AC1+AC3 complete</deliverable>
    <deliverable type="ravc">DS RAVC4 to 2.0.0_SA_COO when AC2 complete</deliverable>
  </deliverables>
</task_order>
