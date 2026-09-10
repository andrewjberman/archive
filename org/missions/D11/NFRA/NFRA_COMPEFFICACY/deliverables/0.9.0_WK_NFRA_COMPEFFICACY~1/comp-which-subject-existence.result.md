# CE-p-4 -- `comp-which` validates a subject's EXISTENCE, not only its shape

**TO:** `NFRA_COMPEFFICACY.TO-CE-P-4` (face amended 2026-09-10 ~00:1xZ @`2fbb844173`, merged to this
branch at `7f3742e9a3`) - **worker:** `0.9.0_WK_NFRA_COMPEFFICACY~1` - **branch:**
`wk-nfra_compefficacy-7-1`, cut from CLOUD @`0e9ef40b37` - **worktree:** `C:/tmp/wk-compeff-7-1`.

---

## 0. THE DEFECT, MEASURED BEFORE ANYTHING WAS WRITTEN

Captured on the UNPATCHED tool into `cep4_before.json` (7 questions), *before* a line of the fix
existed:

```
$ python .tools/comp-which "what does INF_D_99 write to s3"      # BEFORE
comp-which -- candidates for: "what does INF_D_99 write to s3"

  MATCHES (top 3 of 78 -- score is overlap, NOT a confidence):

  1. score 2.00   comp-pipescript io INF_D_99
                gold-script DAG -- intra-pipeline I/O (reads/writes), chains, column-gaps, ...
  ...
  rc=0
```

and in the spilled rank file:

```
  - rank: 1
    tool: 'comp-pipescript'
    score: 2.00
    vetted: true
    call: 'comp-pipescript io INF_D_99'
```

`INF_D_99` exists in no script tree. `GOLD_ID` (`.tools/comp-which:1279`) validated the SHAPE;
nothing validated the EXISTENCE. **`vetted: true` is the finding**: not a guess offered as a
guess, a route offered as a vetted one, to an object that is not there.

---

## 1. THE AUTHORITY CENSUS -- found, not invented

**Instrument 1, the pattern's consumers.** `python .tools/comp-find 'GOLD_ID' .tools --all`
-> **2 hits across 397 files scanned** (corpus=all; 4 ephemeral-floor, 1 binary not searched),
BOTH in `.tools/comp-which` (`:1279` DEF, `:2236` SURFACED). The pattern has **no second
consumer**, so there is no competing id-space to reconcile.

**Instrument 2, the estate's own resolvers.** `comp-which "where are gold ids registered"` found
no registry (it fell through to the on-rails `comp-find registered`, 6,524 hits / 29,315 files --
a denominator, not an answer). Reading the tools the router itself points at settled it:

- `org/modules/graph/pipeline_cli.py:203` `_discover_script_trees` -- *"re-derive the script-tree
  universe from the FILESYSTEM at call time -- NOT a frozen list ... A longer hand-list would have
  gone stale the next time someone adds a tree; a predicate cannot."*
- `org/modules/graph/pipeline_cli.py:3016` `_resolve_gold_script` -- resolves an id by **globbing**
  `data/inf/scripts/gold/` then `data/black_diamond/scripts/gold/`.

**This estate registers gold-script ids in the FILESYSTEM.** There is no registry file, and that is
a declared design position, not a gap. Nothing was edited; the authority is READ.

**The census (denominators):** 30 `data/<tree>/scripts/<layer>/` directories on disk; **3** carry
`GOLD_ID`-shaped stems.

| authority directory | ids | positive control |
|---|---:|---|
| `data/black_diamond/scripts/gold` | 29 | `A_00` |
| `data/cot/scripts/gold` | 28 | `A_00` |
| `data/inf/scripts/gold` | 43 | `INF_A_-1` |
| **distinct across all 3** | **74** | |

**The probes, verified absent BEFORE being planted** (denominator 3 of 3 dirs, 74 of 74 ids):

- `INF_D_99` -- ABSENT. The planted non-existent subject.
- `INF_D_20` -- ABSENT. `INF_D_02` is REAL; `INF_D_20` is the two digits transposed. The negative
  control.
