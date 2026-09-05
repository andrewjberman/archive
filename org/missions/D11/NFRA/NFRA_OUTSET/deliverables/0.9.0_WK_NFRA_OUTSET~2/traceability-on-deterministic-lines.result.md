# TO-OS-s-11 result -- every deterministic report line now names its tool, vintage and re-run recipe

**TO:** `NFRA_OUTSET.TO-OS-s-11` (`.../task-orders/NFRA_OUTSET.TO-OS-s-11.traceability-on-deterministic-lines.md` @`f2ef16d70a`)
**Cell:** `OS-s-11` - **outcome_ref:** FWD-3 - **verb:** build - **depends_on:** OS-s-10
**Executed by:** `0.9.0_WK_NFRA_OUTSET~2` in worktree `C:/tmp/wk-OUTSET-2`, branch `wk-OUTSET-2`, base HEAD `f2ef16d70a`
Both addressing limbs read `~2` at HEAD before I started; no carry step.

> **HEADLINE, with the denominator the arm count does not carry: 4 of 4 deterministic strata now carry a re-run recipe, and 1 of 4 has a DEMONSTRATED end-to-end reproduction.** Stratum C's own printed recipe was re-run and its 17 rows re-derived EXACTLY by an independent implementation of the documented fold -- with a negative control proving the comparison can fail. The other three carry recipes that are untested (D, B-host) or untestable on this fabric (the seam-fed exits, because nothing publishes and the runner holds no grant). **Twelve green arms are not a reproduced report.** Row `NFRA_OUTSET-W2-S18`.

---

## 1. WHAT WAS MISSING

`render_stratum` rendered `stratum / question / vintage / denominator / rows`. The vintage was a
prose string (`"git history @<pin>, trailing 14d"`); there was no tool, no invocation and no way
for a reader to re-derive a row. The cell's manifest evidence class is **absent** -- correctly:
nothing in the report was re-runnable.

Meanwhile the OS-s-10 seam artifact was *already carrying* `tool` and `argv` -- the producer
records exactly what it ran -- and `_outset_read` dropped both on the floor. Half the traceability
this cell needed was already being published and simply never read.

## 2. WHAT I BUILT -- `infra/aws/ec2/estate-report-runner/estate_report_runner.py` only

| Change | Where | What |
|---|---|---|
| `REPRODUCIBILITY_CLAIMS` + `_trace()` | `:1220-1264` | The recipe shape: `tool`, a list of **concrete argv lines**, `vintage`, `claim`, `note`. A recipe a reader must reconstruct is not a recipe. |
| `_stratum(..., reproduce=None)` | `:1266` | One **optional** additive key. The status vocabulary is untouched -- that contract is SPEC s.5's and the module says so at `:1587`. |
| `render_trace()` + wired into `render_stratum` | `:1291` | The recipe reaches the report. An **absent** recipe renders LOUDLY (`NO RECIPE ... UNVERIFIABLE BY THE READER`), for the same reason a failed instrument does. |
| `_outset_read` surfaces `tool` + `argv` | `:1620`, `:1660` | The producer already recorded them; two dict keys make a seam-fed row `rail-reproducible`. |
| `_outset_trace()` | `:1690` | One helper, both seam consumers. If the artifact names no tool/argv it returns `not-reproducible` **with the reason** rather than inventing a plausible command. |
| a recipe on every stratum, every exit | A, B, C, D | Including the failure exits -- 8 exits, 8 recipes. |

**The claim vocabulary is a declared domain, not an ad-hoc string.** Three values, one axis
("what KIND of recipe does this row carry"): `rail-reproducible` (a comp-tool + argv the
**producer** recorded), `host-reproducible` (exact git argv at a named pin + the fold), and
`not-reproducible` (**with the reason**). `_trace` raises on anything else -- the battery proves
it. And the module states in its own text what the field does **not** claim: it describes the
**recipe, never the reader's access**. A recipe you are not entitled to run is still a recipe, and
conflating the two would let the IAM gap (`W1-S19`) read as an evidence gap.

## 3. ACCEPTANCE

### O11-AC1 -- PASS by output

`timeout 120 python .tools/tests/test_os11_traceability.py` - expect `PASS` - **rc 0**

```
=== test_os11_traceability: PASS (12/12) ===
```
Second grain: `python -m pytest -q` -> `1 passed in 10.59s`.

| arm | result |
|---|---|
| A1 | every deterministic stratum carries tool+invocation+vintage+claim -- **8 of 8 exits clean** |
| A2 | a seam-fed row names the **producer's own** tool and argv (`comp-heat drift`, `python .tools/comp-heat drift --budget 60 --json`) |
| A3 | a host-computed row names **concrete git argv** at the pin |
| A4 | a stratum with nothing to re-run says `not-reproducible` rather than inventing a command |
| **B RED MUTANT** | the recipe dropped **at the definition** of `_stratum` -> **0 of 8** exits still carry one. Mutated at the definition deliberately: a use-site mutant is only as wide as that site, and I shipped one last order that left a second live carrier (`W2-S17`) |
| C1/C2/C3 | absence renders loudly; a mutant that renders it silently breaks the arm; the recipe reaches the **rendered** stratum |
| D | the claim vocabulary is closed -- an undeclared value is refused, not defaulted |
| **E** | **THE REPRODUCTION** -- runner rows **17**, independent re-derivation **17**, `identical=True` |
| **E3** | **NEGATIVE CONTROL** -- corrupt the recipe (`--since` 90d -> 2d) and it yields **107** cold subtrees instead of 17, `rows differ=True`. Arm E can fail |

