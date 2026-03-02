# Lambda Deployment Protocol — Opal Capital

**For:** All agents writing Lambda source code (AWS Engineer, DevOps, MoltBot, any Claude Code session)
**Linked from:** `start_here.md` (repo root)
**Companion doc:** `infra/aws/TERRAFORM_PIPELINE_STRATEGY.md`
**Last Updated:** 2026-02-23

---

## Why This Document Exists

Lambda code deployed outside Terraform causes **state drift** — the next `terraform apply` by any agent will either revert the change or error out. This document is the single authority on how to write, package, and deploy Lambda code while maintaining parity between:

- Local source code (git)
- Terraform state (S3)
- Live AWS infrastructure

**Every agent must read this before touching Lambda code.**

---

## The Golden Rule

> **Terraform is the only deployment mechanism.** No `aws lambda update-function-code`, no `deploy.sh`, no manual console uploads. Ever.

---

## 1. Where Things Live

| Concern | Location | Example |
|---------|----------|---------|
| Lambda source code | `infra/aws/lambda/{function-name}/` | `infra/aws/lambda/bd-gold-clients/lambda_function.py` |
| Terraform config | `infra/aws/terraform/{pipeline}/` | `infra/aws/terraform/bd-pipeline/lambdas.tf` |
| Reusable Lambda module | `infra/aws/terraform/modules/yang-lambda/` | Used by 95% of Lambdas |
| Source-to-deploy map | `infra/aws/lambda/ci/lambda-source-map.json` | CI drift detection |
| CI build script | `infra/aws/lambda/ci/build-zip.sh` | Deterministic zip builder |
| Deploy recorder | `infra/aws/lambda/ci/record-terraform-deploy.sh` | Updates source map after apply |

When you modify a Lambda, you are **always touching at least two locations**: the source directory and the Terraform config. If you only touch one, you've left the system in an inconsistent state.

---

## 2. Writing New Lambda Code

### 2.1 Create the Source Directory

```
infra/aws/lambda/{function-name}/
  lambda_function.py          # Required — must contain lambda_handler()
  requirements.txt            # Only if the function has non-layer dependencies
  (other .py modules)         # Co-located helper files
```

**Do NOT include in the source directory:**
- `deploy.sh` (deprecated pattern)
- Test files (put in `tests/` outside the source dir, or exclude in Terraform)
- Documentation, scratch files, notebooks
- `__pycache__/`, `*.pyc`

### 2.2 Create the Terraform Resource

Add to `infra/aws/terraform/{pipeline}/lambdas.tf`:

```hcl
module "my_new_lambda" {
  source        = "../modules/yang-lambda"
  function_name = "my-new-lambda"
  source_dir    = "${local.lambda_base_dir}/my-new-lambda"
  role_arn      = aws_iam_role.my_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.12"
  timeout       = 120        # Set appropriately — do NOT leave defaults
  memory_size   = 1024       # Set appropriately — do NOT leave defaults
  layers        = [local.pandas_layer]  # If needed
  environment_variables = {
    BUCKET_NAME = "opal-data-portal-v2"
  }
}
```

**Memory/timeout guidance:**

| Workload | Memory | Timeout |
|----------|--------|---------|
| Lightweight trigger/router | 128 MB | 30s |
| API handler (DynamoDB reads) | 256–512 MB | 30s |
| Pandas/data processing | 1024–3072 MB | 120–600s |
| Heavy ETL (full dataset rebuild) | 3072+ MB | 600–900s |

Undersized memory causes silent OOM kills that appear as mysterious timeouts. Always size deliberately.

### 2.3 Add IAM Permissions

Add to `infra/aws/terraform/{pipeline}/iam.tf`. Match the principle of least privilege:

```hcl
resource "aws_iam_role" "my_role" {
  name = "my-new-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "my_role_policy" {
  name = "my-new-lambda-policy"
  role = aws_iam_role.my_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      # Add ONLY the permissions the Lambda actually needs
    ]
  })
}
```

### 2.4 Register in the Source Map

Add entry to `infra/aws/lambda/ci/lambda-source-map.json`:

```json
"my-new-lambda": {
  "source_dir": "infra/aws/lambda/my-new-lambda",
  "files": ["lambda_function.py"],
  "output_dir": "infra/aws/terraform/{pipeline}/code",
  "tf_file": "infra/aws/terraform/{pipeline}/lambdas.tf",
  "tf_resource": "module.my_new_lambda.aws_lambda_function.this",
  "last_deployed_commit": null,
  "last_deployed_at": null
}
```

This is what CI uses for drift detection. If you skip this, CI is blind to your Lambda.

---

## 3. Dependency Management

### 3.1 Use Lambda Layers (Default)

Layers are the standard for shared packages. Common layers already available:

| Layer | ARN Pattern | Contains |
|-------|-------------|----------|
| AWS SDK Pandas | `arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python311:21` | pandas, numpy, pyarrow |
| Custom Pandas/PyArrow | `arn:aws:lambda:us-east-1:313476888478:layer:pandas-pyarrow-layer:1` | pandas, pyarrow |
| yfinance | `arn:aws:lambda:us-east-1:313476888478:layer:yfinance-dependencies:1` | yfinance + deps |
| BD Gold Common | `arn:aws:lambda:us-east-1:313476888478:layer:bd-gold-common:1` | Shared BD utilities |

Reference layers in Terraform via the `layers` parameter on the `yang-lambda` module.

### 3.2 When a Package Isn't in an Existing Layer

**Stop and flag it.** Do not:
- Run `pip install -t .` into the Lambda source directory
- Vendor hundreds of dependency files into git
- Create ad-hoc zip scripts

Instead, one of these must happen:
1. **Build a new Lambda Layer** — package the dependency as a reusable layer, publish via Terraform. Follow §3.4 below exactly.
2. **Use a container image Lambda** — for extremely complex or large native-compiled dependencies (e.g., `package_type = "Image"` with ECR)
3. **Intentional inline vendoring** — only with explicit approval, using `requirements.txt` + the `build-zip.sh` CI script

**This is an infrastructure task.** If you are not the AWS Engineer or DevOps agent, stop here and hand off. Do not build or deploy a Lambda Layer as a Data Scientist, React Designer, or any non-infrastructure persona.

### 3.3 Never Pip-Install Into the Source Directory Without Approval

Inline vendoring (pip installing into the source dir) creates:
- Hundreds of files committed to git
- Nondeterministic builds (different pip versions produce different outputs)
- Merge conflicts on every dependency update
- Bloated zips that may exceed Lambda's 50MB zip limit

This pattern exists in some legacy Lambdas (`portfolio_optimization_loader`, `news_ingestion_scheduler`) but is **not the standard** for new work.

---

## 3.4 Building a New Lambda Layer

This section is the canonical protocol for creating a new Lambda Layer from scratch. Follow it in order. Every step is mandatory.

### Build Environment — Decide First

Lambda Layers containing **native extensions** (packages with C/Cython/Fortran compiled code — numpy, scipy, hdbscan, psycopg2, etc.) **must** be built in a Linux environment that matches the Lambda execution environment (Amazon Linux 2023, x86_64).

| Situation | Allowed approach |
|-----------|-----------------|
| Docker available locally | Build inside `public.ecr.aws/lambda/python:3.12` container |
| No Docker, CI available | Use GitHub Actions `ubuntu-latest` runner |
| No Docker, no CI, **pure-Python packages only** | `pip download --platform manylinux2014_x86_64 --only-binary=:all:` on Windows is acceptable |
| No Docker, no CI, **native extensions needed** | **STOP. Do not proceed.** Create an EC2 build task or GitHub Actions workflow first. |

**Why this matters:** `pip download --platform` downloads pre-built manylinux wheels, which works when the package publishes them. If a package doesn't publish manylinux wheels, the download silently falls back to a source distribution that will fail to import on Lambda. Never assume platform targeting is a safe universal substitute for a real Linux build.

### Step-by-Step: Creating a New Layer

**Step 1 — Create the layer source directory and `requirements.txt` (git first)**

```
infra/aws/lambda/layers/{layer-name}/
  requirements.txt        # Pinned versions + rebuild instructions (committed to git)
```

The `requirements.txt` **must be committed to git before the layer zip is uploaded to S3.** This is the "deployed code must correspond to a git commit" rule applied to layers. If the layer exists in AWS but no git artifact describes its contents, the deploy is out of compliance.

