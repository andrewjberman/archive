# ADVI_INSURE TO-R1-DS — AC5 (pattern record) + AC6 (exclusions) + the 76260 re-emit

**Seat:** `0.4.0_DS_ClientPlatform~R` (S4) · **Under:** `2.0.0_SA_COO` 76245, 76260
**Taken:** 2026-08-27 ~17:4x–17:5xZ · **Cells:** `INS-f-1`, `INS-inv-2`, `INS-inv-3`, `INS-inv-5`

---

## 1. THE RE-EMIT (76260) — NEGATIVE CONTROL PASSED

Cleared by COO 76260. `python data/assets/scripts/gold/bd49f_insurance_nav_current.py
--date 2026-08-25 --write --force` → `WROTE and VERIFIED: head-object ContentLength=12934`.

**The producer's own falsifier gates ran BEFORE the write and all passed:** row count reconciles to
the export's 106 declared contracts · NAV tie-out `raw delta 0.000000` against tolerance `0.005`
· AC3 census 15 columns / 0 violations **with its own positive control firing (3 planted names
caught: `twr_ytd`, `nav_series`, `avg_weight`)**. That built-in control is sharper than the one I
wrote by hand this morning, because it plants its own violations rather than trusting a clean scan.

### The before/after diff — the control COO named, run as a diff and not as metric agreement

| | |
|---|---|
| shape | (106, 15) → (106, 15) · columns identical |
| **UNCHANGED (12)** | `bd_account_id, bd_account_number, account_id, relationship_id, firm, spine_class, carrier, product, current_emv, as_of_date, source_pipeline, schema_version` |
| **MOVED (2)** | `account_id_basis`: `NOT-DERIVABLE-UPSTREAM` → **`STRUCTURALLY-INAPPLICABLE`**<br>`advisor_basis`: `NOT-DERIVABLE-UPSTREAM` → **`NOT-CAPTURED-PENDING-SURFACE`** |

**VERDICT: PASS — only the two stamp fields moved.** Invariants re-measured on the AFTER artifact:
rows **106**, sum `current_emv` **51,807,815.31**, null NAV **4**, `as_of_date` spread
**99 / 4 / 2 / 1**. Every one matches the baseline I pre-measured *before* the write, so this is a
control, not a post-hoc comparison. `_ingested_at` is excluded from the diff by construction (it is
the emission stamp; requiring it to be invariant across a re-emission would be incoherent).

⚠ **`account_id_basis` moved because COO's approved 72236 amendment finally reached the artifact** —
the landed parquet predated commit `@e9697d309d`. The issuer owned that mis-expectation in 76260;
recorded here so the artifact's history is legible without the message thread.

---

## 2. AC5 — `INS-f-1` PATTERN RECORD: VERIFIED AND EXTENDED, NOT RE-AUTHORED

**`ADVI_INSURE_PATTERN_RECORD.md` already existed** (`~J`, 180 lines) and covers all five parts AC5
names: landing grammar · gold table shape · spine keys · platinum key form · class-axis value. **I
listed the destination before writing** — the corrective from this session's second-producer
near-miss — and it caught a live artifact for the second time today.

### The defect I found in it, and why it was the one that mattered

Line 90 carried **`NOT-DERIVABLE-UPSTREAM`** for the advisor leg — **the value falsified four hours
earlier by my own census and restamped by COO 76245.**

> ⛔ **A PATTERN RECORD IS THE ONE ARTIFACT WHOSE ERRORS ARE DESIGNED TO BE COPIED.** Cottonwood
> reuses this document by construction. A stale stamp in the producer misleads one consumer; the
> same stamp here **replicates into the next firm's build** and arrives there carrying the
> authority of a ratified pattern. This is the "your own committed artifact goes stale against the
> ruling that corrected it" class, landing on the highest-leverage carrier in the project.

**Repaired, with the prior text preserved rather than overwritten** — a porting firm needs the
mistake more than the conclusion. The row now separates:

- **what stays TRUE** (the original measurement, undisturbed): 0 of 95 columns match an
  advisor-identifier shape across all three spine tables; every advisor handle is a name string;
  the two name formats are not mutually parseable; a name-string join across a six-figure dim is a
  silent-collision generator that returns a plausible number rather than an error;
- **what was FALSE**: that no upstream change could ever populate it — i.e. that the remedy lay
  with the vendor. The carrier is `relationshipdetail.financialTeam[]`, **already sanctioned,
  already routed, never called.**

**The portable lesson now stated in the record itself:** `NOT-DERIVABLE` and `NOT-CAPTURED` are
different claims **with different owners** — one points at the vendor, one points at us. A porting
firm inheriting the wrong one *hands its own gap to its vendor and waits.* Stamp the **remedy**,
not the symptom.

