# IB159-1 -- the portal authorizer's render-token path: what is live (IRPT_BCKEND.TO-IB-pr-463)

**Verdict: RELEASED_THE_RECORD_IS_BEHIND** (claim: inferred). Base commit ffbb53b4a4. Read only: the authorizer was not
invoked, nothing was built, signed in to, written or proposed as a release.

## What is live
- `opal-portal-authorizer`: CodeSha256 `gQp2IooAM3EgebVQeII27xcE+KuEDhyYfrlwr6Jqcsc=`, last modified 2026-10-03T19:52:32Z,
  21,172 bytes. The downloaded package's base64 sha256 EQUALS CodeSha256 (measured). One member, `index.mjs`, 65,333 bytes: a
  bun-minified bundle of 4 lines.
- Environment key names: `IRPT_RENDER_JWT_PUBLIC_KEY_PEM` only (names, no values).
- The live member carries the whole render-token path: `authorizeRenderToken`, `isRenderAudienceToken`,
  `hasForbiddenRenderClaims`, `assertBoundedRenderExpiry`, `getRenderPublicKeyPem`, the route table with the series route
  entry, and the handler routes `aud irpt-render` to it before the human path.

## Which source it is
- Compared by content to 5 revisions of the file (26ffa22b79 to ee822c425f), line endings normalised: **matched none**, and it
  cannot match by construction (a 4-line bundle against 263 to 451 lines of source; the raw line counts are uninformative).
  Row IRPT_BCKEND-D2-W318-S1.
- By the bundle-feature test (string literals survive minifying): `ee822c425f` is the match. 60 of its 63 literals are in the
  live member; the 3 absent are import paths the bundler inlined. Everything the four later commits add is present.
- No commit on the file follows ee822c425f; the file at HEAD is that blob, which is also the blob at CLOUD @ca49283ff1, the
  build input the 2026-10-03 ledger names.

## The four commits after the map's 26ffa22b79 (all in the live member)
| commit | date | order | adds | released by |
|---|---|---|---|---|
| 4bca50737e | 2026-09-22 | IB-rtq-2 | the render-token branch, three GET routes | ledger 20260925T1546Z (A2) |
| 18971693ad | 2026-09-22 | IB-rtr-2 | four-claim refusal, exp required and <= 300 s | ledger 20260925T1546Z (A2) |
| 972976ebca | 2026-09-25 | export section A (direct) | past-exp refused, no leeway | ledger 20260925T1546Z (A2) |
| ee822c425f | 2026-10-03 | IB-pr-307 | the 49F reporting series route | ledger 20261003T1946Z |

## Packaging and the map
- Built by `build-nodejs-lambda.sh portal-auth opal-portal-authorizer` (bun bundle, S3), applied by terraform from that S3
  object (`lambdas.tf:50-72`), not by terraform's own archive. Map entry: `artifact_sha256` = the live digest;
  `last_deployed_commit` 26ffa22b79, `last_deployed_at` 2026-09-09. The sha field was brought current (80ba60328c); the
  commit and date fields were not, after two ledgered applies. Row IRPT_BCKEND-D2-W318-S2.

## Senders and routes
- Mint: `irpt-export-render` Lambda (`submit_installed.py:170`; `mint.py:171`), live by digest and key names (switch value
  not read). Carry: render host (`render_export.cjs:278`) and the portal print page (`portal/src/api/api-client.ts:152`, DEV
  dbeb6764 read only).
- From the live authorizer a verifying token is admitted on four routes (performance, analysis sections, narrative, reporting
  series: `index.mjs:57-64`) and refused elsewhere. The ledger of 2026-10-03 records a series read admitted (P1) and a
  foreign-account token refused (P2).

## Orders behind the commits
IB-rtq-2, IB-rtr-2, IB-pr-307: all `complete`; the first two bound "NO Lambda deploy", IB-pr-307 left the deploy to the issuer
under a CTO never-widen half. Export section A: a direct commit, no order file. Ledger entries: see the JSON.

## Not established
No byte-identity with a rebuild (no build allowed); the value of the export switch; the render host and served portal build;
which script wrote the map's sha line; whether the map's recorder was run. Full list in the JSON.
