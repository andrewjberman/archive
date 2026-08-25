# PROMOTE-HOLD REGISTER — live sovereign holds on PROD promotion

**Compiled:** 2026-08-25 by `0.0.0_AB_MSTR`
**Why this is a FILE and not a message:** the seat these holds bind — a DT instance — **does not
exist yet**, and **no sender can be relied on to guess a not-yet-existing seat's serial in
advance** (see the Delivery note at the foot: the first attempt at hold (3) went to the wrong DT
serial). A brief must be **liftable from somewhere**, and this is that somewhere. **Whoever briefs
the next DT instance lifts this file, verbatim.**
⚠ **NOT because mail to an unseated inbox is lost — it is not.** A QUEUED message IS read at that
seat's `org/XXX.md` Step 1b B startup pull. *An earlier version of this header said a message
cannot reach an unseated seat; that was overstated and is corrected here, at the top, rather than
only in the note at the bottom.*

⛔ **ENUMERATION ONLY. Nothing here is adjudicated.** Where a sovereign word is silent, this file
records the silence rather than resolving it. Reading a resolution into this document would be the
inferred-gate / widened-word class the estate has paid for repeatedly.

---

## (1) ETFS PROMOTE — NOT YET

**Andrew-direct 2026-08-24 ~15:2xZ, base CTO terminal. VERBATIM:**
> *"We are not positioned to promote yet. Until data pipeline is complete with full data structure
> for daily bloomberg data for all ETFs, and it displays properly on DEV build with GICS replaced
> for sub-categories on frontend."*

- Record: `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260824_OPEN_CALLS_49F_HELD_ON_MIKE_ETF_PROMOTE_CONDITIONS_BBG_PIPELINE_STRUCTURE.md`; restated `docs/architecture/ETFS_POSITIONING_PRD.md:751` (R2-1).
- **TWO NAMED CONDITIONS, both his:** (a) the daily Bloomberg data pipeline complete with full data
  structure for **all** ETFs; (b) it **displays properly on the DEV build**, with GICS replaced by
  sub-categories on the frontend.
- Live deploy-completion entry: `org/critical_paths/change_management/20260824T1241Z_etfs-positioning-prod-promote-v2-1-165_deploy_completion.md`
  — reads **HELD-PENDING-SOVEREIGN**, and on its own face: *"NOT COMPLETED. NOT ABORTED. NEITHER
  TERMINAL IS TRUE OF THIS ENTRY."* **Do not close it as either.**

## (2) 49F SOURCING — HELD ON MIKE (49 Financial)

Same record, item (1). `org/projects/ADVI_49FSRC.json` PARKED.
⚠ **This is a SOURCING hold, not a promote hold.** Listed because the PERFRP record names it as a
possible interaction — **not** because it is the same kind of thing.

## (3) PERFRP — DEV ONLY, NO PROD PROMOTE

**Andrew-direct 2026-08-25 ~01:1xZ, received DIRECTLY at `0.7.0_AE_CloudOps~G` (not a relay).
VERBATIM:**
> *"Yeah we do want to build this out but it needs to stay on the DEV branch not promoted to PROD
> until we know the data pipeline and all underlying data is verified end to end."*

Record `@34791b8d31`. **He authorises the DEV build explicitly** — *"we do want to build this
out"* — so this holds the PROMOTE ACT only.

### ⛔ Its condition is not merely PENDING — it has MEASURED counter-examples

Contributed by `3.0.0_SA_CVO`, whose function is verification. Both filed in
`org/surprise_channel/ADVI_PERFRP/INVESTIGATION_v1.md`, both found by the executing DS lane, both
re-derived or confirmed at the CVO seat:

- **`ADVI_PERFRP-S3`** — the canonical returns table is **HOLLOW AT THE FRONTIER**. `twr_daily`'s
  `r_net`/`r_gross` are physically NULL for every row across the five most recent partitions (529
  censused; 523 COMPUTED / 6 ALL-REFUSED; last COMPUTED 2026-08-07). **Refused partitions carry 9
  columns, not 13** — the four missing are `bmv/emv/cf_net/cf_gross`, *the operands returns are
  computed from* — so those partitions withhold the material to reconstruct the answer.
- **`ADVI_PERFRP-S7`** — **8 of 13 sources serve NO contract period.** Every shallow source floors
  2026-07-14 or later; the contract's earliest period start is QTD 2026-07-01.

**WHY THIS RIDES THE BRIEF:** *a hold whose condition reads "not yet done" is priced differently
from one whose condition has known failing measurements.* A DT seat reading *"verified end to
end"* with no attachments will reasonably plan for a verification PASS. These two say the
underlying data does not currently support one — **and they were found by the lanes building on
it, not by a verification sweep that has yet to run.**
**Neither CVO nor MSTR claims the condition is unmeetable.** Both items are GRADUATED-and-open with
named owners; neither blocks the DEV work his word authorises.

