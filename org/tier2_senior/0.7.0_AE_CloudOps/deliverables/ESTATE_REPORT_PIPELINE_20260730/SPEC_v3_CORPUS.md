# ESTATE REPORT v3 -- CORPUS CORRECTION: the scan reads USER INPUT, not git

**Author:** `0.7.0_AE_CloudOps~B` · **Approver:** `3.0.0_SA_CVO` · **Date:** 2026-07-31
**Status:** RE-SPEC FOR APPROVAL. Build is STOPPED per CVO 004228Z. Nothing built to this spec.
**Supersedes:** spec-input-5 v2 (the attribution bridge) as the SPINE. See §5 for what survives.

---

## 0. The correction, and why it invalidates a thing that works

Andrew ruling 6, verbatim (CVO record): the git-activity summary is *"useless to an agent who needs
to understand high signal key semantics ... the real semantic and scan needs to be from USER INPUT.
the user input needs to be tracked and scanned for key tribal knowledge."*

His two examples of the target class:
- *"too many opal etfs-tracking AWS resources between S3 and DDB, unclear which is canonical (all of
  them listed in that same convo)"*
- *"opal-data-mdpf is a mistake and should be decommissioned"*

**Both are facts that exist ONLY because he said them.** Neither is derivable from any commit, any
artifact, or any live AWS state. That is the whole point and it is what the v1/v2 corpus could never
have surfaced no matter how good the attribution got.

**THE UNCOMFORTABLE PART, RECORDED BECAUSE IT IS THE LESSON:** last night's pipeline WORKED. It ran
end to end, produced a real report, and I fixed eight defects in it. **A working pipeline on the
wrong corpus is not a partial success; it answers a question nobody asked.** No amount of defect-
fixing inside it would have converged on the right answer, because every defect I found was a defect
in *how faithfully it read git* -- and git was the wrong thing to read. Ruling 6 is a correction one
level above the entire debugging session, and it arrived from the only participant who was not
inside the measurement.

---

## 1. PRIMARY deterministic half -- the USER-INPUT CAPTURE CENSUS

Enumerate the **verbatim-bearing artifacts** that appeared or changed in-window. Deterministic,
compiled, no AI.

| Source | What is extracted | Contract |
|---|---|---|
| `RULINGS_LEDGER.jsonl` (mirror) | rows appended in-window; payload is `ruling` (carries Andrew verbatim in quotes) + `basis` | **CTO's `CORPUS_INTERFACE.md`** |
| `SEMANTIC_NOTES_{s3_buckets,ddb_tables}.md` (mirror) | per-resource `**Verbatim:**` blocks -- *literally what ruling 6 named* | same |
| workspace verbatim records | `ANDREW_RULING_*` / `ANDREW_DIRECT_*` deliverables | XXX.md record-verbatim law makes these greppable BY CONVENTION |
| session logs + inbox messages | `VERBATIM` blocks | same |
| `docs/references/`, `docs/briefs/` | recordings/memos landed in-window | path convention |

Output per capture artifact: path, in-window change type, pointer, and the extracted verbatim
block(s). **Pointers, not summaries** -- the distillation is §2's job.

### 1a. THE CONTROL THAT MATTERS MOST -- filter on `basis`, never on `type`

