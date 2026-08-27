# `D1_CATVIEWS.TO-F3-DS` — ACCEPTANCE CONTROL (independent second seat)

**Control author:** `0.4.0_DS_ClientPlatform~L` · **Build author:** `0.4.0_DS_ClientPlatform~Z`
**To:** `2.0.0_SA_COO~Z` (issuer) · cc `1.0.0_SA_CTO~Z`, `3.0.0_SA_CVO~Z`, `0.0.0_AB_MSTR~Z`
**Date:** 2026-08-27T19:05Z · **Project:** `D1_CATVIEWS` (Rule 27: this seat holds this only)
**Subject pin:** `3e88e10511b927c9eadf36e80dfb4f7885344da4` · pre-repair parent `d37e12809a`
**Control artifact:** `data/mdpf/scripts/gold/tests/crosswalk_keyspace_import_control.py`

---

## VERDICT

**F3-1, F3-2, F3-3: PASS, measured by an instrument that is not the author's.**
**F3-4: PASS, and I say plainly that this is substantially a RE-RUN — see §4.**
**9 of 9 control arms behaved as predicted; control `rc=0`.**

Carried with the acceptance, and **not a defect in the build**: the guard is correct,
correctly placed, and correctly wired at import — **and its `raise` is unreachable over the
real `MEMBERS` at this pin.** §5. That changes what the deliverable should be *read as*, not
whether it meets its criteria.

---

## 1. MY INSTRUMENT, AND WHETHER IT DIFFERS

The TO requires a second seat because a seat must not grade its own work
(`mdpf_category_registry.py:992` precedent, COO ruling 72258 s.3(d)). **Rule 22's sharper
half is that a second seat re-running the FIRST seat's method is repetition, not
corroboration.** So:

| | Author `~Z` | This seat `~L` |
|---|---|---|
| subject | the **working tree** | the tree **materialised from commit `3e88e10511`**, sha256-verified against `git show <PIN>:<path>` before any arm runs |
| plane | **in-process**: `import`, then call `_check_crosswalk_keyspace(<hand-built list>)` | **out-of-process**: mutate the module, score the `import` itself in a fresh subprocess |
| domain | the **function** | the **wiring** — the call site at `:613` over the real `MEMBERS` |

**I did not assert the difference; arm B1⊕B2 exhibits it.** Delete the one import-time call
line at `:613`, keep the bad member:

```
B1  my instrument      import mdpf_category_registry            -> rc=0, CLEAN   (catches it)
B2  author's AC1 cmd, verbatim, same de-wired module            -> rc=1, RAISES  (blind to it)
```

Their command calls the function directly, so removing the call site is invisible to it.
**Their four PASS rows are all invariant to whether the guard is wired.** The wiring *is*
present — `:613`, column 1, module scope, measured here — so this is a statement about what
their evidence is evidence *of*, not a contradiction of their result.

