# TO MDPF_EVR.FE-2 — render `reconstructed` points as ORDINARY (measured-identical pixels, label preserved)

<task_order id="MDPF_EVR.FE-2" project="MDPF_EVR">
<issued_to>0.4.0_DE_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-15T18:55Z</issued>
<status>complete</status>
<completed>2026-08-15T19:3xZ by 0.4.0_DE_ClientPlatform -- portal DEV 778ea780 (core Implementation B) + e8b1fb07 (AC-8 per-firm flat point_class[] read, COO-ruled 190348Z); proof-of-spec instance VALID rc=0 (8/8 rows PASS, mutant FIRED-AS-EXPECTED, determinism STABLE); AC-7 VALUE numbers unchanged before/after (band-extent 0->0, ranges []->[], value sum identical); PNG portal/.frontend-dev/screenshots/mdpf_evr_fe2_inflection_after.png (control: _coreB_778ea780.png, chart panels pixel-identical). Log: org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-08-15/mdpf_evr_fe2_reconstructed_ordinary_1849-1930Z.md. Awaiting COO validate/close.</completed>
<validated>2026-08-15T19:35Z by 2.0.0_SA_COO (issuer) -- INDEPENDENT: proof-of-spec re-run rc=0 (8 rows, 0 violations); DE's exercise instrument run by COO against COO's OWN S3 pulls of the served inflection + global artifacts = 75 PASS / 0 FAIL; pre-change module (684e67de) against the same inputs = 40 FAIL / exit=1 (instrument discriminates); AC-7 VALUE numbers reproduced (band-extent 0, ranges [], aggregate sum 78,209,487,100.32 over 445/445 -- only labels move, no STOP condition); AC-8 live carry {measured 438, reconstructed 7} on all series; PNG READ by COO: no band/dash/legend, 7 dates indistinguishable, color law clean. CLOSED. Portal DEV 778ea780 + e8b1fb07 UNPUSHED (lanes commit, integrators push); PROD promote = DT lane on Andrew's word.</validated>
<post_close_correction date="2026-08-18T13:15Z" by="2.0.0_SA_COO (issuer)">THE 49F PROVENANCE SURPRISE IS FALSIFIED -- CORRECTION ATTACHED TO THE CLAIM BECAUSE THE SEAT THAT RAISED IT IS STOOD DOWN. DE's 190236Z surprise-channel line ("the served 49financial slice's cohort_provenance has a class distribution count-identical to cottonwood's -- 411 custody-absent / 44 / 32 / 15 -- smells like a mis-sourced provenance channel on 49f") was relayed by COO (190743Z, as ungrounded/routed) and by MSTR (190653Z, WITH added confidence MSTR has since retracted 131138Z as their own error: editorialised on a number they had not re-derived). CTO FALSIFIED IT ON THE ARTIFACT (130828Z): platinum/mdpf/49financial/aggregate-aua-timeseries.json read at THREE versions -- current (08-17T13:50:49Z), the 08-15T13:50:49Z version LIVE WHEN DE MEASURED, and the legacy json/mdpf/49financial key -- ALL carry cohort_provenance rows {custody:'Schwab', model:'SmartX'} x445/446/429, index-aligned, no date key, no class enums; point_class[] = measured x445/446; negative control on a nonexistent prefix = 0. The 411/44/32/15 distribution is exactly and ONLY cottonwood's served slice. VERDICT: a WRONG-FIRM READ ON THE MEASUREMENT SIDE, not a mis-sourced producer -- the served 49F provenance channel does not describe cottonwood. Nothing was acted on (correctly scoped as a LOOK; cost = one CTO read). DE's log at logs/2026-08-15/mdpf_evr_fe2_reconstructed_ordinary_1849-1930Z.md:117 carries the original claim; any DE session reading that log meets this correction here first. THE REAL FINDING UNDERNEATH (CTO): cohort_provenance carries THREE shapes across four scopes (per-firm inflection/49f = source names, no date; cottonwood = dated class enums; global = dated per-partner slots), so one declared FE reader schema cannot be right for more than one -- CTO ruling in flight; that ruling, not this smell, is the thing to read.</post_close_correction>
<priority>P2 — Andrew-direct ruling, spawn-triggered (MSTR spawned DE for this)</priority>
<authority>Andrew-direct at the MSTR terminal 2026-08-15, VERBATIM: "yes they should render as ordinary points" — answering the open question MSTR surfaced after his ~0350Z ruling "i dont want to draw attention to the interpolated points at all, no one cares about that, its more problematic to open up the can of worms and seed doubt rather than just another data point that is probably within 10bps anyway on a random day no one cares about". Record: org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20260815_NO_FIRST_CLASSING_RECONSTRUCTED_POINTS.md + LD-0417 (MSTR broadcast 184917Z).</authority>
<supersedes>NOTHING. MDPF_EVR.FE-1 (cancelled @bc686bde7e) asked for the OPPOSITE outcome (make reconstructed MORE distinct). This TO has an inverted objective and is NOT FE-1 reinstated.</supersedes>
</task_order>

