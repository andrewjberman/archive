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


---

## APPENDED CORRECTION 2026-08-24 ~22:20Z (author's own, append-only — nothing above is edited)

**The `data_as_of 2026-08-21` in the vintages table above is a SILVER-STAMPED VALUE NOW UNDER INVESTIGATION, not the issuer's own as-of.** `1.0.0_SA_CTO~Z` verified both ends after the 22:00:11Z fire: raw bronze carries `Date=8/24/2026` on every DIVZ/IDVZ row while silver stamps them `2026-08-21` — the issuer's own date is in the bytes and silver discards it (`ETFS_INGEST-Z-S16`, reclassified BLOCKING @`01e16da959`). The platinum artifact I rendered against was published 12:30:47Z from silver as it then stood, so its `data_as_of` inherits that stamping.

**SCOPE OF THIS CORRECTION — ONE LINE, AND I MEASURED IT RATHER THAN ASSERTING IT BROADLY.** In MCP 5321 I said “my AC record's `data_as_of 2026-08-21`” should be read with this caveat. **That was over-broad and wrong about the location.** Measured across both committed records: the AC record contains **zero** platinum `data_as_of` assertions, and every `2026-08-21` in it (4) and in the proof-of-spec (5) is the string `bbg/2026-08-21/` — the **Bloomberg derived-layer S3 partition prefix**, a different tree from a different producer, **correct and untouched by Z-S16**. The assertion exists in exactly **one** place: the vintages row above.

**WHAT THIS DOES NOT TOUCH.** Every finding in this record — the labels rendering correctly, the colour channel reading 0 of 11 across three tables, the `getAssetClassBgColor` fallback mechanism, the colour-law PASS — is independent of what date the rows carry. **No figure above is retracted.** The vintage is annotated, not corrected, because the byte-identical artifact re-check (76,149 B, same ETag, 12:30:47Z) still holds.


---

## SECOND APPEND 2026-08-24 ~22:26Z — THE EVIDENCE SUBSTRATE IS PINNED, because it is about to be overwritten AND versioning has a 14-DAY FUSE

`1.0.0_SA_CTO~Z` ruled (msg 5395) that `ETFS_POSITIONING.TO-5`'s AC3 is discharged by an **ad-hoc QA run** — and named the condition neither seat had stated: **`platinum/etfs/positioning_data.json` is a LIVE SERVED KEY, and an ad-hoc run overwrites production serving in place.** That is the exact object every figure in this record was rendered from.

**WHAT I MEASURED ON HEARING IT, and it changes the remedy:**

| | |
|---|---|
| bucket versioning | **Enabled** — so an overwrite does not destroy the bytes immediately |
| the rendered object's VersionId | `BUS3S19KAalW2aeY6pYNj4MvVjMS4SoU` |
| lifecycle rule `expire-noncurrent-versions-14d` | **`NoncurrentDays: 14`, Enabled, prefix-wide** |

> ⛔ **SO “versioning protects it” IS TRUE FOR FOURTEEN DAYS AND FALSE AFTER.** The moment the ad-hoc run writes, these bytes become NONCURRENT and are **permanently deleted 14 days later.** This record is the baseline the T5-1 build TO is meant to cite, and T5-1 is gated on a field that does not exist yet — **the evidence could evaporate before the build that cites it happens.** Pinning the VersionId alone would have bought 14 days and read as durable.

**THEREFORE THE BYTES THEMSELVES ARE COMMITTED**, not a pointer to them:
`deZ_ETFS_INGEST_T5_PINNED_platinum_positioning_data_20260824T123047Z.json`

Verified identical to the live object, twice — before and after the copy: **md5 `ee2c4a89152261051b9109c93b971dd6` == the live `ETag`, 76,149 bytes == live `ContentLength`.** (Single-part upload, so the ETag IS the md5; that is why the comparison is sound rather than merely suggestive.) Every count in this record — 114 rows, 4 funds, 2 shells, 11 distinct `sub_asset_class` values — is now **re-derivable from a committed artifact** rather than from a key that is scheduled to be overwritten.

**This does not object to the ad-hoc run.** Refreshing a served key is the producer's normal act and NEVER#3 governs MOVING served output, not refreshing it. CTO~Z's notify-before-write condition is the right control and I am not asking for more. **I am removing my own dependency on the timing of it** — once the bytes are committed, it does not matter whether I am told before or after.


---

## THIRD APPEND 2026-08-24 ~22:31Z — THE PIN IS PROVABLY THE PUBLISHED ARTIFACT, verifiable without trusting this seat

A self-taken pin has one weakness: **authorship.** I committed bytes and asserted they were the served object. The producer's own immutable run manifest closes that, and it is checkable by anyone:

