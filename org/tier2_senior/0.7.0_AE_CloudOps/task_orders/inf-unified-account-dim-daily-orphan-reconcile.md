<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC-INF-UAD-ORPHAN</id>
    <title>inf-unified-account-dim-daily Lambda — un-attributed S3 zip reconciliation + provenance audit + recurrence prevention</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-13</issued_date>
    <status>complete</status><!-- 2026-05-13: AE 0.7 AC1-6 PASS; Phase 2 follow-up TO authored at task_orders/record-terraform-deploy-content-commit-fix.md -->
    <accepted_at>2026-05-13T15:02:44Z</accepted_at>
    <accepted_by>0.7.0_AE_CloudOps</accepted_by>
    <completed_at>2026-05-13T19:00:00Z</completed_at>
    <ship_commits>51b74564c (AE 0.7 backfill), 743323ff6 (AE 0.6.1 v1.7.54 upload), 2071a8ace (AE 0.6.1 manual restore)</ship_commits>
    <ship_tag>inf-pipeline-v1.7.54</ship_tag>
    <session_log>org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-05-13/session_inf_uad_daily_orphan_reconcile.md</session_log>
    <followup_to>org/tier2_senior/0.7.0_AE_CloudOps/task_orders/record-terraform-deploy-content-commit-fix.md (ADHC-RECORD-TF-DEPLOY-CONTENT-COMMIT)</followup_to>
    <priority>HIGH — gates the next inf-pipeline Lambda apply that includes inf-unified-account-dim-daily in scope. Author session expects empirical RAVC2 within current session window (AE 0.6.1 v1.7.53 deploy session lineage; orphan compounded across two consecutive deploys).</priority>
    <estimated_effort>~0.5-1d (diagnostic + binary-diff + git-log search + CloudTrail pull + source-map reconciliation + optional terraform apply)</estimated_effort>
    <dual_owner>0.4.0_DT_ClientPlatform (CI/build-and-upload.sh hygiene; consultation only — primary lane is 0.7.0_AE_CloudOps for infra/aws/lambda/inf-pipeline/**)</dual_owner>
  </metadata>

  <references>
    <ref type="incident_lineage_v1_7_52">org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-05-12/session_chain_22_and_lambda_v1.7.52.md §"Orphan drift incident" — AE 0.6.1 surfaced at 22:38Z: terraform plan showed source_code_hash diff for inf-unified-account-dim-daily attributable to un-tracked S3 upload at 16:47:00Z 2026-05-12. COO ruled Option C scoped -target apply on advisor-publisher only; orphan reconciliation deferred to today's TO.</ref>
    <ref type="incident_lineage_v1_7_53">org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-05-13/ (in-flight) — AE 0.6.1 v1.7.53 deploy session 2026-05-13 AM: orphan COMPOUNDED. Pre-v1.7.52 hash → post-v1.7.52 hash → today's plan delta hash:
      - 2026-05-07 original (legit): artifact_sha256 sourced from commit lineage (12316 B zip)
      - State post-v1.7.52 Lambda live: `8eWiL153rp9E2+OOLvwtYiNZa2iSiW9gfo+3QxX0AqY=` (per AE 0.6.1 RAVC2 report)
      - Source map AFTER today's build-and-upload (commit `dba29da4e` 14:24:50Z 2026-05-13): `vUH5XGTYcEWs/3fmzuv5sgFwq1UjeFy/209rQl2JpDo=` (per current `infra/aws/lambda/ci/lambda-source-map.json`)
      - Lambda CURRENT live `aws lambda get-function-configuration` 2026-05-13 ~14:30Z: `8eWiL153rp9E2+OOLvwtYiNZa2iSiW9gfo+3QxX0AqY=` (live STILL on 2026-05-07 build)
      
      **State divergence:** Source map expected ≠ Lambda live ≠ original 2026-05-07 known-good. Three states for one Lambda. Next un-scoped `terraform apply` would push source map's `vUH5XGTYcEWs...` content (orphan-sourced) onto Lambda live, replacing 2026-05-07 known-good with provenance-unknown zip.</ref>
    <ref type="s3_evidence">S3 `opal-313476888478-lambda-artifacts` versions of `inf-pipeline/inf-unified-account-dim-daily.zip`:
      | LastModified UTC | VersionId | Size | ETag |
      |---|---|---|---|
      | 2026-05-12T16:47:00Z | ANTWEyecNCzcZRqapgz.5Zt_tfLzHGKq | 12296 | "38dd0bbb61258405fcf462907173e868" |
      | 2026-05-12T15:49:47Z | mq72nTyNiXIiU6yEvDeRiOhGJAjZcS_8 | 12296 | "38dd0bbb61258405fcf462907173e868" |
      | 2026-05-07T20:51:10Z | Q_bfywbFIe5reQ1k8oC65QoncETJZvfa | 12316 | "7ff21b6b0837627e5fd2bf900ba23e54" |
      
      Two 2026-05-12 versions: IDENTICAL content (same ETag + size), uploaded ~58 minutes apart. Indicates a process that re-uploaded the same content twice — possibly a CI retry or a duplicate uploader. Pre-2026-05-12 history shows ONE upload on 2026-05-07 (the legitimate build).</ref>
    <ref type="rule_violated">CLAUDE.md Rule 1: "Terraform is the only Lambda deployment mechanism. Never use `aws lambda update-function-code`, `deploy.sh`, or the AWS console to deploy code." Rule 4: "Every Lambda must have an entry in `infra/aws/lambda/ci/lambda-source-map.json`. CI drift detection depends on this."</ref>
    <ref type="source_map">infra/aws/lambda/ci/lambda-source-map.json — entry `functions["inf-unified-account-dim-daily"]` current state: artifact_sha256=`vUH5XGTYcEWs...`, last_deployed_commit=`dba29da4e92f90c0664c9788c4b9b16cdd6fdf98` (AE 0.6.1's v1.7.53 source-map sweep), last_deployed_at=2026-05-13T14:24:50Z, source_dir=`infra/aws/lambda/inf-pipeline/inf-unified-account-dim-daily`, files=[lambda_function.py, pull_unified_account_dim.py, jwt_freshness.py]</ref>
  </references>

  <context>
    `inf-unified-account-dim-daily` is one of 7 daily-dim Lambdas in the inf-pipeline (per
    ADVI_INFETL LAMBDA-DIMS Phase A+B). It writes silver-complete sentinels at
    `silver/_silver_complete/{date}/unified_account_dim.json` which feed into
    `inf-silver-aggregator` quorum gate.

    Last legitimate, attributed deploy: 2026-05-07T20:51:10Z (commit lineage traceable via prior
    source map ledger).

    Two un-attributed S3 zip uploads occurred 2026-05-12 (15:49Z + 16:47Z, identical content).
    Neither corresponds to a commit in the source map's `last_deployed_commit` history at that
    time. AE 0.6.1's plan today reflects this orphan content as the "expected" state because
    `build-and-upload.sh` re-hashes S3 zips during inf-pipeline sweep operations and updates
    the source map JSON to match whatever is in S3 — even when S3 content has un-known provenance.

    If we apply terraform unscoped today, Lambda live transitions from known-good 2026-05-07
    content → unknown 2026-05-12 orphan content. This is a CLAUDE.md Rule 1 violation by way of
    indirection: although the apply itself runs through Terraform, the source content
    bypassed Terraform. We must reconcile before next deploy.
  </context>

  <objective>
    Three outcomes required for closure:

    (1) **Provenance:** identify what the orphan zip CONTAINS and whether the content corresponds
        to ANY commit in the repo (legitimate but undocumented build) or is provenance-unknown
        (CLAUDE.md Rule 1 violation requiring revert + re-build).

    (2) **Reconciliation:** restore the three-state divergence (source map expected = Lambda live
        = known-good commit) to a single coherent state. Decision tree:
        - If orphan content matches a known commit: ratify source map as authoritative, apply
          to push Lambda live forward to that content (with source map's `last_deployed_commit`
          backfilled to the discovered commit).
        - If orphan content is provenance-unknown: REVERT source map to 2026-05-07 known-good
          hash, REBUILD from a known commit via `build-and-upload.sh`, apply.

    (3) **Recurrence prevention:** identify who/what uploaded the orphan zip via CloudTrail S3
        `PutObject` events 2026-05-12 15:49 + 16:47 UTC. If a runaway script / scheduled job /
        another agent's offline activity, surface root cause + propose preventive guard
        (lambda-source-map update on every S3 upload OR a CI check that flags S3 uploads
        without corresponding source map commits).
  </objective>

  <phase id="0" when="before-write — empirical diagnostic, no code changes">
    <step>
      <run>aws s3api get-object-tagging --bucket opal-313476888478-lambda-artifacts --key inf-pipeline/inf-unified-account-dim-daily.zip --version-id ANTWEyecNCzcZRqapgz.5Zt_tfLzHGKq</run>
      <expect>Output includes any tagging that might identify uploader (Tier tag, Owner tag, principalId via S3 object metadata). If no tags, surface absence (S3 default tagging absent from CI uploader is suspicious).</expect>
      <if_mismatch>If S3 tagging API errors, fall through to CloudTrail step (Phase 0 Step 2).</if_mismatch>
    </step>
    <step>
      <run>aws cloudtrail lookup-events --lookup-attributes AttributeKey=ResourceName,AttributeValue=opal-313476888478-lambda-artifacts --start-time "2026-05-12T15:00:00Z" --end-time "2026-05-12T17:00:00Z" --query 'Events[?EventName==`PutObject` || EventName==`UploadPart`].[EventTime,Username,UserIdentity.type,UserIdentity.arn,RequestParameters.key,SourceIPAddress]' --output table</run>
      <expect>Two PutObject (or UploadPart-CompleteMultipartUpload) events on or near 15:49:47Z + 16:47:00Z 2026-05-12 for the inf-unified-account-dim-daily.zip key. Username/arn identifies actor: workspace user vs CI service role vs another agent's session.</expect>
      <if_mismatch>If CloudTrail retention has aged out (90 days default for management events; data events require S3 trail config), check `aws s3api list-object-versions --bucket opal-313476888478-lambda-artifacts --prefix inf-pipeline/inf-unified-account-dim-daily.zip --query 'Versions[].Owner.ID'` for differing owner IDs — would prove multiple actor identities even without full CloudTrail.</if_mismatch>
    </step>
    <step>
      <run>aws s3 cp s3://opal-313476888478-lambda-artifacts/inf-pipeline/inf-unified-account-dim-daily.zip /tmp/orphan-uad-daily.zip --version-id ANTWEyecNCzcZRqapgz.5Zt_tfLzHGKq &amp;&amp; aws s3 cp s3://opal-313476888478-lambda-artifacts/inf-pipeline/inf-unified-account-dim-daily.zip /tmp/legit-uad-daily.zip --version-id Q_bfywbFIe5reQ1k8oC65QoncETJZvfa &amp;&amp; unzip -d /tmp/orphan-uad /tmp/orphan-uad-daily.zip &amp;&amp; unzip -d /tmp/legit-uad /tmp/legit-uad-daily.zip &amp;&amp; diff -r /tmp/orphan-uad /tmp/legit-uad | head -50</run>
      <expect>Binary diff between orphan content (2026-05-12) and legitimate 2026-05-07 zip. Either: (a) ONLY a build-time embedded constant (timestamp, version string, requirements.txt freeze) differs — implying same source code, re-built — or (b) lambda_function.py / pull_unified_account_dim.py / jwt_freshness.py content differs.</expect>
      <if_mismatch>Document divergence in TO RAVC2 comment.</if_mismatch>
    </step>
    <step>
      <run>For each .py file in the orphan zip differing from the legitimate zip, run `git log --all --oneline -p -- infra/aws/lambda/inf-pipeline/inf-unified-account-dim-daily/{filename}` and search for any commit whose blob hash matches the orphan content's hash. Use `git hash-object /tmp/orphan-uad/{filename}` to compute the blob hash; then `git log --all --pretty=format:"%H %s" --diff-filter=AM | xargs -I {} git ls-tree {} -- infra/aws/lambda/inf-pipeline/inf-unified-account-dim-daily/{filename} | grep {orphan-blob-hash}`.</run>
      <expect>Either: (a) MATCH — an existing commit's tree contains an identical blob, identifying the source commit + the build context; or (b) NO MATCH — orphan content does not correspond to any commit in the repo, definitively a CLAUDE.md Rule 1 violation.</expect>
      <if_mismatch>NO MATCH ⇒ Phase 1 Branch B (revert + rebuild). MATCH ⇒ Phase 1 Branch A (ratify + backfill last_deployed_commit).</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="reconciliation — branch on Phase 0 outcome">
    <branch label="A" when="orphan content traces to a legitimate commit">
      <step>
        <run>Edit `infra/aws/lambda/ci/lambda-source-map.json` to set `functions["inf-unified-account-dim-daily"].last_deployed_commit` to the discovered commit SHA; ensure `artifact_sha256` matches the orphan content's sha256 (already does per current source map).</run>
        <expect>Source map authoritatively reflects "current S3 zip came from commit X" with a valid SHA. The `dba29da4e` source-map sweep commit's automated update is preserved; only `last_deployed_commit` field corrected.</expect>
        <if_mismatch>If commit lookup itself is ambiguous, surface options to COO before mutating source map.</if_mismatch>
      </step>
      <step>
        <run>From `infra/aws/terraform/inf-pipeline/`: `terraform plan -target=module.inf_unified_account_dim_daily.aws_lambda_function.this`</run>
        <expect>Plan shows source_code_hash diff: actual=`8eWiL153rp9...` (Lambda live, 2026-05-07 origin) → expected=`vUH5XGTYcEWs...` (source map, ratified orphan). 1 change, 0 add, 0 destroy. Plan exit 0.</expect>
        <if_mismatch>If plan shows additional un-attributed diffs on other Lambdas, document each + surface to COO before apply.</if_mismatch>
      </step>
      <step>
        <run>`terraform apply -target=module.inf_unified_account_dim_daily.aws_lambda_function.this -auto-approve`</run>
        <expect>Apply exits 0, 1 changed. Lambda live transitions to `vUH5XGTYcEWs...`. Re-plan shows 0 diff for this Lambda.</expect>
        <if_mismatch>If apply fails, halt + surface to COO.</if_mismatch>
      </step>
      <step>
        <run>`.tools/safe-commit.sh --author="0.7.0_AE_CloudOps &lt;0.7.0_AE_CloudOps@opal.agent&gt;" -m "fix(inf-uad-daily): backfill source map last_deployed_commit + apply ratified zip ..." -- infra/aws/lambda/ci/lambda-source-map.json` then `git tag -a inf-pipeline-v1.7.54 -m "..."` then `git push origin CLOUD --follow-tags`</run>
        <expect>Single commit + tag pushed. record-terraform-deploy.sh idempotent on rerun.</expect>
        <if_mismatch>If safe-commit.sh aborts on contamination, clean stray staged files via `git reset HEAD -- &lt;extras&gt;` and rerun.</if_mismatch>
      </step>
    </branch>
    <branch label="B" when="orphan content is provenance-unknown — CLAUDE.md Rule 1 violation">
      <step>
        <run>Revert `infra/aws/lambda/ci/lambda-source-map.json` entry for `inf-unified-account-dim-daily` to the 2026-05-07 known-good state (`artifact_sha256=`8eWiL153rp9...``, `last_deployed_commit=&lt;2026-05-07-origin-commit-SHA&gt;`, `last_deployed_at=2026-05-07T20:51:31Z`).</run>
        <expect>Source map reflects the only commit-traceable known-good state.</expect>
        <if_mismatch>Halt + surface to COO if origin commit lookup is ambiguous.</if_mismatch>
      </step>
      <step>
        <run>`bash infra/aws/lambda/ci/build-and-upload.sh inf-pipeline inf-unified-account-dim-daily` from a clean working tree at HEAD on CLOUD branch.</run>
        <expect>Fresh build + S3 upload + source map update with new `last_deployed_commit=&lt;current HEAD&gt;`, `last_deployed_at=&lt;now&gt;`, `artifact_sha256=&lt;new build's hash&gt;`. Build matches `lambda_function.py + pull_unified_account_dim.py + jwt_freshness.py` HEAD content.</expect>
        <if_mismatch>If build fails, halt + surface to COO.</if_mismatch>
      </step>
      <step>
        <run>`terraform plan` + apply against `module.inf_unified_account_dim_daily` — same as Branch A Step 2-3.</run>
        <expect>Lambda live = clean rebuild from current HEAD; orphan content never reached production.</expect>
        <if_mismatch>Per Branch A Step 2-3.</if_mismatch>
      </step>
      <step>
        <run>Optional: aws s3api delete-object --bucket opal-313476888478-lambda-artifacts --key inf-pipeline/inf-unified-account-dim-daily.zip --version-id &lt;both 2026-05-12 orphan version IDs&gt; — destructive; ASK COO before executing.</run>
        <expect>Orphan zip versions removed from S3 (cosmetic; current version is the fresh rebuild, so orphans are unreachable but still listed).</expect>
        <if_mismatch>HOLD — destructive operation, COO approval required.</if_mismatch>
      </step>
      <step>
        <run>Commit + tag + push (Branch A Step 4).</run>
      </step>
    </branch>
  </phase>

  <phase id="2" when="recurrence prevention — non-blocking; folds into RAVC2 doc">
    <step>
      <run>Document in RAVC2 session log: actor identity from Phase 0 Step 2 (CloudTrail) + recommended preventive guard. Options to surface to COO/CTO:
        (a) Add CI check in `build-and-upload.sh` that ABORTS if S3 zip exists but source map entry's `last_deployed_commit` doesn't HEAD match.
        (b) Add ContentMD5 metadata tagging on every S3 upload so post-hoc forensics can identify uploader.
        (c) S3 bucket policy denying PutObject without specific tag set (forces all uploads through `build-and-upload.sh` which tags).
        (d) Add lambda-source-map.json owned-paths exception requiring co-edit of an audit log file (`org/lambda-source-map-audit.log` — append-only ledger of every source map mutation).
      </run>
      <expect>RAVC2 doc cites the empirical uploader identity (or its absence) + recommends 1+ guards from the list. COO/CTO ratify before authoring follow-up TO.</expect>
      <if_mismatch>If CloudTrail aged out (no uploader identity recoverable), recommend (a) + (b) as forward-looking guards regardless of past actor.</if_mismatch>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: Phase 0 outputs (CloudTrail uploader + binary diff + git commit search) appended to TO RAVC2 closeout in session log.
    AC2: Lambda live `CodeSha256` (`aws lambda get-function-configuration --function-name inf-unified-account-dim-daily`) MATCHES source map `artifact_sha256` MATCHES the commit referenced by `last_deployed_commit`. All three coherent.
    AC3: `terraform plan` in `infra/aws/terraform/inf-pipeline/` reports ZERO source_code_hash drift on `inf-unified-account-dim-daily`. Run twice (5 min apart) to confirm stability.
    AC4: Session log Compiler Tools section reproduces `comp-iam service inf-unified-account-dim-daily` (verify no IAM gap surfaced by reconciliation) + AC2 + AC3 evidence with timestamps.
    AC5: Recurrence prevention recommendation surfaced to COO with empirical actor identity (Phase 2).
    AC6: If Branch B (revert + rebuild): commit author lineage cites the abandoned `vUH5XGTYcEWs...` orphan + the new rebuilt artifact_sha256 + the HEAD commit it was built from.
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1 (before write):
    <run>comp-iam service inf-unified-account-dim-daily</run>
    <expect>Zero MISSING permissions — Lambda's IAM policy covers all S3/CloudWatch/etc operations its source code performs.</expect>
    <if_mismatch>If MISSING: surface + fix iam.tf in same commit as Lambda reconciliation.</if_mismatch>

    Phase 2 (before commit):
    <run>comp-pipescript deployed (N/A — this is a Lambda, not a gold script)</run>
    <expect>SKIP — N/A for Lambda TOs. Substitute: post-apply `aws lambda get-function-configuration --function-name inf-unified-account-dim-daily --query 'CodeSha256'` confirms live hash matches source map.</expect>
    <if_mismatch>Document MISMATCH in RAVC2.</if_mismatch>

    Phase 3 (after commit):
    <run>comp-iam gaps</run>
    <expect>No new IAM gaps introduced; orphan reconciliation should be IAM-neutral.</expect>
    <if_mismatch>Surface to COO + author iam.tf cleanup TO.</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    SHARED FILES:
    - `infra/aws/lambda/ci/lambda-source-map.json` — owned by all AE lanes (multi-lane append-only ledger); coordinate-by-MCP with AE 0.6.1 + AE 0.6.0 + AE 0.5.0 before editing during a window where they may be building other Lambdas. AE 0.6.1 currently driving chain #25 RAVC2 + may bundle v1.7.54 with this orphan reconciliation OR keep it as a standalone tag — AE 0.7 owns the call.
    - `infra/aws/terraform/inf-pipeline/inf-unified-account-dim-daily.tf` — single-owner AE 0.7 lane.

    NO CROSS-DOMAIN BLAST:
    - No portal frontend impact (Lambda is silver-side, no UI surface).
    - No DS impact (silver dim Lambda; dim builder is internal Orion API pull).
    - DT 0.4 consult only if CI/build-and-upload.sh hygiene gap surfaces in Phase 2 recommendation.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Reasoning: this is an infrastructure reconciliation, not a code change. Lambda live state will either stay on 2026-05-07 build (Branch B revert) OR transition to ratified content (Branch A) which AE 0.6.1's plan today already characterized as a `8eWiL153rp9... → vUH5XGTYcEWs...` semantic-neutral hash flip (same `lambda_function.py` content per Phase 0 binary diff IF Branch A applies). No silver/bronze partition data semantically changes; existing silver/_silver_complete sentinels remain valid.
      
      If Phase 0 binary diff reveals MATERIAL code change in the orphan zip (e.g., logic in `pull_unified_account_dim.py` modified): SURFACE to COO before any apply — this becomes a code-correctness review, not just a reconciliation, and DS may need to validate silver outputs against the new code.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. Session log: `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-05-13/inf_uad_daily_orphan_reconcile.md` with Phase 0 forensic outputs + Phase 1 branch decision + Phase 2 prevention recommendation + Compiler Tools section reproducing AC1-AC6 evidence.
    2. Lambda reconciliation commit (Branch A or Branch B path) + `inf-pipeline-v1.7.54` git tag (assuming TO closes during today's session) + push with `--follow-tags`.
    3. Phase 2 RAVC2 to COO with the 4-option preventive guard recommendation.
  </deliverables>

  <ravc>
    AE 0.7 RAVC2s to COO when AC1-AC6 all PASS. COO RAVC4s if evidence satisfies acceptance. COO surfaces Phase 2 recommendation to CTO for ratify before authoring any follow-up preventive-guard TO.
  </ravc>
</task_order>
