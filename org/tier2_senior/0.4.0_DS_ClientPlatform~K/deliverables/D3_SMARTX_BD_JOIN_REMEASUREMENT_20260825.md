# SMARTX_BD_EXACT_JOIN — re-measurement at a new vintage, and the enum ADOPTION record

**`0.4.0_DS_ClientPlatform~K` · 2026-08-25 · `D3_MODELOVERLAY.TO-R1-DS` surface (a), cells `D3-a-1..a-4`, `D3-inv-3`**
**Measured at `2026-08-25T12:42:51Z`.** Every number below carries its denominator.

---

## 1. Why this exists when TO-D3.1 already delivered a spec

TO-D3.1 delivered `SMARTX_BD_EXACT_JOIN_SPEC_20260819.md` and the machine-readable contract
`data/_contracts/smartx_bd_join_disposition.yaml` v1.0, **CTO-ratified @`f097698bf6`**. That work is
good and I did not redo it.

Two things were still owed, and they are the whole content of this document:

1. **AC1 — the run #9 baselines are A VINTAGE.** A contract measured on 08-19 is a claim about
   08-19. Re-measure and print your own.
2. **AC2 — adopting a schema authored elsewhere is itself a Rule 24 authoring act.** I may not
   inherit someone else's four-postulate verdict; I have to run it.

**BUILD LADDER rung 2 applied first:** the enum, the contract, and the U1 answer already exist, so
nothing here re-authors them. What follows is verification and one refinement.

---

## 2. AC1 — the re-measurement

Instrument: `a06_dim_identity_crosswalk.build_crosswalk` classification logic, re-run over the live
partitions. Both vintages, same code path, so the comparison is like-for-like.

| | BASELINE (contract vintage) | CURRENT |
|---|---|---|
| map partition | `2026-08-19` | `2026-08-24` |
| universe partition | `2026-08-18` | `2026-08-24` |
| **denominator — map rows** | **7,305** | **7,332** |
| **denominator — universe accounts** | **7,316** | **7,340** |
| `JOINED` | 7,286 (99.74%) | 7,311 (99.71%) |
| `KEY_OUTSIDE_ACCOUNT_GRAMMAR` | 16 (0.22%), 13 distinct | 18 (0.25%), 13 distinct |
| `KEY_VALID_ACCOUNT_ABSENT` | 3 (0.04%) | 3 (0.04%) |
| `UNRESOLVED` | **0** | **0** |
| **MECE arithmetic** | 7,286+16+3+0 = **7,305 = denominator** | 7,311+18+3+0 = **7,332 = denominator** |

**The baseline reproduces the ratified contract EXACTLY — every value, to the row.** That is the
strongest available evidence that the contract's numbers are real measurements and not recollection.