Format for `requirements.txt`:

```
# {layer-name} Lambda Layer
# Python 3.12 / Amazon Linux 2023 (manylinux_2_17_x86_64)
#
# HOW TO REBUILD:
#   [exact commands to reproduce the layer zip — see example below]
#
# PINNED VERSIONS (as built YYYY-MM-DD):
package-name==X.Y.Z
other-package==X.Y.Z
```

The compiled `python/` directory lives alongside `requirements.txt` on disk but is **gitignored** (`infra/aws/lambda/layers/*/python/`). Only `requirements.txt` is committed.

**Step 2 — Build the layer zip**

Docker approach (preferred for native extensions):
```bash
docker run --rm \
  -v "$(pwd)/infra/aws/lambda/layers/{layer-name}:/layer" \
  public.ecr.aws/lambda/python:3.12 \
  bash -c "pip install -r /layer/requirements.txt -t /layer/python/ \
           && find /layer/python -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null; true"

cd infra/aws/lambda/layers/{layer-name}
python -m zipfile -c /tmp/{layer-name}.zip python/
```

`pip download` approach (pure-Python packages only):
```bash
pip download \
  --platform manylinux2014_x86_64 \
  --implementation cp \
  --python-version 312 \
  --only-binary=:all: \
  -d /tmp/{layer-name}-wheels \
  package1==X.Y.Z package2==X.Y.Z

mkdir -p infra/aws/lambda/layers/{layer-name}/python
for whl in /tmp/{layer-name}-wheels/*.whl; do
  unzip -q -o "$whl" -d infra/aws/lambda/layers/{layer-name}/python/
done
# Strip unnecessary files to reduce size:
find infra/aws/lambda/layers/{layer-name}/python -maxdepth 1 -name "*.dist-info" -exec rm -rf {} +
find infra/aws/lambda/layers/{layer-name}/python -type d -name "tests" -exec rm -rf {} +
find infra/aws/lambda/layers/{layer-name}/python -type d -name "__pycache__" -exec rm -rf {} +

python -m zipfile -c /tmp/{layer-name}.zip \
  infra/aws/lambda/layers/{layer-name}/python/
```

Check zip size before proceeding:
```bash
ls -lh /tmp/{layer-name}.zip
# > 50MB → must use S3 upload (see Step 3)
# ≤ 50MB → can use local filename in Terraform (but S3 is preferred for consistency)
```

**Step 3 — Commit `requirements.txt` to DEV**

```bash
git add infra/aws/lambda/layers/{layer-name}/requirements.txt
git commit -m "chore({pipeline}): add {layer-name} layer requirements.txt"
```

---

> ### 🛑 GATE — MANDATORY CHECK BEFORE ANY AWS OPERATION
>
> You are about to upload a binary artifact to AWS. Once published as a Lambda Layer version,
> it is **immutable** — it cannot be modified, only replaced by a new version.
> The `requirements.txt` in git is the only source-of-record for what is inside the zip.
>
> **Run this check right now:**
> ```bash
> git log -1 --oneline infra/aws/lambda/layers/{layer-name}/requirements.txt
> ```
>
> **Expected output:** a commit hash and message — e.g. `a3fc8c8 chore(news-pipeline): add news-trending-deps layer requirements.txt`
>
> **If the output is empty (no commit found):** STOP. Go back to Step 3. Do not run `aws s3 cp`. Do not run `terraform apply`. The requirements.txt must be committed first.
>
> **If you skip this gate and proceed anyway:** you will have a layer version deployed in AWS with no git artifact describing its contents. This violates the "deployed code must correspond to a git commit" rule. You will have to publish a new layer version after remediation — the deployed one cannot be patched.

---

**Step 4 — Upload zip to S3**

Layer zips are stored at a dedicated prefix in the artifact bucket:

```bash
aws s3 cp /tmp/{layer-name}.zip \
  s3://opal-313476888478-lambda-layers/{layer-name}.zip \
  --region us-east-1
```

> **Note:** Use `s3://opal-313476888478-lambda-layers/` — NOT the Terraform state bucket (`opal-313476888478-terraform-state`). The state bucket is for Terraform state only.

**Step 5 — Write the Terraform resource**

