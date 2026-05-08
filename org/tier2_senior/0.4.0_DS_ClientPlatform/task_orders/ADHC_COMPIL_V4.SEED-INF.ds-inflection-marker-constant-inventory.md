<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.SEED-INF</id>
    <project>ADHC_COMPIL_V4</project>
    <title>Marker constant inventory — Inflection pipeline (allowlist seed for comp-constants)</title>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>complete</status><!-- shipped 14a5474d5 (COO override-commit, DS~C author preserved); 9 constants, 33 sites, 3 drift flags -->
    <priority>medium</priority>
    <estimated_effort>~30-60 min</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §3 row 3 + §4 TO-3</ref>
    <ref type="parent_to">ADHC_COMPIL_V4.003 (AE 0.7 — comp-constants new tool, queued)</ref>
    <ref type="anchor_incident">INFNNA Joe Brandenburg attribution 2026-05-07 — INFLECTION_REP_IDS rep_id=6 missing from 8+ files; manual coordinated sync. PRD §5: Grep INFLECTION_REP_IDS workspace-wide returned 30+ files (limit hit).</ref>
  </references>

  <context>
    AE 0.7's TO-3 (comp-constants new tool) needs an allowlist + canonical-value config. The Inflection pipeline has the highest density of marker constants in the codebase (PRD §5 evidence: INFLECTION_REP_IDS appears in 30+ files). Comprehensive inventory will let AE ship TO-3 with a richer day-1 config and full drift-detection coverage for the lane that needs it most.

    This is parallel pre-work: produce a structured YAML inventory of Inflection-pipeline marker constants. AE 0.7 consumes it when authoring `comp-constants.config.yaml`. No code changes; pure inventory.

    Three SEED TOs run in parallel: SEED-BD (DS~B), SEED-INF (this), SEED-MULTIFIRM (DS~D). Together they feed TO-3.

    Marker constant = ALL_UPPER_SNAKE_CASE module-level constant representing firm/cohort identifiers, ID lists, threshold bounds, allowlists, blacklists, or feature flags. Examples: `INFLECTION_REP_IDS`, `INFLECTION_FIRM_TAG`, `INFGRD_FIRM_AUA_LOWER`, `INFLECTION_REP_NAMES_BLACKLIST`. NOT marker: utility constants like `BUFFER_SIZE`, `RETRY_LIMIT`.

    **Special drift attention:** INFLECTION_REP_IDS canonical post-INFNNA.001 fix is `{3, 6, 11, 12}`. Some sites may still show old `[3, 11, 12]` (not yet propagated; per session-end summary: `pull_inflection_assets.py:53` + `create_tax_dim_queries.py:45` + `pull_inflection_transactions.py` (v1) still OLD). Flag every drift site.
  </context>

  <scope>
    <step>
      Search surfaces:
      - `data/orion/scripts/{bronze,silver,gold}/**/*.py`
      - `data/orion/manual_api/**/*.py`
      - `infra/aws/lambda/inf-pipeline/**/*.py`
      - Any inf-* directories or scripts referenced from Lambda source map.

      Use Grep with pattern `^[A-Z][A-Z0-9_]+ *=` to surface candidate constants.
    </step>

    <step>
      Triage candidates: keep only marker constants. Skip utility constants. Record borderline cases in YAML notes.
    </step>

    <step>
      Produce YAML at `org/modules/graph/comp-constants-seed-inf.yaml` in this format:

      ```yaml
      # Auto-seeded by ADHC_COMPIL_V4.SEED-INF (DS~C 2026-05-08)
      # Consumed by ADHC_COMPIL_V4.003 (comp-constants tool authoring)
      lane: inf
      constants:
        - name: INFLECTION_REP_IDS
          type: set
          canonical_value: "{3, 6, 11, 12}"
          sites:
            - file: data/orion/scripts/silver/_orion_api_silver_lib.py
              line: 36
              value: "{3, 6, 11, 12}"
              comment: "INFLECTION_REP_IDS = {3, 6, 11, 12}  # canonical post-INFNNA.001"
            - file: data/orion/manual_api/pull_inflection_assets.py
              line: 53
              value: "[3, 11, 12]"
              comment: "OLD — drift; not yet updated"
              drift: true
          notes: "rep_id=6 (Joe Brandenburg) added 2026-05-07 INFNNA.001 fix. Drift sites still on old [3,11,12]."
      ```

      For each constant: canonical_value; site list (file:line:value:comment, drift:true if value differs from canonical); notes if drift exists or related-constants exist.
    </step>

    <step>
      Pre-commit gate: `.tools/ds-commit-gate.sh org/modules/graph/comp-constants-seed-inf.yaml`.
    </step>

    <step>
      Commit + push. `safe-commit.sh --author "0.4.0_DS_ClientPlatform~C <0.4.0_DS_ClientPlatform~C@opal.agent>" -m "feat(ADHC_COMPIL_V4.SEED-INF): Inflection-pipeline marker constant allowlist seed" -- org/modules/graph/comp-constants-seed-inf.yaml`
    </step>
  </scope>

  <acceptance_criteria>
    1. YAML committed at `org/modules/graph/comp-constants-seed-inf.yaml`.
    2. ≥ 5 marker constants inventoried (PRD §5 evidence suggests this lane has 6+ candidates incl Cottonwood placeholders).
    3. Each constant has ≥ 1 site (file + line + literal value + comment context).
    4. **All INFLECTION_REP_IDS drift sites explicitly flagged with `drift: true`** (catch the rep_id=6 propagation gap surfaced in INFNNA.001).
    5. Pre-commit gate PASS.
    6. Session log includes Compiler Tools section reproducing each `<run>` from `<compiler_tools_mandate>` with observed output and pass/fail vs `<expect>`.
    7. RAVC2 to COO with: commit SHA, constant count, site count, drift count + list.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Grep -rn "^[A-Z][A-Z0-9_]+ *=" data/orion/scripts/ data/orion/manual_api/ infra/aws/lambda/inf-pipeline/ --type py 2>&amp;1 | head -50</run>
        <expect>≥15 candidate ALL_UPPER_SNAKE_CASE assignments surfaced for triage (Inflection lane is dense per PRD §5 evidence).</expect>
        <if_mismatch>If &lt;10: broaden to include `data/orion/scripts/` subtree fully + check ssm/eb dispatch scripts.</if_mismatch>
      </step>
      <step>
        <run>Grep -rn "INFLECTION_REP_IDS" --type py</run>
        <expect>≥8 files matched (per PRD §5 grep evidence — 30+ files limit-hit; concentrated in py).</expect>
        <if_mismatch>If &lt;5: grep is broken or PRD evidence stale; surface to COO.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>python -c "import yaml; d=yaml.safe_load(open('org/modules/graph/comp-constants-seed-inf.yaml')); drift=sum(1 for c in d['constants'] for s in c['sites'] if s.get('drift')); print(f'lane={d[\"lane\"]} constants={len(d[\"constants\"])} sites={sum(len(c[\"sites\"]) for c in d[\"constants\"])} drift={drift}')"</run>
        <expect>lane=inf; constants ≥5; sites ≥15; drift ≥1 (INFLECTION_REP_IDS old [3,11,12] sites still present per session-summary).</expect>
        <if_mismatch>If drift=0: re-check pull_inflection_assets.py + create_tax_dim_queries.py + any remaining v1 transaction puller — these are known drift sites.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    None. Parallel-dispatchable with SEED-BD (DS~B) + SEED-MULTIFIRM (DS~D) + AE TO-3.
  </dependencies>
</task_order>
