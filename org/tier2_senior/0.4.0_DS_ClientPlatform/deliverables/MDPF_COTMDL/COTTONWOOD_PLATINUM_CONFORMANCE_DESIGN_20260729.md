# Cottonwood -> platinum: conformance design (interim + durable)

**Author:** 0.4.0_DS_ClientPlatform~A · **Gate:** 1.0.0_SA_CTO · **Date:** 2026-07-29
**Status:** DESIGN ONLY -- nothing here is built or deployed. Commissioned by CTO 161341Z
(Andrew-direct design brief), revised by CTO 161556Z + 162325Z.

> **Andrew's ask, as relayed:** a modified cottonwood publisher path for the interim that accounts
> for the interpolation, noted somewhere relevant; non-model restored so it displays; and the
> publisher writing CANONICAL NAMES to the CANONICAL PLATINUM FOLDER.
>
> **This design's headline answer: two of those three are already true, and the third does not need
> a modified publisher.** The recommendation is CONFORMANCE + ONE IAM GRANT + ONE LABEL FIX. No
> cottonwood-special producer, no publisher deviation, and therefore -- per item (e) -- no interim
> deviation to record, which is the best possible outcome for that item.

---

## 0. THE PREMISE CORRECTION THIS DESIGN RESTS ON (measure it yourself before trusting the rest)

CTO 161556Z §3 states: *"platinum/mdpf/cottonwood has NO underscore sibling and **every object is
stale at 2026-07-28T20:35:22Z**. Nothing wrote cottonwood today at all. So the working writer skips
cottonwood."*

**The second and third sentences are refuted. The publisher does NOT skip cottonwood.** Measured via
`head-object` (UTC-authoritative):

| key (`platinum/mdpf/...`) | LastModified (UTC) |
|---|---|
| `cottonwood/aggregate-aua-timeseries.json` | **Wed, 29 Jul 2026 16:15:32 GMT** |
| `cottonwood/account-distribution.json` | **16:15:31 GMT** |
| `cottonwood/aum-metrics.json` | **16:15:32 GMT** |
| `global/aggregate-aua-timeseries.json` | 16:15:32 GMT |
| `49financial/aggregate_aua_timeseries.json` | 15:05:22 GMT |

**The 16:15Z publisher fired and wrote all four firms including cottonwood, under canonical
hyphenated names.** Andrew's item (c) -- "the publisher writing canonical names to the canonical
platinum folder" -- **is already satisfied for cottonwood today.**

**How the wrong reading happened, and it is a banked trap:** `aws s3 ls` renders **LOCAL** time and
this host is UTC-4. The cottonwood objects list as `2026-07-29 12:15:31`, which is `16:15:31Z`. A
`20:35:22` local stamp on 07-28 is `2026-07-29T00:35:22Z` -- the overnight chain. *Reading an
`s3 ls` column as UTC shifts every conclusion by four hours and, across midnight, by a day.* This is
`feedback_aws_s3_ls_lastmodified_is_local_time_never_a_liveness_oracle`, live again.

### So what DOES skip cottonwood?

Two different writers, and only one skips:

| writer | key form | fired today | cottonwood? |
|---|---|---|---|
| `opal-assets-mdpf-portal-publisher` (`cron(15 16)`) | **hyphen**, canonical | 16:15:31-32Z | **YES -- writes it** |
| chain revamp stage (post-15:02:30Z fire) | **underscore** | 15:05:22Z | **NO -- skipped** |

The underscore writer skipped cottonwood because **STAGE6-REVAMP refused**: the cottonwood leg was
un-composed (`meta.composed_backfill` absent). That refusal was correct, and **its precondition is
now cleared** -- I composed the slice at 15:52:29Z (see §2).

---

## 1. WHY THE PAGE IS STILL THIN, IN ONE SENTENCE

**The publisher republished cottonwood faithfully from a gold tree that never received the fix,
because the accrual bridge is IAM-blocked.**

Served cottonwood after the 16:15Z fire (measured): `37,518 B`, `model_aua` **2/450**
(07-21..07-22), `non_model_aua` **0/450**, `partner_custody_total` **0/450**. That is Andrew's
screenshot exactly: one date span in Daily AUM Analysis, Period End Summary empty (no month-end lies
between two adjacent July dates).

