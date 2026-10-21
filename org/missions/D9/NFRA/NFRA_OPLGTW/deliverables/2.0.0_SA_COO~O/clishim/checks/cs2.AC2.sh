#!/usr/bin/env bash
# OPLGTW OG-cs-2 AC2 (cli-shim workstream, wave 2): app/folder_tools.py DESCRIBE, against a fake in-memory S3 client holding real parquet bytes. One fresh process, no AWS, no network.
#   describe_object(principal, rec, is_master_admin, is_opal, s3, path) -> dict ; path is "bucket/key" of ONE parquet object.
#  (a) a refusal (bronze path, unserved bucket, an Opal non-admin with no grant) makes ZERO S3 calls and answers the same refusal dict as list_folder: code folder_refused, guard_denied true, an error string naming the folder;
#  (b) an allowed describe answers {"path", "size", "columns": [{"name","type"}...] in file order, "dropped_columns": [names], "num_rows", "row_groups"}; the five sensitive column classes are NOT in "columns" and ARE named in "dropped_columns" (a tax id, an email and a date of birth column are dropped, a tax_lot_id and an account_id column are kept);
#  (c) the object is read through RANGED GETs of its footer only: the bytes the fake served are under a quarter of the file (a 350 KB file);
#  (d) an object that is not parquet answers {"error", "code": "not_parquet"}; an absent object answers {"error", "code": "not_found"}; neither raises.
. "$(dirname "$0")/../../r47/checks/_gwtests.sh"
res=$(python3 -I - "$(native "$GW")" <<'PYEOF'
import io, os, sys
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
    import pyarrow as pa, pyarrow.parquet as pq
    from app import data_entitlement as de, folder_tools as ft
except Exception as exc:  # noqa: BLE001
    print("import failed: %s: %s" % (type(exc).__name__, str(exc)[:80]))
    print("NO")
    sys.exit(0)

N = 60000
tbl = pa.table({"account_id": [i % 50 for i in range(N)], "tax_lot_id": list(range(N)), "tax_id": ["x%d" % i for i in range(N)],
                "email": ["u%d@example.invalid" % i for i in range(N)], "date_of_birth": ["1970-01-01"] * N,
                "quantity": [float(i) for i in range(N)]})
buf = io.BytesIO()
pq.write_table(tbl, buf, row_group_size=10000)
DATA = buf.getvalue()
OBJ = {("opal-data-assets", "schwab/08335338/silver/fact_trn/date=2026-10-20/a.parquet"): DATA,
       ("opal-data-assets", "schwab/08335338/silver/fact_trn/date=2026-10-20/junk.parquet"): b"this is not parquet at all, just text " * 40}


class FakeS3:
    def __init__(self):
        self.calls = 0
        self.served = 0

    def head_object(self, Bucket, Key, **kw):  # noqa: N803
        self.calls += 1
        if (Bucket, Key) not in OBJ:
            raise KeyError("NoSuchKey")
        return {"ContentLength": len(OBJ[(Bucket, Key)])}

    def get_object(self, Bucket, Key, Range=None, **kw):  # noqa: N803
        self.calls += 1
        if (Bucket, Key) not in OBJ:
            raise KeyError("NoSuchKey")
        data = OBJ[(Bucket, Key)]
        if Range:
            a, b = Range.split("=")[1].split("-")
            data = data[int(a):int(b) + 1]
        self.served += len(data)
        return {"Body": io.BytesIO(data), "ContentLength": len(data)}

    def list_objects_v2(self, **kw):
        self.calls += 1
        raise AssertionError("not for describe")

    def download_file(self, *a, **kw):
        self.calls += 1
        raise AssertionError("describe must not download the object")


def rec(allow=(), deny=()):
    return de.PersonAccess("active", 3, False, frozenset(), frozenset(), frozenset(allow), frozenset(deny))


def desc(s3, path, admin=False, opal=True, r=None):
    try:
        return ft.describe_object("tid/oid", r, admin, opal, s3, path)
    except Exception as exc:  # noqa: BLE001
        return {"_exc": "%s: %s" % (type(exc).__name__, str(exc)[:60])}


GOOD = "opal-data-assets/schwab/08335338/silver/fact_trn/date=2026-10-20/a.parquet"
s3 = FakeS3()
cases = [desc(s3, "opal-data-assets/schwab/08335338/bronze/a.parquet", admin=True),
         desc(s3, "opal-data-harvest/amgt/a.parquet", admin=True),
         desc(s3, GOOD, r=rec())]
say("refusals answer folder_refused, guard_denied true, an error naming the folder", all(c.get("code") == "folder_refused" and c.get("guard_denied") is True and isinstance(c.get("error"), str) and c["error"] for c in cases))
say("refusals made ZERO S3 calls (%d)" % s3.calls, s3.calls == 0)
s3 = FakeS3()
out = desc(s3, GOOD, admin=True)
names = [c.get("name") for c in out.get("columns", [])]
say("columns in file order, sensitive classes dropped and named (%s | dropped %s)" % (names, out.get("dropped_columns")), names == ["account_id", "tax_lot_id", "quantity"] and sorted(out.get("dropped_columns", [])) == ["date_of_birth", "email", "tax_id"])
say("every column carries a type string, size %s, num_rows %s, row_groups %s" % (out.get("size"), out.get("num_rows"), out.get("row_groups")), all(isinstance(c.get("type"), str) and c["type"] for c in out.get("columns", [])) and out.get("size") == len(DATA) and out.get("num_rows") == N and out.get("row_groups") == 6)
say("only the footer was read through ranged GETs: %d bytes of %d" % (s3.served, len(DATA)), 0 < s3.served < len(DATA) // 4)
g = desc(FakeS3(), GOOD, r=rec(allow=["opal-data-assets/schwab/08335338/"]))
say("a person granted the master folder describes the object", [c.get("name") for c in g.get("columns", [])] == ["account_id", "tax_lot_id", "quantity"])
bad = desc(FakeS3(), "opal-data-assets/schwab/08335338/silver/fact_trn/date=2026-10-20/junk.parquet", admin=True)
miss = desc(FakeS3(), "opal-data-assets/schwab/08335338/silver/fact_trn/date=2026-10-20/none.parquet", admin=True)
say("junk answers not_parquet and an absent object answers not_found, neither raises (%s | %s)" % (bad.get("code") or bad, miss.get("code") or miss), bad.get("code") == "not_parquet" and bool(bad.get("error")) and miss.get("code") == "not_found" and bool(miss.get("error")))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
