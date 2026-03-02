# Terraform Pipeline Strategy — Opal Capital AWS Infrastructure

**For:** All agents (DevOps, AWS Engineer, Systems Architect)
**Reference Implementation:** `infra/aws/terraform/smartx-pipeline/`
**Last Updated:** 2026-02-23

---

## Pipeline Maturity Matrix

Check this table before starting work on any pipeline. Update it after completing each milestone.

| Pipeline | Terraform | Structure | S3 Backend | EventBridge | IAM | EC2 | CI/CD Mapped | Git Tag |
|----------|-----------|-----------|------------|-------------|-----|-----|--------------|---------|
| **BD Pipeline** | Full | 2 files (main + stage4-ec2) | YES | Via Step Functions | Inline in main.tf | Yes | Yes | None (pending gold layer decision) |
| **SmartX** | Full | Canonical 7-file split | YES | Yes (separate file) | Yes (separate iam.tf) | Yes | Yes | `smartx-v1.0.0` |
| **Seeking Alpha** | Partial | Single main.tf (368 lines) | NO | Yes (inline) | Yes (inline) | No | Yes | None |
| **Yang** | Full | Canonical 6-file split | YES | No (S3-triggered) | Yes (separate iam.tf) | No EC2 | Yes | `yang-v1.0.0` |
| **Portfolio** | Partial | Single main.tf | NO | No | No | No | Yes | None |
| **Causality** | Minimal | Single main.tf | NO | No | No | No | Partial | None |
| **News** | Full | Canonical 7-file split | YES | Yes (separate file) | Yes (separate iam.tf) | No EC2 | Yes | `news-v1.0.0` |
| **Other/Misc** | Catch-all | Single main.tf | NO | No | No | No | Partial | None |

**Target state for every pipeline:** Full Terraform, canonical file split, S3 backend, all resource types managed, CI/CD mapped, git tagged.

---

## 1. Canonical Module Structure

Every pipeline MUST follow this layout:

```
infra/aws/terraform/{pipeline-name}/
  main.tf              # Provider + S3 backend + default_tags + locals
  lambdas.tf           # All Lambda functions (yang-lambda module or direct)
  eventbridge.tf       # Schedule rules + targets + permissions
  iam.tf               # All IAM roles + inline policies
  ec2.tf               # EC2 instances (only if pipeline has them)
  outputs.tf           # ARNs/IDs for cross-reference
  variables.tf         # Input variables (instance IDs, role names with date suffixes)
  IMPORT_COMMANDS.sh   # One-time import script (kept as documentation)
```

Pipelines without EC2 or EventBridge simply omit those files. Never cram everything into `main.tf`.

### Standardized main.tf Skeleton

Every pipeline gets this boilerplate:

```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "opal-313476888478-terraform-state"
    key    = "{pipeline-name}/tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      Project     = "OpalPortal"
      ManagedBy   = "Terraform"
      Environment = "Production"
      System      = "{PipelineName}"  # e.g., "BDPipeline", "SmartXPipeline"
    }
  }
}

locals {
  account_id = "313476888478"
  region     = "us-east-1"
}
```

### When to Use the yang-lambda Module vs Raw Resources

| Scenario | Use | Example |
|----------|-----|---------|
| Standard zip-packaged Python Lambda | `module "name" { source = "../modules/yang-lambda" }` | 95% of Lambdas |
| Container image Lambda (`package_type = "Image"`) | Raw `aws_lambda_function` resource | bd-price-update |
| CI/CD-managed code (needs `ignore_changes`) | Raw `aws_lambda_function` with lifecycle block | smartx ingestion pipeline |
| Non-Lambda resources (IAM, EventBridge, Step Functions, DynamoDB, EC2) | Always raw resources | Too varied to modularize |

### Resource Tagging Standard

Every resource gets these tags via `default_tags` on the provider:
- `Project = "OpalPortal"`
- `ManagedBy = "Terraform"`
- `Environment = "Production"`
- `System = "{PipelineName}"` (e.g., `"BDPipeline"`, `"SmartXPipeline"`, `"YangPipeline"`)

