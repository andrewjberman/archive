# BRIEF for 0.4.0_DS_ClientPlatform~B -- Door 5, the collision scripts (AoR link VERIFIED), and how the inf-pipeline situation meets your B1 drive

**From:** 0.6.2_AE_PartnerETL | **Date:** 2026-07-15 ~19:4xZ | **CC:** 1.0.0_SA_CTO (B1 gate owner)
**Authority:** Andrew-direct (my terminal ~19:3xZ): "We are currently sending out DS~B to go check out
and repair the inf-pipeline, so I'd recommend briefing them on the Door 5 scenario and these scripts
with the context of what has been going on thus far on the inf-pipeline."
**Standing:** I am NOT in your lane and this grants me no say in it -- this is context transfer from
someone who worked adjacent to the hold all day. Your TO (OPAL_GLDRNS.B1) + LD-0277 + the hold doc
remain your law; where this brief and the hold doc differ, THE DOC WINS.

## 1. DOOR 5 -- the trap is shaped exactly like your day-0 step

Your B1 step 1 is a read-only ground-state audit. **The first log you open will try to recruit you.**
The chain dies at STEP ZERO: `orion-gold-dispatch.sh` `sync_scripts()` exits FATAL on a basename
collision -- `code/gold/build_assets_dim.py` (8,498 B) vs `code/silver/build_assets_dim.py` (9,244 B,
deployed 2026-07-10T23:37:24Z) -- BEFORE any chain step. Every dispatch since 07-10 dies there. That
accidental FATAL is the ONLY thing holding the held chain, **and the error message prints its own
remedy.** An engineer doing obvious housekeeping clears it in five minutes and is "right" to by every
normal standard. That is Door 5.

- **The test is by EFFECT, never verb** (hold doc, verbatim class): *"would this make
  `code/gold/build_assets_dim.py` and `code/silver/build_assets_dim.py` stop being two different
  files with the same name?"* If yes -- cp, rm, mv, rename, "make identical" -- DO NOT, regardless of
  how obviously correct it looks. Deploying UNRELATED scripts is fine (an unrelated .py leaves the
  collision intact).
- **Your deploy authorization does NOT cover the de-collision.** B1 authorizes code+TF deploys on the
  runner estate -- which makes a collision "cleanup" LOOK in-scope. It is not: the hold doc assigns
  the eventual open to 0.7.0, REVERSIBLY, revert pre-staged BEFORE the open, on Andrew's BY-NAME
  order ("that is the difference between a decision and an accident"). Your job per your own TO is to
  arrive at that gate with everything behind it green -- the open itself is not yours or mine.
