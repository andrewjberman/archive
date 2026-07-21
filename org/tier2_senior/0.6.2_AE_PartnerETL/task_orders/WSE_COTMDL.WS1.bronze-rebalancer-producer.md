<task_order>
<id>WSE_COTMDL.WS1.bronze-rebalancer-producer</id>
<project>WSE_COTMDL</project>
<issued_to>0.6.2_AE_PartnerETL</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<priority>P1 (parallel to MDPF cutover; cutover keeps attention precedence)</priority>
<date>2026-07-21</date>

<references>
  <ref type="prd">docs/architecture/WSE_COTTONWOOD_MDPF_FOLDIN_PRD.md (sec 3,4,5,7,9,10)</ref>
  <ref type="discovery">org/tier2_senior/0.6.2_AE_PartnerETL/deliverables/COT_MODEL_PORTFOLIO_DISCOVERY_WSE_20260721.md</ref>
</references>

<objective>
Build the EventBridge-scheduled bronze producer `opal-assets-bd-rebalancer-daily-pull` that mints a
Rebalancer bearer off blackdiamond/cot/session and lands the 3 raw BD Rebalancer JSON types byte-for-byte
under s3://opal-data-assets/blackdiamond/cottonwood/bronze/, then emits the complete-stamp LAST. Mirror the
existing opal-assets-bd49f-* BD producer -- do NOT improvise a sibling pattern.
</objective>

<hard_gate>
STANDING VENDOR-EGRESS WORD (Andrew) is REQUIRED before the SCHEDULED daily pull ships/runs. The per-use
grants (@b5af1e929, @3e563306c) were discovery/scoped-read -- a recurring producer needs the standing grant.
COO has SURFACED this to Andrew. You may BUILD + unit-test the producer (dry, no live scheduled egress) while
staged, but the scheduled daily pull does NOT activate until the standing word lands. Do NOT assume the
per-use grant covers the recurring producer.
</hard_gate>

<scope>
  <in>
    - Auth: GET rebalancer.bdreporting.com/auth/token (Cookie-authed off blackdiamond/cot/session); re-mint mid-run; re-pull cookie on 401. requests.Session + urllib3 Retry (C5 smartx_client pattern).
    - 3 bronze pulls, byte-for-byte (Rule 17a, NO parquet at bronze): bronze/rebalancer_models/MODELS_{date}.json (POST /api/models/strategies/search paginated), bronze/rebalancer_model_detail/{modelId}_{date}.json (GET /api/models/{id} per model), bronze/rebalancer_accounts/ACCOUNTS_{date}.json (POST /api/accounts/search take=200 paginated, full 910-account book).
    - Landing verified by the listing-based set-identity guard (landing_guard.py / mirror_conversion.set_identity, ListObjectsV2 run-time denominators). Emit meta/{date}-complete.json stamp LAST (never before all 3 land).
  </in>
  <out>
    - NO writes anywhere except blackdiamond/cottonwood/bronze|meta (firm-sep; never blackdiamond/49f). NO parquet at bronze. NO DataMining assignment pull (Rebalancer is authoritative). NO model-scoped GET paths (/api/models/{id}/accounts etc. = SPA-shell 200, NOT real routes -- PRD sec 4 negative finding). NO new alarm/twin (07-17 suspend). Cookie in-memory only, never logged/committed.
  </out>
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-iam service opal-assets-bd-rebalancer-daily-pull (or the mirrored bd49f producer role as the pattern)</run>
      <expect>The scoped role can PutObject to blackdiamond/cottonwood/bronze/** + meta/**, read blackdiamond/cot/session secret, read cot holdings silver. NO write to blackdiamond/49f.</expect>
      <if_mismatch>STOP. comp-iam models (action) not (action,resource): verify the exact new prefix with `aws iam simulate-principal-policy --policy-source-arn <role> --action-names s3:PutObject --resource-arns <exact blackdiamond/cottonwood/bronze key>` (ONE resource-arn/call; positive control SEPARATE; ground fresh IAM on live get-role-policy). Coordinate the role with WS-5 (0.7.0).</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io (the opal-assets-bd49f producer being mirrored)</run>
      <expect>Confirm the mirrored pattern's landing-guard + complete-stamp + firm-sep assert -- replicate, do not improvise.</expect>
      <if_mismatch>STOP. Ground the sibling pattern before writing.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/commit-gate.sh on the producer .py (py_compile + ds-precommit + ruff); `from __future__ import annotations` present</run>
      <expect>PASS. Bronze writes raw JSON only (Rule 17a) -- NO parquet, NO schema coercion at ingest.</expect>
      <if_mismatch>STOP. Fix before commit.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy (post standing-egress GO)">
    <step>
      <run>aws s3 ls s3://opal-data-assets/blackdiamond/cottonwood/bronze/ (ListObjectsV2 key+ETag+Size) after first scheduled run</run>
      <expect>All 3 raw types land (models + model_detail per model + accounts) + meta/{date}-complete.json stamp LAST, mtime > deploy-commit-time. HeadObject is NOT the acceptance instrument.</expect>
      <if_mismatch>Surface to COO+CTO. Missing/partial = producer wiring failed; the complete-stamp must NOT emit on a partial land.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
  - WS-5 (0.7.0_AE_CloudOps): owns the scoped IAM role + EventBridge schedule + TF -- coordinate the role/schedule BEFORE the producer deploys (the producer runs under WS-5's role/trigger).
  - WS-2 (DS): consumes your bronze; the complete-stamp triggers WS-2 silver. Notify DS on first bronze land.
  - Firm-sep: never touch blackdiamond/49f (IAM deny + assert).
</cross_domain_coordination>

<acceptance_criteria>
  1. 3 raw bronze JSON types land byte-for-byte under blackdiamond/cottonwood/bronze/ on the schedule (ListObjectsV2-verified); meta complete-stamp emitted LAST only on full land.
  2. NO parquet at bronze; NO write outside blackdiamond/cottonwood/{bronze,meta}; firm-sep assert exercised.
  3. Standing egress word confirmed present before the scheduled pull activates.
  4. Session log Compiler Tools section reproduces every <run> + observed result + pass/fail vs <expect>.
</acceptance_criteria>

<dependencies>
  <dependency agent="ANDREW" task="standing-egress-word" status="pending (surfaced by COO)"/>
  <dependency agent="0.7.0_AE_CloudOps" task="WSE_COTMDL.WS5 (scoped role + EventBridge)" status="staged"/>
</dependencies>
</task_order>
