# NFRA_MSGRAPH.S2 — DEPLOY PLAN (coordinated; pre-execution)

**TO:** NFRA_MSGRAPH.S2 | **Lane:** 0.8.0_AE_CloudComp | **Date:** 2026-06-26
**Status:** ALL code + IaC built, committed, proven offline. This is the ordered, coordinated, irreversible deploy — held for the globgrph deploy-window + the deploy-go. Per CLAUDE.md: a begun deploy FINISHES in-session (open a deploy-completion ledger entry at start); coordinate the window with the NFRA_GLOBGRPH owner (no in-flight-derive clobber).

## What's already landed (reversible, committed, NOT yet applied/deployed)

| Component | Commit | State |
|---|---|---|
| Derive extractor + SS4 cert + 11/11 regression | `fb625d0f5` | committed, MS-disabled (`GLOBGRPH_MS_ENABLED=0`) |
| Gateway `/ms/*` endpoint (4 read GETs + `/ms/health`) + production `HttpMsGatewayCaller` | `5fd78e01e` | committed |
| Gateway TF: `/ms/health` 6h liveness probe + `MS_INGEST_BEARER` IAM grant | `1a23a3ed4` | committed, **not applied** |
| Server-layer READ-ONLY scoping (`_read_get` GET-pin) — Andrew 163709Z | `cac16138a` | committed |

## Pre-reqs (coordinate / confirm before step 1)

- **Globgrph deploy window** — the derive task-def env lives in the NFRA_GLOBGRPH TF root; the nightly Fargate derive must not be clobbered mid-run. COO to coordinate the window + name the owner.
- **Mint `opal/mcp/ms-ingest-token`** out-of-band (boto3, 32-byte; value never in TF state — same discipline as the OTP bearer). Register it in the PREMCP token inventory (CTO arch note A: A-class credential, inherits A1 revocation / A2 least-scope).

## Ordered deploy (each step finishes before the next; rollback noted)

1. **Mint the secret** `opal/mcp/ms-ingest-token` (boto3 `create-secret`). Rollback: `delete-secret`.
2. **Gateway TF apply** (`safe-apply` in `infra/aws/terraform/m365-mcp-gateway`): adds the `/ms/health` liveness Lambda + IAM grant + the secret read on `gw_golive`. Rollback: `terraform destroy` of the new resources (additive — no existing resource changed). 0-diff verify.
3. **Gateway code redeploy** (EC2, `safe-ec2-deploy.sh` per Rule 7/12: local→S3→EC2 pull): ships `ms_ingest.py` + the `server.py`/`config.py` changes; the on-box deploy step fetches `MS_INGEST_BEARER` → writes it + `MS_INGEST_IDENTITY=andrew@opalinvest.com` into the gateway `.env`. Verify: `GET /ms/health` with the bearer → `{"ok":true}` (proves the server-held delegated token mints). Rollback: redeploy the prior gateway artifact.
4. **Derive env wiring** (NFRA_GLOBGRPH TF root, WITH the owner): set on the derive task-def — `GLOBGRPH_MS_ENABLED=1`, `MS_GATEWAY_BASE_URL=https://mcp.opalinvest.dev`, `MS_INGEST_BEARER` (from the secret). Rollback: unset `GLOBGRPH_MS_ENABLED` (MS goes dark; AWS derive unaffected).
5. **Derive image rebuild + deploy** (globgrph Fargate): the container must carry `ms_cloud_extract.py` + the `derive_runner.py` edits. Coordinate with the globgrph owner's build/deploy path.
6. **First MS-enabled derive** — run in the coordinated window (NOT an ad-hoc validation run; per CLAUDE.md validate on the scheduled nightly's artifacts where possible, else a single coordinated enable run). Watch for `OK: MS_EXTRACT_COMPLETE nodes=... edges=...` + the AWS-superset invariant.
7. **comp-kuzu confirm** (the TO AC#1 + mandate): `comp-kuzu "MATCH (n) WHERE n.source='ms' RETURN labels(n), count(*)"` → MS nodes present + first-class + categorized; provenance header `current`. Also assert the AWS node count is unchanged (strict superset).
8. **Close the deploy-completion ledger entry**; RAVC COO (live MS estate in comp-kuzu → unblocks S3) + CTO (deploy + live confirm).

## Safety invariants carried through the deploy

- **Two fail-closed layers**: gateway `/ms/*` is read-only-by-construction (`_read_get` GET-pin) + structure-only (output allowlist); the derive SS4 emit cert fails the derive closed on any content/comms leak.
- **Additive-only**: a gateway/MS failure never fails the AWS derive (best-effort fold); a content/comms leak fails the WHOLE derive closed (return 1, no commit) — the catastrophic floor.
- **MS-disabled is the safe resting state**: if anything in 4–6 misbehaves, unset `GLOBGRPH_MS_ENABLED` and the estate reverts to AWS-only, byte-identical.
