"""l1_check.py <id>: the round-28 (workstream GATEWAY) criteria of cell MX-l-1, run from the repository (or worktree) root.
Ids: l1.AC1 (the `size` mapping on a fixture catalog and a hand-made census, in-process), l1.AC2 (the option's guards and the regression: no option
changes nothing, the existing options still refuse, bad censuses are refused, validate_size refuses planted defects), l1.AC3 (pytest: the new test
file plus the five existing atom_decomposition files). Prints a DENOMINATOR line, one line per arm, then RESULT: PASS|FAIL.
ASCII only; python 3.9. L1_ROOT (default: the current directory) names the root that holds workflows/atom_decomposition.
The contract is decompositions/NFRA_MCPINDEX_DECOMP.round28-GATEWAY.md R28.3 (L1) as AMENDED by the order's section 1 (the order wins)."""
import contextlib
import copy
import importlib.util
import inspect
import io
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
R28 = os.path.normpath(os.path.join(HERE, ".."))
FIX = os.path.join(R28, "fixtures")
ROOT = os.environ.get("L1_ROOT") or os.getcwd()
AD = os.path.join(ROOT, "workflows", "atom_decomposition")
EMIT_PY = os.path.join(AD, "emit_catalog_v02.py")
NEW_TEST = os.path.join(AD, "tests", "test_size_class.py")
OLD_TESTS = ["tests/test_group_links.py", "tests/test_c_group.py", "tests/test_tool_index_and_harvest.py", "tests/test_depth_kinds.py",
             "tests/test_serves_map.py"]
BASELINE_PASSED = 88   # the five existing files at the round-28 base; the new file adds at least 8
NEW_MIN = 8
NAMES = ("size_class", "validate_size", "load_size_census", "attach_size", "size_header_line", "apply_size_census",
         "SIZE_CENSUS_SCHEMA", "SIZE_LARGE_BYTES", "SIZE_VERY_LARGE_BYTES", "SIZE_VERY_LARGE_ROWS")
OK, BAD = [], []


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def fx(name):
    return os.path.join(FIX, name)


def jload(p):
    with open(p, encoding="utf-8", errors="replace") as fh:
        return json.load(fh)


