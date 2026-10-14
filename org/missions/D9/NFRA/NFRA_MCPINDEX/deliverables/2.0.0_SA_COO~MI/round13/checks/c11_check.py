"""c11_check.py -- grades MX-c-11 (the emitter's loader and validator, the tool index, the version) for the table-grain harvest rows.

  python c11_check.py ac1   the harvest loader accepts a CORRECT 78-row set and refuses 11 one-defect rows
  python c11_check.py ac2   tool_index: pending members apply only when the census lists the tool; a harvest row names only a served tool
  python c11_check.py ac3   the emitter's header is v0.5 and carries Andrew's verbatim and the record path

The implementation under test is workflows/atom_decomposition/emit_catalog_v02.py unless C11_IMPL names another module file
(the cut-time planted arms use that to prove the check discriminates). Exit 0 PASS, 1 FAIL, 9 the instrument could not run.
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import g1lib  # noqa: E402

IMPL = os.environ.get("C11_IMPL") or os.path.join("workflows", "atom_decomposition", "emit_catalog_v02.py")
RECORD = "org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261014_124xZ_GATEWAY_DATA_CONTRACTS_CENSUS_CRO_FANOUT.md"
VERBATIM = ("We need to colonize that bucket. We need to figure out all the gold and silver tables that are in that bucket and where "
            "we want to create tools because the asset managers need to be able to do direct research right to the bucket.")


def load_impl():
    spec = importlib.util.spec_from_file_location("c11_impl", IMPL)
    m = importlib.util.module_from_spec(spec)
    sys.modules["c11_impl"] = m
    spec.loader.exec_module(m)
    g1lib.use_registry()
    return m


def good_rows(tmp):
    """The reference 78-row set (plant_gen.py, nothing deployed) written to tmp/good."""
    gen = os.path.join(HERE, "plant_gen.py")
    g1f = os.path.join(tmp, "g1.md")
    with open(g1f, "w", encoding="utf-8", newline="") as f:
        f.write(g1lib.g1_text())
    dep = os.path.join(tmp, "none.json")
    with open(dep, "w") as f:
        f.write("[]")
    out = os.path.join(tmp, "good")
    r = subprocess.run([sys.executable, gen, "--g1", g1f, "--out", out, "--deployed-tools", dep], capture_output=True)
    if r.returncode != 0:
        print("ERROR: reference rows: %s" % r.stderr.decode("utf-8", "replace")[-200:])
        sys.exit(9)
    return out


def ac1():
    import yaml
    m = load_impl()
    tmp = tempfile.mkdtemp(prefix="c11ac1_")
    good = good_rows(tmp)
    m.CATALOG_ENTRIES_DIR = good
    rows, errors = m.load_harvest_entries()
    acc = len(rows)
    print("ACCEPT: %d of 78 correct table-grain rows load (errors %d)" % (acc, len(errors)))
    for k in sorted(errors)[:3]:
        print("  %s: %s" % (k, str(errors[k])[:170]))
    base = "harvest_bloomberg_harvest_silver_article"
    with open(os.path.join(good, base + ".yaml"), encoding="utf-8") as f:
        seed = yaml.safe_load(f)

    def arm(fname_stem, edit):
        d = os.path.join(tmp, "arm_" + fname_stem)
        os.makedirs(d, exist_ok=True)
        row = yaml.safe_load(yaml.safe_dump(seed))
        s_ = edit(row)
        stem = s_ if (isinstance(s_, str) and s_.startswith("harvest_")) else base
        with open(os.path.join(d, stem + ".yaml"), "w", encoding="utf-8", newline="\n") as f:
            yaml.safe_dump(row, f, sort_keys=False)
        m.CATALOG_ENTRIES_DIR = d
        r2, e2 = m.load_harvest_entries()
        return stem in e2 and stem not in r2

    def e_prefix(r):
        r["prefix"] = "zzz/harvest/silver/article/"
        return "harvest_zzz_harvest_silver_article"

    def e_gold_root(r):
        r["prefix"] = "amgt/harvest/gold/"
        return "harvest_amgt_harvest_gold"

    def e_oldshape(r):
        for k in ("table", "layer", "format", "contract", "nl_tags", "retired"):
            r.pop(k, None)

    def e_wrongname(r):
        return "harvest_wrong_name"

    arms = {
        "unknown top-level prefix": e_prefix,
        "whole gold root rowed": e_gold_root,
        "contract missing": lambda r: r.pop("contract"),
        "contract.id missing": lambda r: r["contract"].pop("id"),
        "retired is a string": lambda r: r.__setitem__("retired", "no"),
        "size.claim outside the enum": lambda r: r["contract"]["size"].__setitem__("claim", "guess"),
        "retired without a reason": lambda r: r.__setitem__("retired", True),
        "file name is not the slug": e_wrongname,
        "old 11-field shape": e_oldshape,
        "an extra field": lambda r: r.__setitem__("zz_extra", 1),
        "layer outside gold/silver/bronze/state": lambda r: r.__setitem__("layer", "platinum"),
    }
    refused = 0
    for name, edit in arms.items():
        ok = arm(name.split()[0] + str(len(name)), edit)
        refused += 1 if ok else 0
        if not ok:
            print("  NOT REFUSED: %s" % name)
    print("REFUSE: %d of %d one-defect rows refused" % (refused, len(arms)))
    shutil.rmtree(tmp, ignore_errors=True)
    return acc == 78 and not errors and refused == len(arms)


def ac2():
    import yaml
    m = load_impl()
    tdir = m.TOOL_INDEX_DIR
    with open(os.path.join(tdir, "members.yaml"), encoding="utf-8") as f:
        members = (yaml.safe_load(f) or {}).get("members") or []
    base_tools = [x["tool"] for x in members]
    row_ids = set()
    for x in members:
        if x.get("member") == "a":
            row_ids.add(x.get("index"))
            row_ids.update(x.get("links") or [])

    def census(tools):
        return {"deployed_commit": "0" * 40, "tools": [{"tool": t, "definition": "planted"} for t in tools]}

    # row_keys is {} here (the emitter passes the live channel keys), so the BASE census carries basis errors that are not under
    # test: every arm is graded on the errors it ADDS to the base census's.
    e0 = set(m.load_tool_index(row_ids, census=census(base_tools), row_keys={})[1])

    def run(tools):
        o, e, c = m.load_tool_index(row_ids, census=census(tools), row_keys={})
        return o, [x for x in e if x not in e0], c

    res = []
    out, errs, _c = run(base_tools)
    names = {e["tool"] for e in out}
    res.append(("A base census: no error, no harvest tool listed", not errs and "harvest_list" not in names and "harvest_read" not in names))
    out, errs, _c = run(base_tools + ["harvest_list", "harvest_read"])
    d = {e["tool"]: e for e in out}
    res.append(("B both served: listed as member b with an owner",
                not errs and all(t in d and d[t].get("member") == "b" and str(d[t].get("owner") or "").strip() for t in ("harvest_list", "harvest_read"))))
    out, errs, _c = run(base_tools + ["harvest_list"])
    names = {e["tool"] for e in out}
    res.append(("C only harvest_list served: harvest_read stays out", not errs and "harvest_list" in names and "harvest_read" not in names))
    out, errs, _c = run(base_tools + ["zz_new_tool"])
    res.append(("D an unclassified served tool still refuses", any("zz_new_tool" in e and "no entry" in e for e in errs)))
    out, errs, _c = run([t for t in base_tools if t != base_tools[0]])
    res.append(("E a members entry for an unserved tool still refuses", any(base_tools[0] in e and "does not serve" in e for e in errs)))
    fn = getattr(m, "harvest_read_tool_errors", None)
    rows = {"harvest_x": {"read_tool": "harvest_read"}, "harvest_y": {"read_tool": None}}
    ok_f = bool(fn) and fn(rows, {"harvest_read"}) == [] and bool(fn(rows, {"something_else"})) \
        and any("harvest_x" in e for e in fn(rows, {"something_else"})) and not any("harvest_y" in e for e in fn(rows, {"something_else"}))
    res.append(("F harvest_read_tool_errors(rows, served): a named tool must be served, null is fine", ok_f))
    for name, ok in res:
        print("ARM %s: %s" % ("ok " if ok else "FAIL", name))
    print("ARMS pass %d of %d" % (sum(1 for _n, ok in res if ok), len(res)))
    return all(ok for _n, ok in res)


def ac3():
    src = open(IMPL, encoding="utf-8").read()
    rec = open(RECORD, encoding="utf-8").read() if os.path.exists(RECORD) else ""
    lines = src.splitlines()
    v05 = [ln for ln in lines if ln.strip().startswith("version: 0.5") or "version: 0.5\\n" in ln]
    v04 = [ln for ln in lines if ln.strip().startswith("version: 0.4") or "version: 0.4\\n" in ln]
    sup = [ln for ln in lines if "supersedes: v0.4" in ln]
    res = [("record file holds the verbatim (control)", VERBATIM in rec),
           ("emitter source writes version: 0.5", len(v05) >= 1),
           ("emitter source no longer writes version: 0.4", len(v04) == 0),
           ("emitter source says supersedes: v0.4", len(sup) >= 1),
           ("emitter source carries Andrew's verbatim exactly", VERBATIM in src.replace("\\\n", "").replace("\n# ", " ").replace("\n#", " ")
            or VERBATIM in src),
           ("emitter source cites the record path", os.path.basename(RECORD) in src)]
    for name, ok in res:
        print("CHECK %s: %s" % ("ok " if ok else "FAIL", name))
    print("CHECKS pass %d of %d" % (sum(1 for _n, ok in res if ok), len(res)))
    return all(ok for _n, ok in res)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 9
    ok = {"ac1": ac1, "ac2": ac2, "ac3": ac3}[sys.argv[1]]()
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
