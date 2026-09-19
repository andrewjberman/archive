# LT-n-3 round 7 result -- `0.9.0_WK_LGIC_LGCTFM~1` on `LGIC_LGCTFM.TO-LT-n-3-r7`

**Cell:** `LT-n-3`. A MEASUREMENT of `LGIC_LGCTFM-W2-S2` -- which `node_type` values a real
`lib/opal_lgctfm.py walk` actually produces, by subtraction against `org/standards/LGCTFM_CONTRACT.schema.json`'s
declared enum. This cell decides nothing and fixes nothing (the fork -- widen the enum vs refuse at
the producer -- is the CTO's, on this record).

**Artifacts:** `org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~1/NODE_TYPE_POPULATION_R7.json`
(the record) and `.../walk_r7/{contract.json,COVERAGE_EVIDENCE.json,HAND_SURFACES.json,PLANT.json,PLANT_UNTYPEABLE.json,live-iam-census.json}`
(the real run's own output, kept beside the record), all committed at `e1507822cd` on branch
`wk-lgic-lgctfm-7-1`.

## The run

`cd <WS> && python lib/opal_lgctfm.py walk --subject 49financial --seed opal-data-bd --seed opal-data-inf
--seed opal-data-cot --out org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~1/walk_r7`
(rc=0), `--plant-untypeable` NOT passed (default OFF, R-36). 573 involved nodes, 575 rows written
(incl. 2 planted -- the S3-notification plant and the missing-registry-row RAISE plant, neither of which
is `COGNITO_USER_POOL`), `not_covered=0`, `excluded=9`, `untypeable=0` -- all read off the walk's own
stdout and `contract.json`'s own MEASURED cells, not assembled from the schema.

## The two sets

**Emitted** (18, read off `walk_r7/contract.json`'s `rows[*].node_type`, not the enum):
`CLOUDFRONT_DISTRIBUTION, CW_ALARM, DYNAMODB_TABLE, EC2_INSTANCE, EVENT_RULE, IAM_POLICY, IAM_ROLE,
INSTANCE_PROFILE, LAMBDA, S3Key, S3_BUCKET, S3_BUCKET_POLICY, SCHEDULE, SECRET, SECURITY_GROUP,
SNS_TOPIC, SQS_QUEUE, SSM_DOCUMENT`.

**Declared** (33, `org/standards/LGCTFM_CONTRACT.schema.json` `$defs.node_type.enum` at
`5bb26b51e5f9b36e2a1f06584dee73b81c40cce0`, which is also this round's HEAD -- the file has not moved
since the cut): the 18 above plus `API_GW, API_ROUTE, CODEBUILD_PROJECT, ECS_CLUSTER,
ECS_TASK_DEFINITION, EVENT_SOURCE, IAM_USER, KMS_KEY, LAMBDA_LAYER, LOAD_BALANCER, LOG_GROUP,
ROUTE53_RECORD, SERVICE_PRINCIPAL, STATE_MACHINE, VPC_ENDPOINT`.

**`emitted_minus_declared`: 0 (EMPTY).** Every node_type this real walk produced is inside the declared
enum. This is a genuine ZERO, not a manufactured one: the checker's self-test carries a dedicated
positive arm for exactly this case (`POSITIVE-BAR-nodes-ZERO-violations-is-admissible`), and the
order states plainly a zero answer passes and is a result, not a failure.

**`declared_minus_emitted`: 15** (a finding, not a defect claim) -- enum values this particular
walk's real traffic never produced (a different subject/seed set could produce some of them).

## Why this reads differently from `W2-S2`'s round-2 claim

`W2-S2` says "every walk emits a `COGNITO_USER_POOL` row" outside the enum. Reading
`lib/opal_lgctfm.py:1389-1439` (round-6-era, cited in-file as R-36) shows the `COGNITO_USER_POOL`
plant that once fired UNCONDITIONALLY now fires only behind `--plant-untypeable` (OFF by default,
not passed by this walk), and even when it fires it is **never written into `contract.json`'s `rows`**
-- it is carried separately in `PLANT_UNTYPEABLE.json` with verdict `NOT_COVERED` and counted in
`contract["untypeable"]`. Independently, `cmd_walk`'s row loop (`:1298`) already excludes any node
whose `node_type` is outside the enum from `rows` (routed to `not_covered` instead). Both mechanisms
are consistent with this walk's own `untypeable=0` and `not_covered=0`. This record does not assert
the round-6 repair caused the round-2 finding to lapse -- it reports what THIS run, at HEAD, actually
produced, which is what the order asks for.

## Criterion-by-criterion

All three mechanical criteria run against
`org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/2.0.0_SA_COO~G/fixed_inputs/r7/check_lt_r7.py`
(read-only fixed input, not edited).

- **N3R7-AC1** `n3-population`: emitted 18/18, declared 33/33, `emitted_minus_declared` 0, both stated
  differences agree with the record's own re-derived lists, `schema_pin` and `how_emitted_was_obtained`
  both present. PASS.
- **N3R7-AC2** `r7-vintage-field`: 1 of 1 record present in this checkout graded (`LT-n-3` only, S106's
  per-checkout population); 2 of 2 fixed inputs named with a resolvable commit. PASS.
- **N3R7-AC3** `r7-stale-proofs`: 0 proofs at risk named vs 0 enumerated (set equality holds); the one
  fixed-input commit since the cut is the round's own L6 issuance commit that minted `fixed_inputs/r7`
  itself (informational only). PASS.
- **N3R7-AC4**: JUDGMENT, no verdict from this worker; recorded `UNVERIFIABLE-BY-INSTRUMENT`,
  `status_reason` naming `3.0.0_SA_CVO` at L9.

## Controls

**Mutant:** the committed record's `node_types.emitted_minus_declared` was overwritten to `["LAMBDA"]`
(disagreeing with the record's own emitted/declared lists) and `n3-population` re-run: flipped PASS to
FAIL, naming the disagreement (`stated ['LAMBDA'], derived []`). The file was restored from a
pre-mutation backup and `n3-population` re-run: returned to PASS with output identical to the original
run; `git status --porcelain` confirmed no diff remained on the record. FIRED-AS-EXPECTED.

**Determinism:** `n3-population` run twice against the committed, unmodified record; outputs
byte-identical both times (`diff` empty).

## Commits

- `e1507822cd` `record(LGIC_LGCTFM, 0.9.0_WK_LGIC_LGCTFM~1, LT-n-3 round 7): the node_type population
  measured -- emitted_minus_declared is ZERO` -- `NODE_TYPE_POPULATION_R7.json` and `walk_r7/*`.

No surprise row filed: the run, the record and the checker agree, and the gap between this round's
measured result and `W2-S2`'s round-2 prose is explained by a repair (`R-36`) already visible in
`lib/opal_lgctfm.py` at HEAD, not by anything this cell diverged from.
