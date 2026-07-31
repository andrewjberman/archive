# M9 PRE-FRAMEWORK BASELINE — SCHEMA DESIGN + PER-COMPONENT SOURCE DECLARATION

**Status:** **CAPTURED (first capture) — numbers are in §12.** Both gates cleared before any number
landed: CTO schema 20260731T061312Z, CVO source declaration 20260731T061200Z, freeze
`e649eb8249595cfa683711852831865f1e827f44` pinned before measuring.
**ALL SIX COMPONENTS BANKED** — (a), (b)-token, (b)-type, (c), (d)-count, (d)-attribution.
Fence RULED PERMITTED (CVO~Z Amendment 3); both C-1 declarations written at §15 with the substrate
**re-derived from the rule bank, not relayed**; CVO gate word 20260731T070250Z **PASSED both** after
re-running all five checks independently. Falsifier **reported NOT FIRED** rather than left silent.
**M9-COMPLETE IS NOT REACHED, AND EDGE-1 DOES NOT DISCHARGE ON THIS.** The §3-population capture is
**unsatisfiable as frozen** (§13 + §3 amendment note): the ratified primary segmentation yields
**zero**, because `pods_spanned >= 2` excludes every single-author unit — including the estate's own
published work-unit boundary. Escalated to joint CTO+CVO adjudication; **not mine to tune.**
**v6** — v2 folded CTO's six constraints + the derivation trap; v3 froze; v4 captured; v5 declared;
v6 banked the last two. v1 got three of the six wrong; corrected in place and named in §9.
*(⚠ **THIRD** stale-header instance in this one file — "PRE-MEASUREMENT" while §12 carried results,
"fence pending" after it was ruled, "awaiting CVO" after CVO passed. Each fixed on sight, and the
recurrence is the finding: **the header is the one part nobody re-reads after writing a section**,
so it drifts by default rather than by accident. A status line contradicting its own document is
the exact class this seat was spawned into — and patching it three times is evidence the fix should
be structural, not another patch.)*
**Author:** `0.7.0_AE_CloudOps~D` (measurement-plane seat) · **Date:** 2026-07-31
**Tasking:** `0.0.0_AB_MSTR` 20260731T055536Z (Andrew `/govern` + LD-0090 + CVO~Z fence ruling
`@4b94ad6f3` + CTO confirmation 060030Z)
**Gates:** SCHEMA -> `1.0.0_SA_CTO` before measuring · SOURCE DECLARATION -> `3.0.0_SA_CVO` before
any number banks.

---

## §0 Capturer declaration (CVO~Z control 2; CTO 060030Z made this message the declaration — it
travels with the evidence, per instruction)

**`0.7.0_AE_CloudOps~D` authors, reviews and ratifies NO WS-C1/WS-C2 rail vocabulary while the
fence stands.** Measurement-plane only. If a VELOCITY task would put me on rail vocabulary I refuse
it and route to MSTR — I do not take both. I do not decompose ADVI_PERFORMANCE or MDPF_GLOBAL.

Fence basis (CVO~Z `@4b94ad6f3`, CTO-grounded independently at `4b94ad6f392e1f99`): the apparent
capture contradiction is an **equivocation** — a build-cost baseline and a domain surface are
different objects, and only the second is fenced.

## §0b REQUIRED ARTIFACT-HEADER DECLARATIONS (CTO rider 3 — structural, not prose)

CTO's instruction was to be consistent with my own best idea: I argued (c)'s scope must be a
**required enum, not a footnote**, *because scope is exactly the qualifier dropped when a figure is
quoted onward.* That reasoning applies with equal force to fork A's confound, and §8 prose would
survive being quoted onward no better than a scope footnote would. So it becomes a **required
artifact-level field set** — every emission of this baseline carries these three or it is malformed:

| field | type | value at freeze | what it prevents |
|---|---|---|---|
| `baseline_reading` | enum {`retrospective_reference_class`, `prospective_first_slice`} | `retrospective_reference_class` | silently re-reading the population as the products' own history |
| `comparison_validity` | enum {`same_work_before_after`, `cross_work_compositional`} | `cross_work_compositional` | reading a cross-work delta as a before/after |
| `causal_reading_permitted` | boolean | **`false`** | quoting a later delta as *caused by* the framework |

**A consumer that quotes a causal delta from this baseline contradicts the artifact's own
`causal_reading_permitted: false` field.** That is the point: the confound is now checkable by a
reader who never read §8, which prose could not achieve.

## §1 What M9 is, quoted not paraphrased (PROGRAM §5.9)

| id | wording |
|---|---|
| **a** | archaeology-vs-build wall-clock and agent-context |
| **b** | count of "which artifact is canonical / who writes this / is it live" questions |
| **c** | rail-override count |
| **d** | rework waves caused by a wrong denominator |

Also declared: *"Hand-tagged is fine; it is a baseline, not a gate."* I invent no metric and no
vocabulary (arch-gate constraint 4).

## §2 THE ANTI-LEAK CONTROL — a CLOSED schema, not a careful author

CVO~Z control 1 **excludes** free text rather than discouraging it. **I implement the exclusion as
a TYPE: the schema has no free-text field, so a surface leak is not expressible in it.** Every
field is an integer, a real, an enum from a stated set, an ISO-8601 timestamp with a **computed**
offset, or a source enum token.

*Care is not a control.* A schema with a notes field plus an instruction not to leak is a guard
that depends on the guarded party's attention — the shape `docs/doctrine/CONTROLS_OVER_CARE.md`
rejects. A closed schema fails the leak at write time, not at review time.

**Forbidden by construction:** ADVI/MDPF identifiers, field/column names, path structures, grains,
partition schemes, contract content, work-unit NAMES.
**Permitted:** counts, durations, ratios, denominators, diffstat MAGNITUDES.

## §3 Population — STRUCTURAL predicates, ORDINAL identity

**A work unit is identified by an ORDINAL, never a name** (CTO constraint 3): `work_unit_seq: 7`.
There is no name field and no description field. *A work-unit name is grain vocabulary wearing a
label.*

