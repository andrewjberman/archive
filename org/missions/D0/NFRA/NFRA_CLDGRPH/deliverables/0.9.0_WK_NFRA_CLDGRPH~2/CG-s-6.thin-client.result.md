# CG-s-6 -- `.tools/comp-kuzu` is a THIN CLIENT of the served projection

**TO:** `NFRA_CLDGRPH.TO-CG-D-3` · **cell:** CG-s-6 (decomp v0.2 @`70918d5d2b`) · **FWDs:** FWD-3, FWD-6
**Seat:** `0.9.0_WK_NFRA_CLDGRPH~2`, worker subagent of `2.0.0_SA_COO~A` · **branch:** `wk-NFRA_CLDGRPH-2`, based on CLOUD @`0df8682fa0`
**Push state:** LOCAL. Nothing in this record was pushed, merged or rebased by this seat.
**All measurements 2026-09-04, between 15:4xZ and 16:4xZ, against the live gateway at vintage `2026-09-04T14:45:21.329463+00:00`.**

---

## 1. BEFORE / AFTER, side by side (the FWD-6 evidence, and half of D3-AC8)

### 1a. The CLI surface

| | BEFORE (@`0df8682fa0`) | AFTER (this branch) |
|---|---|---|
| usage | `kuzu_cli.py [-h] [--db-path DB_PATH] [--json] [--limit LIMIT] [--schema] [--mode {auto,full,inc}] [query]` | `kuzu_cli.py [-h] [--json] [--limit LIMIT] [--schema] [query]` |
| description | `Run a Cypher query against the GLOBGRPH Kuzu DB` | `Run a Cypher query against the SERVED GLOBGRPH projection (thin client)` |
| `--db-path` | present, default `...\infra\aws\globgrph\kuzu_nessie_db` | **GONE** |
| `--mode {auto,full,inc}` | present, elects the refresh discipline | **GONE** |
| `--json` / `--limit` / `--schema` | present | present, unchanged |
| forbidden-flag census `--mode\|--db-path\|--force\|--refresh\|--fresh` over `--help` | **6** | **0** |

`--help`, BEFORE, verbatim:

```
usage: kuzu_cli.py [-h] [--db-path DB_PATH] [--json] [--limit LIMIT]
                   [--schema] [--mode {auto,full,inc}]
                   [query]

Run a Cypher query against the GLOBGRPH Kuzu DB

positional arguments:
  query                 Cypher query string (omit with --schema)

options:
  -h, --help            show this help message and exit
  --db-path DB_PATH     Kuzu DB directory (default:
                        C:\Users\AndrewBerman\Desktop\wk-
                        NFRA_CLDGRPH-2\infra\aws\globgrph\kuzu_nessie_db)
  --json                Output results as JSON array
  --limit LIMIT         Append LIMIT N if query has none
  --schema              Print the CloudNode/CloudEdge-with-properties Cypher
                        dialect (stops Cypher-guessing)
  --mode {auto,full,inc}
                        NFRA_KUZUSPLIT P1 refresh mode: full=force full (MSTR
                        startup) | inc=incremental-OR-serve-labeled-stale,
                        NEVER full | auto=back-compat (default). Set with
                        `comp-kuzu --mode inc|full` (the -inc / -full wrappers
                        were retired 2026-09-02). The NEVER-full guarantee is
                        a property of --mode inc itself.
```

`--help`, AFTER, verbatim:

```
usage: kuzu_cli.py [-h] [--json] [--limit LIMIT] [--schema] [query]

Run a Cypher query against the SERVED GLOBGRPH projection (thin client)

positional arguments:
  query          Cypher query string (omit with --schema)

options:
  -h, --help     show this help message and exit
  --json         Output results as JSON array
  --limit LIMIT  Append LIMIT N if query has none
  --schema       Print the CloudNode/CloudEdge-with-properties Cypher dialect
                 (stops Cypher-guessing)
```

### 1b. Every refresh/DB switch that existed, named line by line (the "before" of FWD-6)

Measured on the two files at `0df8682fa0` before any edit:

| where | line(s) | the switch |
|---|---|---|
| `.tools/comp-kuzu` | `:19` | `export GLOBGRPH_KUZU_INCREMENTAL_REFRESH=1` -- elects incremental refresh, fabric-wide, on every call |
| `.tools/comp-kuzu` | `:25` | `export GLOBGRPH_KUZU_REBUILD_LIVENESS=1` -- elects the rebuild-winner liveness discipline |
| `.tools/comp-kuzu` | `:2-13` | header documenting `--db-path`, `--mode full`, `--mode inc` and the rebuild engine as user-facing choices |
| `kuzu_cli.py` | `:30` | `DEFAULT_DB_PATH = _canonical.CANONICAL_DB_PATH` -- the local path the CLI opens |
| `kuzu_cli.py` | `:166-167` | `--db-path`, default `DEFAULT_DB_PATH` |
| `kuzu_cli.py` | `:174-178` | `--mode {auto,full,inc}` |
| `kuzu_cli.py` | `:46-71` | the auto-refresh block: `_canonical.is_canonical`, `_canonical.ensure_fresh`, `_full_rebuild_only`, `_incremental_or_serve_stale`, and the INFO refresh/stale disclosures |
| `kuzu_cli.py` | `:18,20,21` | `import kuzu`, `import _provenance`, `import _canonical` |
| `kuzu_cli.py` | `:73-75` | `os.path.exists(db_path)` + "Run kuzu_load.py first" |
| `kuzu_cli.py` | `:88-89` | `kuzu.Database(db_path, read_only=True)` / `kuzu.Connection(db)` -- the local open |

AFTER: **0 of 10** remain. The engine-token census over the whole file is the D3-AC3 arm below and returns `ENUMERATE: 0 hit(s) across 169 lines / 8 section(s) scanned`.

`.tools/comp-kuzu` went from 30 lines to 14: the two `export GLOBGRPH_KUZU_*` lines and the rebuild commentary are gone; the header now states the transport in two lines and one line says there is no refresh flag. The `comp_log_auto.py` telemetry line and the exit-code passthrough are untouched.

---

## 2. THE RENDERING CHOICE (D3-AC8, judgment -- stated, not graded here)

Every answer ends with ONE line on stderr:

```
VINTAGE: Built from the estate as of 2026-09-04 14:45:21 UTC.  [vintage=2026-09-04T14:45:21.329463+00:00 manifest=84eb18f1abc2 prefix=projection/2026-09-04T14:45:21.329463+00:00/]
```

**Why it reads that way, in the order it reads:**

1. **The service's sentence comes FIRST, verbatim, unmodified.** `PROJECTION_CONTRACT.md` s.3 defines `age_line` as "Plain words derived from `committed_at`: `Built from the estate as of <YYYY-MM-DD HH:MM:SS UTC>.` A reader may display this sentence without knowing build internals," and s.8's CG-s-6 handoff says "display the manifest's `age_line` verbatim." Verbatim is the whole point: the moment the client re-words, rounds or relativises the sentence ("2h old", "current"), the age acquires a SECOND author, and the two carriers drift. There is no formatting code anywhere in `kuzu_cli.py` that touches the sentence -- `_disclosure()` interpolates it and nothing else.
2. **The client runs NO clock.** No `time`, no `datetime`, no `os.path.getmtime` is imported for display purposes. An agent cannot ask this CLI "how old is that, really?" and get an answer computed here, because there is nothing here to compute it with. This is the FWD-3 property stated as an absence rather than as a promise.
3. **The machine fields trail, in brackets, and are for re-derivation, not for reading.** `vintage` is the pointer identity, `manifest` is the first 12 of `manifest_sha256` (enough to match a manifest, short enough not to swamp the sentence a human is meant to read), `prefix` is the exact S3 artifact prefix. An auditor who wants to check the claim has the three keys needed to go straight to `projection/<vintage>/` and hash the manifest. Order encodes audience: plain words for the reader, identifiers for the machine.
4. **It rides stderr, always, in both modes.** Table stdout stays the table; `--json` stdout stays a parseable JSON array (D3-AC4). A disclosure that broke `--json` would be removed by the first consumer that hit it, and a disclosure that can be removed is not a disclosure.
5. **On failure the line names an ABSENCE, never a vintage.** The error path prints

   ```
   ERROR: projection service 502: projection service HTTP 500 on /cypher: {"error":"Parser exception: ..."}
   VINTAGE: unavailable -- the projection service did not answer; no age was inferred and no local copy was read.
   ```

   and exits 1. This is the one place a vintage disclosure is dangerous: a client that keeps printing the last-known age when the service is down is worse than one that prints nothing, because the age is then a lie with a citation. Battery arm iv holds this with two RED mutants -- a client printing `age: 0.0h (assumed current)`, and a client printing the service's real sentence when the service never answered. Both are CAUGHT by the same detector that passes the real output.
