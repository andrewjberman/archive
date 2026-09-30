"""HVST-aa-1 AC2: replay HVST-q-1's recorded job shapes (run 20260930T084110Z-run-4ee47491) through
the new worker/publisher code on stubs.

Reads, READ-ONLY, from the runtime root: runs/<q-1 jobs>.json, the recorded bbg runs of the same UTC
day (for the rejection), progress.sqlite3's harvest_listing_outbox (metadata only) and the cached
listing pages it points at (harvest_listing/*). Writes only to a temp directory. Sockets are blocked
and every stub transport call is counted; the last line printed is the network-call total.

Run: python org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~76/scripts/aa1_ac2_replay_q1.py
"""

import datetime as dt
import hashlib
import json
import socket
import sqlite3
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[8]
sys.path.insert(0, str(REPO))
RUNTIME = REPO.parent / "ajb_workspace" / ".runtime" / "opal-data-harvest"
if not RUNTIME.is_dir():
    RUNTIME = Path("C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest")

from lib.opal_data_harvest import harvest_grammar  # noqa: E402
from lib.opal_data_harvest.publishers import Publisher  # noqa: E402
from lib.opal_data_harvest.worker import Worker  # noqa: E402
from lib.opal_data_harvest.test_bronze_capture import _StubS3  # noqa: E402

RUN_ID = "20260930T084110Z-run-4ee47491"
NETWORK = {"socket_connects": 0, "transport_calls": 0}
SECURITY = {"key": "992_HK_Equity", "ticker": "992 HK", "company": "Lenovo", "aliases": ["Lenovo"]}


def _refuse(*args, **kwargs):
    NETWORK["socket_connects"] += 1
    raise AssertionError("NETWORK CALL ATTEMPTED")


socket.socket.connect = _refuse
socket.create_connection = _refuse


class CountingSession:
    """Any GET through the publisher's session is a network call: counted, then refused."""
    captured = []

    def get(self, url, **kwargs):
        NETWORK["transport_calls"] += 1
        raise AssertionError("TRANSPORT CALL ATTEMPTED: %s" % url)

    def close(self):
        pass


class CountingBbgModule:
    def search(self, session, query, page=1):
        NETWORK["transport_calls"] += 1
        raise AssertionError("bbg search ATTEMPTED (page %s)" % page)

    def article(self, session, identity):
        NETWORK["transport_calls"] += 1
        raise AssertionError("bbg article FETCH ATTEMPTED: %s" % identity)


def _json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def recorded_shapes():
    """The recorded facts the replay is built from -- all read from the runtime root."""
    record = _json(RUNTIME / "run_records" / (RUN_ID + ".json"))
    jobs = {job["publisher"]: _json(RUNTIME / "runs" / (job["job_id"] + ".json")) for job in record["jobs"]}
    conn = sqlite3.connect("file:%s?mode=ro" % (RUNTIME / "progress.sqlite3").as_posix(), uri=True)
    pages = {}
    for pub, query, page, path, sha in conn.execute(
            "SELECT publisher,query,page,path,sha256 FROM harvest_listing_outbox WHERE publisher IN ('wsj','bbg') "
            "AND query IN ('Lenovo','\"Lenovo\"') ORDER BY id"):
        body = Path(path).read_bytes()
        assert hashlib.sha256(body).hexdigest() == sha, "listing file does not match its recorded hash"
        pages[(pub, query, page)] = body  # the latest capture per (publisher, query, page)
    conn.close()
    return record, jobs, pages


def bbg_rejection_of_that_day():
    """The rejection HVST-p-2 records: the recorded 09-30 bbg jobs that FETCHED a key that no
    accepted article came from, with a rejected entry whose issues are short_or_partial_body."""
    found = {}
    for path in sorted((RUNTIME / "runs").glob("20260930*bbg*.json")):
        job = _json(path)
        stored = {a["article_key"] for a in job.get("accepted", [])}
        unstored = [k for k in job.get("fetched_keys", []) if k not in stored]
        issues = [r["issues"] for r in job.get("rejected", []) if "short_or_partial_body" in r["issues"]]
        if len(unstored) == 1 and issues:
            found[unstored[0]] = issues[0]
    return found


def seed_known(worker, publisher, entries):
    """Rows in the worker's articles table so the job's known_ids / known_urls hold what q-1's did."""
    folder = worker.root / "seeded"
    folder.mkdir(exist_ok=True)
    for index, (identity, url) in enumerate(entries):
        saved = folder / ("%s-%d.json" % (publisher, index))
        saved.write_text(json.dumps({"url": url, "article_id": identity}), encoding="utf-8")
        worker.db.execute("INSERT OR REPLACE INTO articles VALUES(?,?,?,?,?)",
                          (publisher, SECURITY["key"], identity, "seed-%d" % index, str(saved)))
    worker.db.commit()


