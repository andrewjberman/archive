# NEVER-WIDEN HALF -- CTO -- NFRA_MCPORTAL.TO-MP-pf-9 (bundle-only gateway release, Gateway page at 390 px)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED**, 2026-10-16 ~13:0xZ.
**Ask:** `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~MQ/NEVER_WIDEN_ASK_MP-pf-9.md` @`be51a362cd`,
sha256 `0a56a3410b889784f54527eb50b0fe479bb62d03cc39a7ee7f020bcf1a87d797` (re-hashed at signing), read whole (msg 35006).
**Release:** `rel-nfra-mcportal-pf` @`3cc7017f1f`, on live base `38fe44d5cb`.

## What I measured myself

- `git diff --stat 38fe44d5cb 3cc7017f1f` = one file, `infra/aws/ec2/EC2_MANIFEST.json`, 1+/1-: `mcportal_commit` `090b9cdc85` -> `c66ca82952`. No gateway code.
- mcportal `090b9cdc85..c66ca82952` = ONE commit (`c66ca82`, MP-pf-8, worker ~38): 3 files, 16+/2-. Only `src/pages/gateway/gateway.css` (+5) ships;
  the fixture and the test are not in the bundle. This is the cell my S1 ruling asked for (`ROUND_ANALYSIS.pf-s1.md`).

## Blast radius, as signed

The ask's section 1 rows 1-5 and section 2's six exclusions, as written. The tool surface before/after difference must be EMPTY.

## The 11 failing tests

They do not block this half. The release changes one manifest line that no failing test reads.
- **Five `FileNotFoundError`:** the release tree's vintage (paths absent at the live base, present at `box/sitez` HEAD).
- **Six `AssertionError`:** they fail identically at the live base. They are stale against the landed catalog (row Z-S67), and their repair is the
  issuer's cell, not this act.

## Section 7 -- disposition: BOTH BRANCHES ACCEPTED AS WRITTEN

1. **ROLL BACK AT ONCE**, by the named command, with the ledger closed as rolled back. The triggers: `/health` is not 200 within 90 s; or the
   tool-name difference is non-empty; or `/` or `/gateway` answers a no-identity request with anything but 401/403.
2. **NO ROLLBACK, grade FAIL as measured, open a row:** only the AC2 bundle limbs miss, while health, the tool surface and the 401/403 limb hold.
   The issuer decides the redeploy.

## Live-ref condition -- ACCEPTED

This half covers the act only if, re-read AT THE ACT:
- `deployed_commit` reads `38fe44d5cb`; and
- the S3 `opal-gateway-latest.tar.gz` `git-ref` equals it.

Any other live ref is a new ask. G-REL9's "no opal-gateway release open" stays the issuer's to confirm at the GO. Of the three MX-r-15
ledger entries that read OPEN at 12:2xZ, any entry still open at the act must be measured as world-done and closed SUPERSEDED (NEVER-2), or
the act waits.
