"""c13_check.py -- grades MX-c-13: the catalog writer's loader, validator and row writer for TABLE-grain silver rows.

  python c13_check.py ac1   load_catalog_entries accepts 161 correct table rows and the existing rows unchanged, and refuses 12 one-defect rows
  python c13_check.py ac3   silver_catalog_row(name, data) emits every table field for a table row and nothing new for an old row;
                            the header records the opal-data-mdpf mirror

The implementation under test is workflows/atom_decomposition/emit_catalog_v02.py unless C13_IMPL names another module file (the
cut-time planted arms use that to prove the check discriminates). Exit 0 PASS, 1 FAIL, 9 the instrument could not run.
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

IMPL = os.environ.get("C13_IMPL") or os.path.join("workflows", "atom_decomposition", "emit_catalog_v02.py")
TABLE_FIELDS = ("bucket", "prefix", "table", "layer", "format", "contract", "fork_keys", "nl_tags", "retired", "open_items", "gap_owner")
SEED = "opal_data_assets_silver_49f_dim_account_xref"


def load_impl():
    spec = importlib.util.spec_from_file_location("c13_impl", IMPL)
    m = importlib.util.module_from_spec(spec)
    sys.modules["c13_impl"] = m
    spec.loader.exec_module(m)
    return m


def good_rows(tmp):
    """The reference 161 rows (plant_gen14.py, nothing deployed) in tmp/good."""
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
    r = subprocess.run([sys.executable, os.path.join(HERE, "plant_gen14.py"), "--g2", files["G2"], "--g4", files["G4"], "--g5", files["G5"], "--g6",
                        files["G6"], "--out", out, "--deployed-tools", dep], capture_output=True)
    if r.returncode != 0:
        print("ERROR: reference rows: %s" % r.stderr.decode("utf-8", "replace")[-200:])
        sys.exit(9)
    return out


def old_rows(tmp):
    """The existing non-harvest, non-need source rows at the base pin (silver and portal): they must keep loading."""
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


def ac1():
    import yaml
    m = load_impl()
    tmp = tempfile.mkdtemp(prefix="c13ac1_")
    good = good_rows(tmp)
    old, n_old = old_rows(tmp)
    mix = os.path.join(tmp, "mix")
    shutil.copytree(good, mix)
    for fn in os.listdir(old):
        shutil.copy(os.path.join(old, fn), os.path.join(mix, fn))
    m.CATALOG_ENTRIES_DIR = mix
    entries, errors = m.load_catalog_entries()
    got_new = sum(1 for n in entries if n in {f[:-5] for f in os.listdir(good)})
    got_old = sum(1 for n in entries if n in {f[:-5] for f in os.listdir(old)})
    print("ACCEPT: %d of %d correct table rows load; existing rows still load %d of %d (errors %d)"
          % (got_new, len(os.listdir(good)), got_old, n_old, len(errors)))
    for k in sorted(errors)[:3]:
        print("  %s: %s" % (k, str(errors[k])[:170]))
    with open(os.path.join(good, SEED + ".yaml"), encoding="utf-8") as f:
        seed = yaml.safe_load(f)

    def arm(edit):
        d = tempfile.mkdtemp(prefix="arm_", dir=tmp)
        row = yaml.safe_load(yaml.safe_dump(seed))
        edit(row)
        with open(os.path.join(d, SEED + ".yaml"), "w", encoding="utf-8", newline="\n") as f:
            yaml.safe_dump(row, f, sort_keys=False)
        m.CATALOG_ENTRIES_DIR = d
        e2, r2 = m.load_catalog_entries()
        return SEED in r2 and SEED not in e2

    arms = {
        "contract.id missing": lambda r: r["contract"].pop("id"),
        "fork_keys lacks platform": lambda r: r["fork_keys"].pop("platform"),
        "fork_keys is a string": lambda r: r.__setitem__("fork_keys", "firm"),
        "layer outside the seven": lambda r: r.__setitem__("layer", "diamond"),
        "retired is a string": lambda r: r.__setitem__("retired", "no"),
        "retired without a reason": lambda r: r.__setitem__("retired", True),
        "null read_tool without a gap_owner": lambda r: (r.__setitem__("read_tool", None), r.__setitem__("gap_owner", None)),
        "read_tool named and gap_owner set": lambda r: (r.__setitem__("read_tool", "client_get_holdings"), r.__setitem__("gap_owner", "NFRA_OPLGTW")),
        "firm_scope_rule outside the three": lambda r: r.__setitem__("firm_scope_rule", "everyone"),
        "an extra field": lambda r: r.__setitem__("zz_extra", 1),
        "tools is a string": lambda r: r.__setitem__("tools", "client_get_holdings"),
        "open_items is a string": lambda r: r.__setitem__("open_items", "none"),
    }
    refused = 0
    for name, edit in arms.items():
        ok = arm(edit)
        refused += 1 if ok else 0
        if not ok:
            print("  NOT REFUSED: %s" % name)
    print("REFUSE: %d of %d one-defect rows refused" % (refused, len(arms)))
    shutil.rmtree(tmp, ignore_errors=True)
    return got_new == glib.EXPECT_ROWS and got_old == n_old and not errors and refused == len(arms)


def ac3():
    import yaml
    m = load_impl()
    tmp = tempfile.mkdtemp(prefix="c13ac3_")
    good = good_rows(tmp)
    old, _n = old_rows(tmp)
    fn = getattr(m, "silver_catalog_row", None)
    res = []
    if not fn:
        res.append(("silver_catalog_row exists", False))
    else:
        with open(os.path.join(good, SEED + ".yaml"), encoding="utf-8") as f:
            data = yaml.safe_load(f)
        row = fn(SEED, data)
        res.append(("a table row keeps entity first", isinstance(row, dict) and list(row)[:1] == ["entity"] and row.get("entity") == SEED))
        res.append(("a table row carries every table field verbatim", all(f in row and row[f] == data[f] for f in TABLE_FIELDS)))
        res.append(("a table row carries the C1 fields and read_tool", all(f in row for f in
                    ("business_meaning", "example_questions", "grain", "freshness_field", "firm_scope_rule", "never_sum_rules",
                     "producer", "tools", "read_tool"))))
        with open(os.path.join(old, "schwab_dim_position.yaml"), encoding="utf-8") as f:
            odata = yaml.safe_load(f)
        orow = fn("schwab_dim_position", odata)
        want = ["entity", "business_meaning", "example_questions", "grain", "freshness_field", "firm_scope_rule", "never_sum_rules",
                "producer", "tools", "read_tool"]
        res.append(("an old row emits exactly its old fields, nothing new", list(orow) == want and all(orow[k] == odata[k] for k in want[1:])))
    src = open(IMPL, encoding="utf-8").read().lower()
    res.append(("the emitter header records that opal-data-mdpf gold is a measured mirror of served platinum (G4, overlap 100%)",
                "opal-data-mdpf" in src and "mirror" in src and "platinum" in src and "overlap" in src))
    for name, ok in res:
        print("CHECK %s: %s" % ("ok " if ok else "FAIL", name))
    print("CHECKS pass %d of %d" % (sum(1 for _n2, ok in res if ok), len(res)))
    shutil.rmtree(tmp, ignore_errors=True)
    return bool(res) and all(ok for _n2, ok in res)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 9
    ok = {"ac1": ac1, "ac3": ac3}[sys.argv[1]]()
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