- `INF_D_02` -- PRESENT. The positive control for the negative control.

---

## 2. THE CHANGE -- **ROUTER-SIDE, BY DECLARATION**

`.tools/comp-which`, **226 insertions, 0 deletions, 4 hunks** (blob
`810fad08478a27fcac5a5f8d54ee13ab6a79e0ce`). ASCII-only (0 non-ASCII bytes measured).

**Why router-side and not population-side.** A population-side fix has nowhere to land. The
populations `comp-which` ranks over -- `graph-call-manifest.yaml` `tools_index` and
`comp-coverage-map.yaml` -- describe **TOOLS**, not **SUBJECTS**; neither carries a gold-script id
and neither is the authority the census found. The subject authority is the filesystem, and the
order forbids editing a registry (correctly: a registry that is wrong is a row, not an edit). So
the only place a subject check can live is the router. **Consequence, stated rather than hidden:**
a second router, or any consumer that ranks without going through this file, does not inherit it
(section 5).

| hunk | what |
|---|---|
| `:1281+` (155 lines) | `_gold_subject_universe()` -- the authority as a **PREDICATE over the same substrate the estate's own resolver uses**, walking `data/*/scripts/*/`. `_authority_line()` names it with its denominator. `_resolve_gold_subject()` decides. `_edit1()` + `_nearest_ids()` build candidates. |
| `:2042+` (9) | the spilled rank file's header gains `subject`, `subject_resolved`, `authority_consulted`. |
| `:2398+` (9) | the per-question subject state is RESET at the top of `main()`. |
| `:2410+` (53) | **THE GATE**, at the router's entry. |

**Every layer, not only gold.** The walk covers `data/*/scripts/<any layer>/`, not just the three
gold dirs, deliberately: refusing a real id that happens to live in a silver tree would be an
OVER-refusal, and an over-refusal on the enforcing rail is worse than the confident mis-route it
replaces. The three gold dirs are simply where all 74 currently live.

**Fail-OPEN on an unreadable substrate.** An `OSError` anywhere in the walk yields an EMPTY
universe, and an empty universe **disables the check** (`_resolve_gold_subject` returns
`not-applicable`). A filesystem this cannot read must never become *"no registry carries it"* --
that would refuse every real id at once, on no evidence.

**A refusal is not a crash: rc 1, comp-which's OWN abstain code.** Not a new convention. `:2170`
already carries it -- *"The BANNER lets an AGENT see doubt. rc lets a PROGRAM see it"* -- and names
its only consumer, `comp-tool-hud.sh:424` `_route_out="$(... comp-which --route-only "$q" ...)" ||
_route_out=""`, where a nonzero blanks the nudge, which that hook's own comment states is the
intent. **Not rc 2**, which is this tool's ARGUMENT-error code (`--budget` misuse): the question
here is well-formed; the subject is not there. The rank file is still spilled, `tools_ranked: 0`.

**The candidate pass is deliberately not pure `difflib`.** `SequenceMatcher` scores `INF_D_20`
closer to `INF_D_10` (0.875) than to `INF_D_02` (0.75) -- so the single most likely real intent
behind a transposed id, *the exact negative control this check exists for*, was **ABSENT** from a
difflib-only list on the first implementation (measured on this tool). `_edit1()` adds the
adjacent-transposition limb and runs FIRST; difflib fills the remainder. Two passes because they
fail differently: edit-1 is exact and can return nothing; difflib always returns something and
orders by a ratio that does not model a transposition.

---

## 3. P4-AC1 -- THE BATTERY, ARM BY ARM

**Invocation (verbatim):**
`timeout 600 python org/missions/D11/NFRA/NFRA_COMPEFFICACY/deliverables/0.9.0_WK_NFRA_COMPEFFICACY~1/test_cep4_subject_existence.py`
-> **rc 0**, final line **`CEP4-SUBJECT-EXISTENCE-ENFORCED`**, `arms failed: none`.

The battery prints the CLI it ran (`C:\tmp\wk-compeff-7-1\.tools\comp-which`) because the `~/bin`
forwarder is baked to the MAIN tree (row W1-S2, ruled standing at the cut).

