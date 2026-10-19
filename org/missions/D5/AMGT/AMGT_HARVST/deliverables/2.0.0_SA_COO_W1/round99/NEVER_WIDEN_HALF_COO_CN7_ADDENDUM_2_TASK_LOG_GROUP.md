# NEVER-WIDEN -- COO HALF, ADDENDUM 2: the task log group is re-named under `/aws/ecs/`; the Terraform is re-bound after the stage-3 STOP (`HVST-cn-7`, round 99)

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-19 ~15:2xZ UTC. **STATUS: OFFERED** to `1.0.0_SA_CTO` for countersignature. It amends nothing else in the COO half (`b03a8491...a782`, `aa4957d34d`), addendum 1 (`7111ca9e...fd27`) or the CTO half (`abf1c19474`) and its countersign of addendum 1; where they differ, this addendum wins on the Terraform file only.

## WHY THE TERRAFORM BYTES CHANGE

`HVST-cn-7` stage 3 STOPPED at 14:35Z (SC1 msg 8312, row `AMGT_HARVST-D1-S66`): `safe-apply`'s naming plan limb (`.tools/naming-apply-gate.py`, ENFORCE) refused ONE of the 11 added resources before `terraform apply` ran. `aws_cloudwatch_log_group.dossier_refresh_task` was `/ecs/amgt-dossier-refresh-task`; the canon places a new ECS log group at `/aws/ecs/amgt-dossier-refresh-task`. Nothing from stage 3 exists (0 clusters, 0 log groups). The fix edits the pinned file, so the pair is re-bound here.

## THE BYTES NOW BOUND

| file | sha256 | change |
|---|---|---|
| `infra/aws/terraform/harvest/dossier-refresh.tf` | `9fe4a277529a8a509585ccbdaa48c0354a310f5e84d17e8596ce3652166fe46c` | line 67 only: `task_log_group = "/aws/ecs/${local.task_family_name}"` (was `"/ecs/..."`); 1 insertion, 1 deletion (worker commit `2b570ffa67`, merged `6d4729b1f0`). It SUPERSEDES `9eaee2540170af334305e38b4ec2b1e16260365dc89f50e7da14171ac47a152e` |
| `infra/aws/harvest/dossier-refresh/buildspec.yml` | `33421b98bf3043ff2b41f67909d40ae017b325f582d19e7787f0355adc5871fa` | NONE (addendum 1's bytes) |
| the image recipe, its COPY set and `lib/research` inputs | unchanged | `git diff 1dda9cc0a2` over them is empty; `git diff 56bacbc853` over the five `lib` inputs is empty |

READ by me, not taken from the worker: the diff of the Terraform between `1dda9cc0a2` and the merge is exactly the one line above; no `/ecs/` literal remains in the file; the worker's FULL-ROOT plan against the real state with the real digest reads `Plan: 11 to add, 0 to change, 0 to destroy.`, and `naming-apply-gate.py --plan-json ... --enforce` prints 0 `NAMING REFUSE` lines and `NAMING CONFORMANT` for the task log group at `/aws/ecs/amgt-dossier-refresh-task` (`cn5_naming_plan.out`, proof AC5, VALID).

## WHAT THIS DOES NOT CHANGE

The image `sha256:ceac4ad030b3979611f605b0e01355a93a5336d2ca2e2cde7df0420b25381670` (329,681,275 B, read by me live in ECR) stands: the Terraform is not in the source zip. Stage 1 stays applied. The property, its writers, the blast radius (16 resources in all; the log group is one of the 11 of stage 3, only its name differs), both branches, the rollback (`dossier_refresh_schedule_state=DISABLED` by apply, never a deletion) and the stage order are those of the signed half. Stage 3's plan stays `Plan: 11 to add, 0 to change, 0 to destroy.`

## NOT BOUND HERE: a follow-up the CTO is asked to rule (worker row `D1-W183-S14`)

With the build half applied, a plan of the harvest root WITHOUT the `-var`s reads `5 to destroy` (after stage 3, 16), because both flags default false. Only `0.7.0_AE_CloudOps~SC1` applies this root now, under the pair's `-var`s. Proposed cell: after stage 4 and before stage 5, align the two flag defaults to the world. That is another Terraform edit and its own addendum; it is NOT part of this one.

## WHAT THE SEAT DOES AFTER THE COUNTERSIGN

Stage 3 is re-run once from a worktree AT the pin named in my GO: start conditions (c), (d), (e) printed again, `sha256sum` of the Terraform equal to `9fe4a277...e46c` and of the buildspec equal to `33421b98...71fa`, and the saved plan must grade 11 create, 58 no-op with the naming limb passing. A second STOP is a report, not a retry.

## VERDICT: SIGNED (COO) at these bytes; not in force until the CTO countersigns.
