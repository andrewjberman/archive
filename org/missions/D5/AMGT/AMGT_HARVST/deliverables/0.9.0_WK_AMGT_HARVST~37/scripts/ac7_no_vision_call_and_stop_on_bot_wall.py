#!/usr/bin/env python3
"""HVST-w-2 AC7 (guard b) -- read from the CAPTURE run's own record after AC1 (and the AC2 upload leg): vision-model
calls, verification repairs, re-authentications and browsers started must all be 0, and if any job met a bot wall or
VerificationRequired the run must have STOPPED there. OFFLINE: reads w2_ac1_state.json, w2_ac2_upload.json, the
receipts AC1 recorded and the producer's events.jsonl window. Nothing is called.
"""
import datetime
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELIV = HERE.parent
REPO = HERE.parents[7]


def main():
    common = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--git-common-dir"], capture_output=True, text=True,
                            check=True).stdout.strip()
    main_tree = (Path(common) if Path(common).is_absolute() else (REPO / common)).resolve().parent
    events_path = main_tree / ".runtime" / "opal-data-harvest" / "events.jsonl"
    st = json.loads((DELIV / "w2_ac1_state.json").read_text(encoding="utf-8"))
    up = json.loads((DELIV / "w2_ac2_upload.json").read_text(encoding="utf-8"))
    t0 = datetime.datetime.fromisoformat(st["started_at"])
    t1 = datetime.datetime.fromisoformat(st["finished_at"])
    print("AC7 -- read from the capture run's own record (w2_ac1_state.json), window %s .. %s" % (t0.isoformat(), t1.isoformat()))
    print("capture: %d invocation(s), %d job(s); stop reason recorded by the runner: %s" % (
        len(st["invocations"]), sum(len(i["jobs"]) for i in st["invocations"]), st["stop_reason"]))

    window = []
    for line in events_path.read_text(encoding="utf-8").splitlines():
        try:
            e = json.loads(line)
            at = datetime.datetime.fromisoformat(e["at"])
        except (ValueError, KeyError):
            continue
        if t0 <= at <= t1:
            window.append(e)
    hosts = sorted({str(e.get("host")) for e in window if e.get("event") == "http"})
    kinds = {}
    for e in window:
        kinds[e["event"]] = kinds.get(e["event"], 0) + 1
    print("events.jsonl rows in the capture window (all publishers, denominator %d): %r" % (len(window), kinds))
    print("hosts of http events in the window: %r" % hosts)

    vision_hosts = [h for h in hosts if "moonshot" in h or "kimi" in h or "openai" in h or "anthropic" in h]
    lib_hosts = dict(st.get("requests_hosts_via_requests_lib") or {})
    moonshot_via_requests = sum(n for h, n in lib_hosts.items() if "moonshot" in h)
    auth_refreshes = sum(int(i["auth_refreshes"]) for i in st["invocations"])
    repairs = sum(int(i["verification_repairs"]) for i in st["invocations"])
    forbidden_events = [e["event"] for e in window if e["event"] in (
        "reauth_started", "reauth_succeeded", "verification_started", "verification_action", "verification_succeeded",
        "retry_after_reauth", "retry_after_verification")]
    trips = st.get("guard_trips") or []
    trips_ac2 = up.get("guard_trips") or []
    browser_launches = int(st.get("popen_launches") or 0) + sum(1 for t in trips if t["entry"] == "verification.sync_playwright")

    print("\nGUARD (b) TALLY")
    print("  calls to api.moonshot.ai / any vision-model endpoint: %d   (events.jsonl vision hosts %r; requests-library moonshot calls %d; "
          "requests-library hosts seen at all: %r)" % (len(vision_hosts) + moonshot_via_requests, vision_hosts, moonshot_via_requests, lib_hosts))
    print("  verification repairs: %d   (receipts %d; events %d)" % (
        repairs + sum(1 for x in forbidden_events if x.startswith("verification")), repairs,
        sum(1 for x in forbidden_events if x.startswith("verification"))))
    print("  re-authentications: %d   (receipts %d; events %d)" % (
        auth_refreshes + sum(1 for x in forbidden_events if "reauth" in x), auth_refreshes,
        sum(1 for x in forbidden_events if "reauth" in x)))
    print("  browsers started: %d   (subprocess/browser launches %d, sync_playwright trips %d)" % (
        browser_launches, st.get("popen_launches", 0), sum(1 for t in trips if t["entry"] == "verification.sync_playwright")))
    print("  guard trips: capture %d %r; upload leg %d %r" % (len(trips), [t["entry"] for t in trips], len(trips_ac2),
                                                              [t["entry"] for t in trips_ac2]))

    print("\nBOT WALL / VerificationRequired CHECK over every job (denominator %d):" % sum(len(i["jobs"]) for i in st["invocations"]))
    walls = []
    for i in st["invocations"]:
        for j in i["jobs"]:
            flag = j["error_type"] == "VerificationRequired" or j["status"] in ("request_rejected", "throttled")
            print("  inv %d %-28s status=%-34s error_type=%s%s" % (i["n"], str(j["security_key"])[:28], j["status"], j["error_type"],
                                                                     "   <-- BOT WALL" if flag else ""))
            if flag:
                walls.append((i["n"], j))
    if walls:
        n, w = walls[0]
        print("A BOT WALL WAS MET at inv %d job %s (%s): the runner's stop reason was: %s" % (n, w["job_id"], w["security_key"], st["stop_reason"]))
    else:
        print("no job met a bot wall or VerificationRequired. What DID stop the run: %s" % st["stop_reason"])
        for i in st["invocations"]:
            for j in i["jobs"]:
                if j["status"] == "account_or_harvester_unavailable":
                    print("  job %s (%s) -> status account_or_harvester_unavailable; the invocation's sa http events: %r" % (
                        j["job_id"], j["security_key"], [(e["path"].rsplit("/", 1)[-1], e["status"], e["bytes"]) for e in i["http_events"]]))
    ok = (not vision_hosts and not moonshot_via_requests and not repairs and not auth_refreshes and not forbidden_events
          and browser_launches == 0 and not trips and not trips_ac2)
    print("\nAC7: %s" % ("ALL FOUR COUNTS ZERO; the run stopped at the first suppression, never repaired" if ok else "A COUNT IS NON-ZERO -- see above"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
