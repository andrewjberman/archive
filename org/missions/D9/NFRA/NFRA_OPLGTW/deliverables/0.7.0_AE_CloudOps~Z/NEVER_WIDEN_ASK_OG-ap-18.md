# NEVER-WIDEN ASK -- OG-ap-18: the ten G1 typed harvest tools (v3, re-cut on OG-yr-1's live release)

To: `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O` and `3.0.0_SA_CVO~Z` -- THREE halves, each signed on its own.
From: `0.7.0_AE_CloudOps~Z`. Phase A of `NFRA_OPLGTW.TO-OG-ap-18` at A6/A7 (issuer msg 34290).
**NOTHING IS DEPLOYED.** 48 of 48 tests pass; there are no failures to name this time.

| | |
|---|---|
| **release** | `047f11aa991e5c7ed188876f07a8599447cf2849` on `rel-nfra-oplgtw-gt3` |
| **base** | `bf7ffb62f4ae5af8298d3c24960c63d2965542d9` -- OG-yr-1's release, read live THREE ways at the cut |
| **supersedes** | `7521aee725` (v2, never signed) and `4275edccad` (v1, could not have started on the host) |
| **ledger** | `nfra-oplgtw-gateway-release-gt` (Phase B; never opened for v1 or v2) |

**Why there is a v3, and why your v2 reading does not carry.** A6(3) held v2 back: `OG-yr-1` deployed
first on Andrew's "live now", which moved the live ref from `bacec95ccd` to `bf7ffb62f4`. The three
halves sign THIS `release_sha`. The cut itself is otherwise the v2 cut you have already read, minus one
file (A6(1)), and **every one of the 17 taken files is byte-identical to its v2 blob** -- verified md5
by md5, not assumed. So if you read v2, the delta you are being asked to re-read is: a new base, one
dropped test file, and section 8 below, which is new and is the part that matters.

## 1. The `diff`, by file -- 17 files, and `lib/` becomes a NEW artifact member

| file | +/- | taken |
|---|---|---|
| `app/harvest_identity.py` | +532 | whole, gt-8 `43e5e0383e` -- **the safe calendar root** |
| `app/harvest_press.py` | +504 | whole, gt-9 `73804a2c4a` -- the pruned search window |
| `app/harvest_figures.py` | +561 | whole |
| `app/harvest_research.py` | +540 | whole |
| `app/harvest_typed.py` | +222 | whole -- the shared admission, cap and envelope |
| `tests/test_og_gt0..gt4.py` | +1405 | whole, five files |
| `tests/test_og_gt9.py` | +214 | whole, gt-9 |
| `app/tools.py` | +63 | by hunk -- the ten registrations |
| `app/destructive_ops.py` | +10 | by hunk -- the ten into `SAFE_TOOLS` |
| `app/data_entitlement.py` | +10 | by hunk -- the ten into `NATIVE_TOOLS` |
| `tests/test_entitlement_admin.py` | +2 -2 | by hunk -- `registered_tool_names` 65 -> 75 |
| `tests/test_data_entitlement_family.py` | +3 -3 | by hunk -- `non_data` 56 -> 66 |
| **`deploy-to-ec2.sh`** | **+8 -1** | **by hunk, gt-8 -- the artifact gains `lib/`** |

**DROPPED from v2 (A6(1)): `tests/test_og_gt8.py`.** Two of its three tests assert on `app/news_typed.py`,
which rides `OG-ap-19`, so the suite could not go green in this release by construction. It is absent from
this tree, and the control is that the same path DOES resolve at v2 -- so its absence is the drop and not
a bad read.

**`lib/` IS A NEW ARTIFACT MEMBER, and that is the one change here that is not application code.**
gt-8's deploy hunk refuses the upload outright when `lib/trading_calendar.py` is missing from the repo,
stages that one file into the bundle, and adds `lib` to the tar. So `/opt/opal-gateway/lib/` appears on
the host for the first time, carrying exactly one file. Nothing else enters the artifact.

**How this cut was built, in a way you can check rather than trust.** `OG-yr-1`'s three files and v2's
eighteen are **DISJOINT** -- the intersection of the two path sets is measured at 0 -- so v2's content
applies to the new base unchanged. The 17 files were taken as v2's own content and then each compared
against its v2 blob: **17 of 17 byte-identical, 0 differing, 0 missing.** `OG-yr-1`'s three files remain
at the base's content, each equal to the HEAD blob, so this cut moves nothing of that release.

`app/tools.py` carries 7 non-ASCII characters. They are **PRE-EXISTING**: 7 at the base, 7 at the
release, and **0 in the lines this cut adds** -- the same lines, shifted by this cut's own insertion.

