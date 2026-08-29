# ADVI_49F.c02-GROSSLEG — G-1 DETERMINATION: outcome (a) CODE WRONG

**Seat:** `0.4.0_DS_ClientPlatform~N` · **Cell:** `C02-g-1` · **Written** 2026-08-29 ~21:4xZ
**Accepted by** `2.0.0_SA_COO` msg **83867** ("G-1 SATISFIED. Outcome (a) CODE WRONG. G-2 NOT
TRIGGERED. G-3 IS RELEASED."). Determination message = **83856**.
**Vintage of every source read for the determination:** `bfaa0a6e6e`, branch CLOUD.

⛔ **This is the determination. The fix rides a SEPARATE commit** (TO: *"The first commit on this
TO must be a determination"*).

---

## 1. VERDICT

**(a) CODE WRONG.** `c02_twr_engine.py:286` put the fee add-back on the wrong side of the
subtraction. `r_gross` is meant to be gross-of-fee, the estate's ratified definition says so in
words that can be cited, and the stored value was net-of-fee **with the fee subtracted a second
time**.

**(b) NAME WRONG — NOT TRIGGERED.** Refuted by citation, not by absence (below). The convention
gate at `1.0.0_SA_CTO` is therefore **not invoked**, and nothing was renamed.
**(c) NEITHER — REFUTED BY MEASUREMENT**, not by assertion (§5).

---

## 2. RE-DERIVED FROM THE FILE, NOT FROM ANY PARAGRAPH

Read via `git show bfaa0a6e6e:<path>` — **not the worktree copy, and expressly not the cell's
quoted `8ae7a3ab82` block** (`3.0.0_SA_CVO` 83567 disposition: *"re-derive the sign from the file
rather than from any paragraph"*).

```
commit-ish   bfaa0a6e6e (branch CLOUD)
file blob    a7947b5ad52b5f98bb06f08dd2586d6fd4b9cee2
             rev-parse HEAD:<path> == hash-object <path>  -> worktree CLEAN against HEAD
```

```
:283-284  fee_cf   = led[final_class == "FEE-MANAGEMENT"].groupby(...)["signed_amount"].sum()
:286      cf_gross = cf_net.add(-fee_cf, fill_value=0.0)      =>  cf_gross = cf_net - fee_cf
:190-191  r        = (emv - cf) / bmv - 1

fee_cf < 0  =>  cf_gross > cf_net  =>  r_gross - r_net = fee_cf / bmv  <  0
```

⭐ **THE HALF THAT IS RIGHT LOCATES THE DEFECT EXACTLY.** `cash_cf` at `:276-282` admits only
`_GRAIN_CLASSES[boundary]` = `(EXTERNAL, INTERNAL)`. FEE-MANAGEMENT is in **neither** set, so the
fee is correctly ABSENT from `cf_net` and `r_net` correctly carries the drag.
**The file implemented the ratified sentence's FIRST half correctly and its SECOND half inverted.**
That is why nothing about `cf_net` / `r_net` moves, and why `PRF-inv-6` clause 1 holds by fact.

---

## 3. THE ESTATE'S OWN RATIFIED DEFINITION — CITED, NOT ABSENT

`org/tier1_exec/3.0.0_SA_CVO/deliverables/SPEC_49F_GROUP_C_TWR_ENGINE_20260811.md` @ `bfaa0a6e6e`
(blob `1c9839749fda07f25c0a90f8b98dc75006a46735`):

| line | verbatim |
|---|---|
| `:34` (row C_02) | *"**GROSS and NET pair per sec8**: net retains FEE-MANAGEMENT debits; gross adds back FEE-MANAGEMENT (VERIFIED family: MGFEE/TPFEE/SMFEE); transaction costs remain deducted in BOTH"* |
| `:81` (acceptance) | *"gross-net spread == fee add-back identity on a sampled account"* |

**RATIFICATION CHAIN**, so this is not a draft being called ratified:

- `1.0.0_SA_CTO` msg **60281** — *"GROUP C REVIEW: **APPROVED** … Reviewed in full. VERDICT:
  APPROVED"*; five policies ruled; **one amendment, and it is `C_00`'s `debit_credit` limb, not
  this one.**
- `3.0.0_SA_CVO` msg **60280** (the delivery) describes C_02 as *"gross/net via the VERIFIED
  fee-family **ADD-BACK**"*.
- `POLICY_BLOCK.json:3` names this same document as the engine's `authority`.
- Five production runners cite it in line 3 of their docstrings.

**"ADD BACK" fixes the DIRECTION and nothing further needs inferring: gross ≥ net.** The stored
leg had gross < net on every fee day.

---

## 4. A SECOND INSTRUMENT THAT IS NOT ANOTHER READING OF THE SUBJECT FILE

**Two sibling firms implement the same sec8 sentence and both put the add-back on EMV.**
⚠ **CONVENTION READ ONLY** — no data crosses, no mirror, no sync, and nothing is imported or
called from the 49F tree. Ruled legal on the record by `2.0.0_SA_COO` 83867: *"CLAUDE.md's
cross-firm law binds a BUCKET or a KEY-PREFIX … It does not bind reading source to learn how a
ratified sentence was implemented."*

```
data/inf/scripts/gold/runners_inf/c02_twr_engine.py:14-16 @ bfaa0a6e6e
   "r_gross(t) = [EMV - CF + MgmtFeeAddback] / BMV - 1 ... spread == addback/BMV"
   :57   fee_add = -fee.groupby(...)["transAmount"].sum()          (addback POSITIVE)

data/cot/scripts/gold/runners_cot/c02_twr_engine.py:15-17 @ bfaa0a6e6e   (+ rebate netting)
   :81-86  EXECUTABLE FIXTURE 5 -- BMV=100 EMV=103, fees -2 rebate +1 -> addback +1
           net = r(103) = 0.03 ;  gross = r(103 + addback) = 0.04
           assert (gross - net) == +addback/100

  49F  (pre-fix)  r_gross = (emv - cf_net - addback)/bmv - 1     EMV MINUS the addback
  BOTH SIBLINGS   r_gross = (emv - cf_net + addback)/bmv - 1     EMV PLUS  the addback
```

Same ruled sentence, three implementations, one sign — different authors, different firms, one of
them carrying a numeric fixture that asserts the direction.

---

## 5. WHY (c) IS REFUTED BY MEASUREMENT

**(c) had exactly one live route:** if FEE-MANAGEMENT `signed_amount` were POSITIVE, then
`cf_net - fee_cf` would be the CORRECT build.

| quantity | value | denominator |
|---|---|---|
| FEE-MANAGEMENT `signed_amount` NEGATIVE | **6,216** | 6,216 (present on 5 of 15 partitions) |
| …POSITIVE | **0** | 6,216 |
| CONTROL — same column, same reader, non-fee rows | NEG 13,660 / POS 29,460 / ZERO 22,180 | 65,300 |

The control is the point: the instrument reads **both** signs on the control population, so an
all-negative fee read is a property of the FEE CLASS and not of the reader.

⭐ **AND ONE STORED ACCOUNT-DAY SETTLES IT WITH NO CONVENTION ARGUMENT AT ALL** —
account `0062640151` @ `2025-12-10`:

```
bmv 4,348.72   emv 4,302.41   cf_net 0.00   cf_gross +46.31   (fee_cf -46.31)
emv == bmv - 46.31 EXACTLY  ->  the market was FLAT; the fee was the only mover.

r_net             = -0.01064911   CORRECT (the account fell by exactly the fee)
r_gross AS STORED = -0.02129822   EXACTLY TWICE the fee rate
r_gross add-back  = +0.00000000   a flat market before fees is a ZERO gross return
```

A gross-of-fee return of −2.13% on a day the portfolio earned exactly zero before fees is not a
convention. **(b) dies on the same number:** under (b) the field would be misnamed but its VALUE
would be some real quantity, and *"net with the fee charged twice"* is not a quantity any
convention names. No document in the estate proposes carrying a fee as a contribution.

---

## 6. G-4 — THE SIGNED GAP, PRE-FIX. NO ABSOLUTE VALUE ANYWHERE IN THE INSTRUMENT

15 partitions from `s3://opal-data-49financial/gold/advi/canonical/{twr_daily,flow_ledger}`.
**COVERAGE DELIBERATELY OFF THE REPORTER'S WINDOW:** twelve are an every-45th spread across the
whole 534-date history (`2024-07-08 .. 2026-06-26`), entirely outside
`0.4.0_DS_ClientPlatform~C`'s `2026-07-01..08-28` sweep and off its `2026-07-07` ledger read;
three are the current tail. **A different POPULATION, which is what makes it corroboration rather
than repetition.**

| quantity | value | denominator |
|---|---|---|
| OK account-days evaluated | 72,903 | — |
| fee-days (`cf_gross != cf_net`) | 205 | 72,903 |
| **SIGNED gap `r_gross - r_net` NEGATIVE** | **205** | **205** |
| SIGNED gap POSITIVE | 0 | 205 |
| SIGNED gap ZERO | 0 | 205 |
| **NEGATIVE CONTROL** — non-fee-day `r_net == r_gross` EXACT | **72,698** | **72,698** |
| identity `gap == -(cf_gross-cf_net)/bmv`, max residual | 2.296e-16 | 205 |

⛔ **NOT-EVALUABLE-BY-SCHEMA, disclosed rather than dropped:** 1 of 15 partitions (`2024-07-08`)
carries **4,074 of 4,074 REFUSED-NO-BMV**, so c02 never wrote the `bmv/emv/cf_net/cf_gross`
columns there. **A partition that could not be asked is not a partition that answered NO.**
14 of 15 evaluable.

---

## 7. ⛔ A FINDING NOT IN ANY MESSAGE IN THE THREAD — AND IT WAS WORSE THAN FIRST REPORTED

`data/assets/scripts/gold/runners_49f/tests/test_c02_twr_engine.py:99-116` @ `bfaa0a6e6e`,
`test_gross_net_spread_is_the_fee_addback_identity`, asserted **`r_net - r_gross = +5%`** — the
**opposite sign from the ratified sentence its own function name cites.** A RELATION arm
transcribed from the IMPLEMENTATION, so it scored the implementation's own blind spot as a PASS.

⛔ **AND THE BASELINE RUN FOUND IT WAS NOT EVEN REACHING THAT ASSERTION.** Measured before any
edit: `12 passed, 1 FAILED` — the fee arm failing at `c02:261`, the `in_kind_signed_value` schema
guard, with `flows_from_ledger` also having become a 2-tuple. **Both preconditions arrived with
`ADVI_49F.c02-CFINPUT` (`cab1f8bff9`), so the arm has been DEAD, not merely wrong, since that
commit.** A wrong arm and a dead arm are different failures and this file had both.

**Ruled IN SCOPE by `2.0.0_SA_COO` 83888** under three binding conditions — *"the arm is not the
authority"* — all three discharged in the fix commit; the falsifier sequence is recorded there.

---

## 8. WHAT THIS DETERMINATION DOES NOT DO

- **Does not touch `cf_net` / `r_net`** — the SERVED leg. `PRF-inv-6` clause 1 holds by fact.
- **Does not re-emit, backfill, re-run or serve the 534-date history.** The corrected leg does not
  exist anywhere in stored history and will not until a re-emission **this cell does not
  authorize** (cell §4). ⛔ **"The fix landed" is not "the data is right."**
- **Does not widen into row SELECTION** (`ADVI_49F.c02-CFINPUT`, complete).
- **Does not re-task `0.4.0_DS_ClientPlatform~C`.**
- **Routes nothing on this subject to `4.0.0_SA_CRO`** — D2 distribution restriction, Andrew
  ~16:1xZ 2026-08-24, recorded on `ADVI_49F.json`.

## 9. G-5 — DISCHARGED BY NOTIFICATION, NEVER BY EDITING ANOTHER SEAT'S LOG

| carrier | author | act |
|---|---|---|
| `org/surprise_channel/ADVI_PERFRP/INVESTIGATION_v1.md:418` | `3.0.0_SA_CVO` | named, msg **83879** |
| `org/tier1_exec/1.0.0_SA_CTO/logs/2026-08-28/self_drive_D2-D3_tick19.md:58` | `1.0.0_SA_CTO` | named, msg **83880** |
| `org/tier1_exec/2.0.0_SA_COO/drive_log_20260828T1548Z.md:124` | `2.0.0_SA_COO` | issuer's own; **already annotated in place** — read at source, not delegated to this seat |

Both cited lines verified present at those exact line numbers @ `bfaa0a6e6e`.
Delivery: **2 DELIVERED / 0 QUEUED / 0 REFUSED (denominator 2)**.
