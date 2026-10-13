# CTO half -- NFRA_MCPORTAL MP-z-5: the gateway release that serves the FWD-20 breakdown page

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-13 ~20:5xZ.
**Ask:** `0.7.0_AE_CloudOps~MQ` msg 33749;
`org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~MQ/NEVER_WIDEN_ASK_MP-z-5.md` @fa8d4250bf (read whole).
**Serves:** PRD v0.7 FWD-20, which Andrew made MC Portal's first outcome
(`ANDREW_DIRECT_20261012_205xZ_SITEZ_PORTFOLIO_SEVEN_PROJECT_RULINGS.md` item 2), and direction XB-20261013T185926Z-4d72
Z1, "FIRST on site Z".

## VERDICT: SIGNED, for exactly the ask's section 1 blast radius (items 1-11) and section 2's never-touch list

**Read by this seat, against the ask:**

| read | result |
|---|---|
| `git diff --name-only 185dc04888 233440afaf`, whole repo | **6 paths**, exactly the ask's section 3 list: the five gateway app/tests files plus `EC2_MANIFEST.json` |
| `git merge-base --is-ancestor 185dc04888 233440afaf` | TRUE: the release descends from the live base |
| `EC2_MANIFEST.json` diff | one line, `mcportal_commit` `bc37107` -> `0e02a1f`. No other service entry moves |
| `server.py` import line | the single token `PlainTextResponse` added to the `starlette.responses` import, as section 3a declares |

## Section 3a, the third `server.py` hunk: ACCEPTED

The `PlainTextResponse` import is required by the deep-link handler's own 404 branch; without it every unlisted path
raises `NameError`. It sits inside MP-z-3's graded, drained commit `e42d2c35c3`, and it adds no route and no behaviour
beyond the handler. It is therefore part of "the deep-link handler", not a fourth change. The order's STOP clause is not
triggered.

## Section 6, step 1's "0 failed": option (b), with the 7 failures named as a closed set

- **"0 failed" is graded where the tests' inputs exist:** box/sitez HEAD, already measured at **87 passed / 0 failed**
  for the same payload bytes. Re-read once at the act.
- **On the release tree, the failing set must be EXACTLY the 7** that row NFRA_MCPORTAL-Z-S45 names, and nothing else:
  - **5 fixture-absent failures:** `org/devices/DEVICES.json` and the cp2 capture read `ls-tree` = 0 at the base;
    they sit in four test files this release does not modify.
  - **2 MP-z-1 tests encoding the post-OG-tg-1 world.**
- Any failure outside those 7, or any of the 7 failing for a different reason than its row names, STOPS the act.
- **The two MP-z-1 failures describe the live truth, not a defect.** On the live base, `identity_scope.py` still seeds
  `opalbloomberg@opalinvest.com` as an m365 holder, so the breakdown page will truthfully show that principal holding
  m365 tools. The page reports the deployed world, as FWD-20 requires.
- Those two clear when NFRA_OPLGTW's r30 release (OG-tg-1) ships after this one
  (`NFRA_OPLGTW/ledger/CTO_RULING_R37_ONE_RELEASE_PF1_TG1_BD2_SH1_20261013.md`). Andrew reads the page either way. The
  one-line explanation at his sitting (direction Z7) says the Bloomberg account mirrors him "for now" until r30.

## Both branches

- **Applied (A):** `/health` returns 200 within 90 s, then AC1 and AC2 as the ask's section 5 writes them. The MCP
  tool-name difference before and after is EMPTY, with both counts recorded.
- **Fails mid-act (B), including `/health` not 200 within 90 s:** the ask's section 4 rollback runs AT ONCE.
  - It redeploys from the clean base tree `C:/tmp/mp-z5-rb`, proven 109 of 109 md5-EQUAL with a discriminating
    negative control.
  - The versioned key `opal-gateway-185dc04888.tar.gz` is never written by this act; `opal-gateway-latest.tar.gz` is
    rewritten by the redeploy.
  - The ledger entry closes as rolled back.
  - No IAM, Terraform, ALB, secret or schedule moves in either direction.

## Sequencing

This is the ONE gateway release in flight. NFRA_OPLGTW's r30 release (R1 of round 37) queues behind this act's ledger
close.

-- 1.0.0_SA_CTO~Z
