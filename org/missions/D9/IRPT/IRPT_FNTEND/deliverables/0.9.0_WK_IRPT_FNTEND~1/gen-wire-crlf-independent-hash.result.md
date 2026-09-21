# IRPT_FNTEND.TO-FE-s-50 -- gen-wire.ts CRLF-independent hash. Result.

Worker `0.9.0_WK_IRPT_FNTEND~1`, worktree `C:/tmp/wk-irpt_fntend-9-1-fe-s-50` (branch
`wk-irpt_fntend-9-1-fe-s-50`), portal sub-worktree `C:/tmp/wk-irpt_fntend-9-1-fe-s-50/portal`
(branch `wk-irpt_fntend-9-1-fe-s-50-portal`).

## THE FIX

`portal/src/pages/InvestorReporting/__tests__/fe-s-13/gen-wire.ts` gained one helper,
`stableTextForHash(text) { return text.replace(/\r\n/g, '\n') }`, at `:118-125` (right
after `sha256Of` at `:107-109`, unchanged). It is called at the four named call sites,
wrapping the existing argument -- `sha256Of(text)` -> `sha256Of(stableTextForHash(text))`
(or `stableTextForHash(schemaText)` at the one site that names the variable
`schemaText`):

- `:304` -- `renderModule()`'s per-document header digest (was `:293` pre-edit).
- `:376` -- `renderResponses()`'s per-operation header comment (was `:365`).
- `:384` -- `renderResponses()`'s per-operation `pins` entry (was `:373`).
- `:498` -- `generate()`'s main-loop `pins` entry (was `:487`).

No other function's logic changed. `renderType`, `renderIndex`, `routeRows` and
`sha256Of` itself are byte-identical to what this worktree started with.

## THIS CHECKOUT'S OWN LINE ENDINGS

`git ls-files --eol docs/contracts/investor-reporting/v1/AnalysisReport.schema.json`
reads `i/lf w/crlf` -- this checkout's working tree carries CRLF (core.autocrlf=true),
which is exactly the case row `IRPT_FNTEND-S68` (round 8) named: the same schema bytes
hash differently on a CRLF checkout than on the LF checkout that produced the
currently-committed `contracts/wire/*.ts` headers. So regenerating on THIS checkout
was a real, non-vacuous exercise of the fix -- not merely a no-op confirmation.

## REGENERATION

Ran the generator via its own CLI entry (`import.meta.main`):
`bun run src/pages/InvestorReporting/__tests__/fe-s-13/gen-wire.ts` ->
`WIRE TYPES GENERATED: 11 of 11; RESPONSE ENVELOPES GENERATED: 12 of 12 routes`, rc=0.

`git diff --stat src/pages/InvestorReporting/contracts/wire/` (after `grep -v
"^warning"` to drop the CRLF-checkout noise) showed exactly 12 files changed, each a
single line -- the `Source sha256:` value -- and nothing else:

```
 .../contracts/wire/AnalysisReport.ts               |  2 +-
 .../contracts/wire/AnalysisRequest.ts              |  2 +-
 .../contracts/wire/DirectoryEntry.ts               |  2 +-
 .../contracts/wire/ExportBundle.ts                 |  2 +-
 .../contracts/wire/ExportReceipt.ts                |  2 +-
 .../contracts/wire/HoldingsSnapshot.ts              |  2 +-
 .../contracts/wire/NarrativePacket.ts               |  2 +-
 .../contracts/wire/PerformanceReport.ts             |  2 +-
 .../contracts/wire/RenderPackage.ts                 |  2 +-
 .../contracts/wire/ResolvedScope.ts                 |  2 +-
 .../contracts/wire/StatusEnvelope.ts                |  2 +-
 .../InvestorReporting/contracts/wire/responses.ts   | 24 +++++++++++-----------
 12 files changed, 23 insertions(+), 23 deletions(-)
```

(`responses.ts` carries 12 response headers/pins -- one sha256 line per operation,
24 changed lines total = 12 header-comment lines + 12 `pins:` array lines.)

`index.ts` (the third generated file, carrying the `pins` array with `{name, sha256}`
per document) showed as `M` in `git status --porcelain` both before and after
`git add`, but `git diff`, `git diff --cached` and `git hash-object` all agreed its
clean-filtered bytes are IDENTICAL to the committed blob
(`896fb846d00b9de863bbf9a94e2cb993a00de79b` both ways) -- a stat-level false-dirty
flag, not a real change; `safe-commit.sh`'s own `git add` confirmed this by NOT
including it in the 14-file commit (11 document types + `responses.ts` + `gen-wire.ts`
+ the new test = 14; `index.ts` excluded because `git add` found nothing to stage).

## TESTS

New: `fe-s-50/hash-stability.test.ts`, one case per one of the four call sites
(denominator 4), each built from REAL on-disk schema/response bytes (never synthetic
text) read twice -- once normalized to LF, once forced to CRLF -- through the fixed
code path. `SAME HASH AT CRLF AND LF: 4 of 4`.

Existing `fe-s-13` suite (content-pins, field-map, no-route, producer-fixtures,
request-corpus, routes): 33 pass / 0 fail, unaffected.

Collateral check (not an acceptance criterion, run for confidence): `fe-s-25`
(consumer-boundary / `generator.test.ts`, whose `F25-AC8` is the exact test that
surfaced row S68) also stayed green after the regeneration and commit: 12 pass / 0 fail.

Whole-portal typecheck: `tsc -b --noEmit`, rc=0, both before and after regeneration.

## A LABEL CORRECTION IN THE NEW TEST

The cell text quoted the four call sites' line numbers at spawn time (:293, :365, :373,
:487) -- before this cell's own edit (the `stableTextForHash` helper, 8 lines) shifted
everything after it down. The first commit's `hash-stability.test.ts` printed those
pre-edit numbers in its labels even though it ran against the post-edit file. A second,
label-only commit re-pointed them to the current lines (:304, :376, :384, :498,
confirmed by `grep -n "sha256Of(stableTextForHash" gen-wire.ts` against the committed
blob). No behavior change: `SAME HASH AT CRLF AND LF: 4 of 4` and `tsc -b --noEmit rc=0`
both held before and after.

## COMMITS

Portal (frozen, LOCAL only):
- `57251c1a` "fix(FE-s-50, 0.9.0_WK_IRPT_FNTEND~1): gen-wire.ts's stamped hash is
  CRLF-independent" -- 14 files changed (gen-wire.ts, the new test, 11 document wire
  types, responses.ts).
- `05dae2bd` "docs(FE-s-50, 0.9.0_WK_IRPT_FNTEND~1): fix stale line-number labels in
  hash-stability.test.ts" -- 1 file changed, the label correction above.