Individual resources add a `Name` tag and optionally `Stage` (e.g., `"trigger"`, `"ingestion"`).

---

## 2. Bringing a Pipeline Under Management — Agent Checklist

Follow these phases in order. Do not skip steps.

### Phase 1: Reconnaissance

Inventory every AWS resource belonging to the pipeline.

```bash
# List all Lambdas with a given prefix
aws lambda list-functions \
  --query "Functions[?starts_with(FunctionName, '{prefix}')].{Name:FunctionName,Runtime:Runtime,Role:Role}" \
  --output table

# For each Lambda, capture full configuration
aws lambda get-function-configuration --function-name {name} \
  --query '{Handler:Handler,Runtime:Runtime,Timeout:Timeout,MemorySize:MemorySize,Role:Role,Environment:Environment,Layers:Layers[*].Arn}' \
  --output json

# List IAM roles related to the pipeline
aws iam list-roles --query "Roles[?contains(RoleName, '{prefix}')].RoleName" --output text

# For each role, list inline policies
aws iam list-role-policies --role-name {role-name} --output text

# Get each inline policy document
aws iam get-role-policy --role-name {role-name} --policy-name {policy-name} \
  --query 'PolicyDocument' --output json

# List attached managed policies
aws iam list-attached-role-policies --role-name {role-name} --output text

# List EventBridge rules
aws events list-rules --query "Rules[?contains(Name, '{prefix}')].{Name:Name,Schedule:ScheduleExpression,State:State}" --output table

# Get EventBridge rule targets
aws events list-targets-by-rule --rule {rule-name} --output json

# Get Lambda resource policy (for Lambda permissions)
aws lambda get-policy --function-name {name} --output json

# EC2 instances
aws ec2 describe-instances --filters "Name=tag:Name,Values={name}" \
  --query 'Reservations[*].Instances[*].{ID:InstanceId,Type:InstanceType,State:State.Name}' --output table

# ECR repositories
aws ecr describe-repositories --query "repositories[?contains(repositoryName, '{prefix}')]" --output table

# DynamoDB tables
aws dynamodb describe-table --table-name {name} --output json

# Step Functions state machines
aws stepfunctions list-state-machines --query "stateMachines[?contains(name, '{prefix}')]" --output table
```

### Phase 2: Write Terraform Files

1. Create directory: `infra/aws/terraform/{pipeline-name}/`
2. Write `main.tf` using the skeleton above — set the S3 backend key and System tag
3. Write Lambda resources in `lambdas.tf`:
   - Use `yang-lambda` module for standard Lambdas (pass `source_dir`, `function_name`, `role_arn`, etc.)
   - Use raw resource for container-image or CI/CD-managed Lambdas
4. Write IAM roles + policies in `iam.tf` — match EXACT policy documents from AWS (use the `get-role-policy` output)
5. Write EventBridge rules + targets in `eventbridge.tf`
6. Write EC2, DynamoDB, Step Functions as needed
7. Write `variables.tf` for hardcoded values (instance IDs, role names with date suffixes from `name_prefix`)
8. Write `outputs.tf` exporting key ARNs and identifiers

**Critical rule:** Match AWS state exactly. Do not "improve" policies or change names during import. Get to 0-diff first, then refactor.

### Phase 3: Initialize + Import

```bash
cd infra/aws/terraform/{pipeline-name}/
terraform init
```

Write `IMPORT_COMMANDS.sh` with every import command. Then run them one at a time.

**Import Command Reference:**

