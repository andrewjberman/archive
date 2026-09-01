# TO OPAL_ADVIPOINTERS.P2-FLOOR-49F — schedule FLOOR for the canonical 49F runner chain + silver-completeness event accelerator (TF) (push plan §3 row 2, AE half)

<task_order id="OPAL_ADVIPOINTERS.P2-FLOOR-49F" project="OPAL_ADVIPOINTERS">
<issued_to>0.7.0_AE_CloudOps~M [RE-ADDRESSED 2026-09-01T07:5xZ by the issuer 2.0.0_SA_COO, from the bare BASE. REASON: the base holds NO live session (1pt process truth 0 hits, 1a NOT REGISTERED, 1b 0 markers) and it held 5 open TOs spanning TWO projects -- OPAL_ADVIPOINTERS and ADVI_INSURE -- a Rule 27 one-project-per-instance collision at seating time, so the base COULD NOT LAWFULLY BE SEATED on all of them. This lane takes the OPAL_ADVIPOINTERS four ONLY; ADVI_INSURE.TO-S1-AE stays at the base and is re-addressed separately. Authority: Andrew-direct 2026-09-01 ~06:5xZ full-force-on-D2 drive loop, XXX.md COO row @4469fc738c. Nothing else on these faces changes -- scope, acceptance criteria and sequencing are untouched.]</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T16:05Z</issued>
<dated>2026-08-19 build (TF draft today is fine — read-only prep per your 152834Z order; NO APPLY before tonight's 23:01Z bd platinum fixture passes). Unattended cycles 08-20/21/22 are the proof bar.</dated>
<status>COMPLETE -- ALL SIX CRITERIA DISCHARGED. Issuer ruling 2026-09-01T10:2xZ, 2.0.0_SA_COO. ⛔ THIS LINE IS A POINTER, NOT THE RULING: the authoritative record is the DATED STATE TABLE in the section "STATE OF THIS TO" at the end of this file, which supersedes every earlier REMAINING/status summary including the one this line replaces. BASIS, and it does NOT rest on a checker verdict (3.0.0_SA_CVO 91248: `VALID rc=0` is FORM-VALID, never SATISFIED): P2F-1 plan rows enumerated pre-apply; P2F-2 satisfied as authored, retro-tag REFUSED as a false-vintage citation; P2F-3a floor ENABLED since 2026-08-19T17:32:28Z cron(45 12 * * ? *); P2F-3b EXERCISED POSITIVE 2026-09-01 -- marker -> S3 event configurationId advi-49f-silver-complete-accelerator read from the DISPATCHER'S OWN CloudWatch record -> CHAIN OK date=2026-08-31 wall=116.1s, fact_acc 7,379 read / 7,379 converter-attested, completing 09:48:37Z against the 12:45Z floor, ~2h57m early against ~2h59m costed in 83402; P2F-4 both limbs 2026-08-29T18:2xZ; P2F-5 no session-local input; P2F-6 delivered @b2665bedc1 rows=6 violations=0 rc=0 first run, checker-vintage eefe9e0a91, GRADED PASS by 3.0.0_SA_CVO 91230 which verified declared_exclusions[0] BY CONTENT element by element rather than by the field's presence. ⛔ THE PRIOR STATUS BLOCK IS RETAINED BELOW AND WAS FALSE AT CLOSE: it read "P2F-3b ACCELERATOR = OPEN, not started -- list-rule-names-by-target returns [] and the function policy carries exactly ONE statement (scheduler principal), so no event source is PERMITTED to invoke it." TRUE WHEN WRITTEN 2026-08-29, FALSE SINCE the wiring landed and decisively so since the 09:46Z fire. It is kept rather than deleted because this face's defining failure all night was summary lines going stale beneath corrections, three generations deep, and a deleted falsehood teaches nobody.

⚠ DECLARED EXCLUSIONS CARRIED WITH THIS CLOSURE -- what it does NOT certify (3.0.0_SA_CVO 91230: an ABSENT item and an EXCLUDED-WITH-REASON item are the same shape to a careless reader and opposite to a careful one):
  (1) THE MARKER THAT TRIGGERED THE EXERCISE WAS LATER FOUND FALSE. schwab/08335338/meta/complete/date=2026-08-31.json was PUT ten times in 35s; the first five preceded the silver they attest to; the surviving object's own body says 16 of 17 declared tables were NOT written, including fact_acc; the ten payloads are DISJOINT so no union or selection over them recovers completeness. THIS DOES NOT WEAKEN P2F-3b -- the accelerator fires on ObjectCreated and 10 events in / 10 invocations out is correct behaviour for what it was given -- BUT THIS CLOSURE CERTIFIES THE ACCELERATOR AND NOTHING ABOUT THE MARKER'S TRUTH.
  (2) THE PRODUCER DEFECT IS OPEN AND OWNED ELSEWHERE: OPAL_ADVIPOINTERS.P2F-MARKER-DS at 0.4.0_DS_ClientPlatform~V. Root cause is a GRAIN MISMATCH in the SHARED core (date-grained key, invocation-x-lane payload and gate). M-2a and M-2b are WITHDRAWN as unsatisfiable; M-2c/M-2d/M-2e stand; the COMPLETENESS CONTRACT is at 1.0.0_SA_CTO. NOTHING about that defect is closed by this TO closing.
  (3) UPSTREAM AND UNOWNED: six of the seventeen DECLARED tables map to bronze feeds that are dead or never existed (fact_rlw has NEVER had a prefix; four dead 32-88 days). Surfaced to 1.0.0_SA_CTO for placement at 91318; NOT absorbed into D2 and not covered here.
  (4) THE UNTAGGED-ACCELERATOR TRACEABILITY GAP remains OPEN and UNOWNED, carried in the proof instance's declared_exclusions[0]. The permanent-owner convention is 1.0.0_SA_CTO's call. This closure does not resolve it and cannot absorb it.</status>
<priority>P1 — the canonical chain's only trigger today is a session act; NEVER#4: a production pipeline MUST have a schedule</priority>
<authority>Push plan @a2f27c8d0a §3 row 2 + CTO HOST RULING (verbatim in-row: the runner executes under the S3-code standard as its OWN scheduled stage — NOT appended to the legacy chain's stage list; revisable on your read only with new evidence). Ratified P2 spec: org/tier1_exec/4.0.0_SA_CRO/deliverables/P2_UNIFIED_MORNING_SCHEDULE_TIMING_MAP_SPEC_20260811.md (@9b5896793f: floors labeled PROPOSED-FROM-TF until the live both-namespace sweep confirms; schedule-existence paired with trigger-characterization). 49F verifies morning-ready (BD REST settles 05:02Z prior-day; Schwab silver lands ~12:18Z).</authority>
</task_order>
> **ROOT SUPERSEDED BY REFERENCE (COO, 2026-08-18 ~17:42Z): Andrew-direct ~1730Z moved the ADVI gold home to `opal-data-49financial/gold/advi/` (per-client bucket; ANDREW_DIRECT_20260818_CLIENT_GOLD_BUCKET_SUPERSESSION.md). Every `opal-data-assets/portal/gold/advi/49financial` root reference in this TO reads through OPAL_ADVIPOINTERS.GOLDHOME-REPOINT-49F (one act, before the P2 apply). Key names, criteria ids, dates unchanged.**


## Objective
Stand up the production trigger for the canonical 49F runner chain: an EventBridge SCHEDULE FLOOR
(fires daily after the ~12:18Z Schwab silver landing) plus the silver-completeness EVENT as an
ACCELERATOR — event-driven as accelerator only, never the sole trigger (NEVER#4). The invocation
target is DS~A's entrypoint per their P2D-4 contract (S3-code standard; own scheduled stage).

## Compiler tools (three-phase)
Phase 1: `comp-blast` on the mdpf-pipeline scheduled-floor TF precedent + `comp-iam gaps` after any
iam.tf change (necessary NOT sufficient — new resource ARNs verified on the live primitive,
`simulate-principal-policy` ONE --resource-arns per call, positive control as a SEPARATE invocation).
Phase 2: commit before apply (Deployment Rule 2). Phase 3: plan 0-diff after apply + tag
(`git tag -a` + push --follow-tags); `comp-freshness` row NOT added (moratorium — no monitors).

## Cross-domain coordination
- shared_resource: DS~A's entrypoint S3 code key — also_in_to OPAL_ADVIPOINTERS.P2-DISPATCH-49F. DS~A
  is last_write_owner on the script; you on the TF. Do not apply until P2D-4's written contract is in
  hand; MCP DS~A the schedule expression before apply.
- shared_resource: `opal-data-assets/portal/gold/advi/49financial/**` — written by the scheduled
  chain; read by DS~B (P4-EMIT) + CVO (pins). No writes from TF itself.

## Acceptance criteria
- P2F-1 PLAN EXPECTED-ROWS-BOUNDED: the TF plan's expected rows enumerated IN WRITING before apply
  (draft to COO+CTO for the pre-apply read — your 152834Z posture, kept); apply via `safe-apply` only;
  CTO per-apply gate honored.
- P2F-2 0-DIFF + TAG: post-apply plan 0-diff; tag pushed --follow-tags.
- P2F-3 FLOOR + ACCELERATOR: the schedule floor exists with a concrete ScheduleExpression (never
  event-only — print the expression); the silver-completeness event is wired as accelerator; both
  target DS~A's entrypoint under the S3-code standard as its OWN stage (host ruling; any contrary
  finding goes to CTO as new evidence, not silently implemented).
- P2F-4 THREE UNATTENDED WRITES: 08-20, 08-21, 08-22 each produce
  `portal/gold/advi/49financial/*/date={T-1}` written by the SCHEDULED run (TO-2 precedent bar) —
  evidence per day: the run's own log + S3 listing with LastModified in the scheduled window; T-1 per
  the trading calendar, never wall-clock.
- P2F-5 NO SESSION-LOCAL INPUT: the fired path resolves everything from S3 (attested from the run log
  of cycle 1; an expected log's ABSENCE is a finding, not a pass).
- P2F-6 proof instance VALID rc=0 positional: ids P2F-1,P2F-2,P2F-3,P2F-4,P2F-5,P2F-6.

<proof_of_spec>
  <expected_criteria>P2F-1,P2F-2,P2F-3,P2F-4,P2F-5,P2F-6</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/OPAL_ADVIPOINTERS.P2-FLOOR-49F_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- No bare `terraform apply` (safe-apply), no bare commits (safe-commit), no
  `aws lambda update-function-code` (Terraform only).
- No alarms / SNS / SES / freshness checkers / monitors (moratorium, Andrew 07-28 standing).
- No applies before the 23:01Z fixture verdict; if PHASE_B1 fails tonight, the fixture outcome routes
  first — do not interleave.

## Reporting
COO (cc CTO, DS~A, MSTR) at plan-drafted, at applied, and after each unattended cycle (one line each).
Surprise channel: one banked line to COO. Session log with Compiler Tools section = deliverable.


## EXECUTING LANES ON THIS TO'S CELLS -- issuer record, 2026-08-29T18:0xZ (2.0.0_SA_COO)

⛔ **WRITTEN BECAUSE THE ALLOCATIONS BELOW WERE MADE BY MESSAGE AND APPEAR ON NO FACE ANYWHERE.**
`to-check --all --assignee 0.4.0_DS_ClientPlatform~V` returned ZERO rows while that lane was doing this
work -- **not misattributed, ABSENT.** A face-reading census cannot see a cell allocated to a lane other
than the TO's owner, because there is nowhere for it to be recorded. Surfaced by `1.0.0_SA_CTO` 83447 as
a property of its own instrument; this is the instance.

| cell | executing lane | allocated | state |
|---|---|---|---|
| **P2F-4 wall-clock date read** on `advi-49f-gold-dispatch` | `0.4.0_DS_ClientPlatform~V` | COO 83394 | READ-ONLY, first. **CONFIRM-OR-REFUTE, not confirm.** Do NOT fix if found. |
| **composite `_SILVER_COMPLETE.json` emit** (P2F-3b route (a)) | `0.4.0_DS_ClientPlatform~V` | COO 83406 | BUILD, sequenced AFTER the read. Marker carries a **DECLARED** table list, never one derived from a listing. |

**TO OWNER REMAINS `0.7.0_AE_CloudOps`** -- these are cells executed by a DS lane, not a re-address of the TO.
**Rule 27 holds: both cells are `OPAL_ADVIPOINTERS`, so `~V` remains a one-project instance.**
⛔ **P2F-3b's TF rows stay with `0.7.0_AE_CloudOps` and are NOT started until the marker emit lands.**


## P2F-4 ISSUER RULING 2026-08-29T18:0xZ (2.0.0_SA_COO), on 0.4.0_DS_ClientPlatform~V's read 83466

✅ **WALL-CLOCK LIMB -- SATISFIED. THE HYPOTHESIS IS REFUTED.** `advi-49f-gold-dispatch` resolves NO date
at all (0 occurrences of `date|today|utcnow|now(|trading`, case-insensitive, POSITIVE-CONTROLLED: `def`=6,
`import`=5 in the same file). Full path: scheduler -> dispatch (passes only `StartedByDispatcher`) -> SSM doc
(*empty = production path, T-1 from the trading calendar*) -> `chain_49f_entrypoint.py --production` calling
`_tc.prev_trading_day(...)`. **Verified at the SERVED ARTIFACT, not the repo:**
`s3://opal-data-49financial/_code/chain_49f_entrypoint.py`, 33,416 B, byte-identical to HEAD; **AST on the
SERVED bytes** shows `prev_trading_day` at `:433`/`:441` and `expected_last_trading_day` called **ZERO** times.
(`comp-pipescript deployed` does NOT cover this script -- 0 hits for `chain_49f` -- so the object was read
directly rather than a tool's silence being reported as coverage.)

⛔ **THE 08-20 ABORT IS EXPLAINED, NOT EXCUSED: it ran PRE-FIX code, 193 minutes before `b5b0f26238`.**
Settled with `%ct` EPOCH seconds because `git log --date=format-local` printed `11:58:20Z` -- local time
wearing a literal `Z`, the documented trap -- and 193-after versus 193-before flips the conclusion.

⭐ **AND THE FINDING WORTH MORE THAN THE REFUTATION: the pre-fix expression was `expected_last_trading_day`
= T-0 on any trading day. A CALENDAR FUNCTION USED AT THE WRONG FRONTIER IS A DIFFERENT DEFECT FROM IGNORING
THE CALENDAR, AND IT HAS A DIFFERENT REMEDY.** It COINCIDES with wall-clock on a trading day -- which is why
three log lines could not separate them -- and DIVERGES on a non-trading day.
**BD is SHARED SHAPE, NOT SHARED CAUSE:** `gold_dispatch.sh:312` is `$(date -u +%Y-%m-%d)` with no calendar in
the expression at all. **BD ignores the calendar; ADVI mis-selected within it.** BD's remedy is to introduce
a calendar; ADVI's already happened.

⛔ **THREE-WRITES LIMB: NOT DISCHARGED BY THIS RULING.** P2F-4 asks for 08-20/21/22 each producing a write;
08-20 aborted, and *explained* is not *produced a write*. **The named dates were a proxy for THREE CONSECUTIVE
UNATTENDED SCHEDULED WRITES and that intent survives the proxy** -- so the limb re-assesses on three consecutive
POST-FIX scheduled dates (08-21 and 08-22 are two). **One short listing closes it; it is NOT closed here.**

⚠ **RESIDUALS, as that seat stated them and accepted as the answer's edges rather than gaps:** no live
scheduled fire was observed (evidence is served-artifact byte-identity, not an execution), and the SSM
document's TERRAFORM was read rather than the live document.

⛔ **ISSUER'S OWN CORRECTION: my allocation (83394) closed with *"a refusal is the friendly version of this
bug and we should not rely on getting it again"* -- an UNCONDITIONAL assertion of a live latent defect on top
of a hedged premise. REFUTED: it was pre-fix code failing loudly on the day it was fixed. There is no
friendly-version-of-a-lurking-bug here.**


## ✅ P2F-4 DISCHARGED -- ISSUER RULING 2026-08-29T18:2xZ (2.0.0_SA_COO), on 0.7.0_AE_CloudOps 83526

**BOTH LIMBS SATISFIED. No open limb remains on P2F-4.**

**LIMB 1 -- "never wall-clock": SATISFIED** on `0.4.0_DS_ClientPlatform~V` 83466 (source plane): the dispatch
resolves NO date at all (0 tokens, positive-controlled), the path runs to `_tc.prev_trading_day`, and the AST
on the SERVED bytes shows `expected_last_trading_day` called ZERO times.

**LIMB 2 -- "three unattended writes": SATISFIED WITH MARGIN -- SEVEN, not three** (83526, behaviour plane):
```
  08-21->08-20  08-22->08-21  08-25->08-24  08-26->08-25  08-27->08-26  08-28->08-27  08-29->08-28
  7 of 7 match prev_trading_day(run_date) EXACTLY; every write lands 68-109 s after the 12:45:42Z fire,
  inside the scheduled window; log form chain_YYYYMMDDTHHMMSSZ.log EXCLUDES adhoc/backfill by construction.
```
⭐ **AND THE CORROBORATION IS ON A DIFFERENT PLANE, NOT THE SAME ONE TWICE: `~V` read `prev_trading_day` in the
SERVED BYTES; this is seven days of OUTPUT agreeing with it. Source AND behaviour.** (Rule 22 DISCRIMINATION:
re-derived with a different instrument, not a re-run of the first.)

⛔ **THE TWO EMPTY DAYS ARE CORRECT SKIPS AND WOULD HAVE READ AS FAILURES.** 08-23 and 08-24 each produced a
3,627 B log and NO manifests -- **`prev_trading_day` for BOTH is 2026-08-21, already built by the 08-22 run.**
**A "three consecutive writes" test run naively across the calendar would score them as MISSES and report 5 of 7.
They are the freshness gate working: nothing new to build, so nothing built.** Identical log sizes to the byte
on both days is the tell.

⚠ **RESIDUALS CARRIED, NOT BLOCKING THE DISCHARGE, and stated by the measuring seat rather than found later:**
(1) the 08-29 run wrote **2** manifests where others wrote 4-6 -- **a write either way, but NOT established as a
COMPLETE one**; whether that is fewer changed dimensions or an incomplete run is unmeasured. **Worth one look on
the next run rather than a finding today.** (2) off-schedule writes on `date=2026-08-19`/`08-18` are the
already-excluded adhoc/backfill runs, named so nobody re-finds them as anomalies. (3) manifests under
`dimensions/_manifests/` were measured; not every downstream artifact per run.

⛔⛔ **THE LINE BELOW IS INCOMPLETE. CORRECTED 2026-09-01T09:3xZ by the issuer 2.0.0_SA_COO on 0.7.0_AE_CloudOps~M 91211: `P2F-6` (the proof-of-spec instance) IS ALSO OPEN, NEVER STARTED, AND AE's.** Declared path `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/OPAL_ADVIPOINTERS.P2-FLOOR-49F_PROOF_OF_SPEC.json` -- ABSENT. **MEASURED THREE WAYS before assertion:** (a) declared path absent; (b) filename census `comp-find "P2-FLOOR" --name` = 12 hits / 145,393 files, none a proof instance; (c) **`comp-read` on the FULL FACE** asking directly whether P2F-6 is discharged anywhere below its status block -- 17 sections, no discharge. ⛔ **SO "REMAINING: P2F-3b ONLY" IS A SUMMARY LINE THAT WAS ITSELF STALE, AND THREE SEATS QUOTED IT -- `0.7.0_AE_CloudOps~M`, `0.4.0_DS_ClientPlatform~V`, AND THE ISSUER. It is the SAME defect as reading `<status>` and not the body, one section further down: a correction that becomes a summary becomes stale in its turn.** REMAINING ON THIS TO IS THEREFORE: **P2F-3b AND P2F-6.**

## STATE OF THIS TO -- 2026-09-01T09:4xZ, `2.0.0_SA_COO` (issuer). THIS SECTION SUPERSEDES EVERY EARLIER "REMAINING" LINE ON THIS FACE, INCLUDING MY OWN 09:3xZ CORRECTION ABOVE.

```
  P2F-1  DISCHARGED     P2F-2  DISCHARGED (satisfied as authored; retro-tag REFUSED, reasoning below)
  P2F-3a DISCHARGED     P2F-4  DISCHARGED (both limbs, 2026-08-29T18:2xZ)
  P2F-5  DISCHARGED     P2F-6  DISCHARGED 2026-09-01 -- delivered @b2665bedc1 by 0.7.0_AE_CloudOps~M,
                               rows=6 violations=0 VALID rc=0 on the FIRST run, checker-vintage
                               eefe9e0a91, artifact-resolution 5 of 5 at pin. GRADED PASS by
                               3.0.0_SA_CVO 91230, which verified the instance BY CONTENT (opening
                               declared_exclusions[0]) rather than by the field's presence.

  P2F-3b OPEN -- THE ONLY UNRESOLVED CRITERION ON THIS TO.
```

⛔ **WHY THIS SECTION EXISTS AND WHY IT IS A SECTION RATHER THAN A THIRD SUMMARY LINE.** This face has
now produced the SAME defect three times in one night at three different depths: the `<status>` block
read instead of the body; then the closing "REMAINING: P2F-3b ONLY" line, which was itself stale and
which THREE seats quoted (`0.7.0_AE_CloudOps~M`, `0.4.0_DS_ClientPlatform~V`, and the issuer); then my
own 09:3xZ correction of that line, which was true for forty minutes and was falsified by P2F-6 landing.
**A correction that becomes a summary becomes stale in its turn, and each generation is quoted with more
confidence than the last because it is more recent.** The remedy is not a fourth summary line -- it is a
DATED state table that names what it supersedes, so a reader who lands anywhere in this file's tail is
told which statement is live rather than having to date them.

⛔ **P2F-3b's GATE IS NOT A CLOCK -- MEASURED 2026-09-01T09:3xZ BY THE ISSUER, ON THE SERVED PLANE.**
The line this section replaces said P2F-3b was "sequenced behind `0.4.0_DS_ClientPlatform~V`'s producer
emit (COO 83406)", and both holding seats read as waiting for a scheduled fire. The composite marker
`P2F-MARKER-DS` declares:

```
  SUBJECT   s3://opal-data-assets/schwab/08335338/meta/complete/    -> EMPTY (literal None)
  DELIMITER children of schwab/08335338/meta/  -> conversions/ , pulls/   DENOMINATOR 2
                                                 complete/ HAS NEVER EXISTED as a prefix
  CONTROL   meta/conversions/ -> 5 objects, SAME instrument, adjacent prefix
                                                 so the None is an ABSENCE, not a dead call
  FIRES     conversions/20260830T121549Z  landed 2026-08-30T12:17:50Z
            conversions/20260831T121550Z  landed 2026-08-31T12:18:29Z
```

~~>> **THE SCHEDULED RUN THE POST-CLOSE CHECK WAITS FOR HAS ALREADY FIRED TWICE AND WROTE NO MARKER
   EITHER TIME.** A third fire at ~12:18Z today predicts a third identical result. Waiting is
   therefore a SELF-INFLICTED WAIT against an event already observed not to produce the thing. <<~~

⛔ **THE STRUCK CLAUSE ABOVE IS WITHDRAWN BY ITS AUTHOR, 2026-09-01T09:4xZ, on `0.7.0_AE_CloudOps~M`
91235 -- FOUR MINUTES AFTER I WROTE IT. THE MEASUREMENT ABOVE IT STANDS; THE SENTENCE I STAPLED TO IT
DOES NOT.** 08-30 and 08-31 were **not duty cycles**:

```
  BUILD days  08-22,25,26,27,28,29   n=12-13 manifests, FIRST pass 09:46Z
  SKIP  days  08-23,24,30,31         n=1     manifest,  only ~12:18Z
  silver objects written   08-25..08-29: 15/day     08-30: 0     08-31: 0
```

**The converter converted NOTHING on either day.** A per-date completeness marker for a date that was
never built **must not be written -- writing one would be a false completeness claim.** So those runs
had nothing to score; they were neither failures nor duty cycles. ⚠ **And the `~12:18Z` I quoted is the
SKIP-DAY pass, not the build pass** -- I read a run time off two skip days and called it the schedule.

**The producer landed 2026-08-29T21:25Z, AFTER that day's build pass. 08-30 and 08-31 both resolved
`prev_trading_day = 08-28`, already built. 09-01 resolves to 08-31 -- a NEW date. So today's 09:46Z
pass is the FIRST duty cycle this marker has ever had.**

⭐ **KEPT ON THE FACE RATHER THAN EDITED OUT, because it is the same shape three times tonight and this
is the cheapest place to see it: AN INTERPRETATION STAPLED TO A CORRECT MEASUREMENT INHERITS THE
MEASUREMENT'S CREDIBILITY.** Nothing in *"complete/ has never existed"* required *"and therefore two
runs failed"* -- I supplied that, and it travelled INSIDE a true reading to three seats and into a
committed face. **A face showing a withdrawn inference beside the measurement that survived it is worth
more than one that only ever shows conclusions that held.**

⭐ **AND THE THREE-WAY OUTCOME SET THAT ACTUALLY SETTLES IT** (adopted from `0.7.0_AE_CloudOps~M`
91235 s.5, which killed its own armed binary wait rather than let it emit a FINDING at a time when no
build was due -- **a timeout that cannot tell "no marker" from "nothing to mark" manufactures exactly
this error, on a timer**):

```
  MARKER-FIRED          marker appears                        -> P2F-3b exercised
  BUILT-BUT-NO-MARKER   silver for date=2026-08-31 written,   -> a REAL finding; settles (a)-vs-(b)
                        complete/ still absent                   on the SERVED plane, without
                                                                 touching the producer
  NO-DUTY-CYCLE-YET     no silver written                     -> absent marker stays UNINFORMATIVE
```

⚠ **AND THE BOUND ON THAT, HELD RATHER THAN COLLAPSED:** the measurement is of the SERVED plane. It does
NOT establish whether the M-2 emit is APPLIED in the producer that fired. Two readings survive it and
they want opposite remedies -- **(a)** M-2 is DESIRED-not-APPLIED (the face's own provenance carries the
tell verbatim: `0.7.0_AE_CloudOps` 85110, *"OPAL_BUILD_COMMIT = 5c7b2a9a6b, DESIRED at the time"*), or
**(b)** M-2 is applied and the emit did not fire or wrote a different key. **Neither is decided by
waiting; both are decided by one read of the deployed producer.** Routed to `0.4.0_DS_ClientPlatform~V`
(producer lane, Rule 13) at 91232, `0.7.0_AE_CloudOps~M` at 91233, `1.0.0_SA_CTO` (85120 gate word) at
91234. ⛔ **No ad-hoc run is authorized and COO 83898 stands: a hand-written marker is NOT closing
evidence and the SCHEDULED fire remains the acceptance.** Reading why two fires wrote nothing is not
manufacturing the marker.

⚠ **ISSUER'S OWN ERROR, DISCLOSED ON THE FACE RATHER THAN IN THE THREAD.** I opened this edit intending
to record P2F-3b's dependency as DISCHARGED -- both seat summaries read that way, and `P2F-MARKER-DS`
describes M-2 in the past tense throughout. **I measured before editing and the measurement said the
opposite.** Two summaries agreeing is not corroboration when one describes what the other performed, and
a face written in the past tense is a DESCRIPTION, never a STATE.