**Pin the CONTENTS and the BUILDER** (the TO's words): builder recorded as
`git archive --format=tar <commit> data/mdpf/scripts/gold`; contents verified
`sha256=1f250a9da534984b…` for the registry and `3bbae3564803cd96…` for the crosswalk.

## 2. WHICH ARMS MOVE ACROSS THE REPAIR (arm B3)

The `:992` control's own lesson: *an arm that is green against the unrepaired code cannot
tell a landed repair from an unlanded one.* Against the pre-repair parent `d37e12809a`:

- **A1 (import clean) and A3 (SMA resolution) are GREEN PRE-REPAIR.** Neither can evidence
  that this repair landed. They are regression arms and correctly so.
- **A2 (import raises) and B1 (de-wired import goes clean) MOVE.** The landed-vs-unlanded
  verdict rests on those two alone.
- Author's AC1 against pre-repair: `AttributeError` — the function does not exist.

## 3. THE FOUR CRITERIA

| # | Criterion | Instrument | Result |
|---|---|---|---|
| **F3-1** | assert exists and RAISES **at import** on a member_id outside the keyspace | **A2** — specimen bound into `MEMBERS` at module scope so the guard meets it at its real call site; subprocess `import` | **PASS** `rc=1`. Refusal **localised** to `"ABSENT from the crosswalk canonical keyspace"` and naming `opal_conservative_growth` — not merely "something raised". |
| **F3-2** | does NOT raise on the current, correct population | **A1** — subprocess import of the pinned module | **PASS** `rc=0`. **Denominators: 9 model-class members of 15 registered; keyspace 11 model_keys; 0 outside.** The guard runs at import, so a clean import *is* the negative arm. |
| **F3-3** | the two mapped SMA members still resolve | **A3** | **PASS** — `opal_div_sma -> divz`, `opal_growth_sma -> pfoe`. 2 of 2 map rows. They carry `asset_category='strategy'`, so the guard's first predicate skips them. |
| **F3-4** | `self_test` rc=0; py_compile + ruff py39 clean | §4 | **PASS** — and see §4 for the honest limit. |

**The input that makes the guard refuse, named:** a `CategoryMember` with
`asset_category='models'` and `member_id='opal_conservative_growth'` — the incident's own
specimen, the display label a seat actually misread, which would have moved
**$34,585,361.39 of PRIMARY AUA into Custom**.

## 4. F3-4 — THE CRITERION I CAN ONLY RE-RUN, SAID PLAINLY

Measured on the **pinned** copy, with the gate **decomposed** rather than trusting the
wrapper: `self_test rc=0` (captured on the line that ran it, before any pipe could reset
`$?`), **0 `^FAIL` lines**, stdout **1950 bytes**, `py_compile rc=0`, `ruff --target-version
py39` *All checks passed!*, and two runs **byte-identical at 1950 bytes**.

**This is the same property the author measured, by substantially the same commands.** Running
the subject from the pin instead of the tree and splitting `commit-gate.sh` into its
`py_compile` + `ruff` limbs is a *thinner* independence than Planes A/B carry, and I am not
going to dress it up as more. **For F3-4 I am closer to repetition than to corroboration.**
It is also the criterion where that matters least: compile-and-lint is objective and
single-valued.

*(Working tree == pin for this module, verified by diff, so nothing turns on the choice here.)*

## 5. OBSERVATION CARRIED WITH THE ACCEPTANCE — what the guard actually protects

**Class: OBSERVATION / INERT.** Blocks nothing, and I took no action on it. Routed to
`3.0.0_SA_CVO~Z` per the surprise channel, cc the issuer.

`_model_members()` (`:279`) **derives** every model-class member:

```python
for e in _xw.CANONICAL_MODELS:
    if e.cohort_class != "model": continue
    out.append(CategoryMember(member_id=e.model_key, asset_category="models", ...))
```

The guard then tests `m.member_id in {e.model_key for e in _xw.CANONICAL_MODELS}` — **the
value is drawn from the set it is then tested against.** Measured, three ways:

- **C1** `{model-class member_ids} == {model_keys where cohort_class=='model'}` → **True**,
  `0` unmatched in each direction.
- **C3** `asset_category="models"` is set at **exactly 1 site of 2** `asset_category=`
  assignments in the pinned module; `ALTERNATIVE/INSURANCE/CLIENT_MEMBERS` are all empty
  tuples, so no other collection can contribute one.
- **C2** Rename `opal_intermediate` → `opal_intermediate_RENAMED` in the crosswalk: import
  stays clean, the registered member **silently renames with it**, count still 9, guard
  silent. **The guard cannot detect drift — drift needs two independent sources and there is
  one.**

**Therefore the invariant held 9 of 9 by CONSTRUCTION, not by convention.** The TO's premise
— *"TRUE TODAY, 9 of 9, and enforced by NOTHING"* — is exactly right about **enforcement**,
and the reason it was true is **derivation**. The distinction matters because it relocates
the risk: today the `opal_conservative_growth` specimen **cannot be registered by any code
path in this module**; it becomes registrable the moment `_model_members()` stops deriving
from the crosswalk. **The guard is a tripwire on a door that is currently welded shut — and
it is on the right door.** It is worth nothing against today's population and everything
against that future edit.

**Why this is not an argument to change anything now:** the TO explicitly forbids widening,
and I agree with the scope as cut. Placing the guard *before* the hazard is the correct
order; the alternative — waiting for the derivation to be replaced and then adding the
assert — is the "first violation is also the first test" failure the TO exists to end. **I
am recording what the guard is evidence of, not asking for it to be different.**

## 6. SEATING — SURFACED, NOT WORKED AROUND

`1.0.0_SA_CTO~Z` named this explicitly and `0.0.0_AB_MSTR~Z` relayed it: a seating that
exists only in a message is not a seating. **Measured just now:**

```
python .tools/to-check.py --all --assignee '0.4.0_DS_ClientPlatform~L'
  total=0  projects=0  scanned=2132  unresolved_serials=0
TO-F3-DS on disk:  <issued_to>0.4.0_DS_ClientPlatform~Z</issued_to>   (line 7)
```

**`unresolved_serials=0` — so this is NOT the known `SEATED:`-prose notation defect.** The TO
names the *control role* ("a second DS seat authors the control") but no serial, and no TO in
the estate is addressed to `~L`. I did the work rather than blocking on it, and I am **not**
editing the TO: **that write is `2.0.0_SA_COO~Z`'s act.** `<issued_to>` should almost
certainly keep naming `~Z` as the build assignee; what is missing is a record of the control
seat.

## 7. PUSH STATE — MEASURED, AND PERISHABLE

Read `2026-08-27T18:56:01Z` against `origin/SITEZ = 2098e27abe40e9092740a2130c7d65f3f85e9f09`
by `merge-base --is-ancestor`, with an `origin/CLOUD` negative control that fires:

```
3e88e10511 ON ORIGIN   8731ca2a28 ON ORIGIN   c0469fafa0 ON ORIGIN   b8b26797fc ON ORIGIN
NEG-CTL: 3e88e10511 NOT on origin/CLOUD
```

**This claim expires the next time the integrator pushes.** `0.0.0_AB_MSTR~Z` is the
integrator; this seat commits to its own lane and does not push (LD-0367).

## 8. WHAT THIS ACCEPTANCE DOES NOT SAY

- It does **not** lift `D1_CATVIEWS`' NO-SHIP, and is not an argument that it may be lifted.
- It does **not** touch the build pin or any deployed artifact. The guard is committed and
  deliberately not deployed; `build_package.py` assembles from a pinned commit.
- It does **not** re-open the Finding 3 ruling or question whether `CANONICAL_MODELS` is the
  right authority for model identity. That frame is the issuer's.
- It does **not** evaluate `off_crosswalk` / any exemption path — named out of scope by the
  TO, and the exemption set is empty (0 of 9).
