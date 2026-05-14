<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFGRO.TO-000b</id>
    <project>ADVI_INFGRO</project>
    <title>[STAGE 0 FOLLOW-ON] Mechanical-apply CTO-ratified cashflow taxonomy reclassifications + schema flip + INF_C_01 update + ε verify</title>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>complete</status>
    <priority>P1 — gates Stage 1 .001-.006 dispatch (authoring proceeds in parallel against current bucket state)</priority>
    <authorized_by>CTO 5-item ratification table 2026-05-11 21:37Z + Andrew global GO on TWR semantic + Andrew redirect window OPEN on tax-withheld move</authorized_by>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFGRO_PRD.md v0.2 (`b66c07f64`) — §2.3 cashflow taxonomy + §6.TO-000b scope + Appendix C 4-pattern acceptance gates</ref>
    <ref type="stage_0">commit `119b04124` (DS~C) — orion_cashflow_taxonomy.yaml v1 + INF_C_01 refactor + byte-equivalent inheritance verify</ref>
    <ref type="cto_ratification">CTO consolidated 5-item ratification 2026-05-11 21:37Z (msg `20260511T213802Z`)</ref>
    <ref type="ds_c_review">DS~C 5-item review (msg `20260511T213508Z`) + SV disambiguator (`b33f42a63`) + TO-000 RAVC4 (msg `20260511T213535Z`)</ref>
    <ref type="memory_pattern">Dual-track YAML schema (`bucket` active + `prd_proposed_bucket` documentary) — separates ratification from application (5th memory candidate session)</ref>
  </references>

  <context>
    Stage 0 (TO-000) shipped the YAML scaffold + INF_C_01 refactor with byte-equivalent inheritance ($0.0000 delta across 8 metrics). DS~C surfaced 5 open_items for CTO ratification.

    CTO 5-item ratification table delivered 21:37Z (canonical reference for this TO):

    | # | Item | YAML flip | Disposition | Materiality |
    |---|---|---|---|---|
    | 1 | Starting Value | NNA → Internal | **RATIFIED-APPLY** | -$6.64M firm NNA inflow (896 rows / 69 accts; Joe affected 158 rows / $1.47M). Andrew global GO + DS~C 5-signal SV verdict. |
    | 4a | Dividend Paid from Cash | INHERIT EXCLUDE; `prd_proposed_bucket` NNA → Internal | DOC UPDATE | -$172 (101 rows). Trivial. PRD §2.3 hypothesis resolved against; doc catches up to cross-check. |
    | 4b | Income Paid | Same as 4a paired | DOC UPDATE | -$172 paired with 4a. |
    | tax | Federal/State/Foreign Tax Withheld + Tax Credit | NNA outflow → Return | **RATIFIED-APPLY** | +$2.33M firm NNA-outflow reduction (2,561 rows; Joe: 61 Federal Tax = -$42K). PRD §2.3 Bucket C aligned with Andrew's "GRO is market performance not friction" intent. |
    | other-variants | Client/Rollover Contribution + Merge In/Out variants under "Other" activity_category | Internal → NNA | **RATIFIED-APPLY** | ~$3K (40 rows). Trivial. PRD §2 structural note 2. |

    **Andrew redirect window OPEN on tax-withheld move.** If Andrew objects, that sub-scope deferred; other 4 items ship independently. CTO confidence aligned with Andrew's stated GRO intent.

    Schema flip (compound key → type_desc-only) is the structural consequence of accepting all reclassifications. DS~B's Stage -1 audit + DS~C's TO-000 ratified compound for variant-preservation; post-ratification, variant collapse becomes safe.

    ε verification on 30-day sample window per CVO measure-not-assume ruling. Phase A surfaces ε as data quality, NOT failure.
  </context>

  <scope>
    <step>Phase 1 — Pre-write reads:
      Re-read `data/orion/scripts/silver/orion_cashflow_taxonomy.yaml` (v1 from Stage 0).
      Read INF_C_01 current state (`87dcd38db99c5b24` from Stage 0 ship).
      Read CTO ratification table (above) + DS~C 5-item review.
      Run `comp-blast canonical_nna` baseline for empirical-downstream confirmation.
    </step>

    <step>Phase 2 — YAML mechanical apply (3 bucket flips + 2 doc updates):

      **2a APPLY — Item 1 Starting Value (NNA → Internal):**
      - Locate Starting Value entries by (type_desc="Starting Value", activity_category=*)
      - Flip `bucket: NNA` → `bucket: Internal`
      - Update `rationale` to cite DS~C's 5-signal verdict + `b33f42a63` SV disambiguator
      - Materiality note: -$6.64M firm NNA inflow

      **2b APPLY — Tax-withheld + Tax Credit (NNA outflow → Return):**
      - Locate entries: Federal Tax Withheld, State Tax Withheld, Foreign Tax Withheld, Tax Credit
      - Flip `bucket: NNA` → `bucket: Return`
      - Update `rationale` to cite PRD §2.3 Bucket C + Andrew intent (GRO = market performance, taxes = friction-on-return)
      - Materiality note: +$2.33M firm NNA-outflow reduction (2,561 rows)

      **2c APPLY — Other-variants (Internal → NNA):**
      - Locate entries: Client Contribution / Rollover Contribution / Merge In / Merge Out under (activity_category="Other") subset
      - Flip `bucket: Internal` → `bucket: NNA`
      - Update `rationale` to cite PRD §2 structural note 2 (variant collapse)
      - Materiality note: ~$3K (40 rows)

      **2d DOC UPDATE — 4a/4b prd_proposed_bucket (NNA → Internal):**
      - Locate entries: Dividend Paid from Cash, Income Paid
      - Keep `bucket: Internal` (no functional change)
      - Update `prd_proposed_bucket: NNA` → `prd_proposed_bucket: Internal`
      - Update `rationale` to note CTO inherit-decision resolved against PRD §2.3 hypothesis; $34K materiality below ε noise floor
    </step>

    <step>Phase 3 — Schema flip (compound key → type_desc-only):
      Stage 0 used compound key `(type_desc, activity_category)` to preserve variant-row handling. Post-reclassification, the "Other" activity_category variants collapsed into their primary type_desc buckets (2c).

      Refactor YAML schema:
      - Each `types` entry now keyed by `type_desc` only (drop `activity_category` key field)
      - Where multiple compound entries existed for same type_desc with different activity_category, MERGE into single type_desc entry (record activity_category values in a `merged_from_categories` list for audit trail)
      - VERIFY no compound-key entries had different `bucket` values per activity_category (if any, surface as separate open_item — DO NOT silently merge)
    </step>

    <step>Phase 4 — INF_C_01 consume new schema:
      Update `INF_C_01.canonical_nna.py` taxonomy loader:
      - Change lookup key from (type_desc, activity_category) compound → type_desc-only
      - Verify all current canonical_nna.parquet output rows have type_desc present (should be 100% since Stage 0 byte-equivalence verified)
      - Preserve all 3-bucket semantic (NNA / Internal / Return → NNA inclusion logic unchanged: NNA rows emitted, Internal+Return excluded)
    </step>

    <step>Phase 5 — ε verification on 30-day sample window (CVO measure-not-assume):
      Run INF_C_01 against current silver for trailing 30-day window. Compare:
      - Pre-TO-000b (post-Stage 0): canonical_nna.parquet baseline
      - Post-TO-000b: canonical_nna.parquet with reclassifications applied
      
      Expected delta direction:
      - Starting Value bucket flip → -$6.64M NNA inflow on full-history; pro-rated for 30-day window
      - Tax flip → +$2.33M NNA-outflow reduction on full-history; pro-rated for 30-day window
      - Other-variants → ~$3K trivial
      
      Document actual deltas + ratio to expected. Surface any unexpected (>10% deviation from predicted) as ε data quality signal — NOT failure, just empirical surfacing per CVO ruling.
    </step>

    <step>Phase 6 — Pre-commit gate per CLAUDE.md rule 14:
      `.tools/ds-commit-gate.sh data/orion/scripts/silver/orion_cashflow_taxonomy.yaml data/orion/scripts/gold/INF_C_01.canonical_nna.py`
    </step>

    <step>Phase 7 — Commit + push + S3 deploy + manual SHA verify:
      safe-commit.sh with author "0.4.0_DS_ClientPlatform~C". Push CLOUD. Manual SHA verify both files on S3.
    </step>

    <step>Phase 8 — RAVC2 to COO with:
      - Commit SHA + S3 ETag MATCH for both files
      - Joe Brandenburg full-history NNA: pre/post deltas (expected -$1.47M from SV; +$42K from tax; net -$1.43M)
      - Firm-level full-history NNA: pre/post deltas (expected -$4.31M net: -$6.64M SV - $3K other +$2.33M tax)
      - 30-day window deltas (pro-rated)
      - Empirical ε signal: actual vs predicted deviation %
      - Any DOC UPDATE entries (4a/4b) verified
      - Schema collapse audit: any compound-key entries with bucket conflict surfaced
    </step>
  </scope>

  <acceptance_criteria>
    1. YAML 3 bucket flips applied (Items 1, tax, other-variants) per CTO ratification.
    2. YAML 2 doc updates (4a/4b prd_proposed_bucket) applied.
    3. Schema flipped compound → type_desc-only with merged_from_categories audit trail.
    4. INF_C_01 refactored to consume type_desc-only schema.
    5. ε verification on 30-day sample shows actual deltas within 10% of predicted (or explained surfacing).
    6. Pre-commit gate exits 0.
    7. S3 deploy SHA MATCH on both files.
    8. RAVC2 includes Joe + firm-level full-history NNA deltas + 30-day window deltas + schema collapse audit.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      `comp-blast canonical_nna` baseline for empirical-downstream confirmation
      `comp-pipescript io INF_C_01` (current state)
    </phase>
    <phase id="2" when="before commit">
      `.tools/ds-commit-gate.sh` on edited .py + .yaml files
      Local ε verification run
    </phase>
    <phase id="3" when="after commit">
      Manual SHA verify on S3 deploy (both files)
      Sample canonical_nna.parquet read post-rerun to confirm bucket flip effects + schema flip
    </phase>
  </compiler_tools_mandate>

  <notes>
    **Architectural-pattern enforcement (PRD v0.2 Appendix C):**
    - C.1 walk-back: N/A (no bronze partition reads in this TO; pure YAML+INF_C_01 refactor)
    - C.2 bug-shadows: APPLY — confirm zero inline classifier remaining post-refactor in INF_C_01 (grep verification)
    - C.3 internal parity: APPLY — single-path declaration at top of INF_C_01 for YAML location (env > script-dir > repo-relative); docstring-aligned
    - C.4 code/docstring divergence: APPLY — verify INF_C_01 docstring + path constants align; manual grep

    **Andrew redirect window on tax-withheld (Item 2 / 2b):**
    If Andrew objects to NNA → Return reclassification BEFORE you ship, ratchet TO-000b acceptance to defer 2b. Schema flip (Phase 3) + 4a/4b doc updates + Item 1 SV + other-variants are independent and can still ship. Surface CTO + COO immediately if Andrew objects.

    **Dual-track YAML schema preserves:**
    - `bucket` = active state INF_C_01 reads
    - `prd_proposed_bucket` = documentary record of PRD §2.3 hypothesis
    - 4a/4b doc update demonstrates pattern: cross-check resolved against hypothesis → doc catches up without functional change

    **Stage 1 dispatch gate:** dispatching Stage 1 .001-.006 follows your RAVC2 close on this TO. Stage 1 authoring proceeds against current `bucket` field in parallel — COO authoring shape sequence-independent.

    **Effort estimate:** ~2-3h. Mechanical YAML edits (~30min) + schema flip (~30min) + INF_C_01 refactor (~30min) + ε verification (~45min) + commit/deploy/verify/RAVC2 (~30min).

    **Today's DS~C session — pace yourself:** TO-8 + SV verdict + TO-000 + Bug A audit (in flight) + TO-000b would be 5 substantive ships in one session. Reasonable but watch fatigue — surface if depth-of-attention is suffering.
  </notes>
</task_order>
