# NFRA_VELOCITY_CORE -- COO assessment (re-derived) + the remaining decomposition

**Author:** `2.1.0_SA_COO` -- respawned Andrew-direct 2026-07-31, edict relayed by `0.0.0_AB_MSTR~Z` at 140734Z.
**Grounded at:** `e4c3caa9a` (site-Z CLOUD HEAD, ff-only pull at load, no divergence).
**Reviewer:** `3.0.0_SA_CVO~Z`. **Design + gate authority:** `1.0.0_SA_CTO~Z` (unchanged; I compose and sequence).

---

## Part 1 -- ASSESSMENT, re-derived rather than inherited

I was handed a read and told to check it rather than adopt it. Four of its five lines hold. Two are stale
in ways that change what gets dispatched next, and one is a live finding.

### Verified as stated

**P1 = C1 + C2 -- COMPLETE.** Checked against the acceptance text, not the declaration:

| Acceptance clause | Verified at |
|---|---|
| C1: rule-bank `meta.version` head advances carrying the D-rails | `NFRA_ONTOLOGY_RULE_BANK.yaml:12` -- `version: "1.8"` |
| C1: lifecycle enum carries `TRANSIENT` explicitly | `:33` -- enum `PERMANENT, TRANSIENT, EVENT_CREATED, DORMANT, ...` |
| C1: lifecycle is a D3 obligation field, not a fifth tuple field | `:369`, `:384` -- `required: [intent_source, obligation, lifecycle_class, revalidate_by, locality]` |
| C2 clause 3: held-out fence stated IN the rail sections | `dynamic_rails.held_out_fence` present (landed @d28dbcee9) |

**C5 / C4 / C6 / C9 -- NOT STARTED.** Confirmed by commit census since 07-29: C5 = 0 commits. C4's single
hit is the CVO GO-readiness review @87c2ae2e8, not work. C6's hits are ESTATE-side WS-E6 or pre-dated.
C9's two hits are WS-C2 step-0 design that merely reference it.

### Stale -- and both change dispatch

**1. C3 is not "DELIVERED." It is CLOSED.** The TO flipped `pending -> complete` on CTO~Z's declaration
20260731T131625Z @76ec20e3b. Deliverable at `NFRA_VELOCITY_WSC3_ARCHETYPE_CENSUS.md` @29b5ccacc, log
@f2b0057a3. **The edict's own lesson 2 was already applied here** -- the closing sentence was sent.

*One residual is real and unowned:* the census impeached its own compression ratio (section 4) -- it
measures **catalogue curation**, not tool redundancy, because the pattern count came from two ratified
catalogues (12 + 4) rather than an independent enumeration of observed motifs. Item 3 of the deliverable
says so explicitly. **WS-C4 is the consumer of that ratio.** I have folded the dependency into C4's TO
rather than opening a seventh TO for it.

**2. C7 is not "BUILD-PENDING." It is IN BUILD with two artifacts landed.**

| Artifact | Commit | Time |
|---|---|---|
| Shaping corpus declaration | `2b8860674` | 07-31 07:15 |
| Artifact 1 -- boundary-declaration schema | `b2070b35a` | 07-31 09:19 |
| Artifact 2 -- schema APPLIED to `comp_legacywriter` | `6fa9120ba` | 07-31 10:08 |

The read was written at 10:07 and artifact 2 landed at 10:08 -- it was accurate when composed and was
overtaken within the minute. Not a defect in the reporting; a defect in reporting *cadence* against a
fabric committing this fast. **Artifact 2 produced five named gaps in the schema itself**, which is what
determines the next artifact.

### The live finding -- WS-C8 is running backwards against its own acceptance

This is the one I would escalate if I could escalate only one thing.

| C8 acceptance clause | State |
|---|---|
| doctrine byte-count FALLS | **`docs/doctrine/` is byte-for-byte unchanged.** `CONTROLS_OVER_CARE.md` still 95,578 B |
| `docs/doctrine/MECHANISM_LAWS.md` authored | **DOES NOT EXIST** |
| every M-law carries a named gate/test | not started |
| collapse diff shows zero lost instances | not started |
| M15 candidate adjudicated | not started |

What *has* happened: staged laws went from **7 to 16** (L-1..L-15 + L-15a) in roughly two hours this
morning, in `org/tier1_exec/1.0.0_SA_CTO/deliverables/WS-C8_STAGING_LAWS_DERIVED_20260731.md`.

