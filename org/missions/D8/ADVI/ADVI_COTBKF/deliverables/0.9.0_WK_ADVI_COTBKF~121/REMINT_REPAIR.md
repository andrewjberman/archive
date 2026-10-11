# What an operator now sees when the guarded re-mint fails (CB-bt-3, round 72)

Everything here was shown by tests against a FAKED, versioned bucket (`data/assets/scripts/silver/tests/test_commonwealth_ard_remint.py`). The mode was NOT run against the real bucket and no AWS call was made. The mode deletes nothing and rolls nothing back. The gold producer was not edited. Machine-readable twin: `REMINT_REPAIR.json` beside this page. Code commit: a24adedd5d.

## What it prints, in order

1. Before the first put (after every refusal has passed): `REMINT-BEGIN keys=<n>`, then one `WILL-WRITE s3://...` per key in write order. A refused run prints neither.
2. As each day, the sidecar and the method row complete: the existing `REPLACED ...` lines. A clean run ends with the same `ARD-COTTONWOOD-REMINT ...` line as before and prints no report.
3. On a stop, or on any interruption the process can see: `ERROR: <what stopped>`, then a count line (`N of M planned key(s) were attempted; read back from the bucket after the stop: a WRITTEN, b NOT-WRITTEN, c UNKNOWN`), then one line per key attempted: `WRITTEN s3://...`, `NOT-WRITTEN s3://...` or `UNKNOWN s3://...`, then any `HALF-PAIR s3://.../data.parquet s3://.../manifest.json new=<data|manifest>` lines.

The state of a key is READ, not remembered: after the stop the mode does a HEAD of each key it attempted and compares the version id and ETag with the capture's (the run had just checked the served object equals the capture). Moved = WRITTEN. Unchanged = NOT-WRITTEN. A head that fails (or finds the key absent) = UNKNOWN, never guessed, and never hides the error that stopped the run.

## By kind of failure

| What fails | What the operator sees |
|---|---|
| a put raises (day data, day manifest, sidecar, method-row data, method-row manifest) | `ERROR: writing ... stopped: <reason>`; the key that raised is `NOT-WRITTEN`; every key put before it is `WRITTEN`; keys not yet reached are not named (they are in the WILL-WRITE list) |
| a day's data.parquet lands, its manifest.json put raises (also F10: the ETag does not verify) | data `WRITTEN`, manifest `NOT-WRITTEN`, and `HALF-PAIR <data> <manifest> new=data` |
| the method row's data.parquet lands, its manifest.json put raises | the same, for the method row's two keys |
| a read-back finds the stored object wrong (day data hash, day manifest check, sidecar sha256, method-row data) | the error names the key; both keys of the day / the method row are `WRITTEN` (they did land); no HALF-PAIR, because the pair is whole, it is the content that is wrong |
| the method row's manifest.json is stored wrong, unreadable as JSON, or absent on read-back (NEW: it used to be a success) | exit 1, `ERROR: read-back of the method row s3://.../manifest.json does not match what the producer wrote for its row` (or `found nothing`), all keys `WRITTEN`, no success line |
| the process is interrupted (KeyboardInterrupt, any BaseException) | the same report, labelled `ERROR: the run was interrupted by <Type> before it finished`, then the exception goes on (the shell sees the interrupt) |
| a head fails while the report is being read | that key prints `UNKNOWN`; a pair with an UNKNOWN side prints `PAIR-UNKNOWN <data> <manifest>` instead of a guess; the original error and exit value stand |
| a read fails before the first put (F9) | unchanged: the bond-check line and the exception; nothing was written, so nothing is named |
| a hard kill (SIGKILL, power loss) | NOTHING more can print: no handler runs. The operator has the WILL-WRITE lines printed before the first put and the capture, and compares each listed key's current version id with the capture. Stated in the docstring, the block comment and the `--remint` help text |

## Restore

Unchanged by this repair: a person under the sign-off copies the captured version id of each `WRITTEN` key back over the key (S3 CopyObject with the captured VersionId). `NOT-WRITTEN` keys need nothing. `UNKNOWN` keys must be listed by a person before anything is concluded. A `HALF-PAIR` is restored by restoring its `new=` file.

## Not established

See `not_established` in the JSON: the real bucket, a hard kill, a second writer, a stale head, the exact serialisation the producer uses for the method-row manifest (the comparison refuses when it differs).
