# D7_NOTIFY TO-F / F-1 — THE FOUR-LEG FAILURE MATRIX

**Author** `0.5.0_AE_OpalETL~Z` · **2026-08-21** · **TO** `D7_NOTIFY.TO-F` ACTIVE @`4ab6731e51`

**THE QUESTION THIS ANSWERS IS NOT "DOES EACH LEG WORK."** It is: *when one leg fails, what does the
system do?* Every cell below is a **named behaviour**. **No cell says "should not happen"** — where a
cell is unreachable it says by what construction, and where it is undetectable it says by what.

**DENOMINATOR: 4 LEGS x 5 FAILURE MODES = 20 CELLS**, both axes named at issue. *(Not a test count —
the exercises are F-2 and there are more and fewer of them than there are cells.)*

---

## 0. THE AXIS — and the Rule 24 record, because enumerating it is an authoring act

**AXIS INTENT (one, and only one): WHERE IN THE LEG'S OWN CHAIN THE FAILURE OCCURRED.** Every leg,
without exception, runs the same chain:

```
TRIGGER  ->  CONFIG RESOLVE  ->  CONTENT COMPOSE  ->  TRANSPORT SUBMIT  ->  DELIVERY
   M1            M2                   M3                    M4                M5
```

| | mode | means |
|---|---|---|
| **M1** | NOT TRIGGERED | the leg's entry point was never reached this cycle |
| **M2** | CONFIG UNRESOLVED | it ran; a target, credential or parameter is unset or unresolvable |
| **M3** | CONTENT UNRESOLVED | config was fine; the data needed to compose did not resolve |
| **M4** | TRANSPORT REFUSED | a well-formed send was submitted and the transport rejected it |
| **M5** | ACCEPTED, UNDELIVERED | the transport accepted; no human received it |

**(i) MECE.** *Mutually exclusive* by an explicit tie-break: **a failure is classified by the FIRST
stage that fails.** A run with both a bad address and bad data is M2, not M2-and-M3.
*Collectively exhaustive* **against a DECLARED LAYER, and the layer is the load-bearing half:** this
axis covers **AVAILABILITY — the leg did not deliver.** It does **not** cover **CORRECTNESS — the leg
delivered, and was wrong.** **THAT UNCOVERED MEMBER IS REAL AND IT IS THE HIGHEST-CONSEQUENCE ONE IN
THE SYSTEM** (a client email reaching the wrong client), so it is not waved off — it gets its own
axis in §3 rather than being smuggled into this one.
**(ii) SAME GRAIN.** All five are stages of one execution chain. *A credential expiry is NOT a sixth
mode* — it is a CAUSE of M2/M4, and admitting causes onto a stage axis is exactly the grain break the
postulate forbids. It lives inside the cell it causes.
**(iii) INTENT COHERENCE.** One intent: locate the break. No value smuggles in severity, likelihood
or ownership — those are columns, not axis values.
**(iv) STATE COHERENCE — AND THIS AXIS FAILS IT, DELIBERATELY AND VISIBLY.** State axis:
*observable-in-estate vs not*. **M1–M4 are observable** (exit codes, greppable log tokens, raised
exceptions). **M5 IS NOT OBSERVABLE BY ANY LEG'S OWN CODE** — the transport accepting *is* our leg
succeeding — and the instrument that would observe it (bounce/complaint topics, a delivery monitor)
is **explicitly forbidden** by this TO's own DO-NOT and by the standing notification moratorium.
**So building the obvious instrument delivers M1–M4 and structurally cannot deliver M5.** Postulate
(iv) requires naming which values do not move: **it is M5, in all four legs.**

---

## 1. THE LEGS

| | leg | plane | entry point |
|---|---|---|---|
| **L1** | internal DL email | Lambda (`opal-ticket-api`) | `notify_dl_isolated` |
| **L2** | Teams buzz | runner (Scheduled Task, 5 min) | `runner.main` -> `intake_pass.run_once` |
| **L3** | client email (submit-ack + pickup) | Lambda (`opal-ticket-api`) | `notify_client_isolated` |
| **L4** | escalation sweep | runner plane | `sweep.py` — **UNWIRED** |

