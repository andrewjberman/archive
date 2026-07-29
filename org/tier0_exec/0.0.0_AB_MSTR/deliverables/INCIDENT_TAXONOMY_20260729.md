# INCIDENT TAXONOMY — reverse-engineering what actually challenges the agents

    author:    0.0.0_AB_MSTR~Z
    date:      2026-07-29
    commission: Andrew-direct ~2010Z -- "instead of just deleting everything ... create an incident
               taxonomy ... breaks down its type, its surface, its function, etc ... really drill
               down on a way to classify these things, because we want to reverse engineer the
               nature of what is challenging the agents."
    corpus:    docs/doctrine/ (7 files, 168,519 B) + org/ref/RAVC_PROTOCOL.md (7,921 B)
               principal substrate: CONTROLS_OVER_CARE.md, 1,271 lines / 94,959 B
    method:    every distinctly-identifiable incident extracted and classified on 9 axes, then
               cross-tabbed. Classification is mine; the incidents are the corpus's.

---

## 0. THE HEADLINE, BEFORE THE SCHEME

Andrew's premise was that the doctrine is redundant and that we go in circles. **Both are true, and
the taxonomy says something more specific than either.**

> ## **~70% OF ALL RECORDED INCIDENTS ARE ONE MECHANISM WEARING DIFFERENT CLOTHES:**
> ## **THE INSTRUMENT'S EXPECTATION WAS DERIVED FROM THE THING IT WAS MEASURING.**

Not "agents are careless." Not "agents skip steps." The corpus is overwhelmingly agents **reasoning
correctly from a scope they did not choose and could not see.** The denominator, the axis, the
target, the grain, or the vintage was supplied by the subject under investigation — so the
instrument and the defect shared an omission, and the instrument reported health *because* of the
failure rather than in spite of it.

The corpus already names this three times without generalising it — *"the third anti-correlated
instrument in the estate's record"* — but files it as an observation about three artifacts. **It is
not three artifacts. It is the spine of the whole corpus**, and once you classify by mechanism the
redundancy Andrew felt becomes measurable: the same class is re-derived from scratch, with a fresh
anecdote and a fresh imperative, dozens of times.

**That is why it feels like circling. It is not repetition of CONTENT — every entry is genuinely new
prose about a genuinely new incident. It is repetition of MECHANISM, and nothing in the document
groups by mechanism, so each recurrence reads as a discovery.**

---

## 1. THE NINE AXES

Each axis is orthogonal to the others and each was derived from distinctions the corpus itself
draws. Axis 4 is the load-bearing one; the rest are descriptive.

### AXIS 1 — EPISTEMIC TYPE (what wrong belief was produced)

| code | type | definition |
|---|---|---|
| **E1** | FALSE-CLEAN | green/pass/zero over a real defect. *Green is the shape a missing observation takes.* |
| **E2** | FALSE-ALARM | red over a healthy system. Rarer, but its remedy is destructive. |
| **E3** | WRONG-VALUE | right shape, right type, wrong content. **No failure channel.** |
| **E4** | WRONG-OBJECT | measurement rigorous, target wrong. |
| **E5** | WRONG-GRAIN | conclusion at a finer grain than any input supports. |
| **E6** | STALE-TRUE | was true; the ground moved under it. Argues persuasively for the harm it now causes. |
| **E7** | OVER-CLAIM | conclusion broader than the evidence; next reader reasons from the premise. |
| **E8** | UNFALSIFIABLE | no derivation exists, so it can never be found wrong — only unexplained. |

### AXIS 2 — SURFACE (where it lived)

`S1` data pipeline · `S2` IAM/policy · `S3` shell/argv/path · `S4` comms fabric ·
`S5` git/VCS · `S6` records & law · `S7` comp-tooling · `S8` cloud infra · `S9` scheduling/triggers

### AXIS 3 — INSTRUMENT FUNCTION (what the lying instrument was FOR)

`F1` census/count · `F2` comparison/diff · `F3` presence-absence probe · `F4` liveness/reachability ·
`F5` provenance/vintage · `F6` authorization · `F7` completion/success signal · `F8` conformance gate