def factory(publisher, envelope, record, *args):
    client = Publisher(publisher, envelope, record)
    client.session = CountingSession()   # marks the session built: the real transport is never made
    client.module = CountingBbgModule()  # (bbg's module double; unused by wsj)
    return client


class Sessions:
    def get(self, publisher):
        return {"generation": 0}


def main():
    record, jobs, pages = recorded_shapes()
    print("REPLAY of %s: jobs %s" % (RUN_ID, [(j["publisher"], j["status"], j["reached_span"]) for j in record["jobs"]]))
    rejected = bbg_rejection_of_that_day()
    print("recorded rejection (bbg jobs of 2026-09-30, fetched and not stored): %s" % rejected)
    stub = _StubS3()
    now = dt.datetime.now(dt.timezone.utc)
    for (pub, query, page), body in pages.items():
        ext = "html" if pub == "wsj" else "json"
        harvest_grammar.put_listing_bronze(pub, query, page, body, ext, now, client=stub)
    with tempfile.TemporaryDirectory() as scratch:
        config = {"harvest_grammar": True, "new_only": True, "articles_per_security": 5, "candidate_limit": 20,
                  "minimum_request_seconds": 0, "jitter_seconds": 0, "retrieval_mode": "backfill",
                  "backfill_floor": "2000-01-01", "max_listing_pages": {"wsj": 3, "bbg": 2}}
        worker = Worker(scratch, config, factory, Sessions(), harvest_client=stub)
        # the held-key side: the rejected key is on the books as the base's rejection recorded it
        for key, issues in rejected.items():
            worker._hold_on_rejection(key, issues)
        skipped = {pub: jobs[pub]["skipped_keys"] for pub in jobs}
        seed_known(worker, "wsj", [("wsj-seed-%d" % i, e["key"][len("wsj:"):])
                                   for i, e in enumerate(skipped["wsj"]) if e["why"] == "known_urls"])
        # bbg's known ids: q-1's own known_ids skips plus every article the earlier 09-30 bbg jobs
        # stored (q-1 stopped at the rejected key, before it reached the later hits)
        known = {e["key"][len("bbg:"):] for e in skipped["bbg"] if e["why"] == "known_ids"}
        for path in sorted((RUNTIME / "runs").glob("20260930*bbg*.json")):
            known |= {str(a["article_id"]) for a in _json(path).get("accepted", [])}
        print("bbg known_ids seeded: %d (q-1 recorded previously_stored=%s)" % (len(known), jobs["bbg"]["previously_stored"]))
        seed_known(worker, "bbg", [(identity, "https://seed/bbg:%s" % identity) for identity in sorted(known)])
        results = worker.run([SECURITY], ["bbg", "wsj"], max_jobs=2)
        by_pub = {r["publisher"]: r for r in results}
        wsj, bbg = by_pub["wsj"], by_pub["bbg"]
        run_record = json.loads(worker.last_run_record.read_text(encoding="utf-8"))
        worker.close()

    print("wsj: status=%s  reached_span=%s  (q-1 recorded reached_span=%s)" % (
        wsj["status"], json.dumps(wsj["reached_span"]), jobs["wsj"]["reached_span"]))
    assert wsj["reached_span"] and wsj["reached_span"].get("from_cache") is True
    print("wsj: fetched_keys=%d listing requests=0 (all %d pages served from cached listing bronze)" % (
        len(wsj["fetched_keys"]), len([k for k in pages if k[0] == "wsj"])))
    held = {e["key"]: e for e in bbg.get("held_keys", [])}
    print("bbg: status=%s  fetched_keys=%s  held_keys=%s" % (bbg["status"], bbg["fetched_keys"], json.dumps(list(held.values()))))
    print("bbg: q-1 recorded fetched_keys=%s" % jobs["bbg"]["fetched_keys"])
    for key in rejected:
        assert key not in bbg["fetched_keys"] and held[key]["state"] == "held" and held[key]["fetched_this_run"] is False
        print("HELD (not fetched): %s  state=%s reason=%s failed_days=%s" % (
            key, held[key]["state"], held[key]["reason"], held[key]["failed_days"]))
    print("run record keys_held: %s" % json.dumps(run_record["keys_held"]))
    print("stub transport calls: %d   socket connects attempted: %d" % (NETWORK["transport_calls"], NETWORK["socket_connects"]))
    print("NETWORK CALLS MADE: %d" % (NETWORK["transport_calls"] + NETWORK["socket_connects"]))


if __name__ == "__main__":
    main()
