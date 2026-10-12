# NEVER-WIDEN -- COO HALF: deploy the fenced `opal-research-pull-enqueue` handler (HVST-bx-2, round 80)

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-12 ~13:4xZ, on `1.0.0_SA_CTO~DELL1` msg 4215 and the record
`org/missions/D5/AMGT/AMGT_HARVST/ledger/CTO_RULING_R79_BS3_CARRIED_AND_ENQUEUE_FENCE_20261012.md` section 1. **Pairs with:**
`1.0.0_SA_CTO~DELL1`'s half (owed). **Actor:** `0.7.0_AE_CloudOps~HV1`, by order
`task-orders/AMGT_HARVST.TO-HVST-bx-2.the-fenced-enqueue-handler-deployed.md`.

## THE ACT (this box, once)

1. Build and upload `lambda_function.py` of the bx-1 merge commit `<M>` (`infra/aws/terraform/harvest/build-and-upload.sh`).
2. Terraform plan targeted at `module.harvest_enqueue` in `infra/aws/terraform/harvest`; read it; apply once with `safe-apply`.
3. Three side-effect-free invocations of the deployed function (no payload carries a ticker).

## THE PIN

The code is whatever commit `<M>` the issuer names in AMENDMENT 1 to the order: the merge of `HVST-bx-1` (the handler's tier fence
and its unit tests), built and merged by `safe-merge.sh` after its proof reads VALID. The deployed bytes must equal
`git show <M>:infra/aws/lambda/research/pull_enqueue/lambda_function.py`; the seat prints both sha256 values.

## BLAST RADIUS

- The function's code, once. Its IAM role, the API Gateway route, the authorizer, the SQS queue and the research bucket are not
  touched. The deployed behaviour changes for exactly one population: a caller whose authorizer context is not `tier == internal`
  (or has no context) now gets a 403 where it got a 202 and a real enqueue before.
- **Who loses access:** any non-internal login that today reaches `POST /api/private/research/pull`. That is the point of the
  ruling. The internal analyst page is unaffected if the authorizer passes `tier: internal` for internal logins; the order's
  third arm proves the handler admits that shape, and does NOT prove the authorizer emits it (read at the act: C-d).
- Silver writers, gold, the harvest runner, the box consumer and Bloomberg are not touched.

## CONDITIONS (each checked at the act, not assumed)

- **C-a.** The deployed bytes' source equals `<M>`'s file (sha256 printed, with a positive control: the pre-change file's hash differs).
- **C-b.** The plan reads `Plan: 0 to add, 1 to change, 0 to destroy`, the one change being the function's code hash. Anything else:
  STOP, apply nothing.
- **C-c.** No arm invocation carries a `ticker`. A real ticker would write a status object and enqueue a Bloomberg pull.
- **C-d.** Before the apply, the seat reads how the portal authorizer sets `tier` for an internal login (the authorizer's source or
  its served context) and records the field's path. If the authorizer emits it somewhere the handler does not read, the apply is
  not done and the issuer is told by a row: the fence would then lock the internal page out.
- **C-e.** A ledger entry is opened before the upload and closed after the arms.

## ROLLBACK

Rebuild and upload the pre-change file (`git show <M>~1:...`), apply the same targeted plan once, read `CODESHA256` equal to the
value in `bx2_before.out`.

## VERDICT: SIGNED (COO), pending `1.0.0_SA_CTO~DELL1`'s half
