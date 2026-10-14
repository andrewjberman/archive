# NEVER-WIDEN ASK -- OG-ap-18: the ten G1 typed harvest tools

To: `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O` and `3.0.0_SA_CVO~Z` -- THREE halves, each signed on its own.
From: `0.7.0_AE_CloudOps~Z`. Phase A of `NFRA_OPLGTW.TO-OG-ap-18` at amendments A1-A2.
**NOTHING IS DEPLOYED.** Release cut, 44 tests passing, `ap18.AC1` PASS.

| | |
|---|---|
| **release** | `4275edccad2d48fe0183a783a120527bab6fb16b` on `rel-nfra-oplgtw-gt` |
| **base** | `bacec95ccd6cafd2201f7433af24ae2748732355` -- the live `deployed_commit`, md5-verified 107 of 107 |
| **ledger** | `nfra-oplgtw-gateway-release-gt` (Phase B) |

## 1. The `diff`, by file -- 15 files, 3537 added, 5 removed

| file | +/- | taken |
|---|---|---|
| `app/harvest_figures.py` | +561 | whole, pinned trunk `6ff58597d6` |
| `app/harvest_research.py` | +540 | whole |
| `app/harvest_identity.py` | +526 | whole |
| `app/harvest_press.py` | +405 | whole |
| `app/harvest_typed.py` | +222 | whole -- the shared admission, cap and envelope |
| `tests/test_og_gt0.py` ... `test_og_gt4.py` | +1405 over 5 | whole |
| `app/tools.py` | +63 | by hunk, from the hookup `0cda8e2505` |
| `app/destructive_ops.py` | +10 | by hunk -- the ten into `SAFE_TOOLS` |
| `app/data_entitlement.py` | +10 | by hunk -- the ten into `NATIVE_TOOLS` |
| `tests/test_entitlement_admin.py` | +2 -2 | by hunk -- `registered_tool_names` 65 -> 75 |
| `tests/test_data_entitlement_family.py` | +3 -3 | by hunk -- `non_data` 56 -> 66 |

`app/typed_scope.py`, `app/harvest_published.py`, `tests/test_og_gt5.py` and `tests/test_og_gt6.py`
are **absent from the cut and from the tree**. That exclusion needed checking rather than trusting:
the ten files come from trunk HEAD, which is NEWER than `typed_scope.py` (OG-gt-6 drained it after
these cells), so a HEAD copy could have grown an import of a file this release omits -- green deploy,
dead on import. Measured: no shipped file references either excluded module, and all five modules
import cleanly in the release tree.

## 2. The ten `tools`, their class, and what they answer `refused`

All ten are READ tools, `SAFE` in `destructive_ops`, `legacy` class in `data_entitlement`
(`NATIVE_TOOLS`, deliberately NOT `DATA_GRANT_TOOLS`): `harvest_resolve_security`,
`harvest_security_coverage`, `harvest_get_chatter`, `harvest_search_articles`, `harvest_get_article`,
`harvest_get_fundamentals`, `harvest_query_columns`, `harvest_get_research`,
`harvest_get_filing_analysis`, `harvest_get_peers_and_scores`.

Every one calls `harvest_typed.admit_typed(tool, ref, ...)` **before any S3 call**, which is OG-hv-1's
admission: a principal, then `tools._is_opal_user`, then the served-prefix test. So each inherits
exactly these refusals -- `principal_required`, `harvest_opal_only`, `harvest_prefix_not_served` --
and adds its own: `harvest_bad_argument`, `harvest_over_cap`, `harvest_read_failed`,
`harvest_unreadable`. A non-Opal caller is refused all ten.

## 3. The `widening`, stated plainly

**No new bucket reach. No IAM change. No grant.** These tools read `s3://opal-data-harvest` through
the SAME policy and the SAME Opal-only admission that OG-hv-2 already put live, under the same 24
served prefixes. `gateway-global-internal-reader-role` gains nothing; `harvest_read_iam.tf` is not
touched.

What widens is **ease**: ten typed, projected readers over what `harvest_read` could already fetch
one object at a time. Named plainly, the data they make easy to read is **research notes, filing
analyses, press and social chatter, peer sets and scores, and Bloomberg bronze tables read FROM THE
BUCKET** -- there is no vendor call anywhere in these modules, so no Bloomberg entitlement is touched
and nothing goes through their queue.

