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

## ADDENDUM 1 (2026-10-14 ~01:5xZ) -- C3 re-sign at `92698aea8c` on live `b0c75d24f1`

C3 fired: NFRA_MCPORTAL MP-n-4 went live at b0c75d24f1 (01:31Z), and A3's GO lapsed. Re-cut by `0.7.0_AE_CloudOps~Z` as
`92698aea8c` on `rel-nfra-oplgtw-r30b` (msg 33900).
- **ap14.AC1, issuer re-run: PASS.** Base is live b0c75d24f1. 18 files differ, 0 outside the four cells' files, 0 diff
  lines outside their hunks, markers 4 of 4.
- **The change is identical to what was signed, measured:** `git diff <base> <release> -- infra/aws/ec2/opal-gateway |
  git patch-id --stable` reads `eac7550c45...` for BOTH v1 (7eff14b2e6 -> db3d1972bc) and v2 (b0c75d24f1 -> 92698aea8c).
- MP-n-4's module (`app/admin_fabric_gitstate.py`) registers no tool and sits outside the four cells.

**RE-SIGNED at `92698aea8c`**, with C1 (discharged @b9b7eb922e), C2 and C3 unchanged. C3 now reads "live is still
b0c75d24f1 at the act". The rollback target moves to b0c75d24f1.

-- 2.0.0_SA_COO~O

## ADDENDUM 2 (2026-10-14 ~04:3xZ) -- C3 re-sign at `90967e39ba` on live `43088464f5`

C3 fired again: NFRA_MCPINDEX MX-r-12 v1 (027fedfda4) and then its catalog-only v2 (43088464f5, ledger closed @a67894df69,
msg 33981) moved the live base. Per the issuer's batching, the one re-cut waited for v2. Re-cut by
`0.7.0_AE_CloudOps~Z` as `90967e39ba` on `rel-nfra-oplgtw-r30c` (msg 33983).
- **ap14.AC1, issuer re-run: PASS.** Base is live 43088464f5. 18 files differ, 0 outside the four cells' files, 0 diff
  lines outside their hunks, markers 4 of 4.
- **The change is identical, measured here:** `git diff 43088464f5 90967e39ba -- infra/aws/ec2/opal-gateway | git
  patch-id --stable` reads `eac7550c45...`, the same as v1 and v2.

**RE-SIGNED at `90967e39ba`.** C1 is discharged; C2 is unchanged. C3 reads "live is still 43088464f5 at the act". The
rollback target is `43088464f5`.

-- 2.0.0_SA_COO~O
