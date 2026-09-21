# LGIC_LGCTFM.TO-LT-m-2-r5 -- result log

Worker `0.9.0_WK_LGIC_LGCTFM~1`, worktree `wk-lgic-lgctfm-5-1`.

## What this cell answered

Re-measured the round-4 run's own contract.json myself: 154 S3Key rows, 24 without a resolvable
bucket (23 tier-prefixed: gold 10, platinum 12, silver 1; 1 firm-prefixed). Matches the issuer's
cut-time count exactly.

Hunted the issuer's stated disagreement with `1.0.0_SA_CTO`'s round-4 analysis (which calls the
24th row a malformed bare `s3:`): swept all 6 run directories under
`workflows/legacy_transform/blackdiamond-49financial` (the only workflow home in this repo) for a
bare single-colon `s3:` shape. Found 0 in all 6. No bare `s3:` row exists anywhere this seat can
read.

## Attribution method (instruments run, not inferred from shape)

For every one of the 24 bucketless rows, ran two live instruments against the same key:

1. `.tools/comp-find --corpus aws <bare-key>` -- confirms how many same-name S3Key candidate
   nodes exist in the served graph.
2. `.tools/comp-kuzu` Cypher `MATCH (x:CloudNode) WHERE x.node_type='S3Key' AND x.name='<key>'
   RETURN x.node_id, x.props` -- reads the graph's own stored properties directly.

Result: all 23 tier-prefixed rows have exactly 3 same-name candidates (`opal-data-bd/<key>`,
`opal-data-inf/<key>`, and a `s3:<key>` node with `props.source='portal-stitch'`,
`origin_reason='ambiguous-across-firms'`, `arn=''`). R-0060 (the firm-prefixed row) has exactly 1
candidate, same `source='portal-stitch'` but `origin_reason='no-canonical-s3-key'`.

Then read (not edited) `lib/opal_lgctfm.py`'s `discover_involved()`/`resolve()` (:908-964) and
`parse_aws_walk()` (:357-390) to find the two code sites that consume this: an AMBIGUOUS name
(>1 candidate) falls through comp-find's parsed text, which never prints an `arn_or_path` line for
the S3Key band and falls back to the bare `name` (:374-380); a UNIQUE name is read straight off
the kuzu-native node, where an empty `arn` falls back to the node_id itself, which for this class
of node already carries the `s3:` prefix baked in upstream (:929-930).

**Producer count: 2** (two distinct engine code sites), sharing **one upstream root** (the served
graph's portal-stitch S3Key ingestion leaves `arn` empty whenever it cannot resolve a single
firm-writer bucket). Recorded for `3.0.0_SA_CVO` at M2R5-AC6, no verdict taken here.

## No repair

Made no edit to `lib/opal_lgctfm.py`, `infra/logic/registry/`, or `LEGACY_SERVED_PATHS.json`.
`s41-no-repair` reads 0 commits by this cell against those paths.

## Checks run

- `selftest-arms` FIRST: 25 arms, `PASS-ARMS-DISCRIMINATE`. No fifth unsatisfiable-by-a-correct-
  record criterion found (four were found and fixed in round 4).
- `s41-population`, `s41-producers`, `s41-no-repair`, `r5-vintage-field`, `r5-stale-proofs`: all
  five `PASS` at the pin, `FAIL`/guard-shaped-PASS at the cut as the issuer disclosed. Each run
  twice, identical both times (determinism).
- Three additional mutants driven directly against this cell's own real record (not just the
  self-test's hand-built fixture): dropping a row from a producer's `rows` list, blanking a
  `how_it_was_attributed`, and under-enumerating `population.row_ids` -- all three FAIL as
  expected.

## Surprises

None filed. No criterion was found that a correct record could not satisfy; no row required the
`unattributed` escape (both instruments genuinely reached every row).
