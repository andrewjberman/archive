# ONE-DATE REPLAY PACKET -- 49financial 2026-10-08 (IRPT_BCKEND IB-pr-534, round 192, workstream ~P)

Order: IRPT_BCKEND.TO-IB-pr-534 (issued by 2.0.0_SA_COO~P2; CTO ruling: a one-date replay of 2026-10-08 is its own cell with its own pair, decided after the producer release's after-read).
Worker: 0.9.0_WK_IRPT_BCKEND~381. Record: IB192-2_timeout_and_replay.json (same folder). Surprise rows: IRPT_BCKEND-D2-W381-S1 to S5 (INVESTIGATION_v1.md).
Scope: READ ONLY. Nothing was invoked, written, uploaded, applied, deployed, signed in, or sent to a vendor. The replay was not run and no candidate was built.
Base commit (worker HEAD before the first commit): 201e7e9c273e8274c0a4ea1ad1aa0b205f69a079.

## What the gap is

49financial's served index holds ten dates, latest 2026-10-12. 2026-10-08, a Thursday and a trading day, is absent. The 2026-10-09 scheduled fire ran 309.9 seconds of plugin time and was marked TimedOut with response code 137 (SIGKILL). It did not run into the 3600-second window, so the timeout does not explain it (IRPT_BCKEND-D2-W381-S1). The source for 2026-10-08 was intact at fire time: its custody partition was written at 2026-10-09T09:46:44Z, before the fire at 14:15Z (IRPT_BCKEND-D2-W381-S4). Nothing replays a failed date, so the gap stayed.

## Branch A -- the replay (NOT run)

The replay is one operator-issued producer command on the daily-runner host, under the 49financial publish principal as the dispatcher's script assumes it: holdings_snapshot.py --firms 49financial --as-of 2026-10-08 --upload, with no --qa so that the served table is written. The dispatcher itself sends no --as-of, so this is not a scheduled fire.

Gate outcome, read from code: evaluate_publish_gate adds source_frontier_older when the candidate's business date is behind the served frontier by more than zero trading days. The candidate 2026-10-08 is two trading days behind the served 2026-10-12 (lib/trading_calendar.py, NYSE fallback calendar). The gate runs before the index write. As the code stands, the replay is REFUSED on this one condition. Other conditions were not evaluated, because no candidate was built.

So Branch A cannot land on the code as it is. It needs one of the routes below, and the choice is the CTO's to rule, not this packet's:
- (a) a gap-fill exemption in the gate for a date absent from the served index and older than the frontier. It moves the gate for every firm and every later fire.
- (b) an operator path past source_frontier_older for one named firm and one date. It moves the gate for one run only.
- (c) no code change: a ruling alone cannot land the replay, because the gate runs on every upload.
- (d) leave the gap. Each attempt rewrites the refusal record.

Writes, if a route lands the replay (key shapes; the bucket is the firm's publication bucket):
- gold parquet and platinum json (or header and part objects) under date=2026-10-08, new objects only;
- the manifest under date=2026-10-08, a new object;
- one new version of current/manifest.json, conditional on the ETag captured at the start of the run.
On the refused path, which is the path the code takes today, the only write is the overwrite of current/publish_refusal.json.

## Branch B -- rollback

The served manifest version of current/manifest.json was read at 2026-10-14 by list-object-versions: daFZJt6f7G9.CXj3MJftFYV.DNUOVFQh (IsLatest, last modified 2026-10-13T14:20:49Z). Rollback is a copy-object of that version back onto the key, which creates a new version carrying the prior bytes. That copy is a write and needs its own pair. The 2026-10-08 revision objects stay in the bucket as unreferenced immutable objects. Deleting the replay's index version instead is destructive and needs Andrew's word. The 49F refusal record's prior state was not read (the census names cottonwood as the only firm with one), so a rollback of that object would need that read first.

## Blast radius

One date's keys: the four object families above, all under date=2026-10-08. The index gains one row, keyed 2026-10-08. latest_date stays 2026-10-12, because it is the maximum of the keys. Every other date is untouched: publish() copies the prior dates and replaces only the key it lands (publication.py lines 295-298), and that key is the builder's custody partition date, which for this run is 2026-10-08 because that partition exists (IRPT_BCKEND-D2-W381-S3 records that nothing asserts the landed date equals as_of). The other ten rows keep their manifest references byte for byte. The one 49F-only object the current code writes is the refusal record. Both sets of facts are in the record's replay block.

## The source_frontier_older answer and the route it needs

source_frontier_older is true for this replay. Its route is one of (a) to (d) above. A replay under (a) or (b) changes a gate that protects every firm, so the route needs a signed pair with a ruling that names both branches, the replay and the rollback. A replay under (b) for one date should state the bypass as its one exception and nothing wider.

## Ordering

The replay runs after the producer release's after-read, never before. The release is the IB-pr-532 release (the three firm bundles and the first scheduled fire after the mint, per NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-532.md), and its after-read is the first scheduled fire's manifest read. The replay that lands before that read would change a served index the after-read has not yet judged, and the release's stop rule would then compare against a moved baseline.

## The releasing seat's NEVER-2 ledger

The seat that runs the replay opens its own change-management entry under org/critical_paths/change_management/ at the start, and closes it at completion. The entry names: the replay command and its route; the index version before the run (daFZJt6f7G9.CXj3MJftFYV.DNUOVFQh); the expected index after (ten rows plus 2026-10-08, latest 2026-10-12); the rollback in Branch B; and the after-read, which is current/manifest.json with a row for 2026-10-08 and latest_date 2026-10-12, and a page that asks for 2026-10-08 returning that row. The entry is not created here.

## COO half

2.0.0_SA_COO~P2 -- UNSIGNED at these packet bytes.

## CTO half

1.0.0_SA_CTO -- UNSIGNED at these packet bytes.

The packet's own sha256 is left for the signers and is not computed here. Both halves must be signed at these packet bytes, and the route chosen, before Branch A may run.

## What this packet did not measure

- The cause of the 2026-10-09 kill (exit 137). No command output was read.
- Any candidate build, so the other gate conditions (reconcile, multi-asset, class outside the six, lost accounts) are not known for the 2026-10-08 replay.
- The index body. The ten dates are the COO's S165 read; the version sizes are measured.
- The contents of the 2026-09-23 tax-managed membership capture, the only one listed, which a 2026-10-08 build would state as its vintage.
- The release's own after-read, which is due after the release.
- The bundle sha256 values, and any IAM policy beyond the grant record.
- Any holding value, account identifier or client identifier. None is recorded here.

## Sources

- Producer: data/assets/scripts/gold/investor_reporting/holdings_snapshot.py at 201e7e9c27 (evaluate_publish_gate lines 3031-3088; run_firm 3133-3224).
- Publication: infra/aws/lambda/investor-reporting/holdings/publication.py at 201e7e9c27 (publish 222-314).
- Dispatcher: infra/aws/lambda/investor-reporting/holdings_refresh/refresh_dispatch.py at 201e7e9c27 (EXECUTION_TIMEOUT line 25).
- Record: IB192-2_timeout_and_replay.json in this folder.
