# EC2 Code Deployment Standard — S3 Artifact Model

**For:** All agents executing code on EC2 instances (AWS Engineer, DevOps, MoltBot, any Claude Code session)
**Status:** MANDATORY — violations break traceability and cause silent deployment drift
**Companion docs:** `docs/deployment/EC2_DEPLOYMENT_PROTOCOL.md`, `CLAUDE.md`
**Last Updated:** 2026-02-23

---

## The Problem This Solves

Agents have been writing Python scripts freeform on EC2 instances — inlining code in SSM commands, SCP-ing one-off files, editing directly on VMs. This creates:

- **No audit trail** — nobody knows what version of a script is running
- **Quoting hell** — Python code inline in SSM `--parameters` breaks constantly (f-strings, brackets, quotes)
- **Ghost code** — scripts on VMs that don't exist in the repo
- **Unreproducible state** — the next agent or rebuild can't recreate what's running

---

## The Rule

**Code lives in the repo. Code gets synced to S3. EC2s pull from S3. Nothing else.**

```
repo (source of truth)                    S3 (artifact store)                     EC2 (execution only)
data/black_diamond/scripts/   ──sync──►   s3://opal-data-bd/scripts/   ──pull──►  /home/ec2-user/scripts/
data/seeking-alpha/scripts/   ──sync──►   s3://opal-data-sa/scripts/   ──pull──►  /home/ec2-user/scripts/
infra/aws/ec2/{service}/      ──sync──►   s3://opal-ci-staging/...     ──pull──►  /home/ubuntu/{service}/
```

### Three Non-Negotiable Rules

1. **Never write code directly on an EC2 instance.** Not via SSM, not via SSH, not via SCP of ad-hoc files. Write it locally in the repo first, upload to S3, then trigger execution on the EC2.

2. **Never inline Python (or any non-trivial code) in SSM commands.** SSM commands should only orchestrate: pull from S3, run the script, upload logs. The SSM payload is a thin shell wrapper, not application logic.

3. **Ad-hoc and diagnostic scripts go through the same path.** Even throwaway one-time diagnostic scripts. Write locally → upload to S3 → run on EC2. This takes 30 seconds longer and gives you a traceable artifact.

---

## How It Works

### Step 1: Write the script locally

Write or edit the script in the repo under the appropriate path:

```
data/black_diamond/scripts/gold_layer/02_build_positions_cube.py   # pipeline script
data/black_diamond/scripts/diag_aua.py                              # diagnostic script
infra/aws/ec2/smartx-exporter/scripts/post-export-v2.sh            # service script
```

### Step 2: Upload to S3

```bash
# Pipeline scripts — sync the whole directory
aws s3 sync data/black_diamond/scripts/gold_layer/ s3://opal-data-bd/scripts/gold_layer/ --delete

# Core scripts
aws s3 sync data/black_diamond/scripts/core/ s3://opal-data-bd/scripts/core/ --delete

# One-off diagnostic
aws s3 cp data/black_diamond/scripts/diag_aua.py s3://opal-data-bd/scripts/diag_aua.py
```

### Step 3: Execute on EC2 via SSM

The SSM command is a **thin shell wrapper** — it pulls from S3 and runs:

```bash
aws ssm send-command \
  --instance-ids "i-01003b035d2988dfb" \
  --document-name "AWS-RunShellScript" \
  --timeout-seconds 600 \
  --parameters commands='[
    "aws s3 sync s3://opal-data-bd/scripts/ /home/ec2-user/scripts/ --quiet",
    "cd /home/ec2-user/scripts",
    "python3 gold_layer/02_build_positions_cube.py --upload 2>&1"
  ]'
```

**Notice:** The SSM payload does three things — sync, cd, run. No application logic.

### Step 4: Commit

If the script is worth running, it's worth committing:

```bash
git add data/black_diamond/scripts/diag_aua.py
git commit -m "diag: investigate AUA discrepancy vs BD truth"
git push origin DEV
```

---

## S3 Bucket Conventions

| Pipeline / Service | S3 Bucket | S3 Prefix | Local Source |
|---|---|---|---|
| BD Gold Layer | `opal-data-bd` | `scripts/gold_layer/` | `data/black_diamond/scripts/gold_layer/` |
| BD Core | `opal-data-bd` | `scripts/core/` | `data/black_diamond/scripts/core/` |
| BD Diagnostics | `opal-data-bd` | `scripts/` (root) | `data/black_diamond/scripts/` |
| Seeking Alpha | `opal-data-sa` | `scripts/` | `data/seeking-alpha/scripts/` |
| SmartX Exporter | `opal-ci-staging` | `ec2-deploy/smartx-exporter/` | `infra/aws/ec2/smartx-exporter/` |
| CI/CD staging | `opal-ci-staging` | `ec2-deploy/{service}/{commit}/` | Varies by service |

