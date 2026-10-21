#!/usr/bin/env bash
# OPLGTW OG-cs-2 AC1 (cli-shim workstream, wave 2): app/folder_tools.py, ADMISSION and LIST, against a fake in-memory S3 client. One fresh process, no AWS, no network.
#   list_folder(principal, rec, is_master_admin, is_opal, s3, path, start_after="") -> dict ; path is "bucket/prefix".
#  (a) REFUSALS make ZERO S3 calls and answer {"error": <words naming the folder>, "code": "folder_refused", "guard_denied": True, "folder": "<bucket>/<prefix>"}: an unserved bucket (opal-data-harvest), a bronze path, a raw path, a folder an Opal non-admin has no grant for, a non-Opal caller;
#  (b) a master_admin lists "opal-data-assets/schwab/08335338/": prefixes hold "silver/" and NOT "bronze/"; listing ".../silver/" holds the two table prefixes; the list page carries objects with key, size and last_modified, and `truncated` and `next_start_after` when the fake says more remain (the fake pages at 2 keys);
#  (c) a person granted "opal-data-assets/schwab/08335338/" lists inside it and is REFUSED for the sibling master "opal-data-assets/schwab/08242234/" (zero S3 calls); deny wins (a deny on a sub-folder refuses it).
. "$(dirname "$0")/../../r47/checks/_gwtests.sh"
res=$(python3 -I - "$(native "$GW")" <<'PYEOF'
import datetime, io, os, sys
G = sys.argv[1]
sys.path.insert(0, G)
os.environ["MOCK_GRAPH"] = "1"
import warnings
warnings.simplefilter("ignore")
ok = True


def say(label, cond):
    global ok
    ok = ok and bool(cond)
    print("%s: %s" % (label, "ok" if cond else "NOT OK"))


try:
    from app import data_entitlement as de, folder_tools as ft
except Exception as exc:  # noqa: BLE001
    print("import failed: %s: %s" % (type(exc).__name__, str(exc)[:80]))
    print("NO")
    sys.exit(0)

KEYS = {
    "opal-data-assets": {
        "schwab/08335338/silver/fact_trn/date=2026-10-20/a.parquet": 100,
        "schwab/08335338/silver/dim_position/date=2026-10-20/b.parquet": 200,
        "schwab/08335338/bronze/raw1.csv": 50,
        "schwab/08242234/silver/dim_balance/date=2026-10-20/c.parquet": 300,
    },
    "opal-data-harvest": {"amgt/x.json": 1},
}


class FakeS3:
    def __init__(self, page=2):
        self.calls = 0
        self.page = page

    def list_objects_v2(self, Bucket, Prefix="", Delimiter="", MaxKeys=1000, StartAfter="", **kw):  # noqa: N803
        self.calls += 1
        keys = sorted(k for k in KEYS.get(Bucket, {}) if k.startswith(Prefix))
        contents, prefixes = [], []
        for k in keys:
            rest = k[len(Prefix):]
            if Delimiter and Delimiter in rest:
                p = Prefix + rest.split(Delimiter)[0] + Delimiter
                if p not in prefixes:
                    prefixes.append(p)
            else:
                contents.append(k)
        items = [("c", k) for k in contents] + [("p", p) for p in prefixes]
        items = [x for x in items if x[1] > StartAfter] if StartAfter else items
        more = len(items) > min(MaxKeys, self.page)
        items = items[:min(MaxKeys, self.page)]
        return {"Contents": [{"Key": k, "Size": KEYS[Bucket][k], "LastModified": datetime.datetime(2026, 10, 20, tzinfo=datetime.timezone.utc)} for t, k in items if t == "c"],
                "CommonPrefixes": [{"Prefix": k} for t, k in items if t == "p"], "IsTruncated": more}

    def head_object(self, **kw):
        self.calls += 1
        raise AssertionError("not for list")

    def get_object(self, **kw):
        self.calls += 1
        raise AssertionError("not for list")

    def download_file(self, *a, **kw):
        self.calls += 1
        raise AssertionError("not for list")


def rec(allow=(), deny=()):
    return de.PersonAccess("active", 3, False, frozenset(), frozenset(), frozenset(allow), frozenset(deny))


def lst(s3, path, admin=False, opal=True, r=None, after=""):
    try:
        return ft.list_folder("tid/oid", r, admin, opal, s3, path, after)
    except Exception as exc:  # noqa: BLE001
        return {"_exc": "%s: %s" % (type(exc).__name__, str(exc)[:60])}


def refused(out, folder_has):
    return out.get("code") == "folder_refused" and out.get("guard_denied") is True and isinstance(out.get("error"), str) and folder_has in out.get("error", "") + out.get("folder", "")


s3 = FakeS3()
cases = [("an unserved bucket", lst(s3, "opal-data-harvest/amgt/", admin=True), "opal-data-harvest"),
         ("a bronze path", lst(s3, "opal-data-assets/schwab/08335338/bronze/", admin=True), "bronze"),
         ("a raw path", lst(s3, "opal-data-assets/raw/x/", admin=True), "raw"),
         ("an Opal non-admin with no grant", lst(s3, "opal-data-assets/schwab/08335338/", r=rec()), "opal-data-assets"),
         ("a non-Opal caller", lst(s3, "opal-data-assets/schwab/08335338/", opal=False, r=rec(allow=["opal-data-assets"])), "opal-data-assets")]
say("refusals answer folder_refused naming the folder, guard_denied true (%s)" % ", ".join("%s: %s" % (n, "ok" if refused(o, h) else o) for n, o, h in cases), all(refused(o, h) for _, o, h in cases))
say("refusals made ZERO S3 calls (%d)" % s3.calls, s3.calls == 0)
s3 = FakeS3(page=50)
top = lst(s3, "opal-data-assets/schwab/08335338/", admin=True)
tables = lst(s3, "opal-data-assets/schwab/08335338/silver/", admin=True)
tp = sorted(top.get("prefixes", []))
tt = sorted(tables.get("prefixes", []))
say("master admin lists the master folder: silver/ shown, bronze/ NOT shown (%s)" % tp, any(p.rstrip("/").endswith("silver") for p in tp) and not any("bronze" in p for p in tp))
say("the silver folder lists its two table prefixes (%s)" % tt, len(tt) == 2 and any("fact_trn" in p for p in tt) and any("dim_position" in p for p in tt))
s3 = FakeS3(page=2)
pg = lst(s3, "opal-data-assets/schwab/08335338/silver/fact_trn/date=2026-10-20/", admin=True)
objs = pg.get("objects", [])
say("a page carries objects with key, size and last_modified (%s)" % [sorted(o) for o in objs[:1]], bool(objs) and all({"key", "size", "last_modified"} <= set(o) for o in objs))
s3 = FakeS3(page=1)
big = lst(s3, "opal-data-assets/schwab/08335338/silver/", admin=True)
say("truncated and next_start_after are carried when the fake says more remain", big.get("truncated") is True and isinstance(big.get("next_start_after"), str) and big["next_start_after"])
s3 = FakeS3(page=50)
g = rec(allow=["opal-data-assets/schwab/08335338/"])
inside = lst(s3, "opal-data-assets/schwab/08335338/silver/", r=g)
calls_before = s3.calls
sib = lst(s3, "opal-data-assets/schwab/08242234/", r=g)
say("a granted person lists inside the granted folder and is refused for the sibling master with no S3 call", bool(inside.get("prefixes")) and refused(sib, "08242234") and s3.calls == calls_before)
d = rec(allow=["opal-data-assets"], deny=["opal-data-assets/schwab/08335338/silver/"])
ref = lst(s3, "opal-data-assets/schwab/08335338/silver/", r=d)
say("deny wins: a denied sub-folder is refused for a whole-bucket grant", refused(ref, "silver"))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
