"""c12_check.py -- grades MX-c-12's table-grain harvest rows against G1 @ the pin (g1lib.PIN).

  python c12_check.py ac1 [--rows DIR]   prefix set, contract ids, file names, legacy prefix_key (78 of 78)
  python c12_check.py ac2 [--rows DIR]   field fidelity per row, the retire list, the exact key set
  python c12_check.py ac3                the generator under 5 planted deployed-tool sets (read_tool policy), 390 of 390 rows

DIR defaults to workflows/atom_decomposition/catalog_entries. The generator under test is workflows/atom_decomposition/
gen_harvest_rows.py unless C12_GEN names another (the cut-time planted arms use that to prove the check discriminates).
Every denominator is printed beside its verdict. Exit 0 = PASS, 1 = FAIL, 9 = the instrument could not run.
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import g1lib  # noqa: E402

ROOT = os.getcwd()
ROWS_DIR_DEFAULT = os.path.join("workflows", "atom_decomposition", "catalog_entries")
BASE_FIELDS = {"bucket", "business_meaning", "example_questions", "grain", "freshness_field", "firm_scope_rule",
               "never_sum_rules", "producer", "read_tool", "gap_owner"}
NEW_FIELDS = {"table", "layer", "format", "contract", "nl_tags", "retired"}


def resolve_prefix(row):
    if "prefix_key" in row:
        g1lib.use_registry()
        sys.path.insert(0, os.path.join(ROOT, "lib"))
        import opal_naming
        addr = opal_naming.legacy_address(row["prefix_key"])
        return addr[len("s3://"):].partition("/")[2]
    return row.get("prefix")


def load_rows(d):
    import yaml
    import glob
    rows = {}
    for path in sorted(glob.glob(os.path.join(d, "harvest_*.yaml"))):
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        rows[os.path.basename(path)] = data
    return rows


def contract_of(c):
    return {"id": g1lib.enc(c["contract_id"]), "size": c["size"], "keys": c["securities"], "freshness": c["freshness"],
            "partition": c["partition"], "producer": c["producer"]}


def ac1(d, g1):
    rows = load_rows(d)
    errs = []
    prefixes = {}
    for fn, r in rows.items():
        if not isinstance(r, dict):
            errs.append("%s: not a mapping" % fn)
            continue
        p = resolve_prefix(r)
        if p in prefixes:
            errs.append("%s: prefix %s also in %s" % (fn, p, prefixes[p]))
        prefixes[p] = fn
        if fn != "harvest_%s.yaml" % g1lib.slug(p or ""):
            errs.append("%s: file name is not harvest_%s.yaml" % (fn, g1lib.slug(p or "")))
        if p in g1:
            if (r.get("contract") or {}).get("id") != g1lib.enc(g1[p]["contract_id"]):
                errs.append("%s: contract.id %r != %r" % (fn, (r.get("contract") or {}).get("id"), g1lib.enc(g1[p]["contract_id"])))
            lk = g1lib.legacy_key(p)
            if lk and r.get("prefix_key") != lk:
                errs.append("%s: legacy hyphen table must carry prefix_key %s (never a typed literal)" % (fn, lk))
            if not lk and "prefix_key" in r:
                errs.append("%s: prefix_key on a non-legacy table" % fn)
            if ("prefix" in r) == ("prefix_key" in r):
                errs.append("%s: exactly one of prefix / prefix_key" % fn)
    missing = sorted(set(g1) - set(prefixes))
    extra = sorted(set(prefixes) - set(g1))
    ids_ok = sum(1 for p, fn in prefixes.items() if p in g1 and (rows[fn].get("contract") or {}).get("id") == g1lib.enc(g1[p]["contract_id"]))
    print("ROWS files=%d; G1 contracts=%d @%s; prefix set equal=%s (missing %d, extra %d); contract.id match %d of %d; other errors %d"
          % (len(rows), len(g1), g1lib.PIN, "yes" if not missing and not extra else "NO", len(missing), len(extra), ids_ok, len(g1), len(errs)))
    for x in missing[:5]:
        print("  missing: %s" % x)
    for x in extra[:5]:
        print("  extra: %s" % x)
    for e in errs[:8]:
        print("  " + e)
    return not missing and not extra and ids_ok == len(g1) and not errs and len(rows) == len(g1)


def ac2(d, g1):
    rows = load_rows(d)
    base = {}
    for _fn, r in load_rows(g1lib.base_rows_dir()).items():
        base[resolve_prefix(r)] = r
    by_prefix = {}
    for fn, r in rows.items():
        if isinstance(r, dict):
            by_prefix[resolve_prefix(r)] = (fn, r)
    fails = {}

    def bad(field, fn, why):
        fails.setdefault(field, []).append("%s: %s" % (fn, why))

    graded = 0
    retired_set = set()
    for p, c in g1.items():
        if p not in by_prefix:
            bad("row", p, "no row")
            continue
        fn, r = by_prefix[p]
        graded += 1
        want_keys = set(BASE_FIELDS) | set(NEW_FIELDS) | ({"prefix_key"} if g1lib.legacy_key(p) else {"prefix"})
        if r.get("retired") is True:
            want_keys.add("retired_reason")
            retired_set.add(p)
        if set(r) != want_keys:
            bad("keys", fn, "key set differs: extra %s missing %s" % (sorted(set(r) - want_keys), sorted(want_keys - set(r))))
        if r.get("bucket") != c["bucket"]:
            bad("bucket", fn, repr(r.get("bucket")))
        for f in ("table", "layer", "format", "grain"):
            if r.get(f) != c[f]:
                bad(f, fn, "%r != G1 %r" % (r.get(f), c[f]))
        if r.get("contract") != contract_of(c):
            bad("contract", fn, "differs from G1 size/securities/freshness/partition/producer or id")
        if r.get("nl_tags") != c["nl_tags"]:
            bad("nl_tags", fn, "%r != %r" % (r.get("nl_tags"), c["nl_tags"]))
        eq = r.get("example_questions")
        old = base.get(p) or {}
        if not (isinstance(eq, list) and eq and all(isinstance(x, str) and x.strip() for x in eq)):
            bad("example_questions", fn, "empty")
        else:
            lost = [q for q in c["common_queries"] + list(old.get("example_questions") or []) if q not in eq]
            if lost:
                bad("example_questions", fn, "lost %d question(s) (every G1 common_query and every round-12 question stays): %r" % (len(lost), lost[0][:60]))
        ns = r.get("never_sum_rules")
        old_ns = old.get("never_sum_rules") if isinstance(old.get("never_sum_rules"), list) else []
        want_ns = list(c["never_sum_rules"]) + [x for x in old_ns if x not in c["never_sum_rules"]]
        if want_ns:
            if not (isinstance(ns, list) and all(x in ns for x in want_ns)):
                bad("never_sum_rules", fn, "lost a G1 or round-12 never-sum rule")
        elif not (isinstance(ns, str) and ns.startswith("NONE")):
            bad("never_sum_rules", fn, "G1 and round 12 state none: want a 'NONE -- <reason>' string, got %r" % (ns,))
        if old.get("business_meaning") and r.get("business_meaning") != old["business_meaning"]:
            bad("business_meaning", fn, "a round-12 business_meaning is kept verbatim where the row existed")
        ff = r.get("freshness_field")
        cols = [x.get("name") for x in c.get("columns") or [] if isinstance(x, dict)]
        if isinstance(ff, str) and ff.startswith("FIELD:"):
            if ff[len("FIELD:"):].strip() not in cols:
                bad("freshness_field", fn, "%r names no G1 column" % ff)
        elif not (isinstance(ff, str) and ff.startswith("NONE") and c["freshness"]["derived_from"] in ff):
            bad("freshness_field", fn, "want FIELD:<G1 column> or 'NONE -- ' carrying G1's derived_from; got %r" % (ff,))
        pr = r.get("producer")
        pn, pc = c["producer"].get("name"), c["producer"].get("claim")
        low = pr.lower() if isinstance(pr, str) else ""
        if not (isinstance(pr, str) and pr.strip()):
            bad("producer", fn, "empty")
        elif pn and pn not in pr:
            bad("producer", fn, "does not carry G1's producer name")
        elif pc == "inferred" and "inferred" not in low:
            bad("producer", fn, "G1 claim inferred but the text does not say so")
        elif pc == "absent" and not ("not traced" in low or "absent" in low):
            bad("producer", fn, "G1 claim absent but the text does not say so")
        bm = r.get("business_meaning")
        if not (isinstance(bm, str) and len(bm.strip()) >= 40 and not bm.startswith("NONE")):
            bad("business_meaning", fn, "empty, under 40 chars or NONE")
        if r.get("firm_scope_rule") != "opal-internal-only":
            bad("firm_scope_rule", fn, repr(r.get("firm_scope_rule")))
        rt, go = r.get("read_tool"), r.get("gap_owner")
        if rt is None and not (isinstance(go, str) and go.strip()):
            bad("read_tool", fn, "null read_tool needs a gap_owner")
        if rt is not None and go is not None:
            bad("read_tool", fn, "gap_owner must be null when read_tool is named")
        if not isinstance(r.get("retired"), bool):
            bad("retired", fn, "not a bool")
        if r.get("retired") is True and not (isinstance(r.get("retired_reason"), str) and r["retired_reason"].strip()):
            bad("retired", fn, "retired true without retired_reason")
    want_ret = set(g1lib.RETIRE_REQUIRED)
    cond = g1lib.RETIRE_CONDITIONAL
    extra_ret = retired_set - want_ret
    if want_ret - retired_set:
        bad("retire_list", "set", "not retired: %s" % sorted(want_ret - retired_set))
    if extra_ret - {cond}:
        bad("retire_list", "set", "retired but not on the list: %s" % sorted(extra_ret - {cond}))
    if cond in retired_set:
        fn, r = by_prefix[cond]
        m = r.get("retired_reason", "")
        ev = [w for w in m.replace(",", " ").split() if w.endswith(".md") or w.endswith(".json") or w.endswith(".txt")]
        if not any(os.path.exists(w.strip("`'\"()")) for w in ev):
            bad("retire_list", fn, "research-dossier retired without a reason citing an evidence file that exists")
    nfield = sum(len(v) for v in fails.values())
    print("ROWS graded %d of %d; failing fields: %s"
          % (graded, len(g1), ", ".join("%s x%d" % (k, len(v)) for k, v in sorted(fails.items())) or "none"))
    print("RETIRED set = %s" % sorted(retired_set))
    for k, v in sorted(fails.items()):
        for x in v[:2]:
            print("  [%s] %s" % (k, x))
    return graded == len(g1) and nfield == 0


def ac3(g1, text):
    gen = os.environ.get("C12_GEN") or os.path.join("workflows", "atom_decomposition", "gen_harvest_rows.py")
    if not os.path.exists(gen):
        print("GENERATOR absent: %s" % gen)
        return False
    typed = sorted({p["name"] for c in g1.values() for p in c.get("proposed_tools") or []})
    arms = {
        "D0 nothing deployed": [],
        "D1 raw tools only": ["harvest_list", "harvest_read"],
        "D2 raw + all typed": ["harvest_list", "harvest_read"] + typed,
        "D3 typed only (harvest_read not deployed)": typed,
        "D4 D2 minus harvest_get_fundamentals": [t for t in ["harvest_list", "harvest_read"] + typed if t != "harvest_get_fundamentals"],
    }
    tmp = tempfile.mkdtemp(prefix="c12ac3_")
    g1f = os.path.join(tmp, "G1_pinned.md")
    with open(g1f, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    ok_arms, rows_ok, rows_all = 0, 0, 0
    for name, deployed in arms.items():
        out = os.path.join(tmp, name.split()[0])
        dep = os.path.join(tmp, name.split()[0] + ".json")
        with open(dep, "w", encoding="utf-8") as f:
            json.dump(deployed, f)
        r = subprocess.run([sys.executable, gen, "--g1", g1f, "--out", out, "--deployed-tools", dep,
                            "--existing", ROWS_DIR_DEFAULT], capture_output=True, timeout=100)
        if r.returncode != 0:
            print("ARM %s: generator rc=%d: %s" % (name, r.returncode, (r.stderr or r.stdout).decode("utf-8", "replace")[-200:].strip()))
            rows_all += len(g1)
            continue
        rows = load_rows(out)
        by_prefix = {resolve_prefix(x): x for x in rows.values() if isinstance(x, dict)}
        bad = 0
        for p, c in g1.items():
            rows_all += 1
            x = by_prefix.get(p)
            want = g1lib.expected_read_tool(c, set(deployed))
            if x is None or x.get("read_tool") != want or (want is None and x.get("gap_owner") != "NFRA_OPLGTW") \
                    or (want is not None and x.get("gap_owner") is not None):
                bad += 1
                if bad <= 2:
                    print("  [%s] %s: read_tool %r gap_owner %r, want %r" % (name, p, x and x.get("read_tool"), x and x.get("gap_owner"), want))
            else:
                rows_ok += 1
        if len(rows) == len(g1) and bad == 0:
            ok_arms += 1
        print("ARM %s: files %d, rows wrong %d" % (name, len(rows), bad))
    print("ARMS pass %d of %d; rows graded right %d of %d" % (ok_arms, len(arms), rows_ok, rows_all))
    return ok_arms == len(arms) and rows_ok == rows_all


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 9
    mode = sys.argv[1]
    d = ROWS_DIR_DEFAULT
    if "--rows" in sys.argv:
        d = sys.argv[sys.argv.index("--rows") + 1]
    g1, _registry, text = g1lib.load_g1()
    ok = {"ac1": lambda: ac1(d, g1), "ac2": lambda: ac2(d, g1), "ac3": lambda: ac3(g1, text)}[mode]()
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
