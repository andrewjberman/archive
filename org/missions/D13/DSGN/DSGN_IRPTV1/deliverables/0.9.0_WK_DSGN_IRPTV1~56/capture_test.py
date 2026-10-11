"""Capture the producer's own served bodies, offline, from the producer's own test worlds. Copied into the ops/tests folder of
an OUTSIDE export (r5 = the release's pin, r6 = revision 6's pin) and run there. Writes JSON to $CAPTURE_DIR."""
import json
import os
import threading

import test_owned_report as support
from test_owned_report import report_world  # noqa: F401
from test_owned_requests import retention_world, world  # noqa: F401
import test_owned_requests as treq

OUT = os.environ["CAPTURE_DIR"]
os.makedirs(OUT, exist_ok=True)
TOKENS = ("history-one", "history-two", "history-three")


def dump(name, value):
    with open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=1, sort_keys=True)


def test_sections_bodies(report_world):  # noqa: F811
    r = report_world
    dump("sections_ycharts", r.reader.sections(r.w.case.principal, r.id))
    document = support._opal_document(r.report["request_ref"])
    support._publish(r, document)
    dump("sections_opal", r.reader.sections(r.w.case.principal, r.id))


def test_history_and_read_bodies(world):  # noqa: F811
    reader, records, _ = treq.setup(world, TOKENS)
    page = reader.history(world.case.principal)
    dump("history_upload", page)
    request_id = records[0]["identity"]["request_id"]
    dump("read_plain", reader.read(world.case.principal, request_id))
    dump("read_opted", reader.read(world.case.principal, request_id, include_comparisons=True, include_composition=True))


def test_history_selected_and_unreadable(world):  # noqa: F811
    if not hasattr(__import__("owned_requests"), "SelectionUnreadable"):
        return  # revision 6 has no client member to capture
    import test_history_row_client as h
    reader, records, _ = treq.setup(world, TOKENS)
    h.counted_reads(world, client="client-a")
    dump("history_selected", reader.history(world.case.principal))
    counting = world.stores.artifacts.get
    lock, seen = threading.Lock(), []

    def get(principal, artifact_id, **kwargs):
        saved = counting(principal, artifact_id, **kwargs)
        with lock:
            seen.append(artifact_id)
            broken = len(seen) == 1
        if broken:
            document = json.loads(saved["data"])
            document["browser"] = "x"
            return dict(saved, data=json.dumps(document).encode())
        return saved
    world.stores.artifacts.get = get
    dump("history_unreadable", reader.history(world.case.principal))


def test_status_job_opal_dates(report_world):  # noqa: F811
    """derive() on an OPAL_ENGINE document, wrapped as owned_status.read wraps it, then the public view entry.py serves."""
    import prospect_dates
    import status
    r = report_world
    document = support._opal_document(r.report["request_ref"])
    sha = "ab" * 32
    input_ref = {"input_id": "portfolio_" + sha, "content_sha256": sha}
    identity = {"request_id": "REQ-" + "1" * 24, "revision": 1}
    detail = {"report_id": "RPT-" + "2" * 32, "revision": "3" * 64}
    out = {}
    try:
        dates = prospect_dates.derive(input_ref, document, detail, identity)
        env = status.build_envelope(identity["request_id"], "prospect_analysis" if "date_basis" in dates else "analysis_generate",
                                    "1", "READY", None, source_dates=dates, public_reason_code="ANALYSIS_READY", actions=[])
        out = {"result": "ANSWER", "body": status.public_view(env)}
    except Exception as exc:  # the revision-6 control: the census refuses
        out = {"result": "REFUSED", "code": str(exc)}
    dump("status_job_opal", out)
