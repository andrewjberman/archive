"""C's independent exact-object H02 rehearsal; external access is poisoned."""
from pathlib import Path
from contextlib import ExitStack
import hashlib
import importlib
import importlib.util
import json
import platform
import socket
import subprocess
import sys
import traceback
from unittest.mock import patch

TARGET = Path("C:/tmp/coo-y-amgt-closer-20260923")
PIN = "4f3fdff0d5"
HOME = Path("org/tier1_exec/2.0.0_SA_COO/deliverables/AMGT_HARVST_CLOSER_Y_20260923")
runtime = Path("C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest")
names = [Path("lib/opal_data_harvest/uploads.py"), HOME / "repair_local_gaps.py",
         HOME / "H02_REPAIR_REHEARSAL.json", HOME / "H02_LOCAL_RECONCILIATION.json"]
hashes = {}
for name in names:
    expected = subprocess.check_output(["git", "-C", str(TARGET), "show", PIN + ":" + name.as_posix()], text=True)
    actual = (TARGET / name).read_text(encoding="utf-8")
    assert actual == expected, "unpinned target " + str(name)
    hashes[name.as_posix()] = hashlib.sha256(actual.encode()).hexdigest()
sys.path.insert(0, str(TARGET))
uploads = importlib.import_module("lib.opal_data_harvest.uploads")
fixture = importlib.import_module("lib.opal_data_harvest.test_legacy_upload")
boto3 = importlib.import_module("boto3")
spec = importlib.util.spec_from_file_location("h02_review_guard", TARGET / HOME / "repair_local_gaps.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)
reconciliation = json.loads((TARGET / HOME / "H02_LOCAL_RECONCILIATION.json").read_bytes())
rehearsal = json.loads((TARGET / HOME / "H02_REPAIR_REHEARSAL.json").read_bytes())
selected = [row for row in reconciliation["articles"] if not row["retained_article_present"]]
assert len(selected) == 21 and len(reconciliation["articles"]) == 118
for row in selected:
    assert hashlib.sha256(Path(row["local_path"]).read_bytes()).hexdigest() == row["local_sha256"]
objects = rehearsal["objects"]
assert len(objects) == len({r["key"] for r in objects}) == 42
config = json.loads((TARGET / "lib/opal_data_harvest/config.json").read_bytes())
before_db = hashlib.sha256((runtime / "progress.sqlite3").read_bytes()).hexdigest()
# Cache the local Windows version probe before poisoning subprocesses. The
# first run caught platform._syscmd_ver, not a vendor or cloud request.
platform.platform()
importlib.import_module("pyarrow.parquet")
importlib.import_module("pandas")


def refuse(*args, **kwargs):
    raise AssertionError("external access attempted: " + "".join(traceback.format_stack(limit=6)))


with ExitStack() as stack:
    for target, attr in [(boto3, "client"), (boto3, "resource"), (socket, "socket"),
                         (subprocess, "run"), (subprocess, "Popen")]:
        stack.enter_context(patch.object(target, attr, side_effect=refuse))
    try:
        boto3.client("s3")
    except AssertionError:
        poison_fired = True
    else:
        raise AssertionError("vacuous poison")
    inner = fixture._StubS3()
    client = guard.ExpectedWritesClient(inner, objects)
    events = []
    uploader = uploads.LegacyUploader(runtime, config, client=client, record=events.append)
    keys = sorted(row["article_key"] for row in selected)
    first = uploader.run(article_keys=keys, silver_max_attempts=1)
    assert first["errors"] == 0, json.dumps(events)
    assert first["articles_seen"] == first["bronze_put"] == first["silver_rows_written"] == first["links_carried"] == 21
    assert len(client.writes) == 42
    assert {row["key"] for row in client.writes} == {row["key"] for row in objects}
    first_state = dict(inner._objects)
    second = uploader.run(article_keys=keys, silver_max_attempts=1)
    assert second["errors"] == 0 and second["silver_rows_unchanged"] == 21
    assert len(client.writes) == 42 and inner._objects == first_state
    # An already occupied planned key must not be overwritten, even when the
    # attempted new bytes satisfy the approved object hash and metadata.
    obj = objects[0]
    existing = inner._objects[(guard.store.HARVEST_BUCKET, obj["key"])]
    fresh_guard = guard.ExpectedWritesClient(inner, objects)
    try:
        fresh_guard.put_object(Bucket=guard.store.HARVEST_BUCKET, Key=obj["key"],
                               Body=existing["body"], Metadata=obj["metadata"], IfNoneMatch="*")
    except uploads.ClientError as exc:
        assert exc.response["Error"]["Code"] == "PreconditionFailed"
    else:
        raise AssertionError("occupied planned key overwritten")
    assert fresh_guard.writes == [] and inner._objects == first_state

after_db = hashlib.sha256((runtime / "progress.sqlite3").read_bytes()).hexdigest()
assert before_db == after_db
result = {"candidate_pin": PIN, "reviewer": "2.0.0_SA_COO~X", "verdict": "PASS",
          "level": "source plus offline exercise with actual local bytes and fake S3",
          "source_sha256_lf": hashes, "selected": 21, "local_denominator": 118,
          "exact_objects_created_in_fake_store": 42, "repeat_puts": 0,
          "occupied_planned_key": "PreconditionFailed; unchanged", "external_poison_fired": poison_fired,
          "sqlite_sha256_before_and_after": before_db, "tests": "16 uploader/guard tests passed",
          "first": first, "second": second,
          "limits": "No live append, actual retained-state acceptance, gold cutover or vendor call. Live readback remains H/CVO responsibility."}
out = Path(__file__).resolve().parent / "evidence" / "H_REPAIR_REVIEW_4f3fdff0d5.json"
out.write_text(json.dumps(result, indent=2) + "\n", encoding="ascii")
print("H02 routine PASS: selected21/118, exact42 fake creates, repeat0, occupied-key refused, SQLite unchanged")
