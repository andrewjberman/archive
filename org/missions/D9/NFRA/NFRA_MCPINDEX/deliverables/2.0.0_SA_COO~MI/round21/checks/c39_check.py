"""c39_check.py -- grades MX-c-39 (R21-2: two depth kinds, `latest` and `series_start`; every measured history_depth claim is tagged with its kind), from the repo root.

The CTO's round-20 analysis (msg 35237, accepting the CVO's correction): a LATEST-date claim is a floor (a later served value means more data); a SERIES-START claim is a ceiling (an equal or EARLIER served
start passes, a LATER start means a shorter history and FAILS). Round 20's MX-c-28 tagged every measured claim `depth_kind: floor`; this cell replaces the value by the kind. The kind of a claim is DECLARED in
tool_index/members.yaml, on the depth spec (`depth_kind: series_start`; absent means `latest`), matched to a measured claim by its (row, field); nothing is guessed from the field name in the emitter.

  python c39_check.py ac1   tests/test_depth_kinds.py (new, at least 8 tests) with tests/test_depth_floor.py, test_tool_index_and_harvest.py, test_c_group.py and test_serves.py pass
  python c39_check.py ac2   the emitter's own function on the REAL members.yaml and measured.yaml (load_tool_index, an injected census): every measured history_depth claim carries `depth_kind` equal to the
                            kind its member spec declares for its (row, field) (the independent derivation below parses members.yaml), `measured_at` equal to its `read_at`, and no claim carries the old value
                            `floor`; exactly the series-start specs are `series_start` (6 claims at the live blob); freshness, inferred and absent claims carry neither key

The tree is the worktree (or C39_ROOT). Exit 0 PASS, 1 FAIL, 9 no run."""
import os
import subprocess
import sys

import yaml

ROOT = os.environ.get("C39_ROOT") or "."
AD = os.path.join(ROOT, "workflows", "atom_decomposition")
KEYS = ("depth_kind", "measured_at")
KINDS = ("latest", "series_start")
# The independent anchor (the CVO named the case): a field that holds the START of a series. A spec on one of these fields MUST be declared series_start, and nothing else may be.
SERIES_FIELDS = ("total.series_start", "as_of_first")
ANCHOR_SERIES_CLAIMS = 6   # at the live blob b81c48aa3c: as_of_first x3 and total.series_start x3 (three tools each read the aum and aggregate rows)


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok  " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def claims(h):
    if not isinstance(h, dict):
        return []
    return list(h.get("links") or []) if h.get("claim") == "per-link" else [h]


def spec_kinds(node, out):
    """Every dict of members.yaml that names a row AND a field is a depth spec; its kind is its depth_kind (default latest)."""
    if isinstance(node, dict):
        if isinstance(node.get("row"), str) and isinstance(node.get("field"), str):
            out[(node["row"], node["field"])] = node.get("depth_kind", "latest")
        for v in node.values():
            spec_kinds(v, out)
    elif isinstance(node, list):
        for v in node:
            spec_kinds(v, out)


def ac1():
    f = os.path.join(AD, "tests", "test_depth_kinds.py")
    if not os.path.exists(f):
        print("ERROR: %s absent" % f)
        return report([("the new test file exists", False)])
    env = dict(os.environ, PYTHONPATH=os.path.abspath(AD))
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--no-header", "tests/test_depth_kinds.py", "tests/test_depth_floor.py",
                        "tests/test_tool_index_and_harvest.py", "tests/test_c_group.py", "tests/test_serves.py"], cwd=AD, env=env, capture_output=True, text=True, timeout=280)
    tail = [ln for ln in (r.stdout or "").replace("\x1b", "").splitlines() if "passed" in ln or "failed" in ln][-1:]
    print("pytest rc=%d: %s" % (r.returncode, tail[0].strip() if tail else (r.stdout or r.stderr)[-200:]))
    co = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--co", "tests/test_depth_kinds.py"], cwd=AD, env=env, capture_output=True, text=True, timeout=120)
    n_new = sum(1 for ln in (co.stdout or "").splitlines() if "::" in ln)
    print("new tests collected: %d" % n_new)
    return report([("the five test files pass", r.returncode == 0), ("the new file holds at least 8 tests", n_new >= 8)])


