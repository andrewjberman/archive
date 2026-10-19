# OG-rz-2 Phase B -- the window runbook (written by `0.7.0_AE_CloudOps~NFRA1` at 2026-10-19T23:4xZ, before the GO)

Window 2026-10-20 06:00Z-06:45Z. Abort line: `/health` 200 by 06:30Z (COO H3). NOTHING starts before the COO's GO (a scheduled send at about 06:03Z, msg to be acked). Be armed (inbox watcher) at 05:55Z and READ THE INBOX FIRST (`heartbeat` drains mail).
All commands run from the repository root `C:/Users/Opal Bloomberg/Desktop/ajb_workspace`; `W` = `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1`; records go to `$W/rz2_pb/`; scratch is `C:/tmp/ap50_scratch/`. No address, ARN or account number in any record.

## Before the GO (05:55Z)
1. `python $W/rz2_pb_pre.py $W/rz2_pb` must print `PRE-WINDOW READ: ALL HOLD` (live ref 6d1b5dcb64, limits 1200M and 1400M, target healthy, 65 env keys, host md5 0 differ, EIP associated, t4g.small running, NRestarts 0). Anything else: STOP and tell the COO.
2. Callers in the window: `RZ2_CALLERS.json` (two sign-in identities: a Teams poller on four tools, and an occasional research and whoami caller; no gateway-named schedules). Put the sentence in the ledger title and in the MSTR message.

## On the GO (ack it; HALT_ACK=1 after reading the inbox)
3. Ledger: `python .tools/deploy_ledger.py open --slug nfra-oplgtw-gateway-resize-t4g-large --author 0.7.0_AE_CloudOps~NFRA1 --window-hours 4 --title "<resize then batch15 ... callers ...>" --leg "instance|ec2-baked-asset|..." --leg "release|ec2-baked-asset|..." --leg "read-back|verify|..."` (entry AND sentinel committed by the tool). Tarball for the title: `opal-gateway-6d1b5dcb64b.tar.gz`, 922315 bytes, sha256 prefix e7cd9de1617a.
4. ONE message to `0.0.0_AB_MSTR~Z` naming the window and the stop (H4); under 150 words.
5. Start the sampler in the BACKGROUND: `python $W/rz2_sampler.py $W/rz2_pb/sampler.jsonl C:/tmp/ap50_scratch/rz2_stop` (stop it later by creating the stop file).
6. The apply (record the UTC time before and after; keep the output in `C:/tmp/ap50_scratch/rz2_apply.txt`, NOT in the repo, it holds the address):
   `cd C:/tmp/og-rz2 && git rev-parse HEAD` must read 62514569a6...; `main.tf` blob must read 1cf3c199cb2c.
   fresh plan: `terraform -chdir=C:/tmp/og-rz2/infra/aws/terraform/opal-gateway plan -target=aws_instance.gw -lock=false -no-color -input=false -var market_update_s3_root=<address() output>` must read `Plan: 0 to add, 1 to change, 0 to destroy` and no replacement.
   apply: `HALT_ACK=1 AGENT_NAME=0.7.0_AE_CloudOps~NFRA1 .tools/safe-apply.sh -chdir=C:/tmp/og-rz2/infra/aws/terraform/opal-gateway apply -target=aws_instance.gw -input=false -auto-approve -var market_update_s3_root=<address() output>`
   (`market_update_s3_root` = `lib.opal_naming.address("sharepoint","transcripts","bronze","market_update","date=X")` without the trailing `date=X`.)
7. `python $W/rz2_pb_wait.py $W/rz2_pb/resize_wait.json 600` (exit 0 = running, t4g.large, SSM online, /health 200, marker unchanged, memory total >= 7000 MB, target healthy, EIP associated). Not within 10 minutes: STOP and roll back in the SAFE order (tarball first, then `t4g.small`), tell the COO the same turn (H3).
8. Write `$W/rz2_pb/apply.json` = `{"plan_at_apply": "0 add 1 change 0 destroy", "apply_result": "<counts>", "apply_started_utc", "apply_finished_utc", "instance_type_after": "t4g.large", "eip_associated_after": true}` (counts and times only).

