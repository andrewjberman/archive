# GC-BF0 — PULLER CAPABILITY ASSESSMENT for targeted backfill

**archetype:** VALIDATE
**Author:** `0.6.2_AE_PartnerETL~B` · **TO:** MDPF_3FIRMS.GC-BF0 @3b9ea142e (+ addenda @0a99ec058, CTO 152449Z)
**To:** `1.0.0_SA_CTO` (gate) · **CC:** `2.0.0_SA_COO`, `3.0.0_SA_CVO`
**Completed:** 2026-07-24T15:32Z · **Repo vintage:** all `file:line` below @ `8d9158b500`

---

## BOTTOM LINE — read this first

**BOTH PULLERS FAIL (B). NEITHER MAY BE USED TO BACKFILL. VERDICT: `NOT-CAPABLE` FOR BOTH.**

Neither SmartX nor Eclipse can target a historical date. Both accept a `--date`, both ignore it, both land
**the run date's data under the key you asked for, at exit 0**. This is the exact failure Andrew named at
~1452Z, and it is present in *both* systems, not one.

**THE COLLECTION ORDER (~1509Z) CANNOT BE EXECUTED AS WRITTEN.** Running either puller against the target
dates would produce 22 dates of fabricated history, a continuous-looking chart, and a **passed visual smoke
test**. COO's 151103Z read is correct and this assessment confirms it at source.

**ONE DATE LOOKED RECOVERABLE WITHOUT ANY PULL — AND ON EXAMINATION IT IS NOT LANDABLE.**
**2026-05-21 INF = 399 accounts** sits in our own retained S3 object-version history. It is serving-stable
across 6 retained versions, but it is **byte-identical to the previous trading day's roster**, it comes
from an artifact source-documented as carrying mis-stamped dates, and **no mechanism exists to land it that
survives a producer run**. CTO ruled `(iii)` at 160933Z: **ZERO RECOVERED**. Preserved as
MEASURED-BUT-UNLANDABLE. See §3 for the find and **§3a for the corrections and the ruling** — §3a governs.

---

## §0 — Denominator and scope

| Item | Value |
|---|---|
| Systems in scope | 2 (SmartX/49F, Eclipse/INF). Cottonwood OUT — sovereign-settled, **not assessed, not probed** |
| Pullers assessed | **2 of 2** |
| Dates in scope | SmartX 21 · Eclipse 6 (CTO 152449Z: 05-21, 06-01, 07-01, 07-13, 07-14, 07-15) — **the 5 overlap** |
| Dates EXCLUDED as not-historical-pulls | **2026-07-20, 2026-07-21** — coverage-frontier/lag-window cause, owned by GC-BF1. Stated, not silently omitted |
| Coverage axis used | **429 trading days**, per the addendum. Not 447 |
| **Bytes written by this assessment** | **ZERO.** Every probe read-only (`s3 ls`, `s3api get-object` to scratchpad, source reads). No bucket, partition, or artifact was written |
| NEVER#4 | **Affirmed.** No ad-hoc gold run was triggered. Nothing here validates against one |
| Vendor egress | **NONE.** I called neither the SmartX nor the Eclipse API. All evidence is source + our own buckets |

### §0a — THE ECLIPSE EGRESS QUESTION, NAMED (per COO 153210Z [HARD STOP])

**Eclipse is NOT on the standing vendor-egress lift list** (ORION · SMARTX · cot-BD · arxiv). **No Eclipse
API call was made in producing this assessment, and none is pending.**

**It did not need one, and that is a substantive result rather than a dodge.** Eclipse's (A) and (B) are
**source-determined**: the puller's own code shows `--date` reaching nine label sites and zero request sites,
and all four consumed endpoints are literal current-state paths. A vendor call could not have *changed* that
verdict — it could only have confirmed a fabrication I can already predict from source. So the Eclipse
verdict is **`NOT-CAPABLE` (source-confirmed)**, **not** `CAPABILITY-UNDETERMINED — requires egress`.

**Where egress would be required, and is therefore an open Andrew-word item:** any attempt to obtain the 5
permanently-unfillable dates (06-01, 07-01, 07-13, 07-14, 07-15) from a *different* Eclipse surface — e.g.
the `/auditlog/*` family, the only paths in the vendor's 493-path catalog carrying date parameters. **I did
not probe it and am not recommending it**; the catalog is an Orion-published OpenAPI doc read on-box. If CTO
wants that avenue explored it needs Andrew's explicit per-use word first.

