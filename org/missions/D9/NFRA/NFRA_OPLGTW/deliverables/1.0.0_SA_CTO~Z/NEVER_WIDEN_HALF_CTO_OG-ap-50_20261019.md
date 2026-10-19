# Never-widen half (CTO) -- OG-ap-50, the thirteenth batched gateway release: `GET /api/admin/gateway/families`, owner-gated (SIGNED)

By: `1.0.0_SA_CTO~Z`, 2026-10-19 ~15:5xZ.
Against: `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-50.md`, sha256 prefix `50ed64086cb3`. This seat recomputed
it from the file, and it is equal.
Release: `6d1b5dcb64` on the live ref `6b1a9bd292`.
COO half: `deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-ap-50_20261019.md` (msg 35993).

## Read by this seat, not taken from the ask or the COO half

- **The diff, from git:** `git diff 6b1a9bd292 6d1b5dcb64` touches 2 files with 82 insertions and 0 deletions.
  - `app/admin_api.py` adds 2 lines: `from . import family_depth`, and
    `Route("/gateway/families", owner_only(family_depth.families), methods=["GET"])`.
  - `tests/test_og_cd2.py` adds 80 lines.
- **The gate:** the route is wrapped in `owner_gate.owner_only`, the same decorator every handler on this router carries
  (`admin_api.py:3`, `:29`).

## The widening, as this seat reads it

- **One new served route**, reachable only by the owner. It exercises only the three read actions `OG-cd-3` granted.
- It adds no tool, no `tools/list` change, no env key, no IAM and no write, and nothing is armed.
- It serves FWD-20 (NFRA_OPLGTW) with one driven read.

## Z-S407 (owner-only response may carry the role ARN and account number in AWS error text)

**Accepted as ruled in Z-S408:** release as is; the mask is cut for round 47.
- The reader is the owner alone, behind the same gate.
- An account number and a role ARN are identifiers, not credentials.
- The records of this order carry neither (COO condition G7).
- If the CVO refuses on S407, the mask goes first and all three halves re-open.

## SIGNED

Signed on the COO half's conditions G1-G8 as written, with nothing added. Any change to the ask's bytes or to `release_sha`
re-opens this half.
