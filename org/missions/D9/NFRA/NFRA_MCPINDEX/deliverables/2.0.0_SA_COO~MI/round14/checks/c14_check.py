"""c14_check.py -- grades MX-c-14's silver table rows against the CRO's G2, G4, G5 and G6 contracts at their pins (glib.PINS).

  python c14_check.py ac1 [--rows DIR]   the entity set (174), hashed ids, the legacy_addresses rows and the fork registry file
  python c14_check.py ac2 [--rows DIR]   each row equals the expected CLEAN row (no firm or product token), the carrier scan
  python c14_check.py ac3                the generator under 5 planted deployed-tool sets (read_tool policy), 870 of 870 rows

DIR defaults to workflows/atom_decomposition/catalog_entries. A table row is a non-harvest yaml there that carries a `contract`.
The generator under test is workflows/atom_decomposition/gen_silver_rows.py unless C14_GEN names another. The registry files are read
from infra/logic/registry unless PLANT_REGISTRY_DIR names a copy (the cut-time planted arms). Exit 0 PASS, 1 FAIL, 9 the instrument
could not run.
"""
import glob
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import glib  # noqa: E402

ROWS_DIR_DEFAULT = os.path.join("workflows", "atom_decomposition", "catalog_entries")
CONSISTENCY_ONLY = ("read_tool", "tools", "gap_owner", "business_meaning")


def load_rows(d):
    import yaml
    rows = {}
    for path in sorted(glob.glob(os.path.join(d, "*.yaml"))):
        fn = os.path.basename(path)
        if fn.startswith("harvest_"):
            continue
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if isinstance(data, dict) and "contract" in data:
            rows[fn] = data
    return rows


def expected(allc):
    return {cid: (g, c) for cid, (g, c) in allc.items() if glib.in_scope(c)}


def leaves(x, path=""):
    """Every string key and string value in a row, with its path."""
    if isinstance(x, dict):
        for k, v in x.items():
            yield path + "/" + str(k), k
            for p in leaves(v, path + "/" + str(k)):
                yield p
    elif isinstance(x, list):
        for i, v in enumerate(x):
            for p in leaves(v, path + "/" + str(i)):
                yield p
    elif isinstance(x, str):
        yield path, x


def ac1(d, allc):
    rows = load_rows(d)
    exp = expected(allc)
    want = {glib.entity(cid) + ".yaml": glib.hashed_id(cid) for cid in exp}
    have = {fn: (r.get("contract") or {}).get("id") for fn, r in rows.items()}
    missing = sorted(set(want) - set(have))
    extra = sorted(set(have) - set(want))
    idbad = [fn for fn in set(want) & set(have) if have[fn] != want[fn]]
    uniq = len(set(want)) == len(want) and len(set(want.values())) == len(want)
    print("ROWS files=%d; in-scope contracts=%d (G2+G4+G5+G6 less %d already rowed in silver_datasets); entity names and hashed ids unique=%s; "
          "missing %d, extra %d, contract.id wrong %d"
          % (len(rows), len(exp), len(allc) - len(exp), "yes" if uniq else "NO", len(missing), len(extra), len(idbad)))
    for x in missing[:4]:
        print("  missing: %s" % x)
    for x in extra[:4]:
        print("  extra: %s" % x)
    reg_dir = glib.registry_dir()
    reg = json.load(open(os.path.join(reg_dir, "legacy_addresses.json"), encoding="utf-8")).get("legacy_addresses", [])
    have_reg = {(r.get("bucket"), r.get("template")): r for r in reg}
    need = {(c["bucket"], glib.row_prefix(c)) for cid, (g, c) in exp.items() if glib.needs_registry(c)}
    other = {k for k in need if k in have_reg and have_reg[k].get("reader") != "NFRA_MCPINDEX"}   # (bucket, template) is unique: another project holds it
    need = need - other
    reg_ok = sum(1 for k in need if k in have_reg and have_reg[k].get("reader") == "NFRA_MCPINDEX" and not have_reg[k].get("params")
                 and have_reg[k].get("shape") == ("prefix" if k[1].endswith("/") else "object"))
    print("REGISTRY legacy_addresses rows (reader NFRA_MCPINDEX) resolve %d of %d distinct registered prefixes (%d more already held by another project: %s)"
          % (reg_ok, len(need), len(other), sorted(other)[:2]))
    fp = os.path.join(reg_dir, glib.FORK_REGISTRY)
    fork = json.load(open(fp, encoding="utf-8")).get("rows", {}) if os.path.exists(fp) else {}
    want_fork = glib.fork_registry_rows(allc)
    fork_ok = sum(1 for k, v in want_fork.items() if fork.get(k) == v)
    print("FORK REGISTRY %s holds %d of %d rows exactly (the restore values and key_template)" % (glib.FORK_REGISTRY, fork_ok, len(want_fork)))
    return (uniq and not missing and not extra and not idbad and len(rows) == glib.EXPECT_ROWS and reg_ok == len(need)
            and fork_ok == len(want_fork))


