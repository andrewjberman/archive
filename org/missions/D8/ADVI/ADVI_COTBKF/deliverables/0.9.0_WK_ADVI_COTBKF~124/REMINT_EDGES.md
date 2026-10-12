# REMINT_EDGES -- what an operator sees when another writer got in (TO-CB-bu-2, round 73)

Record: `REMINT_EDGES.json` beside this file. Code: `data/assets/scripts/silver/commonwealth_account_return_daily.py` @933ad24673. Faked bucket only; the mode was not run against a real one, deletes nothing, and the producer and `lib/` were not edited.

**Refused before the put, tested on a fake.** Every put of a planned key carries `IfMatch=<the captured ETag>`. If another writer changed the key after the capture check, the bucket refuses the put (412) and stores nothing. The run stops with exit 1. The producer's put path is `put_object(Bucket, Key, Body)` for every object, so the condition rides the producer's own call. Whether the real bucket honors it is not established (see the JSON).

**What is printed** (one line per key, `<STATE> s3://bucket/key`):

```
ERROR: writing 2026-06-17 stopped: the served object s3://<bucket>/<key>/manifest.json changed after the capture check (precondition failed: its ETag is no longer the one the capture holds); the put was refused and nothing was stored for it
ERROR: nothing was deleted and no rollback was attempted; 2 of 7 planned key(s) were attempted; read back from the bucket after the stop: 1 WRITTEN, 0 NOT-WRITTEN, 0 UNKNOWN, 1 CHANGED-BY-ANOTHER-WRITER (roll back the WRITTEN keys from the capture, by a person under the sign-off):
WRITTEN s3://<bucket>/<key>/data.parquet
CHANGED-BY-ANOTHER-WRITER s3://<bucket>/<key>/manifest.json
PAIR-OTHER-WRITER s3://<bucket>/<key>/data.parquet s3://<bucket>/<key>/manifest.json data=WRITTEN manifest=CHANGED-BY-ANOTHER-WRITER
NOTE: CHANGED-BY-ANOTHER-WRITER = ...
```

- `WRITTEN`: a put of this run returned, and the key is still that version.
- `CHANGED-BY-ANOTHER-WRITER`: the key's version moved and no put of this run returned for it. It is never printed as this run's write. Read what is there before any restore. (Rarely, a put that landed and whose reply was lost reads the same; the note says so.)
- `WRITTEN-THEN-CHANGED`: this run's put returned and the key has moved again since. Restoring it from the capture would also discard that other writer's object.
- `PAIR-OTHER-WRITER`: a day (or the method row) with a side another writer changed. It is not a `HALF-PAIR`, because no new file of this run's is claimed for that side.
- `NOT-WRITTEN`: the key is still at the capture's version.

**Not covered.** An identical-bytes rewrite in the gap keeps the ETag, so the put passes and is this run's write (same content either way). A writer after this run's put is seen only if a stop triggers the report; a clean run makes no check after its puts.

**The hard kill is its own failure point (F8k), not described.** An uncaught exception (F8) is reported per key and re-raised. A kill (SIGKILL, power loss) runs no handler and prints nothing: the operator has the `REMINT-BEGIN` and `WILL-WRITE` lines printed before the first put, and the capture. The help text, the `remint_days` docstring and the block comment say the same.