Entry predicates (structural only):
`pods_spanned >= 2` (integer, distinct committing serials) · `has_served_consumer` (boolean) ·
`delivered_within_window` (boolean)

**🔒 FROZEN. CTO approved the schema at 20260731T061312Z; THIS COMMIT IS THE FREEZE HASH** (§10
step 4). The three predicates above are pre-registered as of this commit and are not editable
afterward — a later change is an ADDED column with its own hash, never an overwrite.

Choosing a reference class after seeing the treatment is post-hoc and unfalsifiable; pinning it
first is pre-registration, and it is the honest sense in which this capture is time-sensitive.
**Freezing before the first number is what makes this a control rather than a rationalisation** —
and it is checkable by anyone, because the freeze is a commit hash and the numbers land after it.

### ⚠ §3 AMENDMENT NOTE (appended 2026-07-31, CTO-instructed 064734Z — the frozen predicates above are NOT edited)

**`pods_spanned >= 2` is UNSATISFIABLE against any SINGLE-AUTHOR segmentation, and the estate's own
published work-unit boundary is single-author by construction.**

Established by collision, three times, from independent directions:

| candidate | outcome | why |
|---|---|---|
| **S-C** single-commit (null) | population **0** | one commit has one author |
| **S-A** session-log-anchored — **the RATIFIED PRIMARY** | population **0** | **measured: max pods = 1 across all 3,530 units** — a session log is authored by one serial |
| **S-B** deploy-boundary | 415 (see deviation note) | an external delivery boundary is the *only* one of the three that yields multi-author units (max pods 24) |

**So §3 has TWO holes, not one, and they interact.** §13 found that it froze predicates without
defining a segmentation function. This note records the second: **the predicates additionally
constrain which segmentation functions could ever satisfy them — and they exclude the one the
estate publishes about itself.** `pods_spanned >= 2` silently presupposes a **multi-agent
collaboration unit**, which neither a commit nor a session log supplies.

**This is a fact about the frozen predicates, not a candidate result** — which is why it lives here
with the predicates rather than in the candidates file (CTO 064734Z). It was invisible to reading
and appeared only when something ran into it: **a null candidate that fails loudly is an
instrument, and the candidates that could pass could not have found it.**

Neither number is banked as the §3-population capture. Amending the predicates is CTO's and CVO's,
not mine — I am recording the collision, not resolving it.

## §4 The schema

| field | type | notes |
|---|---|---|
| `work_unit_seq` | integer | **ordinal identity; NO name field exists** |
| `component` | enum {`a`,`b`,`c`,`d`} | PROGRAM §5.9 id |
| `metric_id` | enum (fixed, §4.1) | no free naming |
| `unit_kind` | enum {`DECOMPOSE`,`SPEC`,`IMPLEMENT`,`VERIFY`,`REWORK`,`INTEGRATE`,`DEPLOY`,`REVIEW`} | **CTO's project-generic set, ADOPTED — see §9.2** |
| `value` | number | — |
| `unit` | enum {`minutes`,`count`,`ratio`,`sessions`,`commits`,`lines`} | — |
| `denominator` | number | **required, never null** |
| `denominator_of` | enum (fixed) | what it counts — closes the "number OF what" law |
| `capture_method` | enum {`DIRECT_OBSERVATION`,`GIT_DERIVED`,`SELF_REPORT`} | **CTO constraint 6** |
| `source_id` | enum (fixed, §5) | **an enum token, NOT a path — CTO constraint 5** |
| `status` | enum {`MEASURED`,`CARRIED`,`NOT_YET_MEASURABLE`} | COO's convention, reused not reinvented |
| `scope` | enum {`device_local`,`repo_global`} | §5.1 — load-bearing |
| `window_start`/`window_end` | ISO-8601, **computed offset** | never a hand-typed `Z` (host UTC-4; a typed `Z` cancels the check instead of prompting it) |

### §4.1 Metric ids (fixed)
`a_archaeology_minutes` · `a_build_minutes` · `a_archaeology_ratio` · `a_context_sessions`
`b_canonicity_questions` · `c_rail_override_count` · `c_rail_deny_count`
`d_rework_wave_count` · `d_rework_wave_denominator_attributed`

**Aggregate rule (inherited, not invented):** no aggregate headline without per-series
decomposition (WS-E4.3, already structural in `series()`).

## §5 PER-COMPONENT SOURCE DECLARATION (CVO's gate — read before any number banks)

**Binding attestation: NO component reads `org/mcp/agent_telemetry/` or the M3 verdict sink
`org/mcp/comp-tool-runs.jsonl`, pre-fix or post-fix.** I am the seat that repaired M3; reading my
own in-repair instrument into the baseline is the exact axis-confusion the condition prevents
(verification law 6).

| comp | `source_id` | instrument | scope | `capture_method` | non-M3 |
|---|---|---|---|---|---|
| a | `SRC_SESSION_LOGS` | agent session logs + commit timestamps | `repo_global` | `GIT_DERIVED` (durations) + `SELF_REPORT` (phase split) | ✅ |
| b | `SRC_FABRIC_MSGS` | session logs + inbox bodies vs a FIXED question-pattern set | `repo_global` | `SELF_REPORT` (deterministic first pass + judgment residue, **counts reported separately**) | ✅ |
| c | `SRC_RAIL_LOG` | `org/mcp/comp-which-rail.log` | ⚠ `device_local` | `GIT_DERIVED` | ✅ separate instrument from M3 — CVO ruled this explicitly 20260731T023531Z |
| d | `SRC_COMMIT_STRUCTURE` | repeat-touch structure over commit metadata | `repo_global` | `GIT_DERIVED` (count) / `SELF_REPORT` (attribution) | ✅ |

### ⚠ §5.1 DECLARED WEAKNESS IN (c) — surfaced now, not discovered later

**`org/mcp/comp-which-rail.log` is NOT TRACKED IN GIT** (verified: `git ls-files --error-unmatch`
fails; `.gitignore` carries the sibling sinks at `:261`, `:447-448`, `:454`). It is **device-local**,
so a rail-override count from it is **this device's traffic only, silently short by every other
device's**. Local file at capture design: 5,336,054 bytes.

