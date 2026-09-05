# TO-OS-s-13 result -- the composition contract

**Produced by `0.9.0_WK_NFRA_OUTSET~3`**, worktree `C:/tmp/wk-OUTSET-3`, branch `wk-OUTSET-3`.
**Tree vintage for every measurement below:** HEAD `f2ef16d70a`.
**TO:** `org/missions/D11/NFRA/NFRA_OUTSET/task-orders/NFRA_OUTSET.TO-OS-s-13.the-composition-contract.md`
· **verb:** record · **outcome_ref:** FWD-6 · **cell:** OS-s-13 · **depends_on:** OS-s-9

⛔ **BOTH CRITERIA ARE `judgment="true"`.** Evidence and a reasoned reading are recorded; **no verdict
is written on either.** `3.0.0_SA_CVO` grades them at L9.

## 0. The headline

**The contract exists, at `docs/architecture/NFRA_OUTSET_COMPOSITION_CONTRACT.md`, and the test of it
PASSES in the sense that matters: "converging AND hot AND undeployed" IS expressible without a new
tool, and I ran it rather than argued it.** All three limbs answered on one shared key -- the
repo-root-relative path -- in ~10.5 s total, every call bounded.

**And the single most important thing this cell found is a correction to my own earlier work.**
`NFRA_OUTSET-W3-S9` and the `OS-s-12` census row -- both mine -- recorded `comp-pipescript` as
`FAILED` and `budget=not-accepted`. **Both are wrong.** `--budget` is on the `deployed` **subcommand**
parser, not the top-level parser I probed, and with it the tool answers. That is the "counted the
wrong thing perfectly" failure, committed by me, inside the project that exists to name it. Filed as
`NFRA_OUTSET-W3-S10`; carried in the contract's own body at s.1.2, not quietly relied upon.

## 1. The manifest evidence, re-grounded before building on it

The cell's premise: *"comp-heat's header states ONE hop of the composition; nothing states the rest."*
**Confirmed, with a control against the false-zero modes on record.**

- **The one stated hop**, `.tools/comp-heat@f2ef16d70a:34-36`, quoted verbatim in the contract's s.0.
  It is also emitted at **run time** as the last line of `comp-heat drift` -- so it is a live clause,
  not only a source comment.
- **"Nothing states the rest"**: a repo-wide search for `composition contract` returned **3 files** --
  this project's PRD, its brief, and `docs/architecture/ADVI_FRONTEND_CORRECTNESS.md:126`, whose hit
  is the substring inside *"de-composition contract"* and is a different sense. **A non-zero result
  in the same shape is the control** that the search was live rather than a false zero.
  `docs/architecture/` holds **469** files; none carries this subject by name.
- **What exists and is not duplicated:** `org/modules/graph/comp-output-contracts.yaml` is the
  **per-tool output** contract (coverage line, plane/vintage header, exit-code semantics,
  gate-enforced complete). It governs what ONE answer carries; this contract governs how TWO answers
  JOIN. Different axis -- cited, not replaced. (Build ladder rung 2 checked before writing.)

## 2. O13-AC1 -- the document (evidence, NO verdict)

**Home:** `docs/architecture/NFRA_OUTSET_COMPOSITION_CONTRACT.md` -- one file, inside my `<paths>`.
**Owner:** `1.0.0_SA_CTO`, and the claim is recorded as **DECLARED, not ACCEPTED**. Basis: the only
pre-existing clause of this composition is comp-heat's header, whose author line reads *"Author:
1.0.0_SA_CTO (comp-tool registry)"*, and this document generalises exactly that clause. **A worker
cannot confer ownership on a seat that has not accepted it**, so the field carries its own status
rather than asserting an owner as fact; `2.0.0_SA_COO`/`3.0.0_SA_CVO` may reassign without the
document being wrong. The **home** is not in doubt.

**All four hops covered, each measured live and bounded at `f2ef16d70a`:**

| hop | instrument | key | domain | bound | measured |
|---|---|---|---|---|---|
| LOCAL->GIT | `comp-heat drift` | repo path | whole repo (30,659) | `--budget` | rc=0, 0.5 s |
| GIT->DEPLOY | `comp-pipescript deployed` (+`comp-freshness`) | repo path or script id | **DS corpus (554)** | `--budget` **on subcommand** | rc=0, 8.4 s |
| co-evolution | `comp-fedobs coevolution` | repo path **pair** | whole repo, served | **none** | rc=0, 2.9 s |
| pairwise verdict | `comp-heat compare` | repo path **pair** | whole repo | `--budget` | rc=0, 1.0 s |

**The finding that makes the contract useful: all four hops share the repo-root-relative path as
their key.** That was not written down anywhere before.

