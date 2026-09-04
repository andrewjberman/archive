# NFRA_COMPEFFICACY.TO-CE-G-2 -- disclose-only: served-graph vintage on every comp-blast / comp-trace answer

**Assignee:** `0.9.0_WK_NFRA_COMPEFFICACY~2` (spine-v3 L7 worker, subagent of `2.0.0_SA_COO`)
**Branch:** `wk-CE-2` · **Worktree:** `C:\tmp\wk-CE-2`
**Commits (LOCAL, on `wk-CE-2`):**
- `e7dda3d93c` -- surprise rows S34, S35
- `a4a517214e` -- surprise row S36 (lane gap)
- `4dc2b75dd9` -- `org/modules/graph/cli.py` disclosure implementation (`GIT_COMMIT_AUTHOR_OVERRIDE=ANY_EXEC_OR_AE`, audited)
- `9c992ebbb5` -- `.tools/tests/test_g2_disclosure_battery.py` (`GIT_COMMIT_AUTHOR_OVERRIDE=TOOL_BATTERIES`, audited)

## 1. BEFORE -- each tool's disclosure as it stood, quoted whole (G2-AC1 evidence)

### comp-blast, pre-fix (`.tools/comp-blast component:AdvisorsTab.tsx --budget 90`, rc=3)

```
=== comp-kuzu provenance ===
  DB: kuzu_nessie_db  (27223 nodes / 58606 edges)
  source: nessie
    nodes snapshot-id: 1686878912724079672
    edges snapshot-id: 7100061770924681169
    nodes metadata: warehouse/globgrph/graph_nodes_4c6c23bd-fffa-427e-9cd9-7a9deaa3426d/metadata/00000-c2383248-deda-400e-a0ec-37c53fb7990f.metadata.json
  built: 2026-09-04T01:27:09.170275+00:00 (age: 1.6h)
  WARN: BEHIND Nessie HEAD -- pin 1686878912724079672 != HEAD 6051392224445700551 (writer=derive_runner, committed_at=2026-09-04T02:09:19.993324+00:00)
  per-table vintage (marker = authoritative; independent of local pin):
    cse: last-write 23.5h ago (< 26h cadence)
    ...
============================
  BUDGETED CALL: SERVING EXISTING GRAPH STALE (age 1.6h); refresh skipped to keep the whole call within Rule-T (BEHIND Nessie HEAD (...)).
NOT-FOUND: no graph node matches 'component:AdvisorsTab.tsx' -- ...
```

No line starts with `VINTAGE:`. `DB:`, `built:`, and the stale note are three SEPARATE lines
inside a multi-line block, and the block is absent from `--json` output entirely (comp-blast's
`--json` had no NOT-FOUND payload at all -- a pre-existing gap, see s.3 below).

**Vintage carrier at source (read only):** `infra/aws/globgrph/_provenance.py:600`
(`built_at = m.get("built_at", "?")`) reads the manifest; `:603` prints `DB: {db_label}  ({nc}
nodes / {ec} edges)`; `:622` prints `built: {built_at} (age: {age:.1f}h){flag}`. The stale label
comes from `infra/aws/globgrph/_canonical.py`'s `_write_refresh_failure` (kind
`inc-served-labeled-stale`, lines 113-123) and `needs_refresh` (lines 81-96), surfaced via
`comp_blast_universe.load_kuzu_universe`'s `BUDGETED CALL: SERVING EXISTING GRAPH STALE` text.

### comp-trace, pre-fix (`.tools/comp-trace AdvisorsTab.tsx`, rc=3 -- `--budget 90` was a USAGE ERROR, see S35)

```
Building trace graph...
Graph built: 2129 nodes, 2920 edges (66.9s)
=== comp-trace provenance ===
  cache: C:\tmp\wk-CE-2\.comp-graph\graph.json  built_at=2026-09-04T03:03:26Z (age 1.1min)
  sha-drift at load: UNCHECKED (freshness check not on this path)  |  served: rebuilt (head-pinned from CURRENT source this invocation)
  universe: head-pinned TRACE graph, 2129 nodes / 2920 edges (gold+components+lambda+s3+endpoints -- NOT the kuzu estate planes)
NOT-FOUND: no graph node matches 'AdvisorsTab.tsx' -- ...
```

