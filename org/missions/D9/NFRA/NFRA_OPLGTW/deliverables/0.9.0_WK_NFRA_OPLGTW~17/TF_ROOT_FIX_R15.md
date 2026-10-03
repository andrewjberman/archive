# OG-tf-2 -- TF_ROOT_FIX_R15 (0.9.0_WK_NFRA_OPLGTW~17, round 15)

Decision record, committed BEFORE any implementation (task order section 1 item 2). Rulings: CTO R2 and R3,
`ledger/ROUND_ANALYSIS.round14.md` section 3. Premise state at HEAD `aa774e5110`: the grant writer equals `af2d762970`'s
closure (OG-gw-2); `build_package.py` stages from `EC2_MANIFEST.json` `services.opal-gateway.deployed_commit` (OG-gw-1);
the order's acceptance helper makes a fresh sparse worktree, unsets every `TF_VAR_*`, runs `terraform init` and ONE
untargeted plan, and runs nothing before it.

## 1. The owner keys (R2) -- chosen

Two keys `mcportal_owner_key`, `mcportal_owner_key_claim` added to the EXISTING secret `gateway/principals/rosters`
(the OG-rl-4 precedent), values read IN MEMORY from the live function's `MCPORTAL_OWNER_KEY` / `MCPORTAL_OWNER_KEY_CLAIM`,
sha256-compared, written with a read-modify-write of the secret JSON that leaves the three pre-existing keys byte-equal
(per-key sha256 before and after). The root reads them with a `data "aws_secretsmanager_secret_version"` + `jsondecode`;
the two `variable` blocks are deleted. The claim's `oid`/`sub` validation moves to a `lifecycle { precondition }` on the
function (a precondition is a check, not `ignore_changes`). Ledger `nfra-oplgtw-tf-root-owner-keys` (legs: secret keys,
plan clean), entry and sentinel committed before the write.

Rejected (CTO R2, restated): reading the live function's own environment (self-referential, fails on a fresh account);
`ignore_changes` (Terraform stops governing the owner); a literal default (a personal identifier committed); `TF_VAR_*`
(the acceptance unsets them); a NEW secret (creates a resource; the existing secret already carries the principals).

## 2. The archive input (R3) -- chosen: `data "external"` running a root-local wrapper

The only code that can run between `terraform init` and the plan, with nothing run first, is a data source. Terraform has
no built-in data source that executes a program; the smallest provider that does is `hashicorp/external` (the same
registry, publisher and lock-file mechanism as the `aws` and `archive` providers already locked here). The root gets:

- `build_gw_stage.py` (stdlib, in the root dir -- the only place this order may write): runs the pinned
  `build_package.py --out <root>/.build/...zip --stage-dir <root>/.build/mcportal-grant-writer-staged`, with the build's own
  stdout redirected to stderr (the external protocol needs ONE JSON object on stdout), and prints `{"staged_dir": "<path>"}`.
  A build refusal (rc != 0) exits non-zero, so the plan fails LOUD (it never zips an empty directory).
- `data "external" "mcportal_grant_writer_stage"`: `program = ["python", "${path.module}/build_gw_stage.py"]`.
- `data.archive_file.mcportal_grant_writer.source_dir` reads `data.external...result.staged_dir`, so the zip is ordered after
  the build. No managed resource is upstream of the data source, so it is READ at plan time, not deferred (the property the
  old header comment demanded: a deferred data source leaves `source_code_hash` unknown on every plan).
- `.build/mcportal-grant-writer-staged/` and the zip are gitignored in the root's `.gitignore`: nothing built is committed.

The staged bytes still come from the manifest's `deployed_commit` (OG-gw-1), so the plan hash is the released closure's,
never the working checkout's. The header comment's manual "BUILD, then plan" step is replaced by this.

Rejected:
1. Commit a copy of `.build/staged` or of the zip (the root already tracks two liveness zips): a committed copy of a build
   drifts from its source and hides staleness -- CTO R1 ruled this out for the deployed bytes, and it is the same defect.
2. Make `build_package.py` output tracked: outside `<paths>` (a lambda-dir edit) and the same drift.
3. `terraform_data` / `null_resource` + `local-exec`: runs at APPLY, so the plan still has no input (and the old header
   records why a depends_on data source defers).
4. A documented "run the build first" plan step: the acceptance runs nothing first; it would fail, which is the defect.
5. Editing `build_package.py` to print JSON: out of `<paths>`; the wrapper does it in the root.

Cost: a third provider in `.terraform.lock.hcl` (one `terraform init` fetch from the registry that already serves the other
two; no PyPI, no vendor API), and `python` on the PATH of the planning device.

## 3. The layer (R3) -- chosen: reference the DEPLOYED version through a data source

`data "aws_lambda_layer_version"` by `layer_name = "mcportal-grant-writer-deps-layer"` (latest = version 1, the one the
function carries). The function's `layers` reads the data source's `arn`. The `aws_lambda_layer_version` resource and its
two build-output file reads are deleted: no rebuild, no PyPI.

CONTINGENCY (named now, measured at the plan): the resource was created by a Terraform apply (2026-09-29), so it is likely
in state; removing a managed resource from config plans a DESTROY of layer version 1 -- a change that cannot be removed
without an apply or a `removed`/`moved` block (both barred by the order). If the untargeted plan shows that destroy, this is a
BLOCKING row naming it, per the order, and the layer part is reported as not met rather than worked around.
