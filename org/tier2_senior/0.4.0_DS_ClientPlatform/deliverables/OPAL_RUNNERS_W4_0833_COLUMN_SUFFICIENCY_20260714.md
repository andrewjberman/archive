# OPAL_RUNNERS W4 — 0833 column sufficiency for Groups A/B (the COLUMN half)

**TO:** OPAL_RUNNERS W4 (JOINT: `0.4.0_DS_ClientPlatform` = columns · `0.6.2_AE_PartnerETL` = landing facts)
**Author of this half:** `0.4.0_DS_ClientPlatform` · **Measured:** 2026-07-14 ~03:15Z · **READ-ONLY**
**Source:** `opal-data-assets/schwab/08335338/bronze/` (0.6.2's 3-tier-verified monolith copy; terminal)
**Extraction:** `data/assets/scripts/silver/crs_reader.py` — nested-zip unwrap + T1 hard-raise.

> **W4 is the falsifier for the entire 49F refactor.** A false "0833 cannot support Group A" abandons the
> plan on the falsifier itself. So this deliverable obeys CTO's method rider (v-, off 0.6.2's zip-in-zip
> near-miss): **(a)** every claim carries its extraction method; **(b)** a zero-column/zero-row result is
> **UNPARSEABLE-UNTIL-PROVEN**, never reported as absent; **(c)** the container chain is stated per type.

---

## 0. The headline — and the near-miss that shaped it

**Group B (events / holdings / lots) is FULLY present in 0833. Group A account identity is present.
Group A *advisor-role / attribution / split-fee* did not match in the 13 parsed types — but that negative
is SOFT, and here is why it must stay soft:**

