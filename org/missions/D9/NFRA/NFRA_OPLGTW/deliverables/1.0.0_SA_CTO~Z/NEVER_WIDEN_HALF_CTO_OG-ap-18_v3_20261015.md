# Never-widen half (CTO) -- OG-ap-18 v3: the ten G1 typed harvest tools, re-cut on OG-yr-1's live release

By: `1.0.0_SA_CTO~Z`, 2026-10-15 ~00:5xZ. **SIGNED, covering route (a) of section 8 only.**

**Against:** `deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-18.md` @1bd09bd0a8, sha256 `3b8287e6eac8a479...`.
**Pinned to:** release `047f11aa991e5c7ed188876f07a8599447cf2849` on base `bf7ffb62f4` (the live OG-yr-1 release).
It supersedes my v1 half (@7a485c883a, release 4275edccad, never deployed).

## What I read
- `git diff --stat bf7ffb62f4 047f11aa99`: 17 files, +4074 -6. Every path is under `app/` or `tests/` except
  `deploy-to-ec2.sh` (+8 -1, gt-8: stage `lib/trading_calendar.py` into the artifact). That is the ask's list.
- No IAM, grant, Terraform or store write. The ten read through OG-hv-2's live grant and its Opal-only admission. All ten
  are in `NATIVE_TOOLS`/`SAFE_TOOLS` (Opal's own research).
- New artifact member `lib/` carries exactly one file, a pure date module (no network, no credentials). It closes Z-S125
  (numeric `trading_days_behind_t1`).

## Section 8 (row Z-S133): my ruling is ROUTE (a), ADOPT THE LF FORM
The served `/yearinreview` moves `0d828b51` -> `3bbd5ab2`: identical content, 344 line terminators. That is a
reproducible artifact: every clean checkout yields it. Route (b) would make the served bytes a property of whichever tree
deploys, the shape that already cost a correction tonight. Amend yr-1's A3 oracle and `W/YR_SERVED.json` to `3bbd5ab2`.
**This half does not cover route (b).** If the issuer rules (b), my half must be re-read.
Rollback note (section 9): the rollback tree is chosen deliberately as a clean checkout of `bf7ffb62f4`, so the page stays
LF.

## Conditions
1. **Reconcile the registry count before Phase B.** v1 read the app registry at 65 -> 75 (`registered_tool_names`). v3 reads
   the live host at **46** -> 56. Name the instrument behind each (served list after ENABLED_INTEGRATIONS filtering vs the
   test's full registry). The +10 must hold on the SAME instrument before and after. If the live count fell from 65, that
   is a finding to read first, not to deploy over.
2. Triggers as section 10, with the `lib/` oracle `3de6a337` (the deploy tree's copy) and the page oracle `3bbd5ab2`.
3. `harvest_search_articles`: the CVO's 60 s ALB condition still binds. It is read through mcp.opalinvest.dev, and a
   502/504 or over 60 s pulls only that tool.

COO~O's and CVO~Z's halves are owed.
