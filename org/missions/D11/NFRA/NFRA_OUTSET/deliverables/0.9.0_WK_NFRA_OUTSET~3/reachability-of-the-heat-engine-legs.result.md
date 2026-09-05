# TO-OS-s-15 result -- reachability of the heat engine's O2-O4 legs

**Produced by `0.9.0_WK_NFRA_OUTSET~3`** (slot ~3, worktree `C:/tmp/wk-OUTSET-3`, branch `wk-OUTSET-3`),
executing an order whose `<issued_to>`, DELIVERABLE line and `<paths>` block all name
`0.9.0_WK_NFRA_OUTSET~1`, after a re-seat. That divergence is row `NFRA_OUTSET-W3-S1`.

**This document sits in `deliverables/0.9.0_WK_NFRA_OUTSET~3/`, NOT the `~1` folder the order names, and that
was decided by a MEASUREMENT rather than a preference.** Writing to the `~1` folder was tried first and the
lane gate REFUSED the commit: `owned-paths-validate.py` clause 4 (ADHC_OWNPTH.004) resolves the owner from the
SERIAL IN THE PATH, so `deliverables/0.9.0_WK_NFRA_OUTSET~1/` is a FOREIGN folder to serial `~3` no matter what
the order's `<paths>` block says. The order's own `<preflight>` lane clause grants a worker "its own
deliverables folder by the tree convention", and that folder is the only one that both satisfies the gate and
is inside the grant. Recorded as row `NFRA_OUTSET-W3-S5` with the refusal verbatim. **The order's `<paths>`
block and the mechanical lane gate disagree about this path, and the gate is the one that decides.**

**TO:** `org/missions/D11/NFRA/NFRA_OUTSET/task-orders/NFRA_OUTSET.TO-OS-s-15.reachability-of-the-heat-engine-legs.md`
· **verb:** decide · **outcome_ref:** FWD-8 · **cell:** OS-s-15 · **depends_on:** OS-s-1
**Tree vintage for every measurement below:** HEAD `61904105639022e4f0a3601a3954860ca7283be6`.

⛔ **BOTH CRITERIA ARE `judgment="true"`. This document records evidence and a reasoned reading and writes
NO verdict on either.** `3.0.0_SA_CVO` grades them at L9.

⛔ **NOTHING WAS BUILT AND NOTHING WAS REMOVED.** This cell is read-only on `.tools/comp-heat` and
`org/modules/heatmap/` and changed no byte of either -- confirmed by the commit's own pathspec. A "retire"
reading here is a RECOMMENDATION to the issuer, never an act.

---

## 0. THE DECISION, up front

| leg | module | reachable from `comp-heat`? | retire? |
|---|---|---|---|
| O2 | `object_locality.py` | **NO** -- 0 of comp-heat's 6 heatmap imports name it | **NO. Not a retire candidate.** A live non-CLI consumer imports it, and the CLI's substitute computes a different, weaker quantity. |
| O3 | `object_recommend.py` | **NO** -- 0 importers outside `object_report.py:39` | **NO. Wire it.** It is the verify-before-recommend guardrail the live CLI already defers to BY NAME while shipping archive candidates without it. |
| O4 | `object_report.py` | **NO** -- 0 importers anywhere, 0 runners | **NO, but it is the weakest of the three.** It is a render, and FWD-8's ACCEPT clause is about the ranked list with a reason per line, which is O3's payload. |

**Therefore `OS-s-16` should exist, and it is a WIRE, not a build** (build ladder rung 2 -- the estate already
has the code, it self-tests, and it runs end-to-end today). Full reasoning in section 4.

---

## 1. What I measured, and with which instrument

The question "is this leg reached?" fails in one direction: **an empty search reads exactly like a dead leg,
and that error retires something live.** Two instruments on different substrates were used, and the search
instrument carried a positive control in the same invocation shape.

- **Instrument A -- native `Grep` (text).** Chosen over `comp-find` deliberately: `comp-find` CONTENT mode has
  two measured false-zero modes on this project (`NFRA_OUTSET-S2`, rc 124 with zero bytes on both streams;
  `NFRA_OUTSET-S6`, a sub-floor `--budget` returning rc 0 with a full confident denominator and no budget
  line). Both are silent, and the second one poisons the very denominator a coverage claim rests on.