---

## Status of the four open questions — UPDATED 2026-08-25 ~01:5xZ

Originally flagged by `0.7.0_AE_CloudOps~G`, who declined to resolve them. **Two have since been
resolved and TWO OF THESE ENTRIES WERE STALE WITHIN THE HOUR** — corrected here, in place, rather
than appended below.

- **How wide is "this" in (3)? — STILL NOT STATED.** Said answering a PERFRP question. Whether it
  reaches the wider 49F ADVI serving surface is **not stated, and nobody has defined it.**

- **What counts as "verified end to end"? — DEFINED ON HIS BEHALF. NOT undefined.**
  `1.0.0_SA_CTO` defined it as **PRD author** in `ADVI_PERFRP` **s.14** (`@5e25201f74`; verified on
  `origin/CLOUD` and the text resolves there — a citation a reader can follow). **This is INSIDE the
  delegation AE~G's own verbatim record names** — *"is his call OR THE PRD AUTHOR'S ON HIS BEHALF"*
  — with **the LIFT explicitly reserved to Andrew**. A seat quietly defining a sovereign condition
  would be widening it; a PRD author defining a verification standard inside a named delegation, in
  the governed PRD, is the job the delegation exists for.
  **The standard:** (a) CHAIN — every serving family's lineage at Rule 22a's three layers, incl. the
  twr D-1 mirror remedy landed with real returns EMITTING on the scheduled run; deferred families
  verified AS DECLARED, never silently waived. (b) CONTENT — the s.11 #12 parity report vs the BD
  dashboard rendered on DEV and READ, per-figure deltas explained. (c) INDEPENDENT — CVO re-derives
  both legs.
  ⛔ **SO HOLD (3) IS `DEFINED-ON-HIS-BEHALF` AND `UNMET` — which is a state WITH A PATH**, not an
  undefined condition. Do not read it as blocked on a definition.

- **WHO VERIFIES? — ASSIGNED, and no seat self-appointed.** s.14(c) gives **CVO** the *independent
  re-derivation of the two component legs* — the per-deliverable verification function that seat
  already runs. **COO assembles** the satisfaction claim with denominators (the issuer act).
  **ANDREW LIFTS** (the sovereign act). Three seats, three verbs.
  **CVO's refusal STANDS and is compatible:** they declined to be certifier of the *whole lift
  claim*, which s.14 never asks of them. CTO has invited CVO to say if their read of s.14(c) is
  heavier than that, rather than letting the two positions diverge silently.

- **Are (2) and (3) one hold or two? — RULED: TWO, INDEPENDENT.** `1.0.0_SA_CTO`, on the record:
  the PERFRP DEV-only hold and the 49F switch hold (Mike) are **separate objects; satisfying one
  releases nothing of the other.** AE~G's conservative default is now **the ruled reading, not a
  working assumption.**

### ⛔ THE SOVEREIGN RESIDUE — real, and smaller than "define it"

**One line from Andrew: RATIFY s.14 as the standard, REPLACE it, or NAME A DIFFERENT VERIFIER.**
It rides CTO's open-calls list as the hold-(3) card. **Nothing in the chain requires any seat to
self-appoint to anything it refused**, and no seat should treat the standard as sovereign-ratified
until he answers — it is authored under delegation, which is not the same thing.

## Provenance and limits

**All three are HIS gates, stated unprompted.** None is agent-manufactured: the no-inferred-gates
rule bans minting an approval step from precedent or prudence, and does not touch a sovereign's own
word.

⛔ **THIS REGISTER DOES NOT CLAIM TO BE COMPLETE.** It enumerates holds that were **written**. **A
hold spoken and not recorded would not appear here, and there is no instrument for that.** Treat it
as a floor.

**Rule 19 is untouched** — the portal main tree stays on DEV always. These hold the PROMOTE ACT;
they are not a new mechanism, and PROD promotes remain a DT lane act via `/prod-deploy`.

---

## Delivery note (amended 2026-08-25, correction by `0.7.0_AE_CloudOps~G`)

This file exists because **a spawn brief must be liftable from somewhere**, and because **no sender
can be relied on to guess a not-yet-existing seat's serial in advance.** It does **not** exist
because mail to an unseated inbox is lost — **a QUEUED message DOES reach a seat that spawns
later**, read at `org/XXX.md` Step 1b B.

**Hold (3) has already been pre-positioned into `0.2.0_DT_PortfolioAnalytics`** — the serial Andrew
named — by `0.7.0_AE_CloudOps~G`, with the unstated scope items marked unstated. **Their first
attempt went to `0.4.0_DT_ClientPlatform` and was wrong**, which is the whole argument for the
brief: it is the one surface that does not depend on guessing the serial.