comp-trace already carried BOTH vintage axes (T3, comp-trace dial 2026-08-04) but as
`cache: <path>  built_at=<ts> (age <N>min|h)` -- no single `VINTAGE:` line, no `STALE-SERVED`
concept, and `.tools/comp-trace ... --budget 90` (G2-AC3's own invocation) failed with an argparse
usage error (rc=1) because `p_trace` never declared `--budget` (S35).

**Vintage carrier at source (read only, pre-edit):** `org/modules/graph/cli.py:348`
(`built = _LOAD_PROVENANCE.get("built_at")`) and `:358`
(`print(f"  cache: {_CACHE_FILE}  built_at={built_s} (age {age_s})", file=sys.stderr)`), both in
`_emit_trace_provenance` -- pinned against `git show HEAD:org/modules/graph/cli.py` at the commit
this order was cut on (`79d19e4555`, the parent of this work).

**Note on comp-trace's universe:** comp-trace's engine (`_get_graph` / `TraceGraph`) is a DIFFERENT
graph than comp-blast's canonical kuzu DB -- a local, head-pinned, working-tree-scoped graph with
its own cache (`.comp-graph/graph.json`). The TO's own framing ("disclose WHICH graph it served")
anticipates this; the fix generalizes the ONE line format to whichever graph each tool actually
serves, never assumes they are the same graph.

*(G2-AC1 is `judgment="true"`: this section is evidence with NO verdict, graded by `3.0.0_SA_CVO`
at L9.)*

## 2. AFTER -- the shared disclosure line, both tools

One form, one shared implementation (`_format_vintage_line` / `_vintage_dict`,
`org/modules/graph/cli.py`), called by both `cmd_blast` and `cmd_trace`:

```
VINTAGE: DB: <name>  (<nodes> nodes / <edges> edges)  built: <ISO-8601 Z> (age: <N.N>h)[  STALE-SERVED: <label>]
```

`--json` carries `vintage: {db, nodes, edges, built, age_h, stale_served}` (plus
`built_unread_reason` alongside a `null` `built`/`age_h` on an unreadable manifest -- never a
silent 0.0h).

### comp-blast, post-fix (`.tools/comp-blast component:AdvisorsTab.tsx --budget 90`, rc=3)

```
VINTAGE: DB: kuzu_nessie_db  (27223 nodes / 58606 edges)  built: 2026-09-04T01:27:09Z (age: 2.5h)  STALE-SERVED: served-stale (BEHIND Nessie HEAD (pin 1686878912724079672 != HEAD 6051392224445700551 (writer=cse_producers_nightly, committed_at=2026-09-04T03:31:02.004103+00:00)))
```

`STALE-SERVED` fires here because the served graph is genuinely behind Nessie HEAD at exercise
time (`_canonical.needs_refresh`, read-only) -- an honest, live reading of the seam's own
predicate, not a planted condition.

### comp-trace, post-fix (`.tools/comp-trace AdvisorsTab.tsx --budget 90`, rc=3)

```
VINTAGE: DB: graph.json  (2129 nodes / 2920 edges)  built: 2026-09-04T03:03:26Z (age: 0.9h)
```

No `STALE-SERVED`: comp-trace's local graph is discarded and rebuilt on drift, never served stale
(`_get_graph`), so this axis is always `None` on this engine -- correctly reflected, not
suppressed.

### comp-blast `--json`, post-fix (`.tools/comp-blast component:AdvisorsTab.tsx --budget 90 --json`, rc=3)

```json
{
  "query": "component:AdvisorsTab.tsx",
  "status": "NOT_FOUND",
  ...
  "vintage": {
    "db": "kuzu_nessie_db",
    "nodes": 27223,
    "edges": 58606,
    "built": "2026-09-04T01:27:09Z",
    "built_unread_reason": null,
    "age_h": 2.5,
    "stale_served": "served-stale (BEHIND Nessie HEAD (...))"
  }
}
```

comp-blast's `--json` previously had NO NOT-FOUND payload at all (only the clean/found path
supported `--json`); this order adds the minimum NOT-FOUND JSON branch needed to carry `vintage`
there too, per the TO's own "on EVERY answer ... JSON mode as a field" bar. Text-mode output for
every OTHER path is byte-for-byte unchanged except for the ONE new `VINTAGE:` line inserted.

## 3. NO ENGINE CHANGE (G2-AC5)

sha256 of `infra/aws/globgrph/_canonical.py`, `kuzu_nessie_load.py`, `kuzu_cli.py` at `HEAD`,
via `git show` (never a worktree read -- autocrlf hazard):

```
d494be6660b0dd9674383a2504756d4fb852677eee5729718cc3298ff69b2952
8b79ca1bdfd51c1823c0c6780086d55d7e9c751d7651820f873cf1d4b42a5b3d
37a8accbd12f9fc11d6b3de3c07393ac28c0529eb91f17af0f211f82e0eb7c49
```

