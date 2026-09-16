# EN-t-3 round 2 -- result

**Task order:** `org/missions/D14/LGIC/LGIC_ENFORCE/task-orders/LGIC_ENFORCE.TO-EN-t-3-r2.roots-census.md`
**Worker:** `0.9.0_WK_LGIC_ENFORCE~3`, branch `wk-lgic-enforce-2d-3`, base `CLOUD`@`62c701411e`.
**Status:** the order stays **OPEN**. `T3R-AC2` is FAIL by output; `<status>` was NOT flipped.

## What landed

| path | commit |
| --- | --- |
| `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/LIMB_ROOTS_CENSUS.md` | `c613781701` |
| `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/roots/` (68 extracts) | `c613781701` |
| `org/missions/D14/LGIC/LGIC_ENFORCE/surprise-channel/investigations/INVESTIGATION_v1.md` (2 rows) | `c613781701` |

All 72 backend roots under `infra/aws/terraform/` were init'd and planned ONE AT A TIME with terraform
v1.9.8, `plan -lock=false -input=false -out=<abs scratch>` then `show -json`, each root's `.terraform`
(686 MB measured) deleted and its removal verified before the next init (`dotdir_removed` TRUE 72 of 72).
Free space 18.32 GB at the start, 12.07 GB at the end, re-measured before every tenth root (8 readings,
lowest 12.96 GB): the order's 10 GB stop line was never reached.

**Nothing was applied.** No state was written, `org/mcp/naming-gate.enforce` was never created, and
enforcement was `--enforce` per invocation. `G-F`'s flip is not this cell's.

## The five criteria

| id | verdict | deciding line | denominator |
| --- | --- | --- | --- |
| `T3R-AC1` | **PASS** | `VERDICT: PASS-PREPLAN-REFUSES-NONE` (rc=0) | 77 of 77 Terraform directories; 0 refused or failed |
| `T3R-AC2` | **FAIL** | `VERDICT: FAIL-ROOT-NOT-PLANNED` (rc=1) | 72 of 72 roots recorded; 68 planned, 4 NOT planned |
| `T3R-AC3` | **PASS** | `VERDICT: PASS-ZERO-EXISTING-REFUSED` (rc=0) | 2431 resource changes; 0 refusals of a resource neither created nor renamed; 0 limb errors |
| `T3R-AC4` | **PASS** | `VERDICT: PASS-ADDITIONS-DISCLOSED` (rc=0) | 34 of 34 creates and renames listed |
| `T3R-J1` | **RECORDED** (judgment) | no self-verdict; `3.0.0_SA_CVO` grades it at L9 | 68 of 72 roots carry an extract and a `plan_sha256` |

The CTO's round-1 analysis s.2 RULING ADD reads **ZERO** on the roots that could be planned: across 2431
resource changes in 68 roots the enforcing plan limb printed 1590 `NAMING` lines (198 CONFORMANT, 9
NOT-GRADED, 1367 WARN, 16 REFUSE) and refused **nothing** that was neither created nor renamed. All 16
REFUSE lines sit on pending CREATES, listed by root and address in the census section 5.

## Why the order stays open

`T3R-AC2` requires every backend root planned. Four cannot render a plan on this box, and no repair for
any of them lies inside this order's `<paths>`:

| root | terraform rc=1 reason | why this worker cannot fix it |
| --- | --- | --- |
| `nfra-agentbus-port2` | `max_message_size` 1048576, outside the provider's 1024-262144 range (both queues, `sqs.tf:31` and `:46`) | an edit under `infra/aws/terraform/`, not granted |
| `seeking-alpha` | `module "news_dedup"` missing required `artifact_key`, passing an undeclared `source_dir` (`main.tf:168-171`) | an edit under `infra/aws/terraform/`, not granted |
| `harvest` | `filebase64sha256` cannot open `./.build/chatter-axis-producer.zip` | gitignored (`*.zip`) and absent from the MAIN checkout too; its builder `lambda_src/build_zip.py:225` runs `pip download` -- egress off Opal infrastructure |
| `trade-pipeline` | root variable `jwt_secret` has no value | carried by the gitignored `secrets.auto.tfvars`, present only in the main checkout; a fabricated value would not be the root's real plan |

The order's own THE CELL item 1 prescribes recording exactly such a root NOT planned with its reason,
which the census does for all four. `T3R-AC2` refuses that same state. That contradiction is row
`LGIC_ENFORCE-W3-S12` and is the recut's to resolve.

## Rows filed

- **`LGIC_ENFORCE-W3-S12`** (BLOCKING, INERT) -- the four unplannable roots, and item 1 versus `T3R-AC2`.
- **`LGIC_ENFORCE-W3-S13`** (OBSERVATION, INERT) -- `terraform init` rewrote the TRACKED
  `.terraform.lock.hcl` on 2 of the 72 roots (`market-overview`, `seeking-alpha`: the `archive` provider
  pruned), a write outside `<paths>` produced by an invocation the order prescribes. Both files are left
  MODIFIED AND UNSTAGED in this worktree, so neither reaches the branch the COO drains.

## What is NOT claimed

- The plans are **live reads**. A re-plan after AWS state moves will not reproduce a root's `plan_sha256`;
  hash disagreement is not by itself extract disagreement.
- `T3R-AC3`'s refusal arm **cannot be falsified by a well-formed extract**: `naming-apply-gate.py` caps a
  non-addition at WARN in `judge_capped()` while `check_en_r2.py`'s `_addition()` reads the same
  before/after own-name attribute, so the two rules agree by construction. The mutant control therefore
  targets that criterion's vacuity guard (the `and changes` clause) instead, and says so.
- Nothing is claimed about the 4 unplanned roots' names AT PLAN TIME. They were graded only by the
  pre-plan limb, which never refuses.
- The order's context numbers (78 directories, 73 roots) do not match the live tree (77, 72). The
  difference is `infra/aws/terraform/amgt-resapp`, removed by `ea6cd450fa` between the decomp vintage
  `8e0d09e418` and this worker's base. Every criterion enumerates from `git ls-files` at HEAD.
