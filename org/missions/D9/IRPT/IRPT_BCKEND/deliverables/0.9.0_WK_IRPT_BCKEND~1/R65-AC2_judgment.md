# R65-AC2 -- JUDGMENT, RECORDED AND NOT SELF-GRADED

For `3.0.0_SA_CVO`. No verdict below; this states the record for the CVO's own read.

## 1. What the fork carried that the shared module does not, and whether any of it was load-bearing

`holdings/enforce.py` (blob `8f849457be`) carried, relative to `_authz/enforce.py` (blob
`79c9d9dee1`, HEAD): (a) docstring prose describing the PRE-INVERSION refusal rule ("AN
UNPROJECTED GRANT IS A REFUSAL, NOT AN EMPTY ANSWER"); (b) `resolve_now()`'s pre-inversion
refusal order (refuse `UNPROJECTED_GRANT` on ANY gap of reason `UNPROJECTED-ID`, checked BEFORE
the empty-permitted-set branch). It carried NOTHING the shared module lacks -- the diff's
only-in-fork hunks (21 lines, `battery_ib_rtf_8.py` arm (a), this commit) are entirely the
SUPERSEDED text and logic the CTO's own ruling `@61627f39f9` (`IRPT_BCKEND.TO-IB-rtf-2`) already
replaced on every other route. Re-derived independently this run: `holdings/enforce.py`'s
committed bytes were byte-identical to `_authz/enforce.py` as it stood at commit
`28ccac62c9eed361c669dada2aa36eee5d2a65c8` (`git hash-object` on `git show
28ccac62c9:infra/aws/lambda/investor-reporting/_authz/enforce.py` == `8f849457be`), which
PRE-DATES `@61627f39f9`.

**Was any of it ever load-bearing?** No live evidence of it. `holdings/snapshot.py` and
`holdings/entry.py` (the callers) name no holdings-specific requirement for the stricter
refuse-on-any-unprojected-gap rule; the ruling S82 (`@b37fdfd5cd`) itself names this exact
behaviour as the DEFECT ("A REAL GAP RENDERS AS NO GAP"), not a feature holdings needs. The
round-2/`IB-rtd-8` history: row `IRPT_BCKEND-W1-S16` (`_authz/tests/test_w1_s16_advisor_firm_bound
.py`'s own docstring, and `holdings/tests/test_w1_s16_advisor_firm_bound.py` pre-fold) shows the
copy was RE-STAGED once already, at `IB-rtd-8`, to carry the six-swap advisor-axis fix forward --
proving the estate's own practice for this file was "re-stage from the canonical module", never
"diverge on purpose". The gap this order closes is that the re-stage stopped being mechanical
(a committed flat copy someone has to remember to re-run) between `IB-rtd-8` and `@61627f39f9`.

## 2. Should `_authz/` become a shared LAYER rather than a per-function bundle?

`IB-rte-4`'s carried question (row `IRPT_BCKEND-W1-S20`'s class), now with a SECOND incident on
the identical mechanism: a per-function bundle of `_authz/enforce.py` -- whether committed
(`stage.py`, this cell's own defect) or staged at build time (`staged_from`, the other six
routes' existing mechanism and now holdings' own) -- still requires EVERY function's manifest
entry to be re-verified whenever the shared module changes, because each is a SEPARATE pinned
copy. `staged_from` closes the "someone forgot to re-run a script" failure mode (the pin is
re-derived at build time from HEAD, not hand-maintained), but it does NOT close the underlying
one-bundle-per-function multiplication: THIS cell's own census needed to check `7 of 7` separate
manifest declarations to confirm one shared fact. A LAYER (`irpt-common`, which already carries
`ids`/`keys`/`jsonschema`/`firm_registry.json` for these same functions) would make it `1 of 1`:
one layer version, attached by every function's Terraform, with no per-function pin to drift. The
committed BUILD_MANIFEST.json's own layer-dependency census pattern
(`infra/aws/lambda/investor-reporting/holdings/BUILD_MANIFEST.json`'s `layer_dependencies`) already
exists for exactly this purpose on `ids`/`keys`. Whether `_authz` should join that layer is a
capacity/versioning decision outside this order's BOUNDS (no layer change is authorized here);
this record restates the question for the CVO/CTO with a second data point: TWO staleness
incidents now on the SAME per-function-bundle shape (`IB-rte-4`'s `served.py`/`loaders.py` gap,
and this order's `enforce.py` gap), both on the identical file family.

## 3. Does `IRPT_FNTEND`'s v0.8 clause need the CTO's named carve-out, or does the fold land first?

Out of this order's BOUNDS and this worker's `<paths>` grant (no `IRPT_FNTEND` path is readable
from this worktree). Restated for routing, per this order's own text naming the question: the fold
in THIS order (`IB-rtf-8`) is now landed for its arm (a)-(b)-(c) portion (arm (d) stops this pass,
per design), so if `IRPT_FNTEND`'s v0.8 clause was conditioned on "the fold lands first", that
condition is now partially true -- the CODE fold is committed; the DEPLOY (arm (e)) is not, and
will not be until both never-widen halves are SIGNED. Whether that partial state satisfies the
v0.8 clause's intent is the CTO's call, not this worker's.
