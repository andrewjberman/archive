<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.SEED-BD</id>
    <project>ADHC_COMPIL_V4</project>
    <title>Marker constant inventory — BD pipeline (allowlist seed for comp-constants)</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>pending</status>
    <priority>medium</priority>
    <estimated_effort>~30-60 min</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §3 row 3 + §4 TO-3</ref>
    <ref type="parent_to">ADHC_COMPIL_V4.003 (AE 0.7 — comp-constants new tool, queued)</ref>
    <ref type="anchor_incident">INFNNA Joe Brandenburg attribution 2026-05-07 — INFLECTION_REP_IDS rep_id=6 missing from 8+ files; manual coordinated sync</ref>
  </references>

  <context>
    AE 0.7's TO-3 (comp-constants new tool) needs an allowlist + canonical-value config. The PRD §3 row 3 lists a starter set (~6 constants) but a comprehensive inventory will let AE ship TO-3 with a richer day-1 config and full drift-detection coverage.

    This is parallel pre-work: produce a structured YAML inventory of BD-pipeline marker constants. AE 0.7 consumes it when authoring `comp-constants.config.yaml`. No code changes; pure inventory.

    Three SEED TOs run in parallel: SEED-BD (this), SEED-INF (DS~C, Inflection-side), SEED-MULTIFIRM (DS~D, shared/edge). Together they feed TO-3.

    Marker constant = ALL_UPPER_SNAKE_CASE module-level constant representing firm/cohort identifiers, ID lists, threshold bounds, allowlists, blacklists, or feature flags. Examples: `BD_FIRM_TAG`, `BD_REP_IDS`, `INFGRD_FIRM_AUA_LOWER`, `BLACKLIST_REP_IDS`. NOT marker: utility constants like `BUFFER_SIZE`, `DEFAULT_TIMEOUT`, `RETRY_LIMIT`.
  </context>

  <scope>
    <step>
      Search surfaces (BD-side + BD-shared + companion pipelines you touch):
      - `data/black_diamond/scripts/{bronze,silver,gold}/**/*.py`
      - `infra/aws/lambda/bd-pipeline/**/*.py`
      - `infra/aws/lambda/bd-*/**/*.py` (any other bd-prefixed Lambda dirs)
      - Any orphan BD config files under `data/black_diamond/`

      Use Grep with pattern `^[A-Z][A-Z0-9_]+ *=` to surface candidate constants.
    </step>

    <step>
      Triage candidates: keep only marker constants (firm/cohort/threshold/allowlist/blacklist semantics). Skip utility constants. Record borderline cases in YAML notes.
    </step>

    <step>
      Produce YAML at `org/modules/graph/comp-constants-seed-bd.yaml` in this format:

      ```yaml
      # Auto-seeded by ADHC_COMPIL_V4.SEED-BD (DS~B 2026-05-08)
      # Consumed by ADHC_COMPIL_V4.003 (comp-constants tool authoring)
      lane: bd
      constants:
        - name: BD_FIRM_TAG
          type: string
          canonical_value: '"black_diamond"'
          sites:
            - file: data/black_diamond/scripts/silver/_bd_silver_lib.py
              line: 42
              value: '"black_diamond"'
              comment: "BD_FIRM_TAG = \"black_diamond\""
            - file: ...
          notes: "Used in S3 prefix construction + firm-routing predicates"
        - name: BD_REP_IDS
          type: set
          canonical_value: "{...}"
          sites: [...]
          notes: "..."
      ```

      For each constant: canonical_value (the most-common or designated-canonical value); site list (file:line:value:comment); notes if drift exists or there's a sister-constant relationship.
    </step>

    <step>
      Pre-commit gate: `.tools/ds-commit-gate.sh org/modules/graph/comp-constants-seed-bd.yaml` (or equivalent — YAML-only file, no py_compile needed; just confirm ds-precommit-check passes).
    </step>

    <step>
      Commit + push. `safe-commit.sh --author "0.4.0_DS_ClientPlatform~B <0.4.0_DS_ClientPlatform~B@opal.agent>" -m "feat(ADHC_COMPIL_V4.SEED-BD): BD-pipeline marker constant allowlist seed" -- org/modules/graph/comp-constants-seed-bd.yaml`
    </step>
  </scope>

  <acceptance_criteria>
    1. YAML committed at `org/modules/graph/comp-constants-seed-bd.yaml`.
    2. ≥ 5 marker constants inventoried (comprehensive — not just starter set).
    3. Each constant has ≥ 1 site (file + line + literal value + comment context).
    4. Drift flagged in YAML notes if any constant has divergent values across sites.
    5. Pre-commit gate PASS.
    6. Session log includes Compiler Tools section reproducing each `<run>` from `<compiler_tools_mandate>` with observed output and pass/fail vs `<expect>`.
    7. RAVC2 to COO with: commit SHA, constant count, site count, any drift findings.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Grep -rn "^[A-Z][A-Z0-9_]+ *=" data/black_diamond/scripts/ infra/aws/lambda/bd-pipeline/ --type py 2>&amp;1 | head -50</run>
        <expect>≥10 candidate ALL_UPPER_SNAKE_CASE assignments surfaced for triage. If fewer, broaden glob to `infra/aws/lambda/bd-*/`.</expect>
        <if_mismatch>If &lt;5 results: search wider (include data/orion/scripts/ for BD-shared); if 0: check shell quoting / report to COO.</if_mismatch>
      </step>
      <step>
        <run>Grep -rn "BD_FIRM_TAG\|BD_REP_IDS\|INFGRD_FIRM_AUA" data/ infra/aws/lambda/ --type py</run>
        <expect>Confirms PRD-cited starter constants appear in BD codebase; baseline check before YAML construction.</expect>
        <if_mismatch>If 0 results, the starter set is misnamed; surface to COO before authoring YAML.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>python -c "import yaml; d=yaml.safe_load(open('org/modules/graph/comp-constants-seed-bd.yaml')); print(f'lane={d[\"lane\"]} constants={len(d[\"constants\"])} sites={sum(len(c[\"sites\"]) for c in d[\"constants\"])}')"</run>
        <expect>lane=bd; constants ≥5; sites ≥10 (most marker constants appear at multiple sites).</expect>
        <if_mismatch>If constants &lt;5: re-scan for missed candidates. If sites &lt;= constants: likely missed multi-site coverage; re-grep each constant name.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    None. Parallel-dispatchable with SEED-INF (DS~C) + SEED-MULTIFIRM (DS~D) + AE TO-3.
  </dependencies>
</task_order>
