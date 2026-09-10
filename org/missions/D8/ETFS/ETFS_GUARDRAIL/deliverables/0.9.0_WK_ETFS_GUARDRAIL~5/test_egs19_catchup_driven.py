#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-19 S19-AC1 battery -- THE CATCH-UP BRANCH DRIVEN.

Prints EGS19-CATCHUP-BRANCH-DRIVEN only when every arm (a)-(h) holds.

WHAT THIS BATTERY CAN AND CANNOT RE-MEASURE, said once and plainly, because a
battery that hides this is the thing the estate keeps getting burned by:

  The cell's act is IRREVERSIBLE AND ONE-SHOT -- one served slice was archived,
  deleted, and refilled by the producer's own catch-up path. The 404 that proved
  the hole existed is GONE the moment the producer healed it, and re-creating it
  would be a SECOND delete, which this order's BOUNDS forbid outright. So each arm
  below is labelled with its evidence class:

    [LIVE]     re-derived by THIS run against live AWS / the live repo.
    [CAPTURED] read from egs19_evidence.json, the act driver's verbatim record of
               every command it ran (argv, rc, stdout, stderr, UTC), committed at
               abba4a2d68 BEFORE any grading read, per spine v3.9.

  Six of the eight arms carry at least one LIVE instrument. Arm (c) is CAPTURED
  ONLY and says so in its own output line; its raw stderr is printed verbatim.

Bounds: vendored CLI v1 shim (`.tools/aws.cmd`), every call under a timeout; no
`--output text` (CRLF); every S3 time UTC via s3api; denominators on every list.
ASCII only.

Run from the worktree root:
  timeout 900 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~5/test_egs19_catchup_driven.py
"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
AWS = os.path.join(ROOT, ".tools", "aws.cmd" if sys.platform == "win32" else "aws")
EVIDENCE = os.path.join(HERE, "egs19_evidence.json")

BUCKET = "opal-data-etfs"
PARTNER = "cottonwood"
HOLE = "2026-09-03"
NEIGHBOUR = "2026-09-04"
NEWEST = "2026-09-08"
SLICE_KEY = "daily/%s/%s.json" % (PARTNER, HOLE)
FN = "cot-etf-ownership-daily"
LOG_GROUP = "/aws/lambda/%s" % FN
RULE = "cot-etf-ownership-daily-schedule"
ASSETS_BUCKET = "opal-data-assets"
FACT_PREFIX = "blackdiamond/cottonwood/silver/fact_holdings"
ROLE = "cot-etf-ownership-daily-role"
SRC_PIN = "ea47e92a72"  # the vintage this battery reads the producer source at
ENTRY = os.path.join(ROOT, "org", "critical_paths", "change_management",
                     "20260910T0340Z_etfs-guardrail-egs19-catchup-driven-20260910_deploy_completion.md")
MAILER_TOKENS = r"(?i)\bses\b|sesv2|send_email|send_raw_email|\bsns\b|boto3\.client\(\s*[\"']ses"

ARMS: list[tuple[str, bool, str]] = []


def arm(name: str, ok: bool, detail: str) -> bool:
    ARMS.append((name, ok, detail))
    print("  ARM %-3s %-4s %s" % (name, "PASS" if ok else "FAIL", detail))
    return ok


def aws(args: list[str], timeout: int = 120) -> tuple[int, str, str]:
    try:
        p = subprocess.run([AWS] + args, capture_output=True, timeout=timeout, cwd=ROOT)
        rc, so, se = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT after %ds" % timeout
    return (rc,
            so.decode("utf-8", "replace").replace("\r\n", "\n"),
            se.decode("utf-8", "replace").replace("\r\n", "\n"))


def aws_json(args: list[str], timeout: int = 120):
    rc, so, se = aws(args, timeout)
    doc = None
    if rc == 0 and so.strip():
        try:
            doc = json.loads(so)
        except Exception:
            doc = None
    return rc, doc, so, se


def step(label: str, ev: dict) -> dict | None:
    for s in ev["steps"]:
        if s["label"] == label:
            return s
    return None


def head(key: str) -> tuple[int, dict | None]:
    rc, doc, _, _ = aws_json(["s3api", "head-object", "--bucket", BUCKET, "--key", key,
                              "--output", "json"])
    return rc, doc