### `INS-inv-2` — no cot prefix, and the control that makes the zero mean something

| target | predicate `cottonwood\|cot_\|/cot/\|\bcot\b` (case-insensitive) |
|---|---|
| **the pattern record** (subject) | **0 hits** |
| `CLAUDE.md` (positive control) | **2 hits** — matched `/cot/`, `cot` |
| the TO face (positive control) | **5 hits** |

⚠ **MY FIRST POSITIVE CONTROL FAILED AND I ALMOST BANKED THE ZERO ANYWAY.** I ran the predicate
against my own census deliverable expecting it to fire; it returned **0**, which made the subject's
0 indistinguishable from a dead predicate. Re-run against two files that genuinely carry cot
references, both fire, and the matched substrings are printed above — **so the subject's zero is
now a measurement.** A control has its own subject and I picked the wrong one first.

**Also measured at source:** the insurance producer and `insurance_leg.py` carry **0** cot
references. bd↔cot separation holds at code, at artifact, and at the pattern record.

---

## 3. AC6 — `INS-inv-3` / `INS-inv-5`, measured over my own commits

**Denominator: 3 commits this session** — `f05d754d43`, `0c4f706937`, `57a1320b6d` (4 files total,
listed in full: two deliverables under my own lane, the gold producer, and this record).

### Limb 1 — no alarm / SNS / SES / monitor / freshness-checker / shadow / parallel emitter / comparator

Predicate over **added lines only**: `SNS|SES|CloudWatch|put_metric|alarm|Alarm|freshness|shadow|
parallel emitter|comparator|boto3.client(.sns`. Raw result: **2 hits.** ⛔ **BOTH ARE PREDICATE
ARTIFACTS, and I opened them rather than quoting the count:**

| hit | actual text | disposition |
|---|---|---|
| `f05d754d43` | *"…not as a staleness **alarm** — no trading-calendar claim is being made"* | prose **disclaiming** an alarm. Not one. |
| `0c4f706937` | *"…the direction that CLO**SES** the question"* | **`SES` as a substring of "CLOSES".** |

**REAL VIOLATIONS: 0.** *A common-token predicate returns native vocabulary as violations — the
same class that once returned 422 false "egress" hits from the word "regression". The count was
never the answer; opening the two lines was.*

**Nothing I built emits, alerts, monitors, or compares.** Every act this session was a read, a
document, a stamp constant, or one idempotent re-emit of an existing partition under an explicit
issuer clearance. **No shadow path and no parallel emitter: the re-emit wrote the SAME key that
already existed** (`--force` on `date=2026-08-25`), which is the opposite of standing up a second
producer — and the near-miss where I nearly *did* author a second one is recorded at
`ADVI_INSURE_TO-R1-DS_AC2_AC3_VERIFICATION_20260827.md` s.0.

### Limb 2 — Advisor tab and Distribution tab are OUT CATEGORICALLY

Predicate `DistributionTab|AdvisorTab|Advisor tab|portal/` over added lines, per commit:
**0, 0, 0.** No frontend file was touched; no commit reaches `portal/`. The frontend plane
(`INS-e-1..5`) remains DE-class and I did not enter it.

**AC6 verdict: SATISFIED**, grounding SOURCE, both limbs, denominators printed.

---

## 4. STATUS AFTER THIS ROUND

| criterion | status |
|---|---|
| **AC1** | `DISTINGUISHED` (INS-b-2, satisfied) / `APPLIED-GATED` (INS-b-1, INS-inv-4 — on `INS-a-1..3`) |
| **AC2** | **`DESIGN-COMPLETE`** with the advisor hop as a NAMED EXCEPTION until the capture lands / `APPLIED-GATED` |
| **AC3** | **printed and clean** — 15 columns, 0 violations, producer-side control firing. `INS-inv-1` byte-identity half NOT taken and NOT claimed (no change made to any AM figure) |
| **AC4** | ⛔ **SHUT** — arm-(a) sovereign gate. Not re-asked. |
| **AC5** | **SATISFIED** — pattern record verified, corrected, `INS-inv-2` measured with a firing control |
| **AC6** | **SATISFIED** — both limbs, 0 real violations |

**Open and owned elsewhere:** the `relationshipdetail.financialTeam[]` capture at
`0.6.0_AE_PartnerETL` under TO-A1-AE (COO 76245a), which flips `advisor_basis` from
`NOT-CAPTURED-PENDING-SURFACE` to a derived value. **Open at the round:** PRD:84's undefined
`a00`/`a01` naming, routed as a PRD ambiguity, not chased.

**No vendor egress at this seat, all session.**
