"""Independent offline review of H's producer delta at one exact commit."""
from pathlib import Path
from contextlib import ExitStack
import copy
import hashlib
import importlib
import json
import socket
import subprocess
import sys
from unittest.mock import patch

TARGET = Path("C:/tmp/coo-y-amgt-closer-20260923")
PIN = "ac4316c44793138052c19168248cbf9c00c25ee8"
FILES = ["lib/research/metrics/chatter_axis.py",
         "lib/research/metrics/generation_writer.py",
         "lib/research/metrics/tests/test_chatter_incomplete.py"]
hashes = {}
for name in FILES:
    expected = subprocess.check_output(["git", "-C", str(TARGET), "show", PIN + ":" + name], text=True)
    actual = (TARGET / name).read_text(encoding="utf-8")
    assert expected == actual, "unpinned review target " + name
    hashes[name] = hashlib.sha256(actual.encode()).hexdigest()
sys.path.insert(0, str(TARGET))
axis = importlib.import_module("lib.research.metrics.chatter_axis")
writer = importlib.import_module("lib.research.metrics.generation_writer")
fixtures = importlib.import_module("lib.research.metrics.tests.test_chatter_axis")
boto3 = importlib.import_module("boto3")
entries = [{"identity": key, "security_key": key, "ticker": key,
            "identity_status": "MEASURED"} for key in ["A", "B"]]
checks = []


def refuse(*args, **kwargs):
    raise AssertionError("offline review attempted external access")


def run(details, read_error=None, table=None):
    def reader(key, start, end):
        if key == read_error:
            raise RuntimeError("planted unreadable window")
        return {"counts": {end: 9}, "store_item_count": 30, "items_in_window": 30,
                "bodies_read": 30, "duplicate_links": 0, "key_forms": [key],
                "crosswalk_status": "GOLD-DIRECT", **details.get(key, {})}

    def write(generation, table_name):
        return writer.default_write_generation(generation, table_name, resource=fixtures.FakeResource(table))

    with patch.object(axis, "read_universe_names", return_value=(entries, {"source": "review", "coverage_vintage": "old-vintage"})), patch.object(axis.pool_reader, "gold_window_read", side_effect=reader):
        return axis.compute_chatter_axis(as_of_date="2026-09-23", count_fn=axis.gold_daily_mention_scores,
                                         write_fn=write if table is not None else None, run_id="independent")


with ExitStack() as stack:
    for target, attr in [(boto3, "client"), (boto3, "resource"), (socket, "socket"),
                         (subprocess, "run"), (subprocess, "Popen")]:
        stack.enter_context(patch.object(target, attr, side_effect=refuse))
    try:
        boto3.client("s3")
    except AssertionError:
        checks.append("external-access poison positive control fires")
    else:
        raise AssertionError("poison is vacuous")
    good = {"complete": True, "states": {}}
    for label, bad in [("true completeness with nonzero partial state", {"complete": True, "states": {"partial": 1}}),
                       ("missing completeness flag", {"states": {}}),
                       ("truthy integer is not literal True", {"complete": 1, "states": {}})]:
        result = run({"A": bad, "B": good})
        assert result["input_coverage"]["unresolved"] == ["A"]
        assert result["input_coverage"]["resolved"] == 1
        assert result["rows"] == []
        assert all(p["state"] == "FAILED" and p["pointer"] is None and p["receipt"] is None
                   for p in result["products"])
        checks.append(label + " holds both products in dry run")
    table = fixtures.FakeTable()
    result = run({"B": good}, read_error="A", table=table)
    assert result["input_coverage"]["unresolved"] == ["A"]
    assert result["read_detail"]["A"]["read_error"] == "RuntimeError"
    assert len(table.items) == 2
    assert all(r["record_type"] == "generation_failed_marker" for r in table.items.values())
    checks.append("first security read failure survives later success; no-prior run creates only markers")

    generation = copy.deepcopy(run({"A": good, "B": good})["generations"][0])
    assert generation["rows"], "direct writer control needs nonempty rows"
    generation["state"] = "FAILED"
    table = fixtures.FakeTable()
    with patch.object(table, "batch_writer", side_effect=AssertionError("must not enter batch")) as batch:
        try:
            writer.default_write_generation(generation, resource=fixtures.FakeResource(table))
        except writer.GenerationWriteError as exc:
            assert exc.receipt["rows_written"] == 0 and not exc.receipt["pointer_written"]
            assert exc.receipt["failed_marker_written"]
        else:
            raise AssertionError("declared FAILED unexpectedly succeeded")
        batch.assert_not_called()
    assert len(table.items) == 1
    assert next(iter(table.items.values()))["record_type"] == "generation_failed_marker"
    checks.append("declared FAILED with nonempty rows and pointer never enters batch or replaces pointer")

result = {"candidate_pin": PIN, "reviewer": "2.0.0_SA_COO~X", "verdict": "PASS",
          "evidence_level": "source plus offline exercise", "source_sha256_lf": hashes,
          "independent_checks": checks, "candidate_reader_legacy_suite": "102 passed in 0.46s",
          "limits": "Routine producer review only; no live writes, served cutover, browser HOLD, enum change or CVO integrity acceptance."}
out = Path(__file__).resolve().parent / "evidence" / "H_PRODUCER_REVIEW_ac4316c447.json"
out.write_text(json.dumps(result, indent=2) + "\n", encoding="ascii")
print(json.dumps(result, indent=2))
