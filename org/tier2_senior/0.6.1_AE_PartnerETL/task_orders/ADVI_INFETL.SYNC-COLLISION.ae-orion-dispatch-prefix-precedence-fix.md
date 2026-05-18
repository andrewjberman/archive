<task_order>
  <metadata>
    <id>ADVI_INFETL.SYNC-COLLISION</id>
    <slug>ae-orion-dispatch-prefix-precedence-fix</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <date>2026-05-18</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED GO 2026-05-18. No external gate. ONE cross-domain sequencing requirement: orion-gold-dispatch.sh is concurrently edited by AE 0.7.0 (ADVI_INFETL.RUNDATE-DISPATCH-IMPL) -- see cross_domain_coordination; MCP 0.7.0 before committing to that file.</dispatch_unblock_condition>
    <project_code>ADVI_INFETL</project_code>
    <priority>P1 -- a systemic deploy-sync correctness defect. The orion-gold-dispatch.sh sync silently runs stale code for every script that exists in 2+ S3 code/ prefixes. Confirmed to have silently disabled the INFINC.006 Pattern E migration; the blast radius (pull_inflection_assets_v2.py, pull_inflection_positions_daily.py) is UNVERIFIED and may include live data-correctness defects -- Phase 0 resolves that.</priority>
    <sla>Phase 0 census FAST (~1-2h -- it determines whether a live data defect exists). Phases 1-4 ~3-5h wall depending on Phase 0 findings + the 0.7.0 coordination window.</sla>
  </metadata>

  <references>
    <defect_report>0.6.1_AE_PartnerETL INFINC.006 chain-validation 2026-05-18 (session log session_advi_infinc006_chain_validation.md). VERDICT: the INFINC.006 Pattern E TXN migration has NEVER executed in any chain run. chain_full_20260517_140109 completed but INF_API_PULL_TXN ran PRE-INFINC.006 code (no `mode=` line; log strings match commit 5c1ea192d~1, not the deployed 5c1ea192d).</defect_report>
    <root_cause>orion-gold-dispatch.sh sync_scripts() (lines ~283-304) bulk-downloads 4 S3 prefixes into ONE flat dir keyed by basename, last-write-wins, prefix order ['code/gold/','code/manual_api/','code/silver/','code/bronze/']. pull_inflection_transactions_rest.py exists in 3 of them; code/bronze/ is downloaded LAST so its stale 2026-04-30 copy (15,792 b) clobbers the INFINC.006 code/manual_api/ copy (21,835 b, 2026-05-15). DS~D deployed correctly per the INFINC.006 Phase-4 spec (code/manual_api/); the sync silently clobbers it on every chain run.</root_cause>
    <blast_radius>Systemic -- every script present in 2+ code/ prefixes. 0.6.1 flagged pull_inflection_assets_v2.py + pull_inflection_positions_daily.py as likely-stale (bronze copy wins, differs from manual_api); pull_inflection_performance_rest.py collides but all copies byte-identical (harmless).</blast_radius>
    <no_regression_so_far>For transactions specifically: NO data regression -- the pre-INFINC.006 code is a daily full per-account inception-to-date pull (correctness-safe; no incremental-window gap). silver/transactions/2026-05-17 = 1,300,879 rows / 48 cols, 88.33% enriched, coherent vs the TXNAMG.003 amalgamated writer. What was LOST is the AC5 optimization (~7min/day -> &lt;1min) + the incremental+weekly-backstop design not being in force. assets_v2 + positions_daily are NOT yet verified -- Phase 0 must.</no_regression_so_far>
    <lane>orion-gold-dispatch.sh is the 0.6.1 ADVI_INFLEC.W4.11 lane. Fix routed to 0.6.1 per the lane + the fresh defect context.</lane>
    <ec2_standard>docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md -- S3 artifact model; write locally -> upload to S3 -> EC2 pulls. orion-gold-dispatch.sh is EC2-side (Amazon Linux) -- exempt from CLAUDE.md Rule 16.</ec2_standard>
  </references>

  <context>
    The Inflection gold chain runs on the inf-gold-runner EC2 via orion-gold-dispatch.sh. Its sync_scripts() stage pulls script code from four S3 prefixes (code/gold/, code/manual_api/, code/silver/, code/bronze/) into one flat working directory keyed by basename. When the same basename exists in multiple prefixes, the LAST-downloaded prefix wins -- silently. The prefix order puts code/bronze/ last, so a stale bronze-prefix copy of any multi-homed script overrides a fresh deploy to any other prefix.

    This is a structural deploy-correctness defect: an agent can deploy correct code to the documented prefix, verify the S3 object's sha256, and STILL have the chain run a different (stale) version -- with no error, no warning. It already silently disabled INFINC.006. It must be made structurally impossible to clobber silently.

    This TO does both halves: (1) immediate remediation so the chain runs correct code now, and (2) the structural sync_scripts() fix so silent clobbering cannot recur. Plus a Phase-0 census that determines whether the blast radius includes a LIVE data-correctness defect (assets_v2 / positions_daily) that needs separate escalation.
  </context>

  <scope>
    <phase id="0" name="empirical census + live-defect determination">
      - `aws s3 ls` all four code/ prefixes; enumerate EVERY basename present in 2+ prefixes.
      - For each multi-homed basename: pull every copy, diff them, identify which prefix the chain currently runs (last in sync order) vs which is the intended/current copy.
      - SPECIFICALLY for pull_inflection_assets_v2.py + pull_inflection_positions_daily.py: determine whether the clobbering (chain-executed) copy is stale-but-CORRECT (behaviour-equivalent, only an optimization/cosmetic delta) or stale-and-WRONG (produces materially different bronze/silver data). This is the live-data-defect question.
      - DETERMINE for each multi-homing: is it intentional architecture (different prefixes intentionally serve different chain stages) or accidental cruft (a script that should live in exactly one prefix). If any multi-homing turns out intentional-architectural, surface to COO before the Phase-2 design -- precedence ordering then matters and is a design call.
      - DELIVERABLE: a census table. If any script is found stale-and-WRONG and live, ESCALATE TO COO IMMEDIATELY (do not bundle it into the Phase 1-4 timeline) -- a live data defect gets its own fast track.
    </phase>
    <phase id="1" name="immediate remediation">
      - For every multi-homed script whose chain-executed copy is NOT the intended/current one: re-deploy the intended copy OVER the losing-prefix basename(s) on S3, so the chain runs correct code regardless of sync order. NO S3 OBJECT DELETION -- re-deploy/overwrite only (no deletion authorization needed).
      - Verify: after re-deploy, the basename resolves to the intended content at every prefix it appears in (sha256 parity across copies).
    </phase>
    <phase id="2" name="structural sync_scripts() fix">
      - Fix sync_scripts() so a basename collision can NEVER silently run the wrong code. Required behaviour: FAIL-LOUD on an unexpected basename collision (the sync aborts/errors with the colliding basename + the conflicting prefixes named) -- a silent last-write-wins is banned. If Phase 0 found genuinely-intentional multi-homing, add an EXPLICIT declared precedence map for those specific basenames (highest-precedence prefix wins, lower-precedence copies skipped) so the intentional cases pass while any NEW/undeclared collision still fails loud.
      - Bare prefix reordering is REJECTED (0.6.1's note) -- it is fragile; a future dual-homed script silently breaks again. The fix must be collision-detecting, not order-dependent.
    </phase>
    <phase id="3" name="verification">
      - Demonstrate via a chain run (SSM-direct or the next cron fire) that INF_API_PULL_TXN now executes the INFINC.006 Pattern E code -- the `mode=` line + the INFINC.006 log signatures present (the inverse of the defect-report evidence).
      - Confirm sync_scripts() fails loud (or applies declared precedence) on a basename collision -- a synthetic colliding-basename test.
    </phase>
    <phase id="4" name="commit + deploy">
      - Commit per CLAUDE.md (safe-commit.sh, agent author). Deploy orion-gold-dispatch.sh per the EC2 code deployment standard (S3 artifact model). Tag/push per the EC2 deployment protocol.
      - Update org/projects/ADVI_INFETL.json phase + the EC2-side deployment record if applicable.
    </phase>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-blast orion-gold-dispatch</run>
        <expect>The dispatcher's chain-step / consumer graph, OR a "not modeled" result. orion-gold-dispatch.sh is a shell dispatcher, not a gold pipeline node -- if comp reports no nodes, that is expected; record it and proceed (the blast radius is established empirically by the Phase-0 S3 census instead).</expect>
        <if_mismatch>If comp DOES model it and shows consumers beyond the INF gold chain, widen the Phase-3 verification to those consumers.</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls s3://opal-data-inf/code/gold/ ; aws s3 ls s3://opal-data-inf/code/manual_api/ ; aws s3 ls s3://opal-data-inf/code/silver/ ; aws s3 ls s3://opal-data-inf/code/bronze/</run>
        <expect>The full basename inventory of all four prefixes -- the empirical basis for the Phase-0 multi-homed-basename census.</expect>
        <if_mismatch>If a prefix is missing or empty, reconcile against the dispatcher's sync_scripts() prefix list before proceeding -- the defect model may be incomplete.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-iam service inf-gold-runner (or the dispatcher's EC2 role) IF any new boto3/aws-cli S3 op was added</run>
        <expect>No new IAM gap. If Phase 1/2 only re-deploys existing-pattern S3 objects + edits shell logic with no new AWS API surface, this is N/A -- state so in one line.</expect>
        <if_mismatch>Fix iam.tf before deploy; run comp-iam gaps.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <conditional>
      Transactions: NO reprocess needed -- 0.6.1 verified the pre-INFINC.006 TXN code is correctness-safe (full inception-to-date pull); historical silver/transactions is semantically correct. The fix only restores the optimization + incremental design for FUTURE runs.
      assets_v2 / positions_daily: CONTINGENT on Phase 0. If Phase 0 finds the chain-executed (clobbering) copy is stale-and-WRONG and has been writing materially different bronze/silver data, a reprocess scope IS required -- 0.6.1 adds an explicit Phase-3 re-ingestion block (affected S3 prefix globs + mtime verification + downstream consumer freshness gate) and surfaces it to COO. If Phase 0 finds them stale-but-correct, no reprocess -- state the reasoning.
    </conditional>
  </data_reprocess_scope>

  <cross_domain_coordination>
    orion-gold-dispatch.sh is CONCURRENTLY edited by AE 0.7.0 under ADVI_INFETL.RUNDATE-DISPATCH-IMPL (E1: step_is_date_capable() predicate + DATE-CAPABILITY CONTRACT catalog comment; E2: validate_rundate_coherence guard). Your sync_scripts() fix is a different function in the SAME FILE. MANDATORY: MCP 0.7.0 before you commit to orion-gold-dispatch.sh. Sequencing: 0.7.0's RUNDATE-DISPATCH-IMPL guard-first deploy is near-term -- the clean order is 0.7.0's E1/E2 lands first, then you rebase the sync_scripts() fix on top of their committed orion-gold-dispatch.sh and deploy. Confirm the actual order with 0.7.0 directly; do NOT both edit-and-deploy the file in an uncoordinated window. If 0.7.0's deploy slips and blocks you &gt;1 wake cycle, surface to COO.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Phase 0 census delivered: every basename present in 2+ code/ prefixes is enumerated with a copy-diff and the identification of which copy the chain currently runs. pull_inflection_assets_v2.py + pull_inflection_positions_daily.py are EXPLICITLY classified stale-but-correct or stale-and-wrong with evidence.</ac>
    <ac id="AC2">If Phase 0 found any script running stale-and-WRONG code with a live data impact, it was escalated to COO immediately on discovery -- not deferred to TO completion.</ac>
    <ac id="AC3">Immediate remediation: every multi-homed script resolves to the intended/current content at every prefix the chain syncs (sha256 parity verified). No S3 object was deleted.</ac>
    <ac id="AC4">sync_scripts() structurally fixed: a basename collision FAILS LOUD (sync errors, naming the basename + conflicting prefixes) -- silent last-write-wins is eliminated. A synthetic colliding-basename test demonstrates the fail-loud (or the declared-precedence skip for any Phase-0-confirmed intentional multi-homing). Bare prefix reordering was NOT the fix.</ac>
    <ac id="AC5">A chain run (SSM-direct or cron fire) demonstrably executes the INFINC.006 Pattern E TXN code -- the `mode=` line + the INFINC.006 log signatures present in the chain log (inverse of the defect-report evidence).</ac>
    <ac id="AC6">The orion-gold-dispatch.sh cross-domain coordination with AE 0.7.0 was honored -- MCP exchanged before commit; RUNDATE-DISPATCH-IMPL's E1/E2 changes are intact in the deployed file (not clobbered).</ac>
    <ac id="AC7">No emoji in code/logs. Deployed per the EC2 code deployment standard (S3 artifact model). Session log includes the Compiler Tools section reproducing the mandate runs.</ac>
  </acceptance_criteria>

  <deliverables>
    - Phase 0 census table (in the session log or a docs/briefs/ note).
    - Fixed orion-gold-dispatch.sh deployed to the inf-gold-runner per the EC2 standard.
    - Re-deployed correct copies of the affected multi-homed scripts on S3.
    - Session log under org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-05-18/ with the Compiler Tools section.
    - RAVC2 to COO with: the census, the commit SHA, the AC5 chain-log evidence, the AC4 synthetic-collision test output, and the 0.7.0 coordination record.
  </deliverables>
</task_order>
