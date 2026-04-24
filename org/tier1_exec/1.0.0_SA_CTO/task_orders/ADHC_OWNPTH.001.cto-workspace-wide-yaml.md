<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <id>2.0.0_SA_COO-2026-04-24-adhc-ownpth-001-cto-workspace-wide-yaml</id>
  <project>ADHC_OWNPTH</project>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_to>1.0.0_SA_CTO</issued_to>
  <issued_date>2026-04-24</issued_date>
  <status>complete <!-- 1.0.0_SA_CTO bbf990dc 2026-04-24: .owned-paths.yaml committed; 15 lanes, 70+ rules, 0 MISSING; YAML parse OK --></status>

  <title>ADHC_OWNPTH TO 1 — Workspace-wide .owned-paths.yaml authoring</title>

  <references>
    <ref type="prd">docs/architecture/ADHC_OWNPTH.md</ref>
    <ref type="draft">org/tier1_exec/1.1.0_SA_CTO/drafts/owned_paths_comp_learns_half.yaml (COMP_LEARNS-half; merge base if present in feature_clb worktree)</ref>
  </references>

  <context>
    ADHC_OWNPTH was chartered to structurally prevent cross-lane git-sweep incidents via a
    pre-commit hook. Four incidents in two weeks (7ae0ef6b / c6285ae8 / 2b3bfcd4 / abfed84d
    triplet) occurred with all cultural guardrails in force. Andrew directive 2026-04-22:
    "propose owned-paths pre-commit hook, not more rules." PRD authored by 1.0.0_SA_CTO on
    2026-04-24 (docs/architecture/ADHC_OWNPTH.md).

    TO 1 is the YAML-authoring phase. The YAML declares path ownership; TO 2 (DS) codes the
    hook against this schema; TO 3 (AE) wires it. Nothing downstream can proceed without the
    YAML. Draft COMP_LEARNS-half may exist in the feature_clb worktree — merge verbatim if
    available; otherwise reconstruct from §6.1 schema in the PRD + git ls-files enumeration.
  </context>

  <scope>
    Author `.owned-paths.yaml` at repo root (ajb_workspace/). Schema per PRD §6.1.

    Required coverage:
    1. Every agent lane: BASE_EXEC (1.0.0_SA_CTO + 2.0.0_SA_COO), COMP_LEARNS
       (1.1.0_SA_CTO + 2.1.0_SA_COO + 1.1.0_DS_CompLearns, SC), POD4 (DE/DT/DS/DS~A/DS~B),
       SHARED_CLOUD_OPS (0.7.0_AE_CloudOps), SHARED_PARTNER_ETL (0.5.0_AE_OpalETL +
       0.6.0_AE_PartnerETL + 0.6.1_AE_PartnerETL), SHARED_MARKET_INTEL (0.1.0_DT_*),
       ANY_EXEC (both CTOs + both COOs — cross-lane authorized writes), ANY (intentionally
       multi-agent-writable paths).

    2. Every top-level path group from `git ls-files | awk -F/ '{print $1"/"$2}' | sort -u`:
       - org/tier1_exec/**, org/tier2_senior/**, org/projects/**, org/modules/**
       - data/black_diamond/scripts/**, data/orion/scripts/**
       - infra/aws/**, infra/aws/ec2/EC2_MANIFEST.json (AE 0.7.0 owns)
       - portal/** (Any DE can write; DT pushes)
       - docs/architecture/** (ANY_CTO), docs/deployment/** (BASE_EXEC)
       - .tools/** (ANY — shared tooling), comp/** (COMP_LEARNS)
       - CLAUDE.md, org/XXX.md (BASE_EXEC only)
       - org/compiler-tools-log.md, org/git-author-override-audit.log (ANY)
       - org/projects/REGISTRY.md (ANY_EXEC), org/projects/*.json (ANY_EXEC)
       - memory/** (ANY — shared workspace memory)

    3. Unmapped path handling: lane UNDEFINED. Phase 1 (warn-mode) → WARN + audit log entry.
       Phase 2 (block-mode) → EXIT 1. Include a comment block at YAML top explaining this.

    4. Merge the COMP_LEARNS-half draft verbatim if accessible; use it as the COMP_LEARNS
       lane definition source of truth. If not accessible from ajb_workspace, reconstruct
       from the PRD §6.1 schema.

    5. Add YAML header with version, date, authoring agent, and rollout phase field
       (default: 1 = warn-mode). The hook reads this to determine behavior.

    Do NOT implement the hook script (TO 2 scope). Do NOT modify .git/hooks/ (TO 3 scope).
    YAML only.
  </scope>

  <dependencies>
    <dependency agent="None" status="none" required="No upstream TOs. TO 1 is the root of the gate chain."/>
  </dependencies>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>git ls-files | awk -F/ '{print $1"/"$2}' | sort -u</run>
        <expect>Complete list of top-level path groups in the repo. Every output line must have a YAML rule. Document this list in session log.</expect>
        <if_mismatch>STOP. Every top-level path group must have coverage.</if_mismatch>
      </step>
      <step>
        <run>find org/tier1_exec -maxdepth 1 -type d; find org/tier2_senior -maxdepth 1 -type d</run>
        <expect>Full list of agent home directories (lane candidates). Every directory must be represented in YAML lanes.</expect>
        <if_mismatch>STOP. Missing agent lane in YAML = that agent can commit to any path without a warning.</if_mismatch>
      </step>
      <step>
        <run>cat org/tier1_exec/1.1.0_SA_CTO/drafts/owned_paths_comp_learns_half.yaml 2>/dev/null || echo "DRAFT NOT FOUND — reconstruct from PRD schema"</run>
        <expect>Either: existing 232-line COMP_LEARNS-half draft content (merge verbatim as COMP_LEARNS lane block), or "DRAFT NOT FOUND" (reconstruct from PRD §6.1). Document which path taken.</expect>
        <if_mismatch>NOTE only (not a blocker). Reconstruct if draft absent.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python3 -c "import yaml; yaml.safe_load(open('.owned-paths.yaml'))" 2>&amp;&amp; echo "YAML PARSE OK"</run>
        <expect>Exit 0 + "YAML PARSE OK". No syntax errors.</expect>
        <if_mismatch>STOP. Fix YAML syntax before committing.</if_mismatch>
      </step>
      <step>
        <run>git ls-files | awk -F/ '{print $1"/"$2}' | sort -u | while read p; do grep -q "$p" .owned-paths.yaml &amp;&amp; echo "OK: $p" || echo "MISSING: $p"; done</run>
        <expect>Zero MISSING lines. Every tracked path group has a rule.</expect>
        <if_mismatch>STOP. Add missing path rules before committing.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>.tools/owned-paths-validate.py .owned-paths.yaml (if TO 2 has shipped; skip if not yet available)</run>
        <expect>Exit 0 when available. If TO 2 not yet shipped, note N/A and confirm validation when TO 2 completes.</expect>
        <if_mismatch>Surface validation errors to 2.0.0_SA_COO before declaring TO 1 complete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    1. `.owned-paths.yaml` exists at repo root, committed under 1.0.0_SA_CTO author.
    2. YAML schema matches PRD §6.1: lanes block + paths block + rollout_phase field.
    3. Every top-level path group from `git ls-files` enumeration has a rule (zero MISSING).
    4. Every agent home directory has a corresponding lane entry.
    5. COMP_LEARNS-half merged verbatim (or reconstructed if draft absent — document which).
    6. YAML parses without error: `python3 -c "import yaml; yaml.safe_load(...)"` exit 0.
    7. Unmapped path handling documented in YAML header comment.
    8. Session log includes compiler tools section with all Phase 1-3 runs + observed outputs.
    9. MCP COO with commit hash on completion. Note: MCP must cite at minimum 3 lane examples
       from the YAML that cover the known incident paths (org/tier1_exec/1.1.0_SA_CTO/,
       infra/aws/, data/black_diamond/scripts/).
  </acceptance_criteria>

  <evidence>
    <!-- To be filled by CTO on completion -->
  </evidence>
</task_order>
