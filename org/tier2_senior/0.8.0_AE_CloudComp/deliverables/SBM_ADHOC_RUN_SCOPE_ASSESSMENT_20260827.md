# SCOPE ASSESSMENT — THE EPHEMERAL SBM AD-HOC RUN

**Task** `1.0.0_SA_CTO~X` msg `76256`, Andrew-authorized, releases this seat for THIS task only
**Lane** `0.8.0_AE_CloudComp~Y` · **Measured** 2026-08-27 17:38–18:0xZ · **Priority** LOW
**Closes** WP-0 RESIDUAL item 1 (`WP0_EVIDENCE_CAPSULE.md`): *"The SBM structural-view producer is
NOT in the repository… Options: locate (it may live outside the repo trees swept) or reconstruct."*
**Scope discipline:** assessment only. **Nothing built, formalized or reconstructed.**

---

## HEADLINE — THE RECORD IS NOT LOST. THE PRODUCER AND THE OUTPUT ARE.

```
  THE RECORD    C:\Users\AndrewBerman\Desktop\C3i_STRUCTURAL_DEFINITION_BRIEF_2026-08-26.md
                27,726 bytes · 534 lines · mtime 2026-08-26T09:32Z
                NEVER COMMITTED -- outside the git worktree entirely
  THE PRODUCER  ABSENT everywhere. No script, notebook, or harness, in or out of the repo.
  THE OUTPUT    ABSENT. No partition, no block assignments, no MDL curve data.
                Every quoted figure exists ONLY as prose.
  THE INPUT     UNIDENTIFIABLE. Its population reconciles with no substrate in the estate.
```

**Andrew's expectation is confirmed and slightly better than expected:** it was purely experimental,
nothing formalized exists, a rebuild must build new — **but the experimental design is fully
documented**, so a rebuild does not start from nothing. It starts from a specification.

---

## 1. WHAT WAS RUN

### 1.1 The producer does not exist — measured four ways

| instrument | result |
|---|---|
| `comp-which` "what runs stochastic block model / MDL block search" | **0 relevant** — top 3 tied at score 1.50, all unrelated (`comp-aws`, `comp-estate`, `comp-pipescript`) |
| filename sweep, `infra/aws/globgrph` · `org/modules/graph` · `.tools` · CVO deliverables | **0** for `sbm`, `block_model`, `fusion`, `consensus`, `stochastic_block` |
| git history, `--diff-filter=A` over `*C3i_STRUCTURAL*`, `*STRUCTURAL_DEFINITION_BRIEF*` | **0 adds** · positive control: `CLAUDE.md` returns its add commit `71236266fe` |
| whole-disk find, repo + Desktop, untracked included | producer **0** · **record FOUND on Desktop** |

**The brief itself names no implementation.** Across 534 lines the only tool token is `comp-estate`
(4 occurrences, in the C3.i id-space section, not the experiment). It is a decision document written
for Andrew in deliberately non-technical language — *"THE EXPERIMENT, IN PLAIN TERMS"*, *"Imagine
transmitting the entire wiring diagram"* — **not a lab notebook.**

**Corroboration, different instrument:** `1.0.0_SA_CTO~X`'s WP-0 capsule reached the same verdict
independently by repo-state audit. This assessment adds the half their capsule left open: **where the
record actually is.**

### 1.2 What the brief says the implementation WAS

> *"degree-corrected stochastic block model implemented directly (numpy/scipy); no SBM library
> present in the estate. Optimiser self-test comparing incremental against from-scratch block
> statistics: **PASS (max deviation 0.000000)** — run before any figure here was quoted."*

Two things worth keeping: the variant is **degree-corrected**, and **a real optimiser control was run
before any figure was quoted.** The experiment was disciplined; it was simply never committed.

---

## 2. WHAT IT CONSUMED

### 2.1 As declared

**Topology axis:** 19,482 nodes · 36,513 edges · 55 distinct node types · `semctl` layer **excluded**
· graph vintage **"pre-nightly 2026-08-26"**.

*The exclusion is a circularity gate, stated on the brief's face: "The layer produced by the old
anchor method was excluded from the input — inferring structure from the previous method's own output
would be circular."*

**Co-change axis:** 27,670 commits parsed · machine co-movement excluded (gate-regenerated /
auto-append paths, which co-move by construction) · **commit-size cap SWEPT (10/25/50) rather than
picked, main run cap = 25** · 3,532 files · 6,393 co-change pairs.

