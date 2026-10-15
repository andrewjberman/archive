# DSGN_RBNDV2 -- round 4: the RSI modal through its real trigger, and the white-alpha BEFORE counts (CTO round-3 analysis @4802286e30, items 1 and 2)

**Author:** `2.0.0_SA_COO~RB`, 2026-10-15 ~12:4xZ. **Branch read:** `feature/dsgn-rbndv2-light` @cf2bdeaa (LOCAL, never pushed), the dev build served at port 5174 against the real backend.
**Method:** a scratch copy of the UI walker (`walk-rbprobe.mjs`, a copy of `.claude/skills/ui-walk/walk.mjs` with a probe and an optional click selector; never committed, deleted when this round closes) signed in as the walker (armed, one load, one action, disarmed; the post-disarm login was REFUSED every time),
pressed a label or clicked a selector, and read the open dialog in the page.

## 1. The RSI modal through its real trigger (item 2, W10-S2)

The RSI modal opens from a click on a bar of the Global RSI chart (`RSIBars.tsx`: a recharts `Bar` `onClick`). The scripted walk clicked `.recharts-bar-rectangle path` (3 matches on `/market`); the dialog titled **Global RSI** opened.
Read: 53 text elements, **0 white-alpha text elements**; the viewport screenshot (`tmp/ui-walk/20261015T123343Z/shots/clicksel.png`, gitignored) shows the A-light frame (white surface, thin silver edge, eyebrow "GLOBAL RSI" with the violet underline and a help icon, a square close control,
a hairline under the header, the Spotlight / Ranked / Full chips with Spotlight active in white on violet, the Hottest and Coldest cards by asset class with legible navy names and signal-coloured figures, a footer line and a Close button). The default Spotlight view holds no recharts axis, so the modal's chart-tick fill is not readable in this view (`tickFills` empty); the Ranked and Full
views were not pressed. **Verdict on the control:** RSI is reachable, so W10-S2 is no longer an unreachable-modal finding; the signal-coloured figures (green, red, orange, yellow) are the FWD-5 population.

## 2. The white-alpha BEFORE counts (item 1)

Counted live in the opened dialog: a text-bearing element is counted when its computed `color` is `rgb(255,255,255...)` or `oklab(0.99...)` (Tailwind v4 computes `text-white/60` as `oklab(0.999994 ... / 0.6)`).

| modal (trigger) | text elements | white-alpha text elements | what they are |
|---|---|---|---|
| Index Performance (press "S&P 500") | 38 | **3** | the inactive period chips `30D`, `90D`, `3Y`: `text-white/60` with a `hover:` variant, computed `oklab(0.999994 ... / 0.6)` |
| U.S. Regime: Momentum (press "Multi-Asset Momentum") | 55 | **4** | the inactive chips `1Y`, `3Y` (same cause) and the chart tooltip labels `Score`, `RSI Score` (`rgba(255,255,255,0.85)` on the violet tooltip: legitimately white, stays) |
| CNN Fear & Greed Index (press "Fear & Greed") | 111 | **0** | its chips carry no `hover:text-white` variant, so the round-1 rule already turns them navy |
| Global RSI (chart-bar click) | 53 | **0** | none |

**Cause:** the round-1 legibility rule in `portal/src/index.css` (lines 546 to 555) is `[data-panel-surface="light"] [class*="text-white/"]:not([class*=":text-white/"])`: an element whose class list also holds a variant (`hover:text-white`, `hover:bg-white/10`) is excluded by the `:not`, so its white-alpha text stays white on the silver surface.
**Second defect measured in the same read:** an ACTIVE chip (`bg-[hsl(var(--primary))] text-white`, the `1Y` chip of Index Performance, the `90D` chip of Fear and Greed) computes to navy `rgb(10, 23, 51)` on the violet fill, about 2.6:1, because the same rule turns every `text-white` navy (row `DSGN_RBNDV2-W1-S2`).
The AFTER counts and the computed chip colours are read at the drain of order `RV-w-1`.
