# ADVI_STITCH.TO-A1-DS — AC1 / `STI-d-0` — RE-GROUNDING AT A PINNED VINTAGE

**Cell:** `STI-d-0` · **Criterion:** `STIA1DS-AC1` · **Grounding class:** LIVE STATE
**Seat:** `0.4.0_DS_ClientPlatform~Q` · **Issuer:** `2.0.0_SA_COO` (dispatch 71357)
**PINNED VINTAGE (UTC):** `2026-08-25T20:47:26Z` .. `2026-08-25T20:55:23Z`
**Instrument:** `aws s3 ls --recursive --summarize` (CLI auto-paginated, materialised set counted —
`--no-paginate` deliberately NOT used) and `aws s3api list-object-versions`.

`STI-d-0` exists because the partitions move daily and a Phase-A census that opens on a stale count
inherits its staleness silently. Every figure below is re-measured, printed beside the run's, and
every difference is named.

---

## 1. THE RE-GROUND TABLE — 8 figures

| # | figure | run (inherited) | measured @ pinned vintage | delta |
|---|---|---|---|---|
| J1a | `opal-data-bd` top-level prefixes | 30 | **30** (0 top-level objects) | **0 — HOLDS** |
| J1b | in-territory prefixes | 4 of 30 | **4 of 30** | **0 — HOLDS** |
| J3a | `backfill_v2/` | 292 keys / 2.47 GB | **292** / 2,467,990,218 B | **0 keys — HOLDS** |
| J3b | `forwardfill_v2/` | 636 keys / 5.24 GB | **640** / 5,244,616,142 B | **+4 keys** |
| J4 | `silver/` (legacy silver) | 7,913 keys / 2.79 GB | **7,916** / 2,788,114,373 B | **+3 keys** |
| J5 | `gold/` (legacy gold) | 73,526 keys / 32.83 GB | **73,563** / 32,832,890,102 B | **+37 keys** |
| b-3 | frozen series × dates | 3 × ~2,424 | **2,424 / 2,424 / 2,425** | **0 — HOLDS exactly** |
| b-5 | migration size | ~8,800 obj / ~13 GB | **16,121 obj / 12.10 GiB** | **+7,321 obj (+83%)** — s.4 |

**Three of eight figures moved.** All three moved UP, none moved down. The direction matters: the
source planes gained keys, so a copy sized on the run's numbers would have under-copied.

---

## 2. WHY THE THREE MOVED — the source planes are NOT frozen

| plane | newest LastModified | keys written in last 7d | reading |
|---|---|---|---|
| `backfill_v2/` | 2026-04-14 15:48:50 | **0 of 292** | genuinely DORMANT (Rule 25 clear of the 90d bar) |
| `forwardfill_v2/` | 2026-08-24 20:09:25 | **52 of 640** | **LIVE — still receiving daily** |
| `silver/` | 2026-08-25 10:09:36 | **76 of 7,916** | **LIVE** |
| `gold/` | 2026-08-25 08:49:30 | **53,559 of 73,563** | **LIVE, republished at scale** |

**Consequence for the oracles that say "a census equal to the source census"** (`STI-a-1`, `a-2`,
`a-3`, AC3, AC4): the source census is a moving target for three of four planes. Equality is only
well-defined against a **PINNED MANIFEST**, not against a live re-list. Every census I emit will
name its vintage, and the landed-vs-source comparison will be against the manifest captured at copy
time — not a fresh `ls` at verification time, which would report a false mismatch on any day the
producers ran between the two reads.

---

## 3. CONTENT vs TIMESTAMP — and a correction to my own first read

⛔ **A LastModified sweep answers REPUBLISH, never CHANGE.** `gold/` showing 53,559 of 73,563 keys
touched in 7 days does **not** mean the data changed. The discriminating instrument is the ETag
across retained versions, which this bucket supports (`get-bucket-versioning` → **Enabled**).

