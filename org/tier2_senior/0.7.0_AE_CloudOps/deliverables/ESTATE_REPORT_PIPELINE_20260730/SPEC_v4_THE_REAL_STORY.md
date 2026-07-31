# ESTATE REPORT v4 -- THE REAL STORY (ruling 7 delta)

**Author:** `0.7.0_AE_CloudOps~B` · **Approver:** `3.0.0_SA_CVO` · **Date:** 2026-07-31
**Status:** DELTA SPEC FOR APPROVAL. v3 build PAUSED at a clean point. No build motion.
**Delta against:** `SPEC_v3_CORPUS.md` @32580af5f2. Ruling 7 @66c83fd8e3.

---

## 0. The product changes, not just the corpus

Andrew ruling 7, VERBATIM core: *"every single text of user input from me into a terminal session
needs to be tracked somewhere on a day by day basis. that that text store, in addition to git co
change, in addition to deployment motion, needs to be synthesized athletically with considerable
meta analysis and judgment to get to the real story. the real story is less than 1000 characters a
day... the 5-10 sentences that actually mattered and a couple reference pointers. Those few
sentences are what id feedback."*

**The deliverable is now THE STORY.** The nugget census becomes internal means. Ruling 6's curated
surfaces (`RULINGS_LEDGER`, `SEMANTIC_NOTES`) are **derived records**; ruling 7 demands the **raw
feed they derive from**.

---

## 1. THE CAPTURE LAYER -- and the measured reason the obvious build is wrong

**Source:** harness session transcripts, `~/.claude/projects/<project>/*.jsonl`. **314 for this
project/device.**

### 1a. THE FINDING THAT IS THIS SECTION'S SPINE

Measured against ground truth I personally hold (I was in the session; Andrew sent me **five**
messages):

| How it arrived | Stored as | Count |
|---|---|---|
| turn boundary | `type: user` (+ `last-prompt`) | **2 of 5** |
| **MID-TURN** | `type: queue-operation` + `attachment` — **never `user`** | **3 of 5** |

**A naive `type == "user"` extractor captures 40%, and simultaneously admits skill bodies, system
reminders, task notifications and tool_results as if Andrew had typed them.** False negatives and
false positives at once.

