# IB-rte-1 RESULT -- THE BOUNDED TEST PRINCIPAL DECLARED AND ITS SIGN-OFF PACKET

**TO:** `IRPT_BCKEND.TO-IB-rte-1` | **worker:** `0.9.0_WK_IRPT_BCKEND~1` | **branch:**
`wk-irpt_bckend-5-1` | **base commit:** `391e4ad948869b8972bf6d96d5cc54392b351d5e` (HEAD of `CLOUD`
at hand-off, unchanged through this run). READ-ONLY on every live plane throughout. No identity
created, no ownership map written, no directory annotated, no policy changed, no apply.

## Criteria

| id | verdict | invocation | deciding line |
|---|---|---|---|
| `R51-AC1` | **PASS-by-output** | `timeout 1800 py -3.12 org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/battery_ib_rte_1.py` | rc=0, `"overall_pass": true` then `IBR51-TEST-PRINCIPAL-DECLARED-AND-PACKETED` |
| `R51-AC2` | **RECORDED (judgment)** -- no verdict | evidence assembled for `3.0.0_SA_CVO` at L9 | in the proof-of-spec instance under `UNVERIFIABLE-BY-INSTRUMENT` |

Transcript committed beside this file: `IB-rte-1_R51-AC1_battery_output.txt`.

## (a) The identity plane, measured -- 6 of 6 objects named with current hashes

- **The authorizer:** `opal-portal-authorizer` (`naqxlm`), `index.handler`, `nodejs22.x`,
  `CodeSha256 KHwksfO1XjL0Jg66kc7L+gFIOEsZT/7l2i8STRgBvS4=` (re-verified live this run, unchanged
  since `RT2_test_principal_human_gated.md`'s 2026-09-11 reading) -- REQUEST/CUSTOM, verifies a
  homegrown RS256 JWT via Secrets Manager `opal/auth/jwt-public-key`, **NOT Cognito** (the account
  has zero user pools) -- `infra/aws/terraform/partners-api/api-gateway.tf:7-10`,
  `docs/contracts/investor-reporting/v1/routes.json:_api`.
- **The trust anchor:** `IRPT_DIRECTORY_BUCKET_MAP` on `irpt-directory-search`'s live environment
  reads `{"49financial":"opal-data-bd","cottonwood":"opal-data-cot","inflection":"opal-data-inf"}`
  -- `infra/aws/lambda/investor-reporting/_authz/loaders.py:46-57 @391e4ad948`.
- **The enforcer's dependency triple** (re-read fresh this run for 49financial, never cached
  across a request per `Enforcer`'s own docstring): the directory artifact (`sha256` of its parsed
  JSON `5abc0a8a09414e6d717aeda01d901229ca4d8b562756bcfe5dd7397ed8ce372e`, `firm_id_opaque
  fir_c9fc04650e2134d6ea033da2`, 4,576 entries), the ownership map (`sha256`
  `0864a3a716a8502edf31f110c0f409edb31fdde62172961a08947e12a8568adf`, 179 advisors), the policy
  (`{"policy_id": "irpt-scoped-v1", "policy_revision": "1"}`, entitlement revision
  `irpt-ent-49financial-1`) -- `infra/aws/lambda/investor-reporting/_authz/loaders.py:71-131
  @391e4ad948`.
- **The one firm enumeration:** `data/firm_registry.json` (`git hash-object
  99b8eeb54fb08a7ea6e4b89b64f300ee6cab3200 @391e4ad948`), the object `FirmBinding`/`_keys`/`_ids`
  all validate a firm token against.

**6 of 6 objects named** (authorizer, bucket-map env, directory, ownership, policy, firm
registry).

**THE ONE OBJECT that makes a principal a FIRM_ADVISOR of ONE firm** is NOT in this project's
code at all: a row in DynamoDB table `opal-users-v2` (`firmId`, `advisorKey`/`advisorId`), read by
`generateAccessToken()` and injected by the edge validator as the nine trusted headers
`_scope/resolve.py:88-98` reads. Cited from `RT2_test_principal_human_gated.md`, re-verified live
this run (table `ACTIVE`, 79 items).

## (b) The principal, shaped -- and a defect this makes newly visible

Terminated-client count per firm, read live from each firm's own `latest.json` pointer:

| firm | as_of | entries | TERMINATED |
|---|---|---|---|
| **49financial** | 2026-09-17 | 4,576 | **71** |
| inflection | 2026-09-17 | 291 | 0 |
| cottonwood | 2026-09-17 | 260 | 0 (all 260 carry `indicator: UNKNOWN` -- filed `IRPT_BCKEND-W1-S24`) |

**49financial chosen** (the only firm with >= 1 TERMINATED entry).

**Advisor id:** `abby_horton`, an EXISTING key in 49financial's live ownership map (43 granted
accounts, 18 granted relationships) -- **not** an `_ids.py`-issued opaque id: no `"advisor"` kind
exists in that module and bound 13's own typed-id list excludes advisor too. Filed
`IRPT_BCKEND-W1-S21`.

