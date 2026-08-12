# Task Order: OPAL_BRDSEP.T1 -- Opal asset base, segmented, 2026-04-01 -> 2026-08-11

<task_order>
<to_id>OPAL_BRDSEP.T1</to_id>
<title>Establish the total Opal asset base by segment over 2026-04-01 -> 2026-08-11, plus client/account deltas</title>
<issued_to>0.4.0_DS_ClientPlatform~O</issued_to>
<issued_by>1.0.0_SA_CTO</issued_by>
<coordinator>2.0.0_SA_COO (informed)</coordinator>
<issued>2026-08-12</issued>
<status>complete</status>
<!-- ACCEPTED by 1.0.0_SA_CTO 2026-08-12 ~1850Z. Evidence: deliverable @7d46e2d79d + window-asymmetry
     addendum @22e0471761 + proof-of-spec VALID @64447ad426 (9 rows, 0 violations, 8 PASS / 1
     UNCOMPUTABLE-BY-CONSTRUCTION). CTO-INDEPENDENT VALIDATION, not a rubber stamp: (a) the four
     segment end-values sum to the stated $1,839,005,286.29 EXACTLY; (b) the Inflection figure
     $144,978,896.75 matches my OWN pre-dispatch by_model measurement to $0.25 (rounding) -- an
     independently-derived witness, not a re-read of their output; (c) all six coverage ratios
     re-derived by datetime diff, 132-day window confirmed, 6/6 match.
     ASSIGNEE EXCEEDED THE TO ON THREE AXES: corrected hazard #1 at source (silver/netassets/ 353
     partitions DOES span both endpoints -- my enumeration caught only the sibling silver/holdings/,
     so Andrew's pre-authorised 05-15 fallback was never needed); found a FOURTH hazard of the same
     class the TO did not carry (Cottonwood has no April-1 baseline either, point_class=absent not
     zero, $136.5M); and closed a half-met instruction of mine UNPROMPTED (the "by how much" on the
     window asymmetry) rather than leaving it for review to catch.
     THE FINDING THAT OUTRANKS THE MEASUREMENT: coverage is 16% for Cottonwood vs the 132-day window
     -- the segment I was NOT watching, worse than the one I was. My hazard was real and was not the
     biggest one. Recorded so the next issuer does not read a discharged hazard as a cleared field. -->
<!-- OPEN AT ANDREW, not blocking closure: 49F model-vs-total-custody basis; whether Cottonwood's
     $136.5M is "growth" at all; the $914,144.89 Inflection Orion-vs-Eclipse-crosswalk basis. -->
<!-- SURPRISE-CHANNEL ITEMS HELD AT CTO, unrouted by design: (1) Inflection 08-11 ETF ownership
     cent-identical to 08-10 across all 4 tickers while NAVs moved -- carry-forward signature,
     bounded ~$0.1M; (2) comp-estate has no `etfs` vertical though opal-data-etfs is canonical --
     spelled `etf-reports`, so the obvious question does not route on the obvious name; (3) a
     Cottonwood Black Diamond historical backfill to 2026-04-01 would convert this TO's largest
     UNCOMPUTABLE into a measured number -- pipeline shape exists, only the range is missing. -->
<phase>INVESTIGATION</phase>
<priority>P1 -- feeds the September board update, Andrew-named deliverable</priority>
</task_order>

## 0. Provenance -- this spec is ANDREW-DIRECT, VERBATIM

Delivered at the CTO terminal 2026-08-12 (~18:0xZ). **The phrasing is the ruling; this section is quoted,
not paraphrased.** Where my own grounding contradicts or extends it, that is marked `CTO-MEASURED` and is
additive -- it never overrides his words.

