# HVST-co-6 -- DRAFT (NOT an order; staged by 2.0.0_SA_COO~W1, 2026-10-20 ~18:5xZ)

**Status:** staged inputs for the packaging cell of the gold rebuild. It is NOT cut and sits outside `task-orders/`, so no gate reads it. It is cut when (a) `HVST-co-5` is merged (its measured wall time, peak memory and driver closure are the cell's inputs) and (b) the host call `dell1-20261020T184002Z-3d0c` is ruled. This file is the FARGATE branch (my recommendation); a Lambda ruling replaces it with a split-build cell, which is larger and is not drafted.

## What the cell would be

Author and PLAN (not apply) the gold rebuild's container task on Fargate, on the `HVST-cn-5` pattern: a new Terraform file `infra/aws/terraform/harvest/gold-refresh.tf`, its image recipe `infra/aws/harvest/gold-refresh/{Dockerfile,buildspec.yml,build-image.sh}` and a names check, the schedule written `DISABLED` and the flags defaulting to the applied world once applied. Workstream `GOLD-PACKAGE` (the L6 gate keys one issuer to workstream and round). Class WORLD (`infra/` floor); applies nothing.

## The reuse map (read by me from `infra/aws/terraform/harvest/dossier-refresh.tf`, 541 lines, at HEAD; not exercised)

| piece in `dossier-refresh.tf` | gold rebuild |
|---|---|
| `aws_ecs_cluster.dossier_refresh` (`amgt-dossier-refresh-cluster`), `aws_security_group.dossier_refresh` | REUSE by reference or a second cluster: a decision for the cell's face, not a default (a shared cluster couples two producers' lifecycles; no data crosses). |
| the VPC and subnet literals (`vpc-0cc0c6a75e54605e3`, `subnet-023db8cbfd99ffff2`, public IP, no NAT) | REUSE the same literals. |
| ECR repository, CodeBuild project, build role and policy, build log group | NEW, own names: the image recipe differs (the dossier image COPYs only what the dossier driver reads). |
| task role and policy: reads the harvest bucket, writes ONLY `amgt/harvest/gold/research_dossier/*` | NEW role, scoped to the THREE gold prefixes only (`article_security_mention/`, `chatter_daily/`, `chatter_event/`) for `s3:PutObject`; read `ListBucket` and `GetObject` on the harvest bucket. `write_gold` does one conditional `PutObject` (`IfNoneMatch="*"`) and one `head_object` read-back, so no `DeleteObject`, no `PutObjectAcl`. |
| task definition by DIGEST, `cpu 1024 / memory 4096`, entryPoint `python -m <module>`, `command` with `--write --require-trading-day` | NEW family; cpu and memory sized from `co-5`'s measured `peak_rss_mb` (not guessed); entryPoint `python -m lib.research.harvest.gold_refresh`, command `--write --require-trading-day`. |
| scheduler role and policy, `aws_scheduler_schedule` (`cron(0 10 ? * MON-FRI *)` America/New_York, `DISABLED` first) | NEW, own clock. Recommendation for the CTO's pair: a morning slot before the dossier fire (for example 06:00 America/New_York), because the gold `as_of` is the LAST COMPLETED trading day, so no upstream landing is waited for and the two producers do not overlap. The clock is the pair's to rule. |
| `precondition` that the digest is non-empty before the run half plans | COPY. |

## What `co-5` must have measured first (the cell reads these, it does not guess them)

`GOLD-CENSUS wall_seconds` over all three tables, `peak_rss_mb`, `gets`/`bytes_read`, the driver's closure (207.34 MB, read), and the per-table wall (mention 2715.1 s, read from the uncommitted output). The task size and the CodeBuild image build time come from those.

## Names

Every new resource name is `opal_naming` `name()` output (rule 30): the registry rows to add (`infra/logic/registry/`) are part of the cell, as `cn5_names.py` did for the twelve dossier names (`NAMES-CHECK terraform_literals=12 builder_match=12 mismatches=0`, negative control fires). A builder REFUSAL is a missing registry row to add, never a hand-typed name.

## Open items I could not settle from files

- Whether the gold task's `as_of` default (the last completed trading day) is the CTO's intent for "the trading-day-current `chatter_daily` partition": the previous builds wrote `date=2026-10-08` on 2026-10-09T10:34Z, which is T-1; the pair confirms.
- Whether `chatter_daily` and `chatter_event` should be rebuilt on every fire or only when the mention snapshot changed: the driver builds all three each run (a full snapshot each), which is add-only but multiplies objects daily.
- The deliberate run (`co-7`) writes real objects: its pair names the three tables, the prefix, the key shape and that nothing is deleted.