> ### The 5 "unparseable" types include FAM and SLM — and those carry account+person-name identity.
> **My reader returned nothing for them because they are CSV, not pipe-delimited CRS.** Had I reported
> the parsed-types result as the answer, I would have filed *"0833 has no advisor/name identity"* — a
> false negative on the exact axis the 49F case turns on, produced not by unwrapping (0.6.2's version)
> but by my reader silently not handling a second file format. **The types most likely to carry Group A
> identity are precisely the ones my reader cannot yet read.** That is rider (b), earned a second time in
> one night.

**Nothing here adjudicates what a gap MEANS.** I assert what the columns carry and what I could not read.
The joint gap list goes to Andrew; neither of us decides whether an absence makes 0833 insufficient.

---

## 1. Extraction method (rider a)

Every 0833 bronze object is **a zip inside a zip** (0.6.2, producer-verified: the vendor nests; neither
`sdd-daily-pull.ps1` nor `sdd-backfill` compresses — so bronze is raw, Rule 17a intact). `crs_reader`
unwraps up to 4 zip layers, reads the pipe-delimited payload, composes the two-row H2/H3 header, and
**hard-raises unless parsed rows tie to the vendor's T1 attested count.**

**Positive control (rider b), on real bytes before trusting any absence:**
`08335338/…/rps/20260710` → single unwrap leaves `PK\x03\x04` (still a zip; decoded as text → no H1, the
all-zero trap). Full unwrap → master `08335338`, firm `49 FINANCIAL`, **D1 93,406×58 + D2 7,144×34 =
100,550 rows = T1 attested.** 92 columns, reconciled. The reader is immune to the zip-in-zip false
negative; a zero-column result from it is a T1 raise, never a silent empty set.

---

## 2. The 13 PARSED types — every one ties to its trailer

| type | container chain | sections (rows × cols) | T1 |
|---|---|---|---|
| `acc` | zip→zip→CRS | D1 7,144×90 | ✓ |
| `rps` | zip→zip→CRS | D1 93,406×58 · **D2 7,144×34** (account BALANCE table) | ✓ |
| `trn` | zip→zip→CRS | D1 9,319×135 | ✓ |
| `sec` | zip→zip→CRS | D1 2,248×69 | ✓ |
| `uln` | zip→zip→CRS | DL 273,567×56 | ✓ |
| `ult` | zip→zip→CRS | DL 196,449×56 | ✓ |
| `rld` | zip→zip→CRS | DL 507×81 | ✓ |
| `rlu` | zip→zip→CRS | DL 289,336×82 | ✓ |
| `rly` | zip→zip→CRS | DL 236,352×82 | ✓ |
| `rtu` | zip→zip→CRS | DT 114,767×70 | ✓ |
| `rty` | zip→zip→CRS | DT 78,846×70 | ✓ |
| `upn` | zip→zip→CRS | DP 56,531×39 | ✓ |
| `upt` | zip→zip→CRS | DP 36,783×39 | ✓ |

337 distinct columns across the 13. Full inventory: appendix / `scratchpad w4_cols.json` (attached on request).
**The RPS D2 section (7,144 account-balance rows) is present on 0833 exactly as on 0824** — so
`read_schwab_raw()`'s silent drop is a both-masters defect, re-confirmed here.

## 3. A/B sufficiency across the 13 parsed types

*(a column MATCH is proof of presence; a NON-match is "no column in the parsed set matched these patterns"
— it is checkable against the full inventory, and it is SOFT wherever an unparsed type could carry it.)*

| Group A/B need | in parsed 0833? | evidence / caveat |
|---|---|---|
| **A — account identity** | **PRESENT** | `master_account_name`, `account_id`, `mstracct_number`, `acct_regis`, `account_status` across 12 types |
| **A — advisor/rep identity** | **no parsed match — SOFT** | 0 of 13 parsed. **But FAM/SLM (unparsed, §4) carry person-name identity.** DO NOT read as absent. |
| **A — advisor ROLE (49F variance)** | **no parsed match — SOFT** | custody files would not carry an advisory role model; likely a different source, but FAM/SLM unread |
| **A — attribution keys** | **no parsed match — SOFT** | same — attribution is an advisory-system concept, and 5 types are unread |
| **A — split-fee/payout (49F variance)** | **NOT the payout layer** | `trn` has `commission`, `broker_service_fee`, `prime_broker_fee`, `trade_away_fee` — these are **trade execution fees, NOT the advisor split-fee/payout layer.** Presence of "a fee column" is not presence of the split-fee layer. |
| **B — holding/position** | **PRESENT** | `quantity_settled`, `cusip`, `ticker_symbol`, `closing_quantity` across rps/uln/ult/rl* |
| **B — transaction/event** | **PRESENT** | `trn` (135 cols), `settle_date`, `transaction_cost`, tcf confirms |
| **B — lot / tax** | **PRESENT** | `rld`/`rlu`/`rly`/`rtu`/`rty`: `cost_basis_*`, `adjusted_gain_loss_dollars`, `lot_selct`, realized+unrealized |

## 4. The 5 UNPARSEABLE types — reader gaps, NOT data absences (rider b)

Each is a distinct format variance `crs_reader` does not yet handle. **None is evidence that 0833 lacks
anything** — they are evidence that my reader has 4 formats left to cover.

| type | container | why it did not parse | what it appears to carry |
|---|---|---|---|
| **`fam`** | zip→zip→**CSV** | **comma-delimited + quoted, NO H-rows** — not the pipe/H1 grammar | account# · custodian name · **PERSON NAME** · account# · registration name · id → **looks like account↔name identity (Group A)** |
| **`slm`** | zip→zip→**CSV** | same CSV grammar as FAM | same identity shape as FAM |
| **`tcf`** | zip→zip→CRS | **H1 layout differs**: `H1\|SCHWAB\|CONFIRM \|08335338\|…` — master in field 3, not field 2; my H1 regex expects `SCHWAB\|<digits>` | trade CONFIRMS: bus date, account#, trade/settle date, action, symbol, CUSIP (Group B events) |
| **`tcfx`** | zip→zip→CRS | **3 header rows (H1/H2/H3) for 2 data sections (D1/D2)** — fits neither my 2:1 nor 1:1 pairing | confirms-extended, two sections |
| **`tnn`** | zip→zip→CRS | **`H01`/`T01`/`T02` two-digit prefixes**, 3 lines, no data rows | a 1099 tax-download **notice** (its own T02 says "NOT an official tax document") — likely genuinely no data |

**FAM/SLM are the load-bearing entry.** They are the most likely 0833 carrier of Group A name/identity,
and they are unread. **Until `crs_reader` gains a CSV path and re-parses them, the Group A identity
question is OPEN, not answered** — and reported as open.

## 5. Joint gap list → Andrew (UNADJUDICATED)

1. **Does 0833 carry advisor-role / attribution / split-fee-payout at all?** Not in the 13 parsed types.
   **Blocked on reading FAM/SLM (CSV) first** — I will not answer it while the likely carrier is unread.
   If the answer is still no after FAM/SLM, that is a real Group-A sufficiency gap, and whether it makes
   0833 insufficient (vs. needing a second advisory source) is **Andrew's call, not ours.**
2. **The split-fee distinction:** 0833 `trn` has trade fees but no evident advisor payout layer. Whether
   the 49F split-fee model can be built from trade fees or needs its own source — Andrew/CTO.
3. **`read_schwab_raw()` drops RPS D2 on 0833 too** (7,144 account-balance rows) — the both-masters
   confirmation of the held-lib defect already on Andrew's board.

## 6. What THIS half owes next (my work, not a gap)

- **Add a CSV path to `crs_reader`** and re-parse FAM/SLM — this is the single highest-value reader gap,
  because it gates the entire Group A identity answer. Then re-run §3.
- **`tcf` alt-H1 + `tcfx` 3-header shape** — two more reader variances; lower stakes (Group B, already
  covered by trn/uln), but they are UNCONVERTED and must not read as absent.
- 0824 column census: **deferred** — 0.6.2 reports it still moving (3,202→3,208 in 20s, climbing to
  5,966). I will not fix a denominator on it tonight; the container shape is identical (nesting depth 2,
  both masters), so the reader work transfers.

---

*Every count enumerated at run time, none sampled. `crs_reader` positive-controlled before any absence
was trusted. The negatives in §3 are checkable against the full column inventory, and marked SOFT
wherever an unparsed type could overturn them.*
