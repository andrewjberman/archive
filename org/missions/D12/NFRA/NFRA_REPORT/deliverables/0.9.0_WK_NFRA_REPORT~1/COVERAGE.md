# COVERAGE / DENOMINATOR CARRIER — every count states what it counted out of (cell RP-s-10, outcome FWD-10)

Authority: `NFRA_REPORT_PRD.md` manifest row S10 (`FWD-10`: *"A reader can trust that a number covers
what it claims to cover"*), brief F3 and F5 (measured starting state below), and the estate's own
`docs/doctrine/A_VALUE_MUST_CARRY_ITS_CLAIM.md`. Renders through `STATE_MODEL.md`/`ROW_STRUCTURE.md`
(this document adds no new state vocabulary; it adds a RULE that binds every count any other cell's row
produces).

## 0. THE RULE, STATED AS BINDING, NOT AS ADVICE

**EVERY COUNT THIS REPORT PRINTS CARRIES ITS DENOMINATOR, IN THE SAME BREATH, NEVER SEPARABLE FROM IT.**
A bare number is never rendered alone. `"3"` is not a value this report emits; `"3 of 7"` is. **EACH
COUNT is checked against this rule at the point it is authored, not audited after the fact** — a row
that cannot state its denominator does not get to state its numerator either. This is the discipline
`FWD-10` names, and it is what binds every other row's numbers, not a suggestion offered beside them.

**A denominator certifies the SWEEP, never the pattern** (bound, verbatim) — "3 of 7 alarm targets have
zero confirmed subscribers" certifies that 7 targets were swept and 3 matched; it says nothing about
whether "zero confirmed subscribers" is the right pattern to have swept for. Confusing the two is how a
correct-looking count survives a wrong question.

## 1. THE MEASURED DEFECT THIS RULE REPLACES

- **Brief F3** — *coverage, not staleness, is the freshness story.* The illustrating case: `mdpf` reads
  `0/1`. A reader told only "stale" or "not stale" about the one thing MDPF has learns nothing about
  the fact that the denominator is 1 — one artifact, total, in scope. **`0/1` and `0/500` are not the
  same finding wearing the same headline**, and a staleness-only rendering makes them look identical.
- **Brief F5** — *the drift section colours on INSTRUMENT FRESHNESS rather than on DRIFT.* A surface
  monitored by one instrument that happens to be fresh reads exactly as healthy as a surface monitored
  by fifty instruments that are all fresh — the COLOUR carries no information about how much of the
  surface was actually swept, only about whether the (possibly tiny) part that was swept looked recent.

**Both are the same defect at two different report sections: a score computed without regard to what
fraction of the truth it is a score OF.** The bound this cell restates directly: *"a thinly-monitored
surface must not produce a score that reads as healthy as a thoroughly-monitored one."* `0/1` reading
green next to `450/500` reading green is exactly that failure, and it is a coverage failure, not a
staleness failure — the fix is a denominator on the number, not a fresher timestamp.

## 2. THE PATTERN TO REUSE — do not mint a second vocabulary

The battery finding is explicit: *"the estate's own a-value-carries-its-claim discipline is the pattern
to reuse... the CONSUMING half is the whole mechanism."* From `docs/doctrine/A_VALUE_MUST_CARRY_ITS_CLAIM.md`:

> *"A value must carry the claim it is making, in a field a consumer can reject on — never in a
> heuristic, a convention, or a reader's memory of how it was produced."*

That doctrine's own worked, LIVE example is exactly the shape this cell needs, and it already exists in
this project: **`org/standards/PROOF_OF_SPEC.schema.json`'s `acceptance[].denominator` field** —
`required`, `type: string`, `minLength: 1`, described as *"every count states what it is out of; 'N/A'
only with a reason."* This is not a proposal; it is a field this worker has satisfied FOUR TIMES already
in this same project (`TO-RP-s-1`, `TO-RP-s-2`, `TO-RP-s-6`, `TO-RP-s-7`'s proof instances), and
`.tools/proof-of-spec-check.py` **actively rejects** an instance where an acceptance row's
`output_evidence` is present but thin (`len(output_evidence.strip()) < 8`) and where `denominator` is
schema-absent or empty. That is a REAL consuming half: a producer cannot get a proof-of-spec instance
to validate (`rc=0`) without a non-empty denominator string on every row.

**So the SHAPE to copy for the report's own numbers, once its renderer exists, is exactly this:** one
field per count, required, non-empty, sibling to the number, checked by a validator that runs before
the artifact is treated as complete — not a second, report-specific vocabulary for the same idea.

## 3. THE DECLARED LIMIT — the discipline is real here; it is not yet enforced there

**This is the finding the coordinator's steer asked for directly, said plainly rather than dressed as a
field nobody checks.**

The consuming half described in §2 is real **for `PROOF_OF_SPEC` instances.** It does **not yet exist
for the report artifact itself** — the actual daily rendering `FWD-10` is about. Evidence, not
assertion: every report-content cell in this decomposition's manifest, including this one, is tagged
`wire` in the PRD's own lane column (S1, S2, S4, S6, S7, S8, S9, S10, S11, S12, S13 — `S3` is `align`,
`S5` is `port`; none is `verify` or a build of the renderer itself). **`wire` cells write the LAW the
report must follow; none of the cells run so far has built the report's own generator code, so there is
no artifact yet for a consumer to run against, and no validator yet that could reject a bare count in
one.** A rule stated only in this document's prose (§0 above) is, today, a WRITING CONVENTION this
project's own cells have chosen to follow voluntarily — not a GATE. Per the doctrine this cell is
directed to reuse: *"a denominator field that nothing rejects on drifts to unpopulated."* Nothing yet
rejects on the report's own future denominators, because the report does not yet exist as code.

**This is not a gap this cell can close from its own paths.** Building a report-generator lint/schema
is a code artifact outside `org/missions/D12/NFRA/NFRA_REPORT/deliverables/`, `decompositions/`, `prd/`
and the two other paths this cell is admitted to — and per the bound, this cell's job is to state the
discipline that binds every other row's numbers, not to build the renderer that will one day be bound
by it. The gap is named here so a later cell that DOES build the renderer (or its own schema) inherits
this requirement as a stated dependency rather than reinventing it or omitting it.

**A second, narrower honesty about the one real consumer that DOES exist (§2):** it checks PRESENCE
(the field is non-empty), never TRUTH. `.tools/proof-of-spec-check.py` cannot detect a denominator that
states the wrong sweep size — a row claiming `"3 of 7"` when the real population was 12 passes the
schema exactly as cleanly as a correct one. The defence against THAT failure mode, in this project's own
practice (see §4), has never been a schema field alone — it has been an independent re-derivation or a
positive control, run BY the cell that states the number, at the time it states it. A denominator field
is the FLOOR (Rule 22's own word for this pair of criteria applies equally here); the ceiling is still a
human or a second instrument checking the number, not a schema.

## 4. THIS PROJECT'S OWN ROWS, ALREADY PRACTICING THE DISCIPLINE — worked evidence, not aspiration

Every count this same worker has produced in this project already carries its denominator, voluntarily,
before this cell existed to require it — cited here as evidence the discipline is followable, not
merely statable:

- `ALERT_DELIVERY.md`: *"3 of 7 distinct alarm targets have ZERO confirmed subscriptions"*; *"51 alarms,
  7 distinct SNS topics"* — every alarm-delivery count states the topic population it was swept from.
- `DEPRECATION.md`: *"5 of 10 ALIVE... 3 of 10 AMBIGUOUS... 2 of 10 UNRESOLVED-BY-THIS-WALK"* — every
  deprecation-walk count states it is out of the ten candidates named in Andrew's own ruling text, and
  the document explicitly refuses to let the unresolved five read as either alive or dead by omission.
- `ROW_STRUCTURE.md`: the mutant-control counts (`AC1=25 of 112 lines`, `AC2=3 of 112 lines`) and the
  worked delta specimens each state the population a `worse`/`better`/`unchanged` verdict was drawn
  from.

**None of these was required by a schema when it was written — each was written this way because the
discipline in §0 is the right way to state a number, independent of whether anything enforces it yet.**
That is also the strongest available argument that a future enforcing consumer (§3) would cost little:
the numbers already arrive in the right shape; a validator would only need to reject the absence of a
shape every row already has.

## 5. What this document does NOT do

- Does not build a renderer, schema, or lint step for the report artifact's own future numbers — outside
  this cell's paths, and premature: the artifact those numbers would live in has not been built by any
  cell in this round.
- Does not claim the one real consuming half that exists (`proof-of-spec-check.py`) validates the TRUTH
  of a denominator, only its PRESENCE — stated in §3 rather than left to be assumed.
- Does not mint a second denominator vocabulary distinct from `PROOF_OF_SPEC.schema.json`'s own field —
  per the battery finding, the existing shape is the one to copy.