**Regressions on the same runner file:** `test_os9_cochange_source.py` **16/16**, `test_os10_seam.py` **12/12**, both rc 0.

### O11-AC2 -- JUDGMENT (`judgment="true"`) -- EVIDENCE ONLY, NO VERDICT

**The row taken**, from stratum `C_lifecycle` at pin `f2ef16d70aa171efa000e0cbf8a22825e64971a1`:

```
{"subtree": ".tools/valgate", "last_touch": ">= 90d ago (outside the scan window)"}
```

**The recipe that row names**, rendered by the report itself:

```
reproduce: tool=git (host-computed; no tool exists for the citation leg on this host)  claim=host-reproducible
           at vintage: host git history @f2ef16d70aa171efa000e0cbf8a22825e64971a1, trailing 90d
           $ git -C <repo> ls-tree -r --name-only wk-OUTSET-2
           $ git -C <repo> log wk-OUTSET-2 --since 2026-06-07T12:00:00+00:00 --name-only --no-merges --pretty=format:
           note: run BOTH at pin f2ef16d70a... with TZ=UTC, then apply the fold in _stratum_lifecycle:
                 map each path to its depth-2 prefix (only paths with >=3 segments), take universe MINUS
                 touched, sort, and take the first 30. The CITATION leg is NOT part of this recipe because
                 it is not measured here at all.
```

**Re-run, and reproduced.** Both commands were executed as printed (substituting `<repo>`), and the
rows re-derived by an implementation of the fold written **independently of the runner's** --
deliberately not a second call to `_stratum_lifecycle`, which would have proved only that a
function is deterministic:

```
runner rows=17, independent re-derivation rows=17, identical=True
```

**And the comparison can fail.** Corrupting the recipe's `--since` to 2 days yields 107 cold
subtrees, `rows differ=True`. Without that, "the rows matched" would be an unfalsified claim.

**WHAT IS NOT REPRODUCED, because the criterion says a row that cannot be reproduced IS the
finding:**
- `D_naming` -- recipe names the compile step and the pin; **not re-run here**, it needs the manifest this host pulls at that pin. Reconstructing one would be a second implementation.
- `B_relationships` (host stand-in) -- recipe is a git log command plus the `attribute_path` fold; reproducible in principle, **not exercised end to end**.
- `A_propagation` and `B_relationships` **via the seam** -- their recipes come from the artifact's own `tool`/`argv`, and every arm exercising them uses an **injected** artifact. Nothing publishes to a seam prefix (`W2-S15`) and the applied role grants nothing on one (`W1-S19`). `rail-reproducible` is, on this fabric, a claim about the recipe that has never been exercised against a real publish.

## 4. GATES

| Gate | Result |
|---|---|
| `bash .tools/commit-gate.sh` (3 files) | `OK: pre-commit gate clean for 3 of 3 file(s)`, rc 0 |
| non-ASCII introduced | **0** |
| `comp-system --gate --changed` | `NOT_APPLICABLE ... gate open`, rc 0 -- pathspec matches no trigger |

## 5. ROWS FILED

| id | class / hazard | one line |
|---|---|---|
| `W2-S18` | OBSERVATION / **ARMED** | 4 of 4 strata carry a recipe; **1 of 4** is demonstrably reproduced. Carry that denominator wherever the 12-of-12 goes |
| `W2-S19` | OBSERVATION / INERT | this cell's edit broke OS-s-9's mutation anchor; the uniqueness assert **refused loudly** instead of mutating nothing. Re-pointed. **OS-s-14 will hit it too** |
| `W2-S20` | OBSERVATION / **ARMED** (`3.0.0_SA_CVO`) | the `_stratum` shape now carries a field SPEC `@58505c291` does not describe; the spec is not in any `<paths>` and only the CVO can close the gap |

## 6. DECLARED NON-APPLICATIONS

- **No spec document edited** -- SPEC `@58505c291` is a commit-pinned CVO deliverable, not a file in this order's `<paths>`. Row `W2-S20`.
- **The `reproduce` field is OPTIONAL, not required, in the shape** -- a required field would break every caller and consumer at once. The **battery** requires it of the four deterministic strata, which puts the obligation where it can be enforced without widening the contract for callers that have no recipe to give.
- **No producer stood up and no IAM touched** -- both outside `<paths>`; `W2-S15` and `W1-S19` carry them. Setting `ESTATE_OUTSET_SEAM_PREFIX` would point the runner at a prefix nobody publishes to.
- **`D_naming` not reproduced by reconstructing a manifest** -- that is a second implementation of the compile step, which the BOUNDS forbid.
- **No monitor, alarm or freshness-checker; no delete verb; no new dependency.**