## 2. The ten `tools`, their class, and what they answer `refused`

All ten are READ tools, `SAFE` in `destructive_ops`, `legacy` class in `data_entitlement`
(`NATIVE_TOOLS`, deliberately NOT `DATA_GRANT_TOOLS`): `harvest_resolve_security`,
`harvest_security_coverage`, `harvest_get_chatter`, `harvest_search_articles`, `harvest_get_article`,
`harvest_get_fundamentals`, `harvest_query_columns`, `harvest_get_research`,
`harvest_get_filing_analysis`, `harvest_get_peers_and_scores`.

Each calls `harvest_typed.admit_typed` **before any S3 call** -- OG-hv-1's admission: a principal, then
`tools._is_opal_user`, then the served-prefix test. So each inherits `principal_required`,
`harvest_opal_only` and `harvest_prefix_not_served`, and adds `harvest_bad_argument`,
`harvest_over_cap`, `harvest_read_failed` and `harvest_unreadable`. A non-Opal caller is refused all ten.

## 3. The `widening`, stated plainly

**No new bucket reach. No IAM change. No grant.** These read `s3://opal-data-harvest` through the same
policy and the same Opal-only admission OG-hv-2 already put live, under the same 24 served prefixes.
`gateway-global-internal-reader-role` gains nothing and `harvest_read_iam.tf` is untouched.

What widens is **ease**: ten typed, projected readers over what `harvest_read` could already fetch one
object at a time -- research notes, filing analyses, press and social chatter, peer sets and scores, and
Bloomberg bronze tables **read from the bucket**. There is no vendor call in any of these modules, so no
Bloomberg entitlement is touched and nothing goes through their queue.

The second widening, smaller and worth naming: the host gains `lib/trading_calendar.py`. It is a pure
date-arithmetic module with no network and no credentials, and it is what lets these tools state a
trading-day lag instead of an absent reason.

The third is in section 8, and it is a widening of a different kind: a page this release does not take
would nonetheless change on the host.

## 4. The `order` of acts, and that no grant is part of it

ONE act: the deploy, under ledger `nfra-oplgtw-gateway-release-gt`, entry and sentinel first. No
Terraform, no IAM apply, no store write. Phase B: ledger, deploy from `C:/tmp/og-rel-gt3` under the A1
guard (deploy tree HEAD == the full `release_sha`, its parent == live `deployed_commit`), read back the
triggers, then the served read of all ten.

**The release worktree's cone now carries `infra/logic`** (row `Z-S132`, ruled by the issuer in msg
34290), because `deploy-to-ec2.sh` resolves two `.env` S3 roots through `lib/opal_naming.py address()`
and that refused the yr-1 deploy outright on its first attempt. Proved at CUT time rather than at deploy
time -- see section 7.

## 5. `Both branches` of a call

| branch | what happens | evidence |
|---|---|---|
| **refused** | the admission answers before any S3 call, so **zero S3 calls** | `admit_typed` runs first in every tool; OG-hv-2's served read measured `s3_calls_on_refusal 0` for the same admission with a counter in place of the client |
| **admitted** | the read is **capped at 64 MB on the body itself** (so a lying `Content-Length` cannot defeat it; over it -> `harvest_over_cap`) and the output **projected to 50 KB**, carrying `truncated` and `projected_to_bytes` | `app/harvest_typed.py:24-28, 54, 147-153` |

Every answer carries `as_of`, `source_keys`, `denominator`, `absent_reason`, so an empty answer says why.

## 6. The host-shaped import check -- re-run at the new base, and twice it was MY instrument that was wrong

A4 made this a Phase A trigger because v1's evidence ("imports cleanly in the release tree") is a
property of a module **at a depth**: the checkout is 8 parents deep, the host is 4, and `parents[5]` is
correct in the first and fatal in the second.

Run here: the release tree's `app/` copied to `C:/tmp/g3/app` with `lib/trading_calendar.py` beside it,
then all five G1 modules **and `app.tools`** imported in a FRESH interpreter whose `sys.path` is that
root alone.

- **Depth proof:** `C:/tmp/g3/app/harvest_identity.py` has **exactly 4 parents**, the same as
  `/opt/opal-gateway/app/harvest_identity.py`.
- **Result: 6 of 6 OK**, each resolving at 4-parent depth.
- At that depth gt-8's `_calendar()` **resolves** (`calendar_source` reads
  `NYSE/hardcoded-fallback-2024-2027`), T-1 is `2026-10-14`, and the module's own `_behind()` yields
  **3, 1 and 0** trading days behind T-1 for `2026-10-09`, `2026-10-13` and `2026-10-14` stamps -- a
  number, not the absent reason. That is what Phase B must see, measured before the deploy at the host's
  own depth.

