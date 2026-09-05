# BRIEF -- /drive v2: the COO's loop drives LIMBS, not project status words

**From:** `0.0.0_AB_MSTR`, on Andrew-direct 2026-09-03 ~13:2xZ-13:3xZ at the MSTR terminal. **To:** `1.0.0_SA_CTO`
(skill law and the annex), `2.0.0_SA_COO` (the skill's owner-operator), `3.0.0_SA_CVO` (the companion tick). **Ledger:**
LD-0530. **Record:** `ANDREW_DIRECT_20260903_132xZ_DRIVE_V2_AGREED_COMPLETELY.md` (same directory).

## 0. His words, verbatim

> I also want to see the drive skill, I'm wondering if we can adjust it to tighten it up a little bit here so that we
> can really modernize it to head off most of these issues at the pass. COOs should be very aggressive in driving L5 L6
> activity. That seems to be where the break is happening.

Then, on the tightened shape in section 3 below, entire:

> I agree completely

## 1. The two requirements (the headline)

1. **The tick's unit is the measured LIMB of each active project**, in the `/canonical-flow` grammar (Ln, round, task
   orders terminal of total, decomposition cells covered of those serving an ungraded FWD), never the register's
   status word or the flat hot list.
2. **The COO is aggressive at L5 and L6 by construction:** the five obligations in section 3 run in order at every
   tick before any agent-liveness triage, and the loop is standing ON at 20 minutes for `2.0.0_SA_COO` over every
   project whose `dep_stage` reads `EXECUTING`, `ROUND_CLOSE` or `DECOMP`. This supersedes the standing OFF of
   LD-0288/0289/0293 on his word above.

## 2. Measured facts the brief rests on (2026-09-03)

**The break is between limbs, not inside them.** NFRA_COMPEFFICACY today, from the tree's commit times:

| Round | Last TO complete | L10 stamp | Next L6 cut | Idle at CVO (L8-L10) | Idle at COO (L5-L6) |
|---|---|---|---|---|---|
| 1 | 23:51Z | 00:24Z | 00:46Z | 33 min | 22 min |
| 2 | 01:35Z | 01:50Z | 02:06Z | 15 min | 16 min |
| 3 | 03:29Z | 03:54Z | 04:21Z | 25 min | 27 min |
| 4 | 05:03Z | 05:21Z | 07:35Z | 18 min | 2 h 14 min |
| 5 | 08:36Z | not landed at 13:10Z | -- | 4 h 34 min and counting | -- |

Rounds carried one to three orders each to one worker class; three CloudComp lanes sat live and idle between rounds;
14 of 31 decomposition cells had ever carried an order while FWD-2/3/4 read "every tool". Both Tier-1 seats were
pulled onto other work in the gaps, and with no loop the project moved only when a seat happened to read its inbox.

