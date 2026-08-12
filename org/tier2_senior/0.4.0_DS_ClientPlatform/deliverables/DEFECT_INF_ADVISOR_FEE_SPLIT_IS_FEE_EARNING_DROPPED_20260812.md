# DEFECT — INF advisor summary serves fee_earning_aua = $0.00 for an entire book

**Filed:** 2026-08-12 ~15:45Z · **Owner at filing:** 0.4.0_DS_ClientPlatform
**Surfaced by:** 4.0.0_SA_CRO~A 153326Z (COO copied) · **Confirmed + mechanism-grounded here**
**Status:** ⛔ **OPEN — LIVE ON A SERVED ARTIFACT. NOT FIXED. Persisted ahead of a device reboot.**

⚠ **PERSISTED BECAUSE IT EXISTED ONLY IN SESSION CONTEXT.** The mechanism below was ground at
source and at the input during the reboot wind-down; none of it is captured anywhere else.

## THE SYMPTOM — verified on the live object, not on the relay

`s3://opal-data-inf/platinum/advisors/patrick_scanlan/summary.json`
LastModified **2026-08-12T15:02:53Z** · generated_at **15:02:52Z** · data_as_of 2026-08-12

| field | served value |
|---|---|
| `book.fee_earning_aua` | **0.0** |
| `book.non_fee_earning_aua` | **23,659,587.43** (the ENTIRE book) |
| `book.fee_earning_account_count` | **0** |
| `book.non_fee_earning_account_count` | **159** (= `book.account_count`) |
| `book.avg_fee_bps_earned` | **114.5** |

⛔ **INTERNALLY CONTRADICTORY ON ITS FACE:** a 114.5 bps earned rate sitting beside a ZERO
fee-earning base. The contradiction is the tell, and §"why" below explains why one survived.

## ⛔ MECHANISM — SOURCE-CONFIRMED AND INPUT-CONFIRMED (not inferred)

Producer: `infra/aws/lambda/inf-portal-advisor-publisher/lambda_function.py`

```
:1059  billing_dim = load_silver_dim('silver/api_dims/billing/', 'Billing dim')
:495   if 'is_fee_earning' in sub.columns and 'ending_mv' in sub.columns:   <-- THE GATE
:504       rec['fee_earning_aua'] = round(billing_fp_aua, 2)               <-- THE ONLY SITE
:737   fee_earning_aua = billing.get('fee_earning_aua', 0.0) or 0.0        <-- SILENT DEFAULT
:738   non_fee_aua = max(0.0, total_aua - fee_earning_aua)                 <-- WHOLE BOOK FALLS
```

**`:504` is the ONLY place `fee_earning_aua` is ever set, and it is gated at `:495` on TWO columns
being present. When the gate is False the key is never written, `:737` silently substitutes `0.0`,
and `:738` assigns the entire book to non-fee.**

### THE INPUT — the gate is False because a column vanished
`s3://opal-data-inf/silver/api_dims/billing/snapshot_date=2026-08-12/data.parquet`
908 rows x 17 cols · **`is_fee_earning` ABSENT** · `ending_mv` PRESENT (908 non-null, sum
**209,225,005.59** — which ties exactly to the firm `total_aua`, so the dim covers the whole book).

### ⛔ THE REGRESSION IS DATED — it is TODAY, not pre-existing
Denominator: 1,598 billing parquet partitions materialised client-side.

| snapshot_date | rows | cols | `is_fee_earning` |
|---|---|---|---|
| 2026-08-01 .. 08-04 | 900 | 13 | PRESENT (True 787/900) |
| 2026-08-05 | 902 | 13 | PRESENT (787/902) |
| 2026-08-06 .. 08-10 | 907 | 13 | PRESENT (789/907) |
| 2026-08-11 | 908 | **17** | PRESENT (789/908) |
| **2026-08-12** | 908 | 17 | ⛔ **ABSENT** |

**Present every day 08-01 through 08-11; gone on 08-12.** The schema widened 13 -> 17 on 08-11
(the `ending_mv_reported` / `ending_mv_source` / `ending_mv_status` basis columns appear), and on
08-12 the column count held at 17 while `is_fee_earning` dropped out.
⚠ **INFERRED, NOT CONFIRMED:** the loss is temporally adjacent to the **ending_mv basis** work
(COO commissioned a longitudinal investigation @5e9c253613) and those basis columns are the ones
that appeared. **Adjacency is not causation and I did not confirm it.**

### ⭐ WHY `avg_fee_bps_earned` SURVIVED — and why that matters
It is computed on a **different path** (`:467-490`, `annual_fee_pct` weighted by `ending_mv`, with
a `fee_amount / holdings_aua` fallback) that **does not depend on `is_fee_earning`**. **Two paths,
one predicate, only one fell through** — which is exactly why the artifact is self-contradictory
rather than uniformly zeroed. **A uniform zero would have looked like "no data"; a contradictory
pair is what made it findable.**

### WHY THE FIRM NUMBER IS CORRECT
`platinum/firm/header_metrics.json` at the same 15:02:52Z publish serves
`fee_earning_aua = 203,216,860.04` correctly — the firm path uses a different derivation. **This is
CRO~A's "fourth implementation": three sites were corrected under CPR-6, this one was not, and the
disagreement went from 22x to categorical.**

## ⛔⛔ AMENDMENT 1 (15:56Z) — ROOT CAUSE **CLOSED**, AND MY "OPEN" LINE BELOW WAS WRONG