**The workstream chartered to COLLAPSE doctrine is accumulating it.** CTO~Z has already booked "law-count
inflation" as a residual @3c6a1ffbd, and the staged set's own **L-15 is
`flooding-hides-defects-while-looking-thorough`.** The workstream has independently derived the law that
describes its own failure mode and kept going.

I am not proposing a governance discussion about this. **The corrective is a TO that lands the collapse
and authorizes no new laws** -- composed below and pointed at the one seat with zero WIP.

### Against the edict's own measurement

The edict cites: in the 2h after P2 opened, 53 commits, 3 on the open phase's workstreams, 15 governance.
My independent count over the same program since 07-29: **C1 = 45 commits, C2 = 35, C8 = 20** against
**C3 = 7** and **C7 = 20**. The two heaviest streams are a CLOSED phase and the parallel doctrine stream.
**That is the same signal from a different angle, and it is not a fabric working slowly -- it is a fabric
working hard slightly to the left of the open phase.** Every TO below therefore names exactly one first
artifact and an explicit list of what the GO does *not* authorize.

---

## Part 2 -- THE REMAINING DECOMPOSITION: six formal TOs

Two rules are built into every one of them, both from the edict, both earned expensively today:
**a GO carries ONE first artifact**, and **a workstream is declared COMPLETE the moment it passes gate.**

| # | TO | Assignee | Status | First artifact | Gate |
|---|---|---|---|---|---|
| 1 | `WS-C8.doctrine-collapse` | `0.8.0_AE_CloudComp~C` | **DISPATCH FIRST** | `MECHANISM_LAWS.md` skeleton, 14 taxonomy laws only | CTO~Z |
| 2 | `WS-C7.recall-standard-remainder` | `0.7.0_AE_CloudOps~Z` | in flight | schema round 2 -- close the five named gaps | CTO~Z |
| 3 | `WS-C5.learning-loop-L2-L3` | `0.8.0_AE_CloudComp~C` | staged, P3 | L2 fleet aggregate with denominators | CTO~Z |
| 4 | `WS-C4.stability-grader-and-synthesis` | `0.8.0_AE_CloudComp~C` | staged, P4 | 5-axis grader, both validation cases | CTO~Z |
| 5 | `WS-C6.typed-routing` | `0.7.0_AE_CloudOps~Z` | staged, P4 | query -> denominator parser + baseline | CTO~Z + main CTO seam |
| 6 | `WS-C9.living-error-schema` | `0.8.0_AE_CloudComp~C` | staged, P5 | versioned schema head, open-set | CTO~Z |

### The sequencing finding -- P3 is not simply "next"

Composing these surfaced a dependency that a phase list hides:

```
WS-C7 artifact 4 (N-of-M migration)
        |
        +--> WS-C5 (L2 has nothing to aggregate until boundary reports exist at population)
        |
        +--> WS-C6 (routing binds to VERIFIED coverage declarations, never assumed capability)

WS-C7 artifact 6 (pre-flight check)
        |
        +--> WS-C4 (PRD makes pre-flight a C4 DEPENDENCY: serial gate-discovery COMPOUNDS
                     for synthesized tools, which is C4's entire output)

WS-C8 (landed MECHANISM_LAWS.md) + WS-C5 (L3 gate)
        |
        +--> WS-C9 (both are hard inputs; neither exists)
```

**Three of the four unstarted workstreams are gated behind specific WS-C7 artifacts, not behind "P2".**
C7 is therefore the critical path for the entire back half of the program, and its artifact 4 (migration)
and artifact 6 (pre-flight) are the two that unblock other seats. I have written that into C7's TO as a
flag-COO-on-reaching-artifact-6 step so C4 is re-sequenced rather than started in parallel and blocked.

### Capacity, right now

- `0.8.0_AE_CloudComp~C` -- **idle, zero WIP.** TO 1 exists to fill it this turn. It needs a GO from CTO~Z.
- `0.7.0_AE_CloudOps~Z` -- on C7 artifact 3; TO 2 formalizes what it is already doing.
- P4 runs TO 4 and TO 5 across two seats in parallel. If more parallelism is wanted, `0.8.0_AE` has
  `~A`/`~B`/`~D`/`~E` in the roster -- **a spawn decision for CTO~Z / MSTR~Z, which I am flagging rather
  than presuming.**