---

## 2. THE MATRIX — 20 cells

### L1 — INTERNAL DL EMAIL (Lambda)

| mode | named behaviour |
|---|---|
| **M1** | **Silent at runtime, by construction.** If the CREATE write path stops calling it, nothing at runtime says so — the ticket returns 201 exactly as before. Caught only at **build time**, by the A2 seam test that asserts the call site by AST. **The runtime signal for this cell is: there is none.** |
| **M2** | `DLAddressUnset` -> caught -> **`WE_DL_UNCONFIGURED`** -> ticket still **201**. Covers all three refusal cells (map unset · firm absent · no `*` default). A **CONFIG** act. |
| **M3** | **DEGRADES SILENTLY.** A missing content field renders as an **empty string** (`:495-505`), and if `firm` is missing the subject collapses to the bare title. **No token, no counter.** The email goes out incomplete and nothing says it was. |
| **M4** | SES raises (throttle · unverified identity · IAM deny) -> caught -> **`WE_DL_SEND_FAILED`** -> ticket still **201**. An **OPERATIONAL** act, deliberately a different token from M2 because the remedies are opposite. |
| **M5** | **Nothing happens and nothing can.** SES returns a MessageId; if the DL bounces or does not exist, this leg has already succeeded. Undetectable per §0(iv). **Live today:** the DL does not exist yet (`WE-1` open), so this cell is not hypothetical. |

### L2 — TEAMS BUZZ (runner, 5-minute Scheduled Task)

| mode | named behaviour |
|---|---|
| **M1** | **No buzz this cycle; nothing is lost, only delayed.** The cursor is unmoved, so the next fire catches up. **TWO signals, and the second is stronger than the design's own claim:** `LastTaskResult`, and `run_intake.cmd`'s log, which writes a **start** line *and* an **exit** line per pass (`%USERPROFILE%\opal_ticket_intake\runner.log`). **The start line makes non-firing detectable BY ABSENCE**, which `LastTaskResult` alone cannot do — it holds the last result forever and looks identical whether the task ran a minute ago or never ran again. Both are pull-only reads a human must go and look at, by design (moratorium: no alert). |
| **M2** | Two distinct exits: **`exit 4` CONFIG-REFUSED** (a `runner_config.json` key unset, `portal_base` not https, or the cursor config item **absent** — absence is a refusal, because an empty cursor would buzz the entire backlog) and **`exit 2` IDENTITY-FAIL** (pinned gateway token expired/unsatisfiable). Separate codes because one is a config act and one is a re-auth act. The next 5-minute fire retries. **⚠ THIS CELL IS NOT HYPOTHETICAL — IT IS THE SECOND MOST COMMON OUTCOME IN PRODUCTION. See FINDING 3: 59 of 169 passes (34.9%), longest unavailable window ~130 minutes.** |
| **M3** | **Two sub-cells, and they are not alike.** *Contract violation* -> **`REFUSED`**, named field, receipt written, **cursor advances** (a forged row must not wedge the pass forever). *Unparseable `created_at` that passes the shape check* -> **UNCAUGHT `ValueError` — see §4 FINDING 1. This is the one cell in the matrix whose current behaviour is a total, permanent outage of its leg.** |
| **M4** | The gateway call returns no id -> `SendResult(False)` -> receipt `SEND_FAILED` -> **the pass STOPS** (`break`) -> **`exit 3`**. Ordered retry: nothing behind that row is processed, the cursor does not advance, the next fire retries. **Stated trade-off (in-code): a send that succeeded server-side but lost its response yields a DUPLICATE buzz. A duplicate line is the cheaper error; a silently lost buzz is an SLA miss.** |
| **M5** | Graph returns a message id; nobody reads the channel. Undetectable per §0(iv). |

### L3 — CLIENT EMAIL (Lambda) — submit-ack + pickup