```bash
# Lambda function
terraform import aws_lambda_function.NAME function-name

# Lambda via yang-lambda module
terraform import module.NAME.aws_lambda_function.this function-name
terraform import module.NAME.aws_cloudwatch_log_group.lambda /aws/lambda/function-name

# IAM role
terraform import aws_iam_role.NAME role-name

# IAM inline policy (format: role-name:policy-name)
terraform import aws_iam_role_policy.NAME "role-name:policy-name"

# IAM managed policy attachment (format: role-name/policy-arn)
terraform import aws_iam_role_policy_attachment.NAME "role-name/arn:aws:iam::aws:policy/PolicyName"

# IAM instance profile
terraform import aws_iam_instance_profile.NAME profile-name

# EventBridge rule
terraform import aws_cloudwatch_event_rule.NAME rule-name

# EventBridge target (format: rule-name/target-id)
terraform import 'aws_cloudwatch_event_target.NAME' rule-name/target-id

# Lambda permission (format: function-name/statement-id)
terraform import aws_lambda_permission.NAME function-name/statement-id

# EC2 instance
terraform import aws_instance.NAME i-xxxxxxxxxxxx

# ECR repository
terraform import aws_ecr_repository.NAME repo-name

# DynamoDB table
terraform import aws_dynamodb_table.NAME table-name

# CloudWatch log group
terraform import aws_cloudwatch_log_group.NAME /aws/lambda/function-name

# Step Functions state machine
terraform import aws_sfn_state_machine.NAME arn:aws:states:us-east-1:313476888478:stateMachine:machine-name
```

**Git Bash gotcha:** Paths starting with `/` get mangled by MSYS. Prefix the command:
```bash
MSYS_NO_PATHCONV=1 terraform import aws_cloudwatch_log_group.NAME /aws/lambda/function-name
```

### Phase 4: Reconcile to 0-Diff

```bash
terraform plan -no-color 2>&1 | tee plan-output.txt
```

For each diff in the plan output:

| Diff Type | Action |
|-----------|--------|
| **Tag additions** (ManagedBy, System, etc.) | Expected on first apply. These are safe. |
| **Configuration mismatch** (wrong timeout, memory, handler) | Fix the `.tf` file to match AWS exactly |
| **Code hash diff** on CI/CD-managed Lambda | Add `lifecycle { ignore_changes = [filename, source_code_hash] }` |
| **Resource not found** during import | Verify resource name with AWS CLI, fix import command |
| **Policy document diff** | Re-query the policy from AWS and paste the exact JSON |
| **Description diff** | Add `description` attribute to match AWS |

Iterate until `terraform plan` shows only tag additions or "No changes."

Then apply:
```bash
terraform apply
terraform plan  # MUST show "No changes. Your infrastructure matches the configuration."
```

### Phase 5: Finalize

1. Add pipeline Lambdas to `infra/aws/lambda/LAMBDA_MANIFEST.json` with `terraform_managed: true`
2. Optionally add Lambdas to `infra/aws/lambda/ci/lambda-source-map.json` for drift detection coverage
3. Commit all changes to DEV
4. Create git tag:
   ```bash
   git tag -a {pipeline}-v1.0.0 -m "{Pipeline}: initial Terraform import, all N resources reconciled"
   git push origin {pipeline}-v1.0.0
   ```
5. Update the Pipeline Maturity Matrix in this document

---

## 3. Deployment Model

### Terraform Owns Everything — Config AND Code

All Lambda code deployment goes through `terraform apply`. There is no separate CI/CD code deployment.

**The flow:**
```
Edit code → git commit → git push origin DEV → (drift check runs automatically)
                                               → when ready: terraform apply → code deploys to AWS
                                               → terraform plan (verify 0-diff) → git tag
```

Pushing to DEV does NOT deploy code. It triggers the `lambda-drift-check.yml` workflow which reports whether local code differs from what's in AWS. Deployment is intentional — you run `terraform apply` when you're ready.

### How Code Gets Packaged

The `archive_file` data source (in the yang-lambda module or inline) zips the local source directory. When `terraform apply` runs, it detects the hash change and deploys the new zip to AWS.

