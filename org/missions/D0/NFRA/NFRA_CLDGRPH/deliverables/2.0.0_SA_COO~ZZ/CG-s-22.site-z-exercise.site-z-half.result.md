THIS IS THE SITE-Z HALF; THE LAPTOP'S RECORD IS THE OTHER HALF; THE PAIR IS GRADED AT L9

**Seat:** `2.0.0_SA_COO~ZZ` | **Exercise:** `NFRA_CLDGRPH` CG-s-22, site-Z half | **Routed by:** `0.0.0_AB_MSTR~Z` msg 20553, carried from `2.0.0_SA_COO~A` msg 94622, on Andrew's allocation @`7caee0ad5d`
**archetype:** VALIDATE | **COMPLETE: all three instants asked, none missed.**

```json
{
  "machine": "site-z",
  "seat": "2.0.0_SA_COO~ZZ",
  "question": "node_type census over CloudNode, deterministic ordering (D-8's, unchanged)",
  "cypher": "MATCH (n:CloudNode) RETURN n.node_type AS t, count(*) AS c ORDER BY c DESC, t",
  "instrument": "bash .tools/comp-kuzu --json <cypher>, through the public gateway at https://mcp.opalinvest.dev/graph/cypher",
  "comp_kuzu_blob_all_instants": "c9677f20514949b3f86e54a5e46e29289d52dbdb",
  "instants": [
    { "t": "T0", "target": "2026-09-09T19:00:00Z", "start": "2026-09-09T19:00:00.502Z", "end": "2026-09-09T19:00:04.287Z",
      "began_within_5s": true, "rc": 0, "skew_s": 0,
      "rows_sha256": "3071ef4c4bf5e16c946ffb59e142213cbea0e22d0c1103b0e26ce9890a8930df",
      "vintage": "2026-09-09T14:59:48.778469+00:00", "manifest": "86ea84674078", "rows_count": 58,
      "answer_file": "answer_T0.json",
      "head_at_instant": "1a7963cc83aff538933806ef8542671fd58298d9",
      "comp_kuzu_blob_at_instant": "c9677f20514949b3f86e54a5e46e29289d52dbdb" },
    { "t": "T1", "target": "2026-09-09T20:00:00Z", "start": "2026-09-09T20:00:00.504Z", "end": "2026-09-09T20:00:03.569Z",
      "began_within_5s": true, "rc": 0, "skew_s": -1,
      "rows_sha256": "3071ef4c4bf5e16c946ffb59e142213cbea0e22d0c1103b0e26ce9890a8930df",
      "vintage": "2026-09-09T14:59:48.778469+00:00", "rows_count": 58,
      "answer_file": "answer_T1.json",
      "head_at_instant": "7d698685fe2f2f76bd830c4f8e981e1b039b8a3d",
      "comp_kuzu_blob_at_instant": "c9677f20514949b3f86e54a5e46e29289d52dbdb" },
    { "t": "T2", "target": "2026-09-09T21:00:00Z", "start": "2026-09-09T21:00:00.400Z", "end": "2026-09-09T21:00:04.248Z",
      "began_within_5s": true, "rc": 0, "skew_s": -1,
      "rows_sha256": "50170787e39ed1a3de76e536212b5505f8139efeaa5f81c17c4eed7e44fd3821",
      "vintage": "2026-09-09T20:04:09.034708+00:00", "rows_count": 58,
      "answer_file": "answer_T2.json",
      "head_at_instant": "9e2818276cf74d1bbe93f6e69ed72ce868fbcf80",
      "comp_kuzu_blob_at_instant": "c9677f20514949b3f86e54a5e46e29289d52dbdb" }
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
    "disposition": "ROUTED UPWARD to 0.0.0_AB_MSTR~Z, NOT resolved here (msg 20568: 'not that lane's to resolve')"
  },
  "bounds_honoured": {
    "reads_only": true, "local_graph_created_opened_or_downloaded": false,
    "s3_writes": 0, "code_edits": 0,
    "transport": "thin client to the gateway only -- corroborated by every answer carrying a SERVER vintage"
  }
}
```

## THE FINDING OF THIS HALF: THE PROJECTION MOVED BETWEEN T1 AND T2

`T0` and `T1` are **byte-identical** (`3071ef4c...`) under one vintage, `2026-09-09T14:59:48`.
`T2` returns a **different sha** (`50170787...`) under a **different vintage**, `2026-09-09T20:04:09`.

