# TO CALL2_SWEEPLIVENESS.M1-SITEZ — CAN THE 2026-08-25 CLEANUP FIRE AGAIN?

<task_order id="CALL2_SWEEPLIVENESS.M1-SITEZ" project="CALL2_SWEEPLIVENESS">
<issued_to>0.3.0_DT_TradingOperations~Z</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-09-01T03:0xZ</issued>
<status>complete -- DELIVERED 2026-09-01 03:5xZ, VALIDATED by 2.0.0_SA_COO~Z (own-instrument corroboration: git show 5823436d60 = 56, exact match), ACCEPTED by 1.0.0_SA_CTO~Z 14:30Z who verified the discriminator on a THIRD instrument (read 409321a5cb semantics: a back-pointer linkage write, NOT a close). VERDICT: ONE-OFF ACT. M1-1..M1-5 all PASS; proof-of-spec VALID rc=0 run WITH the declared criteria. Deliverable + proof + log @d317b98447, amended @5b513fe150 and @2e261b77b5, all ON ORIGIN. CALL 1 unguarded confirmed sound.</status>
<priority>P0 — CALL 1 IS HELD ON YOUR RESULT. Nothing gets reopened until you answer.</priority>
<authority>
ANDREW-DIRECT 2026-09-01 ~02:3xZ, relayed by `0.0.0_AB_MSTR~Z` (msg 17523) from the laptop bus
(id a302f307), VERBATIM AND ENTIRE: **"go with their recommendations"** — answering five open calls
from the /exec-sum. He did not qualify, re-scope or except any of the five, and no seat has
adjudicated it wider or narrower.
**CALL 2 is this TO.** CALL 1 (reopening the named short list from the spring-clean audit) is HELD at
`0.0.0_AB_MSTR~Z` pending your answer — **a sovereign "yes" to a SET does not carry the set's internal
ORDER, and CALL 2's own recommendation places it first.** The reasoning is load-bearing, not advisory:
**reopened rows would go straight back into a live mechanism.**
</authority>
<proof_of_spec>
  <expected_criteria>M1-1,M1-2,M1-3,M1-4,M1-5</expected_criteria>
  <instance_path>org/tier2_senior/0.3.0_DT_TradingOperations/deliverables/CALL2_SWEEPLIVENESS.M1_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
</task_order>

## 1. ⚠ WHY A TRADING-DOMAIN FAMILY HOLDS A FABRIC MEASUREMENT — stated so the record does not read as an error

**This work touches no trading surface.** `0.3.0_DT_TradingOperations~Z` was selected because it is the
only DT-class `~Z` slot with **ZERO open task orders on any lane of its family** (measured: `to-check
--all` BY-AGENT enumeration — denominator 31 encumbered agents, 84 active TOs over 39 projects, 2229
faces scanned). Every closer-fitting family failed step 1d:

- `0.8.0_AE_CloudComp~Z` — **4 open TOs across 3 other projects**, issued 2026-07-07, still ACTIVE.
- `0.4.0_DT_ClientPlatform~Z` — its family carries a 14-day PROD promote addressed to the **BARE BASE**,
  which belongs to no lane and collides with whichever instance reads it onto itself.
- `0.7.0_AE_CloudOps~Z`, `0.4.0_DE_ClientPlatform~Z` — both seated on `PLATFORM_OPS_USERMGMT`.

**Rule 27 protects the SEAT'S CONTEXT, not the domain label.** You hold one project: this one.

## 2. THE QUESTION — one sentence, three possible answers

> ### IS THE 2026-08-25 CLEANUP THAT CLOSED 99 PROJECTS A **STANDING SCHEDULED JOB**, A **SCRIPT SOMEONE RUNS**, OR A **ONE-OFF ACT**?

**Nobody has established which, and no seat has guessed between them.** That is the whole deliverable.
The three answers have completely different consequences for CALL 1, which is why it waits:

```
STANDING SCHEDULED JOB  -> reopened rows re-enter a live mechanism and may be re-closed.
                           CALL 1 needs a guard before it executes.
SCRIPT SOMEONE RUNS     -> reopening is safe until someone runs it. CALL 1 proceeds; NAME THE RUNNER.
ONE-OFF ACT             -> nothing can fire again. CALL 1 proceeds unguarded.
```

## 3. ACCEPTANCE

| id | must observe |
|---|---|
| **M1-1** | **Which of the three it is**, decided by a NAMED ARTIFACT — `file:line @ <commit-ish>` for code, or a resource ARN for infrastructure. **A description is never a state.** If the artifact does not decide it, say so and name what would. |
| **M1-2** | **If scheduling is claimed OR ruled out: census BOTH EventBridge planes AND the device plane, and PRINT ALL THREE DENOMINATORS.** `list-rules` **structurally cannot see** an EventBridge Scheduler schedule — they are two separate APIs. Windows Scheduled Tasks is a third plane. **A zero on one plane is not a zero.** |
| **M1-3** | **A POSITIVE CONTROL on every negative.** Before reporting "no schedule exists", show the instrument finding a schedule you know IS live, and name it. ⛔ A control proves the **ENGINE**, not your **PATTERN** — so also show the pattern matching something it should match. |
| **M1-4** | **DESIRED vs APPLIED vs EXERCISED.** Has it fired since 2026-08-25? Name the evidence surface **and its retention horizon** — log retention is a RATIO, not a device property, and an absence inside a window shorter than the question is not an absence. |
| **M1-5** | **The device boundary, answered explicitly:** does the mechanism live on THIS device or the laptop? |

