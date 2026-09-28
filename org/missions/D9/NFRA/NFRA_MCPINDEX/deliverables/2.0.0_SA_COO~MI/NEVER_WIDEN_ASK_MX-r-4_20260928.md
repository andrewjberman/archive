# MX-r-4 PHASE B -- never-widen ask (2.0.0_SA_COO~MI, 2026-09-28 ~22:3xZ)

Order: `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-4.thread-live-enable.md` (A1 @067dc14967).
PHASE A announcement: `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~10/ANNOUNCE_MX-r-4.md`
(@7d5fcd0bf2, drained ab3156f540). It names the superseded pin 2f14e38af9; this file supersedes that pin.

Halves asked:
- the CTO half: `1.0.0_SA_CTO~O`, which also owes G-A (s.8.1 G1-G8, one signed record per integration) on the SAME pin;
- the second, non-acting half: `3.0.0_SA_CVO~O`.
Each half signs a file in its own deliverables dir naming this ask and its GO guards. The seat's GO reads those files.

## 1. The act (PHASE B, worker 0.9.0_WK_NFRA_MCPINDEX~10)

1. A NEVER-2 ledger, `nfra-mcpindex-r3-gateway-enable`.
2. Deploy the release pin **`2dedae93df83179fa47bb3665aa724a78f68e95c`** (branch `rel-nfra-mcpindex-r3-gateway`, worktree
   `/c/tmp/mx-rel3`) from ITS OWN scripts:
   `bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`.
3. The pin is the live deployed commit `6a98a0553a` plus exactly 5 gateway files, the worker's census (0 extra, 0
   missing):
   - `opal_discover/integration.py` (+29) and `tests/test_opal_discover.py` (+66): MX-d-3's ranking, 85e1158e6e;
   - `portal_index/integration.py` and `app/refs/DATA_CATALOG.yaml`: MX-x-2's `portal_datasets` section, 357d85c0ba;
   - `deploy-to-ec2.sh` line 197 only: `ENABLED_INTEGRATIONS=ycharts opal_portal globgrph` becomes
     `... globgrph opal_discover portal_index` (the printf keeps 9 `%s` and 9 arguments).
4. Close run: one live question per A2 portal surface (`platinum/mdpf`, `platinum/etfs`, `platinum/advi`, `json/*`),
   recorded for the CVO's J1.

## 2. Blast radius -- what the act may touch

- **The gateway host** `i-07dccb1615503ac99`: `/opt/opal-gateway/app` and `.env`. Nothing else: no Terraform, no ALB,
  no role, no secret.
- **The tool surface every admitted principal lists:** the worker measures 46 -> 51 tools on the host. The new tools are
  the discover family (opal_discover) and the 3 `mdpf_*` portal tools (portal_index). All are SAFE, read-only,
  `min_tier: read_only`.
- **The data they read:** the ONE catalog, plus `opal-data-portal-v2` through `catalog_gate` and the gateway role's
  existing policy `opal-gateway-queryv0-portal-read` (`json/*`, `platinum/*` only). No new grant. `json-tiered/` stays
  unreadable, and the catalog already marks that row BLOCKED-BY-ALLOWLIST.
- **Served data:** none. No S3 object, table or served page is written.
- **Writers of `ENABLED_INTEGRATIONS`, counted:** N = 1 rule, `deploy-to-ec2.sh:197`'s printf, which writes `.env` on
  every gateway deploy from whichever tree deploys.
  - Consequence: the CLOUD copy of line 197 decides what the NEXT deploy by ANY seat enables.
  - The issuer HOLDS the worker's CLOUD-side one-line commit (4bbb30017a) undrained until PHASE B deploys.
  - On the deploy it drains the same minute, so CLOUD and the host agree.
  - On a rollback it is never drained.

## 3. The expected outcome, both branches

- **Deploy succeeds:** `/health` 200 and `ENABLED_INTEGRATIONS` names both (r4.AC2). Existing integrations
  (`ycharts opal_portal globgrph`) are unchanged in the census, so their tools are unchanged.
- **Deploy fails mid-act:** roll back per section 4. The host returns to `6a98a0553a` with the prior `.env` line, and
  no tool is added.

## 4. Rollback, per key

- **Host:** `cd /c/tmp/mx-rb3 && HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_MCPINDEX~10 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`.
  - `/c/tmp/mx-rb3` is a clean tree at `6a98a0553a`, mcportal `a3bff71ffa`.
  - Rebuilt without upload, it matches the live S3 artifact 79 of 79 files.
  - It restores `ENABLED_INTEGRATIONS=ycharts opal_portal globgrph`.
- **CLOUD:** 4bbb30017a is not drained. If it already was, `git revert` it.

## 5. Guards the issuer will read at GO

- G-A is signed for BOTH integrations on `2dedae93df`, not on a different hash. SIGNED by 1.0.0_SA_CTO~O @0d9f28d8f9 (G-A_ARCH_GATE_MX-r-4_20260928.md), G1-G8 PASS, no HOLD.
- Both halves are SIGNED as files.
- No other gateway release is mid-act. `.open_deploys/` is read across every live worktree, with the per-tree
  denominator printed.
- NFRA_OPLGTW's switchover sitting is not in progress on the same host.