Add to `infra/aws/terraform/{pipeline}/lambdas.tf`:

```hcl
# -----------------------------------------------------------------------------
# Lambda Layer: {layer-name}
# Python 3.12 / Amazon Linux 2023 — manylinux wheels
# Contains: [list packages]
# Required by: [list functions that use it]
# Zip stored in S3: s3://opal-313476888478-lambda-layers/{layer-name}.zip
# Source: infra/aws/lambda/layers/{layer-name}/requirements.txt
# -----------------------------------------------------------------------------
resource "aws_lambda_layer_version" "{tf_resource_name}" {
  layer_name  = "{layer-name}"
  description = "[short description] (Python 3.12)"

  s3_bucket = "opal-313476888478-lambda-layers"
  s3_key    = "{layer-name}.zip"

  compatible_runtimes = ["python3.12"]
}
```

Wire it to the Lambda function:
```hcl
module "my_function" {
  ...
  layers = [aws_lambda_layer_version.{tf_resource_name}.arn]
}
```

**Step 6 — Register in `lambda-layer-map.json`**

Add an entry to `infra/aws/lambda/ci/lambda-layer-map.json`:

```json
"{layer-name}": {
  "source_dir": "infra/aws/lambda/layers/{layer-name}",
  "s3_bucket": "opal-313476888478-lambda-layers",
  "s3_key": "{layer-name}.zip",
  "tf_file": "infra/aws/terraform/{pipeline}/lambdas.tf",
  "tf_resource": "aws_lambda_layer_version.{tf_resource_name}",
  "build_platform": "manylinux2014_x86_64",
  "python_version": "3.12",
  "last_built_commit": null,
  "last_built_at": null,
  "used_by": ["{function-name-1}", "{function-name-2}"]
}
```

**Step 7 — Follow the standard deployment sequence**

From §4 below: commit → plan → apply → 0-diff → tag → push.

The commit before `terraform apply` must include both the updated `lambdas.tf` (new layer resource + function wired to it) and the updated `lambda-layer-map.json`.

### Layer Checklist

Before calling layer work "done":

- [ ] `infra/aws/lambda/layers/{layer-name}/requirements.txt` committed to DEV
- [ ] Layer zip built in correct environment (Linux/Docker for native extensions)
- [ ] Layer zip uploaded to `s3://opal-313476888478-lambda-layers/{layer-name}.zip`
- [ ] `aws_lambda_layer_version` Terraform resource written in `lambdas.tf`
- [ ] Lambda function's `layers = [...]` updated in Terraform
- [ ] Entry added to `infra/aws/lambda/ci/lambda-layer-map.json`
- [ ] All Terraform + map changes committed to DEV before `terraform apply`
- [ ] `terraform plan` shows only expected changes
- [ ] `terraform apply` succeeds, `terraform plan` shows "No changes"
- [ ] Layer ARN verified on the Lambda: `aws lambda get-function-configuration --function-name {fn} --query Layers`
- [ ] Git tag created and pushed with `--follow-tags`

---

## 4. The Deployment Sequence

### Correct Order (mandatory):

```
1. Write source code     → infra/aws/lambda/{function-name}/
2. Write Terraform       → infra/aws/terraform/{pipeline}/lambdas.tf, iam.tf, etc.
3. Update source map     → infra/aws/lambda/ci/lambda-source-map.json
4. Commit to DEV         → git add specific files && git commit
5. terraform plan        → verify changes are expected
6. terraform apply       → deploy to AWS
7. terraform plan        → MUST show "No changes" (verify 0-diff)
8. Git tag               → git tag -a {pipeline}-v{X.Y.Z} -m "description"
9. Push                  → git push --follow-tags
```

### Why This Order Matters

- **Commit before apply:** `archive_file` hashes whatever is on disk at apply time. If you apply before committing, the deployed code doesn't correspond to any commit. The tag then points to the wrong state.
- **Plan after apply:** Confirms Terraform state matches AWS reality. If the post-apply plan shows drift, something went wrong.
- **Tag after 0-diff:** The tag certifies that at this commit, Terraform and AWS are in sync.

### What NOT to Do

