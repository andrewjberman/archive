# ADVI_INSURE TO-R1-DS — AC2 DESIGN LIMB + AC3 FORBIDDEN-FIELD CENSUS

**Seat:** `0.4.0_DS_ClientPlatform~R` (S4) · **Under:** `2.0.0_SA_COO` GO 76135, ruling 76226
**Taken:** 2026-08-27 ~17:0x–17:2xZ · **Cells:** `INS-c-1`, `INS-c-2`, `INS-c-3`, `INS-inv-1`
**Predecessor:** the INS-a-2 occupancy census (@f05d754d43) — every number below is checked against it.

---

## 0. ⛔ THE FRAMING I ARRIVED WITH WAS WRONG, AND CORRECTING IT CHANGED THE ACT

I reported to COO that my next step was the gold table **DESIGN** limb. **The gold table already exists**
and has since 2026-08-26T00:16:34Z:

```
s3://opal-data-49financial/gold/advi/insurance/insurance_nav_current/date=2026-08-25/data.parquet
```

**106 rows x 15 columns.** So the act this round needed was **VERIFICATION of a landed artifact**, not
authorship of a new one. Designing a table that exists would have produced a second producer for one
served key — the exact defect AC4 names.

I found it in **my own 08-26 deliverable**, which cites the path in its own evidence block. *The artifact
was in a document I wrote, and I still opened the round intending to author it fresh.* Recorded because
the corrective is mechanical, not attentional: **before authoring, list the destination prefix.**

⚠ **PATH NOTE:** AC2's candidate is `opal-data-49financial/gold/advi/` + `insurance_nav_current/date={D}/`.
The landed key carries an extra `insurance/` segment: `gold/advi/**insurance/**insurance_nav_current/…`.
Recorded as a deviation from the TO's candidate wording. **Not** flagged as a defect — the candidate was
written as a candidate, and the extra segment is consistent with the tree's `canonical/` + `dimensions/`
sibling grouping. Issuer's call if it matters.

---

## 1. AC2 CONFORMANCE — denominator 106 rows

| AC2 requirement | measured | verdict |
|---|---|---|
| ONE additive current-state gold table | 1 key under `gold/advi/insurance/` (denominator: 11,741 keys swept in `gold/advi/`, 1 insurance-bearing) | **HOLDS** |
| in `opal-data-49financial/gold/advi/` | yes (+ `insurance/` segment, s.0) | **HOLDS** |
| **one row per insurance account per `asOfDate`** | rows **106** · distinct `bd_account_id` **106** · distinct (`bd_account_id`,`as_of_date`) **106** — all three equal | **HOLDS** |
| carrying the spine keys account → relationship → advisor → firm | account ✔ · relationship ✔ · **advisor ✘** · firm ✔ | ⛔ **3 of 4 — see s.3** |

### Value parity bronze → gold, end to end

| | bronze (census) | gold | |
|---|---|---|---|
| account records | 106 | 106 | match |
| null NAV | 4 | 4 | match |
| **sum `current_emv`** | **51,807,815.31** | **51,807,815.31** | **exact** |

**The 4 unvalued accounts ride as rows with a NULL NAV** — not dropped, not `fillna(0)`. COO build-changer
(3) is satisfied *by the existing artifact*, not by anything I did this round.

### Vintage — build-changer (2), satisfied

`as_of_date` is carried **per row**, and its distribution reproduces the census exactly:

| `as_of_date` | gold rows | census (bronze) |
|---|---|---|
| 2026-08-24 | 99 | 99 |
| 2025-11-17 | 4 | 4 |
| 2024-03-28 | 2 | 2 |
| 2026-02-06 | 1 | 1 |

**The partition is `date=2026-08-25` (run date) while the rows carry four different real vintages.** The
hazard I flagged — one run-date stamp mislabelling 7 of 106 — **does not occur**: the partition dates the
*capture*, the column dates the *value*. `as_of_date` is null on **0 of 106**, which is what makes COO's
76226 ruling (`asOfDate` canonical, 106/106 coverage) implementable; `currentEmv.asOf` is correctly **not**
carried as a second date field.

---

## 2. AC3 — FORBIDDEN-FIELD CENSUS, PRINTED

**Denominator: 15 gold columns.** Token set (16): `return, twr, irr, performance, series, benchmark,
alpha, beta, sharpe, yield, ytd, mtd, qtd, since_inception, cagr, annualized`.

Full schema, enumerated, **no ellipsis**:
`bd_account_id, bd_account_number, account_id, account_id_basis, relationship_id, firm, spine_class,
advisor_basis, carrier, product, current_emv, as_of_date, source_pipeline, schema_version, _ingested_at`

### **HITS: 0.** No analytics, no returns, no series field.

**POSITIVE CONTROL ON THE MATCHER** — a zero from an unexercised matcher is worthless. Probe set
`[current_emv, twr_1y, carrier]` → matcher flags **exactly `twr_1y`**. It discriminates: the 0 above is a
measured absence, not a dead predicate.

**Upstream corroboration, different substrate:** the census ran the same probe over the 34 distinct
*source* keys → also 0. The forbidden set is absent both in what arrives and in what is built.

> **A snapshot plane that grows a series has become an AM calculation.** Today it has not. This is a
> property of one vintage, and it is a re-take at every emission, not a closed verdict.

---

## 3. ⛔ THE ONE REAL GAP — the advisor spine hop, and its stamp overstates

