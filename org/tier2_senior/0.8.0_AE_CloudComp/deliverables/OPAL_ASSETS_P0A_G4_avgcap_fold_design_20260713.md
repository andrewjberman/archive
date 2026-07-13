# OPAL_ASSETS P0-A (re-scoped) -- G4 avgcap-fold DESIGN

**Author:** `0.8.0_AE_CloudComp` (sole lane, Andrew-direct) | **Date:** 2026-07-13
**For:** `2.0.0_SA_COO` (dispatch) | **CC (design align):** `0.7.0_AE_CloudOps~A` (base table+emitter owner), `1.0.0_SA_CTO~B` (schema arch-gate), `0.4.0_DS_ClientPlatform` (P0-B / avgcap lane)
**TO:** `OPAL_ASSETS.P0-A` (`b9fafa92c`), amended by COO re-scope 034836Z: **no parallel table** -- `0.7.0~A` owns the base table+emitter+backfill; my half = **G4 (fold per-partner 49F ETF ownership + `partial` flag) + G5 convergence**, extending ~A's table.

> **archetype:** DIAGNOSE (grounded the fold source + sovereign boundary; design output)

---

## 0. Headline

The G4 **interim** fold is **fully Opal-side** -- it consumes the already-served `opal-data-etfs/daily/{partner}/{date}.json` series (my own bucket), **zero bd/RPS/Schwab read by me**. My TO invariant-1 (`STRICTLY OPAL-SIDE, STOP-and-flag on a needed sovereign read`) does **not** trip for the interim fold. The both-masters (`08335338`) side is P2/G2 (sovereign, `~A`'s pull), not the interim.

## 1. The fold SOURCE -- grounded (not what the PRD name implies)

The PRD (sec 4 G4) names `avgcap_bd_rps_recon` for the fold. Grounding that name:

- **`data/etfs/scripts/gold/avgcap_bd_rps_recon.py`** (DS-authored, ETFS_AVGCAP.W1 AC#3) is a **recon/diagnostic** that reads `opal-data-bd` (RPS silver + bd `gold/canonical/holdings`) + `opal-data-schwab` (`03_silver/account_xref`, master `0008242234`) **on demand** and **prints a summary** (`--out /tmp/recon.json`). It is a **sovereign-reading tool, NOT a served artifact.** Do not read it as the daily fold source.
- The **already-served Opal-side** per-partner ETF-ownership series is **`opal-data-etfs/daily/{partner}/{date}.json`** (ETFS_SETUP). Live-verified shape (49financial/2026-06-24):
  ```
  [{schema_version, partner, date, etf_ticker, ownership_value, account_count, source_artifact, source_as_of}, ...]
  ```
  Partners present: **49financial** (frozen 2026-06-24 -- ad-hoc Schwab cadence per ETFS_AVGCAP D6), **inflection** (FRESH 2026-07-10), **cottonwood**. Monthly rollup at `opal-data-etfs/monthly/{YYYY-MM}.json` (separate AVGCAP deliverable, not the daily-record fold source).

**Sovereign boundary (clean for interim):** consuming `opal-data-etfs` is an Opal-side read of my own bucket -- parallel to reading the mdpf served output. The bd/RPS read that *built* the 49F series happened upstream in ETFS_SETUP/DS's cadence (last 06-24), not here. A **fresher** 49F number requires DS/ETFS_SETUP to re-run its 49F producer (a sovereign-scoped bd/RPS read = **DS lane**) -- I surface to DS, I do not self-run.

## 2. How the `partial` flag lands

49F's `source_artifact` = `opal-data-bd/schwab/silver/rps/date=YYYYMMDD` = the **`08242234` RPS book only**. D1 (PRD 3c, confirmed SPLIT) proved 49F Opal-ETF custody **spans both masters** (`08242234` RPS + `08335338` CBUGL, ~22K position rows). So avgcap-only = **`08242234`-only = a real undercount**. Therefore each 49F held entry carries:

```
partial_flag = "08242234-only"   # derived directly from source_artifact
```

Flag is **REMOVED** when the both-masters dedup lands (P2/G2 -- `~A`'s `08335338` CBUGL pull, deduped by account). **Flag-removal = G4 DONE** (PRD AC4; a missing flag during interim = a silent undercount = the failure AC4 falsifies).

## 3. The fold SHAPE (into `~A`'s ETF cohort rows -- align w/ `~A` + CTO~B)

Each `etf_{divz,idvz,pfoe,pfde}` cohort row gains a `held_by_partner` LIST attribute (the G6 stamp's ETF-ownership dimension promoted to the bucket):

```
held_by_partner: [
  { partner,
    held_value,                       # from opal-data-etfs/daily[etf_ticker].ownership_value
    account_count,
    ownership_pct,                    # held_value / etf_total_net_assets, 6dp (PRD MDPF_OWNTS precision)
    source_master(s): [ ... ],        # LIST from day 1 (CTO~B forward-compat)
    as_of,                            # the series' OWN source_as_of -- NEVER a cross-partner min
    state,                            # fresh | rolled_forward | missing
    partial_flag                      # "08242234-only" during interim; ABSENT once both-masters lands
  }, ...
]
```

Per-partner today:
| partner | held source | state | as_of | source_master(s) | partial_flag |
|---|---|---|---|---|---|
| 49financial | `opal-data-etfs/daily/49financial` | `rolled_forward` | 2026-06-24 | `[08242234]` | `"08242234-only"` |
| inflection | see open pt 1 | `fresh` | 2026-07-10 | `[]` (fund/Eclipse) | (none) |
| cottonwood | `opal-data-etfs/daily/cottonwood` (one-way, PRD 3e) | per own vintage | own | `[]` | (none) |

Honest-state rules match `~A`'s G6 contract exactly: `as_of` = own-field; a `rolled_forward` held value is never presented `fresh`; a `partial` interim value is always flagged.

## 4. Open coordination points (non-blocking)

1. **Inflection double-source:** mdpf `etf_decomposition[].held_by_partner` already carries inflection (target_weight estimate + WS-D.2 RPS override). Pick ONE canonical source for inflection's held to avoid double-source on `~A`'s table. **Recommend `opal-data-etfs/daily/inflection`** (the measured series) as canonical; align with `~A`.
2. **Grain = DAILY** (`opal-data-etfs/daily`). Confirm the monthly rollup is out of scope for the daily-record fold.
3. **49F freshness** past 06-24 = DS/ETFS_SETUP re-run (sovereign-scoped, DS lane). Interim record honestly reads `rolled_forward@06-24`.

## 5. G5 convergence (forward-look, post-G2)

At P2, cohort-8 (`49f_schwab_custody`) flips `incomplete`->present when `~A`'s `08335338` CBUGL pull lands; the 49F `held_by_partner` `partial_flag` drops as the both-masters account-deduped ownership replaces `08242234`-only. The row shape above is **forward-compatible** (LIST source_master, per-entry state/as_of/flag) so neither the table nor the row schema migrates when P2 lands -- the values change, the shape does not. This satisfies never-widen at the row level.

## 6. Compiler Tools

| Tool | Call | Result |
|---|---|---|
| `comp-which` | "what serves the mdpf aggregate_aua daily output" | near-tie route (adapter-audit/blast/parity); ran the direct source grounding instead |
| `comp-blast` | `mdpf_aggregate_aua` | no EXTRACTED edges (lower bound; dynamic-key consumers not edged) -- grounded served path at source |
| `comp-glob` | `**/*avgcap*`, `**/*rps_recon*` | located `avgcap_bd_rps_recon.py` (etfs gold) + `ETFS_AVGCAP.md`; 972 sovereign-held paths correctly excluded |

Raw `aws s3 ls`/`cp` on `opal-data-etfs` (my own bucket) + `opal-data-portal-v2` served partition = operational/Opal-side reads (free per COMPRAIL); no sovereign bucket touched.

## 7. Status

Design **done, drop-in-ready.** Implementation **blocked only on `~A`'s table handoff** (table ARN + GSI ARN + emitter path + final CTO~B-ratified row shape). Any write I add rides its own **Rule-22a** `simulate-principal-policy` on the exact table+GSI ARN + a positive control before I trust a PutItem. No parallel TF, no sovereign read.