### (a) authority census -- printed first
As section 1. `[PASS] a` (3 dirs, 74 distinct ids, a positive control in each), plus
`[PASS] a:absent:INF_D_99`, `[PASS] a:absent:INF_D_20`, `[PASS] a:present:INF_D_02`.

### (b) planted non-existent -- `what does INF_D_99 write to s3`
```
comp-which -- SUBJECT NOT FOUND: "INF_D_99"

  NOT ROUTED. This question names a gold-script id that matches the id SHAPE
  but exists in no script tree, so every tool below it would be pointed at an
  object that is not there. 0 tools ranked -- deliberately, not for want of a
  match.

  AUTHORITY CHECKED: data/*/scripts/*/*.py stems matching GOLD_ID -- 74 ids across 3 directories: data/black_diamond/scripts/gold, data/cot/scripts/gold, data/inf/scripts/gold

  CANDIDATES -- nearest real ids by edit distance. These are CANDIDATES,
  NOT a route: comp-which did NOT decide you meant one of them.
    ? INF_D_09   [data/inf/scripts/gold]
    ? INF_D_11   [data/inf/scripts/gold]
    ? INF_D_10   [data/inf/scripts/gold]
    ? INF_D_08   [data/inf/scripts/gold]
    ? INF_D_07   [data/inf/scripts/gold]

  Re-ask with a real id, or list the id space:
    comp-find --name '*.py' data/*/scripts/gold
    comp-estate --definitions
  Verdict on the artifact: subject_resolved: false in the spilled rank file.
  -- rc=1
  [PASS] b:refused          -- the verdict is a first-class output, not a crash
  [PASS] b:authority-named  -- all 3 authority dirs NAMED in the terminal output
  [PASS] b:ranked-rows      -- ranked tool rows presented as a route = 0 (BEFORE: 78 of 78)
  [PASS] b:no-route-line    -- no tool is offered as a route
  [PASS] b:rc               -- rc=1, comp-which's existing ABSTAIN code (:2170)
  BEFORE this change, same question, same CLI: rc=0, 78 ranked rows, rank 1 = comp-pipescript io INF_D_99
```

### (c) positive control -- the four F-10 / C-S46 phrasings, BYTE-EQUAL
The four strings verbatim from
`org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~6/f10_lib.py:23-28`.

**The compared object, stated because it decides the claim:** the RANKED LIST = the `tools:` rows
of the spilled rank file (rank / tool / score / vetted / call / does) **plus** the terminal route
block. The spill **HEADER is excluded and named as excluded** -- that is where `subject_resolved`
lands, so comparing whole files would compare the fix against itself and could never pass.
Excluded from the terminal comparison: the Rule-T `WITHIN BUDGET` seconds (wall clock) and the
`rank-<pid>.yaml` filename (pid) -- both differ run-to-run **on an unchanged tool**.

| # | phrasing | rank rows | rc (BEFORE) | ranked-list diff | terminal diff |
|---|---|---:|---|---|---|
| 1 | `What AWS resources exist + how are they typed/connected?` | 78 of 78 (BEFORE 78) | 0 (0) | EMPTY | EMPTY |
| 2 | `What's the drift / blast radius / unmanaged surface?` | 78 of 78 (BEFORE 78) | 0 (0) | EMPTY | EMPTY |
| 3 | `Is any resource dual-managed across TF states?` | 78 of 78 (BEFORE 78) | 1 (1) | EMPTY | EMPTY |
| 4 | `Cloud-shape snapshot + diff over time` | 78 of 78 (BEFORE 78) | 0 (0) | EMPTY | EMPTY |

`[PASS] c` -- **4 of 4 byte-equal** on both objects.