| mode | named behaviour |
|---|---|
| **M1** | As L1/M1: silent at runtime, caught only by the seam test. |
| **M2** | **Link omission is a DEGRADATION, not a failure, and that is the ruled behaviour.** Firm absent from `CLIENT_LINK_MAP` -> **the link is OMITTED, never defaulted** (there is deliberately no `*` row: an inflection client must not be handed a 49F link). **The email still sends.** |
| **M3** | **Three sub-cells, three different actions.** *Recipient set not singular* -> `ClientRecipientNotSingular` -> **`WE_CLIENT_NOT_SINGULAR`, NO SEND** — a leak averted, and the only M3 in the matrix that refuses. *Claimer name unresolved* -> **`WE_CLIENT_NAME_DEGRADED`** with a three-way reason token, **and the message STILL SENDS** with "An Opal advisor" (E-2 ruled 2026-08-21T09:06Z). *Any other missing field* -> **renders blank, silently**, as L1/M3. |
| **M4** | SES raises -> caught -> **`WE_CLIENT_SEND_FAILED`** -> the ticket/claim stands. |
| **M5** | Undetectable per §0(iv). **Worse here than on L1:** the recipient is a **client**, so an undelivered ack is invisible to us and visible to them as silence. |

### L4 — ESCALATION SWEEP (runner plane) — **UNWIRED**

| mode | named behaviour |
|---|---|
| **M1** | **THIS IS TODAY'S STATE, NOT A HYPOTHETICAL. The sweep has never run and cannot run: nothing imports it.** An unaddressed request sits past 2p ET and **no escalation occurs, ever.** This is `F-3`'s subject and it is held by `F-0` pending Andrew's explicit word. |
| **M2** | `CutoffUnset` -> **refuses rather than defaulting**, because a baked `14:00` would be a second literal that could drift from the client-facing cutoff. **UNREACHABLE today** (M1). |
| **M3** | **Handled, and handled BETTER than L2's identical input class:** an unparseable `created_at` returns `None`, is counted into `Digest.unparseable`, is **NOT adjudicated**, and the digest's `frame()` line **states it beside the count**. **UNREACHABLE today** (M1). |
| **M4** | **UNDEFINED BY DESIGN, not failed.** The scope fence stops this module at a payload object — no sender, no surface, no recipient. There is no transport to refuse. |
| **M5** | **N/A** — no transport bound. |

---

## 3. THE EXCLUDED AXIS, NAMED — correctness failures that report success

§0(i) declares this axis covers availability. These are the members it does **not** cover, listed
rather than omitted, because **the worst failure in this system is not a leg that stops — it is a leg
that succeeds at the wrong thing.**

| leg | correctness failure | what guards it today |
|---|---|---|
| L1 | the DL map points at the wrong address -> a firm's ticket lands in another firm's inbox | **nothing structural** — map correctness is a config review |
| L3 | the recipient derivation yields the wrong client | **`ClientRecipientNotSingular`** guards *plurality*, not *identity*. A single **wrong** address passes it. |
| L3 | the firm-keyed link points at another firm's portal | the map has **no `*` row** — omission is structural, misconfiguration is not |
| L2 | a buzz composed from the wrong row / a duplicate buzz | duplicates are an **accepted, stated** trade-off (L2/M4); receipts are the human's dedupe evidence |
| L4 | escalating a ticket that was in fact addressed | the predicate is `status == "open"`, ruled by Andrew; claimed-but-unanswered is **out of scope by his word** |

**This table is a disclosure, not a work item.** Nothing here is proposed for building — several of the
obvious guards would be monitors, which are under moratorium.

---

## 4. FINDINGS

### FINDING 1 — L2/M3: an unparseable `created_at` PERMANENTLY WEDGES the buzz leg (MEASURED)

`row_contract.validate_form_ticket` checks `created_at` by **SHAPE** (`len >= 20 and endswith("Z")`);
`buzz.received_eastern` requires it to **PARSE**. The gap between those two is an uncaught
`ValueError` out of `compose_buzz`, which is called **outside** `run_once`'s try.

