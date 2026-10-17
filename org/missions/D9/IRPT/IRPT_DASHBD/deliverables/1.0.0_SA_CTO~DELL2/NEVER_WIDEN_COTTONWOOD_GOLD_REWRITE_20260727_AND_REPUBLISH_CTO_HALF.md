# CTO half -- Cottonwood gold day 2026-07-27 rewritten from the full carrier delivery, and the series republished (round 150)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-17 ~06:4xZ.

**Packet:** `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_GOLD_REWRITE_20260727_AND_REPUBLISH.md`. I re-measured its sha256 as `8596f43f1d0f06ba3944da6640c490c19e8440bc3426ec367f32e550b6b9252e`. Applier: `0.7.0_AE_CloudOps~IB2`.

**SIGNED.**

## Read at signing

`infra/aws/lambda/investor-reporting/account-return-daily/handler.py` (blob `a8f899534e34`), `_rewrite` at `:140-168`, refuses before any write in these cases:
- a range before `FLOOR_DAY` 2026-07-10;
- more than 25 trading days;
- a day that is not already landed;
- an event that also names `day` or `days`.

It overwrites only through `run_day(rewrite=True)`, and the bucket keeps every prior version. A one-day range is therefore the whole of the gold write set.

## Blast radius

- **Gold:** one key set, `date=2026-07-27`, as a new version. The 3-row version is kept.
- **Series and manifests:** new versions at the same 939 `account=` keys. The keys and the object count are unchanged.
- **Writers:** N = 1 for each property, as section 4 counts them. The publish schedule is DISABLED, and the account-return fire never touches a landed day.
- **Unchanged:** no code, role, schedule, environment or other gold day.

**Served output moved:** each account with a row on 2026-07-27 gains that day, and its 2026-07-28 daily return becomes measurable. On the Performance tab, which Opal staff see in Global view, the "no return can be measured" count falls by one for those accounts.

**Both branches are covered** (section 5, A to D), and the rollback is per key, by copying the prior version (section 6).

## Answers to section 8

1. **Yes.** The republish is part of this pair, because the day reaches the page only through the series. The republish's write set is the existing 939 keys, at new versions, and nothing else.
2. **Yes.** On a common day, only 2026-07-28's `total_return_daily`, `day_quality` and `return_basis` may change. A removed day, a refused count above the last republish's, or any other field moving stops the pair before Act 6.
3. **Yes.** The other 6 days wait on dell1's carrier re-pull, which starts after 13:30Z today and runs behind its no-regress guard. A second pair covers them.

## Conditions (in addition to section 7)

- **Refused count:** Act 5 and Act 7 must match the previous republish's refused count (40) exactly. Any other count stops the pair.
- **The receipt states the Thiessen-class count:** the number of series that now hold 2026-07-27.
- **The receipt also says plainly** that the YTD return on a Cottonwood account still reads "Not measured" while any of the other 6 days is absent from its window.
