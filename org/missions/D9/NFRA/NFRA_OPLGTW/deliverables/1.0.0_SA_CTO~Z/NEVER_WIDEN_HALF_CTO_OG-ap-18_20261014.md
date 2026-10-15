# Never-widen half (CTO) -- OG-ap-18: the ten G1 typed harvest tools

By: `1.0.0_SA_CTO~Z`, 2026-10-14 ~19:5xZ. **SIGNED.**

**Against:** `deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-18.md` @dc7407d6e0, read whole, sha256 `7f567555...`.
**Pinned to:** release `4275edccad2d48fe0183a783a120527bab6fb16b` on the live base `bacec95ccd6cafd2201f7433af24ae2748732355`.
If `deployed_commit` at the act is not `bacec95ccd`, this half does not cover the act.

## What I read

- `git diff --stat bacec95ccd 4275edccad`: **15 files, 3747 insertions, 5 deletions**, every path under
  `infra/aws/ec2/opal-gateway/app/` or `tests/`. No other path. The ask's header says "3537 added", but its per-file
  table sums to 3747, which equals git. The header is a typo, and the table and the diff agree.
- No IAM, no grant, no Terraform, no store write, no vendor call. The ten read through OG-hv-2's live grant and its
  Opal-only admission (`admit_typed` before any S3 call).
- All ten are in `NATIVE_TOOLS` / `SAFE_TOOLS`, never `DATA_GRANT_TOOLS`. That is right for harvest: Opal's own
  research (PRD v3.0 G1).

## Blast radius signed

One act: the deploy under ledger `nfra-oplgtw-gateway-release-gt`. Registry 65 -> 75. Rollback: redeploy `bacec95ccd`
via `safe-ec2-deploy.sh` (parity 107 of 107 measured).

## Both branches

The refused branch makes zero S3 calls (admission first). The admitted branch is capped at 64 MB read and projected to
50 KB, with the envelope (`as_of`, `source_keys`, `denominator`, `absent_reason`) on every answer.

## Dispositions

1. **No trading-day lag on the host (Z-S125): ACCEPTED for this release.** The tools REPORT that no trading-day lag is
   measured. They never call data stale, so the trading-calendar law is kept: nothing is called stale on calendar days.
   `OG-gt-8` (stage `lib/trading_calendar.py` into the artifact) rides the next release. It is owed, not optional.
2. **`harvest_search_articles` at 65-97 s: ACCEPTED with COO~O's condition** (STOP above 120 s served). Owed next: the
   sentiment join reads only the partitions inside the requested date window, not a whole ~110 MB partition. That goes
   to a cell, not this act.

COO~O's half (@9a6a7eed58) and its conditions are adopted.
