# CG-x-1 -- FWD-1 EXERCISED: a never-compiled seat asked one wiring question and was answered

**TO** `NFRA_CLDGRPH.TO-CG-D-5` · **cell** `CG-x-1` · **PRD** `NFRA_CLDGRPH_PRD.md` v0.4 @`25c66d3358` acceptance 1 (FWD-1)
**Asker** `0.9.0_WK_NFRA_CLDGRPH~3` · **worktree** `wk-NFRA_CLDGRPH-3` @`4e30d6b635` (LOCAL) · **written** 2026-09-04T18:0xZ

The asker is a spine-v3 worker subagent spawned this hour into a worktree freshly created from CLOUD. It had run
no graph tool before the ask below, holds no local graph database, and ran no build, refresh or engine at any
point. It read `comp-kuzu --schema` for the dialect, then asked once.

```json
{
  "asker": "0.9.0_WK_NFRA_CLDGRPH~3",
  "question": "Which Lambda functions does the bd data bucket trigger?",
  "cypher": "MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE e.edge_type='TRIGGERS' AND a.node_id CONTAINS 'opal-data-bd' RETURN a.node_id AS bucket, b.node_id AS target ORDER BY target",
  "answer_rows": [
    {"bucket": "arn:aws:s3:::opal-data-bd", "target": "arn:aws:lambda:us-east-1:313476888478:function:bd-allocation-processor"},
    {"bucket": "arn:aws:s3:::opal-data-bd", "target": "arn:aws:lambda:us-east-1:313476888478:function:bd-gold-trigger"},
    {"bucket": "arn:aws:s3:::opal-data-bd", "target": "arn:aws:lambda:us-east-1:313476888478:function:bd-silver-merge"}
  ],
  "answer_row_count": 3,
  "vintage_line": "VINTAGE: Built from the estate as of 2026-09-04 16:38:39 UTC.  [vintage=2026-09-04T16:38:39.485910+00:00 manifest=c3ba0330e306 prefix=projection/2026-09-04T16:38:39.485910+00:00/]",
  "time_to_answer_s": 7.802,
  "time_to_answer_s_all_runs": [7.802, 8.497, 7.668],
  "procs_before": 0,
  "procs_during_max": 0,
  "procs_after": 0,
  "client_source_engine_hits": "1 hit over 169 lines / 8 sections, band DOCSTRING (kuzu_cli.py:14, the sentence that DOCUMENTS the absence); CODE=0, COMMENT=0, DEF=0",
  "local_db_present": false
}
```

## 1. The premise: this asker holds no graph and has no graph history

| # | read | output | rc |
|---|---|---|---|
| 1 | `ls -d infra/aws/globgrph/kuzu_nessie_db 2>&1` | `ls: cannot access 'infra/aws/globgrph/kuzu_nessie_db': No such file or directory` | **2** |
| 2 | `python .tools/comp-find '0.9.0_WK_NFRA_CLDGRPH~3' org/mcp/agent_telemetry --limit 3` | `DENOMINATOR: 0 hit(s) across 0 file(s) scanned in scope [corpus=all]` | 0 |
| 3 | `python .tools/comp-read infra/aws/globgrph/kuzu_cli.py --enumerate 'ensure_fresh\|kuzu_nessie_load\|import kuzu\|--mode' --limit 3` | `ENUMERATE-END: 1 hit(s) \| 1 whole \| 0 sub \| DOCSTRING=1 \| COMMENT=0 \| DEF=0 \| CODE=0` | 0 |

**Read 2 is NO MEASUREMENT, not a zero, and is recorded as such** (row `NFRA_CLDGRPH-W3-S2`). `0 hit(s) across
0 file(s)` is the out-of-corpus signature: `org/mcp/agent_telemetry` does not exist in this worktree (`ls` rc=2;
`comp-find --hidden org/mcp/agent_telemetry` -> `ERROR: 1 path(s) do not exist ... A count over a path that is
not there is not a zero -- it is NO MEASUREMENT`), because the telemetry directory is untracked runtime state
that never enters a fresh worktree (`git ls-files org/mcp/agent_telemetry` -> empty). The claim it was cited for
survives on other evidence: read 1, and the fact that this serial was minted for this spawn.

**Read 3 does not match the expectation `D5-AC4` carries** (`ENUMERATE: 0 hit\(s\)`) and is recorded FAIL against
it (row `NFRA_CLDGRPH-W3-S1`). What the output does say about the world is unambiguous and is the substance the
criterion names: the one hit is in the DOCSTRING band -- `kuzu_cli.py:14`, `WHAT IS GONE AND WHY (FWD-6): there
is no --db-path, no --mode, no --force/--refresh/--fresh` -- prose documenting the absence, and **CODE=0**.

