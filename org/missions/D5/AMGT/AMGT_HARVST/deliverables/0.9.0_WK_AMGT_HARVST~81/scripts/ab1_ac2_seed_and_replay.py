"""HVST-ab-1 AC2: the seed against the runtime root, then a replay of the recorded bbg and wsj job
shapes through the new code on stubs.

1. SEED. `ab1_seed_hold.seed` derives the `bbg:NM5NLQ6K50XZ01` hold row from the runtime
   `events.jsonl` through the hold's own rule and INSERT OR IGNOREs it into the runtime
   `rejected_hold` (the ONE runtime write). Printed before and after; a second run changes nothing.
2. wsj REPLAY. The recorded wsj listing page (runtime `harvest_listing/`, read-only) is served by a
   stub transport to a LIVE wsj job; the job's `reached_span` is printed beside the page's own date
   bounds.
3. bbg REPLAY. The recorded bbg listing pages (p1, p2 -- p2 carries NM5NLQ6K50XZ01) are served to a
   harvest-mode bbg job over a scratch root holding the seeded row read back from the runtime db. The
   story route of the seeded key is counted: on the hold's day it is HELD (0 requests); the next UTC day
   is the hold's designed retry (1 request).

Sockets are blocked and counted for the whole script. No publisher, no S3.
"""

import datetime as dt
import json
import socket
import sqlite3
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[7]
for entry in (str(REPO), str(HERE)):
    if entry not in sys.path:
        sys.path.insert(0, entry)

import ab1_seed_hold  # noqa: E402

NETWORK_CALLS = []


def _refuse(*args, **kwargs):
    NETWORK_CALLS.append(args[:2])
    raise AssertionError("NETWORK CALL ATTEMPTED")


socket.socket.connect = _refuse
socket.create_connection = _refuse

from bs4 import BeautifulSoup  # noqa: E402

from lib.opal_data_harvest import worker as worker_module  # noqa: E402
from lib.opal_data_harvest.publishers import DowJones  # noqa: E402
from lib.opal_data_harvest.test_aa1_cached_reach_and_hold import _factory  # noqa: E402
from lib.opal_data_harvest.test_bronze_capture import _StubS3  # noqa: E402
from lib.opal_data_harvest.test_n1_received_bytes_and_run_record import BASE_CONFIG  # noqa: E402
from lib.opal_data_harvest.test_n1_received_bytes_and_run_record import SECURITY  # noqa: E402
from lib.opal_data_harvest.test_n1_received_bytes_and_run_record import _BBGModule  # noqa: E402
from lib.opal_data_harvest.test_n1_received_bytes_and_run_record import _PUBLISHED  # noqa: E402
from lib.opal_data_harvest.test_n1_received_bytes_and_run_record import _Sessions  # noqa: E402
from lib.opal_data_harvest.test_n1_received_bytes_and_run_record import _next_data_html  # noqa: E402
from lib.opal_data_harvest.test_n1_received_bytes_and_run_record import _typed  # noqa: E402
from lib.opal_data_harvest.test_n1_received_bytes_and_run_record import make_factory  # noqa: E402

RUNTIME = ab1_seed_hold.RUNTIME_ROOT
LISTINGS = RUNTIME / "harvest_listing"
WSJ_PAGE = LISTINGS / "wsj_p1_e513433c8e6841d6.html"
BBG_PAGES = {1: LISTINGS / "bbg_p1_30dc8b1ceb74344a.json", 2: LISTINGS / "bbg_p2_f24dcb2958e9f3c7.json"}
STORY = "https://www.bloomberg.com/article/api/story/id/%s"


def section(title):
    print("\n== %s ==" % title)


def step_seed():
    section("1. SEED bbg:NM5NLQ6K50XZ01 into the runtime rejected_hold")
    result = ab1_seed_hold.main()
    return result["after"]


def step_wsj():
    section("2. wsj LIVE job over the recorded listing page")
    page = WSJ_PAGE.read_bytes()
    node = BeautifulSoup(page.decode("utf-8"), "html.parser").select_one("script#__NEXT_DATA__")
    items = json.loads(node.string)["props"]["pageProps"]["searchResults"]
    stamps = [dt.date.fromisoformat(str(i["timestamp"])[:10]) for i in items if i.get("timestamp")]
    print("recorded page: %s, hits=%d, dated by timestamp=%d, dates %s .. %s"
          % (WSJ_PAGE.name, len(items), len(stamps), min(stamps), max(stamps)))
    base = "https://www.wsj.com"
    routes = {base + "/client?legacy=false": b'{"isLoggedIn": true, "type": "subscriber"}', base + "/search": page}
    urls = DowJones._parse_urls("wsj", base, page.decode("utf-8"))
    for index, url in enumerate(urls):
        routes[url] = _next_data_html({"props": {"pageProps": {"isServerUnlockedContent": True, "articleData": {
            "id": "wsj-replay-%d" % index, "headline": "WSJ Replay %d" % index, "publishedDateTimeUtc": _PUBLISHED,
            "flattenedBody": _typed("WSJ replay %d" % index)}}}})
    fixtures = {"wsj": {"routes": routes, "article_urls": set(urls), "module": None}}
    inners = {}
    with tempfile.TemporaryDirectory() as scratch:
        worker = worker_module.Worker(scratch, dict(BASE_CONFIG), make_factory(fixtures, inners), _Sessions())
        try:
            (job,) = worker.run([SECURITY], ["wsj"], max_jobs=1)
        finally:
            worker.close()
    print("job status: %s, accepted: %d, /search GETs: %d"
          % (job["status"], len(job["accepted"]), sum(i.calls.count(base + "/search") for i in inners["wsj"])))
    print("wsj reached_span:", json.dumps(job["reached_span"]))
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    assert job["reached_span"] == {"start": min(stamps).isoformat(), "end": today, "basis": "listing_dates"}, \
        job["reached_span"]
    print("OK: start = the page's oldest hit date, end = the fetch date, basis = listing_dates (not stop_bound)")