**Measured on all 106 rows:** `advisor_basis = NOT-DERIVABLE-UPSTREAM` (106/106) ·
`spine_class = unassigned` (106/106) · `account_id` **null 106/106** with
`account_id_basis = NOT-DERIVABLE-UPSTREAM` (106/106).

`relationship_id` and `firm` are fully populated. **So AC2's "every aggregation is a JOIN, never a
computation in the frontend" holds for relationship and firm rollups and DOES NOT HOLD for advisor.**

### Three routes to the advisor hop. I measured all three; none was taken.

| # | route | status |
|---|---|---|
| 1 | `relationship.teams[]` on the landed `relationshipaccountdetailsearch` | **key present on 77/77, EMPTY on 77/77.** Genuinely cannot supply it. |
| 2 | `relationshipdetail` (S4) `financialTeam[]` — the AE's own AC2 map names this as the advisor carrier | ⛔ **SANCTIONED and NEVER CALLED** (see below) |
| 3 | a join to `a00`/`a01`, which PRD:84 names as the spine source | ⛔ **NOT DETERMINED BY ME** (see below) |

**On route 2, at source:** `insurance_leg.py:79` — `"relationshipdetail": (True, "")` — **egress
ALLOWED, not gated.** `:100` registers its route `GET /relationship/request/relationship/%s`. The vehicle
dispatches generically through `call_surface(surface, …)`, so it *can* call it. **It never did:** the
landed bronze holds exactly three surfaces — `insurancerelationshiplist`,
`insurancerelationshiplist_export`, `relationshipaccountdetailsearch`. **`relationshipdetail` has zero
landed objects.**

>> ⛔ **THEREFORE `NOT-DERIVABLE-UPSTREAM` IS THE WRONG CLAIM ON `advisor_basis`, AND IT IS WRONG IN THE
>> DIRECTION THAT CLOSES THE QUESTION.** "Upstream" asserts the source *cannot* supply it. Measured, the
>> source **can**: the surface is sanctioned, routed, and supported by the vehicle — it was simply **not
>> captured**. The honest stamp is `NOT-CAPTURED` / `PENDING-SURFACE`.
>>
>> **The two differ by permanence.** A frontend reading `NOT-DERIVABLE-UPSTREAM` concludes advisor rollup
>> is impossible and designs around its absence forever. The truth is one uncalled `GET` away. **This is
>> `A_VALUE_MUST_CARRY_ITS_CLAIM` failing in its subtle form: the field carries a claim, the claim is
>> populated, and it is false.** An absent field invites a question; a confidently wrong one ends it.

**On route 3, and I am not going to pretend I closed it:** PRD:84 says the spine keys come
"from `a00`/`a01`". **I did not establish what `a00`/`a01` resolve to** — no such table exists under
`gold/advi/` (11,741 keys swept), and the PRD names them without defining them at that line. If the
intended advisor route is a join to an ADVI dimension keyed on `relationship_id`, then route 2 is
unnecessary and the correct stamp is different again. **I am reporting an open fork, not a diagnosis.**

⚠ **AND `account_id_basis` IS A DIFFERENT QUESTION WITH A DIFFERENT ANSWER — do not fold them.** My
08-26 join established `account_id` is a **Schwab account number**, which an insurance policy at
Brighthouse or Allianz structurally does not have (0 of 106 join, positive control 200/200, negative
control 0/5,337). **`NOT-DERIVABLE-UPSTREAM` is CORRECT on `account_id_basis` and OVERSTATED on
`advisor_basis`.** Two fields, one stamp value, two different truths — and the shared string is exactly
what would let a reader carry the sound verdict onto the unsound one.

---

## 4. AC2 STATUS — as the issuer's split requires

Per the TO's ~21:0xZ amendment, AC2 reports as two limbs and never as one verdict:

- **DESIGN limb — `DESIGN-COMPLETE` with one named exception.** Schema, partition grammar, grain,
  null-carrying, vintage semantics and forbidden-field posture are all **landed and verified**, not
  merely specified. **Exception: the advisor spine hop (s.3), which is unresolved and mis-stamped.**
- **APPLIED limb — remains `APPLIED-GATED`.** One 2026-08-25 capture is a specimen, not a plane;
  `INS-b-1`/`INS-inv-4` still wait on `INS-a-1..3` at `0.6.0_AE_PartnerETL`.

**AC3** — the printed census is **s.2 above**, matcher positive-controlled. Its `INS-inv-1` half (the
byte-identity control on every existing AM figure) is **NOT taken in this document** and is not claimed:
it is a BEFORE/AFTER pair around a change, and no change has been made.

---

## 5. WHAT I DID NOT DO

- **No vendor call.** No egress at this seat; the 08-25 grant was per-use to the AE lane.
- **No write to any data plane.** Every act here was a read. The gold artifact is untouched.
- **I did not amend the gold table's `advisor_basis`.** It is another lane's landed producer output and
  the stamp change implies a producer change — surfaced, not adjudicated.
- **I did not call `relationshipdetail`,** and will not without Andrew's per-use word naming that surface,
  regardless of `SURFACE_EGRESS` reading `True`. **An allowlist entry is the code's permission, not the
  fabric's authorization** — the same distinction this project has already had to make twice.

---

**Instruments:** `s3api` direct reads (auto-paginated, client-side counts), pandas over the landed
parquet, source read at `insurance_leg.py:79,100,307-317`. **Denominators: 11,741 `gold/advi/` keys ·
1 insurance gold object · 106 rows · 15 columns · 16 forbidden tokens · 77 relationships · 3 landed
bronze surfaces of 6 registered.**
