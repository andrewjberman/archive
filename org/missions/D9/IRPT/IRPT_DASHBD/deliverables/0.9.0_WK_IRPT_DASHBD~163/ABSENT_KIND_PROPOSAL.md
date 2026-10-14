# ABSENT_KIND_PROPOSAL -- a closed vocabulary for why a figure is absent

Status: PROPOSAL for the CTO's ruling (round 104, cell DB-b-198, order IRPT_DASHBD.TO-DB-b-198). No code reads
`absent_kind`. No sample carries the field. This file adds no component, builder, checker or sample edit.
Issuer of the proposal: 0.9.0_WK_IRPT_DASHBD~163. Contract at this change: 0.4.1 (`unit_scale` on each percent member).

Source facts (measured, counts only): the round-103 sample (sha256 25446cfc...) holds 117 members; 38 are absent at
member grain and 79 are filled; it holds 39 absent by-row entries across 36 by-row maps (11 maps are wholly absent).
The order's figure of 73 absent members reproduces only on the round-101 sample (sha256 76a48793...); see the
surprise row IRPT_DASHBD-D2-W163-S1 in INVESTIGATION_v1.md.

## Vocabulary

The CTO's candidate closed set, each member defined in one sentence:

- `NOT_HELD`: the client holds none of the thing the figure measures, so the baseline prints a dash, never zero.
- `NOT_APPLICABLE`: the figure does not apply to this member, period or account under its definition.
- `NO_SOURCE_YET`: Opal has no source for the figure yet (no sibling contract carries it, or its source is not read by this build).
- `INSUFFICIENT_HISTORY`: the source holds too little history for the period the figure covers.

Proposed fifth candidate, for the CTO's ruling and NOT part of the set the CTO stated:

- `SOURCE_BREAK` (a candidate, not a member): the source holds the period, but a day inside the window carries a null
  daily return, so the window cannot be bridged. Integrity of the held period, a different axis from history length.
  If the CTO rules that a break is a history gap, this member folds into `INSUFFICIENT_HISTORY` and the set stays at four.

## Proposed home of the field

The field is per figure (the same member is absent for one reason in one period and filled in another), so it is
data, not contract. Three carriers were weighed against the shape check `check_sample_shape` (checks/r97), which
today requires the absent form to be exactly `{"absent": str}`, and against the contract's `document.filled_report`,
which requires top-level keys `household` and `values` only.

- **Carrier A (recommended): a sibling key inside the absent form.** A figure holds
  `{"absent": "<reason in words>", "kind": "<KIND>"}`. Changes: `check_sample_shape` and `is_absent` (checks/r101)
  accept an optional `kind` drawn from the closed set; `document.filled_report` names the optional key; the builder
  writes it. The reason text stays the words a reader sees. Cost: one contract bump, three checker edits, no change
  to the member set, the values keys or the top-level shape. A reader that ignores `kind` is unaffected.
- **Carrier B: a static `absent_kind` on each contract member.** Changes: the contract member definitions. It cannot
  hold the kind, because the kind is data-dependent: 33 of the 39 by-row entries are INSUFFICIENT_HISTORY on this
  sample, and the same member is filled on another period. It also breaks the rule that each member's bytes are fixed
  across a version except `unit_scale`. Not recommended.
- **Carrier C: a top-level map on the filled report, `absent_kinds`.** Changes: `document.filled_report` top-level keys
  (from two to three) and the top-level shape check. Every reader of the top-level keys changes. Not recommended.

Who reads it (today and under Carrier A): the sample builder writes the absent form; `check_sample_shape` and
`is_absent` validate it; the tab and the export read each figure by member id and print every absent form as its words
(the contract's `absent_rule`). No reader consumes `kind` yet. A reader that wants the kind for a rule (a dash, a
suppressed row, a retry) must name that rule in its own contract before it reads the field.

## Four-postulate record

Taxonomy law, CLAUDE.md rule 24 (i) MECE, (ii) SAME GRAIN, (iii) INTENT COHERENCE, (iv) STATE COHERENCE, in the form of
R-0006 (MECE and same grain) and R-0009 (intent and behavior coherence) in rcg/rulings/RULINGS.jsonl.

### MECE

Domain: the sample's ABSENT MEMBERS at member grain (a member holding the absent form, or a per-account map in which
every entry is absent) and the by-row ABSENT ENTRIES. Domain falsified first by one unscoped read of the
absent form over the sample: 117 members, 36 by-row maps, 112 by-row entries, 39 of them absent, 27 members holding
the absent form at top level, 11 wholly absent maps. The subtraction below runs from these printed denominators.
Each item was classified by a first-match rule on its reason text, and a second match on any item was asserted absent.

Member grain, denominator 38:

