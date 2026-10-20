"""HVST-co-2 (AMGT_HARVST, 0.9.0_WK_AMGT_HARVST~186): a READ-ONLY measurement of the gold chatter
rebuild. Writes nothing to S3, calls no gold, silver or bronze writer, no Bloomberg, no model.

Method: the HVST-cn-4 import-closure method (deliverables 0.9.0_WK_AMGT_HARVST~181/cn4_closure.py),
reused unchanged -- the same child process with a builtins.__import__ hook, the same per-distribution
sizes, the same static LIBIMPORT check and the same two controls -- pointed at the new entry
lib.research.harvest.publication_gold. The two controls print first, as the order requires.

Also measured: the write rule of write_gold (read from its source lines), the newest date= partition
of each gold table (S3 list only, no object body), the trading-day lag (lib/trading_calendar.py), and
the roster source of a gold build (its file and function, and one newest chatter_daily object's
security_key column against the covered-universe listing).

Run from the repo root of the worktree:
    python -u <this file> > <this file's folder>/co2_gold.out
"""
import ast
import datetime
import importlib.metadata as im
import io
import json
import os
import re
import subprocess
import sys

MIB = 1024 * 1024
LIMIT_BYTES = 250 * MIB
ENTRY = "lib.research.harvest.publication_gold"
POSITIVE = "lib.research.harvest.store"
NEGATIVE = "json"
GOLD_TABLES = ("chatter_daily", "chatter_event", "article_security_mention")
ROSTER_FILE = ("org/missions/D5/AMGT/AMGT_HARVST/deliverables/"
               "0.9.0_WK_AMGT_HARVST~129/securities.universe.r75.json")
ROSTER_FUNCTION = "lib/research/harvest/universe_securities.py:build"

CHILD = r'''
import builtins, sys
root, target, out = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, root)
_orig = builtins.__import__
importer_of = {}
def _hook(name, globals=None, locals=None, fromlist=(), level=0):
    try:
        caller = sys._getframe(1).f_globals.get("__name__", "?")
    except Exception:
        caller = "?"
    before = set(sys.modules)
    try:
        return _orig(name, globals, locals, fromlist, level)
    finally:
        for k in list(sys.modules):
            if k not in before and k not in importer_of:
                importer_of[k] = caller
builtins.__import__ = _hook
err = None
try:
    exec("import " + target, {"__name__": "__closure_driver__"})
except BaseException as e:
    err = type(e).__name__ + ": " + str(e)[:300]
mods = []
for k, caller in importer_of.items():
    f = getattr(sys.modules.get(k), "__file__", None)
    mods.append([k, f, caller])
import json  # imported only after the measured import, so the json control is not pre-loaded
with open(out, "w", encoding="utf-8") as fh:
    json.dump({"target": target, "error": err, "modules": mods}, fh)
'''

STDLIB = set(sys.stdlib_module_names)


def is_third(top):
    return top not in STDLIB and not top.startswith("_") and top != "lib"


def run_child(root, target):
    scratch = os.path.join(root, ".scratch")
    os.makedirs(scratch, exist_ok=True)
    out = os.path.join(scratch, "co2_" + target.replace(".", "_") + ".json")
    if os.path.exists(out):
        os.remove(out)
    p = subprocess.run(
        [sys.executable, "-u", "-W", "ignore", "-c", CHILD, root, target, out],
        cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if p.returncode != 0 or not os.path.exists(out):
        return None, "child rc=%s stderr_tail=%s" % (p.returncode, p.stderr[-600:].replace("\n", " | "))
    with open(out, encoding="utf-8") as fh:
        data = json.load(fh)
    if data.get("error"):
        return None, "import error: " + data["error"]
    return data, ""


def static_tops(path):
    """Third-party top-level names imported at module top level (tl) and only inside functions (lz)."""
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read(), filename=path)
    tl, lz = set(), set()

    def names_of(node):
        if isinstance(node, ast.Import):
            return [a.name.split(".")[0] for a in node.names]
        if isinstance(node, ast.ImportFrom):
            if node.level or not node.module:
                return []
            return [node.module.split(".")[0]]
        return []

    def visit(node, in_func):
        for child in ast.iter_child_nodes(node):
            f = in_func or isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda))
            if isinstance(child, (ast.Import, ast.ImportFrom)):
                for t in names_of(child):
                    if is_third(t):
                        (lz if f else tl).add(t)
            visit(child, f)

    visit(tree, False)
    lz -= tl
    return tl, lz


