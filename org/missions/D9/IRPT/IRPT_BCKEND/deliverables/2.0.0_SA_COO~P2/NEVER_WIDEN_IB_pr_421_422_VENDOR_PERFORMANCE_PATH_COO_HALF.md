# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-421 + IB-pr-422: the vendor performance path without the one-use plan (one release: one zip, two IAM policies)

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-11 ~09:0xZ | **Signed against:**
- packet `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~282/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-421.md`, **blob e6ac0b9548**;
- packet `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~283/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-422.md`, **blob 853883965b**.

**Ordered by:** `1.0.0_SA_CTO~DELL2` msgs 4416, 4488, 4509, on Andrew-direct 2026-10-09
`org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20261009_024xZ_LAW_EDIT_CLAUDE_MD_EGRESS_OPEN_EXCEPT_BBG.md`. A rebuild that
changes the zip digest, or a plan that changes either grant, re-opens this half.

## What this release does, said plainly

It WIDENS served output and it WIDENS one role. Today every fresh vendor-path performance request is refused at
`performance/authorization.py:90` (4 of 4 requests of the 2026-10-11 07:30Z product walk). After this release a signed-in Cottonwood
or Inflection user's fresh performance request calls Black Diamond or Orion with the firm's stored session credential. Who may ask is
unchanged: nothing under `_authz/`, `_scope/`, `served.py` or `entry.py` moves. 49 Financial never reaches this path.

## Blast radius signed

| step | the act may touch | the only thing that may land | rollback |
|---|---|---|---|
| 1 | role `irpt-performance-adapter-role`: two inline policies ADDED | `irpt-performance-approved-session-policy`: `secretsmanager:GetSecretValue` on `arn:aws:secretsmanager:us-east-1:313476888478:secret:blackdiamond/cot/session-jnzOyC`; `irpt-performance-approved-orion-session-policy`: the same action on `arn:aws:secretsmanager:us-east-1:313476888478:secret:orion/jwt/current-ewrBtp` | targeted destroy of the two policies (CTO pre-authorised for the case where step 1 landed and step 2 cannot); the role returns to the 7 policies listed below |
| 2 | function `irpt-performance-adapter`: its code package | CodeSha256 `OF+8j4ucXsxwJ195NKEQZnma22T8bYVUriw9YP859RU=` | redeploy S3 version `7IkeCAOa8F8IzqgaW1_WCLczFhmtzaLn` (digest `9kYLdR64P0p2TEbDXcQu1hrpQ9KtqjPNnFDpoE/W31A=`), re-read as present first |

No route, schedule, layer, environment or table change; no other function; no other role. After the release each fresh vendor use
also writes ONE use record to the requests table (an unconditional put, a log), under a permission the role already holds.

**Writers.** The function's code: N = 1 (its Terraform module). The role's inline policies: N = 1 (the same root,
`infra/aws/terraform/investor-reporting/performance/`). 2 rules read.

## Read by this seat at signing (dell2, 2026-10-11 ~09:0xZ), each by its own read

| Check | Read | Packets say | Equal |
|---|---|---|---|
| IB119-1-AC1..AC3 and proof at box/dell2 (drain @416ead492f) | PASS, PASS, PASS, VALID | PASS, VALID | yes |
| IB120-1-AC1..AC3 and proof at box/dell2 (drain @311ed8c55c) | PASS, PASS, PASS, VALID | PASS, VALID | yes |
| live adapter CodeSha256 | `9kYLdR64...W31A=` | the same | yes |
| latest S3 version of the adapter zip and its `content-sha256` | `7IkeCAOa8F8IzqgaW1_WCLczFhmtzaLn`, equal to the live digest | the same | yes |
| role's inline policies now (`list-role-policies`) | 7: directory-read, logs, ownership-map-read, selection-read, service-profile-read, render-grant-read, retained; none reads a secret | the same 7 | yes |
| the two secret ARNs (`describe-secret`; no value read) | both exist, ARNs as in the table | the same | yes, 2 of 2 |
| `retained.tf:177-214` before the edit | both session policies and both data sources count-gated on the plan variable | the same | yes |
| `lambda.tf:62-65` | the module `depends_on` `performance_approved_session` | the same (cause of the untargeted plan's 1 change) | yes |
| whole `performance/tests` at box/dell2 | 1 failed, 268 passed | the same | yes |

NOT read by this seat, taken as filed: the built zip's bytes (worker scratch `C:/dev/_scratch282/`; the apply's BUILD_ONLY digest
compare is the control); the 17 replay arms; the targeted plan itself (2 add, 0 change, 0 destroy, run twice by the worker; the apply
re-plans it and STOPS on any other count); the naming limb's run (rc 0, both names CONFORMANT).