## THE IMPLEMENTATION CONSTRAINT IS THE WHOLE TO — read this before the objective

`portal/src/lib/pairedProvenanceRead.ts` carries a closed 3-value render enum
(`PointClass = 'measured' | 'interpolated_estimate' | 'absent'`, `:33`; `VALID` set `:159`) and
the law at `:29`: **"Never silently 'measured'."** Unknown strings degrade LOUD to
`interpolated_estimate` + `console.warn` (`slotClass` `:271-274`). Today `reconstructed` is such an
unknown string, so the 7 reconstructed inflection points render estimate-class with a warn.

**IMPLEMENTATION A — REJECTED, named so nobody "simplifies" into it:** map `reconstructed ->
'measured'`. That inverts `:29` and ASSERTS a reconstructed value is measured — precisely what the
ratified EVR `reconstructed-never-measured` honesty condition forbids. Nobody asked for it.

**IMPLEMENTATION B — ADOPTED:** add `'reconstructed'` to the closed enum as its OWN member, give it
MEASURED-IDENTICAL STYLING at every render site, and drop the console warn for this now-KNOWN class.
The point renders ordinary — his ask — while the TYPE and the SERVED DATA still say `reconstructed`.
Under B nothing is ever LABELLED measured; the honesty condition governs CLAIMS, not pixels.

**THREE COLLAPSE POINTS THAT WOULD SILENTLY TURN B INTO A — source-read by the issuer, all three
must carry the class through, not collapse it:**
1. `pairedProvenanceRead.ts:271-276` `slotClass` — once in `VALID`, the raw string returns as-is.
   Correct; no change beyond the enum + VALID additions.
2. `pairedProvenanceRead.ts:280-294` `derivedFirmClass` — the fall-through at `:294` returns
   `{ cls: 'measured' }` for anything not interpolated/absent. **A `reconstructed` slot would be
   RELABELLED `measured` here.** Add the explicit branch: any slot `reconstructed` (and none
   interpolated) -> firm class `reconstructed`. Decide + document precedence when custody and model
   slots differ (recommend: `interpolated_estimate` > `reconstructed` > `measured`, matching the
   existing any-cohort-interpolated derivation).
3. `portal/src/pages/ModelPortfolios.tsx:731-737` (Global aggregate row) — collapses to
   `interpolated_estimate` vs `'measured'`. **A reconstructed date would be RELABELLED `measured`
   here.** Carry `reconstructed` through (same precedence rule).
Any other site that narrows the class to a 2-way measured/interpolated split is the same defect —
grep `pointClass` / `PointClass` consumers and enumerate them in your report WITH THE DENOMINATOR.

**4. [ADDED 1904Z — DE scope surface 190236Z, VERIFIED by the issuer on the served artifact]:
`provenanceIndex` `:245-249` — on the LIVE per-firm inflection slice
(`s3://opal-data-portal-v2/platinum/mdpf/inflection/aggregate-aua-timeseries.json`, publisher
written_at 2026-08-15T13:50Z) `cohort_provenance` has 445 entries and ZERO carry a `date` key
(model slot = source names: 'Eclipse' x438 / 'reconstructed(evr-1.0.0) -- ...' x7). The reader
returns null -> predates-contract -> ALL 445 points labelled `measured`, INCLUDING the 7
reconstructed. PREMISE CORRECTION: on per-firm the 7 do NOT render estimate-class today — they
already render ordinary AND are already RELABELLED `measured` via the fail-safe (Implementation A,
pre-existing). The class IS served on that slice in the date-aligned `point_class[]`
({measured 438, reconstructed 7}) which the per-firm reader by contract (`:141-148`) never reads.
RULING (COO 190348Z): land a per-firm `point_class[]` array read as a SEPARATE commit after core B —
fail-safe ORDER: (1) cohort channel well-formed -> slots as today; (2) cohort malformed/absent AND
`point_class[]` present + length-aligned to `dates[]` -> array read (unknown strings still degrade
LOUD via VALID; add a mutant fixture on this path); (3) neither -> predates-contract `measured` as
today. Length-misaligned array = malformed = warn + (3), never index-guess. Keep the malformed-
channel warn. The `:141-148` per-grain derivation-owner rule is AMENDED by this ruling (the flat
array owns derivation for that grain when the cohort channel cannot carry classes) — document
in-code beside `:141`. Global's `readGlobalPointClass` (2 reconstructed dates) is in core-B scope.**
**ROOT NOT CLOSED BY THIS FIX (MSTR 190626Z, routed to CTO by COO): a date-less `cohort_provenance`
beside a date-aligned `point_class[]` is a PRODUCER/CONSUMER CONTRACT MISMATCH — the reader expects
dated cohort entries (`:13-14` schema SoT), the producer emits an aligned array. The fail-safe order
above is the correct CONSUMER-side hardening and is correct under EITHER canonical answer — which is
exactly why the FE fix must NOT be read as closing the question. Which form is canonical is CTO's
architecture call, routed 1908Z. DE does not wait on it.**

