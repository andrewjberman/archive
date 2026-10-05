# Never-widen ask -- OG-rl-6 Phase C2, r17c: /yearinreview OWNER-ONLY on live e91819e281

By: `2.0.0_SA_COO~O` (issuer), 2026-10-05 ~14:xxZ.
- **Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-6.gateway-release-r17.md`, amendments
  A1-A4 (A4 @20b7b406df).
- **Spec:** CTO R14 and R15 (`ledger/ROUND_ANALYSIS.round16.md` s.6-7, R15 @16f729348e).
- **Andrew-direct:** record @121b7b016e, verbatim "Visible to me only. Eventually will be visible to select managers at
  my discretion."
- **PHASE C-A2 evidence:** `deliverables/0.9.0_WK_NFRA_OPLGTW~15/ANNOUNCE_OG-rl-6-C2.md`, drained @43c04ceb2d.
- **Supersedes:** `NEVER_WIDEN_ASK_OG-rl-6-C_20261005.md`. That ask's tenant-wide bytes, `14e0af86fa`, and their
  halves have lapsed.

**Halves owed, FRESH, all three against THIS file at its commit:**
- `1.0.0_SA_CTO~O` (CTO);
- `3.0.0_SA_CVO~O` (CVO), REQUIRED: served output moves, with a new route and a new `.env` key;
- `2.0.0_SA_COO~O` (COO): signed in section 5.

## 1. The bytes

**Release branch.** `rel-nfra-oplgtw-r17c` (`/c/tmp/og-rel13`), one commit `37be3485db` on live `e91819e281`. Host md5
reads 94 of 94 equal to live. The commit has 6 files:

| File | Change | Ships to the host? |
|---|---|---|
| `app/config.py` | +8: `YEARINREVIEW_VIEW_ALLOWED_EMAILS`, parsed like `SPRINT_VIEW_ALLOWED_EMAILS` | yes |
| `app/server.py` | +5/-2: import, guard-branch predicate, 2 Routes | yes |
| `app/yearinreview_view.py` | new | yes |
| `app/static/yearinreview/index.html` | new | yes |
| `deploy-to-ec2.sh` | +1 comment line, +1 printf token: `YEARINREVIEW_VIEW_ALLOWED_EMAILS=andrew@opalinvest.com` | no, but it renders `.env` |
| `tests/test_yearinreview_view.py` | new | no |

**Issuer re-read, independent of the worker:**
- `git -C /c/tmp/og-rel13 diff --stat e91819e281 HEAD` lists exactly the 6 files.
- The template delta is the one comment line plus one printf token.
- `_allowed()` reads `return bool(roster) and email in roster`. That is FAIL-CLOSED: an empty roster admits nobody.
  `/sprint`'s version admits the tenant on an empty roster.

**The four acceptance arms, through the real GuardMiddleware with a local ES256 key (`rl8_guard_arms.py`): 11 of 11.**
- With the roster set to the owner:
  - the owner gets 200;
  - a verified non-owner gets 403, with no page bytes, audited `DENIED` / `roster`;
  - a planted, unsigned identity gets 401;
  - no identity gets 401.
- With the roster empty, or missing: the owner gets 403 and the non-owner gets 403.
- Mutant control: `/sprint`'s empty-admits form fails `test_yearinreview_empty_roster_403`.

**Template render.** It produces 51 names, equal to `r17/ENV_KEYS_R17B.txt`. The new value's digest equals
`sha256("andrew@opalinvest.com")`. As a control, live's template renders 50 names.

**Rollback.** `/c/tmp/og-rb12` at `e91819e281`, equal to the live S3 artifact for 94 of 94 files. Rollback renders the
r17 template, which brings back 50 names and no `/yearinreview` route.

## 2. Blast radius -- what the act may touch

**Host app files.**
- Before: live `e91819e281`.
- After: `config.py` and `server.py` change, and the view and the page are added.
- Rollback: redeploy `/c/tmp/og-rb12`.

**Host `.env`.**
- Before: 50 names.
- After: 51 names, with `YEARINREVIEW_VIEW_ALLOWED_EMAILS` holding andrew@ only. Every other value hash is unchanged.
- Rollback: the r17 render.

**Served `/yearinreview`.**
- Before: 404.
- After:
  - andrew@ gets 200;
  - any other verified tenant identity gets 403;
  - no identity, or a forged one, gets 401;
  - publicly, the ALB OIDC wall returns 302 first.
- Rollback: redeploy.

**Every other route.** Unchanged. The verify re-reads the floor: `rl6.AC1`, `ht.AC2`, and `rl4.AC1` against the
51-name set.

**Unchanged:** the 65 tools; grants and the state store (0 writes); Terraform, IAM, the ALB, secrets, the contract.

**Egress (row Z-W15-S49).** Verifying a planted identity makes the host fetch the regional ELB public key once, from
AWS's own key endpoint. That is the same call every real request makes. It is Opal's own AWS identity path, not a
vendor.

**Manifest.** `deployed_commit` moves; the previous value is `e91819e281`.

## 3. The named properties and their writers

**(a) Who reads `/yearinreview`.**
- Writers, N = 3:
  - the ALB OIDC wall (unchanged);
  - the GuardMiddleware identity branch (CHANGED: a predicate added);
  - the roster: `config.py` parse, the template value, and `_allowed` (NEW).
- Expected: only andrew@ is served. Every other identity gets 403, and an absent identity gets 401.
- Other branch: any non-owner gets 200, or an empty roster admits anyone. That is a widening; roll back at once.

**(b) The `.env` key set.**
- Writers, N = 1: the template render (CHANGED by exactly one key).
- Expected: 51 names, the 50 before plus the one key; every other value hash unchanged.
- Other branch: any other name lost or added, or any other value changed; roll back.

**(c) Every route that existed before.**
- Writers, N = 1: `server.py` routing and middleware (CHANGED).
- Expected: the floor passes and the tools are still 65.
- Other branch: any regression; roll back.

## 4. Act and verify (PHASE C-B, steps 18-21)

1. Re-read live; if it moved, re-cut.
2. Open ledger `nfra-oplgtw-gateway-release-r17b`, entry and sentinel first.
3. Run `rl7_verify.sh before`.
4. Deploy from `/c/tmp/og-rel13` with `DEPLOY_BASE_REF=e91819e2819df8c8df5708bc66e4f4273bb1a834`.
5. Run `rl7_verify.sh after` immediately (17 checks).
6. On any failure: roll back from `/c/tmp/og-rb12`, re-verify, and close ROLLED BACK.
7. Run AC3 and AC4, each against its `<expect>`.

The signed-in 200 at Andrew's browser is reported to him as UNEXERCISED until he opens the page.

## 5. Halves

**COO -- SIGNED, `2.0.0_SA_COO~O`, 2026-10-05.**
- The act may touch exactly the keys in section 2 and the manifest.
- The rollback is pre-built and proven equal to live.
- Both branches are named for every property in section 3, with each property's writers counted.
- My reads of the release diff and the fail-closed predicate are independent of the worker's.

**CTO -- owed.**

**CVO -- owed** (required).
