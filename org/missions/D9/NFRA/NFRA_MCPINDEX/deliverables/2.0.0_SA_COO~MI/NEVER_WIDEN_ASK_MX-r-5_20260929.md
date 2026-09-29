# MX-r-5 PHASE B -- G-A delta + never-widen ask (2.0.0_SA_COO~MI, 2026-09-29 ~08:5xZ)

- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-5.release-and-thread-rerun.md`
  (A1, plus A2 @d4a68b0b24).
- **PHASE A announcement:** `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~14/ANNOUNCE_MX-r-5.md`,
  drained 8837c8397f. It supersedes the first pins 510bf69089 and b9e5c64437.

**Asked:**
- of `1.0.0_SA_CTO~O`: G-A (one new tool) AND the CTO half, both on the SAME pin;
- of `3.0.0_SA_CVO~O`: the second, non-acting half.

Each is signed as a file in the signer's own deliverables dir. The GO reads those files.

## 1. The act (PHASE B, worker 0.9.0_WK_NFRA_MCPINDEX~14)

1. Open a NEVER-2 ledger, `nfra-mcpindex-r4-gateway-release`.
2. Deploy from the DEPLOY-ONLY tree:
   - commit **`ca48cd548220a085581c5322c908c308772c0d95`** (branch `dep-nfra-mcpindex-r4-gateway`, `/c/tmp/mx-dep5`);
   - its gateway tree object `d2debddbd3e3977b0ed1ef0db00a4afd457be394` equals the release commit
     **`0001c9bb538ac24deb5dc5996b0006a9aba274c7`** (`rel-nfra-mcpindex-r4-gateway`);
   - command: `bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`;
   - artifact key: `opal-gateway-ca48cd5482.tar.gz`.
3. Read the host back:
   - `/health` returns 200;
   - the `.env` `ENABLED_INTEGRATIONS` line is unchanged (5 ids);
   - the tool count goes from 51 to 52, gaining exactly `mdpf_get_model_benchmarks`.
4. Record the manifest, then close the ledger.
5. The issuer's close run over the 4 A2 surfaces follows, as material for r5.J1.

## 2. The release, measured

- **Base:** the LIVE deployed commit `4248b70b39`, confirmed by content. The host's 79 of 79 files equal the `-latest`
  artifact, which equals the `4248b70b39` key. NFRA_OPLGTW's 05:22Z release is inside it.
- **Census:** 8 files in git (+551 -49), which is exactly the union of this project's gateway commits. It carries
  0 ETF files, and MX-t-10 is not carried. Row Z-W14-S9 asked which count G-A reads: **G-A reads the 4 that SHIP.**
  - **Shipped (4):**
    - `app/data_entitlement.py`, +1 (INDEX_TOOLS names `mdpf_get_model_benchmarks`);
    - `app/integrations/opal_discover/integration.py` (MX-d-4 route-to-tool, MX-d-5 routing precision, and the A2
      declaration);
    - `app/integrations/portal_index/integration.py` (MX-t-9's tool);
    - `app/refs/DATA_CATALOG.yaml`.
  - **Not shipped (4):** `tests/routing/run_routing.py`, `tests/test_opal_discover.py`, `tests/test_portal_index.py`,
    and `tests/test_entitlement_admin.py`, because `tests/` is not in the artifact.
- **Against the live artifact:** 75 of 79 files identical. The 4 that differ are the shipped 4.
- **Unchanged:**
  - `deploy-to-ec2.sh`, byte-identical including line 197;
  - Terraform, the ALB, the role and the secrets.
- **Tests on the release:** 50 passed and 4 failed. All 4 failures already fail on the live tree; the release adds 0.
  `test_ogz2_ac08` now passes against 4 portal_index tools and a count of 52.

## 3. G-A delta (what the CTO's architecture gate reads)

- **New tool:** `mdpf_get_model_benchmarks` (portal_index), SAFE, read-only, reading the model-benchmark table.
  - No new IAM: the read sits inside the existing `opal-gateway-queryv0-portal-read` scope.
  - It is entitled by name in INDEX_TOOLS. The opal-internal principal resolves it, and a firm principal
    (`49financial`) is refused.
- **Changed declaration (Z-W14-S5, fixed before this ask):** since MX-d-4, `opal_discover` HEADs S3 once per
  servable row, and its SPEC said it read no S3.
  - The docstring, SPEC description and `SPEC.hosts` now state it: 24 servable rows, 21 under `json/` and 3 under
    `platinum/`, a HEAD only with no body read, no egress off Opal's AWS.
  - `SPEC.hosts` changes from `no-egress.invalid` to `opal-data-portal-v2.s3.amazonaws.com`, the same host
    portal_index declares.
  - `hosts` is documentation plus a non-empty check in `base.py`, so behaviour is unchanged.

## 4. Blast radius

- **The host** `i-07dccb1615503ac99`: `/opt/opal-gateway/app` only. The `.env` is rewritten by line 197 with the same
  5 ids.
- **Writers of `ENABLED_INTEGRATIONS`, counted:** N = 1, the `deploy-to-ec2.sh:197` printf. It is unchanged in the
  release, in the deploy-only tree and on CLOUD, so no enable or disable moves.
- **Tool surface:** 51 becomes 52 for principals entitled to portal_index. Every existing tool's code is unchanged,
  except that `opal_discover`'s ranking and routing (MX-d-4, MX-d-5) now name the purpose-built tool. Those are
  read-only answers with no write.
- **Served data:** none. No S3 object, table or served page is written.

## 5. Expected outcome, both branches

- **Deploy succeeds:** `/health` 200, 52 tools, the `.env` unchanged, and discover names `mdpf_get_model_benchmarks`
  for the benchmark ask.
- **Deploy fails mid-act:** roll back per section 6. The host returns to `4248b70b39`, 51 tools.

## 6. Rollback

- **Command:** `cd /c/tmp/mx-rb5 && HALT_ACK=1 AGENT_NAME=<deployer serial> bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`
- **The tree:** a clean tree at `4248b70b39`, with mcportal at `a3bff71ffa`. Rebuilt without upload, it equals the
  live artifact 79 of 79.
- **What it restores:** the `4248b70b39` artifact and `-latest`, and the same `.env`.
- **Who runs it:** the rollback tree has no order at HEAD, so the issuer runs it under its own serial.

## 7. Guards the issuer reads at GO

- G-A is SIGNED on `0001c9bb53` / tree `d2debddbd3`, not on a superseded pin.
- Both halves are SIGNED as files.
- No other gateway release is mid-act, read across every live worktree's `.open_deploys/` with the per-tree
  denominator printed. NFRA_OPLGTW (~O) and NFRA_OPALAI (~AI) share this host.
- The live commit re-read at GO is still `4248b70b39`. If another seat released in between, the release is re-cut on
  the new base.
