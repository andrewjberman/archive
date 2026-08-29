# L3W1-CCX -- MEASUREMENTS TAKEN BEFORE THE v2 PIN

**This is NOT a shard and not a deliverable.** It is the working measurement record for
`NFRA_C3MATERIALIZE.TO-L3W1-CCX`, written so the numbers survive the session that produced them.
The deliverables are the two shards (`symbol_to_file.bridge.json`, `motif_to_portalsym.bridge.json`)
plus the proof-of-spec instance; when they land they carry these values with their own evidence
blocks and **this file is superseded by them**. Nothing here is certified and nothing here should be
cited as a row value.

**Executor** `0.8.0_AE_CloudComp~X` · **taken** 2026-08-29 00:1x-00:2xZ · **device-local**
**Held on:** the certified-v2 pin (issuer 79908). `bridge_kind` is a required shard field whose enum
the re-cut moves, so emitting shards before v2 would produce files my own committed schema refuses.

---

## 1. VIEW_PAIR (`L3W1-buvb-1`) -- MEASURED, CONTROLLED

Read from the L2 record's bytes at `64ae1ae879` via `git show` (not the working tree).

| quantity | value | note |
|---|---|---|
| `\|S\|` STRUCTURE entities | **19,482** | derived by this run; record's declared denominator 19,482 -- AGREE |
| `\|B\|` BEHAVIOR entities | **3,726** | derived by this run; record's declared denominator 3,726 -- AGREE |
| `\|S ^ B\|` raw id intersection | **0** | the expected value, and it discriminates (below) |
| duplicate ids within S / within B | 0 / 0 | |

**POSITIVE CONTROLS -- all three FIRE.** A zero from an instrument never shown finding anything is
not a measurement.

1. `S ^ S` = 19,482 (expect `|S|`) -- FIRES
2. `B ^ B` = 3,726 (expect `|B|`) -- FIRES
3. one real B id injected into S, re-run = exactly 1 -- FIRES
   (injected token: `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/NFRA_EPISTEMY.C10-PRECOND/WIRING_PLAN.md`)

**Why the zero is structural, not accidental:** 1,388 of 19,482 S ids start `arn:`; 0 of 3,726 B ids
do. 11,367 S ids contain `/` and 3,715 B ids do -- so the two spaces OVERLAP IN SHAPE and share no
member, which is exactly the case a shape-based heuristic would get wrong.

**What a false answer would look like:** a NON-ZERO would mean one string is both an ARN and a repo
path, so the likely cause would be a parse or truncation on one side, not a shared entity. A zero
produced by reading the WRONG KEY (`id` where the declared key is `entity_id`) is the silent-0 class
L1 recorded against itself (its mis-derivation #3, 6,161 ids read as 0); controls 1-3 exclude it
because they read the SAME key through the SAME accessor.

---

## 2. `symbol_to_file` -- MEASURED

Source: `org/modules/graph/tsgraph_spike/out/portal_full.graph.json` (**UNTRACKED**, device-local).

| quantity | value |
|---|---|
| nodes / edges | 11,232 / **16,397** |
| node classes / edge labels | 13 / 16 (both fully censused, not sampled) |
| `Module` nodes | 374 |
| **edges targeting a `Module`** | **0 of 16,397** |

**Corroborates L1's "declared by the store: NO -- 0 of 16,811 portal edges target a Module"** by a
different instrument: L1 reached it while declaring the grain; this run censused inbound edges per
dst class across all 13 classes.

**POSITIVE CONTROL -- and the first one was worthless.** The first attempt selected its control class
via `next(iter(nodes))`, which *was* the Module node, so the control tested the subject's own class
and returned 0. A control that can only return the subject's answer discriminates nothing. Re-run
against classes the probe is known to find:

| dst class | nodes | inbound edges |
|---|---|---|
| Field | 4,969 | **10,747** |
| TypeDecl | 807 | **2,238** |
| ReactComponent | 442 | **1,740** |
| ... | | |
| Hook / JSXElement / JSXRender / **Module** | | **0** |

9 of 13 classes return non-zero. Same accessor, same edge list, same `dst` key throughout.

⛔ **A SILENT-NULL WAS HIT AND CAUGHT.** The first pass read edge `type`; the declared key is
`label`. It returned `None` for all 16,397 edges -- L1's own mis-derivation #3 shape. It was caught
by the census disagreeing with itself, NOT by a control.

⛔ **VINTAGE / REPRODUCIBILITY FINDING (owner: L1's author).** 16,397 here vs L1's 16,811 at
`@baca7f07eb`, delta **414**. The file is **UNTRACKED** (`git ls-files` no match), so *neither*
figure is re-derivable from git at any pin, by this seat or by a certifier. The CONCLUSION is robust
to the delta -- 0 of 16,397 and 0 of 16,811 say the same thing -- but a row citing "16,811" cites a
number no instrument can reproduce. The shard will cite its own measured denominator with device and
date, and name L1's as a floor it did not reproduce.

### Row values determined (to be written into the shard with full evidence)

- **basis = `inferred`.** With 0 declared edges the roll-up is recoverable ONLY by parsing the symbol
  id's module prefix. The face's own definition lands exactly here; `measured` would be the defect it
  names.
- **cardinality_class = `UNMEASURED`, NOT `FUNCTION`.** The only available probe is that parse, which
  yields one parent per child BY CONSTRUCTION and cannot return >1 -- L1's disowned tautology (its
  mis-derivation #5). The committed schema REFUSES `FUNCTION` without
  `probe_can_return_multiple: true`, so the guard fires on its own author's subject.
- **declarability = `NAMED_GAP_STORE_OWNER`** (owner named on the shard): the store CAN declare this
  edge and does not -- a gap with an owner, not a wish.
- **endpoints:** PREPARED, `same_plane` HELD until the v2 pin (issuer interim; ruled false under
  Reading A but the value is written only at the re-cut pin).

---

## 3. `motif_to_portalsym` -- store-declared half MEASURED

Source: `infra/aws/globgrph/stitch_graph.json` (read-only).

| quantity | value | vs the face's carried floor |
|---|---|---|
| edges | **43,633** | -- |
| `CONTAINS` | **12,352** | reproduces EXACTLY |
| distinct `edge_type` values | **58** | face carried **57** -- did NOT reproduce |

The 58 count was censused with no null or empty member; the full list was printed, not sampled.
Independently reproduced by `3.0.0_SA_CVO~X`, and the stale 57 was found to propagate to all 8
`motif_to_portalsym` cells in the certified rectangle -- now inside the issuer's re-cut boundary,
which derives the census at build instead of carrying a typed number.

`CONTAINS` by `level`: `None` 10,786 · function 1,201 · file 133 · prefix 120 · object 112.

---

## 4. STATE AT THE TIME OF WRITING

- Schema `BRIDGE_ROW.schema.json` committed `@c13f23efde`, independently verified by the certifier.
- The schema's `bridge_kind` enum (copied from the pre-ruling rectangle) REFUSES every candidate
  re-cut value -- measured, surfaced, and the fix is a builder re-run at the v2 pin, not an edit.
- That re-run is PRE-VALIDATED against the dry re-cut in scratch: `bridge_kind` auto-reads
  `['BRIDGE_CROSS_PLANE', 'ROLLUP_CONTAINMENT']`, the five row enums stay identical, 12/12 controls
  pass, nothing typed. Not executed against the deliverable -- the issuer said not before v2.
- Awaiting: certifier re-certification of `rectangle.recut1.dry.json` `@c96ce17a1c` -> issuer names
  certified v2 -> schema re-run + both shards emitted in one act.