```hcl
# yang-lambda module (standard pattern — 69 Lambdas)
data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = var.source_dir
  output_path = "${path.module}/builds/${var.function_name}.zip"
  excludes    = ["__pycache__", "*.pyc", ".git"]
}

# Inline pattern (for multi-file Lambdas not using the module)
data "archive_file" "ingestion_pipeline" {
  type        = "zip"
  source_dir  = "${path.module}/../../lambda/smartx_ingestion_pipeline"
  output_path = "${path.module}/code/opal-smartx-ingestion-pipeline.zip"
  excludes    = ["__pycache__", "*.pyc", "deploy.sh", "*.md"]
}
```

### The Source Map (Drift Detection)

`infra/aws/lambda/ci/lambda-source-map.json` maps each Lambda to its source directory. Used by the drift-check workflow to detect when code has been committed but not yet deployed via `terraform apply`.

### Adding a New Lambda

1. Add the Lambda to the pipeline's `lambdas.tf` (use yang-lambda module or inline `archive_file`)
2. Add entry to `LAMBDA_MANIFEST.json` with `terraform_managed: true`
3. Optionally add to `lambda-source-map.json` for drift detection coverage
4. Run `terraform apply` to create/deploy
5. Verify with `terraform plan` — must show "No changes"

### Lifecycle Rules Reference

| Rule | When to Use | Example |
|------|-------------|---------|
| `ignore_changes = [ami, user_data, key_name, security_groups]` | Imported EC2 instance — only manage tags/config | smartx EC2 exporter |

**Note:** `ignore_changes` on `filename` or `source_code_hash` is NOT used. Terraform manages all code. The yang-lambda module's `ignore_changes = [last_modified]` only prevents timestamp noise.

---

## 4. Git Tagging Protocol

### Tag Format

```
{pipeline}-v{MAJOR}.{MINOR}.{PATCH}
```

Pipeline names match the directory name under `infra/aws/terraform/`:

```
smartx-v1.0.0
bd-v1.0.0
yang-v1.0.0
seeking-alpha-v1.0.0
portfolio-v1.0.0
causality-v1.0.0
```

### Version Bump Rules

| Bump | When | Example |
|------|------|---------|
| **major** | Breaking infra change, resource replacement, backend migration | `v1.0.0 -> v2.0.0` |
| **minor** | New resource added, new feature, non-breaking config change | `v1.0.0 -> v1.1.0` |
| **patch** | Bug fix, tag update, policy tweak, config correction | `v1.1.0 -> v1.1.1` |

### When to Tag

- After a `terraform apply` that reaches 0-diff plan (mandatory)
- After adding new resources to an existing pipeline
- After any commit that changes live AWS state
- **v1.0.0** specifically: when a pipeline first achieves full Terraform management with S3 backend

### Commands

```bash
# Create an annotated tag
git tag -a {pipeline}-v{X.Y.Z} -m "{Pipeline}: brief description"
git push origin {pipeline}-v{X.Y.Z}

# List tags for a pipeline
git tag -l "{pipeline}-v*"

# See what changed since a tag
git diff {pipeline}-v1.0.0..HEAD -- infra/aws/terraform/{pipeline-name}/

# Compare two tags
git diff {pipeline}-v1.0.0..{pipeline}-v1.1.0 -- infra/aws/terraform/{pipeline-name}/
```

### Rules

- Tags are created on DEV after verification, never on unverified commits
- Tags are immutable — never delete or move a tag
- Every tag message should summarize what changed and what was verified
- When merging DEV to main, tags carry forward automatically

---

## 5. Rollback Procedures

### Tier 1: Git Revert + Terraform Apply (Preferred)

For infrastructure changes that broke something:

```bash
# Identify the bad commit
git log --oneline infra/aws/terraform/{pipeline-name}/

# Revert it
git revert {bad-commit-sha}

# Apply the reverted state
cd infra/aws/terraform/{pipeline-name}/
terraform plan    # Preview what will change
terraform apply   # Roll back infrastructure

# Verify
terraform plan    # Must show "No changes"
```

This works because Terraform state is in S3 (versioned). The revert changes the `.tf` files back, and `terraform apply` reconciles AWS to match.

