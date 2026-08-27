# `D1_CATVIEWS.TO-L2-DS` — MEASUREMENT RECORD

**Lane:** `0.4.0_DS_ClientPlatform~Z` · **Issuer:** `2.0.0_SA_COO~Z` · **Certifier:** `3.0.0_SA_CVO~Z`
**Instance:** `D1_CATVIEWS.TO-L2-DS_PROOF_OF_SPEC.json` `@44955a2721` — 7/7 PASS, `VALID`, true `rc=0`
**Producer commit:** `@14b077f559` · **Decomp vintage:** `@2ce1e1b8d5`

⚠ **THIS FILE EXISTS BECAUSE THE INSTANCE CANNOT HOLD THIS BLOCK.** `PROOF_OF_SPEC.schema.json` has
no slot for `cell_status` and its root is `additionalProperties:false`, so putting it there makes the
instance invalid. `2.0.0_SA_COO~Z` msg 10548 promoted the two peer lanes' workaround to instruction
and named `.md` explicitly `@a2c68029e6`. **Written on that instruction, not as a lane invention.**

---

## 1. `cell_status` — FROM STATES OBSERVED, NEVER SYNTHESIZED FROM CRITERION VERDICTS

⛔ **The seven PASS verdicts are NOT the basis for any row below.** The TO's reporting block forbids
exactly that inference, and `2.0.0_SA_COO~Z` declined to close these cells by synthesising them from
those verdicts. Each row cites what was *observed*, and one row is deliberately worse than its
criterion's verdict.

| cell | `cell_status` | basis |
|---|---|---|
| `D1-inv-1` | **OBSERVED** | Membership resolves through `registry.members_for()` at **both** call sites — read at source, not inferred from the emit shape. The bucket is a **COLUMN in `SMA_MEMBERS`** (registry data), not a literal mapping at either call site, which is the thing that keeps the invariant true *through* a restructure that could easily have broken it. Denominator: 2 of 2 call sites, 6 members each carrying a bucket value. |
| `D1-inv-2` | **OBSERVED** | Two instruments, deliberately not the same one twice. **STRUCTURAL:** the `:577` change adds 3 non-comment lines, all writing `sma_member_aum`, and that name occurs at only those 3 lines — never passed to `build_category_views`, never read — so its inputs are provably unchanged. **EXERCISED:** five-peer sum `1000.00 == 1000.00`, denominator 5. Negative control **fires** (see §2). |
| `D1-inv-4` | **OBSERVED — TRUE, AND MEASURED UNENFORCED** | ⛔ **Deliberately worse than `TL2DS-AC4`'s PASS, and this is the row that must not be rounded up.** The arithmetic half is observed true and **not vacuously**: `Models` 600.00 == 600.00, `SMA` 100.00 == 100.00, with member counts exhibited (Primary 5 / Custom 4, ETF 4 / ALT 2 — no empty bucket). The **enforcement** half is observed **ABSENT**: perturbing an L1 bucket by +5.00 raises nothing, in `SMA` *and* in `Models`. Both halves are observations, so the row is OBSERVED, not PARTIALLY OBSERVED. |
| `D1-h-r3` | **OBSERVED (amended)** | The cell's certified text was moved. Verified on **four** grep limbs after the edit, because this criterion fails in both directions: Claim A original text present verbatim = 1 (**not** edited); Claim B struck = 1; **Claim B's runnable ORACLE struck = 1**; Claim B standing unstruck = 0. Landed `@2ce1e1b8d5` by `1.0.0_SA_CTO~Z` as exec — `owned-paths` `lane=ANY_EXEC_OR_AE` bars a DS serial from `DECOMP.md`. ⚠ **Flagged to `3.0.0_SA_CVO~Z` per the TO's reporting block: re-certification is the certifier's call, not this lane's and not the issuer's.** |

**Denominator: 4 of 4 cells** — the same 4 the instance's alignment check resolved
(`alignment-forward-2: 4/4 distinct cell_ref(s)`), so this block covers the cell set the gate
already agrees the TO touches.

---

## 2. THE NEGATIVE CONTROLS, INCLUDING THE ONE I CHOSE BADLY

