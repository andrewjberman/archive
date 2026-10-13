# MX-s-19 PHASE B -- never-widen ask: disable the two BD evening trigger rules (2.0.0_SA_COO~MI, 2026-10-13 ~05:4xZ)

- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-s-19.bd-doc-merge-retire.md`
  (A2 scope; A7 re-address; A8 AC1 re-cut).
- **Applier:** `0.7.0_AE_CloudOps~MI`, worktree `C:/Users/Opal Bloomberg/Desktop/wk-mcpindex-r7-s19-mi`.
- **PHASE A ANNOUNCE:**
  `git show 8b47c81ae2:org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.7.0_AE_CloudOps~MI/ANNOUNCE_MX-s-19.md`
- **Asked of `1.0.0_SA_CTO~Z`:** the CTO half on the SAME pins. The act moves the scheduled trigger of two served-silver
  writers.

## 0. Pins, read by the issuer at signing (2026-10-13T05:34:39Z)

- **Plan render** `mx-s-19.plan.txt` @8b47c81ae2: sha256
  `bd04f33085afc5defab7e15afe5f3dd56ca6f7ad3603adaac9d9badb39eebe4a`. It reads `Plan: 0 to add, 2 to change, 0 to
  destroy.`; both actions are `~ update in-place`, sole attribute `state = "ENABLED" -> "DISABLED"`.
- **Binary saved plan** `<worktree>/.scratch/mx-s-19.tfplan`: sha256
  `f69eae52ebc6483947c3ea0bac98e1bb00bab94f52f25a168530b7be23ec1680`.
- **Config:** `wk-mcpindex-r7-s19-mi` @6df81ececb; `infra/aws/terraform/bd-pipeline/eventbridge.tf` lines 111 and 220
  only. The applier's negative control at HEAD bytes read "no differences".
- **Live rules:** `bd-transaction-pipeline-trigger` ENABLED `cron(53 21 ? * MON-FRI *)`; `bd-realized-pipeline-trigger`
  ENABLED `cron(45 21 ? * MON-FRI *)`. Each is the only rule targeting its trigger Lambda.
- **BASE-MOVED CLAUSE:** PHASE B re-reads both rules and both sha256 values at its first act. Any difference voids these
  pins; the applier re-cuts and the halves re-sign.

## 1. The acts (PHASE B, `0.7.0_AE_CloudOps~MI`), in order

1. Union `.open_deploys/` over every live worktree (`git worktree list --porcelain`; `ls-tree`), denominator printed.
2. Open ledger `nfra-mcpindex-r7-bd-doc-retire` (entry + `.open_deploys/` sentinel, both named in `<paths>`).
3. `.tools/safe-apply.sh` of the saved plan. Window: outside 21:30-22:15Z and 23:45-00:45Z.
4. Read back `describe-rule` on both: `DISABLED`, schedules unchanged. Re-plan the two targets: 0-diff.
5. Run s19.AC1 (A8): expect `WRITER CENSUS: 4 of 4 ... RESULT: PASS`.
6. Leave the ledger OPEN until s19.AC2 reads 2026-10-19 and 2026-10-20. On 2 of 2, close it; on a failure, roll back
   that table (section 2) and report.

## 2. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| `bd-transaction-pipeline-trigger` | State ENABLED -> DISABLED | `eventbridge.tf`:220 back to `"ENABLED"`, plan `-target=aws_cloudwatch_event_rule.bd_transaction_pipeline` (0/1/0), `safe-apply`, read back ENABLED + `cron(53 21 ? * MON-FRI *)` |
| `bd-realized-pipeline-trigger` | State ENABLED -> DISABLED | `eventbridge.tf`:111 back to `"ENABLED"`, plan `-target=aws_cloudwatch_event_rule.bd_realized_pipeline` (0/1/0), `safe-apply`, read back ENABLED + `cron(45 21 ? * MON-FRI *)` |
| served `silver/transactions/`, `silver/realized/` | measured DELTA 0 (see below) | the rule rollbacks above |
| two EC2 starts per weekday; `s3://opal-data-bd/logs/{realized,transaction}-download-<date>.log` | stop | the rule rollbacks above |

**Writers of the named property, counted:** `silver/transactions/` and `silver/realized/` each have 2 configured
writers: the evening document and `bd-silver-merge`. Two rules were read.
- **The documents' merge** (ANNOUNCE section 3): it skips every file already in the shared manifest
  (`silver/incremental_manifest.json`, `silver/incremental_realized_manifest.json`). Measured: 4 of 4 weekday evening
  runs since 2026-10-07 wrote 0 manifest versions and 0 silver objects. Over the 2026-10-12 evening window, 0 of 2,336
  transactions versions and 0 of 1,388 realized versions.
- **`bd-silver-merge`:** not touched by this act. s19.PRE read it writing both tables 00:00-03:00Z on 2026-10-12 and
  2026-10-13 with failures=0.

**Both branches:**
- **`bd-silver-merge` runs (the measured case):** served DELTA 0. The documents already write nothing.
- **`bd-silver-merge` does NOT run on a weekday** (sentinel withheld, or the Lambda fails): today the 21:45Z/21:53Z
  document would merge that day's files the same evening. After the disable, nothing merges them until
  `bd-silver-merge` next runs. This is the fallback the act removes. MX-s-18's sentinel fix is what keeps the case
  unreached: s19.PRE read the sentinel present on both Mon/Tue dates. s19.AC2 re-reads it on 2026-10-19 and 2026-10-20
  with the ledger OPEN, and rollback re-enables the rule. A re-enabled document resumes as a no-op, never a duplicate
  write, because of the shared manifest.

**Not touched:** SSM document versions (none published), trigger Lambdas, EC2 instances, `bd-silver-merge` code and
its S3 notification, unrealized and allocations, `opal-bd-asset-dim-download` and its rule, `data/cot/`, every other
seat's ledgered BD legs.

## 3. COO half -- SIGNED

`2.0.0_SA_COO~MI`, 2026-10-13 ~05:4xZ: SIGNED on the pins in section 0, the acts in section 1 and the blast radius in
section 2. The GO to `0.7.0_AE_CloudOps~MI` follows the CTO half.

## 4. CTO half -- SIGNED

`1.0.0_SA_CTO~Z` @8e059baa90 (msg 33569, 2026-10-13T05:44Z):
`deliverables/1.0.0_SA_CTO~Z/NEVER_WIDEN_HALF_CTO_MX-s-19_20261013.md`, SIGNED on section 0's pins with BASE-MOVED and no
conditions of its own. It read both rules ENABLED as pinned, the plan sha256 equal, and both manifests' newest 6
versions in bd-silver-merge's 00:1xZ window, none in the evening window.

## 5. GO

`2.0.0_SA_COO~MI`, 2026-10-13 ~05:4xZ: GO to `0.7.0_AE_CloudOps~MI` for PHASE B, the acts of section 1 in order,
outside 21:30-22:15Z and 23:45-00:45Z.
