# IRPT_FNTEND.TO-FE-s-32 -- Holdings under the gate: result

Worker `0.9.0_WK_IRPT_FNTEND~2`. Portal commit `7df6b4a2` (branch `wk-irpt_fntend-5-2-fe-s-32`, LOCAL). The proof instance sits beside this file.

## What changed (portal 7df6b4a2)

- `tabs/holdings/HoldingsTab.tsx`. The body renders when FE-s-30's `isAnswerBearing(snapshot.availability)` is true; it no longer requires READY. The predicate is consumed and never copied. `isCompleteState` (unchanged) chooses complete vs qualified. A qualified answer carries `AnswerStatus`, imported from `tabs/reporting/` and not edited: state, qualifier, business date and reason code. It also carries `HoldingsQualification`: the classification gap as raw node counts, and "Target weights -- model revision not named" whenever target weights are shown. A failed request clears the snapshot, as `ReportingTab` does.
- `tabs/holdings/slices.ts`: `classificationGapOf`, `showsTargetWeights`. `tabs/holdings/SliceTable.tsx`: `formatPct` exported; the classification cells carry `data-classification-authoritative`.
- `tabs/holdings/DrillTree.tsx` (W1-S35). The pie labels are drawn inside each slice and show `pctOfParent` from the snapshot. `outerRadius="80%"`, `labelLine={false}`. Slice names stay in the legend and the table.
- `__tests__/fe-s-26/renders-differently.test.ts`. PARTIAL and UNCERTAIN are re-classified as body renders, with ruling I cited per map. The test prints both ways: the READY-only gate's slot, ruling I's slot, and the rendered slot.
- `__tests__/fe-s-22/capture-hash.test.ts`. The DISTINCTION verdict's digest input now reads `round2-captures.frozen.json`, and the verdict moves whole.
- `__tests__/fe-s-32/`: the browser test, the node driver, the no-answer map, and `vite.worktree.config.ts`.

## Both ways

| Measurement | Before (base e85498be) | After (7df6b4a2) |
|---|---|---|
| Holdings slot, target (UNCERTAIN) | status-panel (READY-only gate) | holdings-tab, qualified |
| Holdings slot, missing-attribution (PARTIAL) | status-panel | holdings-tab, qualified |
| Holdings slot, no-answer (UNAVAILABLE, full document present) | status-panel | status-panel @UNAVAILABLE |
| Pie labels inside the chart (3 maps x 390/1440) | 6 of 18 (0 of 3 at 390 on every map) | 18 of 18 |

## Criteria, dev server and port

| Criterion | Server | Port | Deciding line |
|---|---|---|---|
| F32-AC1 | up (not used) | 5213 | `rc=0` |
| F32-AC2..AC6 | UP | 5213 | `4 of 4`; `PARTIAL: CLASSIFICATION GAP SHOWN AS UNKNOWN`; `UNCERTAIN: MODEL REVISION STATED AS UNNAMED`; `6 of 6`; `18 of 18` |
| F32-AC7 | up (not used) | 5213 | `DISTINCTION VERDICT DIGESTS: frozen round-2 set` |
| F32-AC8 | UP (deciding) and DOWN (recorded) | 5213 | up: 102 pass / 0 fail; down: 97 pass / 5 skip / 0 fail, with the declared SKIPPED line |
| F32-AC9 | -- | -- | recorded, graded at L9 |

`IRPT_FE_DEV_PORT=5213` was exported on every `bun test` run. The server was started from `<WS>/portal` as `bun run dev --port 5213 --strictPort --config src/pages/InvestorReporting/__tests__/fe-s-32/vite.worktree.config.ts`. It was killed before this report (PID 3204 and child; afterwards the probe read `ECONNREFUSED`). Ports 5202 and 5237 belonged to other seats and were not touched.

**Worktree-local vite cache: it worked.** `<WS>/.scratch/vite-cache-fe-s-32/deps` was created, and the junctioned main `node_modules/.vite` was not the cache. Its first form, a static import of `vite` and `vite.config.ts`, broke the whole-portal typecheck. The committed form loads the portal config through vite's own `loadConfigFromFile` at runtime (row W2-S28).

## Captures for F32-AC9

Written by the deciding run at portal 7df6b4a2 into this folder, with `fe-s-32_captures.manifest.json`. Disk = manifest = printed digest, 14 of 14.

