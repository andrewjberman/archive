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

## The question it must be adjudicated WITH

**Is knob 2 SUPERSEDED (by the P1 corpus) or merely STOPPED?** Not answerable from data: "stopped 28
days, 3 canonical tables never emitted" is consistent with both, and 28 days is nowhere near the
90-day dormancy bar, so no standing rule reaches it. **If SUPERSEDED**, retiring `a01_runner`
deletes this defect outright. **If STOPPED**, the defect must be fixed by choosing one writer.
Either way it is a P5 decommission decision, not a cutover act.

## Residual risk carried until then (the reason this is filed rather than shrugged)

A latent chain that starts running post-cutover would write and read the OLD root silently — and a
second writer on one key makes "which output is authoritative?" unanswerable after the fact rather
than before it.
