"""IB-pr-525 arms, run on the BUILT zip's own handler.py bytes (round 188, worker 0.9.0_WK_IRPT_BCKEND~372).

Adapted from deliverables/0.9.0_WK_IRPT_BCKEND~369 harness (the round-187 stubbed harness p187_cells.py, _patches and _run,
copied here; the check file is untouched). Usage:
    python -I ib188_arms.py <extracted_built_root>
The extracted root is a scratch directory holding the built zip's members (handler.py at its root). No AWS call is made:
s3 is a placeholder object and every function that would reach S3 or the producer is patched with a recorder.
Prints one JSON object: the four arms with their observed call sequences and refusals, and the verdicts.
"""
import contextlib
import io
import json
import os
import sys
from unittest import mock

ROOT = os.path.abspath(sys.argv[1])
NEWEST = "2026-10-06"
DAYS_LOTS = ["2026-09-28", "2026-09-29", "2026-09-30"]


def _patches(h, calls):
    import pandas as pd

    def compute(s3, days, accounts, thresholds, workers=12):
        calls.append(("compute", list(days)))
        return pd.DataFrame([{"business_date": d, "account_id": a} for d in days for a in accounts]), "49financial", "2020-01-01"

    def emit_day(s3, part, firm, day, upload=True, thresholds=None, first_data_date=None, src=None):
        calls.append(("emit_day", day))
        return {"rows": len(part), "landed": upload}

    def emit_classes(s3, firm, days, upload=True):
        calls.append(("emit_classes", list(days)))
        return {}, {}

    def emit_lots(s3, firm, days, accounts, upload=True, workers=12):
        calls.append(("emit_lots", list(days), list(accounts)))
        return {d: 1 for d in days}, {}

    return [
        mock.patch.object(h.ard, "load_declaration", lambda: {}),
        mock.patch.object(h.ard, "declared_sources", lambda doc: ["src"]),
        mock.patch.object(h.ard, "source_entry", lambda doc, s: {}),
        mock.patch.object(h.ard, "firm_scope", lambda src: "49financial"),
        mock.patch.object(h, "_gold_location", lambda firm: ("b", "p/")),
        mock.patch.object(h, "newest_landed_day", lambda s3, b, p: NEWEST),
        mock.patch.object(h, "population_accounts", lambda s3, firm: (NEWEST, ["P1", "P2"])),
        mock.patch.object(h, "newest_accounts", lambda s3, b, p, d: ["P1"]),
        mock.patch.object(h, "load_thresholds", lambda: {"t": 1}),
        mock.patch.object(h, "compute", compute),
        mock.patch.object(h.ard, "emit_day", emit_day),
        mock.patch.object(h, "emit_classes", emit_classes),
        mock.patch.object(h, "emit_lots", emit_lots),
        mock.patch.object(h, "record_lots_status", lambda *a, **k: None),
    ]


def _run(event, root):
    if root not in sys.path:
        sys.path.insert(0, root)
    for name in [m for m in sys.modules if m == "handler"]:
        del sys.modules[name]
    import handler as h
    calls = []
    stack = _patches(h, calls)
    for p in stack:
        p.start()
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            out = h.run(object(), "2026-10-02", event)
        return {"out_stages": (out or {}).get("stages") if isinstance(out, dict) else None, "refused": None,
                "log_lines": len(buf.getvalue().splitlines())}, calls
    except SystemExit as e:
        return {"out_stages": None, "refused": str(e), "log_lines": len(buf.getvalue().splitlines())}, calls
    finally:
        for p in reversed(stack):
            p.stop()


if __name__ == "__main__":
    base = {"backfill": {"start": "2026-09-28", "end": "2026-09-30"}, "accounts": "population"}
    result = {"root": "built_root", "arms": {}}

    res_a, calls_a = _run(dict(base, stages=["lots"]), ROOT)
    names_a = [c[0] for c in calls_a]
    lots_a = [c for c in calls_a if c[0] == "emit_lots"]
    no_returns = not any(n in ("compute", "emit_day", "emit_classes") for n in names_a)
    lots_once = len(lots_a) == 1 and lots_a[0][1] == DAYS_LOTS and bool(lots_a[0][2])
    result["arms"]["lots_only_no_returns_calls"] = {
        "calls": names_a, "refused": res_a["refused"], "stages_named": res_a["out_stages"],
        "verdict": "no_returns_call" if (no_returns and lots_once and res_a["refused"] is None) else "NOT_MET"}

    res_b, calls_b = _run(dict(base), ROOT)
    names_b = [c[0] for c in calls_b]
    want_b = ["compute", "emit_day", "emit_day", "emit_day", "emit_classes", "emit_lots"]
    result["arms"]["default_event_unchanged"] = {
        "calls": names_b, "refused": res_b["refused"],
        "verdict": "unchanged" if (names_b == want_b and res_b["refused"] is None) else "NOT_MET"}

    refusal_rows = []
    all_refused = True
    for label, extra in (("unknown_stage", {"stages": ["lots", "nonsense"]}), ("empty_list", {"stages": []}),
                         ("returns_only", {"stages": ["returns"]}), ("string", {"stages": "lots"})):
        r, c = _run(dict(base, **extra), ROOT)
        ok = r["refused"] is not None and "REFUSED" in r["refused"] and "stages" in r["refused"].lower() and not c
        all_refused = all_refused and ok
        refusal_rows.append({"case": label, "refused_by_name": ok, "calls": [x[0] for x in c], "message": (r["refused"] or "")[:160]})
    result["arms"]["malformed_stages_refused"] = {"cases": refusal_rows, "verdict": "refused" if all_refused else "NOT_MET"}

    r_d, c_d = _run({"accounts": ["P1"], "stages": ["lots"]}, ROOT)
    ok_d = r_d["refused"] is not None and "REFUSED" in r_d["refused"] and not c_d
    result["arms"]["scheduled_event_stages_refused"] = {
        "calls": [x[0] for x in c_d], "message": (r_d["refused"] or "")[:160],
        "verdict": "refused" if ok_d else "NOT_MET"}

    result["arms_run_on"] = "built_zip_handler_py_bytes"
    print(json.dumps(result, indent=1, sort_keys=True))
