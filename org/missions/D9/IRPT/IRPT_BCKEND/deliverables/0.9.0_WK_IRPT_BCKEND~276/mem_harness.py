"""IB-pr-414 memory harness: ONE firm's run_firm of ONE bundle tree, peak memory sampled across the whole run. AWS READS ONLY.

Usage: python -I mem_harness.py <repo_root> <tree> <scratch> <label> <firm> [as_of] [--gate-trace]
  - the tree's OWN holdings_snapshot.run_firm, real sources + real served index, upload=True THROUGH A GUARDED CLIENT so the publish
    gate runs (it only runs on an upload that captured the firm's index); every write is captured in memory and never leaves the
    process (the "upload disabled" of the census), every other mutation raises. NOTHING is put anywhere.
  - peak memory: (a) a sampler thread reads psutil rss every 20 ms; (b) the OS peak working set (psutil memory_info().peak_wset on
    Windows) read at the end -- the primary number, since a sampler can miss a spike while a C call holds the GIL.
  - phase marks wrap build_snapshot, served_publication, evaluate_publish_gate and land when the tree has them: rss before/after and the
    sampled peak inside each, so the gate's own cost is separable from the build's.
  - canonical_lookup calls are COUNTED (table_lookups); with --memo they are also memoised as ~269's replay_driver_cached.py does
    (same key -> same answer; the table is read-only). The census runs use NO --memo.
Writes <scratch>/mem_<label>_<firm>.json: numbers only (no account id, security id, name). With --gate-trace also writes
<scratch>/gate_<label>_<firm>.json: the gate's full decision (outcome, conditions, listed) for the replay comparison.
"""
import json
import os
import sys
import threading
import time

import psutil

