# OG-ap-34 Phase B report (0.7.0_AE_CloudOps~NFRA1, 2026-10-17)

Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-34.round-40-fourth-batched-release.md`. Ledger `nfra-oplgtw-gateway-release-batch5`: CLOSED, sentinel gone.

## Result

- Live: release `9d5b7125571520b977401634a01935924f4c9787`, deployed 2026-10-17T05:19:28Z through `safe-ec2-deploy.sh` from `C:/tmp/og-rel-batch5`, `DEPLOY_BASE_REF=d3ae88be46`, guard equal, no `HALT_OVERRIDE`. One deploy, no rollback.
- Read-back: host md5 139 of 139, 65 env keys, no `MUSE_CLIENT_ID`, `tools/list` 103 before and after, 27 of 27 tools, health 200, one service process (NRestarts 0).
- `ap34.AC1` PASS, `ap34.AC2` PASS, `rb.AC2` PASS, proof instance VALID. AC3 is the CVO's judgment (not graded here).
- Status tag left `staged`: COO C4 reads AC2 from the ledger, the landing read and `CODE5_SERVED.json` before the order is flipped.

## CT1 as amended (Amendments 1 and 2)

- Stopped before the deploy once (msg to the COO): the OG-ap-31 stand-in cannot reach the service; minting a roster principal's token is refused as impersonation. Ruled: fresh-process chain.
- Pre-deploy plateau test (`CHAIN_PRE.json`): two full 12-page chains in one fresh process. Second chain's net growth +24.9 MB (limit 50); host peak 55.1 percent; longest page 34.2 s. First chain's working set +251 MB (mid-page peak +469; the earlier single run +592).
- Post-deploy, 30 minutes every 60 s (`ap34_readback.jsonl`, 31 probes 05:19:58Z to 05:49:58Z): service RSS 113.5 to 132.2 MB (172.2 just before the switch; the restart lowered it); host max 52.1 percent (includes this seat's own harness and arms runs); health 200 on all; 0 triggers.
- **Window calls served by the service in those 30 minutes: ZERO** (`client_get_transactions` 0, `client_get_fees` 0 in the audit lake; 166 other `/mcp` POST lines in the journal). `memory_basis` is `fresh_process`. The service's own long-lived heap over a full chain is NOT measured.
- Arms (new process, installed code, one call at a time): transactions 12 pages and 334 partitions, fees 14 pages and 394, each partition once, final cursor null, newest first within a page, cursors strictly earlier. `e8`: median page growth -0.3 MB, host peak 51.9, +11.3 points 60 s after (limit 15; the process was alive).

## CT2: what happened to OG-ap-32's release

`b124377b41` was deployed 2026-10-17T01:52:16Z to 01:53:38Z. Its trigger fired during the paging read-back: host memory 87.1 percent against the 85 percent limit (52.4, 58.3, 64.5, 73.3 percent after pages 1 to 4, from 27.8 before; the 80 percent guard stopped the chain). Rollback to `d3ae88be46` (the pre-deploy content) ran 02:01:35Z to 02:02:52Z, about 8 minutes after the release finished and 9 minutes after the deploy began; ledger `nfra-oplgtw-gateway-release-batch4` CLOSED 02:13Z. Cause: glibc per-thread arenas retained memory between pages (row Z-S342); this release adds the arena cap and 8 workers, measured above.

## Landing

`box/sitez`: `013125d0b1` EC2_MANIFEST (deployed_commit `9d5b712557`, previous `d3ae88be46`, 10 of 10 checksums cross-checked against the host), `85fcb792f1` runbook 7.2. Rollback: the pre-deploy content held by `d3ae88be46`, S3 tarball `opal-gateway-d3ae88be46.tar.gz`, 895333 bytes, sha256 `764f565cffef310156c85a4c31ad972d10615f0fbc0c732c8fa8fceca3f8b236`.
