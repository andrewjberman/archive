"""RIV-w-1 AC1 -- the three /rivalfunds routes behave, on the module's own handlers.

The live neighbour (a published page) does not exist until RIV-d-2, so S3 and the viewer are stubbed HERE and only
here (AC2 is the live seam). Stubs replace the module-level _s3() and _viewer() exactly as /sprint's are shaped."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


class _Body(io.BytesIO):
    def read(self, amt=None):  # noqa: D401
        return super().read() if amt is None else super().read(amt)


class StubS3:
    def __init__(self, prefix):
        self.prefix = prefix
        self.days = ["2026-09-28", "2026-09-29"]

    def get_paginator(self, _):
        stub = self

        class P:
            def paginate(self, **kw):
                yield {"CommonPrefixes": [{"Prefix": f"{stub.prefix}date={d}/"} for d in stub.days]}

        return P()

    def list_objects_v2(self, **kw):
        return {"CommonPrefixes": [{"Prefix": f"{self.prefix}date={d}/"} for d in self.days], "IsTruncated": False}

    def get_object(self, Bucket, Key, **kw):
        for d in self.days:
            if f"date={d}/" in Key and Key.endswith("index.html"):
                return {"Body": _Body(f"<html><body>PAGE {d}</body></html>".encode()), "ContentLength": 40}
        raise Exception("NoSuchKey")

    def head_object(self, Bucket, Key, **kw):
        self.get_object(Bucket, Key)
        return {"ContentLength": 40}


def run(v):
    root = c.setup_path()
    gw = root / "infra" / "aws" / "ec2" / "opal-gateway"
    sys.path.insert(0, str(gw))
    from starlette.applications import Starlette
    from starlette.routing import Route
    from starlette.testclient import TestClient

    from app import rivalfunds_view as rv

    page_uri = c.address("rivalfunds", "etfs", "platinum", "page", "date=X")
    key_prefix = page_uri.split("/", 3)[3].rsplit("date=X", 1)[0]
    stub = StubS3(key_prefix)
    rv._s3 = lambda: stub
    if hasattr(rv, "_s3_client"):
        rv._s3_client = stub
    viewer = {"email": "someone@opalinvest.com"}
    rv._viewer = lambda request: viewer["email"]
    if hasattr(rv, "audit"):
        rv.audit.log_call = lambda *a, **k: None
    if hasattr(rv, "_cache_clear"):
        rv._cache_clear()
    app = Starlette(routes=[Route("/rivalfunds", rv.rivalfunds_page), Route("/rivalfunds/archive", rv.rivalfunds_archive),
                            Route("/rivalfunds/{day}", rv.rivalfunds_day)])
    cl = TestClient(app, follow_redirects=False)
    a = cl.get("/rivalfunds/archive")
    v.check(a.status_code == 200 and "2026-09-28" in a.text and "2026-09-29" in a.text, f"/rivalfunds/archive lists both days ({a.status_code})")
    p = cl.get("/rivalfunds")
    v.check((p.status_code == 200 and "PAGE 2026-09-29" in p.text) or (p.status_code in (302, 307) and "2026-09-29" in p.headers.get("location", "")),
            f"/rivalfunds serves (or redirects to) the newest day ({p.status_code})")
    d = cl.get("/rivalfunds/2026-09-28")
    v.check(d.status_code == 200 and "PAGE 2026-09-28" in d.text, f"/rivalfunds/2026-09-28 serves that day ({d.status_code})")
    bad = cl.get("/rivalfunds/2026-13-99x")
    v.check(bad.status_code in (400, 404), f"a malformed day is refused ({bad.status_code})")
    miss = cl.get("/rivalfunds/2020-01-02")
    v.check(miss.status_code == 404, f"an unpublished day is 404 ({miss.status_code})")
    v.check(rv.is_rivalfunds_path("/rivalfunds") and rv.is_rivalfunds_path("/rivalfunds/archive") and not rv.is_rivalfunds_path("/rivalfundsx"),
            "is_rivalfunds_path matches /rivalfunds and /rivalfunds/... only")
    viewer["email"] = ""
    u = cl.get("/rivalfunds/archive")
    v.check(u.status_code in (401, 403), f"no signed-in identity -> refused ({u.status_code})")
    src = (gw / "app" / "rivalfunds_view.py").read_text(encoding="utf-8")
    v.check("opal-data-etfs" not in src and "rivalfunds/etfs/platinum" not in src, "bucket and prefix are not typed in the module (builder output)")


failures = c.guarded("AC1", run)
if failures == 0:
    print("AC1 RESULT: PASS 0 failures")
else:
    print(f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
