<task_order>
  <metadata>
    <id>YALP_MDSRC.SEC1</id>
    <slug>ae-committed-plaintext-credential-remediation</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-21</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — dispatched immediately per CTO ruling 2026-05-21T13:xx Z. This is a STANDALONE security-remediation TO. It is NOT folded into the P3 fred-family cleanup TO and is NOT gated on F2/F5 or any implementation-chain milestone. It dispatches on its own clock. Phase 0 (AUDIT) is read-only AWS-state inspection — non-conflicting with the in-flight F2 apply; begin it the moment the F2 apply/tag/push mechanical sequence is clear of your hands (minutes away) or interleave it if you have a window. Rotation work (Phase 1+) is the substantive effort.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P0 — live-credential exposure in a public-history git object. Four plaintext secrets are committed in a tracked file. JWT_SECRET is the highest-severity item: a token-forgery surface across the entire auth fabric. This dispatches now, ahead of debt-paydown work.</priority>
    <sla>~1 effort-day for items 1-3 (audit + 4-key rotation + file fate). The JWT rotation needs a planned cutover (below) — that coordination, not raw effort, is the long pole.</sla>
  </metadata>

  <references>
    <finding>CTO session-29 escalation, empirically confirmed 2026-05-21. infra/aws/terraform/LAMBDA_SNAPSHOT_PRE_TERRAFORM_20260203_125339.json — committed in e671d9c21 — carries FOUR inline plaintext secrets, none of them Secrets Manager ARNs:
      - FRED_API_KEY     — plaintext
      - JWT_SECRET       — plaintext (HIGHEST severity — token-forgery across the auth fabric)
      - NEWS_API_SECRET  — value present
      - OPENAI_SECRET    — value present
    A second copy of the snapshot exists in the worktree at worktrees/comp-learns-_stub/.</finding>
    <cto_ruling>CTO MCP 2026-05-21: standalone security-remediation TO; do NOT fold into P3; do NOT gate on F5. Owner = infra-security AE lane; COO capacity call assigned it to 0.7.0_AE_CloudOps (CloudOps/IAM/security is your lane). Item 4 (git-history scrub) is a destructive op (history rewrite + force-push) — OUT of this TO's auto-scope, held for Andrew's explicit ruling; CTO is surfacing it to him this session.</cto_ruling>
    <standard>docs/architecture/THIRD_PARTY_DATA_INTEGRATION_STANDARD.md (RATIFIED, 73e4da697) — §3 step 2: third-party API keys live in Secrets Manager, never inline. FRED/NEWS/OPENAI keys all fall under this. The end state for all four keys is a Secrets Manager reference on every live consumer.</standard>
    <secrets_manager>opal/external-apis is the existing third-party-key secret (F4/F5 FRED key path). Confirm during AUDIT whether NEWS/OPENAI keys already have a Secrets Manager home or need one; JWT_SECRET is an auth-fabric secret, not a third-party key — likely a separate secret name.</secrets_manager>
  </references>

  <context>
    A pre-Terraform Lambda snapshot JSON was committed to the repo on 2026-02-03 with four live credentials inline as plaintext. The file is tracked and in public git history; a second copy sits in a worktree. The snapshot reflects deployed-Lambda env state as of that date — the plaintext values MAY still be the live credentials, or they may have drifted. The AUDIT phase establishes ground truth before any rotation.

    Two distinct exposure surfaces: (1) the credentials themselves are exposed and must be rotated; (2) the file keeps getting carried in commits and must stop being tracked. This TO closes both for items 1-3. The git-history scrub (removing the secret bytes from past commits) is item 4 — it is destructive and waits on Andrew.

    JWT_SECRET is special: rotating it invalidates every JWT signed with the old secret. A naive rotation logs out every live session. The rotation must be a PLANNED cutover (dual-secret validation window, or a low-traffic window with stakeholder awareness). Do not rotate JWT_SECRET without a cutover plan surfaced to COO first.
  </context>

  <scope>
    <in_scope>
      ITEM 1 — AUDIT (read-only; no AWS mutation):
      - For each of the 4 keys (FRED_API_KEY, JWT_SECRET, NEWS_API_SECRET, OPENAI_SECRET): determine the CURRENT deployed value/reference on every consuming Lambda — is the live env var a plaintext value or already a Secrets Manager reference?
      - Enumerate which Lambda functions consume each key (env var presence). Use the lambda-source-map.json + aws lambda get-function-configuration.
      - Compare each deployed value against the plaintext in the committed snapshot — flag any key whose committed plaintext == current live value (still-exposed) vs already-rotated.
      - Produce an audit table: key / consuming Lambdas / current form (plaintext|SM-ref) / committed-value-still-live (yes|no) / target Secrets Manager secret name.

      ITEM 2 — ROTATE:
      - Rotate all 4 credentials at the provider (FRED, NEWS API, OpenAI, and the JWT signing secret).
      - Move each to a Secrets Manager secret; update every live consuming Lambda's env to a Secrets Manager reference (not a plaintext value).
      - JWT_SECRET FIRST in severity but LAST in execution order until its cutover plan is signed off: surface a JWT rotation cutover plan to COO before executing it (dual-secret validation window OR planned low-traffic cutover). Do not invalidate live sessions without that sign-off.
      - FRED/NEWS/OPENAI rotations have no live-session blast radius — execute those without waiting.

      ITEM 3 — FILE FATE GOING FORWARD:
      - Add infra/aws/terraform/LAMBDA_SNAPSHOT_PRE_TERRAFORM_20260203_125339.json (and the worktrees/comp-learns-_stub/ copy path) to .gitignore.
      - Remove both copies from the working tree (git rm --cached + delete the file; this is a tracked-file removal, not a recursive delete — not destructive-op-gated).
      - This stops future commits of the file. It does NOT scrub history — that is item 4.
    </in_scope>
    <out_of_scope>
      ITEM 4 — GIT-HISTORY SCRUB. Removing the secret bytes from past commits requires a history rewrite + force-push — a destructive operation. NOT in this TO. CTO is surfacing it to Andrew; it executes only on Andrew's explicit ruling, as a separate follow-up. Rotating the credentials (item 2) is what neutralizes the exposure regardless of whether/when history is scrubbed — do not block items 1-3 on item 4.
      - Any change to F2/F5 FRED Lambda code or the implementation chain. SEC1 touches credential plumbing only.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="before any rotation — discovery">
      <step>
        <run>grep -rIl -e FRED_API_KEY -e JWT_SECRET -e NEWS_API_SECRET -e OPENAI_SECRET infra/aws/lambda/ infra/aws/terraform/</run>
        <expect>The committed snapshot JSON + the worktree copy appear. Any OTHER tracked file containing a plaintext value of one of the 4 keys is an additional finding — surface it to COO immediately, do not silently fold it in.</expect>
        <if_mismatch>If a plaintext key value is found in a file other than the two known snapshot copies, STOP and RAVC1 COO with the path — scope may need to widen before rotation.</if_mismatch>
      </step>
    </phase>
    <phase id="1" when="before writing the iam/terraform changes">
      <step>
        <run>comp-iam service {each consuming Lambda identified in ITEM 1}</run>
        <expect>For every Lambda that will switch a key to a Secrets Manager reference, secretsmanager:GetSecretValue on the target secret ARN is either already granted or flagged MISSING.</expect>
        <if_mismatch>Any MISSING secretsmanager:GetSecretValue grant must be added to iam.tf before the env switch is applied — otherwise the consumer hard-fails at runtime resolving the reference.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit / before apply">
      <step>
        <run>comp-iam gaps</run>
        <expect>Zero new permission gaps introduced by the iam.tf changes. Every consuming Lambda's boto3 secretsmanager:GetSecretValue call is covered.</expect>
        <if_mismatch>Close the gap in iam.tf and re-run before terraform apply.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after apply">
      <step>
        <run>aws lambda get-function-configuration for each consuming Lambda — inspect the env block</run>
        <expect>No plaintext key value remains in any consuming Lambda's env. Each of the 4 keys resolves via a Secrets Manager reference on every consumer.</expect>
        <if_mismatch>Any residual plaintext value means the rotation is incomplete — do not RAVC2; name the Lambda + key.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - FRED_API_KEY: F2 + F5 (the FRED Lambdas) are the primary consumers. F2 is mid-apply under this same agent; F5 dispatches on F2 0-diff. The FRED key rotation must not break the F2/F5 Lambdas — coordinate the FRED key swap so the new Secrets Manager value is live BEFORE or ATOMIC WITH the consumer env switch. Per the standard, opal/external-apis already holds the FRED key for F4/F5 — the rotation updates that secret's value + the consumers' references.
    - JWT_SECRET: the auth fabric (portal-auth pipeline / partners-api / any Lambda issuing or validating JWTs) is the blast radius. Coordinate the cutover plan with COO; if portal-auth Lambdas are in scope, that is a portal-auth-pipeline touch — flag it.
    - No silver/bronze script or S3-data-prefix changes — auto-rule 4 (data reprocess scope) is N/A; this is credential plumbing only.
  </cross_domain_coordination>

  <acceptance_criteria>
    - ITEM 1: an audit table committed (session log or a brief under docs/briefs/) — for each of the 4 keys: consuming Lambdas, current form (plaintext|SM-ref), whether the committed plaintext is still the live value, target Secrets Manager secret. Machine-checkable: 4 rows, every cell populated.
    - ITEM 2: all 4 credentials rotated at the provider. Phase-3 mandate run shows zero plaintext key values in any consuming Lambda env — every key resolves via a Secrets Manager reference. JWT_SECRET rotation executed only after a COO-signed cutover plan; the closeout cites the cutover window + that no unplanned mass session-invalidation occurred.
    - ITEM 3: both snapshot copies removed from the working tree and the path(s) in .gitignore; `git status` shows the files gone and `git check-ignore` confirms the path is ignored. Committed via .tools/safe-commit.sh.
    - Full deploy cycle for any Terraform/IAM change: code -> TF -> source map -> commit -> plan -> .tools/safe-apply.sh (HALTGT, Rule 18) -> 0-diff -> tag -> push --follow-tags -> record-terraform-deploy.
    - Session log includes the Compiler Tools section reproducing every Phase 0-3 <run> with observed result + pass/fail vs <expect>.
    - RAVC1 to COO + CTO when this TO is scoped/started; RAVC2 to COO + CTO on completion of items 1-3, explicitly stating item 4 (history scrub) remains open pending Andrew.
  </acceptance_criteria>
</task_order>