A half that is comfortable with `harvest_read` and not with these ten should say so: the difference is
convenience and shape, not reach.

## 4. The `order` of acts, and that no grant is part of it

ONE act: the deploy, under ledger `nfra-oplgtw-gateway-release-gt`, entry and sentinel first. There is
no grant step, no Terraform, no IAM apply and no store write anywhere in this order -- OG-hv-2's grant
is already live and is what these tools read through. Phase B is: ledger, deploy from
`C:/tmp/og-rel-gt` under the A1 deploy-source guard, read back the triggers, then the served read of
all ten.

## 5. `Both branches` of a call

| branch | what happens | evidence |
|---|---|---|
| **refused** | the admission answers before any S3 call, so **zero S3 calls** happen | `admit_typed` runs first in every tool; OG-hv-2's own served read measured `s3_calls_on_refusal 0` for the same admission by replacing the client with a counter |
| **admitted** | the read is **capped at 64 MB on the read itself** (`TYPED_MAX_BYTES`, enforced on the body, so a lying `Content-Length` cannot defeat it; over it -> `harvest_over_cap`) and the output is **projected to 50 KB** (`PROJECT_LIMIT = 51200`), carrying `truncated` and `projected_to_bytes` | `app/harvest_typed.py:24-28, 54, 147-153` |

Every answer carries the envelope `as_of`, `source_keys`, `denominator`, `absent_reason` -- so an empty
answer says WHY it is empty instead of reading as "no such data".

## 6. Two recorded reads A2 asked for -- and one is already a finding

**(a) The trading calendar does NOT reach the installed code. Measured now, not deferred to the served
read.** On `i-07dccb1615503ac99`: `lib/` is **absent** from `/opt/opal-gateway` entirely,
`lib/trading_calendar.py` is **absent**, and the service interpreter answers
`ModuleNotFoundError: No module named 'lib'`. The deploy ships the gateway app directory, not `lib/`.

`app/harvest_identity.py:108-127` imports it lazily behind a guard and, when it cannot, **reports**
`"lib/trading_calendar.py is not importable on this runtime, so no trading-day lag is measured"`
rather than guessing. So nothing breaks and nothing lies -- but `trading_days_behind_t1` will be
absent on every call until the deploy ships `lib/`, and any freshness these tools state is therefore
NOT trading-day based. That matters against the standing rule that the trading calendar is the one
frontier for staleness. Rows `Z-W72-S2` and `Z-W79-S3` anticipated it; this ask measures it. Filed as
a row; the remedy is a deploy-cone change owned outside this order.

**(b) `harvest_search_articles` latency.** Its live probe read one silver partition of about 110 MB
for the sentiment join and took **65-97 s**. The order asks for the SERVED latency, which is a Phase B
measurement; it is not in this ask because it has not been served yet. The halves should know the
shape they are signing: one tool of the ten is a tens-of-seconds call, well beyond the others.

## 7. The `rollback`

Redeploy the base `bacec95ccd` through `safe-ec2-deploy.sh` with `DEPLOY_BASE_REF`. Complete and not a
hope: that ref's parity with the host is measured at 107 of 107 above. No IAM to undo, because none is
applied.

## 8. The `triggers` Phase B reads back

| trigger | instrument | pass |
|---|---|---|
| service up | `GET /health` on `127.0.0.1:8080` | `{"ok":true}` |
| registry **+10** | the app's own registry (`registered_tool_names`), not a `@mcp.tool` grep | **65 -> 75** |
| `.env` names unchanged | key NAMES only; the release touches no file under `deploy/` | unchanged |
| the running bytes ARE the release | SSM md5 over `app/`, `deploy/`, `dashboard/` vs `4275edccad` | all equal |

Any trigger failing: redeploy the base and file an ARMED row naming `2.0.0_SA_COO~O`.

## 9. What is NOT asked

No IAM, no grant, no store write, no vendor call, no new bucket or prefix, no route, no `.env` key, no
catalog edit. `harvest_get_published_analysis` (OG-gt-5) and `app/typed_scope.py` are NOT in this
release and ride their own ask. And no deploy until all three halves are signed at `release_sha`.