The chain is:

```
 [staging]                          [canonical gold tree]                [platinum / served]
 gold/mdpf_revamp/cottonwood/  --->  portal/gold/mdpf/cottonwood/  --->  platinum/mdpf/cottonwood/
 aggregate_aua_timeseries.json       aggregate-aua-timeseries/            aggregate-aua-timeseries.json
 (COMPOSED 15:52:29Z -- GOOD)        {YYYY-MM-DD}.json                    (published 16:15:32Z)
         |                                    ^                                    ^
         |                                    |                                    |
         +----- build_portal_gold_accrual ----+                                    |
                *** BROKEN: AccessDenied ***       opal-assets-mdpf-portal-publisher
                wrote 0 of 11 planned objects              (working correctly)
```

**Exactly one link is broken, and it is not a producer and not the publisher.** The 15:45:21Z bridge
run died on its FIRST PutObject:

```
AccessDenied: PutObject on arn:aws:s3:::opal-data-assets/portal/gold/mdpf/49financial/
  aggregate-aua-timeseries/2026-07-27.json
User: assumed-role/mdpf-daily-runner-ec2-role/i-02448edb624a7a7cf
"because no identity-based policy allows the s3:PutObject action"
```

`"no identity-based policy ALLOWS"` = **MISSING GRANT**. Distinct from the 15:02Z legacy-emit failure
(`"with an EXPLICIT DENY"` = the intended writekill). Two AccessDenied on one role within an hour,
opposite in kind; they must never be reported as one issue. Crash on object 1 of 11 => **none** of
the 11 landed. CTO ruling 155914Z routes the targeted grant to AE~A.

---

## 2. WHAT IS ALREADY FIXED (ad-hoc, 15:52:29Z -- NOT production evidence)

`build_cottonwood_mdpf_slice.py --upload`, run locally under the ANDREW-DIRECT ~1602Z routing.

| | before | after |
|---|---|---|
| ETag | `dd4d21a84cc62b11bdaa385707447d66` | `a95153abc2e830a9bfd51344e140b1cd` |
| Size | 37,237 B | 80,429 B |
| `meta.composed_backfill` | **ABSENT** (the refusal predicate) | **PRESENT** |

`n_backfilled 44`, window `2026-05-28..2026-07-17`, `first_measured_date 2026-07-20`. Gates PASS
(absent-is-not-zero, strict-Opal, conservation, W-2b identity). Coverage `model 50 / non_model 6 /
custody 38` of 450.

**This unblocks the STAGE6-REVAMP refusal.** The composed slice is sitting in staging, correct and
waiting for a bridge that cannot write.

---

## 3. ITEM (b) -- ANSWERED, CLOSED, AND IT DECIDES (a)

**Is carrying the 07-23 interpolated `non_model` forward still correct? NO. Do not extend the
compose.** (CTO accepted 161556Z; recorded here because a design doc must carry its own reasoning.)