**Two readings in this check were my instrument and not the code, and both are kept in the record
because each looked exactly like a defect.** The first run used `python -I` and read **5 of 6**:
`app.tools` failed `ModuleNotFoundError: No module named 'anyio'`, because `-I` ignores the user
site-packages that carries it. That is a DEPENDENCY absence, not a depth failure, and the host runs
under its own venv with every dependency. The second run then read `trading_days_behind_t1 = null` with
*"the trading calendar cannot place ... (ValueError)"* for every probe, which looked like a regression
against v2's measured `2`. It was my stamp SHAPE: `_behind` parses `%Y-%m-%dT%H:%M:%SZ` -- a **literal
`Z`**, which is what S3 `LastModified` renders -- and I had passed `+00:00`. The wrong-shape probe is
**kept as a control** that comes back ABSENT, so the record can tell a wrong instrument from a real
defect. And v2's `2` against today's `3` for the same `2026-10-09` stamp is one trading day of clock
movement: T-1 was `2026-10-13` then and reads `2026-10-14` now.

## 7. The `tests`, and the no-upload dry read of the naming step

**48 passed, 0 failed, 0 errors** over nine suites: `gt0` 5, `gt1` 4, `gt2` 5, `gt3` 5, `gt4` 7, `gt9` 4,
`hv1` 5, `entitlement_admin` 9, `data_entitlement_family` 4. The counts **reconcile** against v2 rather
than merely looking clean: v2 read 49 passed / 2 failed over ten suites, and dropping
`tests/test_og_gt8.py` removes its 1 passed and both of its failures, which is exactly 48 / 0.
`tests/test_yearinreview_view.py` was also run at this base -- 12 passed -- so the cut does not disturb
the release it sits on.

**The naming step, proved at CUT time with no upload** (`W/gt3_naming_dryread.sh`, `RESULT: PASS`). It
runs the deploy script's OWN bytes for that step -- lines 94-107, located by anchor rather than a pinned
number, span sha256 `96537219...` -- so it exercises the two `address()` substitutions AND the two `case`
shape guards that a hand-written python call never reaches. Three arms:

- **POSITIVE** -- both roots resolve through the builder and both shape guards pass.
- **NEGATIVE-IMPORT** -- a `WORKSPACE_ROOT` with no `lib/` refuses `exit 1` with no root escaping.
- **NEGATIVE-SHAPE** -- a stub `address()` that exits 0 with a wrong-shaped root IS refused by the guard.

