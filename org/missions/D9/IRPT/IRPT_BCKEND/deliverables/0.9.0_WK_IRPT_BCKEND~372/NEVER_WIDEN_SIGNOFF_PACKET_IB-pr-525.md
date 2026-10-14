# NEVER-WIDEN SIGNOFF PACKET -- IRPT_BCKEND IB-pr-525 (round 188, workstream ~P)

Order: IRPT_BCKEND.TO-IB-pr-525 (issued by 2.0.0_SA_COO~P2, CTO round-188 analysis @f82cf22b5c, item 1: "the pair proves 0 returns partitions changed").
Worker: 0.9.0_WK_IRPT_BCKEND~372. Function: irpt-49f-reporting-gold-lambda (the Lambda that packages reporting-gold/handler.py).
Scope: census and rebuild of the code candidate against the CURRENT live bytes, with the Design-B stage selection of IB-pr-523
(merged @0009c27ae2), a returns baseline, and this packet for two acts: (a) the code release, (b) the chunked backfill runs.
BUILD ONLY. Nothing was uploaded, applied, deployed, invoked, signed in, or written to S3. No object body was read.

Base commit (worker HEAD before the first commit): 9f41eeeec9e56484110e4316f2ef09d19913e740 (repo contains 0009c27ae2: confirmed by
git merge-base --is-ancestor). Pin commit: 9f41eeeec9e56484110e4316f2ef09d19913e740 (handler.py blob 2e470059a82e7828b08d735af73463ac08ca2fbb;
sha256 af6c01b395d36b079a42c46563ccaafeca808ab12be6d0112f0db8e8b4358510). The last commit to change handler.py is 5243b0008c (the IB-pr-523 content).

## The served change, in words

A backfill event may now carry a `stages` key, valid only inside a backfill object. Absent: the run does all three stages (returns,
class, lots), exactly as before. `"stages": ["lots"]`: an activity-and-lots-only run. It writes the activity partitions
(account_activity_daily) and the two lot partitions (account_lot_realized, account_lot_unrealized_daily) for the days of the range,
and it writes a status object under the activity prefix (`_status/lots_not_computed.json`, on a real run only). It never computes,
never writes the returns partitions (account_return_daily) and never writes the class partitions. Any other `stages` value (an
unknown stage, an empty list, ["returns"], a string) is refused by name before any call, and a `stages` key on an event with no
backfill object is refused by name. The scheduled path is unchanged. The change is one commit: +37 and -2 lines in handler.py.

## Live and built sha256

- LIVE: CodeSha256 J6M/92MhjYM/0kKoYRQwR0ah68DizcvnkVSE6o24udg= (hex 27a33ff763218d833fd242a86114304746a1ebc0e2cdcbe7915484ea8db8b9d8),
  read 2026-10-13, LastModified 2026-10-13T12:39:43Z, version UcKN2ttQzhg5B3jn3POSxVBGg15TqpON (content-sha256 metadata equal, 223320 bytes).
  Equal to the source map artifact_sha256 and to the bytes fetched to scratch. Timeout 900, MemorySize 3008, Handler handler.lambda_handler.
- BUILT (BUILD_ONLY, packed twice, byte-identical, 224058 bytes): BYe52LrfcJxuD22UKvDEgSG0SlldOp2H/fGLzS7jbfE= (hex 0587b9d8badf709c6e0f6d942af0c48121b44a595d3a9d87fdf18bcd2ee36df1).
- Members: 19 each. 18 identical to live. ONE changed member: handler.py (built af6c01b3..., equal to the repo blob at the pin).
- Signature and attribute instrument (signature_closure_attr.py): 0 signature mismatches and 0 attribute mismatches on the built zip and on the live zip (12 attribute calls checked each).
- Source map: not edited; sha256 9cde65e5050208f408588fc456bfa616ed0d2a9aa70ac2fc5cc4fb8c6ab79f98 before and after. handler.py is a native member, so no row changes.

## Offline arms (run on the BUILT zip's own handler.py bytes; no invoke, no AWS call)

(a) lots-only: compute, the returns emit and the class emit are not called; the lots emit is called once for the three days: verdict no_returns_call.
(b) default backfill: calls compute, emit_day x3, emit_classes, emit_lots, identical to the live (pre-change) bytes: verdict unchanged.
(c) unknown stage, empty list, ["returns"] and a string: each refused by name, no call: verdict refused.
(d) stages key on a scheduled event: refused by name: verdict refused.

## Returns baseline (read only, keys and ETags, read 2026-10-13)

