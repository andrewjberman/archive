"""HVST-bz-7 (read only): for each of wsj and barrons, the newest ENDED cycle record since the cut, and whether it COMPLETED.
One line per publisher; `NONE` when no record ended since `--since`. Exit 0 always (the criterion reads the lines).
Writes nothing and reads no session or credential."""
import argparse
import glob
import json
import os

PUBLISHERS = ("wsj", "barrons")


def newest(state_dir, publisher, since):
    rows = []
    for path in sorted(glob.glob(os.path.join(state_dir, "cycles", publisher, "*.cycle.json"))):
        try:
            with open(path, encoding="utf-8") as handle:
                record = json.load(handle)
        except ValueError:
            continue
        if str(record.get("started_at", "")) >= since and record.get("ended_at"):
            rows.append((str(record["started_at"]), record))
    return max(rows, key=lambda row: row[0])[1] if rows else None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", required=True)
    parser.add_argument("--since", required=True, help="UTC ISO, e.g. 2026-10-13T08:09:08Z (the windowless pin's start)")
    args = parser.parse_args(argv)
    for publisher in PUBLISHERS:
        record = newest(args.state_dir, publisher, args.since)
        if record is None:
            print("PUBLISHER=%s NONE" % publisher)
            continue
        print("PUBLISHER=%s CYCLE=%s COMPLETED=%s STOPPED=%s ASKED=%s NEW=%s FAILED=%s" % (
            publisher, record.get("cycle_id"), bool(record.get("completed")), record.get("stopped") or "none",
            record.get("asked"), record.get("new"), record.get("failed")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