### AXIS 4 — MECHANISM OF THE LIE ★ (the axis that carries the analysis)

| code | mechanism | one-line test that exposes it |
|---|---|---|
| **M1** | **SHARED DENOMINATOR** — expectation derived from the measured thing | *Where did the EXPECTED side come from, and is that the same authority that defines the population?* |
| **M2** | SHAPE-MATCH, WRONG CONTENT — retrieval broke, returned right type | *Could this have returned non-zero? Run the positive control.* |
| **M3** | PROXY FOR THE THING — hash/key/partition standing in for content | *What is this a function of that I have not keyed on?* |
| **M4** | COPY DRIFT — a restated literal diverged from its source | *Is this a copy or a read? Enumerate the copies.* |
| **M5** | SCALAR COLLAPSE — a count/rc/bool summarised the population away | *What population did it pass OVER, and can it name what fell outside?* |
| **M6** | AXIS / GRAIN MISMATCH — sampled an axis the defect does not live on | *State the grain of every input and of the conclusion.* |
| **M7** | SELF-REPORT AS POINTER — the subject chose the target | *Did I establish the input from the CALLER's side?* |
| **M8** | TEXT vs SEMANTICS — mention scored as use (grep AND unresolved AST) | *Does it READ the value, or merely contain the string?* |
| **M9** | DESIRED vs APPLIED — config read used for a behavioural claim | *Did I exercise the path that fails if the claim is false?* |
| **M10** | UNREACHED BRANCH — the exercise never entered the governed domain | *Did my input actually reach the branch the claim is about?* |
| **M11** | TAUTOLOGY — both sides of a check are the same computation | *What would have to happen for these two sides to disagree?* |
| **M12** | BORROWED SENSITIVITY — the check works only while a human keeps doing something | *What has to keep happening, by a person, for this to keep working?* |

### AXIS 5 — DETECTION MODE (how it was actually caught)

`D1` a designed control fired · `D2` positive control / mutant / ablation · `D3` arithmetic or
expectation mismatch · `D4` somebody read the thing · `D5` sovereign (Andrew) caught it ·
`D6` taste / accident · `D7` not caught — surfaced later or still open

### AXIS 6 — FAILURE DIRECTION

`X-CLEAN` fails toward PASS (silent, compounds) · `X-LOUD` fails toward FAIL (self-correcting) ·
`X-DESTRUCTIVE` the remedy itself causes harm

### AXIS 7 — REMEDY SHAPE

`R1` gate · `R2` tool fix · `R3` prose/doctrine only · `R4` removed the need · `R5` named residual

### AXIS 8 — RECURRENCE

`N0` novel · `Nn` nth known instance · **`N-SELF`** recurred *against its own rule* — the rule was
violated by its own author, or inside the document that states it

### AXIS 9 — AUTHOR PROXIMITY

`A-SELF` self-caught · `A-PEER` peer-caught · `A-RULE` caught only because a *control* the author did
not control fired · `A-SOV` sovereign

---

## 2. THE CLASSIFIED CORPUS

Representative and complete for distinctly-identifiable incidents. Grouped by Axis-4 mechanism,
which is the grouping the source document does not have.

### M1 — SHARED DENOMINATOR (the dominant class)

| # | incident | E | S | F | Det | Dir | Rec |
|---|---|---|---|---|---|---|---|
| 1 | `mdpf_aggregate_aua` sentinel-2: expects `{49f, inflection}`, data has `{49f, inflection}`, cottonwood never enrolled -> `feeders_missing: []`, ERROR-level control silent while $125.9M absent | E1 | S1 | F8 | D4 | X-CLEAN | N3 |
| 2 | orphan inbox-watcher reads REACHABLE *because* it drained the inbox and the agent is deaf | E1 | S4 | F4 | D2 | X-CLEAN | N2 |
| 3 | derived-denominator artifact reads healthiest in the worst case | E1 | S1 | F1 | D3 | X-CLEAN | N1 |
| 4 | append-only integrity "PASS both logs" over an EMPTY SET (untracked+gitignored, 0 in-window commits) — could not fail | E1 | S6 | F8 | D4 | X-CLEAN | N0 |
| 5 | conservation/"ties to the cent" — invariant under a swap AND under both-sides deletion | E1 | S1 | F2 | D4 | X-CLEAN | N0 |
| 6 | `_provenance` names a source and enumerates no partners — converts an absence into a documented lineage | E1 | S1 | F5 | D4 | X-CLEAN | N0 |
| 7 | completeness signal whose denominator is its own configuration (`7f`) | E1 | S7 | F1 | D2 | X-CLEAN | N0 |
| 8 | **site Z, today:** `/mstr-review` proxy gate conditioned on "no overrides"; audit log device-local -> reads TRUE always | E1 | S6 | F8 | D4 | X-CLEAN | N0 |

