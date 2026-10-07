"""RIV-rt-1 AC1 (FWD-22; F.5 item 2; ROUND15_CELLS_DRAFT.md revision 1.5): the gateway serves a fund's chart object at
GET /rivalfunds/YYYY-MM-DD/chart/<FUND>, JSON, behind the same identity wall, from the same page prefix.

Measured today (CLOUD 90e794e816): `app/rivalfunds_view.py` serves `/rivalfunds/<day>` and `/rivalfunds/<day>/audit` only; it has
no `chart_key` and no `rivalfunds_chart`.

Interface (prescribed, verbatim from the cell): `rivalfunds_view.chart_key(day, fund)` (the page prefix +
`date=<day>/charts/<FUND>.json`; `fund` must match `^[A-Z0-9]{1,8}$`) and handler `rivalfunds_chart` for
`/rivalfunds/{day}/chart/{fund}`: 200 `application/json` with the object's bytes; bad day or bad fund -> 400; no object -> 404
JSON `{"error": "no chart for this fund and day"}`; over the cap -> 413-class refusal as the page's; every call audit-logged with
`{"day", "fund", "route": "chart"}`. The route is declared in `ROUTE_CLASS` as `access-layer` and mounted in `server.py` BY THE
ISSUER at the merge (a hookup, not this cell's file).
Offline: S3, the viewer and the audit log stubbed (the audit stub RECORDS); a Starlette app built here mounts
`/rivalfunds/{day}/chart/{fund}` -> `rivalfunds_chart` (when it exists) and `/rivalfunds/{day}/audit` -> `rivalfunds_audit`.
Fixture: the stub holds `<prefix>date=2026-10-06/charts/TXUE.json` (exact bytes below) and `<prefix>date=2026-10-06/audit.html`;
no chart object for IDVZ.
  - (a) `chart_key("2026-10-06", "TXUE")` == `<page prefix>date=2026-10-06/charts/TXUE.json`;
  - (b) GET /rivalfunds/2026-10-06/chart/TXUE -> 200, media type `application/json`, body == the stored bytes exactly, read from
    that key;
  - (c) refusals, none of them reading S3: no viewer -> 401; bad day (2026-13-40) -> 400; bad fund -> 400 for lowercase (`txue`),
    too long (`TOOLONGFND`, 10 characters) and, with the handler called directly (a slash never reaches a `{fund}` path
    parameter through the router), `TX/UE`;
  - (d) GET /rivalfunds/2026-10-06/chart/IDVZ (no object) -> 404 and the JSON body == {"error": "no chart for this fund and day"};
  - (e) the 200 call and the 404 call are each audit-logged with day, fund and route "chart";
  - (f) control: GET /rivalfunds/2026-10-06/audit still returns 200 with the stored audit.html and is audit-logged route "audit".
Not graded here: the over-cap refusal (the cell's "413-class ... as the page's" does not match the page's 502; see the issuer's
INTERFACE QUESTIONS) and the `ROUTE_CLASS` / `server.py` hookup (the issuer's).
FAIL at base: (a), (b), (c), (d), (e) FAIL (no chart_key, no handler); (f) PASSES."""
import asyncio
import io
import pathlib
import sys
import types

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

GW = c.ROOT / "infra" / "aws" / "ec2" / "opal-gateway"
DAY = "2026-10-06"
CHART = (b'{"fund": "TXUE", "asof": "2026-10-05", "generated_at": "2026-10-06T13:00:00Z", "ranges": {"R30": "2026-09-05", '
         b'"R90": "2026-07-07", "R365": "2025-10-05"}, "securities": {"AAPL_US_Equity": {"name": "Apple Inc", "source_words": '
         b'"market close", "points": [["2026-10-05", 255.5, "m"]], "gaps": [], "markers": []}}}\n')


class StubS3:
    def __init__(self, prefix):
        self.prefix, self.keys = prefix, []
        self.objs = {f"{prefix}date={DAY}/charts/TXUE.json": CHART,
                     f"{prefix}date={DAY}/audit.html": b"<html>AUDIT 2026-10-06</html>",
                     f"{prefix}date={DAY}/index.html": b"<html>PAGE 2026-10-06</html>"}

    def get_object(self, Bucket, Key, **kw):
        self.keys.append(Key)
        if Key in self.objs:
            return {"Body": io.BytesIO(self.objs[Key])}
        raise Exception("NoSuchKey")

    def list_objects_v2(self, **kw):
        return {"CommonPrefixes": [{"Prefix": f"{self.prefix}date={DAY}/"}], "IsTruncated": False}


def _logged(calls, **want):
    """The audit-log calls whose args dict (the third positional) carries every wanted item."""
    out = []
    for a, _k in calls:
        d = next((x for x in a if isinstance(x, dict)), {})
        if all(d.get(k) == v for k, v in want.items()):
            out.append(d)
    return out


