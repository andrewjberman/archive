"""Builds PHASE_COVERAGE.json from cloudwatch_events_raw.json (the 6 cold chatter invokes of burst 2026-10-07T01:55:42Z).
Per log stream, in timestamp order, a request is the lines between START and REPORT. Main-thread route=chatter phases are
additive; the nested route=rankings/TRENDING/PRICE lines are emitted by a worker thread inside the final `compute` span
(monthly_chatter.py:342-345, names_read.start(_places_moved_index)) and are NOT added to the sum.
outside_ms = Duration - sum(route=chatter phase ms); the before-first-phase / after-last-phase split of it is read from
CloudWatch event timestamps (1 ms resolution): before = (first phase line ts - START ts) - first phase ms; after = REPORT ts - serialize ts."""
import collections
import json
import os
import re
import subprocess
here = os.path.dirname(os.path.abspath(__file__))
ev = json.load(open(os.path.join(here, "cloudwatch_events_raw.json")))
by = collections.defaultdict(list)
for e in ev:
    by[e["logStreamName"]].append(e)
invs = []
for s, es in by.items():
    es.sort(key=lambda e: (e["timestamp"], e["ingestionTime"]))
    cur = None
    for e in es:
        m = e["message"].rstrip("\n")
        if m.startswith("START RequestId:"):
            cur = {"rid": m.split()[2], "t0": e["timestamp"], "main": [], "nested": [], "ts_main": []}
        elif cur is not None and m.startswith("REPORT"):
            i = re.search(r"Init Duration: ([0-9.]+) ms", m)
            if i:
                cur["init"] = float(i.group(1))
                cur["dur"] = float(re.search(r"\tDuration: ([0-9.]+) ms", m).group(1))
                cur["t_report"] = e["timestamp"]
                cur["stream"] = s
                invs.append(cur)
            cur = None
        elif cur is not None:
            p = re.match(r"AMGT_PHASE route=(\S+) phase=(.+?) ms=(\d+)", m)
            if p:
                if p.group(1) == "chatter":
                    cur["main"].append((p.group(2), int(p.group(3))))
                    cur["ts_main"].append(e["timestamp"])
                else:
                    cur["nested"].append((p.group(1) + " " + p.group(2), int(p.group(3))))
invs.sort(key=lambda x: x["t0"])
cold = []
for x in invs:
    ssum = sum(ms for _, ms in x["main"])
    before = (x["ts_main"][0] - x["t0"]) - x["main"][0][1]
    after = x["t_report"] - x["ts_main"][-1]
    cold.append({"request_id": x["rid"], "log_stream_tail": x["stream"][-12:], "init_ms": x["init"], "duration_ms": x["dur"],
                 "phases": [{"label": lab, "ms": float(ms)} for lab, ms in x["main"]],
                 "outside_ms": round(x["dur"] - ssum, 2),
                 "outside_before_first_phase_ms_by_log_timestamp": before,
                 "outside_after_serialize_ms_by_log_timestamp": after,
                 "nested_rankings_phases_inside_final_compute": [{"label": lab, "ms": float(ms)} for lab, ms in x["nested"]]})
root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
M, S = "lib/research/api/monthly_chatter.py", "lib/research/api/scoped_amgt.py"
sites = [(M, 304, "generation read"), (M, 306, "mentions decode"), (M, 333, "compute"), (M, 335, "names"), (M, 339, "classification"),
         (M, 372, "compute"), (S, 6782, "serialize"),
         (S, 1440, "rankings/TRENDING/PRICE classification"), (S, 1444, "rankings/TRENDING/PRICE names"),
         (S, 1506, "rankings/TRENDING/PRICE generation read"), (S, 1517, "rankings/TRENDING/PRICE compute")]
doc = {
    "function_code_sha256": "OVpDhfwDG3BzKE++wDxMlFA6JrwpTnH3FiHC+NrzsrE=",
    "burst_started_utc": "2026-10-07T01:55:42Z",
    "cold_invokes": cold,
    "label_set": sorted({lab for _, _, lab in sites}),
    "emit_sites": [{"file": f, "line": n, "label": lab} for f, n, lab in sites],
    "unlabelled_spans": ["handler entry to line 289 of monthly_chatter (routing, authorisation, request-time import of the monthly_chatter/rolling_windows chain incl. pyarrow and numpy)",
                         "serialize line to handler return (Lambda wrapper return and runtime response hand-off)",
                         "the nested rankings phases run on a worker thread inside the final compute span; they are not additive"],
    "free_cuts": [
        {"what": "Move the request-time import of monthly_chatter/rolling_windows (pyarrow, numpy, coverage chain) to module scope so it runs in Init",
         "where": "lib/research/api/scoped_amgt.py:6770-6773 (AMGT-ag-0 comment and import)", "est_ms": 812.0,
         "basis": "measured outside-before-first-phase mean (812) of 6 cold invokes; it MOVES to Init Duration, so cold Init+Duration is unchanged unless Init runs on more CPU (UNMEASURED); build isolated-runtime arm named in the AMGT-ag-0 comment must be re-read"},
        {"what": "Pre-warm the pyarrow compute kernels and decode path the first compute span uses, at Init",
         "where": "lib/research/api/monthly_chatter.py:308-333 (cold first compute 962-1475 ms vs warm mean 321 ms, 21 warm invokes)", "est_ms": 814.0,
         "basis": "cold mean 1135 less warm mean 321; inference that the gap is first-use cost; it MOVES to Init the same way"},
        {"what": "Create the S3 client and make its first TLS connection at Init",
         "where": "lib/research/api/monthly_chatter.py:294-297 (pool_reader._client) and the first gold read", "est_ms": 686.0,
         "basis": "cold generation read mean 748 less warm mean 62; the client/TLS share of that gap cannot be split from log lines; upper bound; MOVES to Init"}],
    "free_cuts_exhausted": False,
    "residual_ms": 522.0,
    "residual_note": "warm mean Duration of 21 warm chatter invokes (days=30/90/365) is 521.8 ms: the Duration floor if every cold-only cost left the request",
    "provisioned_concurrency_inputs": {"memory_mb": 1769, "instances": 1, "price_per_gb_second": 0.0000041667,
        "price_source": "docs/briefs/fe-driven-lambda-keep-warm-feasibility-20260603.md:89 (provisioned concurrency allocation, x86, us-east-1, $0.0000041667 per GB-second); function arch x86_64 read from get_function_configuration; the public AWS price page was not re-read here: UNVERIFIED-HERE",
        "hours_per_month": 730, "monthly_usd": 18.9167,
        "arithmetic": "1769/1024 x 0.0000041667 x 3600 x 730 x 1 = 18.9167"},
}
json.dump(doc, open(os.path.join(here, "PHASE_COVERAGE.json"), "w"), indent=1)
print(json.dumps([(c["init_ms"], c["duration_ms"], c["outside_ms"], c["outside_before_first_phase_ms_by_log_timestamp"], c["outside_after_serialize_ms_by_log_timestamp"]) for c in cold]))