**The terminated-client capability gap (FWD-1's own CONSTRAINT), measured firm-wide:** 0 of 179
advisors in 49financial's live ownership map hold ANY terminated-client account in their grant --
universal at this firm today, not an artifact of which advisor is chosen.

**THE LARGER FINDING, measured by running the REAL `Enforcer` wired EXACTLY as
`directory/entry.py` constructs it in production** (`deps=_loaders.deps`, `id_projection` NOT
passed): a real `abby_horton`/`49financial` request is refused **`UNPROJECTED_GRANT`** before the
served/empty-grant branch is ever reached. Re-measured firm-wide: **0 of 22,646** ownership-map
account grants (179 advisors) join the live directory even WITH `_ids.projection_for` applied by
hand. Separately: **0 of 13** live `entry.py`/`handler.py`/`dispatch.py` modules in this project
ever pass `id_projection` to `Enforcer`/`Entry`. **So the bounded test principal does not, by
itself, make FWD-1/2/5's SERVED (200) path exercisable against live data -- this fires for every
live FIRM_ADVISOR request today, independent of which advisor or firm is chosen.** Filed
`IRPT_BCKEND-W1-S22`, ARMED.

**Keys planned (nothing applied):** K1 -- one DynamoDB item in `opal-users-v2` (create; rollback
`DeleteItem` verified by a consistent-read `GetItem` returning no `Item`); K2 -- the session
token from a normal login (ephemeral, never persisted, never logged); K3/K4 (ownership-map row /
directory annotation) explicitly **NOT NEEDED** -- the plan reuses `abby_horton`'s existing grant,
minting zero new entitlement.

## (c) The exercise plan, per outcome

FWD-1 (search -> resolve, vendor calls 0, the terminated-client gap demonstrated), FWD-2 (11
DECLARED routes, 36 of 36 swaps refused per IB-rtb-1's own count), FWD-5 (holdings, custody +
model percentages, swap refused) -- each named with its route, request, artifact, the hash R-40
binds, and its negative control, all in the packet. **All three are currently `BLOCKED_BY`
`UNPROJECTED_GRANT`** (s.b above) until the id-projection wiring gap is fixed; the REFUSAL
mechanism itself, and the fixture-based mechanism batteries IB-rt-2/IB-rtb-1 already ran, remain
valid evidence of the AUTHORIZATION MECHANISM's correctness.

FWD-11: **the SSM parameter `/opal/irpt/opal-principal-roster`** `_scope/global.py` reads for the
OPAL_GLOBAL roster **does not exist** (`ParameterNotFound`, measured live this run) -- no
identity, bounded or not, can resolve OPAL_GLOBAL today. Costed: a second identity is not what's
missing; the roster parameter is, and it is a separate infrastructure act with its own sign-off.
One identity could serve both classes across two SEPARATE sessions (never one concurrent request).

## (d) The packet

`NEVER_WIDEN_SIGNOFF_PACKET_IB-rte-1.md`, `sha256
ff91d42b002642931eac7c526b55ca7269f9be921561b087aeca95820852b297` (re-derived by the battery this
run) -- keys, blast radius per key, rollback per key, the identity-plane writer census, the
lifetime bound, the negative controls.

**Identity-plane writer census** (R-44's pattern, `writer_census_ib_rtc_6.py` adapted to
`dynamodb:PutItem`/`UpdateItem` on `opal-users-v2`): **6 of 263** principals (256 roles, 7 users;
0 unsimulated, 0 UNKNOWN) -- `opal-news-lambda-role`, `opalinvest-auth-lambda-role`,
`trade-submission-lambda-role`, `Andrew_Berman`, `Andrew_Berman_Console`, `Opal_Terminal`. **Blind
spot, named:** an identity provider's own admin surface is not IAM; this census cannot see who can
reach `opalinvest-auth-lambda-role`'s own Lambda through an application-level signup/admin path.

## Rows filed

- `IRPT_BCKEND-W1-S21` (OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO~B`) -- the advisor id is
  not an `_ids.py`-issued opaque id; the task face's own assumption does not hold.
- `IRPT_BCKEND-W1-S22` (OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO~B`) -- the bounded test
  principal alone does not make FWD-1/2/5's SERVED path exercisable: 0 of 13 live entry points
  wire `id_projection`, so every live FIRM_ADVISOR request is refused `UNPROJECTED_GRANT`.
- `IRPT_BCKEND-W1-S23` (OBSERVATION, INERT) -- the task face's example directory-prefix date is
  one day stale against every firm's live `latest.json`.
- `IRPT_BCKEND-W1-S24` (OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO~B`) -- cottonwood's live
  directory carries `termination.indicator = UNKNOWN` for 260 of 260 entries.

## Bounds observed

Read-only against every live plane throughout (S3 reads of directory/ownership artifacts; IAM
`simulate_principal_policy`; Lambda `get-function-configuration`; SSM `get-parameter` -- which
returned `ParameterNotFound`, itself the measurement; DynamoDB `describe-table`). No item written,
no policy changed, no apply. No credential value read, printed or logged anywhere -- every secret
cited by NAME only (`opal/auth/jwt-public-key`, `opal/auth/jwt-private-key`); no `get-secret-value`
issued. `.tools/commit-gate.sh` rc=0 on both new `.py` files. Every invocation ran under `timeout`,
none retried more than once. No existing surprise row edited -- four rows appended inside the
first fence's array.
