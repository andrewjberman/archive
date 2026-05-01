<task_order>
  <metadata>
    <id>TRSB_PATHFIX.TO-2.dt-trade-users-ddb-reconcile</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DT_TradingOperations</issued_to>
    <date>2026-04-27</date>
    <status>complete</status><!-- AMENDED 2026-04-30 by 1.0.0_SA_CTO per Andrew directive: categorical full-send, no dual-write window. Trade ops have not yet officially started so there is no disruption from a clean cutover. -->
    <project_code>TRSB_PATHFIX</project_code>
    <wave>W2 — DDB reconciliation (categorical clean cutover; ships after W1 RAVC4)</wave>
    <prd_ref>docs/architecture/TRSB_PATHFIX_PRD.md §3 W2 + §11 appendix (2026-04-27); AMENDED 2026-04-30 per Andrew "full send, no disruption"</prd_ref>
    <effort>1 session</effort>
    <gates_on>TRSB_PATHFIX.TO-1 COMPLETE — do not start DDB rename until W1 path mismatch
    is closed and smoke-tested. Debug surface area is high enough already.</gates_on>
    <gates_for>None</gates_for>
    <tag>trade-pipeline-v1.8.0 (v1.7.0 was consumed by TFIMPT.W3 ship 2026-04-29)</tag>
  </metadata>

  <objective>
    Reconcile trade-users DDB to AJ's authoritative spec (2026-04-27). Current state has
    7 rows; spec needs 9. Schema uses legacy group label 'authorizers' while frontend type
    expects 'approvers'. Memberships for Austin/Adam/Yang/AJ/Andrew are all wrong. Lauren
    and Alyssa rows are missing entirely.

    AMENDED 2026-04-30 per Andrew directive: categorical clean cutover, NO dual-write
    window. Trade operations have not yet officially started, so there is no live workflow
    to protect during transition. One commit ships the spec end-to-end: DDB rows match
    target state on the 'approvers' label, Lambda code reads 'approvers' only. The legacy
    'authorizers' label is dropped from both DDB and code in the same commit.
  </objective>

  <compiler_tools_mandate>
    <phase_1_before_write>
      - aws dynamodb scan --table-name trade-users (capture pre-state; freeze snapshot to
        commit message or session log)
      - grep -rn 'authorizers\|approvers\|executors\|initiators'
        infra/aws/lambda/trade-pipeline/ (find every group-label consumer in Lambda code)
      - Read submission_handler.py + workflow_handler.py + dashboard_api.py group-label
        branch points (confirm whether they check 'groups' attribute or 'role' attribute)
      - aws ses list-identities --identity-type EmailAddress (cross-check all W2 spec
        members except alyssa are SES-verified; alyssa handled in TO-3)
    </phase_1_before_write>
    <phase_2_before_tag>
      - .tools/ds-precommit-check.py + py_compile + ruff on every .py file edited
      - aws dynamodb scan --table-name trade-users (post-migration; expect 9 rows matching
        spec table — verify 'approvers' present in groups for approver rows; 'authorizers'
        absent from ALL rows)
      - grep -rn 'authorizers' infra/aws/lambda/trade-pipeline/ (expect zero hits — clean
        cutover. Any residual reference in a comment must be called out explicitly.)
    </phase_2_before_tag>
    <phase_3_after_tag>
      - End-to-end submit: trade submit → SES delivery to 4 approvers visible in CloudWatch
        logs of trade-submission-handler; approve → SES to 9 executors visible.
        (Note: Alyssa SES still gated on TO-3 sandbox/verify; her absence is expected until W3)
      - Append to org/compiler-tools-log.md
    </phase_3_after_tag>
  </compiler_tools_mandate>

  <scope>
    TARGET STATE (per AJ spec 2026-04-27 + Andrew confirmation; categorical cutover 2026-04-30):

    | email                       | name      | role     | groups |
    |-----------------------------|-----------|----------|--------|
    | austin@opalinvest.com       | Austin    | approver | [approvers, executors] |
    | adam@opalinvest.com         | Adam      | approver | [approvers, executors] |
    | yang@opalinvest.com         | Yang      | approver | [approvers, executors] |
    | lauren@opalinvest.com       | Lauren    | approver | [approvers, executors] |
    | menachem@opalinvest.com     | Menachem  | executor | [executors] |
    | manav@opalinvest.com        | Manav     | executor | [executors] |
    | alyssa@opalinvest.com       | Alyssa    | user     | [executors] |
    | aj@opalinvest.com           | AJ        | user     | [executors] |
    | andrew@opalinvest.com       | Andrew    | dev      | [executors] |

    Notes:
    - 'authorizers' label is REMOVED FROM ALL ROWS in this commit. No dual-write — Andrew
      directive 2026-04-30: categorical full-send because trade ops have not started yet.
    - Andrew: groups=[executors] ONLY. Keep role=dev — it is a separate power-user field,
      do NOT touch it. Per Andrew 2026-04-27.
    - AJ: executor only per his own spec ("Executer: ...AJ..."). Current DDB 'authorizers'
      was drift. No authorizers/approvers group. Per Andrew 2026-04-27.
    - 'initiators' group is legacy — drop from all rows. Not part of AJ's two-group spec.
    - Menachem already correct (executor only). Update Manav's role 'user' → 'executor'.

    IMPLEMENTATION STEPS:
    1. Phase 1: grep all Lambda code for group-label consumers (submission_handler,
       workflow_handler, dashboard_api). EVERY code path that reads 'authorizers' is
       rewritten to read 'approvers' in the same commit. No dual-read shim.
    2. Write idempotent migration script (Python or boto3) that PUTs each row with
       correct email, name, role, groups, active=true. Test against a scratch table or
       a dry-run flag before applying to prod.
    3. Run migration. Scan post-state to verify 9-row spec match exactly.
    4. Commit Lambda code edits + migration script + session log under one tag.
    5. End-to-end smoke: submit → SES to 4 approvers visible in CW logs; approve → SES
       to 9 executors visible. Tag trade-pipeline-v1.8.0.

    NO follow-up obligation. The cutover is one commit, one tag, done.

    ds-commit-gate.sh REQUIRED before any .py commit (py_compile + AST + ruff).
    .tools/safe-commit.sh --author "..." -m "..." -- &lt;paths&gt; (mandatory; ADHC_OWNPTH.007).
    Author: 0.3.0_DT_TradingOperations &lt;0.3.0_DT_TradingOperations@opal.agent&gt;
  </scope>

  <acceptance_criteria>
    1. aws dynamodb scan --table-name trade-users shows exactly 9 rows matching the target
       state table above.
    2. 'approvers' present in groups for Austin/Adam/Yang/Lauren rows. AJ + Andrew groups
       contain only 'executors'. ZERO occurrences of 'authorizers' in any row's groups.
    3. Zero hits for 'initiators' in any row's groups attribute.
    4. Lambda code reads 'approvers' only — zero references to 'authorizers' in any active
       (non-comment, non-deleted) code path.
    5. ds-commit-gate.sh passes on all .py files touched.
    6. End-to-end CloudWatch evidence: submit → SES to 4 approvers visible (Austin, Adam,
       Yang, Lauren) → approve → SES to 9 executors visible. Same single submit/approve
       cycle confirms both legs of the cutover.
    7. trade-pipeline-v1.8.0 tag applied after clean CloudWatch evidence.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT start before TO-1 (W1) RAVC4 confirms path mismatch is closed.</rule>
    <rule>Do NOT keep 'authorizers' in DDB or Lambda code anywhere — categorical removal.
    Andrew directive 2026-04-30 supersedes the original dual-write window.</rule>
    <rule>Do NOT change Andrew's role field (keep role=dev — used by other tooling).</rule>
    <rule>Do NOT add 'authorizers' or 'approvers' to AJ or Andrew's groups — executor-only.</rule>
    <rule>Do NOT commit Python without ds-commit-gate.sh passing.</rule>
    <rule>Do NOT use git add -A or bare git commit — use .tools/safe-commit.sh with
    explicit pathspecs (ADHC_OWNPTH.007 mandatory).</rule>
  </do_not>

  <deliverables>
    <deliverable type="code">Migration script + Lambda 'authorizers' → 'approvers' rewrite</deliverable>
    <deliverable type="infrastructure">trade-users DDB: 9 rows matching target state, zero 'authorizers'</deliverable>
    <deliverable type="document">Session log with pre/post scan + CloudWatch email evidence</deliverable>
    <deliverable type="tag">trade-pipeline-v1.8.0</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO + 1.0.0_SA_CTO with: AC1-AC7 outputs
    + DDB scan + CloudWatch email traces</deliverable>
  </deliverables>
</task_order>
