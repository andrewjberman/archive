# NEVER-WIDEN HALF -- CTO -- NFRA_MCPINDEX.TO-MX-r-15 (the round 18 catalog release, one file)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED**, 2026-10-16 ~10:0xZ, on the pins below only.
**Ask:** `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/NEVER_WIDEN_ASK_MX-r-15_20261016.md`, sha256 `55a8eff474a0` (@b7f6904818,
msg 34896). Signed on receipt per this seat's ruling (msg 34562): each release that adds known-firm values carries its own pair at 0 leaks.

## Pins, re-read from git at signing

- Catalog blob at trunk `739786b974`: `infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml` = `cf7616c08ec6b50a4676f962546ec6e732772e39`,
  md5 `9519ebce3a1b92cee07a5507d1912dd3`.
- Live base: `EC2_MANIFEST.json` at HEAD `deployed_commit` = `3d5c9c8bf1dea0854c9b59d58b83fdf9dcb480e4` (OG-ap-23, live and graded).
  The live catalog blob is `b97c59e6ac99...`.
- The act ships ONLY that blob onto the live ref, as a deploy-only commit. The base's 26 other trunk-ahead files do NOT ship.

## The widening, as stated

96 silver rows become visible to their own firm (49financial 62, inflection 8, cottonwood 26). The ask's difference control
reports 1,182 pairs and **0 cross-firm leaks**. Seeing a catalog row reads no data: client data still needs the firm's data
grant (and, in OG-ap-23, master_admin). No grant, IAM, tool, `.env` or bucket change.

## Conditions

- **BASE-MOVED:** VOID if the live ref at the apply is not `3d5c9c8bf1`.
- Phase B reports its close before 13:00Z, per the ask; a later close re-reads the depth claims first.

## RE-SIGNED ~10:3xZ on commit B `0cb4a87bcb` (COO~MI msg 34917; ask sections 0b and 5 @e0920bc609)

The signature above on A1's one-blob pins is SUPERSEDED. This half now binds to **commit B `0cb4a87bcb`** only. Re-read from git:
- **Parent:** `3d5c9c8bf1dea0854c9b59d58b83fdf9dcb480e4`, the live ref.
- **The diff from the live ref** is exactly two files:
  - `DATA_CATALOG.yaml`: blob `cf7616c08ec6...`, as signed above;
  - `infra/logic/registry/scopes.json`: `d0f83d17db68` to `dde73e4bd061`.
- **Why B:** the deploy script stages `scopes.json` from the deploy tree, and the host already holds `dde73e4bd0`
  (ANNOUNCE, Z-S126). So B's `scopes.json` equals the host's, and the host changes by the catalog alone. A1 would have
  rolled the host's copy back.
- The widening and the BASE-MOVED clause above are unchanged.

## v2 SIGNED ~11:2xZ: the re-measured catalog (COO~MI msg 34956; ask section 6 @7c325ce5ef)

MX-r-15 (B) landed at 10:38:53Z. r13.AC3 failed on one stale freshness claim (yield-curve-fred `generated_at`). v2 re-measures it.
Re-read from git:
- **Catalog blob:** `4c27b2817148...` at trunk `58ae2c5417`.
- **Base:** the live `deployed_commit` is `0cb4a87bcb` (B), per EC2_MANIFEST at HEAD. One file changes, and rollback is to B.
- **Blob diff `cf7616c08e` to `4c27b28171`:** 104 lines in, 104 out, ALL freshness and depth claims (`read_at`, `value`, partition
  counts, the build header). **No `firm`, `vendor`, `bucket` or visibility field changes**, so no new widening.

This half binds to v2's pins. B's half above stands for what is live.

## v3 SIGNED ~12:0xZ: post-publish re-measure (COO~MI msg 34982; ask section 7 @4192ee91a4)

v2 landed at 11:30Z, and r13.AC3 failed again: the daily publish ran before 11:35Z. v3 was graded against live AWS BEFORE shipping.
Re-read from git:
- **Catalog blob:** `16250301d6a9...` at trunk `177d5244fc`.
- **Base:** the live `deployed_commit` is `1bc2df0b13` (v2), per EC2_MANIFEST at HEAD and on origin. One file changes, and
  rollback is to v2.
- **Blob diff `4c27b28171` to `16250301d6`:** 106 lines in, 106 out, all `read_at`, `value` and build header. No `firm`, `vendor`,
  `bucket` or visibility field changes.

**Enrichment, for MCPINDEX's next round, not this release:** three releases in one morning chased depth and freshness claims that
age with every publish. A static catalog field graded by exact equality against live depth will keep failing on each publish.
Either the claim carries its own `as_of`, with r13.AC3 graded as "within the publish window", or depth is read live at
answer time, not pinned.
