# IRPT_BCKEND.TO-IB-rtr-1 -- RESULT

Worker: `0.9.0_WK_IRPT_BCKEND~17` | Branch: `wk-irpt_bckend-18-17` | Parent commit: `7a55a7327d`

## What was fixed (CELL (a)-(d))

1. **`applyRenderHeaders`** (`infra/aws/lambda-edge/auth-validator-edge/render_auth.mjs`) now injects
   `X-Origin-Verify: cloudfront`, in the SAME shape as the human path's own injection
   (`index.mjs:518`, unchanged): `request.headers["x-origin-verify"] = [{ key: "X-Origin-Verify",
   value: "cloudfront" }]`. This is the constant, never caller-suppliable, and OVERWRITES any
   client-supplied header of that name, exactly like every other injected header.
2. **GET-only admission.** `evaluateRenderBranch` (`index.mjs`) now takes `request.method` and refuses
   (`kind: "refuse"`, `"Render token only admits GET"`) any non-GET render-branch request, checked after
   URI admission. The call site now passes `request.method` through.
3. **The real asset allowlist.** `isRenderStaticAssetUri` (`render_auth.mjs`) now requires the URI to
   start with `RENDER_STATIC_ASSET_PREFIX = "/assets/"` (Vite's own default public asset URL, `<base>` +
   `<assetsDir>/` = `/` + `assets/`) and match the same extension regex as before -- replacing the old,
   disclosed-as-a-guess `/investor-reporting/` prefix (`W16-S2`).

## Exact config source quoted (CELL (d))

