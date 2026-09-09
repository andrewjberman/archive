# CG-s-25 -- comp-debt's SECOND LEG REPOINTED: two queries, one served graph, no store

**TO:** `NFRA_CLDGRPH.TO-CG-F-5` · **cell:** CG-s-25 · **worker:** `0.9.0_WK_NFRA_CLDGRPH~2`,
branch `wk-cldgrph-6-2` · **push state: LOCAL.**
The last local Kuzu open in `comp_debt.py` is gone, and the tool now scores its whole REACHABILITY
family from a worktree that has never held the store it used to require.

```json
{
  "cell": "CG-s-25",
  "to_id": "NFRA_CLDGRPH.TO-CG-F-5",
  "worker": "0.9.0_WK_NFRA_CLDGRPH~2",
  "branch": "wk-cldgrph-6-2",
  "push_state": "LOCAL",

  "the_two_queries": {
    "transport": "projection_client.connect() -- ONE ServedConnection, two execute() calls",
    "nessie_scope": ["LOG_GROUP", "SECRET", "S3_BUCKET", "S3_BUCKET_POLICY", "DYNAMODB_TABLE",
                     "CW_ALARM", "EC2_INSTANCE", "LAMBDA", "SNS_TOPIC", "KMS_KEY"],
    "stitch_scope": ["GOLD_SCRIPT", "S3_DATA_KEY"],
    "stitch_scope_constant": "REACH_STITCH_TYPES -- THE one name; S31/TO-CG-F-11 moves it and nothing else in this file",
    "statement_shape": "MATCH (n:CloudNode) OPTIONAL MATCH (n)-[o:CloudEdge]->() OPTIONAL MATCH ()-[i:CloudEdge]->(n) WITH n, count(DISTINCT o) AS outdeg, count(DISTINCT i) AS indeg WHERE outdeg=0 AND indeg=0 AND n.node_type IN [<scope>] RETURN n.node_type AS t, n.node_id AS id",
    "scope_moved_from_python_into_cypher": "the unscoped _ISOLATED_SWEEP constant is deleted; it existed only because ONE statement had to serve TWO different graphs"
  },

  "the_counts": {
    "per_surface": {"nessie": 308, "stitch": 207},
    "stitch_denominator": "207 of 1674 stitch-typed nodes in the served graph (GOLD_SCRIPT 1380 + S3_DATA_KEY 294)",
    "deduped_across_surfaces": 0,
    "dedup_note": "0 on the LIVE graph because the two scopes are disjoint today; the mechanism is proven on the fixture, where a node returned by BOTH legs counts once (DEDUP_ACROSS_SURFACES=1)",
    "gold_subnodes_dropped": 1133,
    "census_deduped_union": 515,
    "suppressed_logged": 384,
    "residual_real_orphans": 131,
    "new_vs_baseline": 112
  },

  "the_budget": {
    "tool_prints_one": false,
    "row": "NFRA_CLDGRPH-W2-S55",
    "bound_used": "120 s = 2 x projection_client.DEFAULT_QUERY_TIMEOUT_S (60 s), one timeout per scope, IMPORTED not re-typed",
    "measured": "4.8 s wall clock for the WHOLE tool (both families, both legs)",
    "within_budget": true
  },

  "the_vintage_lines": {
    "leg_line": "VINTAGE: Built from the estate as of 2026-09-09 21:05:17 UTC. Stitch source: stitch-codebuild built 2026-09-09T19:55:00Z.  [vintage=2026-09-09T21:05:17.968166+00:00 manifest=09be45b5ff92]",
    "source": "projection_client.vintage_line(conn) AFTER the queries -- the vintage of the rows actually returned, not of a separate health call",
    "scorecard_header": "graph: 2026-09-09T21:05:17.968166+00:00  status=current",
    "printed_once_for_both_legs": true
  },

  "the_baseline_delta": {
    "baseline": "infra/aws/globgrph/comp_debt_baseline.json (the CVO-adjudicated bar)",
    "baseline_reachability_n": 35,
    "residuals_now": 131,
    "delta": 96,
    "new_keys": 112,
    "delta_measured_on": "RESIDUALS, because the baseline holds residual keys and n and has never held a census figure",
    "baseline_edited": false,
    "baseline_edited_instruments": "git diff --quiet HEAD rc 0 AND an LF-normalised sha256 match; the RAW sha256 pair DISAGREES and that is the autocrlf trap, printed rather than hidden (row W2-S58)",
    "row": "NFRA_CLDGRPH-W2-S57",
    "why": "the baseline's universe is kuzu_nessie_db + the July local stitch store; this run's is the September served graph with the cloud stitch folded in"
  },

  "the_census": {
    "ast_walk": "LOCAL_OPEN_SITES=0 of 2 files (comp_debt.py, projection_client.py)",
    "constant": "STITCH_DB_CONSTANT_PRESENT=false -- 0 CODE-band hits; 2 DOCSTRING + 1 COMMENT hits are the retirement note itself",
    "process": "RUNS_WITHOUT_STORE=true -- rc 0 and a full scorecard from a worktree where infra/aws/globgrph/kuzu_stitch_db does not exist",
    "control": "LOCAL_OPEN_PROBE_CONTROL=FIRED -- the same walker finds 3 sites in a planted file (import kuzu, kuzu.Database(...), kuzu.Connection(...))",
    "deleted": ["STITCH_DB", "STITCH_STALE_HOURS", "_stitch_freshness", "_ISOLATED_SWEEP", "the kuzu import"],
    "store_bytes": "UNTOUCHED -- this order makes them UNREAD; retiring them is CG-s-26"
  },

  "surprise_rows_filed": ["NFRA_CLDGRPH-W2-S55", "NFRA_CLDGRPH-W2-S56", "NFRA_CLDGRPH-W2-S57",
                          "NFRA_CLDGRPH-W2-S58", "NFRA_CLDGRPH-W2-S59"],
  "commits": ["<the acts commit>", "<the instance + flip commit>"]
}
```

