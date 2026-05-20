<task_order>
  <metadata>
    <id>MDPF_ASSETS.024</id>
    <slug>ds-aggregator-headline-formula-1a1b1c2a</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED 2026-05-20 (COO~B, from CTO~B's relay of Andrew's 2026-05-20 headline-formula ruling). GO fired to 0.4.0_DS_ClientPlatform (idle-available). This TO is SEQUENCED FIRST in the DS MDPF lane -- MDPF_ASSETS.016 (Cohort 0 historical backfill) gates on it: .016's build_mdpf_process_backfill.py imports mdpf_aggregate_aua, so fixing the headline formula here propagates to the backfill automatically. Do .024 then .016.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- every daily-forward mdpf chain run currently emits a headline opal_aggregate_aua that includes Cohort 2b, which Andrew's 2026-05-20 ruling excludes. High priority (the live headline is wrong by ~$106M), but not P0 -- no portal consumer is live yet (WS-F is Phase 3).</priority>
    <sla>~0.5d wall -- a focused formula change in one gold script + fixtures + the DS deploy cycle.</sla>
  </metadata>

  <references>
    <ruling>Andrew 2026-05-20 (verbatim, via CTO~B): "Cohort 0 must be tracked every day, but it must not be incorporated into Model Portfolios total AUA... We need it for audit but we will not be including it in visible MDPF pipeline to portal. The Model Portfolios global AUA will only be cohort 1a 1b 1c and 2a at this point in time." This SUPERSEDES the WS-A contract §7-Q3 "Opal Aggregate Advised AUA = sum over N>=1 of (Na+Nb)" record (which included 2b).</ruling>
    <prd_amendment>CTO~B is authoring an MDPF_ASSETS PRD amendment as the headline-formula ruling-of-record; reference it once committed (CTO~B will relay the ref). This TO may proceed on the ruling text above -- the spec is unambiguous.</prd_amendment>
    <aggregator>data/mdpf/scripts/gold/mdpf_aggregate_aua.py -- the WS-A canonical aggregator. Currently sets opal_aggregate_aua = partner_total (all cohorts, including 2b Inflection non-model).</aggregator>
    <current_values>Live 2026-05-20 chain (run mdpf_daily_20260520_151238): opal_aggregate_aua $1,854,284,758.53 includes 2b. Post-fix the headline drops to ~$1,749,050,238 (1a+1b+1c+2a); 2b (~$106.11M) + Cohort 0 / etf_public_residual move to audit fields.</current_values>
  </references>

  <objective>
    Change the WS-A aggregator's headline definition: opal_aggregate_aua = Cohort 1a + 1b + 1c + 2a ONLY. Cohort 2b (Inflection non-model) and Cohort 0 / etf_public_residual_total are retained as explicit AUDIT fields on the artifact but are NOT part of the opal_aggregate_aua total. The §7 reconciliation must be updated consistently so it does not false-fail against the new headline definition.
  </objective>

  <context>
    Andrew's ruling: the Model Portfolios global headline AUA = 1a (49F model) + 1b (49F non-model) + 1c (49F SMA) + 2a (Inflection model). Excluded from the headline but still computed + tracked + retained as audit fields: Cohort 2b (Inflection non-model) and Cohort 0 (ETF public residual). Cohort 0 additionally is not emitted to the portal-facing slice at all.

    Today mdpf_aggregate_aua.py sets opal_aggregate_aua = partner_total = sum over partners of (model + sma + non_model) -- which includes 2b. The fix: opal_aggregate_aua = partner_total - cohort_2b (equivalently, 1a+1b+1c+2a directly from the cohort components). Emit `cohort_2b` (or the existing inflection non_model figure) and `etf_public_residual_total` / cohort_0 as named audit fields distinct from the headline. The artifact must make it unambiguous which number is the headline and which are audit-only.

    §7 reconciliation: the existing identity checks reference opal_aggregate_aua. They must be updated so identity_1 / identity_2 / identity_3 reconcile against the NEW headline definition (1a+1b+1c+2a) -- not the old partner_total -- so a correct run does not false-fail. The reconcile must still independently verify the 2b + Cohort-0 audit figures (drop-rather-than-fabricate discipline preserved).

    Daily-forward impact: this changes every subsequent mdpf chain run's headline. No portal consumer is live (WS-F Phase 3), so there is no FE breakage; but the platinum artifact's headline changes value the next run. MDPF_ASSETS.016 (historical backfill) and .022 (broader-1b canonical alignment) both must use this same formula -- .016 inherits it via build_mdpf_process_backfill.py's import of this aggregator; .022 is flagged to align when picked up.
  </context>

  <scope>
    <step>Phase 1 -- comp-pipescript io on mdpf_aggregate_aua.py (below). Direct-read the current opal_aggregate_aua computation + the §7 identity block + the cohort component variables (confirm 1a/1b/1c/2a/2b are individually addressable).</step>
    <step>Phase 2 -- Change opal_aggregate_aua = 1a + 1b + 1c + 2a. Emit cohort_2b and etf_public_residual_total / cohort_0 as explicit named AUDIT fields on the aggregate block, clearly distinct from the headline. Update the §7 identity checks to reconcile against the new headline definition (and still independently verify the audit figures). Update fixtures (mdpf_aggregate_aua_fixtures.py) to assert the new headline + the audit-field separation; add a fixture that would FAIL if 2b leaked back into the headline.</step>
    <step>Phase 3 -- DS commit + S3 deploy cycle per Rule 13: safe-commit.sh agent --author -> push CLOUD -> aws s3 cp data/mdpf/scripts/gold/mdpf_aggregate_aua.py to s3://opal-data-mdpf/code/scripts/gold/ -> comp-pipescript deployed MATCH. comp-validate on the script before signaling.</step>
    <step>Phase 4 -- Empirical: run the aggregator on the latest available date; confirm opal_aggregate_aua = 1a+1b+1c+2a (~$1.749B vs the current ~$1.854B), cohort_2b + etf_public_residual present as audit fields, §7 reconcile PASS. RAVC2 to COO~B with the before/after headline + the audit-field block.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io data/mdpf/scripts/gold/mdpf_aggregate_aua.py</run>
        <expect>Confirms the aggregator's inputs (the WS-B/C/D/E feeders) + PORTAL CONSUMERS of the platinum artifact. COLUMN GAPS clean. (mdpf scripts are partially comp-graph-modeled -- if it returns "Unknown script", document the gap and direct-read the script instead.)</expect>
        <if_mismatch>If a portal consumer is already wired to opal_aggregate_aua, surface to COO~B before shipping -- a live headline value-change would be page-visible.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh data/mdpf/scripts/gold/mdpf_aggregate_aua.py</run>
        <expect>Exit 0 -- py_compile + AST undefined-name scan + ruff all clean. `from __future__ import annotations` first import (Rule 15). No emoji.</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="before signaling">
      <step>
        <run>comp-pipescript deployed data/mdpf/scripts/gold/mdpf_aggregate_aua.py ; comp-validate mdpf_aggregate_aua --artifact &lt;the Phase-4 run artifact&gt;</run>
        <expect>deployed = MATCH (the runner has the new code). comp-validate exit 0 (or exit-0-ADVISORY with documented WARNs).</expect>
        <if_mismatch>STALE -> re-upload to S3 before any run. comp-validate exit 1 -> BLOCKED, do not signal.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <reprocess_required>Forward-only at this TO's scope -- the change takes effect on the next daily mdpf chain run. Historical partitions are re-materialized to the new headline by MDPF_ASSETS.016 (which inherits this formula via the build_mdpf_process_backfill.py import) -- NOT by this TO. This TO does not itself rewrite historical partitions.</reprocess_required>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: data/mdpf/scripts/gold/mdpf_aggregate_aua.py ; mdpf_aggregate_aua_fixtures.py
    also_in_to: MDPF_ASSETS.016 (historical backfill) is SEQUENCED AFTER this TO and inherits the formula via build_mdpf_process_backfill.py's import of this aggregator -- do .024 then .016. MDPF_ASSETS.022 (broader-1b canonical alignment) must also align to the 1a+1b+1c+2a headline -- COO~B flags it at .022 dispatch. MDPF_ASSETS.019's reconcile-block sentinels were shipped against the old headline -- verify they still pass against the new definition (or note the interaction).
    last_write_owner: 0.4.0_DS_ClientPlatform owns the WS-A aggregator. Single DS lane -- no tilde engagement.
    required_action: Ship .024 first; .016 follows.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">mdpf_aggregate_aua.py: opal_aggregate_aua = Cohort 1a + 1b + 1c + 2a. Verified by direct read + a fixture that fails if 2b is included.</ac>
    <ac id="AC2">cohort_2b (Inflection non-model) and etf_public_residual_total / cohort_0 are emitted as explicit, named AUDIT fields on the aggregate block, unambiguously distinct from the opal_aggregate_aua headline.</ac>
    <ac id="AC3">The §7 identity checks reconcile against the new headline definition -- a correct run PASSes identity_1/2/3 and does NOT false-fail; the 2b + Cohort-0 audit figures are still independently verified.</ac>
    <ac id="AC4">Fixtures (mdpf_aggregate_aua_fixtures.py) updated + all pass, including a new fixture asserting 2b is excluded from the headline.</ac>
    <ac id="AC5">Empirical run on the latest date: opal_aggregate_aua reflects 1a+1b+1c+2a (~$1.749B, down from ~$1.854B); cohort_2b ~$106.11M + etf_public_residual present as audit fields; §7 reconcile PASS. Before/after captured.</ac>
    <ac id="AC6">DS deploy cycle complete: safe-commit.sh agent --author, push CLOUD, aws s3 cp to s3://opal-data-mdpf/code/scripts/gold/, comp-pipescript deployed MATCH. ds-commit-gate exit 0; Rule 15 (`from __future__ import annotations`); no emoji. comp-validate exit 0.</ac>
    <ac id="AC7">Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B with the before/after headline + the audit-field block + the §7 reconcile result. On accept, MDPF_ASSETS.json phase narrative updated.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="modify">data/mdpf/scripts/gold/mdpf_aggregate_aua.py</file>
    <file action="modify">mdpf_aggregate_aua_fixtures.py (the WS-A fixture set)</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">mdpf_aggregate_aua.py headline-formula change + updated fixtures, S3-deployed (comp-pipescript deployed MATCH).</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT leave 2b in the opal_aggregate_aua headline -- Andrew's ruling is explicit: headline = 1a+1b+1c+2a only. 2b is audit-only.</rule>
    <rule>Do NOT drop the 2b or Cohort-0 computation -- they are still tracked daily; only their placement changes (headline -> audit field).</rule>
    <rule>Do NOT leave the §7 identities reconciling against the old partner_total headline -- that would false-fail every correct run. Update them consistently.</rule>
    <rule>Do NOT deploy outside the DS commit->S3 cycle (Rule 13). Do NOT rewrite historical partitions here -- that is .016.</rule>
  </do_not>
</task_order>