- returns_partitions 569 (date= partitions 2024-07-08 to 2026-10-12; 1138 objects, data.parquet and manifest.json each).
- activity_partitions 4 (2026-10-07, 2026-10-08, 2026-10-09, 2026-10-12; 8 objects; no _status object).
- listing_digest 8c0afcb7058034cef427148c9354931004ea2f17fd29f9e55fcf9354af13b9d9: SHA-256 of the sorted key TAB ETag lines under
  s3://opal-data-49financial/irpt/49financial/gold/account_return_daily/ (defined in IB188-1_arms_baseline_ledgers.json).
- The pair re-takes this digest after EVERY chunk. The returns digest must be byte-equal before and after each run: 0 returns partitions changed.
  The returns partitions are untouched by the lots-only run (the proof is the hash before and after each chunk, not an assertion).

## Open ledgers and sequencing

Ten change-management ledgers name the function: nine CLOSED, and ONE HELD: `20261013T1228Z_irpt-dashbd-thresholds-swap-20261013`
(HELD-SOVEREIGN-GATED at leg L7, the read of the scheduled 07:41 ET fire of 2026-10-14). Its bytes are the live bytes now (J6M...), so the
live function is on the held deploy's code while its ledger is HELD. Its marker `irpt-dashbd-thresholds-swap-20261013.json` is HELD at the
trunk HEAD and at nine more worktree HEADs, and reads OPEN at nine stale worktree HEADs. Those OPEN copies are stale views: named here, closed by no one.
Denominators: 10 ledger files read, 32 of 32 worktrees read (ls-tree rc=0), 564 marker files read.
SEQUENCING: no code release lands while the thresholds-swap ledger is HELD. Its owner closes it (CLOSED or SUPERSEDED) first, and the
release ledger is opened at start and closed at completion (critical_paths change management, NEVER-2). The scheduled fire at 2026-10-14T11:41Z
reads this function; the release and the first chunk do not run inside that fire window.

## Branch A -- (a) the code release, then (b) the chunked backfill runs

(a) CODE RELEASE, digest-gated, never a mint.
1. Rebuild with the release source map and compare the rebuilt zip's sha256 with the signed built digest 0587b9d8...36df1
   (base64 BYe52LrfcJxuD22UKvDEgSG0SlldOp2H/fGLzS7jbfE=). On any difference ABORT. The release uses the non-BUILD_ONLY path of build-and-upload.sh, which uploads
   the zip to opal-313476888478-lambda-artifacts under investor-reporting/irpt-reporting-gold-lambda.zip and writes artifact_sha256 into the source map.
2. Terraform: infra/aws/terraform/investor-reporting/reporting-gold/ (lambda.tf, module irpt_reporting_gold, resource
   module.irpt_reporting_gold.aws_lambda_function.this). The change is s3_object_version and source_code_hash ONLY.
   Plan to a planfile: 1 to change, 0 to add, 0 to destroy. Then `bash .tools/safe-apply.sh` on that planfile.
3. Gates before the apply: both halves signed at these packet bytes; the thresholds-swap ledger CLOSED or SUPERSEDED; the live CodeSha256 equal to
   J6M/92MhjYM/0kKoYRQwR0ah68DizcvnkVSE6o24udg=; the rollback version re-named and head-object re-read at the apply.
4. After the apply: get-function-configuration CodeSha256 equal to BYe52...; a re-plan of the same target reads No changes; one dry_run event (see (b)).

(b) CHUNKED BACKFILL RUNS.
- Floor: nothing earlier than an account's earliest record. For 49 Financial the census found the source starts 2024-07-08. The 2012 floor
  (Andrew's words: any backfill is thereby cut at 2012) is an operating rule for these runs; the handler itself carries no 2012 floor.
- Range: 2024-07-08 to 2026-10-06 (565 trading days), oldest first.
- Why chunks are small. The handler's MAX_BACKFILL_DAYS is 25, but the function's timeout is 900 seconds. The measured lots-stage rate is
  216.7 seconds per trading day (round-186 census). 900 / 216.7 = 4.15, so about 4 days a chunk (derived). 4 days at that rate is 866.8 seconds,
  96 percent of the timeout. A 25-day chunk would need about 5417 seconds (derived): it cannot finish. 565 days in 4-day chunks is 142 invocations (derived).
  The first real chunk is a ONE-day run that times the lots-only stage (unmeasured today).
- Each run FIRST as a dry run: {"backfill": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}, "accounts": "population", "stages": ["lots"], "dry_run": true}.
  Read the printed counts and any LOTS_SKIPPED line or refusal. The real run (the same event without dry_run) only when the dry run is clean.
