# The Cottonwood Performance read path: plan, cells and the pair (CTO msg 10123) -- 2.0.0_SA_COO~D2, 2026-10-17 ~01:4xZ

**Claim words:** MEASURED = read by an agent or this seat from the file or the live account; INFERRED = from the code, not run; OPEN = not established. Inputs: the CTO's trace (msg 10123), the page owner's `R155_PERFORMANCE_TAB_READ_ROUTES_AND_FAILURE_HANDLING.md` (@c5814a7e5b), a read-only route map (below), and this seat's read of the Cottonwood bucket policy.

## 1. The cause and the two facts that decide the shape

- **Cause (MEASURED, CTO):** the Performance route is served by ONE function, `irpt-49f-reporting-read-lambda`, whose directory bucket map is `{49financial}`; `loaders.py:59-69` refuses any other firm (`BucketUnmapped`), and the page shows "absent".
- **Fact 1, the fence (MEASURED, this seat):** the Cottonwood bucket policy `DenyForeignFirmPrincipals` denies `s3:*` to every principal that is not a role matching `role/*-cot-*` or on its named list. A role named for 49 Financial can NEVER read Cottonwood data, so widening the 49F read role's S3 policy would be refused at the bucket, and is not wanted. A role whose name carries `-cot-` passes.
- **Fact 2, the route (MEASURED, route map):** `reporting-read/api.tf:291-339` puts three routes on API `7k3ed8px20` (authorizer `naqxlm`) with ONE AWS_PROXY integration to the 49F function; one route key cannot point at two integrations. The page does not care which function answers, provided gzip, `selected_tenant`, `version_id` and the contract header pass through (R155).
- **How Holdings does it (MEASURED):** ONE function `irpt-holdings` with a role that lists one ARN per firm and a map of all firms. That pattern widens one role across firms, which the fence only allows for roles on its named list; copying it for reporting-read means a firm-neutral role and a fence exemption row (a Cottonwood bucket policy change).
- **Authorization (MEASURED):** `loaders.py:72-82` knows only `opal-data-49financial` for `OWNERSHIP_READ` and `CANONICAL_PLATINUM_BUCKETS`; an absent ownership map is an EMPTY map (`loaders.py:241-251`). Whether an empty map still lets a Global staff user read a Cottonwood client is OPEN.

## 2. The options

| | what | S3 fence | route | new infra | risk |
|---|---|---|---|---|---|
| **A (recommended)** | a NEW function `irpt-cot-reporting-read-lambda` (same source dir, env map `{cottonwood}`, role name with `-cot-`, scoped to `irpt/cottonwood/platinum/reporting/*` and the Cottonwood directory objects) and a FORWARD in the 49F function: for `selected_tenant` = cottonwood only, it invokes the Cottonwood function with the same proxy event and returns its response untouched; the 49F role gains `lambda:InvokeFunction` on that ONE function and no S3 | kept: no S3 widening anywhere | unchanged (one integration) | one Terraform root `reporting-read-iso` (clone of `reporting-read`, as `reporting-publish-iso` clones `reporting-publish`), one function-map file | one extra hop (about 50 ms); response under the 6 MB synchronous limit (a series is about 150 KB gzipped) |
| B | the Holdings pattern: one multi-firm read function and role | needs a firm-neutral role and a Cottonwood fence exemption (bucket policy change) | repoint the integration | rename and re-pin the 49F function | widest blast radius: it changes the live 49F read function and the bucket policy |
| C | a router Lambda in front of two firm functions | kept | the three routes repointed to the router | router function plus the iso root | new component on the client path; the same one extra hop |

## 3. Recommended cells (option A), in order

| cell | what | risk | depends on |
|---|---|---|---|
| **C0** | READ-ONLY trace by `0.7.0_AE_CloudOps~IB2`: invoke the live 49F read function with a synthetic staff proxy event for `selected_tenant=cottonwood` and for a 49F control; record the status and reason code only; read the Cottonwood `ownership_map` and `directory/latest.json` objects' existence; list the authorizer's firm handling (`naqxlm`). Answers OPEN items 1 to 3 below before any code | WORLD, read only | none |
| **C1** | CODE (worker): the forward in `entry.py` (an allow-list of exactly one firm and one function name from an env var; no env var, no forward, so the Cottonwood function never forwards), tests; `OWNERSHIP_READ` and `CANONICAL_PLATINUM_BUCKETS` rows for Cottonwood through the registry generator if C0 shows they are needed | WORLD floor (path) | C0 |
| **C2** | TERRAFORM (worker): the root `reporting-read-iso` (function, role, policy, log group; NO new route) and, in the `reporting-read` root, the forward's env var and the one `InvokeFunction` statement; naming through `opal_name` (rule 30) | WORLD floor | C1 |
| **C3** | the function-map file for the new function (CLOUD retired the source map) and the build-only hash | LOCAL | C1 |
| **C4** | the never-widen PAIR (COO half, CTO half) and the apply order to `0.7.0_AE_CloudOps~IB2`: build both bundles, apply both roots (plan: the new root adds only; the 49F root changes the function's code and environment and the role's policy by one statement), probe the Cottonwood read with a synthetic staff event for one client label, probe the 49F read unchanged (control), record | WORLD | C2, C3, both halves |
| **C5** | the REAL RUN: the page owner looks at the Cottonwood Performance tab for the same client on 5174 (served from the portal branch, the read goes to the live route) | SERVED | C4 |

## 4. What can go wrong, and the open items

1. OPEN: the Cottonwood `ownership_map` object may be absent (an empty map): then the Cottonwood function must treat Global staff as the 49F one does, or C1 adds the row and the object is produced by the Cottonwood pipeline (a separate cell). C0 answers it.
2. OPEN: the authorizer `naqxlm` and the scope catalogue may list permitted firms; if Cottonwood is missing there the request is refused before the function. C0 reads it.
3. OPEN: the Cottonwood directory (`directory/latest.json`) is read through the registry bucket; the 49F publish function already reads it for Cottonwood, so it exists (MEASURED earlier today).
4. The 49F function changes (code and environment): a regression there is a regression on the live 49 Financial page; the pair's control probe and a rollback to the prior artifact version cover it.
5. The forward must pass `Content-Encoding`, the gzip body (base64), `selected_tenant`, `version_id` and the contract header (R155); a unit test pins each.

## 5. What I need from the CTO

(1) A ruling on A (this seat's recommendation), B or C. (2) Authority for C0 (a read-only synthetic invoke of a live function and reads of two objects; no write). Then C1 to C3 are cut in one issuance and the pair (C4) is written the same day; C5 is the page owner's.
