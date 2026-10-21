#!/usr/bin/env bash
# OPLGTW OG-cs-2 AC3 (cli-shim workstream, wave 2): app/folder_tools.py QUERY, against the REAL bounded engine (app.integrations.schwab.engine.ExecutionEngine) and a fake in-memory S3 client holding real parquet bytes. One fresh process, no AWS, no network.
#   async query_object(principal, rec, is_master_admin, is_opal, s3, engine, codec, path, request, cursor="") -> dict ; path is "bucket/prefix" of a table FOLDER (every .parquet object under it, at most 13 listed) or "bucket/key.parquet" of one object;
#   codec is an app.integrations.schwab.cursor.CursorCodec. Answer: {"columns": [...], "rows": [[...]...], "matched_rows": int, "returned_rows": int, "dropped_columns": [...], "next_cursor": str only when more rows remain}; a refusal or an engine refusal answers {"error", "code", ...} and never raises.
#  (a) a refused path (bronze) makes ZERO S3 calls; a request naming a sensitive column (email) or an unknown top-level key (sql) answers code INVALID_REQUEST with ZERO downloads; a folder of 13 listed objects answers code LIMIT_EXCEEDED with ZERO downloads;
#  (b) a rows request (columns, an eq filter, order_by) answers the right rows; an aggregate request (group_by + sum) answers one row per group with the right sums;
#  (c) paging: 300 matching rows, the default page is 100 and carries next_cursor; the next page continues with no overlap; a cursor reused with a DIFFERENT request answers INVALID_REQUEST, and so does a tampered cursor.
. "$(dirname "$0")/../../r47/checks/_gwtests.sh"
res=$(python3 -I - "$(native "$GW")" <<'PYEOF'
import asyncio, io, os, sys, tempfile
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
    from app.integrations.schwab import engine as eng, cursor as cur
except Exception as exc:  # noqa: BLE001
    print("import failed: %s: %s" % (type(exc).__name__, str(exc)[:80]))
    print("NO")
    sys.exit(0)

B = "opal-data-assets"
P = "schwab/08335338/silver/fact_trn/date=2026-10-20/"


def mk(lo, hi):
    n = hi - lo
    b = io.BytesIO()
    pq.write_table(pa.table({"account_id": [i % 10 for i in range(lo, hi)], "quantity": [float(i) for i in range(lo, hi)],
                             "email": ["u%d@example.invalid" % i for i in range(lo, hi)]}), b)
    return b.getvalue()


OBJ = {(B, P + "a.parquet"): mk(0, 150), (B, P + "b.parquet"): mk(150, 300)}
for i in range(13):
    OBJ[(B, "schwab/08335338/silver/many/date=2026-10-20/p%02d.parquet" % i)] = b"x" * 10


class FakeS3:
    def __init__(self):
        self.calls = 0
        self.downloads = 0

    def list_objects_v2(self, Bucket, Prefix="", Delimiter="", MaxKeys=1000, StartAfter="", **kw):  # noqa: N803
        self.calls += 1
        keys = sorted(k for (b, k) in OBJ if b == Bucket and k.startswith(Prefix) and k > StartAfter)
        keys = [k for k in keys if not Delimiter or Delimiter not in k[len(Prefix):]]
        return {"Contents": [{"Key": k, "Size": len(OBJ[(Bucket, k)])} for k in keys[:MaxKeys]], "CommonPrefixes": [], "IsTruncated": len(keys) > MaxKeys}

    def head_object(self, Bucket, Key, **kw):  # noqa: N803
        self.calls += 1
        return {"ContentLength": len(OBJ[(Bucket, Key)])}

    def get_object(self, Bucket, Key, Range=None, **kw):  # noqa: N803
        self.calls += 1
        data = OBJ[(Bucket, Key)]
        if Range:
            a, b = Range.split("=")[1].split("-")
            data = data[int(a):int(b) + 1]
        return {"Body": io.BytesIO(data), "ContentLength": len(data)}

    def download_file(self, Bucket, Key, Filename, **kw):  # noqa: N803
        self.calls += 1
        self.downloads += 1
        with open(Filename, "wb") as f:
            f.write(OBJ[(Bucket, Key)])


tmp = tempfile.mkdtemp(prefix="cs2ac3")
engine = eng.ExecutionEngine(temp_root=os.path.join(tmp, "engine-root"), memory_total_bytes=lambda: 1 << 40)
codec = cur.CursorCodec(os.urandom(32))
REC = de.PersonAccess("active", 3, False, frozenset(), frozenset(), frozenset(["opal-data-assets/schwab/08335338/"]), frozenset())


def q(s3, path, request, cursor="", admin=True, r=None):
    try:
        return asyncio.run(ft.query_object("tid/oid", r, admin, True, s3, engine, codec, path, request, cursor))
    except Exception as exc:  # noqa: BLE001
        return {"_exc": "%s: %s" % (type(exc).__name__, str(exc)[:80])}


FOLDER = B + "/" + P
s3 = FakeS3()
ref = q(s3, B + "/schwab/08335338/bronze/", {"columns": ["account_id"]})
say("a refused path answers folder_refused with ZERO S3 calls (%d)" % s3.calls, ref.get("code") == "folder_refused" and s3.calls == 0)
s3 = FakeS3()
sens = q(s3, FOLDER, {"columns": ["email"]})
sqlk = q(s3, FOLDER, {"columns": ["account_id"], "sql": "select 1"})
say("a sensitive column and an unknown top-level key answer INVALID_REQUEST with ZERO downloads (%s | %s | %d)" % (sens.get("code"), sqlk.get("code"), s3.downloads), sens.get("code") == "INVALID_REQUEST" and sqlk.get("code") == "INVALID_REQUEST" and s3.downloads == 0)
s3 = FakeS3()
many = q(s3, B + "/schwab/08335338/silver/many/", {"columns": ["account_id"]})
say("13 listed objects answer LIMIT_EXCEEDED with ZERO downloads (%s | %d)" % (many.get("code"), s3.downloads), many.get("code") == "LIMIT_EXCEEDED" and s3.downloads == 0 and bool(many.get("suggestion") or many.get("reason")))
s3 = FakeS3()
rows = q(s3, FOLDER, {"columns": ["account_id", "quantity"], "filters": [{"field": "account_id", "op": "eq", "value": 3}], "order_by": [{"field": "quantity", "direction": "asc"}], "limit": 5})
want = [[3, float(x)] for x in (3, 13, 23, 33, 43)]
say("a rows request answers the five lowest quantities of account 3 (columns %s, matched %s, returned %s)" % (rows.get("columns"), rows.get("matched_rows"), rows.get("returned_rows")), rows.get("columns") == ["account_id", "quantity"] and [list(r) for r in rows.get("rows", [])] == want and rows.get("matched_rows") == 30 and rows.get("returned_rows") == 5)
agg = q(FakeS3(), FOLDER, {"group_by": ["account_id"], "aggregates": [{"function": "sum", "alias": "q", "field": "quantity"}], "order_by": [{"field": "account_id", "direction": "asc"}]})
got = {int(r[0]): float(r[1]) for r in agg.get("rows", [])}
exp = {a: float(sum(i for i in range(300) if i % 10 == a)) for a in range(10)}
say("an aggregate request answers one row per account with the right sum (%d groups)" % len(got), got == exp)
p1 = q(FakeS3(), FOLDER, {"columns": ["quantity"], "order_by": [{"field": "quantity", "direction": "asc"}]})
c1 = p1.get("next_cursor")
say("the default page is 100 of 300 matching and carries next_cursor (returned %s, matched %s)" % (p1.get("returned_rows"), p1.get("matched_rows")), p1.get("returned_rows") == 100 and p1.get("matched_rows") == 300 and isinstance(c1, str) and bool(c1))
p2 = q(FakeS3(), FOLDER, {"columns": ["quantity"], "order_by": [{"field": "quantity", "direction": "asc"}]}, cursor=c1 or "")
a = [r[0] for r in p1.get("rows", [])]
b = [r[0] for r in p2.get("rows", [])]
say("the next page continues with no overlap (%s..%s then %s..%s)" % (a[:1], a[-1:], b[:1], b[-1:]), bool(a) and bool(b) and a[-1] == 99.0 and b[0] == 100.0 and not set(a) & set(b))
other = q(FakeS3(), FOLDER, {"columns": ["quantity"], "order_by": [{"field": "quantity", "direction": "desc"}]}, cursor=c1 or "")
tam = q(FakeS3(), FOLDER, {"columns": ["quantity"], "order_by": [{"field": "quantity", "direction": "asc"}]}, cursor=(c1 or "x")[:-3] + "AAA")
say("a cursor reused with a different request and a tampered cursor answer INVALID_REQUEST (%s | %s)" % (other.get("code"), tam.get("code")), other.get("code") == "INVALID_REQUEST" and tam.get("code") == "INVALID_REQUEST")
g = q(FakeS3(), FOLDER, {"columns": ["account_id"], "limit": 3}, admin=False, r=REC)
n = q(FakeS3(), B + "/schwab/08242234/silver/", {"columns": ["account_id"]}, admin=False, r=REC)
say("a person granted the master folder queries it and is refused for the sibling master (%s | %s)" % (g.get("returned_rows"), n.get("code")), g.get("returned_rows") == 3 and n.get("code") == "folder_refused")
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