- **Instrument B -- Python `ast` parse (structure, not text).** Different substrate: it resolves `import`
  statements as syntax, not as strings, so a commented-out or prose mention cannot inflate it.
- **Positive control (A):** `object_freshness` -> **239 occurrences across 73 files**, reaching `.tools/`,
  `infra/`, `org/` and `docs/`. The sweep was live; the smaller counts below are measurements, not silence.

**Instrument B's denominator, stated because a `*.py` glob would have silently excluded the one file the
question is about:** 30,559 tracked files = **5,624** matching `*.py` (all 5,624 AST-parsed, **0 unparseable**)
**plus 42 extensionless tracked python-shebang scripts** (39 parsed; 3 unparseable, all vendored numpy
`.pyx`/`.pxd` under `infra/aws/lambda/layers/`, none heatmap-related). `.tools/comp-heat` has no extension and
lives only in that second pass -- scanning only `*.py` would have produced a confident zero for the CLI itself.

## 2. The import census (both instruments agree)

**`.tools/comp-heat` imports exactly two heatmap modules, at six sites:**

| module | leg | sites in `.tools/comp-heat` |
|---|---|---|
| `heat_map` | S0 | `:165` (`cmd_freshness`), `:349` (`cmd_score`), `:418` (`cmd_compare`) |
| `object_freshness` | O1 | `:166` (`cmd_freshness`), `:271` (`cmd_drift`), `:419` (`cmd_compare`) |
| `object_locality` | **O2** | **none** |
| `object_recommend` | **O3** | **none** |
| `object_report` | **O4** | **none** |

**The TO's premise "the CLI reaches O1 only" is MEASURED TRUE**, and the fifth subcommand does not disturb it:
`cmd_federated` (`:563`) reaches `.tools/_trino_fed.py`, not the heatmap engine at all. Subcommand set measured,
not read: `python .tools/comp-heat --help` -> rc=0, `{freshness,drift,score,federated,compare}`.

**Importers of each leg, whole tracked corpus:**

- `object_locality` -> **3**: `ms_heat_index.py:62`, `object_recommend.py:43`, `object_report.py:38`
- `object_recommend` -> **1**: `object_report.py:39`
- `object_report` -> **0**
- (`ms_heat_index` -> **0** importers; it is a `python ms_heat_index.py` entry point, not a library)

**No runner, scheduler or launcher exists for any of the three.** Searched `*.{tf,yaml,yml,sh,json,cmd,bat,toml,cfg,ini}`
for `ms_heat_index|object_report.py|object_recommend.py|object_locality.py`: every hit is a proof-of-spec
document, a deliverable, a tool-census sidecar, an audit log, or one Terraform **comment**
(`infra/aws/terraform/shared-infra/s3.tf:357`). Zero invocations.

## 3. The three facts that decide it

### 3a. O2 is load-bearing OUTSIDE the CLI

`org/modules/heatmap/ms_heat_index.py:62` -- `from object_locality import aggregate_tree  # noqa: E402  (DS O2 rollup, unmodified)`.
`ms_heat_index.py` is a live producer, not a spike: `org/tier1_exec/1.0.0_SA_CTO/deliverables/NFRA_TOOLUNIFY_CENSUS/C.sidecar.json:41`
records `warehouse/ms_heat/ms_heat_index.json` at `last_modified_utc 2026-07-17T18:09:45Z`, 2,626,103 bytes,
and `:44` names the producer script as `org/modules/heatmap/ms_heat_index.py`; `base.sidecar.json:169` records
the prefix's role as *"feeds ms_heat_snap Iceberg table via snap_ingest staging"*.

**READ FROM ANOTHER SEAT'S ARTIFACT, NOT MEASURED HERE** -- this worker read no S3 plane and makes no claim
about that object's current state. What is measured here is the import edge. **Retiring O2 breaks a stager.**

