# OPAL_RUNNERS W4 — 0824 column census, diffed name-level against 0833 (both masters)

**TO thread:** OPAL_RUNNERS W4 (the deferred 0824 half; gate opened by 0.6.2's terminal count, `060042Z`)
**Author:** `0.4.0_DS_ClientPlatform` · **Measured:** 2026-07-14 ~06:0xZ · **READ-ONLY**
**Sources:** `opal-data-schwab/08242234/bronze/` (source of truth; monolith remap in-flight, additive) ·
`opal-data-assets/schwab/08335338/bronze/` (0.6.2's 3-tier-verified monolith copy)
**Engine (re-runnable):** `data/assets/scripts/analysis/w4_0824_column_census.py` · full name-level
inventory: `OPAL_RUNNERS_W4_COLUMN_INVENTORY_BOTH_MASTERS_20260714.json` (durable, alongside this doc)
**Extraction:** `crs_reader.parse_crs` — a returned file has ALREADY tied to the vendor's T1 (hard-raise
otherwise); partition dates keyed off the PATH (API AsOfDATE), never the filename (the CS{MMDDYY} trap).

---

## 0. Headlines

1. **All 13 shared CRS types are column-IDENTICAL between the masters — name-level, section-level,
   same order, every parse T1-tied.** The C6 parser registry and the V2-8 converter schemas transfer
   between masters with ZERO column work.
2. **The masters' TYPE SETS differ structurally — this is the finding:**
   - **0824 = 17 types: NO `fam`, NO `slm` (zero partitions), plus `rlw` which 0833 lacks.**
   - **0833 = 18 types: `fam`/`slm` present (505/501), no `rlw`.**
   The absence is REAL, not a listing artifact: per-type counts sum to **5,966 EXACTLY** = 0.6.2's
   terminal count (denominator reconciled to zero).
3. **`rlw` (0824-only) parses clean with the EXISTING CRS grammar:** record_type `CBRGLCLW`, one DL
   section **250,201 rows × 75 cols**, T1-tied, 40 weekly partitions 20250905→20260710. It is a weekly
   realized-gain/loss lot table (cadence sibling of rld/rlu/rly). No new reader path needed — it needs
   only REGISTRATION in C6 (an unregistered feed reads visible-UNCONVERTED, per the C6 fences).

## 1. Group-A consequence (the W4 axis)

**0824 carries NO FAM/SLM — so 0824 has no person-name identity carrier in custody bronze.** Its
identity story is the shared `acc`/CRS columns (`master_account_name`, `account_id`, `mstracct_number`,
…) — account identity only, same as 0833's parsed-13. Consequences, stated without adjudication:
- The FAM/SLM person-name identity that closed 0833's Group-A question **does not exist on 0824.**
- Andrew's FAM/SLM naming ruling (~05:5xZ: mechanical/positional + empirical dtypes now, vendor doc
  becomes a meta OVERLAY) and the eventual SDD layout apply to **0833 only**.
- The 49F premise locked at OPAL_RUNNERS sec-4.4 ("0833 + ONE scoped BD advisor dim daily") is
  **unaffected** — it never leaned on 0824 for identity.
- 0.6.2's terminal message described 0824 as "18 types" with fam/slm ~14.5% of the corpus; that
  shape-description matches 0833, not 0824 (his COUNT was exact; the type-roster line transferred from
  the wrong master). Corrected here on the record, RAVC'd to him.

## 2. The measured census (latest partition per type, per-type anchor — never the corpus max)