When adding a new pipeline or service, follow this convention: `s3://{pipeline-bucket}/scripts/{component}/`.

---

## Run Script Pattern

Every EC2 service that runs scripts should have a **run wrapper** that syncs from S3 before executing anything. This is the canonical pattern:

```bash
#!/bin/bash
set -euo pipefail

S3_BUCKET="opal-data-bd"
SCRIPTS_DIR="/home/ec2-user/scripts"
LOG_FILE="/tmp/run.log"

# ── Step 1: Always sync latest code from S3 ──
echo "Syncing scripts from s3://${S3_BUCKET}/scripts/ ..."
aws s3 sync "s3://${S3_BUCKET}/scripts/" "${SCRIPTS_DIR}/" --delete --quiet

# ── Step 2: Execute ──
cd "${SCRIPTS_DIR}"
python3 gold_layer/00_build_accounts_dimension.py --upload 2>&1 | tee -a "$LOG_FILE"
python3 gold_layer/02_build_positions_cube.py 2>&1 | tee -a "$LOG_FILE"
# ... more scripts ...

# ── Step 3: Upload logs ──
aws s3 cp "$LOG_FILE" "s3://${S3_BUCKET}/logs/$(date +%Y-%m-%d).log" --quiet

echo "Done."
```

**Key points:**
- `--delete` flag on sync ensures removed scripts don't linger on the VM
- Logs go to S3 for traceability
- No application logic in the wrapper — just orchestration

---

## SSM Command Pattern

When triggering scripts remotely via SSM, the command should be minimal:

### CORRECT — Thin orchestration wrapper

```bash
aws ssm send-command \
  --instance-ids "i-01003b035d2988dfb" \
  --document-name "AWS-RunShellScript" \
  --timeout-seconds 600 \
  --parameters commands='[
    "aws s3 cp s3://opal-data-bd/scripts/diag_aua.py /tmp/diag_aua.py",
    "python3 /tmp/diag_aua.py 2>&1"
  ]'
```

### WRONG — Inlined application code

```bash
# DO NOT DO THIS
aws ssm send-command \
  --parameters commands='[
    "python3 -c \"import pandas as pd; import boto3; s3=boto3.client('"'"'s3'"'"'); ...\""
  ]'
```

### WRONG — Multiline Python via SSM heredoc

```bash
# DO NOT DO THIS EITHER
aws ssm send-command \
  --parameters commands='[
    "cat << 'PYEOF' > /tmp/script.py\nimport pandas as pd\n...\nPYEOF",
    "python3 /tmp/script.py"
  ]'
```

Both of these break on quoting, are untrackable, and create ghost code on the VM.

---

## Diagnostic / Ad-Hoc Scripts

Even one-time diagnostic scripts follow the same flow:

1. Write locally: `data/black_diamond/scripts/diag_something.py`
2. Upload: `aws s3 cp data/black_diamond/scripts/diag_something.py s3://opal-data-bd/scripts/diag_something.py`
3. Run via SSM: `aws s3 cp ... /tmp/diag_something.py && python3 /tmp/diag_something.py`
4. Commit if useful, delete if not

**Why bother for throwaway scripts?**
- You have a local copy you can re-run or modify
- The S3 copy serves as an artifact
- No quoting issues — Python runs from a file, not inline
- The next agent can find and understand what was run

---

## What This Replaces

| Old Pattern | New Pattern |
|---|---|
| Python inline in SSM `--parameters` | Write script locally → S3 → EC2 pulls and runs |
| SCP ad-hoc files directly to VM | Upload to S3 → EC2 pulls from S3 |
| SSH + edit files on the VM | Edit locally → sync to S3 → EC2 refreshes |
| `cat << EOF > /tmp/script.py` in SSM | Upload from local to S3 → `aws s3 cp` on EC2 |
| "Let me fix the quoting..." | No quoting to fix — code is in a file |

---

## Enforcement

This standard is enforced by convention and agent instructions:

1. **CLAUDE.md** includes this as a critical deployment rule
2. **START_HERE.md** links to this doc as mandatory reading for all code/VM deployment
3. **Session logs** should note when scripts are deployed to S3 and which S3 paths were used
4. **Run wrappers** (`run_gold_layer.sh`, etc.) always sync from S3 before executing

There is no automated enforcement yet. If you see an agent inlining code in SSM or writing directly to a VM, flag it.

---

## Related Documents

- `docs/deployment/EC2_DEPLOYMENT_PROTOCOL.md` — Full EC2 deployment protocol (infrastructure + code)
- `infra/aws/ec2/EC2_MANIFEST.json` — Service manifest
- `infra/aws/ec2/safe-ec2-deploy.sh` — Deployment wrapper
- `data/black_diamond/scripts/core/run_gold_layer.sh` — Reference implementation of the S3-pull pattern
