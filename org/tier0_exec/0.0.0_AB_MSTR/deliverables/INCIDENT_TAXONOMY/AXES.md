# THE CLASSIFICATION SCHEME — 9 axes

    author: 0.0.0_AB_MSTR~Z · 2026-07-29
    use:    every per-document taxonomy in this directory classifies on these axes.
            Cited by code (E1, M5, D2...) in the per-document tables.

Derived from distinctions the corpus itself draws. **Axis 4 (MECHANISM) is the load-bearing one** —
it is the only axis on which the corpus has no existing organisation, and it is where the redundancy
lives.

---

## AXIS 1 — EPISTEMIC TYPE (what wrong belief was produced)

| code | type | definition |
|---|---|---|
| **E1** | FALSE-CLEAN | green/pass/zero over a real defect. *Green is the shape a missing observation takes.* |
| **E2** | FALSE-ALARM | red over a healthy system. Rarer; its remedy is destructive. |
| **E3** | WRONG-VALUE | right shape, right type, wrong content. **No failure channel.** |
| **E4** | WRONG-OBJECT | measurement rigorous, target wrong. |
| **E5** | WRONG-GRAIN | conclusion at a finer grain than any input supports. |
| **E6** | STALE-TRUE | was true; the ground moved. Argues persuasively for the harm it now causes. |
| **E7** | OVER-CLAIM | conclusion broader than evidence; the next reader reasons from the premise. |
| **E8** | UNFALSIFIABLE | no derivation exists — can never be found wrong, only unexplained. |

## AXIS 2 — SURFACE (where it lived)

`S1` data pipeline · `S2` IAM/policy · `S3` shell/argv/path · `S4` comms fabric · `S5` git/VCS ·
`S6` records & law · `S7` comp-tooling · `S8` cloud infra · `S9` scheduling/triggers · `S10` vendor/external

## AXIS 3 — INSTRUMENT FUNCTION (what the lying instrument was FOR)

`F1` census/count · `F2` comparison/diff · `F3` presence-absence probe · `F4` liveness/reachability ·
`F5` provenance/vintage · `F6` authorization · `F7` completion/success signal · `F8` conformance gate ·
`F9` attribution/identity

## AXIS 4 — MECHANISM OF THE LIE ★

| code | mechanism | the question that exposes it |
|---|---|---|
| **M1** | **SHARED DENOMINATOR** — expectation derived from the measured thing | *Where did the EXPECTED side come from, and is that the same authority that defines the population?* |
| **M2** | SHAPE-MATCH, WRONG CONTENT — retrieval broke, returned the right type | *Could this have returned non-zero? Run the positive control.* |
| **M3** | PROXY FOR THE THING — hash/key/partition standing in for content | *What is this a function of that I have not keyed on?* |
| **M4** | COPY DRIFT — a restated literal diverged from its source | *Is this a copy or a read? Enumerate the copies.* |
| **M5** | SCALAR COLLAPSE — a count/rc/bool summarised the population away | *What population did it pass OVER, and can it name what fell outside?* |
| **M6** | AXIS / GRAIN MISMATCH — sampled an axis the defect does not live on | *State the grain of every input and of the conclusion.* |
| **M7** | SELF-REPORT AS POINTER — the subject chose the target | *Did I establish the input from the CALLER's side?* |
| **M8** | TEXT vs SEMANTICS — mention scored as use (grep AND unresolved AST) | *Does it READ the value, or merely contain the string?* |
| **M9** | DESIRED vs APPLIED — config read used for a behavioural claim | *Did I exercise the path that fails if the claim is false?* |
| **M10** | UNREACHED BRANCH — the exercise never entered the governed domain | *Did my input actually reach the branch the claim is about?* |
| **M11** | TAUTOLOGY — both sides of a check are the same computation | *What would have to happen for these two sides to disagree?* |
| **M12** | BORROWED SENSITIVITY — works only while a human keeps doing something | *What has to keep happening, by a person, for this to keep working?* |
| **M13** | POLARITY / NAMING INVERSION — the label asserts the opposite of the behaviour | *Does the name describe what its PRESENCE DOES?* |
| **M14** | PROSE-AS-CONTROL — the finding's only carrier is text nobody must read | *Can this fail? What stops on it?* |

## AXIS 5 — DETECTION MODE (how it was actually caught)

`D1` a designed control fired · `D2` positive control / mutant / ablation · `D3` arithmetic or
expectation mismatch · `D4` somebody read the thing · `D5` sovereign (Andrew) caught it ·
`D6` taste / accident · `D7` not caught in-window (surfaced later, or still open)

## AXIS 6 — FAILURE DIRECTION

`X-CLEAN` fails toward PASS (silent, compounds) · `X-LOUD` fails toward FAIL (self-correcting) ·
`X-DESTRUCTIVE` the remedy itself causes harm

## AXIS 7 — REMEDY SHAPE

`R1` gate · `R2` tool fix · `R3` prose/doctrine only · `R4` removed the need · `R5` named residual

## AXIS 8 — RECURRENCE

`N0` novel · `Nn` nth known instance · **`N-SELF`** recurred *against its own rule* — violated by its
own author, or inside the document that states it

## AXIS 9 — AUTHOR PROXIMITY

`A-SELF` self-caught · `A-PEER` peer-caught · `A-RULE` caught by a control the author did not control ·
`A-SOV` sovereign

---

## Scope note, stated once and inherited by every file here

These taxonomies classify **what is written down**. That is not a census of what happened. The corpus
itself supplies the caveat (`A_VALUE_MUST_CARRY_ITS_CLAIM`, Corollary 4): *"only the loud ones scar …
historical incidence is UNKNOWABLE; never quote an observed count as a rate."* Every count in this
directory is a **floor with an unknown ceiling**.
