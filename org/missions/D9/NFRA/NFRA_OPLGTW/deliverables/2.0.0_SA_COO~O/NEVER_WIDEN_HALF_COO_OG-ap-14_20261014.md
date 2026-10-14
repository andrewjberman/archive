# Never-widen half (COO) -- OG-ap-14, the r30 gateway release (pf-1 + tg-1 + bd-2 + sh-1)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-14 ~01:3xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-14.md` @c832d025b2, release
`db3d1972bc` on branch `rel-nfra-oplgtw-r30`, base = live `7eff14b2e620c8c1f688d41de6f37c09addde7b4`.

## SIGNED at `db3d1972bc`, on conditions C1-C3

What this seat read at signing:
- **ap14.AC1, issuer re-run: PASS.** Base is the live ref 7eff14b2e6. 18 files differ, 0 outside the four cells' files,
  0 diff lines outside their hunks, markers 4 of 4. No other unreleased cell rides; the ask's section 3 lists the four
  excluded `app/` files.
- **Who gains and who loses** (ask section 2): pf-1 widens the one active profile (`2c61471b14`) to non-data tools;
  bd-2 narrows unprofiled non-admin callers; sh-1 adds one READ tool under each caller's own token.
- **Suites:** 46 passed, 1 failed (`test_ogz1_ac08`). It fails identically at the live ref (a pinned route set never
  moved for OG-ap-7's `/hx/teams/*` routes), so this release does not introduce it.
- **Non-ASCII:** commit-gate's 7-line WARN on `app/tools.py` is pre-existing, measured here. The live and release files
  carry the same 7 lines (em-dashes in comments and docstrings), and the release adds none.
- **Rollback:** redeploy live `7eff14b2e6`, which is measured as the running bytes (105 of 105 md5).

**C1 -- the ask omits one widening, and this half names it.**
- Section 2 calls OG-tg-1 "NARROWS, twice over" and says "nobody gains reach". That is true of its sender gate, but
  not of its unscoping.
- Removing `opalbloomberg`'s `_SEED` entry and its overlay rows (PRD v2.3 item 2) WIDENS the Bloomberg principal's tool
  set to Andrew's. Today that principal is denied 8 of 8 gateway data tools (`identity_scope_denied`; 0.0.3_BG_BBGTerminal
  log, 10-13); after this release the identity scope admits them.
- This is the widening the CTO's positive arm (msg 33850) and A2's `bbg_identity_admitted_8` exist to grade. Andrew's
  word covers it: "opal-gateway-bbg should be an exact copy of opal-gateway for now".
- I sign it as named here. The applier corrects ask section 2 to name it, as a record correction, before B2.

**C2 -- the served read carries every A2 field.** `bbg_identity_admitted_8` reads 8, through the installed code. A
value below 8 is a STOP and a redeploy of the base, not a pass.

**C3 -- the queue and window.** Ledger `nfra-oplgtw-gateway-release-r30` opens entry-and-sentinel-first, inside
11:00Z-23:00Z, with no other gateway release in flight across all worktrees (per-tree denominator printed). If
NFRA_MCPORTAL MP-n-4 lands first (msg 33857), the live base moves. This half then does NOT carry: B1 re-cuts on the
new deployed_commit, AC1 re-runs, and both halves re-sign at the new `release_sha`.

## Not covered

- The two r30 grant writes (OG-mg-1, their own pair).
- OG-hv-2's harvest release.
- Any other gateway change.

-- 2.0.0_SA_COO~O
