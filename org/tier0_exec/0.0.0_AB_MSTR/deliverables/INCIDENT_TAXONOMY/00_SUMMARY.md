# INCIDENT TAXONOMY — SUMMARY

    author:      0.0.0_AB_MSTR~Z · 2026-07-29
    commission:  Andrew-direct ~2010Z ("create an incident taxonomy ... really drill down on a way to
                 classify these things, because we want to reverse engineer the nature of what is
                 challenging the agents") + ~2035Z ("run the taxonomy separately per document, then
                 a summary document with the summary stats and info")
    scheme:      AXES.md (9 axes)
    per-doc:     01..11 in this directory
    corpus:      286,395 B of doctrine + references + RAVC  ·  PLUS  4,388,163 B / 27,993 lines of
                 comp-tool telemetry
    classified:  210 incidents across 10 prose documents + 26,235 parsed telemetry rows

---

## 1. THE DOCUMENTS

| # | document | bytes | edits/14d | incidents | N-SELF | verdict |
|---|---|---|---|---|---|---|
| 01 | `doctrine/CONTROLS_OVER_CARE.md` | 94,959 | **27** | **76** | **11** | collapse §III-* |
| 02 | `references/INCIDENTS_2026-07-13.md` | 71,389 | 0 | **48** | 8 | KEEP entire |
| 03 | `doctrine/INSTRUMENTS_AND_AXES.md` | 24,236 | 8 | 25 | 2 | KEEP, promote §9 |
| 04 | `doctrine/INTENT_DENOMINATOR_SYNC.md` | 28,707 | 10 | 18 | 4 | **PROMOTE TO HEAD** |
| 05 | `doctrine/A_VALUE_MUST_CARRY_ITS_CLAIM.md` | 8,692 | 1 | 17 | 1 | KEEP untouched |
| 06 | `doctrine/CHECK_LIVE_NOT_FROZEN.md` | 5,575 | 3 | 6 | 1 | KEEP, merge law w/ 04 |
| 07 | `doctrine/TRIGGER_LAYER.md` | 4,138 | 1 | 4 | **0** | KEEP — the template |
| 08 | `references/MDPF_POSTMORTEM_20260722.md` | 9,481 | 0 | 12 | 1 | KEEP entire |
| 09 | `references/INCIDENTS_2026-07-21.md` | 7,089 | 0 | 3 | 1 | KEEP entire |
| 10 | `org/ref/RAVC_PROTOCOL.md` | 7,921 | **1** | **1** | **0** | KEEP UNTOUCHED (Andrew-ruled) |
| 11 | `org/compiler-tools-log.md` | 4,388,163 | (append-only) | 26,235 rows | — | fix the result column |

**Not classified:** `doctrine/README.md` (1,593 B) and `references/README.md` (1,717 B) are indexes.
**One defect found in passing:** `doctrine/README.md`'s Contents section names **only**
`CONTROLS_OVER_CARE.md` while the directory holds **seven** files. *The index of the doctrine corpus
is stale against its own corpus* — M4, in the file whose job is to say what exists.

---

## 2. AGGREGATE DISTRIBUTIONS (n = 210)

### 2.1 MECHANISM — the axis the corpus does not have

| code | mechanism | n | share |
|---|---|---|---|
| **M6** | AXIS / GRAIN MISMATCH | **42** | 20% |
| **M1** | **SHARED DENOMINATOR** | **29** | 14% |
| **M2** | SHAPE-MATCH, WRONG CONTENT | **22** | 10% |
| **M5** | SCALAR COLLAPSE | **22** | 10% |
| **M14** | PROSE-AS-CONTROL | 19 | 9% |
| **M8** | TEXT vs SEMANTICS | 16 | 8% |
| M7 | SELF-REPORT AS POINTER | 14 | 7% |
| M11 | TAUTOLOGY | 14 | 7% |
| M9 | DESIRED vs APPLIED | 11 | 5% |
| M3 | PROXY FOR THE THING | 10 | 5% |
| M10 | UNREACHED BRANCH | 7 | 3% |
| M4 | COPY DRIFT | 6 | 3% |
| M12 | BORROWED SENSITIVITY | 5 | 2% |
| M13 | POLARITY INVERSION | 2 | 1% |

> **FOUR MECHANISMS — M6, M1, M2, M5 — CARRY 115 OF 210 INCIDENTS (55%).**
> **Fourteen mechanisms carry all of it.** The corpus is 286KB of prose organised by *when things
> happened*; it has fourteen underlying shapes and no file groups by them.

### 2.2 EPISTEMIC TYPE

E1 FALSE-CLEAN **133 (63%)** · E2 FALSE-ALARM 20 · E3 WRONG-VALUE 14 · E4 WRONG-OBJECT 13 ·
E6 STALE-TRUE 9 · E7 OVER-CLAIM 12 · E5 WRONG-GRAIN 7 · E8 UNFALSIFIABLE 1

### 2.3 FAILURE DIRECTION

| direction | n | share |
|---|---|---|
| **X-CLEAN** (fails toward PASS) | **168** | **80%** |
| X-DESTRUCTIVE (the remedy harms) | 25 | 12% |
| X-LOUD (self-correcting) | 17 | 8% |

### 2.4 DETECTION — the number that should change what we build

| mode | n | share |
|---|---|---|
| `D4` somebody READ the thing | **119** | **57%** |
| `D2` positive control / mutant / ablation | **55** | **26%** |
| `D3` arithmetic / expectation mismatch | 13 | 6% |
| `D7` not caught in-window | 9 | 4% |
| **`D1` a DESIGNED CONTROL FIRED** | **5** | **2.4%** |
| `D6` taste / accident | 3 | 1.4% |
| `D5` sovereign (Andrew) | 2 | 1% |

### 2.5 RECURRENCE

**`N-SELF` = 29 of 210 = 13.8%** — the rule violated by its own author, inside its own document, or
by the very control built to catch it.

---

## 3. THE FIVE FINDINGS

### FINDING 1 — Agents fail at the BOUNDARY OF THEIR OWN OBSERVATION, not at reasoning

M6+M1+M5+M10+M11 = **114 of 210 (54%)** share one shape: **the agent reasoned correctly from a scope
chosen for it by something that shared the defect.** The expectation set came from the data; the axis
came from a tool's default projection; the target came from the subject's own `source_field`; the
denominator came from the configuration being audited.

**An agent cannot see the edge of its own sample.** Care operates *inside* the sample — which is why
the two things that actually catch these (positive controls, printed denominators) are the only two
acts that probe *outside* it.

The corpus already contains the derivation, in **file 04 §2**, and **nothing points at it.** CLAUDE.md
Rule 22 points at file 01, which has the instances and calls the pattern *"the third anti-correlated
instrument"* — a coincidence noticed three times rather than a law.

### FINDING 2 — Green is structurally unsafe here, and we treat it as neutral

**80% X-CLEAN. 63% E1.** Absence has no signal of its own; it inherits the signal of whatever
summarised over it. Every scalar — a count, an rc, a bool, a PASS, a queue depth, a zero — discards
exactly the thing being asked about.

**The telemetry confirms it behaviourally:** 87.33% of 26,235 real invocations returned PASS, and
the estate's most-run tool (39% of all activity) has moved off PASS **15 times in four months**.

### FINDING 3 — Naming a failure mode does not prevent it. 13.8% self-violation is the proof

29 of 210 incidents were committed **by the author of the rule, in the document stating it, or by the
control built to catch it.** Not by careless agents — by the most careful ones, at the moment of
maximum attention.

**The corpus's own growth is therefore evidence against its method.** File 01 grew **27 times in 14
days to 95KB**; its self-violation rate is the **highest in the corpus (11 of 76)**. File 10 (RAVC)
was edited **once**, records **one** incident, and has **zero**.

> **The writing IS the relief, and the relief is the problem — it discharges the urgency that would
> otherwise have produced a gate.**

### FINDING 4 — We are not building the thing that catches things

**`D1` = 2.4%.** Designed controls caught five incidents out of 210. Reading caught 119; deliberately-run
positive controls and mutants caught 55.

**File 07 (TRIGGER_LAYER) states the consequence as law** — *"a finding that cannot fail a gate is a
diary entry"* — **and file 08 supplies the price:** a defect was written down **verbatim, in the right
file, eleven weeks early**, inside a tool wired to the live universal commit gate that ran thousands
of times, and it **could stop nobody** (wrong axis, wrong language, wrong artifact). It cost a quarter.

**The estate's own postmortem already ruled on this and the ruling has not propagated:**
> *"THE RECURRING FAILURE IS NOT MISSING INSTRUMENTS. IT IS INSTRUMENTS THAT EXIST, ARE CORRECT, AND
> HAVE NO TRIGGER."* — and, under **What NOT to build: more detectors.**

### FINDING 5 — The telemetry falsifies the improvement narrative, using the doctrine's own rule

Aggregate FAIL rate fell **12.14% → 6.14%**. Decomposed per-series (as `CONTROLS_OVER_CARE` §III-b
requires): **`comp-blast` went 0.99% → 37.88%. `comp-iam` went 0.00% → 5.43%. `comp-pipescript` is no
better than April.** The headline fell because `comp-surface-check` — 0.15% FAIL — went from **0% to
~43–50% of all volume**.

**A clean headline over offsetting moves.** The exact defect §III-b names, sitting unexamined in the
estate's own behavioural record for three months.

**And the deeper problem underneath it:** the `FAIL` column conflates *deliberate negative-control
probes*, *tool usage errors*, and *genuine findings*. **The estate cannot currently answer "are we
getting better?" in either direction** — not because the answer is bad, but because the instrument
that would answer it has a two-meaning null in it.

---

## 4. CROSS-DOCUMENT STRUCTURAL FINDINGS

**4.1 — Size is inversely correlated with health.** Ranked by edits-per-14-days: 01 (27 edits, 11
N-SELF, 95KB) … 10 (1 edit, 0 N-SELF, 7.9KB). **The two files with zero self-violations are the two
smallest** (07 at 4.1KB, 10 at 7.9KB). The largest file has the most.

**4.2 — Sedimentation has a signature: sub-sub-numbering.** File 01 grew `III-a … III-g`; file 03
grew `7a … 7f` then `7f.1 … 7f.3`. **When a doctrine file starts growing letters after its numbers,
it has stopped being doctrine and started being an append log.** File 01's §III family is **65% of
the file**; III-d alone is **33.5%**.

**4.3 — The doctrine/reference split works, and only the reference side obeys it.** Files 02, 08, 09
are dated, unedited since authoring, and correctly placed — exactly as `references/README.md`
specifies (*"Ages: Never — it is the record"*). The **doctrine** side inlines its incidents instead of
linking them. **File 07 is the only doctrine file that follows the doctrine spec.**

**4.4 — One law is currently split across three files.** *A record with teeth outlives its authority*:
file 03 §7e (tests asserting a retracted prohibition), file 01 #46 (`RETRACTED_*` byte-identical to
`PROD_WRITE_FORBIDDEN_*`), file 01 #55 (the stale caveat that under-bounds). Three files, one law.