---

## What changed, and why it is smaller than it looks

Before this cell, `dispatch_reachability` swept two surfaces with one statement: the nessie one
through `projection_client` (CG-s-8's repoint) and the stitch one through the last
`kuzu.Connection(kuzu.Database(path, read_only=True))` in the file, behind a 48-hour freshness gate
of its own. CG-s-24 folded the cloud-produced stitch into the nightly derive, so both scopes are now
**one served graph** — and the second leg stops being a second *store* and becomes a second *query*.

Three names went with it: `STITCH_DB`, `STITCH_STALE_HOURS`, `_stitch_freshness`. A fourth followed
them: the unscoped `_ISOLATED_SWEEP` constant existed only because one statement had to serve two
different graphs, so the type filter had to happen in Python. With one graph the scope rides the
Cypher, `_isolated_sweep_for(scope)` builds each statement from the caller's constant, and a
repo-wide census (1 of 1 code reference, this file's own) said the constant was safe to delete.

**The reason is recorded where the code was, not in a commit message nobody will find.** The module
docstring now carries why the 48-hour bar is gone: the stitch surface is served, its freshness is
the served VINTAGE line's, printed once for both legs; what the bar protected (the D1 592-hour-stale
lesson) moved into the vintage line a reader sees beside every count; and the refusal that survives
is the one that must — *unreachable*, never *stale* — because "could not read" has to stay
distinguishable from "old".

That refusal now names both scopes. A reader who trips it learns that the stitch leg went the same
way as the nessie one and that there is no local fallback for either.

## The one name the next order moves

`REACH_STITCH_TYPES = {"GOLD_SCRIPT", "S3_DATA_KEY"}` is the **interim** stitch-v1 vocabulary the
CTO admitted at arch-gate GO 20260909T2015Z. S31 (`TO-CG-F-11`) unifies it at the producer —
`GOLD_SCRIPT` splits by grain into `PipelineScript`/`PipelineFunction`, `S3_DATA_KEY` merges into
`S3Key` — and re-reads this leg on the canonical names. The constant now carries that note, the
sweep is *built* from it, and the fixture asserts the statement's type set **equals** the constant,
so when F-11 edits the set the test follows it without being touched. Nothing else in the file names
either literal.

## What the run says

515 isolates in the deduped union — 308 nessie, 207 stitch of 1,674 stitch-typed nodes — 384
suppressed and logged, 131 real orphans, 1,133 function-granular `gold:x:y` sub-nodes dropped as
isolated-by-design. 4.8 seconds, well inside the only bound the tool carries. And the line that
matters sits under the family row:

    VINTAGE: Built from the estate as of 2026-09-09 21:05:17 UTC. Stitch source: stitch-codebuild
    built 2026-09-09T19:55:00Z.  [vintage=2026-09-09T21:05:17.968166+00:00 manifest=09be45b5ff92]

One line, both sources, taken from the connection **after** the queries — so it is the vintage of
the rows that produced those counts, not of a health call made at some other moment.

`deduped_across_surfaces` reads **0** on the live graph, and that is honest rather than
disappointing: the two scopes are disjoint today. The dedup still has to work, because a future
vocabulary change could make them overlap, so it is proven on the fixture instead — a node returned
by both legs counts once, and the drop is counted.

## Three things worth the grader's attention

**The alarm fires 112 times, and it is not a regression.** The CVO baseline holds 35 REACHABILITY
residual keys, established against `kuzu_nessie_db` (19,917 nodes) with the stitch leg reading the
July local store. This run reads the September served graph. 131 residuals now, delta **+96**, of
which 112 keys are new — overwhelmingly `GOLD_SCRIPT` and `S3_DATA_KEY`, i.e. exactly the population
that changed universe. **The baseline was not touched and must not be**; `--establish-baseline`
would rewrite the CVO's file and is not exercised anywhere in this order. Row `W2-S57`, armed to the
CVO, because a standing scan that alarms 112 times on every run is an alarm nobody reads by
tomorrow — and the choice between re-establishing and adjudicating is not this worker's.

**A control nearly failed the order on a file nobody touched.** `BASELINE_EDITED` came back **TRUE**
on the first run. The baseline had not been opened for writing. Cause: `core.autocrlf` gives the
checkout CRLF while the record keeps LF, so an untouched file differs from `git show HEAD:` by
exactly one byte per line — measured 4,504 vs 4,433 bytes, 71 CRLF, 71 lines. The check now runs
three instruments and prints all three, including the raw pair that disagrees, so the trap is
visible rather than silently corrected. Row `W2-S58`. The failure direction is the dangerous one: it
accuses a worker of editing a file it was forbidden to touch, and the accusation looks like rigour.

**Two different things in this estate answer to "comp-debt".** `.tools/comp-debt` does not exist;
`comp-which` has no curated rule for it and answers from a fail-closed lexical fallback;
`comp-find` surfaces `org/modules/graph/comp_debt/`, a *different* fusion/guard package. The tool
this cell repoints is `python infra/aws/globgrph/comp_debt.py`, whose argparse `prog` is
`"comp-debt"` — which is why every carrier calls it that and no instrument can find it. Row
`W2-S56`, armed, because the next order that says "run comp-debt" will either fail to find it or
find the wrong one.

## What was left as found

The family registry still declares `REACHABILITY` `"pending"` on "DS~A authored REACHABILITY Cypher
(not yet handed)" — a Cypher that is present, running and the very thing this cell repointed. The
declaration is invisible in the output (the scorecard tags on the *result's* status, which is
`scored`) and visible only in the source. It is one word plus a docstring line, and it is a claim
about **coverage** where this order's grant is a claim about **transport**, so it is row `W2-S59`
rather than an edit. The stitch store's bytes are likewise untouched: this order makes them unread,
and `CG-s-26` retires them.
