"""CA-j-13: the dell2 reader folder gains two sources, mentions.json and mail_log.json (CTO ruling on call 608c; muse's requested shape).

Prints:  K2-READER ok=<True|False> arms=<n> of 7 failed=<names|none> reason=<text>
Contract (fixed by the issuer; check_k1_records.py pins the assistant's half). data/transcripts/scripts/muse_reader/refresh.py:
  SOURCES gains "mentions" and "mail_log" (after the existing four); make_readers(now_dt) returns a reader for each.
  The readers scan the state table the way read_drafts does (sk "state" rows, "#index#" rows skipped) and read the lists the assistant writes in each row's state JSON:
    mentions  <- state["mentions"] of EVERY object that has one; entries older than 7 days (by `seen_at`) dropped; the items merged, newest `mentioned_at` first; each item is the
                 entry's seven keys plus age_minutes and age_from ("mentioned_at") from with_age.
    mail_log  <- state["mail_log"] of every object that has one; entries older than 7 days (by `considered_at`) dropped; merged, newest `considered_at` first; each item is the entry's
                 seven keys plus "object_id" (the row's pk) plus age_minutes and age_from ("considered_at").
  No row anywhere carries the list -> the reader raises Absent (nothing recorded yet: status absent, items null, never an empty list). A scan failure is unreadable with the error,
  for that source only. Everything is scrubbed on write by the existing scrub() (an address or a key shaped value never reaches a file). README.txt names both files.
Reads no AWS: aws_json is replaced by a fake that returns scan pages.
"""
import datetime
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
REFRESH = ROOT / "data" / "transcripts" / "scripts" / "muse_reader" / "refresh.py"
MENTION_KEYS = {"id", "team", "channel", "from", "snippet", "mentioned_at", "seen_at", "age_minutes", "age_from"}
MAIL_KEYS = {"seq", "tag", "considered_at", "from", "domain", "firm", "subject", "object_id", "age_minutes", "age_from"}
NOW = datetime.datetime(2026, 10, 14, 13, 0, 0, tzinfo=datetime.timezone.utc)
NOW_S = "2026-10-14T13:00:00Z"
ARMS = ("mentions-ok", "mail-log-ok", "absent-not-empty", "unreadable-isolated", "files-and-index", "scrub-on-write", "readme")


def row(pk, state):
    return {"pk": {"S": pk}, "sk": {"S": "state"}, "data": {"S": json.dumps(state)}}


def mention(mid, mentioned_at, seen_at=None, snippet="hello"):
    return {"id": mid, "team": "Team One", "channel": "Chan One", "from": "Sender One", "snippet": snippet, "mentioned_at": mentioned_at,
            "seen_at": seen_at or mentioned_at}


def mail_entry(seq, considered_at, subject="following up"):
    return {"seq": seq, "tag": "M%03d" % seq, "considered_at": considered_at, "from": "Pat Invented", "domain": "example-fund.test", "firm": "invented-firm", "subject": subject}


