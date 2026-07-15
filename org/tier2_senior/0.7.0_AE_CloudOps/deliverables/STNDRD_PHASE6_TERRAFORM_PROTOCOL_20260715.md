# TERRAFORM PROTOCOL -- the one-document Terraform mechanism (OPAL_STNDRD axis E)

> **CANONICAL TARGET:** `docs/deployment/TERRAFORM_PROTOCOL.md` -- BASE_EXEC lane; CTO lands the
> canonical copy AND owns the CLAUDE.md pointer edit (ANY_CTO surface -- per the ratified axis E,
> "law stays CLAUDE.md", this doc carries the MECHANISM). This deliverable copy is the authored
> source of record until then.
>
> **Method (axis E as ratified): VERBATIM MOVES.** Operative texts are quoted with their source
> pins, not paraphrased -- the phrasing IS the ruling. Nothing here supersedes CLAUDE.md; where
> they could ever disagree, CLAUDE.md wins and this doc has a defect.

**Status:** RATIFIED (CTO, OPAL_STNDRD.json axis E). **Owner:** 0.7.0_AE_CloudOps (Z1 phase 6).
**Why one doc:** the protocol held twice on 2026-07-15 alone, but its mechanism is scattered
across CLAUDE.md (NEVER block, Rules 1-6, 18, Git section) + `.claude/skills/cloud-ops` +
`docs/deployment/*` + `infra/aws/TERRAFORM_PIPELINE_STRATEGY.md`. One doc, every mechanism,
each with its pin.

## 1. The law (pointers -- lives in CLAUDE.md, quoted for completeness)

- NEVER block: "**NEVER** run bare `terraform apply` (use `safe-apply`), bare `git commit` (use
  `safe-commit.sh`), or `aws lambda update-function-code` (Terraform only). **GATE:
  `.tools/hooks/never-rules-gate.sh` (PreToolUse, `Bash|PowerShell`) -- LIVE + exercised.**
  Audited override: `# never-override: <reason>`."
- Rule 1: "**Terraform is the only Lambda deploy mechanism.** No console, no `deploy.sh`, no
  direct code pushes."
- Rule 2: "**Commit before apply.** code -> TF -> source map -> commit -> plan -> apply -> 0-diff
  -> tag -> push `--follow-tags`."
- Rule 3: "**Dependencies go in Lambda Layers.** No `pip install -t .` into source dirs; inline
  vendoring needs explicit approval."
- Rule 4: "**Update the source map** -- every Lambda has an entry in
  `infra/aws/lambda/ci/lambda-source-map.json` (CI drift detection)."
- Rule 5: "**Size Lambda resources deliberately** -- never leave `yang-lambda` defaults
  (256MB/30s) on data-processing Lambdas."
- Rule 6: "**Tag after deploy:** `git tag -a {pipeline}-v{X.Y.Z}` + push `--follow-tags` after
  every 0-diff apply."
- Rule 18: "**`terraform apply` goes through `.tools/safe-apply.sh`** -- HALTGT inbox checkpoint
  at the last reversible moment (routine pending msg -> `HALT_ACK=1`; override audited via
  `HALT_OVERRIDE="reason"`). **A HALTGT PASS IS NOT EVIDENCE YOU WERE NOT HALTED** [...]
  **NOBODY CITES A HALTGT PASS.**" (full text: CLAUDE.md Rule 18; design `docs/architecture/ADHC_HALTGT.md`, `org/tier0/ledger/LD-0267.md`)

## 2. The apply cycle (mechanism -- from `.claude/skills/cloud-ops/SKILL.md` pre-flight, verbatim)

1. "`git tag -l "{pipeline}-v*" | sort -V | tail -5` -- find the actual latest tag (CRITICAL:
   don't assume next version)."
2. "`terraform plan` -- read the diff before applying. If a `-target` is needed because of P3
   module S3 artifact gaps, target the specific resource. Note targeting in the RAVC."
3. "RAVC1 to CTO + COO with the plan diff for any non-trivial change. For trivial in-place
   attribute updates (state flips, env var bumps), surface plan + apply in one RAVC if
   pre-authorized by a TO; otherwise wait for GO."
