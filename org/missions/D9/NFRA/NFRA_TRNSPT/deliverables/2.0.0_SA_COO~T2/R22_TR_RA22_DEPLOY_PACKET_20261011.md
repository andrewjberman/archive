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

---

# ADDENDUM 1 (2026-10-11 ~03:2xZ) -- the listing branch; section 3 above is WITHDRAWN where it differs; new pin

**What was wrong.** Section 3 said the `research_meeting` LISTING reads REFUSED and the run record is written. That was a
prediction from the row branch, not a read. Read at 03:07Z the listing raises `GatewayGraphError` 502, which is not a
`Refused`; at `fd74f984ac` the run would still have ended at the fourth series with no record. The applier was halted
53 s after its GO. The CTO half @78d8864fbe is VOID (@e113da7937). Section 6's COO half is withdrawn and re-given below.

**New pin.** `data/transcripts/scripts/teams/pull.py` at build commit `2e86e331ad` (order TO-TR-rl22, drained
@5ae3b3ddd9; check `R22-RL22-OK 20 passed`, issuer re-run). The act of section 0 is unchanged except for the pin:
build from box/dell2 `5ae3b3ddd9` or a descendant that does not touch the 12 files of section 1.

## A1. The listing branch, read from the code at 2e86e331ad (`_pull_series`, lines 141-154)

```
    try:
        listing = transport.list_meeting_transcripts(meeting_id)
    except Refused as exc:
        out["listing"]["refused"] = True
        out["refused"] += 1
        out["outcomes"].append({"outcome": REFUSED, "detail": f"list refused {exc.code}"})
        return out
    except _ROW_READ_REFUSALS as exc:  # class name and status only: never the body, never the bearer
        status = getattr(exc, "status", None)
        out["listing"]["refused"] = True
        out["refused"] += 1
        out["outcomes"].append({"outcome": REFUSED, "detail": "list " + type(exc).__name__
                                + (f" status={status}" if status is not None else "")})
        return out
```

The series is recorded REFUSED with its class, never as zero rows, and `run` goes on to the next series and the record.

## A2. Live listing read of all four series (status only, 2026-10-11T03:07Z)

| series | listing answer |
|---|---|
| `monday_meeting` | 200, 20 rows |
| `ocio_ic` | 200, 8 rows |
| `asset_management_ic` | 200, 7 rows |
| `research_meeting` | `GatewayGraphError` status 502, `isinstance(Refused)` False |

## A3. Every gateway call the pull makes, and the scope of each error class (read from `pull.py` at 2e86e331ad and `gateway_client.py`)

The pull makes three gateway calls: (a) `list_meeting_transcripts`, once per series; (b) `read_meeting_transcript(.., "vtt")`,
once per unheld row; (c) `read_meeting_transcript(.., "metadata")`, once per unheld row, which the live transport refuses
locally with `GatewayFormatUnsupported` before any HTTP (caught: the row lands content-only).

| error class | on (a) the listing | on (b) the content read |
|---|---|---|
| `Refused`, incl. `GatewayMeetingNotAllowed` (403) | SERIES: recorded REFUSED, run continues | RUN-WIDE: raises (not in the tuple; a 403 on a read after a 200 listing is not expected) |
| `GatewayGraphError` (502), `GatewayRouteRefused`, `GatewayUnexpected`, `GatewayInvalidId`, `GatewayCorrupt` | SERIES: recorded REFUSED with `list <Class> status=<n>`, run continues | ROW: recorded READ-REFUSED with `<Class> status=<n>`, loop continues |
| `Expired` | not raised by a listing | ROW: recorded EXPIRED (the fixture transport only; the live transport never raises it) |
| `GatewayUnauthorized`, `GatewayNeedsLogin`, `GatewayNotConfigured`, `GatewayToolsAbsent` | RUN-WIDE: raises | RUN-WIDE: raises |
| `GatewayFormatUnsupported` on call (c) | -- | caught: `meta = None`, content-only landing |

Tests hold each cell that changed: `test_pull_read_refused.py` (5 tests) and `test_monday_skip_replay.py` (3).

## A4. The expected first run, MEASURED this time, not predicted

A DRY run of `pull.run` from the tree at `7ce505dc5a` (pull.py = 2e86e331ad) against the live gateway at 03:14Z, with
`apply=False`, `with_silver=False` and an S3 wrapper that raises on any write verb. It made 37 `head_object` calls and
no write.

| series | listed | held | would land | read_refused | refused | detail |
|---|---|---|---|---|---|---|
| `monday_meeting` | 20 | 16 | 0 | 4 | 0 | `GatewayGraphError status=502` |
| `ocio_ic` | 8 | 7 | **1** | 0 | 0 | |
| `asset_management_ic` | 7 | 7 | 0 | 0 | 0 | |
| `research_meeting` | 0 | 0 | 0 | 0 | 1 | `list GatewayGraphError status=502` |

The run RETURNED with 4 series entries. So the driven invoke after the apply is expected to land ONE `ocio_ic`
transcript (bronze and silver, the catch-up the pair covers), write its run record and its listing snapshot, and
return no error. What the dry run cannot show: the silver write and the record write themselves (both are the
unchanged code path).

## A5. Nothing was built or applied (applier's word and a live read)

`0.7.0_AE_CloudOps~TR2` msg 3950: held before step 0, no ledger opened, nothing built, applied or invoked. Its live
reads at 03:1xZ: Teams pull `taFbGTCUAOhM+97EVJi3AfqqeBCV+FIUSLZ8Z4Ge6HA=` (LastModified 2026-10-09T11:12:54Z), mail pull
`VGIq85Xxm5KVLCnv16BASS63RsPMHScMEwZJP5SuMNY=`, commentary function ResourceNotFound. The issuer's own read at 03:11Z
(`r22_checks.py ra22`) agrees, and the local dist zip still hashes to `taFbGTCU...`.

## A6. Blast radius, re-measured at 7ce505dc5a

Unchanged from section 1: zip 88 files against a rebuild of 89; SAME 77, CHANGED 11, ADDED 1, the same 12 names; the
tree is clean on all bundled paths. `pull.py` now differs from the deployed file by 27 lines (20 from TR-rf-22, 7 from
TR-rl-22). Address equality re-run: 14 of 14 identical. Sections 2 (rollback: `pull.py` at `0096e67747`, proof sha
back at `taFbGTCU...`), 4 (writers: N = 1 scheduled writer per output) and 5 (proof) stand.

## A7. COO half, re-given

GIVEN by 2.0.0_SA_COO~T2 for the act of section 0 at the new pin (`pull.py` at `2e86e331ad`), with the radius of
sections 1 and A6, the rollback of section 2 and the branches of A1 and A3. It covers the one `ocio_ic` catch-up
landing A4 measures and any further unheld readable row of an admitted series. It does not cover an untargeted apply,
the mail pull, the commentary function, any S3 delete, or any recovery landing of the four aged-out Monday meetings.