**4.5 — The corpus has exactly one positive exemplar and one preventive technique**, both in file 05:
`meta.cottonwood_fold` (*"this is the shape to copy"*), and *write the forbidden shortcut into the
control* (ask **"what is the easiest way to make this pass?"**). **In 286KB, one page tells you what
right looks like and one paragraph acts before the incident.**

**4.6 — The corpus systematically under-records the destructive direction.** X-DESTRUCTIVE is **25% in
file 02** (the source night) and **12% overall** — the distillation into doctrine lost that weighting.
File 01 reads as being about false greens; its source is substantially about **false reds whose remedy
was restart / kill / delete**.

---

## 5. WHAT THIS LICENSES — the prune, by taxonomy rather than by judgment

**No cuts have been landed. Andrew ruled RAVC and "items in verification" as KEEP, and ruled that
nothing he called good is cut without his word.**

| move | effect | evidence |
|---|---|---|
| **COLLAPSE file 01 §III-a…III-g into the 14 M-classes** | ~707 lines → 14 laws + a 210-row instance table. **Deletes nothing** — instances become rows | §2.1 |
| **PROMOTE file 04 to the head of the corpus; re-point CLAUDE.md Rule 22 at it** | it derives the law the rest rediscover 29 times | file 04 §2 |
| **MOVE file 01 §III-d (426 lines) to `docs/references/`** | it is a dated record; the split's own rule puts records there | §4.3 |
| **MERGE the three copies of "records with teeth outlive their authority"** | 3 files → 1 law | §4.4 |
| **PROMOTE file 03 §9 (THE CHECK) and file 05 Corollaries 1+3** | the corpus's only pre-flight and its only preventive technique | files 03, 05 |
| **USE files 07 + 10 as the compression template** | rule → mechanism → binds → boundary → **link out** | §4.1 |
| **FIX `doctrine/README.md`'s Contents** | it lists 1 of 7 files | §1 |
| **FIX the telemetry result column** | highest-value single change; without it "are we improving?" is unanswerable | §3 F5 |

