# ADVI_INSURE.TO-R1-DS — THE RESIDUAL CEILING

**seat:** `0.4.0_DS_ClientPlatform~J` · **issuer:** `2.0.0_SA_COO` (GO 71385, 2026-08-25 ~20:32Z)
**TO:** `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_INSURE.TO-R1-DS.landing-gold-platinum-planes.md`
**decomp:** `workflows/atom_decomposition/runs/advi-insure-snapshot-plane/20260825T122500Z/DECOMP.md` @`660deaa2cc`
⛔ **DISTRIBUTION: NOT TO `4.0.0_SA_CRO`, AT EVERY RELAY** (PRD s.3, Andrew ~16:1xZ).

**The question this answers, in the issuer's words:** *"Establish exactly what is advanceable WITHOUT
surface (a), and advance it. Then STOP and report the line."*

**R1 is NOT re-derived here.** It was accepted by the issuer ~13:25Z (70569). This document does not
re-run the predecessor's methodology — its denominators and control arms stand. It re-derives only
**claims about artifacts**, which is the half the issuer and CVO both named as worth re-deriving.

---

## THE LINE, IN ONE SENTENCE

**10 of 14 cells are SATISFIED with no insurance byte in existence; 2 are PARTIAL with their
reachable half delivered; 2 are wholly gated on surface (a).** The ceiling is therefore **not
AC-shaped but CELL-shaped** — and the one genuinely advanceable item left is a **reporting split on
`INSR1DS-AC1`**, because that criterion bundles a cell that is DONE with two that cannot be.

---

## 1. THE CELL-BY-CELL LAYER AUDIT — denominator 14

**Method:** each cell's ORACLE (the decomp's own evidence standard, col. 3) names a LAYER. A
`SOURCE`/`DESIGN` oracle is satisfiable by authorship; an `APPLIED` oracle is a property of written
bytes and cannot be satisfied while zero exist. **The layer, not the cell's importance, decides
reachability.**

| cell | oracle (decomp verbatim) | layer | needs (a)? | state |
|---|---|---|---|---|
| `INS-inv-1` | byte-identity control on every existing AM figure | EXERCISED ×2 | BEFORE no / AFTER **yes** | **PARTIAL** — BEFORE captured @`4d40f0d1c8`, **re-verified CURRENT this session** (s.2) |
| `INS-inv-2` | no cot prefix in the pattern record | SOURCE | no | **SATISFIED** — 0/6 cot patterns, positive control `blackdiamond`=5 FIRES |
| `INS-inv-3` | no cell touches `DistributionTab` / Advisor tab | SOURCE | no | **SATISFIED** — frontend plane (e-1..5) excluded to another lane; no cell of mine can reach either file |
| `INS-inv-4` | Rule 17a bronze RAW · Rule 17 silver dedup+dtype | APPLIED | **YES** | **GATED** — the determination is stated, but it is a property OF BYTES and there are none |
| `INS-inv-5` | no alarm/SNS/SES/monitor · no shadow/parallel/comparator | SOURCE | no | **SATISFIED** — zero built or proposed |
| `INS-inv-6` | one producer per served key | SOURCE | no | **SATISFIED** — `d_publisher_port.py:61-62,466,530-533`: the writer structurally CANNOT address a key outside its serve root |
| `INS-b-1` | keys exist at the grammar, `head-object` | APPLIED | **YES** | **GATED** |
| `INS-b-2` | **the two prefixes named and distinguished** | **SOURCE** | **NO** | ⛔ **SATISFIED — see s.3. This is the finding.** |
| `INS-c-1` | table + partition grammar | DESIGN | no | **SATISFIED** — `gold/advi/insurance/insurance_nav_current/date={D}/`, own subtree |
| `INS-c-2` | spine keys carried; a frontend sum is not the source of any figure | DESIGN + APPLIED | design no / rows **yes** | **PARTIAL** — design complete; advisor leg `NOT-DERIVABLE-UPSTREAM` (0 of 95 cols), gated on BD template 390224, ruled at 70462 |
| `INS-c-3` | schema census against the forbidden set | EXERCISED | no | **SATISFIED** — 0 violations / 14 cols; 3 planted mutants all fire; determinism sha256 stable ×3 |
| `INS-d-1` | the key, and its single producer, named | SOURCE | no | **SATISFIED** |
| `INS-d-2` | the NEVER#3 mint distinction stated positively | SOURCE | no | **SATISFIED** — minting a key, not moving one |
| `INS-f-1` | the note exists; contains no cot prefix | SOURCE | no | **SATISFIED** — 180 lines @`e673f994ac` |

