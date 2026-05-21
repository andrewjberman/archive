<task_order>
  <metadata>
    <id>2.0.0_SA_COO~C-2026-05-21-demov1-to2-transform-engine</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-05-21</date>
    <status>staged</status>
    <project_code>ADVI_DEMOV1</project_code>
  </metadata>

  <objective>
    Phase 2 of ADVI_DEMOV1 — build the deterministic, seeded, two-pass
    pseudonymizer transform engine. Pass 1 builds the complete real->fake mapping
    table for every identity (firm, 168 advisors, 2,962 clients, 6,548 accounts)
    BEFORE any file is touched; Pass 2 walks all ~22,253 platinum objects,
    re-keys the S3 paths AND rewrites content against the mapping, leaving numbers
    and structure intact. Engine runs as an EC2 one-shot job. This TO builds and
    reviews the engine with a `--dry-run`; the actual populate-the-bucket run is
    TO-4.
  </objective>

  <context>
    ADVI_DEMOV1 PRD: docs/architecture/ADVI_DEMOV1.md (v0.1, 2e1321f79). Read §4
    rulings R1/R2/R4/R6, §6 TO-2, §7 risks. Read proposal
    docs/proposals/advisor-intelligence-demo-dataset-20260521.md §6 (the transform
    engine design — you authored it).

    This is the bulk of the project — proposal §9 estimates 1.5-2 days. It can be
    built in parallel with TO-1 (infra) — the build does not gate on infra; only
    the TO-4 run does.

    PHASE-0 DELTAS (TO-0 probe brief, RAVC2-accepted 2026-05-21 — these REFINE
    this TO; read brief §3/§4/§7):
    - The opal-partners-data pseudonymizer is RETIRED (Andrew 2026-04-15) —
      `needs_pseudonymization()` returns False; there is NO serve-time PII
      masking. Real 49F PII is currently served cleartext, gated only by
      firm-scoped auth. CONSEQUENCE: the demo bucket must be 100% fake AT REST —
      there is no serve-time net behind it. The TO-4 R5 leak scanner is the SOLE
      PII defense; build the engine accordingly.
    - The ADVI_ANONYM field map still EXISTS (in pseudonymizer.py
      `_transform_field`) as a field-classification REFERENCE — reuse it as a
      reference only. Do NOT frame the engine as "extending the serve-time
      module"; the module is dead code. The engine is a fresh standalone walker.
    - JSON-PATH-CONTEXT-AWARENESS IS MANDATORY (brief §3, the highest Phase-2
      risk). `label` / `key` / `display_label` are NOT universally PII: in
      concentration/items[], top_holdings[], mix[] they carry TICKERS (`QQQ`,
      `IEFA`) and asset-class labels (`Equities`) — SAFE, keep verbatim; in
      partner_analytics segments[]/clients[] and cumulative_chart adv_drill they
      carry advisor/client names — PII. A blind field-name pseudonymizer is WRONG
      (it corrupts tickers or misses names). The engine must decide by JSON path,
      not field name. The mapping-table-value-match approach (replace any string
      that IS a known real identity) is the safe core — but it must also walk
      object KEYS and bare LIST-STRINGS, and the exec_summary free-text narrative
      needs substring replacement, not keyed-field replacement.
    - Transform scope is NOT platinum-only: the L3 client-detail route
      (handle_client_detail / getClientDetail) reads
      gold/entities/clients/{id}/detail.json. The engine must take its prefix
      list as a PARAMETER — platinum/** is confirmed in scope; whether
      gold/entities/clients/ is included is an open item COO~C is resolving with
      CTO/DE (is getClientDetail superseded by getPlatinumClientSummary?). Build
      the engine prefix-agnostic so the final list is a run-time input, not a
      code change. The definitive prefix list will be confirmed before TO-4.

    CTO rulings that bind this TO:
    - R1 — Two-pass, deterministic, seeded. Pass 1 builds the COMPLETE mapping
      table before Pass 2 touches anything. Any unmapped id encountered in Pass 2
      is a HARD ERROR, never a passthrough — referential integrity across 22 k
      files depends on it.
    - R2 — Reuse the ADVI_ANONYM PII-field classification map (as a REFERENCE —
      the pseudonymizer module is retired, see deltas above) + the determinism
      contract; REPLACE hash output with a seeded faker (realistic names, not
      `a3f9b2..` hashes). Do NOT modify pseudonymizer.py in place.
    - R4 — The real->fake mapping table is a re-identification key. Treat it as a
      secret: it must NEVER be written to opal-data-demo, NEVER committed to git,
      NEVER printed to logs or agent messages. Persist it (if at all) only to a
      secure access-controlled non-demo location, or discard after the run.
    - R6 — The engine runs as an EC2 one-shot job per the EC2 Code Deployment
      Standard (CLAUDE.md Rule 12: write locally -> upload to S3 -> EC2 pulls ->
      execute). No inline code on the VM. A ~4.7 GB / 22 k-object transform
      exceeds a single Lambda invocation.

    The reconciliation constraint (PRD §3 constraint 2 / ruling R7): NO per-value
    dollar jitter. The platinum tree reconciles to the cent (leaderboard ->
    headline; identity_1 decomposition; TWR/epsilon balances). Default is
    dollar-figures-verbatim (ruling R7); a global scalar is Andrew open question
    Q1 — build the engine so the value-handling is a single config switch
    (verbatim default; optional one global constant) so Q1 can be answered without
    a code change.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before authoring (auto-rule 5, new-file repo check):
      <run>git log --oneline -- (the intended transform script path)</run>
      <expect>No prior bulk-walker exists. pseudonymizer.py is the serve-time
      single-response module — confirm it is NOT the bulk walker.</expect>
      <if_mismatch>If a bulk walker already exists, extend it rather than
      author a duplicate; flag to COO~C.</if_mismatch>

      <run>comp-pii audit</run>
      <expect>The component-layer PII audit — use as ONE field-coverage
      cross-reference baseline alongside TO-0's data-layer inventory.</expect>
      <if_mismatch>n/a — orientation input.</if_mismatch>

    Phase 2 — before commit (ds-commit-gate, CLAUDE.md Rule 14):
      <run>.tools/ds-commit-gate.sh (the transform script + any modules)</run>
      <expect>All three checks exit 0: python -m py_compile,
      .tools/ds-precommit-check.py (AST undefined-name scan), ruff check
      --target-version py39.</expect>
      <if_mismatch>Fix every finding before git add — the gate catches Class A
      latent bugs and PEP-604 syntax incompatibilities.</if_mismatch>

    Phase 3 — after committing:
      <run>--dry-run of the engine, output reconciled against TO-0's PII inventory</run>
      <expect>The dry-run mapping + planned re-keys cover every PII field TO-0's
      Phase-0 inventory enumerated; the embedded leak self-check exits clean.</expect>
      <if_mismatch>Any PII field in TO-0's inventory not handled by the engine is
      a real-PII-leak risk — fix before the TO-4 run. Escalate to COO~C if the
      gap implies a TO-0 finding the engine cannot address.</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - shared_resource: pseudonymizer.py
      (infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/pseudonymizer.py)
      — the ADVI_ANONYM serve-time module.
    - required_action: REFERENCE/REUSE only — the transform engine is a NEW
      standalone module that imports or copies the field-classification logic.
      Do NOT modify pseudonymizer.py in place (it is live serve-time code on
      opal-partners-data). If the field map needs a shared location, raise it
      with COO~C before refactoring.
    - The transform script itself is a new file under data/** scripts or a
      dedicated demo-transform path — no collision with other active TOs.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. The transform engine is a NEW standalone module (not an edit to
       pseudonymizer.py), committed to CLOUD under your serial.
    2. Two-pass structure verified: Pass 1 builds the full mapping table (firm +
       168 advisors + 2,962 clients + 6,548 accounts) and the engine refuses to
       enter Pass 2 if the table is incomplete.
    3. Pass 2 re-keys S3 paths (advisors/{real_slug}/ -> advisors/{fake_slug}/,
       clients/{z-id}/ -> clients/{fake-id}/, accounts likewise,
       platinum/49financial/ -> platinum/demo/) AND deep-walks JSON content
       replacing names/slugs/ids/embedded firm_id.
    3a. The content walk handles ALL FOUR PII loci the Phase-0 brief enumerated:
       (i) string VALUES; (ii) object KEYS that are identities (e.g.
       cumulative_chart adv_drill keyed by advisor name, role_breakdown.{name});
       (iii) bare LIST-STRINGS (e.g. cumulative_chart categories[] entries like
       "Chan, William & Shelley (z08327149)"); (iv) the exec_summary free-text
       narrative — substring replacement of any real identity appearing in prose.
    3b. JSON-PATH-CONTEXT-AWARE: label/key/display_label under
       concentration/top_holdings/mix are tickers/asset-classes — left verbatim;
       under partner_analytics segments/clients and cumulative_chart adv_drill
       they are names — transformed. The engine decides by path/value-membership,
       NOT by field name. Verified against the brief §3 reconciliation table.
    3c. The engine takes its S3 prefix list as a PARAMETER (not hardcoded).
       platinum/** is confirmed in scope; gold/entities/clients/ is a pending
       resolution (COO~C / CTO / DE) — the engine must accept the final list as
       a run-time input so the resolution needs no code change.
    4. An unmapped id encountered in Pass 2 raises a HARD ERROR (non-zero exit) —
       demonstrated by a test/dry-run with a deliberately unmapped id.
    5. Dollar values: verbatim by default; the value-handling is a single config
       switch (verbatim | one global scalar) so Andrew Q1 needs no code change.
       No per-value jitter anywhere.
    6. `--dry-run` mode implemented — produces the planned mapping + re-key plan
       without writing to S3.
    7. An embedded PII-leak self-check runs over the transformed output and exits
       clean (this is the engine-level check; the TO-4 scanner is the gate).
    8. The mapping table is NEVER written to opal-data-demo, git, logs, or
       messages (ruling R4) — handling documented in the engine + session log.
    9. Engine is structured to run as an EC2 one-shot per the S3-artifact model
       (ruling R6) — no inline VM code.
    10. .tools/ds-commit-gate.sh exits 0 on all engine files; if any file lands
        under data/*/scripts/{gold,silver,bronze}/ it begins with
        `from __future__ import annotations` (CLAUDE.md Rule 15).
    11. Session log with Compiler Tools section committed.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">the two-pass transform engine module(s) — a new standalone path (DS~C's call; document it; NOT under silver/ — this is not a tier conversion)</file>
      <file action="create">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-21/advi_demov1_to2_transform_engine~C.md</file>
      <file action="reference">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/pseudonymizer.py</file>
      <file action="reference">docs/architecture/ADVI_DEMOV1.md, docs/proposals/advisor-intelligence-demo-dataset-20260521.md</file>
      <file action="reference">the TO-0 probe brief — the reconciled PII field inventory</file>
      <file action="reference">docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Implement R1 two-pass determinism: complete mapping table
    in Pass 1; hard-error on unmapped id in Pass 2.</requirement>
    <requirement id="2">Reuse the ADVI_ANONYM field-classification map (R2);
    replace the hash output with a fixed-seed faker producing realistic names.
    Do not modify pseudonymizer.py in place.</requirement>
    <requirement id="3">Re-key S3 PATHS as well as content — PII lives in keys
    (advisor name-slugs, client/account z-ids) per PRD §3 constraint 1.</requirement>
    <requirement id="4">No per-value dollar jitter (R7 / §3 constraint 2);
    value-handling behind a single config switch.</requirement>
    <requirement id="5">Mapping table treated as a secret (R4) — never in the
    demo bucket, git, logs, or messages.</requirement>
    <requirement id="6">EC2 one-shot execution model (R6) — S3 artifact flow,
    no inline VM code. The engine builds + dry-runs in this TO; the live run is
    TO-4.</requirement>
    <requirement id="7">Reconcile the --dry-run plan against TO-0's PII
    inventory — every enumerated PII field must be handled.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">The reviewed two-pass transform engine, committed + pushed to CLOUD</deliverable>
    <deliverable type="document">A --dry-run output sample + the reconciliation against TO-0's PII inventory</deliverable>
    <deliverable type="document">Session log with Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT modify pseudonymizer.py in place — it is live serve-time code.
    The engine is a new standalone module that reuses its field map.</rule>
    <rule>Do NOT apply per-value dollar jitter — it breaks every Σ-identity and
    renders the demo visibly broken (PRD §3 constraint 2).</rule>
    <rule>Do NOT write the mapping table to opal-data-demo, commit it to git, or
    print it to logs/messages — it is a re-identification key (ruling R4).</rule>
    <rule>Do NOT run the engine against the live opal-data-demo bucket in this TO
    — only --dry-run. The populate run is TO-4, and it gates on TO-1 infra +
    TO-0's PII inventory being final.</rule>
    <rule>Do NOT pip install -t into a Lambda dir; this is an EC2 one-shot, not a
    Lambda. Dependencies follow the EC2 code deployment standard.</rule>
  </do_not>
</task_order>
