# MARKER STORM READ -- OG-m-1 (0.9.0_WK_NFRA_OPLGTW~13)

Read only, nothing written to AWS, chain never triggered. Window: `start` 2026-09-15T23:45:00Z, `end` 2026-09-28T23:45:00Z
(13 days, ending at the read time; the dispatcher log group holds 14 days). Machine record: `MARKER_STORM_READ.json`.
Every AWS call ran as `arn:aws:iam::313476888478:user/Andrew_Berman` through `.tools/aws`.

## 1. PUTs per date

`list-object-versions` on `s3://opal-data-assets/schwab/08335338/meta/complete/`, counted client-side:
195 versions on 19 keys in all time, 0 delete markers. Inside the window: **91 versions on 9 keys** (the other 10 keys
have none in the window; their last PUT was 09-15 or earlier).

| key (date=) | versions in window | first..last PUT (UTC) |
|---|---|---|
| 2026-09-15 | 11 | 09-16 09:46:07 .. 09-16 19:11:18 |
| 2026-09-16 | 10 | 09-17 09:46:08 .. 09:46:56 |
| 2026-09-17 | 10 | 09-18 09:46:08 .. 09:46:52 |
| 2026-09-18 | 10 | 09-19 09:46:07 .. 09:46:59 |
| 2026-09-21 | 10 | 09-22 09:46:08 .. 09:46:58 |
| 2026-09-22 | 10 | 09-23 09:46:09 .. 09:46:49 |
| 2026-09-23 | 10 | 09-24 09:46:10 .. 09:46:54 |
| 2026-09-24 | 10 | 09-25 09:46:08 .. 09:46:48 |
| 2026-09-25 | 10 | 09-26 09:46:08 .. 09:46:52 |

Each date's in-burst PUTs land inside 40 to 52 seconds. The 11th version on date=2026-09-15 (19:11:18Z on 09-16) is the one PUT
outside a 09:46 burst. Newest marker PUT in the bucket: 2026-09-26T09:46:52Z; none since.

## 2. What each PUT said (three newest dates: 09-23, 09-24, 09-25; 30 of 30 versions fetched, 0 errors)

Only `closure.status`, `emitted_at`, `run_id` and `len(written_tables)` were taken.

- Every date: 9 versions `incomplete` then 1 `qualified`, the `qualified` one last (the 10th, at 09:46:54, 09:46:48, 09:46:52).
- Sizes grow monotonically-ish 5,500 -> 16,5xx bytes (09-25: 5,500 .. 16,521). Two adjacent pairs have equal size
  (09-23: 15,720 twice; 09-25: 15,338 twice) but different `run_id` and `emitted_at`, so no two bodies are identical.
- `len(written_tables)` is 1 for most versions, 2 to 4 for a few; it does not rise steadily across a date, because the
  versions are written by concurrent producer runs (`run_id` stamps 09:46:06..09:46:50 are not in PUT order).
- 27 of 30 versions are `incomplete`; only 3 of 30 (one per date) are `qualified`.

So after OG-c-2's deploy (Lambda `opal-assets-silver-schwab` LastModified 2026-09-16T18:49:30Z), each date still writes
10 objects: the qualified-once rule stops a repeat write of an identical qualified closure only. Nine incomplete states
and the final qualified state are each new content, and each is a PUT.

## 3. Dispatches

`filter-log-events` on `/aws/lambda/advi-49f-gold-dispatch` over the window (all events, paginated; 735 events).
**104 invocations** (104 `START`, 104 `Event:`, 104 `dispatched:`, 104 `REPORT` lines; 0 orphan lines).

Join method: per log stream, ordered by timestamp, a `START RequestId` opens an invocation and every line up to its
`REPORT` belongs to it. Source comes from the `Event:` JSON, outcome from the invocation's own `ERROR:`/`OK:` line.

- By source: `aws:s3` 91, `advi.49f.scheduled-floor` 13, other 0. (104 of 104)
- By outcome: CHAIN REFUSED 48, CHAIN ABORT 33, UNKNOWN 15, CHAIN OK 0, other 8 (`OK: chain running past the poll
  budget`, the dispatcher returned before a terminal). (104 of 104)
- Host start, a flag rather than an outcome class: 24 of 104 invocations started the host.
- Crossed: `aws:s3` = REFUSED 48, ABORT 33, RUNNING-PAST-BUDGET 8, UNKNOWN 2; floor = UNKNOWN 13 of 13.
- The 91 `aws:s3` dispatches equal the 91 in-window marker versions, key by key (9 of 9 keys equal): one dispatch per PUT.
- **The dispatcher never returned CHAIN OK in the window (0 of 104).** All 13 scheduled floor runs, the production
  trigger, were logged `ERROR ... signature=UNKNOWN`.

## 4. The UNKNOWNs

15 UNKNOWN in the window; 5 read (both `aws:s3` UNKNOWNs, three floor runs). `get-command-invocation`, instance
i-01003b035d2988dfb:

