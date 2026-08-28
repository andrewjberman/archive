# TASK ORDER — COX3 · NFRA_SUBSTRATECARDING WAVE 3 · MATERIALIZER CARDING

<status>complete -- 2026-08-28 13:0xZ (issuer-flipped on 3.0.0_SA_CVO~X VERIFIED PASS @707b9dc9cd, adjudication D11-T30-1)</status>

**to:** `0.7.0_AE_CloudOps~X` · **issuer:** `2.0.0_SA_COO~X` · **certifier:** `3.0.0_SA_CVO~X`
**scope:** 4 subjects / 28 cells · **contract:** `org/standards/SUBSTRATE_CARD.v2.schema.json`

✅ **DECOMP CERTIFIED?** NOT YET — cert is `3.0.0_SA_CVO~X`'s and runs on the cut packet. The
pipeline's own escape valve applies: a DECOMP-INVALIDATING verdict is the issuer's act to
re-decomp and re-issue. **Do not hold on it.**

<decomp_ref>
workflows/atom_decomposition/runs/nfra-substratecarding-w3/DECOMP.md @e48a7466ba

cells:
W3-aonv-1 W3-aonv-2 W3-aonv-3 W3-aonv-4 W3-aonv-5 W3-aonv-6 W3-aonv-7 W3-cayu-1 W3-cayu-2 W3-cayu-3
W3-cayu-4 W3-cayu-5 W3-cayu-6 W3-cayu-7 W3-nhvy-1 W3-nhvy-2 W3-nhvy-3 W3-nhvy-4 W3-nhvy-5 W3-nhvy-6
W3-nhvy-7 W3-xpxc-1 W3-xpxc-2 W3-xpxc-3 W3-xpxc-4 W3-xpxc-5 W3-xpxc-6 W3-xpxc-7
</decomp_ref>

---

## AUTHORITY

Andrew-direct 2026-08-27, verbatim: *"everything runs under D11, dont get concerned about the
title nor are you allowed to invent gates without my explicit approval"* and *"go surgical mode
here, pivot, we need to find the materializers that actualy matter"*.

## YOUR SUBJECTS

| subject | writer class | write evidence | paths measured |
|---|---|---|---|
| `infra/aws/globgrph/cse_store.py :: PATH A -- append` | CLASS_3 | :577 --ingest JSONL_URI -> :602 ingest_jsonl -> :481 append_cses -> :386 table.append(pa_table). pyiceberg append, ONE Nessie commit, append-only. --d | 1 |
| `infra/aws/globgrph/cse_store.py :: PATH B -- drop` | DESTRUCTIVE | :579 --drop -> :594-596 drop_cse_table(catalog, args.table); return 0 -> :353 catalog.drop_table((NAMESPACE, table)). ⛔ DESTRUCTIVE, NOT an append, an | 1 |
| `infra/aws/globgrph/resource_summaries_store.py` | CLASS_3 | :349 --table NO choices=; :202 create_table creates whatever name it is handed; NAMESPACE=globgrph | **UNMEASURED — yours to resolve** |
| `infra/aws/globgrph/snap_store.py` | CLASS_2 | append; :79 SURFACES 4 top-level keys (AST-measured); :415 choices=sorted(SURFACES) | **UNMEASURED — yours to resolve** |

⛔ **THE SUBJECT GRAIN IS (FILE, WRITE PATH).** `derive_runner.py` is split because it has two
write paths differing in mechanism, bound AND authority. **If YOUR subject turns out to have more**
**than one write path, that is a BLOCKING surprise — say so; do not card them as one.** Path
multiplicity is measured for exactly one subject in this wave and assumed for none.

## ACCEPTANCE CRITERIA

