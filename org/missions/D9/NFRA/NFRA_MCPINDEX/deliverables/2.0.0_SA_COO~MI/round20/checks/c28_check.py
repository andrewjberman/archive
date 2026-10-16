"""c28_check.py -- grades MX-c-28 (R20-2: after release a measured depth claim is a FLOOR with its measured_at; the emitter stays strict), from the repo root.

  python c28_check.py ac1   tests/test_depth_floor.py (new, at least 6 tests) with the existing tool-index and claim tests (test_tool_index_and_harvest.py, test_c_group.py, test_serves.py) pass
  python c28_check.py ac2   the emitter's own function: load_tool_index() run on the REAL tool_index/members.yaml and measured.yaml (an injected census listing the members' tools, an injected row-key map):
                            every `measured` claim of every (a) entry's history_depth (and of each per-link element) carries depth_kind == "floor" and measured_at equal to the claim's read_at;
                            no freshness claim carries either key; no `inferred` or `absent` claim carries either key; and with those two keys removed, every history_depth equals the tracked catalog's
                            tool_index entry (the catalog was emitted from the same measured.yaml). Prints the count of measured claims.

The tree is the worktree (or C28_ROOT). Exit 0 PASS, 1 FAIL, 9 no run."""
import os
import subprocess
import sys

import yaml

ROOT = os.environ.get("C28_ROOT") or "."
AD = os.path.join(ROOT, "workflows", "atom_decomposition")
CAT = os.path.join(ROOT, "infra", "aws", "ec2", "opal-gateway", "app", "refs", "DATA_CATALOG.yaml")
KEYS = ("depth_kind", "measured_at")


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


def ac1():
    f = os.path.join(AD, "tests", "test_depth_floor.py")
    if not os.path.exists(f):
        print("ERROR: %s absent" % f)
        return report([("the new test file exists", False)])
    env = dict(os.environ, PYTHONPATH=os.path.abspath(AD))
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--no-header", "tests/test_depth_floor.py", "tests/test_tool_index_and_harvest.py",
                        "tests/test_c_group.py", "tests/test_serves.py"], cwd=AD, env=env, capture_output=True, text=True, timeout=280)
    tail = [ln for ln in (r.stdout or "").replace("\x1b", "").splitlines() if "passed" in ln or "failed" in ln][-1:]
    print("pytest rc=%d: %s" % (r.returncode, tail[0].strip() if tail else (r.stdout or r.stderr)[-200:]))
    co = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--co", "tests/test_depth_floor.py"], cwd=AD, env=env, capture_output=True, text=True, timeout=120)
    n_new = sum(1 for ln in (co.stdout or "").splitlines() if "::" in ln)
    print("new tests collected: %d" % n_new)
    return report([("the four test files pass", r.returncode == 0), ("the new file holds at least 6 tests", n_new >= 6)])


def ac2():
    sys.path.insert(0, AD)
    import emit_catalog_v02 as em
    tdir = em.TOOL_INDEX_DIR
    members = (yaml.safe_load(open(os.path.join(tdir, "members.yaml"), encoding="utf-8")) or {}).get("members") or []
    pending = (yaml.safe_load(open(os.path.join(tdir, "pending_members.yaml"), encoding="utf-8")) or {}).get("pending") or []
    measured = (yaml.safe_load(open(os.path.join(tdir, "measured.yaml"), encoding="utf-8")) or {}).get("tools") or {}
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
    census = {"deployed_commit": "c28check00", "tools": [{"tool": t, "definition": "d"} for t in tools]}
    entries, errors, _doc = em.load_tool_index(row_ids, census=census, row_keys=row_keys)
    print("DENOMINATOR tool_index entries %d; errors %d%s" % (len(entries), len(errors), (" (first: %s)" % errors[0][:120]) if errors else ""))
    res = [("load_tool_index runs on the real members and measured files without error", not errors and len(entries) > 0)]
    n_meas = bad_floor = bad_fresh = bad_other = 0
    for e in entries:
        if e.get("member") != "a":
            continue
        for c in claims(e.get("history_depth")):
            if c.get("claim") == "measured":
                n_meas += 1
                if c.get("depth_kind") != "floor" or c.get("measured_at") != c.get("read_at") or not c.get("measured_at"):
                    bad_floor += 1
            elif any(k in c for k in KEYS):
                bad_other += 1
        for c in claims(e.get("freshness")):
            if any(k in c for k in KEYS):
                bad_fresh += 1
    print("DENOMINATOR measured history_depth claims %d; without depth_kind floor and measured_at == read_at %d; freshness claims carrying them %d; inferred/absent claims carrying them %d"
          % (n_meas, bad_floor, bad_fresh, bad_other))
    res.append(("every measured history_depth claim carries depth_kind floor and measured_at equal to its read_at (%d of %d)" % (n_meas - bad_floor, n_meas), n_meas > 0 and not bad_floor))
    res.append(("no freshness, inferred or absent claim carries either key", not bad_fresh and not bad_other))
    cat = {e["tool"]: e for e in (yaml.safe_load(open(CAT, encoding="utf-8")).get("tool_index") or [])}

    def strip(h):
        if not isinstance(h, dict):
            return h
        h = {k: v for k, v in h.items() if k not in KEYS}
        if h.get("claim") == "per-link":
            h["links"] = [strip(x) for x in h.get("links") or []]
        return h
    diff = [e["tool"] for e in entries if e.get("member") == "a" and strip(e.get("history_depth")) != cat.get(e["tool"], {}).get("history_depth")]
    res.append(("with the two keys removed, every history_depth equals the tracked catalog's (%d differ)" % len(diff), not diff))
    return report(res)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("ac1", "ac2"):
        print(__doc__)
        return 9
    return {"ac1": ac1, "ac2": ac2}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
