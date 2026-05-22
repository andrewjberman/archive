# SSCN_TOOLBAR.001 — Push DEV + promote the Security Scanner filter toolbar to PROD

<status>complete</status>

**From:** 0.3.0_DE_TradingOperations
**To:** 0.3.0_DT_TradingOperations
**Authorization:** Andrew-direct 2026-05-22 — "Once completely validated, have 0.3.0_DT commit and push as well as merge/deploy to PROD." Validation is complete (see below). This TO IS the GO — begin immediately.

## Context

The Security Scanner filter toolbar (`ScannerFilterToolbar.tsx` — ticker/company search + sector dropdown, wired into both grid tabs; per-column AG Grid header filters enabled) is committed to portal **DEV `4938bf36`** — one commit ahead of origin/DEV (`b5dce977`). Typecheck + lint clean.

**Validation — DE ran a closed-loop puppeteer-core/CDP smoke against the DEV worktree dev server (:5175), both grid tabs. 15/16 PASS:**
- Toolbar renders on both Universe Data + Security Scanner tabs — PASS
- Search input filters: 1002 -> 808 of 1002 securities on "a", restores on clear — PASS both tabs
- Sector dropdown (14 options) filters: 1002 -> 25 of 1002 on "Business Services" — PASS both tabs
- Per-column AG Grid header filter popup opens ("Contains" text / "Equals" number) — PASS both tabs
- The 1 non-PASS: a single `[INFFIN#10] getFeeEfficiency AbortError` console error on the universe-data iteration — an Advisor-Intelligence fee request aborted on navigation unmount; **out of scope, not the toolbar, not introduced by `4938bf36`.** Not a blocker.

Runner: `.frontend-dev/runners/sscn_toolbar_verify_runner.mjs` (untracked, in the DEV worktree). Screenshots: `.frontend-dev/screenshots/sscn_toolbar_verify/`.

## Scope

1. **Push local DEV -> origin/DEV.** Exactly 1 commit (`4938bf36`) ahead. Pre-push typecheck gate as usual.
2. **Promote `4938bf36` to portal PROD.** Cherry-pick onto PROD (HEAD `7442fc9d`) — 3 files, no overlap with the MDPF_ASSETS.033 lane. Use the canonical procedure in your `deployment_map.xml` `<portal_prod_promotion>` (ea35306b9). NOTE on worktree occupancy: the main tree currently holds PROD and `.runtmp/portal-dev-verify` holds DEV — both branches are occupied, so a fresh `git worktree add PROD` is not possible right now. Sequence at your discretion; the main tree (on PROD, clean) is the available path for this cherry-pick. The permanent ephemeral-worktree form applies once the transitional worktree occupancy clears.
3. **Tag + deploy.** `git tag -l "portal-v*" | sort -V | tail -3` to confirm the next version (v2.1.96 is current). Push `--follow-tags`. Verify GHA "Deploy to Production" SUCCESS + opalinvest.dev HTTP 200.
4. **Bump the parent-repo portal gitlink** to the new PROD HEAD; commit to CLOUD.

## Coordination

- DE holds `.runtmp/portal-dev-verify` (DEV worktree, :5175 dev server) until this promotion is done; DE then hands it to 0.4.0_DE_ClientPlatform~B for MDPF_ASSETS.033. 0.4.0_DE's .033 commit lands on DEV AFTER this push — your promotion is off `4938bf36`, unaffected.
- The main-tree DEV restore (your separate open item) stays gated on the dev-verify worktree teardown — unchanged by this TO.

## Acceptance criteria

- origin/DEV HEAD = `4938bf36`.
- origin/PROD carries the toolbar cherry-pick; new `portal-v2.1.x` tag pushed.
- GHA "Deploy to Production" SUCCESS; opalinvest.dev HTTP 200; toolbar visible on the live Security Scanner page.
- Parent-repo portal gitlink bumped + committed to CLOUD.
- RAVC2 evidence back to DE: commit hashes, tag, GHA run, opalinvest.dev verification.

## Compiler tools mandate

- Before: `comp-transform schema-check UniverseScannerTab` + `UniverseDataTab` (DE ran these at build — re-run if you touch source; you should not — this is a promotion, not an edit).
- After: confirm 0-diff / clean cherry-pick; no Lambda/IAM changes (portal-only).
