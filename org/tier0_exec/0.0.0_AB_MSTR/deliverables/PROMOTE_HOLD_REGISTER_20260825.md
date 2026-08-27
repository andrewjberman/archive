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

## (1) ETFS PROMOTE — ✅ DISCHARGED 2026-08-25 ~05:23Z, PROMOTE EXECUTED ~05:47Z

**AUTHORIZED BY ANDREW HIMSELF, at the site-Z MSTR terminal, ~05:23Z. VERBATIM** (carried as TEXT by
`0.0.0_AB_MSTR~Z`, not as a citation, because a cross-fabric citation is not discharged by a commit
sitting on the other fabric's disk):
> *"Yeah we need an 0.2.0_DT_PortfolioAnalytics~Z agent spawned to run the /prod-deploy"*

**He named the SERIAL and he named the ACT** — the hold's own author, ~14 hours later, directing the
exact act the hold was against, at a terminal where the prod-deploy was the live subject.

⛔ **CORRECTED 2026-08-25 ~08:0xZ -- CONDITION (ii) WAS **NOT** MET. THE AUTHORIZATION STANDS ANYWAY.**
`0.0.0_AB_MSTR~Z` retracted their own corroboration after `0.2.0_DT_PortfolioAnalytics~Z` caught it,
and **Andrew named the defect himself at ~07:3xZ: *"this fabric never completed the Asset
Sub-Categories for the ETFs."***
**His condition (ii) verbatim:** *"and it displays properly on DEV build with GICS replaced for
sub-categories on frontend."* **That names the ASSET SUB-CATEGORIES PANEL. IT RENDERS A
PLACEHOLDER** -- `PositioningSummary.tsx:361` gates the whole panel on `attributionData?.portfolios`,
`:562` `enabled: caps.attribution` is OFF in ETF mode, and `:489` pushes a `'-'` label on an empty
segment set.
⛔ **THE AUTHORIZATION IS UNAFFECTED AND THAT DISTINCTION IS THE WHOLE POINT.** His 05:23Z
instruction is **independent of the conditions and sufficient on its own** -- he named the serial and
the act, ~14h after setting the hold, at a terminal where the promote was the live subject. **Case
(a) stands unqualified. (b) does not, and (b) was never load-bearing.** *The defect is in the
corroboration, not the authorization.*
**WHY ~Z's TWO EVIDENCES BOTH FAILED, and it is the night's recurring class:** their *"his own words
at the render ~05:06Z"* were about the **PERFORMANCE panel**, a different panel; their *"sub_asset_class
carries 13 GICS values"* is the **DATA plane**, and the condition is about the **RENDER**. **The data
carrying GICS is exactly what makes the blank panel a FRONTEND defect rather than a data lack -- so
their own evidence, read correctly, pointed AT the failure.** Authorship made it worse: they had
personally measured the 13-value vocabulary an hour earlier, so the fact felt checked.

**WHAT WAS ORIGINALLY CLAIMED (kept for provenance):**
**BOTH OF HIS NAMED CONDITIONS WERE MET AND MEASURED BEFORE THE CUT:**
- **(a) full data structure for all ETFs — MET.** Served `platinum/etfs/positioning_data.json`
  126,863 B @04:53:51Z, `data_as_of` 2026-08-24, four books full, **177 of 187 rows at 8/8 return
  windows**; residual 4 partial + 6 correct nulls, every one enumerated and attributed.
- **(b) displays properly on DEV with GICS replaced by sub-categories — MET, AND HE CONFIRMED IT AT
  THE RENDER HIMSELF** ~05:06Z: *"We now have full performance for everything but still missing SALXX
  YTD and 1Y"*. `sub_asset_class` carries the GICS sector vocabulary, 13 values.
- **The SALXX residual does NOT reopen (a)** — he ruled on it ~06:1xZ (*"recs approved"*):
  complete-coverage-or-NULL does not bend. **Those blanks are a RULED state, not an incomplete
  pipeline.**

**WHAT LANDED:** `origin/PROD` **d9a98bcc**, tag **portal-v2.1.165** (peeled == PROD), cut from
`origin/DEV` 063ff4d7, **parity diff `origin/DEV..d9a98bcc` = 0 BYTES**, CI *Deploy to Production*
SUCCESS. Executed by `0.2.0_DT_PortfolioAnalytics~Z` — the serial he named — at 05:47:35Z.

### ⛔ THE REAL DEFECT THIS SURFACED, AND IT IS A RECORDING FAILURE, NOT A PROMOTE FAILURE

**I could not find a lift on this fabric and asked rather than concluded. `0.0.0_AB_MSTR~Z`'s answer:
the record did not exist.** They broadcast his sentence verbatim to their fabric and **never wrote a
durable Andrew-direct record for it** — the authorization lived in MCP message bodies and in a
session log written *before* the instruction arrived. **Nowhere a searcher would look, and nowhere
this fabric could reach.**
**Their words: *"I CONFUSED BROADCASTING THE WORD WITH RECORDING IT."*** That is Rule 22b's
SENT-vs-READ confusion one layer up.
⛔ **SO MY "I CANNOT FIND A LIFT" WAS A TRUE MEASUREMENT OF A RECORD THAT DID NOT EXIST, NOT A
VISIBILITY GAP ON MY SIDE** — and I had explicitly declined to draw that conclusion, which was the
right call for the wrong reason: I hedged on cross-fabric visibility, and the actual answer was that
there was nothing to see anywhere. **A register that cannot find an authorization is doing its job
whether the cause is distance or absence.**
Now written by them at `.../laneZ_ANDREW_DIRECT_20260825_0523Z_PROD_DEPLOY_AUTHORIZED_ETFS_POSITIONING.md`.

### ⛔ STILL OPEN — NOT MINE TO CLOSE
`org/critical_paths/change_management/20260824T1241Z_etfs-positioning-prod-promote-v2-1-165_deploy_completion.md`
reads **`Status: OPEN`** on this fabric. The act it tracks has now COMPLETED, but **the completion
facts live at site Z and NEVER#6 makes closing it an evidence act, not a bookkeeping one.** Routed
to them; **this register does not close another fabric's deploy ledger.**

### ⛔ THE HOLD AS IT STOOD BEFORE — kept for provenance

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

## (3) PERFRP — ✅ ADJUDICATED BY ANDREW 2026-08-25 ~08:5xZ. ACCEPT ON PROD, NO REVERT. THE DATA HALF STANDS.

**ANDREW-DIRECT, base CTO terminal, VERBATIM** (relayed by `1.0.0_SA_CTO` 69834, recorded +
broadcast same turn):
> **"I'm fine with it on PROD, let's just get the data part sorted"**

**THIS IS THE ADJUDICATION THIS REGISTER EXPLICITLY DECLINED TO MAKE.** The entry below stated two
available readings and said the choice was his. **He chose, and he chose the reading neither
recommendation favoured** — CTO's REC was REVERT; he ruled ACCEPT.

⛔ **HIS CONDITION HAD TWO HALVES AND HE RELEASED EXACTLY ONE.** The original word was *"stay on
the DEV branch not promoted to PROD **UNTIL WE KNOW THE DATA PIPELINE AND ALL UNDERLYING DATA IS
VERIFIED END TO END**."*
- **BRANCH HALF — RELEASED.** No revert, no promote hold, nothing owed by
  `0.2.0_DT_PortfolioAnalytics~Z`, who was never at fault.
- **DATA HALF — NOT RELEASED, AND NOW THE WHOLE OF IT.** *"let's just get the data part sorted"*
  **says the data is not sorted.** The publish gate STANDS; zero PERFRP leaves served remains the
  correct state.
>> **READING THIS AS A GENERAL LIFT WOULD BE THE WIDENING THE LAW FORBIDS** — and it would invert
him precisely: he dropped the half that was protecting nothing and pointed at the half that is. <<

⛔ **AND HIS SENTENCE CONFIRMS THE STRUCTURAL FINDING RATHER THAN OVERRIDING IT.** What was
measured here — that BRANCH POSITION PROTECTED NOTHING (two promotes in 45 minutes, two unrelated
projects, neither naming a passenger, while the DATA gate held and nobody had designated it as the
protection) — **is what he said in one sentence.** The branch was never the thing he cared about.
*The finding was right; the recommendation drawn from it was the wrong half.*

**WHAT "THE DATA PART" POINTS AT** (both already in flight, neither this register's to drive):
`twr_daily`'s 12:45Z SCHEDULED run (`GLD-f-1`, `0.4.0_DS_ClientPlatform~G` — **nobody accelerates
it; an ad-hoc run is not production evidence**), and Cottonwood's ingest gap
(`MODEL_DETAIL_SCOPE=all`, `WSE_COTMDL`, authorized and still unseated).

### ⛔ THE HOLD AS IT STOOD BEFORE — kept for provenance, INCLUDING the reading he did not take

⛔ **CORRECTED 2026-08-25 ~07:2xZ — THIS ENTRY FIRST SAID "ITS SUBJECT IS ON PROD", WHICH IS THE
SOURCE PLANE AND IS NOT WHAT THE QUESTION IS ABOUT.** `0.4.0_DE_ClientPlatform~D` crossed to the
plane that decides it and measured **the RENDER**:
> **FOUR OF FIVE CARDS RENDER ON PROD** — as shells with declared-absence faces and no figures. The
> slot is passed **UNCONDITIONALLY**: *"there is no branch that renders nothing."* The 4-of-5 ratio is
> **mutant-proven** by their L16 leg, not read off. Measured at `origin/PROD`, not their worktree.

**SO THE EXPOSURE IS VISIBLE UI ON A CLIENT-FACING SURFACE, NOT DORMANT CODE.** *"PERFRP commits are
on PROD"* and *"a 49F advisor sees four empty performance cards"* are two very different things, and
**only the second is what a sovereign would actually be ruling on.**

⛔ **FOUR SEATS MEASURED THE SOURCE PLANE AND NONE ANSWERED THE QUESTION** — COO measured commits on
PROD, CVO re-derived it with a negative control, AE~G confirmed independently, and **I put it in
front of Andrew in that form.** Every ancestor test, every negative control and every denominator
agreed with each other **because all of them were about the same wrong plane.** *No control inside
the wrong plane can catch a wrong-plane answer* — our own law, costing four seats to notice, on the
night it was re-recorded. **DE~D's question is the one that broke it: "nobody has said what a 49F
advisor would SEE."**

## (3) PERFRP — ⛔ THE SOURCE-PLANE MEASUREMENT — true, and NOT the deciding one

**PERFRP CODE REACHED PROD ON THE AUTHORIZED ETFS PROMOTE.** Measured independently at this seat
after `2.0.0_SA_COO` and `0.4.0_DE_ClientPlatform~D` raised it:
```
origin/PROD = d9a98bcc  "merge DEV->PROD: v2.1.165 -- ETFS_POSITIONING goes to production
                         for the FIRST time"   author 0.2.0_DT_PortfolioAnalytics~Z  05:47:35Z

79026413 (DE~D's PERFRP mount)  ancestor of origin/PROD : YES
8ecb6b68                        ancestor of origin/PROD : YES
NEG CONTROL 1af11910 (on DEV)   ancestor of origin/PROD : no   <- the test discriminates
PERFRP files in the PROD tree   : 9   (control: 1,065 files total on PROD)
```

✅ **THE PASSENGER WAS RECORDED. THE HOLD WAS NOT. THAT IS THE GAP, AND IT IS THIS REGISTER'S REASON FOR EXISTING.**
`3.0.0_SA_CVO` corrected their own "invisible sweep" framing after going to look:
`20260825T0543Z_etfs-positioning-prod-promote-v2-1-165-sitez_deploy_completion.md` **EXISTS**, names
`perfrp` **3 times** and the promote hash `d9a98bcc` **7 times**, and says verbatim:
> *"the promote carried another fabric's ADVI feature to production as a PASSENGER. It shipped fine.
> It shipped without anyone on this fabric reviewing it, AND THE PASSENGER WAS ONLY VISIBLE BECAUSE
> SOMETHING ABOUT IT HAPPENED TO BE RED."*
⛔ **SO THE PROMOTING SEAT DID ITS JOB: it recorded the passenger at deploy-completion, by name.
WHAT THE ENTRY MENTIONS ZERO TIMES IS THE HOLD** — because `0.2.0_DT_PortfolioAnalytics~Z` had no way
to know a PERFRP hold existed. **The recording worked; the hold-awareness did not.**
**THAT IS PRECISELY WHAT A PROMOTE-HOLD REGISTER IS FOR, and it is the argument for carrying this
file into every DT spawn brief** — a promoting seat cannot honour a hold it has never been shown, and
this one was on the other fabric.
⛔ **AND THE SEAT'S OWN SENTENCE NAMES THE REAL CONTROL GAP: the passenger was visible "because
something about it happened to be RED." THAT IS LUCK, NOT A CONTROL.** A passenger that shipped clean
would have been recorded the same way and noticed by nobody.

⛔ **THE MECHANISM, AND IT IS THE PART WITH REUSE VALUE: A DEV->PROD MERGE CARRIES THE WHOLE BRANCH,
NOT THE AUTHORIZED SUBJECT.** The ETFS promote was properly authorized (hold (1), discharged above,
his own word naming the serial and the act). **PERFRP rode it because both subjects sat on one
branch.** Nobody promoted PERFRP; a promote of something else carried it.
**NO SEAT DECIDED THIS AND NO SEAT IS AT FAULT FOR IT** — the authorizing word, the executing lane,
and the promote act were each individually correct. **The hold was branch-shaped and the carrier was
branch-shaped, and that is exactly the seam a per-subject hold has no way to hold.**

⛔ **WHAT I DO NOT DECIDE, AND WILL NOT:** whether this BREACHES his DEV-only word. Two readings are
both available and the choice is his:
- **It does** — his sentence was *"stay on the DEV branch not promoted to PROD"*, and PERFRP is now
  on PROD by any reading of the words.
- **It does not** — at 04:0xZ he ruled the hold binds **the PROMOTE ACT alone**, publishing is part
  of *"build it out"*, and **no promote act of PERFRP occurred**. The act that occurred was ETFS's,
  and it was authorized.
**ADJUDICATING A SOVEREIGN WORD'S BREADTH IS HIS, IN EITHER DIRECTION** — narrowing it to excuse this
and widening it to condemn this are the same error with opposite signs.

**WHAT IS NOT IN QUESTION:** his lift condition for PERFRP — *"validate that it actually works on the
backend side"*, EXERCISED — **has not been met.** `twr_daily` refuses 7,335 of 7,335 rows at the
frontier and the 12:45Z fire is the exercise. **So whatever the promote's status, the CONDITION the
hold protects is still open**, and that is a fact rather than a reading.

**NOT PROPOSING A ROLLBACK.** Moving served output is NEVER#3 and a rollback of a promote that also
carries an AUTHORIZED subject would un-ship ETFS, which he explicitly wanted live. **Any remedy here
trades one sovereign word against another and is his call, not an integrator's.**

### ⛔ THE HOLD AS IT STOOD BEFORE — kept for provenance

**Andrew-direct 2026-08-25 ~01:1xZ, received DIRECTLY at `0.7.0_AE_CloudOps~G` (not a relay).
VERBATIM:**
> *"Yeah we do want to build this out but it needs to stay on the DEV branch not promoted to PROD
> until we know the data pipeline and all underlying data is verified end to end."*

Record `@34791b8d31`. **He authorises the DEV build explicitly** — *"we do want to build this
out"* — so this holds the PROMOTE ACT only.

### ⛔ UPDATED 2026-08-25 ~04:0xZ — HE RULED THE SCOPE, AND ATTACHED A CONDITION

Andrew-direct, received DIRECTLY at `0.7.0_AE_CloudOps~G` answering their `/open-calls` CALL 1
(record `@2e9c58991a`). **VERBATIM, typo included because the phrasing is the ruling:**
> *"Agreeed with your rec"*

**He ratified a TWO-PART rec and BOTH PARTS BIND:**
1. **PUBLISHING IS PART OF "BUILD IT OUT."** The DEV-only hold binds **the PROMOTE ACT ALONE.**
2. **THE ATTACHED CONDITION, now HIS and no longer a recommendation:** *"PERFRP keys publish only
   after the round-1 emitters are wired and their first emission is read — never as a side effect
   of someone activating the publisher's schedule for the ten legacy twins."*

⛔ **A REC RATIFIED WHOLE IS RATIFIED WHOLE.** Reading only part 1 — the permissive half — and
dropping part 2 would be the widening the law forbids. **The condition travels with the permission.**

**THE MEASUREMENT THAT MADE THE CALL NECESSARY, and it is the durable half:** his 01:1xZ hold is
**BRANCH-SHAPED** (*"stay on the DEV branch not promoted to PROD"*) — **but the data layer is not
branch-scoped.** `platinum/advi/49financial/` is ONE key set in ONE bucket with no environment
conditioning anywhere in the read path, and the portal's `adviKeyRepoint.ts` records an exercised
200 through the auth path on DEV **and** on PROD. **PUBLISHING MAKES A KEY PROD-FETCHABLE WITH NO
PROMOTE OCCURRING.** The promote and the data exposure are two different events, and his earlier
sentence governed only one of them. *A branch-shaped instruction does not bind a plane that has no
branches.*

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

### ✅ THE SOVEREIGN RESIDUE — DISCHARGED 2026-08-25 ~04:1xZ

**Andrew ratified s.14. The card is closed.** At the base CTO terminal, VERBATIM:
> *"I do want to publish i want to get this shit live but we need to validate that it actually works
> on the backend side"*

**What it settles:**
- **PUBLISH INTENT IS AFFIRMED** — the direction is forward and his. Nothing downstream should
  sequence as though going live were optional or distant.
- **THE GATE'S TEST IS "ACTUALLY WORKS" = EXERCISED.** Not configured, not deployed, not green in a
  plan. **That is Rule 22a's BEHAVIOR layer in his own words**, and it RAISES the bar on every
  acceptance currently written as a config check.
- **s.14's SHAPE IS RATIFIED**, with leg **(a) CHAIN weighted as the operative one**; (b) CONTENT
  and (c) INDEPENDENT stand behind it. **The LIFT remains his at the promote act.**
- **It does NOT touch the two holds' independence** — he addressed the backend condition, not the
  register. (2) and (3) remain SEPARATE OBJECTS.

⛔ **THE RE-ORDER THIS CAUSES, and it is the actionable half: THE twr D-1 MIRROR REMEDY IS NOW THE
CRITICAL PATH TO A SOVEREIGN PUBLISH INTENT** — not a diagnostic, not a follow-on. `twr_daily`
refuses **7,335 of 7,335** rows at the frontier; **until the remedy lands the backend computes not
one return, and no amount of frontend work changes that.** Decomp @51e5086607, 26 cells,
`0.4.0_DS_ClientPlatform~H` seated on 21 (surfaces (a)-(d)+(f); (e) held out).

*Recorded for a successor: this seat HELD that remedy's seating earlier tonight on the ground that
it was "not on round-1's critical path." That was true when said and is now exactly inverted — by
his word, it is THE critical path. The hold was reversed before this ruling, on COO's showing that
its basis had died; the ruling then confirmed the reversal from the other direction.*

### ⛔ THE SOVEREIGN RESIDUE AS IT STOOD BEFORE — kept for provenance

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
