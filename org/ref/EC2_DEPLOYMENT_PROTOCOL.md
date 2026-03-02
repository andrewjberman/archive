# EC2 Deployment Protocol — Opal Capital

**For:** All agents writing or deploying EC2 service code (AWS Engineer, DevOps, MoltBot, any Claude Code session)
**Linked from:** `START_HERE.md` (repo root)
**Companion docs:** `docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md`, `infra/aws/TERRAFORM_PIPELINE_STRATEGY.md`
**Last Updated:** 2026-02-23

---

## Why This Document Exists

EC2 services have a fundamentally different deployment model from Lambdas. There is no `archive_file` hash to detect drift automatically — parity depends on manifest tracking, SSM checksums, and disciplined use of deployment wrappers. Deploying outside the wrapper silently breaks the manifest, and the next agent has no idea what's actually running on the instance.

**Every agent must read this before touching EC2 service code.**

---

## The Golden Rules

> 1. **Always use `safe-ec2-deploy.sh`** — never run service-specific deploy scripts directly.
> 2. **Terraform manages infrastructure. Deployment wrappers manage code.**
> 3. **`EC2_MANIFEST.json` is the single source of truth** for what is deployed where.

---

## 1. EC2 Service Inventory

| Service | Type | Instance | Deploy Model | Source |
|---------|------|----------|-------------|--------|
| **moltbot** | Persistent | `i-0b784d4908e320fc4` | Manual (AI agent) | `infra/aws/ec2/moltbot/` |
| **smartx-exporter** | Persistent | `i-06ebcb27395eb3f49` | SCP via deploy script | `infra/aws/ec2/smartx-exporter/` |
| **seeking-alpha-scraper** | Persistent | TBD | SSH via deploy script | `infra/aws/ec2/seeking_alpha_scraper/` |
| **bd-exporter** | Persistent | TBD | S3 sync or SSH | `data/black_diamond/scripts/core/` |
| **bd-gold-layer-runner** | Persistent (stopped) | `i-01003b035d2988dfb` | S3-pull model | `data/black_diamond/scripts/` |
| **bd-gold-detail-generator** | Ephemeral | None (launched on demand) | user-data baked at launch | `infra/aws/ec2/bd-gold-detail-generator/` |

### Instance Types Explained

- **Persistent:** Always-on (or stopped). Code lives on the instance filesystem. Deployed via SCP/SSH/SSM. Tracked in manifest.
- **Ephemeral:** Launched fresh per job. Code is baked into `user-data.sh` or pulled from S3 on boot. Auto-terminates after work completes. CI/CD skips these.

---

## 2. Where Things Live

| Concern | Location | Example |
|---------|----------|---------|
| EC2 service source | `infra/aws/ec2/{service-name}/` | `infra/aws/ec2/smartx-exporter/` |
| BD scripts (special case) | `data/black_diamond/scripts/` | gold_layer/, core/ |
| Deployment manifest | `infra/aws/ec2/EC2_MANIFEST.json` | Tracks all services |
| Deploy wrapper | `infra/aws/ec2/safe-ec2-deploy.sh` | Always use this |
| Parity checker | `infra/aws/ec2/verify-ec2.sh` | Run before starting work |
| Manifest syncer | `infra/aws/ec2/sync-ec2-manifest.sh` | Pulls IPs/IDs from AWS |
| Terraform (infrastructure) | `infra/aws/terraform/{pipeline}/ec2.tf` | Instance, IAM, security groups |
| CI/CD workflow | `.github/workflows/ec2-deploy.yml` | Automated SSM deployment |
| User-data scripts | `infra/aws/ec2/{service}/user-data.sh` | Ephemeral boot scripts |
| Common utilities | `infra/aws/ec2/common/` | Auto-shutdown timer, etc. |

---

## 3. The Separation: Terraform vs Code Deployment

This is the most important concept for EC2. Unlike Lambdas where Terraform does both infrastructure AND code, EC2 splits them:

| Layer | Managed By | What It Controls |
|-------|-----------|-----------------|
| **Infrastructure** | Terraform | Instance resource, instance type, IAM role, instance profile, security groups, tags, root volume |
| **Code** | `safe-ec2-deploy.sh` + CI/CD | Python/Bash scripts, config files, application dependencies |

### Why the Split?

Terraform uses `lifecycle { ignore_changes = [ami, user_data, key_name, security_groups] }` on imported EC2 instances. This prevents Terraform from destroying and recreating running instances. Code deployment is a separate, non-destructive operation.

### What This Means for Agents

- **Changing instance type, IAM permissions, security groups** → Edit Terraform (`ec2.tf`, `iam.tf`), run `terraform apply`
- **Changing Python scripts, deploy scripts, application code** → Edit source, commit, use `safe-ec2-deploy.sh`
- **Both at once** → Do Terraform first (infrastructure), then code deploy second