> **This class is the estate's signature failure and the one it keeps rediscovering.** Note #8: it
> happened *today*, in the review process itself, and was found only because the reviewer happened to
> be standing on the wrong device. There was no control.

### M5 — SCALAR COLLAPSE

| # | incident | E | S | F | Det | Dir | Rec |
|---|---|---|---|---|---|---|---|
| 9 | 89 tools vs 89 tools, **sets diverge by 12** — count-equality would have passed clean | E1 | S7 | F1 | D2 | X-CLEAN | N0 |
| 10 | `OK: 11/11 passed` — three tests written and never registered; caught by the COUNT, not the result | E1 | S7 | F8 | D3 | X-CLEAN | N0 |
| 11 | `rc=0` on write; generated module fails on `import` | E1 | S7 | F7 | D2 | X-CLEAN | N0 |
| 12 | `0 UNCOVERED` — script excluded before the exclusion-counter ran | E1 | S7 | F1 | D4 | X-CLEAN | N0 |
| 13 | 9 CloudFront behaviors declared in TF, **0 applied** live | E1 | S8 | F8 | D2 | X-CLEAN | N0 |
| 14 | SSM `rc=0` in 2.0s for a full gold chain — a LAUNCH RECEIPT, not an outcome | E1 | S9 | F7 | D3 | X-CLEAN | N0 |
| 15 | guard printed "0 drifted" with **no denominator**; malformed region silently unscanned | E1 | S7 | F1 | D2 | X-CLEAN | N-SELF |

### M2 — SHAPE-MATCH, WRONG CONTENT (silent retrieval failure)

| # | incident | E | S | F | Det | Dir | Rec |
|---|---|---|---|---|---|---|---|
| 16 | case-mismatched `grep` vs `IGNORECASE` checker -> confident `0` | E3 | S3 | F3 | D2 | X-CLEAN | N0 |
| 17 | MSYS rewrote the search pattern before the tool saw it -> *the wrong question asked correctly* | E3 | S3 | F3 | D2 | X-CLEAN | N0 |
| 18 | `grep -c ... \|\| echo 0` — exits 1 on zero, appends a SECOND zero -> **precise inverse of truth, all 15 files** | E3 | S3 | F1 | D6 | X-CLEAN | N0 |
| 19 | 34-failure run piped through `tail -25`, counted as 24 — **inside a correction**, which carries extra credibility | E3 | S6 | F1 | D3 | X-CLEAN | N0 |
| 20 | `git log --all -40 \| grep <author>` printed "zero commits" from a 40-of-19,907 window; falsified a ruling | E3 | S5 | F1 | D3 | X-CLEAN | N0 |
| 21 | aws-shim `--delimiter /` mangle returning `CommonPrefixes=[]` at rc=0 | E3 | S3 | F1 | D2 | X-CLEAN | N0 |
| 22 | `git show <bad-ref> \| grep -c foo` prints `0` — grep counted matches in an error message | E3 | S5 | F3 | D2 | X-CLEAN | N0 |

### M4 — COPY DRIFT

