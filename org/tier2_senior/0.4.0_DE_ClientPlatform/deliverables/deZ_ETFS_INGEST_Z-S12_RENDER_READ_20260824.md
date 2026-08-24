# ETFS_INGEST T5 — the render read: site-Z placement proof + `Z-S12` (`Z-S-G` alias) answered

**Seat:** `0.4.0_DE_ClientPlatform~Z` · **Date:** 2026-08-24 · **Class:** EVIDENCE RECORD (not a build; no TO consumed)
**Authorized by:** `1.0.0_SA_CTO~Z` msg 5045 — *"an EVIDENCE record is not a build and needs no TO; it is what Andrew points at and what the T5-1 TO cites as its baseline."*
**Status of T5-1:** NOT STARTED. Awaiting `2.0.0_SA_COO~Z` TO + GO.

---

## Vintages — every claim below is bound to these

| plane | vintage |
|---|---|
| portal | `d43b88c5` (= `origin/DEV` at render time), branch `DEV`, tree clean |
| PRD | `docs/architecture/ETFS_INGEST_PRD.md` @ `e61d75450a` (working tree) |
| platinum artifact | `s3://opal-data-portal-v2/platinum/etfs/positioning_data.json` — 76,149 B, `LastModified 2026-08-24T12:30:47Z` (UTC plane, `s3api`), `data_as_of 2026-08-21` |
| workspace | branch `SITEZ` |

Negative control on the artifact read: `platinum/etfs/zzz_no_such_key_9999.json` → **404**. The instrument discriminates.

---

## 1. Placement condition — **PASS**, by EXECUTION

`0.0.0_AB_MSTR~Z` measured PRESENCE and bounded it explicitly: *"deps EXIST is not that a dev server RUNS or that a render SUCCEEDS."* That bound is discharged here.

| check | result |
|---|---|
| `bun` | resolved **from PATH** (winget path under this profile) — **not** the CLAUDE.md hardcode |
| vite dev server | **booted**, v7.3.5, *"ready in 971 ms"*, HTTP **200** on `:5175` |
| headless renders | **3 succeeded** (`scripts/ui-smoke.mjs`, system Edge, fresh profile) |
| `LOC` | `/positioning` on all three — no silent bounce to `/login` |
| canvas | `rgb(195, 202, 218)` — the silver the colour law expects |
| interaction | `CLICKED: ETFs` — the flip actually flipped and the page re-rendered |

**DE-class placement = SITE Z.** No laptop leg. (Ruled closed by `1.0.0_SA_CTO~Z` 5045.)

> ⚠ **CLAUDE.md's Portal section names bun at `/c/Users/AndrewBerman/.bun/bin/bun`. That path does not exist on this box.** Independently re-confirmed at this seat after `0.0.0_AB_MSTR~Z` first surfaced it. A seat following the law file literally concludes *"bun is not installed on site Z"* — false, and it is the conclusion that would have sent DE-class to the laptop. **Surfaced to CVO~Z's channel, NOT fixed** (BASE_EXEC lane, non-D4).

---

## 2. ⚠ The stale-tree disclosure — read this before the findings, because it changed the measurement

The site-Z portal checkout was at `483b896c` — **13 commits behind `origin/DEV`**, and **4 of those 13 touch `src/pages/Positioning/`**: `ee90fa8e` (the Models↔ETFs flip itself), `a60b558f`, `a7ff6dd4`, `d43b88c5` — all `ETFS_POSITIONING.TO-3`.

**So the first render was of a tree with no flip in it.** Stopping there would have produced *"the ETF flip does not exist on portal DEV"* — confident, well-formed, **entirely false**, against a PRD cell that is correct. A stale tree does not announce itself.

Two of my own intermediate reads were wrong; both were caught before they reached anyone:

- `git -C portal rev-parse origin/DEV` read **pre-fetch** returned the stale ref and looked like "up to date".
- `git branch -a --contains <sha>` printing `origin/DEV` proves **containment, not equality**. I inferred `origin/DEV == 9580e18b` from it and was wrong by a further 10 commits.

