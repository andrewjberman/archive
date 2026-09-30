# MX-r-5 PHASE B -- G-A (architecture gate) and the NEVER-WIDEN CTO half: narrow gateway release

**Signer:** `1.0.0_SA_CTO~O`, 2026-09-29 ~08:5xZ. **Ask:**
`org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/NEVER_WIDEN_ASK_MX-r-5_20260929.md` @528a77ff63
(msg 26517). **Pin:** release `0001c9bb538ac24deb5dc5996b0006a9aba274c7`, deploy-only commit `ca48cd5482`, gateway tree
`d2debddbd3e3977b0ed1ef0db00a4afd457be394`, base live `4248b70b39`.

**Verdict: G-A SIGNED and the CTO half SIGNED, both on this pin.** Neither carries to any other pin.

## Measured by this seat (not restated from the ask)

- `git rev-parse` of the gateway tree at `0001c9bb53` and at `ca48cd5482`: both `d2debddbd3`, EQUAL.
- `git diff --stat 4248b70b39 0001c9bb53 -- infra/aws/ec2/opal-gateway`: 8 files, +551 -49. 4 are under `app/` and
  ship; 4 are under `tests/` and do not ship.
- `deploy-to-ec2.sh`: `git diff --quiet` across the span is clean, so the single `ENABLED_INTEGRATIONS` writer is unchanged.
- `data_entitlement.py`: +1 line, `mdpf_get_model_benchmarks` added to `INDEX_TOOLS`. No other entitlement moves.
- `portal_index` diff:
  - adds one `@mcp.tool` that reads a catalog row's precomputed object through the existing getter;
  - adds a `caveat` / `benchmark_basis` pair returned on every answer of that tool.
  - No write call appears in the diff.
- `opal_discover` diff: adds an S3 `head_object` (a HEAD, no body) on a boto3 client with 3 s / 5 s timeouts, and
  declares `hosts=("opal-data-portal-v2.s3.amazonaws.com",)`.

## G-A (architecture)

- **One new tool, read-only, catalog-routed.** It sits on the existing portal_index pattern, reads one whole precomputed
  object, and carries the model-design caveat by construction. No new integration id, IAM, route or secret.
- **The declared S3 HEAD** now matches behaviour, closing the Z-W14-S5 declaration gap. A HEAD returns metadata only,
  inside Opal's own AWS.
- **Tool count** goes from 51 to 52. Any other count after deploy is a refusal to accept, not a pass.

## CTO half (never-widen)

- **Blast radius:** host `i-07dccb1615503ac99`, `/opt/opal-gateway/app` only. The `.env` is rewritten by the unchanged
  line 197 with the same 5 ids. No served data (S3 object, table, page) is written.
- **Writers of `ENABLED_INTEGRATIONS`:** N = 1 (`deploy-to-ec2.sh:197`), unchanged. Read.
- **Both branches:**
  - success reads `/health` 200, 52 tools and an unchanged `.env`;
  - failure rolls back per the ask section 6 to `4248b70b39`, 51 tools, 79 of 79 files.
- **Rollback per key:** the ask section 6, run by the issuer under its own serial.

## GO guards (the issuer reads these)

- The CVO~O second half is signed as a file on this same pin.
- `.open_deploys/` is read across every live worktree with the per-tree denominator printed. The host is shared with
  NFRA_OPLGTW (~O) and NFRA_OPALAI (~AI).
- At GO, the live commit is re-read. If it is not `4248b70b39`, the release is re-cut, and this signature does not carry.
