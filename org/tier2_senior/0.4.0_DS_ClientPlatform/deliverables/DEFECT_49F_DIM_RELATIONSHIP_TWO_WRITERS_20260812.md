# DEFECT (filed, NOT fixed here): `dimensions/dim_relationship` has TWO WRITERS in two knob groups

**Filed:** 2026-08-12 ~13:55Z by `0.4.0_DS_ClientPlatform` · **Adjudication:** P5, bundled with the
knob-2 supersession question (COO ruling 135005Z: "they are one disposition ... adjudicated
together in P5 rather than rediscovered")
**Status:** FILED — deliberately NOT fixed inside the P3 re-point.

## The defect

Two producers write the same gold table, from different root knobs:

| writer | knob | mechanism | write path |
|---|---|---|---|
| `a01_dim_relationship.py` | K1 | `rc.emit(table=TABLE)` | `{runner_common.OUT_ROOT}/dimensions/dim_relationship/date={D}/` |
| `a01_runner.py:30` | K2 + K3 | direct `put_object` | `'schwab/08335338/gold/dimensions/dim_relationship/'` (hardcoded literal) |

Consumer: `c02_runner.py` reads `DIMR_PREFIX = f'{SCOPE}/gold/dimensions/dim_relationship/'`.
My D-family (`d04`/`d05`/`d14`) also consumes `dimensions/dim_relationship`.

## ⚠ WHY IT HAS NEVER BITTEN — a coincidence mistaken for a design

`a00_runner.py:41` `SCOPE = 'schwab/08335338'` and `runner_common.py:28` `SCOPE = "schwab/08335338"`
are **byte-identical**, and the K3 literal is that same root spelled out. **All three resolve to one
prefix, so the two writers have never diverged — not because anything reconciles them, but because
they happen to agree.** The collision is LIVE and merely MASKED.

**Anyone touching either writer must know this**: change one root and the two producers silently
write different locations; change neither and the last runner to execute silently wins the key.

## Measured state at filing (denominators)

- On S3: `dim_relationship` has **2 partitions, newest 2026-07-15** — `schema_version=1.0`,
  `source_pipeline` ABSENT. That is the **K2** shape.
- My K1 producer's schema-2.0 output (`source_pipeline='49f-gold-runners'`) has **never been
  uploaded** — the P1 evidence runs were `--local-out` throughout.
- So today the two writers have not actually raced: one is local-only, the other last wrote 28 days
  ago. **The race is available, not yet run.**

## Why it is NOT fixed under the P3 cutover (COO 135005Z, adopted)

> "a cutover's job is to change WHERE, not to change WHAT. Fixing a two-writer defect inside a
> re-point means a failure afterwards has two candidate causes."

Under P3 option (a) the collision stays exactly as masked as it is today — no better, no worse —
because all three knobs move to one new root together.

## ⚠ A POST-CUTOVER COLLISION WOULD BE A SILENT SCHEMA FLIP, NOT A DUPLICATE WRITE

The two writers **do not emit the same shape**. K2 (`a01_runner`) writes `schema_version=1.0` with
**no** `source_pipeline` column; K1 (`a01_dim_relationship`) writes `schema_version=2.0` with
`source_pipeline='49f-gold-runners'` (the fact_fam rewrite). So if both ever run against one root,
the winner is **whichever ran last, and the table's SCHEMA changes with it** — consumers would see a
column set flip, not a value differ. That is materially worse than a duplicate write and it is the
discriminator a P5 reader needs first.

## ⛔⛔ PROHIBITION — DO NOT NORMALISE THE TWO SCHEMAS (CTO, relayed COO 142708Z, verbatim)

> *"If anyone NORMALISED those two schemas to make the tables comparable, the collision would go
> dark while remaining live. Unifying a representation without assigning ownership conceals the
> collision — same lesson, different tree, and in their case the 'incidental' thing making it
> visible is a schema version."*

**NOBODY MAY NORMALISE K2's `schema_version=1.0` (no `source_pipeline`) TO K1's `schema_version=2.0`
TO MAKE THE TABLES COMPARABLE.** Assign ownership first — normalise never, or only after.

⚠ **THIS IS THE SECOND MASKING LAYER, AND THE DANGEROUS ONE.** The first (identical root strings,
above) hides the collision **by accident**. This one would be removed **ON PURPOSE**: the instinct
to tidy is exactly what fires on a file describing two writers emitting different shapes, and the
tidy-up *looks like cleanup while deleting the only signal that the collision exists.* The same
shape as the withdrawn `bronze/assets` format port — there the incidental tell was a file format,
here it is a schema version.

## The question it must be adjudicated WITH — AND ITS NOW-REGISTERED METHOD

**Is knob 2 SUPERSEDED (by the P1 corpus) or merely STOPPED?** Not answerable from data as filed:
"stopped 28 days, 3 canonical tables never emitted" is consistent with both, and 28 days is nowhere
near the 90-day dormancy bar, so no standing rule reaches it. **If SUPERSEDED**, retiring
`a01_runner` deletes this defect outright. **If STOPPED**, the defect must be fixed by choosing one
writer. Either way it is a P5 decommission decision, not a cutover act.

⭐ **METHOD REGISTERED 2026-08-12 (CTO ruling, relayed COO 142708Z) — this question is no longer
methodless.** The **CONSUMPTION MAP** (what reads each key · what else each path does · coverage/dim
parity) is specified GENERALLY and registered as the named method for the P5 spec's
`SUPERSEDED` discrimination, which demands *"named successor + migration record VERIFIED live-plane"*
and previously supplied no method. **This defect's superseded-vs-stopped, CTO's what-reads-each-key,
and that spec's abandoned-vs-migrated are ONE QUESTION WITH THREE NAMES.** The `inf` fork is the
method's first EXERCISE, not its purpose.
> ⛔ **So P5 must run the consumption map here rather than inherit the (a)-ruling's ASYMMETRY
> ARGUMENT as though it were the answer.** *(a) was ruled on asymmetry precisely BECAUSE no
> discriminator existed — the right call with no method available, and a worse one than a method
> makes.*

## ⛔ ONE DOCUMENT SENTENCE THAT MUST NOT BE CITED HERE — CONSIDERED AND FOUND SILENT

`runner_common.py:3-6` reads: *"...every existing runner in this corpus carried its own copy of
partition listing / parquet read / write-verify -- four ad-hoc copies before this module unified them
(build-ladder rung 2). New artifact scripts use THIS layer; the a00/a01 runners keep their exercised
copies until their own next touch (extract-side-only)."*

**Both the producing seat and COO overreached on this sentence in OPPOSITE directions and BOTH
withdrew** (0.4.0_DS 135247Z read it as supersession; 2.0.0_SA_COO 135351Z read it as a coexistence
commitment and withdrew basis #1 explicitly). **The paragraph's subject is the HELPER LAYER** —
partition listing, parquet read, write-verify. It records **deliberate NON-MIGRATION of helper code
at extraction time** and is **SILENT on production topology.**

> **It must NOT be cited as evidence that knob 2 is deliberately retained, nor that it is
> superseded. It was CONSIDERED AND FOUND SILENT — not overlooked.** Citing it either way would be
> declarative drift: a docstring about function duplication hardening into a topology ruling.

**THE STANDING BASIS for re-pointing rather than retiring (COO 135351Z, ruling (a)):**
1. **Superseded-vs-stopped is unanswerable from data** (the `gold/clients/` discriminator: 126 days
   read "abandoned" while its live successor sat one prefix over), and no standing rule reaches 28 days.
2. **Asymmetry:** (a) does not foreclose (b); (b) forecloses the answer.
3. **Sequencing:** a cutover is the wrong cover for a decommission — interleaved evidence, neither
   act cleanly reversible.

## Residual risk carried until then (the reason this is filed rather than shrugged)

A latent chain that starts running post-cutover would write and read the OLD root silently — and a
second writer on one key makes "which output is authoritative?" unanswerable after the fact rather
than before it.
