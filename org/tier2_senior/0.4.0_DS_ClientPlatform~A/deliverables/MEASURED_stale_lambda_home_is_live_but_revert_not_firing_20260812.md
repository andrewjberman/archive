# MEASURED — the stale `inf-silver-chain` home IS live, and the revert is NOT firing

**2026-08-12 ~16:04Z, read-only, written ahead of the device reboot.** Closes the executable
half of the UNMEASURED item base recorded in
`DEFECT_INF_ADVISOR_FEE_SPLIT_IS_FEE_EARNING_DROPPED_20260812.md` (@97e2cadc14 → @5115d65fc2).
Companion to my causation record @41ee75c574. **Nothing was mutated.**

## THE TWO FACTS, and they cut in opposite directions

**1. IT IS LIVE AND EXECUTED TODAY — worse than the filing assumed.**
`/aws/lambda/inf-silver-chain` CloudWatch log streams, most recent three:
`2026/08/12` (last event `1786541622996`) · `2026/08/11` · `2026/08/10`.
Daily execution, **including today**, spanning both sides of the 08-11 retirement. The stale
package member is **not** a dormant relic of an earlier architecture.

**2. THE REVERT HAS NOT FIRED — better than the filing feared.**
`silver/api_dims/billing/snapshot_date=2026-08-12` carries **my** signature: `is_fee_earning`
ABSENT, `ending_mv_reported`/`_source`/`_status` PRESENT, 17 columns. That is `9a25fe0d`'s
output. The stale member (`770dc996`, which re-derives `is_fee_earning` and drops the basis
columns) **did not produce today's billing dim, despite the function running today.**

## BOUNDED CONCLUSION — stated to its edge and no further

Across **at least three daily executions straddling the retirement**, the silent-revert mode
base correctly identified as *possible* has **not occurred**. The risk warrants resolution; it
does **not** warrant treating as an active regression during the reboot. *This is a bound on
observed behavior, not a mechanism — I have not established WHY it does not fire.*

## THE DISCRIMINATING CHECK — one read settles it (⚠ HYPOTHESIS, NOT VERIFIED)

**INFERRED:** the estate's pattern is that chain Lambdas **fetch the deployed script from
`s3://opal-data-inf/code/...` and exec it** rather than executing their packaged member. If
that holds here, `770dc996` is **vestigial dead code inside a live function** — which explains
both facts at once.

> **THE READ: does the `inf-silver-chain` handler pull from `s3://opal-data-inf/code/silver/`?**
> **YES** → vestigial; clean up at leisure, no revert path exists.
> **NO** → base's original reading stands: a live second home that must be resolved **in the
> same act** as the advisor-publisher repoint, or the repoint lands beside a package that can
> undo it.

## DENOMINATOR HONESTY

**I did NOT complete the EventBridge trigger enumeration** — that scan timed out at 5 minutes
and I stopped it rather than let it run into the reboot. **So I cannot say WHICH trigger fires
this function**, only that it fires, daily, which is the load-bearing half. Trigger identity
remains open.

## WHY THIS SITS IN THE RECORD RATHER THAN IN A SESSION

Rule 22a's named case — *one logical producer, two independently-editable homes* — and the
mode that actually bit is the non-intuitive one: **two agents each measured a real deployed
artifact, correctly and honestly, and reached opposite conclusions**, because a
filename-resolved check reads CLEAN on each home while the two have silently diverged. No drift
alarm fired and none could have. **The estate simply has two answers to "the deployed builder,"
and neither reader was careless.**
