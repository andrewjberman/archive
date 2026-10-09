# ETFS_RIVALS.TO-APPLY-R28-aw1 -- STOP 3 PLAN READ from dell1

**Seat:** `0.7.0_AE_CloudOps~DELL1` (applier per AMENDMENT 2 and Andrew-direct ~03:5xZ, ruling `1.0.0_SA_CTO~DELL1` msg 1594).
**Date:** 2026-10-09 ~04:15Z. **Order:** `ETFS_RIVALS.TO-APPLY-R28-aw1` @dcd02aa134 (worktree copy CR-stripped sha equals
the pinned blob). **Issuer:** `2.0.0_SA_COO~V1`.
**APPLIED NOTHING.** Steps 1-3 only. Steps 4-6 wait on AMENDMENT 1's conditions (a)-(d) inside 11:15Z-12:50Z.

Both signed halves read IN FULL before any act, at their pins: COO half
`.../2.0.0_SA_COO~RV/round28/NEVER_WIDEN_HALF_COO_R28_AW1_DEPLOY.md` @d3d6c3e73f (SIGNED, five conditions, branches A-C,
per-key rollback) and CTO half `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_ETFS_RIVALS_R28_AW1_DEPLOY_20261008.md`
@a0ee589cc2 (SIGNED on those five conditions, unchanged). AMENDMENT 2 read before AMENDMENT 1, as the order directs.

---

## STOP 1 -- the pin, taken exactly

Tree cut per AMENDMENT 2: `git worktree add --detach C:/tmp/rv-r28-dell1 39889dd4d7`. The site-Z tree `C:/tmp/rv-r8` was
NOT used.

```
tree HEAD = 39889dd4d71a67bc108fe15ae746ed7ab6cbe6f6   (the pin exactly, not "at or after")
```

The pin was taken exactly, so condition 1's `git diff --stat` escape for a later commit does not arise. The CTO half's own
four reads were re-run here rather than inherited, and all four reproduce:

| read | result here |
|---|---|
| `git cat-file -t 39889dd4d7` | `commit` |
| aw-1 tip `a2283fc349` is an ancestor of the pin | rc 0 -- in the pin |
| RIV-tc-1 `b0b65368fb` is an ancestor of the pin | **rc 1 -- NOT in the pin**, as both halves require |
| deployed pin `325bd4e0f8` is an ancestor of the pin | rc 0 |

## STOP 2 -- package, then plan, in the same tree

`python infra/aws/lambda/etfs-pipeline/rivalfunds_package.py` -> rc 0, five trees staged under
`.runtime/rivalfunds-build/`: `etfs-rivalfunds-daily-lambda`, `etfs-rivalfunds-fetch-holdings-lambda`,
`rivalfunds-build-canonical-shape-lambda`, `rivalfunds-build-silver-lambda`, `rivalfunds-publish-page-lambda`.

The plan was made in that same tree immediately after packaging, which is the order's step-2 discipline and
comp-adversary's named hazard (a plan made before packaging reads a stale zip).

**One precondition the order does not name:** a freshly cut worktree has no `.terraform`, so the root required
`terraform init` before it could plan. Run once in the tree: `hashicorp/aws v5.100.0` and `hashicorp/archive v2.8.1`,
INIT_RC 0. Under CLAUDE.md as of law edit `4d77a9c3ea` ("Egress is open on every channel, except Bloomberg") that
provider fetch is inside this seat's autonomy; it is named here rather than left implicit. No lock file is committed.

Saved plan: `C:/tmp/rv_apply28_dell1.tfplan`, 30,352 bytes, PLAN_RC 0, 0 errors.

## STOP 3 -- the plan as read: BRANCH A

```
Plan: 0 to add, 5 to change, 0 to destroy.
```

The five resources, and nothing else:

```
aws_lambda_function.stage["etfs-rivalfunds-daily-lambda"]              will be updated in-place
aws_lambda_function.stage["etfs-rivalfunds-fetch-holdings-lambda"]     will be updated in-place
aws_lambda_function.stage["rivalfunds-build-canonical-shape-lambda"]   will be updated in-place
aws_lambda_function.stage["rivalfunds-build-silver-lambda"]            will be updated in-place
aws_lambda_function.stage["rivalfunds-publish-page-lambda"]            will be updated in-place
```

### Per attribute, from `terraform show -json` on the saved plan

Denominators match executor report 1 at site Z exactly:

```
resource_changes 45 | no-op 40 | update 5      (site Z read 45 / 40 / 5)
other action types: none
```

The DECLARED change set -- `before != after` -- for each of the five:

```
"etfs-rivalfunds-daily-lambda"             ['last_modified', 'source_code_hash']
"etfs-rivalfunds-fetch-holdings-lambda"    ['last_modified', 'source_code_hash']
"rivalfunds-build-canonical-shape-lambda"  ['last_modified', 'source_code_hash']
"rivalfunds-build-silver-lambda"           ['last_modified', 'source_code_hash']
"rivalfunds-publish-page-lambda"           ['last_modified', 'source_code_hash']
```

Package attributes only, on all five. The order's forbidden attributes were proven equal rather than assumed:

```
every one of the five: memory_size = 3008, unchanged
forbidden-attrs differing (role, memory_size, timeout, environment, layers, architectures, handler,
  runtime, vpc_config, kms_key_arn, reserved_concurrent_executions): NONE, on all five
```

`environment` is named explicitly in the order's rules, so it is read explicitly. Only the daily Lambda carries one, and
its `before == after` is **True**:

```
[{"variables": {"RIVALFUNDS_AI_ENABLE": "1", "RIVALFUNDS_OPENAI_SECRET": "rivalfunds/openai-api-key"}}]
```

So `RIVALFUNDS_AI_ENABLE` stays `1` and nothing flips with the deploy.

> ### A correction to my own first reading, recorded because it would have produced a false STOP
> My first pass treated the plan's `after_unknown` set as part of the change set and so reported FAIL on five
> resources, listing `architectures`, `environment`, `ephemeral_storage`, `layers`, `logging_config` and
> `tracing_config` as moving outside the package. That was wrong. `after_unknown` is Terraform marking values it
> cannot predict until after apply; it is not a declared change. The authoritative set is `before != after`, which is
> package-only here. The tell that it was my instrument and not the world: `last_modified` appears in BOTH lists, and
> site Z read the identical plan as branch A off the same 45/40/5 denominators.

## AC1 at the pin

`PYTHONPATH=<tree> python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round15/checks/aw-1.AC1.py`

```
AC1 RESULT: PASS 0 failures          exit=0
```

Arms (a)-(j) all OK, including (j)'s CONTROL arm (the chain on clean replies returns its 2 rows with the 17 stored
columns, both PASS). AC2 is the issuer's and the CVO's to grade and is NOT marked here.

---

## SURFACED, for the issuer to rule BEFORE the 11:15Z window

**The pin does not determine the artifact bytes across boxes, and this is a dell1 build.** 23 of the 239 tracked files
under the packager's seven `STAGED` paths are `w/crlf` in a normal checkout on this box -- every one a `.json` (or one
`.md`) with no `eol=lf` attribute, while all the `.py` files carry `text eol=lf` and are `w/lf`:

```
STAGED-PATH DENOMINATOR: 239 tracked files      w/crlf: 23      w/lf: 216
data/etfs/scripts/rivalfunds/{bbg_budget,leg_gates,peer_groups}.json
infra/logic/registry/*.json  (13 files)
lib/research/identity/{crosswalk.schema,registrations,universe.schema}.json,
  data/{sa_ids,universe,universe_landed}.json, data/SOURCES.md
```

What this does and does not mean:

- It does **NOT** break STOP 1 (the pin is exact) and does **NOT** break branch A: the package changes either way, and
  the declared change set is still `source_code_hash` + `last_modified` only. Steps 1-3 stand as read above.
- It is functionally inert at runtime: these are data files read through `json.load`, which accepts CRLF.
- But the resulting `source_code_hash` is **not** what a build of the same pin on an LF box produces. The deployed
  package `325bd4e0f8` was built at site Z. So "the same pin" has not given, and will not give, the same artifact on
  both boxes.

I did **not** re-cut the tree with `core.autocrlf=false` to force the committed bytes, because AMENDMENT 2 names the
worktree command literally and the choice changes the artifact this deploy ships. **One ask for the issuer:** take the
plan above as it stands, or have me re-cut with `-c core.autocrlf=false`, re-package and re-plan before the window. Both
are quick; the second makes the shipped bytes the committed bytes.

## State at this report

- **APPLIED NOTHING.** No `safe-apply`, no NEVER-2 entry opened yet (step 4 opens it), no function invoked, no test
  event, no S3 object written, no environment variable set.
- Saved plan kept at `C:/tmp/rv_apply28_dell1.tfplan` for step 5.
- Deploy tree `C:/tmp/rv-r28-dell1` detached at the pin and left in place for the window.
- Rollback tree NOT yet cut: per AMENDMENT 2 it is a second detached worktree at `325bd4e0f8`, packaged and planned only
  if a rollback is ordered. Site Z's note stands -- their tree was moved off `325bd4e0f8`, so the COO half's "the deploy
  tree is detached there now" no longer describes any tree; on dell1 the rollback needs its own checkout at that pin.
- Window discipline for step 4: inside 11:15Z-12:50Z, never inside 10:55Z-11:15Z or 12:55Z-13:15Z, and conditions
  (a)-(d) read by me first.