### (d) negative control -- `what does INF_D_20 write to s3`
```
comp-which -- SUBJECT NOT FOUND: "INF_D_20"
  ...
  CANDIDATES -- nearest real ids by edit distance. These are CANDIDATES,
  NOT a route: comp-which did NOT decide you meant one of them.
    ? INF_D_00   [data/inf/scripts/gold]
    ? INF_D_02   [data/inf/scripts/gold]
    ? INF_D_10   [data/inf/scripts/gold]
    ? INF_D_09   [data/inf/scripts/gold]
    ? INF_D_08   [data/inf/scripts/gold]
  -- rc=1
  [PASS] d:not-confident      -- NOT routed with confidence
  [PASS] d:candidates-marked  -- marked as candidates, in words, ABOVE the list
  [PASS] d:nearest-offered    -- INF_D_02 is among the 5 candidates offered
  [PASS] d:candidates-are-real-- 5 of 5 offered candidates are real ids from the authority
  [PASS] d:ranked-rows        -- ranked tool rows = 0
  [PASS] d:rc                 -- rc=1
  BEFORE: rc=0, 78 ranked rows (a vetted route to a non-existent object)
```

### (e) the artifact -- the verdict told apart on the spilled rank file
Per the face as amended @`2fbb844173` (row W1-S1), a **THREE-value** field:

```
  case                                 subject          subject_resolved tools_ranked
  (b) planted non-existent             INF_D_99         false          0            authority: NAMED (154 chars)
  (c) POSITIVE CONTROL, real subject   INF_D_02         true           78           authority: NAMED (154 chars)
  (c) regression phrasing 1 of 4       (none)           not-applicable 78           authority: (not consulted)
  (d) misspelled real id               INF_D_20         false          0            authority: NAMED (154 chars)

  authority_consulted, verbatim from the (b) spill:
    data/*/scripts/*/*.py stems matching GOLD_ID -- 74 ids across 3 directories: data/black_diamond/scripts/gold, data/cot/scripts/gold, data/inf/scripts/gold
  [PASS] e             -- 4 of 4 spilled rank files carry subject_resolved + authority_consulted
  [PASS] e:vocabulary  -- a question with NO subject reads not-applicable, never true (row W1-S1)
  [PASS] e:real-routes -- a REAL subject still routes: rc 0 (BEFORE 0), 78 ranked rows (BEFORE 78)
  real-subject ranked-list diff: EMPTY
  [PASS] e:real-byte-equal -- the REAL subject's ranked list is BYTE-EQUAL to BEFORE (1 of 1)
```

`authority_consulted` is populated **exactly when the check ran** and empty when it did not.
Recording an authority against a question that never had a subject would be a fabricated claim.

### (f) a question carrying no gold id at all
`GOLD_ID.search()` over the four regression phrasings: **0 of 4 carry a gold id** (printed per
phrasing). The gate is structurally unable to fire on them, and 4 of 4 measured byte-equal.
`[PASS] f`.

### (g) the router's own routing harness
See section 4. `[PASS] g:grain`, `[PASS] g` -- rc 0.

---

## 4. ARM (g) -- THE HARNESS, AND ITS THREE PRE-EXISTING DEFECTS

Arm (g) was cut as the bare `python .tools/comp-which-routing-test.py`. **Three defects, all
PRE-EXISTING, all read in the harness's own source at `0e9ef40b37`** (row W1-S3, ruled by the
issuer @`2fbb844173`; the harness defects belong to `0.8.0_AE_CloudComp`):

1. **GRAIN.** `--binary-ref` defaults to `'HEAD'` (`:1134`); `:1177` `ref = None if
   args.binary_ref.upper() == 'WORKING' else args.binary_ref`; `:1181` `vintage, blob =
   extract_binary(ref, tmp.name)`. The bare form extracts the **COMMITTED blob** and is
   structurally incapable of seeing an uncommitted change -- it would have certified this fix by
   running the bytes the fix replaces. This one **fails GREEN**.
2. **GRANT.** `:1653` `out_path = args.out or BASELINE` writes
   `org/tier2_senior/0.8.0_AE_CloudComp/deliverables/comp-which-routing-baseline.json`, outside
   this worker's `<paths>`; the flag's own help says a regression run passes `--out` because
   *"A LATER VINTAGE MUST NOT CLOBBER A COMMITTED BASELINE"*.