def run(v):
    c.setup_path()
    c.offline_guards()
    for p in (str(GW), str(c.ROOT)):
        if p not in sys.path:
            sys.path.insert(0, p)
    from starlette.applications import Starlette
    from starlette.routing import Route
    from starlette.testclient import TestClient

    from app import gen_rivalfunds_location as gen
    from app import rivalfunds_view as rv

    _, prefix = gen.page_location()
    stub = StubS3(prefix)
    viewer = {"email": "someone@opalinvest.com"}
    logged = []
    rv._s3 = lambda: stub
    rv._viewer = lambda request: viewer["email"]
    rv.audit.log_call = lambda *a, **k: logged.append((a, k))
    rv._cache_clear()
    handler = getattr(rv, "rivalfunds_chart", None)
    key_fn = getattr(rv, "chart_key", None)
    routes = [Route("/rivalfunds/{day}/audit", rv.rivalfunds_audit)]
    if handler is not None:
        routes.insert(0, Route("/rivalfunds/{day}/chart/{fund}", handler))
    cl = TestClient(Starlette(routes=routes))
    want_key = f"{prefix}date={DAY}/charts/TXUE.json"

    try:
        got_key = key_fn(DAY, "TXUE") if key_fn is not None else None
    except Exception as e:  # noqa: BLE001 -- a raising chart_key is a failed arm, not a dead check
        got_key = f"RAISED {type(e).__name__}: {e}"
    print("chart_key:", got_key, "| page prefix:", prefix)
    v.check(got_key == want_key and str(got_key).endswith(f"date={DAY}/charts/TXUE.json"),
            "(a) chart_key(day, fund) is the page prefix + date=<day>/charts/<FUND>.json")

    r = cl.get(f"/rivalfunds/{DAY}/chart/TXUE")
    ctype = (r.headers.get("content-type") or "").split(";")[0].strip()
    read_key = want_key in stub.keys
    print("chart:", r.status_code, "| content-type:", ctype, "| bytes equal:", r.content == CHART, "| read chart key:", read_key)
    v.check(handler is not None and r.status_code == 200 and ctype == "application/json" and r.content == CHART and read_key,
            "(b) GET /rivalfunds/2026-10-06/chart/TXUE serves the stored object's exact bytes as application/json")

    n_keys = len(stub.keys)
    viewer["email"] = ""
    r401 = cl.get(f"/rivalfunds/{DAY}/chart/TXUE")
    viewer["email"] = "someone@opalinvest.com"
    r_day = cl.get("/rivalfunds/2026-13-40/chart/TXUE")
    r_low = cl.get(f"/rivalfunds/{DAY}/chart/txue")
    r_long = cl.get(f"/rivalfunds/{DAY}/chart/TOOLONGFND")
    slash = None
    if handler is not None:
        try:
            req = types.SimpleNamespace(path_params={"day": DAY, "fund": "TX/UE"}, headers={}, query_params={},
                                        url=types.SimpleNamespace(path=f"/rivalfunds/{DAY}/chart/TX/UE", query=""))
            slash = asyncio.run(handler(req)).status_code
        except Exception as e:  # noqa: BLE001
            slash = f"RAISED {type(e).__name__}: {e}"
    codes = (r401.status_code, r_day.status_code, r_low.status_code, r_long.status_code, slash)
    print("refusals (no viewer, bad day, lowercase, too long, slash):", codes, "| S3 reads during refusals:",
          len(stub.keys) - n_keys)
    v.check(handler is not None and codes == (401, 400, 400, 400, 400) and len(stub.keys) == n_keys,
            "(c) no viewer 401; bad day 400; bad fund (lowercase, too long, slash) 400; no S3 read on any refusal")

    r404 = cl.get(f"/rivalfunds/{DAY}/chart/IDVZ")
    try:
        body404 = r404.json()
    except Exception:  # noqa: BLE001
        body404 = r404.content[:80]
    print("missing object:", r404.status_code, body404)
    v.check(handler is not None and r404.status_code == 404 and body404 == {"error": "no chart for this fund and day"},
            '(d) no chart object -> 404 JSON {"error": "no chart for this fund and day"}')

    ok_log = _logged(logged, day=DAY, fund="TXUE", route="chart")
    miss_log = _logged(logged, day=DAY, fund="IDVZ", route="chart")
    print("audit log entries route=chart: TXUE", ok_log, "| IDVZ", miss_log)
    v.check(bool(ok_log) and bool(miss_log), "(e) the 200 call and the 404 call are audit-logged with day, fund and route 'chart'")

    ra = cl.get(f"/rivalfunds/{DAY}/audit")
    a_log = _logged(logged, day=DAY, route="audit")
    print("audit page:", ra.status_code, ra.content[:40], "| audit log entries route=audit:", len(a_log))
    v.check(ra.status_code == 200 and ra.content == stub.objs[f"{prefix}date={DAY}/audit.html"] and bool(a_log),
            "(f) control: /rivalfunds/2026-10-06/audit still serves audit.html and is audit-logged route 'audit'")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
