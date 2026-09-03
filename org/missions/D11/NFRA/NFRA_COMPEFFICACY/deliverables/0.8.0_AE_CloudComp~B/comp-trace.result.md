# comp-trace -- TO-CE-T-19 result: THE SUBSET CONDITION IS NOT MET; the order STOPS at a ROW

**Cell:** `CE-t-19` (decomp v0.2.3 @`dcf07b4799`) · **TO:** `NFRA_COMPEFFICACY.TO-CE-T-19` @`8a5d683c38`
**Seat:** `0.8.0_AE_CloudComp~B` · **Written:** 2026-09-03 · **Round:** 5 (L7)
**Outcome:** **STOPPED AT A ROW** -- `NFRA_COMPEFFICACY-S17` (BLOCKING, ARMED), per DELIVERABLE item 1 and T19-AC1's
own second limb (*"...or a ROW and a stop"*).
**Nothing was built, edited or deleted.** `.tools/comp-trace` is unchanged and present; `org/modules/graph/cli.py` is
unchanged; no registry carrier was touched.

---

## THE HEADLINE

Andrew's R-4 is **conditional**: *"comp-trace ... if so it should be retired."* The "if so" is the subset condition.
PRD v0.5 s.7 row T-19 carries `claim: measured` on *"strict subset of blast (`cli.py:1478-1530`)"*, and the L4 owner
recorded the condition **MET** on that citation.

Re-derived here with a different instrument -- enumerating both argparse parsers, then running **both tools** over a
stratified sample of the real node population -- **the condition is NOT MET.**

The cited range `:1478-1530` *is the two parser blocks*, and those blocks already carry the counter-evidence.

---

## 1. THE FLAG TABLE (T19-AC1, first half) -- from `cli.py` @`7b649df39d`, worktree byte-identical to the pin

| trace flag (`p_trace` :1482-1495) | blast equivalent (`p_blast` :1498-1530) | measured |
|---|---|---|
| `--exact` (store_true; *"A miss under --exact is NOT-FOUND (rc=3)"*) | **ABSENT** | `comp-blast <q> --exact` -> **rc=1**, `cli.py: error: unrecognized arguments: --exact` |
| `--all` (*"Trace all matches"*) | **ABSENT** -- blast instead REFUSES ambiguity at rc=5 `AMBIGUOUS-SUBJECT` | different semantics, not a superset |
| `--direction upstream` / `downstream` | **ABSENT spellings** -- blast accepts only `up`/`down`/`both` | trace normalises the aliases at `cli.py:437` |
| `--direction` default | `both` (trace) vs `None`->down (blast) | different default, same axis |
| `--depth` | `--depth` | present both |
| `--json` | `--json` | present both; both parse (`json.load` OK) |
| freshness args | freshness args | present both |

**Blast-only (not in scope here):** `--function`, `--check-consumers`, `--compare`, `--overlap-sweep`, `--population`,
`--min-score`, `--min-mass`, `--grain`, `--head`, `--all-producers`, `--pipeline`.

**The three trace-only items are CARRYABLE** into blast's parser + render exactly as the order scopes them. They are
**not** the reason this order stops. They remain correct work whichever way the re-adjudication goes, and are left
unbuilt because the gate they sit behind failed.

---

## 2. THE PARITY TABLE (T19-AC1, second half) -- real runs, both tools, same session

| # | query | comp-trace | comp-blast | verdict |
|---|---|---|---|---|
| 1 | `gold:A_00.accounts_dimension` | rc 0, 16 stdout lines | rc 0, 377 lines | **both answer** |
| 2 | `lambda:access-anomaly-scanner` | rc 0 | **rc 3 NOT-FOUND** | trace answers, blast does not |
| 3 | `s3:gold/dimensions/accounts_dimension_latest.parquet` | rc 0, 224 lines | **rc 3 NOT-FOUND** | trace answers, blast does not |
| 4 | `eventbridge:bd-allocation-pipeline-trigger` | rc 0, 5 lines | **rc 3 NOT-FOUND** | trace answers, blast does not |
| 5 | `zzz_definitely_not_a_node_ce_t_19` (NOT-FOUND control) | rc 3 | rc 3 | **rc dial matches** |
| 6 | `gold:A_00.accounts_dimension --json` | rc 0, parses | rc 0, parses | both parse |
| 7 | `gold:A_00.accounts_dimension --exact` (HIT) | rc 0 | **rc 1 unrecognized** | flag absent |
| 8 | `gold:A_00.accounts_dimension_NOPE --exact` (MISS) | **rc 3** | n/a (flag absent) | trace-only dial |

