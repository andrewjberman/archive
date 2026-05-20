<task_order>
  <metadata>
    <id>TRSB_LEDGER.012</id>
    <slug>dt-historytab-prod-promotion</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.3.0_DT_TradingOperations</issued_to>
    <date>2026-05-20</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>STAGED 2026-05-20 (COO~B, per CTO~B relay of Andrew's TRSB rulings). LANE: routed to BASE 0.3.0_DT_TradingOperations (not a DT~B) per CTO~B architecture call 2026-05-20 -- portal/PROD single-writer safety: TO-012 and SSCN TO-006 both push origin/PROD, so one DT must own all portal/PROD pushes this session to avoid a non-fast-forward race; base DT already owns TO-006. COO~B surfaced this to Andrew as a recommendation (confirm/override). Two-phase dispatch: Phase 0 (local-dev verification) -- the base DT already has a dev server UP on :5175 at portal DEV b05388dc (stood up for the SSCN DEV smoke; b05388dc's tree includes the 3 HistoryTab fix commits), so Andrew can verify the TradeSubmission History tab on localhost:5175 immediately; no separate Phase-0 GO needed. Phase 1 (portal/PROD promotion) is HARD-GATED on Andrew's local-dev thumbs-up -- production deploy is Andrew's call. COO~B relays Andrew's explicit local-dev approval to trigger Phase 1.</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P1 -- finalizes the live HistoryTab visibility defect Andrew is actively hitting on opalinvest.dev. The fix is already built and on portal DEV; this TO is purely the PROD promotion.</priority>
    <sla>Phase 0: same-session on DT~B registration. Phase 1: same-session on Andrew's local-dev approval.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md (v0.1) -- section 3.5 + section 7 Q2 (COMPLETE retired; EXECUTED is the durable terminal state).</prd>
    <diagnosis>CTO~B ground-truth 2026-05-20: approved/executed trades absent from the TradeSubmission History tab. Root cause = a stale COMPLETE|REJECTED History filter that predated the COMPLETE-retirement (Andrew Q2 ruling). FE fix is architecturally complete; no backend hole -- trade-dashboard-api /submissions/by-status already accepts EXECUTED.</diagnosis>
    <fix_commits>portal DEV: bc5da3d2, 43b36707, 00841008 -- 3 contiguous commits, single file src/pages/TradeSubmission/tabs/HistoryTab.tsx (+60/-17). Authored by 0.3.0_DE_TradingOperations 2026-05-19; on origin/DEV (synced 2026-05-20).</fix_commits>
    <ruling>Andrew 2026-05-20 (via CTO~B): PROD promotion AUTHORIZED, gated on a local-dev verification first.</ruling>
    <empirical_anchor>TRADE-20260518-181840-2E31B0 -- Lauren-initiated, approved + executed by Andrew, DDB status=EXECUTED, brokerage_email_sent=true. Invisible in the History tab pre-fix; MUST be visible post-fix. This is the pass/fail anchor for both Phase 0 and Phase 2.</empirical_anchor>
  </references>

  <objective>
    Promote the HistoryTab.tsx visibility fix (3 commits, already on portal DEV) to portal/PROD so it reaches the live opalinvest.dev environment. Phase 0: stand up a local dev server off portal DEV so Andrew verifies the fix before any production change. Phase 1: on his thumbs-up, cherry-pick the 3 commits onto portal/PROD, build-verify, push, and let the GHA deploy carry them to opalinvest.dev for Andrew's final verification.
  </objective>

  <context>
    opalinvest.dev deploys from portal/PROD (GHA deploy.yml -> S3 opalinvest-portal -> CloudFront EVTSA9VEHNZVH). There is no deployed DEV environment -- a DEV push is CI-only (portal/DEPLOY_HERE.md). The fix is on origin/DEV (tip b05388dc) but origin/PROD is at 4f8502e6, behind -- so Andrew, testing the live URL, is on PROD and still sees the bug.

    The 3 fix commits are contiguous and touch exactly one file (src/pages/TradeSubmission/tabs/HistoryTab.tsx). Scope is strictly History-tab visibility:
      - bc5da3d2 surfaces EXECUTED trades alongside COMPLETE+REJECTED (the limbo-state fix).
      - 43b36707 unions My-Submissions across initiator + approver + executor involvement.
      - 00841008 makes the USER view degrade gracefully when an augmentation query fails.

    Do NOT pull any other DEV commit. portal DEV also carries SSCN_DIVDEF work (Presets dropdown, b05388dc etc.) -- that is a different project's PROD promotion (handled separately under SSCN_DIVDEF TO-006) and MUST NOT ride this push. The cherry-pick keeps the two PROD promotions disjoint.

    This TO touches only the portal submodule's PROD branch. It does NOT bump the parent CLOUD repo portal gitlink (the parent gitlink tracks the DEV-cycle and is maintained separately; the opalinvest.dev deploy path is GHA-from-portal/PROD and is independent of the parent gitlink).
  </context>

  <scope>
    <step>Phase 0 -- Stand up a local dev server on portal DEV. Notify COO~B when it is up so Andrew can verify the History tab. NO production change in this phase.</step>
    <step>Phase 1 -- After COO~B relays Andrew's local-dev thumbs-up: cherry-pick the 3 commits onto portal/PROD, build-verify, push origin PROD, monitor the GHA deploy to completion.</step>
    <step>Phase 2 -- Andrew verifies on the live opalinvest.dev URL. RAVC2 to COO~B with evidence.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="local-dev verification (before any PROD change)">
      <step>
        <run>cd portal &amp;&amp; git checkout DEV &amp;&amp; git pull origin DEV &amp;&amp; /c/Users/AndrewBerman/.bun/bin/bun install &amp;&amp; /c/Users/AndrewBerman/.bun/bin/bun run dev --port 5175</run>
        <expect>Dev server starts on http://localhost:5175 against portal DEV (tip b05388dc or the current origin/DEV head). No build/start error. The 3 fix commits (bc5da3d2/43b36707/00841008) are in the checked-out DEV history (git log --oneline | grep HistoryTab confirms).</expect>
        <if_mismatch>If the server fails to start or the 3 commits are not in DEV history, STOP -- do not proceed to Phase 1. MCP COO~B with the failure.</if_mismatch>
      </step>
      <step>
        <run>Notify COO~B the server is up; Andrew opens TradeSubmission -> History tab and checks for TRADE-20260518-181840-2E31B0 and other approved/executed trades.</run>
        <expect>Andrew confirms the anchor trade (and approved/executed trades generally) now appear in the History tab. COO~B relays his explicit thumbs-up.</expect>
        <if_mismatch>If the anchor trade is STILL absent on local dev, the DEV fix is incomplete -- STOP, do NOT promote to PROD, MCP COO~B + CTO~B immediately. Promoting an incomplete fix to PROD is the failure mode this Phase-0 gate exists to prevent.</if_mismatch>
      </step>
    </phase>
    <phase id="1" when="PROD promotion (gated on Andrew's Phase-0 thumbs-up)">
      <step>
        <run>cd portal &amp;&amp; git checkout PROD &amp;&amp; git pull origin PROD &amp;&amp; git cherry-pick bc5da3d2 43b36707 00841008</run>
        <expect>All 3 commits apply cleanly onto portal/PROD; the only file changed is src/pages/TradeSubmission/tabs/HistoryTab.tsx (git diff --stat origin/PROD..HEAD confirms 1 file).</expect>
        <if_mismatch>On a cherry-pick conflict: resolve preserving the fix intent described in the 3 commit messages (EXECUTED surfaced; My-Submissions union; graceful USER-view degradation). If the conflict is non-trivial or PROD's HistoryTab.tsx has diverged structurally, abort the cherry-pick (git cherry-pick --abort) and MCP COO~B before proceeding. If any file other than HistoryTab.tsx shows in the diff, abort -- scope contamination.</if_mismatch>
      </step>
      <step>
        <run>/c/Users/AndrewBerman/.bun/bin/bun install &amp;&amp; /c/Users/AndrewBerman/.bun/bin/bun run build (or bunx tsc -b)</run>
        <expect>Zero TypeScript errors; production build exits 0 on portal/PROD post-cherry-pick.</expect>
        <if_mismatch>If the build fails, do NOT push. Diagnose -- a clean cherry-pick that fails to build means PROD lacks a dependency the fix relies on. MCP COO~B + CTO~B.</if_mismatch>
      </step>
      <step>
        <run>git push origin PROD</run>
        <expect>Push succeeds; the GHA deploy.yml workflow triggers on the PROD push.</expect>
        <if_mismatch>If the push is rejected (non-fast-forward), re-pull origin PROD and re-evaluate -- do not force-push.</if_mismatch>
      </step>
      <step>
        <run>Monitor the GHA deploy.yml run to completion (gh run list / gh run watch).</run>
        <expect>The deploy workflow completes green: bundle uploaded to S3 opalinvest-portal, CloudFront EVTSA9VEHNZVH serving the new build.</expect>
        <if_mismatch>If the GHA deploy fails, capture the run log, MCP COO~B + CTO~B. Do not retry blindly.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="post-deploy verification">
      <step>
        <run>Andrew verifies on the live opalinvest.dev URL: TradeSubmission -> History tab shows TRADE-20260518-181840-2E31B0.</run>
        <expect>The anchor trade is visible in the History tab on the live site. Andrew confirms.</expect>
        <if_mismatch>If the anchor trade is absent on live after deploy completion, check CloudFront cache age / x-cache; a stale edge cache can mask a correct deploy. If still absent after cache settles, MCP COO~B + CTO~B.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <compiler_tools_note>
    The compiler toolchain models the data/portal/Lambda dependency graph; it does not model git cherry-pick / branch-promotion operations -- the entire surface of this TO. comp-* returns nothing relevant here (same documented gap as ADHC_HALTGT section 5 / ADHC_VALGATE section 5.2). The structured mandate above substitutes build-verification (bun build / tsc exit 0) and empirical anchor-reproduction (TRADE-20260518-181840-2E31B0 visible) for comp-graph runs.
  </compiler_tools_note>

  <data_reprocess_scope>
    <no_reprocess_needed>Portal-FE-only change -- no data, no Lambda, no S3 data artifact, no silver/bronze script. A branch promotion of an already-built FE fix. No reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: portal/PROD branch ; src/pages/TradeSubmission/tabs/HistoryTab.tsx
    also_in_to: SSCN_DIVDEF TO-006 is a separate portal/PROD promotion (Security Scanner scope). The two are DISJOINT by design -- TO-012 cherry-picks ONLY the 3 HistoryTab commits; it does NOT do a full DEV-&gt;PROD merge. Do not let the SSCN Presets-dropdown / scanner work ride this push. If TO-006 and TO-012 land near-simultaneously, sequence with the SSCN DT lane / base COO via MCP so the two PROD pushes do not collide on origin/PROD.
    last_write_owner: 0.3.0_DT_TradingOperations~B owns this PROD promotion. The fix commits are DE 0.3.0's work, already on DEV.
    required_action: Cherry-pick (not merge). Confirm single-file diff before pushing. Coordinate with the SSCN DT lane if TO-006 is in flight on origin/PROD concurrently.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Phase 0: a local dev server runs on portal DEV; Andrew confirms TRADE-20260518-181840-2E31B0 and approved/executed trades appear in the TradeSubmission History tab on local dev. COO~B relays the explicit thumbs-up.</ac>
    <ac id="AC2">Phase 1: the 3 commits bc5da3d2 / 43b36707 / 00841008 are cherry-picked onto portal/PROD; git diff --stat origin/PROD-pre..PROD-post shows exactly one file changed (src/pages/TradeSubmission/tabs/HistoryTab.tsx). No other commit rode the push.</ac>
    <ac id="AC3">portal/PROD post-cherry-pick builds clean (bun run build / tsc exit 0); origin PROD is pushed; the GHA deploy.yml run completes green.</ac>
    <ac id="AC4">Phase 2: Andrew verifies on the live opalinvest.dev URL that TRADE-20260518-181840-2E31B0 appears in the History tab.</ac>
    <ac id="AC5">No emoji in any commit message / log. Session log with the Compiler Tools section (the Phase 0/1/2 run table + observed results). RAVC2 to 2.0.0_SA_COO~B citing the cherry-pick SHAs on PROD, the GHA run URL, and Andrew's live-verify confirmation.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="cherry-pick">portal :: src/pages/TradeSubmission/tabs/HistoryTab.tsx (via commits bc5da3d2, 43b36707, 00841008)</file>
  </scope_files>

  <deliverables>
    <deliverable type="local-dev">Phase 0 local dev server on :5175 off portal DEV, for Andrew's pre-promotion verification.</deliverable>
    <deliverable type="commit">3 commits cherry-picked onto portal/PROD; origin PROD pushed; GHA deploy green.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section + Phase 0/1/2 evidence. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT execute Phase 1 (the PROD cherry-pick + push) until COO~B relays Andrew's explicit Phase-0 local-dev thumbs-up. Production deploy is Andrew-gated.</rule>
    <rule>Do NOT do a full DEV-&gt;PROD merge. Cherry-pick the 3 named commits only -- a merge would sweep the SSCN_DIVDEF Presets-dropdown work and other DEV commits into PROD uncontrolled.</rule>
    <rule>Do NOT force-push origin PROD. On a non-fast-forward rejection, re-pull and re-evaluate.</rule>
    <rule>Do NOT bump the parent CLOUD repo portal gitlink in this TO -- out of scope.</rule>
    <rule>Do NOT promote to PROD if the Phase-0 local-dev verification fails -- escalate instead.</rule>
  </do_not>
</task_order>
