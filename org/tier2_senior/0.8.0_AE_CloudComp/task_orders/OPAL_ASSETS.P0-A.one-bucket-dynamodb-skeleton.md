<task_order>
<id>OPAL_ASSETS.P0-A</id>
<project>OPAL_ASSETS</project>
<title>P0 -- the ONE canonical daily AUM bucket SKELETON (G5 shell): a DynamoDB table + a skeleton emitter that reads the ALREADY-DAILY SERVED sources and writes one honest row per cohort per day. Opal-side ONLY. No sovereign reads.</title>
<assigned_to>0.8.0_AE_CloudComp</assigned_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_date>2026-07-13</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: project OPAL_ASSETS is complete-as-superseded; this TO was last touched 2026-07-12, predating the project close 2026-07-15. Closed as a record act, not a work verdict. Prior status: pending</status>
<priority>P0 -- BUILDABLE NOW, no sovereign gate. Andrew-commissioned macro-project; MSTR-authorized P0 start (030x). This is the AE half of G5 (bucket + served artifact); the DS half (G4 avgcap fold + the mdpf emitter extension) is STAGED for DS post-Round-8 (OPAL_ASSETS.P0-B). The skeleton reads EXISTING served outputs, so it does NOT block on DS.</priority>
<dispatch>GO 2026-07-13 by 2.0.0_SA_COO. You are the confirmed sole 0.8.0 lane (MSTR respawn, PID 29628). Read the PRD full_spec BEFORE building.</dispatch>
<full_spec>docs/architecture/OPAL_ASSETS_PRD.md @ 79231da3e (PRD v0.1, CTO~B). This TO is the AE-side P0 slice of PRD sec 4 (G5) + sec 6 (P0). The PRD is authoritative on row shape, as_of semantics, and guardrails -- read sec 0, 3a, 3d, 4:G5, 6, 7 before building.</full_spec>

<load_bearing_invariants>
  1. STRICTLY OPAL-SIDE (MSTR-direct guardrail, hard): the skeleton reads ONLY already-daily SERVED outputs -- the mdpf `aggregate_aua` served artifact, the Opal-ETF issuer-float served outputs (TrueShares/Filepoint), and Inflection served. NO new bd / Schwab / RPS / 08335338 / 08242234 reads -- those are P1/sovereign, HELD for Andrew's nod. If the skeleton appears to NEED a new sovereign read to populate a cohort, STOP and flag COO -- that cohort is P1, label it in-row and move on; do NOT drift into a sovereign read.
  2. ONE ROW PER COHORT PER DAY, HONEST STATE (PRD sec 0, 3a, 3d): row shape `{cohort, source_master(s), value, as_of, state}` where `state in {fresh, rolled_forward, missing}`. Each row carries its OWN-field `as_of` -- NEVER a cross-partner min/aggregate as_of. A stale cohort reads stale FOR ITSELF; an absent cohort reads `missing`; never silently rolled forward into a false green, never smeared. This IS the deliverable's honesty (PRD sec 7 guardrail 5: NEVER silently undercount).
  3. DYNAMODB VIA TERRAFORM ONLY (Andrew-direct persist target; CLAUDE.md deploy rules): create the table through `.tools/safe-apply.sh` -- no console, no boto3 create_table. Key design MUST satisfy BOTH access patterns in one table: (a) a day's 14 rows = ONE query (PK=date, SK=cohort), AND (b) any cohort's full history = ONE query (a GSI PK=cohort, SK=date, or equivalent). Demonstrate both queries return in acceptance.
  4. RULE 22a IAM ON THE WRITE (hard, SEV-ish -- it is a NEW resource): the emitter's DynamoDB PutItem is a NEW-resource grant. comp-iam models (action) NOT (action,resource) and will clear it green falsely. Verify APPLIED truth with `aws iam simulate-principal-policy --policy-source-arn <emitter role> --action-names dynamodb:PutItem dynamodb:Query --resource-arns <EXACT table ARN + GSI ARN>` WITH a positive control on a resource the role DOES hold (else a refusal reads as implicitDeny and you learn nothing). Live-grounded, not comp-iam-DESIRED-alone.
  5. G6 IS THE ACCEPTANCE HARNESS, NOT A BUILD ITEM: the 14 per-cohort freshness alarms (mdpf-pipeline-v1.5.0, 0.7.0~A) already discriminate live. The bucket row's `state`/`as_of` MUST be consistent with the G6 stamp shape (the row IS the G6 stamp promoted to the bucket). Align, do not re-derive.
  6. NO SERVED CUTOVER IN P0: this is the SKELETON. It stands up the table + emitter + honest rows. It does NOT flip any served ModelPortfolios/AUM surface onto the bucket -- that is P2 and rides NEVER#2 never-widen co-sign + NEVER#4. P0 delivers a bucket that is honest-about-its-gaps, running alongside (not replacing) today's surface.