**MY FIRST READ WAS WRONG AND I AM CORRECTING IT ON THE FACE.** I sampled ONE key —
`gold/canonical/performance/2020-01-02.parquet` — found 10 versions across 6 days at an identical
ETag (`ccaf5016b68d7a13e612864707f318cb`, 15,455 B every time), and concluded the republish was
byte-identical re-emission with stable content. **That key is an outlier and the conclusion does not
generalise.** One key is not a population; the coverage pass overturned it.

### 3.1 Distinct-ETag count by partition YEAR — `gold/canonical/performance`

Stratified sample, 4 keys per year, **28 of 2,424 keys sampled** (denominator printed):

| partition year | partitions in year | sampled | mean distinct ETags | max |
|---|---|---|---|---|
| 2020 | 365 | 4 | **2.5** | 3 |
| 2021 | 365 | 4 | **3.0** | 3 |
| 2022 | 365 | 4 | **4.8** | 6 |
| 2023 | 365 | 4 | **8.0** | 9 |
| 2024 | 366 | 4 | **11.2** | 12 |
| 2025 | 365 | 4 | **12.0** | 12 |
| 2026 | 233 | 4 | **9.5** | 12 |

**NO partition year is content-stable — not even 2020.** Restatement volume rises monotonically with
recency through 2025. `nna` tracks `performance` closely on the same sample. `holdings` is the
opposite: historical partitions carry **1 version, 1 ETag** — genuinely write-once.

⚠ **These counts are a FLOOR, not a total.** The retained version window tops out at 29 versions, so
a partition restated more times than the window retains reports only what survives. I am not quoting
lifetime restatement counts and neither should any consumer of this file.

### 3.2 The three series are in TWO different states

| series | behaviour | Rule 25 kind |
|---|---|---|
| `canonical/holdings` | write-once; history immutable | **CLOSED-PERIOD-IMMUTABLE** (true of the source) |
| `canonical/performance` | history restated, 2.5→12 distinct ETags by year | **revised — behaves LONG-TTL-LIVE** |
| `canonical/nna` | same as performance | **revised — behaves LONG-TTL-LIVE** |

**Rule 24(iv), state coherence: name the state axis, then ask whether ONE remedy moves every value
together. Here it does not.** The TO/decomp applies one remedy — freeze all three as
closed-period-immutable reference — to three values sitting in two states.

---

## 4. THE `b-5` OBJECT COUNT IS UNDERSTATED BY 83%, AND THE BYTES HID IT

| component | objects | bytes |
|---|---|---|
| `bronze_legacy` sources (`backfill_v2` + `forwardfill_v2`) | 932 | 7.18 GiB |
| `silver_legacy` source (`silver`) | 7,916 | 2.60 GiB |
| gold reference (3 canonical series) | 7,273 | 2.32 GiB |
| **TOTAL** | **16,121** | **12.10 GiB** |

- decomp `STI-b-5` / AC13 state **~8,800 objects / ~13 GB**.
- `292 + 636 + 7,913 = 8,841` — **the ~8,800 is raw + silver ONLY. The frozen series is absent from
  it**, despite `b-5`'s own text reading "10.5 GB raw + 2.79 GB silver + the frozen series."
- **The byte total is why this survived.** `b-5`'s "10.5 GB raw" overstates raw (actual 7.18 GiB) by
  approximately what omitting the frozen series (2.32 GiB) understates the total. **Two errors
  partially cancelling produce a believable ~13 GB, so the figure that was checkable looked right and
  the figure that was wrong was never checked.**

AC13's printed dry-run therefore states **16,121 objects / 12.10 GiB**, not ~8,800.

---

## 5. VERDICT

`STIA1DS-AC1` **SATISFIED** — 8 figures re-measured at a pinned vintage, each printed beside the
run's, every difference named. 5 hold, 3 moved, and one (`b-5`) is understated by a margin that
changes how the copy is scheduled.

Two items are routed to the issuer as decisions rather than absorbed here — s.3.2 (one remedy across
two states, which bears on `STI-inv-5` / AC5's mutant design) and s.4 (the AC13 figure). **Neither
blocks any other cell and I am proceeding on `STI-b-0` / AC2 meanwhile.**

**Nothing has been written to any bucket. This cell is read-only.**