### 2.2 ⛔ AND THE INPUT POPULATION RECONCILES WITH NOTHING IN THE ESTATE

This is the finding that most constrains a rebuild.

```
  the run claims          19,482 nodes / 36,513 edges
  .comp-graph/graph.json   2,249 nodes /  2,947 edges   mtime 2026-08-06   NOT IT
  stitch_graph.json                     43,633 edges    mtime 2026-07-25   NOT IT
  manifest graph_nodes    27,035 nodes (wave projection vintage)           NOT IT
  manifest graph_edges                  58,224 edges                       NOT IT
```

**Independently corroborated by a different seat, during L1, before I looked.**
`0.4.0_DT_ClientPlatform~X` recorded it in their own build scripts:

- `build_l1_cells.py:44` — *"PRD-claimed **19,482 matches NO substrate swept and EXCEEDS the union**"*
- `build_l1_pos.py:125` — *"14,447 over 3 named substrates, **PRD 19,482 UNRESOLVED and not guessed**"*

**That is corroboration rather than repetition** — their instrument was an L1 substrate sweep, mine a
byte-level comparison against four candidate artifacts. Same verdict, different route.

>> **The consequence: the experiment's input is not merely overwritten, it is UNIDENTIFIED. A rebuild
   cannot reproduce the 19,482-node population by pointing at anything that exists today, and nobody
   has been able to say what it was.** <<

---

## 3. WHAT IT EMITTED, AND WHERE THOSE BYTES ARE NOW

**Gone. Every figure exists only as prose.**

```
  comp-find content '694,007'   ->  1 hit  across 27,313 files scanned
                                    NFRA_C3MATERIALIZE_PRD.md:208   (prose table)
  comp-find content '177,474'   ->  2 hits across 27,313 files scanned
                                    PRD:206 (prose) + WP0_EVIDENCE_CAPSULE.md:74 (prose, about the gap)
  comp-find content '694007'    ->  1 hit -- an unrelated financial-sentiment CSV (false positive)
```

**No partition file. No block assignments. No MDL curve data. No seed outputs.** The 256-block
partition that the entire structural argument rests on **does not exist as an object anywhere.**

⚠ **And it could not simply be re-run to recover it** — §5 below.

---

## 4. THE OPINIONS A REBUILD MUST RE-DECIDE

**This is the valuable half of the assessment, and the news is good:** the brief documents the
experimental design thoroughly enough that a rebuild is a re-implementation against a written spec,
not a re-invention.

| decision | what the run chose | status for a rebuild |
|---|---|---|
| SBM variant | **degree-corrected** | documented |
| implementation | direct **numpy/scipy**, no library | documented; `graph_tool`/`igraph` still ABSENT, `numpy 2.4.2` / `scipy 1.17.1` / `sklearn 1.8.0` / `networkx 3.6.1` present |
| search | **randomised greedy** — random start, random visit order | documented |
| search depth | **2 rounds, NO restarts** | documented — **and see §5** |
| B search range | **{64, 128, 256, 512, 1024, 2048}**, minimum at 256 | documented, with the full curve |
| seed policy | **seeds 7 · 23 · 91**; every earlier run used one fixed seed | documented |
| circularity gate | `semctl` excluded | documented, with rationale |
| co-change cap | **swept 10/25/50**, main run 25 | documented |
| co-change filter | machine co-movement excluded | documented |
| optimiser control | incremental vs from-scratch block stats, **max dev 0.000000** | documented, and was run first |
| **partition vs cover** | **not addressed by the experiment** | ⛔ **OPEN** — SBM returns a partition; C3.i is a cover with 540 load-bearing cross-domain memberships |
| **convergence criterion** | not stated | ⛔ **OPEN** |
| **initialisation** | "random start" only | ⛔ **OPEN** |

**The full MDL curve survives in the brief and is worth quoting**, because it is the model-selection
evidence:

```
  B=64  726,815 · 128  701,778 · 256  694,007 (MIN) · 512  698,874 · 1024  715,656 · 2048  740,156
  singletons  0 / 1 / 1 / 15 / 37 / 125   <- the overfitting signature arriving exactly where the
                                             penalty starts to bite
```

Per-seed results also survive:

```
  seed      DL     AMI_vs_type   firm_purity   firm_blocks
     7   694,007        0.144        0.989           48
    23   694,874        0.149        0.996           44
    91   695,063        0.151        0.992           46
  agreement between runs: AMI ~0.505 · ARI ~0.21 · DL spread 1,056 nats (0.15% of best)
```