def main():
    failed, why = [], ""
    try:
        spec = importlib.util.spec_from_file_location("refresh_under_check", REFRESH)
        R = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(R)
        scan = {"rows": [], "fail": False}

        def fake_aws(args):
            if scan["fail"]:
                raise R.AwsError("scan refused (simulated)")
            if args[:2] == ["dynamodb", "scan"]:
                return json.dumps({"Items": scan["rows"], "ScannedCount": len(scan["rows"])})
            raise R.AwsError("unexpected call %s" % args[:2])

        R.aws_json = fake_aws
        stubs = {n: (lambda: []) for n in ("open_calls", "drafts", "eod_today", "sprint_today")}
        D = datetime.timedelta
        iso = lambda dt: dt.strftime("%Y-%m-%dT%H:%M:%SZ")  # noqa: E731

        def arm(name, fn):
            try:
                if not fn():
                    failed.append(name)
            except Exception as exc:
                failed.append("%s(%s: %s)" % (name, type(exc).__name__, str(exc)[:70]))

        def seed_ok():
            scan["fail"] = False
            scan["rows"] = [
                row("chan:t1|c1|root1", {"mentions": [mention("t1|c1|m1", "2026-10-14T12:50:00Z"), mention("t1|c1|m0", "2026-10-14T12:00:00Z")]}),
                row("chan:t1|c2|root2", {"mentions": [mention("t1|c2|m2", "2026-10-14T12:30:00Z")]}),
                row("chan:t1|c3|root3", {"mentions": [mention("t1|c3|old", "2026-10-05T12:00:00Z", seen_at=iso(NOW - D(days=8)))]}),
                row("#index#sms-tag", {"x": 1}),
                row("19:chat@unq.gbl.spaces", {"pending": {"tag": "C001"}}),
                row("mail:owner", {"mail_log": [mail_entry(1, iso(NOW - D(days=8))), mail_entry(2, "2026-10-14T12:10:00Z"), mail_entry(3, "2026-10-14T12:40:00Z", "second")]}),
            ]

        def mentions_ok():
            seed_ok()
            items = R.make_readers(NOW)["mentions"]()
            return ([i["id"] for i in items] == ["t1|c1|m1", "t1|c2|m2", "t1|c1|m0"] and all(set(i) == MENTION_KEYS for i in items)
                    and [i["age_minutes"] for i in items] == [10, 30, 60] and all(i["age_from"] == "mentioned_at" for i in items))

        def mail_log_ok():
            seed_ok()
            items = R.make_readers(NOW)["mail_log"]()
            return ([i["seq"] for i in items] == [3, 2] and all(set(i) == MAIL_KEYS for i in items) and all(i["object_id"] == "mail:owner" for i in items)
                    and [i["age_minutes"] for i in items] == [20, 50] and all(i["age_from"] == "considered_at" for i in items))

        def absent_not_empty():
            scan["fail"] = False
            scan["rows"] = [row("19:chat@unq.gbl.spaces", {"pending": {"tag": "C001"}}), row("#index#sms-tag", {"x": 1})]
            readers = R.make_readers(NOW)
            out = []
            for name in ("mentions", "mail_log"):
                try:
                    readers[name]()
                    out.append(False)
                except R.Absent:
                    out.append(True)
            with tempfile.TemporaryDirectory() as tmp:
                docs = R.refresh(tmp, dict(stubs, mentions=readers["mentions"], mail_log=readers["mail_log"]), NOW_S)
            return all(out) and docs["mentions"]["status"] == "absent" and docs["mentions"]["items"] is None and docs["mail_log"]["status"] == "absent"

        def unreadable_isolated():
            scan["fail"] = True
            scan["rows"] = []
            readers = R.make_readers(NOW)
            with tempfile.TemporaryDirectory() as tmp:
                docs = R.refresh(tmp, dict(stubs, mentions=readers["mentions"], mail_log=readers["mail_log"]), NOW_S)
            scan["fail"] = False
            return (docs["mentions"]["status"] == "unreadable" and docs["mentions"]["items"] is None and bool(docs["mentions"]["error"])
                    and docs["mail_log"]["status"] == "unreadable" and docs["drafts"]["status"] == "ok" and docs["open_calls"]["status"] == "ok")

        def files_and_index():
            seed_ok()
            readers = R.make_readers(NOW)
            if "mentions" not in R.SOURCES or "mail_log" not in R.SOURCES or "mentions" not in readers or "mail_log" not in readers:
                return False
            with tempfile.TemporaryDirectory() as tmp:
                R.refresh(tmp, dict(stubs, mentions=readers["mentions"], mail_log=readers["mail_log"]), NOW_S)
                m = json.loads((Path(tmp) / "mentions.json").read_text(encoding="utf-8"))
                ml = json.loads((Path(tmp) / "mail_log.json").read_text(encoding="utf-8"))
                idx = json.loads((Path(tmp) / "INDEX.json").read_text(encoding="utf-8"))
            return (m["source"] == "mentions" and m["status"] == "ok" and len(m["items"]) == 3 and ml["source"] == "mail_log" and ml["status"] == "ok"
                    and len(ml["items"]) == 2 and {"mentions", "mail_log"} <= set(idx["sources"]) and len(idx["sources"]) == 6)

        def scrub_on_write():
            scan["fail"] = False
            scan["rows"] = [row("chan:t1|c1|root1", {"mentions": [mention("t1|c1|m1", "2026-10-14T12:50:00Z", snippet="key AKIAIOSFODNN7EXAMPLE mail pat@example-fund.test")]})]
            readers = R.make_readers(NOW)
            with tempfile.TemporaryDirectory() as tmp:
                R.refresh(tmp, dict(stubs, mentions=readers["mentions"], mail_log=lambda: []), NOW_S)
                blob = (Path(tmp) / "mentions.json").read_text(encoding="utf-8")
            return "AKIAIOSFODNN7EXAMPLE" not in blob and "pat@example-fund.test" not in blob

        def readme():
            return "mentions.json" in R.README and "mail_log.json" in R.README

        for name, fn in zip(ARMS, (mentions_ok, mail_log_ok, absent_not_empty, unreadable_isolated, files_and_index, scrub_on_write, readme)):
            arm(name, fn)
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
        failed.append("harness")
    print("K2-READER ok=%s arms=%d of %d failed=%s reason=%s" % (not failed, 0 if "harness" in failed else len(ARMS) - len(failed), len(ARMS), ";".join(failed) or "none", why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
