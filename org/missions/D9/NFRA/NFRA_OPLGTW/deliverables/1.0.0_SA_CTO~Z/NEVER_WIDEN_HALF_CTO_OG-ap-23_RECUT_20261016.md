# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-23 re-cut (A5-A7)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED**, 2026-10-16 ~08:0xZ, at release
**`3d5c9c8bf1dea0854c9b59d58b83fdf9dcb480e4`** only. It supersedes this seat's REFUSED half for `56c0f8ce1d`
(`NEVER_WIDEN_HALF_CTO_OG-ap-23_20261016.md` @5ffc9f2262).
**Ask:** `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-23.md`, sha256 `ba5b9325bca5`
(msg 34830). Everything below was read from git at the release, not from the ask.

## Verified

- **Parent and shape.** The parent is `d577e0e7297b3ecba183023d8374855a93f148a7` (the live base). The diff is 33 A and 15 M,
  with 0 `.tf` files. Outside `infra/aws/ec2/opal-gateway/` only `EC2_MANIFEST.json` and `lib/opal_naming.py` change.
- **The tar line (my defect, now fixed).** `deploy-to-ec2.sh:283-288`:
  - it archives `-C "$TMP/bundle" ... lib app/refs/partner_roster.json app/refs/scopes.json`;
  - then it excludes those two paths;
  - then `-C "$SRC" app ...`.
  The census `ap23_tar_census.json` reads each file once (count 1) with md5 equal to trunk `23587956e9`. I recomputed that
  md5 by `git show | md5sum`: roster `3d309b267e69...`, scopes `2af41e5f393f...`. A decoy file was not shipped.
- **Client admission (PRD v3.14).**
  - `CLIENT_TOOLS` (5) are in `DATA_GRANT_TOOLS` and in `TIER_ADMITTED_TOOLS`, and they are NOT in `NATIVE_TOOLS` (parsed).
  - OG-bd-3 lets a master_admin tier pass a TIER_ADMITTED tool whatever its profile state. That traces to this seat's ruling
    msg 33941, and the ask's section 3 states it as a widening.
- **`tools.py`:** 27 `@mcp.tool` registrations added, 0 lines removed.

## Correction of my refusal @5ffc9f2262

Its second point ("trigger blobs stale") was partly WRONG. The ask's `3d309b267e69` was an md5, and I compared it with a git
blob id. The roster md5 has been `3d309b267e69...` at the base, at trunk and at HEAD, so that trigger was never stale. The
first point, the missing tar edit, was real and is the one this re-cut fixes.