Deciding output lines, verbatim:

```
comp-heat drift     -> WITHIN BUDGET: scanned 1 of 1 files; budget: 15 s (flag), used 0.25 s
                       (LOCAL->GIT layer; the GIT->DEPLOY hop = `comp-pipescript deployed` + `comp-freshness`)
comp-heat compare   -> VERDICT: DIVERGING (<0.8x=CONVERGING, >1.25x=DIVERGING, else PARALLEL)
                       .tools/comp-heat: band=HOT ... org/modules/heatmap/heat_map.py: band=COLD
comp-fedobs coevol. -> [SERVED vintage (NOT live) as-of 2026-09-05T04:30:38Z marker_head=f437d60b3c65]
comp-freshness      -> self-test rc=0, all arms PASS
```

## 3. O13-AC2 -- the test of the contract (evidence, NO verdict)

**Expressible without a new tool. Two calls, three shown for clarity, one shared key, ~10.5 s.**

```sh
P=data/black_diamond/scripts/gold/A_00.accounts_dimension.py
Q=data/black_diamond/scripts/gold/B_00.canonical_holdings.py

comp-heat compare "$P" "$Q" --windows 3 --window-days 30 --budget 20   # CONVERGING? and HOT? in ONE call
comp-heat freshness "$P" --top 2 --budget 20                            # HOT? at a path grain alone
comp-pipescript deployed "$P" --budget 25                               # UNDEPLOYED? same key

# TRUE iff VERDICT==CONVERGING AND band==HOT AND verdict in {STALE, MISSING_ON_S3}
```

| limb | result | rc |
|---|---|---|
| converging? | `VERDICT: DIVERGING` | 0 (1.0 s) |
| hot? | `bands: hot=0 warm=0 cold=1` -> COLD | 0 (1.1 s) |
| undeployed? | `[bd-gold] A_00 MATCH` -> deployed | 0 (8.4 s) |

**The conjunction evaluates FALSE for this path.** The criterion asks for the EXPRESSION; the
expression exists, runs bounded, and returns a decidable answer on every limb. `comp-heat compare`
carries the verdict **and both bands in one answer**, which is what makes it two calls rather than three.

**Three conditions on it, recorded in the contract s.2.1:**

1. **Domain intersection.** Limbs 1-2 hold over 30,659 tracked files; limb 3 over **554** -- **1.8%**.
   *"converging AND hot"* is estate-wide; *"AND undeployed"* is not. comp-heat's header says *"Chain
   them for the full local->git->deploy view"*; that is true **inside** the DS corpus and the header
   names no domain. Filed as `NFRA_OUTSET-W3-S11`.
2. **The bound is mandatory on limb 3, not optional.** Unbounded and unscoped, `deployed` returned no
   answer at 9 s or 75 s. Bounded, it always terminates -- answering or cutting cleanly at rc=4.
3. **Three rc values are not interchangeable on limb 3.** `rc=0` a decided verdict; `rc=4` a PREFIX
   carrying **no** verdict; `rc=2` REFUSED, out of domain. Collapsing 4 or 2 into "not undeployed" is
   the false-clean the tool's own refusal text exists to prevent.

**The domain boundary is enforced, not silent** -- which is why W3-S11 is INERT:

```
comp-pipescript deployed .tools/comp-heat --budget 25 -> rc=2
  REFUSED (rc=2): --pipeline/-p is now REQUIRED -- this tool previously defaulted to bd-gold and
  could return a clean zero for a script living in another tree (Andrew-direct 2026-07-30).
  NO GUESS IS MADE.  Script 'comp-heat' not found under data/*/scripts/
```

## 4. The correction to my own prior work

| | recorded before (mine) | measured now |
|---|---|---|
| `--budget` | `not-accepted` | **accepted on the `deployed` subcommand**: `[--budget N] [--cursor UNIT]` |
| answer | `FAILED`, no answer at 9 s or 75 s | **rc=0 in 8.4 s** with a real `MATCH` row and `ANSWER-STATE: PRESENT_WITH_ZERO_RESULTS` |
| Rule T | absent | **full**: `BUDGET REACHED ... scanned 0 of 1 s3_head_object ... a PREFIX, not the answer`, `STATE: NOT-DECIDABLE`, `ANSWER-STATE: PARTIAL_OR_BLIND`, `DEFERRED: 1 of 1` |

**What survives from W3-S9, scoped to the clause actually measured:** the *unbounded, unscoped*
no-argument sweep really did return no answer at 9 s or 75 s. That timing clause stands. **The
generalisation from it to the tool's capability is what was wrong**, and the retraction is scoped to
the capability clause rather than thrown over the whole row.