def load_emitter():
    if not os.path.isfile(EMIT_PY):
        raise RuntimeError("emitter absent: %s" % EMIT_PY)
    sys.path.insert(0, AD)
    spec = importlib.util.spec_from_file_location("emit_catalog_v02_l1_under_test", EMIT_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_json(tmp, name, doc):
    p = os.path.join(tmp, name)
    with open(p, "w", encoding="ascii") as fh:
        json.dump(doc, fh)
    return p


def interface(emit):
    missing = [n for n in NAMES if not hasattr(emit, n)]
    arm("the emitter defines the interface (%s)" % ", ".join(NAMES), not missing, "missing: %s" % ", ".join(missing))
    return not missing


def ac1(tmp):
    rows_doc, census_doc, expected = jload(fx("l1_rows.json")), jload(fx("l1_census.json")), jload(fx("l1_expected.json"))
    n_rows = sum(len(v) for v in rows_doc.values())
    print("DENOMINATOR: fixture l1 -- %d rows in 3 sections, a census of %d entries and %d skipped item(s) (two entities share one location, one "
          "entry has an error, one row is absent from the census); 7 class-edge values; %d expected size mappings"
          % (n_rows, len(census_doc["entries"]), len(census_doc["skipped"]), len(expected["size_by_entity"])))
    emit = load_emitter()
    if not interface(emit):
        return
    c = emit.size_class
    arm("the class edges: 8388607 small, 8388608 large, 25165823 large, 25165824 very large",
        [c(8388607, 5), c(8388608, 5), c(25165823, 5), c(25165824, 5)] == ["small", "large", "large", "very large"])
    arm("the row edges: 999999 rows small, 1000000 rows very large, 0 bytes and no rows small",
        [c(100, 999999), c(100, 1000000), c(0, None)] == ["small", "very large", "small"])
    path = write_json(tmp, "census.json", census_doc)
    census, errs = emit.load_size_census(path)
    arm("the fixture census loads with no error", not errs and bool(census), "errors: %r" % errs[:3])
    rows = copy.deepcopy(rows_doc)
    aerrs = emit.attach_size(rows, census)
    arm("attaching the census to the fixture rows reports no error", not aerrs, "errors: %r" % aerrs[:3])
    got = dict((r["entity"], r.get("size")) for sec in rows.values() for r in sec)
    want = expected["size_by_entity"]
    bad = [e for e in want if got.get(e) != want[e]]
    arm("every one of the %d rows takes exactly its expected size mapping" % len(want), not bad and set(got) == set(want), "differs: %r" % bad[:4])
    badk = [e for e in want if isinstance(got.get(e), dict) and list(got[e]) != list(want[e])]
    arm("the mapping keys come in the contract order", not badk and bool(got), "order differs: %r" % badk[:3])
    arm("measured rows: l1_rows_small is small at 999999 rows and l1_rows_vlarge very large at 1000000",
        got.get("l1_rows_small", {}).get("class") == "small" and got.get("l1_rows_vlarge", {}).get("class") == "very large")
    arm("the unmeasured reasons: a skipped item, an errored entry and a row absent from the census",
        [got.get(e, {}).get("reason") for e in ("l1_skipped", "l1_errored", "l1_missing")] == ["store_or_non_s3", "timeout", "not in the census"])
    arm("the two entities that share a location each take their own entry",
        got.get("l1_shared_a") == want["l1_shared_a"] and got.get("l1_shared_b") == want["l1_shared_b"])
    last_ok = all(list(r)[-1] == "size" and dict((k, v) for k, v in r.items() if k != "size") == o
                  for sec in rows for r, o in zip(rows[sec], rows_doc[sec]))
    arm("size is the last key of every row and every other field is untouched", last_ok)
    arm("the header line is exactly the contract text", emit.size_header_line(census) == expected["header_line"],
        "got %r" % emit.size_header_line(census))
    rows2 = copy.deepcopy(rows_doc)
    hdr, herrs = emit.apply_size_census(path, rows2)
    arm("apply_size_census returns the header line and no error, and rows equal the direct attach", hdr == expected["header_line"] and not herrs and rows2 == rows,
        "hdr=%r errs=%r" % (hdr, herrs[:2]))
    import yaml
    row = [r for r in rows["silver_datasets"] if r["entity"] == "l1_edge_vlarge"][0]
    dumped = yaml.safe_dump([row], default_flow_style=False, sort_keys=False, width=1000000)
    back = yaml.safe_load(dumped)[0]["size"]
    arm("the YAML of a row is ASCII, holds `class: very large` and loads back to the same mapping (measured_at stays a string)",
        all(ord(ch) < 128 for ch in dumped) and "class: very large" in dumped and back == row["size"] and isinstance(back["measured_at"], str))
    arm("validate_size accepts every attached mapping", all(not emit.validate_size(e, m) for e, m in got.items()),
        "refused: %r" % [e for e, m in got.items() if emit.validate_size(e, m)][:3])


def ac2(tmp):
    rows_doc, census_doc, expected = jload(fx("l1_rows.json")), jload(fx("l1_census.json")), jload(fx("l1_expected.json"))
    print("DENOMINATOR: controls (the existing options still refuse and are still listed), no-option regression, %d census/attach refusals planted from the "
          "fixture census, %d validate_size defects planted from an attached mapping, determinism over 2 runs, the CLI wiring read from main's source" % (7, 7))
    emit = load_emitter()
    # controls that must hold at the base too
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        rc = emit.main(["--serves-map", os.path.join(tmp, "absent_serves.json")])
    arm("control: a missing --serves-map file still exits 2 with its own refusal", rc == 2 and "EMIT REFUSED (serves map)" in buf.getvalue())
    helptxt = io.StringIO()
    try:
        with contextlib.redirect_stdout(helptxt):
            emit.main(["--help"])
    except SystemExit:
        pass
    arm("control: --help still lists --group-map, --link-groups and --serves-map",
        all(o in helptxt.getvalue() for o in ("--group-map", "--link-groups", "--serves-map")))
    arm("--help lists --size-census", "--size-census" in helptxt.getvalue())
    if not interface(emit):
        return
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        rc = emit.main(["--size-census", os.path.join(tmp, "absent_size.json")])
    arm("a missing --size-census file exits 2 with `EMIT REFUSED (size census)` before anything is written", rc == 2 and "EMIT REFUSED (size census)" in buf.getvalue(),
        "rc=%r out=%r" % (rc, buf.getvalue()[:100]))
    rows = copy.deepcopy(rows_doc)
    arm("no option: apply_size_census(None, rows) returns an empty header and no error and leaves every row unchanged",
        emit.apply_size_census(None, rows) == ("", []) and rows == rows_doc)
    # load refusals, planted from the present fixture census
    def bad_load(mut, label):
        doc = copy.deepcopy(census_doc)
        mut(doc)
        census, errs = emit.load_size_census(write_json(tmp, "m_%s.json" % re.sub(r"\W", "_", label), doc))
        arm("planted census refused: %s" % label, bool(errs))
    bad_load(lambda d: d.update(schema="size_census/2"), "another schema")
    bad_load(lambda d: d.update(entries={}), "entries not a list")
    bad_load(lambda d: d["entries"].append(copy.deepcopy(d["entries"][0])), "an entity with two entries")
    bad_load(lambda d: d["skipped"].append(copy.deepcopy(d["skipped"][0])), "an entity skipped twice")
    bad_load(lambda d: d["skipped"].append({"entity": d["entries"][0]["entity"], "section": "silver_datasets", "reason": "x"}), "an entity measured and skipped")
    bad_load(lambda d: d.update(read_at="2026-10-21"), "read_at without a time")
    notjson = os.path.join(tmp, "not.json")
    with open(notjson, "w") as fh:
        fh.write("this is not json")
    arm("planted census refused: a file that is not JSON", bool(emit.load_size_census(notjson)[1]))
    # attach refusals
    def bad_attach(mut, label):
        doc = copy.deepcopy(census_doc)
        mut(doc)
        census, errs = emit.load_size_census(write_json(tmp, "a_%s.json" % re.sub(r"\W", "_", label), doc))
        errs = list(errs) + (emit.attach_size(copy.deepcopy(rows_doc), census) if census else [])
        arm("planted census refused at attach: %s" % label, bool(errs))
    def set_prefix(d):
        [e for e in d["entries"] if e["entity"] == "l1_small"][0]["prefix"] = "somewhere/else/"
    def drop_bytes(d):
        e = [e for e in d["entries"] if e["entity"] == "l1_small"][0]
        e["bytes_newest"], e["bytes_uncompressed_newest"] = None, None
    bad_attach(set_prefix, "an entry whose location differs from the row's")
    bad_attach(drop_bytes, "an entry with no byte count")
    noent = copy.deepcopy(rows_doc)
    del noent["silver_datasets"][0]["entity"]
    census, _ = emit.load_size_census(write_json(tmp, "ok.json", census_doc))
    arm("planted rows refused at attach: a row without an entity", bool(emit.attach_size(noent, census)))
    # determinism
    a, b = copy.deepcopy(rows_doc), copy.deepcopy(rows_doc)
    emit.apply_size_census(os.path.join(tmp, "ok.json"), a)
    emit.apply_size_census(os.path.join(tmp, "ok.json"), b)
    arm("determinism: two runs give identical rows (same keys, same order)", json.dumps(a) == json.dumps(b) and json.dumps(a) != json.dumps(rows_doc))
    # validate_size defects planted from an attached mapping
    good = copy.deepcopy(expected["size_by_entity"]["l1_edge_large"])
    arm("validate_size accepts the measured and the absent forms", not emit.validate_size("t", good) and not emit.validate_size("t", expected["size_by_entity"]["l1_missing"]))
    def mut(k, v):
        m = copy.deepcopy(good)
        m[k] = v
        return m
    nomt = copy.deepcopy(good)
    del nomt["measured_at"]
    reorder = dict(reversed(list(good.items())))
    extra = dict(good, note="x")
    cases = [("a class outside the four", mut("class", "huge")), ("a measured size without measured_at", nomt),
             ("measured_at as a full stamp", mut("measured_at", "2026-10-21T15:07:20Z")), ("a class that does not follow the thresholds", mut("class", "small")),
             ("keys in another order", reorder), ("an extra key", extra),
             ("an absent size without a reason", {"class": "unmeasured", "claim": "absent", "reason": "  "})]
    for label, m in cases:
        arm("planted size refused by validate_size: %s" % label, bool(emit.validate_size("t", m)))
    src = inspect.getsource(emit.main)
    arm("main wires the option: it adds --size-census, calls apply_size_census and refuses on its errors", "--size-census" in src and "apply_size_census(" in src and "size_errors" in src)


def ac3(tmp):
    if not os.path.isfile(NEW_TEST):
        print("DENOMINATOR: test file %s absent" % NEW_TEST)
        arm("pytest on the new test file and the five existing atom_decomposition files passes with at least %d tests" % (BASELINE_PASSED + NEW_MIN), False, "file absent")
        return
    env = dict(os.environ)
    env["PYTHONPATH"] = AD
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", "tests/test_size_class.py"] + OLD_TESTS,
                       cwd=AD, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
    out = p.stdout.decode("utf-8", "replace").replace("\r", "")
    m = re.search(r"(\d+) passed", out)
    n = int(m.group(1)) if m else 0
    need = BASELINE_PASSED + NEW_MIN
    print("DENOMINATOR: pytest rc=%d passed=%d (minimum %d = %d existing + %d new) files=6 in %s" % (p.returncode, n, need, BASELINE_PASSED, NEW_MIN, AD))
    arm("pytest on tests/test_size_class.py and the five existing files passes with at least %d tests" % need, p.returncode == 0 and n >= need,
        "rc=%d passed=%d" % (p.returncode, n))


IDS = {"l1.AC1": ac1, "l1.AC2": ac2, "l1.AC3": ac3}


def main(argv):
    if len(argv) < 2 or argv[1] not in IDS:
        print("usage: l1_check.py %s" % "|".join(sorted(IDS)))
        print("RESULT: FAIL")
        return 2
    with tempfile.TemporaryDirectory() as tmp:
        try:
            IDS[argv[1]](tmp)
        except Exception as exc:  # noqa: BLE001
            arm("the check ran to its end", False, "%s: %s" % (type(exc).__name__, exc))
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if not BAD else "FAIL"))
    return 0 if not BAD else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