def first_lib(top, importer_of):
    """Walk the recorded importer chain from a package upward to the first lib module."""
    seen = set()
    cur = importer_of.get(top)
    while cur and cur not in seen:
        seen.add(cur)
        if cur == "lib" or cur.startswith("lib."):
            return cur
        cur = importer_of.get(cur.split(".")[0])
    return "NONE"


def dist_size(dname, cache):
    if dname not in cache:
        d = im.distribution(dname)
        total, n = 0, 0
        for f in (d.files or []):
            try:
                p = f.locate()
            except Exception:
                continue
            if p.is_file():
                total += p.stat().st_size
                n += 1
        cache[dname] = (total, n, d.version)
    return cache[dname]


def measure_closure(root):
    """The cn4 closure of ENTRY. Returns (lines, verdict_fields) with the PKG and LIBIMPORT lines in order."""
    lines = []
    data, why = run_child(root, ENTRY)
    if data is None:
        return None, "ERROR: entry import did not measure: " + why
    mods = data["modules"]  # [name, file, importer] in load order
    importer_of = {n: imp for n, _f, imp in mods}
    lib_mods = sorted((n, f) for n, f, _i in mods if n.startswith("lib."))
    tops = sorted({n.split(".")[0] for n, _f, _i in mods if is_third(n.split(".")[0])})
    lines.append("CLOSURE-IMPORTED target=%s modules=%d lib_modules=%d third_party_tops=%d"
                 % (ENTRY, len(mods), len(lib_mods), len(tops)))

    static_all = {}
    for n, f, _i in mods:
        if f and f.endswith(".py") and os.path.isfile(f):
            try:
                static_all[n] = static_tops(f)
            except SyntaxError as e:
                lines.append("NOTE static parse failed name=%s err=%s" % (n, e))

    pkg_dists = im.packages_distributions()
    dcache = {}
    rows = []
    for t in tops:
        dl = sorted(pkg_dists.get(t, []))
        if dl:
            dname = dl[0]
            size, nfiles, ver = dist_size(dname, dcache)
        else:
            dname, size, nfiles, ver = "NONE", 0, 0, "NONE"
            tfile = next((f for n, f, _i in mods if n == t), None)
            lines.append("NOTE no-distribution top=%s file=%s" % (t, tfile))
        rows.append((size, t, dname, ver, nfiles, first_lib(t, importer_of), importer_of.get(t, "NONE")))
    rows.sort(key=lambda r: (-r[0], r[1]))
    for size, t, dname, ver, nfiles, fl, via in rows:
        lines.append("PKG %s dist=%s version=%s mb=%.2f files=%d first_lib_importer=%s via=%s"
                     % (t, dname, ver, size / MIB, nfiles, fl, via))
    dist_bytes = {}
    for size, t, dname, ver, nfiles, fl, via in rows:
        if dname != "NONE":
            dist_bytes[dname] = size
    third_party_bytes = sum(dist_bytes.values())

    lib_code_bytes = 0
    for n, f in lib_mods:
        if f and f.endswith(".py") and os.path.isfile(f):
            lib_code_bytes += os.path.getsize(f)
        tl, lz = static_all.get(n, (set(), set()))
        lines.append("LIBIMPORT %s top=%s lazy=%s" % (n, ",".join(sorted(tl)) or "none",
                                                      ",".join(sorted(lz)) or "none"))

    removable = []
    for t in tops:
        top_imp = [n for n, (tl, _lz) in static_all.items() if t in tl]
        lazy_imp = [n for n, (_tl, lz) in static_all.items() if t in lz]
        if lazy_imp and not top_imp:
            removable.append(t)

    total_bytes = lib_code_bytes + third_party_bytes
    verdict = "UNDER" if total_bytes <= LIMIT_BYTES else "OVER"
    biggest = sorted(dist_bytes.items(), key=lambda kv: (-kv[1], kv[0]))[:3]
    fields = {
        "lib_modules": len(lib_mods),
        "third_party_pkgs": len(dist_bytes),
        "third_party_mb": third_party_bytes / MIB,
        "lib_code_mb": lib_code_bytes / MIB,
        "total_mb": total_bytes / MIB,
        "verdict": verdict,
        "biggest": ",".join("%s:%.2f" % (n, s / MIB) for n, s in biggest) or "none",
        "removable": ",".join(removable) or "none",
    }
    return (lines, fields), ""


