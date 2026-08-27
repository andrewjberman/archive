# Task Order: NFRA_TERRAFORM TO-2 — P2 REMEDIATION (the highest-risk phase; safe-first, human-gated)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-09-nfra-terraform-to2-remediation</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-07-09</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_TERRAFORM, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>
    <dispatch_state>DISPATCHED + GO 2026-07-09 (Andrew NFRA-first). Executes UNDER the CTO-ARCH-GATED remediation-safety model (infra/aws/NFRA_TERRAFORM_P2_remediation_safety_model.md, 603750209 + c70aeb817 clarification -- CTO arch-gate PASS stands). 0.5.0 owns it end-to-end (did P1 7b4c484fe + P1.5 6ca51a1c0; has the full grounding + wrote the safety model). LIVE-verified reachable (17 work-calls this tick).</dispatch_state>
    <gate_note>THE HIGHEST-RISK PHASE. safe-apply(HALTGT) for EVERY apply; deploy-completion ledger for each multi-step batch; CTO arch-gates each remediation BATCH; CVO certs 0-diff APPLIED==DESIRED (Rule 22a, EXERCISED not config-read).</gate_note>
  </metadata>

  <objective>Close the ~210 UNMANAGED + 15 DRIFTED + state-integrity gaps from P1/P1.5 -> 100% of should-be-managed resources under TF at 0-diff. Executed strictly under the arch-gated safety model, SAFE-FIRST, batch-by-batch, with human sign-off for every irreversible op.</objective>

  <the_hard_rules>
    1. IMPORTS @0-DIFF + TF-ADOPTS-LIVE are the PRIMARY tools (0 live change). If a post-import plan shows a diff -> the authored TF doesn't match live -> FIX THE TF, never apply-to-change during an import.
    2. NO destroy/replace on a LIVE resource without EXPLICIT sign-off: COO-confirm for pure cost-cleanup (idle/stopped, no data/state); ANDREW-confirm for anything with data/state or beyond-cost irreversibility. NEVER agent-self-confirm a delete (CTO clarification c70aeb817 -- a delete of even an idle resource IS a destroy).
    3. GROUND THE MECHANISM before any act (Rule 22): read the resource/producer, prove the remediation is benign, cite it.
    4. FIRM-SEPARATION preserved (bd/cot/inf never cross).
    5. safe-apply(HALTGT) every apply; deploy-ledger open->close per batch.
  </the_hard_rules>

  <sequence>
    <batch id="A" name="TIER-A destroy-live REPLACES -- CAREFUL-FIRST, root-cause, config-only">The 5 (astn/bd-49f-auto-login/crawl-harness/etfs-reports/m365) that plan wants to REPLACE a live EC2. ROOT-CAUSE each FIRST: prove it's benign config drift (AMI/user-data/tag), add the lifecycle `ignore_changes` (or align the TF to live), re-plan to 0-DIFF. This is a CONFIG-ONLY fix -- NEVER apply the replace. If any genuinely needs a live change -> STOP + Andrew. RAVC me + CTO per resolved module; CVO certs the 0-diff.</batch>
    <batch id="B" name="TIER-1 UNMANAGED imports @0-diff">seeking-alpha state-recovery (import-never-reapply), opal-data-bd bucket import, bd-exporter-sg import, inf-parity Deny-belt (the additive cross-firm Deny, never-widens), opal-portal-lambda-role (import + flag the cross-firm-bd-write for review), cloudfront-WAF, the 54 unmanaged secrets. Each import @0-diff, safe-apply, per-group.</batch>
    <batch id="C" name="STATE-INTEGRITY">partner-etl-ops-queue 2-module CONFLICT -> state-rm the duplicate (keep one owner); 2 empty decommissioned skeletons -> trivial s3 rm (COO-confirm, pure cleanup); 49f compdiff = DEPLOY per the joint ruling (COO~B+COO, source-confirmed never-completed) -- PARTIAL now (position-parity + broken-cert guard, no gap-vars) on the un-freeze confirm + served-guard's CTO-GATE-2/COO-floor; gap-drift alarm deferred to the CVO-grounded VP_CERT_GAP baseline.</batch>
    <batch id="D" name="TIER-2/TIER-3 remainder">Tier-2 compute (14 Lambda/23 IAM/12 DDB/4 APIGW/15 EventBridge/5 ECR) imports@0-diff; Tier-3 cost-cleanup deletes = HUMAN-confirm gate (COO for idle EIPs/stopped fetchers; the RUNNING quartz-si2-spike -> confirm intent first, likely the active SCHWABAUTO spike, do NOT touch without owner-confirm).</batch>
  </sequence>

  <acceptance_criteria>
    <criterion>terraform plan estate-wide = 0-diff (or documented-exempt); the ~210 UNMANAGED imported/adopted, the 15 DRIFTED resolved (config-only for the 5 replaces), state-integrity closed.</criterion>
    <criterion>NO live resource destroyed/replaced except explicit human-signed-off ops; every apply safe-apply-gated + deploy-ledger-closed.</criterion>
    <criterion>Firm-sep preserved. CVO EXERCISES 0-diff against LIVE (APPLIED==DESIRED, Rule 22a). CTO arch-gates each batch.</criterion>
  </acceptance_criteria>

  <references>
    <ref type="safety-model">infra/aws/NFRA_TERRAFORM_P2_remediation_safety_model.md (CTO arch-gate PASS, 603750209 + c70aeb817)</ref>
    <ref type="gap">infra/aws/NFRA_TERRAFORM_P1_coverage_matrix.md (7b4c484fe) + drift_results.tsv (6ca51a1c0)</ref>
    <ref type="prd">docs/architecture/NFRA_TERRAFORM_PRD.md</ref>
  </references>
</task_order>
```

<!-- ZOMBIE-RESOLVED 2026-07-13T08:04Z by 2.0.0_SA_COO.
     This TO was <status>pending</status> -- which means DISPATCHED -- while its assignee was
     NOT REGISTERED. Nobody was there. The board read it as ACTIVE work in flight.
     Flipped pending -> staged: `staged` is the TRUE state (scoped, awaiting a GO when a live
     lane exists). NOT flipped to complete -- THE WORK WAS NEVER DONE.
     Detector: .tools/to-liveness-join.py (e8ed4e1d2) -- the join /to-check and fabric-check
     never made. A dispatch into an unverified lane is a hope, not a drive. -->