- Invoker: an operator identity holding lambda:InvokeFunction, not the scheduler. Its identity class is not read here.
- Verification after EVERY chunk: re-list the returns prefix and recompute the listing digest. The hash before and after must be equal
  (0 returns partitions changed). Count the new activity partitions. Read the log for LOTS_SKIPPED, REFUSED or a timeout. STOP on any of them.

## Idempotence (stated)

The activity stage is NOT idempotent: round 186 measured 6,901 activity rows against 6,904 for one day. A re-run of a day therefore
changes its activity and lot content. The pair signs that; the chunked plan never re-runs a landed day except by an explicit decision.

## Branch B -- rollback

(a) Code release: restore the live version. The rollback anchor is version UcKN2ttQzhg5B3jn3POSxVBGg15TqpON of
investor-reporting/irpt-reporting-gold-lambda.zip in opal-313476888478-lambda-artifacts (content-sha256 J6M/92MhjYM/..., read now by list-object-versions
and head-object, re-read at the apply). Rollback per key: s3_object_version back to that id and source_code_hash back to J6M/92MhjYM/...; the source map
row back to the pre-release values. Previous anchors, if ever needed: 8ELUDq_d2wRKI0kSXEuLXFm6iqgsiAyZ (i2r7CbVr...) and qh361rTWYO2VtgsirsJXq6kiqJEVBDpZ (oNgy4rnr...).
(b) Runs: new activity and lot objects can be removed only by an operator DELETE, which needs Andrew's word. Rewritten objects can be restored by version id, only by an
operator identity. What CANNOT be undone by this packet: a day that landed and was then rewritten (its prior content survives only as a noncurrent version).
The status object under the activity prefix is also written on a real run.

## Blast radius

The write set of the lots-only run is the activity prefix, the two lot prefixes (account_lot_realized and account_lot_unrealized_daily), and the status object
under the activity prefix, for the 565 trading days of one firm. It never includes the returns prefix or the class prefix. A mis-run can overwrite a landed
activity or lot day, and the status object. The round-186 census states that bucket versioning is Enabled and that the function role has no delete;
neither was re-measured in this census (no bucket or IAM read was made), so both are carried from that census, not measured here.

## Red list

deliverables/0.9.0_WK_IRPT_BCKEND~278/IB117-1_red_list.json names two target prefixes: infra/aws/lambda/investor-reporting/_contracts/ and
docs/contracts/investor-reporting/. handler.py lies under neither. Its text does not name the red operation analysis-request-original.
changed_paths_touching_a_target is empty; the stop flag is false.

## Consumers (named from the repository)

- Returns table (account_return_daily): reporting-publish/handler.py (lists the gold partitions and builds the platinum series, read-only); the portal
  perfrp contract files portal/src/pages/AdvisorIntelligence/_shared/perfrp/contract.ts and portal/scripts/perfrp-contract-exercise.mjs (matched by name; not read in full).
- Activity table (account_activity_daily): NO reader found. Searched: infra/aws/lambda (non-test), lib/, data/assets/, the portal checkout. Only the producer and
  the gold handler name it. The readers are not named here; this is stated, not inferred.
- The default report's contributions, withdrawals and income per window: the mapping was not read in this census.
- After-read: the default report shows those figures for a window longer than 4 days. A person's read on DEV; no seat can sign in to make it.

## The pair (both UNSIGNED)

- COO half: 2.0.0_SA_COO~P2 -- UNSIGNED at these packet bytes.
- CTO half: 1.0.0_SA_CTO~DELL2 -- UNSIGNED at these packet bytes.
Both halves are signed at these packet bytes before Branch A may run.

## What this census did not measure

- The lots-only chunk time (the 216.7 seconds per day is the round-186 figure). The one-day all-stage durations in the ledgers are 389 seconds (R37 ledger, B1) and
  348 seconds (R45 ledger, dry run); both include the returns stage and are not the lots-only rate.
- The invoker's identity and its permissions (not read).
- The cause of LOTS_SKIPPED (the handler prints it; no run in this census produced one).
- The default report's arithmetic for contributions, withdrawals and income.
- Any object body (none read); any value of any row.

## Surprise rows filed (IRPT_BCKEND-D2-W372-S1 to S4)

S1: no reader of the activity table is named in the repository. S2: the handler's chunk bound (25 days) admits runs the 900-second timeout cannot hold.
S3: the lots-only chunk length is not measured, and the 4-day derivation leaves about 33 seconds of margin (900 minus 866.8). S4: the trunk ledger of the
thresholds-swap deploy reads HELD while the live function runs its bytes, and nine stale worktree HEADs read its marker OPEN. Each is OBSERVATION, hazard INERT.
