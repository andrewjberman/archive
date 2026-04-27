<task_order>
  <metadata>
    <id>TRSB_PATHFIX.TO-2.dt-trade-users-ddb-reconcile</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DT_TradingOperations</issued_to>
    <date>2026-04-27</date>
    <status>staged</status>
    <project_code>TRSB_PATHFIX</project_code>
    <wave>W2 — DDB reconciliation (ships after W1 RAVC4)</wave>
    <prd_ref>docs/architecture/TRSB_PATHFIX_PRD.md §3 W2 + §11 appendix (2026-04-27)</prd_ref>
    <effort>1 session</effort>
    <gates_on>TRSB_PATHFIX.TO-1 COMPLETE — do not start DDB rename until W1 path mismatch
    is closed and smoke-tested. Debug surface area is high enough already.</gates_on>
    <gates_for>None (W3 can run in parallel after W1)</gates_for>
    <tag>trade-pipeline-v1.7.0</tag>
  </metadata>

  <objective>
    Reconcile trade-users DDB to AJ's authoritative spec (2026-04-27). Current state has
    7 rows; spec needs 9. Schema uses legacy group label 'authorizers' while frontend type
    expects 'approvers'. Memberships for Austin/Adam/Yang/AJ/Andrew are all wrong. Lauren
    and Alyssa rows are missing entirely.

    Per Andrew (2026-04-27): dual-write window = 1 calendar week. Write both 'authorizers'
    AND 'approvers' in groups for 1 week (keep both consumers happy), then drop the legacy
    label in a follow-up commit. Reason: 'authorizers' consumed by Lambda code (likely
    submission_handler.py / workflow_handler.py) — a wrong-day rename silently routes
    trades to nobody for approval.
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
        spec table — verify both 'approvers' AND 'authorizers' present in groups for
        dual-write window rows)
      - grep -rn 'authorizers' infra/aws/lambda/trade-pipeline/ (expect zero hits in new
        code, or called out if any legacy reference is in a deprecated comment)
    </phase_2_before_tag>
    <phase_3_after_tag>
      - End-to-end submit: trade submit → SES delivery to 4 approvers visible in CloudWatch
        logs of trade-submission-handler; approve → SES to 9 executors visible.
        (Note: Alyssa SES still gated on TO-3 sandbox/verify; her absence is expected until W3)
      - Append to org/compiler-tools-log.md
    </phase_3_after_tag>
  </compiler_tools_mandate>

  <scope>
    TARGET STATE (per AJ spec 2026-04-27 + Andrew confirmation):

    | email                       | name      | role     | groups (dual-write) |
    |-----------------------------|-----------|----------|---------------------|
    | austin@opalinvest.com       | Austin    | approver | [approvers, executors, authorizers] |
    | adam@opalinvest.com         | Adam      | approver | [approvers, executors, authorizers] |
    | yang@opalinvest.com         | Yang      | approver | [approvers, executors, authorizers] |
    | lauren@opalinvest.com       | Lauren    | approver | [approvers, executors, authorizers] |
    | menachem@opalinvest.com     | Menachem  | executor | [executors] |
    | manav@opalinvest.com        | Manav     | user     | [executors] |
    | alyssa@opalinvest.com       | Alyssa    | user     | [executors] |
    | aj@opalinvest.com           | AJ        | user     | [executors] |
    | andrew@opalinvest.com       | Andrew    | dev      | [executors] |

    Notes:
    - 'authorizers' kept alongside 'approvers' during 1-week dual-write window ONLY for
      the approver-group rows (Austin/Adam/Yang/Lauren). Drop it in a follow-up commit after
      1 week of clean production traffic.
    - Andrew: groups=[executors] ONLY. Keep role=dev — it is a separate power-user field,
      do NOT touch it. Per Andrew 2026-04-27.
    - AJ: executor only per his own spec ("Executer: ...AJ..."). Current DDB 'authorizers'
      was drift. No authorizers/approvers group. Per Andrew 2026-04-27.
    - 'initiators' group is legacy — drop from all rows. Not part of AJ's two-group spec.
    - Menachem + Manav: already correct state (executor only). Update Manav's role to
      executor (currently 'user') for consistency. Leave Menachem unchanged.

    IMPLEMENTATION STEPS:
    1. Phase 1: grep all Lambda code for group-label consumers (submission_handler,
       workflow_handler, dashboard_api). If any code reads 'authorizers', patch to read
       BOTH 'authorizers' OR 'approvers' (dual-read) for the 1-week window.
    2. Write idempotent migration script (Python or boto3) that PUTs each row with
       correct email, name, role, groups, active=true. Test before applying.
    3. Run migration. Scan post-state to verify.
    4. After 1 calendar week of clean prod traffic (~2026-05-04): ship a follow-up tiny
       commit dropping 'authorizers' from groups and dropping the dual-read from Lambda
       code. Tag: trade-pipeline-v1.7.1.

    ds-commit-gate.sh REQUIRED before any .py commit (py_compile + AST + ruff).
    git commit --only -- &lt;paths&gt; (never git add -A or bare git commit).
    Author: 0.3.0_DT_TradingOperations &lt;0.3.0_DT_TradingOperations@opal.agent&gt;
  </scope>

  <acceptance_criteria>
    1. aws dynamodb scan --table-name trade-users shows exactly 9 rows matching the target
       state table above.
    2. 'authorizers' present alongside 'approvers' in groups for Austin/Adam/Yang/Lauren
       rows (dual-write window). AJ + Andrew groups contain only 'executors'.
    3. Zero hits for 'initiators' in any row's groups attribute.
    4. Lambda code reads BOTH 'authorizers' OR 'approvers' for authorization (dual-read
       for 1-week window). No code reads ONLY 'authorizers' exclusively.
    5. ds-commit-gate.sh passes on all .py files touched.
    6. End-to-end CloudWatch evidence: submit → SES to approvers log visible (4 approver
       emails) → approve → SES to executors log visible.
    7. trade-pipeline-v1.7.0 tag applied after clean CloudWatch evidence.
  </acceptance_criteria>

  <follow_up_obligation>
    After 7 days (~2026-05-04): drop 'authorizers' from groups for Austin/Adam/Yang/Lauren
    and drop dual-read from Lambda code. Tiny commit. Tag: trade-pipeline-v1.7.1.
    Andrew to confirm clean traffic before DT executes the drop.
  </follow_up_obligation>

  <do_not>
    <rule>Do NOT start before TO-1 (W1) RAVC4 confirms path mismatch is closed.</rule>
    <rule>Do NOT drop 'authorizers' in this commit — dual-write only. Drop in follow-up
    after 1 week.</rule>
    <rule>Do NOT change Andrew's role field (keep role=dev — used by other tooling).</rule>
    <rule>Do NOT add 'authorizers' to AJ or Andrew's groups — executor-only for both.</rule>
    <rule>Do NOT commit Python without ds-commit-gate.sh passing.</rule>
    <rule>Do NOT use git add -A or bare git commit — use --only with explicit pathspecs.</rule>
  </do_not>

  <deliverables>
    <deliverable type="code">Migration script + Lambda dual-read patch (if needed)</deliverable>
    <deliverable type="infrastructure">trade-users DDB: 9 rows matching target state</deliverable>
    <deliverable type="document">Session log with pre/post scan + CloudWatch email evidence</deliverable>
    <deliverable type="tag">trade-pipeline-v1.7.0</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO + 1.0.0_SA_CTO with: AC1-AC6 outputs
    + DDB scan + CloudWatch email traces</deliverable>
  </deliverables>
</task_order>
