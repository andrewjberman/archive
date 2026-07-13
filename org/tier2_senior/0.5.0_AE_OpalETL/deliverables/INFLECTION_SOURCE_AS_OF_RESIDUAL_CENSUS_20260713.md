# Inflection `source_as_of` Residual Census — co-sign evidence packet

**Author:** 0.5.0_AE_OpalETL · **Date:** 2026-07-13 · **Status:** HOLD (no writes/deletes) pending sign-off
**Dispatch:** MSTR 2026-07-13 (per-partner ETF producer stamps FILE date not DATA date)
**Grounding:** live `opal-data-etfs/daily/inflection/` reads (62 slices) + deployed `inf-etf-ownership-daily` zip (`aws lambda get-function`) + repo `infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/lambda_function.py:137-141,158 @ HEAD`.

## Headline
- **The PRODUCER IS ALREADY FIXED — repo AND deployed (verified on the live zip).** It stamps `source_as_of = df["date"].max()` (true vintage) and keys output on the source-partition date. It cannot mint a weekend slice.
- **What MSTR measured is RESIDUE** from the pre-06-29 buggy version (a daily cron keyed on the RUN date). Weekend/holiday slices STOP at 2026-06-29; every slice 06-30→07-10 is trading-day-only with `source_as_of == date` correct.
- **A present-day fix and a stale-artifact bug print the same RED on a served read** (MSTR's doctrine line). This is served-artifact cleanup, not a code change.
- **Scope: inflection-only.** cot served slices are trading-day-keyed with correct `source_as_of`; bd-49f is a frozen 06-25 backfill (no weekend keys). cot's live output (07-08→07-10 correct) proves its deployed producer is also fixed.

## The residual set — THREE issue classes (buggy era 2026-05-16 … 2026-06-29)

### Class A — 16 PROVABLE carried-value lies (behavioral, sound lower bound)
A slice whose `total_ownership` is unchanged from the prior slice, yet `source_as_of == its own date` (claims own-day-fresh while carrying an older value).

| # | key(date) | dow | total_ownership | current source_as_of (lie) | value first appeared |
|---|---|---|---|---|---|
| 1 | 2026-05-17 | Sun | 13,009,266.18 | 2026-05-17 | 2026-05-16 |
| 2 | 2026-05-18 | Mon | 13,009,266.18 | 2026-05-18 | 2026-05-16 |
| 3 | 2026-05-24 | Sun | 11,780,520.83 | 2026-05-24 | 2026-05-23 |
| 4 | 2026-05-25 | Mon (Memorial Day) | 11,780,520.83 | 2026-05-25 | 2026-05-23 |
| 5 | 2026-05-26 | Tue | 11,780,520.83 | 2026-05-26 | 2026-05-23 |
| 6 | 2026-05-31 | Sun | 12,125,081.42 | 2026-05-31 | 2026-05-30 |
| 7 | 2026-06-01 | Mon | 12,125,081.42 | 2026-06-01 | 2026-05-30 |
| 8 | 2026-06-07 | Sun | 39,729,672.70 | 2026-06-07 | 2026-06-06 |
| 9 | 2026-06-08 | Mon | 39,729,672.70 | 2026-06-08 | 2026-06-06 |
| 10 | 2026-06-14 | Sun | 42,661,203.94 | 2026-06-14 | 2026-06-13 |
| 11 | 2026-06-15 | Mon | 42,661,203.94 | 2026-06-15 | 2026-06-13 |
| 12 | 2026-06-20 | Sat | 42,366,075.01 | 2026-06-20 | 2026-06-19 |
| 13 | 2026-06-21 | Sun | 42,366,075.01 | 2026-06-21 | 2026-06-19 |
| 14 | 2026-06-22 | Mon | 42,366,075.01 | 2026-06-22 | 2026-06-19 |
| 15 | 2026-06-28 | Sun | 43,129,968.77 | 2026-06-28 | 2026-06-27 |
| 16 | 2026-06-29 | Mon | 43,129,968.77 | 2026-06-29 | 2026-06-27 |

### Class B — 7 non-trading-day ORIGIN slices (suspect; classify via method-1)
A *new* value on a Saturday/holiday, stamped that non-trading day. The value is the settled prior-trading-day book, so the honest vintage is the prior trading day — but the slice cites a real `holdings_{that-day}.parquet`, so confirming its true internal `date` needs a read of `opal-data-inf` holdings (method-1, awaiting MSTR clearance).

| key(date) | dow | total_ownership | stamped source_as_of | honest vintage (hypothesis) |
|---|---|---|---|---|
| 2026-05-16 | Sat | 13,009,266.18 | 2026-05-16 | 2026-05-15 Fri (needs method-1) |
| 2026-05-23 | Sat | 11,780,520.83 | 2026-05-23 | 2026-05-22 Fri |
| 2026-05-30 | Sat | 12,125,081.42 | 2026-05-30 | 2026-05-29 Fri |
| 2026-06-06 | Sat | 39,729,672.70 | 2026-06-06 | 2026-06-05 Fri |
| 2026-06-13 | Sat | 42,661,203.94 | 2026-06-13 | 2026-06-12 Fri |
| 2026-06-19 | Fri (Juneteenth) | 42,366,075.01 | 2026-06-19 | 2026-06-18 Thu |
| 2026-06-27 | Sat | 43,129,968.77 | 2026-06-27 | 2026-06-26 Fri (but see Class C) |

### Class C — missing trading day(s)
- **2026-06-26 (Fri, trading day): NO slice exists.** The series jumps 06-25 Thu → 06-27 Sat, and 06-27's value ($43.13M) differs from 06-25's — i.e. 06-27 carries 06-26's data. So a real trading day is absent while its data surfaces under a Saturday key. "A missing date in a daily series is its own lie" (MSTR).
- Fixed-era gaps (07-01, 07-03) are NOT defects — the fixed producer is event-driven off the gold sentinel; no gold completion → no slice (expected, honest).

## The re-stamp problem (why it is not "one line")
`source_artifact` carries the SAME run-date lie — a Sunday slice cites `holdings_2026-06-14.parquet`. So the honest vintage is **not recoverable from the etfs slice alone**:
- **method-2 (value-origin, no inf read):** resolves a carry to its origin date — but the origin is itself a non-trading-day (Class B), so it stops one hop short of the true trading-day vintage.
- **method-1 (read the holdings partition's internal `date` max):** ground truth, but reads `opal-data-inf` gold — cleared as a READ (not a run) only on MSTR's explicit ok given the INF sensitivity today.

## Reconciliation flag
My independent census = **16 provable (A) + 7 suspect (B) = 23 non-honest-vintage slices** + 1 missing trading day (C). 0.8.0's emitter guard reported **10 rows** — likely a windowed lookback (recent N days / current AVGCAP month) vs my full 62-slice history. **Reconcile against his exact fired-row set before any remediation** — his guard is the acceptance oracle; my 23 is the full-history superset.

## Remediation (HELD, both gated)
- **RE-STAMP** `source_as_of` → true vintage (MSTR-recommended; reversible; disclosure-doctrine). Needs **NEVER#2 CTO+COO co-sign**. Blast radius = up to 23 keys, `source_as_of` field only, all values/other fields unchanged.
- **DELETE** the non-trading-day slices → needs **Andrew** (unrecoverable).
- **Acceptance test:** 0.8.0's guard goes quiet on those rows (self-classify `fresh`→`rolled_forward`). NOT my own output.

Full 62-row census TSV colocated: `inflection_census_20260713.tsv`.

---

## METHOD-1 RESULT (2026-07-13, MSTR-cleared holdings read) — **COMPROMISED, and the lie is at the GOLD layer**

Read the internal `date` column of every cited `opal-data-inf/gold/canonical/holdings_{date}.parquet` (READ ONLY, cleared by MSTR; no inf write/run, `build_assets_dim.py` untouched). **Result: the internal `date` column carries the SAME lie one layer down — it is NOT a usable vintage oracle.** This is exactly the trap MSTR named ("do not verify a lying-date fix with another field that can lie the same way"), and it fired.

**PROOF (byte-level, three clusters):** the weekend/carry holdings partitions are the SAME book relabeled across consecutive dates —
- `holdings_2026-06-13 / -06-14 / -06-15`: identical non-date body `0906f25f311d`, 11,487 rows each; internal `date` = 06-13 / 06-14 / 06-15 respectively.
- `holdings_2026-05-16 / -05-17 / -05-18`: identical body `c89665fe892a`, 29,593 rows; internal date = own filename date.
- `holdings_2026-06-06 / -06-07`: identical body `54e0823dabfc`, 32,570 rows.
- **Fixed era 07-06…07-10: all DISTINCT bodies per trading day (11,401–11,465 rows), internal date honest.** So the relabel is buggy-era-only.

**Consequences:**
1. **The lie ORIGINATES at the inf gold holdings layer, not the etfs producer.** The etfs producer read `holdings_{weekend}.parquet` (internal date pre-lied) and faithfully stamped `source_as_of = df["date"].max()` = the relabeled date. It inherited the lie.
2. **Even the "fixed" etfs producer would be fooled by a weekend partition** — its `df["date"].max()` trusts the same field. It is safe ONLY because it is event-driven off the gold sentinel (no weekend runs), NOT because it derives vintage from a trustworthy field. On trading days the holdings internal date is honest, so it is fine.
3. **The TRUE trading-day vintage of a frozen weekend book is NOT recoverable from any current artifact:** internal date lies; the value-origin (method-2) is itself a non-trading day; and book structure shifts sharply (32,801 rows on 06-12 Fri → 11,487 on the 06-13 frozen book), so it is not a simple Friday-settlement revision. Also note the entire holdings history was bulk-rebuilt 2026-07-10 (all LastModified 07-10), and the rebuild mixes two extraction regimes (~29–32K-row books vs ~11K-row books).

**Remediation impact:** "RE-STAMP `source_as_of` to the true vintage" is **not cleanly executable — there is no trustworthy source for the true vintage.** Options narrow to (a) DISCLOSE the carry via an additive field (`carried: true` / `value_origin: <date>` / `vintage_confidence: uncertain`) without asserting a false precise date; (b) accept the value-origin date as `source_as_of` with an explicit caveat that it is "value-first-appeared," not a certified holdings vintage; (c) DELETE (leaves the 06-26 gap). **This is now a DESIGN decision for CTO~B (OPAL_ASSETS owner) + 0.8.0 (emitter semantics) + the NEVER#2 co-sign — not a lane call.**

**SCOPE FLAG (surface, do not adjudicate):** the current served inf gold holdings carry relabeled weekend books — a probable inf-gold-layer defect in the SAME "date field that lies about itself" class as the standing INF hazards. **I did NOT act on inf and did NOT read the inf gold producer SOURCE, so I do not assert the mechanism (Rule 22) — flagging the observed served-artifact fact for MSTR/CTO to route.**

Method-1 outputs colocated: `method1_verdict.txt` (per-slice internal-date table) + the body-hash cluster proof.

---

## CONSUMER BLAST-RADIUS — and the DISCLOSURE MECHANISM ALREADY EXISTS, DEPLOYED (2026-07-13)

**The load-bearing finding: option (a) — disclose-the-carry — is ALREADY BUILT, DEPLOYED, and Andrew-direct, at the layer that matters (the served AUM freshness).**

`opal-assets-daily-emitter` carries `apply_value_repeat_guard` (Andrew-direct, "option A", 2026-07-13). **VERIFIED IN THE DEPLOYED BINARY** (pulled the live zip, not the repo): defined at `:830`, and CALLED in the handler at `:1122` (daily) + `:1164` (backfill). It grounds on Andrew's ACTUAL rule — *"it's only ambiguous on weekends/holidays. otherwise there is no way that we're going to be displaying the same number twice"* — i.e. on WHETHER THE VALUE MOVED, the one signal that does not lie. On a TRADING-day value-repeat claiming `fresh`, it sets `vintage_state=missing`, **keeps the value** (additive-sum invariant), and names the reason. This is the value-grounded disclosure the label-grounded controls (and any etfs-slice re-stamp) cannot be.

### 23-vs-10 RECONCILED — they measure DIFFERENT LAYERS (do not equate)
- **My 23** = source-artifact lies across the FULL etfs history.
- **0.8.0's 10** = emitter OUTPUT rows the value-repeat guard downgraded (it reads the emitter's own `cohort_history` DDB GSI + the NEWEST slice per partner, `_latest_partner_key`). **The guard never reads the 23 historical slices.** So the counts are not supposed to match; the reconciliation is "different instruments, different layers," not "who is right." His guard remains the close oracle for the emitter.

### Full consumer map of `opal-data-etfs/daily/{partner}/{date}.json`
| consumer | reads | residual impact |
|---|---|---|
| `opal-assets-daily-emitter` (0.8.0) | newest slice + own DDB history | **PROTECTED** — value-repeat guard (deployed, verified). Served AUM freshness is safe. |
| `avgcap_monthly_average.py` (etfs gold) | all in-window daily slices | **values CORRECT by Andrew-design** (D1 calendar-day carry-forward — the Friday book IS the Sat/Sun position). Only the **AC6 worst-case `source_as_of` LABEL** is mildly optimistic from the lie. |
| `etf_ownership_dashboard.py` (DE) | LATEST slice per partner | historical residual **not surfaced** (shows latest only). |
| `etfs-canon-fanin` (etfs lambda) | daily slices -> DDB upsert | **copies `source_as_of` verbatim into DDB (`:102`)** -> propagates the lie to any downstream freshness reader of that field. |

### Consequence for the CO-SIGNED remediation (lower stakes than the served RED implied)
The CRITICAL freshness protection **already exists** (Andrew-direct, deployed, value-grounded). Option (a)'s disclosure field on the etfs source slices would improve only **label accuracy** (AVGCAP AC6 + the fan-in DDB `source_as_of`) — NOT the core protection. **So the co-sign is now a cost/benefit on label honesty, not on preventing a served-freshness lie** (that lie is already refused at the emitter). Recommendation for CTO~B/0.8.0/co-sign: weigh a served-write + NEVER#2 co-sign against "a couple of staleness LABELS become honest," given the value is correct-by-design and the freshness claim is already guard-refused. The residual is largely INERT.

**Grounding:** deployed binaries (`inf-etf-ownership-daily`, `opal-assets-daily-emitter` — live zips) + source (`avgcap_monthly_average.py`, `etf_ownership_dashboard.py`, `etfs-canon-fanin/lambda_function.py` @ HEAD). Emitter guard call sites verified in the DEPLOYED zip, not self-reported.
