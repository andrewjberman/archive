# W-A schema record — Rule-24 filing for the ticket row's day-one field set
**Seat:** 0.5.0_AE_OpalETL~Z · **Written:** 2026-08-20 ~2135Z · **TO:** D7_TICKETING.WA-SITEZ (WA-5)
**Authority:** Andrew-direct 2026-08-20 TICKET LIFECYCLE v2 (O6 "analytics built in to the DDB …
process natively" + the no-retrofit word), via CTO~Z ruling 3 and the ~20:09Z day-one amendment.
Rule 24 as widened 2026-08-20: **every schema-enumeration act carries this filing.**

## 1. The field set, and the ONE GRAIN it sits at

**Declared grain: ONE TICKET'S CURRENT LIFECYCLE.** Every field below is a property of a single
ticket row at read time. Nothing here describes a cohort, a queue, or a person.

| Field | Written by | Meaning |
|---|---|---|
| `schema_version` = 2 | create | the row's shape version — the cheapest future-proofing |
| `client_updates[]` `{ts,author,text}` | create (entry 0) + claim/complete appends | the client-request conversation, IN the row |
| `first_response_at` | first responding transition, once | when Opal first responded |
| `reopened_count` | create (0); a future reopen action | how many times reopened |
| `priority` | nobody yet — **RESERVED** | reserved by his word, unpopulated until defined |
| `category`, `tags[]` | claim/close | free-form classification |
| `claimed_at`, `time_to_claim_s`, `claimed_by{}` | claim | claim analytics + claimer identity |
| `completed_at`, `time_to_resolve_s`, `completed_by{}` | complete | resolution analytics + closer identity |

## 2. Four postulates

**(i) MECE / collectively exhaustive against the declared layer.** The layer is "what one ticket's
lifecycle needs to answer without a join". Checked member-for-member against the questions the
lifecycle asks: who asked (`requester`, deployed) · what (`ticket_type`/`title`/`description`,
deployed) · what was said since (`client_updates[]`) · when did we first respond
(`first_response_at`) · who took it and how fast (`claimed_by`/`time_to_claim_s`) · who closed it
and how fast (`completed_by`/`time_to_resolve_s`) · how it ended (`status` + W-C/W-D's
`closure_reason`) · has it recurred (`reopened_count`). **Deliberately NOT here:** the terminal
`closure_reason` axis (W-C/W-D's, adopted separately @f834702451 — one row, two schemas, and this
filing does not cover that one).

**(ii) Same grain.** Every value is a scalar or list *about this ticket*. The one thing that could
have broken this is timing: a stored per-cycle array would mix a lifecycle-grain fact with a
cycle-grain one. It is not stored — see §3.

**(iii) Intent coherence — one axis, one intent.** Each field answers exactly one question. Two
near-misses, both resolved rather than papered over:
- `claimed_by` carries IDENTITY, not authorization. It is a display snapshot; the authoritative
  actor for any audit is `events[]`, which already records every transition with its actor. The
  snapshot never becomes the authority.
- `client_updates[].author` is a NAME OF WHO WROTE, not a permission claim. Who *may* write is the
  matrix's business (W-C), not this field's.

**(iv) State coherence — one remedy moves them all.** Every field above is written by the same
mechanism (the Lambda, at create or at a transition) and needs no per-field machinery. **The axis
member that does NOT move with the others is named rather than hidden: `priority` is RESERVED with
no writer, and `reopened_count` has no writer either until a REOPEN action exists** (a matrix
widening whose natural actor is the requester — CTO~Z ruled it a requester-class action, not an SoD
exception). Those two ship as *declared placeholders*, and a reader must not infer a producer from
their presence.

## 3. Reopen / timing GRAIN — the shape that landed (CTO~Z ruling 3)

**Stored timing scalars are CURRENT-CYCLE BY DEFINITION.** `time_to_claim_s` and
`time_to_resolve_s` describe this lifecycle pass. After a reopen they describe the LATEST cycle,
and that is now stated rather than implied.

**Cross-cycle history DERIVES from `events[]`; it is never stored.** `events[]` already records
every transition with actor and timestamp, so a stored per-cycle array would be a **second home for
a truth `events[]` already holds** — the two-homes defect. Accordingly `reopened_at[]` is
**served-but-derived** (computed at read from `events[]`), while `reopened_count` **is stored**
because a board filters on it, and Andrew's field set is delivered intact at the API surface.

## 4. opal-users-v2 snapshot semantics — MEASURED, not assumed

The claim/complete enrichment reads the directory **server-side** and writes a **display-grade
snapshot on the row — not a live join**. A client view therefore shows the name the claimer had
*at claim time*, which is the honest thing to display beside a timestamp and which survives a later
directory change.

**Measured facts about that table (live `describe-table` + a bounded 3-item sample, 2026-08-20 —
both of which corrected this build):**
- keyed **`PK` = `USER#<email>`, `SK` = `PROFILE`** (a single-table design). My first draft used
  `Key={"email": …}`, which is not the schema and would have raised on **every** call.
- **there is no `user_id` attribute.** Present: `PK SK email name firstName lastName firmId tier
  role status createdAt createdBy lastLogin passwordChangedAt passwordHash mustChangePassword
  updatedAt`. So `claimed_by.user_id` is filled with the row's **actual primary key** (the `PK`),
  which is the directory's own identifier. ⚠ **NAMED FOR THE GATE:** `PK` is a deterministic
  function of `email`, so `user_id` carries no information `email` does not already carry —
  whether the field earns its place is a schema call, not mine.

⛔ **The enrichment FAILS SOFT and therefore fails INVISIBLY.** A directory blip must never cost a
claim, so a lookup failure degrades to the authorizer identity and the claim still returns 200.
That is the right behaviour and it has a price: **neither a missing IAM grant nor a wrong key shape
can be detected from the API's responses.** Two mitigations, both landed: every degradation prints
its reason (CloudWatch — a record, not a monitor), and the IAM grant is verified on the live
primitive rather than inferred (WA-6: `implicitDeny` before this change, positive control
`allowed`, grant added to the role in the same commit).

## 5. `client_updates[]` caps — why the S3 spill is UNNECESSARY, not deferred

Per-entry **2000 chars** (matching the existing `resolution` cap rather than minting a new number)
× per-ticket **50 entries** ≈ **100KB worst case**, inside DynamoDB's 400KB item limit with ample
room for `events[]` and the rest of the row. The least-trusted principal authors the one field
whose growth we do not control, so the caps are the control.

**THE S3 SPILL KEY IS NAMED HERE AND VERIFIABLY NOT BUILT** — with these caps it is unreachable,
so building it would be code for a state that cannot occur (build-ladder rung 1). An over-cap
append is **REFUSED with 409**, never silently dropped.

**APPEND-ONLY IS A PROPERTY OF THE SURFACE, NOT A RULE ANYONE MUST REMEMBER:** the only write to
`client_updates` anywhere in the handler is `list_append` (two call sites: claim, complete). There
is no code path that rewrites or removes an entry, so "append-only" cannot be violated by
forgetting it.

## 6. Outcome-array note (Rule 24 as scoped to predicates, 2026-08-20)

The transition handlers' refusal set is itself an enumeration and is filed as such: a transition
ends **200** (written), **400** (a body carrying server-derived fields — refused, not ignored),
**403** (SoD), **404** (absent), or **409** (state race, or the `client_updates` cap). Checked for
CE against the declared layer "every terminal state of one transition request": no silent-success
member exists, and the 400 is deliberately a refusal rather than an ignore, because a silent ignore
leaves the caller believing they set something.