`.gitmodules` in this worktree is a tracked, 0-byte file -- `git submodule update --init portal` fails
(`fatal: no submodule mapping found in .gitmodules for path 'portal'`, rc=128; filed `IRPT_BCKEND-W17-S1`).
Read instead via `git -C <main-workspace>/portal show 15ceef793bda03c102539c209dde25cb18ab2eba:vite.config.ts`
(`15ceef793bda03c102539c209dde25cb18ab2eba` = the gitlink's own pinned commit, `git ls-files -s portal`; the
main workspace's independent `portal/` checkout already holds that exact commit object). The relevant lines,
verbatim:

```ts
export default defineConfig({
  plugins: [react()],
  cacheDir: path.resolve(path.dirname(fileURLToPath(import.meta.url)), '.vite'),
  resolve: {
    alias: {
      '@': path.resolve(path.dirname(fileURLToPath(import.meta.url)), './src'),
    },
  },
  build: {
    rollupOptions: { output: { manualChunks: { ... } } },
    chunkSizeWarningLimit: 600,
  },
  server: { ... },
})
```

**Neither `base` nor `build.assetsDir` is set anywhere in this object** -- both take Vite's own defaults
(`base: '/'`, `assetsDir: 'assets'`). Corroborated two ways:

- Exactly ONE `vite.config*` file exists in the whole portal tree at that pin (`git -C <main-workspace>/portal
  ls-tree -r --name-only <pin> | grep vite.config` -> one hit), and `package.json`'s `build` script
  (`"tsc -b && vite build --configLoader runner"`) passes no `--base` flag.
- `infra/aws/terraform/portal-auth/cloudfront-distribution.tf` (24 `path_pattern`-scoped behaviours,
  enumerated this session) carries **no** behaviour for `/investor-reporting/*` or `/assets/*` static files
  -- both fall through to the single DEFAULT "SPA static assets" cache behaviour (`:270`, `:121`), so nothing
  in the CloudFront config scopes any built asset to a route-specific prefix either.

So Vite's own default public URL for every built asset is `/assets/<name>-<hash>.<ext>` -- root-relative,
**never** `/investor-reporting/`-prefixed. This matches this round's own decomposition text, written by the
issuer before this cell ran: *"root `/assets/`, not `/investor-reporting/`-prefixed"*
(`IRPT_BCKEND_DECOMP.md` v0.22, R18.1, row `IB-rtr-1`).

## A genuine conflict between CELL (d) and BOUNDS/R118-AC1 (filed `IRPT_BCKEND-W17-S2`)

Fixing the allowlist to the REAL shape necessarily makes ONE test in the pre-existing, unedited
`deliverables/0.9.0_WK_IRPT_BCKEND~16/test_edge_render_delegate.mjs` suite fail: `"three-path admission: a
static asset under /investor-reporting/ is admitted"` asserted the OLD guessed prefix (disclosed by that
worker as a guess, `W16-S2`, because `portal/` was unavailable in its worktree). That test cannot both keep
passing AND have this cell implement the real, config-derived allowlist -- the two shapes are different URIs.
BOUNDS forbids editing any existing test's expected value in that suite, and this cell's own `<paths>` grant
does not include `deliverables/0.9.0_WK_IRPT_BCKEND~16/` at all, so this worker cannot fix that file. The
real fix was implemented (matching the issuer's own decomp text and the CVO's diagnosis, which is this
cell's entire reason for existing), and the criterion is graded HONESTLY below rather than forced green.
See row `IRPT_BCKEND-W17-S2` for full grounding and the proposed remedy (a follow-on cell with write access
to that file).

## Full test output -- own suite (14 of 14 PASS, rc=0)

```
{"event":"render_accepted","jti":"rnd_marker_001","path":"/investor-reporting/print"}
Auth OK (render): render_id=rnd_marker_001 path=/investor-reporting/print
{"event":"render_accepted","jti":"rnd_marker_001","path":"/investor-reporting/print"}
Auth OK (render): render_id=rnd_marker_001 path=/investor-reporting/print
{"event":"render_accepted","jti":"rnd_marker_001","path":"/investor-reporting/print"}
Auth OK (render): render_id=rnd_marker_001 path=/investor-reporting/print
{"event":"render_denied","reason":"method_not_allowed","jti":"rnd_marker_001","path":"/investor-reporting/print","method":"POST"}
{"event":"render_denied","reason":"method_not_allowed","jti":"rnd_marker_001","path":"/api/scoped/investor-reporting/performance/acctset123","method":"POST"}
{"event":"render_accepted","jti":"rnd_marker_001","path":"/investor-reporting/print"}
Auth OK (render): render_id=rnd_marker_001 path=/investor-reporting/print
{"event":"render_accepted","jti":"rnd_marker_001","path":"/assets/index-49a2f1c8.js"}
Auth OK (render): render_id=rnd_marker_001 path=/assets/index-49a2f1c8.js
{"event":"render_denied","reason":"uri_not_admitted","jti":"rnd_marker_001","path":"/assets/README.md"}
{"event":"render_denied","reason":"uri_not_admitted","jti":"rnd_marker_001","path":"/unrelated/nothing-here.js"}
{"event":"render_denied","reason":"uri_not_admitted","jti":"rnd_marker_001","path":"/investor-reporting/assets/app-9f3c1a.js"}
v MISSING-marker control: the PRE-FIX render_auth.mjs (this order's own parent commit, 7a55a7327d) never injects X-Origin-Verify -- reproduces the ORIGINAL bug (66.1056ms)
v MISSING-marker control, live code: the FIXED applyRenderHeaders DOES inject X-Origin-Verify=cloudfront, in the human path's own shape (1.5733ms)
v MISSING-marker control, full handler: a genuine render-admit request now carries X-Origin-Verify on the forwarded request (6.3231ms)
v SPOOFED-marker control: a client-supplied X-Origin-Verify (wrong value) is OVERWRITTEN by the verified constant, never passed through (1.5085ms)
v SPOOFED-marker control, unit-level: applyRenderHeaders overwrites a pre-existing x-origin-verify key on the request object (0.1575ms)
v GET-only: a GET to the print route with a valid render token is admitted (positive control) (1.3149ms)
v GET-only: a POST to an otherwise-admissible render URI, with an otherwise-valid render token, is refused BY THE BRANCH (1.337ms)
v GET-only: a POST to one of the three admissible render API URIs is also refused (1.4016ms)
v real asset allowlist: the print route itself is still admitted (1.318ms)
v real asset allowlist: the DERIVED real asset path shape (/assets/<hash>.<ext>, Vite's own default) is admitted (1.51ms)
v real asset allowlist: a non-JS/CSS/etc file directly under /assets/ (wrong extension) is still refused (1.4103ms)
v real asset allowlist: an UNRELATED URI outside the assets prefix entirely is refused (negative control) (1.4186ms)
v real asset allowlist: the OLD guessed shape (/investor-reporting/assets/*) is now correctly REFUSED -- it is not a real Vite build output path (1.3114ms)
v RENDER_STATIC_ASSET_PREFIX exports the exact derived value (0.1015ms)
i tests 14
i suites 0
i pass 14
i fail 0
i cancelled 0
i skipped 0
i todo 0
i duration_ms 744.5057
```
(rc=0, measured via `echo $?` immediately after the run.)

## Full test output -- pre-existing IB-rtq-3 suite, UNMODIFIED (18 of 19 PASS, rc=1)

```
{"event":"render_accepted","jti":"rnd_test_001","path":"/investor-reporting/print"}
Auth OK (render): render_id=rnd_test_001 path=/investor-reporting/print
{"event":"render_denied","reason":"uri_not_admitted","jti":"rnd_test_001","path":"/investor-reporting/assets/app-9f3c1a.js"}
{"event":"render_accepted","jti":"rnd_test_001","path":"/api/scoped/investor-reporting/performance/acctset123"}
Auth OK (render): render_id=rnd_test_001 path=/api/scoped/investor-reporting/performance/acctset123
{"event":"render_accepted","jti":"rnd_test_001","path":"/api/scoped/investor-reporting/analysis/job456/sections"}
Auth OK (render): render_id=rnd_test_001 path=/api/scoped/investor-reporting/analysis/job456/sections
{"event":"render_accepted","jti":"rnd_test_001","path":"/api/scoped/investor-reporting/narrative/report789"}
Auth OK (render): render_id=rnd_test_001 path=/api/scoped/investor-reporting/narrative/report789
{"event":"render_denied","reason":"uri_not_admitted","jti":"rnd_test_001","path":"/investor-reporting/status"}
{"event":"render_accepted","jti":"rnd_overwrite_001","path":"/investor-reporting/print"}
Auth OK (render): render_id=rnd_overwrite_001 path=/investor-reporting/print
{"event":"render_accepted","jti":"rnd_test_001","path":"/investor-reporting/print"}
Auth OK (render): render_id=rnd_test_001 path=/investor-reporting/print
{"event":"render_denied","reason":"forbidden_claim","jti":"rnd_test_001","path":"/investor-reporting/print"}
{"event":"render_denied","reason":"forbidden_claim","jti":"rnd_test_001","path":"/investor-reporting/print"}
{"event":"render_denied","reason":"forbidden_claim","jti":"rnd_test_001","path":"/investor-reporting/print"}
{"event":"render_denied","reason":"forbidden_claim","jti":"rnd_test_001","path":"/investor-reporting/print"}
{"event":"render_denied","reason":"expired","path":"/investor-reporting/print"}
Auth OK: user=advisor1@49financial.com tier=advisor path=/api/scoped/investor-reporting/directory
Auth FAILED: path=/api/scoped/investor-reporting/directory error=invalid signature
Auth FAILED: path=/api/scoped/investor-reporting/directory error=jwt expired
Auth OK: user=admin1@opal-capital.com tier=internal path=/api/scoped/investor-reporting/directory
v three-path admission: /investor-reporting/print is admitted (8.6398ms)
x three-path admission: a static asset under /investor-reporting/ is admitted (2.973ms)
v three-path admission: GET performance API is admitted (1.7591ms)
v three-path admission: GET analysis sections API is admitted (1.4704ms)
v three-path admission: GET narrative API is admitted (1.5022ms)
v any other URI is refused BY THE BRANCH itself, never falls through to the human path (1.2838ms)
v header injection OVERWRITES client-supplied values of the same names (1.3478ms)
v X-Advisor-Id / X-Advisor-Role / X-User-Type are ABSENT on every render-token admit path, even when the caller supplied fake values (1.2753ms)
v a render token carrying tier=internal is refused BY THIS BRANCH, not merely unused downstream (1.9108ms)
v a render token carrying role=admin is refused BY THIS BRANCH (3.6775ms)
v a render token carrying firmRole=admin is refused BY THIS BRANCH (1.4836ms)
v a render token carrying userType=Dev is refused BY THIS BRANCH (1.1525ms)
v a render token past its exp is refused, using the JWT library's own expiry check (2.9444ms)
v a token for the wrong aud (a human portal token) falls through to the EXISTING human-path evaluation, completely unchanged (2.5192ms)
v regression: missing Authorization header is still refused exactly as before (0.1254ms)
v regression: a token signed by neither key is still refused via the existing catch-all (1.3668ms)
v regression: an expired HUMAN token is still refused exactly as before (1.2882ms)
v regression: the pre-existing admin bypass still injects the pre-existing header set (1.311ms)
v V1 refusal confirmation: a render-signed token fails V1's own verify() parameters with a SIGNATURE error (wrong key), before aud/iss are ever checked (1.8689ms)
i tests 19
i suites 0
i pass 18
i fail 1
i cancelled 0
i skipped 0
i todo 0
i duration_ms 644.6355

x failing tests:

test at ..\0.9.0_WK_IRPT_BCKEND~16\test_edge_render_delegate.mjs:229:1
x three-path admission: a static asset under /investor-reporting/ is admitted (2.973ms)
  AssertionError [ERR_ASSERTION]: SPA static asset must be admitted, not refused
  true !== false
    actual: true, expected: false, operator: 'strictEqual'
```
(rc=1, measured; the single failure is exactly the `/investor-reporting/`-prefixed asset test, the one
whose own assumption this cell's fix corrects.)

## Combined invocation (verbatim, as R118-AC1 names it)

`node --test test_v3_origin_marker_and_assets.mjs && node --test ../0.9.0_WK_IRPT_BCKEND~16/test_edge_render_delegate.mjs`
-> combined rc=1 (the `&&` short-circuits are not triggered since the first command exits 0, but the second
exits 1, so the whole chain exits 1). `<expect>` names `rc=0 on both`; the true measured combined result is
rc=0 on the first, rc=1 on the second. **R118-AC1 is graded FAIL below, honestly, per row `IRPT_BCKEND-W17-S2`.**

## Mutation control (one, real)

`index.mjs`'s GET-only check (`if (method !== "GET") { ... }`) was mutated to `if (false && method !== "GET")`
(dead condition, never fires) and the own suite re-run: both GET-only tests failed as expected
(`AssertionError: Expected values to be strictly equal: false !== true`), confirming the tests actually
exercise the guard. The file was restored from `.scratch/index.mjs.bak` and the suite re-confirmed 14/14
PASS twice (determinism), `git diff` confirmed only the intended two changes remain in `index.mjs`.

## Surprise rows filed

- `IRPT_BCKEND-W17-S1` -- `git submodule update --init portal` fails in this worktree (`.gitmodules` tracked,
  0 bytes); worked around read-only via the main workspace's own portal checkout.
- `IRPT_BCKEND-W17-S2` -- CELL (d)'s real-config derivation and BOUNDS/R118-AC1's "pre-existing suite passes
  unmodified, rc=0" cannot both hold; the real fix was chosen and the criterion graded honestly.

Both `UNDER_INVESTIGATION`, `INERT`, `OBSERVATION` -- neither blocking, both kept working per BOUNDS.
