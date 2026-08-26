# SPEC — THE FACE-FLIP CHECK

**A purpose-level specification. WHAT and WHY only. No implementation, no code, no schedule.**

| | |
|---|---|
| **Author** | `0.4.0_DS_ClientPlatform~V` |
| **Issued by** | `2.0.0_SA_COO`, dispatch 73735 (2026-08-26T21:25:45Z) |
| **Sovereign authority** | Andrew, ~21:07Z 2026-08-26, verbatim **"recs approved"** — record `@862b6bf35c`, relayed `1.0.0_SA_CTO` 73693. ⛔ **This spec exists ONLY because of that word.** CLAUDE.md forbids implementing any gate Andrew has not explicitly asked for; absent his approval this document would itself be a manufactured gate. |
| **Measurement vintage** | 2026-08-26T21:19Z–21:31Z, laptop fabric, `origin/CLOUD` at `77a8dcef19` |
| **Status** | SPEC — NOT APPROVED FOR BUILD. Section 6 carries decisions the issuer must make first. |

---

## 0. What this is, in one paragraph

A **lint on the RECORD**. It reads two facts that already exist as artifacts and reports when they
disagree. **It blocks nothing, holds nothing, and writes nothing.** It is not a gate, it is not a
guard, and it has no opinion about whether any work is correct — only about whether the record of
that work contradicts itself.

---

## 1. THE DEFECT — restatable by someone who was not there

**A task order has more than one surface that reports its state, and only one of them is read by
the person deciding whether to dispatch it.**

When a seat finishes a task order it produces up to three artifacts: the **proof-of-spec instance**
(a JSON file of per-criterion verdicts), sometimes a **certification** (an independent verifier's
signed verdict on that instance), and the **TO face** — the `<status>` field inside the task-order
markdown. The first two are *products of doing the work*. The third is *a separate act of writing*,
required by the TO's own reporting clause, and **nothing enforces it.**

So the three can disagree. And they disagree in one specific, always-identical direction:

> **The instance says PASS. The cert says VALID. The face still says ACTIVE.**

**The face is the surface a dispatcher reads.** A dispatcher looking for work to assign opens the
TO, sees `ACTIVE`, and dispatches it. The other two artifacts — the ones that are true — are not on
the path that decision travels. So the record does not merely contain a stale field; **it routes
work using the one field that is wrong.**

### Why this is not a discipline problem

The instinct is to say the dispatcher should check more carefully, or the executor should remember
to flip. Both were said tonight, and both are wrong in the same way: **they move the cost onto the
next reader instead of removing it.** The defect is structural — a required write with no
enforcement will be skipped at some rate forever, and the surface it leaves behind is not marked as
unreliable. A dispatcher reading the one field a TO exposes gets a wrong answer **by construction**,
and no amount of care at the dispatch chair changes that.

### The evidence

**Measured directly by this seat, and the reason the item exists** — `ADVI_STITCH.TO-A1-DS`:
executed by `0.4.0_DS_ClientPlatform~Q` 2026-08-25T21:07Z–2026-08-26T01:48Z, instance 12-of-13 PASS,
certified by `3.0.0_SA_CVO` `@450f313e06` (VALID rc=0, 0 violations). Its face read
`ACTIVE (seating staged)` for **17 hours** afterward. On that face, `2.0.0_SA_COO`'s dispatch 73605
seated a fresh lane on it at 2026-08-26T20:42Z with a full execution brief — re-ground the baseline,
then move objects that were already landed. Re-running it would have rewritten landed legacy objects
(`STI-inv-5` forbids it outright) and rewound a certified deliverable.

**Relayed, not measured by me:** `2.0.0_SA_COO` reports **five** near-miss instances of this shape on
2026-08-26, **two of which reached fresh seats**. I have grounded one of the five first-hand — the one
above. I cite the other four as issuer-relayed and have not independently verified them; they are
consistent with what I measured but are not my measurement. *(Stated this way deliberately: a spec
that argues from a count its author did not take is the relayer defect.)*

**Independently corroborating, measured by me at this vintage:** across the live TO corpus there are
**11 task orders whose proof-of-spec instance is structurally complete — every expected criterion
present, every verdict terminal — while their face still reads an open-ish status.** Section 4 gives
the denominators. I did **not** adjudicate those 11 individually; some may be legitimately open
(section 6, FINDING-3). The number is offered as evidence that the shape recurs at scale, **not** as
a defect count.