def write_gold_evidence(root):
    """Reads the write_gold source lines and derives add_only and full_snapshot from them."""
    path = os.path.join(root, "lib", "research", "harvest", "publication_gold.py")
    with open(path, encoding="utf-8") as fh:
        src = fh.read().split("\n")
    start = next(i for i, ln in enumerate(src, 1) if ln.startswith("def write_gold("))
    end = next(i for i, ln in enumerate(src, 1) if i > start and ln.startswith("def ")) - 1

    def hits(needle):
        return [i for i in range(start, end + 1) if needle in src[i - 1]]

    put = hits("client.put_object(")
    ifnm = hits('IfNoneMatch="*"')
    rows_in = hits("from_pylist(list(rows)")
    to_parquet = hits("pq.write_table(arrow_table")
    key_line = hits("object_name = store.form_c_object(")
    uri_line = hits("uri = store.address_of(")
    head_line = hits("head = client.head_object(")
    add_only = "yes" if len(put) == 1 and len(ifnm) == 1 else "no"
    full_snapshot = "yes" if rows_in and to_parquet and len(put) == 1 else "no"
    print("NOTE write_gold evidence: def=%d rows_to_arrow=%s parquet=%s key=%s uri=%s put=%s "
          "IfNoneMatch=%s readback=%s file_end=%d"
          % (start, rows_in, to_parquet, key_line, uri_line, put, ifnm, head_line, end))
    return add_only, full_snapshot


def key_shape(store):
    """The object key write_gold builds, derived by calling the same address_of/form_c_object pair."""
    sample = store.address_of("amgt", "gold", "chatter_daily",
                              store.date_partition(datetime.date(2026, 10, 8)),
                              object_name=store.form_c_object("part-20261009T061012Z", "parquet"))
    if not sample.startswith("s3://" + store.HARVEST_BUCKET + "/"):
        raise SystemExit("ERROR: address_of did not return the harvest bucket: " + sample)
    key = sample[len("s3://" + store.HARVEST_BUCKET + "/"):]
    tmpl = (key.replace("chatter_daily", "<table>")
               .replace("date=2026-10-08", "date=<date>")
               .replace("part-20261009T061012Z.parquet", "part-<run_stamp>.parquet"))
    return tmpl