**SmartX egress is lifted, and I still made no SmartX call** — the source read plus our own buckets answered
it, so the lift went unused.

---

## §1 — ECLIPSE (INF) · `data/inf/scripts/bronze/pull_eclipse_portfolios.py` @8d9158b500

### A. TARGETING — **FAIL**
`--date` is declared at **:288-292** and resolved at **:299** (`args.date or now UTC`). It reaches **nine**
sites — :301 log, :325/:335/:345/:360 S3 keys, :376 sentinel field, :390 sentinel key, :398 log — and **not
one is a request**. `eclipse_get(path, eclipse_jwt, timeout)` at **:254** has **no date parameter**; the four
data endpoints are literal current-state paths (**:319, :329, :339, :352**), the only interpolation being
`eclipse_id` at :349.

**Flag exists, flag does not work.** It is an output filename.

### B. FIDELITY — **FAIL (structural, not fixable by adjustment)**
No date reaches the vendor, so the payload **is** current state. The sentinel writes `"date": date_iso`
(**:376**) — **the artifact self-certifies the false vintage**. There is no content field carrying a vendor
as-of, because all four endpoints are current-state by construction. Per the vendor's 493-path catalog, date
parameters exist **only on `/auditlog/*`** — none of the consumed surface.

**No independent check exists ⇒ FAILS B regardless of A.**

### C. AVAILABILITY — **N/A** (the vendor exposes no historical read on this surface)
### D. SAFETY — **ACTIVELY UNSAFE**
A run writes `bronze/eclipse/{date}/` **plus `_meta/pull_complete.json`**. The mirror carries it to the
monolith and silver converts it — **a fabricated partition propagates downstream**. Note the guardrail trap
already recorded at :17-20: *"verify ABSENT, never overwrite" PASSES* — the partition genuinely is absent and
the write genuinely is additive. **A careful, rule-respecting operator is the one who produces the corruption.**

### VERDICT: **NOT-CAPABLE** — applies to all 6 Eclipse dates.

---

## §2 — SMARTX (49F) · `data/mdpf/scripts/feeders/wsb_49f_smartx_model_aua.py` @8d9158b500

### A. TARGETING — **FAIL, and in the most dangerous shape of the two**
`--date` at **:281-282**, threaded as `as_of` through `build()` **:216** → `pull_model()` **:137**. The three
data calls are current-state: `models/{model_id}` **:148**, `enterprises/allocations?modelid={model_id}`
**:153** (query string carries **only** `modelid`), `reportedmodels/{rmid}/holdings` **:179**. `api_get`
**:107-113** builds `Request(f"{API}/{path}")` with no params. The single `data=` in the file (**:101**) is
the OAuth ROPC token POST — not a data request, and carries no date.

`as_of` terminates in exactly two places:
1. **the S3 key** — `f"{FEEDER_PREFIX}/{artifact}/{PARTNER_FIRM_ID}/{date}.parquet"` **:247**
2. **a data column** — `"as_of_date": as_of` at **:168, :190, :202**

> **⚠ THIS IS WORSE THAN ECLIPSE AND IT IS THE FINDING I MOST WANT ON THE RECORD.**
> Eclipse stamps the false date into a *sidecar sentinel*. SmartX stamps it into the **`as_of_date` DATA
> COLUMN of the served parquet** — precisely the field a downstream verifier would reach for as a
> "content-side" check. **The forbidden evidence is manufactured inside the data itself**, so a check that
> reads `as_of_date` would confirm the fabrication with perfect confidence. Any future backfill acceptance
> criterion that names `as_of_date` is not a control.

### B. FIDELITY — **FAIL, on three independent grounds**
1. **No vendor as-of.** Independently established before me: `mdpf012_smartx_historical_probe.py` probed 8
   date-param variants (`asOfDate`, `date`, `from`/`to`, per-account and statistics history, discovery
   endpoints) and **came back NO** — recorded verbatim in `mdpf012_smartx_bucket_history_probe.py:4`
   (*"After the REST historical probe came back NO"*).
2. **No internal reference.** `0.4.0_DS_ClientPlatform~A` (151936Z) measured the estate at the required
   grain: custody `fact_rps_s2` has full history but **no model attribution**; `fact_model_aum_daily` has
   **no account-count column**; the roster is latest-only. **I independently confirmed the served-artifact
   half** (§4) — the 21 dates are absent from *every* retained 49F version's axis.
3. **The only self-describing field is puller-stamped** (A, above).