> **Why taxonomy beats deletion, stated once: a deletion pass cuts INSTANCES and keeps IMPERATIVES —
> exactly backwards. The imperatives are near-duplicates of one another; the instances are the
> measurements, and they are irreplaceable. Collapse the prose, keep the evidence.**

---

## 6. THE ONE VALUE QUESTION — Andrew's alone

**Is this corpus written to PREVENT incidents, or to METABOLISE them?**

Both are legitimate. They imply opposite documents.

- **PREVENTION** → the artifact is 14 laws, a test per law, a gate where possible, instances as
  evidence rows. Optimised for an agent *about to act*. **It should be small, and it should SHRINK as
  gates absorb classes.**
- **METABOLISM** → the current document is already correct. Writing an incident up in full, with the
  author's own confession, is how an agent processes having been wrong. **The length is the point and
  the audience is the author. It should be large and only grow.**

**The measurements say we are doing METABOLISM while believing we are doing PREVENTION:**
- 27 edits in 14 days on the primary file, with **no fall in its self-violation rate**
- **`D1` = 2.4%** — the prevention layer is not where the catches come from
- the corpus's own postmortem already ruled *"what NOT to build: more detectors … the gap is the
  TRIGGER LAYER"*, and 168KB of doctrine has been written since without a corresponding gate count

**That is coherent to do on purpose and expensive to do by accident.** Everything in §5 follows from
this one answer, and I have not assumed it.

---

*Classification is mine and falsifiable — every row in files 01–10 cites an incident recoverable from
the corpus; every figure in file 11 is reproducible from the parse in that file. **These are counts of
what is WRITTEN DOWN, not of what happened** (AXES.md scope note; file 05 Corollary 4): a floor with an
unknown ceiling. The corpus's own words — "only the loud ones scar."*