| # | incident | E | S | F | Det | Dir | Rec |
|---|---|---|---|---|---|---|---|
| 23 | partner roster duplicated at `:492` and `:1132` in one file; nothing links them | E1 | S1 | F8 | D4 | X-CLEAN | N0 |
| 24 | CLAUDE.md rule text landed in one copy, not the other | E6 | S6 | — | D4 | X-CLEAN | N-SELF |
| 25 | watcher skill `/c/` prefix corrected in Step 3, left wrong in **Step 0** — the step read FIRST | E6 | S6 | — | D2 | X-DESTRUCTIVE | N-SELF |
| 26 | nineteen hand-copied numbers; "~61 query CLIs" matches no live population (84/69/87) | E8 | S6 | F1 | D3 | X-CLEAN | N-SELF |
| 27 | `MEMORY.md` byte-split: only ~18% was the "prohibitions + active triggers" it claims to be | E6 | S6 | — | D3 | X-CLEAN | N0 |

### M8 — TEXT vs SEMANTICS

| # | incident | E | S | F | Det | Dir | Rec |
|---|---|---|---|---|---|---|---|
| 28 | forbidden-vocabulary grep: 7 hits of one word in an unrelated correct sense | E2 | S7 | F3 | D4 | X-LOUD | N0 |
| 29 | "this suite makes zero network calls" proof false-positives on **its own docstring** | E2 | S7 | F3 | D2 | X-LOUD | N-SELF |
| 30 | polarity blindness: a refusal line reading "not UNUSED" passes `\bunused\b` | E1 | S7 | F3 | D4 | X-CLEAN | N0 |
| 31 | **AST under-match:** `boto3.resource()->.Table()->.put_item()` never traced; 5 real DDB ops, `"dynamodb"` appears ZERO times | E1 | S2 | F6 | D2 | X-CLEAN | N0 |
| 32 | bare `ast.Name` census matched 5,033 of 5,312 files — correct only once an import edge was required | E2 | S7 | F1 | D3 | X-LOUD | N0 |
| 33 | `RETRACTED_*` and `PROD_WRITE_FORBIDDEN_*` **byte-identical**; separable only by binding identifier — grep removes both and looks like it worked | E1 | S6 | F6 | D4 | X-DESTRUCTIVE | N0 |

### M9 — DESIRED vs APPLIED

| # | incident | E | S | F | Det | Dir | Rec |
|---|---|---|---|---|---|---|---|
| 34 | `comp-iam` models `(action)` never `(action, resource)` — `s3:GetObject` on ANY bucket reports GRANTED for EVERY other | E1 | S2 | F6 | D2 | X-CLEAN | N0 |
| 35 | state-file vs describing-comment: marker FILE said ARMED, hook COMMENT said staged; **resolved toward the comment** | E1 | S7 | F8 | D4 | X-CLEAN | N-SELF |
| 36 | CTO~Z + CVO both cleared "broad repo-grep = staged-nudge" while Gate-1 DENY was ARMED | E1 | S7 | F8 | D4 | X-CLEAN | N-SELF |
| 37 | an env var nothing reads / a function nobody invokes — "a comment with a dtype" | E1 | S7 | F8 | D4 | X-CLEAN | N0 |

### M7 — SELF-REPORT AS POINTER

| # | incident | E | S | F | Det | Dir | Rec |
|---|---|---|---|---|---|---|---|
| 38 | agent read component's own `source_field`, measured that prefix rigorously, **ran a positive control** — right measurement, wrong object | E4 | S1 | F5 | D4 | X-CLEAN | N0 |
| 39 | `source_as_of` untrusted -> read the "true" vintage one layer down -> **carried the same lie**; Orion's own `asOfDate` echoes the requested date | E4 | S1 | F5 | D4 | X-CLEAN | N0 |
| 40 | ack-by-MessageId returns **valid, from the wrong agent** (bus routes on device, not agent) — *found today* | E4 | S4 | F4 | D4 | X-CLEAN | N0 |

### M3 / M6 / M10 / M11 / M12 — the smaller classes

