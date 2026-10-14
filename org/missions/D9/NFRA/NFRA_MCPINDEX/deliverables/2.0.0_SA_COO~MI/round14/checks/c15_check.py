"""c15_check.py -- grades MX-c-15: the silver TABLE row loader joins the fork registry and accepts the clean v2 row.

  python c15_check.py ac1   load_catalog_entries accepts 174 clean rows (null prefix, label, sanitised fork_keys), JOINS the fork registry
                            so each loaded row equals its FULL expected row, keeps the 10 old rows, and refuses 10 one-defect rows
  python c15_check.py ac2   silver_catalog_row emits the joined row with key_template; an old row and an un-joined row are unchanged

The implementation under test is workflows/atom_decomposition/emit_catalog_v02.py unless C15_IMPL names another module file (the
cut-time planted arms use that to prove the check discriminates). The registry files are a planted copy built by the check itself
(glib.plant_registry_dir14), so the check does not depend on the rows or registry rows MX-c-14 lands. Exit 0 PASS, 1 FAIL, 9 no run.
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import glib  # noqa: E402

IMPL = os.environ.get("C15_IMPL") or os.path.join("workflows", "atom_decomposition", "emit_catalog_v02.py")


def load_impl(reg_dir):
    sys.path.insert(0, os.path.join(os.getcwd(), "lib"))
    import opal_naming
    opal_naming.REGISTRY_DIR = reg_dir
    spec = importlib.util.spec_from_file_location("c15_impl", IMPL)
    m = importlib.util.module_from_spec(spec)
    sys.modules["c15_impl"] = m
    spec.loader.exec_module(m)
    return m


def build(tmp, allc):
    files = {}
    for g in glib.PINS:
        p = os.path.join(tmp, g + ".md")
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(glib.group_text(g))
        files[g] = p
    dep = os.path.join(tmp, "none.json")
    with open(dep, "w") as f:
        f.write("[]")
    out = os.path.join(tmp, "good")
    r = subprocess.run([sys.executable, os.path.join(HERE, "plant_gen14.py"), "--g2", files["G2"], "--g4", files["G4"], "--g5", files["G5"],
                        "--g6", files["G6"], "--out", out, "--deployed-tools", dep], capture_output=True)
    if r.returncode != 0:
        print("ERROR: reference rows: %s" % r.stderr.decode("utf-8", "replace")[-200:])
        sys.exit(9)
    reg = glib.plant_registry_dir14(allc)
    return out, reg


def old_rows(tmp):
    base = glib.base_rows_dir()
    d = os.path.join(tmp, "old")
    os.makedirs(d, exist_ok=True)
    n = 0
    for fn in os.listdir(base):
        if fn.startswith(("harvest_", "need_")) or fn == "README.md":
            continue
        shutil.copy(os.path.join(base, fn), os.path.join(d, fn))
        n += 1
    return d, n


def full_of(c, g):
    row, entry = glib.expected_row(c, g)
    full = dict(row)
    full.update(entry["restore"])
    full["key_template"] = entry["key_template"]
    return full


def ac1():
    import yaml
    allc = glib.load_all()
    tmp = tempfile.mkdtemp(prefix="c15ac1_")
    good, reg = build(tmp, allc)
    old, n_old = old_rows(tmp)
    mix = os.path.join(tmp, "mix")
    shutil.copytree(good, mix)
    for fn in os.listdir(old):
        shutil.copy(os.path.join(old, fn), os.path.join(mix, fn))
    m = load_impl(reg)
    m.CATALOG_ENTRIES_DIR = mix
    entries, errors = m.load_catalog_entries()
    exp = {glib.entity(cid): full_of(c, g) for cid, (g, c) in allc.items() if glib.in_scope(c)}
    loaded = sum(1 for n in exp if n in entries)
    joined = sum(1 for n, f in exp.items() if entries.get(n) == f)
    got_old = sum(1 for n in entries if n in {x[:-5] for x in os.listdir(old)})
    print("ACCEPT: %d of %d clean table rows load; %d of %d JOINED to their full expected row (fork_keys, contract, table, prefix, key_template); "
          "existing rows still load %d of %d (errors %d)" % (loaded, len(exp), joined, len(exp), got_old, n_old, len(errors)))
    for k in sorted(errors)[:3]:
        print("  %s: %s" % (k, str(errors[k])[:170]))
    seed_name = next(n for n in sorted(exp) if yaml.safe_load(open(os.path.join(good, n + ".yaml"), encoding="utf-8")).get("prefix"))
    seed = yaml.safe_load(open(os.path.join(good, seed_name + ".yaml"), encoding="utf-8"))

    def arm(edit):
        d = tempfile.mkdtemp(prefix="arm_", dir=tmp)
        row = yaml.safe_load(yaml.safe_dump(seed))
        edit(row)
        with open(os.path.join(d, seed_name + ".yaml"), "w", encoding="utf-8", newline="\n") as f:
            yaml.safe_dump(row, f, sort_keys=False)
        m.CATALOG_ENTRIES_DIR = d
        e2, r2 = m.load_catalog_entries()
        return seed_name in r2 and seed_name not in e2

    arms = {
        "contract.label missing": lambda r: r["contract"].pop("label"),
        "contract.id empty": lambda r: r["contract"].__setitem__("id", ""),
        "prefix is an empty string": lambda r: r.__setitem__("prefix", ""),
        "prefix is a number": lambda r: r.__setitem__("prefix", 7),
        "fork_keys has an unknown key": lambda r: r["fork_keys"].__setitem__("zz", {}),
        "fork_keys.firm is a string": lambda r: r["fork_keys"].__setitem__("firm", "x"),
        "retired without a reason": lambda r: r.__setitem__("retired", True),
        "null read_tool without a gap_owner": lambda r: (r.__setitem__("read_tool", None), r.__setitem__("gap_owner", None)),
        "layer outside the seven": lambda r: r.__setitem__("layer", "diamond"),
        "an extra field": lambda r: r.__setitem__("zz_extra", 1),
    }
    refused = 0
    for name, edit in arms.items():
        ok = arm(edit)
        refused += 1 if ok else 0
        if not ok:
            print("  NOT REFUSED: %s" % name)
    print("REFUSE: %d of %d one-defect rows refused" % (refused, len(arms)))
    shutil.rmtree(tmp, ignore_errors=True)
    return loaded == len(exp) and joined == len(exp) and got_old == n_old and not errors and refused == len(arms)


def ac2():
    import yaml
    allc = glib.load_all()
    tmp = tempfile.mkdtemp(prefix="c15ac2_")
    good, reg = build(tmp, allc)
    old, _n = old_rows(tmp)
    m = load_impl(reg)
    fn = getattr(m, "silver_catalog_row", None)
    res = []
    if not fn:
        res.append(("silver_catalog_row exists", False))
    else:
        names = [(cid, g, c) for cid, (g, c) in allc.items() if glib.in_scope(c)]
        cid, g, c = next(x for x in names if x[2]["fork_keys"] and glib.carrier(str((x[2]["fork_keys"].get("firm") or {}).get("column_or_key_segment"))
                                                                                  .replace(" ", "")))
        name = glib.entity(cid)
        shutil.rmtree(os.path.join(tmp, "one"), ignore_errors=True)
        os.makedirs(os.path.join(tmp, "one"))
        shutil.copy(os.path.join(good, name + ".yaml"), os.path.join(tmp, "one", name + ".yaml"))
        m.CATALOG_ENTRIES_DIR = os.path.join(tmp, "one")
        entries, errors = m.load_catalog_entries()
        data = entries.get(name)
        full = full_of(c, g)
        row = fn(name, data) if data else None
        res.append(("the one row loads", data is not None and not errors))
        res.append(("silver_catalog_row emits the joined row (fork_keys restored)", bool(row) and row.get("fork_keys") == full["fork_keys"]))
        res.append(("silver_catalog_row emits key_template, and the restored table, prefix and contract",
                    bool(row) and row.get("key_template") == full["key_template"] and row.get("contract") == full["contract"]
                    and row.get("table") == full["table"] and row.get("prefix") == full["prefix"]))
        res.append(("entity first, every other field of the loaded row present", bool(row) and list(row)[:1] == ["entity"]
                    and all(k in row for k in data if k != "retired_reason" or "retired_reason" in data)))
        # an un-joined row (the registry holds no entry for its id) carries no key_template
        d2 = os.path.join(tmp, "nojoin")
        os.makedirs(d2)
        raw = yaml.safe_load(open(os.path.join(good, name + ".yaml"), encoding="utf-8"))
        raw["contract"]["id"] = "c-000000000000"
        with open(os.path.join(d2, name + ".yaml"), "w", encoding="utf-8", newline="\n") as f:
            yaml.safe_dump(raw, f, sort_keys=False)
        m.CATALOG_ENTRIES_DIR = d2
        e2, _r = m.load_catalog_entries()
        r2 = fn(name, e2[name]) if name in e2 else None
        res.append(("an un-joined row emits no key_template", bool(r2) and "key_template" not in r2))
        with open(os.path.join(old, "schwab_dim_position.yaml"), encoding="utf-8") as f:
            odata = yaml.safe_load(f)
        orow = fn("schwab_dim_position", odata)
        want = ["entity", "business_meaning", "example_questions", "grain", "freshness_field", "firm_scope_rule", "never_sum_rules",
                "producer", "tools", "read_tool"]
        res.append(("an old row emits exactly its old fields", list(orow) == want and all(orow[k] == odata[k] for k in want[1:])))
    for name, ok in res:
        print("CHECK %s: %s" % ("ok " if ok else "FAIL", name))
    print("CHECKS pass %d of %d" % (sum(1 for _n2, ok in res if ok), len(res)))
    shutil.rmtree(tmp, ignore_errors=True)
    return bool(res) and all(ok for _n2, ok in res)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 9
    ok = {"ac1": ac1, "ac2": ac2}[sys.argv[1]]()
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