def newest_partition(store, client, table):
    prefix = store.table_prefix("amgt", "gold", table)
    dates = []
    paginator = client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix, Delimiter="/"):
        for cp in page.get("CommonPrefixes", []) or []:
            seg = cp["Prefix"][len(prefix):].rstrip("/")
            if seg.startswith("date=") and re.fullmatch(r"\d{4}-\d\d-\d\d", seg[5:]):
                dates.append(seg[5:])
    dates.sort()
    return prefix, dates


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", newline="\n", write_through=True)
    root = os.getcwd()
    if not os.path.isfile(os.path.join(root, "lib", "research", "harvest", "publication_gold.py")):
        print("ERROR: run from the repo root of the worktree (publication_gold.py not under cwd)")
        return 2
    sys.path.insert(0, root)

    # 1. The two closure controls, first.
    pos, pos_why = run_child(root, POSITIVE)
    if pos is None:
        print("CONTROL-POSITIVE target=%s pyarrow_in_closure=unmeasured reason=%s" % (POSITIVE, pos_why))
    else:
        has = any(n.split(".")[0] == "pyarrow" for n, _f, _i in pos["modules"])
        print("CONTROL-POSITIVE target=%s pyarrow_in_closure=%s" % (POSITIVE, "yes" if has else "no"))
    neg, neg_why = run_child(root, NEGATIVE)
    if neg is None:
        print("CONTROL-NEGATIVE target=%s third_party_tops=unmeasured reason=%s" % (NEGATIVE, neg_why))
    else:
        neg_tops = {n.split(".")[0] for n, _f, _i in neg["modules"] if is_third(n.split(".")[0])}
        print("NOTE control-negative json newly_loaded=%d" % len(neg["modules"]))
        print("CONTROL-NEGATIVE target=%s third_party_tops=%d" % (NEGATIVE, len(neg_tops)))

    # 2. The closure of the entry.
    measured, why = measure_closure(root)
    if measured is None:
        print(why)
        return 1
    lines, f = measured
    for ln in lines:
        print(ln)
    print("GOLD-CLOSURE entry=%s lib_modules=%d third_party_pkgs=%d third_party_mb=%.2f lib_code_mb=%.2f "
          "total_mb=%.2f limit_unzipped_mb=250 verdict=%s biggest=%s removable_by_lazy=%s"
          % (ENTRY, f["lib_modules"], f["third_party_pkgs"], f["third_party_mb"], f["lib_code_mb"],
             f["total_mb"], f["verdict"], f["biggest"], f["removable"]))

    # 3. The write rule of write_gold, read from its source lines.
    add_only, full_snapshot = write_gold_evidence(root)
    import lib.research.harvest.store as store
    tmpl = key_shape(store)
    print("GOLD-WRITE key_shape=%s add_only=%s full_snapshot=%s" % (tmpl, add_only, full_snapshot))

    # 4. The newest date= partition of each gold table (S3 list only) and the trading-day lag.
    client = store._default_client()
    newest = {}
    prefixes = {}
    for table in GOLD_TABLES:
        prefix, dates = newest_partition(store, client, table)
        prefixes[table] = prefix
        newest[table] = dates[-1] if dates else "none"
        print("NOTE newest partition table=%s prefix=%s partitions=%d newest=%s"
              % (table, prefix, len(dates), newest[table]))
    import lib.trading_calendar as tc
    now_utc = datetime.datetime.now(datetime.timezone.utc).date()
    expected = tc.expected_last_trading_day(now_utc)
    if newest["chatter_daily"] != "none":
        lag = tc.trading_days_behind(newest["chatter_daily"], expected)
    else:
        lag = -1
    print("NOTE trading_days_behind chatter_daily_newest=%s expected_last_trading_day=%s now_utc=%s "
          "calendar_source=%s" % (newest["chatter_daily"], expected.isoformat(), now_utc.isoformat(),
                                  tc.calendar_source(expected)))
    print("GOLD-NEWEST chatter_daily=%s chatter_event=%s article_security_mention=%s trading_days_behind=%d"
          % (newest["chatter_daily"], newest["chatter_event"], newest["article_security_mention"], lag))

    # 5. The roster source: the file and function, the count, and one newest chatter_daily object.
    roster_path = os.path.join(root, ROSTER_FILE)
    with open(roster_path, encoding="utf-8") as fh:
        roster = json.load(fh)
    roster_keys = {s["security_key"] for s in roster}
    print("NOTE roster file=%s entries=%d distinct_security_keys=%d function=%s"
          % (ROSTER_FILE, len(roster), len(roster_keys), ROSTER_FUNCTION))

    import pyarrow.parquet as pq
    import lib.research.coverage.covered_universe as cu
    daily_prefix = prefixes["chatter_daily"]
    part_prefix = daily_prefix + "date=%s/" % newest["chatter_daily"]
    part_keys = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=part_prefix):
        for o in page.get("Contents", []) or []:
            if o["Key"].endswith(".parquet"):
                part_keys.append(o["Key"])
    part_keys.sort()
    one_key = part_keys[-1]
    body = client.get_object(Bucket=store.HARVEST_BUCKET, Key=one_key)["Body"].read()
    tbl = pq.read_table(io.BytesIO(body), columns=["security_key"])
    daily_keys = {v for v in tbl.column("security_key").to_pylist() if v is not None}
    covered = cu.covered_security_keys(client=client)
    covered_set = set(covered)
    print("NOTE roster newest_chatter_daily_object=%s objects_in_partition=%d rows=%d"
          % (one_key, len(part_keys), tbl.num_rows))
    print("NOTE roster newest_chatter_daily_distinct_keys=%d covered_universe_keys=%d equal=%s"
          % (len(daily_keys), len(covered_set), "yes" if daily_keys == covered_set else "no"))
    print("NOTE roster overlap daily_not_covered=%d covered_not_daily=%d roster_file_vs_daily_not_in_file=%d"
          % (len(daily_keys - covered_set), len(covered_set - daily_keys), len(daily_keys - roster_keys)))
    print("GOLD-ROSTER source=%s names=%d" % (ROSTER_FUNCTION, len(roster)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