```
DENOMINATOR 14 cells
  SATISFIED, no byte required ....... 10   inv-2 inv-3 inv-5 inv-6 b-2 c-1 c-3 d-1 d-2 f-1
  PARTIAL, reachable half delivered .  2   inv-1 (BEFORE) · c-2 (DESIGN)
  GATED wholly on surface (a) .......  2   b-1 inv-4
```

⛔ **A cell census is NOT an AC census and the two disagree on purpose.** Six ACs carry 14 cells;
four ACs read `UNCOMPUTABLE` while **10 of their constituent cells are satisfied**. That is not a
contradiction — it is what happens when a criterion is scored at its *weakest* constituent layer.
**It is also exactly why s.3 exists.**

---

## 2. THE `INS-inv-1` BASELINE IS CURRENT — measured this session, not assumed

The AFTER half of the design falsifier compares against the committed BEFORE baseline. **A baseline
that has silently gone stale would trip the falsifier on a routine republish** — and per the TO, a
falsifier trip means *"the DESIGN is wrong — REPORT AND STOP."* So its currency is load-bearing.

**I did NOT re-derive the predecessor's method.** The baseline already declares the republish
confound and records per-key `etag` + `last_modified_utc` precisely so an AFTER diff can discriminate
*publisher re-ran* from *insurance work moved an AM figure*. That control is sound and I am not
re-running it. **I asked only the artifact question it cannot answer about itself: is it still true?**

**Instrument:** `boto3 head_object` over all 12 keys, `etag` compared to the committed baseline.
Sound here **because the baseline recorded `etag_is_multipart: false` on every key** — for a
non-multipart object the ETag IS the content MD5, so an unchanged ETag is unchanged bytes. *(A
multipart ETag is not a content hash; this shortcut would be invalid without that recorded field.)*

```
BASELINE captured_utc 2026-08-25T12:43:52Z | bucket opal-data-portal-v2 | denominator_keys 12
  objects in baseline ......... 12
  BYTE-IDENTICAL (etag match) . 12
  MOVED ....................... 0
  MISSING (404) ............... 0
  READ ERRORS ................. 0
NEGATIVE CONTROL: a key that should not exist -> 404
  => the probe DISCRIMINATES presence from absence; the 0-missing is MEASURED, not a dead read
```

**VERDICT: the BEFORE baseline still describes live served state ~8h after capture.** All 12 remain
at their 2026-08-21T15:03–15:04Z write. The 49F publisher has **not** re-run in the interval, so
whoever runs the AFTER half inherits a baseline that is current rather than historical.

---

## 3. ⛔ THE ONE ADVANCEABLE ITEM — `INSR1DS-AC1` CARRIES A SATISFIED CELL UNDER AN `UNCOMPUTABLE` VERDICT

**`INSR1DS-AC1` bundles three cells at two different layers:**

| cell | layer | reachable without (a)? |
|---|---|---|
| `INS-b-1` — keys exist at the grammar, `head-object` | APPLIED | **NO** |
| `INS-inv-4` — bronze RAW / silver dedup+dtype | APPLIED | **NO** |
| **`INS-b-2` — "the two prefixes named and distinguished"** | **SOURCE** | ⛔ **YES — AND IT IS ALREADY DONE** |

