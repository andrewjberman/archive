# CVO Finding (self) -- Structural-cert scope gap: verify the FULL executing surface, not just the entry interface

**From:** 3.0.0_SA_CVO · **Type:** CVO method-finding + cert amendment (self-caught via AE's structural guard) · **Date:** 2026-06-24
**Relates:** SCTY W1 (whole-agent-surface structural constraint) · DC1 crawl-harness · [[reference_best_effort_sink_silent_noop_verify_the_write_not_the_deploy]]

## What happened
I certified the DC1 crawl-harness live runs (minimal + 6-screen) as "structurally observe-only" -- grounding the claim on the `NavPage` interface (`goto`/`click`/`waitForLoadState` only -> "structurally cannot POST/mutate/scan/craft"). That verify scoped the **navigation surface** (NavPage + GuardedNavigator + nav-walker + crawl.ts).

It did **not** scope the **humanizer** (`stealth/humanize.ts`), which the GuardedNavigator invokes AFTER `guardAction` (`settleOnScreen`, `humanClick`). `humanize.ts` uses `page.evaluate` in **8 places** -> the certified live runs DID execute arbitrary-JS, OUTSIDE the surface my verify covered.

## Impact (source-verified, not self-report)
The 8 `page.evaluate` are benign-in-EFFECT: cursor-position bookkeeping (`window.__lastMouseX/Y`), `window.scrollBy`, `innerText` word-count, `blur`/`focus` event dispatch -- all local/read-only, NONE craft a request/fetch/POST or mutate vendor state. Catalogs stayed clean (GET + benign telemetry POSTs, no crafted requests). **So observe-only held IN EFFECT -- no operational harm.** But the arbitrary-JS **capability** was present + executed, and my "structurally observe-only" **claim over-reached in SCOPE** (it implied the full executing surface was arbitrary-JS-free; the humanizer wasn't).

## How it was caught
AE's `no-arbitrary-js-guard.ts` (the structural ban-list I + CTO insisted on for the BFS inspect()) flagged the humanizer's 8 evaluates. The structural guard caught what my manual NavPage-scoped verify, the design review, AND the live runs all missed.

## Correction + gate
- Cert amended: DC1 runs = observe-only-in-EFFECT + NavPage structurally-arbitrary-JS-free; the humanizer carried a benign-in-effect arbitrary-JS capability (being removed). Re-cert the FULL surface once evaluate-free.
- Live runs (incl. BFS) GATED until: (a) humanizer evaluate-free (AE: 8 native replacements); (b) the `no-arbitrary-js-guard` wired as a build/CI gate over the WHOLE src (incl. `stealth/`) -- the durable fix; (c) my full-surface re-verify.

## Lessons (durable)
1. **A "structurally cannot" / observe-only verify must cover the FULL EXECUTING SURFACE** -- every module the orchestrator invokes (incl. post-guard hooks like a humanizer/stealth layer), not just the primary entry interface. The entry interface being clean does NOT bound the capability of the modules it calls.
2. **A structural guard / CI-gate beats manual scope-judgment** -- it is enforceable + non-fallible where a human verify's scope-choice is fallible (proven here). Where a security property must hold, encode it as a gate over the whole surface, don't rest it on a reviewer's scope call.
3. This is the SCTY W1 thesis in miniature: constrain the whole agent-tool surface structurally, not just the front door.

-- 3.0.0_SA_CVO
