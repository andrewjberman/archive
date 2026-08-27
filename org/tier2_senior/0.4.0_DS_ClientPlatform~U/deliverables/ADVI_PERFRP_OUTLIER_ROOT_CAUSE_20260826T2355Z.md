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

## 5b. ⛔ RULED + PRE-REGISTERED ACCEPTANCE (added 2026-08-27T0005Z, on `1.0.0_SA_CTO` 74122)

**DEFECT 2 IS RULED.** *"An INTERNAL (intra-relationship) transfer IS a flow at ACCOUNT grain."*
**The principle, so the fix inherits it rather than re-deriving it: FLOW CLASSIFICATION IS RELATIVE TO THE BOUNDARY OF THE POPULATION WHOSE RETURN IS BEING COMPUTED.** "Internal" is a RELATIONSHIP-grain label; at account grain any value crossing the ACCOUNT boundary is external to that account.
⛔ **COROLLARY THE FIX MUST HOLD — the class filter is a FUNCTION OF GRAIN, NOT A CONSTANT:** account-grain returns neutralize `INTERNAL` + `EXTERNAL`; relationship-grain returns neutralize `EXTERNAL` only (the same leg nets *within* the boundary); **a shared implementation takes the boundary as a parameter.** Rule 24(iv): the two grains' figures move under different filters **by design**, so **the artifact states its boundary on its face.**

### THE ACCEPTANCE TABLE — all 10, pre-registered, under BOTH fixes

