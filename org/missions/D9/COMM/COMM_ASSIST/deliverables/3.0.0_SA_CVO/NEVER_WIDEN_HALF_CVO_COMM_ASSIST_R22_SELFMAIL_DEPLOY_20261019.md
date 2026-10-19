# CVO never-widen half -- COMM_ASSIST round 22, cell CA-p-2: deploy the mail handler that refuses mail Andrew sent (targeted `module.ldo_001`, code only)

**Author:** `3.0.0_SA_CVO` (base, laptop), 2026-10-19 ~17:1xZ, on `2.0.0_SA_COO~CA` msg 109843. **Read against:** the COO half
`org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R22_SELFMAIL_DEPLOY_20261019.md`
(b0782e1a73) at the PIN `e6c37673c8`. No CTO R22 half was on disk at this read.

## Blast radius, re-measured independently

| claim in the COO half | instrument (this seat) | result |
|---|---|---|
| the pin is on the trunk | `git merge-base --is-ancestor e6c37673c8 HEAD` | yes |
| the packaged-path diff `1aa63bde67..e6c37673c8` | `git diff --numstat` over every path `build.sh` copies (`handlers.py`, `modules/ldo`, `teams_chat/`, `daily_reports/eod`, `lib/opal_naming.py`, `NAMING_SCHEMA.json`, `infra/logic/registry/`), plus the transcripts root and `registry_files.txt` | `mail_requests.py` +17 -5, `exemptions.json` +11 -3, `legacy_addresses.json` +70, `opal_naming.py` +14 -9, `NAMING_SCHEMA.json` +13 -7; every other path 0, the Terraform root and the manifest included. Matches |
| the code change is what the half says | `git diff` of `mail_requests.py` | `_my_addresses()` reads `a.me()["mail"]`, lowercases it, and raises `me-without-mail` when empty; it is called ONCE per mail event before the loop; `considered()` refuses `from_andrew` after the sender parse and BEFORE the domain test; `REASONS` gains `from_andrew`. Nothing else in the file moves. Matches |
| **the raise does not fire on today's cache** (this seat's added read) | `me()` at the pin (`assist.py`:810-821) reads `state/me.json` once per container; `s3 cp` of that key (KEY NAMES and presence only, no value printed beyond the domain) | `me.json` (117 B, written 2026-10-02T15:29:20Z) carries `display_name`, `id`, `mail`; `mail` is non-empty with domain `opalinvest.com`. The `me-without-mail` branch is not reached on the cached answer. Condition 8 stands as the live check |
| the handler can read that key | the package's existing callers of `a.me()` at the pin (`tenant.py`:212, 264, 556, 710, 1205, 1401; `inbound_count.py`:307), all served by the same role `teams-global-chat-assist-role` | the key is already read on live paths of the same functions. An `iam simulate-principal-policy` read returned a templated resource (`${BucketName}/${KeyName}`) and is NOT relied on |
| the build | own sparse detached worktree at the pin (`C:/Users/AndrewBerman/Desktop/cvo_p2pin_e6c37673c8`, clean), `bash infra/aws/lambda/teams-chat-assist/build.sh` | 34 files, 241,267 B, base64 sha256 `p4kaI5t0i6vgzAZ0xONR/e8G9iDBU3icKNb3PvUdGEg=`, byte-identical to the issuer's build at `C:/Users/AndrewBerman/Desktop/p2pin_e6c37673c8`. The branch-A after-hash is that value |
| `check_p2_equiv.py` | `P2_PIN=e6c37673c8`, both modes, run by this seat ~17:1xZ | equiv: `P2-EQUIV ok=True differ=5 foreign=4 probes=17 same=17 p1=6 of 6`; live: `ok=False ... p1=1 of 6` on the served zip, the base. Matches |
| live pre-state | `.tools/aws lambda get-function-configuration`, both functions; `sqs get-queue-attributes` on `teams-global-chat-assist-dlq.fifo` | `CodeSha256` `RoH5DIiH/lWEutB+Qb3CswFUB402LhOjbx6P5sbk2DE=`, `CodeSize` 238923, LastModified 22:13:25Z / 22:13:31Z, 15 keys, `INGRESS_MARK_MODE=enforce`, both; dead-letter queue 0 and 0. Matches |
| rollback commit's mode default | the empty numstat over the transcripts root; `chat_assist.tf`:41 at the pin | `enforce` |
| disk | `df -h` on `C:` | 37 GB free. Meets the 5 GB precondition at this read |

## Expected outcome

The COO half's branches A and B, exactly. A: targeted `0 to add, 2 to change, 0 to destroy` on
`module.ldo_001.aws_lambda_function.handler` and `.ingress[0]`, changed keys a subset of {`source_code_hash`, `last_modified`},
after-hash `p4kaI5t0i6vgzAZ0xONR/e8G9iDBU3icKNb3PvUdGEg=`; anything else is B and applies nothing. Rollback per the COO half: the
saved live `RoH5DIiH...` zip and a targeted apply from a detached worktree at `1aa63bde67`. The one state write is the `from_andrew`
count, which the old code tolerates.

## Behaviour the half names and this seat confirms

- `_my_addresses()` runs before the loop, so an unreadable or mail-less `/me` fails the WHOLE mail event, colleague mail included,
  until it is fixed (the event retries, then dead-letters). The cache is per container and read once, so a good cache now stays good
  for the container's life. This is the COO half's third residual; condition 8 is its trip-wire.
- A mail Andrew sends from an alias or a second address is not refused (the COO half's first residual).

## Conditions

The COO half's eight are adopted, the one-sitting condition and condition 8 included. None added.

**SIGNED** -- `3.0.0_SA_CVO`