def ac2():
    sys.path.insert(0, AD)
    import emit_catalog_v02 as em
    tdir = em.TOOL_INDEX_DIR
    members = (yaml.safe_load(open(os.path.join(tdir, "members.yaml"), encoding="utf-8")) or {}).get("members") or []
    pending = (yaml.safe_load(open(os.path.join(tdir, "pending_members.yaml"), encoding="utf-8")) or {}).get("pending") or []
    measured = (yaml.safe_load(open(os.path.join(tdir, "measured.yaml"), encoding="utf-8")) or {}).get("tools") or {}
    declared = {}
    spec_kinds(members + pending, declared)
    tools = sorted({str(m.get("tool")) for m in members + pending if m.get("tool")})
    row_ids, row_keys = set(), {}
    for m in members + pending:
        for x in [m.get("index")] + list(m.get("links") or []):
            if x:
                row_ids.add(x)
                row_keys[x] = "k"
    for t, v in measured.items():
        for c in claims(v.get("history_depth")) + claims(v.get("freshness")):
            if isinstance(c, dict) and c.get("row"):
                row_ids.add(c["row"])
                row_keys[c["row"]] = "k"
    census = {"deployed_commit": "c39check00", "tools": [{"tool": t, "definition": "d"} for t in tools]}
    entries, errors, _doc = em.load_tool_index(row_ids, census=census, row_keys=row_keys)
    print("DENOMINATOR tool_index entries %d; errors %d%s; member specs naming a (row, field) %d, of them series_start %d"
          % (len(entries), len(errors), (" (first: %s)" % errors[0][:120]) if errors else "", len(declared), sum(1 for k in declared.values() if k == "series_start")))
    res = [("load_tool_index runs on the real members and measured files without error", not errors and len(entries) > 0)]
    n = wrong = floor_left = missing_at = n_series = 0
    other = 0
    for e in entries:
        if e.get("member") != "a":
            continue
        for c in claims(e.get("history_depth")):
            if c.get("claim") == "measured":
                n += 1
                want = declared.get((c.get("row"), c.get("field")), "latest")
                if c.get("depth_kind") != want or want not in KINDS:
                    wrong += 1
                if c.get("depth_kind") == "floor":
                    floor_left += 1
                if not c.get("measured_at") or c.get("measured_at") != c.get("read_at"):
                    missing_at += 1
                n_series += 1 if c.get("depth_kind") == "series_start" else 0
            elif any(k in c for k in KEYS):
                other += 1
        for c in claims(e.get("freshness")):
            if any(k in c for k in KEYS):
                other += 1
    print("DENOMINATOR measured history_depth claims %d; kind differs from its member spec %d; still the old value floor %d; measured_at != read_at %d; series_start claims %d; other claims carrying the keys %d"
          % (n, wrong, floor_left, missing_at, n_series, other))
    res.append(("every measured history_depth claim carries the depth_kind its member spec declares (%d of %d)" % (n - wrong, n), n > 0 and not wrong))
    res.append(("no claim keeps the old value floor; every measured_at equals its read_at", not floor_left and not missing_at))
    res.append(("exactly the series-start specs are series_start in the emitted claims (%d)" % n_series, n_series == sum(1 for e in entries if e.get("member") == "a" for c in claims(e.get("history_depth"))
                                                                                                            if c.get("claim") == "measured" and declared.get((c.get("row"), c.get("field"))) == "series_start") and n_series > 0))
    anchor_ok = all((k[1] in SERIES_FIELDS) == (v == "series_start") for k, v in declared.items())
    res.append(("a member spec is series_start exactly when its field is a series-start field %s (anchor)" % (list(SERIES_FIELDS),), anchor_ok and any(v == "series_start" for v in declared.values())))
    res.append(("the emitted series_start claims number %d at the live blob (anchor), found %d" % (ANCHOR_SERIES_CLAIMS, n_series), n_series == ANCHOR_SERIES_CLAIMS))
    res.append(("no freshness, inferred or absent claim carries either key", not other))
    return report(res)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("ac1", "ac2"):
        print(__doc__)
        return 9
    return {"ac1": ac1, "ac2": ac2}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
