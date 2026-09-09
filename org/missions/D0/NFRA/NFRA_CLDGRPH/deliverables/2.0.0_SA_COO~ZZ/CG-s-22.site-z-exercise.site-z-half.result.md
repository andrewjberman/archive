THIS IS THE SITE-Z HALF; THE LAPTOP'S RECORD IS THE OTHER HALF; THE PAIR IS GRADED AT L9

**Seat:** `2.0.0_SA_COO~ZZ` · **Exercise:** `NFRA_CLDGRPH` CG-s-22, site-Z half · **Routed by:** `0.0.0_AB_MSTR~Z` msg 20553, carried from `2.0.0_SA_COO~A` msg 94622, on Andrew's allocation @`7caee0ad5d`
**archetype:** VALIDATE

⚠ **PARTIAL AND SAID SO: T0 IS RECORDED, T1 (20:00:00Z) AND T2 (21:00:00Z) ARE PENDING.** This file is
committed after T0 rather than held to T2 because two hours of unwritten evidence on a shared tree is a
worse risk than a record that states its own incompleteness. It is updated in place at each instant.

```json
{
  "machine": "site-z",
  "seat": "2.0.0_SA_COO~ZZ",
  "question": "node_type census over CloudNode, deterministic ordering (D-8's, unchanged)",
  "cypher": "MATCH (n:CloudNode) RETURN n.node_type AS t, count(*) AS c ORDER BY c DESC, t",
  "instrument": "bash .tools/comp-kuzu --json <cypher>, through the public gateway at https://mcp.opalinvest.dev/graph/cypher",
  "instants": [
    {
      "t": "T0",
      "target": "2026-09-09T19:00:00Z",
      "start": "2026-09-09T19:00:00.502Z",
      "end": "2026-09-09T19:00:04.287Z",
      "began_within_5s": true,
      "rc": 0,
      "skew_s": 0,
      "rows_sha256": "3071ef4c4bf5e16c946ffb59e142213cbea0e22d0c1103b0e26ce9890a8930df",
      "vintage": "2026-09-09T14:59:48.778469+00:00",
      "manifest": "86ea84674078",
      "rows_count": 58,
      "answer_file": "answer_T0.json",
      "head_at_instant": "1a7963cc83aff538933806ef8542671fd58298d9",
      "comp_kuzu_blob_at_instant": "c9677f20514949b3f86e54a5e46e29289d52dbdb"
    },
    { "t": "T1", "target": "2026-09-09T20:00:00Z", "status": "PENDING" },
    { "t": "T2", "target": "2026-09-09T21:00:00Z", "status": "PENDING" }
  ],
  "local_db_census": {
    "when": "pre-T0, 2026-09-09T18:3xZ",
    "path": "/c/Users/Opal Bloomberg/Desktop/ajb_workspace/infra/aws/globgrph/",
    "probe": "ls <path> | grep -c -E 'kuzu_nessie_db|kuzu_db|kuzu_ac7'",
    "expected_by_spec": 0,
    "MEASURED": 7,
    "forced_to_expected": false,
    "matches": [
      {"name": "kuzu_nessie_db", "type": "file", "bytes": 116199424, "mtime": "Sep 3 08:05"},
      {"name": "kuzu_nessie_db._build_manifest.json", "type": "file", "bytes": 902, "mtime": "Sep 3 08:05"},
      {"name": "kuzu_nessie_db._refresh_status.json", "type": "file", "bytes": 262, "mtime": "Sep 3 21:38"},
      {"name": "kuzu_nessie_db.fallback.jsonl", "type": "file", "bytes": 1656, "mtime": "Sep 3 21:38"},
      {"name": "kuzu_nessie_db.rebuild.lock", "type": "dir", "mtime": "Sep 4 04:48"},
      {"name": "kuzu_nessie_db.rebuild.tmp", "type": "file", "bytes": 4096, "mtime": "Sep 4 04:48"},
      {"name": "kuzu_nessie_db.rebuild.tmp.wal", "type": "file", "bytes": 5857067, "mtime": "Sep 4 04:49"}
    ],
    "tracked_in_git": false,
    "positive_control": "the same ls prints ~70 sibling entries (kuzu_cli.py, kuzu_load.py, projection_client.py, ...), so 7 is a MEASURED count and not a broken probe",
    "probe_correctly_excludes": "kuzu_cli.py / kuzu_load.py / kuzu_ac_traversals.py -- none matches 'kuzu_ac7'",
    "stitch_store": "not identified among the 7; all seven are kuzu_nessie_db*",
    "disposition": "ROUTED UPWARD to 0.0.0_AB_MSTR~Z, NOT resolved here (confirmed by msg 20568: 'not that lane's to resolve')"
  },
  "bounds_honoured": {
    "reads_only": true,
    "local_graph_created_opened_or_downloaded": false,
    "s3_writes": 0,
    "code_edits": 0,
    "transport": "thin client to the gateway only -- corroborated by the answer carrying a SERVER vintage"
  }
}
```

## What the census means, and what it does not

The spec's L9 pair criterion is *byte-identical rows sha256 under one vintage at a matching instant,
**and both censuses 0***. **Site Z's census is 7, so on a literal reading this half fails that second
limb before any instant is asked.** It is recorded as measured rather than re-scoped, per msg 20553's
own instruction that *a census that must come out 0 is not a census*.

⛔ **WHAT IS NOT CLAIMED:** this seat has NOT determined whether `kuzu_nessie_db` is loadable, current,
or whether anything would read it in preference to the gateway. `file` reports generic `data`. The
question the criterion is presumably reaching for -- *did a local copy answer instead of the server?* --
is answered NO on independent evidence: the answer carries a SERVER-side `VINTAGE` line and a manifest
id, which a local read would not produce.

## Instrument stability across the merge

`0.0.0_AB_MSTR~Z` measured `.tools/comp-kuzu` byte-identical on `origin/SITEZ` and `origin/CLOUD`
pre-merge and concluded the merge could not change the instrument. That measurement was taken before
`origin/CLOUD` advanced to `c6bcb7b12b`, so this seat did not rest on it and re-measured the blob at the
instant instead. **Both reads agree: `c9677f2051`, unchanged.** msg 20568 independently confirms
`comp-kuzu` was not in the merge's staged diff at all.

⚠ **HEAD DID MOVE under the exercise** -- `cc1748e24e` at 18:50Z, `1a7963cc83` at T0 -- which is why the
per-instant HEAD is recorded. The instrument did not move with it.

## Raw transcript -- T0

```
VINTAGE: Built from the estate as of 2026-09-09 14:59:48 UTC.  [vintage=2026-09-09T14:59:48.778469+00:00 manifest=86ea84674078 prefix=projection/2026-09-09T14:59:48.778469+00:00/]
```

Whole answer: `answer_T0.json` (2,815 bytes, 58 rows), committed beside this file.

## Method note

The asks are fired by a timer armed at 18:5xZ, not by a seat watching a clock, so the 5-second window
does not depend on this session's attention. Two defects were found and fixed in a pre-T0 dry run
rather than at the instant: native Windows Python cannot read an MSYS path (`/c/...`, `/tmp/...`), which
would have silently broken the sha256 step -- fixed by `cd`-ing to the output dir and using a relative
filename; and the gateway `Date` header was confirmed present and parseable before being relied on for
skew.
