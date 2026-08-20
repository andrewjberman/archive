# FIELDHOME F2 — Rule-24 schema act: adding 3 PROSE_FIELD homes to the manifest-field axis

**Author:** 0.7.0_AE_CloudOps · **Date:** 2026-08-20 · **Gate:** 1.0.0_SA_CTO (per TO F2)
**TO:** OPAL_KIMIPIPELINE.FIELDHOME @2ba223ad98 · **CTO direction:** 63386
**Change:** `estate-coverage-manifest.yaml` thread rows may now carry `classification`,
`classification_reason`, and `enrichment` (joining the existing `description`), each read by
`gen-estate-resolver.py` with manifest-wins-over-census precedence (F1).

Adding field names to a schema is a SCHEMA-ENUMERATION act, which since the 2026-08-20 Rule-24
widening (Andrew-direct @1ab080d864: every schema-enumeration act — minting, adding values,
adopting — requires the four-postulate test) requires this record. **The axis under test is the
manifest thread-row FIELD-NAME SET** (which attributes a thread row may authoritatively declare).

## The four postulates

### (i) MECE — mutually exclusive, collectively exhaustive
The three additions are distinct attributes with no overlap, with each other or with the existing
fields:
- `classification` — the development-activity STRATUM label (active/maintained/dormant/…).
- `classification_reason` — the JUSTIFICATION for that label (evidence, grounding). A label vs its
  reason are two things; the generator already treats them separately (reads `classification_reason`
  for the orphan-candidate flag at the pre-F1 :71, never `classification`).
- `enrichment` — the PROCESSING/transformation steps a thread applies (dedup, parquet conversion,
  normalization). Distinct from `description` (identity/purpose) and from classification (activity).

COLLECTIVELY EXHAUSTIVE over the adjudicable axis: the runner allowlists exactly four PROSE_FIELDS
(`estate_report_runner.py:179` — `description / enrichment / classification / classification_reason`).
Before F1 the manifest homed 1 of 4; after F1 it homes 4 of 4 — the override surface is now exactly
the runner's prose axis, no more (routing fields are a separate axis, untouched), no less. MECE holds.

### (ii) SAME GRAIN
Every manifest field is a per-thread-row attribute (one value per `family`/thread_id). The three new
fields are per-thread-row, identical grain to `description`, `owning_tool`, `status`, and every other
manifest field. No file-level value beside a cohort-level value; no grain mix.

### (iii) INTENT COHERENCE — one axis, one intent
The manifest field-name set serves ONE intent: **the authoritative per-thread declaration surface
that overrides the derived/census default.** Routing fields (`owning_tool`/`status`/`named_thread`)
override the heuristic; prose fields override the frozen 2026-06-15 census. The three additions are
prose-value overrides — the SAME kind and SAME mechanism (manifest-wins at regen) as the existing
`description` prose override. No content-kind × handling-policy mix is introduced: all are
content-value declarations that win over a default. Intent coherent.

### (iv) STATE COHERENCE — the stability frame
State axis named: **homed vs unhomed**, over the runner's four PROSE_FIELDS.
- Before F1: `description` = HOMED (manifest row, `:81`); `classification` / `classification_reason` /
  `enrichment` = UNHOMED (flow only from the frozen census, no adjudication may edit it).
- The ONE remedy — F1's generator edit (`load_routing()` + `threads.append()` with the `:81`
  manifest-wins shape) — moves all THREE unhomed fields to HOMED **together**, in a single change,
  not three independent builds. After F1, all four PROSE_FIELDS are homed by one mechanism.

**Which values do NOT move together:** NONE. The axis passes cleanly — the remedy is a single
generator edit that homes every unhomed value on the axis at once. (This is the axis passing the
stability frame, the case the postulate is designed to confirm; the failure case it guards against —
values requiring different remedies — does not occur here.)

## Token-hygiene census (word-boundary occupancy over the canon files)

`\b<token>\b` counts, 2026-08-20:

| token | manifest | generator | census (pass1) | runner allowlist |
|---|---|---|---|---|
| `classification` | 0 | 8 | 238 | yes (:179) |
| `classification_reason` | 0 | 10 | 113 | yes (:179) |
| `enrichment` | 1* | 8 | 121 | yes (:179) |
| `description` (baseline, already homed) | 7 | 7 | 113 | yes (:179) |

- `classification` / `classification_reason`: **0 pre-existing manifest occurrences** — the field
  names are new to the manifest and collision-free.
- `enrichment`: the single manifest hit (*) is a SUB-TOKEN of the family NAME
  `causality-data-enrichment-movements` (line 334), NOT a field use. Zero field-level `enrichment:`
  occurrences pre-existed, so the field addition is collision-free; the word-boundary match on a
  hyphenated name is a census artifact, disclosed here, not a naming clash.
- No superstring collision: `\b` separates `classification` from `classification_reason` (verified —
  `classification` in `classification_reason:` does not match `\bclassification\b`). The generator's
  own usage confirms the two are distinct tokens with distinct call sites.

The tokens already carry a single ratified meaning across the census (source), the generator
(consumer), and the runner (allowlist author); the manifest addition adopts that same meaning — no
re-coinage, no second sense.

## Verdict
The manifest-field-axis enumeration passes all four postulates. The addition is MECE, same-grain,
intent-coherent, and state-coherent (one remedy homes every unhomed prose field together). CTO gates.

---

## F4 — ceo-daily-wsjft-digest: DECLARED EXCLUSION (never silent)

The entity `ceo-daily-wsjft-digest` is in the runner's canon universe (the `ceo-digest` vertical,
manifest `adjudications_20260730`) but is DELIBERATELY given NO manifest thread row at this landing.

**Reason.** Its identity is UNRECONCILED: the recorded entity name (`ceo-daily-wsjft-digest`), the
bucket (`astn` / `opal-data-astn`), and the true project code (`OPAL_ASTNWSJ`-or-similar) are not
yet mapped onto one another, and an output-quality review is open (estate-report 2026-08-20
proposal #1, Andrew **"approved"** — the ratified text is itself *about* the unreconciled identity).
Minting a thread row requires `owning_tool` / `status` / `named_thread` — ROUTING values, a NAMING
act that is not this prose lane's to author (0.8.0/CVO own the vertical assignment; 0.8.0 confirmed
this in msg 63436). Guessing them would assert facts the estate has not settled.

**Trigger to mint.** The row is minted WHEN the identity reconciles (project-code map + quality
review close). Until then the exclusion is DECLARED here (and in the RAVC close, cc CTO+CVO — never
silent), and the ratified description lives in the decision record (estate-report 2026-08-20) as its
provisional home.

## Landing-home note (why the mechanism lives in the generator, not the manifest yet)

F1's functional home is the **generator** (`gen-estate-resolver.py`, AE-committable): once a manifest
row carries an adjudicated `classification` / `classification_reason` / `enrichment`, it wins over
census at regen. That works NOW — proven by the 6/6 precedence battery. The manifest's own
**schema-comment documentation** of these fields (a nice-to-have for the next manifest editor) is
deferred to an exec commit: `estate-coverage-manifest.yaml` is owned-paths lane `ANY_EXEC` (a
CVO-authority determination file), so an AE landing schema-comment text into it would need an audited
AE-into-exec override on a CVO-authority file. Rather than override unilaterally, this is surfaced to
COO in the RAVC close: COO/CVO land the schema-comment (and, if wanted, the F4 exclusion note) in the
manifest, OR bless the audited override. **CVO's F3 port of the 5 ratified texts writes the manifest
rows regardless** — that port is CVO's (an exec) by the standing semantic-evolution mandate, so the
first real manifest prose-field values arrive through the sanctioned exec channel, and the mechanism
that makes them survive regen is already landed and battery-proven.
