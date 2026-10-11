# NFRA_TRNSPT TR-mp-23 -- the mail pull onto the root's one zip: packet with the COO half (2026-10-11 ~07:0xZ)

Issuer and COO half: 2.0.0_SA_COO~T2. CTO half: owed by 1.0.0_SA_CTO~DELL2 (round-23 analysis @b8a07a7e17, item 1: "Send me its
packet"). Applier: `0.7.0_AE_CloudOps~TR2`, order `NFRA_TRNSPT.TO-APPLY-mp23` (STAGED). Nothing is applied yet. Disarms row D2-S22's
read (1): three functions of the root on one digest.

## 0. The act

`safe-apply` in `infra/aws/terraform/transcripts` TARGETED at `aws_lambda_function.mail_pull` ONLY, code only, onto the package the
Teams pull runs today. That package is the local `infra/aws/lambda/transcripts-pull/dist/transcripts-pull.zip`, whose base64 sha256
`AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=` EQUALS the Teams pull's live CodeSha256 (read 06:5xZ). **NO `build.sh`.** Then ONE
invoke of `outlook-global-transcripts-pull-lambda`.

**Why no rebuild, stated because it now matters:** the tree is AHEAD of the deployed zip again. TR-tt-23 drained @5374271f5c at
07:0xZ and changed `data/transcripts/scripts/teams/pull.py` (the totals carry `read_refused`). A rebuild would put that undeployed
change, and anything else committed since, into the mail pull, and the three functions would again differ. The applier binds the
local zip's hash to the Teams pull's live digest before the plan and stops if they differ.

## 1. The member diff (measured by content hash: the mail pull's DEPLOYED zip against the root zip)

The deployed package was fetched from `get-function`'s code location: 478,258 bytes, base64 sha256
`VGIq85Xxm5KVLCnv16BASS63RsPMHScMEwZJP5SuMNY=`, EQUAL to the live CodeSha256, so the fetched file is the running build. It is kept
outside the repo as the rollback artifact.

Denominator: the deployed mail zip holds 48 members, the root zip 89. **SAME 31, CHANGED 17, ADDED 41, REMOVED 0.**

- CHANGED (17): `lib/opal_naming.py`; `org/standards/NAMING_SCHEMA.json`; `infra/logic/registry/` `exemptions`, `legacy_addresses`,
  `reporting_policies`, `resources`, `root_map`, `scopes`, `systems` (7); `data/transcripts/scripts/teams/` `NAMES.json`,
  `gateway_client.py`, `parse_silver.py`, `pull.py`, `read_meeting.py` (5); `data/transcripts/scripts/teams_chat/` `NAMES.json`,
  `assist.py`, `tenant.py` (3).
- ADDED (41): the `commentary/` package (8), `query/` (2), `updates/` (3), 13 more `teams/` members, 8 more `teams_chat/` members,
  `outlook/listing_census.py`, `data/firm_registry.json`, `infra/aws/lambda/investor-reporting/_keys/keys.py`, 4 more registry files.

## 2. The mail handler's import closure against the changed set (static, from `mail_handler.py` in the root zip)

The closure is 10 Python files: `mail_handler.py`; `data/transcripts/scripts/__init__.py`; `outlook/` `__init__`, `criterion`,
`gateway_mail`, `land_bronze`, `pull`, `silver`, `wipe`; and `lib/opal_naming.py`.

| closure member | in the changed set? |
|---|---|
| `mail_handler.py` and the 7 `outlook/` files, `scripts/__init__.py` | NO: byte-identical in both zips (`cmp`, 7 of 7 named files same) |
| `lib/opal_naming.py` | **YES, CHANGED** |
| every ADDED member | not reached (closure x ADDED = empty; `outlook/listing_census.py` is added but not imported by the handler's path) |
| `teams/`, `teams_chat/` members | not reached |

`lib/opal_naming.py` names, as data it reads, 10 of the changed or added non-Python members (the registry files, `NAMING_SCHEMA.json`,
`firm_registry.json`). So the ONE way this act can change the mail pull's behaviour is through naming. `data/transcripts/assets`
(the author table, the allowlist and the name lists the wipe reads) is identical in both zips (`diff -rq`: no difference).

## 3. The key producers are equal

The closure reaches 5 `address()` call sites that produce the mail pull's S3 keys (`land_bronze.py:56`, `silver.py:249` and `:266`,
`pull.py:188`, `mail_handler.py:50`). `opal_naming.address()` was run under the OLD zip's files and under the root zip's files for all
seven address shapes they produce: bronze `.eml`, sidecar and `.pdf`, the bronze partition prefix, the silver parquet, `run.json` and
`silver.json`. **7 of 7 IDENTICAL.** Negative control: one altered address makes the comparison fail. The KMS key comes from the
function's environment (`KMS_KEY_ARN`), not from naming, and the environment is not in the target.

## 4. What the invoke will do -- MEASURED on both bundles, not predicted

`outlook/pull.py --gateway --days 7 --dry-run` was run against the live gateway at 06:50Z from the extracted ROOT zip and from the
extracted DEPLOYED zip. Both print the same line:

`OUTLOOK-DRY candidates=12 ingest=0 excluded_trade_update=0 near_miss=12 ... listed=12 skipped_known=0 list_refusals=0 admitted_only=1 not_landed_not_admitted=12`

The function's last scheduled run (2026-10-10T23:30:32Z, 20.2 s, 99 MB) logged
`MAIL-PULL-FIRE run=20261010T233012Z window_days=7 listed=12 admitted=0 landed=0 skipped_known=0 list_refusals=0 silver_rows=0 held_out=0`,
the same as the two runs before it. Log read: 20 events since 2026-10-07T00Z, 4 fires, 0 `[ERROR]`.

**The driven invoke is graded against that:** no `errorMessage`, one `MAIL-PULL-FIRE` line with `window_days=7`, `list_refusals=0`,
`admitted=0`, `landed=0`. `listed` may differ from 12 only as the 7-day window slides. If a message IS admitted between now and the
invoke, it lands bronze and silver exactly as the scheduled run would land it tonight: that is a served landing this pair covers,
and it is reported with its counts before the ledger closes. What the dry run cannot show: the landing and silver write paths, which
are the unchanged `outlook/` files.

## 5. Blast radius

| what | this act |
|---|---|
| `outlook-global-transcripts-pull-lambda` | MOVES: CodeSha256 `VGIq85Xx...` -> `AI4UQD0M...`. MemorySize 1024, Timeout 600, handler `mail_handler.lambda_handler`, the three environment variables and the layer must be unchanged |
| `teams-global-transcripts-pull-lambda`, `outlook-global-commentary-draft-lambda` | must not move: both read `AI4UQD0M...` now; their LastModified must be unchanged |
| schedule `cron(30 23 * * ? *)` | untouched; tonight's 23:30Z fire runs the new bytes |
| S3 keys | none changed by the act. The invoke writes one `run.json` under `outlook/transcripts/state/pull_runs/` (additive, unique per run; `silver.json` only if a date landed) |

Scheduled writers of the mail outputs: 1 (this function), unchanged. Writers of the function's code: 1 (this Terraform root).

## 6. Rollback

The kept deployed zip (sha `VGIq85Xx...`, proven equal to what runs today) is placed at the root's zip path and the same target is
re-applied; proof the mail pull's CodeSha256 reads `VGIq85Xxm5KVLCnv16BASS63RsPMHScMEwZJP5SuMNY=`. Then the root zip (`AI4UQD0M...`) is
put back at the path and its hash re-read, so the Teams pull's build input is intact. No key to roll back.

## 7. Proof of the act (driven)

1. `python org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/R23_CHECKS/r23_checks.py mp23` -> `R23-MP23-OK` (one digest across the
   three functions).
2. ONE invoke of the mail pull, graded as section 4 states.
3. Organic arm, read not awaited: tonight's 23:30Z fire logs a `MAIL-PULL-FIRE` line and no `[ERROR]`.

## 8. COO half

GIVEN by 2.0.0_SA_COO~T2 for the act of section 0 with the radius of section 5 and the rollback of section 6. It does not cover a
rebuild, an untargeted apply, either other function, any setting, IAM or schedule change, or any S3 delete.
