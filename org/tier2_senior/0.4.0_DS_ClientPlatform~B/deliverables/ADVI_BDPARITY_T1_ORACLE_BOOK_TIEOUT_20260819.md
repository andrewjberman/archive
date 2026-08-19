# ADVI_BDPARITY.T1-ORACLE -- the book-tie-out oracle, qt6 group grain (BUILT + MEASURED)

**Seat:** `0.4.0_DS_ClientPlatform~B` | **Issued by:** `2.0.0_SA_COO` | **Built:** 2026-08-19 ~2130Z
**TO:** `org/tier2_senior/0.4.0_DS_ClientPlatform~B/task_orders/ADVI_BDPARITY.T1-ORACLE.book-tie-out-qt6-group-grain.md`
**Tool:** `data/assets/scripts/gold/runners_49f/oracle_book_tieout_qt6.py`

---

## 0. THE BASIS, AND IT IS STAMPED INTO EVERY ARTIFACT

**BOOK BASIS = GROUP-BASED.** Andrew-direct 2026-08-19 ~2012Z, verbatim *"All approved"*, on the COO
`/open-calls` card set; record `org/tier1_exec/2.0.0_SA_COO/deliverables/ANDREW_DIRECT_20260819_OPEN_CALLS_ALL_APPROVED.md`
@1e0ec3b079. The advisor's book is the **portfolio group** (membership view); **role tagging is
RETAINED as an attribute view**, not discarded.

The fence (CVO P2-1) is discharged. **Three things did NOT change and this deliverable holds all three:**

1. **The basis is stamped into the artifact** (`basis` block in every JSON the oracle writes, and the
   first three lines of every console run). This was never contingent on which way the ruling went --
   it is what makes a future basis change visible instead of silent.
2. **Serving still routes P4-class through CTO.** Unfenced is not self-serve. Nothing here is wired
   to a consumer; T1-3 below verifies that as a checked condition on four independent probes.
3. **The Travis-class delta is printed as measured-and-explained.** With group-based ruled, it is the
   *expected headline number*, not a discrepancy to reconcile away.

**NOT conflated with B_02.** Andrew's NET/REAL (cash, "the Schwab approach") valuation ruling
(@a3da94f467) answers a different question and is already answered. Where a valuation-basis term
appears below it is *stated as a component*, never re-adjudicated.

---

## 1. WHAT WAS BUILT

A three-leg tie-out at group grain. The legs are chosen so they differ in **derivation** -- two legs
that agree because they share an input are one leg counted twice.

| leg | what | source | egress |
|---|---|---|---|
| **L1** BD-NATIVE | qt6 "BI Billing" Portfolio-Group EMV -- *the number on the advisor's own BD dashboard*. The oracle's authority. | qt6 run | **VENDOR EGRESS** -- supplied to the tool as a file; the tool never calls the vendor |
| **L2** BD-MEMBERSHIP | `allocation_390224` export, group x account, `Account Market Value` | landed daily via `opal-assets-bd49f-daily-pull` | none |
| **L3** OURS | gold `canonical_valuation.net_mv_plus_cash` (V(t) authoritative) rolled to group over L2's membership | `opal-data-49financial/gold/advi/canonical/` | none |

**L1 vs L3 is the tie-out. L2 sits between them and localises a disagreement to MEMBERSHIP (L1-L2)
or VALUATION (L2-L3).**

### Three hard rules, enforced in the oracle's own frame

1. **NEVER SUM ACROSS GROUPS.** Groups overlap: measured 5,579 of 6,155 accounts (90.6%) in 2+ groups;
   the all-group sum is **$8.25B against a $1.551B distinct-account universe**. The tool **refuses to
   emit a cross-group total** -- that is not a big number, it is a wrong one.
2. **One account counts once per group, but its SUPERVISION SLEEVES are SUMMED.** Enforced by
   `dedupe_group_account` keyed on `(group, account, supervised)` -- mutant-verified load-bearing
   (79 of 201 groups move if bypassed). *Corrected 2026-08-19 ~2245Z; see ADDENDUM.*