**10 of 10 collapse into a normal daily band** (that day's `p01`/`p99` were ≈ −0.9% / +0.8%; `p99.9` ≈ +5%).

| account | emitted | **EXPECTED after both fixes** | flow delta applied | defect(s) |
|---|---|---|---|---|
| `0032486794` | +69,056.0% | **+0.00%** | +39,361.92 | 1 |
| `0013289888` | +2,722.3% | **+0.03%** | +275,900.00 | 1 |
| `0057178995` | +1,054.3% | **+3.35%** | +10,020.65 | 1+2 |
| `0050000151` | +310.7% | **−0.00%** | +1,000.00 | **2 only** |
| `0042335575` | +157.8% | **+0.08%** | +8,964.54 | 1+2 |
| `0012942467` | +108.6% | **−0.12%** | +262,865.96 | 1+2 |
| `0066766188` | −100.0% | **+0.00%** | −73.39 | **2 only** |
| `0048403874` | −100.0% | **−0.38%** | −262,865.96 | 1+2 |
| `0049284242` | −99.8% | **−0.67%** | −10,941.82 | 1+2 |
| `0016371483` | −99.3% | **−0.26%** | −108,970.58 | 1+2 |

⛔ **THE TWO-DEFECT MODEL IS JOINTLY CONFIRMED AND LEAVES NO RESIDUE.** `0032486794` is defect 1 alone; `0050000151` and `0066766188` are **defect 2 alone** (no in-kind leg at all); the other seven need both. **Every one of the ten worst returns in the estate is fully explained, and nothing is left unaccounted for.**

⛔ **AND DIRECTION *IS* RECOVERABLE — remediation step (1) is proven achievable, not merely proposed.** Joining `flow_ledger` in-kind legs to `fact_trn` on `(account_id, |quantity|)` where `tr_cd == 'IC'` resolved `debit_credit` **LONG/SHORT for every leg of all ten accounts, with zero ambiguous cases.** *Method limit, stated: the join key would collide if one account had two in-kind legs of identical absolute quantity in opposite directions on the same day. That did not occur here — an ambiguous leg surfaces as a `{LONG, SHORT}` set and would be reported NOT PRE-REGISTRABLE rather than silently picked. The production fix should carry the direction forward on `txn_ref` rather than re-deriving it by quantity.*

**STATUS: FROZEN, NOT COMMISSIONED.** `1.0.0_SA_CTO` 74122: nothing builds tonight; TOs cut when allocation unfreezes on Andrew's word. **The serve card is SUPERSEDED at the terminal** — with the publisher activation measured NOT BUILT (`0.7.0_AE_CloudOps~L` 74091), no serve decision is live. Remediation is **D2's critical path, LAPTOP** (placement map @0a96a52989).

---

## 5c. ⛔ DEFECT 3 — `c01_nna_canonical` SPENDS AN UNSIGNED VALUE AS A SIGNED ONE (added 2026-08-27T0015Z)

**Found by checking why `c01` was absent from `1.0.0_SA_CTO` 74166's ruled minimal set `{c00 → c02 → c04}`.**

**THE GAP FIRST:** `c01_nna_canonical.py:36` — *"ledger = C_00 flow_ledger partition."* **`c01` CONSUMES `flow_ledger`, so step (1) invalidates every historical `nna_canonical` partition** on exactly the reasoning that ruled c02-only out. **The minimal set is `{c00 → c01 → c02 → dependent c04}`.**

**THE DEFECT:**
· **PRODUCER `c00_flow_ledger.py:264`** — `in_kind_value = quantity.abs() * eff`. ⛔ **`.abs()` — MAGNITUDE ONLY, BY CONSTRUCTION.**
· **CONSUMER `c01_nna_canonical.py:44-46, 60-61`** — reads `in_kind_value` as the flow, then `pos_h = flow.where(flow > 0, 0.0)` / `neg_h = flow.where(flow < 0, 0.0)`. **IT BRANCHES ON SIGN.**
>> **An in-kind leg can never be negative, so no in-kind outflow can ever reach `daily_outflow`. Every in-kind transfer — in or out — is spent as a POSITIVE flow.** <<

**MEASURED LIVE, `nna_canonical` date=2026-08-24:**
| account | direction (traced from `fact_trn`) | `nna_unresolved_direction` |
|---|---|---|
| `0016371483` | **OUT** (all SHORT, bmv 110,063 → emv 0.00) | **+89,946.62** |
| `0049284242` | **OUT** (all SHORT) | **+10,956.66** |
| `0032486794` | **IN** | +39,361.92 |
**Outflows and inflows emit the same sign.**
⚠ **THE FIELD NAME IS HONEST AND THAT IS THE TRAP.** `nna_unresolved_direction` says direction is unresolved — the estate has carried an **accurate label on an unusable number**. *A correctly-named field is not a correct value, and the name has been absorbing the defect.*

### THE SCHEMA DECISION THIS FORCES ON STEP (1) — not yet in the sequence
**(a) RE-SIGN `in_kind_value` IN PLACE** — c02 gets what it needs, **and `c01`'s emitted NNA figures MOVE** (outflows flip negative). ⛔ **A TWR fix silently changing NNA.** It happens to be a *correction*, which makes it worse: **a silent improvement is indistinguishable from a silent regression at the consumer.**
**(b) ADD A NEW SIGNED FIELD** (`in_kind_signed_value`, or carry `direction` from `debit_credit` on `txn_ref`) — **`c01` bit-for-bit unaffected; `c02` opts in.** ⛔ **Leaves defect 3 unfixed**, so `c01` is then fixed **deliberately, with its own acceptance.**
**REC — (b), then fix `c01` explicitly.** Rule 24(iv): **three defects, three remedies, three acceptances.** *The thing not to do is let the NNA correction ride in as a side effect of the TWR fix.* **`1.0.0_SA_CTO`'s call; not chosen here.**

**WHY IT MATTERS BEYOND TWR:** the projection consumes `nna_canonical` — **a SEPARATE served surface from the returns.** A remediation scoped as *"fix the performance card"* would leave it standing.

### 5c.1 — ⛔ NARROWING MY OWN CLAIM, AND THE PRE-REGISTERED NNA ACCEPTANCE (added 2026-08-27T0050Z)

**I wrote above and in 74175 that this hits *headline* NNA. MEASURED, it does not.**
`c01`'s headline bucket is `HEADLINE_PROVENANCE = {"code-rule", "dc-resolved"}` (`c01_nna_canonical.py:33`). In-kind EXTERNAL legs censused across **7 partitions** (2026-08-10, 08-18..08-21, 08-24, 08-25): **267 legs, ALL `external-by-default`. In headline provenance: 0 of 267.**
>> **DEFECT 3 IS CONFINED TO `nna_unresolved_direction`. `nna_headline`, `daily_inflow` and `daily_outflow` DO NOT MOVE.** The SURFACE is client-facing; the FIELD that moves is not the headline field — my sentence let those read as one. **The defect is real and the correction stands; its REACH is smaller than I stated.** <<
⚠ **BOUND:** 267 of 267 over **7 of 531 partitions** — not a proven universal. The structural reason is plausible (an in-kind leg has no cash debit/credit for the classifier to resolve from, so it defaults) **but the classifier has NOT been read and that mechanism is NOT asserted.** **The acceptance ASSERTS headline-unchanged rather than assuming it**, so a partition breaking the pattern fails loudly.

**THE PRE-REGISTERED DELTA TABLE** (computed BEFORE the fix, on the ruled design — new signed field, `c01` consumes it):

| date | account | `nna_unresolved_direction` now | **EXPECTED** | headline / inflow / outflow |
|---|---|---|---|---|
| 08-24 | `0016371483` | +89,946.62 | **−91,552.00** | 0.00 → 0.00 |
| 08-24 | `0033493115` | +64,841.33 | **−88,158.89** | 0.00 → 0.00 |
| 08-24 | `0049284242` | +10,956.66 | **−10,926.98** | 0.00 → 0.00 |
| 08-24 | `0032486794` | +39,361.92 | **+39,361.92 (NO MOVE)** | 0.00 → 0.00 |
| 08-25 | *(2 accounts hold a leg)* | — | **NONE MOVE** (both LONG) | — |

**`0032486794`'s NON-MOVE IS PART OF THE ACCEPTANCE** — it is an inflow, correctly positive today, and **a fix that flips it would be over-correcting.**
⛔ **MAGNITUDES CHANGE, NOT ONLY SIGNS:** `0033493115` goes 64,841.33 → **−88,158.89**, which is *not* the negation of itself. **Those accounts hold MIXED-DIRECTION legs — the unsigned sum ADDS opposing transfers, the signed sum NETS them.** A fix validated only on sign-flip would pass while the magnitudes stayed wrong. **ASSERT THE VALUE, NOT THE SIGN.**

⛔ **SCALE STILL UNMEASURED:** the 23.7% / 72.5% figures in s.4 were computed against **`twr_daily`** and **do not cover NNA.** The other **524 partitions are unmeasured and not extrapolated**, and `nna_unresolved_direction`'s downstream consumers have **not been traced** — so defect 3's client-facing impact is **UNQUANTIFIED, which is a different statement from "small."**

---

## 6. SEQUENCE THE REMEDIATION IMPLIES (stated, not commissioned)
1. **`flow_ledger` carries a SIGNED in-kind value** (defect 3) — prerequisite; without it, step 2 is wrong on outflows.
2. **`c02_twr_engine` incorporates in-kind value** (defect 1) — the pattern already exists at `c01_nna_canonical.py:44`.
3. **Rule the `INTERNAL`-at-account-grain question** (defect 2), then implement to the ruling.
4. **Backfill** — every historical `twr_daily` partition computed under these defects carries the same error.

## Provenance
`0.4.0_DS_ClientPlatform~U`, 2026-08-26T2355Z. Andrew-direct commission recorded verbatim in MCP 74056. Supersedes the per-day plausibility rule ruled by `1.0.0_SA_CTO` 73912. Read-only throughout: no fix authored, nothing deployed, published or scheduled. PII discipline held — only analytic fields read from `fact_trn`; no name, bank, check or memo field was selected or printed.
