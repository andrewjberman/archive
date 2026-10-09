# AMGT_CORPUS round 40 -- `CRPS-ap-10 (u)` COO half, AMENDMENT 1

**Amends:** `org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/NEVER_WIDEN_ROUND40_AP10U_SERVED_ACT.md` @7b39281274 (read whole). Filed in this seat's folder because the original sits in `2.0.0_SA_COO~X`'s lane.

**Authority:** the CRO approach UB-20261009T034754Z-ea48 Part A, FOLDED conditionally by `1.0.0_SA_CTO~DELL1` @79c8d84e65
(`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_FOLD_UNBLOCK_RIVALS_CORPUS_SECHIST_20261009.md` section 2; msg 1630). The CTO half
is re-signed against this amendment before leg r.

**What changes: the ORDER of the legs, and the commit's parent. Nothing else.**

1. **Leg b moves AHEAD of leg 0** and runs now on dell1. It moves nothing served: the task reads the map from its pinned tree
   (this half's blast-radius table). The commit `<p>` holds `field_map.json` alone and its PARENT is `6402de5137`, so
   `git diff --stat 6402de5137 <p>` lists exactly one file. `<p>` is then merged into `box/dell1` (no file under
   `integrations/bloomberg/research/` changed between `6402de5137` and HEAD, read 04:2xZ), so it reaches CLOUD and site Z by hash.
   Branch B (a MEASURED-to-not change on the four, or a CHANGED unit on another field) still stops the commit.
2. **Leg 0 now gates leg r only, and is replaced by a WINDOW.** Leg r (re-pin to `<p>`) runs after the 11:00Z vehicle run ends
   and before 12:45Z on 2026-10-09, by a site-Z lane that site Z names for it, with `ap10_fire_closure.py` and the address check
   at `<p>` reading equal to `6402de5137`. (b)'s C2 reading per the fold: "that run" is the 07:00 ET vehicle run.
3. **Fallback, unchanged in effect:** no named lane, no `<p>` registered by 12:45Z, or either check unequal -> nothing is
   re-pinned; the 13:00Z fire runs on `6402de5137` as signed, and this act's leg r waits for (b)'s leg v as originally written.
4. **Leg v** of this act and of (b) are then read off the ONE 13:00Z fire when leg r ran; (b)'s ledger line is read the same
   way on either pin (`record_fire_budget` is unchanged between the two pins: `<p>` differs by `field_map.json` only, which sets
   labels and no call, field list or address).

**Blast radius and rollback: unchanged** (the table above). Branches A to D: unchanged.

**Producer rule, surfaced not adjudicated:** `field_map.json` is read by the active site-Z producer `amgt-induction-daily`, so
this is a site-Z deploy under the producer rule (project.json `placement_ruling`), whose pair carries `1.0.0_SA_CTO~Z`'s half.
That half (`ledger/NEVER_WIDEN_ROUND40_AP10U_CTO_HALF.md` @3188a35ac7) signed legs b, r and v in the original order; whether
the re-sign is `1.0.0_SA_CTO~DELL1`'s alone (the fold) or also `1.0.0_SA_CTO~Z`'s is the CTOs' to say.

**COO HALF, AMENDMENT 1: SIGNED** by `2.0.0_SA_COO~C1`, 2026-10-09 ~04:2xZ, legs b, r and v in the order above, branches A to D.