### 3b. The CLI's substitute for O2 computes a DIFFERENT, WEAKER quantity -- exercised

`cmd_freshness` gets its cold-directory list from S0's `cluster_by_locality` (`.tools/comp-heat:214`), filters
it at `:215-216`, and renders it at `:236` as **`cold SUBTREES (n>=3, cold_frac>=0.8) -- archive candidates (ADVISORY)`**.

But `cluster_by_locality` (`heat_map.py:102-123`) groups by **`os.path.dirname`, the immediate parent only** --
a flat partition, one key per file. O2's `aggregate_tree` (`object_locality.py:80-108`) accumulates into
**every ancestor**, and `maximal_cold_subtrees` (`:112-134`) then returns only roots whose parent does not
itself qualify. These are different functions computing different quantities.

**Falsifier, run rather than reasoned** -- 8 synthetic scores, all `band="cold"`, `age_days=400`, at
`dead/{a,b,c,d}/f{1,2}.py`, both engines imported unmodified (rc=0, read directly from the process):

```
S0 cluster_by_locality (what .tools/comp-heat:214 calls): 4 keys = ['dead/a', 'dead/b', 'dead/c', 'dead/d']
  CLI filter n>=3 and cold_frac>=0.8 (.tools/comp-heat:215-216) -> 0 'cold SUBTREES': []
O2 aggregate_tree: 5 keys = ['dead', 'dead/a', 'dead/b', 'dead/c', 'dead/d']  (clustered_n=8/total_n=8)
  O2 maximal_cold_subtrees -> 1 root(s): ['dead']
  detail: [{'dir': 'dead', 'n': 8, 'n_cold': 8, 'cold_frac': 1.0, 'oldest_age_days': 400.0, ...}]
```

A directory tree that is **100% cold, 8 files, 400 days old** produces **0** archive candidates from the live
CLI and **1** from O2. So *"the CLI already does locality"* is false, and it is false in the direction that
matters to FWD-8. Filed as row `NFRA_OUTSET-W3-S4` (ARMED; the disarm needs a write to `.tools/comp-heat`,
which this cell does not hold and did not take).

### 3c. The legs are not rotten -- they execute today

- `python object_locality.py --self-test` -> **rc=0**, `OK: object_locality self-test passed (5/5)`.
- `python object_report.py --root <heatmap dir> --top 5` -> **rc=0** (read without a pipe), printing
  `=== O4 hygiene report (ADVISORY-ONLY -- never auto-archives) ===`. **The whole O2 -> O3 -> O4 chain ran
  end-to-end.** Retiring these is not reclaiming dead weight; it is discarding working code.

## 4. The reading, per leg (criterion O15-AC1)

**O2 `object_locality.py` -- NOT-REACHABLE-FROM-CLI, and NOT A RETIRE-CANDIDATE.**
The `file:line` the CLI *would* call: `.tools/comp-heat:214`, which today calls `cluster_by_locality` and
would instead call `object_locality.aggregate_tree` (`object_locality.py:80`) + `maximal_cold_subtrees` (`:112`).
Neither value the criterion offers is true of this leg, which is row `NFRA_OUTSET-W3-S2`: it is unreached by
the named caller and simultaneously load-bearing for an unnamed one (3a), and its capability is not
duplicated by what the CLI uses instead (3b).

**O3 `object_recommend.py` -- NOT-REACHABLE-FROM-CLI; NOT A RETIRE-CANDIDATE; WIRE IT.**
The `file:line` the CLI would call: `object_recommend.assess` (`object_recommend.py:99`), registered as a new
subparser in the block at `.tools/comp-heat:630-668`. Reachability alone would make this a retire candidate --
its only importer is O4, and O4 has none. **The reason it is not** is that `comp-heat freshness` **already
ships an archive-candidate list today** (`:236`) with **no inbound-reference check of any kind**, while
comp-heat's own module docstring (`:11-13`) says *"It never recommends-to-delete (that is O3, separately
guardrailed)"*. The tool defers by name to a leg nothing reaches. Retiring O3 would ratify a live surface that
names dead-looking directories with strictly less safety than the estate already built for it, and would leave
that docstring pointing at nothing.