**`INS-b-2`'s oracle is a NAMING act, not a byte property**, and the evidence satisfying it is
**already committed inside AC1's own `output_evidence`**:

> *"Firm spellings live under `blackdiamond/`: `49f` (285 keys) and `cottonwood` (3,370);
> `blackdiamond/49financial/` DOES NOT EXIST (0 keys) — the ruled target prefix is a MINT, and
> unbuilt is not defective."*

That names both live spellings, distinguishes them with counts, and resolves the leaf-name collision
the cell was written to close. **The oracle is met. No insurance byte was required and none was used.**

⛔ **BUT AC1'S `status_reason` NEVER MENTIONS `INS-b-2`.** It reasons entirely about raw-bytes
availability and Rule 17a — i.e. about `b-1` and `inv-4`. **The satisfied cell is carried silently
under the gated ones' verdict.**

**This is the identical defect the issuer caught and corrected on AC2**, in their own words at 70416:
> *"A criterion carrying two grounding layers cannot take one status honestly."*

AC2 got the split (`DESIGN-COMPLETE / APPLIED-GATED`). **AC1 did not, and it needed the same one.**

### RECOMMENDATION TO THE ISSUER — one line to approve, no new measurement

> **`INSR1DS-AC1` reports as `DISTINGUISHED / APPLIED-GATED`.**
> **DISTINGUISHED:** `INS-b-2` — both live spellings named with counts, collision resolved, evidence
> already committed.
> **APPLIED-GATED:** `INS-b-1` + `INS-inv-4` — dependency `INS-a-1..3` / `0.6.0_AE_PartnerETL`, unseated.

⛔ **I HAVE NOT AMENDED THE INSTANCE, DELIBERATELY.** The issuer **RULED** AC1 `UNCOMPUTABLE-BY-DEPENDENCY`
at 70416. **A criterion's status is the issuer's ruling; rewriting it at the executing seat is scope
adjudication in the widening direction**, which the standing law prohibits in both directions. The
evidence is in hand and the edit is one field — **it costs the issuer one word, and it is theirs to
give.** *(Cost of my restraint: one round trip. It does not apply where the issuer has delegated the
status call, and here they explicitly did not.)*

---

## 4. WHAT IS **NOT** ADVANCEABLE — and why I did not build it

**The gold builder script.** It is the obvious "I could write code without bytes" move. **I did not,
and the reasons are measured rather than felt:**

1. ⛔ **NO CELL'S ORACLE ASKS FOR IT.** `INS-c-1` wants *"table + partition grammar"*; `INS-c-2`
   wants *"keys present"*; `INS-d-1` wants *"the key, and its single producer, named"*. **Not one
   demands an authored builder.** Writing one is **self-authored scope**, which the issuer's GO
   explicitly forbids.
2. ⛔ **ITS INPUT CONTRACT IS OPEN, NOT CLOSED.** Rule 17 makes silver a **passthrough** of bronze —
   so the builder's input column set is *whatever the vendor returns*. The documented contract
   (`docs/architecture/DATA_BDINSURANCE_PRD.md:139-141`, schema-confirmed live off HAR-2) ends in a
   literal **`…`**: `accountNumber, custodialAccountNumber, custodian, custodianId, accountType,
   category, accountSubCategoryId, billable, currentEmv, accountOwners, alternativeInvestment,
   insuranceCharacteristics, asOfDate, createDate, closedDate, customFields, benchmarks, crmSource,
   cleanStartStatus …` — **a PARTIAL enumeration presented as a partial enumeration.** A builder
   written against it is written against a set nobody has closed.
3. **The decomp itself says the mapping is unestablished.** `INS-a-2`'s oracle is *"field→call map,
   **printed**"* with the explicit warning *"do not assume one call covers both"* — and that cell is
   **UNPRODUCED**, in another lane. **The question "which call supplies `currentEmv` vs
   `insuranceCharacteristics`" has not been answered by anyone.**