3. **Join on `zfill(10)`.** Export carries 8-digit; our canonical carries 10-digit.

---

## 2. T1-1 -- THE ORACLE READ, PER GROUP (as_of 2026-08-18)

Denominators, printed beside every number: 30,577 export rows read -> 29,926 after collapse; **201
portfolio groups**; 6,155 distinct accounts; our canonical carries 7,315 accounts.

| portfolio group | accts | L2 membership MV | L3 ours |
|---|---:|---:|---:|
| 49F Schwab AUM | 2989 | $745.6M | $736.1M |  <!-- corrected: $745,570,084.08 -->
| Alex Bright - Local Ops | 2230 | $546.9M | $542.2M |
| Dallas Support | 1498 | $455.1M | $449.4M |
| Collin Plotts | 1771 | **$447.6M** | $436.8M |  <!-- corrected +$3,159,412.24 -->
| Lane Curry - Local Ops | 1361 | **$400.3M** | $372.8M |  <!-- corrected +$3,657,307.24 -->
| **Travis Penfield** | **318** | **$392.6M** | **$377.4M** |
| 49 Private Wealth | 188 | $347.7M | $339.4M |
| Erick Webb - Local Ops | 1187 | $329.7M | $328.7M |

All 201 groups are in the JSON report; the three marked rows carry the ADDENDUM's sleeve correction
(12 of 201 groups moved; **Travis did not**). **Group-grain only** -- no cross-group total exists in the output.

### The L1 leg is BUILT AND EXERCISED but NOT MEASURED BY ME -- stated plainly

The oracle's L1 reader is built and exercised end-to-end (reader -> all three deltas -> report), but
the **live qt6 run was not performed by this seat: I hold no vendor-egress word.** Standing lifts
cover cot-BD (Cottonwood) explicitly *not* bd/49f; the 49f BD scanning grant is Andrew-direct to
`4.0.0_SA_CRO~A` and is continuing. **Availability is not authorization**, and the tool is written so
that a future maintainer cannot quietly turn it into a vendor caller (see its EGRESS docstring).

The L1 value used to exercise the path -- **$456.8M for Travis Penfield** -- is **RELAYED, not
measured here**: it is CRO~A's published measurement (qt6 template 517685 / run 517686, Aug EMV,
asOfDate 08/18) from `org/tier1_exec/4.0.0_SA_CRO~A/deliverables/TRAVIS_GROUP_DECOMPOSITION_HOW_BD_BUILDS_456M_20260819.md`.
**T1-1 is therefore MEASURED for L2/L3 across all 201 groups and RELAYED for L1 on one group.** The
remaining step is one qt6 run under an egress holder -- it is not a build gap.

---

## 3. T1-2 -- THE TRAVIS-CLASS DELTA, MEASURED AND EXPLAINED

```
  BOOK (group-based, ruled)       $ 392,556,451.10   over 318 member accounts
  raw row sum (double-counted)    $ 405,399,972.00   <- NOT the book; 9 dup rows
  OURS V(t) net_mv_plus_cash      $ 377,433,506.75   matched 284 / unmatched 34
  OURS positions-only             $ 367,904,814.02   (like-for-like vs L2)
  delta  L2 - L3                  $  15,122,944.35
     of which COVERAGE            $  25,250,660.86   (34 export members absent from our canonical)
     of which VALUATION           $ -10,127,716.51   (on the 284 both sides carry)
     LIKE-FOR-LIKE (vs positions) $    -599,023.78
  BD NATIVE qt6 EMV (RELAYED)     $ 456,800,000.00
  delta  L1 - L2 (MEMBERSHIP)     $  64,243,548.90
  delta  L1 - L3 (THE HEADLINE)   $  79,366,493.25   (+21.03%)
  -- ATTRIBUTE VIEW (role tagging; retained, NOT the book) --
     architect            233 accts  unweighted $ 316,280,384.19  split-wtd $ 122,500,856.99
     implementor            4 accts  unweighted $  31,386,334.41  split-wtd $  28,247,700.97
     additional_advisor     4 accts  unweighted $   1,059,301.30  split-wtd $     251,572.18
     ANY-ROLE union       241 accts  unweighted $ 348,726,019.90
```

