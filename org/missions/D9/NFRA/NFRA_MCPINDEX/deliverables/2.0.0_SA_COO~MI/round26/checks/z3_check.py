"""z3_check.py <id> [deliverable]: the round-26 (workstream GATEWAY) criteria of cell MX-z-3, run from the repository root.
Ids: z3.AC1 (schema; exactly the 46 tools of the real compare file whose agrees is null and whose source kind is graph,
integration or store, once each, sorted; class equals the source kind; route and feasible values),
z3.AC2 (every cite resolves in the gateway source; call is 8 ASCII words or more; fact and answer_field are present; a
feasible false item carries a reason of 8 words or more; a feasible true item names a route and its cite shows the same call).
Prints a DENOMINATOR line, one line per arm, then RESULT: PASS|FAIL. ASCII only; python 3.9.
The contract is decompositions/NFRA_MCPINDEX_DECOMP.round26-GATEWAY.md section R26.3 (Z3)."""
import copy
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R26 = os.path.normpath(os.path.join(HERE, ".."))
DELIV = os.path.normpath(os.path.join(R26, "..", ".."))
COMPARE = os.environ.get("Z3_COMPARE") or os.path.join(DELIV, "2.0.0_SA_COO~MI", "round25", "evidence", "SOURCE_COMPARE_20261020c.json")
DEFAULT = os.path.join("org", "missions", "D9", "NFRA", "NFRA_MCPINDEX", "deliverables", "0.9.0_WK_NFRA_MCPINDEX~92", "probe_plan.json")
GW = "infra/aws/ec2/opal-gateway/app/"
SCHEMA = "gateway_probe_plan/1"
CLASSES = ("graph", "integration", "store")
ROUTES = ("direct-graph", "vendor-api", "direct-dynamodb", "none")
STR_FIELDS = ("tool", "class", "route", "call", "fact", "answer_field", "reason", "cite")
WINDOW = 6
OK, BAD = [], []


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def jload(p):
    with open(p, encoding="utf-8", errors="replace") as fh:
        return json.load(fh)


def is_ascii(s):
    return isinstance(s, str) and all(ord(ch) < 128 for ch in s)


def words(s):
    return len(s.split()) if isinstance(s, str) else 0


def expected():
    """{tool: kind} for the entries of the real compare file with agrees null and a graph, integration or store source."""
    out = {}
    for t in jload(COMPARE)["tools"]:
        src = t.get("source") or {}
        if t.get("agrees") is None and src.get("kind") in CLASSES:
            out[t["tool"]] = src["kind"]
    return out


def ac1_problems(doc, exp):
    out = []
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA:
        return ["schema is not %s" % SCHEMA]
    items = doc.get("items")
    if not isinstance(items, list) or not all(isinstance(x, dict) for x in items):
        return ["items is not a list of objects"]
    names = [x.get("tool") for x in items]
    if len(set(names)) != len(names):
        out.append("a tool appears more than once: %s" % sorted({n for n in names if names.count(n) > 1})[:4])
    missing = sorted(set(exp) - set(names))
    foreign = sorted(set(names) - set(exp))
    if missing:
        out.append("tools missing: %s" % missing[:5])
    if foreign:
        out.append("tools outside the 46: %s" % foreign[:5])
    if names != sorted(names):
        out.append("items are not sorted by tool")
    for x in items:
        t = x.get("tool")
        if t in exp and x.get("class") != exp[t]:
            out.append("%s: class %r is not its source kind %r" % (t, x.get("class"), exp[t]))
        if x.get("route") not in ROUTES:
            out.append("%s: route %r is not one of %s" % (t, x.get("route"), "/".join(ROUTES)))
        if not isinstance(x.get("feasible"), bool):
            out.append("%s: feasible is not a boolean" % t)
        miss = [f for f in ("tool", "class", "route", "call", "fact", "answer_field", "cite") if not (isinstance(x.get(f), str) and x[f].strip())]
        if miss:
            out.append("%s: empty or non-string field(s) %s" % (t, ",".join(miss)))
        if not isinstance(x.get("reason"), str):
            out.append("%s: reason is not a string" % t)
    return out


def resolve_cite(cite):
    """None when the cite is <repo path under the gateway source>:<line> of an existing file with the line inside it."""
    if not is_ascii(cite) or not cite.strip():
        return "cite is empty or not ASCII"
    m = re.match(r"^(.+):([0-9]+)$", cite)
    if not m:
        return "cite %r is not <path>:<line>" % cite
    path, lineno = m.group(1), int(m.group(2))
    if os.path.isabs(path) or ".." in path.replace("\\", "/").split("/"):
        return "cite path %r is absolute or climbs out" % path
    if not path.replace("\\", "/").startswith(GW):
        return "cite path %r is not under %s" % (path, GW)
    if not os.path.isfile(path):
        return "file %r does not exist" % path
    with open(path, encoding="utf-8", errors="replace") as fh:
        n = sum(1 for _ in fh)
    if not 1 <= lineno <= n:
        return "line %d is outside %s (%d lines)" % (lineno, path, n)
    return None


