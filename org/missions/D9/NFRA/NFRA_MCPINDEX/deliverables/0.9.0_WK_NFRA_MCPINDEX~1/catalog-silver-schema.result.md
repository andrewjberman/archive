# NFRA_MCPINDEX.TO-MX-c-2 -- catalog schema extended to silver datasets, one source file per entry

**Worker:** `0.9.0_WK_NFRA_MCPINDEX~1` | **Cell:** `MX-c-2` | **Round:** 1 | **Written:** 2026-09-21, UTC times below

**Read:** PRD `org/missions/D9/NFRA/NFRA_MCPINDEX/prd/NFRA_MCPINDEX_PRD.md` @b7dc80e2cc CONTRACT C1
(lines 197-217, printed at the bytes in-session); decomp `org/missions/D9/NFRA/NFRA_MCPINDEX/decompositions/NFRA_MCPINDEX_DECOMP.md`
@f506f63a8b s.3 (`MX-c-2` row + acceptance block), s.8 bounds, s.10.2, s.1 falsifier 2, s.11 finding 1.

## What was built

- `workflows/atom_decomposition/emit_catalog_v02.py` -- added `CATALOG_ENTRIES_DIR`,
  `ENTRY_REQUIRED_FIELDS` (the C1 schema, exactly 8 fields), `ENTRY_GRAIN_VALUES`,
  `ENTRY_FIRM_SCOPE_RULES`, `validate_entry()`, `load_catalog_entries()`; `main()` now reads
  `catalog_entries/*.yaml` once, refuses the whole emit (nothing written) if any entry file
  is schema-invalid, and otherwise writes an additive top-level `silver_datasets:` section
  (a list, or `silver_datasets: []` when the directory holds zero source files, as it does at
  this vintage). `channels:` (the 36 EMISSION_MAP rows, 15 channels) is untouched by
  construction -- the new key is a sibling, never nested under `channels:`, so
  `infra/aws/ec2/opal-gateway/app/graphql_plumbing/catalog_gate.py`'s `load_catalog()` (which
  only ever reads `cat.get("channels")`, read at :62 this session) cannot see it and needs no
  companion change (out of this cell's `<paths>` grant regardless).
- `workflows/atom_decomposition/validate_catalog_v02.py` -- added `validate_silver_entries()`
  (imports `validate_entry`/`load_catalog_entries` from the emitter, ONE schema definition,
  never two), run first in `main()` and REFUSING (rc 2) before any live S3 call if a
  `catalog_entries/*.yaml` file is invalid. Also fixed a pre-existing defect in `aws()`: it
  called bare `subprocess.run(["aws"] + args)`, which is not a Win32-executable name and
  raises `FileNotFoundError` under a native (non-bash) Python process on this device (CLAUDE.md
  Git section: "AWS via the `.tools/aws` shim ... never bare `aws`") -- resolved to
  `.tools/aws.cmd` by path, falling back to bare `aws` only where the shim is genuinely
  absent. This is the ONLY reason `AC5`'s live run was exercisable in this environment at all;
  measured before the fix: `FileNotFoundError` traceback, `[WinError 2]`.
- `workflows/atom_decomposition/battery_catalog_v02.py` -- UNCHANGED (0-line diff). It reads
  only `channels:`, is unaffected by the new sibling key, and already passes 41/41 (baseline
  measured before any edit in this cell, see AC5 below); nothing in this cell's criteria
  requires a battery case for a dataset that does not exist yet.
- `workflows/atom_decomposition/catalog_entries/` -- new directory; `README.md` documents the
  schema and the Rule 24 record (below is the deliverable copy, the authoritative one). Zero
  `*.yaml` source files ship in this round (decomp s.10.2/s.5: concrete silver datasets are a
  later tool cell's act, after `MX-c-4`/`MX-g-1`) -- the mechanism is what this cell proves,
  exercised live in `probes/mx_c_2.py AC3` via plant-then-restore.
- `workflows/atom_decomposition/tests/test_catalog_silver_entries.py` -- new, 18 `unittest`
  cases (`ValidateEntryTests`, `LoadCatalogEntriesTests`), run 2026-09-21T06:31Z, `OK` (18/18),
  instrument `py -3.12 -m unittest ... -v`. Exercised against synthetic fixtures / a
  `tempfile.TemporaryDirectory()`, never the real `catalog_entries/` tree.

## Per-criterion measurement (instrument, UTC time, denominator)

All eight run via `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~1/probes/mx_c_2.py`,
`cd <WS> && timeout 120 py -3.12 probes/mx_c_2.py AC<n>`, each printing its own denominator.

| id | instrument | UTC time (this write-up) | denominator | verdict |
|---|---|---|---|---|
| AC1 | `validate_entry()` exercised in-process, 8 fields individually dropped + 1 extra-field case + 1 fully-valid case | 2026-09-21T06:33Z | 8 of 8 C1 fields | PASS |
| AC2 | `CATALOG_ENTRIES_DIR` path resolution + `load_catalog_entries()` against a `tempfile.TemporaryDirectory()` (before/after one planted file) | 2026-09-21T06:34Z | 1 file planted, 1 entity read | PASS |
| AC3 | real subprocess `emit_catalog_v02.py` run against the REAL `catalog_entries/` dir with one planted (then broken, then removed) file; `validate_silver_entries()` called in-process for both arms; `CAT` restored and diffed byte-for-byte afterward | 2026-09-21T06:35Z | 1 planted entry -> 1 emitted row; 1 broken field -> 1 named refusal | PASS |
| AC4 | `git show 41da358d45:.../DATA_CATALOG.yaml` (this worker's cut-head baseline) vs the current emitted file, field-by-field | 2026-09-21T06:36Z | 36 of 36 rows, 15 of 15 channels, 0 field diffs (version + built_at_git_head excepted, named) | PASS |
| AC5 | `py -3.12 validate_catalog_v02.py` (live S3, bucket `opal-data-portal-v2`) + `py -3.12 battery_catalog_v02.py` | 2026-09-21T06:37Z | validate: 36 rows (26 concrete-ok, 9 family-ok, 1 family-empty pre-existing/unrelated); battery: 41/41 | PASS |
| AC6 | `len(bytes) - len(bytes.decode('utf-8'))` on the emitted file, plus a strict-ascii decode | 2026-09-21T06:37Z | delta 0 of 129,962 bytes | PASS |
| AC7 | filesystem walk (current) vs `git ls-tree -r --name-only 41da358d45` (before), both filtered to `*DATA_CATALOG*` / `*catalog*.yaml` basenames, over `infra/aws/ec2/opal-gateway` + `workflows/atom_decomposition` | 2026-09-21T06:38Z | 1 of 1 hit before, 1 of 1 hit after, 0 added, 0 removed | PASS |
| AC8 | this section (below) + `probes/mx_c_2.py AC8`'s independent word-boundary re-count over `emit_catalog_v02.py` | 2026-09-21T06:39Z | 3 of 3 declared `firm_scope_rule` values found, word-boundary | PASS |

Full per-run stdout for AC1-AC7 is reproducible by re-invoking the probe; not pasted verbatim
here beyond the table above (Rule 22 GRAIN/COVERAGE is satisfied by the probe's own printed
denominators at invocation time, which is what the acceptance line's `<expect>` regex grades).

**Pre-existing, unrelated:** `mp.15.json-mdpf-legacy` reads `FAMILY-EMPTY` in `AC5`'s validate
run (0 live keys under `json/mdpf/**`) -- this is the same superseded-legacy-tree state the
catalog's own `never_serve:` section already documents ("json/mdpf/** -- superseded legacy
tree"); unrelated to this cell's silver-entry mechanism and not touched by this cell's diff
(bound 17's sibling: a pre-existing state this cell's change does not create and is not this
cell's to fix).

## RULE 24 FOUR-POSTULATE RECORD -- the entry schema's value sets (`firm_scope_rule`, `never_sum_rules`, `freshness_field` kinds)

### (i) MECE over a declared domain

**`firm_scope_rule` -- 3 values, domain = PRD sec.10.8's sovereign firm-visibility axis**
("Opal users see ALL firms; a firm sees ONLY ITSELF", printed at
`org/missions/D9/NFRA/NFRA_MCPINDEX/prd/NFRA_MCPINDEX_PRD.md` and restated in the emitted
catalog's own header, `# FIRM VISIBILITY (sovereign, PRD sec.10.8)`). By subtraction from
"every way a live-queried dataset's result set can relate to the firm axis":

```
  every way a live query's RESULT SET can relate to the firm axis .......... (the domain)
  minus: carries NO firm dimension at all -> opal-internal-only .............. -1
  minus: carries a firm dimension, resolved PER asking firm -> firm-scoped ... -1
  minus: carries a firm dimension, but only servable AGGREGATED,
         no single firm may see it broken out -> all-firms-aggregate ........ -1
  --------------------------------------------------------------------------------
  remaining ................................................................... 0
```

Exhaustive by construction: a dataset's rows either omit the firm dimension entirely, carry
it and are scoped per-firm, or carry it but only as a cross-firm aggregate -- there is no
fourth relationship a result set can have to "which firm(s) can see this row" (a row cannot
be simultaneously per-firm-scoped and aggregate-only; the two are mutually exclusive by their
own definition, and "opal-internal-only" is exactly the complement of "carries a firm
dimension"). This mirrors the existing catalog's own precedent for `mp.11.non-model-assets`
(`firm: opal-internal, scope: all-firms-aggregate`) -- the third value is not new vocabulary,
it names a pattern the catalog already carries.

**`freshness_field` and `never_sum_rules` KINDS -- 2 kinds each, by construction.** A value is
either NAMED (a specific field/dotted-path, or a specific list of rule strings) or explicitly
declared ABSENT (`NONE -- <reason>`) -- there is no third state, because "unset" is refused by
`validate_entry` (an empty list or missing key is a schema error, never a silent absence).
This is the SAME vocabulary the existing catalog's condition-1 `VINTAGE_FIELD` mechanism
already uses (`emit_catalog_v02.py` -- "a prose pointer is never emitted again"); MX-c-2
extends it to the entry schema rather than inventing a second one.

**Word-boundary census (word-boundary regex, denominator printed):** `probes/mx_c_2.py AC8`
re-runs `re.findall(r"\bVALUE\b", text)` for each of the 3 declared `firm_scope_rule` values
over `emit_catalog_v02.py`'s own text, independently of this document's prose, and requires
every declared value to appear at least once (its own definition is the positive control).
Measured 2026-09-21T06:39Z: `{'opal-internal-only': 1, 'firm-scoped': 1, 'all-firms-aggregate': 1}`
-- denominator 3 of 3 declared values found, 0 undeclared variants (`per-scope`, `global`,
`per-firm`, `firm-only` etc. do not appear as `firm_scope_rule` tokens anywhere in the file;
`global` and `per-scope` ARE present in the file but exclusively as the pre-existing
platinum-row `firm`/`firm_resolution` vocabulary, a DIFFERENT field with its own already-
Rule-24'd value set -- KNOWN_FIRM_VALUES / FIRM_RESOLUTIONS, unmodified by this cell).

### (ii) SAME GRAIN

Every value in each of the three sets describes ONE dataset-entry's ONE property, at
authoring time (when the source `.yaml` file is written), never a per-row or per-query
runtime state. `firm_scope_rule` is not "which firm is asking now" (that is the Gateway's
`principal_class`/`principal_firm`, a runtime identity, already handled by
`catalog_gate.gate()` for the platinum rows and out of this cell's `<paths>`); it is a
declared PROPERTY of the dataset itself, fixed at authoring time, same grain as `grain` and
`freshness_field` beside it in the same file.

### (iii) INTENT COHERENCE

One axis: **let a future tool cell describe a silver dataset's firm-visibility, freshness and
never-sum obligations in ONE file, in the SAME vocabulary the platinum rows already use,
without inventing a second grammar.** No cell here widens scope: no real dataset is added, no
tool is registered, no grant changes, no Schwab file is touched, no S3 key is minted for a
silver row (Andrew: "silver queried live" -- there is no S3 key to mint).

### (iv) STATE COHERENCE -- what this remedy does NOT move

Matches decomp s.9's own STATE COHERENCE line for `MX-c-2` verbatim: **"`MX-c-2` extends the
schema and moves none of the 36 existing rows"** -- confirmed mechanically by `AC4` (0 field
diffs, denominator 36 of 36). Additionally: this remedy moves no `channels:` key, no
`catalog_gate.py` behavior (unread key), no `battery_catalog_v02.py` case (0-line diff), and
no deployed state (nothing here is applied or deployed; `CAT` is a repository file this cell
writes directly, per decomp bound 10 "the catalog is generated, never hand-edited").