### C. AVAILABILITY — **NOT AVAILABLE at the required grain**
Live enumeration of `s3://opal-data-smartx-v2` (read-only):

| Prefix | Contents | Verdict |
|---|---|---|
| `daily/` | **5 objects**, all frozen **2026-01-02** | not a per-date history |
| `timeseries/` | **5 objects**, all frozen **2025-12-26** | not a per-date history |
| `raw/enterprise_aum/` | **1 object** — `49_financial_group_daily_aum.csv`, **1,383 daily rows, 2020-06-29 .. 2025-12-26** | **real per-date history, wrong quantity** |
| `consolidated/` | monthly-grain allocations (`PeriodEndDate`) | wrong grain |

The CSV is the only genuine per-date artifact and it **does cover 2025-12-24** (`$1,365,466,497.81`). But its
columns are `Enterprise, AUM, PerformanceDate` — **enterprise-level AUM with no model split and no account
count.** It cannot supply the count axis, and it stops at 2025-12-26 regardless.

### D. SAFETY
Writes `s3://opal-data-mdpf/mdpf/feeds/{artifact}/{firm_id}/{date}.parquet` (**:241-251**). No completion
sentinel fired from this script — but see the standing Door-6 rule: `gold/meta/pipeline-complete.json` must
never be hand-written.

### VERDICT: **NOT-CAPABLE** — applies to all 21 SmartX dates.

---

## §3 — THE RECOVERABLE DATE: 2026-05-21 needs no pull at all

**The originally-named Eclipse date is already in our possession.**

`s3://opal-data-portal-v2/json/mdpf/inflection/aggregate-aua-timeseries.json`, version
`u1V7X3xHgkPAPChJhpyh1Hk50aOWLAgO` (LastModified **2026-07-08T15:00:43Z**), carries non-null
`by_model[*].account_count` at axis index 394 = **2026-05-21**:

| model | account_count |
|---|---|
| opal_intermediate | 159 |
| opal_blend_5050_int_ltc | 127 |
| opal_long_term_conservative | 54 |
| opal_blend_5050_st_int | 21 |
| opal_long_term_aggressive | 23 |
| opal_short_term | 10 |
| opal_ultra_short_term | 5 |
| **TOTAL** | **399** |

**Corroboration: 6 independently-written retained versions** (07-08 ×3 distinct VersionIds, 07-16, 07-17,
07-18) **all carry 399** on that date. The two current revamp-schema versions carry **NULL**. Count coverage
in the legacy artifact spans **35 of 426 dates, 2026-05-18 .. 2026-07-08** — 05-21 sits inside it.

**The other 5 Eclipse dates are NOT recoverable this way** — 06-01, 07-01, 07-13, 07-14, 07-15 are
`noaxis` (absent from the axis entirely) in every legacy version, and NULL in the current ones. This matches
the Eclipse puller's own recorded position that those gaps are *"RECORDABLE AND PERMANENTLY UNFILLABLE."*

---

---

## §3a — AMENDMENT (2026-07-24T16:14Z): the 399 is NOT LANDING. Outcome = ZERO RECOVERED.

**CTO ruled (iii) at 160933Z. `2026-05-21` ships as an honest-None with the other 20. Nothing was written.**

**The ruling was on MECHANISM, not on the value.** There is no clean upstream repair for INF:
`load_served_account_count` is **49F-only** (`:743`); INF derives `account_count` from the eclipse
`per_date` snapshot (`:966`, `:971`), so an honest upstream repair would need an Eclipse snapshot for
2026-05-21 — which §1 establishes cannot be obtained at any permission level. The only remaining mechanism
was an in-place served write, and the current revamp versions carry 05-21 as NULL, so **the next producer
run would silently revert it** — a repair with a hidden expiry, noticed first by Andrew at a later smoke
test. A visible gap beats an invisible un-landing.

### THREE CORRECTIONS TO §3, ALL AGAINST MY OWN EVIDENCE

1. **The legacy artifact has NO `account_count_total` field.** That field exists only in the revamp schema.
   The 399 was **my own sum of seven per-model cells**, presented above as a read value. It resolves
   correctly — but *it resolves because I measured it, not because I knew it*.
2. **05-20 is 399, not 401** (my 154857Z handoff read only the tail of a two-control run; CVO and CTO both
   inherited the error from me). The coherence line is **399 / 399 / 401**, not 401 / 399 / 401.
   **AND 05-20's seven per-model cells are BYTE-IDENTICAL to the 05-21 claim** — 159/127/54/23/21/10/5 —
   with 05-18 and 05-19 also at 399. So the recovered value is **indistinguishable from the immediately
   preceding day's roster**, which is exactly what a carry-forward or mis-stamp looks like. The corrected
   numbers make the evidence *weaker*, not stronger.