def window_text(cite):
    m = re.match(r"^(.+):([0-9]+)$", cite)
    with open(m.group(1), encoding="utf-8", errors="replace") as fh:
        lines = fh.read().split("\n")
    n = int(m.group(2))
    return "\n".join(lines[max(0, n - 1 - WINDOW):n + WINDOW]).lower()


def anchors(call, route):
    """The tokens of a call that the cited gateway lines must show: request paths, a table name, a table environment name."""
    found = []
    bare = re.sub(r"https?://[^/\s]+(?:/(?:v1\.0|beta))?", " ", call or "")   # a full URL reads as its path
    for tok in re.findall(r"/[A-Za-z][A-Za-z0-9_/.-]*", bare):
        for stop in ("{", "(", "?", "$"):
            tok = tok.split(stop)[0]
        tok = tok.rstrip("/.")
        if len(tok) >= 3:
            found.append(tok.lower())
    if route == "direct-dynamodb":
        found = []
        m = re.search(r"--table-name\s+([A-Za-z0-9_.-]+)", call or "")
        if m:
            found.append(m.group(1).lower())
        found += [t.lower() for t in re.findall(r"\b[A-Z][A-Z0-9_]{2,}_TABLE\b", call or "")]
    return found


def ac2_problems(doc, exp=None):
    out = []
    if not isinstance(doc, dict) or not isinstance(doc.get("items"), list):
        return ["the document has no items list"]
    for x in doc["items"]:
        t = x.get("tool")
        why = resolve_cite(x.get("cite") or "")
        if why:
            out.append("%s: %s" % (t, why))
        call = x.get("call")
        if not is_ascii(call) or words(call) < 8:
            out.append("%s: call is not ASCII or has fewer than 8 words" % t)
        for f in ("fact", "answer_field"):
            if not (is_ascii(x.get(f)) and x[f].strip()):
                out.append("%s: %s is empty or not ASCII" % (t, f))
        feasible = x.get("feasible")
        if feasible is False:
            r = x.get("reason")
            if not is_ascii(r) or words(r) < 8:
                out.append("%s: feasible false needs a reason of at least 8 ASCII words" % t)
        elif feasible is True:
            if x.get("route") == "none":
                out.append("%s: feasible true with route none" % t)
            if not why:
                an = anchors(call, x.get("route"))
                if not an:
                    out.append("%s: feasible true but the call names no request path or table to show" % t)
                elif not any(a in window_text(x["cite"]) for a in an):
                    out.append("%s: the cited lines do not show the call (looked for %s)" % (t, an[:3]))
        else:
            out.append("%s: feasible is not a boolean" % t)
    return out


def synthetic_ac1(exp):
    return {"schema": SCHEMA, "items": [
        {"tool": t, "class": k, "route": "none", "call": "no second client read exists for this tool in this session at all", "fact": "a count", "answer_field": "value",
         "feasible": False, "reason": "no read route outside the gateway exists for this source in this session at all", "cite": GW + "tools.py:228"}
        for t, k in sorted(exp.items())]}


def synthetic_ac2():
    return {"schema": SCHEMA, "items": [
        {"tool": "whoami", "class": "graph", "route": "direct-graph", "call": "GET https://graph.microsoft.com/v1.0/me with the owner's own delegated token",
         "fact": "the signed-in user's userPrincipalName", "answer_field": "userPrincipalName", "feasible": True, "reason": "", "cite": GW + "tools.py:231"},
        {"tool": "mdpf_get_security_classification", "class": "store", "route": "direct-dynamodb",
         "call": "aws dynamodb get-item --table-name etf-classifications --key ticker S SPY read once outside the gateway",
         "fact": "the classification row for one ticker", "answer_field": "classification", "feasible": True, "reason": "", "cite": GW + "mdpf_classification.py:34"},
        {"tool": "ycharts_search", "class": "integration", "route": "none", "call": "the vendor's own search request would need a YCharts session key that is not available",
         "fact": "the number of matches", "answer_field": "matches", "feasible": False,
         "reason": "the vendor session key lives only in the gateway so no second client can call the vendor", "cite": GW + "integrations/ycharts/client.py:96"}]}