6. **The empty answer discloses identically.** `(0 rows)` plus the retained 0-rows-scope note plus the same VINTAGE line -- because "0 rows" is exactly the answer where a reader most needs to know whether the emptiness is the graph's or the vintage's.

---

## 3. WHAT WAS BUILT

### `infra/aws/globgrph/projection_client.py` (NEW, 218 lines)

Stdlib only: `json`, `os`, `subprocess`, `sys`, `time`, `urllib.request`, `urllib.error`. **boto3 is NOT used** -- the token is read with the repo's `.tools/aws` shim through `subprocess`, which is what TO-CG-D-2's exercise proved works from this seat and adds no dependency to this tree.

- `base_url()` -- env `OPAL_GATEWAY_BASE_URL`, default `https://mcp.opalinvest.dev`.
- `get_token()` -- reads Secrets Manager `opal/mcp/graph-read-token` ONCE per process, caches in a module global **in memory only**. No file, no log, no exception message ever carries the value; an empty read is an error, not an anonymous call.
- `query(statement, timeout_s=20.0) -> dict` -- POSTs `statement.encode("utf-8")` to `/graph/cypher` and returns the service's dict **verbatim** (`rows`, `vintage`, `age_line`, `manifest_sha256`, `artifact_prefix`; nothing reshaped).
- `health(timeout_s=20.0) -> dict` -- GET `/graph/health`, verbatim. Live shape today: `{"status":"ok","vintage":"2026-09-04T14:45:21.329463+00:00","pointer_read_at":"...","last_swap":"..."}`.
- `ProjectionClientError(message, status, error)` -- carries the HTTP status and the body's `error` field. No urllib traceback escapes.
- Retry: **transport-level failures only**, 3 attempts x 2 s. A SERVICE answer is never retried (a Cypher parse error re-asked three times is 4 s of nothing).

**One trap paid for during the build, and the line that closes it.** The first draft spawned the shim with a bare `"bash"` in argv. Measured on this worktree: rc=1, stderr EMPTY, and 504 bytes of UTF-16 on **stdout** reading "Windows Subsystem for Linux has no installed distributions" -- i.e. the System32 WSL stub answered, the shim never ran, and the failure surfaced as `could not read the capability bearer ... (aws rc=1: )` with an empty reason. That is the exact class CLAUDE.md's git section routes through `.tools/git_bash_resolver.py`; `_shim_argv()` now calls `git_bash_resolver.bash_argv()` and never puts a bare unix name in argv. The rc!=0 message also falls back to stdout when stderr is empty, so the WSL failure mode can never again present as a blank reason. (Not a surprise row: the law already names this trap; the build simply obeyed it after measuring it.)

### `infra/aws/globgrph/kuzu_cli.py` (REWRITTEN, 189 -> 169 lines)

Keeps `query`, `--json`, `--limit`, `--schema`. Keeps `_print_schema()` verbatim except its one self-description: the docstring now reads "Static + service-free (works even if the projection is offline)" where it read "Static + DB-free (works even if the DB is offline)". The 20 printed dialect lines are byte-identical. Keeps the 0-rows scope note verbatim, including its stdout-in-table / stderr-in-json placement. Removes `--db-path`, `--mode`, `import kuzu`, both seam imports, the provenance header and the whole auto-refresh block. Calls `projection_client.query`. Renders the service's `rows` (a list of dicts) as the same aligned table, or as a JSON array.

### `.tools/comp-kuzu` (REWRITTEN, 30 -> 14 lines)

Both `export GLOBGRPH_KUZU_*` lines and the rebuild commentary are gone. Header states the transport in two lines. `comp_log_auto.py` telemetry and the exit passthrough unchanged.

### `.tools/tests/test_cg6_thin_client_battery.py` (NEW, 332 lines, 7 arms, 45 checks)