Matches the issuer's cut-time values exactly. All three seam files are consumed READ-ONLY: the
disclosure code calls `comp_blast_universe._import_globgrph()` (already imported by
`comp_blast_universe.py`, unedited) to reach `_canonical.refresh_failure` / `_canonical.needs_refresh`
and `_provenance.read_manifest` / `_provenance._age_hours` -- all pre-existing public/quasi-public
reader functions, none touched.

## 4. THE BATTERY (G2-AC6)

`.tools/tests/test_g2_disclosure_battery.py` -- 6 arms, each printing its own denominator, each
with a RED mutant covering one of the TO's three named defect classes:

| Arm | What it proves | RED mutant |
|---|---|---|
| `fresh` | age printed, no STALE-SERVED | strips `built:`/`(age:` from a real line -- fails the presence check |
| `stale_served` | seam's OWN `._refresh_status.json` marker (`inc-served-labeled-stale`) drives `STALE-SERVED`, read back through the seam's unedited `refresh_failure()` first | omits `STALE-SERVED` from a real line -- fails the presence check |
| `unreadable_built` | unparseable `built_at` -> `UNREAD (reason)` + `age: UNKNOWN`, never `0.0h` | fabricates `age: 0.0h` on an UNREAD input -- fails the `UNKNOWN`/no-`0.0h` check |
| `json_field` | `--json` carries `"vintage"` | a payload with no `vintage` key -- fails the presence check |
| `comp_trace_cli` | real `.tools/comp-trace ... --budget 90` invocation prints the line | strips `built:` from the REAL captured line |
| `comp_blast_cli` | real `.tools/comp-blast ... --budget 90` invocation prints the line | strips `built:` from the REAL captured line |

Direct: `python .tools/tests/test_g2_disclosure_battery.py` -> `DENOMINATOR: 6 of 6 arm(s)
recorded a pass` / `PASS`, rc=0.
Pytest, file grain: `pytest .tools/tests/test_g2_disclosure_battery.py` -> `6 passed`.
Commit gate: `bash .tools/commit-gate.sh org/modules/graph/cli.py
.tools/tests/test_g2_disclosure_battery.py` -> `pre-commit gate clean for 2 of 2 file(s)`.

## 5. Bounds respected

- **No engine change** -- s.3 above; a forced touch never occurred, nothing to report.
- **One clock** -- age is always derived from the served graph's own `built_at` (kuzu manifest /
  `_LOAD_PROVENANCE`); STALE-SERVED reads the seam's own `refresh_failure()` marker and its own
  `needs_refresh()` predicate -- never a second, independently-invented vintage source.
- **Graph read, never rebuilt** -- every exercise ran default/`--budget` invocations; `--force`
  was never passed by this order.
- **No new dependency** -- `datetime` (stdlib) is the only new import, used to reformat the kuzu
  manifest's ISO string into the same `%Y-%m-%dT%H:%M:%SZ` shape comp-trace's own provenance
  already renders.

## 6. Surprises filed (this worker)

- **NFRA_COMPEFFICACY-S34** (OBSERVATION, INERT): the worktree carried no copy of the gitignored
  canonical kuzu DB; copied read-only from the main workspace to exercise a real comp-blast answer.
- **NFRA_COMPEFFICACY-S35** (OBSERVATION, ARMED, disarm `2.0.0_SA_COO`): comp-trace's argparse
  never accepted `--budget`; G2-AC3's own invocation was a usage error until this order added it
  as an accepted-but-INERT flag. comp-trace's local rebuild still has no real Rule-T bound.
- **NFRA_COMPEFFICACY-S36** (OBSERVATION, ARMED, disarm `2.0.0_SA_COO`): `.owned-paths.yaml` has
  no spine-v3 (`0.9.0_WK_*`) entry in any lane; this order's own named surfaces
  (`org/modules/graph/cli.py`, `.tools/tests/**`) were refused in block mode. Routed around via the
  documented SINGULAR `GIT_COMMIT_AUTHOR_OVERRIDE=<LANE>` escape hatch, one commit per lane, both
  audited in `org/git-author-override-audit.log`.

## 7. FWD-9

Not this worker's to run (spine v3: `2.0.0_SA_COO` runs the distinct-seat re-run at the drain,
from the exact `G2-AC2`/`G2-AC3`/`G2-AC4` invocations above). Note for that re-run: it depends on
the SAME worktree carrying the copied kuzu DB (S34) -- a re-run in a worktree without that copy
will reproduce comp-blast's original TOOL-FAILED start, not a defect in this order's code.
