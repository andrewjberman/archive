<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-13-reborn-w6-001</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-13</date>
    <status>complete</status>
    <project_code>ADVI_REBORN</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_REBORN_LEADERBOARD_FEES_ROLES_FIX.md</ref>
    <ref type="project">org/projects/ADVI_REBORN.json</ref>
  </references>

  <objective>
    Wave 6-001 DS. Preserve per-role nested `fee_paying` and `no_fee` buckets on `platinum/firm/leaderboard.json` by updating `D_04.client_portal_summary.py`'s leaderboard assembly path. `D_00c.portal_leaderboard.py` already emits these buckets under `role_breakdown[role]`; D_04's `_LEADERBOARD_ROLE_FIELDS` currently trims them. Goal: frontend can compute the intersection of (feeView, selectedRoles) from the platinum artifact without falling back to the all-fee partition.
  </objective>

  <context>
    Andrew audit (Travis Penfield):
    | Fees | Roles | Displayed | Expected |
    |---|---|---:|---:|
    | Fee-Paying | Implementor off | 394M | <= 341M |

    Root cause: D_04 trims `role_breakdown` via `_LEADERBOARD_ROLE_FIELDS = ('aua','nna','inflows','outflows','account_count','client_count')`. `fee_paying` and `no_fee` sub-objects are dropped despite being present upstream in D_00c. Frontend `(data[feeView] ?? data)` fallback then silently reverts to the all-fee slice when those keys are missing.

    Fix is scoped to D_04's leaderboard emit only. No D_00c change (already correct). No other D_04 artifact changes.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing code):
    - `comp-trace employee_leaderboard --direction both --all` — confirm gold -> platinum path.
    - `comp-pipescript io D_04` — confirm writes include `platinum/firm/leaderboard.json` (COO pre-check: yes, terminal write).
    - Read current D_00c `role_breakdown` shape to confirm `fee_paying` + `no_fee` sub-object names and field set.

    Phase 2 (before committing):
    - Re-run `comp-pipescript io D_04` — no new writes/reads expected.
    - Sample regenerated `platinum/firm/leaderboard.json` locally; validate invariants:
      - For each role: `fee_paying.aua + no_fee.aua == role.aua` (within float tolerance).
      - For each role: `fee_paying.account_count + no_fee.account_count == role.account_count` where account_count applies.
    - Log any role lacking partitioned data (expected: none).

    Phase 3 (after commit + S3 upload):
    - Re-validate uploaded artifact at `s3://opal-data-bd/platinum/firm/leaderboard.json`.
    - Log one concrete advisor sample (Travis Penfield preferred) showing nested role fee buckets present and that `fee_paying` portion of `implementor` is nonzero.
    - Append every compiler run to `org/compiler-tools-log.md`.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>data/black_diamond/scripts/gold/D_04.client_portal_summary.py</shared_resource>
    <shared_resource>platinum/firm/leaderboard.json</shared_resource>
    <also_in_to>ADVI_REBORN.W6-002 (DE — consumes this artifact)</also_in_to>
    <last_write_owner>0.4.0_DS_ClientPlatform (this TO)</last_write_owner>
    <required_action>DS must ship + upload regenerated artifact before DE starts W6-002. DE waits for MCP signal with artifact path + Travis Penfield validation sample.</required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `platinum/firm/leaderboard.json` (S3) contains nested `fee_paying` and `no_fee` objects under each `role_breakdown[role]`.
    2. Travis Penfield's `QTD` or `YTD` row in the artifact exposes a nonzero `role_breakdown.implementor.fee_paying.aua` sub-slice.
    3. For every role: `fee_paying.aua + no_fee.aua == role.aua` within float tolerance; log explicit violations.
    4. Existing top-level `fee_breakdown` unchanged.
    5. DS session log records the exact artifact path, validation sample (JSON excerpt), and whether any role lacked partitioned data.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_04.client_portal_summary.py</file>
    </files>
  </scope>

  <requirements>
    - Scope strictly the leaderboard emit path (the `_LEADERBOARD_ROLE_FIELDS` trim and the `role_breakdown` build). Other D_04 artifacts untouched.
    - Follow standard DS deploy cycle: edit + commit + push + S3 upload + bd-gold-trigger (or scoped single-script run for D_04).
    - Do NOT widen the role payload beyond `fee_paying` + `no_fee` (no new metrics; preserve the existing sub-object schema from D_00c).
  </requirements>

  <deliverables>
    - Commit to CLOUD with `--author="0.4.0_DS_ClientPlatform <0.4.0_DS_ClientPlatform@opal.agent>"`.
    - S3 upload of regenerated `platinum/firm/leaderboard.json` via standard gold-trigger path.
    - Session log at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-13/reborn_w6_001_leaderboard_role_fee_buckets.md` with Compiler Tools section.
    - `org/compiler-tools-log.md` entries.
    - MCP message to 0.4.0_DE_ClientPlatform when uploaded artifact is validated (unblocks W6-002).
    - Flip `<status>complete</status>` -> `complete` after acceptance criteria validated.
  </deliverables>

  <do_not>
    - Do NOT modify D_00c — schema is correct upstream.
    - Do NOT change other D_04 artifacts (dashboard, summaries, etc.).
    - Do NOT let DE start W6-002 before DS artifact ships + validates.
  </do_not>
</task_order>
