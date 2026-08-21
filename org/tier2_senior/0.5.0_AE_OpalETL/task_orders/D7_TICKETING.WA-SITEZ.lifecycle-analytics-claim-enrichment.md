# TO D7_TICKETING.WA-SITEZ — Ticket Lifecycle v2 W-A: native analytics fields + claim enrichment (smallest first; unblocks C3/O6)

<task_order id="D7_TICKETING.WA-SITEZ" project="OPAL_TICKET">
<issued_to>0.5.0_AE_OpalETL~Z (build; site-Z). Laptop apply leg = EXECUTION PLACEMENT via 0.0.0_AB_MSTR~Z ferry (envelope law @550b20ec5b: applies stay under laptop apply-time mechanics).</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-20T20:0xZ</issued>
<status>⛔ **APPLY PLACEMENT SUPERSEDED 2026-08-21T1340Z by 2.0.0_SA_COO~Z (issuing seat): CLAUDE.md RULE 26 @95b7eeb458 (Andrew-direct ~0848Z) ROUTES THIS APPLY TO SITE Z, NOT THE LAPTOP.** This TO predates Rule 26 and its laptop-ferry routing below is a RECORD OF WHAT WAS DISPATCHED, not a current instruction -- left in place deliberately rather than rewritten, so the dispatch history stays readable. **Law outranks a TO's routing clause prospectively; nothing about the build or its acceptance changes.** **BUILD COMPLETE + VALIDATED. OUTSTANDING: THE APPLY LEG ONLY (now site-Z, per Rule 26).** — corrected 23:22Z by 2.0.0_SA_COO~Z; the previous text was STALE BY TWO STATE TRANSITIONS and is preserved below.
 ✅ dep-3 CLOSED ~20:12Z — `dep-3 ACCEPTED: TAC-3 SCHEDULE-LANDED` @399df8444a (real fire seat-down, LastTaskResult=0, distinct exits 2/3/4, framed zero). The queue position this field described NO LONGER EXISTS. Line ~220's precondition ("do not begin before the dep-3 registration sitting completes") is DISCHARGED.
 ✅ BUILD EXECUTED + PROOF-VALIDATED at 0.5.0_AE_OpalETL~Z — @81c502cff2 (feat), @9121a55330 (WA-10 distinct tokens), @7e98926a41 (WA-1..WA-10 instance, `VALID rc=0` positional, discriminated), @133b0f24b0 (comp-blast half discharged). COO-validated: `org/tier1_exec/2.0.0_SA_COO/deliverables/laneZ_VALIDATION_20260820_WA_build_leg.md`.
 ⛔ OUTSTANDING, AND IT IS THE ONLY THING OUTSTANDING: **THE APPLY LEG** — laptop-side execution placement via the 0.0.0_AB_MSTR~Z ferry, **WA-6 GRANT FIRST**, then the deployed WA-1/WA-2/WA-8 exercises. Genuinely external to site-Z; carried on the cross-fabric board.
 ⚠ SUPERSEDED TEXT, kept because the retraction is the record: ~~"pending — GO rides this commit's MCP. QUEUE POSITION: behind the dep-3 registration sitting at this seat (1.0.0_SA_CTO~Z @942d4d885c: 'the current dep-2/dep-3 chain is UNCHANGED and remains the critical path'). W-A is first of the four W lanes (CTO sequencing: smallest first)."~~ — the CTO sequencing quote remains TRUE OF ITS MOMENT and was satisfied, not violated.</status>

<!--
⛔ WHY THIS FIELD WAS WRONG FOR ~3 HOURS, AND WHAT IT COST — recorded because I caused the cost.
⛔ MY FIRST VERSION OF THIS NOTE GAVE ITS TIMESTAMPS IN LOCAL TIME AND READ THEM AS UTC.
Corrected by measurement, every value re-derived at the same offset:
  dep-3 feat commit @399df8444a         2026-08-20T15:59:41-04:00  =  19:59:41Z
  THIS <status> LINE authored @9eeb173dc5      16:04:32-04:00       =  20:04:32Z
  file last touched @93ac7ddb68                17:53:17-04:00       =  21:53:17Z  (NOT 17:53Z)
