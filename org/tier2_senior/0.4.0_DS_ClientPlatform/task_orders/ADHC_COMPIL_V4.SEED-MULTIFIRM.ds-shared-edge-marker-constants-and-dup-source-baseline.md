<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.SEED-MULTIFIRM</id>
    <project>ADHC_COMPIL_V4</project>
    <title>Multi-firm/shared/edge marker constants + Lambda dup-source baseline (TO-3 + TO-4 seed)</title>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>pending</status>
    <priority>medium</priority>
    <estimated_effort>~45-75 min</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §3 row 3 + row 4 + §4 TO-3 + TO-4</ref>
    <ref type="parent_to_1">ADHC_COMPIL_V4.003 (AE 0.7 — comp-constants new tool, queued)</ref>
    <ref type="parent_to_2">ADHC_COMPIL_V4.004 (AE 0.7 — comp-shell dup-source mode, queued)</ref>
    <ref type="anchor_incident_1">FIRM_BUCKET_MAP duplicated in 2 Lambda@Edge files (TODO "extract once >2 partners" — Cottonwood = trigger)</ref>
    <ref type="anchor_incident_2">ROUTER-DRIFT 2026-05-07 — false drift: stale `lambda/shared-advisor-router/index.mjs` v1 alongside canonical `lambda-edge/shared-advisor-router/index.mjs` v13</ref>
  </references>

  <context>
    Two parallel feeds for two AE 0.7 TOs:

    **(a) Multi-firm + edge marker constant inventory** for AE TO-3 (comp-constants):
    Inflection (DS~C SEED-INF) + BD (DS~B SEED-BD) cover script-side; this TO covers shared infrastructure: Lambda@Edge JS/TS sources, shared/portal-* Python Lambdas, FIRM_CONFIG / FIRM_BUCKET_MAP scope. This is where the Cottonwood readiness work needs the most coverage.

    **(b) Lambda dup-source baseline inventory** for AE TO-4 (comp-shell dup-source):
    PRD §5 evidence says current repo is post-FIRMSEP.05 clean (no dup-source candidates). TO-4 ships dup-source-detection lint and needs a "current clean state" baseline to validate against (zero false-positive gate). This TO produces that baseline + identifies any near-miss patterns AE can use for unit tests.

    Both produce YAML/JSON outputs in `org/modules/graph/`. No code changes. AE consumes when authoring TO-3 + TO-4.
  </context>

  <scope>
    <step>
      **Part A — Multi-firm + edge constant scan.**

      Search surfaces (JS/TS + Python):
      - `infra/aws/lambda-edge/**/*.{mjs,js,ts}`
      - `infra/aws/lambda/shared-*/**/*.py`
      - `infra/aws/lambda/portal-*/**/*.{py,mjs,js}`
      - `infra/aws/lambda/auth-validator-edge/**/*.{mjs,js}`
      - `infra/aws/lambda/shared-advisor-router/**/*.{mjs,js}` (canonical lambda-edge path)
      - `portal/src/lib/firmAccess.ts` + any portal-side firm-routing constants

      Use Grep for `(const|let|export const) [A-Z][A-Z0-9_]+ *=` (JS/TS) AND `^[A-Z][A-Z0-9_]+ *=` (Python).
    </step>

    <step>
      Triage marker candidates. Focus on:
      - `FIRM_BUCKET_MAP`, `FIRM_CONFIG`, `FIRM_REGISTRY` (multi-firm routing tables)
      - Cottonwood placeholders if any
      - Bucket name constants (`opal-data-{bd,inf,cottonwood}`)
      - Edge-routing tier maps
      - Auth tier/scope enumerations
      - Any const arrays/sets used in firm-allowlist gates

      Skip utility constants (CACHE_TTL_MS, MAX_RETRIES, etc.).
    </step>

    <step>
      Produce YAML at `org/modules/graph/comp-constants-seed-multifirm.yaml`:

      ```yaml
      # Auto-seeded by ADHC_COMPIL_V4.SEED-MULTIFIRM (DS~D 2026-05-08)
      # Consumed by ADHC_COMPIL_V4.003 (comp-constants tool authoring)
      lane: multifirm
      constants:
        - name: FIRM_BUCKET_MAP
          type: object
          canonical_value: "{black_diamond: opal-data-bd, inflection: opal-data-inf}"
          sites:
            - file: infra/aws/lambda-edge/shared-advisor-router/index.mjs
              line: ...
              value: ...
              language: js
            - file: ...
          notes: "TODO 'extract once >2 partners' from FIRMSEP.03 plan; Cottonwood = trigger"
      ```

      Same site format as SEED-BD/SEED-INF. Add `language` field on sites since this lane spans Python + JS/TS.
    </step>

    <step>
      **Part B — Lambda dup-source baseline scan.**

      Search for any source file appearing under multiple Lambda root paths:
      - Pattern: same basename + similar content under both `infra/aws/lambda/<service>/` AND `infra/aws/lambda-edge/<service>/`
      - Also: `_lib.py` / `index.mjs` / `index.py` patterns appearing across multiple Lambda dirs
      - Identify: silver/gold scripts bundled into Lambda dirs that ALSO exist canonically under `data/*/scripts/`

      Use Glob `infra/aws/lambda{,-edge}/*/index.*` and `infra/aws/lambda/*/_*.py` to surface candidates. Then for each duplicated basename, compute SHA + report.
    </step>

    <step>
      Produce JSON at `org/modules/graph/comp-shell-dup-source-baseline.json`:

      ```json
      {
        "scan_date": "2026-05-08",
        "scan_root_paths": [
          "infra/aws/lambda/",
          "infra/aws/lambda-edge/",
          "data/black_diamond/scripts/",
          "data/orion/scripts/"
        ],
        "duplicate_candidates": [
          {
            "basename": "shared-advisor-router/index.mjs",
            "paths": [
              {"path": "infra/aws/lambda-edge/shared-advisor-router/index.mjs", "sha": "...", "size": 12345, "canonical": true},
              {"path": "infra/aws/lambda/shared-advisor-router/index.mjs", "sha": "...", "size": 543, "canonical": false, "comment": "stale post-FIRMSEP.05 cleanup; should not exist"}
            ],
            "status": "clean | flagged | needs_investigation"
          }
        ],
        "lambda_bundled_silver_gold": [
          {
            "lambda_dir": "infra/aws/lambda/inf-pipeline/inf-silver-chain/",
            "bundled_scripts": ["convert_orion_api_to_silver.py", "_orion_api_silver_lib.py"],
            "canonical_paths": ["data/orion/scripts/silver/convert_orion_api_to_silver.py", "data/orion/scripts/silver/_orion_api_silver_lib.py"],
            "drift_check": "compare SHA — out of scope for this baseline (TO-1 territory)"
          }
        ],
        "notes": "Per PRD §5 evidence Glob: post-FIRMSEP.05 cleanup landed; expect zero flagged duplicates."
      }
      ```

      Set `status: clean` for entries where current state matches PRD §5 evidence (no actual duplication problem). Set `status: flagged` if any unexpected dup is surfaced.
    </step>

    <step>
      Pre-commit gate: `.tools/ds-commit-gate.sh` on both files.
    </step>

    <step>
      Commit + push. `safe-commit.sh --author "0.4.0_DS_ClientPlatform~D <0.4.0_DS_ClientPlatform~D@opal.agent>" -m "feat(ADHC_COMPIL_V4.SEED-MULTIFIRM): multi-firm constant seed + dup-source baseline" -- org/modules/graph/comp-constants-seed-multifirm.yaml org/modules/graph/comp-shell-dup-source-baseline.json`
    </step>
  </scope>

  <acceptance_criteria>
    1. YAML committed at `org/modules/graph/comp-constants-seed-multifirm.yaml` — ≥ 4 multi-firm/shared/edge marker constants (less dense than INF lane is fine).
    2. JSON committed at `org/modules/graph/comp-shell-dup-source-baseline.json` — duplicate_candidates surfaced + status classification.
    3. Each constant in YAML has ≥ 1 site with file:line:value:language.
    4. Lambda-bundled-silver/gold inventory section in JSON has ≥ 3 entries (inf-silver-chain + at least 2 BD-side equivalents).
    5. Pre-commit gates PASS.
    6. Session log Compiler Tools section reproduces each `<run>` with observed output + pass/fail.
    7. RAVC2 to COO: commit SHA, both files' contents summarized (constant counts, dup-source flagged count, lambda-bundled count).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Grep -rn "FIRM_BUCKET_MAP\|FIRM_CONFIG\|FIRM_REGISTRY" infra/aws/ portal/src/ 2>&amp;1 | head -30</run>
        <expect>≥3 file matches surfaced; FIRM_BUCKET_MAP is the most-cited per FIRMSEP.03 PRD evidence.</expect>
        <if_mismatch>If 0: check spelling / verify Grep glob coverage; surface to COO if structural miss.</if_mismatch>
      </step>
      <step>
        <run>Glob infra/aws/lambda{,-edge}/*/index.{mjs,js,py}</run>
        <expect>≥15 paths returned across both lambda/ and lambda-edge/ roots; basename collision candidates surface naturally.</expect>
        <if_mismatch>If &lt;5: glob is misspecified; broaden.</if_mismatch>
      </step>
      <step>
        <run>Glob infra/aws/lambda/inf-pipeline/*/_*.py</run>
        <expect>Several `_orion_api_silver_lib.py` + helper-lib copies surfaced — these are Lambda-bundled silver scripts (TO-1 territory; baseline-only here).</expect>
        <if_mismatch>If 0: scan misses inf-pipeline Lambda dirs; verify path spelling.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>python -c "import yaml,json; y=yaml.safe_load(open('org/modules/graph/comp-constants-seed-multifirm.yaml')); j=json.load(open('org/modules/graph/comp-shell-dup-source-baseline.json')); print(f'consts={len(y[\"constants\"])} dup_cands={len(j[\"duplicate_candidates\"])} lambda_bundled={len(j[\"lambda_bundled_silver_gold\"])}')"</run>
        <expect>consts ≥4; dup_cands ≥1; lambda_bundled ≥3.</expect>
        <if_mismatch>If under: re-scan; verify path coverage. dup_cands=0 is acceptable IF all paths classified `status: clean`.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    None. Parallel-dispatchable with SEED-BD (DS~B) + SEED-INF (DS~C) + AE TO-3 + AE TO-4.
  </dependencies>
</task_order>