**Bare-name rescue attempted on rows 2-4** (the best mapping a forwarder could perform):
`access-anomaly-scanner` -> blast **rc 0**; `bd-allocation-pipeline-trigger` -> blast **rc 0**;
`gold/dimensions/accounts_dimension_latest.parquet` -> blast **rc 5 AMBIGUOUS-SUBJECT** (a refusal, not an answer).

### Population measurement -- denominator printed

Stratified sample, seed 19, **158 of 2,302** trace node ids, each run through blast's **own** resolver
(`comp_blast_universe.resolve_subject`, the entry point `cmd_blast` uses at `cli.py:970`):

| spelling | ANSWER rc0 | AMBIGUOUS rc5 | NOT-FOUND rc3 |
|---|---|---|---|
| **full trace-id** (what a caller types today) | **61 (38.6%)** | 0 | **97 (61.4%)** |
| **bare name** (best forwarder mapping) | **92 (58.2%)** | 41 (25.9%) | 25 (15.8%) |

Per type, full-id spelling: `GOLD_SCRIPT` 25/25 ANSWER -- but `S3_ARTIFACT` 0/25, `LAMBDA` 0/25, `EVENTBRIDGE` 0/25,
`SQS_QUEUE` 0/5, `S3_BUCKET` 0/4, `STATE_MACHINE` 0/1, `SNS_TOPIC` 0/1; `ENDPOINT` 16/25, `COMPONENT` 20/22.

> **CORRECTION TO MY OWN INSTRUMENT, recorded because it changes the number.** A first pass counted any non-empty
> match set as a hit and read **133/158 (84.2%)**. That **conflated blast's `AMBIGUOUS-SUBJECT` rc=5 refusal with an
> answer** and overstated coverage by 26 points. The corrected pass distinguishes the three outcomes and is what is
> reported above. A refusal is not an answer.

### Why this is not a vintage problem -- the cheapest competing hypothesis, tested

`load_kuzu_universe(refresh=True)` -- a **forced** refresh, kuzu `graph_nodes` last-write **0.0h** -- still yields
27,134 nodes carrying **zero** node ids under `gold:` (0), `lambda:` (0), `s3:` (0), `eventbridge:` (0), `sqs:` (0),
`sns:` (0), `sfn:` (0), `s3bucket:` (0), and **zero** nodes of type `GOLD_SCRIPT`, `S3_ARTIFACT`, `ENDPOINT`,
`EVENTBRIDGE`, `COMPONENT`. kuzu's own address space is `motifi:` / `ms:` / `type:` / `jsx:` / `arn:` / `render:` /
`pipeline:`.

**This is a schema + address-space difference, not a staleness one. A refresh cannot add a node type the schema does
not carry.**

### Why it cannot be carried inside this cell's BOUNDS