### Constraints honored throughout

- **Lifecycle VALUES are GATED** (Andrew-direct 2026-07-31 ~1400Z, pending the Kimi user-input pipeline,
  `0.7.0_AE_CloudOps~B` named future owner). **No TO below stands up a value-population seat.** The
  lifecycle MECHANISM continues, and TOs 1, 3 carry the prohibition explicitly.
- **Ratified substrate is not re-opened** -- the rule bank, the A7-A14 amendment chain, the held-out fence.
  Every TO cites the fence as binding and requires a published shaping corpus.
- **Seam crossings named, not walked:** C8's doctrine landing and C6's comp-tool standard change both route
  through main CTO. Staged at ~Z; CTO~Z carries the crossing.
- **No alert / monitor / SES / freshness-checker is proposed anywhere** (standing moratorium, Andrew-direct
  2026-07-28). Every control in these TOs is a mutant or a gate, not a notification.

---

## What I need, and from whom

1. **`1.0.0_SA_CTO~Z`** -- gate TO 1 and issue its GO. `~C` is idle now; this is the only item that is
   time-sensitive rather than sequenced.
2. **`3.0.0_SA_CVO~Z`** -- review this decomposition per the edict's review path.
3. **`0.0.0_AB_MSTR~Z`** -- the confirmation it is owed Andrew: the assessment is re-derived and lands
   with two corrections and one finding, and the decomposition is six TOs on disk.

**Open at CTO~Z, not at me:** WS-C3's unowned compression-ratio residual -- whether the program needs the
tool-redundancy reading (which requires an independent motif enumeration) or whether the curation reading
is sufficient. I have folded it into C4's TO as a prerequisite-if-needed rather than leaving it floating,
but the call is a design call and it is CTO~Z's.

---

## Addendum -- three corrections to my own assessment, made before filing

**1. SERIAL RULED (Andrew-direct, my terminal, mid-turn).** VERBATIM: *"Yes MSTR shoudlve spawned you as
2.0.0_SA_COO~Z but they used the extra 2.1.0_SA_COO identity, which is fine, no need to change that at
this point just run it as 2.1.0_SA_COO as youre already running. With that said, yes you are exclsively on
the CORE side of NFRA_VELOCITY, 2.0.0_SA_COO is handling the other fabric on the ESTATE side."*

I had inferred from two gates that `2.1.0_SA_COO` was a CompLearns serial and that the site-Z convention
implied `2.0.0_SA_COO~Z`. **The convention inference was right and the conclusion was wrong** --
`2.0.0_SA_COO` is a LIVE PEER running the ESTATE half of this same decomposition (`e3d9d31e0`,
`8396b9b78`), and one commit attempt I made under `2.0.0_SA_COO~Z` was authoring under a live peer's
serial. It was blocked by the owned-paths gate and never landed. Recorded, not dropped. Full record:
`org/tier1_exec/2.1.0_SA_COO/ANDREW_DIRECT_20260731_serial_2.1.0_stands_CORE_exclusive.md`.

**The gate block is real and is now a grantor request at MSTR~Z**, not an identity question: two gates
still classify `2.1.0_SA_COO` as CompLearns (`install-mstr-ledger-check.sh:65` `comp_re`; owned-paths
`lane=COMP_LEARNS`). I am the grantee and do not amend the gate that governs me.

**2. C7 HAS MOVED AGAIN, AND MY OWN C7 TO WAS STALE BEFORE I FILED IT.** My first draft named "schema
round 2, close the five gaps" as the next artifact. Between drafting and filing: **schema v2 landed with
G1-G5 closed** (@5b92f664d, plus an L-16 known-negative companion), **SPEC-3 landed** (@54e54c57e), and
**the registration-invariant join landed** (10:39Z). Verified on disk, not from a message.

**Corrected next artifact: complete the nine-specimen fixture suite (3 of 9 exist) and make it green.**
The sequencing reason is load-bearing: **the migration points ~90 tools at this schema, and L-16 -- landed
today by CTO~Z -- says an EXERCISED instrument is not a DISCRIMINATING one.** The nine specimens are the
schema's known-negative set. Migrating the estate onto a contract whose discrimination is unproven would
bake an undiscriminating contract into a gate, and SPEC-3 is literally
*validated-on-a-non-discriminating-input*. **Prove it discriminates on nine, then migrate.**

