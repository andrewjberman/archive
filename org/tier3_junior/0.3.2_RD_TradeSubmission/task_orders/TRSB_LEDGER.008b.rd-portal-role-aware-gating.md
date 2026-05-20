<task_order>
  <metadata>
    <id>TRSB_LEDGER.008b</id>
    <slug>rd-portal-role-aware-gating</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.3.2_RD_TradeSubmission</issued_to>
    <date>2026-05-18</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED 2026-05-20 (COO~B). Gate cleared: TRSB_LEDGER.008 (/api/general/trades/users/me endpoint + {email,name,groups,role} contract) is COMPLETE per project JSON; CTO~B independently re-reviewed this TO 2026-05-20 -- dispatch-ready, no rework. GO fired to 0.3.2_RD_TradeSubmission on its session registration. Andrew "everything"-scope ruling 2026-05-20 keeps TO-8b IN for TRSB finalization. NOTE: this TO ends at the portal DEV commit; the PROD promotion of TO-8b's commits is a separate DT-lane TO (TRSB_LEDGER.013, authored post-completion).</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P2 -- Phase 3. Closes hole A4 (portal gates on firm, not role) + completes the Q2 COMPLETE-retirement on the FE side.</priority>
    <sla>1-2d wall.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md (v0.1) -- section 2.A A4 (portal gates on firm, not role); section 3.5 + section 7 Q2 (COMPLETE retired); section 6 TO-8.</prd>
    <gate>TRSB_LEDGER.008 -- the `/api/general/trades/users/me` endpoint and its response contract `{ email, name, groups, role }`.</gate>
    <ruling>Andrew 2026-05-18 Q2: COMPLETE is retired; EXECUTED is the durable terminal state. The orphaned `completeSubmission` FE function is removed in this TO.</ruling>
  </references>

  <objective>
    Gate the TradeSubmission portal page on actual trade-group membership instead of firm identity: the Execution tab + Execute button appear only for users in the `executors` group; the Approvals tab + approve/reject actions appear only for users in the `approvers` group. Also remove the orphaned `completeSubmission` FE function and FE `COMPLETE`-status references (the FE side of the Q2 COMPLETE retirement).
  </objective>

  <context>
    A4: `TradeSubmission.tsx` (lines ~28, ~107-112) shows the Approvals and Execution tabs to any user whose `claims.firmId === 'opal-capital'`. There is no executor/approver check -- every internal user sees the Execute button. Backend enforcement (TO-1) is the real gate and returns 403, but the FE should not present actions the user cannot take.

    The portal learns the caller's trade-groups from the TO-8 endpoint `/api/general/trades/users/me`, which returns `{ email, name, groups, role }`. This is a dedicated endpoint, NOT a JWT claim (CTO~B ruling) -- so the portal fetches it via React Query like any other data.

    Q2 FE cleanup: the backend (TO-4) retires `COMPLETE` and rests trades at `EXECUTED`. The FE has an orphaned `completeSubmission` function and may reference `COMPLETE` in status rendering. Remove the function; ensure status rendering treats `EXECUTED` as terminal. IMPORTANT: legacy rows with `status=COMPLETE` still exist in the table (TO-4 does not migrate them) -- the FE must render a legacy `COMPLETE` row without error (treat it as a terminal/closed state for display).

    Files: portal/src/pages/TradeSubmission/** (TradeSubmission.tsx, tabs/, hooks/, types.ts, services/), portal/src/api/endpoints/trade-submission.ts.
  </context>

  <scope>
    <step>Phase 1 -- Compiler study (below). Confirm the TO-8 endpoint contract from TO-8's RAVC2 deliverable before wiring.</step>
    <step>Phase 2 -- Add a React Query hook that fetches `/api/general/trades/users/me` and exposes the caller's `groups`. Add the endpoint to portal/src/api/endpoints/trade-submission.ts.</step>
    <step>Phase 2 -- Gate the tabs: the Execution tab + Execute button render only if `groups` includes `executors`; the Approvals tab + approve/reject controls render only if `groups` includes `approvers`. Replace the `claims.firmId === 'opal-capital'` gate for these privileged surfaces. (A non-privileged internal user still sees the page + their own submissions; they just do not see privileged tabs.)</step>
    <step>Phase 2 -- Remove the orphaned `completeSubmission` FE function and any call sites. Ensure status rendering treats `EXECUTED` as the terminal success state; a legacy `COMPLETE` row renders cleanly as a closed state (no crash, no undefined).</step>
    <step>Phase 3 -- /frontend-dev visual smoke: confirm the Execution tab is hidden for a non-executor internal user and visible for an executor.</step>
    <step>Phase 3 -- Commit to the portal DEV branch (RD owns the page; RD does not push). Coordinate the push + DEV verification with the Pod DT per the standard portal flow.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check TradeSubmission</run>
        <expect>0 MISSING fields. The trade-groups data (the `groups` list from the /users/me endpoint) is a NEW rendered input -- it will show as UNUSED or absent until wired; that is expected pre-write. NOTE entries are expected aliases.</expect>
        <if_mismatch>Any MISSING field unrelated to this TO = a pre-existing runtime-undefined bug -- flag to COO~B before proceeding, do not absorb it into this TO.</if_mismatch>
      </step>
      <step>
        <run>comp-cache collisions</run>
        <expect>The new React Query key for the trade-permissions / users-me fetch does NOT collide with an existing key. Zero collisions involving the new key.</expect>
        <if_mismatch>If the new key collides with an existing one, rename it before writing -- a key collision corrupts the cache (same key, different response types).</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>comp-transform schema-check TradeSubmission</run>
        <expect>0 MISSING fields; the `groups` data is now in the rendered set, no longer UNUSED.</expect>
        <if_mismatch>If `groups` is still UNUSED, the gating is not actually reading it -- the tab gate would silently fall to the wrong default. Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>bunx tsc -b (or bun run build)</run>
        <expect>Zero TypeScript errors -- including after the `completeSubmission` removal (no dangling call site, no broken import).</expect>
        <if_mismatch>Per-file tsc-clean is necessary but not sufficient -- ensure the whole TradeSubmission bundle compiles after the removal.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>/frontend-dev visual smoke on the TradeSubmission page</run>
        <expect>For a non-executor internal user: the Execution tab and Execute button are absent. For an executor: present. For a non-approver: the Approvals tab is absent. No console errors; a legacy COMPLETE row renders without crashing.</expect>
        <if_mismatch>If a non-executor still sees the Execute button, the gate is reading the wrong source or defaulting open -- do not mark complete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Portal-only change -- no data, no Lambda, no S3, no silver/bronze script. Consumes an existing backend endpoint (TO-8). No reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: portal/src/pages/TradeSubmission/** ; portal/src/api/endpoints/trade-submission.ts
    also_in_to: none active -- no other TRSB TO touches the portal. The COMPLETE retirement spans backend (TRSB_LEDGER.004) + this FE TO; the two must agree on EXECUTED-as-terminal.
    last_write_owner: 0.3.2_RD_TradeSubmission owns the page. DE 0.4 is available for React Query hook-wiring support if needed (PRD §6 names the RD 0.3.2 + DE 0.4 lane) -- coordinate via MCP if you pull DE in.
    required_action: Confirm the TO-8 endpoint contract from TO-8's RAVC2 before wiring. Push handled by the Pod DT, not RD.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The Execution tab + Execute button render only when the caller's `groups` (from /api/general/trades/users/me) includes `executors`; the Approvals tab + approve/reject controls render only when `groups` includes `approvers`. The firm-identity gate no longer governs these privileged surfaces.</ac>
    <ac id="AC2">A React Query hook fetches `/api/general/trades/users/me`; the new query key has zero collisions (comp-cache collisions).</ac>
    <ac id="AC3">The orphaned `completeSubmission` FE function and its call sites are removed. `EXECUTED` renders as the terminal success state; a legacy `COMPLETE` row renders cleanly without error.</ac>
    <ac id="AC4">comp-transform schema-check TradeSubmission: 0 MISSING fields, `groups` in the rendered set. bunx tsc -b: zero errors.</ac>
    <ac id="AC5">/frontend-dev visual smoke confirms the Execution tab is hidden for a non-executor and visible for an executor.</ac>
    <ac id="AC6">No emoji. Committed to the portal DEV branch; push coordinated with the Pod DT. Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="modify">portal/src/pages/TradeSubmission/TradeSubmission.tsx</file>
    <file action="modify">portal/src/pages/TradeSubmission/ (tabs/, hooks/, types.ts, services/ as needed)</file>
    <file action="modify">portal/src/api/endpoints/trade-submission.ts</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">Portal role-aware gating + completeSubmission removal, committed to the portal DEV branch.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section + the /frontend-dev visual smoke result. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do not gate the privileged tabs on firm identity -- the whole point of A4 is group-membership gating. The FE gate is UX; the backend (TO-1) remains the real enforcement.</rule>
    <rule>Do not let a legacy COMPLETE row crash the page -- TO-4 does not migrate historical rows; the FE must tolerate COMPLETE on read.</rule>
    <rule>Do not push the portal submodule yourself -- RD commits, the Pod DT pushes.</rule>
    <rule>Do not begin until TO-8's endpoint exists and its contract is confirmed -- this TO is gated on TO-8.</rule>
  </do_not>
</task_order>