Not a defect I can fix and not a reason to skip (c) — PROGRAM §5.1 already cites a 187/month
baseline and COO's M1a measured 76 overrides against 24,205 lines from this same source. **It is a
scope qualifier that must ride with the number permanently**, because scope is exactly the
qualifier dropped when a figure is quoted onward. Hence `scope` is a required enum, not a footnote.

## §6 THE DERIVATION TRAP — CTO 060030Z, and it invalidated my v1 source for (d)

CTO: *a git-derived row takes COUNTS, TIMESTAMPS and MAGNITUDES only — never subjects, never
paths, never file names,* because the breach arrives through the derivation rather than the author,
so nobody feels themselves doing it.

**This killed my v1 (d) source.** v1 declared (d) would match commit *"revert/fix/correct
subjects"* — reading commit subjects, which are free text and are exactly where grain and contract
vocabulary live. **Corrected in §5: (d) now derives from repeat-touch STRUCTURE over commit
metadata** — same path-set touched again inside the window, measured as counts and diffstat
magnitudes, never as subjects, paths or file names.

### §6.1 THE RULE (CTO rider 1) — stated once, so both cases follow from it

Component (b) also reads prose (session logs, inbox bodies), one layer over. That looks like an
inconsistency with killing (d)'s subject-matching. It is not, and the discriminator is a rule, not
two case-by-case judgments:

> ## A PROSE-READING DERIVATION IS SAFE **IFF** ITS MATCHING VOCABULARY IS **PRE-REGISTERED** AND **PROJECT-GENERIC**.

- **(d) v1 FAILS it.** Matching `revert|fix|correct` against arbitrary subjects means the
  classifier's own pattern list **drifts toward the measured surface's vocabulary in order to stay
  accurate** — the derivation becomes a channel for the thing it is matching against.
- **(b) PASSES it.** *"which artifact is canonical / who writes this / is it live"* is fixed before
  measurement, generic to any project, and carries no ADVI/MDPF content — **the pattern set could
  not encode a grain if it tried.**

Stating it as a rule means a future reader does not have to re-derive why one was killed and the
other kept, and any NEW prose-reading source must pass the same test before it enters §5.

## §7 THE HONEST PARTIAL ON (d) — reported, NOT engineered around

CTO instructed: if a cost dimension cannot be captured without free text, report it as the
falsifier firing rather than working around it, because a workaround silently converts a failed
premise into a passed one.

**Component (d) splits, and only half is mechanical:**
- `d_rework_wave_count` — **GIT_DERIVED.** Repeat-touch structure. No free text. Clean.
- `d_rework_wave_denominator_attributed` — the *"caused by a wrong denominator"* half is a
  **CAUSAL** claim. Cause is not present in commit metadata at any magnitude; it lives in prose.
  It is therefore **`SELF_REPORT` and can never be `GIT_DERIVED`**, and retrospectively it requires
  a human/agent to read prose to classify.

**My reading, offered for CTO/CVO~Z to rule, not asserted:** this is a **LIMITATION, not the
falsifier firing.** The schema still holds — the *artifact* carries only a closed enum, and the
classification act happens outside it. But the resulting row is judgment-grounded, which is weaker
evidence than a mechanical one, and PROGRAM §5.9's own *"hand-tagged is fine"* appears to license
exactly this. **If CVO~Z reads the fence as also barring the classifying READ (not merely the
written artifact), then (d)'s attribution half is genuinely uncapturable retrospectively and the
falsifier HAS fired on that half.** That is a fence-scope question and it is CVO~Z's, not mine —
I am not resolving it in my own favour to keep my task whole.

## §8 THE FORK — decisive recommendation

Both products are **PHASE 0** (CTO `@ee5ff633e1`: MSTR~Z searched 25,048 files / 23,518 commits /
all branches — 5 files describe the obligation, **zero capture it**; MSTR: all 33 S3 buckets
negative). Nothing is built, so "pre-framework cost" must be measured on something:

**A — RETROSPECTIVE REFERENCE CLASS:** measure a–d over comparable completed conventional builds,
class pinned per §3.
**B — PROSPECTIVE FIRST SLICE:** build one slice conventionally and measure it.

**I recommend A. B is not merely weaker — it is structurally unavailable:** it requires decomposing
one of the two projects, which is exactly what CTO's precondition withholds until this baseline
exists. **B can only be run by violating the control it would serve.**

**THE LIMITATION THAT RIDES WITH A, stated now rather than discovered at comparison time:** under A
the baseline measures *the fabric's conventional build cost on comparable work*, **not those two
products' own prior cost.** The eventual comparison is therefore across different work, not a
before/after on the same work — a later delta is partly compositional and **must not be read as
purely causal.** Enumerate what a number is OF before explaining why it differs (verification law
6). Better a declared limitation in the baseline than a discovered confound in the verdict.

## §9 WHAT v1 GOT WRONG (recorded, not silently corrected)

1. **Row-level `source_path`** — a path field in the measurement row, straight into CTO constraint
   5. Replaced by `source_id`, an enum; paths now live only in §5's declaration prose.
2. **`unit_kind` = {`new_surface`,`extension`,`migration`}** — mine classified the OUTPUT's shape,
   which sits closer to product surface. **CTO's set classifies the WORK PHASE and is
   project-generic; adopted without argument** — it is better precisely on the anti-leak axis, and
   it is also the right cut for (a)'s archaeology-vs-build split.
3. **`extraction` = {`deterministic`,`hand_tagged`}** — describes technique, not grounding.
   Replaced by CTO's `capture_method`, which is what CVO actually needs to gate a mixed artifact.
4. **(d) sourced from commit SUBJECTS** — the derivation trap, §6. The most serious of the four:
   a schema that reads clean while the derivation carries the surface in.
5. **No ordinal work-unit identity declared** — added (§3).

## §10 Sequence — LIVE STATE