def ac2(d, allc):
    rows = load_rows(d)
    exp = expected(allc)
    fails = {}

    def bad(field, fn, why):
        fails.setdefault(field, []).append("%s: %s" % (fn, why))

    graded = 0
    for cid, (g, c) in exp.items():
        fn = glib.entity(cid) + ".yaml"
        r = rows.get(fn)
        if r is None:
            bad("row", fn, "no row")
            continue
        graded += 1
        want, _entry = glib.expected_row(c, g)
        if set(r) != set(want):
            bad("keys", fn, "extra %s missing %s" % (sorted(set(r) - set(want)), sorted(set(want) - set(r))))
        for k, v in want.items():
            if k in CONSISTENCY_ONLY or k not in r:
                continue
            if r[k] != v:
                bad(k, fn, "differs from the expected clean value")
        for path, s in leaves(r):
            if glib.carrier(s):
                bad("carrier", fn, "%s carries a firm or product token: %r" % (path, s[:50]))
                break
        eq = r.get("example_questions")
        if not (isinstance(eq, list) and eq and all(isinstance(x, str) and x.strip() for x in eq)):
            bad("example_questions", fn, "empty")
        pr = r.get("producer")
        if not (isinstance(pr, str) and pr.strip()):
            bad("producer", fn, "empty")
        bm = r.get("business_meaning")
        if not (isinstance(bm, str) and len(bm.strip()) >= 40 and not bm.startswith("NONE")):
            bad("business_meaning", fn, "empty, under 40 chars or NONE")
        else:
            stale, empty = glib.marks(c)
            for word, label in ((stale, "NOT CURRENT"), (empty, "EMPTY")):
                if word and word not in bm:
                    bad("business_meaning", fn, "must carry %r (frozen or empty is never current)" % word)
                if not word and label in bm:
                    bad("business_meaning", fn, "carries %s but the contract does not support it" % label)
        rt, go, tl = r.get("read_tool"), r.get("gap_owner"), r.get("tools")
        if rt is None and not (isinstance(go, str) and go.strip()):
            bad("read_tool", fn, "null read_tool needs a gap_owner")
        if rt is not None and go is not None:
            bad("read_tool", fn, "gap_owner must be null when read_tool is named")
        if tl != ([rt] if rt else []):
            bad("tools", fn, "tools %r != %r" % (tl, [rt] if rt else []))
    nfield = sum(len(v) for v in fails.values())
    print("ROWS graded %d of %d; failing fields: %s"
          % (graded, len(exp), ", ".join("%s x%d" % (k, len(v)) for k, v in sorted(fails.items())) or "none"))
    for k, v in sorted(fails.items()):
        for x in v[:2]:
            print("  [%s] %s" % (k, x))
    return graded == len(exp) and nfield == 0


def ac3(allc):
    gen = os.environ.get("C14_GEN") or os.path.join("workflows", "atom_decomposition", "gen_silver_rows.py")
    if not os.path.exists(gen):
        print("GENERATOR absent: %s" % gen)
        return False
    exp = expected(allc)
    names = sorted({t for _g, c in exp.values() for t in glib.candidates(c)})
    clients = [t for t in names if t.startswith("client_")]
    arms = {
        "D0 nothing deployed": [],
        "D1 two client tools": ["client_resolve_account", "client_get_holdings"],
        "D2 every candidate deployed": names,
        "D3 D2 minus client_get_holdings": [t for t in names if t != "client_get_holdings"],
        "D4 D2 minus client_get_fees": [t for t in names if t != "client_get_fees"],
    }
    tmp = tempfile.mkdtemp(prefix="c14ac3_")
    files = {}
    for g in glib.PINS:
        p = os.path.join(tmp, "%s_pinned.md" % g)
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(glib.group_text(g))
        files[g] = p
    ok_arms, rows_ok, rows_all = 0, 0, 0
    for name, deployed in arms.items():
        tag = name.split()[0]
        out = os.path.join(tmp, tag)
        dep = os.path.join(tmp, tag + ".json")
        with open(dep, "w", encoding="utf-8") as f:
            json.dump(deployed, f)
        r = subprocess.run([sys.executable, gen, "--g2", files["G2"], "--g4", files["G4"], "--g5", files["G5"], "--g6", files["G6"], "--out", out,
                            "--deployed-tools", dep], capture_output=True, timeout=100)
        rows_all += len(exp)
        if r.returncode != 0:
            print("ARM %s: generator rc=%d: %s" % (name, r.returncode, (r.stderr or r.stdout).decode("utf-8", "replace")[-200:].strip()))
            continue
        rows = load_rows(out)
        bad = 0
        for cid, (_g, c) in exp.items():
            x = rows.get(glib.entity(cid) + ".yaml")
            want = glib.expected_read_tool(c, set(deployed))
            if x is None or x.get("read_tool") != want or (want is None and x.get("gap_owner") != "NFRA_OPLGTW") \
                    or (want is not None and x.get("gap_owner") is not None):
                bad += 1
                if bad <= 2:
                    print("  [%s] %s: read_tool %r gap_owner %r, want %r" % (name, cid, x and x.get("read_tool"), x and x.get("gap_owner"), want))
            else:
                rows_ok += 1
        if len(rows) == len(exp) and bad == 0:
            ok_arms += 1
        print("ARM %s: files %d, rows wrong %d" % (name, len(rows), bad))
    print("ARMS pass %d of %d; rows graded right %d of %d (client tools in play: %d)" % (ok_arms, len(arms), rows_ok, rows_all, len(clients)))
    return ok_arms == len(arms) and rows_ok == rows_all


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 9
    mode = sys.argv[1]
    d = ROWS_DIR_DEFAULT
    if "--rows" in sys.argv:
        d = sys.argv[sys.argv.index("--rows") + 1]
    allc = glib.load_all()
    ok = {"ac1": lambda: ac1(d, allc), "ac2": lambda: ac2(d, allc), "ac3": lambda: ac3(allc)}[mode]()
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