---

## 2. THE DETECTION PREDICATE

### The pair of facts

| | Fact | Read from |
|---|---|---|
| **A** | The TO's face reports a state meaning *not yet finished* | the `<status>` element inside the task-order markdown |
| **B** | A completion artifact for that same TO exists and is itself finished | the proof-of-spec instance at the path the TO declares in `<instance_path>`, and/or an independent certification naming that TO |

**The inconsistency is `A AND B`.** Neither fact alone is a finding. The lint reports the
**conjunction**, and reports it as *these two artifacts disagree* — never as *this TO is done*.

### ⛔ The false-positive problem, and why fact B must be strengthened

A lint with false positives gets ignored, and an ignored lint is worse than an absent one — it
occupies the slot a real check would fill. So B cannot be *"an instance file exists."* **An instance
is created early and filled in progressively**; its mere existence is the normal condition of a
healthy, actively-executing TO. Keying on existence would fire on exactly the seats doing their job.

Measured at this vintage, the three candidate strengths of B separate cleanly:

| B is… | Fires | What the fire set means |
|---|---|---|
| the instance **file exists** | **15** | mostly noise — includes TOs mid-execution with partially-filled instances |
| the instance is **structurally complete** — every id in the TO's `<expected_criteria>` present in the instance, every verdict terminal | **11** | plausible, but a complete instance may still be legitimately awaiting certification |
| complete **and** an independent **certification** exists naming the TO | **2** | high confidence — the verdict is not merely claimed by the executor, it has been independently accepted |

**Negative control, run:** `ADVI_STITCH.TO-A1-DS` sat in the strongest class (complete instance +
cert) before its face was flipped, and after the flip its leading token reads `delivered` and it
**does not fire**. The predicate discriminates on the field under test rather than on something
correlated with it.

**Which strength the lint should adopt is a design decision and I am not making it — see FINDING-3.**

### What "a state meaning not yet finished" means, and why it is not settled

⛔ **`<status>` IS FREE PROSE, NOT AN ENUMERATED FIELD.** Measured: **429 distinct `<status>` values
across 1,991 task orders.** Reduced to their leading token — case-folded, with any explanatory tail
after `--` / em-dash / `(` stripped — they collapse to **40 distinct tokens**, of which the populated
ones are `complete` (1,761), `closed` (57), `superseded` (37), `staged` (35), `pending` (17),
`cancelled` (16), `active` (13), `done` (12), `archived` (4), plus a long tail of one-offs that are
whole sentences rather than values.

So a predicate cannot key on *"the status reads ACTIVE"* — that phrasing presumes a vocabulary the
field does not have. **Partitioning those tokens into open and closed is minting an enum, which
dispatch 73735 places out of scope. It is FINDING-1.**

---

## 3. THE FAILURE MODE — Rule 28 q7

> **What does it return when it cannot answer, and is that distinguishable from a clean pass?**

**This is the section the spec lives or dies on**, and it is the issuer's stated first concern. The
reason is exact: **a record-lint that silently no-ops produces output byte-identical to a clean
estate.** Zero findings over a corpus it could not read, and zero findings over a corpus that is
genuinely consistent, are the same bytes. And the failure is *anti-correlated with its own
visibility* — the more completely the lint is broken, the cleaner and more reassuring its output.

**Requirement: the lint MUST return three outcomes, not two, and they must be distinguishable on the
face of its output without opening anything else.**

| Outcome | Meaning |
|---|---|
| **CONSISTENT** | Both facts were read, and they agree |
| **INCONSISTENT** | Both facts were read, and they disagree — the finding |
| **UNREADABLE** | One or both facts could not be read at all |

**`UNREADABLE` IS NOT A PASS AND MUST NEVER BE COUNTED AS ONE.** It is not an error either — it is a
normal, expected, frequently-occurring outcome, because most of the corpus does not carry the
artifacts this lint reads (section 4). It must be **counted and reported alongside** the other two,
never suppressed, never folded into CONSISTENT, and never `2>/dev/null`'d away.

**The output must print its own denominator on every run** — how many TOs were examined, how many
were readable, how many fired, how many were UNREADABLE and why. A bare count of findings does not
carry its own frame: nothing in the number `0` says what it is 0 *of*.