| # | step | state |
|---|---|---|
| 1 | CTO arch-gates the schema | ✅ **APPROVED** 20260731T061312Z (schema v2 + fork A) |
| 2 | CVO reads the source declaration | ✅ **PASS** 20260731T061200Z on (a)(b)(c)(d)-count; **(d)-attribution WITHHELD** |
| 3 | CVO~Z rules the §7 fence-scope question | ⏳ OPEN — **does not block; see below** |
| 4 | Freeze §3 criteria + record freeze hash | ✅ **THIS COMMIT IS THE FREEZE** |
| 5 | Measure | ▶ proceeding on (a)(b)(c) + `d_rework_wave_count` |
| 6 | Edge-1 discharges | ⏳ on the **measured** artifact on origin — NOT on schema approval, NOT on a local-only commit |

**Step 3 does not gate step 5 (CTO rider 2).** The `status` enum already carries
`NOT_YET_MEASURABLE`, which is exactly the slot the open question needs:
`d_rework_wave_denominator_attributed` sits there until CVO~Z rules, while everything else is clean
under **either** ruling — so **nothing measured now has to be re-taken whichever way it goes.**
Perishability makes waiting the expensive option, and the design already absorbed the uncertainty.

**If CVO~Z rules the classifying READ barred, that half is genuinely uncapturable retrospectively
and the falsifier HAS FIRED on it — I report it fired and do not rescue it** (CTO instruction, and
I do not resolve it myself even if step 3 runs long).

Values land as an **added table**, never overwriting a row (COO baseline §4 rule).

## §11 What this document deliberately does NOT do

- Does not decompose either project. · Does not author/review/ratify rail vocabulary (§0).
- Does not bank a number (§10 not yet run).
- **Builds no guard, alarm, monitor or checker.** CTO `@ee5ff633e1` is explicit that the control is
  a **work-ordering precondition in the record a decomposer reads, NOT a detector**, and that the
  moratorium must not be cited against it. Nothing here fires anything.

---

# §12 RESULTS — FIRST CAPTURE (added table, nothing above overwritten)

**Freeze hash:** `e649eb8249595cfa683711852831865f1e827f44` — pinned BEFORE these numbers existed.
**Gates cleared:** CTO schema 20260731T061312Z · CVO source declaration 20260731T061200Z.
**Header declarations (§0b):** `baseline_reading=retrospective_reference_class` ·
`comparison_validity=cross_work_compositional` · **`causal_reading_permitted=false`**
**Window (git components):** 2026-04-30 .. 2026-07-29 — **ends before NFRA_VELOCITY was
commissioned (2026-07-29), so it is genuinely PRE-framework.**

| metric_id | value | denominator | denominator_of | capture_method | scope | status |
|---|---|---|---|---|---|---|
| `a_archaeology_ratio` | **0.2666** | 889 | archaeology+build tag-instances | SELF_REPORT | repo_global | MEASURED |
| `a_archaeology_tags` | 237 | 2,446 | all archetype tag-instances | GIT_DERIVED | repo_global | MEASURED |
| `a_build_tags` | 652 | 2,446 | all archetype tag-instances | GIT_DERIVED | repo_global | MEASURED |
| `a_context_sessions` | 2,078 | 4,206 | log files in scope | GIT_DERIVED | repo_global | MEASURED |
| `b_canonicity_questions` | **0** | 4,206 | log files scanned | SELF_REPORT | repo_global | **MEASURED-AS-TOKEN — SEE §12.2. DOES NOT ESTABLISH A RATE OF 0.** |
| `c_rail_override_count` | **76** | 26,590 | rail-log lines | GIT_DERIVED | ⚠ **device_local** | MEASURED |
| `c_rail_deny_count` | **672** | 26,590 | rail-log lines | GIT_DERIVED | ⚠ **device_local** | MEASURED |
| `d_retouch_rate` | **36.77%–56.09%** | 14,154 | eligible commits | GIT_DERIVED | repo_global | MEASURED AS A **RANGE** — SEE §12.3 |
| `d_rework_wave_denominator_attributed` | — | — | — | — | — | **NOT_YET_MEASURABLE** (CVO~Z step 3 open) |

`a_archaeology_ratio`'s denominator is **889 (archaeology+build), NOT 2,446** — the 1,557
NEITHER-tags (VALIDATE / COORDINATE / SCRIBE / MIXED = 63.7%) are **not folded into either side.**

## §12.1 ⚠ A ZERO I ALMOST BANKED, CAUGHT BY THE POSITIVE CONTROL

My first (a)/(b) run returned `a_archaeology_ratio = 0.0000` and every (b) pattern at 0. **Both
were fabricated by a broken retrieval, not measured.** The `git grep -- "org/tier*/*/logs/"`
pathspec matched nothing; the real population is 2,446 archetype tags across 2,078 files. A
positive control — grepping a line I had personally written into a log minutes earlier — returned
the line by direct read and **nothing** through the pathspec, which located the fault in the
RETRIEVAL rather than the estate.

**Had I banked it, `a_archaeology_ratio = 0.0000` would have entered the program's only
product-grade metric as a number produced entirely by a failed glob** — and it would have read as
a stunning finding (*"zero archaeology!"*) rather than as a bug. *Put the control on the retrieval,
not the pattern.*

## §12.2 (b) IS ON THE WRONG AXIS — and the zero is real while the rate is not

The three literal strings PROGRAM §5.9 names return **0 each**. The scan is sound (same loop
returned 2,446 archetype tags), so this is a **real token-count zero — and it does NOT establish
that the questions were not asked.** A broader pre-registered, project-generic probe over the same
4,206 files, each reported separately and never summed:

`canonical` **7,302** (1,815 files) · `authoritative` **569** (374) · `source of truth` **92** (80)
· `still live` **40** (39) · `who owns` **11** · `who writes` **1** · `which is canonical` **0** ·
`is it live` **0** · `is this live` **0**

**§5.9 names a question TYPE; a literal-token count is a proxy on the wrong axis for it.** The
category is plainly present at scale while its literal phrasings are absent. **This is the same
shape as COO's M1c NUDGE zero** (*"no NUDGE token across 24,205 lines"* — recorded as a token count
with the ambiguity named, never as a rate of zero), and it is recorded the same way.

**Consequence:** (b) as literally specified is **not capturable by pre-registered literal
patterns.** Capturing the TYPE needs judgment over prose — which raises **the same fence-scope
question already open for (d)**, and I am not resolving it here for the same reason.

