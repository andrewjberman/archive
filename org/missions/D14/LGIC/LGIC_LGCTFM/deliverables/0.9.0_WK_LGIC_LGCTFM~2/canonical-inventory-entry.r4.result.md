# LT-m-1 (round 4) -- the canonical inventory entry: RESULT

**Cell** `LGIC_LGCTFM.TO-LT-m-1-r4` | **worker** `0.9.0_WK_LGIC_LGCTFM~2` | **branch** `wk-lgic-lgctfm-4-2`
| **artifact commit** `faf5de736845d9c47cd7fb875cbacfef1f90b973` (LOCAL, never pushed)

## THE ORDER IS NOT MET AND STAYS OPEN

| criterion | verdict | deciding line |
|---|---|---|
| `M1R4-AC1` | **FAIL** | `status 'canonical' is not an active one` -> `VERDICT: FAIL-M1-ENTRY` |
| `M1R4-AC2` | **PASS** | `pre-existing entries digest 697f4e9d80df (want 697f4e9d80df); entry count 129 (want 129)` -> `VERDICT: PASS-M1-UNTOUCHED` |
| `M1R4-AC3` | **FAIL** (named invocation) / the same record reads the expected token under the issuer's repair | `VERDICT: FAIL-R4-STALE-PROOFS` in-tree; `VERDICT: PASS-R4-STALE-PROOFS` at `1df2481ca0` |
| `M1R4-AC4` | RECORDED, no verdict | JUDGMENT -- `3.0.0_SA_CVO` at L9 |

`proof-of-spec-check` reads **VALID (rc=0)**; a valid instance is not a met order.

## WHAT WAS BUILT

ONE entry, `cloud.inventory.subject_composition`, added to `org/modules/graph/graph-call-manifest.yaml`
between `cloud.lookup.nodes_by_type` (its nearest neighbour) and `cloud.reachability.transitive` (the
relations half of the same comp-which question), carrying the 11-key shape plus `notes`:

- `tool: comp-find`, `mode: query`, `layer: cloud`
- `canonical_call: comp-find --corpus aws '<name-or-arn pattern>' [NODE_TYPE ...] [--all | --page N] [--budget N]`
- `anti_pattern` carries R-81's four refusals with their measured reasons (comp-estate's parked
  generated file, comp-routes' zero AWS calls, the comp-aws derive deprecated for agent use, and
  comp-iam's `gaps`/`roles`/`services`/`stats` whose population is `lambda-source-map.json`)
- `status: canonical`

**Manifest before -> after:** entries **128 -> 129**; `cloud.inventory.*` ids **0 -> 1**; pre-existing
digest over sorted `(id, sha1(canonical_call)[:12])` pairs **697f4e9d80df -> 697f4e9d80df (unchanged)**;
`tools_index` 78 (untouched); `contract` and `retired_aliases` untouched; file non-ASCII character
count **30 -> 30**; CRLF preserved.

**The call was exercised before it was declared** (read-only): `comp-find --corpus aws '49financial'
--limit 5` -> 8 hits across **2590** aws nodes, `VINTAGE` built 2026-09-19 00:55:44 UTC (stitch source
2026-09-18T03:01:14Z, manifest `1ba8ff79d94b`), drift banding incl. `LIVE-no-DECLARED 341`, `WITHIN
BUDGET` 7.19 s of 90 s.

## WHY `status: canonical`, WHICH IS WHY AC1 FAILS

`core_entry` requires `status` in `(active|current|live)`. The manifest's own per-entry schema (`:29`)
admits `canonical | deprecated | planned | retired`; **125 of its 128 pre-existing entries carry
`canonical`** (retired 2, absent 1); and `NFRA_GRAPHS` s.7 AC1 -- the bar R-81 quotes to *justify* this
entry -- reads *"exactly one **canonical** entry per distinct graph use-case"*. The two token sets do
not intersect, so no entry that is correct for the file can satisfy the arm.

Discriminator, run against the repaired grading core on the real manifest dict with **only** the status
value varied: `canonical` FAIL, `live` PASS, `active` PASS, `current` PASS, `retired` FAIL, `planned`
FAIL -- and in every PASS row no other clause failed. Positive control: the same dict with the entry
removed -> FAIL. Nothing mechanical forces either choice (`comp-which:1585`/`:1609` and
`manifest_check_cli.py:368` special-case only `deprecated`), so the manifest's own vocabulary is the
only tiebreaker -- and typing `live` into a shared estate surface to green my own arm is the move
`LGIC_LGCTFM-W2-S35` refuses. **The remedy is one token in a fixed input this order does not grant.**

## ROWS FILED (3)

| id | class | hazard | what |
|---|---|---|---|
| `LGIC_LGCTFM-W2-S35` | BLOCKING | ARMED, `2.0.0_SA_COO~G` | `m1-entry`'s status token set cannot be satisfied by an entry correct for the manifest |
| `LGIC_LGCTFM-W2-S36` | OBSERVATION | ARMED, `2.0.0_SA_COO~G` | the issuer's mid-round repair (`1df2481ca0`) cannot reach a worker's branch, and the arm it repairs measures that branch; the counted-commit figure is tree-dependent (1 here, 2 merged) |
| `LGIC_LGCTFM-W2-S37` | OBSERVATION | ARMED, `2.0.0_SA_COO~G` | the rule-bank two-phase override is undischargeable by a worker: the discharge writes `infra/system/`, which no worker grant on this round names |

## WHAT THE ISSUER OWES TO CLOSE THIS CELL

1. One token in `check_lt_r4.py` `core_entry` (accept `canonical`, or read the clause from
   `R4_BASE.json` so the fixed input and the graded surface cannot diverge again), then re-run
   `m1-entry`.
2. Re-run `r4-stale-proofs` on the merged tree, where the repair is present -- and re-measure
   `fixed_input_commits_since_cut` there (it reads **2**, not the **1** this branch can see).
3. The `comp-system` recompile that discharges this commit's audited
   `STRUCTURAL-TWOPHASE/rule-bank` override, after the drain.

Nothing live moved. No push, no merge, no rebase. Files touched: the manifest, the channel, this
folder, and nothing else.