SO THE CORRECTED STORY IS NARROWER AND MORE HONEST: the field was NOT written before dep-3 closed
and left to rot. IT WAS WRITTEN FIVE MINUTES AFTER THE dep-3 FEAT COMMIT, ~6 min before its
accept/validate -- ACCURATE WHEN WRITTEN, STALE WITHIN SIX MINUTES.
WHAT IS UNCHANGED IS THE PART THAT COST SOMETHING: THE FILE WAS EDITED THREE MORE TIMES
(21:45:50Z, 21:48:11Z, 21:53:17Z) AND THE STATUS LINE WAS NEVER REVISITED -- while the evidence
sat in my own tick-20 drive log: "dep-3 EXECUTED->ACCEPTED->VALIDATED; TAC-3 = SCHEDULE LANDED."
⛔ AND THE TIMEZONE SLIP IS THE LAW I ALREADY CARRY: --date=format:'%H:%M' RENDERS LOCAL TIME
WITH NO MARKER, exactly like `aws s3 ls`. A TIMESTAMP WITHOUT ITS RENDERING PLANE IS A NUMBER
WITHOUT ITS DENOMINATOR -- committed by me, inside the correction of a staleness error, against a
rule I quoted at another seat four hours earlier. Pin the plane (--date=iso-strict) for any
cross-source time compare.

THE MEASURED COST, 30 MINUTES BEFORE THIS FIX: I read this field, believed it, and BROADCAST TO
THREE SEATS that W-C was "TWO LINKS BACK: dep-3 -> W-A -> W-C(b)". BOTH LINKS WERE ALREADY WRONG.
dep-3 was closed and W-A's build was done. W-C(b)'s real constraint is THE W-A APPLY — ONE LINK,
laptop-side. I corrected a wrong constraint by citing a stale field and produced a differently
wrong constraint, with more confidence, in a message that told other seats to update their boards.

THE CLASS, and it is the one this fabric named all evening: A STATUS FIELD THAT WAS TRUE WHEN
WRITTEN, DESCRIBING A CONDITION THAT HAS SINCE CLEARED, WITH NOTHING MARKING IT SUPERSEDED. Same
shape as the 07-31 gateway deploy record I caught someone else citing four hours ago. THE
DIFFERENCE IS THAT THIS ONE WAS MY OWN ARTIFACT AND I READ IT AS EVIDENCE ABOUT MY OWN LANE.
A CLOSED DEPENDENCY DOES NOT GO BACK AND EDIT THE FIELDS THAT NAMED IT.
-->
<priority>P2 (P1 = dep-3 schedule-landed)</priority>
<authority>ANDREW-DIRECT 2026-08-20 ~19:4xZ, TICKET LIFECYCLE v2 flow, record @942d4d885c (org/tier1_exec/1.0.0_SA_CTO/deliverables/ctoZ_ANDREW_DIRECT_20260820_TICKET_LIFECYCLE_V2_FLOW.md) — his O6 verbatim: "we need to have analytics built in to the DDB... easier to manage if its baked into the DDB and process natively." 1.0.0_SA_CTO~Z ruling 3 (ANALYTICS NATIVE) + C3 (claimer identity visible). Rigor frame: ATOM_DECOMP discipline @9b93c39eeb. 1.0.0_SA_CTO~Z RULES + 2.0.0_SA_COO~Z DECOMPOSES (@550b20ec5b). Design-of-record = the 1.0.0_SA_CTO~Z deliverable above; PRD §-anchor is 1.0.0_SA_CTO~Z's leg (TOs re-point when it lands).</authority>
</task_order>

## Objective
The `opal-ticket-api` Lambda's transition writes gain NATIVE analytics + claim enrichment, computed
IN the Lambda at the transition write (process-native, no external analytics job), appended to
`events[]` as today:

- at CLAIM: `claimed_at`, `time_to_claim_s`, `claimed_by = {name, email, user_id}` — resolved
  SERVER-SIDE at claim time from the claimer's `opal-users-v2` directory row (display-grade
  snapshot ON the ticket row; a snapshot, not a live join).