CTO's interface doc calls this out and it is the single highest-risk item in this spec:
`RULINGS_LEDGER.jsonl` mixes **SOVEREIGN VERBATIM** with **DELEGATED CTO ANNOTATION** (one DDB batch
carries CTO recommendations under Andrew's explicit delegation). Those are **not things Andrew said.**

> **A pipeline extracting "tribal knowledge" that promotes a delegated annotation into an Andrew
> quote would corrupt exactly the signal ruling 6 asks for -- and it would do so invisibly, because
> the output would look like a perfect nugget.** This is the manufacturing-authority failure mode,
> and it is worse than a miss: a missed nugget is absent, a forged one is *believed*.

Implementation: classify every extracted nugget as `SOVEREIGN` or `DELEGATED` from `basis`, carry
that label to the surface of the report, and **never let a DELEGATED item render as a quote.**

### 1b. Declared instabilities I must code against (CTO, measured over 116 rows)

1. `sits_at` / `scope` present on **97/116** -- OPTIONAL, and CTO will not backfill (restamping is
   the mtime-lie class). Never require them.
2. `type` is an **OPEN VOCABULARY** -- 36 distinct values incl. compound forms. **Substring match;
   pass unknowns through.** An exhaustive switch silently drops rows as the vocabulary grows.
3. **APPEND-ONLY WITH RETRACTIONS.** Read *all* rows for an id, honour the most recent. *Several of
   the best findings ARE retractions* -- the trail is evidence, not noise.
4. `id` is human-authored and **not a stable join key.** Substring match only.

---

## 2. Kimi's job -- TRIBAL-KNOWLEDGE DISTILLATION

Over the **content** of §1's artifacts. Per nugget:

- the **quote** (verbatim, unaltered)
- the **resources it names** (the etfs example names a whole set -- the enumeration IS the value)
- the **semantic claim class**: `canonicality-unclear` / `decommission-intent` / `purpose-ruling` /
  `spoken-enumeration`
- the **proposed prose home** + the proposed evolution

**The prose-allowlist control stands UNCHANGED** (`description` / `enrichment` /
`classification(+reason)` only; assembler drops violators and reports the drop). Proposals still
never land -- Andrew ratifies, CVO lands.

---

## 3. Git census DEMOTES to a context appendix

Per CVO (3): keep the code, it is built and honest, it is just not the signal. The attribution
bridge (§5) serves the appendix.

---

## 4. GOLDEN-FIXTURE ACCEPTANCE (the acceptance test that actually binds)

**Replay the day containing the etfs-canonicality conversation. The report MUST surface that nugget
with its resource list.** A pipeline that cannot re-find a nugget Andrew has already named is not
scanning the right corpus, and no other green check redeems that.

**CTO's warning, adopted:** that nugget lives in **BOTH** the SEMANTIC_NOTES verbatim **AND** a
ledger row whose `ruling` field carries the enumeration. **A replay that reads only one file
HALF-PASSES** -- which would look like a pass. Both sources are required for the fixture to count.

Second fixture: `opal-data-mdpf is a mistake and should be decommissioned` -> must surface as
`decommission-intent` naming `opal-data-mdpf`.

---

## 5. What survives from v1/v2 (unchanged, already built and exercised)

Everything structural. Only the corpus changes:
fire-and-forget orchestration · EC2 autostart + self-stop + dead-man ceiling · manifest-first
contract v2 (RUNNING/PENDING/FAILED) · the IAM boundary (producer cannot write `adjudicated/*`) ·
fail-soft AI split with the loud ABSENT marker · scheduled-mark window boundaries (C1) · SET-diff
delta (C2 predecessor search) · supervisor journal to `logs/` · the coverage-denominator discipline,
now applied to **nugget capture** instead of path attribution.

---

## 6. OPEN, and one is now load-bearing rather than an inconvenience

1. **THE DESKTOP REPO HAS NO REMOTE.** The highest-signal corpus lives in
   `C:\Users\AndrewBerman\Desktop\OPAL_WORLD_MODEL\`; my runner reads the **workspace mirror**,
   refreshed by a **manual CTO copy step**. So **MIRROR CADENCE = CORPUS FRESHNESS, and a person is
   in the daily pipeline's critical path.** CTO states plainly that this is *care, not a control*.
   Mitigation I will implement regardless: read the mirror's commit date, **publish it in the report
   as the corpus vintage**, and mark the day `CORPUS-STALE` when it lags the window. That converts a
   silent staleness into a stated one -- it does not fix it. **The fix is a remote. At Andrew,
   raised four times, and my build is now the reason it is load-bearing.**
2. `KIMI_EMPTY` on the last run (200 OK, empty content). **UNDIAGNOSED -- stated as INFERRED:** a
   plausible cause is `max_tokens: 4000` being consumed before visible content on a reasoning-class
   model, but I have **not** confirmed it and will not attribute it without evidence. v3's prompt is
   different anyway; the empty-reply path already renders as a LOUD `AI_SECTION_ABSENT`.
3. Retention ruling on `opal-estate-report` -- still at Andrew.

---

## 7. What I will NOT do before approval

No build. The attribution bridge is **parked**, not extended. The corpus redesign ships first.

-- `0.7.0_AE_CloudOps~B`
