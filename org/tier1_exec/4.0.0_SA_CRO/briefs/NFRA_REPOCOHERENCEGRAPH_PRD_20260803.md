# NFRA_REPOCOHERENCEGRAPH — PRD: the Repo Coherence Graph (RCG)

**Author:** 4.0.0_SA_CRO (Chief Research Officer)
**Home:** org/tier1_exec/4.0.0_SA_CRO/
**Recon ID:** RCN-0004 — registered in RECON_REGISTER.md
**Date:** 2026-08-03. **Status:** STAGED FOR CTO LANDING — canonical home
`docs/architecture/NFRA_REPOCOHERENCEGRAPH_PRD.md` (`docs/architecture/` is `lane=ANY_CTO`; this
copy is the CRO-staged original, per the NFRA_VELOCITY landing precedent).
**Source document:** `C:\Users\AndrewBerman\Downloads\Repository Coherence Graph Proposal.docx`
(Andrew, 2026-08-03) — the founding proposal; this PRD is its estate-grounded implementation spec.
**Design sessions:** Andrew <-> CRO, CRO terminal, 2026-08-03 (four design rounds; all rulings
quoted verbatim below are from that channel, that date).
**Constitution:** `docs/doctrine/INTENT_DENOMINATOR_SYNCHRONIZATION.md` binds every scan, score,
and verdict in this document. `docs/doctrine/CONTROLS_OVER_CARE.md` binds its instruments.

---

## §0 Commission and premise (verbatim anchors)

> *"I think what we need to do is effectively suspend (temporarily) NFRA_VELOCITY work because we
> need to figure out the RCG first."*

> *"The premise is that we need to be able to scan through every folder in the repo, all the way
> down through all nesting, and assess doc by doc, file by file, what is deprecated/cruft/etc.,
> and do a spring cleaning of sorts... Only by cleaning out the repo can we establish a clean base
> by which to facilitate the ontological development of NFRA_VELOCITY."*

> The problem being solved, in Andrew's words: the problem *"plaguing NFRA_VELOCITY right now [is]
> that we're trying to run this in a non-clean setting."*

The two-axis core, Andrew-direct, quoted exactly because the phrasing IS the design:

- **ACTIVE** — *"is this file mechanically referenced or depended upon in some kind of runtime"*
- **RELEVANT** — *"is this file semantically aligned with the current state of the company and
  operations"*

And the review inversion: *"we can back into 'Relevant' to some extent as a function of 'Active'.
I.e., the items that are most active are the first ones we need to review for relevance."*

**Denominator at commissioning:** 25,273 tracked files (git ls-files, 2026-08-03).
Top roots: `org/` 12,738 · `infra/` 7,956 · `data/` 1,820 · `docs/` 1,366 · `tools/` 516 ·
`.tools/` 276 · `deck_generation/` 194 · small roots (`timeseries/`, `research_transcripts/`,
`research/`, `models/`, `users/`, `workflows/`, `etf_netassets_watch/`, ...) ~300.

## §1 The five-step macro sequence (this PRD is step 1a)

