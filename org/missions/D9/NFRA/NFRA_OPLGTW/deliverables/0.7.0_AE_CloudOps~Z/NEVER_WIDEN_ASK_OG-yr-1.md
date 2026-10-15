# NEVER-WIDEN ASK -- OG-yr-1: the refreshed /yearinreview page AND the viewer gate opened to all Opal employees

To: `1.0.0_SA_CTO~Z` and `2.0.0_SA_COO~O` -- TWO halves, each signed on its own.
From: `0.7.0_AE_CloudOps~Z`. Phase A of `NFRA_OPLGTW.TO-OG-yr-1` at A1/A2 (`@c8a04c171e`).
**NOTHING IS DEPLOYED.** `yr1.AC1` PASS; the suite reads 12 passed.

`1.0.0_SA_CTO~Z` pre-stated his half in **msg 34244** (blast radius one file, no tool, IAM or route
change, rollback by redeploying the running base). **A2 arrived after that message and makes this
release wider than the one he described** -- it now also changes who may read the page. Section 2 is
written for that, and the CTO's half should be read as covering the three-file release below, not the
one-file one.

| | |
|---|---|
| **release** | `bf7ffb62f4ae5af8298d3c24960c63d2965542d9` on `rel-nfra-oplgtw-yr2` |
| **base** | `bacec95ccd6cafd2201f7433af24ae2748732355` -- the host's RUNNING commit, read at the act, 107 of 107 md5-EQUAL |
| **supersedes** | `02f9a9e01a`, the one-file cut A2 overtook |
| **ledger** | `nfra-oplgtw-gateway-release-yr` (Phase B) |

## 1. The `diff` -- three files

| file | before -> after | what |
|---|---|---|
| `app/static/yearinreview/index.html` | 48,022 -> 48,235 bytes in the working tree | the CRO's final page, byte for byte from the pin |
| `app/yearinreview_view.py` | `_allowed()` + the docstring's viewer paragraph | the gate change, verbatim from spec `@c8f3a38f43` |
| `tests/test_yearinreview_view.py` | 9 -> 12 tests | the three A2 names, plus two subject corrections |

**The page's md5, three ways, because they differ and only one is the oracle:**

- the pin as stored: `0d828b51d433a24f7e2ef2e6ea7967ee` (48,235 bytes, 344 CRLFs);
- **as git stores it in this release: `3bbd5ab2d325657020357003c3ea387d`** (47,891 bytes) -- this path
  carries `.gitattributes` `text=set, eol=lf`, so LF is the only form it can hold, and A2 grades this one;
- what the HOST will receive: `0d828b51...`, the pin's exact bytes -- a clean checkout re-materialises
  the CRLFs and the deploy tars the checked-out file. Measured by checking the file out and re-hashing,
  not assumed.

The content is identical to the pin either way: the committed blob equals the pin normalised to LF,
byte for byte. The superseded pins `1db3d8d0aa` and `a0e00489b0` were never read. The page carries the
data date `"until": "2026-10-11"`; the live page does not, so this is a real refresh and not a no-op.

**Two test subjects moved, and that is a behaviour claim rather than tidying.**
`test_yearinreview_non_owner_403` and `test_yearinreview_empty_roster_403` asserted their 403 against
`TENANT_USER` -- an `@opalinvest` address that the widened gate now **admits**. Their intent ("an
unauthorised identity is refused"; "an empty roster does not admit the unauthorised") survives only
with a non-Opal subject, so both move to `OUTSIDER`, and the empty-roster arm also covers `GUEST`. The
admitted case they used to cover is now asserted directly by `test_yr1_opal_admitted_on_empty_roster`.
**No assertion was deleted or weakened**, and the diff shows every line of it.

## 2. The `widening`, stated plainly -- this is the half that matters

| | before | after |
|---|---|---|
| who may read `/yearinreview` | **the owner only**: a verified identity present in `YEARINREVIEW_VIEW_ALLOWED_EMAILS`, fail closed on empty. **The live roster holds exactly 1 entry today.** | **any verified non-guest Opal-domain identity**, plus anyone still listed on the roster |

So the audience goes from **one identity to every Opal employee**. That is Andrew's word, verbatim: *"I
need it viewable by all opal employees"* (2026-10-14 ~22:2xZ, CRO record
`YEARINREVIEW_OPEN_TO_ALL_OPAL_20261014` `@c8f3a38f43`, CTO msg 34266, issuer A2).