3. **TERMINATION.** The bare form **does not finish under a 580 s bound ON THE UNPATCHED TOOL**:
   `.tools/comp-which` restored to its HEAD bytes (`git show HEAD:.tools/comp-which`), run
   `2026-09-09 23:42:21Z -> 23:52:01Z`, **rc 124**, 153 lines; then restored from the byte backup
   and **sha256-verified** (`57690d9c...` on both). The same bare form on the patched bytes: rc
   124, 290 lines. **The baseline was run first**: a wrong arm and a dead arm are different
   failures, and this arm was dead before the change.

**The arm as run** (the face's amended form):

```
python .tools/comp-which-routing-test.py --binary-ref WORKING \
  --out org/missions/D11/NFRA/NFRA_COMPEFFICACY/deliverables/0.9.0_WK_NFRA_COMPEFFICACY~1/cep4_routing_test_report.json

SUBJECT : .tools/comp-which @ WORKING-TREE
          blob 810fad08478a27fcac5a5f8d54ee13ab6a79e0ce   captured 2026-09-10T00:07:32Z
...
VERDICT: PASS -- controls held, zero pollution, and comp-which ABSTAINED on
         100% of generated gibberish.
rc=0     window 2026-09-10T00:07:30Z -> 2026-09-10T00:21:16Z
```

**Why the battery READS this run rather than re-running it inline, under a grain control.**
P4-AC1's own invocation is `timeout 600`, and the harness takes longer than that: **680 s**
(23:54:57Z -> 00:06:17Z) and **826 s** (00:07:30Z -> 00:21:16Z) on two consecutive WORKING runs.
A run inside the battery would blow the criterion's own bound. So the harness is run once out of
band by `cep4_run_routing_test.py` (committed, and exercised -- not a promise), and the arm reads
the record **under a grain control**: the blob the harness says it measured must equal
`git hash-object .tools/comp-which` at battery time, or the arm fails as stale.

```
  blob MEASURED                 : 810fad08478a27fcac5a5f8d54ee13ab6a79e0ce
  blob of .tools/comp-which NOW : 810fad08478a27fcac5a5f8d54ee13ab6a79e0ce
  [PASS] g:grain -- the recorded run measured the bytes under test
  [PASS] g       -- rc=0
```

**THE AMENDED BOUND IS BELOW THE MEASURED RUNTIME -- row `NFRA_COMPEFFICACY-W1-S4`.** The amended
clause (g) prefixes `timeout 600`. Both WORKING runs exceeded it (680 s, 826 s). Rather than infer
the consequence, it was **run at its literal bound**:

```
$ timeout 600 python .tools/comp-which-routing-test.py --binary-ref WORKING --out <report>
AMENDED-LITERAL-rc=124        window 2026-09-10T00:25:56Z -> 00:35:57Z   elapsed 601 s
```

**rc 124 is the 600 s clock, not a failing subject** -- the same harness, same flags, allowed to
finish, returns rc 0 and `VERDICT: PASS` on the same blob, twice. Recorded in
`cep4_amended_bound_probe.json` and printed by the battery **beside** the arm's verdict, never as
it -- exactly the treatment the issuer ruled for the bare form.

---

## 4a. CONTROLS

**MUTANT -- the battery CAN fail.** `.tools/comp-which` was mutated at the check's decision point
(`if not ids:` -> `if True:` in `_resolve_gold_subject`, so the resolver always returns
`not-applicable` and the router falls back to its pre-change behaviour) and the battery re-run
through the same invocation. Result: **rc 1, `NOT ENFORCED -- 13 arm(s) failed`, no token.** The
13: `b:refused`, `b:authority-named`, `b:ranked-rows` (*"ranked tool rows presented as a route =
78"*), `b:no-route-line`, `b:rc` (rc 0), all six `d:*` (*"0 candidates offered"*, ranked rows 78),
`e`, and -- **`g:grain`**, because mutating the file changed the blob and the recorded harness run
no longer described the bytes under test. The grain control did the job it was built for.
**Restored and byte-verified:** sha256 `4a56d2b5...4071` identical on the restored file and the
pre-mutant backup, `git hash-object` back to `810fad08...`, `git status` clean on the path.

**DETERMINISM -- STABLE.** Two consecutive full runs, diffed: **2 differing lines of 223**, both
`WITHIN BUDGET: ... used 0.19 s` vs `0.22 s` -- comp-which's Rule-T **wall-clock** reading, a
measured elapsed time and not a verdict. Every arm result, every byte-equality diff, every count
and every rc identical; both printed the token at rc 0. *Those same two line shapes are why the
(c) comparison excludes any `WITHIN BUDGET` line: they differ run-to-run on an UNCHANGED tool, so
including them would have made the byte-equality claim unfalsifiable in the wrong direction.*

---

## 5. P-6 -- THE INHERITANCE ANSWER

**Does every ranker path see the subject check?**

**Inside `comp-which`: yes, and by POSITION rather than by patching each path.** The gate sits in
`main()` immediately after `gid = GOLD_ID.search(q)` and **before** `hits` is built. Everything
downstream is therefore unreachable for an unresolved subject:

| path | reached on an unresolved subject? |
|---|---|
| the `RULES` curated loop / `hits` | no -- not yet built |
| `_default_router` (the DR2 posterior, the DEFAULT router) | no |
| the LEGACY cascade (strong-curated, surface-first drill, manifest backstop, `_posterior_backstop`) | no |
| the grep/glob on-rails fallback (`_run_primitive`) | no |
| `--json` (`_emit_json`) | no -- a dedicated `kind: "subject-unresolved"` object is emitted instead |
| `--route-only` (the HUD preview) | reached, and it shows the refusal (verified) |
| the WARM in-process path (`comp-which-routing-test.py:411`, which calls this same `main()`) | yes -- which is why the per-question state is RESET at the top of `main()` |

**Outside `comp-which`: NO, and here is the measured residual.** `comp-find
'comp_route[_a-z]*\.route\(' org infra .tools --all` -> direct `route()` call sites in first-party
source, excluding this file: **5 sites across 4 files** --
`org/modules/graph/comp_route_shadow.py:92`, `org/modules/graph/comp_route_eval.py:134` (via
`_sh.comp_route`), `org/modules/graph/comp_learns_leg4_exercise.py:73` and `:180`, and
`org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_TOOLHEALTH/clause_b_close_loop_exercise.py:111-112`.

**All five are evaluation / exercise harnesses. None routes a seat anywhere.** So: every
**agent-facing** ranker path inherits the check, because every one of them goes through this
`main()`; the non-inheriting callers are measurement code that scores the ranker rather than
answering a question. **That is the honest shape of P-6's warning** -- the check is router-side, so
a *second* router would not inherit it, and the reason none does today is that there is only one.

---

## 6. WHAT A SEAT NOW SEES ON A MISTYPED SUBJECT

A person can act on it without a follow-up. The output states, in order: that the subject was not
found; that the tool did **not** route and why (0 ranked, deliberately); **which authority was
checked, with its denominator and the three directories by name**; the nearest real ids with the
directory each lives in, explicitly framed as candidates the tool did *not* choose; and two
concrete next commands. The rc is a program-visible 1. The verdict is on the artifact, so a
measurement reading only the spill can tell *"0 rows because nothing fit"* from *"0 rows because
the subject does not exist"* -- two different failures with two different remedies.

## 7. WHAT THIS FIX DOES **NOT** COVER

1. **A subject that exists in a script tree but not in the SERVED graph.** The check answers *"is
   there a file with this stem"*, not *"does the estate's graph carry this node"*. A script
   committed but never deployed, or present but absent from `comp-pipescript`'s DAG, resolves
   `true` here and can still dead-end downstream. This is a strictly weaker claim than existence
   in the served plane, and the field says only what it checked.
2. **Non-gold-id subjects.** Only `GOLD_ID` subjects are validated. An S3 key, a lambda name, a
   portal component or a column name in a question is still shape-unvalidated -- the same class of
   defect, on other id spaces, untouched.
3. **A second router.** Router-side by necessity (section 2). See section 5.
4. **The id-space is a stem census, not a semantic one.** A file whose stem matches `GOLD_ID` but
   which is not a real pipeline script would resolve `true`.
5. **Ranking.** Nothing about scoring, ordering or the candidate pool changed for a resolved
   subject -- measured byte-equal, 5 of 5 questions (4 phrasings + the real subject).

---

## 8. GATES, CONTROLS AND VINTAGES

- `python -m py_compile .tools/comp-which` -> **rc 0** (P4-AC2, verbatim).
- `bash .tools/commit-gate.sh <file>` -> **`OK: pre-commit gate clean for 1 of 1 file(s)`** on
  **5 of 5** files touched: `.tools/comp-which`, `cep4_lib.py`, `cep4_capture_before.py`,
  `cep4_run_routing_test.py`, `test_cep4_subject_existence.py`. ruff py39 clean;
  **0 non-ASCII bytes** in `.tools/comp-which`.
- The gate **refused once, correctly**, on two variables left unused by the arm-(g) restructure
  (`F841` on `rt`, `rt_out_json`). Fixed at the cause; not bypassed.
- `.tools/comp-which-routing-test.py` was **NOT** edited: the subject check did not need to live
  beside the ranker, so the second granted path stays untouched.
- Vintages: branch cut `0e9ef40b37`; work commit `e4c2d4a3e7`; face amendment `2fbb844173`, merged
  `7f3742e9a3`; `.tools/comp-which` blob `810fad08478a27fcac5a5f8d54ee13ab6a79e0ce`.

## 9. ROWS FILED

| id | class / hazard | one line |
|---|---|---|
| `NFRA_COMPEFFICACY-W1-S1` | OBSERVATION / INERT | the accept's two-value `subject_resolved` could not cover the regression set it also named (0 of 4 phrasings carry a gold id). **RULED @`2fbb844173`** -- clause (e) re-cut to the three-value field. |
| `NFRA_COMPEFFICACY-W1-S2` | OBSERVATION / ARMED | `~/bin/comp-which` is baked to the MAIN tree; a bare PATH call from any linked worktree runs the UNPATCHED tool and **fails GREEN**. **RULED @`2fbb844173`** -- standing at the cut; the shim is CloudComp's. |
| `NFRA_COMPEFFICACY-W1-S3` | BLOCKING / ARMED | arm (g)'s bare invocation: defaults to the COMMITTED blob, writes outside the grant, and does not terminate at 580 s on the unpatched tool. **RULED @`2fbb844173`** -- arm re-cut to the parameterised form; harness defects to `0.8.0_AE_CloudComp`. |
| `NFRA_COMPEFFICACY-W1-S4` | OBSERVATION / ARMED | the amended arm (g) carries `timeout 600`; the harness measured 680 s and 826 s on two consecutive WORKING runs, and the literal amended command **measured rc 124** (00:25:56Z -> 00:35:57Z). Open. |

**PROOF-OF-SPEC:** `python .tools/proof-of-spec-check.py <instance> P4-AC1,P4-AC2,P4-AC3` ->
**`VALID (rc=0)`**, `acceptance rows=3 | violations=0`; alignment ENFORCE, forward-1 3/3,
forward-2 1/1, backward 1/1; surprises limb `4 entries; 4 open with a row id; 4 resolve to a
channel row`, mode ENFORCE.

## 10. ARTIFACTS

| file | what |
|---|---|
| `cep4_lib.py` | shared carrier: the authority census, the question set, the CLI invoker, the ranked-list isolator |
| `cep4_capture_before.py` / `cep4_before.json` | the BEFORE baseline, captured on the UNPATCHED tool, refuses to clobber itself |
| `test_cep4_subject_existence.py` | **P4-AC1** -- the seven-arm battery |
| `cep4_run_routing_test.py` | the arm-(g) runner (parameterised harness, out of band) |
| `cep4_routing_test.log` / `.rc.json` / `_report.json` | the arm-(g) record: harness output, rc + blob + window, the harness's own report |
| `comp-which-subject-existence.result.md` | this document |
| `NFRA_COMPEFFICACY.TO-CE-P-4.comp-which-subject-existence.proof_of_spec.json` | the proof-of-spec instance |
