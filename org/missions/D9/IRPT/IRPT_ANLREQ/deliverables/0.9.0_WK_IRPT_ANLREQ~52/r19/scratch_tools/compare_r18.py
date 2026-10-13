"""Compare the AR-y-191 RUN results with the round-18 trace (MIXED_VERSION_TRACE_THIRD_READER.json).

Usage: python compare_r18.py <run_record.json> <r18_trace.json>
Prints, per sheet, the round-18 value and the RUN value for: the pinned door (round 18: INFERRED), the moved-pair door,
the pinned-stored re-open under the pinned pair and the moved pair, the r18.1-stored re-open under the pinned pair,
the reader-only re-open, and the reader-level codes of both readers.
"""
import json
import sys

run = json.load(open(sys.argv[1], encoding="utf-8"))
r18 = json.load(open(sys.argv[2], encoding="utf-8"))
rows18 = r18["cases"]
ref = {}
for c in rows18:
    ref[(c["writer_version"], c["reader_version"], c["input"])] = c

def door_run(sheet, door):
    for d in run["door_cases"]:
        if d["sheet"] == sheet and d["door"] == door:
            return d["outcome"]
    return "MISSING"

def reopen_run(sheet, writer, reader):
    for r in run["reopen_cases"]:
        if r["sheet"] == sheet and r["writer"].startswith(writer) and r["reader"].startswith(reader):
            return r["outcome"]
    return "MISSING"

diffs, lines = [], []
sheets = sorted({d["sheet"] for d in run["door_cases"]})
for s in sheets:
    p = ref.get(("lambda_pinned", "lambda_pinned", s))
    n = ref.get(("new", "new", s))
    x = ref.get(("new", "lambda_pinned", s))
    y = ref.get(("lambda_pinned", "new", s))
    def lead(v):
        return None if v is None else str(v).split(" (")[0].split(" ")[0]
    pairs = [
        ("door: pinned uploads + pinned reader", "r18 INFERRED (no finding on reader output)", p, None, door_run(s, "pinned pair"), "NORMALIZED"),
        ("door: moved uploads + r18.1 reader", "r18 in-world actual (new,new)", n, "writer_door", door_run(s, "moved pair"), None),
        ("re-open pinned-stored, pinned pair", "r18 computed (lambda_pinned,lambda_pinned) pinned gate", p, "computed_reopen_lambda_pinned_uploads", reopen_run(s, "pinned pair", "pinned pair"), None),
        ("re-open pinned-stored, moved pair", "r18 computed (lambda_pinned,new) head gate", y, "computed_reopen_head_uploads_gate", reopen_run(s, "pinned pair", "moved pair"), None),
        ("re-open pinned-stored, reader-only", "r18 computed (lambda_pinned,new) pinned gate", y, "computed_reopen_lambda_pinned_uploads", reopen_run(s, "pinned pair", "reader-only"), None),
        ("re-open moved-stored, pinned pair", "r18 computed (new,lambda_pinned) pinned gate", x, "computed_reopen_lambda_pinned_uploads", reopen_run(s, "moved pair", "pinned pair"), None),
    ]
    row = {"sheet": s}
    for label, src, rec, key, run_v, const in pairs:
        if const is not None:
            r18_v = const if rec is not None and False else None
        if label.startswith("door: pinned"):
            r18_v = "NORMALIZED (inferred; no reader finding)" if p and not p.get("reader_reader_level_codes") else "?"
        elif label.startswith("door: moved"):
            r18_v = (rec or {}).get("writer_door") if rec else "NOT IN R18"
        else:
            r18_v = (rec or {}).get(key) if rec else None
            if r18_v is None and rec is None:
                r18_v = "NOT STORED IN R18 (writer stored nothing)"
        same = lead(r18_v) == lead(run_v) if r18_v and run_v and run_v != "MISSING" else None
        if run_v == "MISSING":
            same = "not run: writer stored nothing"
        row[label] = {"r18": r18_v, "run": run_v, "same_leading_outcome": same}
    lines.append(row)

for row in lines:
    print("== %s" % row["sheet"])
    for k, v in row.items():
        if k != "sheet":
            print("   %-48s r18=%-52s run=%-60s same=%s" % (k[:48], str(v["r18"])[:52], str(v["run"])[:60], v["same_leading_outcome"]))
print("r18 cases: %d; run cases: door %d, reopen %d" % (len(rows18), len(run["door_cases"]), len(run["reopen_cases"])))
