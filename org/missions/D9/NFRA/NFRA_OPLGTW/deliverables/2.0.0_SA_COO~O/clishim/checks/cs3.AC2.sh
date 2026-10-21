#!/usr/bin/env bash
# OPLGTW OG-cs-3 AC2 (cli-shim workstream, wave 2): app/folder_engine.py, the byte-bounded half. One fresh process, a tiny parquet written with pyarrow in a temp folder, no AWS.
#  (a) check_sources(sizes) -> None inside the engine's caps (12 objects, 64 MiB compressed in all) and a dict {"code": "LIMIT_EXCEEDED", "reason": ..., "suggestion": ...} outside them: 13 objects, or a total one byte over 64 MiB; the suggestion tells the caller to narrow (the word "narrow" appears);
#  (b) describe_parquet(read_range, size) reads only the FOOTER: for a 60,000-row file it returns the columns [{"name", "type"}] in file order (names as stored, sensitive ones INCLUDED: dropping is the caller's), num_rows 60000 and row_groups >= 1, and the bytes it asked read_range for are under a quarter of the file;
#  (c) CONTROL: the same function on a 5-row file returns num_rows 5 and the same column shape; on bytes that are not parquet it raises ValueError (no other exception type, no partial answer).
. "$(dirname "$0")/../../r47/checks/_gwtests.sh"
res=$(python3 -I - "$(native "$GW")" <<'PYEOF'
import os, sys, tempfile
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
    from app import folder_engine as fe
    import pyarrow as pa
    import pyarrow.parquet as pq
except Exception as exc:  # noqa: BLE001
    print("import failed: %s: %s" % (type(exc).__name__, str(exc)[:80]))
    print("NO")
    sys.exit(0)
MIB = 1048576
a = fe.check_sources([MIB] * 12)
b = fe.check_sources([MIB] * 13)
c = fe.check_sources([64 * MIB, 1])
d = fe.check_sources([64 * MIB])
say("inside the caps answers None (12 objects, and exactly 64 MiB)", a is None and d is None)
say("13 objects and 64 MiB + 1 byte answer LIMIT_EXCEEDED with a suggestion that says narrow", all(isinstance(x, dict) and x.get("code") == "LIMIT_EXCEEDED" and x.get("reason") and "narrow" in str(x.get("suggestion", "")).lower() for x in (b, c)))
tmp = tempfile.mkdtemp()


def write(path, rows):
    t = pa.table({"a": list(range(rows)), "b": ["x%d" % (i % 7) for i in range(rows)], "email": ["u%d@example.invalid" % (i % 5) for i in range(rows)]})
    pq.write_table(t, path, row_group_size=20000)


big, small = os.path.join(tmp, "big.parquet"), os.path.join(tmp, "small.parquet")
write(big, 60000)
write(small, 5)


def reader(path, counter):
    def read_range(offset, length):
        with open(path, "rb") as fh:
            fh.seek(offset)
            data = fh.read(length)
        counter.append(len(data))
        return data
    return read_range


cnt = []
try:
    out = fe.describe_parquet(reader(big, cnt), os.path.getsize(big))
    cols = [(x["name"], x["type"]) for x in out["columns"]]
    say("a 60,000-row file: columns in file order with types, num_rows 60000, row_groups >= 1 (%s)" % cols, [n for n, _ in cols] == ["a", "b", "email"] and all(t for _, t in cols) and out["num_rows"] == 60000 and out["row_groups"] >= 1)
    say("only the footer was read: %d bytes of %d" % (sum(cnt), os.path.getsize(big)), 0 < sum(cnt) < os.path.getsize(big) / 4)
    cnt2 = []
    out2 = fe.describe_parquet(reader(small, cnt2), os.path.getsize(small))
    say("control: a 5-row file answers num_rows 5 and the same columns", out2["num_rows"] == 5 and [x["name"] for x in out2["columns"]] == ["a", "b", "email"])
except Exception as exc:  # noqa: BLE001
    say("describe_parquet ran (%s: %s)" % (type(exc).__name__, str(exc)[:60]), False)
junk = b"this is not a parquet file at all" * 40
try:
    fe.describe_parquet(lambda o, n: junk[o:o + n], len(junk))
    say("bytes that are not parquet raise ValueError", False)
except ValueError:
    say("bytes that are not parquet raise ValueError", True)
except Exception as exc:  # noqa: BLE001
    say("bytes that are not parquet raise ValueError (got %s)" % type(exc).__name__, False)
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
