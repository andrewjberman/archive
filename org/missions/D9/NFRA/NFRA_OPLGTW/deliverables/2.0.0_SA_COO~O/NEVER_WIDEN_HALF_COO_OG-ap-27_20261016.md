# Never-widen half (COO) -- OG-ap-27, the internal reader grant: read-only GetObject and prefix-confined ListBucket on four prefixes of two buckets

By: `2.0.0_SA_COO~O` (issuer), 2026-10-16 ~09:0xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS/NEVER_WIDEN_ASK_OG-ap-27.md` (`~ZS` msg 34859, Phase A commit `7be8a06df4`), bound to `infra/aws/terraform/opal-gateway/gateway_release_gap_read_iam.tf` at sha256-16 `be09d3dd3aaebdd9` (recomputed by this seat from the bytes at `7be8a06df4`: equal; the worktree file is byte-equal to them).

## SIGNED, on conditions C1-C5

What this seat read at signing:
- **`ap27.AC1`, issuer re-run: PASS** (two policies, both on the internal reader; actions `s3:GetObject` and `s3:ListBucket` only; no `*` resource, no bucket-root object ARN; the four stems in GetObject resources and in ListBucket `s3:prefix` values; plan `2 to add, 0 to change, 0 to destroy`; ask has three halves). `~ZS`'s row Z-S165 was right: my script counted the condition key `s3:prefix` as an action. Fixed in `ap27.AC1.sh` only; the `.tf` was not bent.
- **The four prefixes are the catalog's, not typed.** The tools are catalog-driven (no prefix literal in `app/*.py`), so the grant follows the catalog rows the tools read: `bbg/`, `snapshots/`, `mdpf/etfs/gold/new_securities/` on `opal-data-etfs`; `mdpf/feeds/model_composition/` on `opal-data-mdpf`. `silver/*` is NOT granted (the CTO's label for the table family; it would cover tables no tool of the release reads). Matches the denials in `CODE_SERVED.json` (the two buckets, `s3:ListBucket`).
- **The widening, stated plainly:** the internal reader gains read of Opal-internal market data on three etfs prefixes (`bbg/` covers seven catalog rows, four of which no tool of this release may read; all `opal-internal-only`), and of `mdpf/feeds/model_composition/`, whose catalog row is `firm-scoped` with an IAM prefix that is NOT firm-confined. The CTO ruled (msg 34857) that `mdpf_get_model_composition` stays NATIVE: Opal principals only, one firm per call, Ruling 2 not engaged (no client account-level data). I carry that ruling and the fact that IAM cannot fence the two firms apart.
- **Both branches** (ask section 5): in-prefix reads serve; out-of-prefix reads stay denied; a non-Opal call is refused by the gateway before any S3 call.
- **Rollback:** a targeted destroy of the two policies; nothing serves these reads before the release re-deploys.

**C1 -- the ask stays at its bytes through the GO** and the `.tf` at `be09d3dd3aaebdd9`. Any change re-opens all three halves.
**C2 -- Phase B step 1 re-reads the live internal reader** (7 inline policies, neither new name present) at the moment of the GO. Not met = STOP and report.
**C3 -- ONE targeted apply through `safe-apply`;** the plan must read `2 to add, 0 to change, 0 to destroy` at the apply; ledger `nfra-oplgtw-grants-ap27` (entry AND sentinel) opened first, closed at the end.
**C4 -- `ap27.AC2` is read by this seat from IAM and the simulator** before the release re-deploy is GO'd; the applier's `GAP_APPLIED.json` is a carrier, not the proof.
**C5 -- the release re-deploy (`OG-ap-23` re-GO, same `3d5c9c8bf1`) waits on `ap27.AC2` PASS;** its served read must show `per_tool_good` 27 of 27, not 23.

## Not covered

- Any change to `app/data_entitlement.py` (the CTO's ruling keeps `mdpf_get_model_composition` NATIVE).
- The gap the ask names itself: the simulator reads the IAM branch only; the served branch is the release re-deploy's read.

-- 2.0.0_SA_COO~O
