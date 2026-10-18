# NEVER-WIDEN ASK -- `OG-ev-7` -- MEASURE the `etfs_compare_peers` call's 17.9 s in the running service: ONE arming of the loopback listener under a lease that pins the firm (row `Z-S389`); a measurement, not a fix

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ev-7.round-43-peers-call-in-the-service-under-one-firm-pinned-lease.md` (GO for Step 1, the ask only: msg 35756). **Nothing is armed by this ask or by Step 1.**
**Live release, read now (2026-10-18T17:10Z):** `/opt/opal-gateway/.deployed_commit` reads `a0c83303ee48c95c16a61c0d5e8bd186b1083b66` (`OG-ap-42`, the firm pin; ledger `nfra-oplgtw-gateway-release-batch10` CLOSED 2026-10-18T16:32:05Z). The service is one process, PID `1302970`, up since the deploy at 15:49Z, `NRestarts` 0, the unit limits unchanged (1468006400, 1258291200, 300). The lease parameter `/opal-gateway/probe/lease` is ABSENT, and three calls to the listener (read now, for this ask) answered 403 `probe_not_armed`; the listener is bound to `127.0.0.1` on the service PID. Records: `W/ap42_pb/` and `W/ev7_pre/` (the read-only reads of this Step 1).
**What the service has served so far:** the audit lake holds NO served `etfs_compare_peers` call since the 15:49Z restart (only two unarmed refusals, outcome `denied`), so call 1 of the arming will be the service's first peers call since its restart, as the OG-ap-40 peers call was.

## 1. What this measures, and the rule fixed BEFORE the run

In the `OG-ap-40` arming `etfs_compare_peers` took 17.9 s through the listener in the running service, against 4.5 s in a fresh process (57 rows each way; row `Z-S389`, not explained: a cold first call after a restart, the listener sharing the service's one event loop, or the heap-signal handling). One reading, one arming. This cell takes three readings in one arming and one fresh-process reading, and applies a rule that is fixed now (it is also in `ev7.AC1.sh`'s header, and the check recomputes the verdict from the numbers):
- **The run:** ONE lease, then three `etfs_compare_peers` calls through the listener, back to back, in the same service process, with the same arguments as the `OG-ap-40` peers call: calls 1 and 2 with the `SIGUSR2` heap read around them (`heap_signal` `on`), call 3 WITHOUT any `SIGUSR2` (`heap_signal` `off`; `VmRSS` and `VmHWM` are read from `/proc/<pid>/status` afterwards). Per call: `wall_s`, `vmrss_mb`, `hwm_mb`, `service_pid`. Then the SAME call once in a FRESH guarded process on the host (`fresh_process_wall_s`). Then the lease is deleted.
- **The verdict, in this order:** `COLD` if call 1's wall is at least 2 times call 2's; else `SLOW_IN_SERVICE` if every one of the three walls is more than 2 times `fresh_process_wall_s`; else `SIGNAL_COST` if call 3's wall is at least 20 percent below call 2's; otherwise `INCONCLUSIVE`. Any of the four PASSES the check; `INCONCLUSIVE` is an answer.
- **SAFETY bounds (a breach is a STOP, not a finding):** `VmRSS` after any call at most 1200 MB (the CTO's CT3 ceiling), one service PID throughout, `NRestarts` 0, ONE arming. The 17.9 s itself carries no pass or fail bound: the cell explains it and does not grade it.

## 2. The widening, stated plainly

- **ONE arming of the loopback listener** (`127.0.0.1:8099`, inside the running service), by writing ONE SSM parameter (`/opal-gateway/probe/lease`, type `String`) with this seat's own role: `{"order": "OG-ev-7", "account_ref": "****<last4>/<vendor>/<alias>" (the test account's, never printed or recorded), "firm": "49financial" (the test account's firm), "set_at", "expires_at"}`, **15 minutes** (the order allows 25 or fewer; three peers calls and one fresh-process call need about five). The parameter is DELETED before this seat finishes. No other SSM write, no release, no deploy, no IAM, no Terraform, no env key.
- **What the listener can do while armed (the firm is pinned this time, `OG-pr-4` is live):** `etfs_compare_peers` (market data only; it takes NO firm and NO account argument) for any arguments a loopback caller sends, and `client_get_transactions` ONLY when the call's firm equals the lease's firm AND its account equals the lease's account (another firm is refused 403 `probe_firm_refused` before the tool runs; another account 403 `probe_account_refused`; any other tool 404; a lease without a valid firm is malformed). **This seat makes NO `client_get_transactions` call in this arming.** Any process on the host that can reach loopback can call the listener while armed; unarmed it answers 403 `probe_not_armed` and serves nothing. The SSRF audits (`OG-sec-1`, `OG-sec-3`) read CLEAN, 0 controllable. The window is the lease: 15 minutes at most, and about five in practice.
- **The CVO's condition (msg 35740, carried in his `OG-ap-42` half): his own half first, with the lease, the labels and the disarm read by him, and no persisted bodies.** What he reads: (a) the lease: order `OG-ev-7`, the account in `****<last4>` form, the firm, at most 25 minutes (15 proposed), `set_at` and `expires_at` (the record prints all of them except the account's last four); (b) the audit labels: every listener call, served or refused, is audited as `probe:OG-ev-7` (and `probe:unarmed` before and after), counted from the audit lake; (c) the disarm: `get-parameter` answering `ParameterNotFound` PLUS a call refused 403 `probe_not_armed` after the 6-second wait; (d) NO probe response body is persisted: a peers answer is reduced in memory to its status, its row count and its wall time, and the raw output is not written to the repo, a row or a message.
- **Honest limits:** (1) one arming is one occasion, so a verdict is a reading, not a law; (2) call 1 is the service's first peers call since its restart, which is what `COLD` tests, but the service has been up for about 90 minutes and has served other tools, so it is not byte-for-byte the state of the `OG-ap-40` arming; (3) the fresh-process call runs AFTER the three service calls (the order's step 4), so the operating system's file and network caches may be warmer for it than they were for the 4.5 s on record; (4) the in-service wall is the client-side time of the HTTP call (it includes the listener's HTTP handling and JSON encoding, a few milliseconds), the fresh-process wall is the time around the function itself; (5) the measurement cannot say which step inside the call is slow, only which of the four stated readings the numbers support; (6) the service's own access log has been silent since the `OG-ap-40` deploy (row `Z-S395`), so the calls are counted from the audit lake and the client-side timings, never from the journal.

## 3. The order of acts (Step 2, on the GO that names all three halves signed at this ask's sha256)

1. Re-read the live ref: `/opt/opal-gateway/.deployed_commit` must equal the sha in the GO (`a0c83303ee` unless dell1 deploys again; any other value is a STOP and a row); the `.env` (65 keys), one process, `NRestarts`, the unit limits; every open gateway ledger (an open ledger of another seat is a STOP). Read the lease parameter ABSENT; a connection to the listener answers 403 `probe_not_armed` (record it).
2. Before arming, in a guarded fresh process (the `OG-ap-40` `gather` step): resolve the test account's reference and the first valid period and axis (the pair used in the `OG-ap-40` peers call); the account reference goes from that process to the lease inside one local process and is never printed or written.
3. ARM ONCE (15 minutes): write the lease. Wait 7 seconds (the listener caches an unarmed read for 5).
4. The three `etfs_compare_peers` calls through the listener, back to back: call 1 and call 2 each preceded and followed by `SIGUSR2` (only when the service has the handler installed: `SigCgt` is read first, because an unhandled `SIGUSR2` would terminate the process), call 3 with no signal. After each call, `VmRSS` and `VmHWM` are read from `/proc`. If any `VmRSS` exceeds 1200 MB, or the PID changes: STOP, delete the lease at once, report.
5. The SAME call once in a FRESH guarded process on the host (the `OG-ap-40` harness under the cgroup hard guard `oom_score_adj_1000_cgroup_memmax_1400mb`).
6. DELETE the lease parameter; read `ParameterNotFound`; wait 6 seconds; a call answers 403 `probe_not_armed` (the listener closed at rest); the service PID unchanged and `NRestarts` 0. Count the labelled records from the audit lake.
7. Compute the verdict by the rule; write `W/PEERS_MEASURE.json` (fields as in `ev7.AC1.sh`'s header, plus the per-call numbers and the audit-lake counts), commit, run `ev7.AC1`, write and validate the proof instance, report once with the four walls, the `VmRSS` values, the verdict and the time the lease was deleted.
**Scripts.** Step 2 reuses `ap40_probe_host.py` unchanged for its `state`, `call` and `gather` modes (committed in `W`; `ap40_probe_run.py` is the model for the runner), and adds two small modes (`peers` without `SIGUSR2`, and the fresh-process timing) in NEW files `ev7_probe_host.py` and `ev7_run.py`; they are written and linted after the GO and COMMITTED BEFORE the arming, and the arming does not start unless the uploaded bytes equal the committed blobs (their blob ids go into the Step 2 report). The runner has an emergency path: any exception after the lease is written deletes the parameter.

## 4. Both branches

- **Unarmed (the state at rest, before and after):** the listener answers 403 `probe_not_armed` to every request and serves no data; the gateway's tools, routes and answers are what they were.
- **Armed (the minutes between the write and the delete):** the listener serves `etfs_compare_peers` for any arguments and `client_get_transactions` only for the lease's firm and account (not called here); every call is audited as `probe:OG-ev-7`.
- If the GO does not come, or a STOP happens before the write, nothing was armed and nothing needs undoing.

## 5. Rollback

**Delete the parameter** (`aws ssm delete-parameter --name /opal-gateway/probe/lease` with this seat's role); the listener closes within the 5-second cache window, and in any case at the lease's `expires_at` by itself (the listener refuses an expired lease without a restart; shown in the `OG-ap-40` arming). There is no code or unit change to roll back: the release stays `a0c83303ee`. If the service misbehaves (PID change, `NRestarts` above 0, `VmRSS` above 1200 MB), the lease is deleted first and the service state is reported; a redeploy of the live ref's tree (`922ee425fe`, tarball sha256 `d025c8a103f39645558ddd48b600f671135604c2714ec08b96bfabfc95688424`) is the issuer's call under its own ledger, not part of this cell.

## 6. Triggers (any one: delete the lease parameter at once, read it absent, file an ARMED row naming `2.0.0_SA_COO~O`, report)

`VmRSS` after any call above 1200 MB; the service PID changing; `NRestarts` above 0; host memory above 85 percent; the listener answering ANY call with no lease (a 200 from `/probe/...` while the parameter is absent or after the post-delete wait); `ParameterNotFound` not reading after the delete; the first call after the write answering 403 `probe_not_armed` twice (the service cannot read its lease: a finding about the instance role, not about the measurement; no IAM change is made here); a second arming being needed (a STOP and a row).

## 7. Gate lines

No code is released by this ask: no commit gate, no overlay, no deploy. The ask and the scripts (Step 2) are files in `W`; the Step 1 reads (`W/ev7_pre/`) are counts, status words and times only. No account number, person's name, credential or object content appears in any record.

## 8. The three halves (sign ONCE, on this ask's sha256)

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed on this ask's sha256 and on the live sha `a0c83303ee48c95c16a61c0d5e8bd186b1083b66`, with the rule of section 1 and the safety bounds of sections 1 and 6 fixed as written.

### COO half (`2.0.0_SA_COO~O`)

To be signed on this ask's sha256.

### CVO half (`3.0.0_SA_CVO~Z`)

To be signed FIRST, on this ask's sha256, after reading the lease, the labels and the disarm of section 2 (a to d).
