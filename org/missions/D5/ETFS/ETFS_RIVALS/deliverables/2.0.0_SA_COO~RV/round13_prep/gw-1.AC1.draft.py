"""RIV-gw-1 AC1 (row Z-S47; ROUND_ANALYSIS.round10.md ADDENDUM 3 item 2): the gateway serves the day's audit page at
GET /rivalfunds/YYYY-MM-DD/audit behind the same identity wall, from the same page prefix (no new grant: the read policy already
covers `<key_prefix>*`).

Interface (prescribed): `app/rivalfunds_view.py` gains `audit_key(day)` = `<key_prefix>date=<day>/audit.html` (the generated
location, never typed) and the handler `rivalfunds_audit(request)`: no viewer -> 401; a bad date -> 400; a missing object -> 404
naming the day's audit page; otherwise the object's bytes with the view's `_HEADERS`, read under the same 2 MB cap and TTL cache
as the page. server.py's Route line is the issuer's hookup at the merge, not the cell's.
Offline: S3 and the viewer stubbed; a Starlette app built here mounts `/rivalfunds/{day}/audit` -> `rivalfunds_audit` and
`/rivalfunds/{day}` -> `rivalfunds_day`.
  - (a) GET /rivalfunds/2026-10-06/audit -> 200, body == the stored audit.html bytes, read from key `...date=2026-10-06/audit.html`,
    Cache-Control "private, no-store";
  - (b) refusals: no viewer -> 401; /rivalfunds/2026-13-40/audit -> 400; /rivalfunds/2026-10-05/audit (no audit object) -> 404;
  - (c) control: GET /rivalfunds/2026-10-06 still serves index.html.
FAIL at base: (a) and (b) FAIL (no handler); (c) PASSES."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

GW = c.ROOT / "infra" / "aws" / "ec2" / "opal-gateway"


class StubS3:
    def __init__(self, prefix):
        self.prefix, self.keys = prefix, []
        self.objs = {f"{prefix}date=2026-10-06/index.html": b"<html>PAGE 2026-10-06</html>",
                     f"{prefix}date=2026-10-06/audit.html": b"<html>AUDIT 2026-10-06</html>",
                     f"{prefix}date=2026-10-05/index.html": b"<html>PAGE 2026-10-05</html>"}

    def get_object(self, Bucket, Key, **kw):
        self.keys.append(Key)
        if Key in self.objs:
            return {"Body": io.BytesIO(self.objs[Key])}
        raise Exception("NoSuchKey")

    def list_objects_v2(self, **kw):
        return {"CommonPrefixes": [{"Prefix": f"{self.prefix}date=2026-10-06/"}], "IsTruncated": False}


def run(v):
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
    rv._s3 = lambda: stub
    rv._viewer = lambda request: viewer["email"]
    rv.audit.log_call = lambda *a, **k: None
    rv._cache_clear()
    handler = getattr(rv, "rivalfunds_audit", None)
    routes = [Route("/rivalfunds/{day}", rv.rivalfunds_day)]
    if handler is not None:
        routes.insert(0, Route("/rivalfunds/{day}/audit", handler))
    cl = TestClient(Starlette(routes=routes))

    r = cl.get("/rivalfunds/2026-10-06/audit")
    key_ok = any(k.endswith("date=2026-10-06/audit.html") for k in stub.keys)
    print("audit:", r.status_code, r.content[:40], "| read audit key:", key_ok, "| cache-control:", r.headers.get("cache-control"))
    v.check(handler is not None and r.status_code == 200 and r.content == stub.objs[f"{prefix}date=2026-10-06/audit.html"]
            and key_ok and r.headers.get("cache-control") == "private, no-store",
            "(a) GET /rivalfunds/2026-10-06/audit serves the stored audit.html under the view's headers")

    viewer["email"] = ""
    r401 = cl.get("/rivalfunds/2026-10-06/audit")
    viewer["email"] = "someone@opalinvest.com"
    r400 = cl.get("/rivalfunds/2026-13-40/audit")
    r404 = cl.get("/rivalfunds/2026-10-05/audit")
    print("refusals:", r401.status_code, r400.status_code, r404.status_code)
    v.check(handler is not None and (r401.status_code, r400.status_code, r404.status_code) == (401, 400, 404),
            "(b) no viewer 401, bad date 400, no audit object 404")

    rp = cl.get("/rivalfunds/2026-10-06")
    print("page:", rp.status_code, rp.content[:40])
    v.check(rp.status_code == 200 and rp.content == stub.objs[f"{prefix}date=2026-10-06/index.html"],
            "(c) control: /rivalfunds/2026-10-06 still serves index.html")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
