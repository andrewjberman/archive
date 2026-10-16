# OG-ap-31 Phase B -- state at the close (0.7.0_AE_CloudOps~NFRA1, 2026-10-16 ~22:4xZ)

GO msg 35276 (all three halves: CTO 11957299d4, COO f9117e993a, CVO 5157a00b6f against ask sha256 8115e8edf038...). Live ref before: bf9d23b518. Live ref now: `4be300110ec912ac8c11a1663403e41eea45117c`.

## Acts, in order
- Step-1 re-reads at the GO: manifest, S3 git-ref and host agree on bf9d23b518; host md5 139 of 139 (`ap31_host_md5_phaseb.json`); `.env` 65 keys, no `MUSE_CLIENT_ID`; `tools/list` 103; role resolves; no gateway release in flight in any of the 79 worktrees (the old mcportal sentinels sit in detached trees whose ledgers are closed). `comp-schedule --drift`: 1 armed gate (G-3, the convert_transactions_to_silver sentinel, unrelated); carrier C1 scanned 126468 of 158701 files (budget partial).
- Ledger `nfra-oplgtw-gateway-release-batch3` opened first (entry and sentinel committed, merged to box/sitez), then the Phase A gate overlay restored to the live ref's bytes (13 rewritten, 14 removed; `ap31_overlay_restore.py`), tree clean at the release commit.
- Deploy attempt 1 (21:58Z): REFUSED by the halt gate before any upload (`ap31_deploy_attempt1_halt_gate_refused.out`). Attempt 2 (22:00Z): REFUSED, unknown-base (`ap31_deploy_attempt2_halt_gate_unknown_base.out`). Cures, no override: the trunk copy of `.tools/halt-gate-check.sh` laid into the release tree uncommitted; `org/tier2_senior/0.7.0_AE_CloudOps~Z` added to the sparse cone. Row Z-S324.
- Attempt 3 (22:00:18Z to 22:01:30Z): the one deploy, base guard EQUAL at both checkpoints, `ssm:e11265e5-...` Success, DEPLOYMENT COMPLETE (`ap31_deploy.out`). The wrapper's own manifest commit could not land in the release tree (the naming gate needs the overlay that was restored); its manifest edit stays uncommitted there as the deploy record.
- Read-back: health 200; host md5 139 of 139 equal to the release blobs; control against the base blobs differs on exactly the 4 app files; `tools/list` 103 before and after; 65 keys. No trigger.
- Served read: `ap31_served27.json` (27 of 27), `ap31_arms.json` (e1 to e4), `ap31_e6_discover_buckets_host.txt` (8 of 8, vendor and firm 2 of 2), assembled to `CODE3_SERVED.json` by `ap31_served_build.py`.
- Standing clauses: manifest `30d14203b4` (deployed_commit, 1 of 10 checksums moves: `app/server.py`, cross-checked against the host), runbook 7.2; `rb.AC2` PASS.
- Ledger closed, `ap31.AC2` PASS, proof instance VALID, status complete.

## State left behind
- `C:/tmp/og-rel-batch3` (branch `rel-nfra-oplgtw-batch3` at the release): uncommitted `.tools/halt-gate-check.sh` (trunk copy) and the wrapper-written `infra/aws/ec2/EC2_MANIFEST.json`. KEEP the branch: runbook 7.2 and the manifest history name the release commit.
- `C:/tmp/og-live-bf9d` (pristine detached tree at the base): removable. Rollback is a redeploy of `bf9d23b518`.

## AC3 evidence (A1, COO msg 35278)
- File: `CVO_AC3_BODIES_OG-ap-31.json` in this folder of the SHARED tree (`C:/Users/Opal Bloomberg/Desktop/ajb_workspace/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/`). 57278 bytes, sha256 `5aeca420901d2b224e18a5ed4eeae8c0d479b6bbf92af2232e9c278b3bf847a8`, captured 2026-10-16T22:36:08Z from the live release `4be300110e`. Git-excluded BEFORE it existed (`.git/info/exclude`), untracked, never `git add`ed: it holds client positions.
- Per capture (rows; partitions): holdings 21 rows (partition 2026-10-09); transactions 58 rows, 334 partitions in the 13-month window, 60 read, `window_partial` true, `exact_duplicates_removed` 355, partition 2026-10-16; allocation 2 rows (2026-10-09); fees 5 rows, 395 partitions in the window, 60 read, partial true, 0 duplicates removed, partition 2026-10-15; EMPTY news window 0 rows with `coverage_floor`; chatter 10 rows with `trading_days_behind_t1` 5.
- Masking: an account stays `****<last4>`; withheld 2 person or contact fields (`portfolio_name`) and 2 bare account ids; 0 e-mails, 0 phones, 0 name-shaped values. Numbers, tickers, CUSIPs, security ids and dates are as served. A scan of the file found 0 e-mail addresses and 0 phone numbers.
- Script: `ap31_ac3_capture.py` (committed; it holds no data). One run, no retry loop; read-only.
