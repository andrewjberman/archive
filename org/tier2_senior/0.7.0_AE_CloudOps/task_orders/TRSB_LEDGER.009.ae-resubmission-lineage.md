<task_order>
  <metadata>
    <id>TRSB_LEDGER.009</id>
    <slug>ae-resubmission-lineage</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-18</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED 2026-05-20 (COO~B). Gate cleared: Phases 1+2 (TO-0 through TO-6) ALL shipped + RAVC-accepted (TRSB_LEDGER is 11/12 complete). Andrew "everything"-scope ruling 2026-05-20 keeps TO-9 IN -- the stretch is NOT dropped. GO fired to 0.7.0_AE_CloudOps on its session registration. NOTE: TO-9 ends at the trade-submission-handler deploy (terraform apply, AE-lane) -- no portal change, no PROD-promotion follow-on needed.</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P3 -- stretch. Closes hole B6 (no resubmission lineage). Recommended but droppable.</priority>
    <sla>1d wall -- if dispatched at all.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md (v0.1) -- section 2.B B6; section 4 (scoped as a stretch TO, droppable if Phase 1+2 runs long); section 6 TO-9.</prd>
  </references>

  <objective>
    Make a corrected resubmission of a rejected trade traceable to its predecessor. Today a rejected trade is terminal and a corrected resubmission receives a fresh `submission_id` with no link back -- "this trade is revision 3 of TRADE-X" cannot be reconstructed (B6).
  </objective>

  <context>
    A rejected trade is terminal; the workflow has no resubmission concept. When a user re-enters a corrected trade, it is a brand-new submission with a new `submission_id` and no `parent_submission_id` / `supersedes` link.

    Target: a resubmission carries a `parent_submission_id` (and/or `supersedes`) attribute pointing at the rejected predecessor, so the lineage of a trade across rejection + correction is reconstructable.

    This is a STRETCH TO. It is dispatched only if the Phase 1+2 backend lane (TO-0..TO-6) completes with capacity. It is the lowest-priority item and is explicitly droppable per PRD §4 -- do not let it delay or compete with the Pillar A / Pillar B work.

    File: trade-submission-handler/src/submission_handler.py (+ possibly the portal resubmit affordance, scoped minimally -- a backend-accepted optional field is the v1 floor; a FE resubmit-from-rejected button is a follow-on, not this TO).
  </context>

  <scope>
    <step>Phase 1 -- Direct read submission_handler.py row-creation path. Confirm where `submission_id` is minted and how a new submission item is shaped.</step>
    <step>Phase 2 -- Accept an optional `parent_submission_id` on the submission request; when present, write it (and a `supersedes` marker) onto the new row. The new row is a normal submission in every other respect. If the predecessor exists, optionally annotate the predecessor's `audit_events` with a `SUPERSEDED_BY` note (consistent with the TO-3 append-only pattern -- list_append, no rewrite).</step>
    <step>Phase 3 -- Deploy via terraform apply (CLAUDE.md Rules 1-6). Empirical: resubmit a rejected trade with parent_submission_id set; assert the lineage link resolves.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Direct read: submission_handler.py row-creation + submission_id minting</run>
        <expect>The new-row shape is identifiable; `parent_submission_id` is a new optional top-level attribute, no Terraform schema change. comp-* tools N/A (uninstrumented, PRD §5).</expect>
        <if_mismatch>If the row-creation path is materially different from PRD §2.B, adjust the lineage write accordingly.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>Empirical: submit a trade with `parent_submission_id` pointing at a known rejected trade</run>
        <expect>The new row carries `parent_submission_id` / `supersedes`; the lineage link resolves to the predecessor. If the predecessor annotation was implemented, the predecessor's audit_events shows the SUPERSEDED_BY note.</expect>
        <if_mismatch>If the link does not resolve, do not mark complete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>New optional attribute on future submissions only -- no historical backfill (past resubmissions cannot be retroactively linked and are not in scope). No silver/bronze script, no reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py
    also_in_to: TRSB_LEDGER.003 (submission_handler.py -- audit_events SUBMITTED event)
    last_write_owner: 0.7.0_AE_CloudOps owns the AE backend serial lane. TO-9 runs after TO-3 (and after all of TO-0..TO-6). Pull latest before writing.
    required_action: TO-9 is last in-lane; no cross-agent contention.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The submission path accepts an optional `parent_submission_id`; when present it is written (with a `supersedes` marker) onto the new row.</ac>
    <ac id="AC2">Empirical: a resubmission with `parent_submission_id` set resolves to its predecessor.</ac>
    <ac id="AC3">Deployed via terraform apply (0-diff plan); pipeline tag applied.</ac>
    <ac id="AC4">No emoji. Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="modify">infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">submission_handler.py resubmission-lineage attribute, deployed via terraform apply (0-diff plan), pipeline tag applied.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do not let this stretch TO compete with or delay Pillar A / Pillar B work -- if Phase 1+2 overruns, this TO is dropped.</rule>
    <rule>Do not attempt to retroactively link historical resubmissions -- forward-only.</rule>
    <rule>Do not build a FE resubmit-from-rejected affordance here -- v1 floor is the backend-accepted optional field; the FE button is a separate follow-on.</rule>
    <rule>Do not deploy outside Terraform (CLAUDE.md Rule 1).</rule>
  </do_not>
</task_order>
