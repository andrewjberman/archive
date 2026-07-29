# TAXONOMY 05 — `docs/doctrine/A_VALUE_MUST_CARRY_ITS_CLAIM.md`

    size:      8,692 B / 151 lines
    modified:  2026-07-24 · 1 edit in 14 days
    role:      binding on design, gate conditions, and acceptance criteria. Occasion: six independent
               instances in ~30 hours across six subsystems, five agents, three git trees
    axes:      see AXES.md

---

## 1. STRUCTURAL MEASUREMENT

**151 lines, 4 corollaries, 1 positive instance, 1 provenance block. No appendix chain. One edit in
two weeks.** Structurally the healthiest file in the doctrine corpus.

It is also the only doctrine file whose thesis is about **the artifact**, not about the observer.
Everything else in the corpus asks *"how was the agent fooled?"* This asks *"what should the value
have carried so that nobody could be fooled?"*

---

## 2. CLASSIFIED INCIDENTS

| # | incident | E | S | F | M | Det | Dir | Rec |
|---|---|---|---|---|---|---|---|---|
| 1 | cot completeness sidecars: `>=1 row` measures *not-a-stub*, sold as *complete* | E1 | S1 | F1 | M5 | D4 | X-CLEAN | N0 |
| 2 | D_00 served firm AUA: a HELD cert silently re-based, presented as CERTIFIED | E1 | S1 | F5 | M5 | D4 | X-CLEAN | N0 |
| 3 | deploy_ledger red-scan: three ledgers closed in fact, **UNREADABLE scored as UNCLOSED** | E2 | S6 | F1 | M5 | D4 | X-LOUD | N0 |
| 4 | retry-net `_table_complete`: INFERRED-PRESENT advanced a client-data chain as MEASURED | E1 | S1 | F1 | M5 | D4 | X-CLEAN | N0 |
| 5 | MDPF Global count: `measured` / `band_2firm` / `frontier_stamp` **plotted as one line**; the +408 step is a basis seam, not growth | E5 | S1 | F2 | M6 | D4 | X-CLEAN | N0 |
| 6 | MDPF value line includes Cottonwood, count line does not — **same chart, same artifact** | E5 | S1 | F2 | M6 | D4 | X-CLEAN | N0 |
| 7 | bd/49F served AUA: header held-cert $1,879,986,733.13 vs gold $1,692,561,337.83 — **−9.97%, same nightly run, no instrument reports it** | E1 | S1 | F2 | M4 | D4 | X-CLEAN | N0 |
| 8 | Global `opal_aggregate_aua` vs per-firm `partner_custody_total` — genuinely different quantities, one name | E5 | S1 | F2 | M6 | D4 | X-CLEAN | N0 |
| 9 | **the author made "aua_pct rows must sum ~100" a gate condition; it was already false (90.1%), and the intuitive fix re-commits the defect** | E1 | S1 | F8 | M11 | D4 | X-CLEAN | N-SELF |
| 10 | `keys_staged: 11` — a hardcoded heredoc literal; answers "did the code run" | E1 | S1 | F7 | M1 | D4 | X-CLEAN | N0 |
| 11 | a cottonwood-fold check reading *"a 07-24 version appeared"* — **would have passed on the worst outcome** | E1 | S1 | F8 | M3 | D4 | X-CLEAN | N0 |
| 12 | a retry-net sweep test mocked a predicate the new sweep never calls | E1 | S7 | F8 | M11 | D4 | X-CLEAN | N0 |
| 13 | the excusals fix was "deployed" — committed + pushed, **never staged**; inf chain silently dead 6 days | E1 | S8 | F7 | M9 | D4 | X-CLEAN | N0 |
| 14 | an S3 stage would deploy AC5 — first-boot-only pull; the stage is inert until instance replacement | E1 | S8 | F7 | M9 | D4 | X-CLEAN | N0 |
| 15 | the mutation run "found nothing" — the grep matched the script's own `OK:` stdout | E3 | S7 | F1 | M8 | D4 | X-CLEAN | N0 |
| 16 | `git push` ran — **absorbed into a message body**; the sender re-ran it without knowing why | E1 | S5 | F7 | M2 | D6 | X-CLEAN | N0 |
| 17 | a fix "fixed the cliff" — two sibling scripts carried no hold at all; the cliff was the status quo | E1 | S1 | F8 | M6 | D4 | X-CLEAN | N0 |