The third arm exists because the FIRST version of this check asserted the wrong mechanism and failed
itself: under `set -euo pipefail` the failing command substitution aborts the script before the `case`
runs, so **the shape guard is unreachable for the registry failure its own comment describes** ("fail
closed ... if it is empty"). The fail-closed property holds; the mechanism is not the one the comment
credits. Without the third arm a reader would credit the guard for a refusal `set -e` produced.

One thing the cone still lacks, named because it makes a gate read vacuous rather than refuse:
`org/missions/DIRECTIVES.yaml` is outside it, so the commit-time naming gate prints `NAMING ERROR ...
DIRECTIVES.yaml` and **grades nothing**. Its WARN window means it never blocks. Worth adding to the cone
clause if the issuer wants that limb to actually grade.

## 8. ⛔ THIS RELEASE WOULD CHANGE A PAGE IT DOES NOT TAKE -- row `Z-S133`, and it needs a ruling BEFORE Phase B

**Deploying from this tree moves `/yearinreview`'s served md5 from `0d828b51` to `3bbd5ab2`.** Identical
content; 344 line terminators. This release takes neither of yr-1's files, so a half reading "the
release's files only" would not expect it.

The mechanism, measured in both trees at the same commit:

| | on disk | blob at HEAD | `git status` |
|---|---|---|---|
| `C:/tmp/og-rel-gt3` (fresh checkout) | `3bbd5ab2`, 47,891 B, **0 CRLF** | `3bbd5ab2` | clean |
| `C:/tmp/og-rel-yr2` (the tree that deployed) | `0d828b51`, 48,235 B, **344 CRLF** | `3bbd5ab2` | clean |

The path carries `.gitattributes text=set, eol=lf`, so the blob is LF and **every clean checkout
materialises LF**; yr-1 deployed from a tree whose WORKING COPY held the CRO's original CRLF bytes, and
`deploy-to-ec2.sh` tars the working copy. `git status` reports the path clean in BOTH trees, because
`eol=lf` normalises on read -- which is why nothing complained. The host serves `0d828b51` today,
consistent with that.

**This also corrects my own yr-1 record, and I have fixed it in place.** That ask and `W/yr_release.json`
both said a clean checkout "re-materialises the CRLFs", stated as measured. It does not. What I had
measured was a re-hash of a working copy that already held CRLF, which cannot distinguish the two cases.
**The landed state is correct and needs no redeploy** -- the host serves the CRO's bytes, the data date is
present, and `yr1.AC2` passed against what is genuinely live. What was wrong is the record's reason, and
the forward consequence: the served form is a property of the DEPLOYING TREE, not of the release, so it
is not reproducible.

Two routes, and this seat picks none because it decides what you are signing:

- **(a) ADOPT THE LF FORM -- recommended.** Let this deploy ship the blob's bytes, amend yr-1's A3 oracle
  and `W/YR_SERVED.json` to `3bbd5ab2`, and accept a one-time 344-terminator change to a page whose
  rendered content does not change. Stable forever after, because every clean checkout reproduces it.
- **(b) PRESERVE `0d828b51`.** Write the CRLF bytes into this deploy tree's working copy before the
  deploy so the page is a 0-diff. Keeps the record true and the host byte-stable, but it makes the served
  artifact a property of the deploy tree again -- the same shape A6(2) already had to rule on for
  `lib/trading_calendar.py`.

Until this is ruled, a correct deploy would make a later `yr1.AC2` read host-md5 != source and FAIL.

## 9. The `rollback`

Redeploy the base `bf7ffb62f4` through `safe-ec2-deploy.sh` with `DEPLOY_BASE_REF`. Complete, not a hope:
that ref's parity with the host was measured at **107 of 107** minutes before this cut, and the base is
the live release rather than an older one. No IAM to undo. Note that a rollback leaves
`/opt/opal-gateway/lib/` in place -- the older artifact simply does not reference it, and no code in the
base reads it. **And if route (a) of section 8 is taken, the rollback also restores the page's CRLF
form**, because the base's working copy is whatever tree performs the rollback: pick the rollback tree
deliberately, or the page moves again.

## 10. The `triggers` Phase B reads back

| trigger | instrument | pass |
|---|---|---|
| service up | `GET /health` on `127.0.0.1:8080` | `{"ok":true}` |
| registry **+10** | the app's own registry; `registry_before` re-read at **46** on the live host at 00:0xZ | **46 -> 56** |
| `.env` names unchanged | key NAMES only | unchanged (54 today) |
| the running bytes ARE the release | SSM md5 over `app/`, `deploy/`, `dashboard/` vs `047f11aa99` | all equal |
| **`lib/trading_calendar.py` on the host** | SSM md5 | **`3de6a337e268614698943b038248113b`** |
| **a numeric `trading_days_behind_t1`** | the served `harvest_resolve_security` / `harvest_security_coverage` answers | a number, not `absent_reason` -- this closes row `Z-S125` |
| **the `/yearinreview` page** | SSM md5, per section 8's ruling | `0d828b51` under route (b), `3bbd5ab2` under route (a) -- **stated, either way** |

**The `lib/` md5 oracle is not the repo's copy.** gt-8 stages `$WORKSPACE_ROOT/lib/trading_calendar.py`,
and `WORKSPACE_ROOT` is the DEPLOY TREE -- pinned at the base for every file this cut did not take. So the
artifact carries the base's calendar (`3de6a337`, hardcoded NYSE fallback 2024-2027), not trunk's newer
one (`6596e52f`). Both cover the current frontier, and the numeric lag in section 6 was measured against
the copy that will actually ship. Comparing the host against `6596e52f` would read a correct deploy as a
mismatch (A6(2)).

The CVO's A3 condition stands: `harvest_search_articles` is read through `mcp.opalinvest.dev` against the
ALB's 60 s idle timeout; a 502/504 or a call over 60 s pulls **only that tool**, with an ARMED row naming
the issuer, not the release. From this box the pruned call measures 38-48 s; the host is in-region and the
public-endpoint read is the measurement that counts.

Any trigger failing: redeploy the base and file an ARMED row naming `2.0.0_SA_COO~O`.

## 11. What is NOT asked

No IAM, no grant, no store write, no vendor call, no new bucket or prefix, no route, no `.env` key, no
catalog edit. `harvest_get_published_analysis` (gt-5), `typed_scope.py`, `news_typed.py`,
`tests/test_og_gt8.py` and the gt-10 portal modules are not in this release. And no deploy until all
three halves are signed at this `release_sha` **and** section 8 is ruled.
