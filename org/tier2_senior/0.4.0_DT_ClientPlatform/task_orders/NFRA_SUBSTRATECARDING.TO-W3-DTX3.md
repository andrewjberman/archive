# TASK ORDER — DTX3 · NFRA_SUBSTRATECARDING WAVE 3 · MATERIALIZER CARDING

<status>pending</status>

**to:** `0.4.0_DT_ClientPlatform~X` · **issuer:** `2.0.0_SA_COO~X` · **certifier:** `3.0.0_SA_CVO~X`
**scope:** 2 subjects / 14 cells · **contract:** `org/standards/SUBSTRATE_CARD.v2.schema.json`

✅ **DECOMP CERTIFIED?** NOT YET — cert is `3.0.0_SA_CVO~X`'s and runs on the cut packet. The
pipeline's own escape valve applies: a DECOMP-INVALIDATING verdict is the issuer's act to
re-decomp and re-issue. **Do not hold on it.**

<decomp_ref>
workflows/atom_decomposition/runs/nfra-substratecarding-w3/DECOMP.md @e48a7466ba

cells:
W3-gkih-1 W3-gkih-2 W3-gkih-3 W3-gkih-4 W3-gkih-5 W3-gkih-6 W3-gkih-7 W3-mdiu-1 W3-mdiu-2 W3-mdiu-3
W3-mdiu-4 W3-mdiu-5 W3-mdiu-6 W3-mdiu-7
</decomp_ref>

---

## AUTHORITY

Andrew-direct 2026-08-27, verbatim: *"everything runs under D11, dont get concerned about the
title nor are you allowed to invent gates without my explicit approval"* and *"go surgical mode
here, pivot, we need to find the materializers that actualy matter"*.

## YOUR SUBJECTS

| subject | writer class | write evidence | paths measured |
|---|---|---|---|
| `infra/aws/globgrph/kuzu_load.py` | UNCLASSIFIED | standing=SUPERSEDED and REACHABLE FROM THE LIVE NIGHTLY | **UNMEASURED — yours to resolve** |
| `infra/aws/globgrph/kuzu_stitch_load.py` | UNCLASSIFIED | standing=SUPERSEDED and REACHABLE FROM THE LIVE NIGHTLY | **UNMEASURED — yours to resolve** |

⛔ **THE SUBJECT GRAIN IS (FILE, WRITE PATH).** `derive_runner.py` is split because it has two
write paths differing in mechanism, bound AND authority. **If YOUR subject turns out to have more**
**than one write path, that is a BLOCKING surprise — say so; do not card them as one.** Path
multiplicity is measured for exactly one subject in this wave and assumed for none.

## ACCEPTANCE CRITERIA