**Why this is ARMED:** `.tools/tests/test_os12_census.py` is committed at `74a16082ad` and will keep
emitting `comp-pipescript 124 FAILED ... not-accepted` on every run -- a confident false negative
printed beside a correct denominator. **I did not fix it:** `.tools/tests/` is outside this order's
`<paths>`, and editing it here is exactly the workaround BOUNDS forbids. Routed to `2.0.0_SA_COO`.

## 5. Where the chain does not close -- recorded open, not fixed

G1 `comp-fedobs` accepts no `--budget` · G2 the publication seam is built and **switched off**
(`ESTATE_OUTSET_SEAM_PREFIX` unset; nothing publishes) · G3 the runner's IAM **cannot reach** any
seam location (APPLIED-plane read) · G4 no producer cadence for git-history-shaped tools · G5
co-evolution's second implementation **cannot be retired** (resource-grain vs agent-type-grain) ·
G6 `comp-freshness` does not join the path key.

**G2+G3+G4 compose into one standing fact:** the seam that would let the runner consume outset-tool
answers instead of re-deriving them is **built, correct and inert**. Until all three land, this
composition is available **to an agent at a terminal** and **not** to the runner.

**G2, G3, G4 are `0.9.0_WK_NFRA_OUTSET~1`'s measurements and G5 is `0.9.0_WK_NFRA_OUTSET~2`'s, cited
as theirs and not re-derived here.** In particular OS-s-10's careful distinction is preserved
verbatim in spirit: *"cannot be produced" is not what was measured; "is not produced, and no cell
owns producing it" is.*

## 6. What would have changed the reading

- If `comp-pipescript deployed` had refused `--budget`, or had still not answered when bounded and
  scoped, limb 3 would be **unexpressible** and AC2's answer would be *"it cannot be expressed, and
  that is the finding."* I tested the capability at the subcommand grain **because** the source read
  (`_compbudget.resolve_budget` in `_cmd_deployed`) contradicted my own prior row -- when evidence
  contradicts a measurement, the measurement is a live branch.
- If the four hops had used different key spaces, the conjunction would need a mapping layer and thus
  a new tool. They do not; the shared repo-path key is what makes it a two-call expression.
- If `deployed` had returned a clean zero for an out-of-domain path instead of `rc=2 REFUSED`, W3-S11
  would be **ARMED**, because a chain following the header would silently report unrelated files as
  deployed.

## 7. Declared limits

- **`comp-freshness` was exercised only via `self-test`.** Its live artifact axis (S3/DDB gold chains)
  was not exercised; no AWS data plane was read by this cell beyond `deployed`'s own ETag comparison.
- **The conjunction was demonstrated on ONE path pair.** It is an existence proof of expressibility,
  not a survey of how often the conjunction is TRUE anywhere.
- **The 554-file domain count is a path-glob count** over `data/*/scripts/{gold,silver,bronze}/*.py`;
  `deployed`'s true corpus also includes aux/mdpf prefixes it enumerates by directory glob, so 554 is
  a close lower bound on the intersection, not an exact census of that tool's corpus.
- **Owner is DECLARED, not ACCEPTED** (s.2 above).
- **The vintage is `f2ef16d70a` and every status here is perishable.** Section 5 of the contract names
  the census as the re-measurement instrument -- and names its current mis-scoring.

## 8. Rows filed

| id | class / hazard | one line |
|---|---|---|
| `NFRA_OUTSET-W3-S10` | OBSERVATION / **ARMED** | Corrects my own `W3-S9` + the OS-s-12 census row: `--budget` is on the `deployed` subcommand, and bounded the tool answers rc=0 in 8.4 s. Census will keep emitting the false FAILED; outside my `<paths>`, so routed not fixed. |
| `NFRA_OUTSET-W3-S11` | OBSERVATION / INERT | comp-heat's header promises a *"full local->git->deploy view"* over a join whose right side covers 554 of 30,659 files (1.8%) and names no domain. Boundary is enforced by an explicit `rc=2` refusal, not a silent zero. |

## 9. What I changed

Created `docs/architecture/NFRA_OUTSET_COMPOSITION_CONTRACT.md` (the contract, and the only file
written outside my deliverables folder and the channel). Appended 2 rows to the project channel
(append-only; byte prefix asserted identical before the splice, array re-parsed to **62 rows**, all
ids distinct, no existing row edited; CR/LF/CRLF 1523/1523/1523, zero bare endings). Wrote this
document and the proof-of-spec instance beside it.

**Nothing under `.tools/` and nothing under `org/modules/` was modified** -- every tool named in this
contract was invoked read-only, including the two I found defects in.
