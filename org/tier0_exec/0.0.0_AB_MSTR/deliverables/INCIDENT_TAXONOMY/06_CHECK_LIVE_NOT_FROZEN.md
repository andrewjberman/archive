# TAXONOMY 06 — `docs/doctrine/CHECK_LIVE_NOT_FROZEN.md`

    size:      5,575 B / 73 lines
    modified:  2026-07-19 · 3 edits in 14 days
    role:      frozen-reference-drift doctrine. Ratified LD-0314. General form of Verification Laws
               #7 ("well-grounded != FRESHLY grounded") and #8 ("a stale record says something
               false with authority")
    axes:      see AXES.md

---

## 1. STRUCTURAL MEASUREMENT

73 lines: principle · five instances · how it binds · **the sibling boundary** · pointer. No
appendix chain. **The only doctrine file that devotes a whole section to bounding its own
over-application.**

---

## 2. CLASSIFIED INCIDENTS

| # | incident | E | S | F | M | Det | Dir | Rec |
|---|---|---|---|---|---|---|---|---|
| 1 | C3 materialization emit reported 100%; APPLIED live-graph showed a silent **21% edge loss** | E1 | S7 | F1 | M9 | D2 | X-CLEAN | N0 |
| 2 | semctl: a scan that does not print what its number is OF drifts as the population moves | E1 | S7 | F1 | M5 | D4 | X-CLEAN | N0 |
| 3 | OWNED_BY census carried a frozen count forward instead of re-censusing live | E1 | S7 | F1 | M4 | D4 | X-CLEAN | N0 |
| 4 | **AC4 live-coverage caught 2 unmapped edge-types lane-1's careful point-verification MISSED** — PROJECTED 53 vs RAW 55 | E1 | S7 | F1 | M6 | D1 | X-CLEAN | N0 |
| 5 | the GENESIS SDK is itself a frozen abstraction of Opal's mechanism, drifting silently | E6 | S7 | F5 | M12 | D4 | X-CLEAN | N0 |
| 6 | **the NESTEDABSTRACT drift-gate — built to catch frozen-drift — mapped 1 of ~35 live mechanism files in its own hand-picked surface_map** | E1 | S7 | F8 | M1 | D4 | X-CLEAN | **N-SELF** |

**6 classified incidents.**

---

## 3. DISTRIBUTION

**Mechanism:** M1 **1** · M4 **1** · M5 **1** · M6 **1** · M9 **1** · M12 **1** — one each, no
concentration.

**Epistemic type:** E1 **5** · E6 **1** · **Direction:** X-CLEAN **6 (100%)**

**Detection:** D4 **4** · D2 **1** · **D1 1** — instance 4 is one of only **two** designed-control
catches in the entire doctrine corpus.

**Recurrence:** N-SELF **1 of 6 (17%)** — and it is the load-bearing one.

---

## 4. DOCUMENT-SPECIFIC FINDINGS

**4.1 — Instance 6 is the corpus's cleanest self-violation and it is stated without flinching.** A
drift-gate built to catch frozen-abstraction-drift was itself frozen-drifted, covering 1 of ~35 live
files via a hand-picked allowlist. The generalisation it produces is the sharpest form of M1 in the
corpus:

> **"A control's OWN denominator is live state too — the allowlist / surface-map / threshold-set /
> coverage-list a control reads FROM must get the same live-cadence, or the control silently narrows
> what it can see and reads that narrowing as coverage."**

**4.2 — The sibling boundary is the only over-application guard in the corpus, and it is the reason
this file is short.** It explicitly forbids reading its own principle as *"every unmoving number is a
defect"*, and ties to CLAUDE.md NEVER#1 (the trading-calendar default). The unifying line:

> **"Do not reason from a frozen artifact's age in EITHER direction — ground the live state and count
> in the right frame."**

**This matters disproportionately.** NEVER#1's own record says three agents independently reported a
healthy T-1 pipeline as "frozen for 3 days" — the exact false-alarm this boundary exists to stop.
**A doctrine that only pushed one way would have manufactured those false outages faster.**

**4.3 — Instance 4 has a scalp and the file says so.** *"This instance is not just a principle — it
has a scalp."* It is the corpus's best worked example of live-cadence beating careful
point-verification: lane-1 read comp-kuzu PROJECTED (53 types), the producer emits from RAW (55), and
the 2 raw-only types lived in the gap. **A rigorous instrument on the wrong axis survived review; the
live-cadence detector on the right axis caught it on run #1.**

**4.4 — This file and 04 (INTENT_DENOMINATOR) are the same law at different tenses.** 04 says intent
and denominator must not come from one artifact (a *structural* condition). 06 says a denominator
frozen at time T stops covering the population at T+n (a *temporal* condition). **Both are "the
instrument's expectation must be sourced independently and re-derived."** They are 34KB apart and
neither cites the other on this point.

---

## 5. PRUNE VERDICT

| move | effect |
|---|---|
| **KEEP ENTIRE** | 73 lines, ratified (LD-0314), boundary-guarded, one N-SELF stated honestly |
| **MERGE the LAW with 04's §2** | one law, two tenses (structural + temporal); keep both instance sets |
| **PROMOTE the sibling boundary** | it is the corpus's only anti-false-alarm clause and it protects a live NEVER-rule |
| **PROMOTE instance 6's generalisation** | *a control's own denominator is live state too* — this is M1 applied to the control itself |

**KEEP. Smallest high-value file in the corpus after TRIGGER_LAYER; it earns its length.**