No network in any arm: `projection_client.query` is stubbed by a context manager, and the transport arm stubs `urllib.request.urlopen` and sets a fake token, so Secrets Manager is never called.

---

## 4. THE BATTERY, at both grains

**Direct** -- `python .tools/tests/test_cg6_thin_client_battery.py`, rc=0:

```
CG-s-6 THIN-CLIENT BATTERY -- 7 arm(s), no network
ARM i   clean answer: table + age_line verbatim    9 of 9 checks PASS
ARM ii  --json: stdout array, disclosure on stderr 6 of 6 checks PASS
ARM iii empty result: (0 rows) + note + VINTAGE    4 of 4 checks PASS
ARM iv  service error: rc1, no fabricated age      7 of 7 checks PASS
ARM v   CLI surface: no refresh/db-path choice     5 of 5 checks PASS
    denominator: 6 source token(s) scanned over 170 line(s) of kuzu_cli.py
ARM vi  kuzu_cli.py source: no engine, no seam     7 of 7 checks PASS
    denominator: 2 transport grains checked (CLI->client, client->HTTP body); statement length 102 chars, 2 quote char(s)
ARM vii string literal: byte-for-byte to the wire  7 of 7 checks PASS
BATTERY: 7 of 7 arm(s) PASS
PASS
```

**Under pytest, at the FILE grain** -- `python -m pytest .tools/tests/test_cg6_thin_client_battery.py -q`, rc=0: `7 passed in 0.10s`.

Denominator: **45 checks across 7 arms**, 45 PASS, 0 FAIL, at both grains.

**RED MUTANTS (3, one per arm where a mutant is expressible), all FIRED-AS-EXPECTED:**

| arm | mutant | detector's verdict on the mutant | on the real output |
|---|---|---|---|
| iv | a client printing `VINTAGE: age: 0.0h (assumed current)` on the error path | CAUGHT | clean |
| iv | a client printing the service's real `age_line` when the service never answered | CAUGHT | clean |
| v | a `--help` text that re-adds `--mode {auto,full,inc}` | CAUGHT (`['--mode']`) | clean (`[]` of 5 forbidden flags) |
| vii | a client that applies the shell-escape idiom to the body (`'...'\''...'`) | CAUGHT (bytes differ) | clean (body == statement bytes) |

**Arm vii is the W1-S10 trap, held at two grains.** (a) the statement handed to `projection_client.query` by the CLI equals the typed statement exactly (1 of 1); (b) the request BODY captured at `urlopen` equals `statement.encode("utf-8")` byte for byte, and contains no `'\''` sequence. The fixture carries 2 quote characters over 102 chars precisely because a shape control with no string literal cannot see this defect. The LIVE control on the same property is in s.5 below: a real `WHERE n.node_type='LAMBDA'` returns **203**, not 0.

---

## 5. THE EXERCISE -- real answers through the real gateway

**Exercise 1 (table).** `bash .tools/comp-kuzu "MATCH (n:CloudNode) RETURN n.node_type AS t, count(*) AS c ORDER BY c DESC LIMIT 5"`, rc=0:

```
VINTAGE: Built from the estate as of 2026-09-04 14:45:21 UTC.  [vintage=2026-09-04T14:45:21.329463+00:00 manifest=84eb18f1abc2 prefix=projection/2026-09-04T14:45:21.329463+00:00/]
t           c
----------  ----
C2Motif     6300
Field       4969
MS_FILE     4963
JSXElement  2205
JSXRender   1433

(5 rows)
```

**Exercise 2 (`--json`, a query WITH a string literal -- the W1-S10 live control).** `bash .tools/comp-kuzu --json "MATCH (n:CloudNode) WHERE n.node_type='LAMBDA' RETURN n.node_id AS id LIMIT 3"`, rc=0:

```
VINTAGE: Built from the estate as of 2026-09-04 14:45:21 UTC.  [vintage=2026-09-04T14:45:21.329463+00:00 manifest=84eb18f1abc2 prefix=projection/2026-09-04T14:45:21.329463+00:00/]
[
  {
    "id": "arn:aws:lambda:us-east-1:313476888478:function:opal-trending-topics-portal-publisher"
  },
  {
    "id": "arn:aws:lambda:us-east-1:313476888478:function:bd-49f-fees-runner"
  },
  {
    "id": "arn:aws:lambda:us-east-1:313476888478:function:opal-cot-value-parity"
  }
]
```

