# M9 PRE-FRAMEWORK BASELINE — SCHEMA DESIGN + PER-COMPONENT SOURCE DECLARATION

**Status:** PRE-MEASUREMENT. **No number is banked in this document and none may be until both
gates below clear.** This is the artifact-with-path CTO's precondition `@ee5ff633e1` discharges on.
**Author:** `0.7.0_AE_CloudOps~D` (measurement-plane seat) · **Date:** 2026-07-31
**Tasking:** `0.0.0_AB_MSTR` 20260731T055536Z (Andrew `/govern` + LD-0090 + CVO~Z fence ruling
`@4b94ad6f3` + CTO/CVO/CVO~Z convergence on a main non-rail-author seat)
**Gates:** SCHEMA -> `1.0.0_SA_CTO` (ESTATE arch-gate) before measuring · SOURCE DECLARATION ->
`3.0.0_SA_CVO` (baseline gate) before any number banks.

---

## §0 Capturer declaration (CVO~Z control 2, on the record at assignment)

While the held-out fence stands, I author, review and ratify **ZERO** WS-C1/C2 rail vocabulary.
I am measurement-plane only. I do not decompose ADVI_PERFORMANCE or MDPF_GLOBAL; capturing this
baseline is the pre-step that protects the decomposition, not the decomposition.

Fence basis (CVO~Z `@4b94ad6f3`): the apparent capture contradiction is an **equivocation** — a
build-cost baseline and a domain surface are different objects, and only the second is fenced.
This schema is built so that the first cannot carry the second (§2).

## §1 What M9 is, quoted not paraphrased

PROGRAM §5.9 declares M9 as ADVI_PERFORMANCE + MDPF_GLOBAL build cost vs their pre-framework
baseline, in **four components**:

| id | PROGRAM §5.9 wording |
|---|---|
| **a** | archaeology-vs-build wall-clock and agent-context |
| **b** | count of "which artifact is canonical / who writes this / is it live" questions |
| **c** | rail-override count |
| **d** | rework waves caused by a wrong denominator |

Also declared there: *"Hand-tagged is fine; it is a baseline, not a gate."* I am not inventing a
metric; I am making these four measurable without inventing vocabulary (arch-gate constraint 4).

## §2 THE ANTI-LEAK CONTROL — a CLOSED schema, not a careful author

CVO~Z control 1 excludes free text rather than discouraging it. **I implement the exclusion as a
TYPE, not as discipline: the schema below has no free-text field, so a surface leak is not
expressible in it.** Every field is one of — an integer, a real, an enumerated token from a fixed
list, an ISO-8601 timestamp, or a repo-relative source path.

This is deliberate and it is the whole design. *Care is not a control* — a schema that permits a
notes field and asks the author not to leak into it is a guard that depends on the guarded party's
attention, exactly the shape `docs/doctrine/CONTROLS_OVER_CARE.md` rejects. A closed schema fails
the leak at write time instead of at review time.

**Forbidden by construction (cannot be typed into any field):** ADVI/MDPF identifiers, field names,
path structures inside those products, grains, partition schemes, contract content.
**Permitted:** counts, durations, ratios, denominators, and source paths of the MEASUREMENT
instruments (never of the measured products).

## §3 The reference class — STRUCTURAL predicates, never product identity

A work unit enters the baseline population by **structural** predicate only. This is what lets the
population be defined without naming what is in it:

- `pods_spanned >= 2` (integer, from commit-author distinct-serial count)
- `has_served_consumer` (boolean)
- `delivered_within_window` (boolean)
- `unit_kind` ∈ {`new_surface`, `extension`, `migration`} (enumerated)

Inclusion/exclusion criteria are **frozen at gate-approval time and recorded with a commit hash.**
Choosing a reference class after seeing the treatment result is post-hoc and unfalsifiable; pinning
it before is the entire reason this capture is time-sensitive. That is pre-registration discipline,
and it is the honest sense in which this baseline is perishable.

## §4 The schema (every row: value + unit + denominator + source + status + window)

| field | type | notes |
|---|---|---|
| `component` | enum {`a`,`b`,`c`,`d`} | PROGRAM §5.9 id |
| `metric_id` | enum (fixed list, §4.1) | no free naming |
| `value` | number | — |
| `unit` | enum {`minutes`,`count`,`ratio`,`sessions`,`commits`} | — |
| `denominator` | number | **required, never null** |
| `denominator_of` | enum (fixed list) | what the denominator counts — closes the "number OF what" law |
| `source_path` | repo-relative path | measurement instrument only |
| `extraction` | enum {`deterministic`,`hand_tagged`} | deterministic-first per PROGRAM §6 |
| `status` | enum {`MEASURED`,`CARRIED`,`NOT_YET_MEASURABLE`} | COO's M-table convention, reused not reinvented |
| `window_start` / `window_end` | ISO-8601 | computed offsets, never a hand-typed `Z` |
| `scope` | enum {`device_local`,`repo_global`} | §5 — load-bearing |

### §4.1 Metric ids (fixed)

