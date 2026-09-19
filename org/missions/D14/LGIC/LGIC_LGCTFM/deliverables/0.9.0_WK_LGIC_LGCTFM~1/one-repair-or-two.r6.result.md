# LGIC_LGCTFM.TO-LT-e-7-r6 -- result log

Worker `0.9.0_WK_LGIC_LGCTFM~1`, worktree `wk-lgic-lgctfm-6-1`.

## The question

Round 5 measured 24 bucketless S3Key rows at two code sites and reported both "plausibly" trace to
one upstream root. `1.0.0_SA_CTO`'s round-5 analysis cut this round to ESTABLISH that, not restate it.
This cell was not to confirm the shared root -- it was to find out whether ONE repair actually resolves
BOTH classes.

## Hypothesis and falsifier, stated before the experiment

**H:** A single repair at the portal-stitch S3Key ingestion -- making it resolve or record a
firm-writer bucket rather than leaving `arn` empty -- removes BOTH the 23 tier-prefixed and the 1
firm-prefixed bucketless rows.

**Falsifier:** any outcome where the single repair resolves one class and leaves the other, resolves
neither, or resolves both only via a second change at the other site.

## The experiment

Copied VERBATIM (not paraphrased) the three code sites round 5 attributed, as standalone functions in
a scratch script run OUTSIDE the repo (session scratchpad, `lt_e_7_r6/experiment.py`):

- `discover_involved()`'s kuzu-native node-ingestion loop, `lib/opal_lgctfm.py:923-933`
- `resolve()`, `lib/opal_lgctfm.py:956-964`
- `parse_aws_walk()`'s blank-line fallback, `lib/opal_lgctfm.py:372-380`

`lib/opal_lgctfm.py` was read only (@`21ca7eb0802b14ff7194553a526078bc4ce36b7d`), never edited --
`e7-no-landed-repair` confirms 0 commits by this cell against it.

Fixtures mirror round 5's own measured shapes exactly (`BUCKETLESS_S3KEY_R5.json`): 23 tier-prefixed
keys each with 3 same-name S3Key candidates in the served graph (2 real firm-writer nodes from a
DIFFERENT, untouched producer, plus 1 portal-stitch node with empty `arn`); 1 firm-prefixed key with a
single portal-stitch candidate, read straight off the kuzu-native dict (no `resolve()`/comp-find
involvement for that row, per round 5's own attribution).

**Instrument:** `python experiment.py` (fixture-driven, no live AWS/comp-kuzu call -- the walk's
consuming logic is exercised directly and verbatim).

**BEFORE** (positive control on fixture fidelity): tier_prefixed=23, firm_prefixed=1,
denominator_s3key=154 -- exact match to round 5's measured population.

**THE SINGLE CANDIDATE REPAIR applied to the fixture:** portal-stitch's OWN node (the one node it
mints/owns in both classes) gets a real firm-writer bucket ARN instead of an empty string. Nothing else
changes -- same candidate count, same comp-find rendering behaviour.

**AFTER**: tier_prefixed=23 (UNCHANGED), firm_prefixed=0 (RESOLVED), denominator_s3key=154.

## Why the classes diverged (traced through the copied code, not assumed)

The firm-prefixed row has exactly ONE candidate sharing `(node_type, name)`, so it is read straight off
the kuzu-native `nodes` dict and `arn_or_path = r.get('arn') or nid` now returns the real bucket the
repair wrote.

The tier-prefixed rows have THREE candidates sharing `(node_type, name)` both before and after the
repair -- the other two nodes belong to a DIFFERENT producer's ingestion (firm-writer attribution),
which portal-stitch's fix does not touch. `resolve()`'s ambiguity gate
(`cands[0] if len(cands) == 1 else None`) still returns `None` because `len(cands)` is still 3, not 1.
And the FIRST check in `resolve()`, `by_arn.get(cf_node.get('arn_or_path'))`, can never succeed for
these rows either way: the `cf_node` comes from comp-find's own S3Key rendering, which (per the
engine's own docstring at `:360`, "blank for some types, e.g. S3Key") never prints an arn/path detail
line for this node_type AT ALL -- so `cf_node['arn_or_path']` is always the bare key name, independent
of any candidate's `arn` value, before or after the repair.

## Verdict

**TWO_REPAIRS.** The hypothesis is falsified on its own stated falsifier: the single repair resolves
one class (firm-prefixed) and leaves the other (tier-prefixed) completely unmoved.

**What I would have concluded had the other class moved instead:** had tier_prefixed instead dropped to
0 while firm_prefixed stayed at 1, that would ALSO be TWO_REPAIRS (still one class resolved, one not) --
but it would point the surviving defect at the OTHER mechanism (the kuzu-native `r.get('arn') or nid`
fallback rather than the by_tn ambiguity gate), meaning the next round's remedy would need to target
`discover_involved()`'s node-ingestion arn fallback specifically rather than the ambiguity-resolution
path -- a different single second repair than the one this round's evidence actually points to.

## No repair landed

`lib/opal_lgctfm.py` was read, never edited. `e7-no-landed-repair` reads 0 commits by this cell against
it (0 by any author since the cut_pin).

## Checks run

- `selftest-arms` FIRST: 23 arms (10 POSITIVE-SATISFIABILITY, 13 mutant/other), `PASS-ARMS-DISCRIMINATE`.
- `e7-hypothesis`, `e7-experiment`, `e7-verdict`, `e7-no-landed-repair`, `r6-vintage-field`,
  `r6-stale-proofs`: all six `PASS` at the pin (`FAIL`/guard-shaped-PASS at the cut as the issuer
  disclosed). Each run twice, identical both times (determinism).

## Surprises

None filed. No criterion was found that a correct record could not satisfy -- all three verdict values
remained reachable throughout, and this cell landed on the one the evidence actually supports rather
than the one the round-5 story invited.