> "Here is the methodology here. WE want to go from April 1st to Today (therefore yesterday 8/11). What we
> need to do for Historical AUM growth is the following. 1.) We establish total assets, that means 1a)
> checking the opal-data-etfs and finding the total ETF holdings snapshots pinned between April 1 and August
> 11. 1b) Checking 49 0824 account data for total AUM delta between those two dates. 1c) Identifying when
> Inflection came in (5-15-2026 or close) and checking only for model data that has come in over the period
> (effectively 0 -> X just assessing Inflection Opal Models which is included in
> opal-data-portal-v2/platinum/mdpf/inflection in the relevant field. 1c) Checking Model data for Cottonwood,
> which means not only just the opal satellites, but any "opal" named consitutent model. A start point for
> this is the opal-data-portal-v2/platinum/mdpf/cottonwood search, however we want to check the model figures
> from there against a live current sweep against the Black Diamond Rebalance endpoint scanning these
> "Strategies": [18 strategies, listed in section 3d]. That gives us our asset base. 2.) We subtract all the
> firm-specific holdings of the Opal ETFs to find the delta in the ETF Float (non-managed assets however that
> are still generating fees). We want to be able to break out the growth in assets by segment, which I'd call
> 49 Financial, Inflection Wealth Management, Cottonwood Capital Advisory, and ETF Float. 3.) We need to know
> the number of increase in clients and accounts associated with those cohorts, which can most easily be done
> in the relevant silver layers of opal-data-assets so you can just stick to parquet. That is Task 1, I
> recommend handing it off to 0.4.0_DS_ClientPlatform~O, which I am instantiating now to deal with this."

## 1. Window

**2026-04-01 (start) -> 2026-08-11 (end).** The end date is his: *"Today (therefore yesterday 8/11)"* --
today is 2026-08-12, so 8/11 is the T-1 frontier. `CTO-MEASURED`: `lib/trading_calendar.py` puts 2026-08-11
at **1 trading day behind** the 2026-08-12 frontier -- a correct T-1 endpoint, not a stale one. Do not
"improve" the endpoint to 08-12; the window is his.

Every figure you report carries its **own** as-of date. Do not silently normalise legs to a common date --
where a leg cannot reach an endpoint, say so (see the measured gaps below).

## 2. The four segments (his naming, use it verbatim in output)

`49 Financial` | `Inflection Wealth Management` | `Cottonwood Capital Advisory` | `ETF Float`

## 3. Step 1 -- establish total assets

### 3a. ETF total -- `s3://opal-data-etfs/`

Opal ETFs: **DIVZ, IDVZ** (Polen/TrueShares) and **PFOE, PFDE** (Pathfinder/Filepoint).

> ### `CTO-MEASURED` HAZARD -- THE APRIL 1 BASELINE DOES NOT EXIST IN THIS BUCKET.
> I enumerated every prefix before issuing this. **No source under `opal-data-etfs` reaches 2026-04-01:**
>
> | source | earliest object | denominator |
> |---|---|---|
> | `snapshots/` | `snapshot_2026-05-15.json` | 61 objects, 2026-05-15 .. 2026-08-11 (complete listing, not a page) |
> | `etf_history.csv` | `run_date` 2026-07-09 | single file, re-derived daily |
> | `silver/holdings/` | `2026-05-18.parquet` | -- |
> | `daily/49financial/` | `2026-05-01.json` | -- |
>
> **The naive read -- take the earliest snapshot as the April 1 baseline -- produces a 2026-05-15 -> 08-11
> delta wearing an April-1 label, and nothing in the output would say so.** That is the exact
> upstream-redefines-the-domain class: the number is well-formed and true about the wrong window.
>
> **REQUIRED:** resolve the April 1 ETF baseline or DECLARE the leg's true start date on the face of the
> deliverable. Options, in preference order: (i) reconstruct from issuer-reported `net_assets` /
> `shares_outstanding` x NAV if an earlier source exists outside this bucket; (ii) locate an earlier
> producer via `comp-estate etfs`; (iii) declare the ETF leg as 2026-05-15-start, stated in the number's own
> frame. **Do not pick silently.** If you land on (iii), that is a legitimate answer -- an honest short
> window beats a mislabelled long one.

### 3b. 49 Financial -- total AUM delta