- **What the FATAL is protecting** (why your TO's stamp-order section exists): the deletion class on
  the served NNA spine -- Patrick Scanlan's $52,604.80 short re-fires every run; 21 partitions are
  SPARED-not-protected (one late-posted txn deletes them while sum(advisors)==firm_total ties through
  the loss); a pre-fold time-lock stamp makes the $2.6M mis-attribution permanent. FOLD with real
  data -> verify -> ONLY THEN lock. Your TO has this; the linkage worth adding: **the FATAL is the
  reason those numbers are still safe TODAY.**

## 2. THE SCRIPTS -- Andrew's hypothesis VERIFIED this hour (new evidence)

Andrew's read ("the alternate script is probably related to the AoR update, but that would need to be
verified") is **CONFIRMED, read-only, on the bytes** (both copies pulled ~19:3xZ; diff on file):

- The two copies are the SAME script (ADVI_INFSHIP Phase-1 L4, "build silver/api_dims/assets/ from
  canonical holdings, Path C"). **The ENTIRE diff is one comment block added in the silver copy**,
  dated 2026-07-10 -- an ADVISOR-OF-RECORD TODO, verbatim:
  > TODO(advisor-of-record 2026-07-10): noel_soderblom is NOT in this allowlist and has no servicing
  > rep_id, so if/when this (currently frozen / DI-8) producer is re-activated it will DROP Noel's
  > ~61 advisor-of-record mover accounts from silver/api_dims/assets -- under-counting his
  > top_holdings/assets cross-check and firm AUA. This producer also applies a business-row-filter at
  > the silver layer (advisor_key.isin allowlist), which is a Rule-17 violation. Do NOT patch the
  > allowlist in isolation: noel needs the advisor-of-record capture at silver (raw udf7ADVISOROF
  > passthrough) + a dynamic / fold-aware allowlist before this is reactivated. See
  > lib/inflection_rep_scope.py and the advisor-of-record re-key in INF_C_07/INF_B_00.

Three implications for YOUR drive:
1. **The collision-creating deploy was an AoR ANNOTATION-BANKING act** -- zero functional delta,
   comment only. Whoever wrote it was recording exactly the class of AoR hazard your B1 exists to
   retire, and deployed the annotated copy into code/silver/ while the original sat in code/gold/.
2. **The silver copy is NOT junk -- it is the NEWER copy carrying a load-bearing AoR warning.** The
   "obvious cleanup" (delete the stray silver copy) would destroy the annotation. When Door 5 is
   eventually opened (0.7.0, sovereign order), the correct de-collision PRESERVES the annotated
   version and resolves the PLACEMENT -- design input for whoever stages that open; not an action now.
3. **The TODO's content is inside your chain work:** Noel's AoR capture at silver, the fold-aware
   allowlist, the INF_C_07/INF_B_00 re-key. This producer is frozen (DI-8, one of the frozen-3) and
   must NOT be reactivated pre-fold -- reactivation both drops Noel's ~61 accounts AND is the Rule-17
   violator the TODO names. It unfreezes only as an in-order chain step at the hold-lift (your TO's
   frozen-3 clause) -- and now you know WHY that specific file is in the frozen-3.

## 3. Falsified beliefs -- do not re-derive these (the doc's own table)

- "Repairing bronze lets the chain complete" -- FALSE. The chain dies BEFORE the pull; bronze is
  irrelevant to the freeze.
- "Orion recovering fires the deletion" -- FALSE, retracted by its own author. There is NO vendor clock.
- "The staleness ceiling / dispatch lock is holding the line" -- FALSE. The accidental FATAL is.
- Also pre-answered for you (my 07-10-frontier artifact @ 195653e85, CTO-certified today): the
  monolith orion/eclipse bronze frontier at 07-10 is the raw producer dead under THIS hold; the
  ingestion mirror is healthy and at set parity. Nothing on the monolith side needs you.

## 4. Instruments + the adjacent doors (so an alarm doesn't read as a defect)

- **DOOR instrument = ETag:** gold vs silver copies differ (different size/ETag) = the door is SHUT.
  A one-line check, safe to run any time, never touches the files.
- **CHOKEPOINT = the Lambda env var** `INF_GOLD_DISPATCH_RELEASE` on `inf-gold-trigger` -- NEVER the
  `s3://opal-data-inf/control/` prefix (it reads EMPTY both ways). And per the hold's own lesson: an
  env var nothing reads is a comment with a dtype -- EXERCISE the refusal, don't config-read it.
- **Door 2 = the Wednesday staleness ceiling one-line "fix" -- ENGAGED TODAY (07-15).** You WILL see
  its alarm; the alarm is TRUE and the fix stays SEALED.
- **Door 6 = hand-writing `opal-data-inf/gold/meta/pipeline-complete.json`** (your TO has it; both
  watching roles measured implicitDeny). Corollary from LD-0292: **"re-run mdpf" == writing the
  sentinel == Door 6** -- the known-wrong frozen $528mm reclass stays frozen; a known-wrong frozen
  number is strictly safer than an unheld pipeline.
- **The functional test for every act:** "would doing this ADVANCE the INF chain?" A CHECK does not;
  a FIX does. Your TO makes advancing the chain THROUGH ITS GATES your job -- the doors are the
  paths AROUND the gates.

## 5. Facilitation -- what I can carry for you

- The pulled pair + diff live at my session scratchpad door5/ (mortal); THIS brief carries the
  verbatim diff, which is the whole delta. Re-pull is two read-only GetObjects if you want bytes.
- My frontier census script + artifact (@ 195653e85) cover the monolith-side questions so you never
  need to leave the opal-data-inf estate.
- I hold the schwab/monolith lanes and can answer anything on the mirror/ingestion side same-hour;
  I will NOT touch the inf estate. Base 0.4.0_DS holds your AoR-adjacent history (your TO's
  coordination row) -- their delta-6/D1 work today is unrelated to your chain.
- If your ground-state audit finds anything that contradicts THIS brief, the live estate wins and I
  want the correction (I'll re-issue, not defend).

Good hunting. The gates are real, the numbers behind them are real money, and the whole fabric wants
your drive to reach Andrew's word with nothing left but the word.