**`non_model_aua` is not a series. It is a DERIVED BALANCE** -- `partner_custody_total - model_aua`,
honest-None where either leg is absent (`build_cottonwood_mdpf_slice.py:407-409`, *"never
fabricated"*). On splice dates custody is absent, so the balance is **UNDERIVABLE, not missing.**
Those are different states; only one is a defect.

The guard already exists: the **W-2b identity gate** (`:668-676`) fails the build on
`"W-2b fabricated balance @{d}: non_model={nm} with total={t} model={m}"` -- precisely the shape an
extension would produce.

The compose reads the one-off at **exactly one value site**, `:586 oneoff["model_aua"]`. No path
reads `oneoff["non_model_aua"]` or `oneoff["partner_custody_total"]`. Deliberate and documented at
`:533-536`:

> *"NON-MODEL + CUSTODY stay the daily slice's honest-None: the fold sums only the cottonwood MODEL
> leg (set-equality proof 2026-07-29 001511Z: the 31-moved-date deltas == the one-off MODEL leg
> 31/31 to the cent; its ~$334mm non_model never participated)."*

**And the render agrees, independently** (DE, portal DEV `b0fc1e75`): `ModelPortfolios.tsx:792-794`
-- *"Per-firm Non-Model comes from the artifact's `non_model_aua` (zero pre-backfill = correct)."*
`non_model_assets.json` is **RETIRED estate-wide** (Andrew-direct ~0340Z), not missing.

> **The empty Non-Model band is both sides behaving correctly.** Nothing to produce, nothing to
> render differently. Andrew's "non-model restored so it displays" is, on the measured facts, a
> request to restore something that is correctly absent -- **this needs to go back to him in those
> words**, because it is the one place where the design declines to do what he asked and he is
> entitled to the reason.

### Second, independent reason not to re-serve the old interpolated payload (NEW -- measured here)

The interpolated artifact is on the **OLD assignment-date key convention**; the composed slice is on
the **value_date re-key** (G7). Overlap comparison:

| date | interp `model_aua` | composed `model_aua` |
|---|---|---|
| 2026-07-20 | 123,894,784.66 | 124,376,009.73 |
| 2026-07-21 | 124,376,009.73 | 125,407,303.88 |
| 2026-07-22 | 124,376,009.73 | 125,892,388.69 |

`interp[07-21] == composed[07-20]` exactly -- a **one-day shift**, which is the re-key's signature
(`:525-531` names it: *"first_measured becomes the earliest VALUE date (07-20 at the move, was
partition-keyed 07-21)"*). `interp[07-22]` repeats `interp[07-21]`, i.e. a carry, not a shift.

**LABELLED HYPOTHESIS, NOT A FINDING.** The shift is consistent with the re-key but I have not
source-confirmed the interpolated producer's keying. It is recorded because it changes the risk of
item (a): **splicing an assignment-date-keyed payload onto a value_date-keyed axis mixes two date
conventions on one series, silently.** Anyone implementing (a) must resolve this FIRST. I tested and
rejected the simpler explanation (that the difference is the G8 income residual): the deltas
(-481,225.07 / -1,031,294.15 / -1,516,378.96) do not match the residuals (~1.24-1.25mm) and are not
constant.

---

## 4. RECOMMENDATION -- CONFORMANCE, NOT A MODIFIED PUBLISHER

**Do not build a cottonwood-special publisher path.** The canonical path already serves cottonwood
correctly (§0); it is starved, not broken. Ordered:

| # | action | owner | gate |
|---|---|---|---|
| **1** | **IAM grant** for `mdpf-daily-runner-ec2-role`: `s3:PutObject` on `opal-data-assets/portal/gold/mdpf/*` -- the FULL write set the loop needs, not the single key in the traceback | AE~A | CTO 155914Z (already ruled) |
| **2** | Re-run the accrual bridge. Expect **11 planned, 8 written, 3 R4 errors** (`aum-metrics` sources absent for 49f/inflection/global = the declared-before-built WI-2 gap, expected) | DS | post-grant |
| **3** | Next publisher fire (`cron(15 16)`) carries cottonwood to platinum. **No code change anywhere.** | scheduled | none |
| **4** | **The label fix** (§5) -- the only data-side code change this design asks for | DS (~A) | CTO word, post-freeze |

**Do not race the publisher** (CTO 155914Z). One more fire carrying yesterday's vintages is accepted
and not client-visible-wrong.

**Acceptance is a SERVED-ARTIFACT read, never rc=0** (NEVER#5): after step 3,
`platinum/mdpf/cottonwood/aggregate-aua-timeseries.json` shows `model_aua` **50/450** spanning
`2026-05-28..2026-07-27` (up from 2/450). Report **all three series counts**, every time.

### THE GRANT'S ACCEPTANCE TEST MUST BE AN ACTUAL WRITE (DS base, measured from the run logs)

**The accrual bridge has NEVER successfully written a single object in its entire lifetime.** Full
denominator, no name filter: exactly **2** run logs exist under
`s3://opal-data-mdpf/telemetry/mdpf-daily-runner/accrual-bridge-runs/`, both today.

| run | outcome |
|---|---|
| `20260729T075310Z.log` (07:53Z) | planned the same 11, hit the same 3 R4 errors, last line **`"DRY-RUN -- nothing written"`** |
| `20260729T154521Z.log` (15:45Z) | crashed on PutObject #1, AccessDenied, **0 written** |

> **THE ONLY PRE-PRODUCTION EXERCISE OF THIS BRIDGE WAS A DRY-RUN, AND A DRY-RUN CANNOT CALL
> `PutObject`.** The IAM gap was not *missed* -- it was **structurally undetectable** by the one test
> that was run. The bridge was deployed ~07:45Z, "validated" at 07:53Z by a run that skipped the
> entire write path, and its **first-ever `PutObject` was its first production fire.** A dry-run
> validates PLANNING; it cannot validate PERMISSION, and those are the two halves of this tool.

**Consequence for step 1's acceptance, and this is binding:** the grant is accepted only on **an
actual write that lands a verified object** -- never a dry-run, never an rc=0 re-fire. Otherwise the
fix's validation carries the identical blind spot as the original failure.

*Second instance of one class in our standing record* (the Aug-1 ETFS item: *"Aug 1's production shot
must not be the attach path's first exercise"*). Here the production shot **was** the write path's
first exercise. **Two independent instances is a rule, not a fix** -- routed to CTO as such.

---

## 5. ITEM (d) -- THE LABEL DEFECT (the primary data-side deliverable)

**MEASURED on the object I wrote: 44 of 51 splice dates assert `non_model = "interpolated_estimate"`
with `confidence 1.0` over a value of `None`.** Sample, `2026-05-28`:

```json
model_aua = 454064.58 ,  non_model_aua = None ,  partner_custody_total = None
cohort_provenance = {"model":"interpolated_estimate", "non_model":"interpolated_estimate",
                     "custody":"interpolated_estimate", "confidence":1.0, ...}
```

**Cause:** `:587 row = dict(oo_prov[d])` copies the one-off's provenance row **verbatim**, including
labels for cohorts whose values the compose deliberately does not carry (§3). The values are right;
the labels lie about them.

This is CLAUDE.md's own clause, live: *provenance recording WHERE but not WHAT IT IS OF converts an
absence into a documented lineage, which is worse than no provenance on a missing constituent.* It
also blocks item (d) at the source: provenance cannot survive honestly to the screen while it
asserts estimates over None.

**Proposed fix -- label per cohort, from the value, not from the source row:**

```python
if d in splice:
    oo = oo_prov[d]
    row = {"date": d,
           "model":      oo.get("model", "absent"),   # the ONLY cohort actually spliced
           "non_model":  "absent",                    # underivable: custody absent -> balance absent
           "custody":    "absent",                    # never carried from the one-off
           "window_id":  oo.get("window_id"),
           "confidence": oo.get("confidence")}        # scopes to the model leg only
```

**Vocabulary question for CTO -- I am not overloading `absent` unilaterally.** `absent` currently
means *"no data exists."* A splice-date `non_model` is subtly different: *"inputs exist but the
derivation is not possible."* Options: (i) reuse `absent` (simplest; slight semantic widening);
(ii) add `underivable` to the enum (precise; **an enum change is a frontend contract change** and
needs DE). **My recommendation: (i) for the interim fix, (ii) only if DE independently wants the
distinction on screen.** Shipping a new enum value into a render that does not know it is the
failure mode this whole page has been paying for today.

Note `confidence: 1.0` sitting beside a `None` is the sharpest form of the defect and is removed by
scoping confidence to the model leg.

---

## 5b. THE SERVER-SIDE NON-MODEL LEG (CTO 163338Z + ANDREW-DIRECT ~1724Z)

**ANDREW-DIRECT, VERBATIM (CTO terminal, ~1724Z):** *"Yes if this can be done server-side that is
correct"* -- the balance is computed in the producer and STATED as a field; nothing derives it in the
browser.

> ### THE HEADLINE: IT IS ALREADY BUILT, ALREADY CORRECT, AND ALREADY IN GOLD.
> **There is no data-side work in this item.** The custody leg already reads the custodial holdings
> feed, the balance is already computed server-side and stated as a field, and the `NOT_MEASURED`
> flag is already retired. All of it is sitting in `gold/` waiting for the bridge.

### Q1 -- source binding, firm separation, or unimplemented? **NONE OF THE THREE. IT IS IMPLEMENTED.**

`build_cottonwood_mdpf_slice.py`:

```
:272   prefix = "blackdiamond/cottonwood/silver/fact_holdings/"      # the custodial feed
:385   "partner_custody_total": [(holdings_totals or {}).get(d) for d in dates]
:380   "non_model_aua": [ round(holdings_totals[dates[i]] - model_aua[i], 2)
:382       if holdings_totals[dates[i]] is not None and model_aua[i] is not None else None ]
```

**MEASURED in the artifact I wrote at 15:52:29Z:** `partner_custody_total` **38/450**, window
`2026-06-09..2026-07-27`. `meta.total_covered_dates` = 38.

**FIRM-SEPARATION STOP CONDITION: NOT TRIGGERED, and I checked before answering.** The producer reads
`opal-data-assets/blackdiamond/cottonwood/**` -- **cottonwood's own tree, from cottonwood's own
producer.** The NEVER-rule bars referencing *another* firm's bucket from a pipeline tree (bd <-> cot
<-> inf); this is same-firm, and it is already running successfully today. **Nothing here crosses a
boundary and nothing in this design proposes to.**

### The `NOT_MEASURED` flag is ALREADY RETIRED -- it survives only in the stale served copy

| artifact | `meta.non_model_aua_status` |
|---|---|
| **served platinum** (stale, what CTO quoted) | `"NOT_MEASURED (Rebalancer carries model assignment only)"` |
| **my gold slice** (15:52:29Z) | `"BALANCE = partner_custody_total - model_aua, derived where BOTH present (PRD three-quantity convention); honest-None where either leg is absent -- never independently sourced, never fabricated"` |

**The producer stopped declaring the quantity unavailable some time ago.** The served string is a
fossil of the pre-W-2b build. Retiring it honestly requires **no code change** -- only the bridge.

### Q2 -- the 6-vs-38, and it IS a finding: an ORDERING ARTIFACT

Measured on my composed slice: **38 dates carry BOTH model and custody; only 6 carry `non_model`.**
The 32-date shortfall is derivable and empty. Zero dates have custody without model.

**Cause, at source.** `:380-384` computes the balance in the **DAILY** build, where `model_aua` holds
only the **6 MEASURED** dates. The **COMPOSE** then splices in **44 backfill model dates** -- but
`:594` takes `non_model` from the daily slice verbatim and **never recomputes it.**

```
DAILY build : model 6   custody 38  ->  non_model 6      (correct at that moment)
COMPOSE     : model 50 (6+44)       ->  non_model STILL 6 (never recomputed)
                                        32 dates now derivable, still None
```

**The balance is computed before the model leg is filled, and never revisited.** The 6 that exist are
identity-clean (checked all 6: `custody == model + non_model` to the cent, e.g. 2026-07-24
`463,015,162.92 = 125,132,212.02 + 337,882,950.90` -- which ties to DS base's independent
`fact_holdings` reconciliation of 16,825 rows at `DELTA 0.00`).

**DO NOT "JUST RECOMPUTE THE 32." IT IS A PROVENANCE DECISION, NOT A CODE MOVE.** On those dates
custody is **MEASURED** and model is **INTERPOLATED**, so the balance would be
`measured - interpolated` -- a hybrid that is neither measured nor cleanly estimated, on a
client-facing series, at ~$330mm scale. Options:

| option | consequence |
|---|---|
| **(A) leave None** (status quo) | conservative; band starts 07-20; no hybrid quantity is ever emitted |
| **(B) compute + label the hybrid** | band populates from 06-09; needs a provenance value that says *derived against an interpolated model leg*; the frontend must be able to render it distinctly, or it lies by omission |

**My recommendation: (A) for the interim, (B) only as a deliberate co-signed decision with DE.**
Rationale: (B) triples the visible band by adding a quantity whose estimated component is invisible
unless the render is changed first -- **precisely the "a backfill that arrives on screen
indistinguishable from measured data is worse than the gap" rule in item (d).** (A) is honest and
ships today with the grant.

### Q3 -- THE HONEST LIMIT, STATED PLAINLY

`fact_holdings` begins **~2026-06-09**. So even done perfectly, `partner_custody_total` populates
from June and `non_model_aua` no earlier. Under option (A) the Non-Model band starts **2026-07-20**;
under (B), **2026-06-09**. **Neither spans the 450-day axis, and no fix can make them.**

> **Andrew must not be told "non-model is fixed" and then see a band that starts in June.** The
> correct sentence is: *"Non-model now populates from [date], which is as far back as cottonwood's
> custodial holdings exist. Earlier dates are not missing -- they are outside the data."*

---

## 6. ITEMS (c), (e), (f)

**(c) Canonical conformance -- ALREADY MET for cottonwood.** All four firms now carry hyphenated
`account-distribution.json`, `aggregate-aua-timeseries.json`; cottonwood additionally has
`aum-metrics.json` + `account-units.json`. `non-model-assets.json` is **retired** -- do not create
it (CTO retraction 162325Z).

**Grammar trap, standing:** publisher grammar `^([a-z0-9_-]+)/([a-z0-9-]+)/(\d{4}-\d{2}-\d{2})\.json$`
-- **SCOPE allows underscores, TYPE does not.** A rejected key leaves `all_present` TRUE (computed
over the DERIVED set, which a rejected key never enters) => **a green run that serves nothing.** The
accrual is safe by construction: `:235` builds the key from `t['name']` (hyphen), while the
underscore `t['source']` is quarantined to the `:216` staging read. Date component is guarded by
`_valid_date()` `:178-185`, which fails CLOSED (`:230` *"NEVER fall back to the run date"*).
*Residual, exercised: `_valid_date` accepts ISO week-dates (`2026-W01-1`, 10 chars) on py3.11+, which
the publisher grammar rejects. Measured on local py3.12.10; runners are py3.9 per Rule 15 where this
cannot occur -- that half is INFERRED, not measured.*

**Open, not owned here:** the **underscore** platinum keys (`aggregate_aua_timeseries.json`, 15:05:22Z,
three firms, no cottonwood). Under the grammar these could never have come from the publisher. A
second writer maintains a parallel plane. Nothing in this design touches it, but **an unowned second
writer on a client-facing prefix is worth a ruling** -- flagging, not adjudicating.

**(e) Where it gets noted -- THIS DOCUMENT.** Andrew asked for a durable record of the interim
deviation. **The recommendation produces no deviation:** no modified publisher, no special-case, no
non-canonical name. What needs recording instead is (1) the missing grant and its fix, (2) the label
defect and its fix, (3) item (b)'s ruling that the non-model absence is CORRECT -- all above. If CTO
still wants a ledger entry, this file is the referent.

**(f) The 450-day axis vs ~2 months of cottonwood history.** No artifact -- including the
interpolated one -- has cottonwood data before **2026-05-28**. The axis runs to 2024-11-01, so ~88%
of it is structurally unfillable. **Not a defect: data availability.** But a chart that promises 450
days and can fill 50 reads as broken to Andrew regardless of correctness -- which is precisely what
happened today. **My input (DE owns the call): span the axis to the firm's own data envelope, or mark
the pre-history region as out-of-coverage rather than empty.** Rendering "no data" and "not yet a
client" identically is the same absent-vs-underivable confusion as §5, one layer up.

---

## 7. WHAT THIS DESIGN DOES NOT DO

- **Does not extend the compose** (§3) -- would fabricate a balance and launder ~$334mm.
- **Does not create `non-model-assets.json`** -- retired estate-wide today.
- **Does not build a cottonwood-special publisher** -- the canonical one already serves it.
- **Does not touch IAM** -- AE~A's lane, CTO-ruled.
- **Does not deploy.** Design only. Freeze holds post-17:15Z; fires and the grant outrank this.

**Ad-hoc labelling (NEVER#4):** exactly one ad-hoc write today on my lane --
`gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json` at 15:52:29Z, by me. **Not production
evidence; must not reach CVO's D2 certification.** The 16:15Z publisher fire remains valid
*unattended* D2 evidence -- an ad-hoc producer upstream does not taint the publisher's schedule claim.
