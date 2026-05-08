<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.OPS</id>
    <project>ADHC_COMPIL_V4</project>
    <title>Compiler tools operational test matrix + segment-scope taxonomy — empirical validation across all comp-* tools + segment variations</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>complete</status><!-- Closed 2026-05-08T~PM by AE 0.7.0 per Andrew override of CTO "no action tonight" sequencing. All 7 phases shipped same-session: empirical matrix (108 cases) + segment_scope yaml + 1-page reference card + findings ledger with 16 triage items (2 BLOCKING, 7 NUISANCE, 7 DOC-DRIFT, 4 DEFERRED). Authored by CTO direct per Andrew 2026-05-08 PM directive: "im wondering if we need to clarify which compilers are segment-agnostic versus ones that are targeted (bd-pipeline, inf-pipeline) so agents know what to use. Id also like you to have 0.7.0_AE go and test out the various compilers and variations on their use to see if they actually work, lets operationalize the use of those tools in a TO." -->
    <priority>normal</priority>
    <estimated_effort>~2-3d (AE pace likely ~1-1.5d wall clock per under-budget pattern)</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md (v0.1 + v0.2 + v0.3 addenda)</ref>
    <ref type="retrospective">docs/architecture/ADHC_COMPIL_FULL_CORPUS_RETROSPECTIVE.md (deterministic 1-month methodology)</ref>
    <ref type="trigger">Andrew direct 2026-05-08 PM: agents need clear "segment-agnostic vs targeted" classification + empirical "do tools actually work as documented?" verification</ref>
    <ref type="catalog">org/modules/graph/comp-tools.yaml (current 19+ tool catalog; needs segment_scope metadata field added per tool)</ref>
    <ref type="related_to_VAL">ADHC_COMPIL_V4.VAL (validation pass against current Inflection state) — different scope: VAL is "do new V4 tools work on Inflection?"; OPS is "do ALL comp-* tools work as documented across ALL segments?"</ref>
  </references>

  <context>
    With V4 Phase 1 + addendum complete (11/12 active surfaces SHIPPED 2026-05-08), the compiler tooling has roughly doubled in 30 days. Agents now face two operational questions the catalog doesn't crisply answer:

    1. **Segment scope** — which tools are "segment-agnostic" (single invocation works across BD + INF + multi-firm)? Which are "segment-aware" (auto-detect or explicit flag required)? Which are "segment-locked" (only work on one pipeline)? Without this taxonomy, agents waste time invoking targeted tools without flags + getting partial output, or invoking universal tools assuming flags are required.

    2. **Empirical correctness** — does each tool actually work as documented in `comp-tools.yaml`? Examples are notional (specific command strings) but rarely empirically re-verified. Some tools (comp-xref symbol-lookup, comp-iam EC2 roles) gained NEW capability today; some (comp-pipescript inf-manual-api, comp-validate Orion config) gained NEW segments today. None have been validated end-to-end across the full surface area in one pass.

    This TO operationalizes both questions: produces a published taxonomy + an empirical test matrix that future agents can re-run for regression detection.
  </context>

  <segment_scope_taxonomy_framework>

  CTO-supplied as Phase 1 input. AE refines + populates per empirical findings.

  ### Three-tier classification

  **Tier A — Cross-segment (no flag/context required; single invocation covers all surfaces):**

  Examples: `comp-build`, `comp-trace <node>`, `comp-blast <node>`, `comp-diff`, `comp-xref` (both modes), `comp-cache collisions`, `comp-pii audit`, `comp-shell` (any mode), `comp-tooltip` (any mode), `check-lambda-layer-deps <lambda>` (when --all flag set or single Lambda by name), `comp-routes` (most subcommands).

  **Tier B — Segment-aware (auto-detect or explicit flag required to scope correctly):**

  Examples:
  - `comp-pipescript io/chain/feeds/consumers/deployed` — auto-detects by script-name prefix (`INF_*` → inf, `D_*`/`B_*`/`C_*`/`A_*` → bd) or explicit `--pipeline` flag
  - `comp-validate <script>` — auto-resolver per script-name prefix or explicit `--config` flag
  - `comp-freshness chain <pipeline>` — explicit pipeline arg required (`bd` / `inf`); DDB extension when shipped (.015) takes table arg
  - `comp-platinum page <Component>` — works for any portal page; auto-routes by component pattern; `comp-platinum reverse <key>` accepts `[SPECULATIVE]`-tagged or `--strict` mode
  - `comp-iam service <name>` — Lambda-name first, EC2-role-name fallback (post-V4.013); `comp-iam cross-firm` post-V4.006 ship
  - `comp-transform schema-check <Component>` — accepts `--feature <token>` to escalate feature-named UNUSED to WARN
  - `comp-constants check / index / new` — auto-detects lane (BD/INF/multi-firm) from name prefix; explicit `--lane` flag override
  - `comp-events` (post-V4.005 ship) — TBD; auto-detect from event-source ARN

  **Tier C — Segment-locked (currently only works on one pipeline; future extension may broaden):**

  Examples:
  - `comp-incrparity` — BD-only? (verify empirically)
  - Anything else surfaced by the test matrix below

  ### Cross-cutting axes

  Beyond pipeline (BD/INF/multi-firm), tools may also vary by:
  - **Firm** (49financial / inflection / cottonwood-when-onboarded) — primarily comp-platinum + comp-routes
  - **Layer** (gold / silver / bronze / platinum / portal) — comp-pipescript distinguishes; others sometimes
  - **Surface type** (Lambda / EC2 / CF / API GW / S3 prefix / DDB table) — comp-iam + comp-routes + comp-events
  - **Mode** (default / strict / verbose / json) — varies per tool

  AE populates the matrix below per empirical run.

  </segment_scope_taxonomy_framework>

  <test_matrix_framework>

  ### Test-matrix structure (CTO-supplied skeleton; AE populates)

  Output deliverable: `docs/architecture/ADHC_COMPIL_V4_OPS_TEST_MATRIX.md` — table per tool with one row per (subcommand × segment × mode) variation.

  ### Per-tool test cases (minimum coverage; AE adds more if relevant)

  | Tool | Subcommand | Test cases (AE runs each + records actual vs documented) |
  |---|---|---|
  | `comp-build` | (none) | (1) clean build no errors; (2) `--check` mode exit 0 on clean state; (3) `--check` exit 2 on intentional drift (use TO-12 STALE_NODE_WARN); (4) post-build SHA coverage stats |
  | `comp-trace` | (one) | (1) BD node `D_04` --direction both; (2) INF node `INF_D_04` --direction both; (3) frontend node `AdvisorIntelligence`; (4) Lambda `opal-partners-data`; (5) S3 key prefix `platinum/firm/leaderboard.json` |
  | `comp-blast` | (one) | (1) BD function `build_employee_leaderboard`; (2) INF function `_build_aua_view`; (3) Lambda `inf-gold-trigger`; (4) S3 prefix `silver/canonical_holdings`; (5) helper `_compute_window_decomposition` |
  | `comp-diff` | (one) | (1) HEAD~3 default; (2) --staged; (3) clean repo (zero diff) |
  | `comp-xref` | diff mode | (1) no-arg vs baseline; (2) `--save`; (3) `--ref HEAD~5`; (4) `--json` |
  | `comp-xref` | symbol mode (post-V4.014) | (1) `comp-xref D_04`; (2) `comp-xref AdvisorPublicProfile`; (3) `comp-xref inf-bronze-runner`; (4) zero-match symbol |
  | `comp-pipescript` | dag/io/chain/feeds/consumers | (1) BD `D_04` (auto-detect); (2) INF `INF_D_04` (auto-detect); (3) explicit `--pipeline bd-gold` flag; (4) explicit `--pipeline inf-gold`; (5) explicit `--pipeline inf-manual-api` (post-V4.008); (6) silver script (post-v1.A) |
  | `comp-pipescript` | overlap | (1) two BD scripts; (2) two INF scripts; (3) cross-pipeline (BD vs INF) — should produce empty or distinct sets |
  | `comp-pipescript` | postdeps | (1) BD `D_04`; (2) INF `INF_D_04` |
  | `comp-pipescript` | deployed | (1) BD default (`--pipeline bd-gold` implicit); (2) `--pipeline inf-gold`; (3) `--pipeline inf-silver`; (4) `--pipeline bd-silver`; (5) script that doesn't exist (error path) |
  | `comp-routes` | trace/behaviors/origins/rewrites/api-routes/endpoints/components/auth-map/edge-versions | (1) trace by URL `/api/scoped/advisor-intelligence/...`; (2) trace by endpoint name `getPlatinumLeaderboard`; (3) trace by component name `AdvisorIntelligence`; (4) behaviors full list; (5) auth-map full; (6) edge-versions Lambda@Edge pinning |
  | `comp-cache` | collisions | (1) full collision check (passes today); (2) intentional collision fixture if AE has time |
  | `comp-iam` | service | (1) BD Lambda `bd-gold-trigger`; (2) INF Lambda `inf-gold-trigger`; (3) BD EC2 role `bd-exporter` (post-V4.013); (4) INF EC2 role `inf-bronze-runner` (post-V4.013); (5) `nonexistent-thing` (error path with helpful message) |
  | `comp-iam` | gaps / role / roles / services / stats | (1) gaps default; (2) gaps for new IAM change (intentional drift fixture); (3) role `bd-gold-runner-role`; (4) services full list count |
  | `comp-iam` | cross-firm (post-V4.006) | (1) BD bucket grants; (2) INF bucket grants; (3) future Cottonwood placeholder |
  | `comp-validate` | (script + --artifact) | (1) BD `D_04` with real BD artifact; (2) INF `INF_D_04` with real INF artifact (post-V4.009); (3) `--config` explicit override; (4) symbolic `$INFLECTION_REP_IDS` rule resolution; (5) missing canonical → ERROR (post-V4.009) |
  | `comp-platinum` | page / reverse / tab-audit / summary | (1) page `AdvisorIntelligence`; (2) page `BooksTab`; (3) reverse `platinum/firm/leaderboard.json`; (4) reverse `platinum/firm/header_metrics.json#radial_12m` (post-V4.010 strict mode); (5) reverse with `--strict` flag (exit 2 on no-authoritative); (6) tab-audit |
  | `comp-transform` | schema-check / fields / chains / unused / trace / ternary-audit | (1) schema-check `AdvisorIntelligence`; (2) schema-check with `--feature inflection` (post-V4.011 robustness); (3) schema-check component with no co-located types.ts (verify parent-walk); (4) ternary-audit a cohort/mode component; (5) fields list for any component |
  | `comp-pii` | audit | (1) full audit; (2) intentional PII fixture (if available) |
  | `comp-tooltip` | scan / drift / canonical / migrated / summary | (1) full scan; (2) drift list; (3) summary stats |
  | `comp-incrparity` | (subcommands TBD) | (1) BD parity; (2) INF parity if supported (verify segment lock vs broader) |
  | `comp-freshness` | chain bd / chain inf / synthetic stale | (1) `comp-freshness chain bd`; (2) `comp-freshness chain inf`; (3) synthetic-stale fixture; (4) DDB target post-V4.015 ship |
  | `comp-shell` | (modes TBD) | (1) standard scan; (2) dup-source mode post-V4.004 ship |
  | `comp-constants` | check / index / new | (1) check default (drift detection); (2) check `--lane bd`; (3) check `--lane inf`; (4) `index` rebuild; (5) `new` discovery |
  | `check-lambda-layer-deps` | single / all / json | (1) single `inf-gold-trigger`; (2) `--all` repo-wide; (3) `--json` machine output; (4) Lambda with missing layer dependency (intentional fixture) |
  | `comp-events` (post-V4.005) | list / trace / render-matrix | (1) full event list; (2) trace specific S3-event source; (3) render the daily-pull matrix; compare to hand-authored INFETL_DAILY_PULLS_MATRIX.md |

  ### Per-test recording schema (CTO-required)

  Each test case in the matrix records:
  ```
  | Tool | Subcommand | Test case | Expected (from catalog) | Actual | Match? | Notes |
  ```

  Match column: PASS (matches docs) / DIFFERS (works but output differs from doc) / FAIL (errors or wrong output) / DEFERRED (post-V4.005/.015 ship; not yet shippable).

  </test_matrix_framework>

  <scope>
    <step>
      <run>Phase 1 — read CTO-supplied taxonomy framework + test matrix above. Cross-reference against current `comp-tools.yaml` to identify any tools missing from the matrix.</run>
      <expect>Familiarity with full surface area; gaps in matrix coverage flagged.</expect>
      <if_mismatch>If any tool is missing from the test matrix, add it + document.</if_mismatch>
    </step>
    <step>
      <run>Phase 2 — populate segment_scope metadata in `comp-tools.yaml` per tool. Add new field `segment_scope: cross-segment | segment-aware | segment-locked` to each tool entry. Use the CTO Tier A/B/C classification as starting framework; refine per empirical findings (some tools may move tier post-testing).</run>
      <expect>Every tool in catalog has explicit segment_scope tag.</expect>
      <if_mismatch>If a tool's actual scope differs from CTO classification, document the divergence + adjust classification.</if_mismatch>
    </step>
    <step>
      <run>Phase 3 — execute the test matrix. Run every (tool × subcommand × variation) per the framework above. Record actual outputs in deliverable doc `docs/architecture/ADHC_COMPIL_V4_OPS_TEST_MATRIX.md`. Use the per-test recording schema (Tool | Subcommand | Test case | Expected | Actual | Match? | Notes).</run>
      <expect>Full test matrix populated; each row has Match=PASS/DIFFERS/FAIL/DEFERRED.</expect>
      <if_mismatch>Record divergences; do not silently skip. SKIPPED rows must explain why.</if_mismatch>
    </step>
    <step>
      <run>Phase 4 — file findings summary at top of test matrix doc. Summary should include:
        - Total test cases: N (PASS / DIFFERS / FAIL / DEFERRED count)
        - Tier A/B/C tool counts
        - Notable divergences from documentation (any tools whose actual behavior doesn't match comp-tools.yaml docs)
        - Tool-correctness issues found (false-positive class — likely candidate for follow-on TO)
        - Segment-scope refinements (tools that moved tier post-testing)</run>
      <expect>Summary makes the matrix scannable; agents can find the right tool for their question without reading every row.</expect>
    </step>
    <step>
      <run>Phase 5 — agent-facing reference card. Author `org/modules/graph/comp-tools-segment-scope.md` (or section in comp-tools.yaml) — short reference doc agents can read quickly. Format: 3-tier table + cross-cutting-axes summary + "if you're working on X, use tools Y/Z" guidance.</run>
      <expect>1-page agent-facing reference; companion to comp-tools.yaml's full catalog.</expect>
    </step>
    <step>
      <run>Phase 6 — for any FAIL/DIFFERS findings, file standing-backlog observations in the test matrix doc + flag to CTO for triage. Each issue gets:
        - Tool + subcommand + test case
        - Severity (BLOCKING agent workflow / NUISANCE / DOC-DRIFT-ONLY)
        - Recommended fix (could be tool fix, doc fix, or segment-scope re-classification)</run>
      <expect>Findings ledger ready for CTO consumption; any BLOCKING items get follow-on TO authoring.</expect>
    </step>
    <step>
      <run>Phase 7 — ship via safe-commit.sh. RAVC2 to CTO + COO with summary findings + matrix doc + comp-tools.yaml taxonomy update.</run>
      <expect>Clean ship; matrix doc + yaml taxonomy + agent reference card all committed.</expect>
    </step>
  </scope>

  <acceptance_criteria>
    <ac id="1">`comp-tools.yaml` updated with `segment_scope: cross-segment | segment-aware | segment-locked` field on every tool entry (~19 tools).</ac>
    <ac id="2">`docs/architecture/ADHC_COMPIL_V4_OPS_TEST_MATRIX.md` exists with full test matrix populated; every (tool × subcommand × variation) row has actual-output evidence + Match classification.</ac>
    <ac id="3">Test coverage: ≥75% of CTO-supplied test cases run + recorded; remaining DEFERRED rows explicitly tagged (e.g., comp-events post-V4.005 ship).</ac>
    <ac id="4">Findings summary at top of matrix doc — total counts + tier counts + notable divergences + correctness issues + segment-scope refinements.</ac>
    <ac id="5">Agent-facing reference card at `org/modules/graph/comp-tools-segment-scope.md` (or yaml section) — 1-page summary; segment-tier table + cross-cutting axes + workflow guidance.</ac>
    <ac id="6">Any BLOCKING tool-correctness issues flagged with severity + recommended fix; CTO can dispatch follow-on TOs without further investigation.</ac>
    <ac id="7">Backwards-compat: existing tool behavior unchanged (this is documentation + testing; no tool code changes unless empirical FAIL surfaces a real bug — if so, escalate via RAVC1 before fixing).</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1">Read `comp-tools.yaml` + recent V4 ship history (TO-3 through TO-14 + .016) to confirm full surface area + recent additions.</phase>
    <phase id="2">During execution: append one row per tool run to `org/compiler-tools-log.md` (per existing convention + post-TO-016 synthetic-test annotation if any test fixture is intentionally-failing).</phase>
    <phase id="3">Post-commit: run `comp-build` + verify all node counts unchanged (this TO is doc + test, not code change).</phase>
  </compiler_tools_mandate>

  <ravc>
    <expected_recipient>1.0.0_SA_CTO + 2.0.0_SA_COO (joint)</expected_recipient>
    <expected_evidence>Test matrix doc + comp-tools.yaml diff + agent reference card + findings summary</expected_evidence>
  </ravc>

  <out_of_scope>
    <item>Fixing any FAIL/DIFFERS findings — those become follow-on TOs after CTO triage.</item>
    <item>Refactoring comp-tools.yaml structure beyond adding segment_scope field.</item>
    <item>Authoring new tools (this is testing existing surface).</item>
    <item>Cross-firm Cottonwood test cases — defer until FIRMSEP.10 ships and Cottonwood credentials/bucket are live.</item>
    <item>comp-events test cases — defer until V4.005 ships.</item>
    <item>comp-freshness DDB test cases — defer until V4.015 ships (post-FIRMSEP.10).</item>
    <item>comp-shell dup-source mode — defer until V4.004 ships.</item>
  </out_of_scope>

  <sequencing_recommendation>
    Dispatch tomorrow morning post INFETL.011 first-fire empirical witness (06:00 UTC) AND post-.VAL completion (.VAL is narrower-scoped Phase 2 validation against current Inflection state; OPS is broader). OPS likely lands at ~1-1.5d wall clock per under-budget pattern; can ship same-day if AE 0.7 has bandwidth.
  </sequencing_recommendation>
</task_order>
