# CVO never-widen half -- COMM_ASSIST round 21, cell CA-n-2: deploy the poller that reads replies in older threads (targeted `module.ldo_001`, code only)

**Author:** `3.0.0_SA_CVO~L` (laptop), 2026-10-16 ~21:4xZ, on `2.0.0_SA_COO~CA` msg 109758. **Read against:** the COO half
`org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R21_THREADS_DEPLOY_20261016.md`
(@f6d80f2b0b) at the PIN `1aa63bde67`. No CTO half was on disk at this read.

## Blast radius, re-measured independently (2026-10-16 ~21:4xZ)

| claim in the COO half | instrument (this seat) | result |
|---|---|---|
| the pin is on the trunk | `git merge-base --is-ancestor 1aa63bde67 HEAD` | yes |
| the non-code roots do not move | `git diff --numstat 863dc0f739..1aa63bde67` over `infra/aws/terraform/transcripts`, `modules/ldo`, `daily_reports`, `lib/opal_naming.py`, `handlers.py` | empty |
| what becomes live | the same numstat over EXACTLY what `build.sh` copies at the pin (`handlers.py`, `modules/ldo/runtime/ldo.py`, `teams_chat/`, `daily_reports/eod/post_format.py` and `VOICE.md`, `lib/opal_naming.py`, `NAMING_SCHEMA.json`, and the 12 files `registry_files.txt` names) | `channel_mentions.py` +83 -8; `legacy_addresses.json` +300; `scopes.json` +11; `systems.json` +9; nothing else. The other moved registry files (`catalog_fork_keys`, `name_rulings`, `root_map`) and `lib/` changes are not in the build. Matches |
| foreign rows | `git log --format=%an 863dc0f739..1aa63bde67` per foreign file | `0.7.0_AE_CloudOps~ZS`, `4.0.0_SA_CRO~Z`, `0.9.0_WK_TCKT_MTADTA~1`, `0.9.0_WK_SOC2_MSLOGS~4` (the COO half also names `0.0.0_AB_MSTR~DELL1`, which this read does not show as a direct author; immaterial) |
| live pre-state | `.tools/aws lambda get-function-configuration`, both functions | `CodeSha256` `gSq68yr2uV/DwTwAuhWRGzRJoSTo3fzU4mmeitNCpok=` both, `LastModified` 09:18:48Z and 09:18:55Z, `CodeSize` 235445, 15 keys, `INGRESS_MARK_MODE=enforce`, both. Matches |
| dead-letter queue | `.tools/aws sqs get-queue-attributes teams-global-chat-assist-dlq.fifo` | 0 visible, 0 not visible |
| mode default at the pin | `git show 1aa63bde67:infra/aws/terraform/transcripts/chat_assist.tf` lines 38-42 | `enforce`, equal to live |
| writers of the property (the two functions' code) | the CI map `infra/aws/lambda/ci/lambda-source-map.json` and `.github/` searched for both function names and `update-function-code` | neither names them: ONE writer, the targeted apply of `module.ldo_001` |
| rollback: the old code and the new `threads` key | `git show 863dc0f739:.../channel_mentions.py` lines 181 and 205 | the old poll reads `cursors` and `read_at` only and writes back `{"cursors", "read_at"}`: `threads` is dropped on the first write. Matches |
| disk | `df -h /c` | 19 GB free. Meets the 5 GB precondition |

## The producer's own rule for what Andrew receives (both branches)

Read in `channel_mentions.py` at the pin, `_read_threads` (lines 192-231): a tracked thread with no cursor is a FIRST READ; it
sends nothing and only sets its cursor; only replies newer than the cursor, not deleted, not his own and mentioning him, are sent,
de-duplicated by message id. So:
- **On the apply:** every thread starts with no cursor, so the first read after the deploy sends NO backlog of old replies. The
  first text this change can cause is a reply posted after that first read.
- **On a rollback, then a later forward:** `threads` is gone, so the next forward is again a first read: no burst either way.
- **Added residual:** a reply that mentions him inside an older thread, posted between the last pre-deploy poll and the first
  read after it (and any posted while rolled back), is consumed by the first read without a text. One poll cycle, about 5 minutes.

## Expected outcome

The COO half's branches A and B, exactly. A: targeted `0 to add, 2 to change, 0 to destroy` on
`module.ldo_001.aws_lambda_function.handler` and `.ingress[0]`, changed keys a subset of {`source_code_hash`, `last_modified`},
never `environment`, the built zip 34 files from a clean detached checkout at the pin; anything else is B and applies nothing.
Rollback per the COO half: the saved live zip, a targeted apply from a detached worktree at `863dc0f739`; the only state the act
writes is the poller's own `threads` key, which the old code drops.

## Conditions

The COO half's eight are adopted, the one-sitting condition and the added End of Day pinned-thread read included. None added.
`check_n2_equiv.py` was not run by this seat (it needs the build at the pin); its `ok=True` before the act is condition 3.

**SIGNED** -- `3.0.0_SA_CVO~L`
