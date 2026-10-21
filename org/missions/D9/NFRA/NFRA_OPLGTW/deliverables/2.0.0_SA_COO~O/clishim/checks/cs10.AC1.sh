#!/usr/bin/env bash
# OPLGTW OG-cs-10 AC1 (cli-shim workstream, wave 4): app/integrations/folders/integration.py, the DORMANT integration that mounts the three folder tools. One fresh process, no AWS, no network.
#   INTEGRATION_ID == "folders"; TOOL_NAMES == ("folder_list", "folder_describe", "folder_query"); SPEC (an IntegrationSpec);
#   FoldersIntegration(deps_factory=None): deps_factory() returns an object with attributes s3, engine, codec (default: built lazily on first use, never at construction);
#   `await integ.dispatch(principal, rec, is_master_admin, is_opal, tool, args) -> dict` maps folder_list(path, start_after="") to folder_tools.list_folder, folder_describe(path) to describe_object, folder_query(path, request, cursor="") to query_object;
#   `integ.register(mcp) -> list[str]` registers the three tools with `mcp.tool(name=...)(fn)` and returns TOOL_NAMES as a list.
#  (a) the spec: id folders, tool_prefix folder_, read_only, auth ASSUMED_ROLE, min_tier read_only, a SAFE tool_classifications row for each tool; register() registers exactly the three names in order;
#  (b) dispatch answers EXACTLY what the folder_tools function answers for the same arguments (list, describe, query against the REAL engine);
#  (c) a refused path makes ZERO S3 calls through every one of the three tools; a non-str path, a non-dict request and an unknown tool answer a dict (codes INVALID_REQUEST / unknown_tool) with zero S3 calls and never raise;
#  (d) construction never calls the factory, and a factory that raises makes dispatch answer {"code": "UNAVAILABLE"} instead of raising.
. "$(dirname "$0")/../../r47/checks/_gwtests.sh"
# The engine spawns a child process, and a spawn child re-imports the main script by path: the probe is a FILE with its work behind a main guard
# (a stdin script cannot be re-imported on Windows).
PROBE="$(mktemp "${TMPDIR:-/tmp}/cs10ac1.XXXXXX")"; mv "$PROBE" "$PROBE.py"; PROBE="$PROBE.py"
cat > "$PROBE" <<'PYEOF'
def _probe():
    import asyncio, io, os, sys, tempfile
    G = sys.argv[1]
    sys.path.insert(0, G)
    os.environ["MOCK_GRAPH"] = "1"
    import warnings
    warnings.simplefilter("ignore")
    ok = True


    def say(label, cond):
        nonlocal ok
        ok = ok and bool(cond)
        print("%s: %s" % (label, "ok" if cond else "NOT OK"))


    try:
        import datetime
        import pyarrow as pa, pyarrow.parquet as pq
        from app import data_entitlement as de, folder_tools as ft
        from app.integrations import base
        from app.integrations.folders import integration as fi
        from app.integrations.schwab import engine as eng, cursor as cur
    except Exception as exc:  # noqa: BLE001
        print("import failed: %s: %s" % (type(exc).__name__, str(exc)[:80]))
        print("NO")
        sys.exit(0)

    NAMES = ("folder_list", "folder_describe", "folder_query")
    B = "opal-data-assets"
    P = "schwab/08335338/silver/fact_trn/date=2026-10-20/"
    buf = io.BytesIO()
    pq.write_table(pa.table({"account_id": [i % 10 for i in range(100)], "quantity": [float(i) for i in range(100)], "email": ["u%d@example.invalid" % i for i in range(100)]}), buf)
    OBJ = {(B, P + "a.parquet"): buf.getvalue()}


    class FakeS3:
        def __init__(self):
            self.calls = 0

        def list_objects_v2(self, Bucket, Prefix="", Delimiter="", MaxKeys=1000, StartAfter="", **kw):  # noqa: N803
            self.calls += 1
            keys = sorted(k for (b, k) in OBJ if b == Bucket and k.startswith(Prefix) and k > StartAfter)
            cs, ps = [], []
            for k in keys:
                rest = k[len(Prefix):]
                if Delimiter and Delimiter in rest:
                    p = Prefix + rest.split(Delimiter)[0] + Delimiter
                    if p not in ps:
                        ps.append(p)
                else:
                    cs.append(k)
            return {"Contents": [{"Key": k, "Size": len(OBJ[(Bucket, k)]), "LastModified": datetime.datetime(2026, 10, 20, tzinfo=datetime.timezone.utc)} for k in cs],
                    "CommonPrefixes": [{"Prefix": p} for p in ps], "IsTruncated": False}

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
            with open(Filename, "wb") as f:
                f.write(OBJ[(Bucket, Key)])


    class Deps:
        pass


    tmp = tempfile.mkdtemp(prefix="cs10ac1")
    engine = eng.ExecutionEngine(temp_root=os.path.join(tmp, "engine-root"), memory_total_bytes=lambda: 1 << 40)
    codec = cur.CursorCodec(os.urandom(32))
    s3 = FakeS3()
    d = Deps()
    d.s3, d.engine, d.codec = s3, engine, codec
    integ = fi.FoldersIntegration(deps_factory=lambda: d)
    sp = integ.spec
    cls = sp.tool_classifications
    safe_ok = all(n in cls and str(getattr(cls[n].get("class"), "value", cls[n].get("class"))).lower().endswith("safe") for n in NAMES)
    say("the spec: id %s, prefix %s, read_only %s, auth %s, min_tier %s, SAFE rows %s" % (sp.id, sp.tool_prefix, sp.read_only, getattr(sp.auth_kind, "name", sp.auth_kind), sp.min_tier, safe_ok),
        fi.INTEGRATION_ID == "folders" and sp.id == "folders" and sp.tool_prefix == "folder_" and sp.read_only is True and sp.auth_kind == base.AuthKind.ASSUMED_ROLE and sp.min_tier == "read_only" and safe_ok and tuple(fi.TOOL_NAMES) == NAMES)


    class FakeMCP:
        def __init__(self):
            self.names = []

        def tool(self, name=None, **kw):
            def deco(fn):
                self.names.append(name or fn.__name__)
                return fn
            return deco


    m = FakeMCP()
    got = integ.register(m)
    say("register() registers exactly the three tools in order and returns them (%s | %s)" % (m.names, got), m.names == list(NAMES) and list(got) == list(NAMES))
    REC = de.PersonAccess("active", 3, False, frozenset(), frozenset(), frozenset(["opal-data-assets/schwab/08335338/"]), frozenset())


    def run(coro):
        return asyncio.run(coro)


    FOLDER = B + "/" + P
    for label, who in (("an admin", (None, True, True)), ("a granted person", (REC, False, True))):
        rec, adm, opal = who
        want_l = ft.list_folder("tid/oid", rec, adm, opal, FakeS3(), B + "/schwab/08335338/silver/")
        got_l = run(integ.dispatch("tid/oid", rec, adm, opal, "folder_list", {"path": B + "/schwab/08335338/silver/"}))
        want_d = ft.describe_object("tid/oid", rec, adm, opal, FakeS3(), FOLDER + "a.parquet")
        got_d = run(integ.dispatch("tid/oid", rec, adm, opal, "folder_describe", {"path": FOLDER + "a.parquet"}))
        say("dispatch answers what folder_tools answers for %s: list and describe (%d prefixes, %d columns)" % (label, len(got_l.get("prefixes", [])), len(got_d.get("columns", []))), got_l == want_l and got_d == want_d and bool(got_l.get("prefixes")) and bool(got_d.get("columns")))
    req = {"columns": ["account_id", "quantity"], "filters": [{"field": "account_id", "op": "eq", "value": 3}], "order_by": [{"field": "quantity", "direction": "asc"}], "limit": 4}
    gq = run(integ.dispatch("tid/oid", None, True, True, "folder_query", {"path": FOLDER, "request": req}))
    say("dispatch query runs on the real engine from deps (rows %s, matched %s)" % (gq.get("rows"), gq.get("matched_rows")), [list(r) for r in gq.get("rows", [])] == [[3, 3.0], [3, 13.0], [3, 23.0], [3, 33.0]] and gq.get("matched_rows") == 10)
    z = FakeS3()
    d.s3 = z
    refs = [run(integ.dispatch("tid/oid", None, True, True, t, a)) for t, a in (("folder_list", {"path": B + "/schwab/08335338/bronze/"}), ("folder_describe", {"path": B + "/schwab/08335338/bronze/x.parquet"}), ("folder_query", {"path": B + "/raw/", "request": {"columns": ["a"]}}))]
    say("a refused path makes ZERO S3 calls through every tool (%d)" % z.calls, all(r.get("code") == "folder_refused" for r in refs) and z.calls == 0)
    bad = []
    for t, a in (("folder_list", {"path": 7}), ("folder_describe", {}), ("folder_query", {"path": FOLDER, "request": "select 1"}), ("folder_nope", {"path": FOLDER})):
        try:
            bad.append(run(integ.dispatch("tid/oid", None, True, True, t, a)))
        except Exception as exc:  # noqa: BLE001
            bad.append({"_exc": str(exc)[:40]})
    say("bad inputs answer a dict with a code, zero S3 calls, no raise (%s)" % [b.get("code") for b in bad], all(isinstance(b, dict) and b.get("code") in ("INVALID_REQUEST", "unknown_tool") for b in bad) and z.calls == 0)
    n = {"c": 0}


    def boom():
        n["c"] += 1
        raise RuntimeError("no role")


    lazy = fi.FoldersIntegration(deps_factory=boom)
    built_before = n["c"]
    out = run(lazy.dispatch("tid/oid", None, True, True, "folder_list", {"path": FOLDER}))
    say("construction never calls the factory and a raising factory answers UNAVAILABLE (calls before %d, code %s)" % (built_before, out.get("code")), built_before == 0 and out.get("code") == "UNAVAILABLE")
    print("OK" if ok else "NO")


if __name__ == "__main__":
    import sys as _s
    _probe()
PYEOF
res=$(python3 -I "$(native "$PROBE")" "$(native "$GW")")
rm -f "$PROBE"
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