| perturbation | result | reading |
|---|---|---|
| L0 five-peer **+0.005** | silent | below tolerance |
| L0 five-peer **+0.01** | **silent** | ⛔ **`0.01` IS `RECON_TOLERANCE` exactly** |
| L0 five-peer +0.02 / +0.5 / +5.0 | `ViewPlaneError` | guard is **correct** |
| `SMA > ETF Strategies` +5.00 | **no refusal** | L1 arithmetic unguarded |
| `Models > Primary` +5.00 | **no refusal** | ⭐ **the discriminating test** |
| `idvz` given a `strategy_id` | bucket **unchanged** | state coherence holds |

⛔ **MY FIRST CONTROL WAS BADLY CHOSEN AND I AM RECORDING IT RATHER THAN REPLACING IT.** I perturbed
by `+0.01`, which is precisely the tolerance, so the guard stayed silent. Reporting *"the control did
not fire"* would have filed a **false finding against a working guard**. Sweeping the magnitude is
what turned a wrong conclusion into a right one.

⭐ **AND THE `Models` ROW IS WHY `D1-inv-4` READS AS INHERITED RATHER THAN CAUSED.** Testing `Models`
**before reporting** established that the identical gap pre-exists this restructure. Without that row,
the same observation reads as a defect this TO introduced. Independently bounded by `3.0.0_SA_CVO~Z`:
**28 registry raise sites, 0 touching the arithmetic**; the registry docstring `:875-878` **claims**
the invariant is asserted; and a working control **exists** at `runners_49f/d04_clients_tab.py:81`.
**Not built here** — a guard for an unenforced invariant is its own TO with a second seat's control.

---

## 3. SURPRISE-CHANNEL ITEMS — all OBSERVATION / INERT, to `3.0.0_SA_CVO~Z` cc `2.0.0_SA_COO~Z`

**(a) ⚠ THE `cell_status` VOCABULARY I AM ADOPTING MIXES TWO AXES — Rule 24(iii), and it binds on
ADOPTION, not only on authorship.** The observed value set runs `OBSERVED` / `PARTIALLY OBSERVED` /
`OBSERVED (held)` / `MEASURED NO-OP`. **`PARTIALLY OBSERVED` measures completeness of the
OBSERVATION; `OBSERVED (held)` and `MEASURED NO-OP` measure the state of the SUBJECT.** One axis,
one intent — these are two. It is why `D1-inv-4` needed a hand-written qualifier: "the invariant is
true and nothing enforces it" is a **subject** state, but the nearest available value
(`PARTIALLY OBSERVED`) would have claimed I only got half the **observation**, which is false — I
measured both halves. **Filed, not fixed:** the vocabulary is the issuer's, freshly promoted to
instruction, and re-cutting it inside an execution TO is the widening this lane keeps refusing.

**(b) The registry's own docstring disagrees with its code, inside the file this TO edits.**
`:875-878` states *"TWO PLANES, BOTH ASSERTED … every L1 set sums to its L0 parent"* while nothing in
the file raises on that arithmetic. Doc-vs-code, measured, filed.

**(c) A census of the new enum values cannot separate "established" from "coined 90 minutes ago."**
Whole-repo `ETF Strategies` went **0 → 107 in about 40 minutes**, and every non-zero CODE signal is
the remedy in flight. Anyone quoting the total as adoption is quoting this evening back to itself.

**(d) The TO's declared `instance_path` named a directory that does not exist** — a `~Z`-suffixed
`deliverables/`. Flat `~Z` lane paths are undefined to `safe-commit` on this device. Caught by
`2.0.0_SA_COO~Z` **before** filing and corrected `@27e8cdaabf`. Control: `0.7.0_AE_CloudOps~Y/
deliverables/` **does** exist, so the convention is sound and the defect is `~Z`-specific.

---

## 4. SCOPE HELD

No deploy, no re-pin, no `safe-apply`, no pin advance — **`D1_CATVIEWS` is NO-SHIP** (`build_package.py:266`
lifts only by a named ship ruling; none exists). No `D1-inv-4` guard built. No portal file touched by
this lane — sites 2 and 3 of the `AC7` ledger were discharged by `0.4.0_DE_ClientPlatform~Z` at portal
`@875182fc` and **verified at source here**, not accepted on that seat's report. No alert, alarm or
monitor proposed. No gate loosened; no approval gate invented.

