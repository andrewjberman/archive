# NFRA_SCHWABBF -- Alongside Schwab Box build (release acts A1-A3, order TO-AL-r1): never-widen pair, COO half

**Issuer:** `2.0.0_SA_COO~SA` (laptop), 2026-10-20 ~17:3xZ. **Halves:** COO = this file (SIGNED below); CTO = `1.0.0_SA_CTO` (OWED).
**Pin:** `7ce88d5bdd9` on `box/laptop` (LOCAL; the CloudOps lane applies from the same laptop checkout, so push state does not gate the act; push state read at signing: `git ls-remote origin box/laptop` is behind the pin).
**Andrew-direct:** ~13:5xZ, "it should be exact same setup and logic as already exists with the 49 schwab box. this one should explicitly be labeled as an alongside box"; ~16:3xZ, "I want the new Cottonwood accounts taken care of".
**Order:** `task-orders/NFRA_SCHWABBF.TO-AL-r1.alongside-box-build-and-bootstrap.md` (staged; this pair is its GO).

## 1. The act and what it touches

Create a NEW Windows EC2 and its satellites from the new root `infra/aws/terraform/alongside-schwab-ec2/` (state key `alongside-schwab-ec2/tfstate`), upload four files to `s3://opal-data-assets/code/alongside-schwab-si2/`, run the bootstrap on the new instance, reboot it once.

| class | what | existing resource modified? |
|---|---|---|
| EC2 | 1 instance `schwab-alongside-si2-box-runner`, `t3.large`, default VPC subnet `subnet-039d04cfaee66a5f6`, IMDSv2 required, `prevent_destroy` | no (new) |
| Network | 1 security group, ZERO ingress, egress all | no (new) |
| IAM | 1 role, 1 profile, 1 inline policy, 1 SSM attachment; 1 events role + 1 inline policy | no (new) |
| Secrets | `schwab/alongside/ec2-credentials` created (metadata only); `schwab/alongside/sdd-credentials` IMPORTED (metadata only; `description`, tags ignored) | the import reads and records an existing secret, changes none of its fields |
| EventBridge | 4 rules (one per Cottonwood master) and 4 SSM targets, `State = DISABLED` | no (new) |
| S3 | 4 new objects under `code/alongside-schwab-si2/` | no (new prefix) |

**Does not touch:** the 49F Schwab Box `i-0f3d57a97f14727af`, `quartz-si2-spike-*`, `canonical-schwab-*`, the `schwab/sdd-credentials` and `schwab/sdd/session` secrets, any bronze/silver/gold key, any firm bucket, any other root's state. The role cannot read or delete data (write-only, code read only), cannot reach `opal-data-bd`, `opal-data-cot` or `opal-data-inf` (explicit Deny).

## 2. Writers of the property (counted at signing; N printed)

- Writers of the state key `alongside-schwab-ec2/tfstate`: 1 (the CloudOps lane through `safe-apply`). N = 1.
- Writers of `s3://opal-data-assets/code/alongside-schwab-si2/`: 1 (this order's step 7). N = 1.
- Writers of the Cottonwood bronze prefix `schwab/cottonwood/bronze/`: 0 today; after the box signs in and the rules are enabled, 1 (this box's role, per-master by file-name prefix; C-ONEWRITER). Not in this act.

## 3. Expected outcome, read from the Terraform root (both branches)

The measured read-only plan at the pin (`deliverables/2.0.0_SA_COO~SA/PLAN_READONLY_20261020_pin7ce88d5bdd9_MERGED.txt`, no apply, `-lock=false`): `Plan: 1 to import, 17 to add, 0 to change, 0 to destroy.` Two earlier plans of the same root found two defects (stale name table, import nulling a description) which cells then fixed; the plans are beside it (`..._BEFORE_FIX.txt`, `..._PLUS_AL-f1_FIX.txt`).
- **Branch A:** the CloudOps lane's own saved plan reads exactly that summary and `terraform show` lists no update, replace or delete. Proceed with the apply of that saved plan.
- **Branch B:** any other summary, any `update`/`replace`/`delete`, or a pre-check (order step 3) that finds a resource already present. Do not apply; report to the COO. The root is re-cut by the issuer.

## 4. Blast radius and rollback

- Blast radius: the 17 new resources and the one adopted secret record. No served output moves. A mistaken apply creates unused infrastructure: the instance costs money while running and holds no Schwab session; the rules are DISABLED so nothing fires; the security group admits nothing.
- **Rollback (stated plainly):** nothing is modified, so there is nothing to restore. Undoing the apply means DELETING new resources (instance, role, secrets), which is an irreversible-class act that waits for Andrew's confirmation (CLAUDE.md: deletes and EC2 stops take human confirmation); `prevent_destroy` on the instance and both secrets makes that deliberate. Until then the cheap containment is: leave the rules DISABLED and the instance idle.
- The code upload is additive to a new prefix; to undo, delete the four objects (Andrew's confirmation).

## 5. Conditions of this half

1. Apply only the CloudOps lane's saved plan from the pinned worktree at `7ce88d5bdd9`, through `safe-apply`, in the Alongside root only, no `-target`, no `-var`.
2. No rule is enabled by this act. No secret value is read or printed by this act; the bootstrap writes the generated Administrator password to its own secret and prints nothing.
3. Exactly one reboot of the new instance, before any Schwab session exists on it.
4. The act stops at "box ready for RDP". The sign-in (Andrew), the entitlement read, any pull and enabling the rules are separate acts under their own words.
5. The meta and `_ops` grants stay at master scope (decomposition ruling 6). PRD v0.9 C-TIERS moves Cottonwood meta and `_ops` to firm scope with the master in the file name; the role's two statements are re-pointed in a later round once the manifest file-name form is fixed. The first pull does not need them (the puller WARNs on a manifest-write denial).

## COO half -- SIGNED

`2.0.0_SA_COO~SA`, 2026-10-20, for the blast radius in section 1, both branches in section 3, the rollback statement in section 4 and conditions 1-5, on the pin `7ce88d5bdd9`.

## CTO half -- OWED (`1.0.0_SA_CTO`)
