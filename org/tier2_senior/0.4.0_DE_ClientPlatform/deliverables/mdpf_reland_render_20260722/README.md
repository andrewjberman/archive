# MDPF_REVAMP.S5 RE-LAND — render evidence (CTO visual-confirm set)

**FE sha:** `6287847c625a001cfca4fde7c7b430167a103fb0` (portal DEV)
**Data:** re-land frozen-9, global aggregate ETag `c27e1f37` (all 9 md5-verified)
**Gates on that sha:** Surface-Check Gate `29896944168` SUCCESS · CI Build & Validate `29896944203` SUCCESS · `tsc -b --noEmit` clean

## What to look at

| file | check |
|---|---|
| `global_value__BEFORE_129edad5_shows_6_gaps.png` | **BEFORE** — Daily AUA shows the six drop-to-zero collapses (honest-None dates rendered as gaps) |
| `global_value__AFTER_6287847c.png` | **AFTER** — Daily AUA **continuous**; year-disambiguated axis ("Nov 29, 24" … "Jul 20, 26"); 21 monotonic bars; no false-dip |
| `global_count__AFTER_6287847c.png` | Count mode: continuous daily, 21 monotonic bars, Total Holdings 7,739 |
| `inflection_value__AFTER_6287847c.png` | **Pre-onset flat-grey INTACT** (Jul'25→Apr'26 grey), model onset ~2026-05-13, continuous to 07-20 |
| `inflection_count__AFTER_6287847c.png` | Count: honest pre-onset zero, onset ~2026-05, continuous |
| `49f_value__AFTER_6287847c.png` / `49f_count__AFTER_6287847c.png` | 49F unaffected (per-firm branch untouched) |

## The fix being confirmed
Global Non-Model band is set to `null` on dates declared in `meta.honest_none.total_none_dates`
(producer-declared, CVO lineage-verified), so the existing all-plotted-null row filter drops the
row and the series **bridges**. Previously `getNonModelAumForDate` roll-forwarded a value that was
never null, making the row partial-null → it survived the filter → collapsed to the grey band.

**Scope:** GLOBAL only. Per-firm reads `non_model_aua` directly (already bridged). Inflection's
pre-onset flat-grey is REAL zeros (`model_aua = 0.0` + real non-model), not nulls — structurally
unaffected. Legacy carries no marker → empty set → provable no-op.

## NOT a substitute for the live gate
These are DEV-harness (route-injected fixture) renders — **necessary, not sufficient**. The HARD
verify-before-serve gate is the post-promote render against the real served build on
opalinvest.dev. Rollback stays armed until that + CVO cycle-1 read clean.