## §12.3 (d) — THE PREDICATE IS THE MEASUREMENT, so all four are reported

| predicate (commit introduces NO new path within…) | count | denom | rate |
|---|---|---|---|
| 7d horizon, any author, logs INCLUDED | 6,730 | 15,741 | 42.75% |
| 7d horizon, any author, logs EXCLUDED | 7,939 | 14,154 | **56.09%** |
| 24h horizon, any author, logs EXCLUDED | 7,122 | 14,154 | 50.32% |
| 24h horizon, **same author**, logs EXCLUDED | 5,205 | 14,154 | **36.77%** |

**A 19-point spread across four honest predicates. The spread IS the result** — "rework" is not one
population, and any single figure here would have been a choice wearing the costume of a
measurement. Excluding logs *raised* the rate (42.75%→56.09%), the opposite of my expectation,
because session logs are mostly NEW paths — **the measurement corrected me, my intuition did not.**

**NAMING CORRECTION, and it matters:** I have renamed this `d_retouch_rate`, **not**
`d_rework_wave_count`. What is measured is *re-touch*, which is a **superset** of rework — it
cannot separate correction from normal iteration by structure alone. Calling it "rework" would name
a number for what I wanted it to measure rather than what it measures.

**This widens what I told CTO at 060847Z.** I reported that only (d)'s *attribution* half was
judgment-bound. **The *count* half does not cleanly isolate rework either.** Reporting the widening
rather than letting the earlier, narrower claim stand.

## §12.4 DECLARED GAP — measured population ≠ frozen §3 population

§3 froze a **work-unit** population (`pods_spanned>=2`, `has_served_consumer`,
`delivered_within_window`). **These results are measured over COMMITS and LOG FILES — a proxy
population, not the frozen one.** Segmenting the history into work units satisfying §3 is not
built, so the §3 predicates are **declared-but-unapplied** in this first capture.

Stating it because an unstated proxy-for-population substitution is precisely the axis-confusion
this program exists to catch, and because §3's freeze is only worth something if deviations from it
are visible. **A second capture against the true §3 population would be an ADDED column, never an
overwrite.**

---

# §13 A HOLE IN §3's OWN FREEZE — the frozen class is not yet a class

**Status:** FINDING. **No §3-population capture is banked, and none is in progress** (CTO
063318Z sequenced the inbox-side (b) capture ahead of it; I stopped on that word).
*Sequencing note, stated plainly: I began this segmentation on CVO's 063042Z ruling and CTO's
stop-instruction landed while it was running. Reporting the result, not presenting it as
correctly ordered.*

## §13.1 What happened

Applying §3's frozen predicates required segmenting history into work units. Structural
clustering — commits linked by ≥1 shared path within a 7-day horizon, then the three predicates —
produced:

| stage | count |
|---|---|
| candidate components | 4,570 |
| `pods_spanned >= 2` | 244 |
| **AND** `has_served_consumer` | **65** |
| unit size | min 2 · median 4 · **max 8,043** |
| pods per unit | min 2 · median 2 · **max 77** |

**One component swallowed 8,043 of the 8,654 qualifying commits (93%) and spans 77 distinct
agents.** That is not a work unit; it is the fabric's shared surface.

**Diagnosis (structural, no path content reasoned about):** transitive path-connectivity fuses
unrelated work through ubiquitous hub paths — the top 10 most-touched paths carry **9.9% of all
path-touches** across 19,426 distinct paths, and are touched by nearly every agent on nearly every
task. **The blob is an artifact of the LINKING RULE, not a property of the work.**

## §13.2 THE ACTUAL FINDING — and it is about §3, not about the clustering

**§3 froze the PREDICATES but never defined the SEGMENTATION FUNCTION.**

`pods_spanned >= 2`, `has_served_consumer` and `delivered_within_window` are each well-defined
**given** work units. *What constitutes a work unit was never pinned.* I did not notice at freeze
time; it surfaced only on application. **So the frozen class is not yet a class** — §3 pre-registers
a filter over a population whose construction rule does not exist.

This is a defect in my own control, found by trying to use it. Recording it here because §3's
freeze is only worth something if its holes are as visible as its deviations.

## §13.3 WHAT I AM DELIBERATELY NOT DOING

**I am not tuning a hub-exclusion threshold to make the population appear.** A threshold chosen
*now*, after seeing the blob, is a reference class chosen after seeing the result — **precisely
what §3's pre-registration exists to prevent**, and it would retroactively empty the strongest
control in this artifact. It would also work: some threshold produces a plausible unit count, and
nothing downstream would reveal that the parameter was fitted to its own answer.

**The segmentation function must be defined and frozen on its own, ratified without tuning against
this output.** That is an arch-gate call. Until it exists, `M9-COMPLETE`'s §3-population clause
(CVO 063042Z) cannot be satisfied by any measurement I could take — and that is a real blocker on
the obligation, not a delay in my execution.

---

# §14 (b) TOKEN-AXIS INBOX CAPTURE — banked (CTO authorized 20260731T063838Z)

**Axis:** TOKEN ONLY. No classification, no judgment, no TYPE inference — so this needs no fence
ruling and pre-empts none. **TYPE axis remains pending** CVO~Z's A2.3 self-test + a C-1-analog
declaration (CVO 063717Z).
**Denominators enumerated AT RUN TIME:** 54,700 inbox `.md` files · 117,343,092 bytes ·
captured 2026-07-31T06:39:37Z (computed offset, never a hand-typed `Z`).
**`scope: device_local`** — 0-TRACKED (`.gitignore:248`).

| pattern | inbox hits | inbox files | (durable logs, §12.2) |
|---|---|---|---|
| `canonical` | 23,951 | 11,208 | 7,304 |
| `authoritative` | 2,190 | 1,655 | 570 |
| `source of truth` | 344 | 322 | 93 |
| `still live` | 208 | 192 | 40 |
| `who owns` | 136 | 133 | 11 |
| `who writes` | 21 | 21 | 1 |
| `is it live` | **9** | 9 | **0** |
| `is this live` | **4** | 4 | **0** |
| `which artifact is canonical` | **1** | 1 | **0** |

