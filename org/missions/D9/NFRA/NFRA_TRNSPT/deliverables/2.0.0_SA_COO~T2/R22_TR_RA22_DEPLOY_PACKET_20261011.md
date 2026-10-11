# NFRA_TRNSPT TR-ra-22 -- deploy packet for the Teams pull fix, with the COO half (2026-10-11 ~03:1xZ)

Issuer and COO half: 2.0.0_SA_COO~T2. CTO half: owed by 1.0.0_SA_CTO~DELL2 (msg 3934: signed or refused on this packet).
Applier: `0.7.0_AE_CloudOps~DELL2`, under a change-management ledger entry opened at start. Nothing is applied yet.

## 0. The act

Rebuild `infra/aws/lambda/transcripts-pull/dist/transcripts-pull.zip` with `build.sh` at box/dell2 `fd74f984ac` (or a
descendant that does not touch the 12 files of section 1), then `safe-apply` in `infra/aws/terraform/transcripts`
TARGETED at `aws_lambda_function.pull` ONLY, then ONE invoke of `teams-global-transcripts-pull-lambda` as the driven
proof. The fix itself: build commit `12c64f3c1f` (order TO-TR-rf22, check `R22-RF22-OK 18 passed`, issuer re-run; the
transcripts suite 433 passed, 1 collection error in `test_eod_voice.py` that this change does not touch).

## 1. Blast radius

**Bytes that move (measured: the deployed zip against a rebuild from the tree at fd74f984ac, by content hash).**
The live function's CodeSha256 `taFbGTCUAOhM+97EVJi3AfqqeBCV+FIUSLZ8Z4Ge6HA=` EQUALS the local zip's, so the local zip
is the deployed build input. Denominator: the zip holds 88 files, a rebuild bundles 89. SAME 77, CHANGED 11, ADDED 1,
REMOVED 0.

| file | class | reaches the Teams pull's code path? |
|---|---|---|
| `data/transcripts/scripts/teams/pull.py` | CHANGED, 20 lines: the fix | YES -- the change this act is for |
| `data/transcripts/scripts/teams/census.py` | ADDED | no (a seat CLI; the handler does not import it) |
| `data/transcripts/scripts/teams/NAMES.json` | CHANGED: one added block, `silver_reader` role and policy names | no (read by `readers.tf`, not by the pull) |
| `data/transcripts/scripts/teams_chat/{assist,channel_mentions,mail_requests,tenant}.py` (4) | CHANGED | no (the handler imports `teams.gateway_client`, `teams.land_bronze`, `teams.pull` only; none names `teams_chat`) |
| `lib/opal_naming.py`, `infra/logic/registry/{legacy_addresses,name_rulings,reporting_policies,scopes}.json` (5) | CHANGED | YES -- they compute every address the pull writes; see the equality below |

**Address equality (the control for the five naming files).** `opal_naming.address()` was run under the deployed
zip's files and under the tree for the pull's write families: bronze `.vtt` and sidecar and silver `.parquet` for
each of the 4 series, the run record and the listing snapshot. 14 of 14 addresses IDENTICAL. Negative control: one
altered address makes the comparison fail.

**Keys the changed pull may write** (all in bucket `opal-data-transcripts`, all `address()` output):

| family | key shape | changed by this act? |
|---|---|---|
| bronze | `teams/transcripts/bronze/<series>/date=<D>/<transcript_id>.*` | no: same rows as before, for a row that reads |
| silver | `teams/transcripts/silver/<series>/date=<D>/<transcript_id>.parquet` | no |
| run record | `teams/transcripts/state/pull_runs/run=<started>/run.json` | YES: it is now WRITTEN on every fire (the failed fires wrote none); each series entry gains `read_refused` and `READ-REFUSED` outcomes |
| listing snapshot | `teams/transcripts/state/listing_snapshots/run=<started>/listing.json` | YES: now written on every fire |

It deletes nothing and overwrites nothing: a held row is skipped before any read, and state keys are unique per run.

**Schedules and task families that pick up the new bytes.**

| function (same zip in the stack) | live state | this act |
|---|---|---|
| `teams-global-transcripts-pull-lambda`, rule `teams-global-transcripts-pull-hourly` `cron(0 13-22 ? * MON-FRI *)` | sha taFbGTCU... (2026-10-09T11:12Z) | MOVES -- the target |
| `outlook-global-transcripts-pull-lambda`, `cron(30 23 * * ? *)` | sha VGIq85Xx... (2026-10-07T23:59Z), a different, older zip | MUST NOT MOVE: the apply is targeted. An untargeted apply would move it to all 12 changed files |
| `outlook-global-commentary-draft-lambda` | ResourceNotFound: declared, not applied. Open ledger `irpt-anlreq-t1-commentary-store-and-lambda-20261009` (another seat) | MUST NOT BE CREATED by this act: targeted. NOTE for that seat: after this rebuild the shared `dist/` zip is the fd74f984ac build |