---

## 5. ⛔ THE ONE THING THIS ASSESSMENT WOULD ESCALATE

**The brief names an ambiguity it could not resolve, and that ambiguity is load-bearing for the whole
C3MATERIALIZE architecture.** Quoted from Result 7:

> *"**WHAT THIS MEASUREMENT CANNOT SEPARATE.** A 0.15% spread across wildly different partitions is
> equally consistent with (a) the landscape is genuinely flat — the wiring does not determine a unique
> partition and no optimiser would resolve it — or (b) **the optimiser is weak (greedy, 2 rounds, no
> restarts)**."*

**Why this matters far beyond the ad-hoc run.** The partition instability (AMI 0.505 across seeds) is
the measured fact that justifies:

- PRD §5.1 — *"a single run cannot carry identity"*
- **L3's entire consensus-fusion approach**
- **L4's signature-matching-over-key design**

**If the instability is (b) — an artifact of a 2-round greedy search with no restarts — then part of
the architecture above it is solving a problem a better optimiser would reduce.** If it is (a), the
architecture is correctly motivated and the consensus machinery is necessary.

**Nobody has separated them, and the discriminating experiment is cheap:** re-run the same fit with
restarts and more rounds, and see whether the cross-seed AMI rises. That is a *measurement*, not a
build. **I am not proposing it as work** — WP-6's rebuild is a separate act on the ISCK contract and
this task is assessment only. I am flagging that the question exists, that it is answerable, and that
its answer changes how much of L3/L4 is load-bearing.

---

## 6. BLAST RADIUS — WHAT A REBUILD MUST RE-DERIVE

**Must be re-derived from scratch (no artifact survives):**

1. The **input graph population** — and first, *identify what it was*; 19,482/36,513 matches nothing
   current and two seats have now failed to reconcile it.
2. The **partition** at B=256 and every block assignment.
3. All **seven results** — every number in PRD §4 "WHAT IS PROVEN" traces to this run.

**Survives and does not need re-deriving:**

4. The **experimental design** — variant, search, B range, seeds, gates, filters, controls (§4).
5. The **findings' interpretation** — including the two-halves reading (partition unstable, findings
   stable) and the library-shelving analogy.
6. The **MDL curve and per-seed table** as historical reference points a rebuild can check itself
   against — *though not as evidence, since the input cannot be reproduced.*

**Newly at risk and worth stating:** PRD §4's proven-claims table is cited throughout the arc as
settled. It is settled **on prose whose producer, output and input are all absent**. That does not
make it wrong — the run had a real optimiser control and its findings reproduced across three seeds —
but it does mean **no instrument in the estate can currently re-check any of it.**

---

## 7. ACCEPTANCE

- [x] every claim carries its instrument and denominator; `comp-find` denominators printed verbatim
      (27,313 files scanned, 13 unreadable, ~1,951 binary — the tool's own exclusions, not mine)
- [x] both controls run where a zero could be an instrument artifact — git-history positive control
      (`CLAUDE.md` returns its add), whole-disk search extended beyond the repo after the repo-scoped
      zero, and the `694007` sweep returning a known-unrelated CSV as a live false-positive check
- [x] **ABSENT verdicts are evidenced, not assumed** — and one of them flipped: the record read
      ABSENT to every repo-scoped instrument and was found on the Desktop
- [x] corroboration named and distinguished from repetition (`0.4.0_DT_ClientPlatform~X`'s L1 sweep
      vs my artifact comparison; `1.0.0_SA_CTO~X`'s repo-state audit vs my history check)
- [x] **NOTHING built, formalized or reconstructed.** No code written, no run executed, no artifact
      created outside this assessment.

**Instrument limits, stated.** (i) A content sweep finds tokens, so a producer that never wrote its
figures into a file and was named nothing recognisable would read as absent — though four independent
routes agreeing lowers that risk. (ii) I cannot see site Z; if the run happened there, this
assessment is scoped to the laptop fabric and says nothing about it. (iii) I did not query the
Iceberg warehouse directly for a 19,482-row projection; I compared against the manifest's recorded
denominators, which are a wave-vintage projection and could differ from the run's own filter.

---

*`0.8.0_AE_CloudComp~Y`, 2026-08-27. Assessment only, per `76256`.*
