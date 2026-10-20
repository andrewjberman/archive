"""w4_check.py <id> [deliverable]: the round-24 (workstream GATEWAY) criteria of cell MX-w-4, run from the repository root.
Ids: w4.AC1 (the 7 graded FAIL tools, their class, cause enum, owner rule), w4.AC2 (evidence resolves; fix is a sentence).
Prints a DENOMINATOR line, one line per arm, then RESULT: PASS|FAIL. ASCII only; python 3.9.
The contract is decompositions/NFRA_MCPINDEX_DECOMP.round24-GATEWAY.md section R24.3 (W4)."""
import copy
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R24 = os.path.normpath(os.path.join(HERE, ".."))
EVID = os.path.normpath(os.path.join(R24, "..", "round23", "evidence"))
GRADED = os.path.join(EVID, "BATTERY_GRADED_20261019.json")
DEFAULT = os.path.join("org", "missions", "D9", "NFRA", "NFRA_MCPINDEX", "deliverables", "0.9.0_WK_NFRA_MCPINDEX~80", "fail_attribution.json")
CLASSES = ("tool_error", "source_disagrees", "unexpected_empty", "route_unproven")
CAUSES = ("code", "catalog", "battery", "data")
SCHEMA = "gateway_fail_attribution/1"
FIELDS = ("tool", "fail_class", "cause", "owner", "evidence", "fix")
PROJECT_RE = re.compile(r"^[A-Z][A-Z0-9]+_[A-Z0-9_]+$")
OK, BAD = [], []


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def jload(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def is_ascii(s):
    return isinstance(s, str) and all(ord(ch) < 128 for ch in s)


def expected_tools():
    """{tool: (fail_class, [case ids])} for the tools graded in one of the four classes."""
    g = jload(GRADED)
    return {t["tool"]: (t["fail_class"], list(t.get("cases") or [])) for t in g["tools"] if t.get("fail_class") in CLASSES}


def case_ids_of(path):
    """Every case_id found in a results or cases JSON file."""
    found = set()

    def walk(o):
        if isinstance(o, dict):
            if isinstance(o.get("case_id"), str):
                found.add(o["case_id"])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(jload(path))
    return found


def ac1_problems(doc, exp):
    """List of reasons the document fails AC1 (empty list = clean)."""
    out = []
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA:
        return ["schema is not %s" % SCHEMA]
    items = doc.get("items")
    if not isinstance(items, list) or not all(isinstance(x, dict) for x in items):
        return ["items is not a list of objects"]
    for i, x in enumerate(items):
        miss = [f for f in FIELDS if not (isinstance(x.get(f), str) and x[f].strip())]
        if miss:
            out.append("item %d lacks nonempty string field(s) %s" % (i, ",".join(miss)))
    tools = [x.get("tool") for x in items]
    if len(tools) != len(set(tools)):
        out.append("a tool appears twice")
    if set(tools) != set(exp):
        out.append("tool set differs: missing %s extra %s" % (sorted(set(exp) - set(tools)), sorted(set(tools) - set(exp))))
    for x in items:
        t = x.get("tool")
        if t in exp and x.get("fail_class") != exp[t][0]:
            out.append("%s fail_class %r is not the graded %r" % (t, x.get("fail_class"), exp[t][0]))
        if x.get("cause") not in CAUSES:
            out.append("%s cause %r is not one of %s" % (t, x.get("cause"), "/".join(CAUSES)))
        owner, cause = x.get("owner"), x.get("cause")
        if cause == "code" and owner != "2.0.0_SA_COO~O":
            out.append("%s cause code needs owner 2.0.0_SA_COO~O, has %r" % (t, owner))
        if cause == "catalog" and owner != "2.0.0_SA_COO~MI":
            out.append("%s cause catalog needs owner 2.0.0_SA_COO~MI, has %r" % (t, owner))
        if cause in ("battery", "data") and not (isinstance(owner, str) and PROJECT_RE.match(owner)):
            out.append("%s cause %s needs a project code as owner, has %r" % (t, cause, owner))
    return out


def resolve_evidence(ev, tool, exp):
    """None if the evidence resolves, else the reason it does not."""
    if not is_ascii(ev) or not ev.strip():
        return "evidence is empty or not ASCII"
    if "#" in ev:
        path, cid = ev.rsplit("#", 1)
        if os.path.isabs(path) or ".." in path.replace("\\", "/").split("/"):
            return "evidence path %r is absolute or climbs out" % path
        if not os.path.isfile(path) or not path.endswith(".json"):
            return "results file %r does not exist or is not a .json file" % path
        try:
            ids = case_ids_of(path)
        except (ValueError, OSError) as exc:
            return "results file %r unreadable: %s" % (path, exc)
        if cid not in ids:
            return "case id %r is not in %s" % (cid, path)
        if tool in exp and cid not in exp[tool][1]:
            return "case id %r is not one of the graded cases %s of %s" % (cid, exp[tool][1], tool)
        return None
    m = re.match(r"^(.+):([0-9]+)$", ev)
    if not m:
        return "evidence %r is neither <path>:<line> nor <results file>#<case_id>" % ev
    path, lineno = m.group(1), int(m.group(2))
    if os.path.isabs(path) or ".." in path.replace("\\", "/").split("/"):
        return "evidence path %r is absolute or climbs out" % path
    if not os.path.isfile(path):
        return "file %r does not exist" % path
    with open(path, encoding="utf-8", errors="replace") as fh:
        n = sum(1 for _ in fh)
    if not 1 <= lineno <= n:
        return "line %d is outside %s (%d lines)" % (lineno, path, n)
    return None


def ac2_problems(doc, exp):
    out = []
    items = doc.get("items") if isinstance(doc, dict) else None
    if not isinstance(items, list):
        return ["items is not a list"]
    for x in items:
        if not isinstance(x, dict):
            out.append("an item is not an object")
            continue
        t = x.get("tool")
        why = resolve_evidence(x.get("evidence") if isinstance(x.get("evidence"), str) else "", t, exp)
        if why:
            out.append("%s: %s" % (t, why))
        fix = x.get("fix")
        if not is_ascii(fix) or len(fix.split()) < 8:
            out.append("%s: fix is not ASCII or has fewer than 8 words" % t)
    return out


def synthetic(exp):
    """A valid document built from the graded file; its evidence is the graded file itself (a real file) and a graded case id."""
    items = []
    for t, (fc, cases) in sorted(exp.items()):
        ev = "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round23/evidence/results_all_20261019.json#%s" % cases[0]
        items.append({"tool": t, "fail_class": fc, "cause": "code", "owner": "2.0.0_SA_COO~O", "evidence": ev,
                      "fix": "name the failing call and repair the reader role grant in the gateway code"})
    return {"schema": SCHEMA, "items": items}


def load_deliverable(path):
    if not os.path.isfile(path):
        return None, "deliverable %s absent" % path
    try:
        return jload(path), None
    except (ValueError, OSError) as exc:
        return None, "deliverable %s unreadable: %s" % (path, exc)


def controls(fn, exp, mutants):
    good = synthetic(exp)
    arm("control: a clean synthetic document passes", fn(good, exp) == [], "; ".join(fn(good, exp))[:200])
    for name, mut in mutants:
        d = copy.deepcopy(good)
        mut(d)
        arm("planted negative refused: %s" % name, bool(fn(d, exp)))


def ac1(path):
    exp = expected_tools()
    cnt = {c: sum(1 for v in exp.values() if v[0] == c) for c in CLASSES}
    doc, err = load_deliverable(path)
    n = len(doc.get("items", [])) if isinstance(doc, dict) and isinstance(doc.get("items"), list) else 0
    print("DENOMINATOR: %d graded FAIL tools of four classes (%s) read from BATTERY_GRADED_20261019.json; %d item(s) in the deliverable; 3 planted negatives" % (
        len(exp), ", ".join("%s %d" % (c, cnt[c]) for c in CLASSES), n))
    arm("the graded file holds the 7 tools (3 + 2 + 1 + 1)", len(exp) == 7 and sorted(cnt.values()) == [1, 1, 2, 3], "read %r" % cnt)

    def drop(d):
        d["items"].pop()

    def wrongclass(d):
        d["items"][0]["fail_class"] = "source_unchecked"

    def wrongowner(d):
        d["items"][0]["owner"] = "2.0.0_SA_COO~MI"
    controls(ac1_problems, exp, [("one tool dropped", drop), ("fail_class differs from the graded class", wrongclass), ("a code cause owned by the wrong seat", wrongowner)])
    if err:
        arm("deliverable present and readable", False, err)
        return
    probs = ac1_problems(doc, exp)
    arm("the deliverable names exactly the 7 tools with the graded class, a cause enum and the owner rule", not probs, "; ".join(probs)[:600])


def ac2(path):
    exp = expected_tools()
    doc, err = load_deliverable(path)
    n = len(doc.get("items", [])) if isinstance(doc, dict) and isinstance(doc.get("items"), list) else 0
    print("DENOMINATOR: %d item(s) in the deliverable to ground; evidence is <path>:<line> of an existing repository file or <results file>#<case_id> of a graded case of that tool; fix at least 8 ASCII words; 4 planted negatives" % n)

    def nofile(d):
        d["items"][0]["evidence"] = "workflows/gateway_battery/no_such_file_w4.py:1"

    def pastend(d):
        d["items"][0]["evidence"] = "workflows/gateway_battery/routing_table.py:999999"

    def ghostcase(d):
        d["items"][0]["evidence"] = d["items"][0]["evidence"].rsplit("#", 1)[0] + "#ZZ-99"

    def shortfix(d):
        d["items"][0]["fix"] = "fix the code now please ok"
    controls(ac2_problems, exp, [("evidence names a missing file", nofile), ("evidence line past the end of the file", pastend),
                                 ("evidence case id not in the results file", ghostcase), ("fix shorter than 8 words", shortfix)])
    if err:
        arm("deliverable present and readable", False, err)
        return
    probs = ac2_problems(doc, exp)
    arm("every evidence resolves and every fix is an ASCII sentence of 8 words or more", not probs, "; ".join(probs)[:600])


CHECKS = {"w4.AC1": ac1, "w4.AC2": ac2}

if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    if cid not in CHECKS:
        print("usage: w4_check.py <%s> [deliverable]" % "|".join(sorted(CHECKS)))
        sys.exit(9)
    CHECKS[cid](sys.argv[2] if len(sys.argv) > 2 else DEFAULT)
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    sys.exit(0 if OK and not BAD else 1)
