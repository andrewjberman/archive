# Never-widen half (COO) -- OG-yr-1, the refreshed /yearinreview page and the viewer gate opened to all Opal employees

By: `2.0.0_SA_COO~O` (issuer), 2026-10-14 ~22:5xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-yr-1.md` (sha256 6299198a5778, read at HEAD),
release `bf7ffb62f4ae5af8298d3c24960c63d2965542d9` on branch `rel-nfra-oplgtw-yr2`, base = live `bacec95ccd6cafd2201f7433af24ae2748732355`.

## SIGNED at `bf7ffb62f4`, on conditions C1-C3

What this seat read at signing:
- **yr1.AC1, issuer re-run: PASS.** Base is the live ref `bacec95ccd`. Three files differ and they are the three the order names: the page, `app/yearinreview_view.py`, `tests/test_yearinreview_view.py`.
  The page blob equals the CRO's pin `947fc522a8` in LF form (md5 `3bbd5ab2d325657020357003c3ea387d`); the gate line and the three named tests are in the release.
- **The gate change, read in the diff:** `_allowed()` returns `_is_opal_user(email) or (bool(roster) and email in roster)`, as spec `@c8f3a38f43` gives it. `tools._is_opal_user` refuses the Entra guest form (`#EXT#`), which a suffix check would admit.
  The docstring is corrected to match the code. Two existing tests asserted 403 against an `@opalinvest` address the gate now admits; their subjects move to a non-Opal address and the admitted case is asserted directly. No assertion is weakened.
- **Who gains, who loses:** the readers of `/yearinreview` go from the owner roster (one identity today) to every verified non-guest Opal identity. That is Andrew's word, "I need it viewable by all opal employees", and the page's content (the operating review through 2026-10-11) is the
  Opal-internal brief. Non-Opal and guest identities are refused as before. Nobody loses. No tool, route, IAM, `.env` or storage change; the ALB authenticate-oidc action and GuardMiddleware are untouched.
- **Rollback:** redeploy `bacec95ccd` (parity measured 107 of 107); it restores the old page and the owner-only gate in one act.

**C1 -- the ask stays at its bytes through the GO** (sha256 `6299198a5778`).

**C2 -- the guard at the act.** The deploy tree's `git rev-parse HEAD` equals the full `release_sha`, its parent equals the live `deployed_commit` at the act, and no other gateway deploy is in flight (ONE actor: `0.7.0_AE_CloudOps~Z`, CTO msg 34259; `4.0.0_SA_CRO~Z` stood down).

**C3 -- the oracle for the served page is the CHECKED-OUT form.** The host receives the file as a clean checkout writes it (`0d828b51d433a24f7e2ef2e6ea7967ee`, 344 CRLFs), not the blob's `3bbd5ab2`. `yr1.AC2` is amended (A3) to compare the host with `0d828b51`. The served read also records the admitted arm
(an Opal identity gets 200) and the refused arm (a guest and an outside domain get 403, no page bytes).

## Not covered

- Any other gateway change, and `/sprint`'s gate.

-- 2.0.0_SA_COO~O
