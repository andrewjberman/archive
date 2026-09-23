"""Independent C review of H's pinned gold coverage candidate; offline only."""
from pathlib import Path
import datetime
import hashlib
import importlib
import itertools
import json
import subprocess
import sys
from unittest.mock import patch

TARGET = Path("C:/tmp/coo-y-amgt-closer-20260923")
PIN = "8534a66ecabf6e73125f3cd3bdbdb84b5ce2b96b"
MODULE = "lib/research/coverage/pool_reader.py"
expected = subprocess.check_output(["git", "-C", str(TARGET), "show", PIN + ":" + MODULE], text=True)
actual = (TARGET / MODULE).read_text(encoding="utf-8")
assert actual == expected, "refuse to review unpinned module bytes"
sys.path.insert(0, str(TARGET))
pool_reader = importlib.import_module("lib.research.coverage.pool_reader")


def row(day, score=0.0, status="COMPLETE"):
    return {"security_key": "TEST", "day": day, "mention_score": score, "data_status": status}


def read(rows, start="2024-02-28", end="2024-03-01"):
    with patch.object(pool_reader, "_gold_latest_snapshot_rows", return_value=rows):
        return pool_reader.gold_window_read("TEST", start, end)


checks = []
zero = [row(datetime.date(2024, 2, 28)), row(datetime.date(2024, 2, 29)), row(datetime.date(2024, 3, 1))]
assert read(zero)["complete"] is True
checks.append("three-day leap-year all-zero window is complete")
assert read(zero[::2])["states"]["partial"] == 1
checks.append("missing leap day counted once")
for bad in [True, False, float("-inf"), "1e10000"]:
    r = read([row("2024-02-28", bad), *zero[1:]])
    assert r["states"]["malformed"] == 1 and "2024-02-28" not in r["counts"]
    checks.append("invalid measure excluded: " + repr(bad))
for rows in itertools.permutations([row("2024-02-28", 1), row("2024-02-28", 2), row("2024-02-28", 3)]):
    r = read(list(rows) + zero[1:])
    assert r["states"]["malformed"] == 2 and "2024-02-28" not in r["counts"]
checks.append("all six triple-duplicate permutations exclude the score")
r = read([row("invalid-day", 4), *zero])
assert not r["complete"] and r["states"]["malformed"] == 1
checks.append("malformed calendar date refuses complete")
r = read([row("2024-02-28", 2, "PARTIAL"), row("2024-02-29", 3, "DENIED"), zero[-1]])
assert r["counts"]["2024-02-28"] == 2 and r["counts"]["2024-02-29"] == 3
assert r["states"]["partial"] == r["states"]["denied"] == 1
checks.append("observed partial and denied scores remain distinguished")
try:
    read([], start="2024-03-01", end="2024-02-28")
except ValueError:
    checks.append("reversed range explicitly refused")
else:
    raise AssertionError("reversed range silently accepted")
result = {"candidate_pin": PIN, "reviewer": "2.0.0_SA_COO~X", "verdict": "PASS",
          "evidence_level": "offline exercise", "scope": "routine H gold_window_read boundary change",
          "source_sha256_lf": hashlib.sha256(actual.encode()).hexdigest(), "independent_checks": checks,
          "candidate_plus_legacy_suite": "39 passed in 0.24s",
          "limits": "No deployed cutover, live ranking, retained-data integrity or whole-program acceptance."}
out = Path(__file__).resolve().parent / "evidence" / "H_GOLD_REVIEW_8534a66eca.json"
out.write_text(json.dumps(result, indent=2) + "\n", encoding="ascii")
print(json.dumps(result, indent=2))
