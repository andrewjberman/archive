<task_order>
  <metadata>
    <id>MDPF_ASSETS.025</id>
    <slug>ds-wse-rescope-full-bd-book-certified-aua</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED 2026-05-20 (COO~B, from CTO~B's relay of Andrew's 2026-05-20 custody-scope ruling -- "Ruling 2"). GO fired to 0.4.0_DS_ClientPlatform. SEQUENCING: .025 (WS-E re-scope) and .024 (aggregator headline-selection, already shipped 70e73d4e8) are INDEPENDENT code changes (WS-E feeder vs aggregator) -- parallel-OK; the headline is correct once both land. MDPF_ASSETS.016 (historical backfill) gates on BOTH .024 AND this TO -- do .025 before .016.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- Andrew custody-scope ruling: the 49F headline contribution must be the full Black Diamond book, not the Schwab-custodied subset. Every daily-forward run currently understates 49F by ~$157M until WS-E is re-scoped.</priority>
    <sla>~0.5d wall -- a focused source-change in one gold script + fixtures + the DS deploy cycle. The change is a SIMPLIFICATION (drops the custodian-crosswalk filter).</sla>
  </metadata>

  <amendment id="2026-05-20-taxonomy-correction" supersedes="every '- sma_aua(1c)' term in the body below">
    URGENT CORRECTION 2026-05-20 (Andrew taxonomy ruling, via CTO~B; PRD v0.8 pending). Andrew verbatim: "1c is a subdivision of 1b, so cant double count that." Cohort 1c (SMA) is a NAMED SUB-SLICE of Cohort 1b (non-model) -- NOT a disjoint first-class sibling. This REVERSES the v0.5 three-way framing. Where the body below conflicts with this block, THIS BLOCK GOVERNS.

    CORRECTED FORMULA: non_model_aua(49F) = certified_aua - model_aua(1a). There is NO "- sma_aua(1c)" / "- 1c" term -- DELETE it wherever the body says it. SMA is INSIDE 1b. sma_aua is emitted as a reported SUB-BREAKDOWN FIELD of 1b ("of which SMA: $X") -- never subtracted, never summed separately. Result: 1b (49F non-model, SMA-inclusive) ~$476.4M (the body's "~$451.6M" is WRONG -- it had SMA carved out); 1c ~$24.8M is a display-only sub-slice reported inside 1b. 49F total (1a + 1b) = certified_aua ~$1,812.4M -- a TWO-cohort decomposition, not three.

    HEADLINE: opal_aggregate_aua = 1a + 1b + 2a (NOT 1a+1b+1c+2a -- 1c is not an additive term). The ~$1,906M total is unchanged; only the decomposition changes.

    MUST-LAND-TOGETHER: MDPF_ASSETS.024 (aggregator) is being reworked in lockstep -- its partner_total must become Σ(model_aua + non_model_aua), two terms, sma NOT added. .024 and .025 MUST be corrected + land TOGETHER (a non_model-including-sma feeder from .025 + a still-3-term .024 sum = a live ~$25M double-count). Do not ship one without the other.

    All ACs and scope steps below are read with "- sma_aua(1c)" deleted and sma_aua re-cast as a non-additive sub-field of 1b.
  </amendment>

  <references>
    <ruling>Andrew 2026-05-20 "Ruling 2" (custody scope, Option C; via CTO~B): the 49 Financial headline contribution = the FULL Black Diamond book, `certified_aua` (~$1,812.4M) -- NOT the Schwab-custodied subset (~$1,655.4M). This REVERSES the 2026-05-18 v0.2 Schwab-only ruling. All four custodians count, including the $135.6M ByAll held-away aggregation. Andrew made the call with the full custody decomposition + the held-away-vs-advised trade-off in front of him -- an informed reversal.</ruling>
    <prd>docs/architecture/MDPF_ASSETS.md PRD v0.7 (commit dc780bcc4) -- §3.4 rewritten as the custody-scope formula of record; §3.0.1 headline figure updated. §3.4 is unambiguous; cite it.</prd>
    <wse_script>data/mdpf/scripts/gold/build_mdpf_wse_49f_non_model_aua.py -- currently computes Cohort 1b off the Schwab-filtered partner_custody_total (wse.compute_partner_custody_total + the Schwab account->custodian crosswalk).</wse_script>
    <certified_aua_source>s3://opal-data-bd/gold/aua_certification/{date}.json, field `.certified_aua` -- the BD gold pipeline's clean daily certified-AUA scalar. Daily-available historically (so .016's backfill can read it per date).</certified_aua_source>
  </references>

  <objective>
    Re-scope the WS-E gold script so Cohort 1b (49F non-model AUA) is computed off the FULL Black Diamond book instead of the Schwab-custodied subset:
      non_model_aua(49F) = certified_aua - model_aua(1a) - sma_aua(1c)
    where certified_aua is read from the BD gold pipeline's aua_certification artifact. This drops the silver/fees custodian-crosswalk Schwab filter entirely -- a simplification.
  </objective>

  <context>
    Today build_mdpf_wse_49f_non_model_aua.py derives 1b as a residual on partner_custody_total, which is the Schwab-custodied book (wse.compute_partner_custody_total + the account->custodian crosswalk filters to Schwab). Andrew's Ruling 2 reverses that: the 49F headline contribution is the full BD book.

    The corrected formula: non_model_aua(49F) = certified_aua - model_aua(1a) - sma_aua(1c). Read certified_aua from s3://opal-data-bd/gold/aua_certification/{date}.json `.certified_aua`. The custodian-crosswalk Schwab-filter logic is REMOVED -- certified_aua is already the clean full-book scalar, so the filter is no longer needed.

    Consequences (CTO~B): 49F total $1,655.4M -> $1,812.4M; Cohort 1b $294.7M -> ~$451.6M; the Model Portfolios headline (1a+1b+1c+2a) moves ~$1,749M -> ~$1,906M (Andrew's ~$1.89B). The aggregator (MDPF_ASSETS.024) needs NO code change -- its cohort-selection logic is unchanged + correct; the headline value moves purely because this TO's 1b output grows.

    KEEP the MDPF_ASSETS.019 reconcile sentinels intact -- 1b is now a LARGER residual (certified - model - sma), so the residual-drift / empty-overwrite protection matters MORE, not less. Do not weaken or bypass them.
  </context>

  <scope>
    <step>Phase 1 -- comp-pipescript io on build_mdpf_wse_49f_non_model_aua.py (below). Direct-read the current partner_custody_total / Schwab-crosswalk derivation + confirm the aua_certification artifact shape (`.certified_aua` field, daily availability).</step>
    <step>Phase 2 -- Replace the Schwab-filtered partner_custody_total derivation with: read certified_aua from s3://opal-data-bd/gold/aua_certification/{date}.json; non_model_aua(49F) = certified_aua - model_aua(1a) - sma_aua(1c). Remove the now-dead custodian-crosswalk Schwab-filter code. Update fixtures to assert the full-book formula (1b ~$451.6M; 49F total = certified_aua). Keep the .019 reconcile sentinels.</step>
    <step>Phase 3 -- DS commit + S3 deploy cycle per Rule 13: safe-commit.sh agent --author -> push CLOUD -> aws s3 cp data/mdpf/scripts/gold/build_mdpf_wse_49f_non_model_aua.py to s3://opal-data-mdpf/code/scripts/gold/ -> comp-pipescript deployed MATCH. comp-validate before signaling.</step>
    <step>Phase 4 -- Empirical: run WS-E on the latest available date; confirm non_model_aua(49F) ~$451.6M, 49F total (1a+1b+1c) = certified_aua ~$1,812.4M, and an end-to-end aggregator run produces the headline ~$1,906M. RAVC2 to COO~B (routed to CTO~B for output validation).</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io data/mdpf/scripts/gold/build_mdpf_wse_49f_non_model_aua.py</run>
        <expect>Confirms the WS-E inputs + the downstream consumer (the WS-A aggregator). COLUMN GAPS clean. (If mdpf scripts return "Unknown script", document the gap + direct-read.)</expect>
        <if_mismatch>Surface any unexpected consumer before shipping -- the 1b value-change is significant (~$157M).</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh data/mdpf/scripts/gold/build_mdpf_wse_49f_non_model_aua.py</run>
        <expect>Exit 0 -- py_compile + AST undefined-name scan (catches any reference left dangling by the removed crosswalk-filter code) + ruff clean. `from __future__ import annotations` first import (Rule 15). No emoji.</expect>
        <if_mismatch>Fix before commit -- especially any name left undefined by the custodian-crosswalk removal.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="before signaling">
      <step>
        <run>comp-pipescript deployed build_mdpf_wse_49f_non_model_aua.py ; comp-validate build_mdpf_wse_49f_non_model_aua --artifact &lt;Phase-4 run artifact&gt;</run>
        <expect>deployed = MATCH; comp-validate exit 0 (or exit-0-ADVISORY with documented WARNs).</expect>
        <if_mismatch>STALE -> re-upload before any run. comp-validate exit 1 -> BLOCKED, do not signal.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <reprocess_required>Forward-only at this TO's scope -- the change takes effect on the next daily mdpf chain run. Historical partitions are re-materialized to the full-book basis by MDPF_ASSETS.016 (which inherits this formula + the certified_aua basis) -- NOT by this TO.</reprocess_required>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: data/mdpf/scripts/gold/build_mdpf_wse_49f_non_model_aua.py ; the WS-E fixture set
    also_in_to: MDPF_ASSETS.024 (aggregator headline-selection) is INDEPENDENT -- parallel-OK, no code overlap (aggregator vs WS-E feeder); the headline is correct once both land. MDPF_ASSETS.016 (historical backfill) gates on BOTH .024 AND this TO -- .016's 49F basis = certified_aua per this re-scope. MDPF_ASSETS.019's reconcile sentinels are KEPT -- verify they still pass against the larger 1b residual. MDPF_ASSETS.022 aligns to PRD v0.7 §3.4.
    last_write_owner: 0.4.0_DS_ClientPlatform owns the WS-E gold script. Single DS lane.
    required_action: Ship .025; then .016. .024 is already shipped (its $-value AC is corrected to ~$1,906M -- see the relay to DS).
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">build_mdpf_wse_49f_non_model_aua.py computes non_model_aua(49F) = certified_aua - model_aua(1a) - sma_aua(1c); certified_aua is read from s3://opal-data-bd/gold/aua_certification/{date}.json `.certified_aua`.</ac>
    <ac id="AC2">The Schwab account->custodian crosswalk filter (wse.compute_partner_custody_total Schwab-subset path) is REMOVED -- no dead crosswalk-filter code left behind; ds-commit-gate AST scan confirms no dangling reference.</ac>
    <ac id="AC3">Empirical: 1b (49F non-model) ~$451.6M; 49F total (1a+1b+1c) = certified_aua ~$1,812.4M; an end-to-end aggregator run yields the headline (1a+1b+1c+2a) ~$1,906M.</ac>
    <ac id="AC4">The MDPF_ASSETS.019 reconcile sentinels are intact + still PASS against the larger 1b residual (not weakened/bypassed).</ac>
    <ac id="AC5">Fixtures updated + all pass, asserting the full-book formula.</ac>
    <ac id="AC6">DS deploy cycle complete: safe-commit.sh agent --author, push CLOUD, aws s3 cp to s3://opal-data-mdpf/code/scripts/gold/, comp-pipescript deployed MATCH. ds-commit-gate exit 0; Rule 15; no emoji. comp-validate exit 0.</ac>
    <ac id="AC7">Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B (routed to CTO~B for output validation). On accept, MDPF_ASSETS.json phase narrative updated.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="modify">data/mdpf/scripts/gold/build_mdpf_wse_49f_non_model_aua.py</file>
    <file action="modify">the WS-E fixture set</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">build_mdpf_wse_49f_non_model_aua.py re-scoped to full-book certified_aua + updated fixtures, S3-deployed (comp-pipescript deployed MATCH).</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT keep the Schwab-custodied subset as the 1b basis -- Andrew's Ruling 2 is explicit: the 49F headline contribution is the FULL BD book (certified_aua). All four custodians count.</rule>
    <rule>Do NOT weaken or bypass the MDPF_ASSETS.019 reconcile sentinels -- 1b is now a larger residual; the drift protection matters more.</rule>
    <rule>Do NOT leave dead custodian-crosswalk code -- remove it cleanly; the ds-commit-gate AST scan must be clean.</rule>
    <rule>Do NOT deploy outside the DS commit->S3 cycle (Rule 13). Do NOT rewrite historical partitions here -- that is .016.</rule>
  </do_not>
</task_order>