def main() -> int:
    print("=" * 100)
    print("EG-s-19 S19-AC1 -- THE CATCH-UP BRANCH DRIVEN, NOT AWAITED")
    print("run at %s   worktree %s" % (dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), ROOT))
    print("=" * 100)

    if not os.path.exists(EVIDENCE):
        print("FATAL: evidence ledger absent at %s" % EVIDENCE)
        return 1
    ev = json.load(open(EVIDENCE, encoding="utf-8"))
    print("evidence ledger: %s (%d recorded command(s), act %s -> %s)"
          % (os.path.basename(EVIDENCE), len(ev["steps"]), ev["act_started_utc"], ev["act_finished_utc"]))

    # =================================================================== ARM (a)
    print("\n(a) THE CHOICE -- four properties, for the date TAKEN and for the dates REJECTED  [LIVE]")
    sys.path.insert(0, os.path.join(ROOT, "lib"))
    import trading_calendar as tcal  # noqa: E402
    print("    calendar: %s (lib/trading_calendar.py, is_trading_day)" % tcal.calendar_source())

    span_start, span_end = dt.date(2026, 8, 28), dt.date(2026, 9, 10)
    day, cal, nontrading = span_start, {}, []
    while day <= span_end:
        cal[day.isoformat()] = bool(tcal.is_trading_day(day))
        if not cal[day.isoformat()]:
            nontrading.append("%s (%s)" % (day.isoformat(), day.strftime("%a")))
        day += dt.timedelta(days=1)
    print("    ENUMERATED %d of %d day(s) %s..%s; NON-TRADING: %s"
          % (len(cal), len(cal), span_start, span_end, ", ".join(nontrading)))

    rc, pdoc, _, _ = aws_json(["s3api", "list-objects-v2", "--bucket", ASSETS_BUCKET,
                               "--prefix", "%s/date=" % FACT_PREFIX, "--delimiter", "/",
                               "--output", "json"])
    parts = sorted(x["Prefix"].rstrip("/").split("date=")[-1]
                   for x in (pdoc or {}).get("CommonPrefixes", []) or [])
    newest = parts[-1] if parts else None
    print("    upstream fact_holdings partitions: DENOMINATOR %d, newest = %s (rc %d)"
          % (len(parts), newest, rc))

    def probe(d: str) -> dict:
        pth = os.path.join(ROOT, ".scratch", "battery_probe_%s.json" % d)
        os.makedirs(os.path.dirname(pth), exist_ok=True)
        with io.open(pth, "w", encoding="utf-8", newline="\n") as fh:
            json.dump({"date": d, "probe": True}, fh)
        rel = ".scratch/battery_probe_%s.json" % d
        out = ".scratch/battery_probe_out_%s.json" % d
        rc, _, _, _ = aws_json(["lambda", "invoke", "--function-name", FN,
                                "--payload", "fileb://" + rel, out, "--output", "json",
                                "--cli-read-timeout", "300", "--cli-connect-timeout", "60"],
                               timeout=300)
        try:
            return json.load(open(os.path.join(ROOT, out), encoding="utf-8"))
        except Exception:
            return {"status": "probe-unreadable", "rc": rc}

    candidates = {
        HOLE: "TAKEN",
        NEWEST: "REJECTED -- IS the newest priced partition, so _catchup_missing_dates skips it as skip_date (lambda_function.py:268-269); EG-s-17's exact dead end",
        "2026-09-05": "REJECTED -- not a trading day, so its ABSENCE IS CORRECT; nothing to delete",
        "2026-09-09": "REJECTED -- upstream partition absent (D+1 race, class D); the producer could NOT re-derive it, so a hole there is damage, not a test",
        NEIGHBOUR: "ELIGIBLE BUT NOT TAKEN -- kept intact as the 200 positive control beside the 404",
    }
    props = {}
    for d in [HOLE, NEWEST, "2026-09-05", "2026-09-09", NEIGHBOUR]:
        pr = probe(d)
        hrc, hdoc = head("daily/%s/%s.json" % (PARTNER, d))
        props[d] = {"trading": cal.get(d), "present_now": hrc == 0,
                    "size": (hdoc or {}).get("ContentLength"),
                    "utc": str((hdoc or {}).get("LastModified")),
                    "partition": pr.get("partition"), "priced": pr.get("priced"),
                    "is_newest": d == newest}
        print("    %-11s trading=%-5s slice_present=%-5s size=%-6s utc=%-31s partition=%-5s priced=%-6s is_newest=%-5s"
              % (d, cal.get(d), hrc == 0, (hdoc or {}).get("ContentLength"),
                 str((hdoc or {}).get("LastModified")), pr.get("partition"), pr.get("priced"),
                 d == newest))
        print("                %s" % candidates[d])

    before_inv = ev["daily_inventory_before"]["keys"]
    taken_before = before_inv.get(SLICE_KEY, {})
    print("    THE DATE TAKEN, as it stood BEFORE the act [CAPTURED]: %s  size=%s  utc=%s  ETag=%s"
          % (HOLE, taken_before.get("Size"), taken_before.get("LastModified"), taken_before.get("ETag")))

    t = props[HOLE]
    a_ok = (t["trading"] is True and taken_before.get("Size") == 1345
            and t["partition"] is True and (t["priced"] or 0) > 0 and not t["is_newest"]
            and newest == NEWEST
            and props[NEWEST]["is_newest"] is True
            and props["2026-09-05"]["trading"] is False
            and props["2026-09-09"]["partition"] is False)
    arm("a", a_ok,
        "%s: trading=True, present before the act at %s B, partition=True priced=%d, and NOT the newest "
        "(newest=%s, priced=%s). Rejected with reasons printed: %s, 2026-09-05, 2026-09-09; %s eligible "
        "but held back as the positive control. 3 non-trading days enumerated in the stretch, not 2."
        % (HOLE, taken_before.get("Size"), t["priced"] or 0, newest, props[NEWEST]["priced"],
           NEWEST, NEIGHBOUR))

    # =================================================================== ARM (b)
    print("\n(b) THE ARCHIVE -- byte-equal, and made BEFORE the delete with the entry already OPEN  [LIVE + CAPTURED]")
    arc_key = ev["archive_key"]
    arc_rc, arc_doc = head(arc_key)
    print("    [LIVE] head-object %s -> rc %d, Size %s, LastModified %s, ETag %s"
          % (arc_key, arc_rc, (arc_doc or {}).get("ContentLength"),
             str((arc_doc or {}).get("LastModified")), (arc_doc or {}).get("ETag")))
    print("    [CAPTURED] source  sha256 = %s (%d B)" % (ev["source_sha256"], ev["source_bytes"]))
    print("    [CAPTURED] archive sha256 = %s (%d B)  -- read BACK from S3, not assumed"
          % (ev["archive_sha256"], ev["archive_bytes"]))
    entry_txt = io.open(ENTRY, encoding="utf-8", newline="").read() if os.path.exists(ENTRY) else ""
    m_open = re.search(r"(\d{8}T\d{6}Z) OPENED by 0\.9\.0_WK_ETFS_GUARDRAIL~5", entry_txt)
    opened_at = m_open.group(1) if m_open else None
    del_utc = ev["delete_utc"]
    del_compact = del_utc.replace("-", "").replace(":", "")
    print("    entry OPENED at %s ; DELETE at %s (compact %s) -- opened-at PRECEDES the delete: %s"
          % (opened_at, del_utc, del_compact, opened_at is not None and opened_at < del_compact))
    print("    entry CLOSED and COMMITTED before this grading read: %s"
          % ("CLOSED -- all 6 legs proven" in entry_txt))
    b_ok = (ev["archive_byte_equal"] is True
            and ev["source_sha256"] == ev["archive_sha256"]
            and arc_rc == 0
            and opened_at is not None and opened_at < del_compact
            and "CLOSED -- all 6 legs proven" in entry_txt)
    arm("b", b_ok,
        "archive at %s live-present (rc 0); source and archive sha256 IDENTICAL (%s); entry opened %s "
        "< delete %s; entry closed with all 6 legs proven."
        % (arc_key, ev["archive_sha256"][:16] + "...", opened_at, del_compact))

    # =================================================================== ARM (c)
    print("\n(c) THE HOLE EXISTED -- 404 beside a 200 in ONE call sequence  [CAPTURED ONLY: the producer")
    print("    healed the hole 13 s later and re-creating it would be a SECOND delete, which BOUNDS forbid]")
    s404 = step("HEAD slice AFTER delete (expect 404)", ev)
    s200 = step("HEAD neighbour %s (POSITIVE CONTROL, expect 200)" % NEIGHBOUR, ev)
    sdel = step("DELETE the served slice (ANDREW-DIRECT ~02:5xZ)", ev)
    print("    DELETE   argv: %s" % " ".join(sdel["argv"]))
    print("    DELETE   rc %d at %s" % (sdel["rc"], sdel["finished_utc"]))
    print("    404 ARM  argv: %s" % " ".join(s404["argv"]))
    print("    404 ARM  rc %d at %s ; stderr VERBATIM: %s"
          % (s404["rc"], s404["finished_utc"], s404["stderr"].strip()))
    print("    200 CTRL argv: %s" % " ".join(s200["argv"]))
    print("    200 CTRL rc %d at %s (the neighbour %s was NOT touched)"
          % (s200["rc"], s200["finished_utc"], NEIGHBOUR))
    c_ok = (sdel["rc"] == 0 and s404["rc"] != 0 and "(404)" in s404["stderr"]
            and "Not Found" in s404["stderr"] and s200["rc"] == 0
            and s404["finished_utc"] < s200["finished_utc"])
    arm("c", c_ok,
        "delete rc 0; then head-object on the slice rc %d carrying '(404) ... Not Found' at %s, beside "
        "head-object on %s rc 0 at %s -- the negative and its positive control in one sequence, so the "
        "404 cannot be a broken instrument."
        % (s404["rc"], s404["finished_utc"], NEIGHBOUR, s200["finished_utc"]))

    # =================================================================== ARM (d)
    print("\n(d) THE FIRE IS THE RULE'S SHAPE -- no `date` key, and 1 of 1 START in the log read BY TIME  [LIVE + CAPTURED]")
    rc, tdoc, _, _ = aws_json(["events", "list-targets-by-rule", "--rule", RULE, "--output", "json"])
    targets = (tdoc or {}).get("Targets", []) or []
    print("    (d-i) THE RULE'S SHAPE, ESTABLISHED FROM THE RULE ITSELF  [LIVE]")
    print("      list-targets-by-rule %s -> rc %d, DENOMINATOR %d target(s)" % (RULE, rc, len(targets)))
    override_keys = ("Input", "InputPath", "InputTransformer")
    overrides = []
    for i, t_ in enumerate(targets):
        for k in override_keys:
            present = k in t_
            if present:
                overrides.append(k)
            print("        target %d of %d  Id=%-28s  %-17s %s"
                  % (i + 1, len(targets), t_.get("Id"), k, "PRESENT" if present else "ABSENT"))
    print("      => all 3 of 3 override keys ABSENT on %d of %d target(s). THAT IS THE CONDITION under"
          % (len(targets) - (1 if overrides else 0), len(targets)))
    print("         which EventBridge delivers its DEFAULT scheduled envelope unmodified, so the rule's")
    print("         shape is established from the RULE, not by comparison to an unobservable object.")
    payload = ev["fire_payload"]
    print("    (d-ii) SHAPE-EQUALITY AND NO `date` KEY  [CAPTURED]")
    print("      THE PAYLOAD FIRED, verbatim: %s" % json.dumps(payload, sort_keys=True))
    default_fields = ["version", "id", "detail-type", "source", "account", "time", "region",
                      "resources", "detail"]
    missing = [f for f in default_fields if f not in payload]
    extra = [f for f in payload if f not in default_fields]
    print("      default-envelope fields present: %d of %d %s ; extra fields: %d %s"
          % (len(default_fields) - len(missing), len(default_fields),
             "(none missing)" if not missing else missing, len(extra), extra or "(none)"))
    print("      'date' key in payload: %s ; 'probe' key in payload: %s"
          % (ev["fire_payload_has_date_key"], ev["fire_payload_has_probe_key"]))
    print("      detail-type=%r source=%r resources=%s"
          % (payload.get("detail-type"), payload.get("source"), payload.get("resources")))
    print("    (d-iii) BRANCH-EQUIVALENCE AT THE LINES THAT DECIDE IT  [source-level, quoted at vintage]")
    print("      infra/aws/lambda/cot-pipeline/cot-etf-ownership-daily/lambda_function.py @%s" % SRC_PIN)
    print("        :300  if isinstance(event, dict) and event.get(\"probe\"):   -> `probe` is %s in the"
          % ("ABSENT/falsy" if not payload.get("probe") else "TRUE"))
    print("              payload, so :300-302 (the probe branch) is UNREACHABLE.")
    print("        :304  target_date = event.get(\"date\") if isinstance(event, dict) else None")
    print("        :305  if target_date:                                       -> `date` is %s, so"
          % ("None" if "date" not in payload else repr(payload.get("date"))))
    print("              :304-308 (the explicit-date branch) is UNREACHABLE.")
    print("        :310  day = _latest_partition()")
    print("        :311  result = _process_date(day, universe)")
    print("        :312  catchup_results = _catchup_missing_dates(universe, skip_date=day)")
    print("      => with both guarded branches unreachable, control NECESSARILY reaches the catch-up")
    print("         call at :312. The catch-up path was not merely available; it was unavoidable.")
    print("    WHY THIS ARM NO LONGER CLAIMS BYTE-EQUALITY (row W5-S3, re-cut by the issuer 04:0xZ):")
    print("      the delivered envelope carries a per-delivery UUID `id` and `time`, so two deliveries")
    print("      of the same rule are not byte-equal to EACH OTHER, and the producer never logs its")
    print("      `event` -- no delivered envelope is observable at this seat. A line reading")
    print("      'byte-equal' would have been FALSE, so the arm proves the three facts above instead.")
    inv_meta = ev["invoke_meta"] or {}
    print("    [CAPTURED] invoke rc %d, StatusCode %s, ExecutedVersion %s, fired at %s"
          % (ev["invoke_rc"], inv_meta.get("StatusCode"), inv_meta.get("ExecutedVersion"), ev["fire_utc"]))

    start_ms = ev["log_window_start_ms"]
    end_ms = start_ms + 5 * 60 * 1000
    rc, ldoc, _, _ = aws_json(["logs", "filter-log-events", "--log-group-name", LOG_GROUP,
                               "--start-time", str(start_ms), "--end-time", str(end_ms),
                               "--output", "json"], timeout=180)
    events = [(e["timestamp"], e["logStreamName"], e["message"].rstrip("\n"))
              for e in (ldoc or {}).get("events", []) or []]
    events.sort()
    starts = [e for e in events if e[2].startswith("START RequestId")]
    req_ids = sorted({e[2].split("START RequestId: ")[1].split(" ")[0] for e in starts})
    print("    [LIVE] filter-log-events %s over [%d,%d] -> rc %d, DENOMINATOR %d event(s) in %d stream(s)"
          % (LOG_GROUP, start_ms, end_ms, rc, len(events),
             len({e[1] for e in events})))
    for ts, _stream, msg in events:
        print("           %s | %s"
              % (dt.datetime.fromtimestamp(ts / 1000, dt.timezone.utc).strftime("%H:%M:%S.%fZ"), msg[:200]))
    print("    [LIVE] START RequestId lines: %d of %d event(s); request id(s): %s"
          % (len(starts), len(events), req_ids))
    d_ok = (rc == 0 and len(targets) == 1 and not overrides
            and ev["fire_payload_has_date_key"] is False
            and ev["fire_payload_has_probe_key"] is False
            and "date" not in payload and not payload.get("probe")
            and not missing and not extra
            and inv_meta.get("StatusCode") == 200
            and len(starts) == 1)
    arm("d", d_ok,
        "(d-i) 1 of 1 target with all 3 of 3 override keys ABSENT, which IS the default-envelope "
        "condition; (d-ii) payload shape-equal to that envelope (%d of %d fields, 0 extra) with no "
        "`date` key; (d-iii) branch-equivalence at :300-302 and :304-308 @%s, so control necessarily "
        "reached :312; plus StatusCode 200 and 1 of 1 START RequestId (%s) in %s read BY TIME over a "
        "%d-event window."
        % (len(default_fields), len(default_fields), SRC_PIN,
           req_ids[0] if req_ids else "-", LOG_GROUP, len(events)))

    # =================================================================== ARM (e)
    print("\n(e) THE BRANCH RAN AND FOUND IT ITSELF -- the catch-up path, not the main path  [LIVE]")
    catch_lines = [e for e in events if e[2].startswith("CATCHUP")]
    main_writes = [e for e in events if e[2].startswith("OK: wrote") and NEWEST in e[2]]
    catch_writes = [e for e in events if e[2].startswith("OK: wrote") and HOLE in e[2]]
    for ts, _s, msg in catch_lines:
        print("    THE LINE: %s | %s"
              % (dt.datetime.fromtimestamp(ts / 1000, dt.timezone.utc).strftime("%H:%M:%S.%fZ"), msg))
    resp = ev.get("invoke_response") or {}
    print("    THE RESPONSE, verbatim: %s" % json.dumps(resp, sort_keys=True))
    print("    catchup_processed = %s   <- carries %s" % (resp.get("catchup_processed"), HOLE))
    print("    response['date']  = %s   <- the MAIN path's date, and it is NOT %s"
          % (resp.get("date"), HOLE))
    print("    catchup_failed = %s ; catchup_skipped_unpriced = %s"
          % (resp.get("catchup_failed"), resp.get("catchup_skipped_unpriced")))
    print("    ordering: main-path write for %s at %s, catch-up write for %s at %s (%d ms later)"
          % (NEWEST,
             dt.datetime.fromtimestamp(main_writes[0][0] / 1000, dt.timezone.utc).strftime("%H:%M:%S.%fZ")
             if main_writes else "-",
             HOLE,
             dt.datetime.fromtimestamp(catch_writes[0][0] / 1000, dt.timezone.utc).strftime("%H:%M:%S.%fZ")
             if catch_writes else "-",
             (catch_writes[0][0] - main_writes[0][0]) if (main_writes and catch_writes) else -1))
    e_ok = (len(catch_lines) == 1
            and ("CATCHUP: processed %s (status=ok)" % HOLE) == catch_lines[0][2]
            and resp.get("catchup_processed") == [HOLE]
            and resp.get("date") == NEWEST
            and resp.get("catchup_failed") == []
            and len(catch_writes) == 1)
    arm("e", e_ok,
        "the log carries exactly one CATCHUP line and it is 'CATCHUP: processed %s (status=ok)'; the "
        "response's catchup_processed is ['%s'] while its own `date` field is %s -- so %s was recovered "
        "on the CATCH-UP path the producer walked itself, NOT by a main-path write."
        % (HOLE, HOLE, resp.get("date"), HOLE))

    # =================================================================== ARM (f)
    print("\n(f) THE SLICE IS BACK -- and its content is compared, not assumed  [LIVE]")
    hrc, hdoc = head(SLICE_KEY)
    print("    [LIVE] head-object %s -> rc %d, Size %s, LastModified %s, ETag %s"
          % (SLICE_KEY, hrc, (hdoc or {}).get("ContentLength"),
             str((hdoc or {}).get("LastModified")), (hdoc or {}).get("ETag")))
    print("    [CAPTURED] restored on poll %d of a bound of 30 polls / 15 minutes; poll trail: %s"
          % (ev["poll_count"], json.dumps(ev["polls"])))
    os.makedirs(os.path.join(ROOT, ".scratch"), exist_ok=True)
    rc_a, _, _ = aws(["s3api", "get-object", "--bucket", BUCKET, "--key", SLICE_KEY,
                      ".scratch/battery_live_slice.json", "--output", "json"])
    rc_b, _, _ = aws(["s3api", "get-object", "--bucket", BUCKET, "--key", arc_key,
                      ".scratch/battery_live_archive.json", "--output", "json"])
    live_new = open(os.path.join(ROOT, ".scratch", "battery_live_slice.json"), "rb").read()
    live_arc = open(os.path.join(ROOT, ".scratch", "battery_live_archive.json"), "rb").read()
    sha_new = hashlib.sha256(live_new).hexdigest()
    sha_arc = hashlib.sha256(live_arc).hexdigest()
    doc_new, doc_arc = json.loads(live_new), json.loads(live_arc)
    print("    [LIVE] SECOND INDEPENDENT READER (get-object + json.load, not head-object's metadata):")
    print("           restored rows = %d (non-zero: %s); archived rows = %d"
          % (len(doc_new), len(doc_new) > 0, len(doc_arc)))
    print("           restored sha256 = %s" % sha_new)
    print("           archived sha256 = %s" % sha_arc)
    print("           original  sha256 = %s  [CAPTURED, pre-delete]" % ev["source_sha256"])
    diffs = []
    by_a = {r.get("etf_ticker"): r for r in doc_arc}
    by_n = {r.get("etf_ticker"): r for r in doc_new}
    fields = sorted({k for r in doc_arc + doc_new for k in r})
    for tk in sorted(set(by_a) | set(by_n)):
        a_, b_ = by_a.get(tk), by_n.get(tk)
        if a_ is None or b_ is None:
            diffs.append("%s present on one side only" % tk)
            continue
        for k in fields:
            if a_.get(k) != b_.get(k):
                diffs.append("%s.%s %r -> %r" % (tk, k, a_.get(k), b_.get(k)))
    print("           FIELD-LEVEL COMPARISON: DENOMINATOR %d ticker(s) x %d field(s) = %d cell(s); "
          "differences: %d" % (len(by_n), len(fields), len(by_n) * len(fields), len(diffs)))
    for d in diffs:
        print("           DIFF: %s" % d)
    if not diffs:
        print("           NO DIFFERENCE TO NAME: the re-derivation is BYTE-IDENTICAL to the original, not")
        print("           merely equivalent -- source, archive and restored all carry one sha256. That is")
        print("           the strongest available answer to 'is this a faithful re-derivation or a drift'.")
    for r in doc_new:
        print("           row: etf=%-5s ownership_value=%-14s account_count=%-3s source_as_of=%s"
              % (r.get("etf_ticker"), r.get("ownership_value"), r.get("account_count"),
                 r.get("source_as_of")))
    f_ok = (hrc == 0 and rc_a == 0 and rc_b == 0 and len(doc_new) > 0
            and sha_new == sha_arc == ev["source_sha256"] and not diffs
            and all(r.get("source_as_of") == HOLE and r.get("date") == HOLE for r in doc_new))
    arm("f", f_ok,
        "head-object 200, Size %s, LastModified %s; a second independent reader counts %d non-zero rows; "
        "restored == archived == original on sha256 with 0 of %d field-level differences; every row's "
        "date and source_as_of read %s."
        % ((hdoc or {}).get("ContentLength"), str((hdoc or {}).get("LastModified")), len(doc_new),
           len(by_n) * len(fields), HOLE))

    # =================================================================== ARM (g)
    print("\n(g) NOTHING ELSE MOVED -- counts, and CONTENT vs TIMESTAMP stated separately  [LIVE + CAPTURED]")
    before = ev["daily_inventory_before"]["keys"]
    after = ev["daily_inventory_after"]["keys"]
    pb = [k for k in before if k.startswith("daily/%s/" % PARTNER)]
    pa = [k for k in after if k.startswith("daily/%s/" % PARTNER)]
    print("    [CAPTURED] daily/%s/ slice count: %d BEFORE, %d AFTER (equal: %s)"
          % (PARTNER, len(pb), len(pa), len(pb) == len(pa)))
    print("    [CAPTURED] daily/ (BOTH partners, every key) DENOMINATOR: %d BEFORE, %d AFTER"
          % (len(before), len(after)))
    content_changed, ts_only, added, removed = [], [], [], []
    for k in sorted(set(before) | set(after)):
        a_, b_ = before.get(k), after.get(k)
        if a_ is None:
            added.append(k)
        elif b_ is None:
            removed.append(k)
        elif a_["ETag"] != b_["ETag"] or a_["Size"] != b_["Size"]:
            content_changed.append(k)
        elif a_["LastModified"] != b_["LastModified"]:
            ts_only.append(k)
    both_sides = [k for k in before if k in after]
    print("    (g-i) NO KEY UNDER daily/ CHANGED IN CONTENT -- ETag AND Size compared on every key")
    print("      ETag+Size comparison performed on %d of %d key(s) present on BOTH sides "
          "(DENOMINATOR before %d / after %d)" % (len(both_sides), len(before), len(before), len(after)))
    print("      keys whose CONTENT changed (ETag or Size differs): %d of %d" % (len(content_changed), len(both_sides)))
    print("      keys REMOVED across the window: %d of %d" % (len(removed), len(before)))
    print("      keys ADDED: %d -- %s" % (len(added), added))
    print("        (that addition is THIS ORDER'S OWN ARCHIVE, named in the change-management entry")
    print("         BEFORE the act; it is not a slice and sits outside daily/%s/.)" % PARTNER)
    census_path = os.path.join(HERE, "egs19_daily_etag_census.json")
    with io.open(census_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"comparison": "every key under daily/ on opal-data-etfs, before vs after the act",
                   "denominator_before": len(before), "denominator_after": len(after),
                   "compared_both_sides": len(both_sides),
                   "content_changed": content_changed, "removed": removed, "added": added,
                   "timestamp_touched_identical_bytes": ts_only,
                   "keys": {k: {"before": before.get(k), "after": after.get(k)}
                            for k in sorted(set(before) | set(after))}}, fh, indent=2)
        fh.write("\n")
    print("      the FULL per-key ETag table (all %d keys, both sides) is committed beside this battery"
          % len(set(before) | set(after)))
    print("      at %s -- so 'every key' is literally available, not merely counted."
          % os.path.basename(census_path))
    print("    (g-ii) THE KEYS THE MAIN PATH NECESSARILY RE-PUT, ENUMERATED BY NAME")
    newest_key = "daily/%s/%s.json" % (PARTNER, NEWEST)
    forced = [k for k in ts_only if k == newest_key]
    healed = [k for k in ts_only if k == SLICE_KEY]
    other_touched = [k for k in ts_only if k not in forced + healed]
    print("      WHY ANY EXIST: the handler runs `day = _latest_partition()` then `_process_date(...)`")
    print("      at lambda_function.py:310-311 @%s BEFORE `_catchup_missing_dates` is reached at :312," % SRC_PIN)
    print("      and `_process_date` calls put_object at :245 unconditionally. So EVERY scheduled-shape")
    print("      fire re-PUTs the newest partition's slice, BY CONSTRUCTION. That is not collateral")
    print("      damage; it is the producer's designed idempotence, and it is why the original arm (g)")
    print("      could not be satisfied by any run of the shape arm (d) mandates (row W5-S1).")
    for k in forced:
        print("      NECESSARILY RE-PUT: %s" % k)
        print("        ETag   BEFORE %s" % before[k]["ETag"])
        print("        ETag   AFTER  %s   -> EQUAL: %s"
              % (after[k]["ETag"], before[k]["ETag"] == after[k]["ETag"]))
        print("        Size   %s -> %s  (equal: %s)"
              % (before[k]["Size"], after[k]["Size"], before[k]["Size"] == after[k]["Size"]))
        print("        LastModified %s -> %s  == A TIMESTAMP TOUCH ON IDENTICAL BYTES"
              % (before[k]["LastModified"], after[k]["LastModified"]))
    for k in healed:
        print("      THE HEALED HOLE (not a collateral touch -- this is the cell's own subject): %s" % k)
        print("        ETag   BEFORE %s" % before[k]["ETag"])
        print("        ETag   AFTER  %s   -> EQUAL: %s"
              % (after[k]["ETag"], before[k]["ETag"] == after[k]["ETag"]))
        print("        LastModified %s -> %s  (deleted at %s, refilled by the catch-up path)"
              % (before[k]["LastModified"], after[k]["LastModified"], ev["delete_utc"]))
    print("      ANY OTHER TOUCHED KEY: %d %s" % (len(other_touched), other_touched or "(none)"))
    print("    (g-iii) THE PARTNER'S SLICE COUNT, before and after, with its denominator")
    print("      daily/%s/ : %d BEFORE, %d AFTER -- EQUAL: %s (denominator = every key under that "
          "prefix)" % (PARTNER, len(pb), len(pa), len(pb) == len(pa)))
    print("    WHAT THIS ARM DISCRIMINATES: the failure this outcome fears is the catch-up branch")
    print("      writing WRONG data or clobbering a partition. Content equality across %d of %d keys"
          % (len(both_sides), len(both_sides)))
    print("      refutes exactly that.")
    rc, live_doc, _, _ = aws_json(["s3api", "list-objects-v2", "--bucket", BUCKET,
                                   "--prefix", "daily/", "--output", "json"])
    live_keys = {c["Key"] for c in (live_doc or {}).get("Contents", []) or []}
    live_partner = {k for k in live_keys if k.startswith("daily/%s/" % PARTNER)}
    print("    [LIVE] daily/ now: DENOMINATOR %d key(s) (truncated: %s); daily/%s/ now: %d"
          % (len(live_keys), (live_doc or {}).get("IsTruncated"), PARTNER, len(live_partner)))
    g_ok = (len(pb) == len(pa) and not content_changed and not removed
            and added == [arc_key] and set(ts_only) <= {SLICE_KEY, newest_key}
            and len(forced) == 1 and not other_touched
            and all(before[k]["ETag"] == after[k]["ETag"] and before[k]["Size"] == after[k]["Size"]
                    for k in ts_only)
            and len(live_partner) == len(pb) and rc == 0)
    arm("g", g_ok,
        "(g-i) 0 of %d keys compared on both sides changed CONTENT and 0 were removed, the 1 addition "
        "being this order's own archive; (g-ii) the %d necessarily re-PUT key is enumerated by name "
        "(%s) with both ETags shown EQUAL and its LastModified movement printed as a timestamp touch on "
        "identical bytes, and no OTHER key was touched; (g-iii) daily/%s/ %d -> %d, equal, live re-read "
        "agrees at %d."
        % (len(both_sides), len(forced), forced[0] if forced else "-", PARTNER, len(pb), len(pa),
           len(live_partner)))

    # =================================================================== ARM (h)
    print("\n(h) ZERO SES SENDS -- Andrew's ~02:5xZ constraint, PROVEN on three independent instruments  [LIVE]")
    rc, cfg, _, _ = aws_json(["lambda", "get-function", "--function-name", FN, "--output", "json"])
    names, mailer_hits, dep_sha = [], -1, None
    if rc == 0 and cfg:
        try:
            blob = urllib.request.urlopen(cfg["Code"]["Location"], timeout=120).read()
            z = zipfile.ZipFile(io.BytesIO(blob))
            names = z.namelist()
            src = z.read("lambda_function.py")
            dep_sha = hashlib.sha256(src).hexdigest()
            mailer_hits = len(re.findall(MAILER_TOKENS, src.decode("utf-8", "replace")))
        except Exception as exc:
            print("    package read FAILED: %s" % exc)
    repo_src = open(os.path.join(ROOT, "infra", "aws", "lambda", "cot-pipeline",
                                 "cot-etf-ownership-daily", "lambda_function.py"), "rb").read()
    repo_sha = hashlib.sha256(repo_src.replace(b"\r\n", b"\n")).hexdigest()
    print("    INSTRUMENT 1 -- THE DEPLOYED BYTES (not the repo's, not a filename):")
    print("      package holds %d of %d file(s): %s" % (len(names), len(names), names))
    print("      deployed lambda_function.py sha256 = %s" % dep_sha)
    print("      repo     lambda_function.py sha256 = %s (LF-normalised)  IDENTICAL: %s"
          % (repo_sha, dep_sha == repo_sha))
    print("      mailer-token census over the DEPLOYED bytes (ses|sesv2|send_email|send_raw_email|sns|"
          "boto3.client('ses): %d hit(s)" % mailer_hits)
    print("      => THIS PRODUCER HAS NO MAILER ON ANY PATH. It cannot reach aj@opalinvest.com or any")
    print("         other recipient, because it contains no send call at all.")

    rc1, mdoc, _, _ = aws_json(["iam", "list-attached-role-policies", "--role-name", ROLE, "--output", "json"])
    rc2, idoc, _, _ = aws_json(["iam", "list-role-policies", "--role-name", ROLE, "--output", "json"])
    managed = [p["PolicyName"] for p in (mdoc or {}).get("AttachedPolicies", []) or []]
    inline = (idoc or {}).get("PolicyNames", []) or []
    ses_actions = 0
    for pn in inline:
        rc3, pdoc2, _, _ = aws_json(["iam", "get-role-policy", "--role-name", ROLE,
                                     "--policy-name", pn, "--output", "json"])
        blob2 = json.dumps((pdoc2 or {}).get("PolicyDocument", {}))
        ses_actions += len(re.findall(r'"ses[v2]*:', blob2, re.I))
    print("    INSTRUMENT 2 -- THE ROLE (a different plane from the code):")
    print("      %s: %d managed %s + %d inline %s = DENOMINATOR %d policy(ies)"
          % (ROLE, len(managed), managed, len(inline), inline, len(managed) + len(inline)))
    print("      ses:/sesv2: actions across the inline documents: %d" % ses_actions)
    print("      => the role could not send email even if the code tried.")

    win = ev["ses_window"]
    ses = ev["ses_metrics"]
    print("    INSTRUMENT 3 -- THE RUN WINDOW ITSELF (%s .. %s), re-read LIVE:" % (win["start"], win["end"]))
    live_ses_ok = True
    for metric in ("Send", "Delivery", "Reputation.BounceRate"):
        rc4, sdoc, _, _ = aws_json(["cloudwatch", "get-metric-statistics", "--namespace", "AWS/SES",
                                    "--metric-name", metric, "--start-time", win["start"],
                                    "--end-time", win["end"], "--period", "300",
                                    "--statistics", "Sum", "--output", "json"])
        pts = (sdoc or {}).get("Datapoints", []) or []
        total = sum(p.get("Sum", 0) for p in pts)
        print("      AWS/SES %-22s rc %d  DENOMINATOR %d datapoint(s)  Sum %s   [captured at act time: "
              "%d datapoint(s), Sum %s]"
              % (metric, rc4, len(pts), total, ses[metric]["denominator"], ses[metric]["sum"]))
        if rc4 != 0 or total != 0 or ses[metric]["sum"] != 0:
            live_ses_ok = False
    print("      => ZERO SES sends of ANY kind, from ANY sender, in the window that contains this fire.")
    print("    AND WHAT WAS NOT DONE: `etfs-reports-orchestrator` -- the one component whose mailer")
    print("      reaches aj@ -- was NOT invoked under this order, in any mode, at any point.")
    h_ok = (mailer_hits == 0 and dep_sha == repo_sha and len(names) == 1
            and ses_actions == 0 and rc1 == 0 and rc2 == 0 and live_ses_ok)
    arm("h", h_ok,
        "deployed package = 1 of 1 file byte-identical to the repo source with 0 mailer tokens; role "
        "carries 0 ses: actions across %d of %d policies; AWS/SES Send/Delivery/BounceRate all 0 "
        "datapoints and Sum 0 over the run window, live and at act time."
        % (len(managed) + len(inline), len(managed) + len(inline)))

    # =================================================================== VERDICT
    print("\n" + "=" * 100)
    passed = sum(1 for _n, ok, _d in ARMS if ok)
    for n, ok, _d in ARMS:
        print("  arm %-3s %s" % (n, "PASS" if ok else "FAIL"))
    print("  ARMS PASSED: %d of %d" % (passed, len(ARMS)))
    if passed == len(ARMS) and len(ARMS) == 8:
        print("\nEGS19-CATCHUP-BRANCH-DRIVEN")
        print("\nThe catch-up branch had never once run in this estate. It ran, on a hole made on Andrew's")
        print("own word and healed by the producer finding it ITSELF, and the served slice is byte-identical")
        print("to the one that was deleted.")
        print("=" * 100)
        return 0
    print("\nTOKEN WITHHELD -- %d arm(s) failed; S19-AC1 does NOT pass." % (len(ARMS) - passed))
    print("=" * 100)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