| kind | members | how each is reached |
|---|---|---|
| INSUFFICIENT_HISTORY | 23 | 11 wholly absent per-account maps (3 entries each, all history); 9 household figures whose reason names an account term that is absent for history; 3 members whose reason is history |
| NOT_HELD | 0 | the dash entries sit in partly filled maps, so no member is wholly a dash |
| NOT_APPLICABLE | 0 | none |
| NO_SOURCE_YET | 15 | 9 household-grain return figures (no sibling defines a household daily return series); 6 others (the fee-basis row outside this build's read, the client summary not read by this build, the registration name, the display name, the disclosure text, month to date awaiting a ruled period) |
| SOURCE_BREAK (proposed fifth) | 0 | none |
| **remainder** | **0** | |

By-row entries, denominator 39:

| kind | entries |
|---|---|
| INSUFFICIENT_HISTORY | 33 |
| NOT_HELD | 3 (asset class with no holding on the as-of date; a dash, never zero) |
| NOT_APPLICABLE | 0 |
| NO_SOURCE_YET | 0 |
| SOURCE_BREAK (proposed fifth) | 3 (a window day carries a null daily return, so the link breaks) |
| **remainder** | **0** |

Named members no kind covers. Under the four CTO candidates alone, 3 by-row entries are uncovered: a null daily return
inside a window, on two member ids (`avs.last_12_months.return_cumulative`, `avs.since_inception.return_cumulative`).
They are placed in the proposed fifth candidate `SOURCE_BREAK` and not forced into `INSUFFICIENT_HISTORY`, for the CTO's ruling.
Month to date (one member) reads as NO_SOURCE_YET because its terms exist and the missing piece is a ruling; its
alternative reading is NOT_APPLICABLE, and the CTO should rule which. NOT_APPLICABLE has zero members on this sample.

Mutual exclusivity on this sample: no item matched two rules; no wholly absent map carries two kinds (11 of 11 are pure).

### SAME GRAIN

A kind is a fact about one absent value, so it is recorded at the grain of that value: a by-row entry (one account or
asset class) carries its own kind; a member-grain absent form carries one kind; a wholly absent per-account map has a
member-grain kind only when all its entries share one kind (true for all 11 on this sample). A household figure whose
reason names an account term takes that term's kind, measured once at account grain and carried up; the household
figure does not re-derive it. No kind is a static property of a contract member, because the same member is absent for
different reasons across periods (Carrier B above). If a member's entries ever disagree, its member-grain kind is a set,
not a scalar, and the proposal must be amended before a reader relies on it; none does on this sample.

### INTENT COHERENCE

One axis: the reason a figure is not printed as a number, read by a reader of the report. Three values answer "why no
figure is available from the estate today": NO_SOURCE_YET (no source), INSUFFICIENT_HISTORY (the source is short
for the period), and SOURCE_BREAK if adopted (the held period is not whole). They share the intent "a deficiency in
the estate's data, to be named in words".

NOT_HELD does not share that intent. It states a fact about the client (the client holds none), and its print form
is a dash by the baseline's own rule, which is not a deficiency. A consumer that treats every absent kind as a data
defect would misread a dash. The one-axis test therefore fails for NOT_HELD on a strict reading. The CTO should rule
either that NOT_HELD stays on the axis with its dash print rule stated in the contract, or that it moves to a holdings
axis and the closed set on this axis is the three deficiency values. This proposal does not decide it.

### STATE COHERENCE

The remedy is Carrier A: add `kind` beside `absent` in the absent form. It does NOT move: the reason text (still the words
printed); the figure (an absent form is still never zero and never a default); the member set and the one-entry-per-member
rule of `values`; the `unit` and `unit_scale` of any member; the dash rule for a window the account did not span; any
served value (no sample is rebuilt by this proposal); and the words a reader sees for any figure, since the kind is not
printed unless a reader is written to print it.

## Token census

Method, as the order names it:

    git grep -w -c <TOKEN> -- portal/src/pages/InvestorReporting org/standards org/missions/D9/IRPT data/assets/scripts/gold/irpt_reporting ':(exclude)org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~163'

Denominator (files scanned): `git ls-files -- <same scope> <same exclusion>` = 6153 files.

Counts (word-boundary, whole scope as written, run after this worker's three surprise rows were appended to the investigation file):

| token | hits | files with hits | prior meaning in the scope |
|---|---|---|---|
| NOT_HELD | 176 | 36 | yes: IRPT_YCDGEN holdings-group source status (decomposition R5, overview_coverage.json, a NOT_HELD group whose elements read as unavailable). The portal submodule holds a further 9 hits in 3 files, outside this count (see the scope finding below) |
| NOT_APPLICABLE | 19 | 6 | yes: comp-tool answer-state token in org/standards/COMPTOOL_ANSWER_STATE.enum.json (11 hits, the state the tool voices); an inflection in org/standards/MDPF_TAXSMA_DATA_CONTRACT.json; a cell key in the worker deliverable 0.9.0_WK_IRPT_DASHBD~121/y1_place.py |
| NO_SOURCE_YET | 4 | 3 | no; hits are this order's own text, the round-104 checker and this worker's row S1-S3 text |
| INSUFFICIENT_HISTORY | 4 | 3 | no; hits are this order's own text, the round-104 checker and this worker's row text |

Before the three rows were appended the same run read NOT_HELD 171, NOT_APPLICABLE 15, NO_SOURCE_YET 2, INSUFFICIENT_HISTORY 2;
the rows account for the difference.

Finding (scope): `portal` is a submodule (gitlink, commit 4d6010234e). Without `--recurse-submodules`, `git grep` reads none of
its 824 tracked files, so the superproject denominator leaves that scope out. Supplementary run inside the submodule,
`git -C portal grep -w -c <TOKEN> -- src/pages/InvestorReporting` over its 824 tracked files: NOT_HELD 9 hits in 3 files;
NOT_APPLICABLE, NO_SOURCE_YET and INSUFFICIENT_HISTORY 0 hits. The supplementary run is not in the superproject count above.

Finding (collision): two of the four tokens already name other things in the estate (above). Neither collision is
exercised by code today, since no code reads `absent_kind`. The CTO should choose whether the kind's spelling carries a
namespace (for example a prefix on the field's value set) or whether the holdings status of IRPT_YCDGEN takes another word.
This proposal does not rename the existing tokens.
