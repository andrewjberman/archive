# THE VERDICT RULE — does anything need Andrew today, COMPUTED from the rows (cell RP-s-4, outcome FWD-1)

Authority: `NFRA_REPORT_PRD.md` manifest row S4 (`FWD-1`: *"One morning read DECLARES whether anything
needs Andrew today"*), `C-AI` part 3, and Andrew's clause (a) (*"I can elect to remediate issues or not
at my discretion, separate from the greater flow"* — no outcome in this PRD requires him, or anyone, to
act). Renders through `STATE_MODEL.md`'s Axis 1/Axis 2 vocabulary and consumes `ROW_STRUCTURE.md`'s
per-row `worse | better | unchanged` delta directly — this cell mints no new vocabulary of its own.

## 0. `C-AI` part 3, the spine

**"A VERDICT IS COMPUTED, NEVER GENERATED. A model may render it in better English; it may not decide
it."** The rule below is a deterministic function over already-computed per-row fields
(`STATE_MODEL.md`'s Axis 1/Axis 2, `ROW_STRUCTURE.md`'s delta). No step asks a model to judge, weigh, or
interpret anything. A model MAY write the sentence a reader sees ("Something needs your attention
today: ..."); it never decides which word — `NOTHING` or `SOMETHING` — that sentence uses.

## 1. THE RULE

```
NEEDS-ANDREW today  IFF  (there exists a row with Axis 1 = CHECKED AND Axis 2 = BREACH)
                     OR   (there exists a row whose delta = worse)

VERDICT = "SOMETHING needs Andrew today"  if NEEDS-ANDREW is true
VERDICT = "NOTHING needs Andrew today"    otherwise
```

Two clauses, both already-computed booleans over fields two prior cells already produce:

- **Clause 1 (a live breach exists):** `Axis 2 = BREACH` is only meaningful where `Axis 1 = CHECKED`
  (`STATE_MODEL.md` §2) — this clause cannot fire on a row nobody looked at, by construction, not by a
  rule this cell adds on top.
- **Clause 2 (something got worse since the last edition):** `ROW_STRUCTURE.md` §2's delta function
  already computes exactly this, per row, independently of every other row. This is precisely the
  mechanism `ROW_STRUCTURE.md` was built for — *"so a problem that broke overnight does not look like
  one standing for a month"* — reused here rather than re-derived.

**Why a row that is `INERT`, `BLIND`, `DENY-BY-DESIGN`, `UNCHECKED` or `COARSE`, UNCHANGED since the
last edition, never trips this rule on its own:** none of those five values carries an Axis 2 value at
all (clause 1 cannot fire), and an unchanged row's delta is `unchanged` by definition (clause 2 cannot
fire). A permanent, already-accepted, non-degrading condition — the Website security row rendering
`DENY-BY-DESIGN` forever, per `C-WEBSITE-BLIND` — is exactly this shape, and correctly never re-trips
"something needs you" on its account alone, every single morning, forever. **It is not hidden — it
still renders on its own row, per `STATE_MODEL.md` — it simply is not what makes the TOP-LINE VERDICT
say `SOMETHING`.**

## 2. THE RULE CAN RETURN "SOMETHING" — worked, on a REAL row from this project

`ALERT_DELIVERY.md` §4 (`RP-s-6`, this same worker) already established, live: `opal-infrastructure-alerts`
renders **`CHECKED` / `BREACH`** — its sole confirmed subscriber is an SMS endpoint sitting in the SNS
sandbox with status `Pending`, so the topic reaches nobody despite showing "1 confirmed subscription."

**Applying the rule:** clause 1 (`∃` row `CHECKED`+`BREACH`) is satisfied by this row alone. **VERDICT =
"SOMETHING needs Andrew today."** Checkable by any reader with no knowledge of how this rule is
computed: open `ALERT_DELIVERY.md`, find the row, confirm it reads `CHECKED`/`BREACH`, and the verdict
follows without needing to trust this document's own narration of it.

## 3. THE RULE CAN RETURN "NOTHING" — worked, on a labelled HYPOTHETICAL morning

**FWD-1's own bar: at least one morning where the verdict was correctly `NOTHING`, because a verdict
that is always `SOMETHING` reproduces brief F1's defect in new words** — the current report's subject
line read the same alarming value on every instance in the measured window, and a signal that cannot
vary carries no information however true each instance is. No live daily edition of this report exists
yet to draw a real "nothing" morning from (every `RP-s-*` cell in this decomposition builds the report's
LAW, not its running generator), so this section is explicitly a **HYPOTHETICAL, labelled as such**,
built to demonstrate the rule is structurally CAPABLE of the negative, not to claim a real day already
produced one:

| Row (illustrative) | Axis 1 | Axis 2 | Delta |
|---|---|---|---|
| Website security | `DENY-BY-DESIGN` | — | `unchanged` |
| Blocked-address sentinel | `CHECKED` | `OK` | `unchanged` |
| `opal-login-abuse-alerts` | `INERT` | — | `unchanged` |
| `comp` | `CHECKED` | `OK` | `unchanged` |
| `opal-infrastructure-alerts` (repaired) | `CHECKED` | `OK` | `better` |

**Applying the rule:** no row is `CHECKED`+`BREACH`; no row's delta is `worse` (one is `better`, the
rest `unchanged`). **VERDICT = "NOTHING needs Andrew today."** The one row that improved (`better`) does
not itself trip the rule — only `worse` does — which is correct: an improvement is good news, not a
reason to say something needs attention.

**This table is a demonstration fixture, stated as one, not a claim about any calendar date.** The
mechanism it exercises — clause 1 and clause 2 over real field values — is identical to §2's; only the
input rows differ.

## 4. PURELY DECLARATIVE — no acknowledgement, no escalation, no required response

**The verdict is a statement of fact, never a request.** It carries no reply field, no "acknowledge"
button, no SLA, no escalation path, and no implication that Andrew (or anyone) must act on it today or
any day. Andrew's own clause (a) is verbatim: *"I can elect to remediate issues or not at my discretion,
separate from the greater flow."* **A verdict that quietly expects a response makes Andrew the
acceptance instrument for this report — exactly the defect `FWD-1`'s declarative re-cut exists to
remove.** Concretely, this rule and this document:

- Do not open, assign, or track a ticket, case, or follow-up of any kind.
- Do not name a deadline, an SLA, or a "must be resolved by" date.
- Do not change meaning based on whether Andrew has previously seen or acted on a given row — the SAME
  unresolved `opal-infrastructure-alerts` breach in §2 would render `SOMETHING` again tomorrow if still
  unrepaired, not because the report is nagging, but because it remains a true, current, `CHECKED`/
  `BREACH` fact — and it would stop rendering `SOMETHING` on its account the day it is repaired
  (`delta` no longer `worse`, `Axis 2` no longer `BREACH`), exactly as §3 shows.

## 5. What this document does NOT do

- Does not compute a live verdict for any real calendar date — no report generator exists yet to run
  this rule against (every cell in this decomposition builds law, not the running artifact); §2 cites a
  real row's CURRENT state from an already-built sibling deliverable, and §3 is an explicitly labelled
  hypothetical.
- Does not add a third clause, a severity weighting, or a model-judged "how urgent is this" score — `C-AI`
  part 3 forbids a model from deciding the verdict, and a weighting scheme is a decision, not a fact.
- Does not build, propose, or imply an acknowledgement/escalation mechanism of any kind (§4).
