<task_order>
<to_id>NFRA_COMPSIMILAR.PH1</to_id>
<title>comp-similar Phase 1 — stand up the STABLE resource-summary corpus: the ARN-keyed resource_summaries Iceberg table (globgrph Nessie) + Kuzu projection + derive-at-scan populate</title>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<!-- STAFFING RESOLVED (Andrew-direct 2026-07-17 ~20:2xZ via COO): builder lane = 0.8.0~D (shared with
     NFRA_KUZUSPLIT; base stays Andrew-reserved per LD-0305). MSTR spawn requested. Still gated on CTO arch-gate below. -->
<date>2026-07-17</date>
<status>pending</status>
<!-- GO LIVE 2026-07-17 ~20:5xZ (COO). CTO ARCH-GATED @c3aa13d05 (200221Z): PRD promoted to
     docs/architecture/NFRA_COMPSIMILAR_PRD.md; §9 rules all 6 decisions. BUILD corpus derive-at-scan + table
     DDL now; TF APPLY is the gated step (see standing condition below). Re-homed base->~D per Andrew staffing. -->
<priority>P2 (Andrew batch 2026-07-17). GATE CLEARED — CTO arch-gated @c3aa13d05, all 6 decisions ruled §9.</priority>

<authority>
Andrew-direct (0.8.0 terminal 2026-07-17, recorded @dc4207c7c/1d81e760b/3d326af47): comp-similar = the
functional-overlap axis (BM25 over a resource's SUMMARY, not its name/body like comp-dups) + the
superseded-twin decommission heuristic. PRD v0.1 @ docs/architecture/NFRA_COMPSIMILAR_PRD.md.
</authority>

<gate>
GATE CLEARED — CTO arch-gate @c3aa13d05 (200221Z), all 6 §9 rulings: (1) corpus v1 = DERIVE-AT-SCAN
(authored = PH3); (2) resource_summaries Iceberg + Kuzu LEFT-JOIN APPROVED; (3) OWN TOOL (not a comp-dups
mode); (4) authoring = PH3 gated behind PH1+PH2; (5) heat = BOTH comp-heat(data-cold) + comp-debris
(invoke-cold), confidence-graded [carries to PH2 --supersede]; (6) registration per COMPCLOSE. Lane = ~D
(Andrew staffing). BUILD corpus derive-at-scan + table DDL is GO.
** STANDING CONDITION (CTO) — the TF APPLY is the gated step: NO `terraform apply` on resource_summaries until
   (a) CTO's plan-gate reads the diff (must be NEW-TERRITORY pure-add, nothing modified) AND (b) ~D settles the
   Kuzu-projection coordination with NFRA_KUZUSPLIT (same comp-kuzu path — PH1's LEFT-JOIN and KUZUSPLIT's
   full/inc split must be ONE refresh model, not two). Route the plan to CTO. **
</gate>

<scope>
Phase 1 = the one NOVEL substrate the tool needs (the engine itself is copy-reuse of dup_scan.py's BM25).
  1. Create the ARN-keyed append-only Iceberg table `resource_summaries` in the globgrph Nessie catalog
     (net-new beside graph_nodes/graph_edges; every summary write = an attributable Nessie commit; NO
     collision with graph_nodes — a SEPARATE table per the PRD, not a graph_nodes column).
  2. The Kuzu projection so comp-similar can query it locally (rides the comp-kuzu refresh — coordinate with
     NFRA_KUZUSPLIT's projection model; do NOT hand-roll a second refresh path).
  3. derive-at-scan populate for v1: a resource with no stored summary gets one derived at scan time and
     written back (the "establish, not read" resolution — the summary field does not exist upstream yet).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>aws iam simulate-principal-policy --policy-source-arn &lt;builder-role&gt; --action-names glue:CreateTable s3:PutObject --resource-arns &lt;exact resource_summaries table ARN / S3 prefix&gt; (ONE --resource-arns per call, positive control SEPARATE)</run>
      <expect>Explicit allow on the NEW table/prefix. comp-iam is NECESSARY-NOT-SUFFICIENT for a new resource (models action not (action,resource)) — ground on the live simulate call per Rule 22a.</expect>
      <if_mismatch>STOP. Missing perm on the new table = surface to CTO for the IAM leg before writing.</if_mismatch>
    </step>
    <step>
      <run>comp-aws (globgrph Nessie catalog view) — confirm graph_nodes/graph_edges schema + that resource_summaries does not already exist</run>
      <expect>resource_summaries ABSENT (net-new); graph_nodes summary field CONFIRMED absent (grounds derive-at-scan v1).</expect>
      <if_mismatch>STOP. If a summary field exists, the PRD's derive-at-scan premise changes — re-confirm with CTO.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>Exercise: write 3 real summaries, read them back via the Kuzu projection, confirm ARN-keyed + append-only (a second write to the same ARN appends a versioned row, does not overwrite)</run>
      <expect>3 rows land, project to Kuzu, read-back exact. Append-only proven by the versioned second write.</expect>
      <if_mismatch>STOP. Do not signal Phase-1 complete on an unexercised table.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
NFRA_KUZUSPLIT (same 0.8.0 platform domain): the resource_summaries Kuzu projection must ride the
comp-kuzu-inc/full refresh model KUZUSPLIT defines — coordinate the projection so there is ONE refresh path,
not two. NFRA_COMPSIMILAR composes with OPAL_TAXONOMY's P3-CENSUS: comp-similar's heat-divergence output is
the census's "unused-by-heat" column (~C). Feeds OPAL_LCLRPO (disposal). alert-suspension: comp-similar is a
READ/scan tool, no SES/SNS/CloudWatch leg — clear of the suspension.
</cross_domain_coordination>

<acceptance_criteria>
1. resource_summaries Iceberg table LIVE on Nessie main + Kuzu projection reads it; IAM verified on the live
   simulate call (not comp-iam alone).
2. derive-at-scan populates a summary-less resource and writes it back, exercised on 3+ real ARNs.
3. Session log Compiler Tools section reproduces each mandate run + observed result vs expect.
Phase 2 (the comp-similar engine + supersede mode + registration) and Phase 3 (the ~549-target authored
summary pass) are SEPARATE staged TOs, cut when Phase 1 lands.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/NFRA_COMPSIMILAR_PRD.md</ref>
  <ref type="prd-draft">org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_COMPSIMILAR_PRD_v0.1_DRAFT.md</ref>
  <ref type="project">org/projects/NFRA_COMPSIMILAR.json</ref>
</references>
</task_order>