**Per-pattern, reported separately. NEVER summed into a rate** (CVO condition 3).

## §14.1 REQUIRED DECLARATION on any (b) figure that ships (CTO 063838Z)

**The inbox holds 77% of observable (b) signal volume and is 0-tracked/device-local; durable
session logs hold 23%.** Any (b) figure ships with this split or it is malformed — *a logs-only (b)
would otherwise be a real number silently hiding that three quarters of its evidence existed and
expired.*

## §14.2 THE THREE LITERAL §5.9 STRINGS EXIST — AND ONLY IN THE PERISHABLE STORE

`which artifact is canonical` (1), `is it live` (9), `is this live` (4) appear in inbox bodies and
**zero times** in durable logs. Trace volume, and that is the point: **the only corpus containing
the literal phrasings PROGRAM §5.9 names is the one that is not tracked and that this fabric loses
routinely.** A durable-only capture of (b) would report those three at 0 forever and be, narrowly,
correct — and completely misleading about whether the question was ever asked in those words.

## §14.3 WHY THE BODIES ARE UNTRACKED — the reason is documented, not incidental

CTO (063838Z) declined to order a snapshot noting the bodies *"are untracked for reasons I have not
audited (size, noise, possibly PII)."* **The reason is recorded in `.gitignore`:**
`:235` — *"MCP runtime state (broker database, inbox, liveness) — local runtime only"*, and
`:248` — `org/mcp/inbox/*`, with a deliberate carve-out for one serial's undelivered mail.

**"Local runtime only" is a deliberate scoping decision, not an oversight.** So preserving 54,700
bodies / 111.9 MB to a durable store would *override a standing decision*, which is a named call
for its owner — not something a measurement seat does on its own initiative. **I did not build it.**
Recorded here so the decision-maker has the actual reason rather than a guess at it.

---

# §15 C-1 DECLARATIONS (CVO~Z Amendment 2 + 3) — WRITTEN BEFORE EITHER COMPONENT BANKS

**Fence ruled PERMITTED** — CVO~Z Amendment 3, carried by MSTR 20260731T065433Z.
**No number for (d)-attribution or (b)-type is banked in this document.** CVO reads both
declarations below first; that is their gate and it is unchanged by the clearance.

## §15.1 SUBSTRATE GROUND — re-derived by me from the artifact, NOT taken from the ruling message

Amendment 3's mandatory clause requires citing the substrate so a later auditor re-derives the
clearance from the **rule bank itself**, without a fenced read and without trusting an inbox
message. I therefore verified it rather than relaying it. All checks below are grep-checkable and
touch no fenced object:

| claim | verified at | evidence |
|---|---|---|
| the ratified bank **uses legacy mdpf as a worked D3 exemplar** | `org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml:325` | *"the MDPF delivery-cadence contract (T-1 by 02:00Z) is a **WRITTEN D3 instance**"* |
| …and in the pipeline thread + scope + contract set | `:204` (`mdpf-gold`), `:553` (`scopes.mdpf`), `:519` (the MDPF cadence PRD in `declared_contracts`) | 8 mentions at HEAD |
| …**already present at v1.7** | `@8f8a63200` | commit exists; **5** mdpf mentions at that vintage |
| the **same artifact** declares the hold-out | `:54`, `:60` | *"ADVI_PERFORMANCE and MDPF_GLOBAL are the **HELD-OUT SET**"* |
| the instrument discriminates | positive control | a known-absent token returns 0 on this file |

**So one ratified artifact simultaneously declares MDPF_GLOBAL held out (`:60`) and builds D3 on
the legacy mdpf pipeline's cadence contract (`:325`).** Either legacy mdpf-pipeline content is
outside the fence, or the fence was breached at its own foundation and every D3 rail is void. The
second is untenable — the D3 seed **predates** the fence.

## §15.2 C-1 for `d_rework_wave_denominator_attributed` (Amendment 2 form)

> The classifying read for (d)-attribution touched **reference-class prose, which includes legacy
> mdpf-ESTATE content; ZERO MDPF_GLOBAL project artifacts (none exist); zero ADVI decomposition
> artifacts.** Substrate ground: `NFRA_ONTOLOGY_RULE_BANK.yaml` v1.7 `@8f8a63200` / v1.8 `:60`
> (§15.1, independently re-derived).

## §15.3 C-1 ANALOG for `b_canonicity_questions` (TYPE axis) — CVO's translation, not a copy

CVO 063717Z required this to **translate rather than copy**, because (b)'s corpus is not the
reference class and a literal copy would be false on its face:

> The classifying read for (b)-TYPE touched an **ENUMERATED corpus of fabric messages and session
> logs — 4,207 session-log files and 54,700 inbox bodies, window 2026-04-30 .. 2026-07-29** — which
> includes legacy mdpf-ESTATE content; **ZERO MDPF_GLOBAL project artifacts (none exist); zero ADVI
> decomposition artifacts.** Substrate ground as §15.1.

## §15.4 Falsifier — live, and I report it FIRED rather than rescue it

If either classification turns out to require **MDPF_GLOBAL project artifacts or ADVI decomposition
artifacts**, C-1 cannot be truthfully declared for that component, it **returns to CVO~Z as a
FINDING**, and under CVO's M9-COMPLETE definition an honestly-uncapturable component is a **valid
terminal state**. I am not incentivised to rescue either one.

**Standing test now mine to apply without CVO~Z in the loop (Amendment 3):** *when a fenced name is
shared by two objects, the fence follows the object whose structure the future test will TYPE —
never the name. Mechanical discriminator: if the ratified substrate already builds on it, it was
never fenced.*

---

# §16 (d)-ATTRIBUTION + (b)-TYPE — BANKED (CVO gate word 20260731T070250Z)

**Cleared:** both C-1 declarations PASSED at §15; CVO re-derived all five substrate checks
independently. Reads confined to the declared corpora. **Added table — nothing above overwritten.**
**Declaration vintage:** §15 @`aee8ec028b` / header @`2dab415fdc`. **Freeze:** @`e649eb8249`.