---

## 4. Writing New EC2 Service Code

### 4.1 Directory Structure

```
infra/aws/ec2/{service-name}/
  deploy-to-ec2.sh          # Service-specific deploy logic (called by wrapper)
  requirements.txt           # Python dependencies (if applicable)
  *.py                       # Application scripts
  *.sh                       # Operational scripts
  user-data.sh               # Only for ephemeral instances
  README.md                  # Service documentation
```

### 4.2 Deploy Script Convention

Every persistent service needs a `deploy-to-ec2.sh`. This is called **by the wrapper**, never directly:

```bash
#!/bin/bash
set -e

# The wrapper passes the EC2 host as $1
EC2_HOST="$1"
EC2_USER="ubuntu"
REMOTE_PATH="/home/ubuntu/{service-name}"

# 1. Test connectivity
ssh -o ConnectTimeout=5 "$EC2_USER@$EC2_HOST" "echo ok" || {
  echo "ERROR: Cannot reach $EC2_HOST"
  exit 1
}

# 2. Create remote directory structure
ssh "$EC2_USER@$EC2_HOST" "mkdir -p $REMOTE_PATH"

# 3. Copy files
scp script1.py script2.py requirements.txt "$EC2_USER@$EC2_HOST:$REMOTE_PATH/"

# 4. Install dependencies (if changed)
ssh "$EC2_USER@$EC2_HOST" "cd $REMOTE_PATH && pip3 install -r requirements.txt"

# 5. Verify
ssh "$EC2_USER@$EC2_HOST" "ls -la $REMOTE_PATH/"
echo "Deploy complete."
```

### 4.3 Register in EC2_MANIFEST.json

Every new service must be added to the manifest:

```json
"my-new-service": {
  "instance_type": "persistent",
  "instance_id": "i-xxxxxxxxxxxx",
  "instance_name_tag": "my-new-service",
  "ec2_user": "ubuntu",
  "ec2_host": null,
  "iam_role": "my-new-service-role",
  "source_path": "infra/aws/ec2/my-new-service",
  "remote_path": "/home/ubuntu/my-new-service",
  "deploy_script": "infra/aws/ec2/my-new-service/deploy-to-ec2.sh",
  "deployed_commit": null,
  "deployed_at": null,
  "deployed_by": null,
  "file_checksums": {}
}
```

If you skip this, CI/CD is blind to your service and `verify-ec2.sh` won't check it.

### 4.4 Terraform for Infrastructure

Add the instance to the appropriate pipeline's `ec2.tf`:

```hcl
resource "aws_instance" "my_service" {
  ami                  = "ami-xxxxxxxxx"
  instance_type        = "t3.small"
  iam_instance_profile = aws_iam_instance_profile.my_service.name

  root_block_device {
    volume_size = 20
    volume_type = "gp3"
    encrypted   = true
  }

  tags = {
    Name = "my-new-service"
  }

  lifecycle {
    # CRITICAL for imported instances — prevents replacement
    ignore_changes = [ami, user_data, key_name, security_groups]
  }
}
```

Add IAM role + instance profile + policies to `iam.tf`. Always include `AmazonSSMManagedInstanceCore` for SSM access:

```hcl
resource "aws_iam_role_policy_attachment" "my_service_ssm" {
  role       = aws_iam_role.my_service.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}
```

---

## 5. Deployment Procedures

### 5.1 Before Starting Any EC2 Work

```bash
# Quick git-based drift check (no SSH needed)
./infra/aws/ec2/verify-ec2.sh

# Check a specific service
./infra/aws/ec2/verify-ec2.sh smartx-exporter

# Deep file-by-file comparison via SSM (instance must be running)
./infra/aws/ec2/verify-ec2.sh --ssm smartx-exporter

# If manifest IPs/IDs are stale (instance was restarted, IP changed)
./infra/aws/ec2/sync-ec2-manifest.sh
```

### 5.2 Deploying Code to a Persistent Service

**Correct sequence (mandatory):**

```
1. Edit source code       → infra/aws/ec2/{service-name}/
2. Commit to DEV          → git add specific files && git commit
3. Deploy via wrapper     → ./infra/aws/ec2/safe-ec2-deploy.sh {service} {deploy-script} [host]
4. Verify                 → ./infra/aws/ec2/verify-ec2.sh --ssm {service}
5. Push                   → git push origin DEV
```

**Example:**

```bash
# Edit the code
vim infra/aws/ec2/smartx-exporter/scripts/post-export-v2.sh

# Commit
git add infra/aws/ec2/smartx-exporter/
git commit -m "fix(smartx-exporter): handle missing date column in export"

# Deploy using the wrapper
./infra/aws/ec2/safe-ec2-deploy.sh smartx-exporter \
    infra/aws/ec2/smartx-exporter/deploy-to-ec2.sh

# Verify files match
./infra/aws/ec2/verify-ec2.sh --ssm smartx-exporter

# Push
git push origin DEV
```

