# ADVI_49F.c00-FIX — C00-2 FULL-HISTORY IC CENSUS + the mechanism, source-confirmed

**Author:** `0.4.0_DS_ClientPlatform~A` · **2026-08-19** · TO `ADVI_49F.c00-FIX` (COO, amended @5f01d59ba9)
**Rulings this report is written under:** CTO 213741Z (fence holds; engine half splits), COO 214645Z
(the twr invariance is also a negative control), CTO 214127Z (publish the stratum membership list).

---

## 0. THE HEADLINE

**The affected universe is 1,728 TWR-material accounts (5,427 with any in-kind leg), not 42.**
The 42-account figure was a 4-day floor drawn from 4 of 527 partitions, and it understated the
materially-affected count by **41×**.

**And there is no unaffected window to serve.** 434 affected dates fall inside serve scope with
**zero gaps longer than 7 days** across a 648-day span, so *every* TWR window — SI, YTD, 1Y, QTD,
MTD, any length, any start — spans at least one zero-buried in-kind day.

---

## 1. DENOMINATOR AND RETRIEVAL CONTROLS (stated first, deliberately)

| control | value |
|---|---|
| distinct `date=` partitions in scope | **527** (the TO's "~526" is 527 exact) |
| listing pages / keys returned | 2 pages / **1054 keys** |
| keys per partition | exactly **2** (`data.parquet` + `manifest.json`) — internal consistency check |
| partitions read OK / FAILED | **527 / 0** — every read outcome accounted, no silent drops |
| partition date range | 2024-07-08 .. 2026-08-18 |

**Pagination proof:** 1054 keys exceeds the 1000-key default page size, which is positive evidence
that auto-pagination actually ran. The partition set was **materialised client-side and counted
there** — never `--query 'length(...)'` over a paginated `list-*` (which counts *per page*), and
never `--no-paginate` (which returns page 1 looking clean and complete).

---

## 2. MECHANISM — SOURCE-CONFIRMED, NOT INFERRED

`data/assets/scripts/gold/runners_49f/c00_flow_ledger.py` @`288f5eda4a`:

- **`:240`** — `if prices is not None and bool(is_ic.any()):` gates the **entire** in-kind valuation block.
- **`:315-316`** — `prices = pd.read_parquet(...) if args.prices_local else None`.

So with no `--prices-local`, the block never runs and the `:238-239` defaults survive untouched:
`in_kind_value = 0.0` and `in_kind_unvalued = False`. That pair is a **positive assertion that the
transfer was worth nothing**, and it is exactly the measured signature.

**The competing explanation was falsified against source data, not reasoned away.** If the block
*had* run, `in_kind_unvalued` would be `eff <= 0` → `True`; a `False` therefore requires the row to
be excluded by `ic_all = is_ic & (t["quantity"] != 0)`, i.e. `quantity == 0`. Measured on
`fact_trn date=2026-03-24`: **IC rows carry non-zero quantity 49/49** (115.0, 70.0, 7065.617, …).
Quantity is not the cause; the missing `--prices-local` is.

**Attribution trap, disclosed:** `_ingested_at` is stamped from `asof`, **not write time** — it reads
`2026-03-24` on a partition written today. Producers were attributed on **S3 `LastModified`**, not
that column.

---

## 3. THE DEFECT IS 100% HISTORICAL-BACKFILL — THE LIVE PRODUCER IS CLEAN

| cohort | partitions | written | in-kind state |
|---|---|---|---|
| bulk backfill (no `--prices-local`) | **526** | 2026-08-19T01:12:49–01:13:06Z | 100% zero-buried |
| post-P2D-3 chain instance | **1** (`date=2026-08-18`) | 2026-08-19T17:29:27Z | **CLEAN — 52/52 valued** |

`chain_49f_entrypoint.py:163` **does** pass `--prices-local`. So the producer Friday flips onto
already emits correct in-kind values; the defect is a property of the 01:13Z backfill.
*Denominator for the clean claim: 1 of 1 post-fix chain partitions — a spot check at n=1, not a baseline.*

---

## 4. THE CENSUS

| measure | value |
|---|---|
| partitions with ≥1 IC leg | 524 of 527 |
| total IC legs | 41,305 |
| — zero-buried (`value==0` **and** `unvalued==False`) | **41,253 (99.87%)** |
| — genuinely valued (`value>0`) | 52 (all on the one clean partition) |
| **distinct accounts, any IC leg** | **5,427** |
| distinct accounts, EXTERNAL IC leg | 1,730 |
| **distinct accounts, zero-buried EXTERNAL leg** | **1,728** ← the TWR-material defect universe |
| EXTERNAL IC legs (the only legs reaching c02's cash flow) | 23,068 |

**Why EXTERNAL is the material cut:** only `final_class == EXTERNAL` legs enter c02's cash-flow
assembly, so that subset — not the 5,427 — is the number the declaration should carry.

*Reconciliation of two figures that both appear here:* the membership artifact lists **5,423**
any-IC accounts against the census's **5,427**. The 4-account delta is accounts whose *only* IC legs
are the valued ones on the clean 08-18 partition — they carry an IC leg but no defective one.

---

## 5. MATERIALITY READ — "does any serve-scope TWR window span such a day?"

**Yes, and the stronger form holds.**

| measure | value |
|---|---|
| affected dates in serve scope (2024-11-01+) | 434 |
| affected dates before serve scope | 81 |
| first / last affected serve-scope date | 2024-11-01 / 2026-08-10 |
| span | 648 days |
| **clean runs longer than 7 days between affected dates** | **0** |

The correct statement is therefore not "N accounts are affected on some days" but: **the in-kind
cash-flow input is zero-buried across effectively the whole served history, and no window avoids it.**

---

## 6. WHAT IS NOT CLAIMED (the discipline line, carried verbatim downstream)

**1,728 is a COUNT of accounts carrying a defective INPUT. It is NOT a claim that 1,728 accounts
show a materially wrong return.** The +341% specimen proves the error **can** be severe; it does not
license extrapolating that severity across the universe. Per-account magnitude is unmeasured here
and is `ADVI_49F.c02-CFINPUT` CF-3's job.

Also not claimed: that the historical partitions have been repaired. **The code is fixed; history is
not re-emitted.** See §7.

---

## 7. RESIDUALS, EACH WITH ITS OWNER

1. **Historical re-valuation (item 1)** — blocked by data, not effort: `canonical_positions` holds
   **1 partition against 527** flow_ledger dates, so a re-run with `--prices-local` would value
   nothing. Needs new a03 + b01 legs ×526. *Backfill-program decision at the MON census scoping
   (CTO 213741Z item 4); Andrew's word if it carries real cost.*
2. **Honest-label re-emission over history** — the 526 partitions still carry schema 1.0 zero-buried
   rows. I did not re-run 526 partitions the night before a flip on my own read. Note a re-emission
   also needs a02/a05 mirrors per date, which exist in S3 for **only 2 dates** — the 01:13Z backfill
   produced them locally and never uploaded them.
3. **The engine half** — `c02_twr_engine` never consumes `in_kind_value` (`:19` design statement,
   `:128` sole cf source). Split to **`ADVI_49F.c02-CFINPUT` (MON)**, which carries the harness
   re-read as *its* acceptance.
4. **Served-semantics change** — when the engine TO lands, served TWR values change for ~1,728
   accounts. COO routed that P4-class through CTO with per-key never-widen (CF-4).

---

## 8. ARTIFACTS

| artifact | purpose |
|---|---|
| `ADVI_49F.c00-FIX_IC_STRATUM_MEMBERSHIP.json` | 1,728 EXTERNAL-leg + 5,423 any-IC accounts, per-account affected-date counts and first/last dates. **CVO's Thursday twin-vs-legacy pin read consumes this as a stratum lens** (CTO 214127Z): where new-vs-legacy TWR diverges, membership here classifies the divergence. |
| `ADVI_49F.c00-FIX_PROOF_OF_SPEC.json` | C00-1..C00-6, all PASS, every row MEASURED/RULED with its denominator. |
| commit `89204884d7` | the fix + 5 mutant-controlled tests. |