| dispatch (UTC) | source | SSM Status | stdout bytes | `CHAIN ` terminal line in stdout | chain log first / last line |
|---|---|---|---|---|---|
| 09-16 19:11:18 | aws:s3 | Success | 24000 | no (only `CHAIN START`) | `CHAIN START date=2026-09-15 ...` / `CHAIN OK date=2026-09-15 wall=144.6s` |
| 09-16 12:45:15 | floor | Success | 24000 | no (only `CHAIN START`) | `CHAIN START date=2026-09-15 ...` / `CHAIN OK date=2026-09-15 wall=135.2s` |
| 09-27 12:45:14 | floor | Success | 24000 | no (only `CHAIN START`) | `CHAIN START date=2026-09-25 ...` / `CHAIN OK date=2026-09-25 wall=137.9s` |
| 09-28 12:45:15 | floor | Success | 24000 | no (only `CHAIN START`) | `CHAIN START date=2026-09-25 ...` / `CHAIN OK date=2026-09-25 wall=150.1s` |
| 09-23 09:46:20 | aws:s3 | Failed (rc 2) | 294 | no | `CHAIN START date=2026-09-22 ...` / `CHAIN ABORT stage=a00_dim_account rc=1 wall=0.7s -- nothing after this stage ran` |

Result of the test the order asked for. In 4 of 4 runs whose chain log ends `CHAIN OK`, the dispatcher was classifying
an output that did NOT carry the terminal line: `StandardOutputContent` is exactly 24,000 characters in each, the head
of the run (it holds `CHAIN START` and ends mid-run, at an `EMIT:`/`BUILD OK` line), and the terminal line is beyond it.
24,000 is the character cap SSM documents on this API (inferred from the documentation; measured here as 4 of 4 at
exactly 24000). `_classify` at `lambda_function.py:90-101` does scan every line, so the first-line reading in W4-S12 is
not the mechanism: the scan works on a truncated string. The fifth case is a different mechanism: a 294-byte stdout with
no `CHAIN ` line although its chain log ends `CHAIN ABORT`. Its first stdout line is
`python3: can't open file '/tmp/advi_49f_code/chain_49f_entrypoint.py'`, the host copy of the chain code was not there for
that stage (the dispatch did not start the host, `started_by_dispatcher` false, at 09:46:20, in a burst of 10).

Not measured: the chain-log terminal line for the 33 ABORT, 48 REFUSED and 8 running-past-budget dispatches (only the 5
UNKNOWNs above were paired).

## 5. Who writes the marker

`git grep -lE 'meta/complete'` over tracked `data/` and `infra/` code files, tests excluded: 7 files (matches the
drafting count). The string census MISSED two more writers because the producer builds the key without the literal:
`schwab_runtime.py` (two copies) calls `cm.build_complete_markers` and `cm.write_complete_marker_verified`
(`:234-238` event path, `:336-338` sweep path), and the PUT is at `conversion_manifest.py:274` through
`_write_closure_marker` (`:897`, `:908`), key from `complete_marker_key` (`:164`). No other file calls those functions
(census over `data/` and `infra/`, tests excluded).

| file | role | deployed bytes |
|---|---|---|
| `data/assets/scripts/silver/conversion_manifest.py` | writer | match (sha256 equals the Lambda package member, 43,257 bytes) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-schwab/conversion_manifest.py` | writer | match (same bytes) |
| `data/assets/scripts/silver/schwab_runtime.py` (missed by the string census) | writer | match (19,745 bytes) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-schwab/schwab_runtime.py` (missed) | writer | match (same bytes) |
| `infra/aws/ec2/opal-gateway/app/integrations/schwab/aws_roles.py` | reader | not measured, not a writer |
| `infra/aws/ec2/opal-gateway/app/integrations/schwab/catalog.py` | reader | not measured, not a writer |
| `infra/aws/terraform/opal-assets/advi_49f_floor.tf` | config | not measured |
| `infra/aws/terraform/opal-assets/silver.tf` | config | not measured |
| `infra/aws/terraform/opal-gateway/schwab_reader_iam.tf` | config | not measured |

Deployed package: `opal-assets-silver-schwab`, python3.11, CodeSha256 `v2BztqbuhHD3gH95eMqCQzkjPEotvSoeIezEOfsxu90=`
(equals the sha256 of the downloaded zip, 74,535 bytes, 12 members). 4 of 4 writer files equal the deployed bytes and
equal the HEAD blob.

Why about ten PUTs per date: the silver Lambda runs once per event batch, and each run composes the day's closure from a
fresh read and writes it (`schwab_runtime.py:234-238`), so a date converted by about ten concurrent runs is PUT about
ten times. Each run after the first sees a still-incomplete day until the last table lands.

## What a remedy would have to move

- The marker writer, `conversion_manifest.py` `_write_closure_marker` and its call sites in `schwab_runtime.py` (four
  files: `data/assets/scripts/silver/` copies and the `infra/aws/lambda/opal-assets/opal-assets-silver-schwab/` copies).
  The `data/assets/scripts/silver/*.py` source and its commit-to-deploy: DS lane (rule 13). The infra Lambda copies and the
  deploy of `opal-assets-silver-schwab`: DT/AE.
- The trigger, `silver.tf:758-763` S3 notification `advi-49f-silver-complete-accelerator`, and the `advi_49f_floor.tf`
  coupling: DT/AE (Terraform, PROD trigger). `terraform/opal-assets` is a multi-pipeline surface.
- The classifier, `advi-49f-gold-dispatch/lambda_function.py` (`_classify` `:90-101`, the SSM read it classifies): DT/AE
  (Lambda infra); rows S4, S5 and W4-S12 name the 49F ADVI chain's owners as its owner.
- The host-side chain code under `/tmp/advi_49f_code` and the SSM document `advi-49f-chain-dispatch`: DT/AE; the row for
  the 09-23 bootstrap failure is filed on the channel.
