<task_order>
  <metadata>
    <id>TRSB_LEDGER.012</id>
    <slug>dt-trsb-portal-prod-promotion</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform~B</issued_to>
    <date>2026-05-20</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>STAGED 2026-05-20 (COO~B, per CTO~B relay of Andrew's TRSB rulings). SCOPE WIDENED 2026-05-20: originally the HistoryTab fix only; TO-8b (role-aware gating) landed early, so per CTO~B this TO now promotes BOTH portal-side TRSB changes in one deploy and TRSB_LEDGER.013 is CANCELLED (folded here). FURTHER UPDATE 2026-05-20: Andrew's :5175 verify surfaced an EXECUTED/COMPLETE display-label issue -> TRSB_LEDGER.014 (RD relabel) authored + dispatched; its DEV commit is f9b2d81e -- RAVC2-accepted 2026-05-20. The cherry-pick list is now FINAL at 5 commits: bc5da3d2 + 43b36707 + 00841008 + be5d7631 + f9b2d81e. DT must NOT dispatch Phase 1 until Andrew has re-verified all 3 fixes on :5175 (DT git pull origin DEV first so the :5175 server carries f9b2d81e). LANE: base 0.3.0_DT_TradingOperations -- portal/PROD single-writer (TO-012 + SSCN TO-006 both push origin/PROD; one DT owns all portal/PROD pushes this session). Two-phase dispatch: Phase 0 (local-dev verification) -- the base DT already has a dev server UP on :5175 at portal DEV (b05388dc tree includes all 4 fix commits), so Andrew can verify immediately; no separate Phase-0 GO needed. Phase 1 (portal/PROD promotion) is HARD-GATED on Andrew's local-dev thumbs-up -- production deploy is Andrew's call. COO~B relays Andrew's explicit approval to trigger Phase 1.</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P1 -- promotes the two remaining portal-side TRSB fixes (the live HistoryTab visibility defect Andrew is hitting on opalinvest.dev + the TO-8b role-aware tab gating) from DEV to live opalinvest.dev. Both fixes are already built + on portal DEV; this TO is the PROD promotion.</priority>
    <sla>Phase 0: same-session on dispatch. Phase 1: same-session on Andrew's local-dev approval.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md (v0.1) -- section 2.A A4 (portal gates on firm, not role); section 3.5 + section 7 Q2 (COMPLETE retired, EXECUTED durable terminal).</prd>
    <diagnosis>CTO~B ground-truth 2026-05-20: (1) approved/executed trades absent from the TradeSubmission History tab -- stale COMPLETE|REJECTED filter predating the COMPLETE-retirement; (2) A4 -- the Execution/Approvals tabs gated on firm identity, not group membership. Both FE fixes architecturally complete; no backend hole.</diagnosis>
    <fix_commits>portal DEV, all in portal/src/pages/TradeSubmission/** (+ trade-submission.ts) -- disjoint from SSCN:
      - bc5da3d2 + 43b36707 + 00841008 -- HistoryTab.tsx visibility fix (3 contiguous commits, single file, +60/-17). DE 0.3.0, on origin/DEV.
      - be5d7631 -- TRSB_LEDGER.008b role-aware tab gating + completeSubmission removal (3 files: trade-submission.ts, TradeSubmission.tsx, useTradeSubmissionState.ts, +94/-56). RD 0.3.2, RAVC2-accepted by COO~B 2026-05-20.
      The HistoryTab commits touch only HistoryTab.tsx; be5d7631 touches the other 3 files -- disjoint, no cherry-pick interplay.</fix_commits>
    <ruling>Andrew 2026-05-20: PROD promotion AUTHORIZED, gated on a local-dev verification first. "Everything"-scope -- TO-8b is in for TRSB finalization.</ruling>
    <supersedes>TRSB_LEDGER.013 (the separate TO-8b PROD promotion) is CANCELLED -- folded into this TO per CTO~B 2026-05-20: one local-dev verify session + one cherry-pick set + one GHA deploy covers both, halving Andrew's verification rounds.</supersedes>
    <empirical_anchor>HistoryTab: TRADE-20260518-181840-2E31B0 (Lauren-initiated, approved+executed, DDB status=EXECUTED) must be visible in the History tab. Role-gating: a non-executor/non-approver internal user must NOT see the Execution/Approvals tabs.</empirical_anchor>
  </references>

  <objective>
    Promote both built-and-on-DEV portal-side TRSB fixes -- the HistoryTab visibility fix (3 commits) and the TO-8b role-aware tab gating (be5d7631) -- to portal/PROD in a single deploy so they reach live opalinvest.dev. Phase 0: Andrew verifies both behaviors on a local dev server off DEV. Phase 1: on his thumbs-up, cherry-pick all 4 commits onto portal/PROD, build-verify, push, GHA deploy; Andrew final-verifies both on the live URL.
  </objective>

  <context>
    opalinvest.dev deploys from portal/PROD (GHA deploy.yml -> S3 opalinvest-portal -> CloudFront EVTSA9VEHNZVH). There is no deployed DEV environment (portal/DEPLOY_HERE.md). Both fixes are on origin/DEV (b05388dc tip) but origin/PROD is at 4f8502e6, behind -- so Andrew, testing the live URL, is on PROD and still sees the old behavior.

    The 4 fix commits are all in portal/src/pages/TradeSubmission/** (+ src/api/endpoints/trade-submission.ts). Do NOT pull any other DEV commit -- the SSCN_DIVDEF Presets-dropdown work also on DEV is a separate project's PROD promotion (TO-006) and MUST NOT ride this push. The cherry-pick keeps the two PROD promotions disjoint.

    This TO touches only the portal submodule's PROD branch; it does NOT bump the parent CLOUD repo portal gitlink (out of scope).
  </context>

  <scope>
    <step>Phase 0 -- Stand up / confirm a local dev server on portal DEV. Notify COO~B when up so Andrew verifies BOTH the History tab and the role-gated tabs. NO production change in this phase.</step>
    <step>Phase 1 -- After COO~B relays Andrew's local-dev thumbs-up: cherry-pick all 4 commits onto portal/PROD, build-verify, push origin PROD, monitor the GHA deploy to completion.</step>
    <step>Phase 2 -- Andrew verifies both behaviors on live opalinvest.dev. RAVC2 to COO~B with evidence.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="local-dev verification (before any PROD change)">
      <step>
        <run>cd portal &amp;&amp; git checkout DEV &amp;&amp; git pull origin DEV &amp;&amp; /c/Users/AndrewBerman/.bun/bin/bun install &amp;&amp; /c/Users/AndrewBerman/.bun/bin/bun run dev --port 5175 (the server may already be up from the SSCN DEV smoke -- reuse it if so).</run>
        <expect>Dev server on http://localhost:5175 against portal DEV; all 4 fix commits (bc5da3d2/43b36707/00841008/be5d7631) present in DEV history.</expect>
        <if_mismatch>If the server fails or a commit is missing from DEV history, STOP -- MCP COO~B; do not proceed to Phase 1.</if_mismatch>
      </step>
      <step>
        <run>Notify COO~B the server is up; Andrew verifies on :5175 -- (a) TradeSubmission History tab shows TRADE-20260518-181840-2E31B0; (b) a non-executor/non-approver internal user does not see the Execution/Approvals tabs.</run>
        <expect>Andrew confirms BOTH: the anchor trade appears in History, and role-aware tab gating behaves correctly. COO~B relays his explicit thumbs-up.</expect>
        <if_mismatch>If either behavior is wrong on local dev, STOP -- do NOT promote to PROD; MCP COO~B + CTO~B.</if_mismatch>
      </step>
    </phase>
    <phase id="1" when="PROD promotion (gated on Andrew's Phase-0 thumbs-up)">
      <step>
        <run>cd portal &amp;&amp; git checkout PROD &amp;&amp; git pull origin PROD &amp;&amp; git cherry-pick bc5da3d2 43b36707 00841008 be5d7631 f9b2d81e</run>
        <expect>All 5 commits apply cleanly onto portal/PROD; every file changed is under portal/src/pages/TradeSubmission/** or src/api/endpoints/trade-submission.ts (the set: HistoryTab.tsx, TradeCard.tsx, TradeDetailsModal.tsx, TradeSubmission.tsx, useTradeSubmissionState.ts, utils/tradeStatus.ts, trade-submission.ts) -- git diff --stat origin/PROD..HEAD confirms NO file outside that scope.</expect>
        <if_mismatch>On a cherry-pick conflict: resolve preserving the intent in the commit messages. If the conflict is non-trivial, PROD's files have diverged structurally, or any file outside the 4 appears, abort (git cherry-pick --abort) and MCP COO~B.</if_mismatch>
      </step>
      <step>
        <run>/c/Users/AndrewBerman/.bun/bin/bun install &amp;&amp; /c/Users/AndrewBerman/.bun/bin/bun run build (or bunx tsc -b)</run>
        <expect>Zero TypeScript errors; production build exits 0 on portal/PROD post-cherry-pick.</expect>
        <if_mismatch>If the build fails, do NOT push -- diagnose; MCP COO~B + CTO~B.</if_mismatch>
      </step>
      <step>
        <run>git push origin PROD ; then monitor the GHA deploy.yml run to completion.</run>
        <expect>Push succeeds; the GHA deploy.yml run completes green; CloudFront EVTSA9VEHNZVH serves the new build.</expect>
        <if_mismatch>Non-fast-forward rejection -> re-pull origin PROD, re-evaluate; do not force-push. GHA failure -> capture the run log, MCP COO~B + CTO~B.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="post-deploy verification">
      <step>
        <run>Andrew verifies on live opalinvest.dev: (a) TradeSubmission History tab shows TRADE-20260518-181840-2E31B0; (b) a non-executor/non-approver does not see the Execution/Approvals tabs.</run>
        <expect>Both behaviors correct on the live site. Andrew confirms.</expect>
        <if_mismatch>If either is wrong on live after deploy completion, check CloudFront cache age / x-cache; if still wrong after cache settles, MCP COO~B + CTO~B.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <compiler_tools_note>
    comp-* does not model git cherry-pick / branch-promotion (same gap as ADHC_HALTGT §5). The mandate substitutes build-verification (bun build / tsc exit 0) + empirical anchor-reproduction (the History anchor trade visible + role-gating correct) for comp-graph runs.
  </compiler_tools_note>

  <data_reprocess_scope>
    <no_reprocess_needed>Portal-FE-only branch promotion of already-built fixes. No data, no Lambda, no S3 artifact, no script. No reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: portal/PROD branch ; portal/src/pages/TradeSubmission/** ; src/api/endpoints/trade-submission.ts
    also_in_to: SSCN_DIVDEF TO-006 is a separate portal/PROD promotion (Security Scanner scope). DISJOINT by design -- TO-012 cherry-picks ONLY the 4 named commits; it does NOT do a full DEV->PROD merge. TRSB_LEDGER.013 CANCELLED (folded here). If TO-006 and TO-012 land near-simultaneously, sequence with the SSCN DT lane / base COO via MCP so the two PROD pushes do not collide on origin/PROD.
    last_write_owner: 0.3.0_DT_TradingOperations owns all portal/PROD pushes this session.
    required_action: Cherry-pick the 4 named commits only (not a merge). Confirm the 4-file diff before pushing.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Phase 0: a local dev server runs on portal DEV; Andrew confirms (a) TRADE-20260518-181840-2E31B0 appears in the History tab and (b) role-aware tab gating behaves correctly, both on local dev. COO~B relays the explicit thumbs-up.</ac>
    <ac id="AC2">Phase 1: the 5 commits bc5da3d2 / 43b36707 / 00841008 / be5d7631 / f9b2d81e are cherry-picked onto portal/PROD; git diff --stat shows every changed file under portal/src/pages/TradeSubmission/** or src/api/endpoints/trade-submission.ts and no file outside that scope. No SSCN commit rode the push.</ac>
    <ac id="AC3">portal/PROD post-cherry-pick builds clean (bun run build / tsc exit 0); origin PROD is pushed; the GHA deploy.yml run completes green.</ac>
    <ac id="AC4">Phase 2: Andrew verifies on live opalinvest.dev that the History anchor trade appears AND role-aware tab gating behaves correctly.</ac>
    <ac id="AC5">No emoji. Session log with the Compiler Tools section (Phase 0/1/2 runs + observed results). RAVC2 to 2.0.0_SA_COO~B citing the PROD cherry-pick SHAs, the GHA run URL, and Andrew's live-verify confirmation. This RAVC2 covers BOTH the HistoryTab fix and the TO-8b promotion (TRSB_LEDGER.013 folded).</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="cherry-pick">portal :: HistoryTab.tsx + trade-submission.ts + TradeSubmission.tsx + useTradeSubmissionState.ts (via commits bc5da3d2, 43b36707, 00841008, be5d7631)</file>
  </scope_files>

  <deliverables>
    <deliverable type="local-dev">Phase 0 local dev server on :5175 off portal DEV, for Andrew's pre-promotion verification of both fixes.</deliverable>
    <deliverable type="commit">4 commits cherry-picked onto portal/PROD; origin PROD pushed; GHA deploy green.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section + Phase 0/1/2 evidence. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT execute Phase 1 (the PROD cherry-pick + push) until COO~B relays Andrew's explicit Phase-0 local-dev thumbs-up. Production deploy is Andrew-gated.</rule>
    <rule>Do NOT do a full DEV->PROD merge. Cherry-pick the 4 named commits only -- a merge would sweep the SSCN_DIVDEF Presets-dropdown work and other DEV commits into PROD uncontrolled.</rule>
    <rule>Do NOT force-push origin PROD. On a non-fast-forward rejection, re-pull and re-evaluate.</rule>
    <rule>Do NOT bump the parent CLOUD repo portal gitlink in this TO -- out of scope.</rule>
    <rule>Do NOT promote to PROD if the Phase-0 local-dev verification fails on either behavior -- escalate instead.</rule>
  </do_not>
</task_order>
