# TAXONOMY 10 — `org/ref/RAVC_PROTOCOL.md`

    size:      7,921 B / 172 lines
    modified:  2026-07-24 · **1 edit in 14 days**
    role:      Request → Acknowledge → Validate → Close. Non-negotiable event-based protocol for all
               inter-agent work
    axes:      see AXES.md
    ANDREW'S RULING: "RAVC is very good" — KEEP. This taxonomy tests that ruling against the data
                     rather than restating it.

---

## 1. THE MEASUREMENT THAT VINDICATES THE RULING

| metric | RAVC | corpus median | CONTROLS_OVER_CARE |
|---|---|---|---|
| size | 7,921 B | 12,141 B | 94,959 B |
| edits in 14 days | **1** | 3 | **27** |
| dated-incident appendices | **0** | 2 | 7 |
| inlined incident narratives | **1** | many | ~76 |
| `N-SELF` self-violations | **0** | 1–2 | 11 |
| classified defects it RECORDS | **0** | 6–48 | 76 |

> ## **RAVC IS THE ONLY FILE IN THE ENTIRE CORPUS THAT IS A SPECIFICATION RATHER THAN A SEDIMENT.**
> It says what to DO. Every other file says what WENT WRONG and hopes you infer what to do.
> **That is why it is small, why it is stable, and why it has no self-violations to record: a
> protocol has no measurements to be wrong about.**

**Andrew's ruling is confirmed by the structure, not just by taste.** RAVC is stable because it is
**generative** (it tells you the next action) rather than **defensive** (it tells you what fooled
someone once).

---

## 2. CLASSIFIED CONTENT

RAVC records exactly **one** incident, and it is instructive that it was added as a numbered
sub-clause (§3a) rather than an appendix.

| # | incident | E | S | F | M | Det | Dir | Rec |
|---|---|---|---|---|---|---|---|---|
| 1 | **GC-W1 (2026-07-24):** CVO began verifying a **247-line** draft; the submitted version at `@b078877020` was **310 lines**, and the added `§4A` was *the most decision-critical section in the report* | E4 | S6 | F5 | M7 | D6 | X-CLEAN | N0 |

**The verifier caught it only because the author's cover note happened to mention claims they had not
read.** In their own words: ***"that is luck rather than mechanism."***

**1 classified incident.** Detection `D6` (accident) — one of only two `D6` catches in the corpus.

---

## 3. WHAT RAVC PREVENTS, BY CLASS

RAVC's own failure-mode table maps cleanly onto the taxonomy's axes. This is the reverse of every
other file: it is organised by *what it stops*, not by *what happened*.

| RAVC clause | axis-4 class it closes | how |
|---|---|---|
| **§2 Acknowledge** (silent receipt is a violation) | **M7** self-report-as-pointer | forces a CONSUMER-side signal; the only sound delivery oracle (Rule 22b) |
| **§3 Report with evidence** (commit hash / artifact path / output snippet) | **M9** desired-vs-applied | a claim must carry an exercisable artifact, not an assertion |
| **§3a Amend → re-notify with the new commit-ish** | **M7 / M4** | closes the superseded-draft hole; verifier pins the commit-ish validated |
| **§4 Validate** (open the commit, run the acceptance check) | **M11** tautology | the requester must independently exercise — the two sides cannot be the same computation |
| **§4 REWORK requires a specific delta** | **M14** prose-as-control | "looks off" is a note; a delta tied to expected evidence is actionable |
| **acceptance-flex pre-flag** | **M12** borrowed sensitivity | a waived criterion must be declared, not silently absorbed |

> **§3a is the most valuable clause and it is the newest.** Its failure mode is **silent and it lands
> on the VERIFIER, not the author** — *"a validation verdict rendered against a superseded draft is
> indistinguishable, in the record, from one rendered against the shipped artifact. Both read PASS."*

---

## 4. DOCUMENT-SPECIFIC FINDINGS

**4.1 — RAVC step 2 is load-bearing far outside RAVC.** CLAUDE.md Rule 22b names it as *the fabric's
reachability instrument*: a sovereign `[STOP]`/prohibition broadcast requires an ACK-or-escalate
loop, because `ps`, inbox file-location, and queue depth are all producer-side. **The corpus's entire
delivery-oracle doctrine reduces to "run RAVC step 2."**

**4.2 — Its weakest clause is `§4`'s enforcement, and the corpus proves it.** Validation is mandated
but nothing fails when it is skipped — enforcement is *"CTO/COO startup reconciliation"* and *"session
logs include an RAVC loops closed count."* **Both are prose carriers.** By TRIGGER_LAYER's own
definition that makes RAVC's enforcement a diary entry. *(This is a gap in the enforcement, not in
the protocol.)*

**4.3 — The five escalation triggers are the corpus's only bounded ambiguity-resolution rule**, and
they are what keeps Andrew out of the loop by default. Everything not on the list is explicitly in
scope for the execs. **No other document in the corpus states what NOT to escalate.**

**4.4 — "Go Time" is the anti-permission clause and it is the counterweight to this whole corpus.**
*"Should I continue? / Shall I proceed? / Do you want me to… are banned during go-time. The GO was
the authorization."* A corpus this heavy on verification failure pushes agents toward asking
permission; **RAVC is the only document pushing back.**

---

## 5. PRUNE VERDICT

| move | effect |
|---|---|
| **KEEP ENTIRE, UNTOUCHED** | Andrew-ruled, and the measurements independently confirm it |
| **DO NOT let it accrete incidents** | its value is that it is a spec. §3a is a correctly-placed clause; a §3b, §3c, §3d chain would convert it into CONTROLS_OVER_CARE |
| **USE ITS SHAPE as the compression target** | numbered steps · what each step requires · a bounded escalation list · a table of prevented failures |
| **CLOSE the §4 enforcement gap** | validation is mandated with no failing carrier — TRIGGER_LAYER applies to RAVC too |

> **THE TRANSFERABLE LESSON FOR THE WHOLE PRUNE: RAVC is 7.9KB and stable; CONTROLS_OVER_CARE is
> 95KB and grew 27 times in 14 days. The difference is not subject matter or discipline. RAVC states
> a PROCEDURE and links its one incident; the doctrine files state a CONCLUSION and inline every
> incident that produced it. Procedures converge. Conclusion-collections do not.**