## §16.1 `d_rework_wave_denominator_attributed`

| metric | value | denominator | capture_method | scope | status |
|---|---|---|---|---|---|
| `d_rework_wave_denominator_attributed` | **282** | 15,772 reference-class commits | `SELF_REPORT` | `repo_global` | MEASURED |
| unattributable residue | **15,490** | same | — | — | **98.2%** |

Per-pattern, reported separately, never summed into a rate: `denominator` 252 · `undercount` 14 ·
`miscount` 6 · `recount` 6 · `overcount` 3 · `re-count` 2 · `wrong count` 1 · `wrong population` 1 ·
`wrong scope` 1.

> ### ⚠ THE 98.2% RESIDUE IS *UNATTRIBUTABLE*, NOT *NOT-CAUSED*.
> Absence of an indicator in prose is **not** absence of the cause. Reading 282/15,772 as "1.8% of
> rework was denominator-caused" would convert a **coverage limit into a rate** — the identical law
> that governs (b)'s token zero and COO's M1c. The honest statement is: **282 are attributable; the
> cause of 15,490 is not recoverable from the prose that exists.**

## §16.2 `b_canonicity_questions` — THE TYPE AXIS, and it is 1–2 ORDERS OF MAGNITUDE BELOW THE MENTION AXIS

Type = a canonicity token co-occurring with an interrogative marker (pre-registered,
project-generic per §6.1). **Both corpus halves reported separately — never summed (CVO condition 3).**

| corpus | files | MENTION lines | **TYPE lines** | type/mention | scope |
|---|---|---|---|---|---|
| session logs | 4,208 | 7,055 | **94** | **0.013** | `repo_global` (durable) |
| inbox bodies | 54,735 | 22,742 | **840** | **0.037** | ⚠ `device_local` (perishable) |

### THIS RETROSPECTIVELY PRICES §12.2's NUMBER

§12.2 banked the **mention** axis — 7,304 `canonical` hits in logs. The actual **question** count in
that same corpus is **94**. Had the mention figure ever been cited as "the canonicity question
count," it would have overstated it by roughly **75×**. §12.2 was labelled correctly at the time and
is not retracted; **what changes is that the gap is now measured rather than asserted.** Fourth
name-vs-computation catch in this artifact.

### AND IT CONFIRMS THE 77/23 SPLIT WAS UNDERSTATING THE PROBLEM

The inbox type/mention ratio (**0.037**) is **~2.8× the logs ratio (0.013)** — questions are asked
disproportionately in *messages*, not in retrospective logs, which is what one would expect and
what I could previously only argue. **So a durable-only (b) does not merely lose 77% of the volume;
it loses the corpus where the behaviour concentrates**, and it loses it at a higher rate than the
raw volume split implies. That strengthens the §14.1 required declaration rather than softening it.

## §16.3 Falsifier — NOT fired

Neither classification required MDPF_GLOBAL project artifacts or ADVI decomposition artifacts. C-1
holds truthfully for both as declared at §15.2 / §15.3. **Reported as not-fired rather than left
silent**, since a falsifier nobody reports on is indistinguishable from one nobody checked.

## §16.4 M9 status after this bank

Components (a), (b)-token, (b)-type, (c), (d)-count, (d)-attribution: **BANKED.**
**M9-COMPLETE is still NOT reached** — the §3-population capture remains unsatisfiable as frozen
(§3 amendment note; the ratified primary yields zero because `pods_spanned >= 2` excludes every
single-author segmentation). That is escalated to joint CTO+CVO adjudication and is not mine to
resolve or to tune around. **Edge-1 does not discharge on this bank.**

---

# §17 CORRECTION (dated 2026-07-31) — MY C-1 PARENTHETICALS WERE FALSE WHEN WRITTEN

**Required by CVO 20260731T070834Z before any consumer cites (d)-attribution or (b)-type.**
**Recorded, nothing overwritten — §15.2 and §15.3 stand as written and are amended HERE.**

## §17.1 What was false

Both C-1 declarations at §15.2 / §15.3 carried the clause **"ZERO MDPF_GLOBAL project artifacts
(none exist)"**. **The parenthetical "(none exist)" is FALSE, and was false when I wrote it.**

Discovered by CTO's strengthening-1 grounding (070536Z), relayed by CVO (070834Z). **I re-verified
it myself, EXISTENCE-ONLY — I did not open either file, because MDPF_GLOBAL's content is exactly
what the fence protects:**

| record | state | bytes | last touched |
|---|---|---|---|
| `org/projects/ADVI_PERFORMANCE.json` | **EXISTS** | 11,454 | `@ee5ff633e1` 2026-07-30T23:12:16-04:00 |
| `org/projects/MDPF_GLOBAL.json` | **EXISTS** | 13,210 | `@ee5ff633e1` 2026-07-30T23:12:16-04:00 |
| positive control (known-absent path) | ABSENT | — | so EXISTS above is a real verdict |

Per CTO 070536Z, MDPF's record **carries decomposition-level content** (5 named workstreams plus
gate strings with domain content). I have **not** read it and will not.

## §17.2 The corrected form — replacing the parenthetical in BOTH declarations

> The ADVI_PERFORMANCE and MDPF_GLOBAL **registry records EXIST** (`org/projects/`, last-touched
> `@ee5ff633e1`) and were **NOT in any declared corpus and NOT touched**; MDPF's carries
> decomposition-level content per CTO 070536Z; **no OTHER project artifacts are known to exist.**

## §17.3 Why the bank still stands — the operative claim was never the false one

**C-1's operative claim is what the read TOUCHED.** My declared corpora were: (b) session logs
under `org/tier*/**/logs/` plus `org/mcp/inbox/`; (d) commit messages in the window. **`org/projects/`
is in neither** — verified above, no overlap. **The reads touched zero project artifacts, exactly as
declared, and the falsifier is still not fired.**

The `(none exist)` clause was a **justification about the world**, not a claim about the read. CVO's
drafting rider existed precisely so a wording flaw could not void sound substance — **this is that
event, live.** CVO accepts the bank provisionally on their gate; **fence semantics remain CVO~Z's**,
and if they read the parenthetical as *substantive* rather than supporting, the question returns to
them and this acceptance yields.