No ECS task family and no other schedule reads this zip (the stack's `chat_assist.tf` uses its own zip).

## 2. Rollback, per key

| what | rollback |
|---|---|
| the function's code | rebuild the zip with `pull.py` at `0096e67747` (the pre-fix blob) and re-apply the same target; the proof is CodeSha256 back at `taFbGTCU...6HA=` (reproducible: the build uses fixed timestamps) |
| bronze and silver objects landed after the act | none needed: they are the objects the old code lands for a readable row. The bucket is versioned |
| `run.json` and `listing.json` per run | none needed: additive, unique per run, read by no served consumer. Removing one is an S3 delete and would be Andrew's call |

Same-window: the applier finishes or rolls back in session; the ledger closes on the driven invoke's result.

## 3. Both branches, read from the code at fd74f984ac (`pull.py` `_pull_series`)

- **A transcript that reads (200):** unchanged path. Not held -> `read_meeting_transcript` returns -> `land_bronze.land`
  (or `_land_content_only`) -> outcome `LANDED`, `landed += 1` -> silver parse and write with the same wipe and
  hold-out. Held -> `HELD`, skipped before any read.
- **A transcript whose content read is refused (502 `GatewayGraphError`; also `GatewayRouteRefused`,
  `GatewayUnexpected`, `GatewayInvalidId`, `GatewayCorrupt`):** `read_refused += 1`, outcome
  `{"transcript_id", "outcome": "READ-REFUSED", "detail": "<class> status=<n>"}`, `continue`. Nothing is written for
  that row. The loop reaches the next row, the next series, then the run record and the snapshot.
- **Run-wide refusals still end the run:** `GatewayUnauthorized`, `GatewayNeedsLogin`, `GatewayNotConfigured`,
  `GatewayToolsAbsent`, and `GatewayMeetingNotAllowed` on a content read. A refused LISTING keeps its handling
  (the series is recorded `REFUSED`, the run continues), which is how `research_meeting` reads today.
- **Expected first fire after the act, from this rule and the 02:44Z read:** `monday_meeting` 20 listed = 16 held +
  4 `READ-REFUSED` (2026-04-10, 04-13, 05-04, 06-01) + 0 landed unless a new meeting exists; then `ocio_ic` and
  `asset_management_ic` are listed for the first time by the schedule (their aged-out rows, if any, read
  `READ-REFUSED`; any unheld readable row LANDS -- that is the intended catch-up and it is a served landing this pair
  covers); `research_meeting` listing `REFUSED`. Run record written.

**Stated limit:** the handler's `totals` and the fire's log line do not carry `read_refused` (the worker could not
edit the two test files that pin the totals). The count is in `run.json` per series. A later cell widens the totals.

## 4. Writers of each named output (printed)

| output | scheduled writers | seat-run writers (not scheduled) |
|---|---|---|
| Teams bronze keys | 1: `teams-global-transcripts-pull-lambda` | `pull.py --apply`, `land_bronze.py` CLI |
| Teams silver keys | 1: the same function (`with_silver=True`) | `backfill_silver.py`, `rewipe_silver.py`, `research_fold.py`, `parse_silver.py` CLI |
| `state/pull_runs`, `state/listing_snapshots` | 1: the same function | `pull.py --apply` |

N = 1 scheduled writer per output; its one rule is section 3. The seat-run CLIs are not run by this act.

## 5. Proof of the act (driven, not waited for)

1. `get-function-configuration`: CodeSha256 differs from `taFbGTCU...` and equals the rebuilt zip's hash; the mail
   pull's sha is still `VGIq85Xx...`; the commentary function is still absent.
2. ONE invoke of the function: it returns a run record (no `errorMessage`), `series` has 4 entries, `state_key` is
   set and the object exists; `monday_meeting` shows `read_refused` 4.
3. Organic arm, read not awaited: the Monday 2026-10-12 13:00Z fire's REPORT line has no `[ERROR]`.

## 6. COO half

GIVEN by 2.0.0_SA_COO~T2 for the act of section 0 with the radius of section 1 and the rollback of section 2, against
`pull.py` at `fd74f984ac`. It does not cover an untargeted apply, the mail pull, the commentary function, or any
recovery landing of the four aged-out meetings.
