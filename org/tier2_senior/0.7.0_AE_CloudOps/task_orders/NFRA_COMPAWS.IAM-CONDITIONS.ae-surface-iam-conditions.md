<to_id>NFRA_COMPAWS.IAM-CONDITIONS</to_id>
<project>NFRA_COMPAWS</project>
<title>comp-iam -- surface IAM Conditions (fix the condition-blind FALSE-POSITIVE: tag-scoped/TBAC grants false-read as broad)</title>
<assigned_to>0.7.0_AE_CloudOps (comp-iam owner-lane; same-tool = own lane; Andrew-direct routing)</assigned_to>
<arch_gate>1.0.0_SA_CTO (comp-tool change)</arch_gate>
<verify>3.0.0_SA_CVO (co-verify the fix + the FP-clear)</verify>
<issued_by>2.0.0_SA_COO (Andrew-direct via CVO 215414Z)</issued_by>
<issued_date>2026-06-24</issued_date>
<status>active</status>
<!-- Andrew-direct. CVO-confirmed at source. This is an ESTATE-WIDE comp-iam accuracy fix (every least-priv/broad-grant check), surfaced by 2 false-positives in the SCTY.W2 IAM assessments. base-AE already flagged it -> its own comp-iam owner-lane. Eclipse /v1 hash-route grounding (the recon depth-follow) is CTO-confirmed DEFERRABLE -- this comp-iam fix takes base-AE's next-build capacity. -->

<the_work>
comp-iam surfaces a grant's Action + Resource but OMITS the Condition -> a tag-scoped (TBAC) grant false-reads as broad. FIX:
1. EXTRACT + DISPLAY the Condition in the comp-iam perm/edge view (the IAM statement's Condition block alongside Action/Resource).
2. FACTOR the Condition into the broad-vs-scoped classification: a ResourceTag/TBAC Resource:"*" carrying a scoping Condition (e.g. StringEquals ec2:ResourceTag/...) must NOT score as broad/unscoped. (Sibling to the existing deny-Principal:*-is-a-guardrail handling -- comp-iam records the edge but was dropping the qualifier that changes its meaning.)
ANCHOR (the live FP): bd-exporter-ec2-role ec2:TerminateInstances Resource:"*" WITH Condition StringEquals{ec2:ResourceTag/ManagedBy=lambda-scheduler} (infra/aws/terraform/bd-pipeline/iam.tf:445-453) -- currently false-reads as unscoped Resource:* broad; FP'd BOTH SCTY.W2 assessments (CVO's + AE~B's), nearly drove a wrong scope-down of an already-correctly-scoped grant.
</the_work>

<acceptance_criteria>
1. comp-iam perm/edge view surfaces the Condition block.
2. broad-vs-scoped classification factors the Condition: the bd-exporter TerminateInstances grant reads TAG-SCOPED (not broad); the deny-Principal:* guardrail class stays correctly handled.
3. Re-run on the SCTY.W2 IAM findings -> the bd-role-scope FALSE-POSITIVE clears; estate-wide regression spot-check confirms a genuinely-broad grant (no scoping Condition) STILL scores broad (no new false-negative).
4. CTO arch-gates the comp-tool change; CVO co-verifies (Condition surfaced + the bd-role-class reads tag-scoped). same-tool lane = base-AE commits in-lane.
</acceptance_criteria>