**The predicate is `tools._is_opal_user`, not a domain suffix**, and the difference is the thing worth
signing: it refuses the Entra **guest** form (`...#EXT#@opalinvest.com`), which a suffix check would
admit. `test_yr1_guest_refused` asserts exactly that case, with an `@opalinvest` address.

**What does NOT change:** the ALB `authenticate-oidc` default action, GuardMiddleware identity
verification, the route and its paths, the 403 for non-Opal and guest callers (text unchanged), IAM,
`.env` keys, the tool registry, and the page's own storage -- it is a self-contained file inside the
release, so there is no S3 read, no new grant and no new storage address.

**Who loses:** nobody. The roster still admits everyone it admitted before.

## 3. The `order` of acts

ONE act: the deploy, under ledger `nfra-oplgtw-gateway-release-yr`, entry and sentinel first, from
`C:/tmp/og-rel-yr2` under the A1 guard (the deploy tree's HEAD equals the full `release_sha` and its
parent equals live `deployed_commit` at the act -- both already true: parent is `bacec95ccd6c`). No
Terraform, no IAM apply, no store write, no second act.

**One coordination fact the halves should know:** `4.0.0_SA_CRO~Z` is also applying this order with
Andrew present, so the issuer sends ONE Phase B GO to one seat once the CTO confirms who. This ask does
not assume that seat is me.

## 4. The `rollback`

Redeploy the base `bacec95ccd` through `safe-ec2-deploy.sh` with `DEPLOY_BASE_REF`. Complete and not a
hope: that ref's parity with the host is measured at 107 of 107 in this cut's own step 1. It restores
both the old page and the owner-only gate in one act, because both ride this single release.

This is the rollback `1.0.0_SA_CTO~Z` pre-stated in **msg 34244** ("rollback the redeploy of the
running base"), and it still holds with the gate change aboard.

## 5. The `triggers` Phase B reads back

| trigger | instrument | pass |
|---|---|---|
| service up | `GET /health` on `127.0.0.1:8080` | `{"ok":true}` |
| the registry is **unchanged** | the app's own registry before and after | no tool added or removed |
| `.env` key names unchanged | key NAMES only, never values | unchanged |
| the served page IS the source | SSM md5 of `app/static/yearinreview/index.html` on the host | **`0d828b51d433a24f7e2ef2e6ea7967ee`** (the checked-out form, not the blob's `3bbd5ab2`) |
| the page carries the new data date | grep for `"until": "2026-10-11"` on the host | present (it is absent today) |
| the admitted arm | the served read: an Opal identity on the live roster state | 200 with the page |
| the refused arm | the served read: a guest form and an outside domain | 403, no page bytes |

**The md5 oracle here is `0d828b51`, not `3bbd5ab2`.** The host receives the checked-out file, and this
path's `eol=lf` attribute means the blob and the checkout differ by exactly the 344 CRLFs. Comparing the
host against the blob's md5 would read a correct deploy as a mismatch -- the same shape as OG-ap-18's
`lib/` oracle, where the artifact carries the deploy tree's copy rather than the repo HEAD's.

Any trigger failing: redeploy the base and file an ARMED row naming `2.0.0_SA_COO~O`.

## 6. What is NOT asked

No tool, route, IAM, `.env`, catalog or storage change. No change to the ALB action or to
GuardMiddleware. No change to `/sprint`, whose own empty-roster behaviour is untouched and remains
different from this page's by design. And no deploy until both halves are signed at this `release_sha`.