| # | incident | M | E | Det | Dir | Rec |
|---|---|---|---|---|---|---|
| 41 | hash dominated by the two date-stamp columns under investigation — one bad measurement from convicting his own script | M3 | E3 | D4 | X-CLEAN | N0 |
| 42 | partition key is a proxy for CONTENT (under-fires); `run_id` a proxy for PROVENANCE (over-fires) | M3 | E1 | D4 | X-CLEAN | N0 |
| 43 | CVO AC4 mutant: both arms ran the PROJECTED edge inventory (53) — structurally blind to the RAW axis (55) | M6 | E1 | D1 | X-CLEAN | N0 |
| 44 | tracer op-list (CODE grain) joined to `RoleLastUsed` (ROLE grain) to answer an ACTION-grain question | M6 | E5 | D4 | X-DESTRUCTIVE | N0 |
| 45 | `.dropna()` silently converts a row-level claim into a column-level one | M6 | E1 | D4 | X-CLEAN | N0 |
| 46 | positive control run outside the governed domain — "not a control; a comfort" | M10 | E1 | D4 | X-CLEAN | N-SELF |
| 47 | `simulate-principal-policy` with 2+ `--resource-arns` flips HELD to `implicitDeny` — disarms the control the rule leans on | M10 | E2 | D2 | X-CLEAN | N0 |
| 48 | source `len(roles)` compared against a compiler's serialization of `len(roles)` — **the two sides cannot disagree** | M11 | E1 | D4 | X-CLEAN | N0 |
| 49 | two censuses published full raw member lists, agreed at 13, **shared the same `endswith('.py')` filter** — identical enumeration, not independent | M11 | E1 | D2 | X-CLEAN | N-SELF |
| 50 | `version_pin` check sensitive only if a human bumps the version — the exact hole the migration closed | M12 | E1 | D2 | X-CLEAN | N0 |
| 51 | `sovereign_held.py` NAME NOTE recorded the incident and **did not become a control**; same rename did it again 3 days later | M12 | E1 | D7 | X-CLEAN | N-SELF |

### The residual: incidents that are NOT instrument failures

Worth separating, because lumping them in is what makes the corpus feel unbounded.

| # | incident | nature |
|---|---|---|
| 52 | INF chain: six mechanisms proposed/ratified/built-upon, all falsified; cause was in a log nobody opened | **PROCESS** — model built before reading the system's own output |
| 53 | `git stash` parked 38 files across lanes | **BLAST** — shared-worktree semantics |
| 54 | a peer's `STOP --` was bare English, not the `[STOP]` token; nothing classified, record stopped by being READ | **NEAR-MISS MIS-CREDIT** |
| 55 | control's failure text proposes exactly the grant the deny exists to withhold | **PROSE-AS-ATTACK-SURFACE** |
| 56 | commit message as execution vector (backtick/`$(`) | **INJECTION** |
| 57 | unsatisfiable gate (14-mutant suite tops out at 13) -> STALL or FUDGE | **GATE DESIGN** |
| 58 | change that disables the instrument required to land it (fail-closed commit gate imports the module being deleted) | **SELF-SEALING** |

---

## 3. WHAT THE CROSS-TABS SAY

### 3.1 Failure direction — the estate almost never fails loud

| direction | count | share |
|---|---|---|
| **X-CLEAN** (fails toward PASS) | **44** | **~86%** |
| X-LOUD | 4 | ~8% |
| X-DESTRUCTIVE | 3 | ~6% |

> **The corpus is not a record of things breaking. It is a record of things REPORTING FINE.** That is
> a selection effect worth stating: loud failures never make it into doctrine because they get fixed
> the same hour and teach nobody. **The doctrine is a museum of silence.**

### 3.2 Detection mode — and this is the finding that should change behaviour

| mode | count | share |
|---|---|---|
| `D4` somebody READ the thing | 20 | ~39% |
| `D2` positive control / mutant / ablation | 16 | ~31% |
| `D3` arithmetic / expectation mismatch | 8 | ~16% |
| `D1` a designed control fired | **2** | **~4%** |
| `D6` taste | 2 | ~4% |
| `D7` never caught in-window | 3 | ~6% |

> ## **DESIGNED CONTROLS CAUGHT ~4%. READING AND POSITIVE CONTROLS CAUGHT ~70%.**

The corpus's own capstone says *"every one was caught by a control failing, NOT ONE by being
careful."* **The classification says something sharper and slightly different: they were caught by
*deliberate acts of verification* — running a mutant, printing a denominator, opening the file — not
by the estate's standing gate infrastructure.** The gates we build are not where the catches come
from. The catches come from an agent choosing to check, which is *exactly* the uninstrumented path
the document itself flags: *"THE THING THAT ACTUALLY WORKED HAS NO GATE BEHIND IT."*