| File | Map | Viewport | Kind | sha256 |
|---|---|---|---|---|
| `fe-s-32_holdings_observed_390.png` | observed | 390 | full-page | `cb84b12cb89734edb7e13657457530f83fd3ad93afbdeb6a31e79dbf35f5c533` |
| `fe-s-32_holdings_observed_390_table_scrolled.png` | observed | 390 | slice-table scrolled to the classification columns | `4457ec3bceed060de1d31a961eb257f268a0e45d11b9132d78239b947ab188a1` |
| `fe-s-32_holdings_observed_1440.png` | observed | 1440 | full-page | `9f404bf09b2591f28229dc37ac43073588ea1a19751c6f81fe1e3d4d86735527` |
| `fe-s-32_holdings_observed_1440_table_scrolled.png` | observed | 1440 | slice-table scrolled to the classification columns | `2fa733e61d3c05322133cef1e3c8dea408725059d0b67a22ae12bc253e3c7b0c` |
| `fe-s-32_holdings_target_390.png` | target | 390 | full-page | `446581c0365d7f6390599634e1dbf3571d2bf3e319ac784051530fc89f58fa0b` |
| `fe-s-32_holdings_target_390_table_scrolled.png` | target | 390 | slice-table scrolled to the classification columns | `c358bcb406918d386687ecd9a18d48aa7a2848636c487cafecab1051d187ec17` |
| `fe-s-32_holdings_target_1440.png` | target | 1440 | full-page | `6a6f47c9e25fea1fdb822418da24d8b7d8d900038aeb5bd31f1304922bcf0329` |
| `fe-s-32_holdings_target_1440_table_scrolled.png` | target | 1440 | slice-table scrolled to the classification columns | `360b85d807a6684602f6d5c0fb3c4dec100f2cfc860b420e6c0b09b34cd07895` |
| `fe-s-32_holdings_missing_attribution_390.png` | missing-attribution | 390 | full-page | `eef651c1e98b2ebf2f916ad8b6e8461f8fb42c5ffeffd19eed8c09a05d3e066b` |
| `fe-s-32_holdings_missing_attribution_390_table_scrolled.png` | missing-attribution | 390 | slice-table scrolled to the classification columns | `b5875639aabda9bfbf5830ce93be7ebf1ab229a9b493af7b8a51d9a66b27ced5` |
| `fe-s-32_holdings_missing_attribution_1440.png` | missing-attribution | 1440 | full-page | `73d2bcad5f9f7ee80a61def40642d1466c0ca9dc02a11da253bdccdf8485203a` |
| `fe-s-32_holdings_missing_attribution_1440_table_scrolled.png` | missing-attribution | 1440 | slice-table scrolled to the classification columns | `9c946f0d1d8c2ce626ea8125a517ccf493b9207058a40200e4d68630c8f064fc` |
| `fe-s-32_holdings_no_answer_390.png` | no-answer | 390 | full-page | `ae4386efff2797bb1c5dab0d2ba849b2a5f57e7b551f1fd4bb4a1917559b7109` |
| `fe-s-32_holdings_no_answer_1440.png` | no-answer | 1440 | full-page | `6cb48ea502a837ff469f633a1e80078ae4e34dbf21a0bc9c579f34135a269537` |

What a reader sees, per map:
- **observed (READY).** Neutral band "Ready", business date 2026-09-09, reason OBSERVED_CUSTODY_SERVED, and no qualification panel. The table shows basis "observed custody". Advisory reads "unknown" under an authoritative classification because the fixture token 'ADVISORY' is outside the contract enum (row W2-S29).
- **target (UNCERTAIN).** Amber band "Uncertain -- Qualified answer -- not a complete report", reason TARGET_BLEND_MODEL_REVISION_UNNAMED, the line "Target weights -- model revision not named ...", and table basis "target". The reason code appears to reach the band's edge at 390 (row W2-S31, by eye).
- **missing-attribution (PARTIAL).** Amber band "Partial -- Qualified answer ...", reason NODE_ATTRIBUTION_UNAVAILABLE, and "Classification unknown for 4 of 4 holdings nodes ...". The table shows the holdings with supervision and advisory "unknown".
- **no-answer (UNAVAILABLE).** The status panel, with no body.
- **At 390** the full-page capture shows Basis. Supervision and Advisory sit outside the sideways-scrolling table's box, so they are visible only in `*_390_table_scrolled.png` (row W2-S30). At 1440 all three columns are visible in the full-page capture.

## Rows

IRPT_FNTEND-W2-S28, W2-S29, W2-S30, W2-S31. All OBSERVATION and INERT, appended to `surprise-channel/investigations/INVESTIGATION_v2.md`.
