# Never-widen ask -- OG-rl-6 Phase C, the r17b opal-gateway release carrying /yearinreview on live e91819e281

By: `2.0.0_SA_COO~O` (issuer), 2026-10-05 ~03:5xZ.
- **Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-6.gateway-release-r17.md`,
  amendments A1 @8068200b8f and A2.
- **Spec:** CTO R14 (`ledger/ROUND_ANALYSIS.round16.md` s.6 @b478972fec; msg 29402).
- **Andrew-direct:** "id publish it at mcp.opalinvest.dev/yearinreview". Then, relayed by 0.0.0_AB_MSTR~Z msg 29448:
  "...get that in position from the sitez box, as they are in control of deploys".
- **PHASE C-A evidence:** `deliverables/0.9.0_WK_NFRA_OPLGTW~15/ANNOUNCE_OG-rl-6-C.md`, drained @432c3f0fbb.

**Halves owed, all three against THIS file at its commit:**
- `1.0.0_SA_CTO~O` (CTO);
- `3.0.0_SA_CVO~O` (CVO), REQUIRED, because served output moves: a new page route;
- `2.0.0_SA_COO~O` (COO), signed in section 5.

## 0. ONE QUESTION FOR ANDREW (row Z-W15-S46), not for any half

`/sprint` is owner-only. It sits behind the identity wall AND a host-side roster filter. As built by its kit,
`/yearinreview` has only the identity wall, so **every signed-in Opal tenant account can read the page**, not only
Andrew.

The question: is "publish it" tenant-wide (ship as built), or owner-only like `/sprint` (a kit change before release)?

**Issuer recommendation:** ship as built, tenant-wide behind sign-in. "Publish" reads as wider than the owner, and the
page is behind the Opal tenant's OIDC wall either way. This seat does NOT decide it: scope is relayed, never
adjudicated. Phase C-B waits on the three halves AND on his word on this question.

## 1. The bytes

**Release branch.** `rel-nfra-oplgtw-r17b` (`/c/tmp/og-rel12`), one commit `14e0af86fa` on live `e91819e281`. Host md5
reads 94 of 94 equal to live (SSM e392ab0a). The commit touches 4 files:
- `app/server.py`: +5/-2. One import, one added `or` in the GuardMiddleware identity branch, and two Routes, the same
  hookup as `/sprint` and `/rivalfunds`;
- `app/yearinreview_view.py` (new);
- `app/static/yearinreview/index.html` (new, ASCII);
- `tests/test_yearinreview_view.py` (new, NOT shipped: the tarball carries no `tests/`).

**What the diff does not touch:** no S3 address, IAM, ALB, Terraform, template, contract or `.env` file. That is read
from the release diff, not the README. The applied hookup reported `OK: 3 edits applied` (3 of 3 anchors), and the body
lines of the release's `server.py` diff equal the CLOUD-source diff's (row Z-W15-S44: hunk header only).

**Tests on the release tree:**
- `test_yearinreview_view.py` 5;
- `test_sprint_view.py` 8;
- `app/tests/test_rivalfunds_view.py` 11;
- `test_schwab_q7_asset_download.py` 4;
- `test_ogz2_ac08` 1.

**Rollback.** `/c/tmp/og-rb12` at `e91819e281`. Its 94 gateway files equal the live S3 artifact
`opal-gateway-e91819e281.tar.gz`.

## 2. Blast radius -- what the act may touch

**Host app files.**
- Before: live `e91819e281`.
- After: `server.py` changes, and 2 new files are added.
- Rollback: redeploy `/c/tmp/og-rb12` with `DEPLOY_BASE_REF` set to the release sha.

**Served `GET /yearinreview` and `/yearinreview/`.**
- Before: 404 on the host. Publicly, the ALB's OIDC wall answers 302 on every path.
- After: no identity gives 401; a verified Opal identity gives 200 and the page; the trailing slash redirects.
- Rollback: redeploy.

**Every other route.** Unchanged. The GuardMiddleware edit adds one path predicate to the identity branch; the floor
checks `rl4.AC1`, `ht.AC2` and `rl6.AC1` re-read the r17 surfaces after the act.

**Unchanged:** the tool list (65); `.env` (50 key names); grants and the state store (0 writes); Terraform, IAM, the
ALB, secrets, the contract and the template.

**Manifest.** `deployed_commit` moves; the previous value is `e91819e281`. Rollback reverts the manifest commit.

## 3. The named properties and their writers

**(a) Who can read `/yearinreview`.**
- Writers, N = 2: the ALB OIDC wall (unchanged) and the GuardMiddleware identity branch (CHANGED: one predicate added).
- Expected: the public unauthenticated GET is 302 to login.microsoftonline.com, and the host-local GET with no identity
  is 401. Signed in, it is any tenant account unless Andrew rules owner-only (section 0).
- Other branch: a 200 without identity; roll back at once.

**(b) Every route that existed before.**
- Writers, N = 1: `server.py` routing and middleware (CHANGED).
- Expected: the floor checks pass (`rl4.AC1`, `ht.AC2`, `rl6.AC1`), and the tool list is 65.
- Other branch: any regression; roll back.

**(c) The page bytes.**
- Writers, N = 1: the static file (new).
- Expected: the host md5 equals the release.
- Other branch: a mismatch; roll back.

## 4. Act and verify (PHASE C-B, from the order, steps 18-21)

1. Re-read live; if it moved, re-cut.
2. Open ledger `nfra-oplgtw-gateway-release-r17b`, entry and sentinel first.
3. Run `rl7_verify.sh before`.
4. Deploy from `/c/tmp/og-rel12` with `DEPLOY_BASE_REF=e91819e2819df8c8df5708bc66e4f4273bb1a834`.
5. Run `rl7_verify.sh after` immediately. It checks 15 items: md5, the 65 tools, the 50 names, the host-local 401, the
   public 302, `rl6.AC1`, `rl4.AC1` and `ht.AC2`.
6. On any failure: roll back from `/c/tmp/og-rb12`, re-verify, and close ROLLED BACK.

## 5. Halves

**COO -- SIGNED, `2.0.0_SA_COO~O`, 2026-10-05.**
- The act may touch exactly the keys in section 2 and the manifest.
- The rollback is pre-built and proven equal to live.
- Both branches are named for every property in section 3, with each property's writers counted.
- The audience question (section 0) is routed to Andrew, not decided here.

**CTO -- owed.**

**CVO -- owed** (required: served output moves).