## Objective

The 7 `reconstructed` inflection points (served MDPF provenance lattice: {438 measured, 7
reconstructed}) render **visually indistinguishable from measured points** — same marker, same
stroke, no estimate band/dash/hollow treatment, no tooltip badge that singles them out — with **no
console warn** for the class, while `pointClass === 'reconstructed'` remains true in the paired
read output and in the served data.

## Scope — `reconstructed` ONLY. Do not widen on inference.

- `carried` / `carried_at_declared_cadence(...)` is **OUT OF SCOPE** — different mechanism
  (carry-forward), not the subject of his words. It keeps today's treatment unchanged.
- The EVR emitter + its outputs (Andrew "yes to both" @e4251a4567) are UNTOUCHED.
- The server-side provenance lattice / `point_class` in served data is UNTOUCHED.
- The ratified EVR honesty conditions are UNTOUCHED (B is designed to satisfy them; CRO/CTO own
  the condition and confirm the read — you do NOT wait on that confirmation).

## The safety property MUST survive — this is acceptance-critical

The `:29` law needs a carve-out for a KNOWN class carrying a deliberate presentation ruling, as
distinct from an UNKNOWN string. **An unrecognised class must still degrade LOUD to
`interpolated_estimate` and still warn.** It would be easy to implement this by weakening the
degrade path generally — that is a regression dressed as a feature.
**MUTANT TEST (required):** a test feeding a fabricated garbage class (e.g. `'zzz_no_such_class'`)
through `slotClass`/the paired read must still yield `interpolated_estimate` + a warn. Show it
FAILING against the pre-change code path if the carve-out were written wrong (i.e. prove the test
can fail), then PASSING on your change.

## Portal discipline

- Main portal tree stays on **DEV** (Rule 19) — verified on DEV at TO authoring.
- Rule 20 before commit: `comp-transform schema-check ModelPortfolios` (and any component you
  touch) + `comp-transform ternary-audit ModelPortfolios` (you are adding a new enum member — that
  is exactly the new-mode case).
- **`/frontend-dev` rendered-screenshot check is the acceptance instrument** — the deliverable IS a
  visual outcome; a grep cannot see whether a point looks ordinary. Render the Model Portfolios
  route, READ the PNG, confirm the 7 reconstructed points are indistinguishable from neighbours.
- Commit under your own author line via `.tools/safe-commit.sh` inside `portal/` (its own repo,
  DEV branch); explicit file pathspecs only.

## Acceptance criteria (machine-checkable where possible)

- AC-1: `PointClass` union + `VALID` set include `'reconstructed'`; served `reconstructed`
  slots return `cls: 'reconstructed'` from `slotClass` (unit test).
- AC-2: `derivedFirmClass` returns `reconstructed` for a reconstructed slot with no interpolated
  slot (unit test); precedence documented in-code.
- AC-3: Global aggregate row (`ModelPortfolios.tsx` ~`:731`) carries `reconstructed` through
  (unit or render test) — never relabelled measured.
- AC-4: zero `console.warn` emitted for `reconstructed` on the paired read of the live inflection
  artifact (test asserts warn count 0 for that class).
- AC-5: MUTANT — a fabricated unknown class still degrades to `interpolated_estimate` + warns
  (test present, shown able-to-fail, passing).
- AC-6: `/frontend-dev` screenshot: 7 reconstructed points visually indistinguishable from
  measured; `carried` treatment unchanged; PNG path cited in the report.
- AC-7: enumeration of every `pointClass`/`PointClass` consumer touched-or-confirmed-clean,
  with denominator, **AND the check shown ABLE TO FAIL**: point one consumer at a deliberately
  un-carried class (e.g. temporarily restore the `:294` fall-through, or feed a `reconstructed`
  slot through the Global-aggregate collapse unpatched) and demonstrate the enumeration REPORTS
  the relabel; then restore and show it clean. A "3 of 3 carry the class" line reads identical
  whether the check works or is vacuous.
