# TAXONOMY 04 — `docs/doctrine/INTENT_DENOMINATOR_SYNCHRONIZATION.md`

    size:      28,707 B / 381 lines
    modified:  2026-07-24 · 10 edits in 14 days
    role:      the GENERALIZED SCHEMA behind every coverage failure. Authored 2026-07-23 by
               1.0.0_SA_CTO~Z on Andrew's direct instruction to generalize the process
    axes:      see AXES.md

---

## 1. WHY THIS FILE IS DIFFERENT FROM EVERY OTHER ONE IN THE CORPUS

**It is the only file that states a MECHANISM as a formal relation rather than as a list of
incidents.**

    INTENT       = the set the assertion is SUPPOSED to cover. Obligation. Sourced from ABOVE.
    DENOMINATOR  = the set the assertion ACTUALLY covers. Population. Enumerated from BELOW.
    SOUND  iff   DENOMINATOR ⊇ INTENT
    COVERAGE GAP = INTENT \ DENOMINATOR

And then the pathological case, which is **exactly M1 in AXES.md**:

> *"the pathological case is when INTENT and DENOMINATOR are drawn from the SAME artifact. Then
> `INTENT ≡ DENOMINATOR` by construction, the gap is structurally 0, and the instrument cannot fail
> even when it is wrong."*

> ## **THE CORPUS ALREADY CONTAINS THE UNIFYING THEORY. IT IS IN THIS FILE, AND NOTHING POINTS AT IT.**
> **`CONTROLS_OVER_CARE.md` — 3.3× larger, the file CLAUDE.md actually points at — never references
> it.** M1 is 9 instances there, filed as "the third anti-correlated instrument," a coincidence
> observed three times. **Here it is derived.**

---

## 2. CLASSIFIED INCIDENTS

| # | incident | E | S | F | M | Det | Dir | Rec |
|---|---|---|---|---|---|---|---|---|
| 1 | `comp-freshness` names one firm in its config and checks that firm → Cottonwood never evaluated | E1 | S1 | F8 | M1 | D2 | X-CLEAN | N0 |
| 2 | `PUBLISH_MAP` reports `9/9 all_present` — 9 is both denominator and intent | E1 | S1 | F1 | M1 | D2 | X-CLEAN | N0 |
| 3 | telemetry appender's frozen `VERDICT_EXIT_TOOLS` — the list is what it checks AND what it checks against | E1 | S7 | F1 | M1 | D1 | X-CLEAN | N0 |
| 4 | M2 measured the compiler-log **projection** as if it were the population — wrong artifact | E4 | S7 | F1 | M7 | D5 | X-CLEAN | N0 |
| 5 | the R1R3 TO named a curated subset as the registry — **inside the TO whose subject is that defect**, ratified by three cataloguers | E1 | S6 | F1 | M1 | D1 | X-CLEAN | N-SELF |
| 6 | a 400-node property sample returned 0 → one step from *"kuzu carries no file paths"*; targeted probe: present 60/60 | E1 | S7 | F3 | M2 | D2 | X-CLEAN | N0 |
| 7 | a scan for `graph.json` readers counted a **lint-rule message string** and flagged the linter enforcing the rule | E2 | S7 | F1 | M8 | D4 | X-LOUD | N0 |
| 8 | a probe used `.md` fixtures against a script globbing `*.json` → "0 open" on a populated directory | E2 | S7 | F3 | M2 | D4 | X-LOUD | N0 |
| 9 | a parity probe reported "regen owed" off a read that had RACED an in-flight commit | E2 | S7 | F2 | M2 | D4 | X-LOUD | N0 |
| 10 | **MACHINEFLAG sweep: `subprocess.run(['bash',…])` hit the WSL stub; 10 tools' UTF-16 errors classified as PROSE → 10 false findings against peers** | E2 | S3 | F1 | M2 | D3 | X-DESTRUCTIVE | N0 |
| 11 | CVO~Z tick-29: census knew 2 of 3 rule-bank surfaces, reported completeness over its own coverage | E1 | S7 | F1 | M1 | D1 | X-CLEAN | N-SELF |
| 12 | CVO~Z tick-30: 5 axis-bound edges flagged "missing" — carried `axis:` on a surface the predicate didn't know | E2 | S7 | F3 | M6 | D4 | X-LOUD | N0 |
| 13 | **comp-iam `rc3` laundering — a COVERAGE REFUSAL rendered as FINDINGS** by a frozen classifier | E1 | S7 | F1 | M1 | D2 | X-CLEAN | N0 |
| 14 | **subcommand backfill: DECLARED ≠ REACHABLE.** Three CLAUDE.md-mandated calls written into `tools_index`, which `comp-which` never reads | E1 | S7 | F1 | M1 | D2 | X-CLEAN | N0 |
| 15 | …and the correction to 14 by its own author was itself a PARTIAL READ — one of two routing layers grounded | E7 | S7 | F1 | M6 | D2 | X-CLEAN | N-SELF |
| 16 | **`system_parity` reported 100% correctly for ~30 ticks — ONTOLOGY2 landed ADDITIVELY, so the presence-check could not fail** | E1 | S7 | F8 | M1 | D5 | X-CLEAN | N0 |
| 17 | CVO~Z's own probe `head -c 300 \| json.loads` truncated valid JSON → "NOT JSON", **on the exact class under verification** | E2 | S7 | F3 | M2 | D2 | X-LOUD | N-SELF |
| 18 | a guard's coverage went stale the moment the surface it guards grew a finer GRAIN (tool → subcommand) | E1 | S7 | F8 | M6 | D2 | X-CLEAN | N0 |

