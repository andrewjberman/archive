"""AMGT_RESAPP round 77 -- AMGT-ba-3 checks (FWD-14 data half: the lists' named owner and the out-of-date statement).

  python r77_ba3.py --crit AC1|AC2|AC3

AC1 (build): both committed list files and the generator name the owner (Andrew) with owner_status ASSIGNED; the review
    date and the entry counts are UNCHANGED (a review date is the owner's act, not this cell's).
AC2 (build, plant): `lib.research.lists.owner_line.lists_statement(register, now)` returns a plain owner line and a plain
    out-of-date statement: a list past its review interval says it is out of date and since when; a list in date says so;
    an unreadable register still returns words, never an empty string.
AC3 (bound): no alert is built: the lists package imports and calls no mail, topic, queue or schedule client.

Prints PASS/FAIL clause lines and `R77 BA3 <CRIT> SERVED: YES|NO`; exit 0 on YES.
"""
import argparse
import datetime
import glob
import importlib
import json
import os
import re
import sys

LISTS_DIR = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~5/lists"
# The values at the round-77 cut (shared tree HEAD): a change to either is outside this cell.
BASE = {"publishers": {"reviewed_at": "2026-09-10T22:42Z", "entries": 2, "review_interval_days": 90},
        "social_accounts": {"reviewed_at": "2026-09-10T22:42Z", "entries": 267, "review_interval_days": 30}}
ALERT_WORDS = re.compile(r"\b(sns|ses|sqs|send_email|send_raw_email|publish\(|put_rule|create_schedule|smtplib|"
                         r"put_metric_alarm|scheduler)\b")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print("{0} {1} {2}".format("PASS" if cond else "FAIL", name, detail))

    def verdict():
        yes = bool(ok) and all(ok)
        print("R77 BA3 {0} SERVED: {1}".format(a.crit, "YES" if yes else "NO"))
        return 0 if yes else 1

    if a.crit == "AC3":
        hits = []
        files = sorted(glob.glob("lib/research/lists/*.py"))
        for path in files:
            with open(path, encoding="utf-8") as fh:
                for n, line in enumerate(fh, 1):
                    code = line.split("#", 1)[0]
                    if ALERT_WORDS.search(code) and ("import" in code or "client(" in code or "(" in code):
                        hits.append("{0}:{1}".format(path, n))
        print("   lists package: {0} module(s) read; alert-shaped lines {1} {2}".format(len(files), len(hits), hits[:3]))
        clause("C1 the lists package builds no alert, mail, topic, queue or schedule", files and not hits,
               "{0}".format(len(hits)))
        return verdict()

    if a.crit == "AC1":
        seen = {}
        for name, base in BASE.items():
            path = os.path.join(LISTS_DIR, name + ".json")
            with open(path, encoding="utf-8") as fh:
                doc = json.load(fh)
            seen[name] = doc
            print("   {0}: owner {1!r}; owner_status {2}; reviewed_at {3}; entries {4}; interval {5}".format(
                name, str(doc.get("owner"))[:40], doc.get("owner_status"), doc.get("reviewed_at"),
                len(doc.get("entries") or []), doc.get("review_interval_days")))
        clause("C1 both lists name Andrew as owner, status ASSIGNED", all(
            d.get("owner_status") == "ASSIGNED" and "Andrew" in str(d.get("owner"))
            and "UNASSIGNED" not in str(d.get("owner")) for d in seen.values()))
        clause("C2 the review dates, intervals and entry counts are unchanged", all(
            seen[n].get("reviewed_at") == b["reviewed_at"] and len(seen[n].get("entries") or []) == b["entries"]
            and seen[n].get("review_interval_days") == b["review_interval_days"] for n, b in BASE.items()))
        from lib.research.lists import build_lists

        built = build_lists.build_publishers("2026-01-01T00:00Z")
        clause("C3 the generator emits the same owner, so a regenerate does not undo it",
               built.get("owner_status") == "ASSIGNED" and "Andrew" in str(built.get("owner")),
               "{0!r}".format(str(built.get("owner"))[:40]))
        return verdict()

    try:
        owner_line = importlib.import_module("lib.research.lists.owner_line")
    except Exception as err:  # noqa: BLE001 -- absent at the base: the build check FAILS here
        clause("C0 lib.research.lists.owner_line imports", False, "{0}: {1}".format(type(err).__name__, err))
        return verdict()
    now = datetime.datetime(2026, 10, 7, 12, 0, tzinfo=datetime.timezone.utc)

    def entry(reviewed, interval, owner="Andrew", status="ASSIGNED"):
        return {"owner": owner, "owner_status": status, "reviewed_at": reviewed, "review_interval_days": interval,
                "entries_total": 5, "entries_stale": 0, "list_stale": False}

    register = {"lists": {"publishers": entry("2026-09-10T22:42Z", 90),          # 27 days old of 90: in date
                          "social_accounts": entry("2026-06-01T00:00Z", 30)}}    # 128 days old of 30: out of date
    got = owner_line.lists_statement(register, now)
    print("   plant: owner_line {0!r}".format(got.get("owner_line")))
    print("   plant: out_of_date {0!r}".format(got.get("out_of_date")))
    text = str(got.get("out_of_date") or "")
    clause("C1 the owner line names the owner in plain words", isinstance(got.get("owner_line"), str)
           and "Andrew" in got.get("owner_line") and "UNASSIGNED" not in got.get("owner_line"))
    clause("C2 the list past its interval is called out of date, with the day it fell due", "social" in text.lower()
           and "out of date" in text.lower() and "2026-07-01" in text)
    clause("C3 the list in date is said to be in date", "publisher" in text.lower()
           and ("in date" in text.lower() or "up to date" in text.lower()))
    empty = owner_line.lists_statement({"lists": {}}, now)
    print("   plant (no list read): owner_line {0!r}; out_of_date {1!r}".format(empty.get("owner_line"),
                                                                              empty.get("out_of_date")))
    clause("C4 a register with no list read still returns words", all(
        isinstance(empty.get(k), str) and len(empty.get(k)) > 10 for k in ("owner_line", "out_of_date")))
    banned = ("rot", "register", "stale_count", "entries_stale")
    clause("C5 the words a person reads carry no internal term", not any(
        re.search(r"\b{0}\b".format(w), (str(got.get("owner_line")) + " " + text).lower()) for w in banned))
    return verdict()


if __name__ == "__main__":
    sys.exit(main())
