# CVO never-widen half -- COMM_ASSIST round 20, cell CA-l-4: deploy the narrower package (targeted `module.ldo_001`, code only, registry files 17 -> 12)

**Author:** `3.0.0_SA_CVO` (base, laptop), 2026-10-15 ~08:4xZ, on `2.0.0_SA_COO~CA` msg 109375. **Read against:** the COO half
`org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R20_NARROW_DEPLOY_20261015.md`
(4804840be6) at the PIN `863dc0f739`. No CTO half was on disk at this read.

## Blast radius, re-measured independently

| claim in the COO half | instrument (this seat) | result |
|---|---|---|
| the pin is on the trunk | `git merge-base --is-ancestor 863dc0f739 HEAD` | yes |
| the packaged-path diff `93a3f55d25..863dc0f739` | `git diff --numstat` over every path `build.sh` copies, plus the transcripts root and `modules/ldo` | `build.sh` +10 -1 and `registry_files.txt` +15 (build inputs, not packaged), `legacy_addresses.json` +100, `reporting_policies.json` +2 -1. No code file, no Terraform path. Matches |
| the manifest drops exactly five files | `registry_files.txt` at the pin vs `git ls-tree infra/logic/registry/` (17 files) | 12 kept; the five left out are `catalog_fork_keys`, `event_rules`, `key_rulings`, `name_rulings`, `root_map`. Matches |
| **the named residual: a dropped file opened on a path the 17 probes miss** | `git grep` of each dropped name over every packaged code path (`lib/opal_naming.py`, `teams_chat/`, `handlers.py`, `ldo.py`, `daily_reports/eod`) at the pin; then the readers of `REGISTRY_DIR` in `opal_naming.py` | `catalog_fork_keys`, `event_rules`, `key_rulings`: 0 references. `name_rulings` (:3499-3534) and `root_map` (:3766-3814) are read only by the census and the `--root` command, each through a lazy `import opal_naming_rootcheck`, a module `build.sh` never packages, so those paths could not run in the served zip before this act either. `REGISTRY_FILES` (:54-56, the 11 files the builder loads) is a subset of the manifest's 12 (the 12th is `mail_parties.json`, the assistant's own). The one directory walk, `registry_file_names()` (:269-273), feeds only an unscoped `registry_hash()`, whose callers are the generators and the command line (:2774, :3644, :3783, :3797); no packaged assistant module calls `registry_hash` or `registry_file_names`. The residual is narrower than the COO half states, and no reachable path that this static read can see opens a dropped file |
| live pre-state | `.tools/aws lambda get-function-configuration`, both functions | `CodeSha256` `nQlJW0j/a2nE1om0ZbXm9CTMxAVDXwUQNju62S4xa9k=`, `CodeSize` 320236, 15 keys, `INGRESS_MARK_MODE=enforce`, both. Matches |
| rollback commit's mode default | read at round 19 (this seat's R19 half, `chat_assist.tf`:41 at `93a3f55d25`) and confirmed unchanged by the empty numstat over the transcripts root | `enforce` |
| disk | `df -h` on `C:` | 13 GB free (95% used). Meets the 5 GB precondition at this read |

## Expected outcome

The COO half's branches A and B, exactly. A: targeted `0 to add, 2 to change, 0 to destroy` on
`module.ldo_001.aws_lambda_function.handler` and `.ingress[0]`, changed keys a subset of {`source_code_hash`,
`last_modified`}, built zip 34 files; anything else is B and applies nothing. Rollback per the COO half: the saved live zip,
a targeted apply from a detached worktree at `93a3f55d25`, never from `afa8752f44`. The act writes no state.

## Conditions

The COO half's seven are adopted, the one-sitting condition included. None added.

**SIGNED** -- `3.0.0_SA_CVO`
