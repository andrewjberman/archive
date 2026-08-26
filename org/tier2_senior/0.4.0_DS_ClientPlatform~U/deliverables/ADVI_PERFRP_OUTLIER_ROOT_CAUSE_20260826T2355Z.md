# ADVI_PERFRP — OUTLIER ROOT CAUSE: bottom-up forensics on the worst cases

**Seat:** `0.4.0_DS_ClientPlatform~U` · **Stamped:** 2026-08-26T2355Z · **Commissioned:** ANDREW-DIRECT ~23:4xZ, PEAK PRIORITY
**Method as instructed, verbatim:** *"go through the top 10 worst cases and analyze them from the bottom and assess step by step if the problem is in our calculaation, if its a data error, if its a misunderstood figure, etc."*
**Chain traced per case:** `fact_trn` (raw) → `flow_ledger` (classified) → `c02_twr_engine` (computed) → `twr_daily` (emitted).

---

## 0. VERDICT — ONE MECHANISM, TWO DEFECTS IN OUR CALCULATION, PLUS A DATA GAP THAT BLOCKS THE FIX

**Andrew's hypothesis was right, with one substitution: the deposit is in SECURITIES, not cash.**
His example — *"accounts that had $6 in them and someone deposits 500k … if calculations are not sequenced correctly with regard to transactions"* — is the exact shape. An in-kind securities transfer carries `net_amount = 0.00`, so **the flow reaches the return calculation as ZERO while the securities land in ending market value.** The transferred value is then rendered as **performance**.

| # | defect | class | where |
|---|---|---|---|
| **1** | in-kind legs reach the return as **zero flow** | **OUR CALCULATION** | `c02_twr_engine.py:149` |
| **2** | `INTERNAL` flows excluded at **ACCOUNT** grain | **OUR CALCULATION** / misunderstood figure | `c02_twr_engine.py:148` |
| **3** | flow_ledger **cannot express in-kind DIRECTION** | **DATA ERROR** — and it **blocks** fixing 1 | `c00_flow_ledger` → canonical |

---

## 1. DEFECT 1 — THE VALUE IS IN THE LEDGER AND NEVER REACHES THE CALCULATION

`c02_twr_engine.py:148-149`:
```
ext = led[led["final_class"] == "EXTERNAL"]
cash_cf = ext.groupby([...])["signed_amount"].sum()
```
It sums **`signed_amount` only.** Its own docstring at `:19` states the defect as the design: *"External CF(t) per account-day = SUM(C_00 signed_amount WHERE final_class == EXTERNAL)."*

**MEASURED in `flow_ledger`:**
| date | in-kind rows | `signed_amount == 0` | `in_kind_value` POPULATED | `in_kind_unvalued = False` |
|---|---|---|---|---|
| 2026-08-24 | 141 of 1,147 | **141 of 141** | **138** (3 zero) | 138 |
| 2026-08-25 | 71 of 1,034 | **71 of 71** | **71** | 71 |
**CONTROL:** on **non**-in-kind rows `signed_amount` IS non-zero (97 of 1,006; 104 of 963) — **the field works; it just never carries the in-kind value.**

⛔ **THE PRODUCER DID ITS JOB.** It classified the flow, marked `is_in_kind=True`, **valued it in `in_kind_value`**, and set `in_kind_unvalued=False` — a positive assertion that the value is known. **The consumer reads the wrong field.**

⛔ **AND THE CORRECT HANDLING ALREADY EXISTS ONE FILE OVER.** `c01_nna_canonical.py:44-45`:
```
ink = pd.to_numeric(ext["in_kind_value"], errors="coerce").fillna(0.0)
# in-kind EXTERNAL legs carry value in in_kind_value (cash-signed amount is 0 on IC rows)
```
**Two sibling producers consume the same ledger. NNA handles in-kind correctly and documents exactly why. TWR does not.**

**PROOF — the correction reproduces a sane return to the cent:**
| account | emitted | corrected | bmv |
|---|---|---|---|
| `0032486794` | **+69,056.0%** | **+0.00%** | 57.00 |
| `0013289888` | **+2,722.3%** | **+0.03%** | 10,135.00 |
*The entire "return" was the transferred securities.*

---

## 2. DEFECT 2 — AT ACCOUNT GRAIN, AN `INTERNAL` TRANSFER IS STILL A FLOW

`:148` filters `final_class == "EXTERNAL"`. **`INTERNAL` means intra-RELATIONSHIP. At ACCOUNT grain, money moving between two accounts of the same client is external to each account.**

**SPECIMEN `0050000151`** — `bmv 321.82 → emv 1,321.82`, **delta exactly +1,000.00**; ledger row: `final_class=INTERNAL · signed_amount=1000.0 · is_in_kind=False · rule=journals`.
**The flow is perfectly captured and perfectly valued. It is simply filtered out.** Emitted return: **+310.7%**.
*Not an in-kind problem at all — a grain/semantics problem. Fixing defect 1 alone would not touch it.*