def _bbg_fixture():
    routes, ids = {}, []
    for number, path in BBG_PAGES.items():
        body = path.read_bytes()
        routes["https://www.bloomberg.com/nemo-next/api/search/query?page=%d" % number] = body
        ids += [i["resourceId"] for i in json.loads(body.decode("utf-8"))["results"] if i.get("subtype") == "Article"]
    routes["https://www.bloomberg.com/nemo-next/api/search/query?page=3"] = \
        json.dumps({"pagination": False, "results": []}).encode("utf-8")
    for identity in ids:
        routes[STORY % identity] = json.dumps({"story": {
            "headline": "Replay %s" % identity, "id": identity, "publishedAt": _PUBLISHED,
            "url": "https://www.bloomberg.com/news/articles/replay-%s" % identity,
            "body": {"content": _typed("BBG replay %s" % identity)}}}).encode("utf-8")
    return {"routes": routes, "article_urls": {STORY % i for i in ids}, "module": _BBGModule()}, ids


def _bbg_job(row, day):
    fixtures, inners = {"bbg": _bbg_fixture()[0]}, {}
    with tempfile.TemporaryDirectory() as scratch:
        config = dict(BASE_CONFIG, articles_per_security=50, candidate_limit=50)
        worker = worker_module.Worker(scratch, config, _factory(fixtures, inners), _Sessions(), harvest_client=_StubS3())
        worker._utc_today = lambda: day
        try:
            worker.db.execute("INSERT OR REPLACE INTO rejected_hold VALUES(?,?,?,?,?)",
                              tuple(row[c] for c in ab1_seed_hold.COLUMNS))
            worker.db.commit()
            worker.run([SECURITY], ["bbg"], max_jobs=1)
            records = [json.loads(p.read_text(encoding="utf-8")) for p in (Path(scratch) / "run_records").glob("*.json")]
        finally:
            worker.close()
    gets = sum(i.calls.count(STORY % ab1_seed_hold.SEED_KEY.split(":", 1)[1]) for i in inners["bbg"])
    return records[-1], gets


def step_bbg(row):
    section("3. bbg harvest-mode job over the recorded listing pages (p1 + p2), seeded hold in place")
    fixture, ids = _bbg_fixture()
    key_id = ab1_seed_hold.SEED_KEY.split(":", 1)[1]
    print("recorded pages: %s; Article ids=%d; %s is on page 2: %s"
          % (", ".join(p.name for p in BBG_PAGES.values()), len(ids), key_id, key_id in ids))
    day = dt.date.fromisoformat(row["last_failed_day"])
    record, gets = _bbg_job(row, day)
    held = [h for h in record["keys_held"] if h["key"] == ab1_seed_hold.SEED_KEY]
    print("on the hold's day %s: story GETs for %s = %d; keys_held = %s"
          % (day, key_id, gets, json.dumps(held)))
    assert gets == 0 and held and held[0]["state"] == "held" and held[0]["fetched_this_run"] is False
    print("%s is HELD (not fetched)" % ab1_seed_hold.SEED_KEY)
    record2, gets2 = _bbg_job(row, day + dt.timedelta(days=1))
    print("next UTC day %s: story GETs for %s = %d (the hold's designed retry); keys_held = %s"
          % (day + dt.timedelta(days=1), key_id, gets2,
             json.dumps([h for h in record2["keys_held"] if h["key"] == ab1_seed_hold.SEED_KEY])))
    assert gets2 == 1


def main():
    print("today (UTC):", dt.datetime.now(dt.timezone.utc).date().isoformat())
    row = step_seed()
    step_wsj()
    step_bbg(row)
    # the runtime db carries exactly the one seeded row
    db = sqlite3.connect("file:%s?mode=ro" % (RUNTIME / "progress.sqlite3").as_posix(), uri=True)
    try:
        print("\nruntime rejected_hold rows now:", db.execute("SELECT count(*) FROM rejected_hold").fetchone()[0])
    finally:
        db.close()
    print("NETWORK CALLS MADE: %d" % len(NETWORK_CALLS))


if __name__ == "__main__":
    main()
