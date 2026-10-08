# COO half -- NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE (IRPT_DASHBD, DB-b-41) -- WITHHELD

**Seat:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-07 ~23:1xZ | **Packet:** `deliverables/0.9.0_WK_IRPT_DASHBD~23/NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE.md` @ef8637f37c (merged @f3500197db)

**Status: WITHHELD, not refused.** The blast radius, rollback, branches and pins in the packet are read and accepted as written. The half
is not signed because two preconditions are not met, each a row:

1. **Sizing (row S31 on W23-S2).** The lots stage is measured on 20 accounts only (about +35 s, about +764 MB). The population is 7,597
   accounts against a 900 s / 2048 MB function. I do not accept the first-fire risk: the half is signed when one trading day over all
   7,597 accounts is measured (wall time and peak memory printed) inside both limits, or the stage is split so it is.
2. **The re-pin of account_return_daily.py (row S32 on W23-S6).** Pin 0 ships the round-25 classify_and_sum change to a function running
   pandas 2.2.3. The half is signed when DB-b-43 passes on pandas 2.2.3 and the returns table is byte-identical under 2.2.3, old pin
   against new.

When both hold, this file is replaced by the signed half, which also supersedes the round-22 class pair as the packet states. Until then
the round-22 class pair stands and no apply of `infra/aws/terraform/investor-reporting/reporting-gold` is made by this seat.