**Remedy applied:** `git -C portal merge --ff-only origin/DEV`, after checking all three preconditions — tree clean (`status --porcelain` = 0), deps unchanged (0 files in `package.json`/`bun.lock` across the 13), true fast-forward (`merge-base --is-ancestor`). Stayed on `DEV` throughout (Rule 19). No rebase, no merge commit, nothing discarded. **RATIFIED** by `1.0.0_SA_CTO~Z` 5045.

**Consequence I could not see from inside the submodule** (surfaced by `0.0.0_AB_MSTR~Z` 5049): the parent repo's **gitlink is now dirty** — committed `9580e18b8f` vs tree `d43b88c5`. That gitlink was *already* behind before I touched anything; the sync exposed it rather than creating it. Advancing it is a workspace commit and is **not mine** (DT lane / integrator). **Live hazard for every seat on this tree: a broad pathspec can sweep ` M portal` into an unrelated commit and silently advance the workspace's portal declaration. Scope your pathspecs.**

---

## 3. `Z-S12` (`Z-S-G`, COO~Z alias) — ANSWERED BY LOOKING

`3.0.0_SA_CVO~Z` filed this as a **QUESTION, not a defect**: *"whether that renders wrong is UNMEASURED; it needs a screenshot, not a grep."* Both halves of that were right.

### (a) Today, no fixture — `deZ_ETFS_INGEST_T5_render_etfs-today_20260824.png`

The flip works; header subtitle flips to *"across TrueShares ETFs."*; the four books render as DIVZ / IDVZ / PFDE / PFOE. The page shows the cause-agnostic notice: *"ETF positioning data is not available yet. This view is being rolled out and its data is not published yet…"* Both panels: *"No holdings data available."*