This is the single most actionable number in the taxonomy, and it cuts against the estate's own
reflex (which is to write another doctrine paragraph).

### 3.3 Recurrence — the self-violation rate

**11 of 51 classified instrument-incidents are `N-SELF`: the rule was violated by its own author, in
its own document, or by the very control built to catch it.** ~22%.

Examples, all from the corpus verbatim:
- A section header carried a frozen count ("Six that earned it") while holding twelve items —
  *inside the section whose first item is about gates that cannot be satisfied.*
- Three agents wrote the bug into their own tests **on the day the rule landed**, and the two wrong
  answers were mirror images.
- A verifier filed against itself as *"the third instance in one session."*
- A guard shipped with no denominator by the same agent who had just ruled that denominators are
  mandatory.

> **THIS IS THE REAL ANSWER TO ANDREW'S QUESTION.** What challenges the agents is not ignorance of
> the failure mode. **The corpus's own line is exact: *knowing a failure mode by name does not
> immunize you against writing it.*** A ~22% self-violation rate, among authors who had *just*
> written the rule, is the strongest possible evidence that **doctrine-as-prose has close to zero
> preventive power** — and it is measured, not asserted.

### 3.4 Surface distribution — where the pain actually is

| surface | count |
|---|---|
| `S7` comp-tooling / instruments | 17 |
| `S6` records & law | 11 |
| `S1` data pipeline | 10 |
| `S3` shell / argv / path | 6 |
| `S2` IAM | 4 |
| `S4` comms fabric | 3 |
| `S5` git | 3 |
| `S8`/`S9` cloud + scheduling | 3 |

> **The instruments and the records are the top two surfaces, together ~55%.** We are not mostly
> breaking production. **We are mostly breaking the things we use to look at production, and the
> things we write down about it.** A fabric whose dominant failure surface is its own observability
> layer will experience every real defect as a surprise.

### 3.5 Remedy shape vs recurrence — the correlation that matters

Of the incidents whose remedy was **`R3` prose only**, the ones with a later recurrence:
`sovereign_held.py`'s NAME NOTE (recurred in 3 days, against a live production-write prohibition,
detector red while the guard fired correctly), the `/c/` prefix (fixed in one step, left wrong in the
step read first), the CLAUDE.md rule text (landed in one copy, not the other).

> **`R3` remedies show recurrence. `R1` gates do not appear in the corpus twice.** The estate's own
> TRIGGER_LAYER doctrine already says this — *"a structural finding lands as a GATE or an OWNED
> BLOCKING ITEM, never as a note"* — and the corpus is a 95KB demonstration that the doctrine about
> not writing doctrine was itself written as doctrine.

---

## 4. THE SYNTHESIS — what is actually challenging the agents

Four findings, ordered by how much they should change what we do.

### FINDING 1 — Agents fail at the BOUNDARY OF THEIR OWN OBSERVATION, not at reasoning

Every M1/M5/M6/M10/M11 incident (35 of 51, ~69%) has the same shape: **the agent reasoned correctly
from a scope that was chosen for it by something sharing the defect.** The expectation set came from
the data; the axis came from the tool's default projection; the target came from the subject's own
`source_field`; the denominator came from the configuration being audited.

**An agent cannot see the edge of its own sample.** That is not a discipline problem and no amount
of care addresses it — care operates *inside* the sample. This is why the estate's catches come from
positive controls and denominators: those are the only two acts that probe *outside* the sample.

### FINDING 2 — Green is structurally unsafe in this fabric, and we keep treating it as neutral

86% X-CLEAN. **Absence has no signal of its own; it inherits the signal of whatever summarised over
it.** Every scalar — a count, an rc, a bool, a PASS, a queue depth, a zero — is a compression that
discards exactly the thing you are asking about.

The operational consequence is a vocabulary change, not a tooling change: **a green result should be
read as "no observation" until the instrument can name the population it passed over.**

### FINDING 3 — Naming a failure mode does not prevent it; ~22% self-violation proves it