1. **Debt cleanout** — **1a: the repo / knowledge plane (THIS PRD)** · 1b: AWS / execution plane
   (same 2x2 and vocabulary; candidates routed through NFRA_VELOCITY WS-E3's existing gates;
   consumes 1a's disposition ledger as its intent substrate — specified at 1a-P4, not here).
2. **Ontology refinement** — definitions, documentation, schemas, frameworks, on the clean base.
3. **comp-tools dialing** — coherence tooling at scale across the global Estate Infrastructure.
4. **Tech-debt deleveraging + resource and pattern consolidation** — the debt-heavy macros (MDPF,
   ADVI, ...) proceed on the consolidated substrate.
5. **Standing hygiene** — *"continual processes to manage the hygiene of the knowledge and
   execution planes"* — the RCG rescan loop becomes permanent (§14).

## §2 Relationship to NFRA_VELOCITY

**Suspension (Andrew-direct, temporary):** NFRA_VELOCITY_CORE + NFRA_VELOCITY_ESTATE flip to
**On-Hold** at RCG P0 — never closed, never absorbed. Per the program's own §3b anti-opacity
lesson (eight absorbed projects becoming one opaque record), the suspension commit MUST carry an
open-work ledger: what each workstream holds open (C7 at 1-of-9 specimens; C8's reconciliation
enumerator; the `Lifecycle_Value`/`lifecycle_class` naming act; E2's unreconciled 142+12 census;
E3 structurally inert on lifecycle values; the WS-E8 write-target hold). The suspension record is
CTO/COO's to execute; this PRD is its trigger and citation.

**What carries INTO RCG (the suspension is not a stop):**
- **The vocabulary.** RCG dispositions are expressed in the ratified 7-value `lifecycle_class`
  (rule bank v1.8) + a MIGRATE flag — no forked vocabulary (§3). RCG is the first mass population
  of VELOCITY's type system, on the reversible plane, with Andrew as the producer-asserter the
  ruling requires.
- **The constitution.** Intent-from-above / denominator-from-below / gap-printed governs every
  RCG instrument, including the gate on RCG's own folder (§12).
- **The recall standard's spirit.** Every RCG extractor ships a boundary declaration
  (address space / traversal residue / presentation residue / failure direction) even though
  WS-C7 itself is suspended.

**What RCG hands BACK (the hand-off contract, consumed by the VELOCITY redesign):**
a clean tree · the disposition ledger (thousands of ratified lifecycle assertions) · the
comp-tools dependency map + registry adjudication (which registry generations live code actually
reads) · per-root feature-importance reports (what discriminates, per territory) · the standing
hygiene loop. **The VELOCITY granular redesign itself is out of scope here** — Andrew:
*"[NFRA_VELOCITY] will need to be slightly redesigned to be more granular, but we will cover that
after."* This PRD ends at the hand-off.

## §3 The core model: ACTIVE x RELEVANT

Two orthogonal axes with opposite epistemologies — ACTIVE is a **computation** (§5), RELEVANT is
a **judgment** (§7). Their product is the disposition space:

| | RELEVANT | NOT RELEVANT |
|---|---|---|
| **ACTIVE** | **CANONICAL** — live and wanted. Protect. | **LOAD-BEARING LEGACY** — runtime depends on something semantically superseded. Disposition: **MIGRATE, never archive** (archiving breaks a live path). The highest-risk quadrant; found first by the §7 review order. |
| **NOT ACTIVE** | **REFERENCE / DORMANT** — constitutionally or historically load-bearing: doctrine, session logs, rulings, rollback levers. Keep, typed. | **CRUFT** — the only quadrant that is cleanup. Archive/remove, batched, ratified. |

**Dispositions and their lifecycle_class expression:**

| Disposition | lifecycle_class | Executed as |
|---|---|---|
| CANONICAL | PERMANENT (or EVENT_CREATED where append-only) | none — protected |
| REFERENCE_KEEP | DORMANT / EVENT_CREATED / PERMANENT per charter | none — typed and kept |
| MIGRATE | LEGACY (successor named) | routed to change management; the WRITE retires, never the file blindly |
| ARCHIVE | RETIRED (ruling = the ledger entry) | `git rm` in ratified batches (§13) |
| CONTESTED | UNDECLARED, loud | escalated to Andrew, never model-resolved |

`lifecycle_class` remains PRODUCER-ASSERTED: the model and grader PROPOSE; **Andrew's cohort
ratification is the assertion**. Pinned to the artifact-shape sense of `lifecycle_class` pending
the open `Lifecycle_Value` naming act (SYSTEM_DEFINITIONS `contested_unresolved`).

## §4 File classes (feature semantics are per-class)

| Class | Definition | Native reference physics |
|---|---|---|
| EXEC | .py/.sh/.ps1/.js — runs | imports, invocations, PATH/shebang |
| REG | machine-read .yaml/.json registries/configs | **reader-anchored**: a live consumer's source names its path |
| DOC | .md/.txt prose | citations, lexical mentions, governance pointers |
| DATA | .csv/.parquet/.tsv/.jsonl artifacts | producer/consumer grammar (medallion conventions) |
| RECORD | logs, inbox messages, task orders, handoffs | none expected — historical by design |
| ASSET | binaries, images | colocation only |

Class = f(extension, charter, shebang/frontmatter probe). **RECORD is assigned by path charter,
never extension** (a .md under `org/*/logs/` is RECORD, not DOC).

## §5 ACTIVE: mark-and-sweep garbage collection over a typed reference graph

**The algorithm is tracing GC, literally:** enumerate a root set, extract typed reference edges,
compute the reachability closure. Marked = ACTIVE; unmarked = the candidate sweep population.
Deterministic, re-runnable, no ML on this axis.

**5.1 Root set (enumerated; version-controlled in `rcg/charters.yaml`):**
`CLAUDE.md` + `org/XXX.md` · `.claude/` (skills, settings, hooks) · `.tools/*` + `~/bin`
forwarders · `org/mcp/server.py` + broker/watch machinery · `infra/aws/lambda/ci/
lambda-source-map.json` -> every mapped Lambda tree · the Terraform tree · `.github/` CI ·
active-status `org/projects/*.json` · `MEMORY.md` + memory frontmatter · registries proven
consumed by live tools (cycle-0 output, §9).

**5.2 Typed edge classes** (descending extraction confidence): code import (AST) ·
shell/subprocess invocation · config/data read (reader-anchored source walk) · gate consumption
(hooks, commit-gate, CI) · **governance citation** (CLAUDE.md/skill/XXX.md pointers,
SYSTEM_DEFINITIONS `authority:` fields, memory `[[links]]`) · doc-to-doc citation · git co-change
(evidence only, never confers marking). Governance citation is first-class because in this org
**prose is runtime** — agents execute CLAUDE.md and skills every session; a doc cited by law is
as live as an imported module.

**5.3 Marking rules:**
- **Vintage-weighted:** marking flows from live roots only; the unmarked never confer life on
  each other (dead clusters citing each other stay dead).
- `active_strength` (graded, for review ordering): f(root type weight, hop distance,
  `ref_mech_in` mass, runtime echoes). The mark bit itself stays boolean.
- `ref_dangling_out` recorded during extraction: a file whose own references resolve to nothing
  is decaying measurably.

**5.4 Boundary declaration (mandatory, printed with every scan):** the extractor's address space,
traversal residue (dynamic imports, f-string paths, `getattr` dispatch, shell string-building,
runtime-constructed S3 keys — all invisible to static extraction), presentation residue, and
**failure direction: UNDER-MARKING (false cruft)**. That declared direction forces the safety
default: the sweep **proposes, never executes** (§13), and controls are planted per packet
(§11). The scanner that cannot state what it could not have seen prints that as its first line.

## §6 The feature dictionary (five families + one thin rider; snake_case per the naming act)

**`filesystem` (colocation — all classes):** `fs_root` · `fs_depth` · `fs_charter` ·
`fs_dir_size` · `fs_sibling_class_mix` (a lone .md among code is not a .md in docs/) ·
`fs_name_signal` (date-stamps, `test_`, `tmp`, `spike`, `v\d`, `_old`, `.RELOCATED`, tilde
patterns). Colocation is also the cohort prior: dispositions propagate along directories first.

**`reference_mech` (deterministic edges; EXEC/REG primarily):** `ref_mech_in` by reader class
(code-import / config-read / gate-read / CI) · `reach_from_root` + `reach_hops` +
`reach_root_type` (**the mark bit + its provenance**) · `ref_mech_out` · `ref_dangling_out`.

**`reference_lexical` (the BM25 channel; DOC + EXEC docstrings/comments; EXCLUDED on RECORD and
DATA):** built against the per-scan **estate name lexicon** — every canonical identifier (comp-tool
names, file basenames, project codes, serials, SYSTEM_DEFINITIONS term keys, bucket/key grammars,
Lambda names), each tagged LIVE or RETIRED from registries + git history. Features:
- `ref_lex_in_live` / `ref_lex_in_dead` — BM25-weighted inbound mentions of this file's
  identifiers, split by whether the mentioning file is reach-marked (vintage-weighted reference).
- `ref_lex_out_retired_ratio` — this file's own usage of RETIRED identifiers: the semantic-decay
  signal made deterministic (a doc heavy in retired-era vocabulary announces its era).
- `ref_lex_core_proximity` — §7.2.
Confinement rationale: a log mentioning a retired tool is historically correct, not decayed;
lexical decay only means something where text claims present tense.

**`temporal` (git — all classes):** `t_age` · `t_last_touch` · `t_commit_count` ·
`t_author_live_ratio` (share of authors whose serials still exist) · `t_cochange_cluster` +
`t_cochange_live_ratio` (share of co-change partners reach-marked) · **`t_era_project` +
`t_era_status`** — the file's birth/last-touch joined to the project-registry timeline. A file
born under a closed-as-superseded project, untouched since closure, co-changing with nothing
live, is cruft by three independent measurements before any judgment. The pivot history exists as
structured data; this feature is the single highest-leverage input.

**`status_declared` (self-assertions; DOC/REG):** `s_header_status` (SUPERSEDED / DRAFT / RETIRED
/ CANONICAL parses) · `s_registry_status` (what a registry says ABOUT this file) ·
**`s_conflict`** — declared status contradicting mechanical evidence (declared RETIRED but
reach-marked = load-bearing legacy; auto-flagged to the top of the review queue).

**`activity_runtime` (thin rider; EXEC/REG):** lambda-source-map membership · live hook
references · recent tool-run echoes (`comp-tool-runs.jsonl`, device-local caveat declared).

**Confinement matrix (feature family x file class):**

| | EXEC | REG | DOC | DATA | RECORD | ASSET |
|---|---|---|---|---|---|---|
| filesystem | x | x | x | x | inventory only | x |
| reference_mech | x | x | cite-in only | producer/consumer | — | — |
| reference_lexical | docstrings | — | x | — | — | — |
| temporal | x | x | x | x | inventory only | x |
| status_declared | — | x | x | — | — | — |
| activity_runtime | x | x | — | — | — | — |

RECORD rows are inventoried (counted, aged) but never scored and never swept (§8, §13).

## §7 RELEVANT: backed into from ACTIVE, judged against intent sources

**7.1 The two-pointer review order (Andrew's inversion, operationalized):** relevance
adjudication runs in **descending** `active_strength` — the top of the reach graph first — because
(a) the ACTIVE x NOT-RELEVANT quadrant (load-bearing legacy) is the highest-risk population, and
(b) nothing else can be judged until the core is ratified. Sweep candidacy runs in **ascending**
activity (safest first). The pointers converge on the ambiguous middle — which is where the
model's uncertainty band sits by construction.

**7.2 The ratified active core as semantic anchor:** once the top of the active set is ratified
RELEVANT, that corpus — recency-weighted — operationally defines *"the current state of the
company and operations."* `ref_lex_core_proximity` (BM25 similarity to the ratified core) then
scores relevance for the remainder deterministically. Relevance stops being a per-file essay and
becomes distance-to-a-ratified-center; model + grader handle only the margin. This keeps the LLM
out of the primary classification loop (the source proposal's own constraint, and §6 of the
VELOCITY program's deterministic-first law).

**7.3 Intent sources (from above, per the constitution):** `SYSTEM_DEFINITIONS.yaml` (vocabulary
canon + deprecated senses) · the project registry with closed/absorbed statuses · CLAUDE.md law ·
the retired-name history · the RULINGS channel (§10) — Andrew's exogenous business context,
which outranks all of the above.

## §8 Sub-scan architecture: per-root charters, per-root models

Same pipeline; separate feature weighting, calibration, model, and review queue per scan — base
rates differ by an order of magnitude across roots.

**Charters** (`rcg/charters.yaml`; a categorical feature AND a hard override): `LIVE_CODE` ·
`GOVERNED_REGISTRY` · `DOCTRINE` (protected) · `APPEND_ONLY_RECORD` (protected: inventoried,
never scored, never swept) · `WORKPRODUCT_ARCHIVE` · `SCRATCH` · `PROTECTED_LIVE_CORE`.

| Sub-scan | Files | Dominant classes | Decides here | Special handling |
|---|---|---|---|---|
| `scan_org` | 12,738 | RECORD, DOC, REG | charters do most of the work | `org/*/logs/`, `org/mcp/inbox/`, `org/*/task_orders/`, `handoffs/` = APPEND_ONLY_RECORD. Residual = deliverables, registries, mcp machinery, `org/modules/graph/` (the registry-generation pileup — a named cleanup target) |
| `scan_infra` | 7,956 | EXEC, REG | `reference_mech` is king | roots: lambda-source-map, TF tree, EC2 manifest. Deployed-vs-repo drift fenced OUT to step 1b |
| `scan_docs` | 1,366 | DOC | `reference_lexical` is king | 4th first-class scan — where RELEVANT does the most work; direct feeder to step 2. `docs/doctrine/` = DOCTRINE charter |
| `scan_data` | 1,820 | DATA, EXEC | medallion grammar + pipeline registries | **firm-separation fence: no cohort spans bd/cot/inf; deliberate parallels are never duplication candidates** |
| `scan_misc` | ~1,000 | mixed | whole-cohort dispositions | small orphan roots + root files + **the `tools/` (516) vs `.tools/` (276) collision — first adjudication specimen** |

Per-root CatBoost models for the four primary scans; shared model for misc. Per-root feature
importances are a deliverable (they feed charter refinement now and step 3 later).

**`.tools/` = PROTECTED_LIVE_CORE** (Andrew-direct: *"High priority functions that need care
taken around them is the comp-tools folder and references/dependencies"*): never in a sweep queue
in v1. It is not skipped — it is **cycle 0** (§9): the comp-tools dependency map is built FIRST at
highest recall, because (a) comp-tools out-edges ARE the marking substrate, and (b) reader-anchored
evidence adjudicates the registry generations (`comp-tools.yaml` vs `TOOL_MASTER.yaml` vs
`graph-call-manifest.yaml` vs coverage manifests) by the only test that matters: which ones live
code actually reads.

## §9 The cycle: two workflows bracketing the human session

The unit of operation is a **cycle**, per sub-scan. Cycles across roots interleave freely
(independent models/queues). Proposed order: **cycle 0** = comp-tools dependency map ->
`scan_infra` (crispest physics; trains the loop on strong ground truth) -> `scan_docs` (uses the
ratified infra core as anchor) -> `scan_org` residual -> `scan_data` -> `scan_misc`
opportunistic.

**W1 — `rcg_review_prep`** (leads into review; deterministic except stage D):

| Stage | Runs | Output |
|---|---|---|
| A `scan` | classes + all feature families, full nesting | feature matrix @ scan vintage (git SHA + date), LOCAL |
| B `mark` | root set -> typed edges -> closure | ACTIVE marks + `active_strength`; denominator + boundary declaration printed |
| C `score` | current per-root CatBoost | disposition probabilities + uncertainty band, stamped with model version |
| D `grade` | **agent exploration confidence check** (the only LLM stage): walk the two-pointer queue, read files + neighborhoods, build evidence cards | confidence-scored proposals |
| E `packet` | assemble the review session: cohort-ordered cards, disagreements first, planted controls included | the review packet |

**Stage F — the human session (Andrew):** ratify / override / rule, at cohort grain.

**W2 — `rcg_post_review`** (fully deterministic):

| Stage | Runs | Output |
|---|---|---|
| G `ingest` | ratifications -> label bank; overrides diffed vs model AND grader | `LABELS.jsonl` append |
| H `apply_rulings` | render exogenous rulings into machine effects (§10) | lexicon/charter/label/rule deltas |
| I `retrain` | CatBoost refit on grown labels + deltas | new model version = (cycle, label-bank SHA, rulings SHA, engine SHA) |
| J `rescore_eval` | re-score under the new model; emit MODEL_EVAL (§11) | deltas + next cycle's queue |
| K `execute` | ratified dispositions batched under gates (§13) | commits citing ledger entries |

**Evidence card** (stage D, per file/cohort): reach paths verbatim (who depends on it) · lexical
in/out with live/dead split · co-change partners + marks · era + recency · declared status ·
model score + top CatBoost attributions. **Confidence is convergence, not a vibe:** HIGH = >=3
INDEPENDENT feature families agree, none contradicts — independence means different measurement
planes, and **two absence-shaped signals (unreferenced + untouched) count as ONE family** (the
TRANSIENT lesson). REVIEW = families split. CONTESTED = any `s_conflict` or
mechanical/semantic contradiction — auto-escalated, never model-resolved.

## §10 The RULINGS channel: exogenous business context as a first-class input

Andrew: *"I might bring in new exogenous business logic and context etc. that needs to be
addressed, that part will be very flexible so want to make sure we can handle that properly."*

Mid-review context ("this client relationship is ending," "X is being rebuilt on Y") lands as an
append-only entry, never as session ephemera:

```
rcg/rulings/RULINGS.jsonl:
  {id, date, verbatim,            # never paraphrased -- the phrasing IS the ruling
   scope, rendered_effects: [],   # what stage H turned it into
   model_version_applied, open_questions}
```

Stage H renders each ruling into **machine effects**: a lexicon delta (identifiers LIVE->RETIRED)
· a charter delta (a subtree's grammar changes) · label overrides (cohorts re-dispositioned) · a
new hard rule (a fence). Anything NOT mechanically renderable becomes a versioned
**grader-instructions delta** (`rcg/grader/INSTRUCTIONS.md`) — standing stage-D context, so a
judgment-shaped ruling propagates to every future card instead of living in one session's memory.
Either way the ruling re-scores its blast radius in the same cycle, and every entry records which
model version absorbed it: "when did the system learn this" is always answerable.

## §11 Model grading and improvement

The structure yields a **clean prospective test every session**: the model's blind predictions
are scored against ratifications on labels it never trained on, by construction. Per-cycle
`MODEL_EVAL.jsonl` entry:

- **Prospective precision/recall per disposition class.** The asymmetric bars: ARCHIVE-precision
  is the one that must be near-perfect; MIGRATE-recall outranks MIGRATE-precision.
- **Calibration** — stated confidence vs realized agreement, per root.
- **Grader accuracy tracked SEPARATELY** from model accuracy — two instruments; grading them
  jointly hides which one is wrong. Disagreement analysis feeds `grader/INSTRUCTIONS.md` the same
  way labels feed the model.
- **Planted controls, every packet:** >=2 known-cruft + >=2 known-canonical seeded per review
  batch (`known_negative` law: exercising proves it runs; only a known-negative proves it
  discriminates). **A misgraded control QUARANTINES the cycle's outputs before anything
  executes.**
- **Feature-importance drift per root** — sanity check now, step-3 deliverable later.

**Autonomy ladder (explicit ratchet, never implicit):**
- **L0 (start):** every disposition human-ratified.
- **L1:** auto-disposition for HIGH-confidence ARCHIVE in SCRATCH-chartered subtrees only; earned
  by class precision >= 98% over >=2 consecutive cycles; revoked by any control failure.
- **MIGRATE and CONTESTED are never automated at any level.**

**Provenance law:** every score cites its model version; every executed disposition cites ledger
entry + scan vintage + model version. Full provenance on every deletion, forever.

**Bootstrap (before Andrew labels anything):** free high-confidence seeds — SUPERSEDED/RETIRED
headers, `archive/` subtrees, the 36 dead flat inbox dirs, `.RELOCATED.md`, tracked scratch
residue on the cruft side; CLAUDE.md-cited docs, SYSTEM_DEFINITIONS authorities, live
skills/tools on the canonical side. Weak supervision -> first model -> the human loop starts at
the interesting margin, not at zero.

## §12 The `rcg/` folder contract (Andrew: "IMPERATIVE that folder is kept immaculately clean")

```
rcg/
  MANIFEST.yaml            # THE enumerated allowed-path list + write rules -- the folder's contract
  charters.yaml            # per-root/subtree grammars + the root set
  rulings/RULINGS.jsonl    # append-only (Andrew's exogenous context, verbatim)
  ledger/DISPOSITIONS.jsonl  LABELS.jsonl  MODEL_EVAL.jsonl    # append-only decision record
  grader/INSTRUCTIONS.md   # versioned stage-D standing context
  bin/                     # engine: scan.py mark.py features.py model.py packet.py post_review.py
  workflows/W1_REVIEW_PREP.md  W2_POST_REVIEW.md               # the two procedure contracts
  scans/  models/          # GITIGNORED -- vintaged measurements + weights, local-only, reproducible
```

**The strictness is a GATE, not a norm — the estate's own law pointed at the folder:**
`MANIFEST.yaml` is the intent source; the commit's file list is the denominator; a pre-commit
check (extending the existing commit-gate chain) **DENIES any write under `rcg/` not
manifest-enumerated**. Audited override for genuine additions, which must amend the manifest in
the SAME commit — the manifest can never drift from the tree. Plus:
- **Append-only enforcement** on `rulings/` + `ledger/` (no edits/deletions of prior lines).
- **Single-writer lane** in `.owned-paths.yaml` (the RCG operator seat; grantor commits the
  grant per SoD — the CRO does not write its own).
- **No-satellite-prose rule:** analyses and notes become ledger entries or are not committed.
  The folder that cleans the repo cannot grow its own sediment.
- Committed footprint stays ~a dozen files for the life of the program; the manifest is the
  machine-checkable proof.

Outside the folder, exactly four governance files exist: this PRD (canonical copy at
`docs/architecture/`, CTO-landed) · `org/projects/NFRA_REPOCOHERENCEGRAPH.json` · the REGISTRY
row · a one-line `.tools/comp-rcg` forwarder (rail reachability; registered under the existing
comp-manifest-check invariant — RCG dogfoods the registration gate from birth).

## §13 Execution and safety

- **Propose-never-execute:** no disposition executes without a ledger entry ratified at stage F
  (or earned L1 autonomy, §11).
- **Sweep mechanics:** `git rm` in ratified batches — git history IS the archive; each batch
  commit cites its ledger ids. (Default confirmed over move-to-`archive/`; reversal is
  `git revert` / `git checkout <sha> -- path`.)
- **MIGRATE routing:** through normal change management (safe-commit / safe-apply / deploy
  ledgers); the unit of retirement is the WRITE, not the file (LD-0330's law carried over).
- **Protected classes (never in a sweep queue):** APPEND_ONLY_RECORD subtrees · DOCTRINE ·
  PROTECTED_LIVE_CORE (`.tools/`) · anything carrying a live DORMANT/rollback annotation.
- **Firm separation:** no cohort spans bd/cot/inf; 0824/0833 never-sum binds cohort content.
- **Portal excluded** from v1 (own repo, own process).
- **Standing constraints bind:** the alarm/monitor moratorium (RCG lands as gates + reports +
  owned items, never notification machinery) · LD-0175 (cycles are operator/event-driven; no
  crons) · TRIGGER_LAYER (a finding that cannot fail a gate is a diary entry) · NEVER rules
  (no bare terraform/git primitives; safe-* wrappers everywhere).

## §14 Metrics (anti-Goodhart) and the standing hygiene loop (step 5)

**Measured, with denominators, per cycle:** % of repo carrying a ratified disposition (coverage)
· prospective model precision/recall per class (§11) · control pass rate · **new-cruft rate** —
files entering unreachability since the prior scan vintage, attributable per session/author (the
step-5 signal) · agent-facing search precision (a fixed probe suite of canonical queries;
comp-grep noise measured before/after sweeps).

**Explicitly NOT a metric: raw file-count reduction** — gameable by narrowing the predicate; the
record's own denominator-shrinks-and-looks-like-progress lesson.

**The standing loop (step 5, permanent):** rescan on operator cadence -> delta vs prior vintage
-> new-unreachable report -> triage into the next review packet. The disposition ledger becomes
the intent substrate for step 1b (AWS), and the new-cruft-rate feeds whatever archetype-dynamics
layer the VELOCITY redesign lands (the C9/E7 successor).

## §15 Implementation schedule — feeding NFRA_VELOCITY

Rate limiter: Andrew review sessions (30-60 min each; suggested 2-3/week). Wall-clock bands
assume that cadence; build stages between sessions are agent-paced and fast.

| Phase | Work | Acceptance (machine-checkable) | Feeds VELOCITY |
|---|---|---|---|
| **P0** (days 1-2) | `rcg/` + MANIFEST gate live + charters v1 + suspension record lands (CTO/COO) + project registration | gate DENIES an out-of-manifest write (exercised, both directions); suspension commit carries the open-work ledger | the suspension record itself (honest state, resumable) |
| **P1** (days 2-5) | engine build: scanner, marker, feature families, lexicon builder; **cycle 0 = comp-tools dependency map**; first full scan of ALL roots (inventory only) | boundary declarations print on every extractor; first census published with per-root denominators; registry-generation adjudication table (which registries live code reads) | cycle-0 map -> step 3; the census = the honest denominator VELOCITY never had |
| **P2** (days 5-10) | `scan_infra` cycles: seeds -> first model -> first review sessions -> first executed sweeps | >=1 full W1->F->W2->K cycle clean; controls 4/4 across >=2 packets; ARCHIVE-precision measured; first ratified active core | clean `infra/` tree; ratified core = the semantic anchor; first mass lifecycle assertions |
| **P3** (days 10-15) | `scan_docs` cycles (anchored on the P2 core) | docs coverage >= target set at P2 close; SYSTEM_DEFINITIONS-conformance report (which docs speak retired vocabulary, with counts) | **the direct step-2 feeder: canonical-vs-superseded adjudicated for the ontology corpus; doctrine boundary explicit** |
| **P4** (days 15-22) | `scan_org` residual (incl. `org/modules/graph/` pileup) + `scan_data` (fenced) + `scan_misc` (incl. `tools/` vs `.tools/`) | per-root coverage + eval reports; org registry generations dispositioned; **step-1b spec authored** (AWS plane, consuming the ledger) | clean `org/modules/graph/` = the rule bank's own home de-crufted; 1b spec -> WS-E3's intent substrate |
| **P5** (standing) | hygiene loop armed (operator cadence); autonomy ladder ratchets per §11; hand-off package assembled | new-cruft rate reporting live; hand-off delivered: clean tree + ledger + maps + importances | **the VELOCITY granular redesign begins here, on the fresh state** — Andrew: *"we will cover that after"* |

## §16 Governance and open items

**Roles (not serials — resolve holders from the live roster, never this table):** Andrew —
ratification sessions, rulings, the naming acts. CRO — program spec, the grading loop (stage D),
model-eval reads, RCN register. CTO — PRD landing, the MANIFEST gate, arch-gates on MIGRATE
executions, suspension record. COO — decomposition to build lanes, suspension co-execution,
cross-domain flags. Build lane(s) — the engine, per CTO/COO staffing. CVO — verify passes on
executed sweep batches (the verifier is not the do-er).

**Needs Andrew, in order:** (1) this spec's review + GO; (2) the suspension word to CTO/COO
(P0); (3) the `Lifecycle_Value` / `lifecycle_class` naming act (RCG proceeds pinned to the
artifact-shape sense meanwhile); (4) review-session cadence; (5) the `rcg/` folder name if other
than default.

**Defaults adopted (flip any):** `git rm` over archive-move · org record-mass = APPEND_ONLY,
kept · portal excluded · interleaving order §9 · folder name `rcg/`.

---
*RCN-0004. Evidence basis: the source proposal (9,184 chars extracted, 326 paragraphs) · the
NFRA_VELOCITY record (program + both PRDs + type dictionary + constitution + contracts folder +
CVO session logs @e2218a106f/@fa505d4cff/@e661f608cc) · the live repo census (25,273 tracked
files, 2026-08-03) · four Andrew<->CRO design rounds, this channel, 2026-08-03.*
