"""y5_check.py <id> [deliverable]: the round-25 (workstream GATEWAY) criteria of cell MX-y-5, run from the repository root.
Ids: y5.AC1 (schema, tool, cause enum, owner rule, answer_as_of and source_newest equal the real compare entry),
y5.AC2 (at least two evidence entries that resolve; fix is a sentence of 8 words or more).
Prints a DENOMINATOR line, one line per arm, then RESULT: PASS|FAIL. ASCII only; python 3.9.
The contract is decompositions/NFRA_MCPINDEX_DECOMP.round25-GATEWAY.md section R25.3 (Y5)."""
import copy
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R25 = os.path.normpath(os.path.join(HERE, ".."))
EVID23 = os.path.normpath(os.path.join(R25, "..", "round23", "evidence"))
COMPARE = os.path.join(EVID23, "SOURCE_COMPARE_20261020.json")
RESULTS = os.path.join(EVID23, "results_all_20261020.json")
DEFAULT = os.path.join("org", "missions", "D9", "NFRA", "NFRA_MCPINDEX", "deliverables", "0.9.0_WK_NFRA_MCPINDEX~88", "harvest_date_attribution.json")
TOOL = "harvest_query_columns"
CAUSES = ("code", "catalog", "battery", "data")
SCHEMA = "gateway_harvest_date_attribution/1"
FIELDS = ("tool", "answer_as_of", "source_newest", "cause", "owner", "fix")
PROJECT_RE = re.compile(r"^[A-Z][A-Z0-9]+_[A-Z0-9_]+$")
OK, BAD = [], []


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def jload(p):
    with open(p, encoding="utf-8", errors="replace") as fh:
        return json.load(fh)


def is_ascii(s):
    return isinstance(s, str) and all(ord(ch) < 128 for ch in s)


def real():
    """The compare entry of the tool: (answer_as_of, newest source date, [case ids])."""
    entry = [t for t in jload(COMPARE)["tools"] if t.get("tool") == TOOL][0]
    dates = sorted(entry.get("source_dates") or [])
    return entry["answer_as_of"], (dates[-1] if dates else ""), list(entry.get("case_ids") or [])


def case_ids_of(path):
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
    out = []
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA:
        return ["schema is not %s" % SCHEMA]
    miss = [f for f in FIELDS if not (isinstance(doc.get(f), str) and doc[f].strip())]
    if miss:
        out.append("nonempty string field(s) missing: %s" % ",".join(miss))
    if doc.get("tool") != TOOL:
        out.append("tool %r is not %s" % (doc.get("tool"), TOOL))
    if doc.get("answer_as_of") != exp[0]:
        out.append("answer_as_of %r is not the compare entry's %r" % (doc.get("answer_as_of"), exp[0]))
    if doc.get("source_newest") != exp[1]:
        out.append("source_newest %r is not the newest source date %r" % (doc.get("source_newest"), exp[1]))
    cause, owner = doc.get("cause"), doc.get("owner")
    if cause not in CAUSES:
        out.append("cause %r is not one of %s" % (cause, "/".join(CAUSES)))
    if cause == "code" and owner != "2.0.0_SA_COO~O":
        out.append("cause code needs owner 2.0.0_SA_COO~O, has %r" % owner)
    if cause in ("catalog", "battery") and owner != "2.0.0_SA_COO~MI":
        out.append("cause %s needs owner 2.0.0_SA_COO~MI, has %r" % (cause, owner))
    if cause == "data" and not (isinstance(owner, str) and PROJECT_RE.match(owner)):
        out.append("cause data needs a project code as owner, has %r" % owner)
    return out


def resolve_evidence(ev, exp):
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
        if cid not in exp[2]:
            return "case id %r is not one of the tool's cases %s" % (cid, exp[2])
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
    if not isinstance(doc, dict):
        return ["the document is not an object"]
    ev = doc.get("evidence")
    if not isinstance(ev, list) or len(ev) < 2 or not all(isinstance(x, str) for x in ev):
        out.append("evidence is not a list of at least two strings")
    else:
        if len(set(ev)) != len(ev):
            out.append("an evidence entry is repeated")
        for x in ev:
            why = resolve_evidence(x, exp)
            if why:
                out.append(why)
    fix = doc.get("fix")
    if not is_ascii(fix) or len(fix.split()) < 8:
        out.append("fix is not ASCII or has fewer than 8 words")
    return out


