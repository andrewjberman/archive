# OG-tf-1 -- TF_ROOT_FIX (0.9.0_WK_NFRA_OPLGTW~17, round 14)

STATUS: **STOPPED at order step 4 (row Z-W15-S25) -- CONTENT-DIFF.** The root fix (items 1 and 3 of the cell) is NOT
written, because AC2 cannot pass without an apply this cell may not make. Row: `NFRA_OPLGTW-Z-W17-S2` (BLOCKING, ARMED,
disarm_owner `2.0.0_SA_COO~O`). Item 2 (hygiene) is independent of the diff and was done.

## 1. S25 classification (CLAUDE.md rule 22a: by content, never by hash)

Instrument: `aws lambda get-function --function-name mcportal-grant-writer-lambda` -> `Code.Location` (a presigned URL), fetched and
unzipped IN MEMORY (never written to the repo), per-file sha256, compared with `build_package.py`'s staged output at this
worktree's HEAD `544b8e2466` (the build input the root's `archive_file` zips). Deployed `LastModified` 2026-09-30T10:58Z,
`CodeSha256` `nhz+dwJs...`, 54650 bytes.

Denominator: 11 files deployed, 11 files staged, same 11 names. 8 SAME, **3 DIFF**, 0 only-deployed, 0 only-staged.

| file (repo-relative, inside the zip) | deployed sha256[:12] | staged sha256[:12] | bytes deployed -> staged |
|---|---|---|---|
| `infra/aws/ec2/opal-gateway/app/config.py` | 7244283c201a | 3128d463bd6f | 27507 -> 29788 |
| `infra/aws/ec2/opal-gateway/app/data_entitlement.py` | c12839d856ec | a9eafa664374 | 31834 -> 32133 |
| `org/standards/NFRA_OPLGTW_CONTRACT.json` | f47703a611e5 | a86f7e667cfc | 8806 -> 9189 |

Line-ending control: neither side carries a CR byte (python `bytes.count(b'\r')` = 0 on all six; the `.gitattributes` eol rule
holds), and the LF-normalised bytes differ, so these are not zip-metadata, ordering or line-ending diffs. The size deltas are
real text. (The zip entry timestamps are the fixed 2049-01-01 epoch on the deployed side: the archive IS already deterministic;
nothing about ordering or metadata is in play.)

**Classification: CONTENT-DIFF.** Cause, from `git log` on the three paths: the gateway tree advanced after the 2026-09-30T10:58Z
deploy -- `db92656c72` (10-02, /hx/teams), `1afce6312e` and `2fbc683db9` (10-01, /hx/mail, /hx/transcripts) on `config.py`;
`adc979b13b` (10-01) and `9fcd257fbd` (09-30 22:31 -04) on `data_entitlement.py`; the contract JSON moved at `32ebe6bee6`
(09-30 05:48 -04, dim_transaction). CONTROL: each deployed file is byte-identical to an OLDER committed blob (`git hash-object` equality, searched back through `git log -- <file>`): `config.py` = `c19f86c295` (09-30 03:26 -04), `data_entitlement.py` = `aac92bdff8` (09-30 05:57 -04), contract JSON = `c2f5d5a071` (09-30 02:10 -04) -- so the deployed package is a clean build of an earlier HEAD and the repo has since moved past it; no hand edit, no foreign bytes. The Lambda's import closure reads the gateway
tree at the building checkout, so every gateway edit that touches `app.config` / `app.data_entitlement` / the contract changes
the Lambda's staged package without any edit to the Lambda itself.

Consequence: any root that archives the staged build of HEAD plans `source_code_hash` as a change on
`aws_lambda_function.mcportal_grant_writer` (the OG-rl-3 observation), and applying it would redeploy the grant writer with
code that has never been released there. The targeted grant-writer plan (AC2) therefore reads `~ update in-place`, not "No changes",
for ANY mechanism that archives HEAD's closure. The only mechanisms that read No changes either (a) deploy (apply -- barred) or
(b) pin the archive to the DEPLOYED bytes (a committed copy of a build, which is the repo drifting from its own source and
hides the staleness) -- (b) is a shadow of the deployed artifact, not a fix, and is not mine to choose.

## 2. What was NOT done, and the mechanism the follow-on cell can take (not implemented)

Not written, so nothing below is a claim about a working fix. The two errors the cut measured are variables with no default
(`mcportal_owner_key_claim`, `mcportal_owner_key`). Where the values live today: the live Lambda's environment only
(`MCPORTAL_OWNER_KEY`, `MCPORTAL_OWNER_KEY_CLAIM` present; no Secrets Manager secret or SSM parameter carries them --
`list-secrets` name filter on mcportal/owner/grant returns only `teams/global/owner-phone`, `describe-parameters` filter
`mcportal` returns 0). Candidate mechanisms, smallest first:

1. `data "aws_lambda_function"` reading the live function's own environment into the `environment` block (no variable, no
   literal, no secret in the repo; the plan reads the value, never prints it). Moves nothing live. Cost: the value becomes
   self-referential (terraform can no longer be the place a change to it is made), and it fails on a fresh account. Needs
   `lambda:GetFunction` (held: this worker's own read above succeeded).
2. `lifecycle { ignore_changes = [environment] }` + a placeholder default. Moves nothing live, but stops terraform governing the
   owner config at all, and a placeholder default is the "boot with an empty/wrong owner" the variable's own text refuses.
3. A new Secrets Manager secret + data source: moves a live resource set (creates a secret) -- outside "changes nothing live".

Rejected without trying: a literal default (a personal identifier committed -- barred); `TF_VAR_*` in the checks (the cell says
none); `removed`/`moved` (barred).

The archive/layer inputs (`.build/staged`, the layer zip) are the second failure behind the variables: `.build/staged` is
generated by `build_package.py` and is NOT ignored (git status shows it untracked; row Z-W17-S3); the layer zip's build is
`requirements.txt` -> wheels (network egress to PyPI), not a repo file. Both are decisions for the follow-on cell, after the
CONTENT-DIFF is dispositioned.

## 3. Item 2 -- hygiene (done, independent of the diff)

Untracked (`git rm --cached`): `tfplan`, `tfplan.r8`, `.build/alert-channels.tfplan`, `.build/otp-liveness.tfplan`, and the three
`org/mcp/agent_telemetry/*.jsonl` inside the root. `infra/aws/terraform/opal-gateway/.gitignore` added with `tfplan*`, `*.tfplan`
and `/org/`, so plans and the stray tree cannot be re-committed here.

## 4. Item 3 -- the untargeted plan summary

Not recorded: it needs the root to plan, which needs the item-1 fix. The cut's own measurement stands (plan rc 1, 2 errors, both
"No value for required variable"; `r13/checks/tf.AC1.sh`). The OG-rl-3 plan (row Z-W15-S25) is the last untargeted summary on record.
