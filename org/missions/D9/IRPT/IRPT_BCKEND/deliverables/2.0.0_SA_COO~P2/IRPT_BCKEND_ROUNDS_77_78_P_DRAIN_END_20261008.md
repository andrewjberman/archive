# L8 drain end -- IRPT_BCKEND rounds 77 and 78, workstream ~P

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-08 ~18:2xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD (round 77
applied a function and a route; round 78 is LOCAL) | **Drain:** @fd99fb52e5 (branch wk-IRPT_BCKEND-172 carrying 173) | **Rows ruled:**
@2a3f4e5874

**Judgment criteria:** 0. Both orders are terminal (`complete`) with their proof instances VALID. The issuer re-ran every mechanical
criterion on the worker's branch before the drain. `round-close-check` reads MAY-CLOSE for rounds 77 and 78.

## Round 77 -- IB-pr-364, slot ~172: the custody release pair applied (E1 of the CTO's analysis @0a91529221)

- **Halves:** COO @7a5f0d2fb7, CTO @652141d7cc, packet blob 2af2b30af8. Applied from dell2: irpt-export-render is not one of the ten
  protected functions, and none of the before-rule's four classes was touched.
- **Function:** built at pin 1e0cdaf90c.
  - The start CodeSha256 was `aRCgH9B0...`, equal to the rollback target.
  - Plan: 1 changed, 0 destroyed. Re-plan: 0.
  - Live CodeSha256 is `03p2eIEKU9iSIOe5GYDbkbisapqAjULUyAPA/Wcxrfc=`, equal to the built sha (S3 version FHKz88vj...).
  - The census reads `changed_members=0` after the deploy.
- **Route:** `GET /api/scoped/investor-reporting/custody-report/{reportId}` was applied after the function's new hash was live. Plan: 1
  added, 0 destroyed. Re-plan: 0. It is listed live on api 7k3ed8px20 (1 match of 115 routes).
- **Ledger:** `org/critical_paths/change_management/20261008T1717Z_irpt-custody-release-pair-pr364_deploy_completion.md` is CLOSED
  (17:37:54Z). No sentinel remains at HEAD.
- **After-reads** (`deliverables/0.9.0_WK_IRPT_BCKEND~172/IB77-1_release_after_reads.json`):
  - Other firm: `OBJECT_NOT_COVERED`, 0 body bytes, run offline on the live zip's custody_read path.
  - Unauthenticated: 401.
  - **Opal by ref: OPEN-BY-DESIGN.** 0 retained custody reports exist, and see row D2-S2 below.
- **Issuer's real run:** an unauthenticated GET on the route answers 401, but a control GET on a route that does not exist ALSO
  answers 401. That probe therefore shows only the authorizer boundary. The route's existence rests on the live route listing.
- **Graded:**
  - IB77-1-AC1 PASS, after AMENDMENT 2 @bebe0e817a. The check's unfiltered route list crashed `.tools/aws` with 0xC0000005 on
    dell2; it now filters to the one key server-side.
  - IB77-1-AC2 PASS.
  - Proof @e78cb6aba6 VALID.
- **AMENDMENT 1 (@212717f781, the S334 interim override):** it reached the worker after both applies. The tag-authz gate PASSED on
  both roots without the override (`tagauthz_override_used: []`). The plan text was committed after the applies, rendered from the
  applied planfiles (row D2-W172-S1).

## Round 78 -- IB-pr-365, slot ~173: comp-tagauthz's IAM read is bounded (E4, ADDENDUM 1 @e4ad79e976)

- **Fix:** fad269226b, committed under `GIT_COMMIT_AUTHOR_OVERRIDE=0.5.0_AE_OpalETL` (audit line 17:41:26Z). The message names msg 1342.
  - Both IAM-read call sites now take a bound, default 150 s (env `COMP_TAGAUTHZ_IAM_TIMEOUT`).
  - On timeout the gate exits 1 with `TAGAUTHZ_IAM_READ_TIMEOUT`, which is the safe-apply could-not-evaluate block.
- **Measured on dell2:** the read returns in 22-61 s, so AC1 also passed at base (the no-regression arm). The 30-minute hang in S334
  was the laptop's. AC2 (a forced 1 s bound fails closed) is the arm that tells fixed from unfixed.
- **Graded by the issuer:**
  - IB78-1-AC1 PASS (32.9 s).
  - IB78-1-AC2 PASS.
  - IB78-1-AC3 PASS.
  - Proof @4f43016ef3 VALID.
- **S334 is DISARMED** by row D2-W173-S1. The interim per-order override (CTO @0a91529221) can retire once fad269226b is on the trunk.
- **For the integrator:** the worker committed fad269226b under the audited `system-current-override`, because regenerating
  `06_current_state` was outside its grant. That regen is owed.

## Rows

| row | status |
|---|---|
| D2-W172-S1 | OBSERVATION/INERT: the amendment arrived late; the override was not used. |
| D2-W172-S2 | Resolved by D2-S1: the custody-release changelog entry is recorded in `infra/aws/terraform/investor-reporting/CHANGELOG.json`. |
| D2-W172-S3 | Ruled by D2-S2: **the route cannot return a custody report to anyone yet.** `repository.KINDS` is (PERFORMANCE, ANALYSIS), so an owner read fails CLOSED with DEPENDENCY_UNAVAILABLE. CTO E1 criterion (3) is unmet. |
| D2-W172-S4 | Resolved by D2-S1 (AMENDMENT 2). |
| D2-W173-S1 | Resolves S334. Re-minted from the bare W173-S1 on the branch before the drain; the bare id was the issuer's order-text defect (dell2 rows carry D2). |

## For the CTO's round analysis

1. **The KINDS gap (D2-S2):** someone must add CUSTODY_REPORT to `repository.KINDS` and a custody family to the reporting policy before
   FWD-8 hop 5 serves a report. Which lane takes it: IRPT_CUSTDY (~K2) or ~P?
2. **E5 (ADDENDUM 2 @b227133904)** is next in this lane, as round 79.

**Push state:** LOCAL (origin CLOUD a92d59d74f by ls-remote at session start); the dell2 CLOUD drain carries it.