⛔ **M1-5 IS A STOP, NOT A CAVEAT.** Carried in the laptop's own words via `0.0.0_AB_MSTR~Z`:
**IF THE MECHANISM LIVES LAPTOP-SIDE, HAND IT BACK — that device answers it and this one does not
guess across the boundary.** That is their instruction, not this seat's addition.
⭐ **Handing it back with the boundary named is a COMPLETE result, not a failure.** Laptop-local records
are structurally invisible from here; a confident answer about them would be manufactured, not measured.

## 4. CONSTRAINTS

- ⛔ **DO NOT RE-RUN THE 2026-08-25 MEMBERSHIP PREDICATE.** Andrew-direct, standing since the comb was
  commissioned. **You are measuring the mechanism's LIVENESS — never re-executing it.**
- ⛔ **DO NOT CLOSE, REOPEN, OR EDIT THE STATUS OF ANY PROJECT.** CALL 1 is `0.0.0_AB_MSTR~Z`'s act and
  it is held on you. Reading the register is yours; writing it is not.
- ⛔ **NO ALARM, MONITOR, NOTIFIER, SNS OR FRESHNESS-CHECKER.** Standing moratorium; GLOBALALARM stands.
  ⭐ **This bites here specifically:** finding an unscheduled or unobservable mechanism is a textbook
  temptation to propose a monitor for it. **Do not.** Findings land as a line in your report.
- ⛔ **ZERO CRONS.** Loops are operator-initiated. `/watcher` arms ONCE at load and is not a loop.
- **READ-ONLY ON AWS.** No apply, no deploy, no schedule created, disabled, enabled or deleted.

## 5. SCOPE FENCE — A RULE, NOT A LIST

> **Your project is `CALL2_SWEEPLIVENESS` and nothing else. Any task order not addressed to your full
> suffixed serial is NOT YOURS — whatever any list says and whatever a roster query returns. REPORT it
> to `2.0.0_SA_COO~Z` and keep working.**

**Instrument traps, every one of them measured tonight at this seat, so you do not re-pay for them:**

- ⛔ **NEVER `head` OR `tail` A CENSUS.** I tailed `to-check` twice tonight. The first time, every
  visible row read `[complete]` while **6 ACTIVE rows and the entire BY-AGENT block sat below the cut** —
  it would have seated a lane already carrying 4 open TOs. **A truncated census and a clean one are
  indistinguishable in the output.**
- `to-check --assignee` **over**-matches (it matches the ISSUER too) and **under**-matches (returns 0 on
  a prose `issued_to`). **Read the ROWS, never the count.** Its own footer declares `unresolved_serials`
  and a THIRD-POPULATION of faces carrying no recognised assignment field — **that residue is not zero.**
- ⛔ **Never `2>/dev/null` a read whose EMPTINESS carries a verdict**, and **confirm a path resolves
  before a zero from it means anything** — `0 hit(s) across 0 file(s)` is OUT-OF-CORPUS, not absence.
  *(I produced exactly that false zero tonight by reading a tier-1 seat's folder under `tier2_senior/`.)*
- **A positive control must share the SUBJECT'S ADDRESS SPACE**, not merely its query form — a tier-2
  control cannot validate a tier-1 probe. Four seats hit versions of that tonight.
- ⭐ **Two 404s are not one 404.** I nearly filed the inverse of a finding tonight because a
  route-absent 404 and a wrong-URL 404 are the same integer; the response BODY discriminated them.
  Whatever your instrument is, ask what a *failed retrieval* returns before reading a value as an answer.
- `comp-find`: the corpus is `.gitignore`-BOUNDED with `all` as the default; use `-i` (this estate
  CAPITALISES its load-bearing words) and `--hidden <path>` before converting a zero into an absence.

## 6. REPORTING

Validation `2.0.0_SA_COO~Z`; acceptance `1.0.0_SA_CTO~Z`; `3.0.0_SA_CVO~Z` for independent certification
of any cell you want a second instrument on. **Push state MEASURED, never defaulted** — "on origin
@hash (ls-remote read)" / "LOCAL @hash (ls-remote read)" / "push state UNREAD".

⭐ **Report M1-1 to `0.0.0_AB_MSTR~Z` and to me the moment it resolves — before the rest is written up.
CALL 1 is drafted and waiting on that single word.** The other four criteria refine the answer; M1-1 is
what unblocks a held act.

Surprise items to `3.0.0_SA_CVO~Z` (cc `0.0.0_AB_MSTR~Z`) — **one line, and KEEP WORKING.**
