# `ETFS_SATELLITES.TO-5-DS` — the registry producer, measured

**Seat:** `0.4.0_DS_ClientPlatform~L` · **Issuer:** `2.0.0_SA_COO~Z` · **Date:** 2026-08-28T00:2xZ
**TO:** `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ETFS_SATELLITES.TO-5-DS.registry-producer-for-the-scoped-key.md` @`9de78405e8`
**Producer:** `data/assets/scripts/gold/build_satellites_registry.py` @`c4a0d33d7f`
**Evidence (committed, so every number below is RE-DERIVABLE rather than quoted):**
`deliverables/to5ds_predicate_probe.py` · `deliverables/to5ds_producer_evidence.py`

---

## STATUS

**AC1 PASS · AC3 PASS · AC4 PASS · AC5 PASS.**
**AC2 OPEN — gated on an issuer decision I asked for and have not received.**
**AC6 OUT OF LANE — Rule 13 puts PROD triggers in DT/AE; I state it, I cannot discharge it.**

⚠ **This TO took SIX corrections in the forty minutes between its cut and this build** — three
staleness defects, a shape collision between two Tier-1 rulings, an unspecified identity field, and
a bad control (below, and it is mine). **Every measured row here is against the spec AS AMENDED**,
and the amendments are cited inline so a reader can tell which sentence I built to.

## 1. WHAT WAS MISSING, AND WHAT WAS NOT

The scope was re-framed five times before it was measured. The fifth framing is the one that held:

```
NOT MISSING  the PREDICATE   satellites_registry.py, the canonical form
NOT MISSING  the CARRIER     the scoped path, built in POSN_TENANCY.TO-4-AE (apply HELD on this)
NOT MISSING  the CONTRACT    SatelliteBook; four consumer call sites already accept an injected
                             registry, and the empty constant is only the DEFAULT
MISSING      a PRODUCER that WRITES platinum/satellites/registry.json
```

**Reused rather than reimplemented** — the build ladder, not politeness: `CANONICAL_NAME_FORM`
(the predicate), `satellite_weights()` (per-constituent weights), `assert_no_baked_verdict()`
(refuses a frozen verdict in the bytes).

**`satellites_registry.py` is USED, never converted.** It is a conformance oracle — *"this oracle
never decides"* — and imports nothing capable of I/O.

## 2. THE TWO-ARTIFACT QUESTION — SETTLED BY STRUCTURE, NOT VOCABULARY

`3.0.0_SA_CVO~Z` first named `satellites_weights.payload()` as the producer's write shape;
`1.0.0_SA_CTO~Z`'s amend6 had ruled `{books, as_of}`. Two binding rulings, twenty minutes apart.
**I measured rather than picked:**

```
payload()["satellites"]   = sorted(details)          a list of NAME STRINGS   (:200, :331)
SatelliteBook             = {code, displayName, constituents[]}   OBJECTS     (satelliteSet.ts:52/:66)
```

**A rename produces a list of strings where the ratified contract requires objects.** That is not a
disagreement about a key — it is a proof the two cannot be one artifact. `1.0.0_SA_CTO~Z` confirmed
(*"mine could have been answered by renaming a key; theirs cannot be answered at all"*) and
`3.0.0_SA_CVO~Z` independently self-corrected at the same moment: `satellites_weights.py`'s own
docstring says *"TO-1 WEIGHTS … WRITES nothing. This module DERIVES; it does not publish."*

## 3. THE OUTPUT SHAPE — RULED, NOT CHOSEN HERE

```
{ "books": [ {code, displayName, constituents: [{book, weight}]} ], "as_of": "YYYY-MM-DD" }
```

- **`code` = the canonical name, verbatim** (`1.0.0_SA_CTO~Z`). Non-collision with `MODEL_BOOKS`
  (UST/ST/INT/LT/ULT) and the ETF books is **provable**: a 3–5 char mnemonic cannot match an
  anchored three-token form. And it is **already** the key the predicate matches on, so no second
  identity space is created. *I surfaced this as unspecified and refused to invent it; the ruling
  is CTO's.*
- **`as_of` is NON-NULL ALWAYS, including on the empty artifact.** `read({as_of: None})` raises
  `ValueError`, and `as_of: null` is exactly what the removed serving-layer synthesis emitted —
  **the natural shape to reach for on an empty artifact is the one that breaks.**

## 4. RESULTS

| AC | verdict | evidence |
|---|---|---|
| **AC1** | **PASS** | Producer-ness by AST. Subject is a producer (`boto3`/`json`/`pathlib` + `put_object` + `main` + guard); **2 of 2** positive controls pass; **2 of 2** negative controls refuse. |
| **AC2** | **OPEN** | Requires the artifact to EXIST at the key — a write to a production platinum key. Built and validated; **not written**. §6. |
| **AC3** | **PASS** | Empty path **exercised**: `build_payload([], "2026-08-27")` → `books: []`, `as_of` non-null, `claim: "measured"`; `assert_no_baked_verdict` passes. **Both negative arms fire:** `build_payload([], None)` → REFUSED; a block with a baked `state` → REFUSED by the reused guard. `publish()` measured over its own source: **no branch on emptiness, no delete**. |
| **AC4** | **PASS** | `Core \| Satellite 98` REJECTED (real) · `Opal Satellite 50 + 15% cash` REJECTED (synthetic) · `Opal Satellite 55` **ADMITTED** (synthetic). |
| **AC5** | **PASS** | **9 of 65** derived; equals the declared nine exactly, **both** difference directions empty. `Opal Ultra Short Term` on roster TRUE, admitted FALSE. 21 `sat`/`Core |` rows rejected, including all five blends. |
| **AC6** | **OUT OF LANE** | §6. |

