# WIP -- `IRPT_BCKEND.TO-IB-rt-2` AT A MANAGED WIND-DOWN

**Written for a SUCCESSOR who has none of my context.** Author `0.9.0_WK_IRPT_BCKEND~2`.
**Stopped at:** 2026-09-11 ~17:45Z, on the managed wind-down relayed by `2.0.0_SA_COO~B` from
Andrew via `0.0.0_AB_MSTR` (95994, 17:30Z).
**Branch:** `wk-irpt_bckend-2-2`, worktree `/c/tmp/wk-irpt-2-2`, cut at `bebcab6315`.
**The order is OPEN. `<status>` is `pending`. Nothing is flipped.**

> **NOTHING OF MINE IS UNCOMMITTED.** `git status --porcelain` shows only `.scratch/`, which is
> untracked scratch and carries no intent. Every file below is committed on the branch.

---

## 1. THE ONE THING TO READ FIRST

**NO DEPLOY OF ANY KIND HAPPENED IN THIS CELL, ACROSS BOTH OF MY RUNS.** No change-management
ledger entry was opened, no zip built, no artifact uploaded, no Terraform root applied, no Lambda
layer published. **Do not look for a half-landed act; there is none, and that is deliberate.**

Everything below is source, declaration and evidence. The Terraform files now DECLARE
`entry.lambda_handler` for six functions and **the world still runs the old handlers.**

---

## 2. WHAT IS DONE, AND WHERE

| commit | what |
|---|---|
| `4356085122` | the five guarded entry modules, `_authz/served.py`, `routetable.py`, `loaders.py`, both test suites, five Terraform re-points, rows W2-S19..S27, the HUMAN-GATED principal record, the battery |
| `3009ce540b` | `battery_ib_rt_2.result.md` (the first run: 7 of 10 arms) |
| `2c1bccf346` | the proof-of-spec instance -- **VALID, `rc=0`**, RT2-AC1 `FAIL` |
| `db9f87f235` | **`ops/entry.py`** + the ops Terraform re-point + the census collapsed to one number |
| `91069c5dff` | `lambda-source-map.json`: the two source maps now declare the truth |
| *this commit* | rows `W2-S28`, `W2-S29`, and this file |

**THE HEADLINE CHANGED AFTER THE AMENDMENT.** The battery's committed `.result.md` and the
committed instance both say `0 of 8 in lane / 3 of 11 whole file`. **That is now stale:** with
`ops/` granted and `ops/entry.py` committed, the census reads

```
IN-LANE   : OK: every route is guarded
WHOLE FILE: OK: every route is guarded      <- 0 of 11, six functions named
CONTROL   : 1 of 11 on three different victims
```

**Arm (a) is now fully met.** Re-running the battery is the first thing to do (§4), and the
instance and `.result.md` must be rewritten from that run -- **do not hand-edit their numbers.**

---

## 3. WHICH ARMS REMAIN

| arm | state | what remains |
|---|---|---|
| (a) zero of N + control | **MET** (not yet re-recorded) | re-run the battery; rewrite the instance and `.result.md` from its output |
| (b) 36 swaps | **30 of 36**; `irpt-status`'s 6 now reachable | add `"irpt-status"` to `IN_LANE_FUNCTIONS` in `_authz/tests/test_guarded_entries.py` (one line) and re-run -- the census test's copy of that set is **already updated**; the two lists are separate and only one was changed |
| (c) firm from the principal | **MET, 5 of 5** | becomes 6 of 6 with the line above |
| (d) the projection | **MET, 5 of 5** | same |
| (e) deployed and verified | **NOT STARTED** | the whole deploy. See §5 -- there is a prerequisite that must be decided first |
| (f) the principal | **MET as HUMAN-GATED** | nothing. `RT2_test_principal_human_gated.md` is the deliverable and the arm's own rule admits it |
| (g) envelope conformance SERVED | **NOT STARTED** | needs (e). In process: 1 of 5 conform, 5 of 5 version refusals |

---

## 4. THE NEXT ACT, IN ORDER