3. **"6 independently-written versions" overstates it** (CVO relabel, accepted). All versions are successive
   publications by the same producer reading the same upstream silver. Distinct ETags prove distinct
   *writes*, not distinct *derivations*. What RC-1 establishes is **SERVING-STABILITY**: 399 is what we
   stably served for 05-21 until the revamp schema dropped it. CVO's independent close is genuinely
   stronger than my claim was: 9 distinct ETags, and the axis GREW 426→429 across the concordant set, so
   399 survived four re-derivations that changed the series shape.

### THE MIS-STAMP RISK — REAL, BOUNDED, AND IRREDUCIBLE AT THIS DATE

The legacy INF served artifact is source-documented as carrying **mis-stamped dates** (`:966-982`: *"legacy
07-06 holds the 07-10 snapshot, 07-18 holds 07-20 … 2026-07-06 carried 540 (eclipse's 07-10 roster) beside
the true count of 474"*). **RC-1 is structurally blind to this**: it tests concordance across versions, and
a systematic mis-stamp is inherited by every version that copies it forward. **Agreement measures
propagation, not truth.**

Bounding measurement — LEGACY vs CURRENT (eclipse-derived, a genuinely different axis), **denominator 28**:

| | |
|---|---|
| AGREE | 26 |
| DISAGREE (the complete mis-stamp set) | 2 — `2026-05-28` (402/403, −1) and `2026-06-24` (472/467, +5) |
| 05-21 neighbourhood | 05-18, 05-19, 05-20, 05-22, 05-26, 05-27 — **exact agreement, zero drift** |

So the defect is sparse (~7%), small, and absent from the target window. **But 05-21 itself can never be
cross-checked — it is null in current precisely BECAUSE it is the gap.**

> **THE UNVERIFIED REMAINDER IS EXACTLY THE TARGET SET.** Every date we want to repair is, by construction,
> outside the test that would validate the repair. That is a structural property of this class of work, not
> a gap in the check.

### THE PRESERVED VALUE — record it WITH its doubt

```
2026-05-21 INF account_count = 399  (159/127/54/23/21/10/5)
  source     retained version u1V7X3xHgkPAPChJhpyh1Hk50aOWLAgO (2026-07-08T15:00:43Z)
  evidence   serving-stable across 6 retained versions; 9 distinct ETags; survived 4 axis
             re-derivations (426->429); DISTINCT not inflated-sum (total == per-model sum, 40/40)
  DOUBT      byte-identical to 2026-05-20's roster; unverifiable at this date by construction
  STATUS     MEASURED-BUT-UNLANDABLE / UNVERIFIABLE-AT-DATE
  IF LANDED  must NOT carry class `measured` (COO condition, endorsed)
```

### CLASS-C COMPOSITION — CVO right, my doubt wrong

I hypothesised that 05-21's `count_provenance = exempt_absorbed` **forces** None regardless of INF, which
would have made the restore a no-op. **Source-checked before asserting it, and I was wrong:** at
`:1719-1733` the None decision is taken FIRST by `any(c is None for c in core_cells)`; `exempt_absorbed` is
only the **label** applied afterwards. Filling INF's cells would flip the branch. Measured brackets —
Global 05-20 = **7279**, 05-21 = **None**, 05-22 = **7299**; CVO's ~7,281 sits in the bracket as an
**estimate-in-range, not a measurement** (the composition was never run).

**Axis note:** the Global served artifact is on the **447** axis and 38 `exempt_absorbed` dates include
weekends (05-30/31, 06-06/07, 06-20/21, 06-27/28, 07-04/05, 07-11/12). 05-21 is a Thursday and a genuine
trading-day exemption. Counting that set on the wrong axis yields a wrong denominator.

---

## §4 — 49F: no internal recovery path, and a correction worth keeping

I ran the same version-history recovery check on the 49F served key across **7 retained versions**.
**0 of the 21 dates are recoverable.** They are absent from every legacy axis — never null-on-axis, simply
never there. This independently confirms DS~A's finding by a different route.

**A structural correction found on the way** — the 22 dates present on the legacy (07-18) axis but absent
from the current axis are **market holidays**: 2024-11-28, 2024-12-25, 2025-01-01, 2025-01-09, 2025-01-20,
2025-02-17, 2025-04-18, 2025-05-26, 2025-06-19, 2025-07-04, 2025-09-01, 2025-11-27, 2026-01-19, 2026-02-16,
2026-04-03, 2026-05-25, 2026-06-19 … each carrying a *non-null* count.

**The legacy axis was holiday-polluted and the revamp correctly replaced it with a trading-day axis.** Those
legacy holiday counts were never real observations. This supports the addendum's **429, not 447** instruction
and is a reason to distrust legacy counts as a reference on non-trading days specifically.

---

## §5 — THE INDEPENDENT DATE-CHECK, with its positive control (per addendum @0a99ec058)

Both pullers fail B, so there is no pull to verify. The check below is therefore defined for **the §3
recovery path**, which is the only landing this assessment clears. CVO can run it without me.

```
CHECK  RC-1 (version-concordance recovery check)
GIVEN  a target date D and firm F
  1. aws s3api list-object-versions --bucket opal-data-portal-v2 \
       --prefix json/mdpf/<F>/aggregate-aua-timeseries.json
  2. For each retained VersionId: get-object, locate D in .dates
  3. PASS iff D is ON the axis in >= 2 versions with DISTINCT LastModified,
     by_model[*].account_count is non-null in each, and ALL versions AGREE exactly.
  4. FAIL if D is off-axis, null, or versions disagree.
```

**WHAT WOULD HAVE HAD TO BE TRUE FOR IT TO COME BACK NEGATIVE — and how I exercised it:**

| Negative case | Exercised on | Result |
|---|---|---|
| Date off-axis | the 5 other Eclipse dates (06-01, 07-01, 07-13, 07-14, 07-15) | **flagged ABSENT, 5/5** |
| Date off-axis (non-trading) | weekends 2026-05-23 (Sat), 2026-05-24 (Sun) | **flagged ABSENT, 2/2** |
| Date on-axis but null | 2026-05-21 in the two current revamp versions | **flagged NULL** |
| Whole-set negative | all 21 dates on the 49F key | **flagged unrecoverable, 21/21** |
| Positive control | 2026-05-20, 2026-05-22 (healthy neighbours) | **PRESENT — check does not just say no** |
| Agreement control | 407 dates shared between two 49F versions | **0 disagreements** |

**The check demonstrably returns negative on dates that should be present and are not.** It is not an
instrument that can only confirm.

> **A DEFECT I CAUGHT IN MY OWN INSTRUMENT, recorded because it is the same class this TO is about.** My
> first recovery predicate tested `new[date] is None` — which **silently skips dates absent from the new axis
> altogether**, and returned a confident `0 recoverable`. That is a false negative produced by a
> dict-lookup hole, and it would have buried §3. It was caught only because the arithmetic did not close
> (429 non-null vs 407 shared). **A retrieval that cannot distinguish "null" from "not present" is the same
> failure as a puller that cannot distinguish D from the run date.**
> Likewise my first date-param search used `params=` and found 0 across 25 bronze pullers — **not because
> Eclipse is clean but because no puller in the estate uses `params=` at all.** The corrected pattern found
> cot's real `startDate`/`endDate`/`asOfDate` body params, proving it discriminates. (cot was used **only as
> a control corpus for my instrument** — it was not assessed, per the Cottonwood boundary.)

---

## §6 — RECOMMENDATION to CTO's gate

1. **Do not issue a backfill TO against either puller.** Both are `NOT-CAPABLE`; per the verdict schema, no
   backfill TO may issue against a puller that has not passed B.
2. **Do not execute the collection order as written.** It would fabricate and it would pass the smoke test.
   This needs to reach Andrew **before** anything is collected — it is his own named failure mode.
3. **Land 2026-05-21 = 399 from the retained version** (§3) under check RC-1. One real date, fully verified,
   no vendor call. This is the only date this assessment clears.
4. **Report the remaining 20 as `unavailable-upstream` / honest-None**, not as pending backfill. Per the
   TO's missing-third-state rule these are **not** `NEEDS-ADJUSTED-VERSION` — no adjustment to either puller
   can create a vendor-side historical read that does not exist.
5. **Exclude 2026-07-20 / 07-21** — coverage-frontier repair, GC-BF1.
6. **Flag for whoever writes the next acceptance criterion:** `as_of_date` on the SmartX parquet is
   puller-stamped and must never be used as a fidelity check.

**The honest headline for Andrew:** *the counts for those dates were never captured, and neither vendor will
sell them back to us. We can restore one date truthfully. The rest are a gap we should show as a gap.*
