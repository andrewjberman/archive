# A light -- the fixture (DEC-1), copied from the board so a worker needs no artifact tool

**Source:** the "A light - Opal-led" artboard `project/Main.dc.html` of https://claude.ai/artifact/WVqCCv8SPkiBz8byz4ZpLh
(canvas "DSGN_RBNDV2 light mode", version 1792034242-e102, read 2026-10-15 by `2.0.0_SA_COO~RB`; sha256 of the board file
`2603251772b82750580f16fabf8015b5318d6accfcff8feb50a60cf3573f2e39`). Andrew edited this board; its values are the spec.
The board's sidebar ground and `<main>` ground are both `#eaeaf7`; panels are white. Fonts: Lato 400/700 (the portal already
ships Lato; nothing new loads). No shadow anywhere.

## Tokens (the board's literals, one meaning each)

| token (board literal) | value | role |
|---|---|---|
| ground | `#EAEAF7` | sidebar background AND page background behind the panels |
| panel surface | `#FFFFFF` | every panel and modal body |
| panel edge | `#C4CBDB` | the 1px border of a panel; the sidebar's right border; axis lines |
| rule | `#E3E7EF` | hairline between a panel's header, body and caption; sidebar section dividers |
| row rule | `#EEF1F6` | table-row hairline inside a panel |
| ink | `#0A1733` | titles, active nav text, panel text |
| ink-2 | `#163372` | body text, nav labels' eyebrow ink, links |
| ink-3 | `#4A5878` | inactive nav text, segmented-control text |
| quiet | `#6B7590` | panel number ("01"), source caption |
| accent | `#5F3BE3` | the 2px underline under an eyebrow title, under the active nav item and the active segment |
| bar | `#C9D1E3` | plain bar fill inside a panel |

## The panel ("A light"), verbatim

```css
.eyebrow{display:inline-block;font-size:11px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;padding-bottom:4px;border-bottom:2px solid #5F3BE3;color:#163372}
.pnl{background:#FFFFFF;border:1px solid #C4CBDB;color:#0A1733}
.pnl-h{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:10px 16px;padding:22px 30px 16px;border-bottom:1px solid #E3E7EF}
.pnl-t{display:flex;align-items:baseline;gap:12px;margin:0}
.num{font-size:12px;color:#6B7590;font-weight:400;letter-spacing:0.04em}
.pnl-b{padding:24px 30px}
.pnl-f{margin:0 30px;padding:10px 0 14px;border-top:1px solid #E3E7EF;font-size:11px;letter-spacing:0.08em;text-transform:uppercase;color:#6B7590}
.seg{display:flex;gap:18px;font-size:12px;color:#4A5878}
.seg .on{color:#0A1733;font-weight:700;border-bottom:2px solid #5F3BE3;padding-bottom:3px}
```

Structure: `section.pnl > .pnl-h (h2.pnl-t > span.num + span.eyebrow, then actions on the right) + .pnl-b + .pnl-f ("Source  <name>")`.
Square corners (the board sets no radius; the portal's radius ladder 2/3/4px, `portal/DESIGN.md` C11, stands for controls inside).

## The sidebar ("A light"), verbatim

```css
.nav-a{display:block;padding:7px 0;font-size:14px;color:#4A5878;text-decoration:none}
.nav-a:hover{color:#0A1733}
.nav-on{color:#0A1733;font-weight:700}
.nav-on span{border-bottom:2px solid #5F3BE3;padding-bottom:3px}
```

`<nav>`: width 232px (min 200), `border-right:1px solid #C4CBDB`, `background:#EAEAF7`, `padding:26px 24px 20px`, column, `gap:22px`.
Wordmark top: "opal" 30px/400 letter-spacing -0.01em over "CAPITAL" 8px letter-spacing 0.42em. Each section: an `.eyebrow` label
(Insights / Analysis / Tools) above its links, sections separated by `border-top:1px solid #E3E7EF`. Foot: a 30px square (1px
`#163372` border, no radius, no round avatar) with the user's initial, and the user's name over their role in 12px.
No icons, no filled active tile: the current page is the bold link with the violet underline.

## What the board does NOT settle (the builder decides inside the contract, and says so)

- The collapsed (48px icon) state of the sidebar: the board shows only the expanded rail. Behaviour stays unchanged
  (C-SIDEBAR): keep the collapse and keep the current icons for the collapsed rail only.
- Heat maps: the board has none. C-HEAT: white to silver; the silver end is chosen so the ends differ at a glance on a white panel.