**18 classified incidents.**

---

## 3. DISTRIBUTION

**Mechanism:** M1 **8 (44%)** · M2 **5** · M6 **3** · M7 **1** · M8 **1**

> **The most concentrated file in the corpus.** 44% one mechanism — because the file was written to
> derive that mechanism. Compare CONTROLS_OVER_CARE's flat 9/76 = 12% spread across 14 mechanisms.

**Epistemic type:** E1 **9 (50%)** · E2 **6 (33%)** · E7 **2** · E4 **1**

**Failure direction:** X-CLEAN **12 (67%)** · X-LOUD **5 (28%)** · X-DESTRUCTIVE **1**

> **X-LOUD at 28% is the highest in the corpus by 3×.** This file's §6b is specifically about
> **false findings against WORKING instruments** — the direction the rest of the corpus barely
> records. Its own explanation: *"a false finding against a working instrument spends the author's
> time and the tool's credibility, and a retraction never fully catches its own claim."*

**Detection:** D2 **8 (44%)** · D4 **4** · D1 **3** · D5 **2** · D3 **1**

> **D1 = 3 and D5 = 2.** The only file where designed controls caught a meaningful share — and
> **the only file where Andrew personally caught two.** §6c is explicit: *"What caught it here was
> none of the above: it was Andrew asking what the number was OF."*

**Recurrence:** N-SELF **4 (22%)**

---

## 4. DOCUMENT-SPECIFIC FINDINGS

**4.1 — §6c is the sharpest cell in the entire corpus.** A SOUND instrument, TRUE output, ~30
consecutive correct ticks — and an unfalsifiable verdict, because ONTOLOGY2 landed *additively* so
the presence-check could not fail. **And the verifier had already PROVEN the additivity in writing.**
Not missing data — *a missing inference over data already produced.*

Its operational rule is the cheapest high-value control in the corpus:
> **WHEN YOU ESTABLISH A STRUCTURAL PROPERTY, ASK WHAT INSTRUMENT THAT PROPERTY BLINDS.**
> *Additivity blinds presence-checks. Supersetness blinds membership checks. Idempotence blinds
> run-count checks. Monotonicity blinds threshold checks.*

**4.2 — §6b's firing condition solves the affordability problem no other file addresses.** "Always
positive-control your probe" is unaffordable at 64 sites. The rule instead: **when your instrument
reports a defect in something you have independent ground truth on, check the instrument first.** It
costs nothing (you already hold the answer) and it fired on row 1 of 10 before a single false finding
shipped.

**4.3 — §8's own heading confessed the defect it defines.** It read "The five instances" while the
list held six, then seven. **The frozen-denominator defect, committed by the file that defines
frozen denominators.** Correctly deleted rather than corrected — *"the fix for a frozen count is
never a fresher count."*

**4.4 — The C(N) ladder (§3) is unverifiable from this document and is doing heavy load-bearing
work.** Intent flows DOWN as obligation, denominator flows UP as composition, soundness at every
layer. It is elegant and it is **asserted**, resting on `NFRA_ONTOLOGY_RULE_BANK.yaml`. I did not
verify that the ladder is implemented as described; **the doctrine's own Rule 22 would class the
ladder as INFERRED.**

---

## 5. PRUNE VERDICT

| move | effect |
|---|---|
| **PROMOTE THIS FILE TO THE HEAD OF THE CORPUS** | it contains the unifying theory (M1) the other files rediscover 20+ times |
| **POINT CLAUDE.md Rule 22 HERE** | Rule 22 currently points at CONTROLS_OVER_CARE, which has the instances but not the derivation |
| **EXTRACT §7's five steps as the canonical process** | name the layer · source intent from above · enumerate denominator from below at run time · declare the gap · re-derive both on change |
| **EXTRACT §6b + §6c as two standalone controls** | the firing condition and the property-blinds-instrument question |
| **KEEP §8 as instances** | they are the evidence |
| **FLAG §3 as unverified** | the C(N) ladder is asserted, not grounded, in this document |

**Strongest KEEP in the corpus. This is the file that makes the other 168KB compressible.**