**THE HEADLINE, and under the group-based ruling it is the EXPECTED number: BD's book for Travis
Penfield reads $79.4M (+21.03%) above ours.** Its named components:

- **$64.2M -- MEMBERSHIP (L1-L2).** BD's group carries 347 member accounts; the landed export's
  open/grouped filters yield 318. CRO measured the shortfall at 28 accounts / $42.9M plus 12
  non-Schwab members / $16.1M structurally invisible to Schwab-only feeds. **Also a basis component:**
  qt6 EMV is accrual+cash-inclusive (CRO proved it mechanically on 120,215 rows via the qt1 identity)
  while the export's `Account Market Value` is not -- see the next bullet, which is the same class.
- **$25.3M -- COVERAGE (L2-L3).** 34 accounts in the export's Travis membership that our
  `canonical_valuation` does not carry at all. **All 34 read `Account Is Open = true`** -- so this is
  not a closed-account artifact. Largest: $6.15M, $3.70M, $3.30M, $2.97M, $2.00M. Named, not chased.
- **-$10.1M -- "VALUATION", and it is MOSTLY A MEASURE MISMATCH, not a valuation gap.** See below.

### The finding that changes how this delta should be read

The export's `Account Market Value` is a **positions-grain** column. Measured on the 284 matched
Travis accounts:

| comparison | delta | as % |
|---|---:|---:|
| export Account MV vs our `net_mv_plus_cash` | -$10,127,716.51 | -2.683% |
| export Account MV + `Cash Market Value` vs our `net_mv_plus_cash` | -$5,261,482.51 | -1.394% |
| **export Account MV vs our `net_mv_positions`** | **-$599,023.78** | **-0.163%** |
| export Account MV + Cash MV vs our `net_mv_positions` | +$4,267,210.22 | +1.160% |

**A naive L2-vs-`net_mv_plus_cash` comparison books a $10.1M "valuation gap" that is mostly two
columns at different grains compared because they had similar names.** Like-for-like the residual is
-$599K (-0.163%). Adding the export's separate cash column makes the fit *worse*, so cash is not
simply a missing addend. The oracle now reports both measures and labels which is like-for-like.

**NOT CLOSED, and I am not claiming it is:** per-account identity does **not** hold -- only 2 of 284
tie to the cent, and the matched deltas split 63 export-higher / 212 ours-higher / 9 exact, median
-$4,433. The **-0.163% aggregate residual is a NAMED OPEN CELL**, evidence is aggregate-level, and
the per-holding mechanism is unconfirmed. This is a candidate mechanism named, not a root cause.

### A correction to a number now in circulation

**CRO's `$405.4M` "allocation-export census (group rows, account-MV sum)" reproduces byte-for-byte as
the RAW ROW SUM -- and it double-counts $12.8M across 9 accounts.** An account can sit under 2+
portfolios/relationships inside one group, putting it on 2+ export rows. **The correct export-side
membership figure is $392,556,451.10.** This does not disturb CRO's decomposition (which was built on
BD's own member list, not this sum) but the $405.4M figure should not be quoted forward as a book number.

**Independent re-derivations that TIE (different seat, different code path):** group/account census
201 / 6,155 / 90.6% and the role-tagged union $348,726,019.90 over 241 accounts both reproduce CRO's
published values exactly.

---

## 4. T1-3 -- NO SERVED CONSUMPTION (checked condition, not an intention)

| probe | result |
|---|---|
| a. Is it a chain stage? | `chain_49f_entrypoint.py:_stage_list` is an explicit hardcoded list; **0 references** to this file |
| b. Does anything import/invoke it? | `comp-find` **1 hit across 26,980 files** -- the file's own usage docstring. Nothing else |
| c. Can the tool write anywhere? | **no `boto3`, no `put_object`, no `urllib`/`requests`** -- the only `s3://` string is a docstring comment. Structurally incapable of writing or calling out |
| d. Is the ADVI serving root still empty? | `s3://opal-data-portal-v2/platinum/advi/49financial/` -- **0 keys** |