SAMPLE_S = 0.02


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    root, tree, scratch, label, firm = args[:5]
    as_of = args[5] if len(args) > 5 else "2026-10-08"
    proc = psutil.Process()
    state = {"peak": 0, "stop": False, "phase": "start", "phase_peak": {}}

    def sampler():
        while not state["stop"]:
            r = proc.memory_info().rss
            if r > state["peak"]:
                state["peak"] = r
            p = state["phase"]
            if r > state["phase_peak"].get(p, 0):
                state["phase_peak"][p] = r
            time.sleep(SAMPLE_S)

    t = threading.Thread(target=sampler, daemon=True)
    t.start()

    sys.path.insert(0, os.path.join(root, "org", "missions", "D9", "IRPT", "IRPT_BCKEND", "deliverables", "0.9.0_WK_IRPT_BCKEND~265", "replay"))
    sys.path.insert(0, os.path.join(tree, "data", "assets", "scripts", "gold", "investor_reporting"))
    import boto3
    import holdings_snapshot as hs
    assert os.path.abspath(hs.__file__).startswith(os.path.abspath(tree)), "holdings_snapshot resolved outside the bundle"
    import replay_publish_gate as rp

    marks = []

    def mark(name):
        marks.append({"mark": name, "rss": proc.memory_info().rss, "t": round(time.time() - t0, 1)})

    def wrap(attr, phase):
        if not hasattr(hs, attr):
            return
        orig = getattr(hs, attr)

        def w(*a, **k):
            prev = state["phase"]
            state["phase"] = phase
            mark(phase + ":enter")
            try:
                return orig(*a, **k)
            finally:
                mark(phase + ":exit")
                state["phase"] = prev
        setattr(hs, attr, w)

    t0 = time.time()
    for attr in ("build_snapshot", "served_publication", "evaluate_publish_gate", "land"):
        wrap(attr, attr)

    gate_out = {}
    old_trees = [f.split("=", 1)[1] for f in flags if f.startswith("--old-gate=")]
    if old_trees:
        # SAME-INPUT arm (replay only, never the memory runs): the OLD tree's publish-gate code judges the SAME candidate against
        # the served publication it reads itself (the old served_publication, full node list), through the same publisher and index.
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "hs_old", os.path.join(old_trees[0], "data", "assets", "scripts", "gold", "investor_reporting", "holdings_snapshot.py"))
        old_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(old_mod)
        served_args = {}
        inner_served = hs.served_publication

        def capture_served(publisher, expected):
            served_args["a"] = (publisher, expected)
            return inner_served(publisher, expected)
        hs.served_publication = capture_served
    if "--gate-trace" in flags and hasattr(hs, "evaluate_publish_gate"):
        inner = hs.evaluate_publish_gate

        def tracing(candidate, served, *a, **k):
            res = inner(candidate, served, *a, **k)
            gate_out["decision"] = json.loads(json.dumps(res, sort_keys=True, default=str))
            gate_out["served_nodes"] = None if served is None else (served["node_count"] if "node_count" in served else len(served["nodes"]))
            if old_trees and served is not None:
                old_served = old_mod.served_publication(*served_args["a"])
                gate_out["old_gate_served_nodes"] = len(old_served["nodes"])
                old_res = old_mod.evaluate_publish_gate(candidate, old_served, *a, **k)
                gate_out["old_gate_decision"] = json.loads(json.dumps(old_res, sort_keys=True, default=str))
                gate_out["old_gate_equals_new_gate"] = gate_out["old_gate_decision"] == gate_out["decision"]
                del old_served
            return res
        hs.evaluate_publish_gate = tracing

    # table_lookups: every call of the tree's security-table lookup (_NarrowedClassifier.canonical_lookup: a symbol lookup, or the
    # CUSIP-key fallback after a symbol miss), counted at the call. NOT memoised unless --memo (the replay runs memoise; the census
    # runs do not, so wall_time_s is the producer's own).
    cls = getattr(hs, "_NarrowedClassifier", None)
    lookups = {"calls": 0, "cusip_key_calls": 0, "distinct": set()}
    if cls is not None:
        orig_lookup, memo = cls.canonical_lookup, {}
        use_memo = "--memo" in flags

        def cached_lookup(self, ticker):
            lookups["calls"] += 1
            lookups["distinct"].add(ticker)
            if str(ticker).upper().startswith("CUSIP:"):
                lookups["cusip_key_calls"] += 1
            if not use_memo:
                return orig_lookup(self, ticker)
            if ticker not in memo:
                memo[ticker] = orig_lookup(self, ticker)
            return memo[ticker]
        cls.canonical_lookup = cached_lookup

    ov = rp.Overlay()
    real_client = boto3.client
    boto3.client = lambda service, *a, **k: rp.Guard(real_client(service, *a, **k), ov)
    rec = {}
    try:
        s3 = boto3.client("s3", region_name="us-east-1")
        mark("run_firm:enter")
        state["phase"] = "run_firm"
        res = hs.run_firm(firm, s3, qa=False, upload=True, local_out=None, as_of=as_of)
        mark("run_firm:exit")
        json.dumps({"results": [res]}, indent=1, default=str)  # what main() prints after a firm
        mark("main_print:exit")
        g = res.get("publish_gate") or {}
        rec.update({"outcome": g.get("outcome", "ABSENT (no publish gate in this tree)"), "node_count": res["node_count"],
                    "business_date": res["business_date"], "put_count": len(ov.puts),
                    "overlay_bytes_held": sum(len(v[0]) for v in ov.objects.values())})
    except Exception as exc:  # noqa: BLE001
        rec["error"] = type(exc).__name__ + ": " + str(exc)[:200]
    state["stop"] = True
    t.join(2)
    mi = proc.memory_info()
    rec.update({"label": label, "firm": firm, "as_of": as_of, "python": sys.version.split()[0],
                "holdings_snapshot_has_gate": hasattr(hs, "evaluate_publish_gate"),
                "peak_wset_bytes": getattr(mi, "peak_wset", None), "peak_pagefile_bytes": getattr(mi, "peak_pagefile", None),
                "sampled_peak_rss_bytes": state["peak"], "table_lookups": lookups["calls"],
                "table_lookups_cusip_key": lookups["cusip_key_calls"], "table_lookups_distinct": len(lookups["distinct"]),
                "memoised": "--memo" in flags, "cpu_time_s": round(sum(proc.cpu_times()[:2]), 1), "sample_interval_s": SAMPLE_S,
                "phase_sampled_peak_rss": state["phase_peak"], "marks": marks, "seconds": round(time.time() - t0, 1)})
    with open(os.path.join(scratch, "mem_%s_%s.json" % (label, firm)), "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
    if gate_out:
        with open(os.path.join(scratch, "gate_%s_%s.json" % (label, firm)), "w", encoding="utf-8") as fh:
            json.dump(gate_out, fh, indent=1, sort_keys=True)
    print(label, firm, rec.get("outcome"), rec.get("error"), "peak_wset", rec["peak_wset_bytes"], "sampled", rec["sampled_peak_rss_bytes"],
          "seconds", rec["seconds"], flush=True)


if __name__ == "__main__":
    main()