`cli.py:970-976`, verbatim: *"THE UNIVERSE IS KUZU / Andrew-direct 2026-08-03 ... FAIL LOUD, NEVER FALL BACK (spec 7):
if kuzu is unreachable this exits 1 (TOOL FAILED). A silent fallback to the private scan would reproduce the exact
defect the ruling removes."* Making blast answer over trace's universe would reverse a sovereign ruling, and is in any
case CE-t-6's surface, which this order's BOUNDS place off-limits (*"no change to blast's traversal, scoring or verdict
semantics"*).

**Consequence if the forwarder were built anyway:** roughly **two in five** working `comp-trace` calls would become
NOT-FOUND rc 3 or AMBIGUOUS rc 5 -- the precise false-clear class that `cli.py:377-380` and `:1006-1010` exist to
prevent, reintroduced *through the retirement* instead of through a typo.

---

## 3. CARRIER CENSUS (T19-AC2, measurement half) -- denominator printed, nothing edited

`comp-find -i 'comp-trace' --all --files` -> **39,710 hits across 4,814 distinct files**
(146,932 files scanned; 71,711 EPHEMERAL-FLOOR, 7 UNREADABLE, 4,183 BINARY not searched).

**Excluded as RECORD / TELEMETRY (untouched by any retirement) -- 4,643 files:**

| class | files |
|---|---|
| graph tool cache (`.comp-graph/`) | 3,887 |
| agent inbox mail | 403 |
| agent deliverables / task orders | 157 |
| session logs + handoffs | 103 |
| audit archive | 41 |
| ledger / registry records (`org/tier0/`, `rcg/`) | 24 |
| rail / run telemetry (`org/mcp/*.log|jsonl`) | 22 |
| missions tree records | 6 |

**LIVE CARRIER CANDIDATES: 171 of 4,814.** The retirement-relevant ones, by lane:

| carrier class | files | lane |
|---|---|---|
| the shim itself `.tools/comp-trace` | 1 | **this lane** |
| the engine `org/modules/graph/cli.py`, `trace_graph.py` | 2 | **this lane** |
| registry / contract: `comp-tools.yaml`, `comp-coverage-map.yaml`, `comp-output-contracts.yaml`, `TOOL_MASTER.yaml`, `TOOL_CLASSIFICATION.yaml`, `tool_overrides.yaml`, `tool_index.py`, `graph-call-manifest.yaml`, `.tools/comp-which` | 9 | **this lane** (via `COMPTOOL_REGISTRATION_FLOW.md`) |
| sibling comp-tools naming it (`comp-adversary`, `comp-build`, `comp-pydeps`, `comp-learns-status`, ...) | 6 | this lane |
| graph module code (`pipeline_cli.py`, `graph_status_cli.py`, `manifest_check_cli.py`, `extract_pipeline.py`, `extract_s3.py`, `comp_route_eval.py`, `comp_potion_relevance.py`, `derive_stitch.py`, `extract_portal_stitch.py`) | 9 | this lane |
| tests (incl. `test_trace_blast_xref_notfound_is_loud.py`) | 4 | this lane |
| **agent `prompt.md` personas naming comp-trace** | **28** | **ROUTED -- `2.0.0_SA_COO`** (other seats' identity files) |
| `.claude/skills/` (`cloud-ops`, `comp-adversary`) | 2 | ROUTED -- skill owners |
| docs / architecture / briefs | ~100 | ROUTED -- dated records, mostly NOT rewritten (the T-22 precedent) |

> **The T-22 lesson repeats, larger.** T-22 assumed 5 live carriers and found ~15. Here the class nobody would assume
> is **28 agent `prompt.md` files** -- every tier-1/2/3 persona names `comp-trace`. A retirement that edits the shim
> and the registry but not those leaves 28 seats being *told at load* to use a tool that forwards or is gone.
> **Nothing in this class was edited; it is listed so the decision is made with it visible.**

---

## 4. CALLER CENSUS (T19-AC4, measurement half) -- `org/mcp/comp-tool-runs.jsonl`, denominator printed

28,077 total run rows (0 malformed). `comp-trace` = **57 rows all-time in this file**; `comp-blast` = 601 (contrast).

| seat | comp-trace runs |
|---|---|
| `0.7.0_AE_CloudOps~F` | 18 |
| `0.8.0_AE_CloudComp~D` | 14 |
| `3.0.0_SA_CVO` | 12 |
| `0.8.0_AE_CloudComp~B` | **10 -- THIS CELL'S OWN MEASUREMENT, not caller demand** |
| `0.7.0_AE_CloudOps` | 1 |
| `1.0.0_SA_CTO~X` | 1 |
| `2.0.0_SA_COO~X` | 1 |

Corroborates the PRD/TO figure (45 in the 30d window; ~F 18 / ~D 14 / CVO 11-12). **My own 10 are excluded from any
demand reading** -- they are this order's parity runs.

**The notice to those seats is `2.0.0_SA_COO`'s broadcast on this report, not this seat's message** (TO item 4).

---

## 5. THE EXECUTABLE (T19-AC4, last-step half)

**`.tools/comp-trace` was NOT deleted and is present, measured at report:** 8 lines, unchanged, forwarding to
`cli.py trace` with `comp_log_auto` run logging. **Removal condition, written down as the order requires:** removal
remains a separate act on a later word, and it is now **gated behind the re-adjudication below** -- the condition R-4
made removal contingent on is measured unmet, so there is currently no ruling that authorises removal at all.

---

## 6. WHAT IS OWED, AND BY WHOM

**Disarm owner: `1.0.0_SA_CTO` (L4), routed via `2.0.0_SA_COO`.** A worker may not amend the PRD.

- **(a)** PRD s.7 row T-19's `claim: measured` is the carrier another cell reads -- **CE-t-6 (comp-blast) is recorded
  as depending on THIS cell.** It should not keep asserting a subset that is measured false.
- **(b)** **R-4 needs re-adjudication on the corrected measurement**, because the ruling is conditional and the
  condition failed. The three honest options, stated without preference:
  1. **retire anyway** -- accept the coverage loss as a *decision* rather than a subset claim;
  2. **keep comp-trace** -- close T-19 as NOT-RETIRED with this measurement as its evidence;
  3. **widen** -- carry trace's universe into blast, which is a CE-t-6 / L2 scope change, not a T-19 act.

  This seat expresses no preference. The choice is the L4 owner's and, on (b), plausibly **Andrew's** -- it is his own
  ruling's condition that failed.

**Carryable remainder, unbuilt:** `--exact`, `--all`, and the `upstream`/`downstream` aliases are genuine trace-only
capability that any retirement must carry into blast's parser rather than drop silently. Bounded to the blast parser +
render exactly as the order scopes them; correct work under options 1 and 3 alike.

---

## 7. CRITERION STATUS -- and why no proof instance is filed

| criterion | status | why |
|---|---|---|
| **T19-AC1** | **MET** on its second limb | the flag table and the >=6-query parity table are above, from real runs; the trace-only capability is **not** carried, and instead **"a ROW and a stop"** -- the criterion's own alternative |
| T19-AC2 | measurement half done; **edit half NOT DONE** | census + lanes above; no carrier edited, because the retirement is not authorised |
| T19-AC3 | **NOT REACHED** | no forwarder built -- it is the act the failed gate forbids |
| T19-AC4 | measurement half done; shim **present** (measured) | caller census above; removal condition recorded |
| T19-AC5 | **NOT REACHED** | no new battery: it would test a forwarder that does not exist |

**No `proof_of_spec.json` instance is filed, deliberately.** The instance is the artifact that gates the `complete`
flip, and there is no complete flip: the order stopped at its own gate. Filing an instance that graded AC2-AC5
`N/A-BY-CONSTRUCTION` would assert a disposition -- that the retirement legitimately did not need to happen -- which
is **precisely the question being routed to the L4 owner**. The instance should be filed by whichever order carries
the re-adjudicated cell.

---

## 8. CONTROLS AND VINTAGES

- `cli.py` **byte-identical** to the TO's cited pin @`7b649df39d` (`git diff --quiet`, pin resolves as positive control).
- PRD **byte-identical** to @`5bbdab5ec7` (63,969 bytes / 677 lines both sides).
- TO **committed and byte-identical** to @`8a5d683c38` (`git ls-files --error-unmatch` OK).
- trace graph rebuilt head-pinned this session: **2,302 nodes / 3,044 edges**, `built_at` 2026-09-03T11:48:41Z.
- kuzu: `infra/aws/globgrph/kuzu_nessie_db`, **27,134 nodes**, forced-refresh `graph_nodes` last-write 0.0h.
- **Independent instrument, unchanged by this cell:** `org/modules/graph/tests/test_trace_blast_xref_notfound_is_loud.py`
  -- **6 passed** under pytest at the FILE grain (23.79s) and rc 0 direct. It independently confirms both tools' rc=3
  NOT-FOUND dials and that production is untouched.
- Production sha: **unchanged** -- no `.py` and no shim was edited in this cell.

## 9. COMPILER TOOLS USED

`comp-read` (cli.py shape + the `--for` question, and `--enumerate` for the `_bu` import, the gate enums, the schema
status enum), `comp-find` (`--name` to locate the TO/PRD; `-i 'comp-trace' --all --files` for the carrier census, never
headed -- the 234KB output was persisted and partitioned in a second pass), `comp-blast` / `comp-trace` themselves as
the measured subjects, `.tools/surprise-row-gate.py --self-test` (11 arms, 0 failed) before trusting the row gate.