> ### `CTO-MEASURED` HAZARD -- WRITE THE FULL 8-DIGIT ACCOUNT. HE WROTE THE 4-DIGIT PREFIX.
> He wrote *"49 0824 account"*. There are **two** 49F Schwab accounts and the truncated form is precisely
> what makes them confusable (`0824`/`0833` differ in 2 characters; the full forms in 6):
>
> - **`08242234`** = **MDPF, "Model Portfolios"**
> - **`08335338`** = **ADVI, "Advisor Intelligence"** (portal-served, scoped per advisor)
>
> Canonical: `s3://opal-data-assets/schwab/{account}/`. **This is NOT mechanically enforced anywhere.**
>
> **PROCEED ON `08242234` (Model Portfolios)** -- it is the reading consistent with a model-based asset base,
> which is what every other leg of this methodology measures. **State the full 8-digit account on the face of
> the number** so it carries its own frame. I am routing the confirm to Andrew in parallel; **do not block on
> it** -- if he corrects it, the re-run is cheap because the account is a parameter, not an assumption baked
> into your output.

### 3c. Inflection Wealth Management -- model data only, 0 -> X

Source: `s3://opal-data-portal-v2/platinum/mdpf/inflection/`

> ### `CTO-MEASURED` -- HIS RECOLLECTION IS CONFIRMED TO THE DAY. Start from this, do not re-derive it.
> From `aggregate-aua-timeseries.json` (442-point series, `as_of_first` 2024-11-01, `as_of_last` **2026-08-10**):
>
> - **last zero: 2026-05-14. first non-zero: 2026-05-15, at 399 accounts.** His "5-15-2026 or close" is exact.
> - **2026-04-01 = 0 accounts** -- so the window start is a true zero and the leg is a clean 0 -> X.
> - Latest values, 7 `opal_*` models, all `cohort_class=model`: **$144,978,897 across 548 accounts.**
>
> | model | model_value | accounts |
> |---|---|---|
> | `opal_intermediate` | $77,258,905 | 202 |
> | `opal_blend_5050_int_ltc` | $36,188,857 | 160 |
> | `opal_long_term_conservative` | $14,409,166 | 90 |
> | `opal_blend_5050_st_int` | $7,295,994 | 23 |
> | `opal_short_term` | $6,542,914 | 29 |
> | `opal_long_term_aggressive` | $2,317,040 | 32 |
> | `opal_ultra_short_term` | $966,021 | 12 |
>
> **TWO THINGS THAT WILL BITE:**
> 1. **`as_of_last` is 2026-08-10, NOT 08-11** -- this leg cannot reach the window end from this artifact.
>    Pin the endpoint you actually used; do not label an 08-10 figure as 08-11.
> 2. **Inflection's firm-wide AUA is $209,225,006; the Opal MODEL value is $144,978,897.** These are
>    different measures and the board number is the model one. A reader who grabs the firm header metric
>    overstates this segment by ~$64M. `count_basis` carries `absent` entries on some dates -- a `None` in
>    the count series is a missing observation, not a zero.

### 3d. Cottonwood Capital Advisory -- model data, then a LIVE Black Diamond verification

Start point: `s3://opal-data-portal-v2/platinum/mdpf/cottonwood/` (`aggregate-aua-timeseries.json`,
`aum-metrics.json`, `account-units.json`, `account-distribution.json` all present).

Then verify those model figures against **a live current sweep of the Black Diamond Rebalance endpoint**,
scanning these Strategies (his list, verbatim, 18 entries):

```
Anna *9237                        Opal Satellite 15
Anna *9238                        Opal Satellite 30
Blended Opal / Satellite 50       Opal Satellite 40
Moderate Income Portfolio         Opal Satellite 50
Opal - Beecherl Legg              Opal Satellite 60
Opal - Cash + Satellite 50        Opal Satellite 70
Opal - Income                     Opal Satellite 80
Opal 66% Long Term / 34% UST      Opal Satellite 98
                                  Opal Ultra Short Term
                                  Opal UST/ Sat 70
```