def synthetic(exp):
    return {"schema": SCHEMA, "tool": TOOL, "answer_as_of": exp[0], "source_newest": exp[1], "cause": "battery", "owner": "2.0.0_SA_COO~MI",
            "evidence": ["infra/aws/ec2/opal-gateway/app/harvest_figures.py:176",
                         "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round23/evidence/results_all_20261020.json#%s" % exp[2][0]],
            "fix": "compare the part stamp of the newest part with the partition date it sits in"}


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
    exp = real()
    doc, err = load_deliverable(path)
    print("DENOMINATOR: tool %s; answer_as_of %s and newest source date %s read from SOURCE_COMPARE_20261020.json; case ids %s; 6 planted negatives" % (
        TOOL, exp[0], exp[1], ",".join(exp[2])))
    arm("the compare entry holds a dated answer, a source date and a case id", bool(exp[0]) and bool(exp[1]) and bool(exp[2]), "read %r" % (exp,))
    controls(ac1_problems, exp, [
        ("wrong schema", lambda d: d.update(schema="gateway_harvest_date_attribution/0")),
        ("wrong tool", lambda d: d.update(tool="harvest_read")),
        ("a cause outside the enum", lambda d: d.update(cause="clock")),
        ("a code cause owned by the wrong seat", lambda d: d.update(cause="code", owner="2.0.0_SA_COO~MI")),
        ("answer_as_of altered", lambda d: d.update(answer_as_of="2026-10-08T00:00:00Z")),
        ("source_newest altered", lambda d: d.update(source_newest="2026-10-09"))])
    if err:
        arm("deliverable present and readable", False, err)
        return
    probs = ac1_problems(doc, exp)
    arm("the deliverable names the tool, the real answer date and source date, a cause from the enum and the owner rule", not probs, "; ".join(probs)[:600])


def ac2(path):
    exp = real()
    doc, err = load_deliverable(path)
    n = len(doc.get("evidence", [])) if isinstance(doc, dict) and isinstance(doc.get("evidence"), list) else 0
    print("DENOMINATOR: %d evidence entr(y/ies) in the deliverable to ground; each is <path>:<line> of an existing repository file or <results file>#<case_id> of case %s; fix at least 8 ASCII words; 6 planted negatives" % (n, ",".join(exp[2])))
    controls(ac2_problems, exp, [
        ("only one evidence entry", lambda d: d.update(evidence=d["evidence"][:1])),
        ("evidence names a missing file", lambda d: d["evidence"].__setitem__(0, "workflows/gateway_battery/no_such_file_y5.py:1")),
        ("evidence line past the end of the file", lambda d: d["evidence"].__setitem__(0, "workflows/gateway_battery/routing_table.py:999999")),
        ("evidence case id not in the results file", lambda d: d["evidence"].__setitem__(1, d["evidence"][1].rsplit("#", 1)[0] + "#ZZ-99")),
        ("fix shorter than 8 words", lambda d: d.update(fix="fix the stamp now please ok")),
        ("fix not ASCII", lambda d: d.update(fix="compare the part stamp of the newest part with the partition date caf" + chr(233)))])
    if err:
        arm("deliverable present and readable", False, err)
        return
    probs = ac2_problems(doc, exp)
    arm("two or more evidence entries all resolve and the fix is an ASCII sentence of 8 words or more", not probs, "; ".join(probs)[:600])


CHECKS = {"y5.AC1": ac1, "y5.AC2": ac2}

if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    if cid not in CHECKS:
        print("usage: y5_check.py <%s> [deliverable]" % "|".join(sorted(CHECKS)))
        sys.exit(9)
    CHECKS[cid](sys.argv[2] if len(sys.argv) > 2 else DEFAULT)
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    sys.exit(0 if OK and not BAD else 1)