---

## 5. CONTROLS (run, not asserted)

- **DETERMINISM: STABLE.** Two independent runs, output JSON sha256 identical
  (`aaad066acfbec8df1866a8c89b60a452ca767a93e4979728c00865fe90698135`).
- **MUTANT 1 (zfill(10) join removed): FIRED.** L3 collapsed 284 matched -> **0 matched, $0.00**. The
  join is load-bearing and the instrument discriminates.
- **MUTANT 2 (dedup bypassed): DID NOT FIRE -- and that is a finding about my own build, reported
  rather than buried.** Bypassing `dedupe_group_account` changed the book figure of **0 of 201 groups,
  total |delta| $0.00.** The collapse is done by `build_membership`'s dict keying, which is
  structurally incapable of counting an account twice; the dedup call's real job is narrower
  (deterministic newest-as-of row selection for the surviving row's *attributes*). The docstring was
  corrected to credit the enforcing mechanism. **A rule credited to the wrong mechanism is how the
  load-bearing one gets deleted later as redundant while the decorative one is kept.**

---

## 6. RESIDUALS -- named, owned, not chased

1. **The live qt6 run (L1).** Needs an egress holder. Route: `4.0.0_SA_CRO~A` under the continuing
   grant, or Andrew's word. Template `OPAL_CROA_Probe_GroupKey_qt6` id **517678** is already persisted
   in BD (216 groups x 3 months = 636 rows), so this is a re-run, not a new build.
2. **`Primary Portfolio Group` (dim 436) is NOT in the landed export.** The ruled basis names the
   primary-group partition; template 390224 selects only 2 Portfolio-Group dims (`Portfolio Group`,
   `Portfolio Group Market Value`), neither of them the primary key. **Today's L2 is a MEMBERSHIP view,
   not a primary-group PARTITION.** This is a direct input to T2-DIMS (`bridge_group_account.is_primary`)
   and is why that TO cannot be satisfied from the current export alone.
3. **The -0.163% like-for-like residual** and the **34 open accounts / $25.3M** our canonical does not carry.
4. **`Portfolio Group Market Value` (export col 89) is a trap** -- constant per *portfolio* (2,842 of
   2,875), varies within 179 of 201 groups. It is the denominator of `Account Allocation`, i.e. a
   portfolio-grain measure wearing a group-grain name. Deliberately unused; flagged in the tool.

---

## 7. COMPILER TOOLS

`comp-find` (content + `--name`) for the qt6/bd49f/oracle-reference censuses -- the T1-3(b) no-consumer
verdict rests on its printed denominator (1 hit / 26,980 files), which is exactly the frame a raw grep
would not have carried. `comp-which` exercised at startup per XXX.md A.3 (97 of 97 comp-tools resolve
bare; forwarder ran). `.tools/commit-gate.sh` on the new script: clean. `.tools/proof-of-spec-check.py`
on the instance.

## 8. SURPRISE CHANNEL (one line each, no action taken)

- `aws s3 cp` with a `/cygdrive/c/...` **destination** silently writes to a relative `C:\cygdrive\...`
  tree while reporting success. Pre-existing and estate-wide -- that stray tree holds scratch files from
  at least 6 other sessions. Use native `C:/...` destinations. Not chased; not deleted.
- `opal-data-bd/silver/allocations/` last partition is **2026-08-14** on what reads as a weekly cadence
  (07-31 / 08-07 / 08-14, Fridays). Healthy on that reading -- flagged only because CRO's scan describes
  this map as landing *daily*. **The `opal-data-assets/blackdiamond/49f/bronze/allocation_390224/` feed
  this oracle uses IS daily and IS current (as_of 08-18, pulled 08-19T02:30Z = correct T-1).** No outage
  claimed; a declarative question at most.

---

# ADDENDUM 2026-08-19 ~2245Z -- CORRECTION: THE SUPERVISION SLEEVE

Found while building T2-DIMS, when the T2 producer and this oracle disagreed on 14 of 201 groups.
Two of my own artifacts disagreeing is not shippable, so I chased it. **The oracle was wrong and is
now fixed** (@PENDING). Reported here in full because the numbers above were already delivered.

## What was wrong

Both tools collapsed to one row per `(portfolio_group, account)` and **kept a single row**. But an
account can be split by the vendor's `Account Supervised` column into a **Supervised** and an
**Unsupervised** sleeve, each carrying its **own** market value and allocation. Keeping one row kept
one sleeve and silently dropped the other.

## Why SUM is right, and it is proven not assumed

For every sleeve, `account_market_value / account_allocation == portfolio_group_market_value` **to
the cent** -- i.e. both sleeves divide the *same* portfolio total, so they are slices of one account,
not competing values:

| account | sleeve | market value | allocation | implied portfolio total | stated portfolio total |
|---|---|---:|---:|---:|---:|
| z0821416041 | Supervised | $145,177.38 | 0.036286132 | $4,000,905.31 | $4,000,905.31 |
| z0821416041 | Unsupervised | $2,887,004.52 | 0.721587815 | $4,000,905.31 | $4,000,905.31 |
| z0817426131 | Supervised | $16,275.20 | 0.016467561 | $988,318.79 | $988,318.79 |
| z0817426131 | Unsupervised | $272,407.72 | 0.275627381 | $988,318.79 | $988,318.79 |
| z0816967031 | Supervised | $488,502.34 | 0.097709973 | $4,999,513.61 | $4,999,513.61 |
| z0816967031 | Unsupervised | $497,895.00 | 0.099588688 | $4,999,513.61 | $4,999,513.61 |

**Positive control:** an ordinary single-sleeve account (z0812152081) satisfies the same identity
($448,489.82 implied == stated), so the identity is a property of the feed, not of these three rows.

**Key soundness:** within `(group, account, supervised)` the market value is constant on **29,926 of
29,926 keys -- zero exceptions**, so collapsing to one row per key loses nothing, while the 554 keys
backed by multiple rows (an account reachable through two portfolios/relationships inside one group)
still correctly collapse to one.

## Impact -- and the headline is UNAFFECTED

**3 accounts, 19 `(group, account)` keys, 12 of 201 groups.** Total understatement recovered
**$24,605,360.68**. Corrected examples: Austin Thompson / Lane Curry - Local Ops / Ted Grant each
+$3,657,307.24; Collin Plotts +$3,159,412.24; Sydney Cobb / Patrick Mundlin / Campbell Huber each
+$2,887,004.52; 49F Schwab AUM +$272,407.72.

> **TRAVIS PENFIELD IS NOT AMONG THE 12. His book is $392,556,451.10 before and after, so every
> number in sections 2 and 3 above -- including the +$79,366,493.25 (+21.03%) headline, the
> membership/coverage/valuation split, the attribute view, and the $405.4M double-count correction --
> STANDS UNCHANGED.** What changed is the per-group table for 12 other groups and the
> distinct-account universe ($1.550B -> $1.551B).

## Cross-check after the fix

The two producers are now independent implementations that agree: the oracle reads the **bronze
xlsx positionally with floats**, the T2 producer reads the **silver parquet by name with decimal128**.
Across all 201 groups: **max |delta| $0.005, total |delta| $0.18** -- and the two $0.005 items are
this oracle's `round(x, 2)` on values ending in exactly `.725`/`.755`, not a computation difference.

## The control that had to be re-run

**MUTANT 2 NOW FIRES.** Bypassing `dedupe_group_account` changes **79 of 201** group books, total
|delta| **$206,733,899.92** (Travis inflates to the $405,399,972.00 raw row sum). The earlier
"did not fire, 0 of 201" result was **true of the earlier code** -- adding the sleeve term changed
the mechanism, because sleeves are now SUMMED rather than collapsed by dict keying, which makes the
dedup call the only thing standing between the book and the raw row sum.

**The transferable lesson, and it is why this is in the record rather than a quiet edit: a mutant
result is a statement about the code AT A VINTAGE, not a permanent property. Change what is being
aggregated and every control over that aggregation must be re-run, or you carry a stale verdict
about your own instrument.** The docstring has been corrected a second time accordingly.
