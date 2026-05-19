<task_order>
  <metadata>
    <id>SSCN_DIVDEF.006</id>
    <slug>dt-portal-dev-to-prod-push</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.3.0_DT_TradingOperations</issued_to>
    <date>2026-05-19</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>HARD-GATES on (a) SSCN_DIVDEF.003 DS RAVC2 close (validates DIVZ preset against fresh Lambda v1.1.1 outputs + ships SSCN_GROUP_TAXONOMY.md), AND (b) Andrew DEV smoke approval. On Andrew approval, COO~B flips status pending + dispatch_held=false + sends GO MCP. Bench-staged scope below so DT can pre-prep (bun build readiness + portal/PROD merge mechanics + smoke screenshot scripts) any time before the gate clears.</dispatch_unblock_condition>
    <project_code>SSCN_DIVDEF</project_code>
    <priority>P1 -- closes the SSCN_DIVDEF project lifecycle. Pod 3 + AE 0.5.0 work is the entire upstream chain; PROD push is the final ship step.</priority>
    <sla>~15-30min DT wall once gate clears. portal/DEV -> portal/PROD merge + bun build + push to web server + PROD smoke verification.</sla>
    <deadline>None hard -- ship at DT pace post-gate. Pod 3 closure wall complete on this TO.</deadline>
  </metadata>

  <references>
    <prd>docs/architecture/SSCN_DIVDEF.md PRD v0.2 §4.4 sequencing diagram + v0.1 §6 TO-4 framework (CTO~B; commits a5e1b7ef4 + c34f16d13 2026-05-19).</prd>
    <upstream_de_commits>
      portal/DEV inventory ready to push (3 commits):
       - `45ea7210` (DE 0.3.0 SSCN_DIVDEF.001) -- DIVZ preset + ranking-method UI + 4-group strip + step=0.1 weight input + DEFAULT_CATEGORIES removal
       - `2254437c` (DE 0.3.0 SSCN_DIVDEF.001 constitution ship; auxiliary commit)
       - `b302f5cf` (DE 0.3.0 SSCN_DIVDEF.005) -- UNIVERSE_IDS 6->5 swap + types.ts UniverseId union swap + US_ONLY_UNIVERSES Set-form-retained + sscn_divdef_001_smoke.json AC10 dropdown extension
    </upstream_de_commits>
    <upstream_ae_commits>
      Lambda already on PROD via Terraform deploy chain (NOT in this push scope; this TO is portal-only):
       - `security-scanner-v1.1.1` (commit ea4062681; UNIVERSE_MAP v0.2 5-set + NON_SCORING_COLS amendment)
       - latest/factor_metadata.json asOf=2026-05-18 confirmed; latest/universes/ has 9 subdirs (legacy 4 forensic + new 5 fresh)
    </upstream_ae_commits>
    <upstream_data_state>
      SSCN_DIVDEF.002 COO-executed 2026-05-19T18:26-18:28Z under Andrew-direct "proceed what you can" mandate (DT was on P0 portfolio-management-v2.1.1 openpyxl-fix). 11-file output in `s3://opal-data-portal-v2/json/security_scanner/2026-05-18/` + latest/ overwrites verified. AC7 manifest-emit FAIL EMPIRICAL -- ADHC follow-on; NOT a TO-006 blocker (portal reads latest/factor_metadata.json + latest/universes/{token}/scanner_data.json, NOT latest/manifest.json).
    </upstream_data_state>
    <ds_validation_dependency>
      SSCN_DIVDEF.003 (DS DIVZ-preset empirical validation + SSCN_GROUP_TAXONOMY.md doc) MUST CLOSE before this TO fires. DS pre-stage AC5 13/13 PASS + AC4 skeleton banked; post-GO wall ~50-60min. RAVC2 from DS -> me -> Andrew DEV smoke ask -> Andrew approval -> me flips this TO to pending + GO.
    </ds_validation_dependency>
  </references>

  <context>
    Final PROD ship for SSCN_DIVDEF. portal/DEV carries 3 DE commits (45ea7210 + 2254437c + b302f5cf) that align with Lambda v1.1.1's new 5-universe data on `latest/`. portal/PROD currently points to whatever DEV pointer existed before TO-1 (DE preset+UI ship). On this PROD push, the user experience becomes:
     - Default load: Russell 1000 universe + 13-factor DIVZ preset + 4-group rollup strip (Dividend 40 / Momentum 30 / Value 15 / Quality 15) + step=0.1 weight input
     - Universe dropdown: 5 options (sp500, r1000, rmidcap, sp400, msciusa) -- legacy 4 (r1000v, acwx, eafe, eafev) NO LONGER OFFERED (forensic S3 paths preserved but dropdown drops them)
     - Ranking method control: "Non-sector neutral" default + "Sector neutral" disabled with "Coming soon (v0.2)" tooltip
     - Data vintage: asOf=2026-05-18 across all 5 universes; factor_metadata reflects new set

    DE has no PROD push permission per role abilities (DT/AE gates); this TO is the canonical DT-lane portal push.
  </context>

  <scope>
    <step>Phase 1 (pre-flight, bench-stage-OK before gate clears) -- merge readiness:
      - `cd portal && git checkout DEV && git pull origin DEV` -- confirm DEV at HEAD includes b302f5cf (latest commit per the DE TO-5 ship).
      - `git checkout PROD && git pull origin PROD` -- confirm PROD baseline state.
      - `bun install` (clean install).
      - `bun run typecheck` exit 0; `bun run lint` exit 0.
      - `bun run build` exit 0 (verify the build artifact compiles against current PROD baseline before merging DEV in).
    </step>
    <step>Phase 2 (merge) -- after Andrew DEV smoke approval:
      - `git checkout PROD`
      - `git merge DEV --ff-only` (or `--no-ff` with explicit merge commit per existing portal/PROD convention; DT judgment on merge style consistent with prior portal PROD ships).
      - `bun run build` (post-merge production build).
      - Verify `dist/` (or equivalent) build artifacts produced without errors.
    </step>
    <step>Phase 3 (PROD ship + verification):
      - Push portal/PROD to remote (`git push origin PROD`).
      - Deploy artifacts per existing portal-PROD deployment pattern (CloudFront invalidation if needed; web server pull; whatever the canonical portal/PROD ship sequence is per DT's deployment_map.xml).
      - PROD URL smoke test: page loads cleanly; first-load state matches PRD v0.2 §3 (R1000 default + 13-factor DIVZ preset + 4-group strip + new 5 universes in dropdown + asOf=2026-05-18 shown if surfaced); no console errors.
      - CloudFront cache: invalidate as needed for `/index.html` + the portal entry chunk so users see the new build on next page-load.
    </step>
    <step>Phase 4 (RAVC2) -- to 2.0.0_SA_COO~B + CC 1.0.0_SA_CTO~B with: PROD merge SHA + bun build transcript + PROD URL smoke screenshot + AC1-AC8 confirmations. SSCN_DIVDEF.json status -> "complete" on TO close (3-step closure per CLAUDE.md non-negotiable: JSON + REGISTRY row move to Completed + PRD status note if applicable).</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">portal/PROD `HEAD` includes the 3 SSCN_DIVDEF DEV commits (45ea7210 + 2254437c + b302f5cf) post-merge. `git log --oneline PROD | head -10` shows the SSCN ship.</ac>
    <ac id="AC2">`bun run build` exit 0 on PROD branch post-merge. Build artifacts produced in expected output directory (per portal build config).</ac>
    <ac id="AC3">PROD URL first-load: Universe dropdown shows exactly 5 options (sp500/r1000/rmidcap/sp400/msciusa); Russell 1000 preselected; 13-factor DIVZ preset chips rendered in Dividend->Momentum->Value->Quality order with weights summing 100.0%; 4-group rollup strip shows Dividend 40 / Momentum 30 / Value 15 / Quality 15.</ac>
    <ac id="AC4">Ranking Method control: "Non-sector neutral" selected + "Sector neutral" disabled with tooltip "Coming soon (v0.2)" (or equivalent v0.2 phrasing per CTO PRD Q1).</ac>
    <ac id="AC5">Switching to each of the 5 universes loads scanner data successfully (no 404; jq-equivalent FE-side: page renders ranked rows for each universe). Confirms `latest/universes/{rmidcap, sp400, msciusa}/` paths are reachable from PROD's auth-validator-edge + S3-direct origin chain.</ac>
    <ac id="AC6">Weight input: edit to `7.5` accepted (step=0.1 confirmed); sum recalculates to 100.0%.</ac>
    <ac id="AC7">PROD URL: zero JS console errors on first load (modulo pre-existing CDP-bootstrap-401 race per TO-1 AC8 caveat which is independent of this TO).</ac>
    <ac id="AC8">CloudFront cache invalidated for portal entry chunk; new user on the URL within 5min of push sees the new build (cache TTL behavior per existing portal CF behavior config).</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      `comp-routes trace getUniverseScanner` -- confirm PROD route path stable (no auth changes since TO-1 + TO-5).
      `comp-cache collisions | grep -i scanner` -- expect clean.
    </before_write>
    <before_commit>
      `bun run typecheck` exit 0; `bun run lint` exit 0; `bun run build` exit 0 (pre-merge sanity on DEV).
    </before_commit>
    <after_commit>
      `bun run build` exit 0 (post-merge on PROD branch).
      PROD URL Playwright/headless smoke per AC1-AC8 (whichever portal/PROD smoke tool DT uses for canonical PROD verification).
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    None. Self-contained portal/PROD ship. Lambda v1.1.1 + latest/ data are already on PROD (Lambda runs against single PROD AWS account; data lives at one set of S3 keys; no DEV/PROD bifurcation on the data side). Only portal/{DEV,PROD} branches need merging.
  </cross_domain_coordination>

  <deliverables>
    - portal/PROD merge commit (DEV -> PROD; SHA in RAVC2)
    - bun build artifacts on PROD branch
    - PROD URL smoke screenshot + AC1-AC8 evidence
    - CloudFront invalidation evidence (if applicable)
    - Session log under `org/tier2_senior/0.3.0_DT_TradingOperations/logs/YYYY-MM-DD/` with merge SHA, build transcript, smoke results, AC evidence.
    - RAVC2 to 2.0.0_SA_COO~B + CC 1.0.0_SA_CTO~B on close.
    - SSCN_DIVDEF.json status -> complete (COO~B will handle the 3-step closure: JSON + REGISTRY row move to Completed + PRD status note per CLAUDE.md non-negotiable). DT just MCPs close.
  </deliverables>

  <do_not>
    <rule>Do NOT push to portal/PROD before SSCN_DIVDEF.003 (DS validation) closes + Andrew DEV smoke approves. The gate is structural; bypassing it ships unvalidated data state to PROD users.</rule>
    <rule>Do NOT modify any portal/DEV code in this TO. This is a merge-and-push operation only; the upstream DE commits (45ea7210 + 2254437c + b302f5cf) are authoritative.</rule>
    <rule>Do NOT touch S3 latest/ or Lambda code -- already shipped + verified via TO-2 + TO-4 (Lambda). This TO is portal-only.</rule>
    <rule>Do NOT delete the legacy 4 universe directories from S3 (acwx/eafe/eafev/r1000v under latest/universes/) -- PRD v0.2 §3.5 DO-NOT-DELETE preserved for forensic. They no longer appear in the portal dropdown post-this TO but remain in S3.</rule>
    <rule>Do NOT skip the PROD URL smoke test (AC3-AC8) -- structurally PASS-required. If any AC fails post-push, RAVC2 PARTIAL with the failure; do NOT roll back unilaterally (Andrew + COO~B/CTO~B make the rollback call).</rule>
    <rule>No emojis in commit messages, session log, or CLI transcripts (CLAUDE.md ASCII-only).</rule>
  </do_not>
</task_order>