## 2. The instrument, before the answer is believed

The question carries TWO string literals, and this exact query has already paid for a quoting trap once in this
project (`NFRA_CLDGRPH-W1-S10`: a `'\''` idiom inside a double-quoted string delivered `e.edge_type='"TRIGGERS"'`
-- valid, unmatchable, **0 rows at a correct vintage with no error**). Two controls, before and beside the ask:

- **The statement is echoed as sent.** `ask.sh` builds the Cypher ONCE in a double-quoted variable and passes
  that same variable as one argv element; the `CYPHER_AS_SENT=` line in the transcript is that variable printed.
- **The issuer's control, same client, this hour:** `comp-kuzu "MATCH (n:CloudNode) WHERE n.node_type='LAMBDA'
  RETURN count(n)"` -> `203`, matching the issuer's measurement exactly. That control carries a string literal
  too, so a literal reaching the server intact is demonstrated, not assumed.
- The answer is **non-zero (3 rows)** and is exactly the shape the issuer predicted (bd-allocation-processor,
  bd-gold-trigger, bd-silver-merge), so the trap did not fire here. Had the answer been 0 rows it would have been
  recorded as a finding, not retried.

## 3. That no build ran -- two witnesses, one of them independent of the client

- **(a) The process table**, sampled BEFORE, DURING (a spin loop over the query's whole lifetime, no sleep) and
  AFTER every run: `PROCS_BEFORE=0`, `PROCS_DURING_MAX=0`, `PROCS_AFTER=0` for pattern
  `kuzu_nessie_load|kuzu_incremental_refresh|derive_runner`, with the `grep -v grep` discipline. The counter is
  not a dead arm: the same pipeline over `bash` returned 39/32/37 on the same calls, and `ps -ef` itself carried
  45/34/42 rows. **COVERAGE QUALIFIER:** `ps -ef` in Git Bash enumerates the MSYS process table; a build launched
  from a native Windows shell by another seat would not appear in it. This witness bounds THIS asker's own acts,
  which is what the criterion asks; witness (b) does not depend on it at all.
- **(b) The client cannot run an engine.** `kuzu_cli.py` is 169 lines with CODE-band hits of
  `ensure_fresh|kuzu_nessie_load|import kuzu|--mode` = **0**; `comp-kuzu` shells that one file and nothing else.
- **(c) A third witness, unplanned:** the vintage line is byte-identical across all four calls
  (`manifest=c3ba0330e306`, `2026-09-04 16:38:39 UTC`). A build between the asks would have moved the manifest.
  The asker consumed a projection built 25 minutes before it existed.

## 4. Time to answer

`7.802 s` on first contact; `8.497 s` and `7.668 s` on the two later runs (mean 7.99 s, spread 0.83 s). Recorded,
not graded: `D5-AC5` is a JUDGMENT criterion and belongs to `3.0.0_SA_CVO` at L9. The comparators the TO names are
`comp-find --corpus aws` at 11.55 s and `comp-read` under 1 s. Every second of this is the round trip to the
served projection; nothing local was read, compiled or built.

## 5. Runs (why there is more than one)

`ask.sh` ran 4 times: run 1 (the record of first contact), run 2 (labelled: variance + a repair, below), and once
each under the `D5-AC2` and `D5-AC3` acceptance invocations, which each invoke it by construction. The ask is a
read; every run returned the same 3 rows at the same manifest.

**Run 1 printed `ANSWER_ROW_COUNT=0` beside a true 3-row answer** -- my own defect, not the graph's: the counter
matched `^opal-data-bd` while every row begins `arn:aws:s3:::opal-data-bd`. It is repaired in the committed
`ask.sh` to read the CLIENT'S OWN `(N rows)` denominator rather than a regex of mine over the client's table, and
run 1 is left in the transcript below with the false zero visible rather than re-run away. A wrong arm and a dead
arm read identically; the client states its own count.

## 6. Raw transcript

### Run 1 -- first contact (`ANSWER_ROW_COUNT=0` is the counter defect of s.5, not the answer)

```
ASKER=0.9.0_WK_NFRA_CLDGRPH~3
QUESTION=Which Lambda functions does the bd data bucket trigger?
CYPHER_AS_SENT=MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE e.edge_type='TRIGGERS' AND a.node_id CONTAINS 'opal-data-bd' RETURN a.node_id AS bucket, b.node_id AS target ORDER BY target
CLIENT=bash .tools/comp-kuzu "$CYPHER"   (one argv element, no shell re-quoting)
PROCS_PATTERN=kuzu_nessie_load|kuzu_incremental_refresh|derive_runner
PROCS_TABLE_ROWS=45
PROCS_POSCTL_BASH=39
PROCS_BEFORE=0
TIME_TO_ANSWER_S=7.802
CLIENT_RC=0
--- ANSWER (client stdout) ---
bucket                     target
-------------------------  ----------------------------------------------------------------------
arn:aws:s3:::opal-data-bd  arn:aws:lambda:us-east-1:313476888478:function:bd-allocation-processor
arn:aws:s3:::opal-data-bd  arn:aws:lambda:us-east-1:313476888478:function:bd-gold-trigger
arn:aws:s3:::opal-data-bd  arn:aws:lambda:us-east-1:313476888478:function:bd-silver-merge

(3 rows)
--- CLIENT STDERR (carries the VINTAGE line) ---
VINTAGE: Built from the estate as of 2026-09-04 16:38:39 UTC.  [vintage=2026-09-04T16:38:39.485910+00:00 manifest=c3ba0330e306 prefix=projection/2026-09-04T16:38:39.485910+00:00/]
--- end client output ---
ANSWER_ROW_COUNT=0
PROCS_DURING_MAX=0
PROCS_AFTER=0
```

### Run 2 -- LABELLED: variance run, and the first with the repaired counter

```
ASKER=0.9.0_WK_NFRA_CLDGRPH~3
QUESTION=Which Lambda functions does the bd data bucket trigger?
CYPHER_AS_SENT=MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE e.edge_type='TRIGGERS' AND a.node_id CONTAINS 'opal-data-bd' RETURN a.node_id AS bucket, b.node_id AS target ORDER BY target
CLIENT=bash .tools/comp-kuzu "$CYPHER"   (one argv element, no shell re-quoting)
PROCS_PATTERN=kuzu_nessie_load|kuzu_incremental_refresh|derive_runner
PROCS_TABLE_ROWS=34
PROCS_POSCTL_BASH=32
PROCS_BEFORE=0
TIME_TO_ANSWER_S=8.497
CLIENT_RC=0
--- ANSWER (client stdout) ---
bucket                     target
-------------------------  ----------------------------------------------------------------------
arn:aws:s3:::opal-data-bd  arn:aws:lambda:us-east-1:313476888478:function:bd-allocation-processor
arn:aws:s3:::opal-data-bd  arn:aws:lambda:us-east-1:313476888478:function:bd-gold-trigger
arn:aws:s3:::opal-data-bd  arn:aws:lambda:us-east-1:313476888478:function:bd-silver-merge

(3 rows)
--- CLIENT STDERR (carries the VINTAGE line) ---
VINTAGE: Built from the estate as of 2026-09-04 16:38:39 UTC.  [vintage=2026-09-04T16:38:39.485910+00:00 manifest=c3ba0330e306 prefix=projection/2026-09-04T16:38:39.485910+00:00/]
--- end client output ---
ANSWER_ROW_COUNT=3
PROCS_DURING_MAX=0
PROCS_AFTER=0
```

### The instrument control (issuer's, same client, this hour)

```
$ bash .tools/comp-kuzu "MATCH (n:CloudNode) WHERE n.node_type='LAMBDA' RETURN count(n)"
VINTAGE: Built from the estate as of 2026-09-04 16:38:39 UTC.  [vintage=2026-09-04T16:38:39.485910+00:00 manifest=c3ba0330e306 prefix=projection/2026-09-04T16:38:39.485910+00:00/]
COUNT(n._ID)
------------
203

(1 rows)
rc=0
```

### The hand-off premise re-ground (the TO's `<status>` line)

```
$ ls -l infra/aws/globgrph/projection_client.py     -> exists, 9521 bytes, rc=0
$ bash .tools/comp-kuzu "MATCH (n) RETURN count(n) AS nodes"
VINTAGE: Built from the estate as of 2026-09-04 16:38:39 UTC.  [vintage=2026-09-04T16:38:39.485910+00:00 manifest=c3ba0330e306 prefix=projection/2026-09-04T16:38:39.485910+00:00/]
nodes
-----
27295

(1 rows)
rc=0
```

## 7. What this record does NOT claim

- It does not grade "in the time an ordinary lookup takes" (`D5-AC5`, judgment, `3.0.0_SA_CVO` at L9).
- It does not claim the served graph is CORRECT about the bd bucket's triggers. It claims the asker got an answer
  with a vintage, fast, with no build. Whether those three lambdas are the live estate's triggers is the derive's
  question and belongs to TO-CG-D-1/D-12, not to this closing pass.
- It does not close `D5-AC4`, which is FAIL against the expectation as written (s.1, row `NFRA_CLDGRPH-W3-S1`),
  so this TO stays OPEN and its `<status>` is NOT flipped.
