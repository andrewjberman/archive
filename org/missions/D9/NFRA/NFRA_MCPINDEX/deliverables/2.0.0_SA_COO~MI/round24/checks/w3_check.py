"""w3_check.py <id> [deliverable]: the round-24 (workstream GATEWAY) criteria of cell MX-w-3 (link fixes), run from the repository root.
Prints a DENOMINATOR line, one line per arm, then RESULT: PASS|FAIL. Ids: w3.AC1 (the shape and coverage of the fixes), w3.AC2 (the grounding of
the adds and the result of applying the fixes). It grades against the REAL routing table, census, source sets and catalog. ASCII only; python 3.9.
The contract is decompositions/NFRA_MCPINDEX_DECOMP.round24-GATEWAY.md section R24.3 (W3)."""
import copy
import glob
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R24 = os.path.normpath(os.path.join(HERE, ".."))
SELF = os.path.normpath(os.path.join(R24, ".."))
DELIV = os.path.normpath(os.path.join(R24, "..", ".."))
ROUTING_JSON = os.path.join(SELF, "round23", "evidence", "ROUTING_TABLE_20261019.json")
CENSUS_JSON = os.path.join(SELF, "round22", "evidence", "GATEWAY_SURFACE_CENSUS_20261019_v2.json")
RT_PY = os.path.join("workflows", "gateway_battery", "routing_table.py")
CATALOG = os.path.join("infra", "aws", "ec2", "opal-gateway", "app", "refs", "DATA_CATALOG.yaml")
GW = os.path.join("infra", "aws", "ec2", "opal-gateway")
SCHEMA = "gateway_link_fixes/1"
CITE_RE = re.compile(r"^(?P<path>[A-Za-z0-9_./\-]+\.py):(?P<line>[0-9]+)$")
CITE_IN_TEXT = re.compile(r"[A-Za-z0-9_./\-]+\.py:[0-9]+")
OK, BAD = [], []


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def jload(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def ascii_text(s):
    return isinstance(s, str) and all(ord(ch) < 128 for ch in s)


def words(s):
    return len(s.split()) if isinstance(s, str) else 0


def load_rt():
    spec = importlib.util.spec_from_file_location("routing_table_w3", RT_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cite_ok(cite):
    """A cite is <path>:<line>; the path is repo-relative or relative to infra/aws/ec2/opal-gateway; the file and the line exist."""
    m = CITE_RE.match(cite) if isinstance(cite, str) else None
    if not m:
        return False
    for base in ("", GW):
        p = os.path.join(base, m.group("path"))
        if os.path.isfile(p):
            with open(p, encoding="utf-8", errors="replace") as fh:
                return 1 <= int(m.group("line")) <= sum(1 for _ in fh)
    return False


class World:
    """The real inputs: the scope tools, their MISROUTED pairs, linked rows, source sets and the catalog entities."""

    def __init__(self):
        self.rt = load_rt()
        table = jload(ROUTING_JSON)
        census = jload(CENSUS_JSON)
        cat = self.rt.load_yaml(CATALOG, "catalog")
        _tab, self.by_entity, _vendors, _idx = self.rt.catalog_info(cat)
        self.sources = self.rt.load_source_sets(sorted(glob.glob(os.path.join(DELIV, "0.9.0_WK_NFRA_MCPINDEX~7*", "source_sets_*.json"))))
        ctools = {t["name"]: t for t in census["tools"]}
        self.scope, self.bad, self.linked = [], {}, {}
        for t in table["tools"]:
            if t["verdict"] == "MISROUTED" and t["class"] == "link":
                self.scope.append(t["tool"])
                self.bad[t["tool"]] = sorted(p["row"] for p in t["pairs"] if p["verdict"] == "MISROUTED")
                self.linked[t["tool"]] = sorted(set(ctools[t["tool"]].get("indexes") or []))
        self.scope.sort()


def entries(doc):
    fx = doc.get("fixes") if isinstance(doc, dict) else None
    return fx if isinstance(fx, list) else []


def shape_errors(doc, w):
    errs = []
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA:
        return ["schema is not %s" % SCHEMA]
    names = [e.get("tool") if isinstance(e, dict) else None for e in entries(doc)]
    if sorted(n for n in names if n) != w.scope or len(names) != len(set(names)):
        errs.append("tools %s != scope %s" % (sorted(n for n in names if n), w.scope))
    for e in entries(doc):
        if not isinstance(e, dict):
            errs.append("an entry is not an object")
            continue
        t = e.get("tool")
        for k in ("remove", "add"):
            if not isinstance(e.get(k), list) or not all(isinstance(x, str) and x for x in e[k]):
                errs.append("%s.%s is not a list of row ids" % (t, k))
        keep = e.get("keep")
        if not isinstance(keep, list) or not all(isinstance(x, dict) and isinstance(x.get("row"), str) and ascii_text(x.get("reason")) and words(x.get("reason")) >= 8
                                                  and CITE_IN_TEXT.search(x.get("reason") or "") for x in keep):
            errs.append("%s.keep entries need a row and an ASCII reason of 8 words naming a path:line" % t)
        if not (ascii_text(e.get("basis")) and words(e.get("basis")) >= 8):
            errs.append("%s.basis is not ASCII of at least 8 words" % t)
        if not cite_ok(e.get("cite")):
            errs.append("%s.cite %r does not resolve" % (t, e.get("cite")))
    return errs


def coverage_errors(doc, w):
    errs = []
    for e in entries(doc):
        t = e.get("tool")
        if t not in w.bad:
            continue
        m = set(w.bad[t])
        rem = set(e.get("remove") or [])
        kept = set(x.get("row") for x in (e.get("keep") or []) if isinstance(x, dict))
        if rem & kept:
            errs.append("%s: a row is in remove and keep" % t)
        if (rem | kept) != m:
            errs.append("%s: remove+keep %s != MISROUTED pairs %s" % (t, sorted(rem | kept), sorted(m)))
    return errs


def ground_errors(doc, w):
    errs = []
    for e in entries(doc):
        t = e.get("tool")
        if t not in w.bad:
            continue
        srcs = w.sources.get(t) or []
        for row in e.get("add") or []:
            hit = w.by_entity.get(row)
            if hit is None:
                errs.append("%s: add %s is not a catalog entity" % (t, row))
            elif row in w.linked[t]:
                errs.append("%s: add %s is already linked" % (t, row))
            elif row in (e.get("remove") or []) or row in [x.get("row") for x in (e.get("keep") or []) if isinstance(x, dict)]:
                errs.append("%s: add %s is also removed or kept" % (t, row))
            elif not any(w.rt.s3_matches(hit, s) for s in srcs):
                errs.append("%s: add %s overlaps no s3 source of the tool" % (t, row))
    return errs


def apply_errors(doc, w):
    """After the fixes: (linked - remove - keep) + add has no MISROUTED pair against the tool's source set."""
    errs = []
    for e in entries(doc):
        t = e.get("tool")
        if t not in w.bad:
            continue
        gone = set(e.get("remove") or []) | set(x.get("row") for x in (e.get("keep") or []) if isinstance(x, dict))
        remaining = [r for r in w.linked[t] if r not in gone] + [r for r in (e.get("add") or []) if r in w.by_entity]
        pairs = w.rt.grade_pairs(remaining, w.by_entity, w.sources.get(t) or [])
        left = [p["row"] for p in pairs if p["verdict"] == "MISROUTED"]
        if left:
            errs.append("%s: still MISROUTED after the fixes: %s" % (t, left))
    return errs


def mutants(doc, w):
    """In-memory planted defects; each returns (name, mutated doc, validator that must now report an error)."""
    out = []
    e0 = next((e for e in entries(doc) if e.get("remove")), None)
    if e0 is None:
        return out
    t0 = e0["tool"]

    def mut(fn):
        d = copy.deepcopy(doc)
        tgt = next(e for e in entries(d) if e["tool"] == t0)
        fn(d, tgt)
        return d
    out.append(("a tool dropped from the fixes", mut(lambda d, e: d["fixes"].remove(e)), lambda d: shape_errors(d, w)))
    out.append(("a MISROUTED pair left in neither remove nor keep", mut(lambda d, e: e["remove"].pop()), lambda d: coverage_errors(d, w)))
    good = next(r for r in w.linked[t0] if r not in w.bad[t0]) if any(r not in w.bad[t0] for r in w.linked[t0]) else None
    if good:
        out.append(("a ROUTED row removed", mut(lambda d, e: e["remove"].append(good)), lambda d: coverage_errors(d, w)))
    out.append(("an add that is not a catalog entity", mut(lambda d, e: e["add"].append("no_such_row_planted")), lambda d: ground_errors(d, w)))
    far = next((r for r, h in w.by_entity.items() if r not in w.linked[t0] and not any(w.rt.s3_matches(h, s) for s in (w.sources.get(t0) or []))), None)
    out.append(("an add that overlaps no source of the tool", mut(lambda d, e: e["add"].append(far)), lambda d: ground_errors(d, w)))
    out.append(("a remove with the MISROUTED pair put back by an add of another bad row",
                mut(lambda d, e: e["remove"].clear()), lambda d: apply_errors(d, w) + coverage_errors(d, w)))
    return out


def main(argv):
    crit = argv[0] if argv else ""
    path = argv[1] if len(argv) > 1 else ""
    if crit not in ("w3.AC1", "w3.AC2"):
        print("usage: w3_check.py w3.AC1|w3.AC2 <link_fixes.json>")
        return 2
    w = World()
    print("DENOMINATOR: %d tool(s) in scope (the routing table's MISROUTED class link): %s; %d MISROUTED pair(s); catalog %d entities; source sets for %d tools"
          % (len(w.scope), ",".join(w.scope), sum(len(v) for v in w.bad.values()), len(w.by_entity), len(w.sources)))
    present = bool(path) and os.path.isfile(path)
    arm("the deliverable file exists", present, "absent: %s" % path)
    doc = None
    if present:
        try:
            doc = jload(path)
        except ValueError as exc:
            arm("the deliverable is JSON", False, str(exc))
    if doc is not None:
        if crit == "w3.AC1":
            errs = shape_errors(doc, w)
            arm("schema %s, exactly the scope tools once each, remove/add lists, keep reasons, basis and cites resolve" % SCHEMA, not errs, "; ".join(errs[:4]))
            errs = coverage_errors(doc, w) if not shape_errors(doc, w) else ["shape first"]
            arm("every MISROUTED pair of every tool is in remove or keep, and remove/keep hold only those pairs", not errs, "; ".join(errs[:4]))
        else:
            if shape_errors(doc, w):
                arm("the shape is valid (AC1) before the grounding is graded", False, "; ".join(shape_errors(doc, w)[:3]))
            else:
                errs = ground_errors(doc, w)
                arm("every add is a catalog row, not yet linked, overlapping an s3 source of the tool", not errs, "; ".join(errs[:4]))
                errs = apply_errors(doc, w)
                arm("after the fixes no remaining pair is MISROUTED by the link rule", not errs, "; ".join(errs[:4]))
        base_ok = not shape_errors(doc, w) and not coverage_errors(doc, w)
        if crit == "w3.AC2":
            base_ok = base_ok and not ground_errors(doc, w) and not apply_errors(doc, w)
        planted = mutants(doc, w) if base_ok else []
        want = {"w3.AC1": ("a tool dropped", "a MISROUTED pair left", "a ROUTED row removed", "a remove with"),
                "w3.AC2": ("an add that",)}[crit]
        picked = [m for m in planted if m[0].startswith(want)]
        fired = [name for name, d, fn in picked if fn(d)]
        arm("planted negatives all fire (%d of %d)" % (len(fired), len(picked)), bool(picked) and len(fired) == len(picked),
            "the deliverable is not valid enough to plant on" if not base_ok else "not fired: %s" % [n for n, _d, _f in picked if n not in fired])
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if not BAD else "FAIL"))
    return 0 if not BAD else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