### 5.3 The S3-Pull Model (bd-gold-layer-runner)

Some services don't receive code via SCP. Instead, code is pushed to S3 and pulled on boot:

```
Local source → deploy-to-ec2.sh → S3 bucket → EC2 boot pulls from S3
```

```bash
# Deploy pushes to S3
./infra/aws/ec2/safe-ec2-deploy.sh bd-gold-layer-runner \
    infra/aws/ec2/bd-gold-layer-runner/deploy-to-ec2.sh

# This syncs to:
#   s3://opal-data-bd/code/gold_layer/
#   s3://opal-data-bd/code/core/

# EC2 user-data.sh syncs FROM S3 on boot
```

### 5.4 Ephemeral Instances (user-data)

Ephemeral instances get their code baked into `user-data.sh`. There is no runtime deployment:

1. Edit `infra/aws/ec2/{service}/user-data.sh`
2. If Terraform manages the instance, the user-data change triggers a new launch config
3. If launched by Step Functions / Lambda, the launch script references the user-data file
4. Commit and push — the next launch picks up the new user-data

**Do not** try to SCP code to an ephemeral instance. It will be destroyed after the job completes.

### 5.5 Deploying Infrastructure Changes

For changes to the instance itself (IAM, security groups, instance type):

```
1. Edit Terraform          → infra/aws/terraform/{pipeline}/ec2.tf, iam.tf
2. Commit to DEV           → git commit
3. terraform plan           → verify expected changes
4. terraform apply          → apply infrastructure changes
5. terraform plan           → must show "No changes"
6. git tag + push           → {pipeline}-v{X.Y.Z} --follow-tags
```

---

## 6. Dependency Management

### 6.1 Python Dependencies

| Pattern | When | Example |
|---------|------|---------|
| **requirements.txt + pip** | Most services | `pip3 install -r requirements.txt` in deploy script |
| **venv** | Services needing isolation | seeking-alpha-scraper uses a venv |
| **User-data pip install** | Ephemeral instances | Installed fresh on every boot |

**Key rule:** Dependencies are installed as part of the deploy script, not committed to git. The deploy script should handle `pip install -r requirements.txt` on the remote instance.

### 6.2 System Dependencies

Install system packages in the deploy script or user-data, not manually:

```bash
# In deploy-to-ec2.sh or user-data.sh:
sudo apt-get update && sudo apt-get install -y python3 python3-pip  # Ubuntu
sudo yum install -y python3.11 python3.11-pip                       # Amazon Linux
```

### 6.3 Bun/TypeScript (bd-exporter)

```bash
# bd-exporter uses Bun + Playwright
cd infra/aws/ec2/bd-exporter
bun install
bunx playwright install chromium
```

### 6.4 Docker

Some services (moltbot/openclaw) use Docker. Docker image updates go through the normal deploy cycle — **never push directly to the Docker image on EC2**.

---

## 7. CI/CD: Automated SSM Deployment

### How It Works

The `.github/workflows/ec2-deploy.yml` workflow deploys automatically on push to DEV:

```
Push to DEV (touching infra/aws/ec2/**/*.py|*.sh)
    ↓
[detect] — git diff finds changed services via EC2_MANIFEST.json
    ↓
[deploy] (per service, matrix job)
    ├── Skip if instance_type == "ephemeral"
    ├── Stage files to S3: s3://opal-ci-staging/ec2-deploy/{service}/{commit}/
    ├── SSM Send Command: sync from S3 to remote_path
    ├── Verify SHA256 checksums
    ├── Update EC2_MANIFEST.json (deployed_commit, deployed_at, deployed_by)
    └── Commit manifest back with [skip ci]
```

### What CI Watches

```
infra/aws/ec2/**/*.py
infra/aws/ec2/**/*.sh
infra/aws/ec2/**/Dockerfile
infra/aws/ec2/**/docker-compose*.yml
infra/aws/ec2/**/requirements*.txt
```

It ignores `*.md` and `EC2_MANIFEST.json` (to prevent commit loops).

### SSM vs SSH

CI/CD uses **SSM (Systems Manager)**, not SSH. This means:
- No open SSH ports needed
- No SSH keys in CI
- Instance must have SSM agent + IAM role with `AmazonSSMManagedInstanceCore`
- Instance must be **running** for deploy to succeed

---

## 8. Parity Checking

### verify-ec2.sh

Two modes:

**Mode 1: Git-based (fast, no SSH)**
```bash
./infra/aws/ec2/verify-ec2.sh [service]
```
- Compares `deployed_commit` in manifest vs current HEAD
- Shows undeployed commits since last deploy
- Reports: CLEAN (no drift), DRIFT (undeployed changes), UNKNOWN (no deployed_commit)

**Mode 2: SSM checksum (thorough, instance must be running)**
```bash
./infra/aws/ec2/verify-ec2.sh --ssm [service]
```
- SSM runs SHA256 on all remote files
- Compares against local source checksums
- Reports: files that differ, files only on remote, files only locally

### sync-ec2-manifest.sh

Refreshes instance IDs and public IPs from AWS:

```bash
./infra/aws/ec2/sync-ec2-manifest.sh              # All services
./infra/aws/ec2/sync-ec2-manifest.sh bd-exporter   # One service
```

Run this when:
- An instance was stopped/started (public IP changes)
- An instance was replaced
- The manifest has `null` for `instance_id` or `ec2_host`

---

## 9. What NOT to Do

| Anti-Pattern | Why It's Broken |
|---|---|
| Running `deploy-to-ec2.sh` directly | Bypasses the wrapper. Manifest doesn't update. Next agent thinks old code is deployed. |
| SCP/SSH to push code without using the wrapper | Same problem — manifest drift. |
| Editing files directly on the EC2 instance | No git tracking. Changes lost on next deploy. Invisible to verify-ec2.sh. |
| `pip install` on EC2 without updating requirements.txt | Next deploy won't include the dependency. Silent regression. |
| Pushing to Docker image on EC2 directly | Bypasses deploy cycle. Not reproducible. |
| Changing IAM/security groups via AWS console | Terraform state drifts. Next `terraform apply` reverts the change. |
| Deploying from `main` branch | All work goes to `DEV`. Deploy from `DEV`. |
| Forgetting to commit before deploying | `deployed_commit` in manifest points to wrong SHA. Verify-ec2.sh gives false results. |

---

## 10. Pre-Completion Checklist

Before calling any EC2 work "done":

- [ ] Source code changes are in the correct `source_path` directory
- [ ] Changes committed to `DEV` before deploying
- [ ] Deployed via `safe-ec2-deploy.sh` (not direct script execution)
- [ ] `EC2_MANIFEST.json` updated (wrapper does this automatically)
- [ ] Parity verified: `verify-ec2.sh --ssm {service}` shows CLEAN
- [ ] If infrastructure changed: Terraform `plan` shows "No changes" after `apply`
- [ ] If infrastructure changed: Git tag created `{pipeline}-v{X.Y.Z}`
- [ ] If new service: Entry added to `EC2_MANIFEST.json`
- [ ] If new service: Terraform resources exist in `ec2.tf` and `iam.tf`
- [ ] `requirements.txt` updated if dependencies changed
- [ ] Pushed to remote: `git push origin DEV`

---

## 11. Service-Specific Notes

### smartx-exporter
- Post-deploy must copy `run-all-portfolios.sh` to both `/home/ubuntu/smartx-exporter/` AND `/home/ubuntu/run-all-portfolios.sh` (autostart Lambda expects the latter path)
- Terraform: `infra/aws/terraform/smartx-pipeline/ec2.tf`

### bd-gold-layer-runner
- S3-pull model: deploy pushes to `s3://opal-data-bd/code/gold_layer/` and `s3://opal-data-bd/code/core/`
- EC2 syncs from S3 on boot — no direct SCP
- Instance is normally **stopped** — started by Lambda/Step Functions trigger
- Terraform: `infra/aws/terraform/bd-pipeline/ec2.tf`

### bd-gold-detail-generator
- **Ephemeral** — no persistent deploy. Code lives in `user-data.sh`
- CI/CD skips this service
- To update: edit `user-data.sh`, commit, and the next launch uses the new script
- Terraform manages the launch template

### moltbot
- AI agent — no automated deploy script
- GitHub access via Secrets Manager (`github/moltbot-pat`)
- Setup: `infra/aws/ec2/moltbot/setup-github.sh`
- Has elevation modes: `moltbot-elevate` / `moltbot-lower`

### seeking-alpha-scraper
- Uses SSH key: `~/.ssh/seeking-alpha-scraper-key.pem`
- Python venv at `cookie-env/`
- Deploy: `deploy_hybrid.sh` (called via wrapper)

---

## 12. Related Documents

- `docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md` — Lambda deployment rules
- `infra/aws/TERRAFORM_PIPELINE_STRATEGY.md` — Full Terraform strategy
- `infra/aws/ec2/EC2_MANIFEST.json` — Service manifest (source of truth)
- `.github/workflows/ec2-deploy.yml` — CI/CD workflow
- `infra/aws/ec2/common/setup-autoshutdown-timer.sh` — Auto-shutdown utility