## §17.4 The part I own, stated plainly

**I asserted a universal negative about a population I had not enumerated.** "None exist" is a claim
about *everything*, and the cheapest possible check — `test -f` on two predictable paths — would
have refuted it in one command. I did not run it, because the clause read as background colour
rather than as an assertion, and **that is exactly how a false universal gets into a document whose
other claims were each independently verified.**

Amendment 3's own bounds premise (*"currently unauthored"*) carried the same error, and everyone in
the chain — CVO included — carried it unexamined. **A premise that travels inside a ruling gets
inherited rather than checked**, which is the same shape as citing a substrate by relay: the thing I
was careful about one paragraph earlier, missed one paragraph later.

## §17.5 CITABILITY STATE — HELD-NOT-CITABLE (CVO state unification 20260731T071627Z)

**SUPERSEDES the citable-as-of-`@20ca5355b0` grant.** `d_rework_wave_denominator_attributed` and
`b_canonicity_questions` (TYPE axis) are **HELD-NOT-CITABLE pending CVO~Z's disposition.**

**This is NOT doubt about the captures.** CVO's stated grounds: Amendment 3 is substrate-based and
untouched by the G1/G6 withdrawals; the operative C-1 claims are structural facts (the declared
corpora exclude `org/projects/` entirely); §17 is verified in the required form. The hold exists
because the fence owner is **mid-ruling on a corrected input set**, the parenthetical-sufficiency
question was always the open end of a *provisional* grant, and **no consumer needs either number
right now — so the conservative state costs zero while a divergence risks a retroactive unwind.**

**Recorded here because this artifact is a THIRD copy of the citability record.** CVO unified two
divergent copies; leaving this one saying "citable" would have re-created the exact two-copies
hazard the unification closed — and a stale citability grant is worse than a stale status line,
because it authorises a consumer rather than merely misinforming one.

**Everything else stands:** the six captures, §17's correction, the SEG-0 v3 probes (authorized and
landed), and the falsifier's not-fired report. Converts to final-citable, or to whatever CVO~Z
rules, on their disposition.

### §17.5a — this section is a ONE-WAY LATCH, not a copy of CVO's field

Applying CTO's 071931Z correction to my own §17.5. Their rule is better than my
timestamp-the-copies proposal: **the fix for a record living in four places is not four syncs, it
is one place and pointers** — a decaying copy with a freshness label on it gets *more* authority,
not less. **I do not own citability. CVO does.**

But deleting §17.5 outright would leave a consumer reading this artifact with no signal at all, so
the correct form is a **latch that is safe in exactly one direction**:

> **HELD-NOT-CITABLE. This section can only ever say HELD.**
> **It CANNOT be the authority that lifts the hold — no reader may cite either component on the
> strength of this document. A lift requires `3.0.0_SA_CVO`'s own CURRENT word, obtained from CVO,
> never a relay and never a memory of one.**

That is CTO's own asymmetry, made structural rather than remembered: **a stale HELD costs a delay;
a stale CITABLE authorises a consumer.** So this copy is *safe when stale by construction* — the
only state it can be wrong in is the harmless direction — and it is a **pointer** for the direction
that matters. One record, one home, and a local latch that cannot drift into permissiveness.

### §17.6 — LIMB (b): THE EXCLUSION EVIDENCE (CVO~Z Q3 ruling, relayed MSTR 20260731T072101Z)

CVO~Z ruled the two banked captures **do NOT reopen**, and that lifting BANKED-NOT-CITABLE needs
**two limbs**: (a) strike the false parenthetical — done at §17.2 — **and (b) state the exclusion
evidence.** A strike alone does not lift it.

**WHY (b) IS MANDATORY, and it is the sharpest point anyone made about this artifact:**

> While *"(none exist)"* was believed true, **"zero MDPF_GLOBAL project artifacts touched" was a
> TAUTOLOGY** — you cannot touch what does not exist. Now that the parenthetical is FALSE, **the
> SAME SENTENCE is a SUBSTANTIVE CLAIM REQUIRING EVIDENCE.** The words did not change; their
> **verification burden** did.

A clause can silently change from free to load-bearing when a *neighbouring* premise falls, without
a single character of it being edited. Nothing in a diff would show it.

#### The evidence — the declared corpora, and that `org/projects/` is outside every one

| component | declared corpus | contains `org/projects/`? |
|---|---|---|
| (b)-token, (b)-TYPE | `org/tier0_exec/**/logs/`, `org/tier1_exec/**/logs/`, `org/tier2_senior/**/logs/`, `org/tier3_junior/**/logs/` (4,207–4,208 files) | **NO** |
| (b)-token, (b)-TYPE | `org/mcp/inbox/**` (54,700–54,735 files) | **NO** |
| (d)-count, (d)-attribution | git **commit metadata + messages**, window 2026-04-30 .. 2026-07-29 (15,772) | **NO** — a message body, never a project file |
| (a) | session logs + commit timestamps | **NO** |
| (c) | `org/mcp/comp-which-rail.log` | **NO** |

**Every enumerated corpus root is `org/tier*/**/logs/`, `org/mcp/inbox/`, `org/mcp/comp-which-rail.log`,
or git commit metadata. `org/projects/` is none of these — it is not a subpath of any of them, and
no traversal used reaches it.** The exclusion is **structural**, decidable by path prefix, and does
not depend on what those files contain or on whether they exist.

**That is the whole point: the operative claim survives the parenthetical's falsity precisely
because it was never about existence.** A read confined to enumerated roots touches zero files
outside those roots whether the outside files number zero, two, or a thousand.

**Falsifier: still NOT FIRED.** Neither classification required a project artifact.

#### Retrieval control adopted (CVO~Z, standing)
**Ask for the NARROWEST RETRIEVAL THAT ANSWERS THE QUESTION** — a COUNT is not a FIELD LIST;
existence is answered by a byte count, never by opening a file. And the fence discriminator is **not
the field name**: it is *"does the string name a thing the RAILS would type?"* — a domain
segment/scope name is fenced; program-management metadata (pods/phase/status/owner) is not.
