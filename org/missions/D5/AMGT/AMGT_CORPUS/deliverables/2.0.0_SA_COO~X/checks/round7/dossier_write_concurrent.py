"""AMGT_CORPUS round 7 act B step 2 -- the dossier rewrite, driven concurrently. WRITES (gold puts, never overwrite).

`python -m lib.research.corpus.dossier --write` is `_run_write_all`: a stateless loop of `dossier.write_one` over
`dossier._resolved_security_keys`. This driver calls the SAME function over the SAME key list, concurrently, so the
write set is identical; it exists because the serial loop measured ~2.5 min per name (95 names ~4 h). `write_one` is
resumable by construction: a name already rewritten this date reads its stored inputs equal to fresh inputs and
prints `unchanged ... wrote 0`, so names the serial run already wrote count under `unchanged`.
"""
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from lib.research.corpus import dossier
from lib.research.harvest import store

WORKERS = 10  # processes: the per-name build is CPU-bound (a thread pool measured ~1.8 cores busy)


_CLIENT = None


def _one(key):
    global _CLIENT
    if _CLIENT is None:  # one S3 client per worker process (a boto3 client does not pickle)
        _CLIENT = store._default_client()
    client = _CLIENT
    # write_one prints its own line too; this driver's per-name line is built from the RETURN value, so the tally
    # never depends on interleaved stdout from the worker processes.
    result = dossier.write_one(key, client=client)
    line = "wrote %d inputs_sha16 %s uri %s" % (int(result["wrote"]), result["inputs_sha16"], result["uri"])
    return result, line


def main():
    t0 = time.time()
    client = store._default_client()
    keys = dossier._resolved_security_keys(client=client)
    wrote = unchanged = errors = 0
    with ProcessPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(_one, k): k for k in keys}
        for fut in as_completed(futures):
            key = futures[fut]
            try:
                result, line = fut.result()
            except Exception as exc:  # a failed name is a VALUE to report, never a silent skip
                errors += 1
                print("ERROR: %s %s: %s" % (key, type(exc).__name__, exc), flush=True)
                continue
            if result["wrote"]:
                wrote += 1
            else:
                unchanged += 1
            print("%s %s" % (key, line), flush=True)
    print(
        "names %d wrote %d unchanged %d errors %d elapsed_s %.0f"
        % (len(keys), wrote, unchanged, errors, time.time() - t0),
        flush=True,
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
