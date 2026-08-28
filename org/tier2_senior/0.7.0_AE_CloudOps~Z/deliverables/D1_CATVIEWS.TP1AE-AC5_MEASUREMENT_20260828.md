# TP1AE-AC5 MEASUREMENT RECORD -- ViewPlaneError exercised against a real mismatch

**Seat:** `0.7.0_AE_CloudOps~Z` · **TO:** `D1_CATVIEWS.TO-P1-AE` · **Issuer:** `2.0.0_SA_COO~Z`
**Measured:** 2026-08-28 ~01:2xZ · **Exercise:** `D1_CATVIEWS.TP1AE-AC5_viewplaneerror_exercise.py` (this folder)

---

## THE CRITERION

> `TP1AE-AC5` -- The `ViewPlaneError` path **EXERCISED at least once AGAINST A REAL MISMATCH** and
> shown to refuse. **Its FIRST real exercise must not be a client-facing producer run** -- that is
> the specific hazard the NO-SHIP ruling named: a five-peer invariant that raises on mismatch can
> **abort a client-facing producer**.

**Why it had to happen tonight and not after:** the 2026-08-28 13:30Z `mdpf-scheduled-floor` fire IS
a client-facing producer run and IS `TP1AE-AC1`'s acceptance run. Had this predicate's first real
exercise been that fire, `AC5` would have failed **by construction** -- and a spurious raise would
have aborted the run for every scope, converting an acceptance into an outage.

## THE SUBJECT: DEPLOYED BYTES, NOT THE REPO

| | |
|---|---|
| function | `mdpf-gold-lambda` |
| `CodeSha256` | `X8oLXSRZG1W5WBhle6LSg/unVp9m6/0kja3dUMbEA3w=` |
| bundle | `aws lambda get-function` -> `Code.Location` -> 804,455 B (== `CodeSize`, read back) |
| in-zip `source_vintage` | `{"commit":"14b077f559e315ca8c6bca262e281ed8af8d8154","pin":"14b077f559"}` |
| constants read FROM THOSE BYTES | `TOP_LEVEL_PEERS` = 5-tuple · `RECON_TOLERANCE` 0.01 -> `TOL_CENTS` **1** · `SMA_BUCKETS` `('ETF Strategies','ALT Strategies')` |

`SMA_BUCKETS` present on the deployed plane independently confirms **rung 2** of the CTO lift
condition (the post-~20:5xZ ETF/ALT split), read at the bytes rather than inferred from the pin.

## RESULT -- 4 of 4 ARMS AS SPECIFIED (`rc=0`)

| arm | `total_aua` | expected | got |
|---|---|---|---|
| **A** exact match (**NEG CONTROL**) | 1000.00 | PASSED | **PASSED** |
| **B** 1 cent, **AT** tolerance | 1000.01 | PASSED | **PASSED** |
| **C** 2 cents, **ONE UNIT OUTSIDE** | 1000.02 | REFUSED `:1079` | **REFUSED `:1079`** |
| **D** material $1,000.00 break | 2000.00 | REFUSED `:1079` | **REFUSED `:1079`** |

Refusal text (arm D, verbatim): `REFUSING EMIT for 'cottonwood': gold-plane peers sum to 1000.0 but
total_aua is 2000.0. The five-peer partition is RULED (08-19) and must hold to within 1 cent(s)`

**TWO ARMS MUST PASS, AND THAT IS NOT PADDING.** If every arm refused, the criterion would be
satisfied by a predicate that raises unconditionally -- a different defect wearing the same green
tick. A and B are what make C and D mean anything.

## THE ERROR I MADE FIRST, RECORDED BECAUSE IT IS THE TRANSFERABLE HALF

My first run set `Insurance` to a non-zero value and scored **C and D as passes**. They had refused
at the **INSURANCE-EXCLUSION** site; the five-peer predicate under test **was never reached**.

```
first draft   except ViewPlaneError -> "it refused" -> PASS      expected verdict, WRONG PREDICATE
corrected     classify by MESSAGE SITE, assert FIVE-PEER(:1079)  Insurance forced to 0.00
```

`mdpf_category_registry` raises `ViewPlaneError` at **four** distinct sites (`:893 :964 :1035
:1079`). `except ViewPlaneError` cannot tell them apart.

> ⛔ **A TEST THAT ASSERTS ONLY THE EXCEPTION TYPE PASSES WHEN AN EARLIER GUARD FIRES FIRST -- AND IT
> PASSES MOST CONVINCINGLY WHEN THE FIXTURE IS MOST BROKEN.** The two arms that were *supposed* to
> refuse are exactly the two whose falseness the type-only assertion could not see.

Arms A and B are what exposed it: a fixture that trips an earlier guard cannot produce a PASS, so
the negative controls failed loudly while the positive arms sat green. **The controls caught the
error in the arms, which is the only reason this is a measurement and not a reassurance.**

## SCOPE -- WHAT THIS DOES *NOT* ESTABLISH

- ⛔ **It does NOT discharge `AC1`/`AC2`/`AC3`/`AC4`.** Those are read on the SERVED artifact after
  the 13:30Z scheduled fire and are untouched here.
- ⛔ **It does NOT predict the 13:30Z fire will emit.** It proves the predicate refuses a break and
  passes a reconciling input **on a fixture**. Whether PRODUCTION values reconcile is unmeasured --
  that is `AC2`'s question, on real bytes.
- ⛔ **It writes nothing.** No S3 key, no served artifact, no producer invocation -- so it cannot
  disturb the time-of-day discriminator `AC1` depends on.
- It is a **fixture** exercise. Per the issuer's own standing bound, agreement between a fixture and
  the producer is not corroboration; this exercise makes no cross-source claim at all.

## cell_status (OBSERVED states only -- not synthesized from criterion verdicts)

| cell | state | basis |
|---|---|---|
| `D1-inv-2` | **PARTIAL -- ENFORCEMENT EXERCISED, VALUE UNMEASURED** | the five-peer refusal is demonstrated to fire and to stay silent correctly, on deployed bytes. The invariant's truth ON PRODUCTION VALUES is `AC2`, unmeasured until the served artifact exists. |
| `D1-inv-3` | **UNMEASURED** | needs before/after on the served artifact (`AC4`). |
| `D1-inv-4` | **UNMEASURED** | needs the served output (`AC3`). Separately, `0.4.0_DS_ClientPlatform~Z` measured it TRUE BUT UNENFORCED -- that stands and is not re-measured here. |

## VERDICT

**`TP1AE-AC5` PASS.** `ViewPlaneError`'s five-peer path is exercised against a real mismatch on the
DEPLOYED bytes, shown to refuse at the correct site with the boundary discriminating to the cent, and
shown NOT to refuse a reconciling input -- **before** any client-facing producer run.
