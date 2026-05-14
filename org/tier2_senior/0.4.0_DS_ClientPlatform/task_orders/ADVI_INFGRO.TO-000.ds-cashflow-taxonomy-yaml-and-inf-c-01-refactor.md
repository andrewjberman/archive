<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFGRO.TO-000</id>
    <project>ADVI_INFGRO</project>
    <title>[STAGE 0 FOUNDATION] Author orion_cashflow_taxonomy.yaml + refactor INF_C_01 to consume from it (inherit JOE-TXN-BACKFILL classifications)</title>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>complete</status>
    <priority>P1 — Stage 0 foundation; gates Stage 1 + Stage 2 TOs</priority>
    <authorized_by>Andrew global GO on ADVI_INFGRO (TWR semantic) + CTO PRD v0.1 `0f5db3046` §6.TO-000 (v0.2 amendment in flight, no scope change)</authorized_by>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFGRO_PRD.md v0.1 (`0f5db3046`); §2.3 cashflow taxonomy + §6.TO-000 scope</ref>
    <ref type="empirical_audit">DS~B Stage -1 audit (org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-11/DS_B_session*_stage_neg_1_audit.md) — 1,145,124 rows / 43 distinct type_desc / 14 activity_category buckets</ref>
    <ref type="empirical_audit">DS~C SV disambiguator log (`b33f42a63`) — Starting Value INTERNAL/seed verdict (5-signal evidence + 39-account unrecorded-NNA caveat)</ref>
    <ref type="canonical_lineage">INF_C_01.canonical_nna `23c1f560c` (Merge In/Out classification per Andrew gut-check) — MUST be inherited, NOT re-decided</ref>
    <ref type="cvo_invariant">PRD §2.4 architectural invariant: AUA_growth = NNA + Return + ε</ref>
  </references>

  <context>
    Stage 0 foundation TO for ADVI_INFGRO project. Andrew gave global GO on the TWR-based GRO architecture; CTO authored PRD v0.1 with three-bucket primary cashflow taxonomy (NNA / Internal / Return) + 8-category secondary sub-classification.

    Currently INF_C_01.canonical_nna.py has the cashflow classification logic INLINE (Merge In/Out per JOE-TXN-BACKFILL `23c1f560c`). Stage 0 extracts this to a declarative YAML so:
    - Stage 1 (.001-.006) Return computation can consume the same Internal exclusions as NNA
    - PRD §2.3 ratification is a YAML edit, not a code change
    - CTO/COO can update taxonomy without DS code-review cycles for non-logic changes

    CRITICAL: this TO MUST INHERIT the JOE-TXN-BACKFILL Merge In/Out classification. NOT re-decide. The YAML is a refactor target, not a re-architecture.

    Per CTO routing decision (post-Bug-A-downgrade): DS~C assigned. Bug A audit no longer blocking; DS~C's clean session is the right fit. DS~A standdown for the day.
  </context>

  <scope>
    <step>Phase 1 — Pre-write reads:
      Read PRD §2.3 (canonical 3-bucket cashflow taxonomy) + §6.TO-000 (this TO's spec in CTO's authoring):
        `docs/architecture/ADVI_INFGRO_PRD.md`
      Read existing INF_C_01 classification logic:
        `data/orion/scripts/gold/INF_C_01.canonical_nna.py` (rep_bucket=individual, Merge In/Out classifier)
      Read JOE-TXN-BACKFILL commit context:
        `git show 23c1f560c`
      Read DS~B Stage -1 audit findings:
        `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-11/DS_B_session*_stage_neg_1_audit.md`
      Read DS~C SV disambiguator log (your own session 2 work):
        `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-11/DS_C_session2_starting_value_disambiguator_2026-05-11.md`
    </step>

    <step>Phase 2 — Author `data/orion/scripts/silver/orion_cashflow_taxonomy.yaml`:
      Schema shape (YAML, declarative):
      ```yaml
      version: 1
      authored_by: 0.4.0_DS_ClientPlatform~C
      authored_date: 2026-05-11
      source: ADVI_INFGRO PRD v0.1 §2.3 + DS~B Stage -1 audit + DS~C SV verdict
      
      # Primary classification (3-bucket per architectural invariant AUA_growth = NNA + Return + ε)
      buckets:
        NNA:
          description: Net New Assets — actual cash/asset movements at firm perimeter
          types:
            - type_desc: "Client Contribution"
              direction: in
              sub_category: CASHFLOW_IN
              rationale: client deposits new cash
            - type_desc: "Rollover"
              direction: in
              sub_category: CASHFLOW_IN
            - type_desc: "Merge In from Other Account"
              direction: in
              sub_category: CASHFLOW_IN
              rationale: per JOE-TXN-BACKFILL 23c1f560c inheritance — new asset perimeter inflow
            # ... (continue enumerating from DS~B's audit Items 2, 3 per CTO endorsements: Merge In/Out Exchange 350 pairs = Internal; Cancel Account 101 = NNA outflow)
        
        Internal:
          description: NNA-neutral movements within firm perimeter — no real cash/asset change
          types:
            - type_desc: "Starting Value"  # 896 rows / $6.64M — DS~C empirical INTERNAL/seed verdict
              direction: neutral
              sub_category: ADJUSTMENT
              rationale: synthetic system seed (5-signal evidence: zero MI co-occurrence + anchor-date pattern + security-name descriptions + sub-type proper-usage-on-other-dates + 503-row top-account signature)
              caveat: 39 accounts have ONLY SV (no other Contribution sub-types) — partner-facing NNA under-stated by ~$X subset of $6.64M (better than double-counting)
            - type_desc: "Merge Out to Other Account" 
              direction: neutral
              sub_category: INTERNAL_TRANSFER
              rationale: per JOE-TXN-BACKFILL inheritance
            # ... (Items 2 Exchange In/Out 350 pairs per CTO)
        
        Return:
          description: Performance-relevant — generates growth/loss within firm perimeter
          types:
            - type_desc: "Dividend"
              direction: in
              sub_category: INCOME
            # ... (Item 4 Dividend Paid from Cash + Income Paid per CTO default INF_C_01-cross-check task)
      
      # Open items (REVIEW class — pending CTO ratification or empirical disambiguator)
      open_items:
        - type_desc: ...
          state: REVIEW
          notes: ...
      ```
      
      Encode ALL 43 type_desc from DS~B Stage -1 audit. Use DS~B's 4 REVIEW dispositions (CTO defaults per their 21:00Z message) + DS~C's SV INTERNAL/seed verdict.
    </step>

    <step>Phase 3 — Refactor `INF_C_01.canonical_nna.py`:
      - Add YAML loader: `from yaml_load_taxonomy import load_taxonomy`
      - Replace inline Merge In/Out classifier with lookup against YAML buckets["NNA"] / buckets["Internal"]
      - PRESERVE BEHAVIOR — current INF_C_01 output (8001 canonical_nna rows / Joe NNA $11.69M MAX) MUST replicate exactly post-refactor
      - Inheritance test (CRITICAL): run before-and-after on same silver/transactions snapshot. canonical_nna.parquet rows must match within $1 tolerance.
    </step>

    <step>Phase 4 — Pre-commit gate per CLAUDE.md rule 14:
      `.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_C_01.canonical_nna.py data/orion/scripts/silver/orion_cashflow_taxonomy.yaml`
      (py_compile + ds-precommit-check + ruff)
    </step>

    <step>Phase 5 — Behavioral inheritance verification:
      Run INF_C_01 locally on current silver snapshot. Compare output to last canonical_nna.parquet on S3:
      - Total row count match (±0)
      - Per-advisor NNA sums match within $1
      - Joe Brandenburg MAX NNA: $11,729,310 (per ADVI_INFNNA Joe-fix verdict; should be unchanged)
      Document delta in RAVC2 — any unexpected divergence = bug.
    </step>

    <step>Phase 6 — Commit + push + S3 deploy + manual SHA verify:
      safe-commit.sh with author "0.4.0_DS_ClientPlatform~C". Push CLOUD. AE-side safe-deploy gate auto-fires on push.
      Manual SHA verify INF_C_01 deployed (canonical_nna_loader path on Lambda + EC2 gold runner consume YAML).
    </step>

    <step>Phase 7 — RAVC2 to COO with:
      - Commit SHA + S3 ETag MATCH for INF_C_01
      - YAML committed (referenced from INF_C_01 via relative path or repo-root absolute)
      - 43 type_desc enumerated + classified
      - Inheritance test PASS evidence (row count + per-advisor NNA + Joe MAX NNA)
      - Any REVIEW-class open_items flagged for CTO ratification before Stage 1 dispatch
    </step>
  </scope>

  <acceptance_criteria>
    1. `data/orion/scripts/silver/orion_cashflow_taxonomy.yaml` shipped — 43 type_desc enumerated with primary 3-bucket assignment.
    2. JOE-TXN-BACKFILL Merge In/Out classification inherited EXACTLY (NOT re-decided).
    3. DS~C SV verdict encoded as INTERNAL/seed with empirical-evidence rationale + 39-account caveat.
    4. INF_C_01 refactored to consume from YAML; inline classifier removed.
    5. Behavioral inheritance test PASS: canonical_nna.parquet rows match prior output within $1.
    6. Joe Brandenburg MAX NNA = $11,729,310 (unchanged).
    7. Pre-commit gate exits 0.
    8. S3 deploy MATCH.
    9. RAVC2 includes inheritance evidence + any REVIEW-class open_items.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      `comp-pipescript io INF_C_01` (current consumer of classification logic)
      `comp-blast canonical_nna` (downstream coverage — should be INF_C_02 + INF_D_00c primarily)
    </phase>
    <phase id="2" when="before commit">
      `.tools/ds-commit-gate.sh` on edited .py + .yaml files
      Local behavioral inheritance verify run
    </phase>
    <phase id="3" when="after commit">
      `comp-pipescript deployed INF_C_01` MATCH post-S3-cp
      Sample canonical_nna.parquet read to confirm row count + per-advisor NNA preservation
    </phase>
  </compiler_tools_mandate>

  <notes>
    **Inheritance discipline:** This is a REFACTOR, NOT an architecture-change. If you discover what you believe is a classification bug during enumeration, FLAG it in RAVC2 as a REVIEW open_item — do NOT fix it inline. CTO ratification needed for any classification changes.

    **PRD v0.2 awareness:** CTO authoring v0.2 amendment now (~5min ETA). v0.2 may rename §6.TO-000 to TO-000 or shift section numbering. Reference whichever is current at commit time. v0.2 doesn't change Stage 0 scope.

    **Stage 1 dependency:** Stage 1 TOs (.001-.006) gate on this YAML existing. Author dispatch will follow your RAVC2 close + any CTO REVIEW ratification.

    **Effort estimate:** ~2-4h. Read + enumerate + author YAML (~1h) + refactor INF_C_01 (~30min) + inheritance verify (~30min) + commit/deploy/verify (~30min) + RAVC2 (~30min).

    **Memory entry candidate (for post-EOD batch):** "Declarative taxonomy YAML over inline classifier" — the refactor pattern this TO instantiates.
  </notes>
</task_order>