The stderr line is the disclosure; the stdout block is the parseable array. A separate count with the same literal returns `c = 203` LAMBDA nodes -- a filtered query with a quoted literal returning a NON-zero answer is the live discriminator the W1-S10 row asked for.

**Exercise 3 (the error path).** `bash .tools/comp-kuzu "MATCH (n RETURN oops"`, rc=1, stdout EMPTY:

```
ERROR: projection service 502: projection service HTTP 500 on /cypher: {"error":"Parser exception: Invalid input <MATCH (n RETURN>: expected rule oC_SingleQuery (line: 1, offset: 9)\n"MATCH (n RETURN oops"\n          ^^^^^^"}

VINTAGE: unavailable -- the projection service did not answer; no age was inferred and no local copy was read.
```

**`--schema` still answers with no service and no database** (first line: `comp-kuzu schema -- the GLOBGRPH CloudNode/CloudEdge-with-PROPERTIES dialect`).

---

## 6. THE SEAM IS UNTOUCHED (D3-AC5)

`git show HEAD:infra/aws/globgrph/_canonical.py | sha256sum` -> `d494be6660b0dd9674383a2504756d4fb852677eee5729718cc3298ff69b2952`, the exact value the order names.

Second instrument, different plane: `sha256sum infra/aws/globgrph/_canonical.py` on the WORKTREE returns the same digest, and `git status --porcelain infra/aws/globgrph/_canonical.py` returns empty. The record and the checkout agree; nothing moved. The 33 other consumers of the local DB (`comp-find --corpus aws`, `org/modules/graph/cli.py`, `comp_blast_universe.py`, `comp_detect.py`, `comp_debt.py`, the engines) are untouched and keep reading the local copy until CG-s-8 retires it.

---

## 7. ROW FILED

**`NFRA_CLDGRPH-W2-S11`** (OBSERVATION, INERT, `disposition: UNDER_INVESTIGATION`) -- the graph-call manifest's `C_adhoc_reimplementation` advisory fired 5 ERROR-labelled findings on this order's battery with the remedy "Route graph queries through comp-kuzu so they hit the canonical persisted Kuzu DB", which after this order is a surface comp-kuzu no longer reaches; all 5 hits are Cypher STRINGS in stubbed fixtures that make 0 graph calls. Advisory today (`5 would block in blocking mode`, gate rc=0, `pre-commit gate clean`), and `graph-call-manifest.yaml:6` @`dffbee781c` declares the `advisory -> blocking` promotion. NOT remediated: `org/modules/graph/` is outside this order's `<paths>` and is named in its BOUNDS as CG-s-8's surface. Header denominator restated 54 -> 55 on the append.

---

## 8. WHAT THIS ORDER DID NOT DO

- **Did not touch the local engine, `_canonical.py`, or any other consumer.** That is CG-s-8 / TO-CG-D-7.
- **Did not re-word `org/modules/graph/graph-call-manifest.yaml`** despite row W2-S11 -- out of `<paths>`.
- **Did not build a cache, a fallback-to-local, or a retry-until-fresh.** A service that cannot answer produces an error and an ABSENT vintage; the local copy is not a fallback, it is a second clock.
- **Did not add an alarm, monitor or freshness checker.**
- **Did not grade D3-AC8.** It is `judgment="true"`; s.2 above is the reading act, and `3.0.0_SA_CVO` grades it at L9.

---

## 9. GROUNDING

- Contract: `org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.7.0_AE_CloudOps~T/PROJECTION_CONTRACT.md` s.3 (`age_line` row) and s.8 (CG-s-6 handoff), read at this branch's HEAD.
- Transport: `org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/graph_query.sh` (TO-CG-D-2, merged @`57b6750101`); exercised this turn, HTTP 200, `{"rows":[{"nodes":27206}], ...}`.
- The W1-S10 trap: row `NFRA_CLDGRPH-W1-S10` @`b687429234`.
- Manifest advisory vintage: `org/modules/graph/graph-call-manifest.yaml` @`dffbee781c` (2026-09-02).
