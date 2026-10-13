"""HVST-bz-11 (read only): has the refresh closed Z-S119 for each of wsj and barrons?

For each publisher, over the cycles that STARTED at or after `--since` (the new pin's start), exactly one verdict:
  ALIVE                one ENDED cycle record with completed true and stopped none (the session lasted a full cycle);
  NON_EXPIRY:<class>   a REFUSAL in a cycle checkpoint whose class is not `expired` (blocked, entitlement or other):
                       the refresh cannot fix that, and naming it is the finding;
  REFRESH_FAILED       a checkpoint records the one refresh as `failed`;
  NOT_CURED            a checkpoint records the refresh `done` and still holds two or more `expired` refusals of that
                       publisher (the refresh did not hold);
  WAITING              none of the above yet.
The last line is CLOSE=MET when both publishers are ALIVE or NON_EXPIRY, CLOSE=NOT_MET when either is REFRESH_FAILED or
NOT_CURED, else CLOSE=WAITING. Exit 0 always (the criterion reads the lines). Writes nothing; reads no session or credential."""
import argparse
import glob
import json
import os

PUBLISHERS = ("wsj", "barrons")


def load(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return None


def cycles(state_dir, publisher, since):
    """[(cycle_id, record_or_None, checkpoint_or_None)] for cycles started at or after `since`, oldest first."""
    folder = os.path.join(state_dir, "cycles", publisher)
    found = {}
    for path in glob.glob(os.path.join(folder, "*.cycle.json")):
        record = load(path)
        if isinstance(record, dict) and str(record.get("started_at", "")) >= since:
            found[os.path.basename(path)[:-len(".cycle.json")]] = [record, None]
    for path in glob.glob(os.path.join(folder, "*.checkpoint.json")):
        cycle_id = os.path.basename(path)[:-len(".checkpoint.json")]
        checkpoint = load(path)
        if not isinstance(checkpoint, dict):
            continue
        if cycle_id in found:
            found[cycle_id][1] = checkpoint
        elif cycle_id >= since.replace("-", "").replace(":", ""):  # a running cycle has a checkpoint and no record yet
            found[cycle_id] = [None, checkpoint]
    return [(cid, rec, ck) for cid, (rec, ck) in sorted(found.items())]


def verdict(state_dir, publisher, since):
    rows = cycles(state_dir, publisher, since)
    for _cid, record, _ck in rows:
        if record and record.get("ended_at") and record.get("completed") is True and not record.get("stopped"):
            return "ALIVE"
    for _cid, _rec, checkpoint in rows:
        for refusal in (checkpoint or {}).get("refusals") or []:
            if refusal.get("publisher") == publisher and refusal.get("class") not in (None, "expired"):
                return "NON_EXPIRY:%s" % refusal.get("class")
    for _cid, _rec, checkpoint in rows:
        outcome = ((checkpoint or {}).get("refreshes") or {}).get(publisher, {}).get("outcome")
        if outcome == "failed":
            return "REFRESH_FAILED"
    for _cid, _rec, checkpoint in rows:
        outcome = ((checkpoint or {}).get("refreshes") or {}).get(publisher, {}).get("outcome")
        expired = [r for r in (checkpoint or {}).get("refusals") or []
                   if r.get("publisher") == publisher and r.get("class") == "expired"]
        if outcome == "done" and len(expired) >= 2:
            return "NOT_CURED"
    return "WAITING"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", required=True)
    parser.add_argument("--since", help="UTC ISO, e.g. 2026-10-14T01:00:00Z (the new pin's start)")
    parser.add_argument("--t0-file", help="a file holding one line T0=<UTC ISO>, written by the seat just before it starts the task")
    args = parser.parse_args(argv)
    since = args.since
    if args.t0_file:
        try:
            with open(args.t0_file, encoding="utf-8") as handle:
                text = handle.read()
        except OSError:
            print("CLOSE=WAITING reason=no-t0-file")
            return 0
        found = [line.split("=", 1)[1].strip() for line in text.splitlines() if line.startswith("T0=")]
        since = found[0] if found else None
    if not since:
        print("CLOSE=WAITING reason=no-since")
        return 0
    verdicts = {}
    for publisher in PUBLISHERS:
        verdicts[publisher] = verdict(args.state_dir, publisher, since)
        print("PUBLISHER=%s VERDICT=%s" % (publisher, verdicts[publisher]))
    if any(v in ("REFRESH_FAILED", "NOT_CURED") for v in verdicts.values()):
        close = "NOT_MET"
    elif all(v == "ALIVE" or v.startswith("NON_EXPIRY:") for v in verdicts.values()):
        close = "MET"
    else:
        close = "WAITING"
    print("CLOSE=%s" % close)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