| id | criterion |
|---|---|
| **DTX3-AC1** | 2 cards exist and all VALIDATE against the v2 contract. Every row carries `basis` + `evidence` + `owner`. |
| **DTX3-AC2** | `as_of` carries ONE wave pin: `commit_ish` and `graph_vintage` byte-identical across your cards. `carded_utc` is an HONEST clock read at a DECLARED grain (per-card or per-batch — **state which**), never estimated, never copied. |
| **DTX3-AC3** | **WHERE IS THE TABLE NAME BOUND** — every card states CLASS 1 / 2 / 3 with **the line that binds it**, and whether the bound set is **ENUMERABLE**. A class without a line number is not an answer. |
| **DTX3-AC4** | **WHAT IT WRITES** — a resolvable path or table name, never a description. ⛔ A card that says X is a materializer **without naming WHICH artifact is unfalsifiable** (1.0.0_SA_CTO~X's rule, six arrivals tonight). |
| **DTX3-AC5** | **TRIGGER** — plane (`events` / `scheduler` / `event-driven` / `none-found`) **plus BASIS**. ⛔ An ECS rule target resolves to a CLUSTER, not a script: any "X is triggered by Y" is **INFERRED** unless read from the task definition's container command. Mark it. |
| **DTX3-AC6** | **RULE 26** device/apply owner, and **RULE 25** dormancy (≥90d stale = dormant absent a declared exception). Rule 26 is **NOT a class constant** — measured non-uniform in wave 2. |
| **DTX3-AC7** | **DISCOVERABILITY IS NOT COVERAGE.** No card asserts completeness of the writer population. If your subject can write tables it does not name, say so and say the bound is **UNBOUNDED**. |
| **DTX3-AC8** | **QUALIFY-DO-NOT-FIX.** Zero commits by this lane touching a module it cards. The Class-3 remedy (`choices=`, already written at `snap_store.py:415`) is **NAMED, NOT APPLIED**. |

## ⛔ INSTRUMENT TRAPS MEASURED THIS SESSION — DO NOT REDISCOVER THESE

- **`append` is TWO THINGS** — plain `list.append()` and pyiceberg's `table.append(df)`. A token
  census on it returns confident nonsense. Resolve at the CALL SITE.
- **`to_arrow(` and `load_table(` are READS**, and both sat in a "strong write" token list all night.
- **A regex over dict text over-counts nested keys** — an allow-list read 8 by regex and **4 by AST**.
- **`pyiceberg` appears in files that never use it**, inside quoted citations of another file's header.
- **A bare line number is not a citation** — `CLAUDE.md:552` expired 4h47m before it was first
  cited, and with the live law skew it does not resolve identically across seats **right now**.
- **`comp-find` with a content pattern AND `--name` scans ZERO files** (deterministic).
- **`comp-keys prefix` truncates to 40 by DEFAULT** with the total printed AFTER the rows.

## REPORTING

Route completion to `3.0.0_SA_CVO~X`, cc issuer. State **PUSH STATE as a MEASURED value**
(`ls-remote` read + `merge-base --is-ancestor` with a positive control), never a default.


<proof_of_spec>
  <criterion id="DTX3-AC1" cell_refs="W3-gkih-1, W3-gkih-2, W3-gkih-3, W3-gkih-4, W3-gkih-5, W3-gkih-6, W3-gkih-7, W3-mdiu-1, W3-mdiu-2, W3-mdiu-3, W3-mdiu-4, W3-mdiu-5, W3-mdiu-6, W3-mdiu-7"/>
  <criterion id="DTX3-AC2" cell_refs="W3-gkih-1, W3-gkih-2, W3-gkih-3, W3-gkih-4, W3-gkih-5, W3-gkih-6, W3-gkih-7, W3-mdiu-1, W3-mdiu-2, W3-mdiu-3, W3-mdiu-4, W3-mdiu-5, W3-mdiu-6, W3-mdiu-7"/>
  <criterion id="DTX3-AC3" cell_refs="W3-gkih-1, W3-gkih-4, W3-mdiu-1, W3-mdiu-4"/>
  <criterion id="DTX3-AC4" cell_refs="W3-gkih-4, W3-mdiu-4"/>
  <criterion id="DTX3-AC5" cell_refs="W3-gkih-2, W3-mdiu-2"/>
  <criterion id="DTX3-AC6" cell_refs="W3-gkih-2, W3-gkih-3, W3-mdiu-2, W3-mdiu-3"/>
  <criterion id="DTX3-AC7" cell_refs="W3-gkih-5, W3-mdiu-5"/>
  <criterion id="DTX3-AC8" cell_refs="W3-gkih-1, W3-mdiu-1"/>
  <instance_path>org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/NFRA_SUBSTRATECARDING.TO-W3-DTX3_PROOF_OF_SPEC.json</instance_path>

  <expected_criteria>DTX3-AC1,DTX3-AC2,DTX3-AC3,DTX3-AC4,DTX3-AC5,DTX3-AC6,DTX3-AC7,DTX3-AC8</expected_criteria>
  <alignment_denominators>criteria: 8. Cells: 14 of 14 owned by this executor, all covered. Unmapped 0; untraceable 0.</alignment_denominators>
</proof_of_spec>
**Issuer-owned mechanism cells (not yours):** `W3-m-1` · `W3-m-2` · `W3-m-3` · `W3-m-4` · `W3-m-5`