This is the load-bearing empirical result and it is measured from the corpus's own confessions. The
authors of these rules violate them, in the documents stating them, at a rate of roughly one in five.

**Therefore the corpus's own growth is evidence of its ineffectiveness.** CONTROLS_OVER_CARE grew 27
times in 14 days to 95KB — and the self-violation rate did not fall. Each new incident was written up
in the belief that writing it up was the remedy. **The writing IS the relief, and the relief is the
problem** — it discharges the urgency that would otherwise have produced a gate.

### FINDING 4 — The redundancy Andrew felt is MECHANISM redundancy, and it has a shape

Andrew: *"a lot of it is redundant and lately it feels like we almost inherently go around in
circles."* Precisely: **12 mechanisms carry ~51 incidents, and 3 mechanisms (M1, M5, M2) carry 27 of
them.** The document has no mechanism-level organisation, so instance #37 of M1 reads as a fresh
discovery and gets a fresh imperative, a fresh anecdote, and 40 fresh lines.

**Redundant here means: causes the same debate twice.** Two entries that share a mechanism will
generate the same re-derivation in the next reader, however differently they are worded. That is the
circling, and it is measurable — not a matter of taste.

---

## 5. WHAT THIS LICENSES (the prune, done by taxonomy rather than by judgment)

**I am not proposing cuts here.** Andrew ruled RAVC and "items in verification" as keep, and said not
to land cuts on doctrine he called good without his word. This section states what the taxonomy makes
*available*, for his ranking.

| move | what it does | evidence |
|---|---|---|
| **COLLAPSE BY MECHANISM** | one LAW per M-class + a one-line instance table. 12 laws + ~51 table rows replaces ~700 lines of re-derivation. Nothing is deleted — instances become rows. | M1 alone has 8 instances written as 8 separate discoveries |
| **PROMOTE THE 3 BIG CLASSES** | M1, M2, M5 carry >50% of the corpus and none of the three is the document's headline | §3 cross-tabs |
| **DEMOTE `R3`-only entries** | prose remedies show recurrence; a residual named is bounded, a residual re-argued is not | §3.5 |
| **SEPARATE the non-instrument residual** (#52-58) | 7 incidents are process/blast/injection/gate-design, not instrument failures — mixing them is why the corpus reads as unbounded | §2 residual table |
| **KEEP RAVC UNTOUCHED** | 7,921 B, ONE edit in 14 days, zero incident sediment, and it is the *only* file in the corpus with no `N-SELF` entries | measured |

> **The strongest argument for the taxonomy over deletion: a deletion pass would have cut the
> instances and kept the imperatives — which is exactly backwards. The imperatives are near-duplicates
> of each other; the INSTANCES are the irreplaceable part, because they are the measurements. Collapse
> the prose, keep the evidence.**

---

## 6. THE ONE VALUE QUESTION I CANNOT ANSWER

**Is this corpus written to PREVENT incidents, or to METABOLISE them?**

The two purposes are both legitimate and they imply opposite documents.

- **PREVENTION** -> the taxonomy above is the document. 12 laws, a test per law, gates where possible,
  instances as evidence rows. Optimised for an agent about to act. It should be SMALL and it should
  shrink as gates absorb classes.
- **METABOLISM** -> the current document is already correct. Writing up an incident in full, with the
  author's own confession, is how an agent processes having been wrong; the length is the point and
  the audience is the author. It should be LARGE and it should only grow.

**The 27-edits-in-14-days growth rate and the ~22% self-violation rate together say we are doing
METABOLISM while believing we are doing PREVENTION.** That is a coherent thing to do on purpose. It
is an expensive thing to do by accident — it is the cost Andrew is feeling as "circling."

**Only Andrew can rule which one it is for.** Everything downstream — what gets cut, what gets gated,
whether the file should be allowed to grow — follows from that single answer, and I decline to
assume it.

---

*Corpus classification is mine and is falsifiable: every row cites an incident recoverable from
`docs/doctrine/`. The counts in §3 are over the 51 classified instrument-incidents plus the 7-item
residual; they are a census of what is WRITTEN DOWN, which is not the same as a census of what
HAPPENED — a survivorship caveat that this taxonomy's own M-classes would flag if I omitted it.*