**17 classified incidents.**

---

## 3. DISTRIBUTION

**Mechanism:** M5 **4** · M6 **4** · M9 **2** · M11 **2** · M1 **1** · M2 **1** · M3 **1** · M4 **1** · M8 **1**

**Epistemic type:** E1 **12 (71%)** · E5 **3 (18%)** · E2 **1** · E3 **1**

> **E5 (WRONG-GRAIN) is 18% here vs 3% corpus-wide — a 6× concentration.** This is the only file that
> systematically records **basis** errors: the same field name spanning two quantities. That is a
> distinct failure family and this is its only home.

**Failure direction:** X-CLEAN **16 (94%)** · X-LOUD **1** · X-DESTRUCTIVE **0**

**Detection:** D4 **16 (94%)** · D6 **1** · **D1 = 0** · **D2 = 0**

> **The only file in the corpus with ZERO positive-control catches.** Every instance was found by
> someone reading or grounding a premise. Its own line: *"Every one was caught by a control failing,
> or by someone grounding a premise instead of assuming it. Not one by being careful."*

**Recurrence:** N-SELF **1** — but it is the author's own gate condition, self-reported.

---

## 4. DOCUMENT-SPECIFIC FINDINGS

**4.1 — Corollary 1 (the missing third state) is the most reusable single idea in the entire
corpus.** Four surfaces, one shape: `UNKNOWN ≠ COMPLETE` · `HELD ≠ CERTIFIED` · `UNREADABLE ≠
UNCLOSED` · `INFERRED-PRESENT ≠ MEASURED`. And the sentence that generalises it:

> **"The instinct to widen a predicate until the awkward cases pass is always wrong. It retires the
> control. The awkward cases are awkward because the model is missing a state."**

**4.2 — Corollary 3 is the corpus's only PREVENTIVE technique, as opposed to a detection one.**
*Write the forbidden shortcut into the control.* Ask *"what is the easiest way to make this pass?"*
— if the answer re-commits the defect, the condition is wrong. **It costs one sentence and it acts
before the incident.** Everything else in 168KB is a way of noticing afterwards.

**4.3 — It is the only file that records what RIGHT looks like.** `meta.cottonwood_fold` carrying
`accounts_folded=294`, a per-model breakdown, its source key, and an in-band statement of the
never-sum law. The file states the reason explicitly: *"Doctrine is not only a catalogue of defects.
This is the shape to copy."* **No other file in the corpus contains a positive exemplar.**

**4.4 — Corollary 4's closing caveat is the epistemics of the whole corpus, and it belongs in
AXES.md, not buried at line 121:** *"only the loud ones scar … historical incidence is UNKNOWABLE;
never quote an observed count as a rate. `1 of 25` is a floor with an unknown ceiling."*

**4.5 — Instance 7 is an unresolved live defect sitting inside a doctrine file.** A **−9.97%
discrepancy between two served AUA numbers from the same nightly run, with no instrument reporting
it.** It is cited as an example of a basis defect. It reads as a live client-facing number
disagreement filed as an illustration. **I did not verify current state and am not claiming it is
still open — but a doctrine file is the wrong carrier for it, which is TRIGGER_LAYER's entire thesis.**

---

## 5. PRUNE VERDICT

| move | effect |
|---|---|
| **KEEP ENTIRE — do not touch** | 151 lines, 1 edit/14d, zero appendix chain, highest signal density in the corpus |
| **PROMOTE Corollary 1 + Corollary 3 to CLAUDE.md-adjacent status** | the missing-third-state test and the name-the-forbidden-route rule are both one-liners with gates behind them |
| **MOVE Corollary 4's caveat into AXES.md** | it governs how every count in every taxonomy must be read |
| **ROUTE instance 7 (−9.97%) to an owner** | if still live it is a finding, not an illustration (TRIGGER_LAYER) |

**This is the model the rest of the corpus should be compressed toward: short, one thesis,
corollaries not appendices, a positive exemplar, and an explicit statement of its own epistemic
limits.**