**O4 `object_report.py` -- NOT-REACHABLE-FROM-CLI; the weakest case of the three, and still not a retire.**
The `file:line` the CLI would call: `object_report.classify` (`:49`) / `render_md` (`:55`), same subparser
block. It is a pure render over O3 (`classify` splits RECOMMEND into AUDIT-TRAIL vs ORPHANED-ARCHIVE; `render_md`
emits the markdown). FWD-8's ACCEPT clause -- *"a ranked list with the reason for each line"* -- is satisfied by
O3's payload rendered somehow; O4 is one way and a `comp-heat` subcommand's own printer is another. **If any
leg is folded rather than wired, it is this one**, and that is OS-s-16's call with the code in front of it,
not a retirement.

## 5. NEVER-AUTO-DELETE (criterion O15-AC2)

**PRD R-5, verbatim (`NFRA_OUTSET_PRD.md@7fb59f239b:220`):**
> **R-5 (the never-auto-delete doctrine):** FWD-8's list is advisory and nothing is removed by a tool. Absolute.

All three legs touch removal -- each exists to name things a human might archive -- so R-5 is restated for each,
and **each is measured against it rather than trusted on its docstring.** AST scan for filesystem-mutating
calls (`remove`, `unlink`, `rmtree`, `rmdir`, `removedirs`, `delete*`, `move`, `rename`) across all four files:

| file | removal/move calls | write calls | subprocess |
|---|---|---|---|
| `object_locality.py` | **0** | 1 -- `open@216` | 0 |
| `object_recommend.py` | **0** | 1 -- `open@148` | 2 -- `run@52`, `run@78` |
| `object_report.py` | **0** | 2 -- `open@103`, `open@126` | 0 |
| `.tools/comp-heat` | **0** | 3 -- `open@82`, `@293`, `@328` | 0 |

The scan's raw hits on `replace` were checked individually and every one is `str.replace` on a path or a
timestamp (`object_locality.py:74,76`; `.tools/comp-heat:73,171`) -- **zero filesystem `os.replace`**. Every
write is to an operator-named output path (`--json OUT`, `--out report.md`). Both `object_recommend` subprocess
calls are read-only `git grep`.

**So: no leg fails R-5, and none is a RETIRE-CANDIDATE on R-5 grounds.** The property is structural, not
declarative -- the code contains no call that could remove anything.

Three further observations, each load-bearing for the flag OS-s-16 would carry:

1. **O3 is the leg that IMPLEMENTS R-5's spirit**, not the one that threatens it: `referenced_by`/`referenced_index`
   return `["<grep-error>"]` on any exception or unexpected rc, and uncertainty resolves to **HOLD** -- it fails
   toward not-recommending. It emits the `comp-blast <node> --direction up --check-consumers` graph gate as a
   required per-candidate step rather than auto-running it.
2. **O4 never renders a delete instruction**: its header is `ADVISORY-ONLY -- never auto-archives` and its
   `AUDIT-TRAIL` class exists precisely to stop dated log dirs being read as archive-me.
3. **The gap R-5 currently has is in the LIVE tool, not in the dead legs.** `comp-heat freshness` prints
   `archive candidates (ADVISORY)` with no inbound-reference check; the advisory word is doing all the work.
   That is the asymmetry in section 4's O3 reading.

## 6. What would have changed my mind

Stated as falsifiers, because a decision that names none is an opinion:

1. **O2 -> RETIRE if** `ms_heat_index.py` were itself dead. It is the single edge holding O2 live. Had the
   import at `:62` been absent, or `ms_heat_index.py` shown to be an abandoned spike, O2's only remaining
   consumers would be O3/O4 and all three would stand or fall together. **This is the weakest link in the
   decision and the first thing a challenger should attack** -- and note the vintage: the S3 object behind it
   was last written `2026-07-17`, and this worker did **not** verify the producer still runs (see 7).
2. **O2 -> RETIRE if** `heat_map.cluster_by_locality` had actually computed maximal cold subtrees. Then the CLI
   would already hold the capability and O2 would be a duplicate implementation -- the build ladder would say
   delete it. The falsifier in 3b was run **because** that was the cheapest way to be wrong, and it came back
   the other way (0 vs 1).
