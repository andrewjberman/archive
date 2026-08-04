<task_order>
<to_id>ADHOC.unmanaged-lambdas-adoption</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.7.0_AE_CloudOps~E</issued_to>
<date>2026-08-04</date>
<status>pending</status>
<priority>P2 (CTO morning-wave add 170852Z + rider 170951Z, pulled forward: your lane spawned for a since-superseded build (Andrew took cochange to his own terminal) and this is the ready work fitting your profile)</priority>

<title>Seven unmanaged live Lambdas: ONE adoption-by-default TO with a per-function verdict table -- coldness-discriminated, CRO consulted on the research-adjacent pair, nothing deleted in-TO</title>

<context>
CTO~B's RCG cycle-3 Rule-1 census (460/460 TF files scanned, contrast-case checked): SEVEN live
registered Lambdas have NO Terraform anywhere -- access-anomaly-scanner,
opal-bd-transaction-consolidator, cost-anomaly-scanner, finbert-batch-processor,
schwab-anonymizer, security-sweep-comprehensive, sentiment_query_api. All seven live +
functioning; this is governance adoption, not firefighting.

DISPOSITION FRAMEWORK (CTO 170852Z, binding): ADOPTION-BY-DEFAULT per NFRA_TERRAFORM-P2;
comp-debris + role-coldness as the decommission-candidate DISCRIMINATOR; ONE TO with a
per-function verdict table; CRO CONSULTED before any call on the two research-stack-adjacent
functions; NOTHING DELETED in-TO (a decommission verdict is a recommendation with evidence,
never an action here).

NAME-STEM CONFLATION GUARD (CTO rider 170951Z, fold verbatim -- ONE explicit line the verdict
table must carry): 'finbert (10-file TREE)' = dead, ARCHIVE evidence at CRO (RCG record) vs
'finbert-batch-processor (LIVE fn, finbert_batch_processor/ 1-file tree)' = THIS TO's
adoption-or-decommission subject. Independent artifacts; NEITHER disposition reads onto the
other -- a reader who saw the RCG deliverable must not inherit "finbert is dead" onto the live
function, nor read a KEEP as contradicting CRO's ARCHIVE. Mechanical lead for the CRO check:
the dead tree's IAM history pointed at opal-news-ai-sentiment (live) -- the finbert lineage
runs through the news sentiment stack; CRO will know if the batch processor is current tooling.
</context>

<scope>
Per function (x7): (1) live state grounded (get-function-configuration, role, triggers, last
invocations via the role-coldness read); (2) comp-debris + coldness discriminator applied;
(3) verdict = ADOPT (author the TF import/resource per NFRA_TERRAFORM-P2, source-map entry per
Rule 4) or DECOMMISSION-CANDIDATE (evidence dossier only -- routing to CTO, nothing deleted);
(4) the finbert name-stem line in the table verbatim; (5) CRO consult BEFORE any verdict on the
two research-stack-adjacent functions (finbert-batch-processor + sentiment_query_api) -- their
answer is part of the evidence, not optional. ADOPTED functions: TF committed; applies are
targeted + follow the deploy law (safe-apply, 0-diff verify, tag); imports must not perturb
live config (import-then-plan-zero-diff is the proof).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before any TF authoring">
    <step><run>per function: live primitives (get-function-configuration + role read + trigger census) + comp-debris + the coldness read; comp-iam service where mapped</run>
    <expect>Seven grounded state rows; the discriminator applied with its inputs shown, zero verdicts inferred from names.</expect>
    <if_mismatch>A function whose state cannot be grounded gets an UNKNOWN row and routes to CTO -- never a default verdict.</if_mismatch></step>
  </phase>
  <phase id="2" when="before commit/apply">
    <step><run>ADOPT verdicts: TF import + plan -> ZERO-DIFF proof per function (the import must not change live config); source-map entries added (Rule 4 -- tonight's record-terraform-deploy blindness is the cautionary specimen: verify the map entry lands, do not trust the updater)</run>
    <expect>Import-plan-zero-diff captured per adopted function; source map verified by READ.</expect>
    <if_mismatch>STOP on any nonzero import plan -- an import that would mutate live config is a finding, not an apply.</if_mismatch></step>
  </phase>
  <phase id="3" when="after">
    <step><run>the verdict table (7 rows: state + discriminator inputs + verdict + evidence) to me + CTO + CTO~B (census closure) + CRO (their consult answers cited); decommission dossiers routed, not acted</run>
    <expect>CTO~B can close the Rule-1 census finding on your table.</expect>
    <if_mismatch>REWORK per CTO.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
CRO consult on the research pair is BLOCKING for those two verdicts only (the other five
proceed). TF touches infra/ -- your lane's own paths. The record-terraform-deploy detection-gap
fix (separate morning item) is NOT yours -- but your Phase-2 source-map verification works
around its blindness manually, per the specimen. Nothing shared with the live yang/mdpf
streams.
</cross_domain_coordination>

<acceptance_criteria>
1. Seven-row verdict table, every row grounded on live primitives + discriminator inputs shown.
2. The finbert name-stem line verbatim in the table.
3. CRO consult answers cited for the research pair.
4. ADOPTs: import-plan-zero-diff + source-map-verified-by-read per function; DECOMMISSION
   candidates: dossier-only, routed.
Plus: session log Compiler Tools section reproducing every run. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="framework">CTO 170852Z (adoption-by-default + discriminator + one-TO shape) + rider 170951Z (name-stem guard, folded verbatim above)</ref>
  <ref type="census">CTO~B RCG cycle-3 Rule-1 finding (460/460 scanned)</ref>
  <ref type="law">NFRA_TERRAFORM-P2 (adoption); Rule 4 (source map); deploy law rows 1-6</ref>
</references>
<dependencies><none/></dependencies>
</task_order>
