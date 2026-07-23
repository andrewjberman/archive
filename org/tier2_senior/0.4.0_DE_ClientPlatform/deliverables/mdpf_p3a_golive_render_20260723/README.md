# MDPF_3FIRMS.3F-P3a — Cottonwood MDPF page go-live evidence (2026-07-23 ~013xZ)

**Order:** Andrew-direct go-live via CTO 011332Z (supersedes CTO's 010231Z tomorrow-ruling).
**FE commit:** portal DEV `f8ace4f8` (off `08c6d8b2`), pushed to origin. **Data:** DS 3F-G8
trio, served co-sign CTO 012337Z + COO 013145Z, ETags `67f32c56e6f7`/`2ea36da99b3c`/`7dfc132287ba`.
**Render inputs:** the staged artifacts, byte-identical (ETag-matched) to the served copies.
**Harness:** `portal/scripts/ui-smoke.mjs` (auth-stubbed headless Edge), vite dev @5175.

## The two screenshots

| File | View | What it proves |
|---|---|---|
| `cottonwood_internal_select_v3.png` | Internal Opal user, Select Partner -> Cottonwood Capital Advisors | Donut Total AUM **$458M** with real 5-model split (Conservative Growth in distinct cyan — the closed-literal + color-collision fixes exercised), bell curve 291 funded / median **$207,443**, Total AUA tile **$458M** (page internally consistent), quarter tiles honest-N/A (all-None q0–q3, never 0), both trend panels render the labeled honest-absent state ("Daily AUM history begins July 21, 2026"), truthful measured-snapshot footnote. |
| `cottonwood_claims_view.png` | A cottonwood-claims session (`--firm cottonwood`) | Same real numbers firm-scoped: no internal selector, partner nav only, no benchmark-toggle leakage — the page an actual Cottonwood user gets. |

Silver-canvas color law checked on both: white-text idiom only inside dark panels; canvas
notices dark-on-light; no ghost buttons on canvas.

## Honest residuals (stated, not hidden)

1. **Trend panels are labeled honest-absent tonight by design** — the trend slice's values are
   all-null until the global date axis overlaps Cottonwood's facts (~03:30Z nightly), and the
   dispatcher has no Cottonwood 6d leg yet (routed to CTO as must-resolve). The labeled state
   IS the CTO-ruled product for a newborn firm; it self-populates.
2. **Existing-firm no-op is source-derived, not baseline-render-verified**: the new per-firm
   aum-metrics query is `enabled` for cottonwood only, and every touched expression is a
   `??`-fallthrough to the byte-identical prior expression when pair data is absent
   (`trendStackSeries` returns the same `STACK_SERIES` reference when extras=[]). A same-env
   baseline render was correctly blocked by the shared-worktree stash gate. Post-promote live
   verification on the served domain covers all firms.
3. **Live-path curl probes 401 uniformly** (cottonwood AND the control: inflection + global,
   which serve today's live page) — edge auth, not a serving defect; the FE attaches the bearer.
   Full through-auth verification is the post-promote gate.
4. comp-validate has **NO_CONFIG** for the new G8 producer (DS candor row; his follow-up) —
   artifacts carry the producer's fail-loud identities instead, all PASS this run.
