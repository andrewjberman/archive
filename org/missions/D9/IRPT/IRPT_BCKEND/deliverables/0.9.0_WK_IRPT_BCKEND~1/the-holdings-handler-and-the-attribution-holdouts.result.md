# IB-rt-7 RESULT -- THE HOLDINGS HANDLER AND THE ATTRIBUTION HOLDOUTS

**TO:** `IRPT_BCKEND.TO-IB-rt-7` | **worker:** `0.9.0_WK_IRPT_BCKEND~1` | **branch:** `wk-irpt_bckend-2-1`
**Executes:** the CTO's round-1 ruling 3(b) (the holdings handler at HEAD on its declared authenticated route) and ruling 7 / row C-S75 (actual, assigned and target with missing attribution visible, signed custody totals never redistributed, distinct source clocks).
**Closes (proposes to close, the CVO grades):** `C-S73` (holdings half), `C-S75`, `W2-S11` (holdings half).
**Filed this cell:** `W1-S14` (BLOCKING/INERT -- the amendment's first act names paths the grant does not), `W1-S15` (OBSERVATION/INERT -- the api plan's third line), `W1-S16` (OBSERVATION/ARMED -- `_authz.covers()`'s advisor branch).

---

## 1. WHAT WAS BUILT

The holdings route has carried `status: NO-HANDLER-AT-HEAD` in the published contract since IB-s-15 -- the product needed it and no Lambda existed to target, so it was deliberately not declared in Terraform because *a route pointing at an integration pointing at nothing answers 5xx from INSIDE the auth boundary*. This cell retires that status.

| artifact | what it is |
|---|---|
| `infra/aws/lambda/investor-reporting/holdings/snapshot.py` | the handler. `guard()` + `FirmBinding`; projects by **walking the parent chain**, never by an id prefix; **re-derives** the slice's totals; refuses a snapshot that collapses its clocks; answers `UNAVAILABLE` **naming the as-of** for a missing snapshot. |
| `holdings/stage.py`, `STAGE_MANIFEST.json`, `BUILD_MANIFEST.json` | the flat members staged from `git show <pin>:<path>`, with the index gate's digests **written by the thing that did the staging**. |
| `infra/aws/terraform/investor-reporting/holdings/` | the root: one READ-ONLY role, `s3:GetObject` on the three client-firm buckets under `investor-reporting/*` and a prefix-conditioned `ListBucket`, and nothing that mutates. |
| `docs/contracts/.../v1/` | the route flipped to `DECLARED`, its response contract published, and four **OPTIONAL** fields added to `HoldingsSnapshot` (v1 is immutable; its own rule admits an optional field and forbids a required-ness change -- `required` is byte-identical). |
| `holdings_snapshot.py` | the holdouts and the two clocks in the RUNNER's behaviour, with the difference control running on **every** build. |

**THE HANDLER SERVES; IT NEVER BUILDS.** Test 19 asserts the absence of `put_object`, `build_snapshot` and `read_parquet` against the module's own source rather than promising it in a docstring.

**TWO NAMES FOR ONE OPERATION, measured.** The wire id is `holdings-snapshot` (what the contract declares and a consumer branches on); the cache-key id is `holdings_snapshot`, because `_keys.cache_key` refuses a hyphen as `NOT_A_DECLARED_SHAPE`. Feeding the wire id to the key grammar would refuse **every** request with `KEY_REFUSED` -- which reads exactly like an authorization failure and is not one. Test 21 asserts both halves so a later edit cannot quietly collapse them.

---

## 2. ACCEPTANCE

### `RT7-AC1` -- PASS-by-output

```
timeout 900 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/battery_ib_rt_7.py
-> rc 0, final line: IBRT7-HOLDINGS-SERVED
```

Full output: `IB-rt-7_RT7-AC1_battery_output.txt`. Byte-identical across two same-input runs.

- **(a) SERVED.** The LIVE api `7k3ed8px20` carries **1 of 1** holdings route, `CUSTOM` under authorizer `naqxlm`, its integration uri naming `irpt-holdings`. The published table reads **12 of 12 DECLARED** (was 11 + 1). `unguarded_routes()` over this cell's table: **0 of 1**. An authorized in-process request is SERVED and the slice **validates** against the published contract.
  **THE SIX SWAPS RUN ON TWO PLANES AND BOTH ARE PRINTED.** FIRM_ADVISOR: **6 of 6** refused, refusals carrying 0 protected bytes **6 of 6**, with the authorized request still SERVED -- so the 6 of 6 discriminates rather than being a plane where everything refuses. FIRM_OPERATIONS: **5 of 6**; the exception is the `advisor` kind, because `_authz.covers()` returns an unconditional `True` for an admin principal (`enforce.py:319-320`) while its own docstring says *"within the verified firm"*. Filed as `W1-S16`; `_authz/` is IB-s-3's surface and not in this order's `<paths>`. **No cross-firm bytes are reachable through it** -- what is served is the viewer's own permitted slice either way, measured.
- **(b) BASES NEVER SPLICED, HOLDOUTS VISIBLE.** Every node exactly one basis and `assert_bases_not_spliced` clean for all three firms, run over the LANDED artifacts.

  | firm | nodes | unassigned | value | visible as account nodes | before == after | difference control |
  |---|---|---|---|---|---|---|
  | 49financial | 128,655 | **0 of 5,877** | $0.00 | 0 of 0 | 1,505,496,010.88 | **VACUOUS** (nothing to redistribute) |
  | cottonwood | 971 | **10 of 971** | $0.00 | 10 of 10 | 479,119,691.95 | FIRES |
  | inflection | 2,584 | **84 of 874** | **$7,193,856.71** | 84 of 84 | 195,507,302.27 | FIRES |

  **THE DIFFERENCE CONTROL IS THE POINT.** The redistributing build of the SAME landed snapshot drops the holdouts and spreads their value across the sleeves that DO carry a model -- it **fails** the holdout check and **still reconciles to $0.00 drift**. $7,193,856.71 moves for INF and the total does not change. A reconcile-only acceptance would have passed the economically wrong answer. 49F's control is printed as VACUOUS, never as a pass.
- **(c) TWO CLOCKS.** Both present on the snapshot and on **N of N** nodes: 128,655/128,655, 971/971, 2,584/2,584. **COT's genuinely differ** -- custody `2026-09-10`, overlay `2026-09-11`; 49F and INF read the same date from one partition each, which is reported as equal rather than hidden. A collapsed fixture built from the SAME landed artifact is refused by the producer AND at the serving boundary; a node **silently re-dated** -- where the header still shows two clocks and only a per-node census can catch it -- is refused too.
- **(d) NORMALIZED.** `:acct:` census **0 of 127,071** (49F), **0 of 971** (COT), **0 of 2,584** (INF). Against the refreshed directory: INF **874 of 874** (was 790 of 790 -- the 84 holdouts come from `accounts_v2`, the directory's own source, so carrying them closed the gap completely), COT **837 of 837** directory-side, 49F **5,860 of 5,877**.
- **(e) DEPLOYED.** Live `CodeSha256 = yOiMCrewFEMtE6GCJzBjNdLQsRpliY8zrM3t1AMyynI=` equals the **build input** recorded in `lambda-source-map.json` (content, never filename); handler `snapshot.lambda_handler`, python3.12, timeout 29, layer `irpt-common:5`, role `irpt-holdings-role`. Both roots plan `No changes.` The ledger `20260911T1637Z_irpt-bckend-rt7_deploy_completion.md` is CLOSED with 0 legs open; its sentinel was committed at `2f0cb688de` **before** the act and removed by the close at `5a359024a9`.

**BOTH BUILD GATES WERE MADE TO ENFORCE RATHER THAN ADVISE.** The first build printed *"no BUILD_MANIFEST.json, so layer_dependencies are undeclared and a layer import is indistinguishable from a missing module ... UNENFORCED IS NOT A PASS."* Adding the manifest turned that into `OK: import-closure -- 6 packaged .py file(s), every top-level import satisfied` and, with `declared_blobs`, `OK: 4 of 4 members index-equal, manifest-equal, and LF (0 CR bytes)`.

### `RT7-AC2` -- JUDGMENT, RECORDED, NOT SELF-GRADED

Output for `3.0.0_SA_CVO` at L9. No verdict is offered.

**(i) Which attribution can still reconcile to the cent and be economically wrong after these holdouts, and the fixture that would catch it.**
Three classes survive, and the holdouts close none of them.
*First, MISATTRIBUTION INSIDE A SLEEVE.* COT's TARGET nodes are `custody_value x recursive_model_weight`. If a blend weight is wrong -- a child at 0.30 that should be 0.40 -- every node still sums to the account's custody value and the reconcile is exact. The fixture that would catch it does not exist and is buildable: take a real COT account, perturb ONE `fact_model_blend.relative_allocation`, and assert that the per-leaf values MOVE. Nothing in this cell asserts a leaf's value against an independently-derived expectation; `expand_model` is tested for cycles, missing nodes and retained mass, not for arithmetic against a second source.
*Second, THE OBSERVED/TARGET CONFUSION AT THE READER.* 49F's model node is `ASSIGNED` at the full account value and COT's are `TARGET`; both sit under an `OBSERVED` account and both sum to it. A consumer that renders children without reading `basis` shows a model target as if it were a holding -- the endpoint's own constraint ("model targets never masquerade as observed holdings") -- and every total reconciles. The fixture: render the slice through the FNTEND component and assert the `basis` reaches the label. That is IRPT_FNTEND's to build, not this cell's.
*Third, A WHOLE-FIRM SHIFT.* If the custody feed itself is a day stale, every number is internally consistent and uniformly wrong. This is precisely why the two clocks are carried -- but carrying a clock is not checking it, and nothing here refuses a snapshot whose custody clock is N days behind the business date. The fixture is a one-line assertion nobody has been asked for yet: `business_date - custody_as_of <= the firm's declared tolerance`, and the tolerance does not exist as a declared value anywhere in this project.

**(ii) Which firm's overlay clock is furthest from its custody clock, and what the snapshot says about it.**
**COTTONWOOD, by one day**: `custody_as_of 2026-09-10` (`fact_holdings`), `overlay_as_of 2026-09-11` (`fact_model_assignment`). 49F and INF read `2026-09-11` for both, and for 49F that is structural -- its custody and overlay arrive in ONE table (`fact_allocation_account_map`), so the two clocks *cannot* differ there and equality is not evidence of freshness. What the snapshot SAYS about COT's gap is: the two dates, on the header and on all 971 nodes, and nothing else. **It does not say the gap is acceptable, and it does not say what it means.** Concretely, COT's TARGET attribution is computed from a model assignment dated one day AFTER the holdings it attributes -- an account rebalanced on the 11th has its 10th-of-the-month custody value attributed to its NEW model. Every total reconciles. The reader can now see the condition, which before this cell was invisible; deciding whether it is tolerable is a question for whoever owns the COT feed cadence, and this cell deliberately does not answer it because a tolerance invented by a worker would become a fact by repetition.

**(iii) What the served slice cannot tell a reader about accounts the scope excludes.**
It reports `coverage.remainder` -- the excluded node count and their summed custody value -- and that is deliberately the *only* thing it says. It **cannot** tell a reader: how many distinct accounts those nodes belonged to (the count is of NODES, and an account contributes between one and hundreds); whether an excluded account is excluded because the viewer is not entitled to it or because the ownership map has not caught up (both read as "not in the permitted set", which is exactly the `UNPROJECTED-ID` vs `NOT-IN-DIRECTORY` distinction `_scope.unmatched_reasons` makes at the SCOPE layer and the slice does not carry forward); or whether the firm holds accounts this snapshot never built at all -- the 134 COT accounts and 17 49F accounts that are in one producer and not the other are invisible to a reader of any slice, because they are absent from the snapshot the slice is cut from. A reader who wants "am I seeing everything" gets a number that answers "of what this snapshot held, how much did your scope exclude" -- a narrower question than the one they asked, and the difference is not stated in the payload.

---

## 3. PREFLIGHT (recorded per the face)

- **comp-iam Phase 1** -- `comp-iam service irpt-holdings`: `irpt-holdings-role`, 3 statements -- its own log group; `s3:GetObject` on `arn:aws:s3:::${b}/investor-reporting/*` for the three firm buckets; a prefix-CONDITIONED `s3:ListBucket`. Nothing that mutates, nothing outside the three buckets. The tool also surfaced a second role of a similar name, `irpt-holdings-snapshot-scheduler-role` (0 statements, `directory/schedule.tf`) -- IB-s-12's DISABLED schedule slot, not this cell's and not touched.
- **comp-iam Phase 2** -- `comp-iam gaps`: `Total: 12 missing | 291 deny-present | 1 coverage-unknown | 2 resource-mismatch across 31 service(s)`. **0 rows name `irpt-holdings`**. BLIND SPOT carried from the face: DESIRED plane only, and a GRANTED-BROAD wildcard cannot be falsified by a resource check.
- **comp-schedule** -- DECLARED-NOT-APPLICABLE and still true: this cell creates, changes and fires no schedule, rule or trigger.
- **comp-adversary** -- the assignee's instrument at report time; its findings are the three surprise rows above.

## 4. BOUNDS HELD

NO live vendor call (every read is S3, Lambda, API Gateway or Terraform on Opal infrastructure). No monitor, alarm, SNS or SES. Cross-firm, both shapes: per-firm buckets in the IAM grant plus a prefix condition, and the handler resolves its bucket from the FirmBinding's registry firm, never from the request. No credential in any artifact; a refusal carries a CODE and never the refused value (measured: 6 of 6 refusals echo nothing). No served output touched -- the rebuilt snapshots are under `investor-reporting/qa/`, and the deployed function's `IRPT_HOLDINGS_PREFIX` is the PRODUCTION prefix. Deploys through `.tools/safe-apply.sh` with the sentinel committed before the act and the ledger closed before the grading reads.
