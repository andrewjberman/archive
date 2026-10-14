# Never-widen half (CTO) -- OG-yr-1: the refreshed /yearinreview page and the viewer gate opened to all Opal employees

By: `1.0.0_SA_CTO~Z`, 2026-10-14 ~22:5xZ. **SIGNED.**

**Against:** `deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-yr-1.md` @19beacdb10, read whole, sha256 `6299198a5778...`.
**Pinned to:** release `bf7ffb62f4ae5af8298d3c24960c63d2965542d9` on the live base `bacec95ccd6cafd2201f7433af24ae2748732355`.
This half covers the THREE-file release, not the one-file release pre-stated in my msg 34244. If `deployed_commit` at the
act is not `bacec95ccd`, it does not cover the act.

## What I read
- `git diff --stat bacec95ccd bf7ffb62f4`: 3 files (the page, `app/yearinreview_view.py`, its test file), +59 -14.
- The gate change, line by line: `return _is_opal_user(email) or (bool(roster) and email in roster)`. That is the
  gateway's own Opal-users predicate, which refuses the `#EXT#` guest form. The roster still admits everyone it admitted.

## The widening signed
Viewers of `/yearinreview` go from the owner roster (1 identity live) to every verified non-guest Opal identity.
Andrew-direct ~22:2xZ: "I need it viewable by all opal employees". Unchanged: the ALB OIDC action, GuardMiddleware,
the route, the 403 for outsiders and guests, IAM, `.env`, the tool registry, storage.

## Rollback
Redeploy `bacec95ccd` via `safe-ec2-deploy.sh` (parity 107 of 107). That restores the old page and the owner-only gate in
one act.

## Correction of my own instruction
In msg 34266 I said to grade the page md5 against the LF blob `3bbd5ab2`. That was wrong for the HOST. This path is
`eol=lf`, and the deploy tars the checked-out file, so the host receives `0d828b51` (the CRLF form). The ask measured
that by a checkout and re-hash. **The oracle is `0d828b51d433a24f7e2ef2e6ea7967ee`**, as the ask's section 5 states.
The blob equality is a repo fact, not the served one.

## Actor
One deployer: `0.7.0_AE_CloudOps~Z` (my msg 34258). `4.0.0_SA_CRO~Z` stood down (its msg 34262: nothing opened).
