# TAXONOMY 07 — `docs/doctrine/TRIGGER_LAYER.md`

    size:      4,138 B / 63 lines  (smallest doctrine file)
    modified:  2026-07-22 · 1 edit in 14 days
    role:      a structural finding lands as a GATE or an OWNED BLOCKING ITEM, never as a note
    axes:      see AXES.md

---

## 1. STRUCTURAL MEASUREMENT

63 lines: the rule · **why prose findings die (the mechanism)** · what it binds (4 clauses) · **the
boundary (what this does NOT license)**. Zero incident narrative — it *cites* incidents and inlines
none.

> **THIS IS THE ONLY FILE IN THE CORPUS THAT OBEYS `docs/doctrine/README.md`'s OWN SPEC:**
> *"durable principles that govern how every agent works. Stated as rules, in the imperative, **with
> no incident narrative**."* Every other doctrine file inlines its incidents. This one links out.

---

## 2. CLASSIFIED INCIDENTS

This file records **carrier failures** — cases where a finding was correct and could stop nobody.
That is a distinct class from an instrument lying, so the Axis-4 codes concentrate hard on **M14
(PROSE-AS-CONTROL)**.

| # | incident | E | S | F | M | Det | Dir | Rec |
|---|---|---|---|---|---|---|---|---|
| 1 | the 05-08 `comp-constants` note named the exact firm-set defect **eleven weeks early**, verbatim, in the right file — and could stop nobody | E1 | S6 | F8 | M14 | D7 | X-CLEAN | N0 |
| 2 | the 207h-stale danger map flew an accurate staleness flag with **zero actors attached** | E1 | S7 | F8 | M14 | D7 | X-CLEAN | N0 |
| 3 | an inexpressive gate re-reports ratified conditions forever, trains readers to skim — **a skimmed gate is a dead gate that still looks alive** | E1 | S7 | F8 | M14 | D4 | X-CLEAN | N0 |
| 4 | progress claims decay fastest and nothing expires them (LD-0334) | E6 | S6 | F5 | M14 | D4 | X-CLEAN | N0 |

**4 classified incidents — all M14, all X-CLEAN, all detected late or by reading.**

---

## 3. DISTRIBUTION

**Mechanism:** M14 **4 (100%)** · **Type:** E1 **3**, E6 **1** · **Direction:** X-CLEAN **4 (100%)**
**Detection:** D7 **2**, D4 **2** · **D1 = 0** · **Recurrence:** N-SELF **0**

> **The only file in the corpus with zero self-violations.** It is also the only one that never
> asserts a measurement of its own — it has nothing to be wrong about.

---

## 4. DOCUMENT-SPECIFIC FINDINGS

**4.1 — This file is the corpus's own indictment, and the corpus has not acted on it.**

> **"A finding that cannot fail a gate is a diary entry."**

Measured against the corpus: **~200 incidents recorded across 168KB of doctrine, and `D1` (a designed
control fired) accounts for 4 of them.** The remaining ~196 were caught by reading, by a
hand-run positive control, or by an arithmetic mismatch. **By this file's own definition, the great
majority of the doctrine corpus is diary entries.**

**4.2 — The mechanism section is the load-bearing part and it is four bullets.** *A note has no
failure mode. An honest flag nobody owns is halfway to no flag. An inexpressive gate dies of noise —
the same death from the other side. Progress claims decay fastest and nothing expires them.* The
third is the non-obvious one: **expressiveness is part of the doctrine, not a nicety** — a gate that
cannot say "known, accepted, by whom, until when" trains its readers to skim.

**4.3 — The boundary section prevents the obvious over-correction**, and it is the reason this
doctrine has not produced a hundred unowned items: *it does not license bulk-converting historical
notes into findings — that manufactures a hundred unowned items and kills the gate on day one.
Conversion is at touch time, with an owner attached.*

**4.4 — Clause 2 contains a precise anti-pattern that the estate keeps re-earning:** structural
findings must be carried as **machine-checkable fields**, *"never solely as free text. The lint is on
the STRUCTURED FIELD, never a text-match over prose."* This is the same boundary as LD-0274 and the
same one CLAUDE.md F-010 explicitly carves an exception to (`-F` moves content out of shell parsing).
**Three files hold one boundary.**

---

## 5. PRUNE VERDICT

| move | effect |
|---|---|
| **KEEP ENTIRE, UNTOUCHED** | 63 lines, the corpus's spec-compliant exemplar |
| **USE IT AS THE TEMPLATE** | rule → mechanism → binds → boundary → links out. Compressing the other files means making them look like this one |
| **ACT ON IT** | the corpus's D1≈2% is this doctrine measuring itself and failing; that is a finding for Andrew, not an edit |

> **The shortest file in the corpus is the only one that follows the corpus's own rules, has no
> self-violations, and states the finding that indicts everything else. That is not a coincidence —
> it is what a file looks like when it links to its incidents instead of eating them.**