</load_bearing_invariants>

<compiler_tools_mandate>
  BEFORE WRITE: `comp-blast mdpf_aggregate_aua` (know what already consumes the mdpf served output you read) + `comp-iam service <emitter-lambda>` (perms baseline before the new DynamoDB grant) + `comp-which "what serves the mdpf aggregate_aua daily output"` (confirm the exact SERVED artifact path you read -- do not read a producer intermediate).
  BEFORE COMMIT: `.tools/commit-gate.sh` on every .py (py_compile + ruff); if the emitter is gold-tier add `from __future__ import annotations` (ADHC_DSFLOW.004). `comp-iam gaps` after the iam.tf change.
  AFTER COMMIT/APPLY: `comp-pipescript deployed <emitter>` (MATCH) + the simulate-principal-policy live check (invariant 4) + a real DEPLOYED-role PutItem exercise (not local creds).
</compiler_tools_mandate>

<cross_domain_coordination>
  - **DS (0.4.0_DS_ClientPlatform)** owns the DS half of G5 (mdpf emitter extension) + G4 (avgcap fold) -> OPAL_ASSETS.P0-B, STAGED post-Round-8. The SKELETON reads the EXISTING mdpf served artifact, so no live DS dependency for THIS TO -- but coordinate the row-shape contract with DS before P0-B so the emitter extension writes the same shape. MCP DS before you finalize the table schema.
  - **0.7.0_AE_CloudOps~A** shipped the G6 per-cohort freshness stamp+alarms (mdpf-pipeline-v1.5.0). Your `state`/`as_of` row fields MUST match that stamp's semantics. MCP ~A for the stamp shape; do not diverge.
  - **MDPF_ASSETS** is the depends_on (OPAL_ASSETS extends the mdpf aggregate_aua emitter + freshness checker). Do not fork mdpf; extend/read it.
  - **CTO~B (1.0.0_SA_CTO~B)** is the arch-gate + never-widen principal -- route the table-schema + emitter design to CTO~B before apply if it touches any served contract; the P0 skeleton itself is Opal-side/non-served so a light heads-up suffices, but the ROW SHAPE is the eventual served contract -- get his eyes on the schema.
</cross_domain_coordination>

<acceptance_criteria>
  1. DynamoDB table EXISTS via Terraform (safe-apply, 0-diff post-apply verified). Both access patterns demonstrated with a live query: (a) one query returns a given day's rows for all present cohorts; (b) one query returns a given cohort's history across days. Falsifier: either pattern needs a scan or a second table.
  2. The skeleton emitter writes EXACTLY ONE row per cohort per day for the cohorts it can source from EXISTING served outputs (target: all 14 represented -- a cohort with no Opal-side served source lands as `state=missing`, NOT omitted). Falsifier: a cohort silently absent from a day's partition.
  3. Each row's `as_of` == that cohort's OWN-field as_of (never a cross-partner min). Verify by reading two cohorts with different as_of on the same day -> both distinct values present. Falsifier: two cohorts sharing a smeared as_of.
  4. `state` correctly labels current prod truth: the SOLID cohorts `fresh`, the 8 49F-decomposition cohorts `rolled_forward` carrying their real stale as_of (07-06 as of PRD authoring), any un-sourceable cohort `missing`. Cross-check against the live G6 alarm state (a cohort in ALARM must not read `fresh`). Falsifier: a rolled_forward/missing cohort labeled `fresh`.
  5. Rule 22a live IAM: simulate-principal-policy on the EXACT table + GSI ARN for PutItem+Query, WITH a positive control, ALLOWED; and a real DEPLOYED-role PutItem succeeded (exercised, not local-cred). Falsifier: acceptance rests on comp-iam DESIRED or a local-cred write.
  6. ZERO new sovereign reads in the code path: `grep` the emitter for any bd/schwab/rps/08335338/08242234/black_diamond read -> none. Falsifier: any such read present.
  DELIVERABLE: session log with the Compiler Tools section; RAVC2 back to 2.0.0_SA_COO with the table ARN, the two demo queries' output, the simulate-principal-policy evidence (+positive control), and the day's 14-row partition dump showing the state/as_of labels.
</acceptance_criteria>
</task_order>
