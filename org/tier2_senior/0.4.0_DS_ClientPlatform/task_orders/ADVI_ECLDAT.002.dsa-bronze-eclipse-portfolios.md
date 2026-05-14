<task_order>
  <metadata>
    <id>ADVI_ECLDAT.002</id>
    <slug>dsa-bronze-eclipse-portfolios</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-05-14</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED 2026-05-14 ~21:0XZ by COO per CTO 5-Q ratify + Andrew direct "set up the same jwt refresher that we did for orion for eclipse as well as figuring out bronze and silver ingestion, gold layers can wait for now". DS~A bench-clear post Phase 1.1 P1/P2 close. No further Andrew engagement needed per CTO route. Phase 2 ships in parallel with ADVI_ECLDAT.001 (AE 0.6.1 JWT extension); stop-gap uses Andrew JWT direct from .runtmp pre-Phase-1; supersedes to Lambda-managed JWT post-Phase-1 ship.</dispatch_unblock_condition>
    <project_code>ADVI_ECLDAT</project_code>
    <priority>P1 — Andrew dashboard tomorrow gate; bronze data layer for Eclipse portfolio + model composition</priority>
    <sla>~2-3h wall actual per Pod 4 velocity</sla>
  </metadata>

  <references>
    <ref type="feasibility_brief">docs/briefs/data-scientist-eclipse-ingestion-feasibility-20260514.md (DS~A `23d2e2c54`)</ref>
    <ref type="cto_ratify">CTO 5-Q ratify 2026-05-14 ~20:5XZ — Q2 Option A stop-gap + Phase 1+2 P1 today; Q3 Andrew identity stop-gap acceptable; Q4 $3.4M gap accept (96.6% reconciliation)</ref>
    <ref type="andrew_direct">Andrew 2026-05-14 ~21:0XZ: "set up the same jwt refresher that we did for orion for eclipse as well as figuring out bronze and silver ingestion, gold layers can wait for now"</ref>
    <ref type="sibling_pattern">Existing bronze puller scripts in data/orion/scripts/bronze/ (Orion pattern source); mirror structure for Eclipse</ref>
    <ref type="phase1_dependency_optional">ADVI_ECLDAT.001 (AE 0.6.1 Lambda JWT extension; PARALLEL not BLOCKING)</ref>
  </references>

  <context>
    Eclipse data ingestion empirically proven via DS~A feasibility brief using Andrew's JWT bearer. 11 daily API calls scope:
    - `/v1/portfolio/portfolios/simple` (master account list)
    - `/v1/modeling/models` (Opal model list)
    - Per-Opal-model composition (~9 calls = 1 per Opal model; varies based on portfolio count)

    Eclipse accountId is STRING type (vs Orion id INT) — preserves as-emitted to bronze; silver tier handles type-coerced join per Rule 17 + Phase 3 TO scope.

    Reconciliation expectation: 96.6% first-pass with $3.4M gap accepted per Q4 ratify (T+1 valuation lag normal). Phase 4 gold script `_meta.reconciliation_summary` sentinel tracks; drift below 90% triggers investigation TO. Phase 4 gold deferred per Andrew "gold layers can wait."

    **Stop-gap JWT auth:** Phase 2 ships pre-Phase-1 (AE Lambda JWT extension). Bronze puller reads Andrew JWT from local `.runtmp/eclipse_token.txt` (or similar staging path) for initial empirical ship. Post-Phase-1, supersedes to SM-managed JWT via `aws secretsmanager get-secret-value --secret-id orion/eclipse_jwt/current`.

    Per CLAUDE.md Rule 14+15: ds-commit-gate.sh + `from __future__ import annotations` first import.
  </context>

  <objective>
    Author new bronze puller `data/orion/scripts/bronze/pull_eclipse_portfolios.py` emitting Eclipse portfolio + model composition data to `bronze/eclipse/` S3 path. Daily cadence; 11 API calls scope. Stop-gap Andrew JWT pre-Phase-1; SM-managed post-Phase-1.
  </objective>

  <scope>
    <files>
      <file action="create">data/orion/scripts/bronze/pull_eclipse_portfolios.py — new bronze puller (~150 LOC)</file>
      <file action="readonly_reference">data/orion/scripts/bronze/{existing Orion bronze puller} — pattern source for structure + dispatch hooks</file>
      <file action="modify">data/orion/scripts/dispatch.sh — add pull_eclipse_portfolios chain entry IF dispatch integration required; otherwise OFF-CHAIN initial ship</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript io {existing Orion bronze puller} (Orion sibling pattern read)</run>
      <expect>Pattern source for bronze structure + JWT auth flow + S3 write path conventions.</expect>
    </step>
    <step>
      <run>Read Andrew JWT from .runtmp/eclipse_token.txt (or current empirical stop-gap location); verify expires_at via JWT decode</run>
      <expect>Valid stop-gap JWT; if expired, surface for Andrew refresh OR wait for Phase 1 Lambda ship.</expect>
    </step>
    <step>
      <run>Test 11 API calls manually: curl `https://www.orioneclipse.com/v1/portfolio/portfolios/simple` + `/v1/modeling/models` + sample per-model composition with Andrew JWT</run>
      <expect>Empirical confirmation per feasibility brief; document any new schema fields or response shape changes since brief authoring.</expect>
    </step>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <run>Author pull_eclipse_portfolios.py:
        - `from __future__ import annotations` first import per Rule 15
        - JWT load: stop-gap from .runtmp path OR (post-Phase-1) `aws secretsmanager get-secret-value --secret-id orion/eclipse_jwt/current`
        - 11 API calls per spec: portfolios/simple → models → per-Opal-model composition
        - Write bronze artifacts to `s3://opal-data-inf/bronze/eclipse/{date}/{artifact}.{ext}` (CSV or JSON per artifact shape; consistent with Orion bronze convention)
        - Idempotent: same date re-run produces same output
        - Sentinel-emit: `bronze/eclipse/{date}/_meta/pull_complete.json` with `{rows_per_artifact, api_call_count, started_at, completed_at, jwt_source}`
        - No emoji per CLAUDE.md; ASCII log prefixes (OK/WARN/ERROR/SKIP)</run>
      <expect>Script ~150 LOC; idempotent; sentinel-emitted; structurally consistent with Orion bronze pattern.</expect>
    </step>
    <step>
      <run>ds-commit-gate.sh: py_compile + ds-precommit-check.py + ruff py39 0.15.11</run>
      <expect>All 3 PASS.</expect>
    </step>
    <step>
      <run>Local dry-run: invoke script against current Andrew JWT; verify bronze artifacts land at `s3://opal-data-inf/bronze/eclipse/{today}/`</run>
      <expect>11 API calls succeed; bronze artifacts populated; sentinel manifest written.</expect>
    </step>
  </phase>

  <phase id="3" when="commit + deploy">
    <step>
      <run>safe-commit.sh per Rule 13: commit → push to CLOUD → S3 upload → comp-pipescript deployed MATCH</run>
      <expect>All gates PASS. Author identity DS~A.</expect>
    </step>
    <step>
      <run>Decision: dispatch.sh integration (chain-fired daily) OR off-chain manual run for Andrew dashboard tomorrow</run>
      <expect>Off-chain manual run acceptable for tomorrow dashboard; chain integration deferred to opportunistic follow-on (no urgency).</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + AE 0.6.1 (Phase 1 SM-managed JWT consumer; Phase 3 silver consumer)</run>
      <expect>Evidence-bearing close: commit SHA + safe-deploy log + S3 sentinel verification.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: `data/orion/scripts/bronze/pull_eclipse_portfolios.py` created with `from __future__ import annotations` first import
    AC2: 11 API calls implemented: `/v1/portfolio/portfolios/simple` + `/v1/modeling/models` + per-Opal-model composition
    AC3: Bronze artifacts written to `s3://opal-data-inf/bronze/eclipse/{date}/` per Orion bronze convention
    AC4: Sentinel manifest `_meta/pull_complete.json` emitted with rows + api_call_count + timestamps + jwt_source
    AC5: JWT auth supports stop-gap (local Andrew JWT) OR SM-managed (post-Phase-1 supersession)
    AC6: ds-commit-gate.sh PASS (py_compile + AST scanner + ruff py39)
    AC7: Local dry-run empirical: 11 API calls succeed; bronze artifacts populated
    AC8: safe-deploy.sh PASS + S3 upload + comp-pipescript deployed MATCH
    AC9: No emoji per CLAUDE.md
    AC10: RAVC2 to COO + CC CTO + AE 0.6.1
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 comp-pipescript io reference read; Phase 2 ds-commit-gate.sh; Phase 3 safe-deploy.sh + comp-pipescript deployed MATCH.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: None pre-Phase-1; ADVI_ECLDAT.003 Phase 3 silver gates on this Phase 2 RAVC.
    PARALLEL-OK: ADVI_ECLDAT.001 AE 0.6.1 JWT extension (Phase 1 supersedes stop-gap JWT path; not blocking).
    NO PORTAL CHANGES.
    OWNED-PATHS: data/orion/scripts/bronze/ is DS-lane per CLAUDE.md Rule 13 + 14; ds-commit-gate.sh applies.
    DS SUB-AGENT ROUTING: DS~A primary per CTO route. DS~D could absorb if DS~A bench-engaged on other priority OR cross-pollination valuable.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Pure new bronze layer; no historical backfill needed. Day-of ship + future daily emit.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. pull_eclipse_portfolios.py (~150 LOC)
    2. Bronze artifacts under bronze/eclipse/{date}/
    3. Sentinel manifest pull_complete.json
    4. ds-commit-gate + safe-deploy + S3 SHA-MATCH
    5. RAVC2 with deploy + dry-run evidence
  </deliverables>

  <ravc>DS~A RAVC2 to COO + CC CTO + AE 0.6.1 on AC1-10 PASS.</ravc>

  <notes>
    **Author identity:** `--author="0.4.0_DS_ClientPlatform~A <0.4.0_DS_ClientPlatform~A@opal.agent>"`.

    **Stop-gap discipline:** Andrew JWT direct ships now per Q3 hybrid audit trail. Phase 1 SM-managed JWT supersedes mechanically post-AE ship — script auth path conditional (`if local stop-gap path exists: use_local else: use_sm`). Banked memory entry candidate `reference_eclipse_admin_contacts.md` deferred next-session (DS~A or COO lane).

    **Andrew gold-tier deferral:** per Andrew 2026-05-14 ~21:0XZ "gold layers can wait for now" — Phase 4 gold script `INF_D_XX.opal_account_overlay.py` NOT in current scope. Phase 5 FE wire deferred to DE 0.4 PRD. This TO closes ingestion-side (bronze + silver Phase 3 next).

    **No emoji per CLAUDE.md.** Plain ASCII log prefixes.

    **Idempotency note:** same date re-run produces same bronze output. Stop-gap JWT may expire mid-day; script should fail-fast OR fail-clear with directive to refresh Andrew JWT (Phase 1 supersession eliminates this).
  </notes>
</task_order>
