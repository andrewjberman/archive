<task_order>
  <metadata>
    <id>TRSB_LEDGER.014</id>
    <slug>rd-executed-complete-display-normalization</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.3.2_RD_TradeSubmission</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED 2026-05-20 (COO~B). Andrew hit the EXECUTED-vs-COMPLETE dual-label confusion during his :5175 verify; CTO~B explained (same terminal state -- COMPLETE is the retired legacy name, EXECUTED canonical post-Q2) and Andrew's call is to UNIFY the display label and FOLD IT INTO the in-flight portal PROD promotion. GO fired to 0.3.2_RD_TradeSubmission (live + idle, just closed TO-8b -- same agent, same page). NOTE: .013 was cancelled (folded into .012); this relabel takes a fresh number .014, not the .013 slot.</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P1 -- on the critical path: this commit becomes the 5th commit in TRSB_LEDGER.012's portal/PROD cherry-pick set, and Andrew's local-dev re-verify happens AFTER it lands on DEV. RD is idle; it is a small change.</priority>
    <sla>0.5d wall -- small, single-page display change.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md (v0.1) -- section 3.5 + section 7 Q2 (Andrew Q2: COMPLETE retired; EXECUTED is the durable terminal state).</prd>
    <ruling>Andrew 2026-05-20 (via CTO~B, from the :5175 verify session): legacy COMPLETE-status trades must display under the SAME user-facing label as EXECUTED. The unified label is "Executed" -- canonical: the data model, email_utils "Executed By", and `executed_at` all use it.</ruling>
    <context_to>TRSB_LEDGER.008b (be5d7631) already removed the orphaned completeSubmission function and kept COMPLETE in the TradeSubmissionStatus type for read-tolerance. This TO completes the FE side of the Q2 retirement: the legacy value stays in the type + DDB, but it never renders as a user-facing label.</context_to>
  </references>

  <objective>
    Display-normalize trade status on the TradeSubmission page: a legacy `COMPLETE`-status trade renders under the SAME user-facing label as `EXECUTED` ("Executed") at EVERY status render site on the page. The DynamoDB value is NOT changed -- this is pure display mapping; audit integrity is preserved (TO-4 deliberately did not migrate legacy rows, and this TO must not either).
  </objective>

  <context>
    Andrew, verifying on :5175, saw both "Executed" and "Complete" as distinct status labels and read them as two different states. They are the same terminal state -- COMPLETE is the retired pre-Q2 name; EXECUTED is canonical. Legacy rows keep `status=COMPLETE` in DynamoDB (not migrated, by design). The fix is a display-layer mapping, applied consistently.

    Mechanism -- a SINGLE shared display helper (e.g. `displayStatus(status)`) that maps `COMPLETE` to the `EXECUTED` label, applied at EVERY status render site on the TradeSubmission page: TradeCard, TradeDetailsModal, HistoryTab, the Execution tab -- not just HistoryTab. One helper, all sites; no raw `COMPLETE` string reaches a user-facing label.

    HistoryTab status filter: the dropdown currently has separate "Executed Only" and "Complete Only" options. Collapse them into ONE "Executed Only" option that matches BOTH `status==='EXECUTED'` AND `status==='COMPLETE'` rows. The `StatusFilter` type becomes `'all' | 'EXECUTED' | 'REJECTED'` (the `'COMPLETE'` member is removed from the filter type -- but `COMPLETE` stays in the `TradeSubmissionStatus` data type for read-tolerance).

    Files: portal/src/pages/TradeSubmission/** (status rendering across TradeCard, TradeDetailsModal, tabs/HistoryTab, the Execution tab; a shared helper location e.g. utils/ or services/).
  </context>

  <scope>
    <step>Phase 1 -- Compiler study (below). Enumerate every status render site on the TradeSubmission page (grep for the status field rendered as a label / badge).</step>
    <step>Phase 2 -- Add a single shared `displayStatus(status)` helper that maps `COMPLETE` -> the "Executed" label (and passes EXECUTED/REJECTED/etc. through). Apply it at EVERY status render site -- TradeCard, TradeDetailsModal, HistoryTab, Execution tab. No raw `COMPLETE` string renders as a user-facing label anywhere on the page.</step>
    <step>Phase 2 -- Collapse the HistoryTab status-filter dropdown: one "Executed Only" option matching both EXECUTED and COMPLETE rows; `StatusFilter` type -> `'all' | 'EXECUTED' | 'REJECTED'`.</step>
    <step>Phase 3 -- /frontend-dev visual smoke: a legacy COMPLETE trade shows the "Executed" label; the filter dropdown has one "Executed Only" option that returns both EXECUTED and COMPLETE rows.</step>
    <step>Phase 3 -- Commit to the portal DEV branch (RD owns the page; RD does not push). The commit joins TRSB_LEDGER.012's portal/PROD cherry-pick set -- report the commit SHA in the RAVC2.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check TradeSubmission</run>
        <expect>0 MISSING fields. No new rendered data field is introduced (display-only mapping of an existing `status` field) -- the schema set is unchanged. NOTE entries are expected aliases.</expect>
        <if_mismatch>Any MISSING field unrelated to this TO = a pre-existing runtime-undefined bug -- flag to COO~B, do not absorb it.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>comp-transform schema-check TradeSubmission</run>
        <expect>0 MISSING fields; no schema regression from the helper + filter-type change.</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>bunx tsc -b (or bun run build)</run>
        <expect>Zero TypeScript errors -- including after the `StatusFilter` type narrows to `'all' | 'EXECUTED' | 'REJECTED'` (no dangling reference to the removed `'COMPLETE'` filter member).</expect>
        <if_mismatch>Per-file tsc-clean is necessary but not sufficient -- ensure the whole TradeSubmission bundle compiles after the type change.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>/frontend-dev visual smoke on the TradeSubmission page (HistoryTab + a COMPLETE-status row).</run>
        <expect>A legacy COMPLETE trade renders the "Executed" label (not "Complete"). The HistoryTab status filter has one "Executed Only" option; selecting it returns both EXECUTED and COMPLETE rows. No console errors.</expect>
        <if_mismatch>If a COMPLETE row still shows "Complete", a render site was missed -- the helper is not applied everywhere. Do not mark complete; find the site and fix.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Portal-FE display-only change -- no data, no Lambda, no S3, no silver/bronze script, no DynamoDB write. Legacy COMPLETE rows are NOT migrated (audit integrity per TO-4). No reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: portal/src/pages/TradeSubmission/**
    also_in_to: TRSB_LEDGER.012 (DT) -- the portal/PROD promotion. This TO's DEV commit becomes the 5th commit in .012's cherry-pick set (bc5da3d2 + 43b36707 + 00841008 + be5d7631 + this). COO~B re-scopes .012's cherry-pick list + AC once this commit's SHA exists. Andrew's :5175 local-dev re-verify happens AFTER this lands on DEV (DT pulls origin/DEV first).
    last_write_owner: 0.3.2_RD_TradeSubmission owns the page. TO-8b (be5d7631) is already on DEV -- pull latest DEV before writing so you build on top of it.
    required_action: Land clean on portal DEV; report the commit SHA in the RAVC2 so COO~B can add it to TO-012's cherry-pick set.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">A single shared `displayStatus()` (or equivalently-named) helper maps `COMPLETE` to the "Executed" label and is applied at EVERY status render site on the TradeSubmission page (TradeCard, TradeDetailsModal, HistoryTab, Execution tab). Grep confirms no raw `COMPLETE` string renders as a user-facing label.</ac>
    <ac id="AC2">The HistoryTab status filter has ONE "Executed Only" option that matches both `status==='EXECUTED'` and `status==='COMPLETE'`; `StatusFilter` type is `'all' | 'EXECUTED' | 'REJECTED'`.</ac>
    <ac id="AC3">comp-transform schema-check TradeSubmission: 0 MISSING. bunx tsc -b: zero errors (no dangling `'COMPLETE'` filter-member reference).</ac>
    <ac id="AC4">/frontend-dev visual smoke: a legacy COMPLETE trade shows the "Executed" label; the "Executed Only" filter returns both EXECUTED and COMPLETE rows.</ac>
    <ac id="AC5">The DynamoDB `status` value is NOT changed for any row -- pure display mapping. `COMPLETE` remains in the `TradeSubmissionStatus` data type for read-tolerance.</ac>
    <ac id="AC6">No emoji. Committed to portal DEV (RD does not push). Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B citing the DEV commit SHA (for TO-012's cherry-pick set).</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="modify">portal/src/pages/TradeSubmission/ (status render sites: TradeCard, TradeDetailsModal, tabs/HistoryTab, Execution tab; shared helper)</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">displayStatus helper + all-site application + HistoryTab filter collapse, committed to portal DEV.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section + the /frontend-dev smoke result. RAVC2 to 2.0.0_SA_COO~B with the DEV commit SHA.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do not migrate or rewrite any DynamoDB `status` value -- this is display-only; legacy COMPLETE rows keep COMPLETE in the data (audit integrity, TO-4).</rule>
    <rule>Do not remove `COMPLETE` from the `TradeSubmissionStatus` data type -- it must stay for read-tolerance; only the `StatusFilter` type drops it.</rule>
    <rule>Do not apply the helper at only some render sites -- a missed site re-introduces the dual-label confusion. One helper, every site.</rule>
    <rule>Do not push the portal submodule -- RD commits, the Pod DT (TO-012) handles the PROD promotion.</rule>
  </do_not>
</task_order>
