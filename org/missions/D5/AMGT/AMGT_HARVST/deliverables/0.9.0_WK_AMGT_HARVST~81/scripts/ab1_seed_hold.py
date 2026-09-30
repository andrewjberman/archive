"""HVST-ab-1 change 3: seed a key rejected BEFORE `rejected_hold` existed into the hold, through the
hold's OWN rule -- never a hand-typed row.

DERIVATION. A key was body-rejected in a job when, in the runtime `events.jsonl`, a `job_finished`
event's result file (`runs/<name>.json`) lists the key in `fetched_keys`, does not list it among the
accepted `article_key`s, and records a `rejected` entry carrying the hold's reason
(`worker.HOLD_REASON`, `short_or_partial_body`). Where a result carries `fetch_outcomes`, that
outcome is read instead. A request-level rejection (a 403, `request_rejected`, a fetch that recorded
no outcome) is NOT a body rejection and adds no failed day.

THE RULE. Each distinct UTC day of a body rejection is replayed, oldest first, through
`Worker._hold_on_rejection` on a scratch Worker (`failed_days` +1 per new day, `state` =
`rejected_final` at `HOLD_FINAL_AFTER_DAYS`, else `held`). The one resulting row is inserted into the
runtime `rejected_hold` with INSERT OR IGNORE: a second run finds the row and changes nothing.

No network, no S3. The ONE write is that one row.
"""

import datetime as dt
import json
import sqlite3
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[8]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from lib.opal_data_harvest import worker as worker_module  # noqa: E402

RUNTIME_ROOT = Path("C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest")
SEED_KEY = "bbg:NM5NLQ6K50XZ01"
COLUMNS = ("fetch_key", "reason", "failed_days", "last_failed_day", "state")


def _events(root):
    path = Path(root) / "events.jsonl"
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            yield index, json.loads(line)
        except ValueError:
            continue


def _utc_day(text):
    stamp = dt.datetime.fromisoformat(text)
    return (stamp.astimezone(dt.timezone.utc) if stamp.tzinfo else stamp).date()


def _body_rejected(result, fetch_key):
    """True when `result` (one job's result file) records `fetch_key` as rejected for its body."""
    outcome = (result.get("fetch_outcomes") or {}).get(fetch_key)
    if outcome is not None:
        return outcome.get("outcome") == "rejected" and worker_module.HOLD_REASON in (outcome.get("issues") or [])
    fetched = result.get("fetched_keys") or []
    accepted = {a.get("article_key") for a in (result.get("accepted") or [])}
    rejected = result.get("rejected") or []
    unaccounted = [key for key in fetched if key not in accepted]
    body = [r for r in rejected if worker_module.HOLD_REASON in (r.get("issues") or [])]
    # the join is by counting, so it holds only where it is unambiguous: every unaccounted fetch is
    # matched by exactly one body rejection and the job records no other kind of rejection
    return (fetch_key in unaccounted and len(body) > 0 and len(body) == len(unaccounted)
            and len(rejected) == len(body))


def body_rejection_evidence(root, fetch_key):
    """[{day, event_index, job_result, job_id}] -- one per job whose result records a body rejection."""
    root = Path(root)
    publisher = fetch_key.split(":", 1)[0]
    found = []
    for index, event in _events(root):
        if event.get("event") != "job_finished" or event.get("publisher") != publisher or not event.get("result"):
            continue
        result_path = root / "runs" / Path(str(event["result"]).replace("\\", "/")).name
        if not result_path.exists():
            continue
        result = json.loads(result_path.read_text(encoding="utf-8"))
        if _body_rejected(result, fetch_key):
            found.append({"day": _utc_day(event["at"]).isoformat(), "event_index": index,
                          "job_result": result_path.name, "job_id": result.get("job_id")})
    return found


def derive_row(root, fetch_key):
    """The hold row `fetch_key`'s recorded body rejections produce under the hold's own rule, or None."""
    evidence = body_rejection_evidence(root, fetch_key)
    if not evidence:
        return None, evidence
    with tempfile.TemporaryDirectory() as scratch:
        scratch_worker = worker_module.Worker(scratch, {}, publisher_factory=None, session_manager=object())
        try:
            for day in sorted({e["day"] for e in evidence}):
                scratch_worker._utc_today = lambda day=day: dt.date.fromisoformat(day)
                scratch_worker._hold_on_rejection(fetch_key, [worker_module.HOLD_REASON])
            row = scratch_worker.db.execute(
                "SELECT %s FROM rejected_hold WHERE fetch_key=?" % ",".join(COLUMNS), (fetch_key,)).fetchone()
        finally:
            scratch_worker.close()
    return dict(zip(COLUMNS, row)), evidence


def read_row(root, fetch_key):
    db = sqlite3.connect(str(Path(root) / "progress.sqlite3"), timeout=30)
    try:
        row = db.execute("SELECT %s FROM rejected_hold WHERE fetch_key=?" % ",".join(COLUMNS),
                         (fetch_key,)).fetchone()
    finally:
        db.close()
    return dict(zip(COLUMNS, row)) if row else None


def apply_row(root, row):
    """INSERT OR IGNORE the derived row into `root`'s progress.sqlite3. Returns (before, after)."""
    before = read_row(root, row["fetch_key"])
    db = sqlite3.connect(str(Path(root) / "progress.sqlite3"), timeout=30)
    try:
        db.execute("INSERT OR IGNORE INTO rejected_hold(%s) VALUES(?,?,?,?,?)" % ",".join(COLUMNS),
                   tuple(row[c] for c in COLUMNS))
        db.commit()
    finally:
        db.close()
    return before, read_row(root, row["fetch_key"])


def seed(root, fetch_key):
    row, evidence = derive_row(root, fetch_key)
    if row is None:
        raise SystemExit("no recorded body rejection for %s under %s" % (fetch_key, root))
    before, after = apply_row(root, row)
    return {"derived": row, "evidence": evidence, "before": before, "after": after}


def main():
    result = seed(RUNTIME_ROOT, SEED_KEY)
    print("evidence (body rejections in the runtime events.jsonl -> job result):")
    for item in result["evidence"]:
        print("  ", json.dumps(item))
    print("derived by Worker._hold_on_rejection (HOLD_FINAL_AFTER_DAYS=%d): %s"
          % (worker_module.HOLD_FINAL_AFTER_DAYS, json.dumps(result["derived"])))
    print("rejected_hold row BEFORE:", json.dumps(result["before"]))
    print("rejected_hold row AFTER: ", json.dumps(result["after"]))
    return result


if __name__ == "__main__":
    main()