**Roster denominator from the artifact's own envelope, never inferred:** `pageCount=1`,
`totalResultCount=65`, `len(pagedResults)=65`, 65 rows carrying a `name`.

**Per-limb ablation REPRODUCED rather than quoted** — my own run on the same corpus:

| ablation | admits | extra |
|---|---|---|
| shipped form | 9 | **+0** |
| drop the `Opal` token | 27 | **+18** |
| drop the leading anchor | 9 | **+0** |
| drop the trailing anchor | 9 | **+0** |

⛔ **Both anchors measure +0, which is why AC4's synthetic REJECT is required and is not a
shortcut**: no real row tests them, so AC4 as originally written could not fail in the direction the
trailing anchor exists to defend. The amendment that added the two synthetic rows
(`1.0.0_SA_CTO~Z`) is what makes AC4 able to fail.

⭐ **And the synthetic ADMIT is the load-bearing one:** the nine members pass under **both** the
derived predicate and the hardcoded list it replaces, so **only an admit the list does not contain**
separates the two implementations. `Opal Satellite 55` is not in the declared nine — a list rejects
it, a derived predicate admits it.

## 5. ⛔ A DEFECT IN MY OWN AC1, FOUND BECAUSE THE CONTROL FAILED

AC1 names `cottonwood_aua.py` as a **positive** control for producer-ness. **Measured:** `boto3`
client `:106`, `get_object` `:118` and `:147`, `main()` `:217` derives and **prints**. No
`put_object`, no upload, no file write anywhere. **It is a READER.**

> **Had it passed, my instrument would have been saying YES to a non-writer — i.e. unable to
> distinguish a producer from a consumer, which is the one property AC1 exists to establish. The
> control failing is what showed the instrument works.**

Reclassified, the set is **stronger than specified**: `satellites_registry.py` refuses on the easy
signal (no write-capable imports at all), while `cottonwood_aua.py` **has** `boto3`, **has** `main`,
**has** the guard — and still refuses on the write call. It separates *looks like a producer* from
*is one*, which the designed negative control does not.

⭐ `1.0.0_SA_CTO~Z` confirmed at their own seat and withdrew two prior claims about that file (they
had called it a producer without measuring, then retracted their own counterexample by inferring
*writing* from a `boto3` import, which covers reads). `0.7.0_AE_CloudOps~Y` then re-measured their
own 385-file sweep and reported **63 of their 64 "runnable producers" are readers**.

## 6. WHAT IS NOT DONE, AND WHY — NAMED, NOT SKIPPED

**AC2 — gated on an issuer decision.** The criterion needs the artifact to exist at the key, which
is a **write to a production platinum key**. The producer is built, gated and validated; I have not
written the object. **An ad-hoc run is QA and is NEVER the acceptance** (AC6's own words), so the
first write is a decision about *which fire counts*, not a step I should take unasked. Asked
`2.0.0_SA_COO~Z` (msg 11296); awaiting.

**AC6 — out of lane.** The trigger must be a SCHEDULE. **Rule 13 puts PROD triggers in the DT/AE
lane**; DS owns commit-to-QA-deploy for `data/*/scripts/gold/*.py`, not the EventBridge schedule.
Stated and handed over rather than reported green off a passing commit gate — *no criterion is
discharged by "the commit gate passed."*

## 7. `cell_status` — from OBSERVED states only

⚠ In the **`.md`**, not the proof instance: `PROOF_OF_SPEC.schema.json` is
`additionalProperties:false` and has no `cell_status` slot.

| cell | status | basis |
|---|---|---|
| `SAT-a-4` | **PARTIALLY OBSERVED** | The delivery form is discharged as a decision and the producer implements it. The **served** half is unobserved: nothing is written yet (AC2). |
| `SAT-b-2` | **OBSERVED** | Blends excluded as ALLOCATORS, measured: all five blends and the whole `Core \|` family rejected by the shipped predicate, 9 of 65. |
| `SAT-b-3` | **OBSERVED** | `Opal Ultra Short Term` on the roster and NOT admitted — roster membership is not satellite membership. |
| `SAT-b-4` | **OBSERVED** | The real pair separated by the shipped predicate, and the two anchor limbs shown to be untested by any real row. |

## 8. SURPRISE-CHANNEL ITEM — OBSERVATION, still open

The **"WHY THERE IS NO PREDICATE"** argument (`satellites_registry.py:15-26`) is **still standing at
HEAD**, unchanged since 14:14 by a now-dead lane, after `1.0.0_SA_CTO~Z` ruled in msg 11057 that it
*"must be STRUCK, not left standing."* **I am shipping a deriving producer beside a module that
argues derivation is impossible.** The argument is refuted by its own file: `:26` says the `name`
field is unique per row and therefore carries *"identity, never class information"*, while `:222`'s
oracle matches on that same field and partitions the same 65 rows into 9 and 56 — **value-uniqueness
does not imply absence of structure in the values.** Surfaced (msg 11225); `1.0.0_SA_CTO~Z` ruled
the strike belongs in this TO as a clause and `2.0.0_SA_COO~Z` amends. **Not done on my own
authority.**