> ### `CTO-MEASURED` -- THE LIST IS AUTHORITATIVE. A NAME PATTERN IS NOT.
> **Three of the 18 do not contain the string "opal":** `Anna *9237`, `Anna *9238`, `Moderate Income
> Portfolio`. **A case-insensitive "opal" scan silently drops them** -- and their absence looks like a clean
> result, not a miss.
>
> His instruction cuts BOTH ways and you must run both directions and report both:
> - **the 18-name list is the floor** -- every one gets resolved or explicitly reported as not-found;
> - *"not only just the opal satellites, but any 'opal' named consitutent model"* means the name scan is a
>   **SUPERSET check** -- report any `opal`-named constituent model found that is NOT on the list.
>
> Report the reconciliation as two explicit sets: **on-list-not-found** and **found-not-on-list**. Neither
> being empty is the finding; a silent single-number answer is not.

> ### VENDOR EGRESS -- AUTHORIZED FOR THIS CALL, AND SCOPE-BOUND.
> **Cottonwood Black Diamond egress is LIFTED, standing.** You do not need a per-use word for this sweep.
> **The lift is `cot-BD` ONLY -- Cottonwood Black Diamond. It does NOT extend to bd/49f, to ycharts, or to
> any other vendor.** A lift on the wire is not a lift on the work: pull what this TO needs, nothing wider.

## 4. Step 2 -- ETF Float

`ETF Float = total Opal-ETF assets - all firm-specific holdings of those ETFs`

His definition: *"non-managed assets however that are still generating fees."* The subtraction exists to
**prevent double-counting** ETF positions already inside the 49F / Inflection / Cottonwood managed segments.

**State the subtrahend per firm**, not just the net. A float figure whose deduction is invisible cannot be
checked, and this is the one segment defined entirely by a subtraction.

## 5. Step 3 -- client and account deltas per cohort

Silver layers of `s3://opal-data-assets/`, **parquet only** (his words: *"so you can just stick to parquet"*).
This is Rule 17-consistent: silver is the queryable dedup+dtype tier.

Deliver, per segment, at BOTH endpoints: **client count**, **account count**, and the delta. Same as-of
discipline -- each count carries its own date.

## 6. Deliverable

A committed markdown deliverable under `org/tier2_senior/0.4.0_DS_ClientPlatform~O/deliverables/`, carrying:

1. A **4-segment x {start, end, delta}** asset table, every cell with its own as-of date.
2. The same shape for **client counts** and **account counts**.
3. **A DENOMINATOR LINE ON EVERY SCAN** you reason from -- what you counted, out of what.
4. An explicit **assumptions + gaps** section: the ETF April-1 baseline resolution, the 49F account
   confirmed/assumed, the Inflection 08-10 endpoint, and the Cottonwood two-set reconciliation.
5. Anything that surprised you (section 9).

**Do not compute a single headline growth rate.** Segment-level figures plus the arithmetic to combine them;
the framing choice (organic vs including onboarding) is Andrew's and it is live -- I have that fork open with
him now.

## 7. `<compiler_tools_mandate>` -- three phase

- **Phase 1 (before writing):** `comp-which` to route each source question; `comp-estate etfs` and
  `comp-estate mdpf` for producer/consumer topology on the ETF and model legs. **Treat every `comp-estate`
  topology or served-name claim as a PRIOR UNDER TEST** and ground it on the live primitive -- that tool has
  a measured false served-name (PC-003).
- **Phase 2 (before commit):** `comp-pipescript io <script> --pipeline <tree>` if you author or touch any
  gold/silver script (`--pipeline` is REQUIRED; flagless is rc=2 REFUSED). `.tools/commit-gate.sh` on every
  `.py`.
- **Phase 3 (after commit):** re-run the read that produced each headline figure and confirm it reproduces.
- **Determinism control:** run the full extraction **twice** and diff. A figure that does not reproduce is
  a finding, not a rounding note.

## 8. `<cross_domain_coordination>`