**Exercised, three ways, with a positive control** (the contract still refuses `"short"`, so it does
discriminate — the acceptance is specific to this shape):
1. **PERMANENT WEDGE.** The cursor advances only on a terminal act, so it never gets past the bad
   row. Passes 1, 2 and 3 die identically. **Every 5 minutes, forever.**
2. **TOTAL, NOT PARTIAL.** A stamp sorting before the good rows (`run_once` sorts by
   `(created_at, ticket_id)`) means **every subsequent row is never buzzed.** The whole leg dies,
   not one ticket.
3. **OFF-CONTRACT.** An uncaught exception exits **1**, and the declared exit contract is
   **0/2/3/4/5**. `LastTaskResult` — *the one instrument this design names* — shows a value the
   design has no mapping for.

**REACHABILITY, CHECKED BEFORE REPORTING, AND IT CHANGES THE SEVERITY:** `created_at` is
**server-generated** (`lambda_function.py:389`, `_new_item`), never client-supplied. **A client cannot
trigger this through the form.** It requires a direct table write — a hand edit, a second producer, or
a future writer. **Low likelihood, total impact** — and the contract module exists precisely because
the consumer does not trust the producer.
**AND IT HAS NEVER FIRED, MEASURED RATHER THAN ASSUMED:** the live runner log carries **169 passes /
169 exit lines, 0 unterminated**, and its exit-code census is `rc=0` and `rc=2` **only** — no `rc=1`.
An uncaught exception would log `intake pass exit 1` (the wrapper captures `%ERRORLEVEL%`), so its
**absence across the complete record is positive evidence the wedge has not occurred in production**,
not merely an absence of reports.

**APPENDED 2026-08-21T10:1xZ AFTER `2.0.0_SA_COO~Z`'s VALIDATION -- THE SEVERITY ABOVE WAS TOO
GENEROUS TO ITSELF, AND THE CORRECTION MATTERS TO THE DECISION SITTING ON THIS FINDING.** They
re-derived the de-escalation at source rather than accepting it, and it **holds**: `:389` is the only
write, `_now()` is a call and not a body read, **0 request-body reads in the create range**, 12
`created_at` hits of which exactly 1 is a write, and the other table writers (`update_item` on
claim/complete) never touch it. **The API cannot produce the malformed stamp.**
**BUT THAT PROVES ONLY THAT *THIS LAMBDA* NEVER WRITES A BAD STAMP. IT CANNOT PROVE NOTHING ELSE
DOES.** A **direct table write** -- a backfill, a migration, a console edit, a second producer --
lands a row that never passed `_now()`.
>> **SO THE ACCURATE SEVERITY IS NOT "LOW LIKELIHOOD": IT IS *UNREACHABLE THROUGH THE PRODUCT
SURFACE, REACHABLE THROUGH ANY OPERATOR OR MIGRATION PATH*. Latent and one manual write away -- and
a manual write against the ticket table is exactly the sort of thing someone does DURING AN
INCIDENT.** The wedge is therefore **anti-correlated with the moment you can afford it**: the
conditions that produce the bad row are the conditions under which the buzz leg going permanently
dark costs the most. *(Their derivation, recorded here because it strengthens a finding of mine that
is currently in front of the gate owner as a decision -- and because "low likelihood" was the phrase
that would have made the decision look easier than it is.)*

**RECOMMENDED REMEDY (not applied — `intake_pass`/`row_contract` are live-production files with a
5-minute fuse, and the repair is itself a deploy):** make the contract **parse** the stamp instead of
measuring it. That converts a total wedge into an **already-existing, already-named, already-handled**
outcome — `REFUSED`, receipt written, cursor advances — with no new code path and no new failure mode.
**The sweep already does exactly this** (`_parse_created` -> `None` -> counted, not adjudicated), so
the estate contains both the defect and its own remedy pattern, in one package.