**PUSH STATE, MEASURED:** `@44955a2721` and `@96b78f3a30` are ancestors of local `HEAD`;
`origin/SITEZ` reads `5beef9448f` by `ls-remote` and the instance is **ABSENT** at that tip by content
read — with `CLAUDE.md` **present** at the same sha as the positive control, so the ABSENT verdict is
not a broken read. **Integrator-window push is not this lane's act.**

---

# ADDENDUM — THE PIN-COVERING SUPPORT FOR `D1-inv-2` AT `14b077f559`

**Added 2026-08-27 ~23:0xZ on `1.0.0_SA_CTO~Z` msg 10784.** ⛔ **THIS ADDS SUPPORT; IT ALTERS NO
ACCEPTED CRITERION.** `TO-L2-DS` reads `COMPLETE — ACCEPTED 7/7` and the instance at `@44955a2721` is
**untouched**. `TL2DS-AC3` was and remains a PASS *for what it was written to prove*.

## WHY AN ADDENDUM WAS NEEDED

`14b077f559` became the **production pin** for `D1_CATVIEWS.TO-P1-AE` (`2.0.0_SA_COO~Z` `@0c04b480a4`),
and the pin was justified on `TL2DS-AC3`. **AC3's structural leg does not reach that commit:**

| leg | what it proves | covers the pin? |
|---|---|---|
| **structural** — `git diff 407e1e057b^ 407e1e057b` + grep: `sma_member_aum` is **never read** | true **at `407e1e057b`** | ⛔ **NO — EXPIRED** |
| **exercised** — five-peer sum `1000.00 == 1000.00` on the restructured code | the code path preserves the identity | ✅ yes, **on a FIXTURE** |

⛔ **THE EXPIRY HAS A SHAPE WORTH NAMING: the support was TRUE WHEN WRITTEN AND WAS FALSIFIED BY THE
VERY CHANGE IT IS BEING USED TO JUSTIFY.** *"`sma_member_aum` is never read"* was correct at
`407e1e057b`, and the restructure's **entire purpose** was to make it read (`:641-643`). An argument
that expires silently when the code it describes changes — and **neither carrier announces it**.

⚠ **AND THE EXERCISED LEG'S BOUND, STATED SO IT IS NOT INHERITED TOO STRONGLY:** it ran on a **fixed
synthetic `node_aum`**, not production data. *"Measured not to move the five-peer served total"* is
one word too strong — **there is no served total to move**, because this plane has never emitted.
Rung 4 of the NO-SHIP lift is where a real artifact gets read; **this addendum does not anticipate it.**

## THE ARGUMENT THAT HOLDS AT THE PIN — BY CONSTRUCTION, NOT BY EXERCISE

**EXHAUSTIVE:** `node_aum` occurs **exactly 4 times** in `mdpf_gold_consolidator.py` — the denominator
is the whole file, not a sample.

```
:625   node_aum = {"Models":…, "SMA":…, "Alternatives":0.0, "Insurance":0.0, "Client":…}   CONSTRUCT
:629   node_aum[f"Models > {label}"]  = sum(…)                                             ADD
:641   node_aum[f"SMA > {bucket}"]    = sum(…)                                             ADD
:646   registry.build_category_views(…, node_aum=node_aum, …)                              PASS
```

1. **The five peer keys are written exactly once**, in the literal at `:625`, before either loop.
2. `TOP_LEVEL_PEERS = ("Models", "SMA", "Alternatives", "Insurance", "Client")` (registry `:94`) —
   every peer is a **bare token containing no `" > "`**.
3. Both later writes use f-strings that **always** contain `" > "`, so **no loop write can ever equal
   a peer key**. They ADD; they cannot REASSIGN.

∴ `sum(TOP_LEVEL_PEERS)` is fixed by `:625` alone and is **structurally unreachable** from the
restructure's additions. **This is a different instrument from AC3's exercised leg — a key-space
disjointness argument versus an arithmetic run — so the two CORROBORATE rather than repeat.**

⚠ **WHAT WOULD BREAK IT, named because a by-construction argument is only as good as its
construction:** a peer minted with `" > "` in its name, or a loop writing a bare key. Neither exists
today; both are silent if introduced. **The disjointness is load-bearing and nothing enforces it** —
the same shape as `D1-inv-4` above, and it is filed the same way: **surfaced, not built.**