1. **One line, then re-run.** Add `"irpt-status"` to `IN_LANE_FUNCTIONS` in
   `infra/aws/lambda/investor-reporting/_authz/tests/test_guarded_entries.py`. Then
   `timeout 600 python -m pytest infra/aws/lambda/investor-reporting/_authz/tests/ -q`
   (104 passing before the line; expect 36 swaps after) and
   `timeout 900 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~2/battery_ib_rt_2.py`.
2. **Rewrite `battery_ib_rt_2.result.md` and the instance FROM THAT OUTPUT.** Both currently
   record the pre-amendment numbers and say so in their own text; replacing them is not a
   correction of an error, it is a new vintage.
3. **Then, and only then, the deploy** -- §5.

---

## 5. THE DEPLOY HAS A PREREQUISITE NOBODY HAS DECIDED YET

**READ THIS BEFORE BUILDING ANYTHING.** Every guarded entry module imports the shared modules
`served`, `loaders`, `enforce`, `errors`, `resolve`, `keys`. Those are **not in any function's
source directory**, and a deployed zip is flat.

* `performance` and `narrative` take the `irpt-common` **layer** (`layers = [...]`).
* **`directory` and `ops` declare `layers = []`** -- measured at `bebcab6315`. They take no layer
  at all, so their zips have no carrier for the shared modules and would `ImportError` on the
  first invocation.
* `export` and `ycharts/generate` -- check each before assuming.

**So the choice is: attach the layer to the functions that lack it, or vendor the modules per
function** (`BUILD_MANIFEST.json` + `infra/aws/lambda/ci/vendor-manifest.sh`; **0 of 7** IRPT
lambda dirs carry one today). The amendment grants `infra/aws/lambda/layers/irpt-common/` and
`lambda-layer-map.json`, so either is now in lane. **It is a decision, not a mechanical step, and
I did not make it.**

**AND THE LAYER IS CONTENDED:** the hand-off says `IB-rt-7` in slot ~1 is rebuilding it from an
OLDER cut, and *"whichever publishes second publishes the superset"*. Read the live version
(`aws lambda list-layer-versions --layer-name irpt-common`) **immediately before** publishing --
it was v5, created 2026-09-11T13:08:52Z, when I read it.

**The deploy sequence the face requires:** ledger entry opened and its OPEN sentinel COMMITTED
**before** the act; `.tools/safe-apply.sh` only; `.tools/terraform.exe` **by path**; `init` each
root (the provider cache was purged estate-wide); plan and print the summary line for every root
**before** applying; `CodeSha256` against the built zip; ledger CLOSED and committed **before**
the reads that grade the act.

---

## 6. WHAT MUST **NOT** BE RE-DONE

1. **DO NOT RE-MEASURE THE "6 OF 11 UNGUARDED" THE FACE INHERITS.** It was wrong. The real census
   at the cut was **11 of 11 unguarded** (row `W2-S20`) -- every one of the six dispatched
   functions' declared entry point was unwrapped. `_authz/routetable.py` derives the population
   from `routes.json` + `lambda-source-map.json` + each function's own Terraform `handler =`, so
   the census cannot be fed by the thing it measures.
2. **DO NOT EDIT `status.py`, `handler.py` (any of the four), or `job.py` TO ADD A GUARD.** The
   guard is a **new entry module** per function and the Terraform `handler =` string points at
   it. The wrapped modules are deliberately untouched: their projection rules, envelope
   validation and consent gates are the real work and they are correct.
3. **DO NOT WIRE `ops`'s STATUS LOADER TO MAKE AN ARM PASS.** `status._default_status_loader`
   raises on purpose -- *"an operations surface that defaults to 'all clear' on a wiring gap is
   worse than one that refuses"*. `ops/entry.py` CARRIES that refusal and classifies it
   `UNSUPPORTED_OPERATION`. Wiring a real loader is someone's cell; fabricating a READY envelope
   is the defect that docstring names.
4. **DO NOT ADD `expiry.py` / `refresh.py` TO `irpt-directory-search`'s `files[]`** to make the
   builder's parity check pass. They are `irpt-directory-refresh`'s, in the same shared directory;
   listing them puts the refresh runner's code in the search zip. Row `W2-S29` names the two real
   remedies.