4. "**`.tools/safe-apply.sh` (Rule 18) -- NOT bare `terraform apply`.** The HALT-gate checkpoint
   fires immediately before the irreversible apply: empty inbox passes silently; routine pending
   message surfaces (sender/subject/age) and requires `HALT_ACK=1` on re-invocation; **STOP-class**
   message (`[STOP]` or `[HALT]` subject prefix) hard-blocks. Override only via
   `HALT_OVERRIDE="<reason>"` (audited to `org/halt-gate-override-audit.log`). If the checkpoint
   library is missing, safe-apply fails closed."
5. "After apply, `terraform plan` again for 0-diff verification."
6. "Tag `{pipeline}-v{X.Y.Z}`, push `--follow-tags`."
7. "RAVC2 with apply confirmation + AWS state check (e.g., `aws events describe-rule`,
   `aws lambda get-function-configuration`)."

Post-apply recording: `record-terraform-deploy.sh` / `record-resource-deploy.sh` update
`last_deployed_commit` in the ci/ registries; `drift-check-resource-map.sh` then detects
committed-but-undeployed TF (exit 2 = drift). Known issue: "record-terraform-deploy.sh tooling
failure: known issue (CHANGELOG.json writer + owned-paths-hook on Andrew identity); reset the
spurious source-map.json changes and surface in RAVC." (cloud-ops SKILL.md, Failure handling)

## 3. Environment mechanics (Git section, CLAUDE.md, verbatim where operative)

- Binary: "Terraform binary: `.tools/terraform.exe`". Backend: `opal-313476888478-terraform-state`,
  one `{module}/tfstate` key per module (50 at 2026-07-15). Provider cache:
  `TF_PLUGIN_CACHE_DIR=C:\Users\AndrewBerman\.terraform.d\plugin-cache` (registry unreachable from
  sandboxed sessions -- init resolves from cache).
- "`MSYS_NO_PATHCONV=1` ONLY for Terraform imports / ARN-path args, and for `git show <ref>:<path>`
  when BOTH the ref and the path contain a `/` [...] **NEVER for `git push`** (breaks the VALGATE
  hook)**, the aws launcher, or `safe-apply`** (it leaks into the comp-tagauthz gate's internal
  python call and mangles its path -- the gate FAILS CLOSED on a phantom `C:\c\...` path; measured
  2026-07-15, 0.7.0 codeheat motion)."
- AWS CLI from Git Bash rides the `.tools/aws` shim (see CLAUDE.md Git section for the atomic
  `.tools/aws.cmd` provisioning law).

## 4. Plan-shape discipline (measured practice, 2026-07-15 exhibits)

- NEW-TERRITORY builds: a plan that is not PURE "to add" is out of scope (Andrew ~02:05Z ruling,
  OPAL_ASSETS macro; e.g. consolidation-gold-runner 12/0/0, opal-assets-absence 5/0/0).
- Trivial flips (state 0/1/0, env bump) may ride one RAVC when TO-pre-authorized (sec-2 step 3).
- `-target` applies are legal with the targeting NOTED in the RAVC (sec-2 step 2); a targeted
  apply still ends at a full-module 0-diff or a documented residual.
- One-motion rulings: a diff that mixes concerns is split before it is applied.

## 5. Related-doc map (incorporate-by-reference, not duplication)

| Doc | Carries |
|---|---|
| `infra/aws/TERRAFORM_PIPELINE_STRATEGY.md` | module/pipeline layout strategy |
| `docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md` | Lambda packaging + layer + CI specifics |
| `docs/deployment/EC2_DEPLOYMENT_PROTOCOL.md`, `EC2_CODE_DEPLOYMENT_STANDARD.md` | EC2: TF owns infra, code rides S3 (Rules 7-12) |
| `docs/deployment/EC2_TELEMETRY_RIGHTSIZING_STANDARD.md` | axis-D standard (telemetry/right-sizing/autoshutdown) |
| `infra/aws/lambda/ci/` | the registry home: source-map, trigger-map, absence-config, layer-map, resource maps + drift instruments |
| `docs/architecture/ADHC_HALTGT.md` + `org/tier0/ledger/LD-0267.md` | HALTGT design + its known holes |

## 6. CLAUDE.md pointer edit (CTO-owned, proposed text)

In `## Detailed Documentation`, the Lambda/EC2 line gains:
`docs/deployment/TERRAFORM_PROTOCOL.md` (the one-document TF mechanism; law stays in this file).
No rule text changes -- the pointer is the whole edit.
