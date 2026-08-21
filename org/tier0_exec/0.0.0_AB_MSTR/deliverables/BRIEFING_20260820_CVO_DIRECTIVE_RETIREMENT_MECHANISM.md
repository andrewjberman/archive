# BRIEFING → 3.0.0_SA_CVO — a COMPILED directive-retirement mechanism (Andrew-direct commission)

**From:** 0.0.0_AB_MSTR (register owner) · 2026-08-20 ~1930Z · Andrew-direct at my terminal.
**Ask of CVO, his routing choice verbatim below: ANALYZE AND SUGGEST A MECHANISM — a proposal
back through MSTR/Andrew, not a build.**

## THE COMMISSION, VERBATIM

> Ok let's close out the D8 job, pull it off the directives.yaml, perhaps we can have a
> "directives_retired.yaml" or something where completed work goes, please go figure out how to
> implement that in the missions folder or whereve that lives. Assess the status of that function
> and how it is compiled, what dependenceies it has, and build something out of this nature that
> is equivalently compiled, never hand drawn if we can avoid it. I would recommend handing this
> as a briefing to 3.0.0_SA_CVO and have them analyze and suggest a mechanism to this end.

**Sequencing note (MSTR's read, stated not adjudicated):** D8 is NOT hand-pulled tonight — his
"never hand drawn if we can avoid it" makes D8's removal the mechanism's FIRST EXERCISE. D8 is
the perfect test case: terminal on both boards, sovereign confirmation on the production surface
("they work perfectly", site-Z acceptance record @393211922e), serving on PROD as v2.1.164.

## THE ASSESSED ANATOMY (grounded at my seat this hour — verify, then build on it)

1. **`org/missions/DIRECTIVES.yaml` is a DERIVED VIEW, not a source.** Header tripwire (CTO,
   verbatim): *"recomputable from missions.yaml alone or it is rejected."* Rows carry NO
   paths/attach/holes; members are REFERENCES to sub-group ids / project codes. If a retired
   view needs its own globs, the view is wrong.
2. **The source layer:** `org/tier0/missions.yaml` (attribution index, MSTR-owned) + the
   per-sub-group tree `org/missions/{GROUP}/{SUB}/` with the three-file contract:
   `commits.jsonl` MACHINE (regenerated wholesale from git each emit — never hand-edited),
   `state.yaml` HUMAN (the machine's hard boundary), `execsum.yaml` mixed (prose human,
   anchors machine).
3. **The compiler:** `.tools/comp_missions.py` (`comp-missions emit` / `compile`);
   `org/missions/MISSIONS.md` is an explicit BUILD ARTIFACT; a post-commit refresh hook exists
   (`.tools/git-hooks/missions-refresh-post-commit.sh`). The compile pattern to be "equivalently
   compiled" against is THIS one.
4. **The register's constitutional line, load-bearing for your design:** *THE MACHINE CANNOT
   WRITE A STANCE* — activity is machine-derived from git; DECIDED/BUILT/SERVING/frontier are
   human-asserted with `as_of` + TTL, and aged judgments are LABELED (`STALE-DECLARED`), never
   deleted. "This directive is COMPLETE" is a judgment of the same kind — expect the FACT of
   retirement to be a human/sovereign assertion and the VIEW of it to be machine-compiled.
5. **Consumers of DIRECTIVES.yaml (the dependency set):** ZERO code parsers found (comp-find
   sweep this hour — no .py/.sh reads it). Its readers are AGENTS AND LAW: LD-0428 makes it the
   device boundary + ownership map + shared registry (a ~Z seat works only SITEZ-placed rows);
   the COO/CTO boards read stances; sovereign rulings event-refresh stance cells (D2 today
   @LD-0429). So the retirement mechanism's real dependency is the READING PROTOCOL: a retired
   row must stop reading as live work everywhere agents consult placements, without breaking
   LD-0428's boundary semantics or erasing the record.

## DESIGN QUESTIONS YOUR PROPOSAL SHOULD ANSWER (framing, not prescription)

- **What is the SOURCE of the "completed" fact?** Candidates to weigh: a sovereign word recorded
  (D8's case), project-registry close states (`org/projects/*.json` status), both-board terminal
  reads. Per anatomy point 4, the fact looks human-asserted-with-citation; the compile derives
  the view from it. Name the field, its home, and its writer.
- **One file or a status axis?** His sketch is `directives_retired.yaml` (a sibling home);
  the alternative is a `status`/lifecycle field on the row with the views compiled either way.
  **Rule 24 binds this choice as a schema act (the widened form — adoption/values included), and
  the freshly ratified Lifecycle_Stage enum (EMERGING/ACTIVE/WINDING_DOWN/DISSOLVING/DISSOLVED +
  UNASSERTED, rule-bank home) exists as of today** — assess reuse-vs-new under token hygiene
  before any new token is minted; a directive-grain axis beside a vertical-grain enum needs the
  grain postulate answered either way.
- **What compiles it?** The `comp-missions` pattern is the house form (emit/compile, build-
  artifact banner, post-commit hook). "Equivalently compiled, never hand-drawn" = the retired
  view carries the same tripwire: recomputable from its source alone.
- **What does retirement DO to LD-0428 reads?** A retired SITEZ row is no longer that fabric's
  work — but the boundary law must not lose it as HISTORY (the shared-registry half of his
  DIRECTIVES rationale). Label-not-delete is the register's own precedent.
- **TTL/stability:** does a retired row's stance freeze (no TTL aging on a closed judgment), per
  the closed-period-immutable pattern in the estate's dormancy law?

## WHAT COMES BACK

Your analysis + a proposed mechanism (schema, source-of-fact, compiler leg, first-exercise plan
for D8) routed to MSTR; Andrew rules; the build lands per its Rule-24 record + owner gates
(compiler changes are an 0.8.0-class build row COO cuts; the register files are MSTR-owned).
Not urgent by his word beyond "let's close out D8" — treat D8's pull as the acceptance test of
whatever you propose.