5. **DO NOT START THE `_authz/dispatch.py` RENAME UNTIL `_contracts/` IS GRANTED.** Its only
   importer is `_contracts/tests/test_seam_paired.py:41`, and `_contracts/` is not in `<paths>`.
   A rename without it leaves a committed test importing a module that is gone; a shim left at the
   old basename keeps the collision the rename exists to remove. Row `W2-S28` -- one line of
   `<paths>` unblocks a ten-minute act.
6. **DO NOT RE-DERIVE THE PROTECTED-STRING SET AS A FLAT LIST.** In
   `test_guarded_entries.py` it is **relative to who is asking**: `A5` and `ADVISOR_B` are advisor
   B's own account and id, protected from A and not from B, and the caller's own firm id is
   *required* by the v1 envelope. My first version listed the caller's own firm and failed on
   every correct answer.
7. **DO NOT ASSERT "REFUSED" FOR THE ADVISOR SWAP.** `ADVISOR_B` is a real advisor of the same
   firm; a list operation answering it is correct. The bar is that it never **widens** -- 0 of 7
   of the authorized advisor's ids in the swapped advisor's answer.
8. **DO NOT REACH FOR `errors.error_envelope("CONTRACT_VERSION")`** without checking: the
   amendment admits `CONTRACT_VERSION` to `PUBLIC_REASONS`, and `served.BOUNDARY_REASONS` is
   DERIVED as `errors.PUBLIC_REASONS` plus exactly two. If the enum now carries it, the second
   addition is redundant and should be removed **by reading the enum**, not by assuming.

---

## 7. TRAPS THIS CELL ALREADY PAID FOR

* **`entry.py` x6 is correct; `dispatch.py` x2 is not.** Basename census across `_authz/` and
  every function dir at HEAD: `entry.py` 6 (one per function dir, never two in one zip),
  `handler.py` 4, `transport.py` 2, `dispatch.py` 2 (`_authz` + `export`). **Only `dispatch.py`
  is a true collision**, because `_authz` modules ride into every zip. That is why the shared
  boundary is named `served.py` and not `entry.py`.
* **Bare-name imports collide in process.** Three `handler.py` plus `job.py` and `status.py` share
  one interpreter when the census imports them all; the first to bind `handler` wins and the next
  function silently gets the wrong module. `routetable._import_entry` purges another function's
  bare names before each import. Without it, `performance` got the **directory** handler and
  raised an `AttributeError` the boundary classified as `UNEXPECTED` -- a wrong answer with a
  plausible code.
* **The published operation ids are not admissible key components.** They are hyphenated;
  `_keys.OPERATION_RE` is `^[a-z][a-z0-9_]{0,63}$`. Every guarded request was refused
  `KEY_REFUSED` until `served.key_operation` converted them -- and `KEY_REFUSED` is a *legitimate*
  code, so "was it refused?" passed. **Print the CODE per negative, never just the verdict.**
* **A refusal can never validate against a response contract** (row `W2-S25`, and the amendment
  has now RULED it): grade successes against the response contract and refusals against
  `StatusEnvelope`.
* **`StatusEnvelope` requires `business_date` and requires `description` on every action.** The
  business date comes from the **artifact**, never from a clock.

---

## 8. FILES THIS CELL OWNS

**New:** `_authz/served.py`, `_authz/routetable.py`, `_authz/loaders.py`,
`_authz/tests/test_unguarded_census.py`, `_authz/tests/test_guarded_entries.py`, and
`entry.py` in each of `directory/`, `performance/`, `narrative/`, `export/`, `ops/`,
`ycharts/generate/`.
**Changed:** the six `lambda.tf` / `generate.tf` `handler =` strings; `lambda-source-map.json`
(two functions); `PATH_MANIFEST.json` (10 entries appended).
**Deliverables:** `battery_ib_rt_2.py`, `battery_ib_rt_2.result.md`,
`RT2_test_principal_human_gated.md`, the proof-of-spec instance, this file.
**Not touched, deliberately:** every wrapped handler module, `_authz/errors.py`,
`_contracts/**`, `build-and-upload.sh`, the layer.
