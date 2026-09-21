# LGIC_LGCTFM.TO-LT-e-6-r4 -- RESULT (`0.9.0_WK_LGIC_LGCTFM~1`)

**Branch:** `wk-lgic-lgctfm-4-1` (linked worktree). **Commits, all LOCAL:** `21ca7eb080` (the repair, the
run, the control and four rows), plus the commit carrying this file and the proof instance.
**Order status: still `pending`** -- E6R4-AC1 reads FAIL, and a FAIL row leaves the order open.

## Verdicts

| criterion | verdict | deciding line |
|---|---|---|
| E6R4-AC1 | **FAIL** | `VERDICT: FAIL-E6-SOURCES` -- 3 refused tokens remain, all NOT-USED ledger rows |
| E6R4-AC2 | PASS-by-output | `hand surfaces treated: 1` / `VERDICT: PASS-E6-HANDSURFACE` |
| E6R4-AC3 | PASS-by-output | `floor 90 = rowed 81 + excluded 9 + unaccounted 0` / `VERDICT: PASS-E6-COVERAGE` |
| E6R4-AC4 | PASS-by-output | 19 of 19 node_types held or grew, 0 dropped / `VERDICT: PASS-E6-NO-LOSS` |
| E6R4-AC5 | RECORDED (judgment) | graded at L9 by `3.0.0_SA_CVO`; no verdict here |

The checker's own controls were run FIRST: `selftest-arms` -> `PASS-ARMS-DISCRIMINATE`, **24** arms, 8
positive-satisfiability. The order's face says 21; row `W1-S37`.

**All four mechanical arms read FAIL at the cut**, confirmed before any work: e6-sources (4 refused, 0
allowed), e6-handsurface (`no hand_surfaces entry`), e6-coverage and e6-no-loss (`no contract at ...`).

## HALF ONE -- the authorization plane

`lib/opal_lgctfm.py` `live_iam_plane()`. Three R-81-assigned instruments, in order:

1. `comp-iam refresh-census --out <run>/live-iam-census.json` -- ONE read-only
   `iam:GetAccountAuthorizationDetails`, vintage stamped at the read. This is `comp-iam reconcile`'s own
   named remedy, printed in its refusal text.
2. `comp-iam reconcile --census <that>` -- **the gate, and it is load-bearing.** The census is admitted
   only if its fail-closed vintage gate passes; `rc 3` raises `SystemExit` rather than degrading to a
   declared read. Exercised in both directions: against the estate's default census the same command
   returns `rc=3 REFUSED: APPLIED reconcile NOT PERFORMED -- the census carries NO vintage`; against this
   run's census it returns `[FRESH]` (age 0.0h, TTL 24h) and proceeds.
3. `comp-iam live --census <that>` -- `population cross-check: graph 248 vs census 256`.

**How the read differs from the old one -- PLANE, not spelling.** `comp-iam reconcile`'s own report on
this run: **`live roles (census): 256 | TF-parsed roles: 210 | matched: 206`**. 50 live roles were
outside the old read's population entirely; 4 declared roles are not live. The leg's denominator moved
210 -> 256. The sharper tell is second-order: round 3 had to carry `opal-49f-value-parity` in
`granting_roles_not_in_the_live_graph` -- a role the repo declares that AWS does not have -- and **this
run's list is empty**, because a live-plane read cannot produce a declared-but-not-live role at all.
The join moved too: a granting role binds to its graph node by **ARN identity** first, name only as a
fallback.

**50 granting roles**, 95 compute nodes reached forward, 5 execution roles added in reverse.

**Disclosed blind spot, counted not assumed.** The census expands INLINE policy documents and records an
attached-managed policy as `UNRESOLVED` with no Resources text -- **148 of 256 roles** carry at least
one. A grant reachable only that way is not matched. `HAS_POLICY` still reaches such a role when the
policy itself carries a token, and the blind spot is asserted by a **driven arm**, so the day the census
starts resolving managed policies the arm flips. `comp-iam simulate` is named as the instrument that
would settle one such case and is deliberately not used to enumerate a population -- a per-pair oracle
asked a population question narrows the question rather than widening the plane, which is AC5's own
hazard.

## HALF TWO -- the hand surface, GUARDED

`source_map_guard()` runs `comp-lambdamap check` inside every walk, over two independent planes (the map
against the Terraform tree and the on-disk source directories), and the output travels in the run's
`HAND_SURFACES.json`. `rc=1` means drift FOUND; a guard that cannot run reports `UNMEASURED`, never
clean.

`source-map functions: 216 | TF lambdas: 188` -> **3 `WRONG_SOURCE_DIR` + 9 `MISSING_ENTRY`**. One of the
nine is **`opal-49f-value-parity`** -- a **subject** function, TF-backed, with no `functions{}` entry, so
the `source_text` leg is structurally blind to it. **A count could not have produced that:** 216 entries
against 217 live, totals agreeing while 19 names disagree.

## Coverage: 381 -> 402 involved, ZERO drops

| node_type | r3 | r4 | | node_type | r3 | r4 |
|---|---|---|---|---|---|---|
| IAM_ROLE | 46 | **56** | | S3Key | 154 | 154 |
| LAMBDA | 67 | **73** | | SECRET | 5 | 5 |
| EVENT_RULE | 37 | **38** | | S3_BUCKET_POLICY | 3 | 3 |
| IAM_POLICY | 22 | **23** | | CW_ALARM / SQS_QUEUE / SSM_DOCUMENT / SNS_TOPIC / S3_BUCKET | 2 | 2 |
| EC2_INSTANCE | 19 | **20** | | CLOUDFRONT_DISTRIBUTION / DYNAMODB_TABLE / SECURITY_GROUP | 1 | 1 |
| SCHEDULE | 9 | **10** | | LOG_GROUP | 0 | 0 |
| INSTANCE_PROFILE | 6 | **7** | | | | |