- AC-7 SPLIT [ADDED 1908Z, MSTR 190626Z — ACCEPTANCE-CRITICAL, the screenshot cannot see it]:
  classify every consumer as **DISPLAY-ONLY** (styles on the label) vs **VALUE-AFFECTING**
  (BRANCHES on the label: an aggregate exclusion, a filter, a coverage count, a band-extent
  derivation — `pairedProvenanceRead.ts:21-22` states the BAND EXTENT ALWAYS DERIVES FROM
  point_class, so that is one such consumer by the file's own law). Today all 445 per-firm points
  are labelled `measured` via the fail-safe; after AC-8, 7 become `reconstructed`. **For every
  value-affecting consumer show the BEFORE/AFTER number. If any served or rendered NUMBER moves,
  STOP and report to COO + MSTR before landing — Andrew ruled on how points LOOK; he did not rule
  that a number may change.** Expected: zero numbers move (B styles reconstructed as measured, so
  band-extent and any measured-vs-estimate branch should treat it as measured-side) — but expected
  is not evidence; print the before/after.
- AC-8 [ADDED 1904Z]: per-firm inflection paired read on the LIVE served artifact returns
  `pointClass: 'reconstructed'` at exactly the 7 reconstructed dates and `'measured'` at 438
  (test fixture built from the served file; cite the S3 key + `written_at`); the malformed-
  channel warn still fires; a length-misaligned `point_class[]` fixture falls to predates-contract
  with a warn.

**TWO CLAIMS, TWO INSTRUMENTS — neither discharges the other (MSTR 185326Z, adopted 1858Z):**
| Claim | Instrument | Row |
|---|---|---|
| PIXEL claim — "renders ordinary" (Andrew's actual ask) | `/frontend-dev` rendered screenshot | AC-6 |
| LABEL claim — "never called measured" (the honesty condition) | derived-class read at EVERY consumer, able-to-fail | AC-7 (+AC-2, AC-3) |

**A screenshot is STRUCTURALLY INCAPABLE of seeing a relabel: under Implementation B a
reconstructed point styled-as-measured and a reconstructed point RELABELLED measured are
pixel-identical BY DESIGN.** So a green screenshot says nothing about AC-7, and AC-7 must never be
discharged with a PNG. Conversely, a clean consumer enumeration says nothing about whether the point
LOOKS ordinary. Both rows carry their own evidence in the proof-of-spec instance.

## proof_of_spec (machine-readable contract — Andrew-direct 2026-08-11)

<proof_of_spec>
  <expected_criteria>AC-1,AC-2,AC-3,AC-4,AC-5,AC-6,AC-7,AC-8</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/MDPF_EVR.FE-2_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

Assignee fills the instance (schema `org/standards/PROOF_OF_SPEC.schema.json`) from their OWN
efforts — one row per id, criterion VERBATIM + exact re-runnable invocation + evidence + denominator
— and validates BEFORE the `complete` flip with the POSITIONAL id form (there is no flag; a flagged
form exits rc=2 and the 2-arg fallback prints VALID with coverage UNCHECKED — CHECK THE RC):
`python .tools/proof-of-spec-check.py org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/MDPF_EVR.FE-2_PROOF_OF_SPEC.json AC-1,AC-2,AC-3,AC-4,AC-5,AC-6,AC-7,AC-8`
AC-6 evidence is the screenshot path + your read of it, not a class-name argument. AC-5 evidence
must show the mutant test able to fail (a dead mutant control invalidates the instance).

## compiler_tools_mandate

BEFORE WRITE: `comp-transform schema-check ModelPortfolios`; `comp-blast` on `pairedProvenanceRead`
(who else consumes the enum). BEFORE COMMIT: schema-check + ternary-audit + the portal pre-commit
hook. AFTER COMMIT: `/frontend-dev` screenshot (AC-6).

## cross_domain_coordination

`0.0.0_AB_MSTR` (arch, integration, push; spawned you for this). `2.0.0_SA_COO` (issuer; report
at completion with the proof-of-spec + screenshot). CRO/CTO confirm the honesty-condition read on
Implementation B in parallel — **NOT a gate on your work.**

## reporting

Report to `2.0.0_SA_COO` (cc `0.0.0_AB_MSTR`) at completion, or IMMEDIATELY if any consumer site
cannot carry the class through without a wider refactor (that is a scope surface, not a decision
you make alone). Surprise channel: one line to COO, no action, keep working.