```
platinum/etfs/_manifests/2026-08-21/0b2b20a0a2b7.json   (833 B, immutable, one per run)
  producer       etf_positioning_publisher     stage platinum     status published
  generated_utc  2026-08-24T12:30:42Z
  target         opal-data-portal-v2/platinum/etfs/positioning_data.json
  body_bytes     76149          ==  the pin   76149
  body_sha256    ae4c405cc877…  ==  the pin   ae4c405cc877…        MATCH
```

**That hash was recorded BY THE PUBLISHER AT WRITE TIME, in an object this seat did not write and cannot alter.** So the pinned file is not merely *a copy I say is the artifact* — it is **provably the published artifact**, and every figure in this record is re-derivable from bytes whose authenticity does not rest on my word. `2.0.0_SA_COO~Z` independently verified the pin on sha256 (stronger than the md5-vs-ETag check I ran) and `3.0.0_SA_CVO~Z`'s cited ETag reproduces from it — three seats, three oracles, one artifact.

⛔ **AND A CORRECTION TO THE PRESERVATION ACCOUNTING, because the tidy version is wrong.** It was proposed that pin + versioning + manifests are *three independent preservation paths*, i.e. that an overwrite is recoverable even without the pin. **Measured: it is ONE preservation path, ONE 14-day lease, and ONE verifier.** The manifest is **833 bytes** — it records a HASH of the artifact, not the artifact, so it can PROVE a copy authentic but cannot PRODUCE one. Versioning expires per the fuse above. **Only the committed bytes reconstruct.** The manifests are load-bearing as the verification oracle, which is a different job from preservation and does not substitute for it.

*Identified as this artifact's manifest by its timestamp: `s3 ls` renders LOCAL, so `08:30:49` is `12:30:49Z` — two seconds after the artifact's own write. Reading it in the wrong plane would have made it look like a different day's run.*


---

## FOURTH APPEND 2026-08-24 ~22:52Z — MY DECLARED EXCLUSION IS NOW CLOSED, AND THE ANSWER IS THE EXACT INVERSE OF ETF MODE

The AC record declared UNMEASURED: *“whether the MODELS artifact's vocabulary can reach the shared tables — I could not locate a Models `positioning_data.json` under `opal-data-portal-v2/platinum/` or `opal-data-assets/json/`.”* **`1.0.0_SA_CTO~Z`'s leaf census found it in a tree I had not searched** — `opal-data-portal-v2/**json**/positioning/` — one of THREE live keys sharing the leaf `positioning_data.json` (the third, `positioning/positioning_data.json`, is ~244 days old; Rule 25's same-leaf twins hazard, recorded not dispositioned). **Measured at this seat rather than relayed:**

```
json/positioning/positioning_data.json   8,133 B STORED, ContentEncoding: gzip -> 73,458 B decompressed
  110 rows carrying sub_asset_class, 10 distinct — ALL Models-side segments
  US Large Cap 26 · Ultra Short Duration 25 · Short Duration 14 · Developed 14 · High Yield 9
  Intermediate 7 · Structured Credit 4 · EM 4 · Volatility 4 · US Mid Cap 3
```

| table | covers MODELS | covers ETF (from §3 above) |
|---|---|---|
| `SUB_ASSET_CLASS_COLORS` | **10 of 10** | 0 of 11 |
| `SUB_ASSET_COLORS` | **10 of 10** | 0 of 11 |
| `SUB_ASSET_CLASS_DISPLAY_MAP` | 7 of 10 | 0 of 11 |

> **THE COLOUR TABLES ARE 100% LOAD-BEARING FOR MODELS AND 0% FOR ETF.** They were never generic — they are the Models vocabulary, and ETF mode is the tenant that shares them.

**This SHARPENS `AC3` from a reasoned warning into a measured one.** §3 noted that `SUB_ASSET_CLASS_COLORS` membership is CONTROL FLOW — `getSubAssetClass` returns the normalized value *only if the key exists*. That branch currently succeeds for **every one of the 10 live Models values**. So `AC6` option (a) would mean adding ~24 GICS keys to a table in which **every existing key is live for Models**, on a page whose byte-identical rendering is a sovereign constraint. **Option (b) avoids touching it at all** — which is a stronger argument for the determination than the one I made, and I did not have it when I made it.

*The `DISPLAY_MAP`'s 7-of-10 is NOT a gap: the three absent values (`Developed`, `EM`, `Intermediate`) are the already-SHORTENED forms. That map goes long→short (`International Developed`→`Developed`), so a value already in short form needs no entry. Counting it as a miss would have been the map working correctly, mis-read as a defect.*

⚠ **And the artifacts are not symmetric in transport:** the Models key is stored **gzipped** (`ContentEncoding: gzip`, 8,133 B stored vs 73,458 B decompressed) while the ETF key is stored plain (76,149 B). A byte-size comparison between the two — 8 KB vs 76 KB — invites the conclusion that Models carries a tenth the data. **It carries 110 rows to ETF's 114.** Noted because a size ratio is exactly the kind of number that gets quoted.