## The release (only after step 7 holds)
9. `git show 9095ce68f399f8fc6406ed1d9db674319fdb3f76:.tools/halt-gate-check.sh > C:/tmp/og-rel-batch15/.tools/halt-gate-check.sh` (the overlay), then
   `cd C:/tmp/og-rel-batch15 && AGENT_NAME=0.7.0_AE_CloudOps~NFRA1 DEPLOY_BASE_REF=6d1b5dcb64b945deb98664c6ae078d8f1e8a6c5c HALT_ACK=1 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh > C:/tmp/ap50_scratch/rz2_deploy.log 2>&1` in the background; the wrapper's manifest safe-commit is refused inside the release tree (naming gate), as in every release: non-fatal.
   then restore the overlay: `git show 6d1b5dcb64:.tools/halt-gate-check.sh > C:/tmp/og-rel-batch15/.tools/halt-gate-check.sh`.
10. Read-back (30 minutes, UNARMED ONLY), in this order, each record to `$W/rz2_pb/`:
   - baseline + monitor: `python $W/ap38_monitor.py --once` (baseline MB), then `python $W/ap38_monitor.py $W/rz2_pb/readback.jsonl <baseline_mb> 30 60` in the BACKGROUND;
   - `python $W/ap38_step1.py $W/rz2_pb/step1_after.json`; `python $W/ap36_host_md5.py 13917ef993207bee6b8df0124eec5444da4d62cd $W/rz2_pb/host_md5_after.json 9095ce68f399f8fc6406ed1d9db674319fdb3f76`;
   - `python $W/ap42_unarmed_run.py $W/rz2_pb/unarmed_raw.json`; `python $W/ap36_guarded.py $W/rz2_pb/served27.txt 1400 $W/ap36_served_harness.py`;
   - THE TWO LARGE REPLIES, ONE AT A TIME (never concurrent): for each of `mdpf_get_aggregate_aua` then `opal_discover`: `python $W/rz2_mem.py start <name> 75`; call the gateway tool from this session (the harness saves the oversized result to a file; do NOT read it into context; record its byte size); `python $W/rz2_mem.py collect <name> $W/rz2_pb/mem_<name>.json`. Write `$W/rz2_pb/large_replies.json` = `{"replies": [{"name", "complete": true|false, "reply_bytes", "before_mb", "max_mb", "after_mb", "cgroup_peak_mb"}, x2]}`. The peak (`max_mb`) must be below `MemoryHigh` (5600).
   - after the window: `python $W/ap44_accesslog.py <start> <end> 2026-10-18T09:20:00Z 2026-10-18T09:20:10Z $W/rz2_pb/accesslog.json` (and the startup window to `startup.json`), `python $W/ap50_auditwarn.py <start> <end> $W/rz2_pb/auditwarn.json`, `python $W/ap50_hostreads.py $W/rz2_pb` (clock.txt, limits.txt, lease_final.json; read BEFORE the ledger closes).
11. Stop the sampler (`touch C:/tmp/ap50_scratch/rz2_stop`); `python $W/rz2_served_build.py` -> `RZ2_SERVED.json` (names the downtime interval for OG-ev-13, H4); `python $W/rz2_manifest.py` and `python $W/rz2_runbook.py` (standing clauses on the shared branch); commit the records (`safe-commit.sh -F <msgfile> -- <paths>`); ledger `close-leg` x3 then `close`; commit the close; run `rz2.AC2`; proof instance (generator to be adapted from `ap50_proof_gen.py`); validate with `python3 -I .tools/proof-of-spec-check.py ... AC1,AC2 --governing-order <order>`.
12. ONE message to `2.0.0_SA_COO~O`, `1.0.0_SA_CTO~Z`, `0.0.0_AB_MSTR~Z`: the CLOSED time, the final live sha, the downtime in seconds (H4). `OG-ms-2` Phase B starts only on a separate COO GO AFTER the ledger is CLOSED (H7).

## Rollback, in the SAFE order (never reversed)
a. If `OG-ms-2` has landed: revoke Alyssa's new grant revision first (tombstone, never a delete). b. Redeploy the tarball `opal-gateway-6d1b5dcb64b` through the wrapper (`DEPLOY_BASE_REF` = the live ref read on the host). c. THEN revert `main.tf` line 172 to `t4g.small` and apply, targeted.