**7 grew, 12 held, 0 dropped.** Every `dropped` list in the record is EMPTY rather than unexplained --
there is no drop to name. The record computes the delta over the UNION of both rounds' type sets, so a
type present in one and not the other would surface rather than vanish. **Not all of the +21 is the
re-point:** the token floor itself moved 88 of 2590 to 90 of 2595 between the rounds, and the record says
so rather than attributing the whole delta to the leg.

## Routing -- round 3's `W1-S23` does not recur

The walk gained `--contract-name`, so a deliverables run is named `*.lgctfm-contract.json`.
`.tools/receiving-check.py` reads **`ACCEPT lgctfm-contract ... 1 ACCEPT | 0 HAND BACK | 0 UNCHECKED`**
(rc=0). The route resolved; the contract is schema-valid.

## The blocking finding (E6R4-AC1)

`core_sources()` (`check_lt_r4.py:127-132`) is a bare substring test over the whole method note. The
repair removed both mentions it owned and named all three allowed instruments -- the allowed half went
**0 -> 3** and the refused half **4 -> 3**. The three that remain are rows of the **78-tool COMP-TOOL
LEDGER whose verdict column literally reads NOT USED**:

- `:329 | 3 | comp-aws | NOT USED -- the ENGINE that derives the graph ...`
- `:352 | 26 | comp-estate | NOT USED -- semantic descent over layers/definitions ...`
- `:385 | 59 | comp-routes | NOT USED -- CloudFront to origin to Lambda serving path ...`

The arm cannot tell a refused tool named as a SOURCE from one named as NOT USED. That ledger is mandated
by an Andrew-direct (~18:3xZ, msg 98038, record `@c9e54d5c0f`) as a Rule-24 subtraction over a **printed
denominator of 78 tools**, so satisfying the arm means deleting or re-spelling three of its rows --
the workaround the order forbids. **The perverse direction is the point: a design that DOCUMENTS having
rejected a refused tool scores worse than one that never mentions it.** Row `LGIC_LGCTFM-W1-S35`,
BLOCKING, ARMED, `disarm_owner: 2.0.0_SA_COO~G`. No fixed input edited, no ledger row touched.

Scope, measured: the contract's coverage block carries **0 of 8** refused tokens; 3 of 3 residual hits
sit inside the ledger table, 0 of 3 in any design section.

## The other three rows

- **`W1-S36`** (ARMED) -- `LGCTFM_CONTRACT.schema.json` `$defs.coverage` is CLOSED
  (`additionalProperties: false`, exactly five keys), so R-81's guard output **cannot** ride inside the
  contract: the first build read `HAND BACK ... Additional properties are not allowed`. The schema is
  outside this order's grant, so the guard rides in its own sidecar instead. **`LT-x-5` runs this engine
  next and will meet the same wall if it reaches for `coverage.hand_surfaces`.**
- **`W1-S37`** -- the order's `21 arms` against a measured 24 (four arms are minted per round-4 order,
  so the total drifts; the issuer's own notice reports 28 after its repair).
- **`W1-S38`** (ARMED) -- `core_stale()` tests the record's `fixed_input_commits_since_cut` for EQUALITY
  against a live re-derivation, but a worker measures it on **its own branch**. Here it reads **1**
  (the L6 issuance that minted the fixed input; zero round-4 proofs at its parent, so `proofs_re_run` is
  `[]`, the repaired rule's mint case exactly). On the merged index it reads at least 2. The record
  states its own scope in a `_worktree_scoped` field rather than guessing.

## On the issuer's mid-round repair of the checker (`1df2481ca0`)

Verified rather than trusted. That commit is reachable in this worktree's object database but is **not an
ancestor of this branch**, and a worker may not merge. `git diff` of `check_lt_r4.py` between this HEAD
and `1df2481ca0` touches **only** `core_stale`, the new `proofs_at_risk` helper, the `r4-stale-proofs`
arm and its self-test arms -- `core_sources`, `core_handsurface`, `core_no_loss` and every `e6` arm are
**byte-identical**. So grading AC1-AC4 here IS grading them on the repaired checker. `r4-stale-proofs`
is not among this order's criteria; its instruction ("measure at your own write time") was followed and
no number was copied from the message.

## The control

`e5_legs_control.py` moved with the leg and got stronger: it no longer stubs the grant MATCHER, it
injects a census in the live census's own shape and lets the real parser read it. **Nine arms,
`ALL-ARMS-HOLD`**, four new and three of those negative -- a DENY naming the subject is not a grant; an
UNRESOLVED attached-managed statement reaches nobody; and a census Allow re-pointed at another firm
reaches nobody.

## Proof

`LGIC_LGCTFM.TO-LT-e-6-r4.repoint-and-declare.proof_of_spec.json` --
`python .tools/proof-of-spec-check.py <instance> E6R4-AC1,E6R4-AC2,E6R4-AC3,E6R4-AC4,E6R4-AC5
--governing-order <order>` -> **VALID (rc=0)**, 8 of 8 artifact rows CONTENT-resolved, 4 of 4 surprises
resolving to channel rows. **A VALID instance is not a met order:** AC1 is FAIL and the order stays open.
