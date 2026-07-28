# MDPF NON-MODEL — PRODUCER TRACE AGAINST THE 0824 CANONICAL FORMULA

**Author:** `0.2.0_DT_PortfolioAnalytics`
**Date:** 2026-07-28 ~14:41Z
**Directed by:** Andrew, direct at my terminal ~14:35Z — *"trace both producers against the 0824 formula"*
**Basis ruling being tested:** Andrew-direct ~14:27Z, recorded verbatim @`13fbdea6d` —
> "the answer is 0824 schwab total value minus 49F smartx model aggregation, that is canonical balance."

**Scope:** verification only. No writes to served output, no fixes, no promote, no invalidations.

---

## THE TEST

```
non_model  ==  partner_custody_total  -  model_aua
```

**Plane:** APPLIED / served. All artifacts pulled live from `s3://opal-data-portal-v2` this session;
each downloaded file's size byte-matches its `head-object` `ContentLength` (retrieval control).
**Indexed BY DATE (`dates.index('2026-07-22')`), never by array position** — the per-firm artifacts carry
429 dates and global/cottonwood carry 447, so positional indexing would silently read the wrong row.

## RESULT — REVAMP: EXACT, 3 OF 3

| artifact | `partner_custody_total` | `model_aua` | custody − model | actual `non_model_aua` | verdict |
|---|---:|---:|---:|---:|---|
| 49financial | 1,689,302,889.53 | 1,414,120,540.22 | 275,182,349.31 | 275,182,349.31 | **EXACT** |
| inflection | 202,258,677.80 | 137,997,265.16 | 64,261,412.64 | 64,261,412.64 | **EXACT** |
| cottonwood | 458,189,558.77 | 124,376,009.73 | 333,813,549.04 | 333,813,549.04 | **EXACT** |

**SOURCE-CONFIRMED, independently of the arithmetic** —
`data/mdpf/scripts/backfill/build_aggregate_aua_timeseries.py` @HEAD:
- `:22` — `"non_model_aua": [...]   # 1b' = Schwab_total - 1a`
- `:430` — `# Collapse: 1b' = Schwab_total - 1a = (1b + 1c); fold sma_aua into non_model_aua and`

**That is Andrew's sentence in code.** The REVAMP producer implements the canonical formula.

## RESULT — LEGACY: DOES NOT SATISFY IT

`data/mdpf/scripts/backfill/build_legacy_compat_emit.py:615-640` @HEAD, verbatim:
```
# enterprise_total = 49F (1a+1c+1b, full Schwab book) + Inflection 2a
# model_aum = 49F 1a + Inflection 2a (sum of by_model stack lines)
# non_model_aum = 49F 1b + 1c -- 2b is NOT in the headline (audit field)
...
nm_total = round(enterprise_total - model_aum_total, 2)
```

- **Inflection's non-model (2b) is excluded BY DESIGN** (its own comment says so).
- **Cottonwood is absent entirely** — the emit predates 3FIRMS.
- **It carries values forward:** `247,692,229.36` is byte-identical across 07-18..07-22;
  `220,293,935.19` across 07-11..07-15. `getNonModelAumForDate` then roll-forwards on top of that.
- **@2026-07-22 it reports `247,692,229.36`** where the canonical formula gives `275,182,349.31`.

**VERDICT: REVAMP is canonical under Andrew's definition; LEGACY is not.** The leg currently feeding half
the deployed Global headline (`json/portfolios/non_model_assets.json`) is the **non-canonical** one.

---

## THE FINDING THIS TRACE SURFACED — MIXED SCOPE IN THE GLOBAL ARTIFACT

```
GLOBAL model_aua       1,676,493,815.11   ==  49F + inflection + cottonwood    EXACT 3-firm sum
GLOBAL non_model_aua     275,182,349.31   ==  49financial's non_model_aua      EXACT 49F-ONLY
```

**The Global artifact pairs a THREE-FIRM model leg with a ONE-FIRM non-model leg.**

| | value |
|---|---:|
| sum of per-firm `non_model_aua` | 673,257,310.99 |
| GLOBAL `non_model_aua` | 275,182,349.31 |
| **not carried into Global** | **398,074,961.68** |

Inflection's `64,261,412.64` and Cottonwood's `333,813,549.04` each pass the canonical formula **exactly**
in their own artifacts, and are then absent from Global's non-model band.

> **WHY THIS SURVIVED REVIEW:** `opal_aggregate_aua == model_aua + non_model_aua` still holds as an
> **equation** (1,676,493,815.11 + 275,182,349.31 = 1,951,676,164.42). The artifact is **internally
> consistent and externally mixed-scope.** A self-identity check PASSES. Only a cross-artifact comparison
> catches it. *An instrument that cannot fail is not an instrument.*

## RESOLVED BY ANDREW — reading (b). GLOBAL SCOPE IS CORRECT.

I put two readings to Andrew and did **not** choose between them. **He answered directly, ~14:43Z, verbatim:**

> "global is scoped correctly, i am reffering to 49 here"

**THIS CLOSES THE SCOPE QUESTION:**
- **Reading (a) is DEAD.** The `398,074,961.68` is **NOT a shortfall and NOT a defect.** The Global artifact's
  49F-only non-model band is **correct as designed** — do not "fix" it, and do not carry my mixed-scope
  framing forward as a finding.
- **Reading (b) stands:** Global is *49F custody + all-firm models*, by design.
- **His formula governs the 49F LEG**, which is exactly where he pointed it.

> ⚠ **The one residual from reading (b) survives his ruling: the band is unlabelled.** Nothing on the page
> states the non-model band is 49F-scoped. That is a disclosure question, not a correctness one, and it is
> not mine to decide. Surfaced, not adjudicated.

## THEREFORE — THE VERDICT ON THE LIVE P0

With scope settled, the chain closes with no remaining ambiguity:

| | value | status |
|---|---:|---|
| canonical 49F non-model (REVAMP, formula-exact) | 275,182,349.31 | **CANONICAL** |
| legacy non-model actually consumed by the page | 247,692,229.36 | **NON-CANONICAL** |
| difference | 27,490,119.95 | the whole gap |

```
CORRECT headline   1,676,493,815.11 + 275,182,349.31  =  1,951,676,164.42   ->  $1.95B
RENDERED headline  1,676,493,815.11 + 247,692,229.36  =  1,924,186,044.47   ->  $1.92B
```

**$1,951,676,164.42 is the correct number.** The deployed $1.92B is wrong **because the renderer sources its
non-model leg from the non-canonical legacy producer** (`json/portfolios/non_model_assets.json`) instead of
the canonical REVAMP artifact — `portal/src/pages/ModelPortfolios.tsx:1168-1172`.

**This is a FIX I have NOT made and am NOT authorised to make** (verification-only scope, CTO's GO required).
Recording the mechanism, not repairing it.

## RESIDUALS / DENOMINATOR

- **Denominator:** 4 REVAMP served artifacts (global + 3 firms) + the legacy `non_model_assets.json`.
- **ONE DATE TESTED** — 2026-07-22, the served frontier. **The full 447-date history was NOT tested;** the
  identity could differ on other dates and I have not looked.
- **Cottonwood's artifact is the 2026-07-23T21:47:07Z vintage** (not refreshed by the 13:41:05Z restore), so
  its `333,813,549.04` is as-of that write.
- The deployed-PROD headline mechanism (cross-basis sum at `portal/src/pages/ModelPortfolios.tsx:1168-1172`)
  is documented separately in my 141956Z / 144116Z messages to `1.0.0_SA_CTO`.