def load_deliverable(path):
    if not os.path.isfile(path):
        return None, "deliverable %s absent" % path
    try:
        return jload(path), None
    except (ValueError, OSError) as exc:
        return None, "deliverable %s unreadable: %s" % (path, exc)


def counts(exp):
    c = {}
    for k in exp.values():
        c[k] = c.get(k, 0) + 1
    return c


def ac1(path):
    exp = expected()
    c = counts(exp)
    doc, err = load_deliverable(path)
    print("DENOMINATOR: %d tool(s) in scope: the compare entries of SOURCE_COMPARE_20261020c.json with agrees null and a graph, integration or store source (graph %d, integration %d, store %d); 8 planted negatives" % (
        len(exp), c.get("graph", 0), c.get("integration", 0), c.get("store", 0)))
    arm("the real compare file yields the 46 tools (graph 33, integration 9, store 4)", len(exp) == 46 and c == {"graph": 33, "integration": 9, "store": 4}, "read %d: %r" % (len(exp), c))
    good = synthetic_ac1(exp)
    arm("control: a clean synthetic plan over the real tool set passes", ac1_problems(good, exp) == [], "; ".join(ac1_problems(good, exp))[:200])
    names = sorted(exp)
    muts = [
        ("wrong schema", lambda d: d.update(schema="gateway_probe_plan/0")),
        ("a tool dropped", lambda d: d["items"].pop(0)),
        ("a tool twice", lambda d: d["items"].append(copy.deepcopy(d["items"][0]))),
        ("a tool outside the 46", lambda d: d["items"].append(dict(copy.deepcopy(d["items"][0]), tool="zzz_not_a_tool"))),
        ("a class that is not the source kind", lambda d: d["items"][0].update({"class": "store" if d["items"][0]["class"] != "store" else "graph"})),
        ("a route outside the enum", lambda d: d["items"][0].update(route="telepathy")),
        ("items out of order", lambda d: d["items"].reverse()),
        ("feasible not a boolean", lambda d: d["items"][0].update(feasible="yes"))]
    for name, mut in muts:
        d = copy.deepcopy(good)
        mut(d)
        arm("planted negative refused: %s" % name, bool(ac1_problems(d, exp)))
    del names
    if err:
        arm("deliverable present and readable", False, err)
        return
    probs = ac1_problems(doc, exp)
    arm("the plan holds exactly the 46 tools once each, sorted, with class = source kind, a route from the enum and a boolean feasible", not probs, "; ".join(probs)[:600])


def ac2(path):
    exp = expected()
    doc, err = load_deliverable(path)
    n = len(doc.get("items", [])) if isinstance(doc, dict) and isinstance(doc.get("items"), list) else 0
    print("DENOMINATOR: %d plan item(s) to ground; each cite is <path>:<line> under %s with the line inside the file; call 8 ASCII words or more; feasible false needs a reason of 8 words or more; feasible true needs a route and a cite whose lines (+-%d) show the call's request path or table; 6 planted negatives" % (n, GW, WINDOW))
    good = synthetic_ac2()
    arm("control: a clean synthetic plan (a Graph read, a DynamoDB read, an infeasible vendor read) passes", ac2_problems(good) == [], "; ".join(ac2_problems(good))[:300])
    muts = [
        ("a cite to a missing file", lambda d: d["items"][0].update(cite=GW + "no_such_file_z3.py:1")),
        ("a cite past the end of the file", lambda d: d["items"][0].update(cite=GW + "tools.py:99999999")),
        ("a call of fewer than 8 words", lambda d: d["items"][0].update(call="GET /me once")),
        ("a feasible false item with a short reason", lambda d: d["items"][2].update(reason="no key")),
        ("a feasible true item whose cited lines do not show the call", lambda d: d["items"][0].update(cite=GW + "tools.py:3")),
        ("an empty answer_field", lambda d: d["items"][1].update(answer_field=""))]
    for name, mut in muts:
        d = copy.deepcopy(good)
        mut(d)
        arm("planted negative refused: %s" % name, bool(ac2_problems(d)))
    if err:
        arm("deliverable present and readable", False, err)
        return
    probs = ac2_problems(doc, exp)
    arm("every cite resolves, every call and reason is long enough, and every feasible item's cite shows its call", not probs, "; ".join(probs)[:600])


CHECKS = {"z3.AC1": ac1, "z3.AC2": ac2}

if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    if cid not in CHECKS:
        print("usage: z3_check.py <%s> [deliverable]" % "|".join(sorted(CHECKS)))
        sys.exit(9)
    CHECKS[cid](sys.argv[2] if len(sys.argv) > 2 else DEFAULT)
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    sys.exit(0 if OK and not BAD else 1)