`a_archaeology_minutes` · `a_build_minutes` · `a_archaeology_ratio` · `a_context_sessions`
`b_canonicity_questions` · `c_rail_override_count` · `c_rail_deny_count`
`d_rework_waves` · `d_rework_waves_denominator_caused`

**Aggregate rule (inherited, not invented):** no aggregate headline without per-series
decomposition — the WS-E4.3 rule, which is already structural in `series()`.

## §5 PER-COMPONENT SOURCE DECLARATION (CVO's gate — read this before any number banks)

**Binding attestation: NO component below reads `org/mcp/agent_telemetry/` or the M3 verdict sink
`org/mcp/comp-tool-runs.jsonl`, pre-fix or post-fix.** The baseline must be methodologically the
first number, not a hand-tag/telemetry mix (axis-confusion, verification law 6). I am the seat that
repaired M3; reading my own in-repair instrument into the baseline is the exact conflation the
condition exists to prevent.

| comp | source | scope | extraction | non-M3 attestation |
|---|---|---|---|---|
| **a** | agent session logs `org/tier*/*/logs/**` + commit timestamps | `repo_global` | hand_tagged + deterministic timestamps | ✅ no telemetry read |
| **b** | session logs + `org/mcp/inbox/**` message bodies, matched against a FIXED question-pattern set | `repo_global` | deterministic first pass, hand_tagged residue, **both counts reported separately** | ✅ no telemetry read |
| **c** | `org/mcp/comp-which-rail.log` | ⚠ **`device_local`** | deterministic | ✅ rail log is a SEPARATE instrument from M3 — CVO ruled this explicitly at 20260731T023531Z |
| **d** | git commit history (revert/fix/correct subjects) + `docs/references/INCIDENTS_*.md` | `repo_global` | hand_tagged, criteria fixed at §3 freeze | ✅ no telemetry read |

### ⚠ §5.1 A DECLARED WEAKNESS IN COMPONENT (c) — surfaced now, not discovered later

**`org/mcp/comp-which-rail.log` is NOT TRACKED IN GIT** (verified: `git ls-files --error-unmatch`
fails; `.gitignore` carries the sibling telemetry sinks at `:261`, `:447-448`, `:454`). It is
**device-local**, so a rail-override count taken from it is **this device's traffic only and is
silently short by every other device's**. Current local file: 5,336,054 bytes.

This is not a defect I can fix and it is not a reason to skip (c) — PROGRAM §5.1 already cites a
187/month rail-override baseline, and COO's M1a measured 76 overrides against a 24,205-line
denominator from this same source. **It is a scope qualifier that must ride with the number
permanently**, because `scope` is exactly the field that gets dropped when a figure is quoted
onward. Hence `scope` is a required enum in the schema (§4) rather than a footnote.

## §6 THE ONE DESIGN FORK — named, with a decisive recommendation for CTO

Both products are **PHASE 0** (CTO `@ee5ff633e1`: 25,048 files / 23,518 commits / all branches
searched by MSTR~Z — 5 files describe the obligation, **zero capture it**; all 33 S3 buckets
negative per MSTR). Nothing has been built. So "pre-framework build cost" must be measured on
*something*, and there are exactly two candidates:

**Reading A — RETROSPECTIVE REFERENCE CLASS.** Measure a–d over comparable already-completed
conventional builds in the fabric's record, reference class pinned now per §3.

**Reading B — PROSPECTIVE FIRST SLICE.** Build one slice of ADVI/MDPF conventionally and measure it.

**I recommend A, and B is not merely weaker — it is structurally unavailable.** B requires
decomposing one of the two projects, which is precisely what CTO's precondition withholds until
this baseline exists. B is therefore circular: it can only be run by violating the control it would
serve. A is takeable today against data that already exists.

**THE LIMITATION THAT MUST RIDE WITH READING A, stated now rather than discovered at comparison
time:** under A the baseline measures *the fabric's conventional build cost on comparable work*,
**not those two products' own prior cost.** The eventual comparison is therefore across different
work, not a before/after on the same work — so a later delta is partly compositional and **may not
be read as purely causal**. Enumerate what the number is OF before explaining why it differs
(verification law 6). I would rather this be a declared limitation in the baseline than a
discovered confound in the verdict.

## §7 Sequence

1. CTO arch-gates this **schema** (§2–§4, §6 fork). No measuring before that word.
2. CVO reads the **source declaration** (§5, §5.1). No number banks before that word.
3. Freeze §3 criteria + record the freeze commit hash.
4. Measure. Land values as an **added table**, never overwriting a row (COO's baseline §4 rule).
5. Edge-1 discharges on this artifact having a path — never on a status claim.

## §8 What this document deliberately does NOT do

- Does not decompose ADVI_PERFORMANCE or MDPF_GLOBAL.
- Does not author, review or ratify rail vocabulary (§0).
- Does not bank a number (§7 sequence not yet run).
- Does not build a guard, alarm, monitor or checker — CTO `@ee5ff633e1` is explicit that the
  control here is a **work-ordering precondition in the record a decomposer reads, NOT a detector**,
  and that the moratorium must not be cited against it. Nothing in this schema fires anything.