| id | criterion |
|---|---|
| **COX3-AC1** | 4 cards exist and all VALIDATE against the v2 contract. Every row carries `basis` + `evidence` + `owner`. |
| **COX3-AC2** | `as_of` carries ONE wave pin: `commit_ish` and `graph_vintage` byte-identical across your cards. `carded_utc` is an HONEST clock read at a DECLARED grain (per-card or per-batch — **state which**), never estimated, never copied. |
| **COX3-AC3** | **WHERE IS THE TABLE NAME BOUND** — every card states CLASS 1 / 2 / 3 with **the line that binds it**, and whether the bound set is **ENUMERABLE**. A class without a line number is not an answer. |
| **COX3-AC4** | **WHAT IT WRITES** — a resolvable path or table name, never a description. ⛔ A card that says X is a materializer **without naming WHICH artifact is unfalsifiable** (1.0.0_SA_CTO~X's rule, six arrivals tonight). |
| **COX3-AC5** | **TRIGGER** — plane (`events` / `scheduler` / `event-driven` / `none-found`) **plus BASIS**. ⛔ An ECS rule target resolves to a CLUSTER, not a script: any "X is triggered by Y" is **INFERRED** unless read from the task definition's container command. Mark it. |
| **COX3-AC6** | **RULE 26** device/apply owner, and **RULE 25** dormancy (≥90d stale = dormant absent a declared exception). Rule 26 is **NOT a class constant** — measured non-uniform in wave 2. |
| **COX3-AC7** | **DISCOVERABILITY IS NOT COVERAGE.** No card asserts completeness of the writer population. If your subject can write tables it does not name, say so and say the bound is **UNBOUNDED**. |
| **COX3-AC8** | **QUALIFY-DO-NOT-FIX.** Zero commits by this lane touching a module it cards. The Class-3 remedy (`choices=`, already written at `snap_store.py:415`) is **NAMED, NOT APPLIED**. |

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
  <criterion id="COX3-AC1" cell_refs="W3-aonv-1, W3-aonv-2, W3-aonv-3, W3-aonv-4, W3-aonv-5, W3-aonv-6, W3-aonv-7, W3-cayu-1, W3-cayu-2, W3-cayu-3, W3-cayu-4, W3-cayu-5, W3-cayu-6, W3-cayu-7, W3-nhvy-1, W3-nhvy-2, W3-nhvy-3, W3-nhvy-4, W3-nhvy-5, W3-nhvy-6, W3-nhvy-7, W3-xpxc-1, W3-xpxc-2, W3-xpxc-3, W3-xpxc-4, W3-xpxc-5, W3-xpxc-6, W3-xpxc-7"/>
  <criterion id="COX3-AC2" cell_refs="W3-aonv-1, W3-aonv-2, W3-aonv-3, W3-aonv-4, W3-aonv-5, W3-aonv-6, W3-aonv-7, W3-cayu-1, W3-cayu-2, W3-cayu-3, W3-cayu-4, W3-cayu-5, W3-cayu-6, W3-cayu-7, W3-nhvy-1, W3-nhvy-2, W3-nhvy-3, W3-nhvy-4, W3-nhvy-5, W3-nhvy-6, W3-nhvy-7, W3-xpxc-1, W3-xpxc-2, W3-xpxc-3, W3-xpxc-4, W3-xpxc-5, W3-xpxc-6, W3-xpxc-7"/>
  <criterion id="COX3-AC3" cell_refs="W3-aonv-1, W3-aonv-4, W3-cayu-1, W3-cayu-4, W3-nhvy-1, W3-nhvy-4, W3-xpxc-1, W3-xpxc-4"/>
  <criterion id="COX3-AC4" cell_refs="W3-aonv-4, W3-cayu-4, W3-nhvy-4, W3-xpxc-4"/>
  <criterion id="COX3-AC5" cell_refs="W3-aonv-2, W3-cayu-2, W3-nhvy-2, W3-xpxc-2"/>
  <criterion id="COX3-AC6" cell_refs="W3-aonv-2, W3-aonv-3, W3-cayu-2, W3-cayu-3, W3-nhvy-2, W3-nhvy-3, W3-xpxc-2, W3-xpxc-3"/>
  <criterion id="COX3-AC7" cell_refs="W3-aonv-5, W3-cayu-5, W3-nhvy-5, W3-xpxc-5"/>
  <criterion id="COX3-AC8" cell_refs="W3-aonv-1, W3-cayu-1, W3-nhvy-1, W3-xpxc-1"/>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/NFRA_SUBSTRATECARDING.TO-W3-COX3_PROOF_OF_SPEC.json</instance_path>

  <expected_criteria>COX3-AC1,COX3-AC2,COX3-AC3,COX3-AC4,COX3-AC5,COX3-AC6,COX3-AC7,COX3-AC8</expected_criteria>
  <alignment_denominators>criteria: 8. Cells: 28 of 28 owned by this executor, all covered. Unmapped 0; untraceable 0.</alignment_denominators>
</proof_of_spec>
**Issuer-owned mechanism cells (not yours):** `W3-m-1` · `W3-m-2` · `W3-m-3` · `W3-m-4` · `W3-m-5`