> **THE 3 IT DROPS ARE THE HIGHEST-SIGNAL MESSAGES IN THE SESSION** — ruling 4 (*"WE could have an
> EC2 do this with autostart implementation"*), ruling 4a (the >900s rationale), and the standing
> hold. **The entire compute-architecture decision of this build arrived mid-turn.** A pipeline on
> the obvious row type would have omitted the rulings that determined the pipeline, while looking
> complete — because the turn-boundary messages it *did* capture are perfectly real.

Not an edge case: across the 40 most-recent transcripts, `queue-operation` appears in **40 of 40**
sessions and `attachment` in 39 of 40.

### 1b. Correct extraction

Union of `user` + `queue-operation` + `attachment`, **de-duplicated**, then filtered for genuine
human text. The filter is ruling 6's **fail-closed three-way provenance, one layer lower** — and
here the forgery risk is industrial, because the raw feed is far too large for anyone to eyeball.
`HUMAN` / `HARNESS` / `UNCLASSIFIED`; anything unrecognised is **never admitted as Andrew's words**.

### 1c. CAPTURE FIXTURE (CVO (1)) — a permanently-armed regression test

Replay **this session's transcript**. Extraction MUST yield **exactly Andrew's 5 texts**, all 3
mid-turn ones present, and **zero** skill bodies / system reminders / tool_results. Known
denominator, known split, known content, participant-held ground truth. **That makes the 40%
failure mode impossible to reintroduce silently.**

**SECOND CAPTURE FIXTURE, created by the finding itself (ruling 7a, @1c3d953180).** Within minutes of
my reporting this, Andrew sent CVO **two more sovereign rulings — BOTH MID-TURN**: confirmation of the
R7 reading this spec is built against, and the prompt-embedding mandate in §3.5. **The finding
predicted the failure and the fabric immediately produced two more instances of it, at a different
terminal, in a different session.** CVO's transcript for today is therefore a second replay fixture by
construction. Two independent fixtures, two devices' worth of sessions, one failure mode.

### 1d. COVERAGE DENOMINATOR, stated in every day's manifest

`314 transcripts` is **this device, this project**. A laptop-only day is a **true partial, not a
complete day**. **Site-Z is a DECLARED GAP** until its capture path exists (gate already at Andrew).
A story built on a partial corpus says so on its face.

---

### 1e. PERSISTENCE CONTRACT (CVO binding addendum, 015119Z)

Ruling 7 says the input must be *"tracked **somewhere** on a day by day basis"* and v4 never named
the somewhere. Naming it:

**(a) HOME + GRAMMAR — ANDREW-DIRECT, mid-turn ~0155Z, VERBATIM (supersedes my proposal):**

> *"where it would be, would be the same bucket where kimi tracks the change logs and other story
> details"*
> *"should be a daily sub folder in there for text-input, change-cochange, deployment-motion,
> kimi-report, signed-review, something like this"*

**DAY-FIRST, with one subfolder per artifact class.** This replaces my class-first
(`input/YYYY/MM/DD/`) proposal — his layout puts the *day* at the top, which is right, because the
unit of this whole product is a day and every consumer asks "what happened on date X" before it asks
"which class of thing".

```
s3://opal-estate-report/{YYYY-MM-DD}/
    text-input/{device}/{session_id}.jsonl   <- the capture store (§1)
    change-cochange/                          <- synthesis input (b): git change AND CO-CHANGE
    deployment-motion/                        <- synthesis input (c)
    kimi-report/                              <- THE STORY (was daily/)
    signed-review/                            <- Andrew+CVO's ratified output (was adjudicated/)
```

`{device}` stays inside `text-input/` — coverage is device-scoped today (site-Z is a declared gap,
§6.1), so a partition that cannot express "which device" makes a partial day indistinguishable from a
complete one. **The key itself carries the denominator.**

**"change-cochange" IS AN INSTRUCTION, not a folder name.** Ruling 7 said *"git co change"* and I read
it as "git change"; this names it twice. **CO-CHANGE — what moves TOGETHER — is a required analytic,
not a synonym for change.** Two files that always change in the same commit are coupled whether or not
any graph says so, and that coupling is exactly the kind of tribal knowledge no artifact declares.
Folded into input (b) as a stated requirement.

**"signed-review" is a better name than my "adjudicated"** and I am adopting his: *signed* names the
act that matters — a human put their name to it — where *adjudicated* only names that a decision
occurred.

**IAM consequence, stated because the shape changed:** the boundaries are now MID-KEY wildcards
(`arn:aws:s3:::opal-estate-report/*/signed-review/*`, `.../*/text-input/*`) rather than leading
prefixes. S3 supports mid-key `*`, so every boundary in (b) below survives the restructure — but each
one must be RE-EXERCISED against the new pattern, because a policy that was correct under a leading
prefix is not thereby correct under a mid-key one. A5's deny-test is re-run, not assumed.

**(b) IAM BOUNDARY — and this store gets a HARDER rule than `daily/`.**
This is **the primary record of Andrew's words.** Anything that can silently rewrite it can rewrite
what he said, and no downstream reader could tell.
- capture role: `s3:PutObject` on `input/*` **only**.
- **EXPLICIT DENY on `s3:DeleteObject` + `s3:DeleteObjectVersion` for `input/*`** — the producer
  cannot delete or rewrite history it has already written. Deletion stays human-reserved.
- versioning is already ON bucket-wide, so even a same-key rewrite is recoverable rather than
  destructive.
- the **story builder READS `input/*` and WRITES `daily/*`** — different prefixes, and the pointer
  **validator resolves against `input/*` INDEPENDENTLY**, never against the builder's index. That is
  CVO's validator law expressed as a prefix boundary rather than a convention.

**(c) DE-DUP KEY.** `sha256(session_id + "\x1e" + normalized_text)`.
**Required, not hygiene:** a single mid-turn message appears in **both** the `queue-operation` and
`attachment` row classes (§1a), so the union that fixes the 40% miss *guarantees* duplicates. Keying
on a row `uuid` would fail — the same utterance carries different ids across row types. Normalization
is whitespace-collapse only; **never case-fold or strip punctuation**, because the stored text is
evidence and must stay byte-faithful to what he typed.

**(d) RETENTION — rides the open Andrew ruling (§6.3), and RAISES ITS WEIGHT.**
No lifecycle rule, consistent with the rest of the bucket. But flag plainly: **that open ruling now
governs the retention of Andrew's own verbatim words, not just derived reports.** A lifecycle rule
applied here would delete primary evidence. The store grows unbounded until he rules; that is a
deliberate choice, stated, not an oversight.

---

## 2. THREE SYNTHESIS INPUTS

**(a) user-input store** (§1) · **(b) git change** — re-admitted from appendix; the attribution
bridge already built and exercised serves it · **(c) deployment motion** — new, and **measured
before speccing**:

| Source | Kind | MEASURED daily reach |
|---|---|---|
| `org/critical_paths/change_management/*.md` | **INTENT** | 408 total, **41 in 7 days** (~6/day) — the richest daily signal |
| git tag history | **INTENT** | **10 in 7 days** (~1.4/day) — sparse, high-confidence (a tag *is* a completed deploy) |
| `EC2_MANIFEST.services.*.deployed_at` | **STATE** | **12 of 28 services carry it**; newest besides my own write is **2026-07-24** — 6 days stale |
| `lambda-source-map` `artifact_sha256` / `_last_deploy_recorded` | **STATE** | 156/194; last recorded **2026-07-29** — 2 days stale |

**CVO's prior confirmed and sharpened: intent records carry daily motion; state records are PARTIAL
and LAGGING.**

> **AND THE DISAGREEMENT IS THE STORY, exactly as CVO predicted.** 41 completion entries vs 10 tags
> vs a source-map last-recorded two days ago. These three should roughly agree about how much
> deployed this week. **They do not, and that gap is a high-leverage story sentence** — not noise to
> reconcile away.

⚠ **HONESTY NOTE ON MY OWN MEASUREMENT:** the newest `deployed_at` in EC2_MANIFEST
(`2026-07-30T23:35:00Z`) is **my own write from tonight**. I must not read my own write as evidence
the registry is current — with it excluded, the record is 6 days stale. Same class as every other
defect this session.

---

## 3. OUTPUT CONTRACT -- two layers (CVO POINTER RULING)

### SURFACE — keeps Andrew's stated shape, verbatim
**< 1000 characters. 5-10 sentences that actually mattered. A couple of reference pointers.**
**NO per-sentence citations on the prose.** He asked for a high-signal read; a citation thicket
trades that away for a property we hold elsewhere.

### SUBSTRATE — harder than I proposed
Every sentence carries, **in the JSON**: its `basis` class (ruling 6 classifier), resolvable
`source_pointer(s)` into the capture store / git / deployment record, and the **verbatim behind any
quote**. Validated **FAIL-CLOSED at build time**: **a sentence that cannot ground DOES NOT SHIP —
the story SHRINKS rather than asserts.**

> **THE VALIDATOR MUST NOT SHARE A FAILURE MODE WITH THE BUILDER** (CVO, binding). It resolves every
> pointer **independently against the store**, never against the builder's own index of what it
> wrote. A validator reading the builder's bookkeeping would confirm the builder's own belief and
> pass a fabricated pointer. *This is the first time tonight this law is applied BEFORE the failure
> rather than after it.*

**Compression is ~100:1 against this session alone. Everything the story omits is invisible to its
reader BY DESIGN — so the pointers are a SAFETY PROPERTY, not a convenience:** they are the only
path from the story back to what it dropped.

---

## 3.5. THE PROMPT ARTIFACT — Andrew's own words go in front of Kimi, every day (ruling 7a)

Andrew-direct, VERBATIM: *"also this text block here {the story} is extremely important text block,
kimi should see it every day when constructing the report"*.

**The daily prompt EMBEDS the ruling 7 verbatim block ITSELF — not a paraphrase, not a distilled
instruction, not my summary of what he meant.** His definition of the real story IS the instruction.

**WHY THE VERBATIM AND NOT MY PARAPHRASE, stated so nobody later "cleans it up":** every rewrite of a
sovereign instruction is a lossy re-encoding by an agent who was not the author. A paraphrase drifts
across edits and **nothing downstream can detect the drift, because the paraphrase reads perfectly
well.** This is `org/XXX.md`'s record-verbatim law — **the phrasing IS the ruling** — applied to a
prompt instead of a ledger.

**VERSIONED AND TRACEABLE (my addition, required by the above):** the block is a **versioned artifact
with a content hash**; every report records `prompt_version` + `prompt_sha` in its manifest, so any
day's story is traceable to the EXACT block that produced it. Without it, a silent prompt edit
redefines "the real story" with **no visible discontinuity in the output** — a frozen-map dependency
wearing a prompt's clothes.

Ruling 7a also confirms **(1)** CVO's R7 reading — which this spec is built against — as sovereign,
and **(2)** the capture layer as **its own sovereign mandate**, not an implementation detail of the
story. §1 is therefore a deliverable in its own right and survives any future change to the story
format.

---

## 4. Acceptance

1. **CAPTURE FIXTURE** (§1c) — exact-5 replay, both directions.
2. **etfs-canonicality** — must surface in or behind the story, **both sources** (measured: 6 ledger
   rows AND 2 notes blocks; a one-file replay half-passes and looks like a pass).
3. **opal-data-mdpf decommission-intent** — 12 ledger rows, **0 notes blocks**; a different
   distribution, so "both sources" is fixture 1's property, **not a universal law**.
4. **POINTER VALIDATION** — every shipped sentence resolves independently; a deliberately-corrupted
   pointer must FAIL the build, not warn.
5. **SURFACE BUDGET** — machine-checked `< 1000 chars`, 5-10 sentences.
6. **PROMPT PROVENANCE** — the R7 verbatim block is present in the SENT payload **byte-for-byte**
   (assert on the actual request body, not on the template — the template is the builder's own index
   of what it believes it sent), and `prompt_sha` in the manifest matches it. A drifted or
   paraphrased block FAILS the build.
7. **CAPTURE FIXTURE 2** — replay CVO's session; ruling 7a's mid-turn messages must all survive.
   **Denominator pinned AT DAY CLOSE, not now** (CVO note 1): that session is still accruing — a
   THIRD mid-turn sovereign instruction landed after this spec was written. The fixture is specified
   as a **MUST-INCLUDE SUBSET** (these known utterances must be present) rather than an exact count,
   which is precisely why it survives the day continuing to grow. An exact-count assertion written
   mid-day would have gone red for the correct reason and been "fixed" by loosening it.

### Sentence-boundary rule (CVO note 2) — stated so AC5 is deterministic

A naive `.`-split is fooled by abbreviations and decimals, so "5-10 sentences" would be
non-deterministic and the budget check would pass or fail on formatting noise. **Rule: sentences are
split on `[.!?]` followed by whitespace + an uppercase letter or end-of-string, with a
non-splitting exception list** (`e.g.`, `i.e.`, `etc.`, `vs.`, `approx.`, `No.`, single capital +
`.`), **and decimals `\d\.\d` never split.** The rule ships as a named function with its own unit
fixtures, because a budget enforced by an undefined counter is not enforced.

---

## 5. Salvage (CVO-approved split)

**Unchanged:** `classify_basis` 3-way fail-closed (exercised, 117 rows, ordering trap held) · the
entire runner substrate (fire-and-forget, autostart, self-stop, dead-man, manifest contract v2, IAM
boundary, fail-soft AI split, C1 window marks, supervisor journal) · coverage-denominator discipline.
**Demoted to internal means:** the ruling-6 nugget census. **Re-admitted:** git census + attribution
bridge as input (b). **New:** capture layer, deployment motion, story contract + validator.

---

## 6. Open at Andrew

1. **Site-Z capture path** — a declared gap; without it "every single text" is device-scoped.
2. **Desktop world-model repo has no remote** — mirror cadence = corpus freshness for input (b)'s
   derived records.
3. **Retention ruling** on `opal-estate-report`.

-- `0.7.0_AE_CloudOps~B`
