<task_order>
  <metadata>
    <id>TRSB_LEDGER.013</id>
    <slug>dt-role-aware-gating-prod-promotion</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.3.0_DT_TradingOperations</issued_to>
    <date>2026-05-20</date>
    <status>cancelled</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>CANCELLED 2026-05-20 (COO~B, per CTO~B 2026-05-20) -- FOLDED INTO TRSB_LEDGER.012. TO-8b landed early, so be5d7631 (the commit this TO would have promoted) is now part of TRSB_LEDGER.012's widened 4-commit cherry-pick set: one local-dev verify session + one cherry-pick + one GHA deploy promotes both the HistoryTab fix and the role-aware gating, halving Andrew's verification rounds. This TO file is retained cancelled for the record; do NOT dispatch it. --- ORIGINAL: STAGED 2026-05-20 (COO~B). PROD promotion of TRSB_LEDGER.008b's portal commit. LANE: base 0.3.0_DT_TradingOperations -- same portal/PROD single-writer rationale as TRSB_LEDGER.012 (one DT owns every portal/PROD push this session to avoid a non-fast-forward race). GATED on: (1) TRSB_LEDGER.008b fully closed -- RD 0.3.2's closeout commit landed + TO RAVC-accepted; (2) Andrew's PROD-promotion authorization (production deploy is Andrew's call). COO~B flips to pending + fires GO when both gates clear.</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P2 -- promotes the TO-8b role-aware-gating fix from DEV to live opalinvest.dev. Separable from the TO-012 history-fix promotion; rides its own DT-lane push.</priority>
    <sla>Same-session on both gates clearing.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md (v0.1) -- section 2.A A4 (portal gates on firm, not role); section 7 Q2 (COMPLETE retired).</prd>
    <gate>TRSB_LEDGER.008b -- RAVC2-accepted by COO~B 2026-05-20; portal DEV commit be5d7631.</gate>
    <fix_commit>portal DEV: be5d7631 -- "TradeSubmission -- role-aware tab gating (TRSB_LEDGER.008b / A4 fix) + remove orphaned completeSubmission". 3 files: src/api/endpoints/trade-submission.ts, src/pages/TradeSubmission/TradeSubmission.tsx, src/pages/TradeSubmission/hooks/useTradeSubmissionState.ts (+94/-56).</fix_commit>
    <ruling>Andrew 2026-05-20 "everything"-scope: TO-8b is in scope for TRSB finalization. Production deploy authorization is a separate Andrew call (this TO's Phase-1 gate).</ruling>
    <sibling>TRSB_LEDGER.012 -- the HistoryTab-fix PROD promotion. Same DT, same portal/PROD branch; disjoint files (TO-012 = HistoryTab.tsx; this TO = TradeSubmission.tsx + 2 others). The two cherry-picks do not conflict; sequence them on the single DT lane.</sibling>
  </references>

  <objective>
    Promote the TRSB_LEDGER.008b role-aware tab-gating fix (commit be5d7631, already on portal DEV) to portal/PROD so it reaches live opalinvest.dev. Cherry-pick the single commit onto portal/PROD, build-verify, push, and let the GHA deploy carry it; Andrew final-verifies the gating behavior on the live URL.
  </objective>

  <context>
    Same deploy topology as TRSB_LEDGER.012: opalinvest.dev deploys from portal/PROD (GHA deploy.yml -> S3 opalinvest-portal -> CloudFront EVTSA9VEHNZVH). TO-8b's fix is on origin/DEV (be5d7631) but not on PROD. be5d7631 is a single commit touching 3 files, none of them HistoryTab.tsx -- so it is disjoint from TO-012's cherry-pick and the two do not conflict regardless of which lands first.

    RD 0.3.2 already ran a route-mocked Playwright visual smoke on DEV covering 4 group states + legacy-COMPLETE (all PASS) -- the gating behavior is DEV-verified. Phase 0 local-dev verification is therefore OPTIONAL (offered for Andrew if he wants to eyeball it); the hard gate is Andrew's PROD-promotion authorization.

    This TO touches only the portal submodule's PROD branch -- it does NOT bump the parent CLOUD repo portal gitlink (out of scope, same as TO-012).
  </context>

  <compiler_tools_mandate>
    <phase id="0" when="optional local-dev verification">
      <step>
        <run>If Andrew wants a pre-promotion eyeball: the dev server on :5175 (portal DEV) already includes be5d7631 -- Andrew opens TradeSubmission and confirms a non-executor/non-approver does not see the Execution/Approvals tabs.</run>
        <expect>Tab gating behaves per AC1 of TO-8b. Optional -- TO-8b's Playwright smoke already DEV-verified this; skip if Andrew is satisfied with that.</expect>
        <if_mismatch>If the gating misbehaves on local dev, STOP -- do not promote; MCP COO~B + CTO~B.</if_mismatch>
      </step>
    </phase>
    <phase id="1" when="PROD promotion (gated on Andrew authorization)">
      <step>
        <run>cd portal &amp;&amp; git checkout PROD &amp;&amp; git pull origin PROD &amp;&amp; git cherry-pick be5d7631</run>
        <expect>be5d7631 applies cleanly onto portal/PROD; the diff shows exactly the 3 TO-8b files (trade-submission.ts, TradeSubmission.tsx, useTradeSubmissionState.ts) and nothing else.</expect>
        <if_mismatch>On a cherry-pick conflict: resolve preserving the role-aware-gating intent (the be5d7631 commit message + the TO-8b spec). If the conflict is non-trivial or any file outside the 3 appears, abort (git cherry-pick --abort) and MCP COO~B.</if_mismatch>
      </step>
      <step>
        <run>/c/Users/AndrewBerman/.bun/bin/bun install &amp;&amp; /c/Users/AndrewBerman/.bun/bin/bun run build (or bunx tsc -b)</run>
        <expect>Zero TypeScript errors; production build exits 0 on portal/PROD post-cherry-pick.</expect>
        <if_mismatch>If the build fails, do NOT push -- diagnose; MCP COO~B + CTO~B.</if_mismatch>
      </step>
      <step>
        <run>git push origin PROD ; then monitor the GHA deploy.yml run to completion.</run>
        <expect>Push succeeds; GHA deploy.yml completes green; CloudFront EVTSA9VEHNZVH serves the new build.</expect>
        <if_mismatch>Non-fast-forward rejection -> re-pull origin PROD, re-evaluate; do not force-push. GHA failure -> capture the run log, MCP COO~B + CTO~B.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="post-deploy verification">
      <step>
        <run>Andrew verifies on live opalinvest.dev: a non-executor/non-approver user does not see the Execution/Approvals tabs; the firm-identity gate is gone.</run>
        <expect>Role-aware gating behaves correctly on the live site.</expect>
        <if_mismatch>If gating misbehaves on live after deploy, check CloudFront cache age/x-cache; if still wrong after cache settles, MCP COO~B + CTO~B.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <compiler_tools_note>
    comp-* does not model git cherry-pick / branch-promotion (same gap as TRSB_LEDGER.012 / ADHC_HALTGT §5). The mandate substitutes build-verification (bun build / tsc exit 0) + behavioral verification (the tab-gating check) for comp-graph runs.
  </compiler_tools_note>

  <data_reprocess_scope>
    <no_reprocess_needed>Portal-FE-only branch promotion of an already-built fix. No data, no Lambda, no S3 artifact, no script. No reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: portal/PROD branch
    also_in_to: TRSB_LEDGER.012 (HistoryTab-fix PROD promotion) + SSCN_DIVDEF TO-006 (Security Scanner PROD promotion) also push origin/PROD. All three are base-DT-owned -> single-writer, serialize them. be5d7631's 3 files are disjoint from TO-012's HistoryTab.tsx -- no cherry-pick conflict between .012 and .013.
    last_write_owner: 0.3.0_DT_TradingOperations owns all portal/PROD pushes this session.
    required_action: Cherry-pick the single commit be5d7631 only (not a merge). Confirm the 3-file diff before pushing. Sequence after/before TO-012 on the DT lane as convenient -- order does not matter (disjoint files).
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">be5d7631 is cherry-picked onto portal/PROD; the diff shows exactly the 3 TO-8b files and no others.</ac>
    <ac id="AC2">portal/PROD post-cherry-pick builds clean (bun run build / tsc exit 0); origin PROD is pushed; the GHA deploy.yml run completes green.</ac>
    <ac id="AC3">Andrew verifies on live opalinvest.dev that role-aware tab gating behaves correctly (non-privileged user does not see Execution/Approvals tabs).</ac>
    <ac id="AC4">No emoji. Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B citing the PROD cherry-pick SHA, the GHA run URL, and Andrew's live-verify confirmation.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="cherry-pick">portal :: src/api/endpoints/trade-submission.ts, src/pages/TradeSubmission/TradeSubmission.tsx, src/pages/TradeSubmission/hooks/useTradeSubmissionState.ts (via commit be5d7631)</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">be5d7631 cherry-picked onto portal/PROD; origin PROD pushed; GHA deploy green.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT execute Phase 1 until COO~B confirms (1) TRSB_LEDGER.008b is fully closed and (2) Andrew has authorized the PROD promotion.</rule>
    <rule>Do NOT do a full DEV-&gt;PROD merge -- cherry-pick be5d7631 only.</rule>
    <rule>Do NOT force-push origin PROD.</rule>
    <rule>Do NOT bump the parent CLOUD repo portal gitlink -- out of scope.</rule>
  </do_not>
</task_order>
