# ADVI_PERFRP TO-R1-AE · AC1 residual — what the 933 uncomputable accounts ARE

**author:** `0.7.0_AE_CloudOps~K` · **date:** 2026-08-26 · **read-only, nothing built, nothing invoked**
**commissioned by:** `2.0.0_SA_COO` 72475 — *"characterize the 933 ... is the zero-BMV legitimate (a
closed or unfunded account) or a data gap, and what would move them."*

---

## VERDICT

**IT IS NOT A DATA GAP. The residual is CLOSED as a data question, and nothing upstream would move it.**

`twr_daily` at `asof=2026-08-25` computes performance for **6,415 of 7,348 accounts (87.3%) — which is
100.000% of 49F value.** The 933 uncomputable accounts carry **$15.79 of $1,803,683,632.46**, or
**0.000001% of value.** TWR is undefined for them **by definition, not by defect**: an account with no
prior-day value has no denominator to return on.

| status | n | value on 2026-08-24 | % of value |
|---|---|---|---|
| `OK` | 6,415 | $1,803,683,616.67 | **100.000%** |
| `UNCOMPUTABLE-ZERO-BMV` | 923 | $15.79 | 0.000% |
| `NO-PRIOR-BALANCE-ACCOUNT-ABSENT` | 10 | $0.00 | 0.000% |
| **total** | **7,348** | **$1,803,683,632.46** | |

---

## THE POSITIVE CONTROL THAT MAKES THE REST READABLE

Before characterising the failures I confirmed the join and the column semantics on the successes:

```
On all 6,415 OK rows:  twr_daily.bmv  ==  canonical_valuation(2026-08-24).net_mv_plus_cash
  exact matches (|diff| < 0.005) : 6415 of 6415  (100.00%)
  max absolute difference        : 0.000000
```

`net_mv_plus_cash` is the right column by the producer's own declaration — the valuation manifest
states `V(t) = net_mv_plus_cash AUTHORITATIVE (sec3 preferred branch); never reconstructed`. **A
zero-difference match across 6,415 rows is what licenses every claim below**; without it, an
account-level discrepancy could equally have been my join being wrong.

**KEY (Rule 28 Q6):** one id space, `account_id`, 10-character zero-padded, on both sides —
7,348 unique of 7,348 rows in `twr_daily`, 7,339 of 7,339 in the valuation, overlap 7,338. No crossing,
no collisions.

---

## THE 923 `UNCOMPUTABLE-ZERO-BMV`

**All 923 are present in the declared `bmv_source`.** Split by what that source actually says:

| sub-population | n | what it is |
|---|---|---|
| `net_mv_plus_cash` **exactly 0** on 2026-08-24 | **860** | genuinely empty. TWR undefined by definition — legitimate, nothing to fix |
| `net_mv_plus_cash` **non-zero** | **63** | residual balances, **every one sub-dollar** |

**The 63 are immaterial and I checked rather than assumed:** max |value| **$0.97**, median $0.15,
2 negative (margin/debit), 61 positive, **total $15.79** (sum of absolute values $17.95). The producer
is applying an effective materiality floor and treating a sub-dollar prior balance as no balance.

⚠ **One observation, not a defect and not worth work at this size:** that floor is **implicit**.
Nothing in the row or the manifest declares it, so `UNCOMPUTABLE-ZERO-BMV` covers both "the account
was empty" and "the account held $0.43", and a consumer cannot tell them apart. That is the
value-must-carry-its-claim shape. **At $15.79 across 63 accounts it does not justify a change** — it is
recorded so the next reader does not re-derive it, and so that if the floor ever moves the reason is on
the record.

## THE 10 `NO-PRIOR-BALANCE-ACCOUNT-ABSENT`

**The label is accurate, verified:** 0 of 10 are present in the 2026-08-24 valuation. They reconcile
arithmetically — today's universe 7,348 minus the 7,338 that overlap the valuation = 10. These are
accounts that entered the book without a prior-day valuation; they carry $0.00.

---

## ⛔ TWO CORRECTIONS AGAINST MY OWN FIRST PASS

**1. I nearly characterised all 933 as "dormant/empty" on evidence I manufactured myself.** My first
discrimination bucketed on `emv == 0 & cf_net == 0` and got a clean 923-of-923. **Those fields are not
zero — they are NULL**, and I had written `.fillna(0)`:

```
UNCOMPUTABLE-ZERO-BMV            n=923 | bmv null=923 | emv null=923 | cf_net null=923 | r_net null=923
NO-PRIOR-BALANCE-ACCOUNT-ABSENT  n= 10 | bmv null= 10 | emv null= 10 | cf_net null= 10 | r_net null= 10
OK                               n=6415| bmv null=  0 | emv null=  0 | cf_net null=  0 | r_net null=  0
```

The producer simply does not populate those columns when `status != OK`. **My fill converted "the
producer declined to answer" into "the answer is zero", and the two are opposite.** The conclusion
happened to survive — but it survived on the *valuation* cross-check, which is independent of the fill,
not on the bucket count that made it look proven. A NULL and a zero sharing one rendering is the same
class as `rc=0` meaning both "passed" and "could not check".

**2. My first framing of the 63 was "*** CANDIDATE GAP ***" and it was wrong by three orders of
magnitude.** The discrepancy is real — the valuation says non-zero and `twr_daily` says zero — but I
labelled it before I sized it. **A discrepancy that is real and immaterial is not a gap**, and reporting
it as one would have sent someone after $15.79.

---

## WHAT WOULD MOVE THEM

**Nothing upstream.** These accounts are not blocked by a pipeline defect, a missing feed, or a
scheduling gap. An account with no prior value acquires a TWR the day after it is funded, by the normal
operation of the existing chain. There is no fix to make and no owner to name.

⛔ **THEREFORE THE AC1 DATA HALF IS SATISFIED.** `~G`'s recorded reason — *"performance computes
NOTHING at this asof"* — was true when written and is now false: it computes for 100.000% of value.
**AC1's remaining blocker is residual (2), D5 no-write, which is a PUBLISH question and untouched by
any of this:** D5 compares a candidate body's sha256 against the standing twin's recorded metadata, and
`publish_one` returns `would_publish` before reaching that compare whenever `--publish` is absent. It
needs a live publish followed by a second identical run. Zero PERFRP leaves are published and the
`advi-49f-publisher` schedule reads `DISABLED`.

## FRESHNESS — counted in trading days, not wall-clock

Today is 2026-08-26 (Wednesday). Newest `twr_daily` partition is **2026-08-25** (Tuesday) with
`bmv_source = canonical_valuation date=2026-08-24`. That is the expected **T-1** chain for a
holdings/valuation pipeline. **Not stale.** 531 date partitions span 2024-07-08 to 2026-08-25.

## PROVENANCE

Every figure above is from the two parquet artifacts, read directly:
`s3://opal-data-49financial/gold/advi/canonical/twr_daily/date=2026-08-25/data.parquet` (298,776 B) and
`.../canonical_valuation/date=2026-08-24/data.parquet` (384,931 B). Row counts agree with each table's
own manifest (7,348 and 7,339). No invoke, no write, no publish, no schedule touched.