### Tier 2: S3 State Version Restore (Emergency)

If Terraform state itself is corrupted:

```bash
# List state versions
aws s3api list-object-versions \
  --bucket opal-313476888478-terraform-state \
  --prefix {pipeline-name}/tfstate \
  --query 'Versions[*].{VersionId:VersionId,LastModified:LastModified,Size:Size}' \
  --output table

# Download a known-good version
aws s3api get-object \
  --bucket opal-313476888478-terraform-state \
  --key {pipeline-name}/tfstate \
  --version-id {good-version-id} \
  terraform.tfstate.restored

# Replace remote state (CONFIRM WITH USER BEFORE DOING THIS)
aws s3 cp terraform.tfstate.restored \
  s3://opal-313476888478-terraform-state/{pipeline-name}/tfstate
```

### Code Rollback (CI/CD-Managed Lambdas)

```bash
# Option A: Redeploy old code via git (triggers CI/CD)
git checkout {good-commit} -- infra/aws/lambda/{function-source-dir}/
git commit -m "fix: Roll back {function} to {good-commit}"
git push origin DEV

# Option B: Direct AWS rollback (fastest, no CI needed)
# Use backup from pre-terraform migration
aws lambda update-function-code \
  --function-name {function-name} \
  --zip-file fileb://path/to/backup.zip
```

### Rollback Decision Tree

| Failure | Action |
|---------|--------|
| Single Lambda code broken | Option B (direct AWS rollback), then fix code in git |
| Single Lambda config broken (timeout, memory, etc.) | `git revert` the TF commit + `terraform apply` |
| Multiple resources broken by a terraform apply | `git revert` + `terraform apply` |
| Terraform state corrupted | S3 state version restore (Tier 2) |
| Everything broken | See `infra/aws/terraform/ROLLBACK_PROCEDURE.md` |

---

## 6. Pipeline Priority Order

Recommended execution order for bringing remaining pipelines to full management:

### Priority 1: BD Pipeline (S3 backend migration)

Most complex pipeline (25+ Lambdas, Step Functions, EventBridge, EC2). Already has full Terraform but uses LOCAL state. Needs:
- Add `backend "s3"` block with key `bd-pipeline/tfstate`
- Run `terraform init -migrate-state` to move local state to S3
- Split `main.tf` into canonical file structure (lambdas.tf, iam.tf, eventbridge.tf)
- Verify 0-diff plan
- Tag `bd-v1.0.0`

### Priority 2: Yang Pipeline

20+ Lambdas already in Terraform via modules. Has commented-out S3 backend with WRONG bucket name. Needs:
- Uncomment and fix backend to use correct bucket (`opal-313476888478-terraform-state`) and key (`yang-pipeline/tfstate`)
- Run `terraform init -migrate-state`
- Add missing EventBridge rules and IAM roles
- Verify 0-diff plan
- Tag `yang-v1.0.0`

### Priority 3: Seeking Alpha

7 Lambdas + IAM + EventBridge already in single main.tf. Needs:
- Add S3 backend
- Split into canonical file structure
- Import any missing resources
- Verify 0-diff plan
- Tag `seeking-alpha-v1.0.0`

### Priority 4: Portfolio

11 Lambda modules + DynamoDB table. Needs:
- Add S3 backend
- Import DynamoDB table
- Add missing IAM and EventBridge resources
- Split into canonical file structure
- Tag `portfolio-v1.0.0`

### Priority 5: Causality

8 Lambda modules, simplest pipeline. Needs:
- Add S3 backend
- Add missing IAM and EventBridge resources
- Tag `causality-v1.0.0`

### Priority 6: News Pipeline

Zero Terraform today. Needs:
- Full reconnaissance of all resources
- Write all TF files from scratch
- Import everything
- Add to CI/CD pipeline
- Tag `news-v1.0.0`

### Priority 7: Other/Misc

Assess contents and decide: split into proper pipelines or keep as catch-all with S3 backend.