**So today the lookup miss is UNREACHABLE.** Nothing renders, so nothing can render wrong. The route is still undeployed (`public-data-router` + the `qualified_arn` pin are committed-not-deployed, per TO-3's own status). A verdict taken today would have read "harmless" — **for the wrong reason.**

### (b) With the REAL artifact as the fixture — `deZ_ETFS_INGEST_T5_render_etfs-fixtured_20260824.png`

No fabricated fixture: the live platinum artifact was pulled and used verbatim.

| fund | holdings | status |
|---|---|---|
| DIVZ | 0 | `book_only` shell |
| IDVZ | 0 | `book_only` shell |
| PFDE | 90 | `full` |
| PFOE | 24 | `full` |
| **total** | **114** | |

11 distinct non-null `sub_asset_class` values = **10 GICS sector names + `Cash & Cash Equivalents`**; **1 row carries NULL**. DIVZ/IDVZ rendering as hollow placeholder bars is **correct** — shells, not fabricated data (F2 undeployed).

**The two halves of the answer point opposite ways:**

**✅ THE LABELS ARE FINE.** Every GICS name renders in full, correctly spelled, in the SUB ASSET column — *Information Technology, Consumer Discretionary, Communication Services, Financials, Health Care, Industrials, Energy*. **Nothing is mislabelled.** The display-map miss is harmless because the fallback chain ends in `return apiSubAssetClass` — the raw value survives to the page.

**❌ THE COLOUR CHANNEL IS DEAD.** Re-derived independently at this seat; `3.0.0_SA_CVO~Z`'s figure reproduces exactly:

| table | site | keys | covers |
|---|---|---|---|
| `SUB_ASSET_CLASS_COLORS` | `pages/Attribution/constants/holdings-shared.tsx:71` | 21 | **0 of 11** |
| `SUB_ASSET_COLORS` | `lib/chartColors.ts:279` | 21 | **0 of 11** |
| `SUB_ASSET_CLASS_DISPLAY_MAP` | `pages/Positioning/tabs/HoldingsTab.tsx:136` | 13 | **0 of 11** |

**Mechanism, source-confirmed** — `getAssetClassBgColor`, `holdings-shared.tsx:99-104 @ d43b88c5`:

```ts
export function getAssetClassBgColor(assetClass: string, subAssetClass?: string): string {
  if (subAssetClass && SUB_ASSET_CLASS_COLORS[subAssetClass]) {
    return SUB_ASSET_CLASS_COLORS[subAssetClass]
  }
  return ASSET_CLASS_COLORS[assetClass] || PALETTE.gray500
}
```

With 0/11 coverage, **every one of the 110 equity rows falls to the same `ASSET_CLASS.equity` fill.** Visible result: the SUB ASSET column is one flat blue top to bottom, and the Portfolio Composition treemap paints every constituent tile the same blue. In Models mode that colour is the **discriminating** channel (Large / Mid / Small / Developed / EM each get their own shade). In ETF mode it carries **zero information**.

> **So it does not render WRONG. It renders UNDIFFERENTIATED.** That is a third thing neither prediction allowed, and it is why the screenshot was the right instrument: the lookup census predicted breakage, the fallback chain predicted harmlessness, and the page shows correct text with a dead colour dimension. **The census answered the DATA plane; only the render answered the RENDER plane.**

### Colour law (silver canvas) — **PASS**

No light text or light buttons on the canvas. The unavailable notice is dark-red-on-light-red at canvas level — correct. The flip's inactive `MODELS` is dark text on silver; the active pill carries its own accent fill, which is what makes its white text legal. All content sits inside dark `Panel`s.

---

## 4. Consequence for C3 / T5-1 — **T5-1 is TWO halves**

C3 is ruled: sub-categories = `GICS_INDUSTRY_GROUP_NAME`, one level finer, **24 values**.

**Those 24 will miss the same three tables, exactly as the 11 do now.** A T5-1 build that only swaps the FIELD inherits this dead colour channel at **finer grain** — 24 undifferentiated values instead of 11, i.e. **strictly worse, because the finer the axis the more the colour channel was carrying.**

So T5-1 is:

1. the field swap to `GICS_INDUSTRY_GROUP_NAME` (C3, ruled); **and**
2. a **colour/vocabulary act** keyed on the 24 new values.

Half (2) is a **Rule 24 authoring event** — values proposed to an existing axis, requiring the four-postulate record + a token-hygiene census (per the 2026-08-20 widening: proposing/adopting values is itself an authoring act). **It is not something this seat mints inside the swap.** Celled by `2.0.0_SA_COO~Z` per CTO~Z 5045.

---

## 5. Bounds — what was NOT measured

- **PRE-DEPLOY read.** The fixture is the real artifact, so this is what the page will do when the route lands — but the route is **not deployed**, so this is **not** a live-serving observation and must not be cited as one.
- Not exercised: the Performance view, Expand Details, the PFOE/IDVZ/DIVZ tabs, or any DIVZ/IDVZ row rendering (zero rows — structurally unmeasurable until F2 deploys).
- The **1 NULL** `sub_asset_class` row (of 114) — not isolated. Flagged, not chased.
- **0 of 108** constituent tickers collide with `ETF_CATEGORIZATION`'s 36 keys, so the `getETFCategory` fallback — which *could* have returned a MODEL SEGMENT for a stock — does not fire on today's data. **That is a measured absence on today's universe, not a structural guarantee**; a future constituent named like a universe ETF would trip it.
- My chosen positive control for that ticker parse (`SPY`/`AGG`) was **absent from the file**, so it never fired. The parse is corroborated by the 36 recovered keys being plainly ETF tickers (`BIV`, `BSCQ`, `DIVZ`…), **not** by the control I picked. Weaker evidence than intended — stated rather than presented as clean.

---

## 6. Artifacts

| file | what it shows |
|---|---|
| `deZ_ETFS_INGEST_T5_render_models-empty_20260824.png` | Models mode, empty backend — the baseline render that proved the toolchain |
| `deZ_ETFS_INGEST_T5_render_etfs-today_20260824.png` | ETF mode **as it stands today** — flip works, cause-agnostic unavailable notice, zero holdings |
| `deZ_ETFS_INGEST_T5_render_etfs-fixtured_20260824.png` | ETF mode with the **real** platinum artifact — the render that answers `Z-S12` |

RAVC: reported 5041 → validated `1.0.0_SA_CTO~Z` 5045, accepted `0.0.0_AB_MSTR~Z` 5049.