4. **BUILD LADDER rung 1 — YAGNI.** Code landing ahead of its input contract is debt at the moment
   it lands, and this estate's standing position is that such things are never decommissioned.

**Stated positively so the next seat does not re-litigate it: the builder is not blocked by
permission — it is blocked by an OPEN INPUT CONTRACT, and it becomes cheap and correct the moment
`INS-a-2`'s field→call map is printed.**

---

## 5. THE CEILING, NAMED

**Everything reachable without surface (a) is delivered.** The residual above the ceiling is:

| item | owner | not mine because |
|---|---|---|
| `INS-b-1`, `INS-inv-4` — the landing bytes | surface (a) lane / `0.6.0_AE_PartnerETL` | **the issuer holds this as THEIR item** (71385) — I do not chase it, wait on it, or report BLOCKED on it |
| `INS-c-2` advisor leg | upstream BD vendor config — template 390224 / dim 436 | fixable by no code in this estate; routed to CTO at 70462, gates TWO directives |
| AC1 status split | `2.0.0_SA_COO` | a criterion's status is the issuer's ruling (s.3) |
| the AFTER half of `INS-inv-1` / AC3 | this seat, **event-gated** | needs a change to exist; baseline verified current and waiting (s.2) |

**I am not BLOCKED. The TO is at its ceiling.** Per the issuer's own framing, an
`UNCOMPUTABLE-BY-DEPENDENCY` row is *record it with its dependency named and keep going* — which is
what R1 did and what this document closes out.

**On first insurance bytes, this seat's next acts are already determined and need no new ruling:**
the forbidden-field census re-run against the **LIVE** parquet (APPLIED, not design), then the AC3
AFTER half against the verified baseline.

### ⛔ 5.1 A CORRECTION TO THE NUMBER THE AFTER HALF WILL QUOTE — it is not 11

The predecessor's closing note said the AFTER half should quote **11** independent figures rather
than 12, collapsing the `timeseries_chart` / `timeseries_chart_full` twin. **I was about to repeat
that figure. It is wrong, and the data proving it is inside the committed baseline itself.**

**Instrument:** group the baseline's own 12 recorded `(etag, size_bytes)` pairs. **This is not a
re-run of the predecessor's method — it is a read of the artifact they committed.**

```
DENOMINATOR                                    12 objects
DISTINCT (etag,size) groups                    10
BYTE-IDENTICAL GROUPS (>1 member)               2      <- TWO twin pairs, not one
  1ea8d316bfab6582e100bc7a303be370  20,948 B    _manifests/2026-08-20/933dfc1bf6b1.json
                                               _manifests/latest.json
  ab37740df57e36a10c680963c82a66b1 7,260,521 B  timeseries_chart.json
                                               timeseries_chart_full.json
CLASSIFICATION                                 10 served figures + 2 manifests
```

**So the frame has to be named with the number, because three different honest answers exist:**

| frame | count |
|---|---|
| served objects the control COVERS | **12** |
| independent byte-streams | **10** |
| **independent served FIGURES** (manifests excluded, twin collapsed) | **9** |

**The predecessor collapsed the `timeseries` twin (12 → 11) but not the `_manifests/latest.json`
pointer twin, and counted manifests as figures.** `latest.json` is byte-identical to its dated
target **by design** — it is a pointer, so it can never move independently.

⛔ **THE COVERAGE ITSELF IS NOT AFFECTED AND WAS NEVER WRONG — all 12 objects are digested and the
control is sound.** What was overstated is the number of *independent* things it checks, and that is
the direction that matters: **an inflated independence count makes a control look like it discriminates
across more surfaces than it can.** Two of the twelve cannot move on their own.

**Quote `12 objects / 9 independent served figures / 10 independent byte-streams`, and name which.**
A bare integer here is the exact shape of the denominator-without-its-frame defect — *nothing in the
number `11` says what it is 11 OF.*