## Both branches, in the CTO's two steps, one sitting, one ledger entry

0. **Source map first.** The adapter's entry in `infra/aws/lambda/ci/lambda-source-map.json` is re-pinned to the candidate entry of
   `deliverables/0.9.0_WK_IRPT_BCKEND~282/` (every investor-reporting member at `cd833e66cb`), one commit touching only that file,
   before any build. The other entries are not touched.
1. **Policies.** Targeted plan at the two addresses: exactly 2 adds, 0 changes, 0 destroys, or STOP. Apply through `safe-apply`.
   After-read: `get-role-policy` on each, printing its ONE secret ARN and single action.
   - With the policies landed and the old zip still live, the grant is unused: the old code refuses at its plan check before any
     secret read. So a stop between the steps is a safe state.
2. **Zip.** `BUILD_ONLY=1` prints `OF+8j4uc...` or ABORT. Upload, then the full-root plan with a KNOWN hash: exactly 1 change, the
   function, or STOP. Apply through `safe-apply`. After-read: live CodeSha256 equals the built digest.
3. **Live-call arm within a minute of the promote:** one GET of the performance route as a non-49F caller answers typed, no 500, and
   0 `TypeError` and 0 `AccessDenied` lines in the log group from the promote on. A 500, a `TypeError` or an `AccessDenied` is Branch B
   for step 2 at once.
- **Branch B.** Step 2: redeploy `7IkeCAOa...` (`9kYLdR64`). Step 1, only if step 2 cannot land or is rolled back: the targeted
  destroy of the two policies. The source-map entry is re-pinned back in the same sitting if step 2 is rolled back.

## What the pair does NOT establish -- stated so the close cannot overclaim

- **No vendor call has been made on these bytes.** The cell made none and read no credential. The live-call arm above proves the
  function answers; it does not prove a vendor figure is served. The first real evidence is the laptop's re-walk of DSGN_IRPTV1 FWD-1,
  and until then the outcome is ABSENT, not exercised.
- **The session secrets may be stale.** A cookie or token that the vendor rejects yields a typed refusal after a use record is written.
  That is a correct refusal and not a rollback case; it is a row and a credential question for its owner.
- **A repeat is refused today (row D2-W282-S2).** `retained.py` refuses to reopen a vendor-calculated report, so a firm's first fresh
  request is served and an identical repeat reads `RetainedVendorFigureRefused`. Unchanged by this release; it will show in the re-walk
  if the walk repeats a request.
- **One test of the suite fails** (`test_holdings_gold_calendar_gap.py::test_the_fallback_calendar_is_graded_in_its_own_years_and_clipped_outside_them`,
  row D2-W282-S3). It imports none of the five changed modules. It was NOT run on the pre-change tree, so "pre-existing" is inferred.
- **Left for a later cleanup:** `var.approved_performance_plan`, `local.performance_plan_firm` and the two plan environment variables
  are no longer read by the code and are not removed here.

## SIGNED, with conditions

GIVEN for zip `OF+8j4ucXsxwJ195NKEQZnma22T8bYVUriw9YP859RU=` and the two single-secret grants above, on these conditions: (1) one
sitting, one ledger entry opened and committed before any write, naming the function, the role and both policies; (2) policies before
zip, each step's count exact or STOP; (3) the live-call arm as stated, with `AccessDenied` added to its failure set; (4) the close
states the vendor path as APPLIED, UNEXERCISED until the re-walk reads a figure; (5) the apply comes by a new order of this seat.

`2.0.0_SA_COO~P2`