**3. THE C8 FINDING STRENGTHENED WHILE I WROTE IT UP.** Since my measurement: **L-16 landed** (@8ed2fde1e)
and CTO~Z then **declined to mint L-17, recording an instance under L-1 instead** (@0e1ea5e7c, *"I ruled an
enum gap from a token list without reading the definitions"*). **That decline is the correct reflex and it
is exactly what the C8 TO institutionalizes** -- the workstream is now self-correcting on law-count
inflation, but `MECHANISM_LAWS.md` still does not exist and `docs/doctrine/` is still byte-for-byte
unchanged. **The restraint is real; the collapse is still unstarted.** The TO authorizes the collapse and
zero new laws.

### What this addendum is evidence of

Three of my own inputs went stale inside one composition window -- a summary I was handed, a TO I drafted,
and a measurement I published. **On a fabric committing at this rate, a plan of record is stale on
arrival, and the correct response is to pin state to disk and commits rather than to re-summarize.** Every
TO filed here carries its state pinned that way, and the C7 TO says in its own notes that if the pin is
stale again, that staleness is itself the report.

---

## CORRECTION -- CVO~Z tested my C8 claim and my prose was too harsh

I flagged this myself as the weakest point in the assessment and asked CVO~Z to hit it. It did, at source.

**What I wrote:** the staged L-ids are *"plausibly the same mechanism under a new name."*
**What is true, measured:** **~10 of 13 are NOT in the M-taxonomy** (L-1, L-3, L-4, L-6, L-7, L-8, L-9,
L-10, L-12, L-13). **~3 are genuinely close** -- L-2 ~ M1, L-5 ~ M11, L-11 ~ M14.

**And the reason is CTO~Z's own measurement, not an opinion:** WS-C2 step 0 established that the
M-taxonomy **types WHERE AN ASSERTION SITS and does not type INSTRUMENT FALLIBILITY, by construction.**
The ten uncovered laws are predominantly **control-design laws**. They are not bloat -- **they are the
residual step 0 named, being written down.**

**This changes the finding's framing, and in a way that matters more than the correction itself:**

- **What STANDS, independently re-derived by CVO~Z:** `MECHANISM_LAWS.md` is ABSENT; `docs/doctrine/`
  holds 7 files, none of them the collapse. **The collapse has not started.** That was and remains the
  load-bearing fact, and it is why the TO is pointed where it is.
- **What I withdraw:** the accumulation framing. A workstream writing down a *measured taxonomy gap* is
  not a workstream running backwards. The law-count growth was the visible thing and I read it as the
  defect; the invisible thing -- that most of the growth was legitimate new content -- was the part that
  needed measuring, and I asserted instead of measuring it.
- **What this SURFACES, now routed to CTO~Z as a scope question:** if ~10 staged laws are genuinely
  outside the corpus C8 collapses, then **`MECHANISM_LAWS.md` may need a second section, or the
  control-design laws a separate home.** The PRD scopes C8 to collapsing the 14. That scope may be one
  section short. **That is a design call and it is CTO~Z's, not mine and not the build seat's.**
- **What survives unchanged:** the TO. It defers the merge behind a dedup pass rather than presuming
  redundancy, so it holds under this answer exactly as designed -- and the dedup pass is now
  **quantified at ~3 rather than asserted over the set.**

**CVO~Z declared a conflict before ruling:** it authored or co-produced several of the laws it judged
(L-1, L-3, L-5, L-6, L-7, L-8, L-9), and marked its own verdict **UNVALIDATED-REUSE** pending a seat that
did not author them -- per its own A10.4 remedy. **So the ~10/~3 split is the working figure with that
caveat attached, not a settled one.** Base CVO's cross-seam pass is the named route. I am carrying the
caveat into the TO rather than quietly promoting the number.

**Two other review outcomes, recorded so the file is not just my own account:** CVO~Z supported the C7
re-point on **ratified** grounds rather than as a preference -- **A11.1: an invented oracle that accepts
the existing corpus is indistinguishable from a ratified one, until something that should fail passes**,
and after a migration the discrimination question becomes *unanswerable* because every tool passes and
passing looks like evidence. And it confirmed the denominator handling on my commit census was correct
*because* I labelled it, not despite it.
