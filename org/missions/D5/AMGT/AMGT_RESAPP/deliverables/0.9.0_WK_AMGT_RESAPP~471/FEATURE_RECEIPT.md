# FEATURE RECEIPT -- AMGT-bn-1 (AMGT_RESAPP round 107)

## What the branch carries

- Branch: `cand/dell1/amgt-sa-team-estimate-mark` (nested portal worktree `C:/dev/wk-resapp-471/portal`, LOCAL, not pushed)
- Head commit: `bb56c53d12a506bf3441bf7e4b2efb197a9e752f` (LOCAL; the re-seat commit on top of the first pass `844d72ebeeaa024b1518706781b2e65052cfe759`)
- Base: `e0b43076d9daf56f8eb4937137180e3cf4246e7f` (PROD)
- Changed paths (`git diff --name-only e0b43076 HEAD`):
  - `src/pages/SecurityAnalysis/tabs/ModelTab.tsx`
  - `src/pages/SecurityAnalysis/__harness__/teamEstimateMark.harness.cjs`
  - `src/pages/SecurityAnalysis/__harness__/teamMarkFixture.SHOP_CN_Equity.json`
  - `src/pages/SecurityAnalysis/__harness__/teamMarkFixture.PBR_US_Equity.json` (replaced at the re-seat with the live post-withhold body, byte copy of `round107_prep/fixtures/pbr_model_slice_live.json`)
  - `src/pages/SecurityAnalysis/__harness__/teamMarkFixture.GOOGL_US_Equity.json`

## Pages changed

| page | route | class | gate |
|------|-------|-------|------|
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

- `package.json`: `git diff e0b43076 HEAD -- package.json | wc -l` = 0
- `bun.lock`: `git diff e0b43076 HEAD -- bun.lock | wc -l` = 0
- `src/lib/firmAccess.ts`: `git diff e0b43076 HEAD -- src/lib/firmAccess.ts | wc -l` = 0
- `src/App.tsx`: `git diff e0b43076 HEAD -- src/App.tsx | wc -l` = 0

## How to look

- Dev build: `cd portal && bun run dev:live --port 5174`
- Page: `/security-analysis`, Model tab, Key Figures P/E row. Names: `SHOP CN` (2025 text range `74x-193.1x`, 2026E and 2027E team estimates carry the mark), `PBR US` (2026E `5.9x` and 2027E `6.1x` are team estimates and carry the mark; the vendor ratio is withheld for 2026 to 2028), `GOOGL US` (vendor P/E, no mark).
