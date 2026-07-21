<task_order>
<id>WSE_COTMDL.WS4.mdpf-ddb-foldin</id>
<project>WSE_COTMDL</project>
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>staged</status>
<priority>P1 (LAST in the chain; gated on WS-3 + CTO DDB-contract + cutover precedence)</priority>
<date>2026-07-21</date>

<references>
  <ref type="prd">docs/architecture/WSE_COTTONWOOD_MDPF_FOLDIN_PRD.md (sec 8)</ref>
</references>

<objective>
Fold the gold dim_model_portfolio rows into the MDPF DDB as the Cottonwood contribution, firm-separated
(cottonwood), same model-row shape as the other firms. Ground the exact DDB write path + schema FIRST; scoped
IAM per Rule 22a; CTO gates the DDB-contract before any MDPF write.
</objective>

<hard_gate>
CTO gates the DDB fold-in CONTRACT (PRD sec 8) BEFORE the first MDPF write. Do NOT write to the MDPF DDB until
CTO has ratified the exact model-row schema + write path. NEVER hand-write any MDPF completion/pipeline-complete
marker (forged-completion / Door-6 class).
</hard_gate>

<scope>
  <in>
    - GROUND (Rule 20 dependency graph + Rule 22 mechanism, at SOURCE): the exact MDPF DDB table, the model-row / held_by_partner schema, and the write path the other firms use. Do NOT infer.
    - The firm-separated Cottonwood fold-in write (keyed cottonwood), same shape as other firms' model rows.
    - Scoped IAM for the DDB write, verified per Rule 22a: `aws iam simulate-principal-policy --resource-arns <exact table ARN> --action-names dynamodb:PutItem` (ONE resource-arn/call; isolated positive control). comp-iam is NOT sufficient for a new table/action.
  </in>
  <out>
    - NO write to any firm's rows but cottonwood. NO MDPF completion-marker hand-write. NO new alarm.
  </out>
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-blast (the MDPF DDB write path / the aggregate->DDB fold) + comp-aws (the MDPF DDB table)</run>
      <expect>Enumerate the exact DDB table + write path + the model-row schema the other firms use. Confirm the cottonwood key is firm-separated.</expect>
      <if_mismatch>STOP. Ground the DDB contract at source before writing; surface to CTO (who gates sec 8).</if_mismatch>
    </step>
    <step>
      <run>aws iam simulate-principal-policy --policy-source-arn &lt;fold-in role&gt; --action-names dynamodb:PutItem --resource-arns &lt;exact MDPF DDB table ARN&gt; (+ SEPARATE positive control)</run>
      <expect>GRANTED for the exact table; positive control (a known-held action) confirms the simulator is discriminating. NO 2+ resource-arns in one call.</expect>
      <if_mismatch>STOP. Fix IAM (coord WS-5) + re-verify on the live primitive before any write.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after first fold-in">
    <step>
      <run>DDB get/query the cottonwood model rows post-write + confirm other firms' rows UNCHANGED</run>
      <expect>Cottonwood rows present + correct shape; 49F/Inflection/global rows byte-unchanged (firm-sep held).</expect>
      <if_mismatch>STOP + RED-ALERT to COO+CTO. Any other-firm-row change = firm-sep violation, roll back.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
  - WS-3 (DS): provides the gold dim_model_portfolio this folds in. QA/verify the first dim before it serves (PRD sec 11f).
  - WS-D / MDPF surface: coordinate the DDB model-row contract (CTO gates sec 8).
  - 0.2.0_DT_PortfolioAnalytics: MDPF DDB / parity context -- coordinate the schema.
  - WS-5 (self-lane): the fold-in role's DDB grant.
</cross_domain_coordination>

<acceptance_criteria>
  1. CTO-ratified DDB contract (sec 8) BEFORE any write.
  2. Cottonwood model rows folded in firm-separated; other firms' rows unchanged (machine-verified).
  3. DDB PutItem IAM verified on the exact table ARN via simulate-principal-policy (isolated positive control).
  4. NO MDPF completion-marker hand-written. Session log Compiler Tools section reproduces every <run>.
</acceptance_criteria>

<dependencies>
  <dependency agent="0.4.0_DS_ClientPlatform" task="WSE_COTMDL.WS3 (gold dim)" status="staged"/>
  <dependency agent="1.0.0_SA_CTO" task="DDB fold-in contract ratification (sec 8)" status="pending"/>
  <dependency agent="0.7.0_AE_CloudOps" task="WSE_COTMDL.WS5 (fold-in role DDB grant)" status="staged"/>
</dependencies>
</task_order>