**The skill as it stands** (`.claude/skills/drive/SKILL.md`, 349 lines): unit = hot-registry project + flat task
order; classes ADVANCING / NEXT-ACTION-READY / STUCK-*; agent-liveness triage (2b) with a three-tick nudge ladder;
**cap 5 dispatches per cycle**; OFF by standing word, alive only in paired mode; no word for round, compile, stamp,
coverage or FWD, so a stalled stamp reads as "a gate someone else legitimately holds"; the L8 compile (COO's own act)
is never named; roughly half the text is liveness-oracle doctrine that belongs in `DRIVE.md`.

## 3. The tightened shape (agreed)

At every tick, for every project in scope, in this order, BEFORE Step 2b's agent triage:

1. **Graduated round -> L5/L6 same tick.** A stamped round with graduated rows (SPEC_ERROR -> L6, DECOMP_INVALIDATING
   -> L5) is acted on in the tick that reads it: the decomposition amended and the orders cut, not scheduled.
2. **Width rule at L6.** Every uncovered cell that serves an ungraded FWD and has no unmet dependency is cut THIS tick,
   one order per cell, one cell per lane; lanes seated via `/mstr-spawn` in the same tick under the COO's spawn
   authority. **The dispatch cap is retired**; the bound is the decomposition's own dependency axis. A cell that serves
   no FWD is never cut for coverage's sake (the completion marker is the FWDs).
3. **Terminal orders -> L8 compile now.** Every task order terminal with no compile packet at L8 is compiled by the COO
   in the tick; the compile is the COO's act, not a wait.
4. **The L8 packet at CVO:** unread (no READ ack) at one tick -> nudge citing ground truth; at two ticks -> `[STUCK]`
   to `0.0.0_AB_MSTR` naming the packet and the clock. Two ticks, not three.
5. **Idle lane + uncovered FWD-serving cell = a DEFECT** written in the tick's own log row, never a state; the remedy is
   obligation 2 in the same tick.

**Cadence:** 20 minutes fixed while any project in scope reads EXECUTING / ROUND_CLOSE / DECOMP; 60 minutes only when
none does. **Standing ON** for `2.0.0_SA_COO` (base) from the moment this lands; lane COOs (`~A` etc.) run the same
tick over their own team's project. **Paired mode** and its scoped no-op tick are unchanged for paired arms.

**The log** (substantive ticks only, as today): one limb table --
`project | limb | round | TOs terminal/total | cells covered/FWD-serving | act fired this tick` -- plus the existing
findings table. The identity gate, resolve-don't-attest, RAVC on every dispatch, Rule 27 (orders from cells only, seats
via MSTR), the sovereign exclusion list and the no-`jq` reads all stay. **The liveness-oracle doctrine (2b.2a's block
and its incidents) moves to `org/tier1_exec/2.0.0_SA_COO/DRIVE.md` whole**, leaving the imperative + gate + pointer
in the skill, per the skill's own last line.

## 4. The companion tick at the CVO (agreed in the same word)

The longest idle today was L8-L10 at `3.0.0_SA_CVO`, which no COO tick can perform. The CVO gets the same tick shape,
scoped to its limbs: **compile packet received -> L9 adjudication and the L10 stamp in the tick that reads it**; a
packet older than one tick without a stamp is the CVO's own defect row; `[STUCK]` to MSTR at two ticks when a stamp is
blocked on something outside the CVO's power. Cadence and log as in section 3. Skill name and file: `1.0.0_SA_CTO`'s
call (a `/stamp` skill, or a CVO mode of the same skill body); the obligation is the brief's, the form is the CTO's.

## 5. Mechanical acceptance (what "landed" means)

- **A tick over today's NFRA_COMPEFFICACY state at 12:56Z** (12 of 12 terminal, no compile, stamp unread) produces:
  obligation 3 fires (compile), obligation 4 nudges, and the limb table reads `L7 -> L8 | round 5 | 12/12 | 14/31`.
  **Falsifier:** replayed over the 08:36Z-13:10Z window, the tick nudges at 08:56Z and escalates `[STUCK]` at 09:16Z;
  the skill as it stands does neither (measured: nothing fired until Andrew's word at 13:0xZ).
- **Obligation 2 on the same state** cuts the eleven cuttable tool cells COO identified (93647) in one tick, not across
  rounds; a cell with an unmet dependency (CE-t-24 behind CE-t-10) is sequenced, not skipped.
- `python .tools/proof-of-spec-check.py` / the L6 gate are untouched: every order the tick cuts still passes
  `to-pipeline-gate.py` on its own; the tick changes WHEN orders are cut, never what an order must carry.
- The skill body shrinks: the moved doctrine reads in `DRIVE.md` at the same wording, cited by section.

## 6. Owners and sequence

1. `1.0.0_SA_CTO` lands the skill text (sections 3-4) and the `DRIVE.md` move; states the commit and the push state.
2. `2.0.0_SA_COO` arms it standing at 20 minutes on landing and runs the first tick over NFRA_COMPEFFICACY and
   NFRA_CLDGRPH; the first log is the acceptance artifact of section 5.
3. `3.0.0_SA_CVO` arms the companion tick on its landing.
4. `0.0.0_AB_MSTR` verifies loop-health under `/govern` (the standing note in the skill: `/govern` verifies `/drive`,
   it does not run it) and carries the first log's limb table to Andrew.
