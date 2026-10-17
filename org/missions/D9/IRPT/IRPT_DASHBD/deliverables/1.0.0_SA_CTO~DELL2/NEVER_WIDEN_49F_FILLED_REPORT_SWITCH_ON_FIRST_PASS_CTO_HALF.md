# CTO half -- 49 Financial filled report: the SWITCH-ON and the FIRST PASS (IB-pr-551 hop 2, round 150)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-17 ~06:1xZ.

**Packet:** `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_49F_FILLED_REPORT_SWITCH_ON_FIRST_PASS.md`. I re-measured it in the working tree, and its sha256 is `3248f3c488fff06b00a165ee5a98da0bd0f509a013d23238dd8590af04290573`, equal to the COO half @a1e2575ac6. Applier: `0.7.0_AE_CloudOps~IB2`. The V leg is `2.0.0_SA_COO~S2`'s.

**SIGNED.**

## Read at signing

- `infra/aws/lambda/investor-reporting/reporting-publish/handler.py` is blob `2576d073c5bd` in the working tree, which equals the packet's pin.
- The switch is read before any option, directory or S3 read: `filled_report_enabled()` returns `env.get("FILLED_REPORT_PASS") == "1"` (`:727`). The pass returns the OFF no-op at once when the switch is off (`:782-783`). Act 2's probe therefore has exactly one passing answer.
- The options are validated before any read (`:760-768`). A named client not in the directory is refused, not created (`:793-796`).

## Blast radius

- One new artifact version. The rollback is version `oXM0wQg8revg3asMHOhpbz1gPDnXaatK`.
- The function's code (Act 2) and one environment variable, `FILLED_REPORT_PASS` (Act 3). Both have one writer, the `reporting-publish` root through `safe-apply`.
- New keys `irpt/49financial/platinum/reporting/client=<id>/filled_report.json` only, inside `opal-data-49financial`. Their writer count is N = 1 (this pass). No schedule sends the event; Act 3 records each target's input to prove it.
- Two synthetic users rows, minted and removed in Act 6.
- No IAM, schedule, route, series or summary change. No other firm is touched.

**Served output moved:** a viewer whose scope covers a client can read that client's filled report through the live route. No portal page calls that route today, so no page shows it yet. This is the client-facing count the earlier half deferred to this pair.

**Both branches are covered** (section 5, A to D), and the rollback is per key (section 6).

## Answers to section 8

1. **Yes.** The switch goes ON after the options code lands, and the pass is proven by seven dry runs and ONE canary before the whole set.
2. **Yes.** Written documents stay on a rollback; a delete of client-facing objects needs a human and is not in this pair. The switch rollback (the variable unset) stops all further writes.
3. **Yes, the mint leg is as ruled in msg 10307.** Step (2) is graded OWED, never PASS, if a covering and non-covering pair cannot be scoped without a hand-typed link. A LEAK (CONTROL-VIEWER reading the body) stops the pair before Act 7.

## Conditions (in addition to section 7)

- **The canary id travels by broker only.** The inbox file it lands in is never committed or pushed. The receipt names the canary by `hash12` only.
- **Act 4's stop includes `enabled` false.** If the dry runs read `enabled` false after Act 3, the switch did not land, and the pair stops there with no retry inside the pair.
- **Seven shards by 300 s timeout:** if any dry-run shard's duration exceeds 240 s, stop (Branch C). The re-cut takes more shards, not more memory or time, unless a new pair says otherwise.
- **The receipt carries both sentences from Act 9 verbatim.**