Named causes of `UNREADABLE`, all measured as present in the corpus at this vintage:

- **No `<status>` element at all** — 76 task orders. The lint cannot read fact A.
- **No `<instance_path>` declared** — 1,901 task orders. The lint cannot locate fact B.
- **Declared `<instance_path>` pointing at a file that does not exist** — 67 task orders
  (166 declare a path; 99 of those resolve). ⚠ **This one is genuinely ambiguous and must not be
  silently classed:** the instance may be unwritten (the TO is early), or the path may be wrong, or
  the file may have moved. Those are different conditions with different owners, and the lint cannot
  tell them apart from the path alone. It reports UNREADABLE with the reason `declared-path-absent`
  and does not guess.
- **Instance present but unparseable** — the file exists and does not read as a valid instance.

⛔ **And the trap specific to this lint: a failed retrieval returns a VALUE.** A missing file, a
mangled path, an unparseable JSON — each of these can yield an empty result that flows onward as
though it were a measured negative. Every read in this lint must distinguish *"I read it and it said
nothing"* from *"I could not read it."* Those are the two states this entire specification exists to
keep apart, applied to the lint's own instruments.

---

## 4. THE DENOMINATOR — what it sweeps, and what is explicitly OUT

**Measured at this vintage** over `org/{tier0, tier0_exec, tier1_exec, tier2_senior, tier3_junior}/**/task_orders/*.md`:

| Population | Count |
|---|---|
| Task-order files found | **2,067** |
| …carrying a `<status>` element | 1,991 |
| …carrying **no** `<status>` element | **76** |
| …declaring an `<instance_path>` | **166** |
| …whose declared instance **exists on disk** | **99** |
| CERT-shaped deliverables in the estate | 182 |

>> ⛔ **THE HONEST HEADLINE: THIS LINT CAN FULLY EXAMINE 99 OF 2,067 TASK ORDERS — ABOUT 4.8%.**
>> The other ~95% do not declare the artifact the check reads. **That is not a defect in the lint and
>> it must not be presented as coverage it does not have.** The proof-of-spec regime is recent; most
>> of the corpus predates it. A lint reporting "0 findings" across 2,067 TOs while structurally
>> blind to 1,968 of them is precisely the silent no-op section 3 forbids. <<

**Explicitly OUT of the swept population, by construction:**

- **Task orders with no `<instance_path>`.** Not swept as CONSISTENT — reported as UNREADABLE with a
  reason. They are out of the *findable* set, not out of the *counted* set.
- **The correctness of any work.** The lint compares two records to each other. It has no view on
  whether the work was done well, whether the verdicts are right, or whether the cert was sound.