**Reverse direction, measured because a join has two sides** (the "accounts examined, not only
accounts that failed" half): 5,763 of 7,340 universe accounts (78.51%) carry at least one
allocation; 1,577 (21.49%) carry none. Reported as an **account-side** number and deliberately NOT
placed on the row-grain axis — a 49F account with no SmartX allocation is the expected state for a
non-model account, not a defect.

**Delta 08-19 → 08-24:** rows +27, universe +24, joined +25, grammar +2, absent +0, unresolved +0.
The distinct non-8-digit key set is **unchanged at 13** and all are exactly 9 digits at both
vintages — so the +2 is **two additional ROWS carrying already-known bad keys**, not two new bad
keys. Stating that distinction is the difference between "the residual grew" and "the residual did
not change shape".

### Controls, run at BOTH vintages

| control | result |
|---|---|
| POSITIVE — 50 known 8-digit keys | **50 of 50** present in the universe |
| NEGATIVE — synthetic `9999999999` | **absent** (the test is not undiscriminating) |
| RELAXED-JOIN — zfill the 13 distinct 9-digit keys | **0 of 13** admitted |
| UNIVERSE SHAPE | **7,340 of 7,340** ten-char `00`-leading; zero native 9/10-digit members |

The relaxed-join control matters most: it establishes the `\d{8}` test is **not manufacturing** the
grammar residual. Those keys are genuinely outside the universe.

### The LOCKSTEP caveat, honoured

`a06`'s own docstring warns the two derivation universes agree **by coincidence, not construction**.
I did not treat them moving together as evidence they match. The 1,577 no-allocation accounts and
the 21 residual rows are reported as **measured set differences**, never reconciled by assertion.

---

## 3. AC2 — the four-postulate ADOPTION record

Run by me, on my own measurements, at both vintages. **Verdict: ADOPT v1.0 UNCHANGED.**

| postulate | test | result |
|---|---|---|
| **(i) MECE** | EMPIRICAL, not by-construction: count rows satisfying >1 test, and rows satisfying none | rows in >1 class = **0**; rows in no class = **0**; arithmetic reconciles at both vintages |
| **(ii) SAME GRAIN** | is the declared key `allocation_id` actually unique per partition? | duplicates = **0** at both vintages — the declared grain is real |
| **(iii) INTENT COHERENCE** | one intent (join-resolution OUTCOME); check the 5 rejections hold | all measured, not preferential — see §3.1 |
| **(iv) STATE COHERENCE** | test the declared stability split across a REAL universe refresh | **holds, with one refinement — §3.2** |

### 3.1 The rejections still hold at the new vintage

`NO_SMARTX_ALLOCATION` is wrong grain (an account property; measured separately at 1,577/7,340).
`CLOSED` classifies nothing (zero `close` rows in the map). `OTHER_CUSTODIAN` would be INFERRED —
nothing in the data names a custodian. Two renames (`NON_8DIGIT_KEY`, `NOT_IN_ACCOUNT_UNIVERSE`)
were naming fixes, not drops. None of these is weakened by the 08-24 data.

### 3.2 The stability frame — and a correction I filed against myself

**I first reported the contract's frame as OPTIMISTIC. It is not. I was wrong, and I retracted it
on the record (msg 70486).**

I compared 08-19 and 08-24, found the same 3 `KEY_VALID_ACCOUNT_ABSENT` specimens, and concluded
the "moves under a refresh" bucket **moves 0 of 3**. That was **a 2-point sample read as a time
series** — and both endpoints happened to sit at the same value.

Measured across **eight** vintages it plainly moves:

| date | absent | change |
|---|---|---|
| 08-13 | 3 | `10299365`, `41879643`, `99250989` |
| 08-14 | 4 | **new** `76683216` |
| 08-17 | 4 | — |
| 08-18 | 3 | **CLEARED** `76683216` |
| 08-19 | 3 | — ← my sample point A |
| 08-20 | 5 | **new** `19149018`, `30682432` |
| 08-21 | 5 | — |
| 08-24 | 3 | **CLEARED** `19149018`, `30682432` ← my sample point B |

**Three distinct accounts cleared under universe refreshes. The contract's claim is CORRECT.**

**The replacement finding is sharper than the one I withdrew, and it is new to both the contract and
me — the class is BIMODAL:**

- **STABLE CORE — 3 accounts** (`10299365`, `41879643`, `99250989`), present at **all eight**
  vintages, never cleared. Departure **confirmed** against the contract's own evidence claim: over
  **536** `fact_acc` partitions, `41879643` and `99250989` were present at `2024-07-08` and are
  absent at both `2025-07-31` and `2026-08-24`. These are **departed accounts still carrying an open
  SmartX allocation** — a routine refresh will never readmit them.
- **TRANSIENT TAIL** — churns in and out, clears within 1–4 trading days. Genuinely refresh-resolved.

> **So the split the contract draws BETWEEN `GRAMMAR` and `ABSENT` recurs INSIDE `ABSENT`.**
> Anyone sizing remediation off *"refresh the account dimension and the absent bucket clears"* will
> clear the transient tail and **never** clear the core.

**NOT proposed as a contract change.** v1.0 is ratified, `D6`/`TO-G` gates on it, and this is
evidence about the class's behaviour, not a new value. Recorded here and in the proof-of-spec.

*The transferable half: a constant and a cycle are indistinguishable at two samples, and the
flattering reading is "stable" — because stable needs no further work. It also failed toward
**accusing** a ratified contract rather than excusing it, which is the direction that gets audited
least, because nobody re-checks a criticism of someone else's document.*

### 3.3 Token-hygiene census

`comp-find -i` (case-insensitive per Rule 21 — this estate capitalises its load-bearing words).

| token | occupancy | verdict |
|---|---|---|
| `KEY_OUTSIDE_ACCOUNT_GRAMMAR` | 32 estate-wide | distinctive, safe |
| `KEY_VALID_ACCOUNT_ABSENT` | 22 estate-wide | distinctive, safe |
| `JOINED` | `data/`: 209 any-case vs **7** upper-case-only | **high collision** with the English word |
| `UNRESOLVED` | `data/` 410, `docs/architecture/` 99 | **high collision** (`UNRESOLVED-CLIENT`, `unresolved_serials`) |

**Predicate audited rather than quoted** — the 209-vs-7 split *is* the finding, not noise around it.

**NOT a rename request:** the contract is ratified and a cross-package consumer gates on it;
renaming would be far worse than the collision. **The actionable output:** any census over this axis
must **qualify the token** (`join_status: JOINED`) and never grep the bare word.

---

## 4. What surface (a) hands to surface (b)

- The enum, adopted unchanged, with a **per-row non-optional `evidence` column** implemented in
  `b04_account_model_membership.py` — each of the four statuses writes a distinct string naming the
  test that produced it. A status with no evidence is an assertion.
- `UNRESOLVED` carried as a first-class value **at 0**, never as a filter — so a future unexplained
  row surfaces as a published number instead of vanishing from the denominator.
- The classification identity `joined + explained = denominator` asserted **in the producer** and
  written into the manifest at every run, so it is a property of the **artifact**, not of a log line.

---

## 5. Residual open items — routed, not silently held

1. **The U1 roster producer exists in TWO HOMES** —
   `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/silver.py` and
   `infra/aws/lambda/smartx_assets_pull/silver.py`, byte-identical at D3.1's read. `b04` now
   **depends** on that table, so this is live coupling: the Rule 22a shape where a filename-resolved
   check reads clean until the two diverge. Flagged, not chased.
2. **`dim_portfolio_group` / `bridge_group_account` each have exactly ONE partition** (`2026-08-18`).
   Stated as a measurement, **not** a staleness finding — I have not established their cadence and
   NEVER#1 forbids reading a wall-clock gap as a broken producer.
3. **The advisor level is NOT-BUILDABLE-UPSTREAM** — `is_primary` NULL 29,907/29,907. Ruled out of
   R1 by COO (70461); root cause is a vendor-side BD template field, routed to CTO.