**FIXED 2026-08-21T141933Z -- ACT 2, on Andrew's word ("approved on all three, proceed"), gate decision by
`1.0.0_SA_CTO~Z` (HOLD lifted).** `validate_form_ticket` now PARSES the stamp instead of measuring
it, so the row lands in the **existing** `REFUSED` outcome -- receipt written, cursor advances -- with
no new code path and no new failure mode.
**PLANE, measured before the act:** NOT in the Lambda package (`files = ['lambda_function.py']`), ON
the runner import path (`runner -> intake_pass -> row_contract`), task live on a 5-minute cadence
from this tree. **So saving it WAS the deploy**, and bar A5-A7 applied: exercised in the same
continuous act, in this tree, **scored on output** -- a real dry-run pass emitted
`REFUSED ... does not parse` for the bad row and **`WOULD-BUZZ` for the row behind it**
(`fetched=2 buzzed=1 refused=1`). That second line is the fix: the wedge is gone.
**THE COUPLING IS NOW A TEST, NOT A COMMENT.** `buzz` imports `row_contract`, so they cannot import
each other and the parse expression is necessarily duplicated -- and a duplicated expression is
exactly what drifts back into this defect. The property *anything the contract ACCEPTS, the composer
can HANDLE* is asserted over a 7-stamp set, with a guard that it is not vacuous.
**THE `expectedFailure` FORCING FUNCTION WORKED AND THAT IS THE REUSABLE PART:** it flipped to
**UNEXPECTED SUCCESS** and took the run **non-zero**, so the fix could not land quietly -- and it
surfaced the three sibling tests still documenting the *defect*, which then had to be rewritten to
assert the *behaviour*. **That was the maintenance it existed to trigger, not an inconvenience.**

### FINDING 2 — the two SES legs disagree about whether degradation is announced

L3 announces a degraded **claimer name** (`WE_CLIENT_NAME_DEGRADED`, three-way reason) because E-2
ruled it must. **Every other missing field on both legs renders blank and says nothing.** So the
estate has one loudly-instrumented degradation and a family of silent ones beside it, on the same
code path. **Named, not fixed:** widening it is a design call, and a token per field would be noise.

### FINDING 3 — L2/M2 IS THE LEG'S DOMINANT FAILURE AND IT IS MEASURED, NOT PREDICTED

Read off the **live** runner log — the complete record (no rolled predecessors), **denominator
printed with every figure**:

```
SPAN      2026-08-20 15:59 ET  ->  2026-08-21 05:54 ET   (~14h)
PASSES    169 start lines / 169 exit lines / 0 unterminated
EXITS     rc=0  110  (65.1%)      rc=2 IDENTITY-FAIL  59  (34.9%)
WINDOWS   6 separate exit-2 runs of 13 runs total; lengths 26, 20, 8, 2, 2, 1 passes
LONGEST   26 consecutive passes ~= 130 MINUTES, 00:09 -> 02:14 ET
```

**THE BUZZ LEG WAS UNAVAILABLE FOR ROUGHLY A THIRD OF ITS PASSES, WITH A WORST WINDOW OF ~2 HOURS.**
The cause is the pinned gateway credential the TO itself names (the **~1h dependency**), and recovery
is **agent-triggered** — which is why the longest window is **overnight**, when no seat was active to
re-trigger it.
**NOTHING WAS LOST, AND THAT IS THE DESIGN WORKING:** the cursor does not advance on a failed pass,
so a ticket arriving inside a window is **delayed, never dropped**. But a client-facing SLA is
measured in wall-clock, and **a form ticket submitted at 00:30 would not have reached the Teams
thread until ~02:15.**
**NOT PROPOSED FOR REMEDY HERE.** Every obvious fix is either a credential-refresh mechanism or a
monitor, and the second is under moratorium. **This cell's value is that it is now a number instead
of an adjective** — the design said "the next 5-minute fire retries", which is true and reads as
though the exposure were five minutes.

### FINDING 4 — M5 is unobservable in all four legs, and its instrument is forbidden

Recorded under §0(iv) rather than as a gap to close. **A delivery monitor is exactly what the
moratorium bans**, and the correct posture is to know the blind spot, not to instrument it.

-- `0.5.0_AE_OpalETL~Z`
