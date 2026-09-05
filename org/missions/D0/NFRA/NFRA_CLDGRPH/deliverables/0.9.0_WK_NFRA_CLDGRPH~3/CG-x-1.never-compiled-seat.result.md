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
- ~~It does not close `D5-AC4`, which is FAIL against the expectation as written (s.1, row `NFRA_CLDGRPH-W3-S1`),
  so this TO stays OPEN and its `<status>` is NOT flipped.~~ **SUPERSEDED BY s.8 (the re-hand pass, 2026-09-04
  ~18:4xZ), NOT retracted:** the sentence was TRUE of the order as it stood at `70ecc4068e`. The issuer amended
  `D5-AC4`'s pattern at `88c4db9dd4` and re-handed the order; s.8 re-measures it and it PASSES. Row
  `NFRA_CLDGRPH-W3-S1` stands as filed.


---

# 8. THE RE-HAND PASS (round 2, same asker, same worktree, amended `D5-AC4`)

**Written** 2026-09-04 ~18:4xZ - **worktree** `wk-NFRA_CLDGRPH-3` @`5376ecaa8b` (LOCAL; CLOUD merged in, and the
first pass's own commit `70ecc4068e` is an ancestor of this HEAD, so the evidence in s.1-s.7 above is AT my HEAD).
**Why this section exists:** the issuer amended `D5-AC4` at `88c4db9dd4` - dropping the `--mode` alternative that
matched the module docstring documenting its own absence - and re-handed the order. Sections 1-7 are the first
pass and are NOT re-derived. This section re-measures every mechanical criterion at THIS head, so no row in the
proof instance is carried on a number I did not take myself.

## 8.1 `D5-AC4` on the AMENDED invocation - the criterion this re-hand exists for

```
$ timeout 120 python .tools/comp-read infra/aws/globgrph/kuzu_cli.py --enumerate 'ensure_fresh|kuzu_nessie_load|import kuzu' --limit 3
  SOURCE: 169 lines | 8 section(s) via python-ast | enumerate: 'ensure_fresh|kuzu_nessie_load|import kuzu'
  ENUMERATE: 0 hit(s) across 169 lines / 8 section(s) scanned
    whole-value matches: 0   |   substring matches: 0
    BANDS (sum to 0):
      DOCSTRING   0
      COMMENT     0
      DEF         0
      CODE        0
         0  ENUMERATE   ABSENT hit 0/0 scanned 169 lines / 8 sections; pattern absent from this file
ENUMERATE-END: 0 hit(s) | 0 whole | 0 sub | DOCSTRING=0 | COMMENT=0 | DEF=0 | CODE=0
rc=0
```

**PASS by output** against `expect` = `ENUMERATE: 0 hit\\(s\\)`. **Denominator: 169 lines / 8 AST sections, the
whole file** - not a page, not a band. Every band is 0, so this is a true absence and not a re-banding of the
first pass's docstring hit.

**THE ARM IS NOT DEAD - the control, taken by me, not quoted from the issuer.** The issuer stated the amended
pattern still returns 5 hits with CODE=4 on the pre-CG-s-6 client @`c7b6a0d200`. I did not take that number on
trust; I reproduced it. `git show c7b6a0d200:infra/aws/globgrph/kuzu_cli.py` (rc=0, 10327 bytes - the positive
control that the ref resolved and the read is not a mangled empty) into `.scratch/`, then the IDENTICAL enumerate:

```
  SOURCE: 189 lines | 6 section(s) via python-ast
  ENUMERATE: 5 hit(s) across 189 lines / 6 section(s) scanned
    whole-value matches: 2   |   substring matches: 3
    BANDS (sum to 5): DOCSTRING 0 | COMMENT 1 | DEF 0 | CODE 4
        18  CODE        WHOLE  hit 1/5 import kuzu
        43  COMMENT     WHOLE  hit 2/5 #   full -> force the full kuzu_nessie_load UNCONDITIONALLY ...
        51  CODE        SUB    hit 3/5 refreshed, reason = _canonical.ensure_fresh(
ENUMERATE-END: 5 hit(s) | 2 whole | 3 sub | DOCSTRING=0 | COMMENT=1 | DEF=0 | CODE=4
```

Same detector, same pattern, a file that genuinely embeds the engine: **5 hits, CODE=4**, matching the issuer's
measurement exactly. The amended criterion can still fail on the thing it exists to catch, and - unlike the
original - it can now also PASS when the property holds. The first pass's finding is intact: what changed is the
carrier, not the bar.

## 8.2 The other mechanical criteria, RE-MEASURED at this head (not carried on the first pass's numbers)

| criterion | invocation (bounded) | deciding output | denominator | verdict |
|---|---|---|---|---|
| `D5-AC1` | `ls -d infra/aws/globgrph/kuzu_nessie_db 2>&1; echo "rc=$?"` | `ls: cannot access ...: No such file or directory` / `rc=2` | 1 of 1 path named; the SAME command on `infra/aws/globgrph` returns the dir at `rc=0`, so the arm is live | **PASS** |
| `D5-AC2` | `bash .../ask.sh` | `TIME_TO_ANSWER_S=17.058` then `VINTAGE: Built from the estate as of 2026-09-04 18:11:48 UTC.` | 1 ask, 3 answer rows by the client's own `(3 rows)` denominator, `CLIENT_RC=0` | **PASS** |
| `D5-AC3` | `bash .../ask.sh \\| grep -E '^PROCS_(BEFORE\\|AFTER)='` | `PROCS_BEFORE=0` / `PROCS_AFTER=0` | 0 matches of `kuzu_nessie_load\\|kuzu_incremental_refresh\\|derive_runner` out of a 52-row `ps -ef` table, `grep -v grep` discipline; `PROCS_DURING_MAX=0`; the same pipeline over `bash` returned 38, so the counter is not a dead arm | **PASS** |

The answer is unchanged in substance: the same three bd-pipeline lambdas (`bd-allocation-processor`,
`bd-gold-trigger`, `bd-silver-merge`) from `arn:aws:s3:::opal-data-bd`, `ANSWER_ROW_COUNT=3` on both runs.

## 8.3 TWO THINGS MOVED BETWEEN THE PASSES. Both are recorded, neither is graded here.

**(a) The projection's vintage moved, and that is not my act.** First pass:
`manifest=c3ba0330e306`, `2026-09-04 16:38:39 UTC`. This pass, on BOTH runs, byte-identical to each other:
`manifest=a78b6836265e`, `2026-09-04 18:11:48 UTC`. Some other seat built a projection between the two passes.
It is not this asker's doing and the evidence is positive, not merely absent: `PROCS_BEFORE/DURING_MAX/AFTER` are
0 on every run, and my FIRST ask of this pass already read `18:11:48` - before it I had run only
`comp-kuzu --schema` (the order's `compiler_tools_mandate`, a read). The manifest being IDENTICAL across my two
asks is the third witness that nothing built under me. For FWD-1 this sharpens rather than weakens the endpoint:
a seat that has compiled nothing consumed a graph somebody else built, and was told which graph it was.

**(b) THE TIME TO ANSWER ROUGHLY DOUBLED, and it now sits ABOVE the comparator the order names.**

| pass | runs | `TIME_TO_ANSWER_S` | mean | vs the order's comparator (`comp-find --corpus aws` = 11.55 s at L5) |
|---|---|---|---|---|
| first (`70ecc4068e`) | n=3 | 7.802, 8.497, 7.668 | 7.99 s | BELOW |
| re-hand (this) | n=2 | 17.058, 16.372 | 16.72 s | ABOVE |

**This is recorded, NOT graded.** `D5-AC5` ("in the time an ordinary lookup takes") is `judgment="true"` and
belongs to `3.0.0_SA_CVO` at L9; a worker verdict on it is INVALID by the order's own `proof_of_spec` block. What
I can say without grading: n=2 and n=3 are both small, the two passes ran against DIFFERENT projections
(`c3ba0330e306` vs `a78b6836265e`) over a network round trip, and this pass holds no measurement that separates a
slower client from a larger projection from a slower link - I did not run one, because isolating it is a
different question than the one this cell asks and would have been work the order did not name. The CVO grades
the endpoint on the numbers above, with both passes visible.

## 8.4 What this section still does not claim

Sections 7's other two bullets stand unchanged: this record does not grade `D5-AC5`, and it does not claim the
three answered TRIGGERS edges are true of the live AWS estate (that is TO-CG-D-1/D-12's cell, not this closing
pass's). What IS now claimed, and was not at `70ecc4068e`: every mechanical criterion of TO-CG-D-5 reads PASS by
its own output at `5376ecaa8b`, so the order's `<status>` is flipped to `complete` in the same commit as this
record and the proof instance.
