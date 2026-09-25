"""HVST-s-1 AC0 -- the BEFORE state, read from S3 AT RUN TIME. READ ONLY."""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import snapshot_lib  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
WORKER = pathlib.Path("lib/opal_data_harvest/worker.py")


def main():
    print("AC0 -- BEFORE state, read live from s3://%s at run time (nothing copied from the task order)"
          % snapshot_lib.store.HARVEST_BUCKET)
    counts, rows = snapshot_lib.snapshot()
    snapshot_lib.print_counts("BEFORE", counts)
    snapshot_lib.dump(HERE / "before.pickle", counts, rows)
    print("BEFORE snapshot rows pickled: %d rows -> %s" % (len(rows), HERE / "before.pickle"))

    print("")
    print("DEPLOYED PERSIST LOCATION -- %s bytes at the `finally` wrapping the per-article loop:" % WORKER)
    lines = WORKER.read_text(encoding="utf-8").splitlines()
    for number in range(218, 250):
        print("%s:%d: %s" % (WORKER, number, lines[number - 1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
