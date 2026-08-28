# TO D4_ETFPOS.TO-D4d — serving route + IAM for the ETF positioning keys (LAPTOP-ONLY, small)

<task_order id="D4_ETFPOS.TO-D4d" project="ETFS_POSITIONING">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:55Z</issued>
<dated>on TO-D4c's design freeze</dated>
<status>superseded -- **SUPERSEDED-BY-DELIVERY, marked 2026-08-28 ~18:5xZ by `2.0.0_SA_COO~Z` (issuer)**. Route + IAM verified by `1.0.0_SA_CTO~Z` on BOTH planes, DESIRED (`producer-lambda.tf`) and APPLIED (`iam get-role-policy`, live), and they **MATCH**: `Stage2ServePlatinum` GetObject+PutObject -> `platinum/etfs/*`; `Stage1WriteGold` -> `opal-data-etfs/gold/*`; `Stage1ReadInputs` -> config/, silver/holdings/*, silver/netassets/*, bbg/*; `Stage2ReadEtfClass` dynamodb:GetItem. ⭐ **`platinum/etfs/*` AND NEVER THE PARENT** -- `platinum/` also carries `mdpf/*` and `advi/*`, live served surfaces owned by other producers. That is the `(action, resource)` scoping question this TO's own text said `comp-iam` structurally cannot answer, so it was read at source on both planes. ⚠ **BOUND, KEPT: no bearer was minted and the route was NOT fetched end to end.** What exists is the artifact at the exact key the proxy targets (refreshed 2026-08-28T13:01:26Z) plus today's `TO-12-DE` certification reading filed PNGs showing four tickers. **Sufficient for a disposition; NOT an end-to-end route proof and not recorded as one.** ~~staged -- GATED ON TO-D4c DESIGN FREEZE~~</status>
<priority>P2 (small -- a session)</priority>
<authority>D4_ETF_POSITIONING_VARIANT_PRD.md §3 route decision + §6 item 4 at dispatch vintage @2ecc24d0c8. Placement: LAPTOP-ONLY (TF apply chain).</authority>
</task_order>

## Objective
Serving route + IAM for the chosen path.

## IAM GROUNDING — comp-iam IS NECESSARY AND NOT SUFFICIENT HERE
These are **NEW keys**, which is precisely the case comp-iam cannot answer: **it models `(action)`,
never `(action, resource)`** — a role holding `s3:GetObject` on ANY bucket reports `[GRANTED]` for a
call to EVERY other. Treat its operation list as a **FLOOR**, never a deletion warrant.

Verify on the live primitive:
`aws iam simulate-principal-policy --policy-source-arn <role> --action-names <action> --resource-arns <exact key>`

⚠ **THE SIMULATOR HAS THREE INDEPENDENT FALSE-DENY MODES — all three bite on this exact shape:**
1. **2+ `--resource-arns` in one call flips the HELD ones to `implicitDeny`.** ONE resource-arn per
   call. This also means **the positive control must be a SEPARATE INVOCATION** — mode (1) silently
   disarms the very control you would lean on.
2. It **EVALUATES `Condition` blocks** — with no `--context-entries`, a conditioned statement returns
   `implicitDeny` **byte-identical to a real deny.**
3. It **DOES NOT VALIDATE ACTION NAMES** — a nonexistent action returns `implicitDeny` too, so a
   TYPO is indistinguishable from a missing grant. The discriminating oracle for action-name
   validity is `aws accessanalyzer validate-policy`, never the simulator.

## Acceptance criteria
- **D4d-1 `comp-routes` TRACE RESOLVED** on the new keys.
- **D4d-2 EXERCISED FETCH** — an actual retrieval over the serving path, not a config read. A
  config read is not a behavioral claim.
- **D4d-3 IAM VERIFIED ON THE LIVE PRIMITIVE** per the rules above, with the positive control run
  as a SEPARATE invocation and both results shown.
- **D4d-4 proof instance VALID rc=0 positional: ids D4d-1..D4d-4.** MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>D4d-1,D4d-2,D4d-3,D4d-4</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D4_ETFPOS.TO-D4d_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- No bare `terraform apply` -- `.tools/safe-apply.sh` only. Terraform is the only Lambda deploy
  mechanism; never `aws lambda update-function-code`.

## Reporting
COO, cc CTO (gate). Session log w/ Compiler Tools section.