- at COMPLETE: `completed_at`, `time_to_resolve_s`, `completed_by = {name, email, user_id}`.
- `created_at` exists; one grain = one ticket's lifecycle.

**AMENDED ~20:09Z — ANDREW-DIRECT DAY-ONE FIELD SET (his no-retrofit word, "don't want to have to
be retroactively adding stuff", routed via 1.0.0_SA_CTO~Z 2777):** the cut ALSO carries, at day one:
- `schema_version: 2` (cheapest future-proofing);
- `priority` enum RESERVED (a reserved value is a schema act — it rides the Rule-24 record);
- `category` / `tags[]` free-form at claim/close;
- `reopened_count` + `reopened_at[]`;
- `first_response_at`;
- **`client_updates[]` APPEND-ONLY `{ts, author, text}` with the ORIGINAL DESCRIPTION as entry
  zero** — his rich-text store of client requests, IN the row (no second store, no join). DDB
  400KB item cap NOTED with the S3-spill key DESIGNED-NOT-BUILT (named in the schema record;
  never built in this TO).
`ticket_type`/`status`/`source`/`requester`/`events[]` are deployed and stay.

The Rule-24 schema record RIDES this change and covers the FULL field set above (grain declared,
axis intents stated, four-postulate note incl. the reserved priority enum; the outcome-array/enum
surfaces re-tested per the 08-20 Rule-24 widening).

## Acceptance criteria (D7F pattern: stable ids, mutants, both directions, positional proof)
- **WA-1** CLAIM transition, exercised on a real row: `claimed_at` + `time_to_claim_s` +
  `claimed_by{name,email,user_id}` land on the row, identity resolved server-side from
  opal-users-v2 (never from the request body).
- **WA-2** COMPLETE transition, exercised: `completed_at` + `time_to_resolve_s` + `completed_by`
  land; `time_to_resolve_s` measures create→complete on the row's own timestamps.
- **WA-3** MUTANT (D7F-4 class, both directions): a request body carrying forged
  `claimed_by`/analytics fields is ignored-or-refused (server-derived only) — the mutant
  DISCRIMINATES (forged in → not on row; legit claim → correct identity on row).
- **WA-4** REGRESSION: existing consumers unbroken — board/list/get render rows WITHOUT the new
  fields (pre-W-A rows) and WITH them; `events[]` append shape preserved; existing battery
  (authz 12/12, D7F rows) re-run green.
- **WA-5** Rule-24 schema record committed WITH the change (field set, grain, axis intent;
  opal-users-v2 snapshot semantics stated: display-grade copy, not a live join).
- **WA-6** IAM per Rule 22a: the Lambda role's read of `opal-users-v2` verified on the LIVE
  primitive — `aws iam simulate-principal-policy` with ONE `--resource-arns` (the exact table ARN)
  + a SEPARATE positive control; comp-iam treated as floor. Laptop apply: ledger opened/closed +
  tag; 0-diff.
- **WA-7** Proof instance VALID rc=0 POSITIONAL (`python .tools/proof-of-spec-check.py <instance>
  WA-1,WA-2,WA-3,WA-4,WA-5,WA-6,WA-7,WA-8,WA-9,WA-10`) — rc taken unpiped.
- **WA-9** THE 3.0.0_SA_CVO~Z PRE-CUT ITEMS DISCHARGED, each with its own evidence: (a) the requester-keyed
  GSI decision RECORDED (index added + verified, or the explicit no-index decision that obligates
  W-C's printed bound); (b) `client_updates[]` per-entry AND per-ticket caps exercised (an
  over-cap append is refused, both directions) — with the S3 spill verifiably NOT built; (c) the
  `_sod_block` carve-out for the client-update append decided and exercised (the requester CAN
  append to their own ticket, and CANNOT do anything else to it — the carve-out is scoped, proven
  by the second half); (d) the reopen/timing GRAIN resolved per 1.0.0_SA_CTO~Z's ruling BEFORE the Rule-24
  record is written, and the record states which shape landed.
- **WA-10** ⛔ **THE DEGRADATION PRINT DISCRIMINATES** — it separates *"the lookup RAN and the
  directory has no such row"* (a fact about the world, no follow-up) from *"the lookup DID NOT
  COMPLETE"* (a defect), and the second **names which way it failed**. Exercised in BOTH directions.
  **Necessary because the degraded state is SEMANTICALLY VALID:** a blank claimer name is the
  *correct* rendering for a genuinely-absent user, so a collapsed print leaves the defect reading as
  normal. ⛔ **NOT dischargeable by pointing at the apply sequencing** — that remedy is
  acceptance-scoped and one-shot; this one is a property of the system. Dischargeable by pointing at
  code that already separates the two cases. **Full statement + the asymmetry table: see the WA-10
  section below.**
- **WA-8** DAY-ONE SET exercised (the ~20:09Z amendment): a create carries `schema_version:2` +
  `client_updates[0]` == the original description; a claim/close append lands a further
  `client_updates[]` entry APPEND-ONLY (a mutant overwrite/delete of an existing entry is
  refused/ignored — append-only discriminates); `first_response_at` set on the first responding
  transition; `reopened_count`/`reopened_at[]` behave on a reopen (or the reopen path's absence
  is stated honestly if no reopen transition exists yet — no phantom claim); the S3-spill key is
  NAMED in the schema record and verifiably NOT built.

<proof_of_spec>
  <expected_criteria>WA-1,WA-2,WA-3,WA-4,WA-5,WA-6,WA-7,WA-8,WA-9,WA-10</expected_criteria>
  <instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/D7_TICKETING.WA_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## 3.0.0_SA_CVO~Z PRE-CUT FINDINGS FOLDED (2817 @3c29c35122, ~20:33Z) — three land HERE because W-A is the table touch

**(a) DECIDE THE REQUESTER-KEYED GSI AT THIS TO, NOT AT W-C (P1-1).** The table today has only
`status-index` (hash `status`, range `created_at`, projection ALL) — **no requester-keyed index
exists.** W-C's client "My Requests" view would therefore ride a `Limit`-bounded scan plus
in-memory filter: the estate's own truncated-page class, except turned into a **CLIENT-FACING
COMPLETENESS CLAIM** — a client who filed 12 can be shown 8 with nothing saying so. **W-A is the
table touch, so the index decision belongs here.** Either add the index (with its own IAM/22a
verification) or record the explicit decision not to, in which case W-C's WC-2c must print its
bound. Do not leave this to be discovered at the view build.

**(b) CAP `client_updates[]` AT AUTHORING TIME — the build-ladder answer to the 400KB cap
(unknown-unknown 1).** `client_updates[]` is an append-only array authored by the **LEAST-TRUSTED
principal** — the one field on the row whose growth Opal does not control — against the DDB 400KB
item cap whose S3 spill is deliberately *designed-not-built*. The row **already** caps
`description` at 8000 and `resolution` at 2000, so **a per-entry cap and a per-ticket cap make the
spill unnecessary** rather than deferred. Cap it here; do not build spill infrastructure (rung 1:
does this need to exist at all?).

**(c) THE `_sod_block` CARVE-OUT IS A DESIGN-TIME DECISION, NOT A TEST-TIME DISCOVERY
(unknown-unknown 2).** `_sod_block` forbids the requester from acting on their own ticket — and the
requester is **exactly who authors a client update.** Resolve the carve-out explicitly (scoped to
the client_updates append, nothing wider) or the append path meets a denial at test time.

⚠ **(d) ROUTED TO 1.0.0_SA_CTO~Z, NOT RULED HERE — the reopen GRAIN collision (P1-2).**
`reopened_count`/`reopened_at[]` are in the cut by **Andrew's own day-one word**, and I am not
dropping a sovereign field on a review finding. But 3.0.0_SA_CVO~Z's mechanism is sound and must be resolved
*before* the schema lands: there is **no writer** for them today (zero `reopen` occurrences, no
MATRIX action, no handler), and — the load-bearing half — **they collide in grain with the
single-valued timing fields the transition handlers set unconditionally.** After a
reopen/reclaim/recomplete, `time_to_resolve_s` silently means **LAST CYCLE** while `reopened_count`
says N: Rule 24(ii) same-grain, and the naming-vs-semantic class. `events[]` already records every
transition, **so per-cycle timings are derivable** — the build-ladder answer. Also note a REOPEN
action is itself a matrix widening whose natural actor is the requester, whom `_sod_block` forbids.
**The schema must land coherent: either the timing fields are explicitly last-cycle by definition,
or per-cycle timings derive from `events[]`. 1.0.0_SA_CTO~Z rules the shape; this TO carries the requirement
that it is resolved before the Rule-24 record is written, never after.**

## ⛔ WA-10 (NEW, 21:4xZ) — THE DEGRADATION PRINT MUST **DISCRIMINATE**, AND IT IS THE SAME DEFECT AS THE APPLY SEQUENCING

*(`3.0.0_SA_CVO~Z` @3170, conditioning the soft-fail resolution before it is built — folded because
the apply leg is still ahead of us.)*

**The degraded state here is SEMANTICALLY VALID, which is one degree worse than invisible.** A ticket
showing **no claimer name** is the **CORRECT** rendering for a claimer who genuinely has no
`opal-users-v2` record. So the failure does not merely lack an error — **it produces an outcome that
a reader, a client, and a future auditor would each read as normal and correct.**

**Therefore "every degradation prints its reason" is NECESSARY AND NOT YET SUFFICIENT.** If the print
collapses to one message (*"no name available"*), then **ABSENT-FROM-DIRECTORY** (legitimate,
expected, permanent) and **LOOKUP-FAILED** (IAM deny, wrong key shape, transport error) emit the
**same line**, and the record still cannot separate them. *That is Rule 22a's shape stated plainly:
**true to the letter and false to the purpose**, because a control that fires identically on the
healthy and the broken case discriminates nothing.*

**WA-10, as a PROPERTY (the mechanism is the builder's):** the print separates **at least** *"the
lookup RAN and the directory has no such row"* from *"the lookup DID NOT COMPLETE"* — **and the
second names which way it failed.** The first is a fact about the world needing no follow-up; the
second is a defect that does. Exercised in both directions.

>> ⛔ **AND IT COMPOSES WITH THE APPLY-LEG SEQUENCING — THEY ARE ONE DEFECT SEEN FROM TWO ENDS.**
The mis-sequenced exercise (running the deployed enrichment test **before** WA-6's grant is applied)
reads **"works, no names"** — which is **exactly** the indistinguishable state above. So:
**if the print DISCRIMINATES, a mis-sequenced exercise ANNOUNCES ITSELF instead of passing green; if
it does not, the exercise PASSES and the grant's absence is invisible in the one test written to
catch it.** Fixing neither means **the acceptance evidence is UNFALSIFIABLE** — a green run that
cannot distinguish a working enrichment from an ungranted one. *A test that cannot fail is not weak
evidence; it is not evidence.*

⛔ **CORRECTED 21:4xZ — "FIX EITHER AND BOTH CLOSE" IS *NOT* SYMMETRIC, AND THE ASYMMETRY DECIDES
WHICH ONE GETS BUILT** (`3.0.0_SA_CVO~Z` @3186, correcting my own sentence). **That sentence is true
only of the ACCEPTANCE EVIDENCE, which is the frame I stated it in — and read one sentence out of
that frame it becomes "these are interchangeable", whose natural next move is to take the cheaper
one. The cheaper one is RE-ORDERING TWO STEPS. It costs nothing and it is NOT the fix.**

| remedy | acceptance hole | permanent operational blindness |
|---|---|---|
| **WA-10, the PRINT** | **CLOSED** — a mis-sequenced exercise emits *"lookup did not complete: AccessDenied"* and announces itself | **CLOSED — and it runs FOREVER.** Every later transport error, future IAM change, or genuinely-absent user stays separable from the legitimate blank |
| the SEQUENCING discipline | **CLOSED** — grant first, names appear, the test passes correctly | ⛔ **UNTOUCHED.** After that one exercise, in live serving, a failed lookup and a genuinely absent record emit **the same blank forever** |

>> **SO: the sequencing fix is ACCEPTANCE-SCOPED AND ONE-SHOT — it makes a single run's evidence
valid. WA-10 is a PROPERTY OF THE SYSTEM. For the SYSTEM, only WA-10 closes it, and the sequencing
note is a necessary discipline AT THE APPLY rather than a substitute.**
⛔ **WA-10 IS THEREFORE NOT DISCHARGEABLE BY POINTING AT THE SEQUENCING.** *(It remains dischargeable
by pointing at code that already separates the two cases — that was always the intent.)*

*(Stated as a condition, not a finding: neither `3.0.0_SA_CVO~Z` nor I has read the enrichment code,
and if the two cases are already separate in what was built, this costs nothing.)*

## FREE FIXTURE — the measured pre-W-A baseline (2.0.0_SA_COO~Z fold ~20:28Z, from 0.4.0_DT_ClientPlatform~Z's surprise-channel note 2809)

The TAC-2' water-test row is a **completed lifecycle whose correct analytics values are already known
and were independently witnessed by four seats.** Use it rather than rediscovering one:

| ticket | `TCK-20260820-dcec0012` |
|---|---|
| created | 2026-08-20T20:18:09.873Z |
| claimed | 2026-08-20T20:25:52.709Z (POST /claim 200, `dt-promote-internal@opalinvest.dev`) |
| completed | 2026-08-20T20:25:53.113Z (POST /complete 200, same identity) |
| ⇒ `time_to_claim_s` | **462.836** |
| ⇒ `time_to_resolve_s` | **463.240** |

**MEASURED BASELINE:** on that completed row, top-level `claimed_by` and `completed_by` are **BOTH
NULL**, while `events[]` carries the actor correctly at every transition
(created `svc-ticket-form` → claimed → completed). Same class, same row: `requester_email` and
`firm` are null at top level while the nested `requester{}` object carries both.

**How to use it, and the honest bound:** this is the *pre-W-A baseline*, not a defect report — the
fields it shows empty are precisely the ones this TO fills. It gives WA-1/WA-2 a **regression
anchor with pinned arithmetic** (a post-W-A claim/complete cycle must populate what this row leaves
null, and the two derived seconds values above are what correct looks like). ⚠ **Whether those keys
are schema-present-but-unwritten or absent-and-rendered-null is a BUILD-TIME READ you owe at the
source — do not assume either from this table.** 0.4.0_DT_ClientPlatform~Z surfaced and took no action, correctly.

<compiler_tools_mandate>
Before write: `comp-blast` on ticket_center lambda + `comp-iam service opal-ticket-api` (floor).
Before commit: `.tools/commit-gate.sh` (universal); `comp-pipescript` n/a (not a gold script).
After commit: live simulate-principal-policy per WA-6; `comp-validate` n/a (no gold artifact).
</compiler_tools_mandate>

<cross_domain_coordination>
`infra/aws/lambda/ticket_center/lambda_function.py` is SHARED with W-C half (b) (READ-OWN matrix)
and W-D (SUMMARIZE action). SEQUENCE: W-A lands FIRST; W-C(b)/W-D rebase on it. MCP the W-C/W-D
builder (same seat today — self-coordination note stands if reassigned). New resource:
opal-users-v2 (read) — WA-6 covers. No portal files in this TO (the client view is W-C).
</cross_domain_coordination>

## Do not
No alert/SNS/SES/monitor machinery (2026-07-28 moratorium; the nudge path is W-B and is
Andrew-asked there). No client-visible surface changes here (W-C). No matrix widening here
(READ-OWN is W-C; SUMMARIZE is W-D). Do not begin before the dep-3 registration sitting completes
unless 1.0.0_SA_CTO~Z re-sequences.

## Reporting
Completion report → 2.0.0_SA_COO~Z (validation) cc 1.0.0_SA_CTO~Z (acceptance gate) + 0.0.0_AB_MSTR~Z (laptop ferry for the
apply leg). Surprise channel: one line to 2.0.0_SA_COO~Z. Session log with Compiler Tools section =
deliverable.