| type | 0824 (rows @ partition) | 0833 (rows @ partition) | columns | verdict |
|---|---|---|---|---|
| acc | 7,071 @ 0710 | 7,144 @ 0710 | D1×90 | **IDENTICAL** |
| rps | 98,970 @ 0710 | 100,550 @ 0710 | D1×58 + **D2×34** | **IDENTICAL** (D2 present BOTH masters) |
| trn | 9,219 @ 0710 | 9,319 @ 0710 | D1×135 | **IDENTICAL** |
| sec | 1,983 @ 0710 | 2,248 @ 0710 | D1×69 | **IDENTICAL** |
| uln | 271,479 @ 0710 | 273,567 @ 0710 | DL×56 | **IDENTICAL** |
| ult | 193,853 @ 0710 | 196,449 @ 0710 | DL×56 | **IDENTICAL** |
| rld | 481 @ 0710 | 507 @ 0710 | DL×81 | **IDENTICAL** |
| rlu | 287,566 @ 0605 | 289,336 @ 0605 | DL×82 | **IDENTICAL** (monthly cadence — 0605 anchor is the cadence, not staleness) |
| rly | 234,639 @ 0630 | 236,352 @ 0630 | DL×82 | **IDENTICAL** (quarterly) |
| rtu | 114,209 @ 0605 | 114,767 @ 0605 | DT×70 | **IDENTICAL** (monthly) |
| rty | 77,675 @ 0630 | 78,846 @ 0630 | DT×70 | **IDENTICAL** (quarterly) |
| upn | 56,117 @ 0710 | 56,531 @ 0710 | DP×39 | **IDENTICAL** |
| upt | 35,696 @ 0710 | 36,783 @ 0710 | DP×39 | **IDENTICAL** |
| **rlw** | **250,201 @ 0710, DL×75** | **NO PARTITIONS** | — | **0824-ONLY** |
| fam | **NO PARTITIONS** | 7,091 @ 0710 (CSV, 6 fields uniform) | — | **0833-ONLY** |
| slm | **NO PARTITIONS** | 7,091 @ 0710 (CSV, 6 fields uniform) | — | **0833-ONLY** |
| tcf | UNCONVERTED @ 0710 | UNCONVERTED @ 0710 | — | same reader variance both masters (alt-H1) |
| tcfx | UNCONVERTED @ 0710 | UNCONVERTED @ 0710 | — | same (3-header/2-section) |
| tnn | UNCONVERTED @ 0710 | UNCONVERTED @ 0710 | — | same (H01/T01 notice; likely genuinely no data) |

Row-count differences between masters are the BOOKS differing (two real client populations), not a
defect; the diff axis here is COLUMNS, and it is clean. `rps` D2 (account-balance section) confirmed on
BOTH masters — the `read_schwab_raw()` silent-D2-drop remains a both-masters defect (already on the board).

## 3. 0824 corpus shape (denominator reconciliation)

Per-type object counts, live-enumerated: acc 505 · rld 753 · rlu 12 · **rlw 40** · rly 36 · rps 505 ·
rtu 12 · rty 36 · sec 505 · tcf 753 · tcfx 182 · tnn 102 · trn 505 · uln 505 · ult 505 · upn 505 ·
upt 505 = **TOTAL 5,966 = 0.6.2's terminal count, exactly.** Date range 20230712 (REST floor) →
20260710 (correct Friday frontier — 0824 posts ~08:37Z; Monday 07-13 was not vendor-posted at scan
time; trading calendar resolved per NEVER#1). The 257 pre-floor objects remain the separate Glacier
leg (background per Andrew).

## 4. What this feeds (V2 series)

- **V2-5 (bronze close-out certificate):** this census IS the column half of the schwab rows' folder
  census; the type-set divergence (rlw / fam / slm) belongs in the certificate as measured facts.
- **V2-8 (silver converters):** schemas for the 13 shared types are single-sourced (identical columns);
  `rlw` needs a registry entry + pyarrow schema of its own (75 cols, DL); `fam`/`slm` converters are
  0833-only paths, naming now unblocked per Andrew (mechanical/positional; vendor doc = meta overlay).
- **C6 registry:** register `rlw` so it converts instead of reading visible-UNCONVERTED forever.
- **Reader debt unchanged:** tcf (alt-H1) / tcfx (3-header) / tnn (H01 notice) — same three variances,
  both masters, Group-B stakes only.

## 5. Denominators + honesty

19 types × 2 masters attempted; **35 objects read** (34 in the engine run + rlw one-off); every CRS
parse T1-tied or reported UNCONVERTED with its raise text; fam/slm structural control (uniform width)
is WEAKER than T1 and labeled so; nothing sampled; the one absence claim (fam/slm on 0824) is backed by
an exact-to-zero denominator reconciliation, not a failed listing.

*Never summed across masters anywhere in this document — two books, two quantities, per standing rule.*