| Anti-Pattern | Why It's Broken |
|---|---|
| `aws lambda update-function-code` | Terraform state doesn't know about the change. Next apply reverts it. |
| Running `deploy.sh` | Same problem. Legacy scripts bypass Terraform entirely. |
| `terraform apply` before `git commit` | Deployed code doesn't match any commit. Tag is meaningless. |
| Forgetting `terraform plan` after apply | You don't know if state is actually clean. |
| Skipping the source map update | CI drift detection is blind to your Lambda. |
| Adding `lifecycle { ignore_changes = [filename, source_code_hash] }` | Terraform will never deploy code updates. Only use for container-image Lambdas managed via ECR. |
| `aws s3 cp` (layer zip) before committing `requirements.txt` | Layer version is published with no source-of-record in git. The immutable layer version cannot be patched — a new version must be published after remediation. See §3.4 Gate. |
| Storing layer zip in the Terraform state bucket | State bucket is for Terraform state only. Layer zips go in `s3://opal-313476888478-lambda-layers/`. Mixing them causes confusion and breaks the separation of concerns. |

---

## 5. Modifying Existing Lambdas

When editing code for a Lambda that's already Terraform-managed:

1. Edit the source files in `infra/aws/lambda/{function-name}/`
2. If adding new `.py` files, verify they're in the `source_dir` that Terraform zips (check the `yang-lambda` module call or `archive_file` block)
3. If adding new dependencies, follow Section 3 (layers first, not inline pip)
4. If changing memory/timeout/env vars, update the Terraform config too
5. Follow the deployment sequence in Section 4

**Do not** change Lambda configuration (memory, timeout, environment variables, layers) via the AWS console or CLI. All config lives in Terraform.

---

## 6. Files to Exclude from Lambda Zips

The `yang-lambda` module automatically excludes:
- `__pycache__/`
- `*.pyc`
- `.git`
- `deploy.sh`
- `*.md`

If you add files to a Lambda directory that shouldn't be deployed (tests, scratch, data files), either:
- Move them outside the source directory, or
- Add them to the `excludes` list in the Terraform `archive_file` block

---

## 7. Pre-Completion Checklist

Before calling any Lambda work "done", verify every item:

- [ ] Source code is in `infra/aws/lambda/{function-name}/`
- [ ] Terraform module/resource exists in `infra/aws/terraform/{pipeline}/lambdas.tf`
- [ ] IAM role and policy exist in `infra/aws/terraform/{pipeline}/iam.tf`
- [ ] Dependencies use layers (not pip-installed into source dir) unless explicitly approved
- [ ] If a new layer was created: `requirements.txt` committed before S3 upload, entry in `lambda-layer-map.json`, layer zip in `s3://opal-313476888478-lambda-layers/` (not the state bucket)
- [ ] Memory and timeout are sized for the workload (not left at defaults)
- [ ] `lambda-source-map.json` has an entry for this function
- [ ] All changes are committed to `DEV` before running `terraform apply`
- [ ] `terraform plan` shows only expected changes before apply
- [ ] `terraform plan` shows "No changes" after apply
- [ ] Git tag created: `{pipeline}-v{X.Y.Z}`
- [ ] Pushed with `--follow-tags`
- [ ] No `deploy.sh` was used, no raw AWS CLI deployments

---

## 8. Quick Reference: Terraform Tag Protocol

```bash
# After successful terraform apply + 0-diff plan:
git tag -a {pipeline}-v{X.Y.Z} -m "{Pipeline}: brief description of changes"
git push --follow-tags

# Version bumps:
# MAJOR — breaking infra change, resource replacement, backend migration
# MINOR — new resource, new feature, non-breaking config change
# PATCH — bug fix, policy tweak, config correction

# List tags for a pipeline:
git tag -l "{pipeline}-v*"
```

---

## 9. Related Documents

- `infra/aws/TERRAFORM_PIPELINE_STRATEGY.md` — Full Terraform strategy, import procedures, rollback
- `infra/aws/terraform/modules/yang-lambda/` — Reusable Lambda module source
- `infra/aws/lambda/ci/lambda-source-map.json` — Source-to-deployment mapping for functions
- `infra/aws/lambda/ci/lambda-layer-map.json` — Source-to-deployment mapping for layers
- `.github/workflows/lambda-deploy.yml` — CI drift detection workflow