**`0.4.0_DS_ClientPlatform~A` owns the cause and stated it unprompted (@41ee75c574).** The column did
not "vanish": **they RETIRED it from silver on 08-11**, deliberately, as leg (b) of the flag act —
Andrew-direct instruction #2 under CTO's Rule-17 ruling that a judgment classification is
gold-tier — and re-homed the derivation to `lib/fee_classification.py`. **Correct act.**
**The defect is the CENSUS, not the retirement:** the retirement was gated on repointing every
reader; they repointed five and verified all five deployed (md5 TIE), **but enumerated the reader
set over `data/inf/scripts/` ONLY.** `inf-portal-advisor-publisher` lives under
`infra/aws/lambda/` and no search of that subtree could ever have surfaced it.
⭐ **The lesson in one line, theirs: A CENSUS OVER A SUBTREE IS NOT A CENSUS OVER CONSUMERS.**
✅ **My INFERRED adjacency to the 13→17 widening is CONFIRMED — the SAME act**, deployed in the same
window, first exercised on the same 08-12 scheduled run. One act, two visible effects, which is
why both landed on one partition.

## ⛔⛔ AMENDMENT 2 — TWO HOMES, MEASURABLY DIVERGENT (this supersedes §"deployed builder" below)

~A corrected my line *"the deployed builder still derives the column."* **They were right that it is
false of the artifact THEY read — and I was right about the artifact I read. WE READ TWO DIFFERENT
DEPLOYED ARTIFACTS AND THEY DO NOT MATCH.** Measured by me on both sides, same session:

| artifact | md5 | bytes | `_derive_is_fee_earning` | `ending_mv_source` |
|---|---|---|---|---|
| `s3://opal-data-inf/code/silver/build_billing_dim.py` | **9a25fe0d** | 15,460 | **0** | **3** |
| `inf-silver-chain` **Lambda package** member | **770dc996** | 8,266 | **2** | **0** |

⛔ **WHICH ONE EXECUTED IS DECIDABLE FROM THE OUTPUT, AND IT IS THE S3 OBJECT:** the 08-12 partition
has **no `is_fee_earning`** and **does** carry `ending_mv_reported`/`_source`/`_status` — the exact
signature of `9a25fe0d`. **~A's account is therefore complete and correct: the S3-staged code is
what runs, and the retirement is a completed act, not an open mystery.**

⚠ **BUT THE LAMBDA PACKAGE IS A STALE SECOND HOME CARRYING THE PRE-RETIREMENT CODE**, and that is a
NEW finding neither of us filed: **if `inf-silver-chain` ever executes that member, it would
re-derive `is_fee_earning` and drop the `ending_mv_*` basis columns — silently reverting a ruled
Andrew-direct act.** ⛔ **NOT MEASURED: whether that Lambda is on a live trigger, and whether it is
the billing dim's producer at all or a stale sibling.** *That is the next act on this line and it
is not mine to assume either way.*
⭐ **This is Rule 22a's own named case — "one logical producer, two independently-editable homes" —
and note WHICH failure mode we hit: not a false drift alarm, but the second one, where a
filename-resolved check reads CLEAN on each home while the two have silently diverged. Both of us
measured a real deployed artifact, honestly, and reached opposite conclusions.**

## ⛔ NOT MY CPR-6 — AND ⚠ THE SECTION BELOW IS SUPERSEDED BY AMENDMENT 2
- No commit of mine touched `build_billing_dim.py`; CPR-6's commit does not appear in its history.
- **DEPLOYED bytes read directly** (`aws lambda get-function` -> package -> member, per Rule 22a):
  the deployed `inf-silver-chain/build_billing_dim.py` **DOES** derive the column — `:88`
  `df["is_fee_earning"] = (sched != ZERO_FEE_SCHEDULE) & (fee.fillna(0) > 0)`, called at `:126`,
  and listed in the output columns at `:153`. **9 occurrences in the deployed member.**

⛔ **SO THE OPEN QUESTION IS THE SHARP ONE: the deployed builder derives and lists the column, yet
the 08-12 partition it should have written does not contain it.** Candidates, ALL UNVERIFIED:
(a) a different producer wrote that partition; (b) a conditional path in the builder drops it;
(c) the partition predates a redeploy; (d) a downstream re-write. **NOT MEASURED — do not guess.**

## THE DEFECT CLASS (independent of the cause)
**`:737`'s `billing.get('fee_earning_aua', 0.0)` applies a silent default to a REQUIRED field.**
A missing input became a plausible number instead of a refusal — the same swallow class as the
`b01` `dim_boundary` defect ruled FATAL the same hour (@0205eef992). **A `.get(default)` on a field
whose absence changes the meaning of the output is a swallow wearing a convenience idiom.**
**Recommendation (NOT a ruling, not mine to make): the gate at `:495` should REFUSE when
`is_fee_earning` is absent rather than let `:737` manufacture a zero.**

## REACHABILITY — ⚠ UNDETERMINED, AND NOT CLAIMED
CRO~A: `comp-routes` traces `/api/scoped/advisor-intelligence/advisors/{id}/summary.json` to
`gold/entities/advisors/{id}/summary.json`, which is **ABSENT** in `opal-data-inf`; comp-routes is
DESIRED-plane with a firm-parametric bucket blind spot. **The discriminating instrument is the
deployed-FE read census (D_00 lane) and it was NOT run.**
⛔ **No client-impact claim is made here.** If any surface reads the platinum advisor summary, it
currently shows this advisor with zero fee-earning AUM.

## NEXT ACTS FOR WHOEVER PICKS THIS UP
1. **Determine why the 08-12 partition lacks a column its deployed builder derives** (the four
   candidates above). This is the root cause and nothing should be fixed before it.
2. **Run the D_00 deployed-FE read census** to settle reachability.
3. **Then** decide the `:495`/`:737` refuse-vs-default question (CTO/COO call, not DS's).
⛔ **Do NOT "fix" it by defaulting differently or by back-filling the column — that treats the
symptom and would erase the evidence of which producer dropped it.**
