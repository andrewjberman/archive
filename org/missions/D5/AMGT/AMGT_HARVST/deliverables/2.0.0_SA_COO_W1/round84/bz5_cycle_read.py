"""HVST-bz-5 (read only): the FIRST ENDED cycle record of a publisher under the new pin, and how many of its failures name
their reason. A failure NAMES its reason when `detail` is not the bare `status` and carries a `:` (the exception class or
`HTTP <code>` then the message, as HVST-bx-3 writes it). Prints one line; exit 0 when a record was read, 1 when none ended
since `--since`. Writes nothing."""
import argparse
import glob
import json
import os


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-dir", required=True)
    parser.add_argument("--since", required=True, help="UTC ISO time of the new pin's first start, e.g. 2026-10-13T05:52:43Z")
    parser.add_argument("--publisher", default="bbg")
    args = parser.parse_args(argv)
    folder = os.path.join(args.state_dir, "cycles", args.publisher)
    rows = []
    for path in sorted(glob.glob(os.path.join(folder, "*.cycle.json"))):
        try:
            with open(path, encoding="utf-8") as handle:
                record = json.load(handle)
        except ValueError:
            continue
        if str(record.get("started_at", "")) >= args.since and record.get("ended_at"):
            rows.append((str(record["started_at"]), record))
    if not rows:
        print("NO-ENDED-CYCLE-SINCE %s" % args.since)
        return 1
    rows.sort(key=lambda row: row[0])
    record = rows[0][1]
    failures = record.get("failures") or []
    named = [f for f in failures
             if f.get("detail") and f.get("detail") != f.get("status") and ":" in str(f.get("detail"))]
    print("CYCLE=%s STOPPED=%s FAILED=%d NAMED=%d" % (record.get("cycle_id"), record.get("stopped") or "none",
                                                      len(failures), len(named)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