---

## 3. DEFECT 3 — THE DIRECTION IS NOT EXPRESSIBLE, AND IT BLOCKS THE FIX

⛔ **`flow_ledger` CANNOT SAY WHETHER AN IN-KIND TRANSFER WENT IN OR OUT.**
`r_dc`, `r_cc`, `r_cy` are **empty strings on all 141** in-kind rows · `quantity` is **141 positive / 0 negative** (magnitude only) · `in_kind_value` is **unsigned** (0.00 … 104,145.50) · `signed_amount` is 0.0.
The direction exists upstream in `fact_trn` (`debit_credit` = LONG/SHORT) and **does not survive into canonical.**

>> **THEREFORE "MAKE `c02` READ `in_kind_value`" IS NOT THE FIX — it would be correct on every inflow and wrong on every outflow.** `flow_ledger` must first carry a **SIGNED** in-kind value. **Two remedies, two owners, in sequence.** <<

**I PROVED THIS ON MYSELF.** My first correction pass added the unsigned value to every leg and produced corrected returns of **-199.00%, -174.58%, -181.72%** — **below -100%, which is impossible.** The impossibility is what exposed the sign bug; a less extreme error would have passed.

---

## 4. SCALE — AND THIS IS WHY A PLAUSIBILITY FILTER WAS THE WRONG INSTRUMENT

**Flow value INVISIBLE to the return calculation:**
| date | EXTERNAL cash (seen) | EXTERNAL in-kind (missed) | INTERNAL cash (missed) | INTERNAL in-kind (missed) | **share invisible** |
|---|---|---|---|---|---|
| 08-24 | 3,590,629.31 | 286,972.44 | 13,151.14 | 816,765.95 | **23.7%** |
| 08-25 | 4,867,471.69 | **12,588,776.28** | 141,790.26 | 117,166.73 | **72.5%** |

**Accounts affected, against a denominator of 6,412 / 6,415 with a computed return:**
| date | affected | missed flow >100% BMV | 10–100% | 1–10% | <1% | **visible as >20% outlier** | **WRONG BUT LOOKS PLAUSIBLE** |
|---|---|---|---|---|---|---|---|
| 08-24 | **22** | 5 | 5 | 5 | 7 | **9** | **13** |
| 08-25 | **14** | 2 | 2 | 5 | 5 | **4** | **10** |

>> ⛔ **A PER-DAY PLAUSIBILITY FILTER WOULD HAVE CAUGHT 9 OF 22 AND 4 OF 14.** It would have suppressed the conspicuous cases, **left 13 and 10 wrong-but-plausible returns serving**, and created the belief the problem was handled. **The visible outliers were never the problem — they were the only part of it that announced itself.** <<
**Andrew's ruling against the filter is vindicated by the measurement, not merely by preference.**

---

## 5. WHAT THIS DOES *NOT* CLAIM

· **Not every affected return is wrong by a client-relevant amount** — 7 and 5 sit under 1% of BMV.
· **No fix authored.** No emitter, engine or ledger change; nothing deployed or published.
· **The corrected returns in s.1 are INFLOWS only** — outflow corrections are not computable from canonical until defect 3 is closed (s.3).
· **The three `in_kind_unvalued = True` rows on 08-24 are a genuine, correctly-flagged residual** — the producer says it does not know those values, and that is distinguishable from the 138 it does know.
· **Whether an `INTERNAL` leg should count at account grain is a SEMANTICS ruling** (`1.0.0_SA_CTO` / Andrew), not a measurement. I measured that it is excluded and what that costs; I did not rule that it should be included.

---

## 6. SEQUENCE THE REMEDIATION IMPLIES (stated, not commissioned)
1. **`flow_ledger` carries a SIGNED in-kind value** (defect 3) — prerequisite; without it, step 2 is wrong on outflows.
2. **`c02_twr_engine` incorporates in-kind value** (defect 1) — the pattern already exists at `c01_nna_canonical.py:44`.
3. **Rule the `INTERNAL`-at-account-grain question** (defect 2), then implement to the ruling.
4. **Backfill** — every historical `twr_daily` partition computed under these defects carries the same error.

## Provenance
`0.4.0_DS_ClientPlatform~U`, 2026-08-26T2355Z. Andrew-direct commission recorded verbatim in MCP 74056. Supersedes the per-day plausibility rule ruled by `1.0.0_SA_CTO` 73912. Read-only throughout: no fix authored, nothing deployed, published or scheduled. PII discipline held — only analytic fields read from `fact_trn`; no name, bank, check or memo field was selected or printed.
