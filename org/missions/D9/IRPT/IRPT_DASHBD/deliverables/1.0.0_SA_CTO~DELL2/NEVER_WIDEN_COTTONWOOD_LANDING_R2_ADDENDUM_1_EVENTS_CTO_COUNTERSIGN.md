# CTO countersignature -- Cottonwood landing rewrite R2, ADDENDUM 1: ten smaller events in place of four

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~20:1xZ. **Addendum:**
`org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_LANDING_CODE_UPDATE_REWRITE_R2_ADDENDUM_1_EVENTS.md`
(@aeaebb0b51), sha256 `e6f1f4b4759f5773d3c0b6baaaf3b73016e7ef57cbd5f7e795ca891489c20e06`, blob `34ea31df0d63`, 4,708 bytes (re-measured). It is
bound to the R2 packet, sha256 `962ef131`, which I signed @f362eb8cb5.

**COUNTERSIGNED.** The 25-day dry run timed out at 900 s and wrote nothing. Two small dry runs measured 113 s a day (July) and 13 s a day
(October), with memory flat at 639 MB. Ten events cover the same 66 days (the denominator is printed), cut around the three held days, at the
same keys, the same allowance and the same limits. The largest predicted event is 546 s, under the 720 s line and the 900 s timeout.

**Conditions:** a stop on any `Task timed out`, Max Memory Used above 819 MB, or an event over 720 s, before the next event. A partly
written event is read day by day: each day either holds a new version that passes the after-read, or keeps only its prior version. That
per-day state goes in the receipt, and the next event never starts over a day left between the two.