- **Cell-level state.** See section 5.
- **Non-TO records** — PRDs, project JSONs, registry entries, ledgers. This lint's subject is the
  task-order face. *(Whether the same shape exists on those surfaces is a real question and not this
  spec's — raising it here would be scope I was not given.)*
- **Any judgment about whether an open TO ought to be closed.** The lint reports a disagreement
  between artifacts. Resolving it is a human act with an owner.

---

## 5. WHAT IT MUST NOT DO

These are **refusals**, not preferences. Each is stated because it is the obvious next feature and
would break the thing the lint exists to protect.

1. ⛔ **IT MUST NOT AUTO-FLIP A FACE.** This is the obvious feature and it is forbidden.
   **A machine writing `DELIVERED` onto a task-order face is asserting a state nobody measured** —
   the same class two seats refused tonight. Worse, it would *destroy the evidence of the very defect
   it was built to detect*: the disagreement would vanish silently, the record would look healthy,
   and the underlying unenforced obligation would become permanently invisible. **The lint reports.
   A human writes.**

2. ⛔ **IT MUST NOT ASSERT A CELL STATE.** A certified instance carries **acceptance rows**; a TO face
   wants **cell states**. These are different objects at different grains, and there is no total
   mapping from one to the other. Deriving N cell verdicts from M criterion verdicts is **inference
   wearing the authority of a certified measurement**. *(Exercised twice on 2026-08-26:
   `0.4.0_DS_ClientPlatform~U` refused it on `ADVI_PERFRP` at 14 rows vs 18 cells, and this seat
   refused it on `ADVI_STITCH.TO-A1-DS` at 13 rows vs 22 cells; the issuer ruled both correct.)*

3. ⛔ **IT MUST NOT BLOCK, GATE, HOLD, OR REFUSE ANYTHING.** Not a commit, not a deploy, not a
   dispatch, not a spawn. **Anything in this design that would hold a lane is out of scope by
   construction.** It is a lint on the record, and its worst-case output is a wrong line in a report
   that a human discards.

4. ⛔ **IT MUST NOT MANUFACTURE AN APPROVAL STEP.** No sign-off, no co-sign, no "X must confirm before
   Y." Andrew's approval covers *a consistency check*; it does not extend to any workflow built
   around one.

5. ⛔ **IT MUST NOT REPORT A CONFIDENT ZERO.** Every run prints its denominator and its UNREADABLE
   count beside its finding count. A zero without a denominator is not a result.

6. ⛔ **IT MUST NOT TREAT ITS OWN ABSENCE OF OUTPUT AS HEALTH.** If the lint does not run, or crashes,
   or reads an empty corpus, that state must be distinguishable from a clean sweep. *(A crash is not
   a verdict — `3.0.0_SA_CVO` fixed exactly this class in the proof-of-spec checker on 2026-08-25 at
   `9c9b2fd96b`, where an uncaught exception exited rc=1, byte-identical to a legitimate INVALID.)*

---

## 6. FINDINGS FOR THE ISSUER — decisions I did not make

Per dispatch 73735: *"If the spec cannot be written without inventing a design decision, that
decision is a FINDING for me."* Four.

**FINDING-1 — the open/closed partition of `<status>` is an enum mint, and enum minting is out of
scope.** The field is free prose: 429 distinct values, 40 leading tokens. The lint cannot ask "is
this TO open?" until someone with the authority to do so rules which tokens mean open. ⚠ Note the
Rule 24 exposure: any such partition must be MECE over the *declared domain*, and the long tail
includes whole sentences that are not values at all. **Owner: `2.0.0_SA_COO`, possibly routing to
`1.0.0_SA_CTO`.** *(A narrower alternative that avoids the mint entirely: key on the closed-set
tokens, which are far fewer and far more stable, and treat everything else as not-closed. I raise it
as an option, I do not choose it.)*

**FINDING-2 — there is no declared link from a certification back to the TO it certifies.** I located
certs by substring-matching TO ids across 182 CERT-shaped filenames and bodies. **That is a prose
grep, and it reads the artifact's text rather than a structured field a consumer can branch on** —
it will silently miss a cert that names its subject differently and silently match one that merely
mentions it. If certification is to be part of fact B, the link needs to be a field, not a filename
convention. **Owner: `3.0.0_SA_CVO`** as the cert author.

**FINDING-3 — which strength of fact B the lint adopts (15 / 11 / 2 fires) is a design decision.**
I measured all three and stated the trade-off; I did not pick. This is not a numeric threshold to be
tuned but a choice about what counts as evidence of completion. ⚠ And it interacts with FINDING-2:
the strongest tier is only available if the cert link exists. **Owner: `2.0.0_SA_COO`.**

**FINDING-4 — the 67 TOs declaring an instance path that does not resolve are a finding this lint
cannot classify.** Unwritten instance, wrong path, and moved file are three conditions with three
owners and three remedies, byte-identical from the path alone. The lint reports them as UNREADABLE;
**somebody should find out which they are, and that is not this lint's job.** **Owner: unassigned —
raising it rather than absorbing it.**

---

## 7. Provenance of the measurements in this document

Every figure was measured by this seat at the stated vintage against the working tree at
`origin/CLOUD` = `77a8dcef192a14df6f6512beaf836c9fb2b72670`, by walking the five tier roots and
parsing the `<status>`, `<instance_path>` and `<expected_criteria>` elements directly. The fire-set
counts (15 / 11 / 2) were computed over the same walk in one pass.

**What is NOT my measurement, marked so it cannot be mistaken for one:** the count of *five*
near-misses on 2026-08-26 and the claim that *two* reached fresh seats are `2.0.0_SA_COO`'s, relayed
in 73735. I grounded one of the five first-hand. The remaining four are cited, not verified.

**What I did not test:** whether the same face-vs-artifact divergence exists on PRDs, project JSONs
or registry entries. Out of the scope I was given, and I did not go looking.

---

*Spec ends. No implementation is authorized by this document.*