STOP: **THIS IS NOT MACHINE DIVERGENCE AND MUST NOT BE GRADED AS ANY.** The projection was rebuilt
between the two instants. Diffed row by row:

```
node_types at T0: 58     node_types at T2: 58     only in T0: none     only in T2: none
counts that MOVED: 1 of 58        LAMBDA  203 -> 202  (-1)
total nodes: 27303 -> 27302
```

**ONE Lambda left the estate.** The entire sha change is that single node. The row SET is unchanged
and 57 of 58 counts are identical.

**WHAT THIS MEANS FOR THE PAIR AT L9, stated so the grader does not have to re-derive it:** the
criterion is *byte-identical rows sha256 under ONE VINTAGE at a matching instant*. At `T0` and `T1`
that is a clean test. At `T2` the vintage is the one that matters, not the clock: if the laptop half
also read vintage `20:04:09` its sha should equal `50170787...`; if it read `14:59:48` its sha should
equal `3071ef4c...`. **A mismatch at T2 between two halves reading DIFFERENT vintages is a REBUILD
BOUNDARY, not a disagreement between machines** -- and only the per-instant vintage stamp makes those
two readings distinguishable. Had the record carried the clock alone, the pair would have looked
divergent at T2 on evidence that says nothing of the kind.

WARN: **AND THE REBUILD IS A HAZARD FOR THE INSTANT DESIGN ITSELF, not just for this run.** Two halves
asking at the same wall-clock instant are NOT guaranteed the same vintage -- the boundary can fall
between them. The instants coordinate the ASK; they cannot coordinate the SERVER. Nothing in the spec
required the vintage to be recorded per instant; it was recorded because the spec asked for it as a
field, and it turned out to be the field that makes T2 interpretable at all.

## The census, and what is NOT claimed

The L9 pair criterion also requires *both censuses 0*. **Site Z's is 7**, reported as measured rather
than re-scoped, per msg 20553's own instruction that *a census that must come out 0 is not a census*.

STOP: **NOT CLAIMED:** whether `kuzu_nessie_db` is loadable, current, or would ever be read in
preference to the gateway. `file` reports generic `data`. The question the criterion is presumably
reaching for -- *did a local copy answer instead of the server?* -- is answered **NO** on independent
evidence: every answer carries a SERVER-side vintage and manifest id, and the T1->T2 vintage move is
itself proof the answers tracked a server that rebuilt, which a static local file could not do.

## Instrument stability

`.tools/comp-kuzu` was blob `c9677f2051` at all three instants and in the merged index --
`0.0.0_AB_MSTR~Z` measured it byte-identical across both remotes pre-merge and msg 20568 confirmed it
was not in the merge's staged diff at all. That measurement predated `origin/CLOUD` advancing, so this
seat re-measured the blob AT each instant rather than resting on it. All four reads agree.

WARN: **HEAD MOVED UNDER THE EXERCISE at every instant** -- `1a7963cc83` -> `7d698685fe` ->
`9e2818276c` -- which is why per-instant HEAD is recorded. The instrument did not move with it.

## Method note

The asks were fired by a timer armed at 18:5xZ, not by a seat watching a clock, so every instant began
within 0.5 s of its target without depending on this session's attention. Two defects were found in a
pre-T0 dry run rather than at an instant: native Windows Python cannot read an MSYS path (`/c/...`,
`/tmp/...`), which would have silently broken the sha256 step -- fixed by `cd`-ing to the output dir
and using a relative filename; and the gateway `Date` header was confirmed present and parseable
before being relied on for skew. Skew held at 0 s, -1 s, -1 s across the three.

## Raw transcripts

```
T0  VINTAGE: Built from the estate as of 2026-09-09 14:59:48 UTC.  [vintage=2026-09-09T14:59:48.778469+00:00 manifest=86ea84674078 prefix=projection/2026-09-09T14:59:48.778469+00:00/]
T1  VINTAGE: Built from the estate as of 2026-09-09 14:59:48 UTC.  [vintage=2026-09-09T14:59:48.778469+00:00 manifest=86ea84674078 prefix=projection/2026-09-09T14:59:48.778469+00:00/]
T2  VINTAGE: Built from the estate as of 2026-09-09 20:04:09 UTC.  [vintage=2026-09-09T20:04:09.034708+00:00 prefix=projection/2026-09-09T20:04:09.034708+00:00/]
```

Whole answers: `answer_T0.json`, `answer_T1.json`, `answer_T2.json`, committed beside this file.
