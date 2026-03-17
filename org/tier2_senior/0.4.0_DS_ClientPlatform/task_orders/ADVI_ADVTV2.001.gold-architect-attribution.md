<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-03-17-gold-architect-attribution</id>
    <issued_by>0.4.0_DE_ClientPlatform</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-17</date>
    <status>complete</status>
  </metadata>

  <objective>
    Productionize the architect attribution decision tree (`.tmp_architect_attribution.py`)
    into a new gold script that writes a `resolved_architect` column. This replaces the
    raw `architect` field as the canonical architect assignment for all downstream ADV views.
    The leaderboard, Top 3, rolling flows, and all ADV analytics must show ONLY the 19
    true architects with correctly attributed AUA — no 49F House, no Unassigned, no stale
    architects.
  </objective>

  <scope>
    <files>
      <file action="create">data/black_diamond/scripts/gold/08b_build_architect_attribution.py</file>
      <file action="modify">data/black_diamond/scripts/gold/08_build_nna_aua_by_advisor.py</file>
      <file action="modify">data/black_diamond/scripts/gold/run_gold_layer.sh</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Create `08b_build_architect_attribution.py` that implements the full T0-T16 decision
      tree from `.tmp_architect_attribution.py`. It must:
      (a) Define the 19 true architects via the T0 filter (AUA >= $5M, relationships >= 5,
          not 49F House/Unassigned, at least 1 new account in trailing 12M).
      (b) Build implementor->architect pairing maps at 80% and 60% thresholds.
      (c) Run T1-T16 in order: direct architect, implementor (true/80%/60%), relationship
          inheritance (4 passes), portfolio_group (true/junior), local_relationship 60%,
          consultant (true/80%/60%), additional_advisor (true/junior).
      (d) Scope to FUNDED accounts only (accounts present in account_performance with AUA > 0).
      (e) Write output to S3: `gold/views/architect_attribution.parquet` with columns:
          account_id, relationship_id, resolved_architect, tier (T1_direct ... T16_rel_inherit_4),
          original_architect, original_implementor.
      (f) Also write `gold/views/rel_architect_lookup.parquet` with the attributed
          relationship->architect mapping (modal resolved_architect per relationship),
          REPLACING the current output from script 08.
      (g) Print tier summary and conservation check (resolved + unresolved = total).
    </requirement>

    <requirement id="2">
      Modify `08_build_nna_aua_by_advisor.py` `load_relationship_advisors()` to READ
      `gold/views/rel_architect_lookup.parquet` (which 08b now writes) instead of
      deriving it from raw accounts_dimension. Script 08 should no longer call
      `modal_str` on the raw architect field — it consumes the attributed lookup.
      If `rel_architect_lookup.parquet` is missing, fail with a clear error:
      "Run 08b_build_architect_attribution.py first."
    </requirement>

    <requirement id="3">
      The attributed lookup must contain ONLY the 19 true architects plus "Unresolved"
      (for the ~277 accounts / ~1.7% AUA residual). No 49F House, no Unassigned, no
      stale architects. Downstream scripts 09 and 10 will automatically pick this up
      since they read from `rel_architect_lookup.parquet`.
    </requirement>

    <requirement id="4">
      Add consultant and additional_advisor fields to `00_build_accounts_dimension.py`
      so they are available in the gold layer for T11-T15. Currently these fields exist
      in silver transactions but are dropped during the gold build. Carry them through
      as `consultant` and `additional_advisor` columns in `accounts_dimension_latest.parquet`.
    </requirement>

    <requirement id="5">
      Normalize "Olivia Shin" -> "Liv Shin" in the architect field during
      `00_build_accounts_dimension.py` gold build (confirmed typo duplicate with
      overlapping relationship).
    </requirement>

    <requirement id="6">
      Update `run_gold_layer.sh` to run `08b_build_architect_attribution.py` AFTER
      script 08's dependencies (00, 05b) but BEFORE script 08 itself. The new
      execution order: ... -> 05b -> 08b -> 08 -> 09 -> 10.
    </requirement>

    <requirement id="7">
      Validate output by comparing the 19-architect AUA totals and account counts
      against the research output in `.tmp_architect_attribution.py`. Small variance
      is expected (daily data refresh) but the architect list and tier distribution
      pattern should match.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      `python 08b_build_architect_attribution.py` runs end-to-end, reads from S3,
      writes `architect_attribution.parquet` and `rel_architect_lookup.parquet` to S3.
    </criterion>
    <criterion id="2">
      `rel_architect_lookup.parquet` contains exactly 19 distinct architect names plus
      "Unresolved". No 49F House, no Unassigned, no stale architects.
    </criterion>
    <criterion id="3">
      Conservation check passes: resolved + unresolved = total funded accounts.
    </criterion>
    <criterion id="4">
      Scripts 09 and 10 run successfully against the new lookup without code changes
      (they already read `rel_architect_lookup.parquet`).
    </criterion>
    <criterion id="5">
      `run_gold_layer.sh` executes the full chain including 08b without errors.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify scripts 09 or 10 — they consume rel_architect_lookup.parquet as-is.</constraint>
    <constraint>Do NOT remove the modal_str function from 08 — other callers may use it. Just stop calling it for the architect lookup.</constraint>
    <constraint>The T0 filter (19 architects) is deterministic from the data. Do NOT hardcode architect names — compute them from the filter criteria each run so the list updates if the data changes.</constraint>
    <constraint>Consultant and additional_advisor fields (req 4) come from silver transactions. Use the same S3 bucket (opal-data-bd) and key pattern as the existing silver readers in 00_build_accounts_dimension.py.</constraint>
    <constraint>No emojis in code or print statements (CLAUDE.md rule 13).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="none" status="complete">
      Research deliverable `.tmp_architect_attribution.py` and DS log
      `logs/2026-03-13/advi_mvplvl_003_architect_attribution_tree.md` — decision tree
      validated against 5,423 funded accounts, 98.3% AUA resolved.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">New script `08b_build_architect_attribution.py` + modifications to 08 and 00</deliverable>
    <deliverable type="commit">Updated `run_gold_layer.sh` with correct execution order</deliverable>
    <deliverable type="document">Updated `data_contract.xml` reflecting the new `architect_attribution.parquet` output and `rel_architect_lookup.parquet` schema change</deliverable>
  </deliverables>
</task_order>