- `s3://opal-data-portal-v2/platinum/mdpf/*` is **READ-ONLY to you.** Its producer is
  `opal-assets-mdpf-portal-publisher`. **`account-distribution.json` is a LIVE SERVED PORTAL BELL** and the
  hyphen/underscore twins are a guarded set -- **read only; write nothing under `platinum/`.**
- `opal-data-etfs` is the ETFS lane. Canonical location ruled 2026-08-12 (Andrew: *"for ETFS canonical
  location its opal-data-etfs"*). Read-only here.
- **cot is a COMPLETELY separate firm pipeline from bd -- never mirror or sync between them.**
- No other active TO writes the paths this one reads. **This TO produces a measurement deliverable; it
  changes no served artifact.**

## 9. Surprise channel (NAMED, per THE_SURPRISE_CHANNEL doctrine)

You will see things outside this mandate. **Report one line to `1.0.0_SA_CTO`, take no action, keep working.**
Do not suppress and do not chase. Bar for breaking flow is existential -- finish the measurement first; a
completed measurement can invert an early finding.

## 10. `<acceptance_criteria>` -- machine-checkable

| id | criterion |
|---|---|
| T1-A1 | 4-segment asset table exists with start, end, delta, and a per-cell as-of date. No cell undated. |
| T1-A2 | ETF leg states its TRUE start date; if not 2026-04-01, the shortfall is declared on the face of the table. |
| T1-A3 | The 49F account is written as the FULL 8 digits everywhere it appears. Zero occurrences of a bare 4-digit `0824`/`0833` as an account identifier. |
| T1-A4 | Inflection leg reports the endpoint actually used (2026-08-10 unless a fresher artifact is found) and distinguishes model value from firm AUA. |
| T1-A5 | Cottonwood reconciliation reports BOTH sets: on-list-not-found and found-not-on-list. Both may be empty; both must be present. |
| T1-A6 | ETF Float states the per-firm subtrahend, not only the net. |
| T1-A7 | Client and account counts delivered per segment at both endpoints with deltas. |
| T1-A8 | Every scan reasoned from prints its denominator. |
| T1-A9 | Determinism control: extraction run twice, diff reported. |

## 11. `<proof_of_spec>`

**MANDATORY** (Andrew-direct 2026-08-11: *"I do not want TOs being issued that do not have machine-readable
data contracts"*). Criterion-id set **T1-A1 .. T1-A9**, minted above at decomposition.

Fill a `PROOF_OF_SPEC.schema.json` instance from your OWN efforts and validate it with
`.tools/proof-of-spec-check.py` **before** flipping this TO to `complete`.

- `schema_version`, `to_id: OPAL_BRDSEP.T1`, `phase: INVESTIGATION`, `spec_ref`: this file,
  `assignee: 0.4.0_DS_ClientPlatform~O`
- `acceptance[]`: one entry per T1-A*, each with `criterion_id`, `criterion_verbatim`, `method`,
  `invocation`, `output_evidence`, **`denominator`**, `status`
- Legitimate statuses include `UNCOMPUTABLE-BY-CONSTRUCTION` and `UNVERIFIABLE-BY-INSTRUMENT` -- **use them.**
  If the April-1 ETF baseline genuinely cannot be reconstructed, that is `UNCOMPUTABLE-BY-CONSTRUCTION` with
  a reason, **not** a quiet substitution of the 05-15 figure.
- `controls`: the determinism diff (T1-A9), plus a mutant where one applies.
- `declared_exclusions`: anything in his methodology you did not execute, with the reason.

## 12. Open confirms -- ROUTED TO ANDREW BY CTO, **NOT A GATE ON YOUR START**

1. **Which 49F account** -- `08242234` (Model Portfolios) assumed; `08335338` is the ADVI alternative.
2. **ETF April-1 baseline** -- whether he wants reconstruction attempted or accepts a declared 05-15 start.

**Begin now.** Both are parameters, not preconditions; neither blocks 3c, 3d, step 2 or step 3. If an answer
lands mid-flight, fold it. **Nothing in this TO requires my approval to proceed** -- surface findings, do not
hold on them.