3. **O3/O4 -> RETIRE if** `comp-heat freshness` did **not** already emit archive candidates. If the live tool
   were silent on "what is safe to put away", O3/O4 would be unbuilt capability with no consumer and YAGNI
   would govern -- FWD-8 would be an honest build-from-scratch. It is the *existing, unguarded* advisory list
   at `:236` that makes the guardrail leg worth wiring instead of deleting.
4. **All three -> RETIRE if** they no longer executed. A leg that cannot run is not a wiring job. Both
   exercised runs in 3c returned rc=0.
5. **OS-s-16 -> struck if** any leg had contained a removal call it could not be stripped of. None does (5).

## 7. Declared limits of this measurement

- **The S3/Iceberg half of 3a is another seat's artifact, read not measured.** No AWS plane was touched.
- **Not measured: how many real cold subtrees in this estate the flat grouper misses.** The falsifier proves
  the miss exists on a synthetic case; the estate-wide count needs a full-corpus `comp-heat freshness` run
  diffed against an O2 run over the same scores. That is OS-s-16's measurement, outside a `decide` cell.
- **Not measured: whether `ms_heat_index.py` is still scheduled.** Its import edge is measured; its cadence is
  not. Sibling `OS-s-7` (`0.7.0_AE_CloudOps~W`) measured that the neighbouring `code_heat` parquet has no
  refresh cadence and no owner. **That is that seat's measurement, cited not adopted**, and it does not
  transfer to `ms_heat_index` -- the two are different artifacts and I did not check the second.
- **A dynamic import (`importlib` with a computed name) would be invisible to both instruments.** Nothing in
  the census suggests one, but the coverage claim is over static imports.

## 8. Rows filed

| id | class / hazard | one line |
|---|---|---|
| `NFRA_OUTSET-W3-S1` | OBSERVATION / INERT | `<issued_to>` names slot `~1`; slot `~3` executed after the re-seat, so the deliverables folder name is not the author. |
| `NFRA_OUTSET-W3-S2` | OBSERVATION / INERT | O15-AC1's two-value vocabulary is not MECE over the measured world -- O2 is neither REACHABLE-FROM-CLI nor a RETIRE-CANDIDATE. |
| `NFRA_OUTSET-W3-S3` | OBSERVATION / INERT | O3 hardcodes `timeout=180` / `timeout=60` on its `git grep` calls; comp-heat's Rule T budget cannot reach them, so OS-s-16 must thread or refuse. |
| `NFRA_OUTSET-W3-S4` | OBSERVATION / **ARMED** | `comp-heat freshness` labels a flat leaf-dir grouping `cold SUBTREES`; a 100%-cold 8-file tree yields 0 candidates. Disarm needs a `.tools/comp-heat` write this cell does not hold. |
| `NFRA_OUTSET-W3-S5` | **BLOCKING** / INERT | The lane gate refused the deliverables write to the `~1` folder the order's `<paths>` names: clause 4 resolves the owner from the serial IN THE PATH. Resolved same-turn by landing in `deliverables/0.9.0_WK_NFRA_OUTSET~3/`, which the order's own `<preflight>` grants. |
| `NFRA_OUTSET-W3-S6` | OBSERVATION / INERT | Absorbs the issuer's amendment `b630052d6a` (`<issued_to>` re-addressed `~1` -> `~3`) and partly corrects its premise: a mis-addressed `<issued_to>` disables the **deliverables limb alone**, not "any path" -- the lane-ANY task-order and channel writes were admitted in the same call. |

## 9. What I changed

`org/missions/D11/NFRA/NFRA_OUTSET/surprise-channel/investigations/INVESTIGATION_v1.md` (6 rows appended;
`git diff --numstat` = **96 insertions, 0 deletions**, and the pre-existing byte prefix was asserted identical
before writing), this document, and the proof-of-spec instance beside it. **`.tools/comp-heat` and
`org/modules/heatmap/` were read and never written.**
