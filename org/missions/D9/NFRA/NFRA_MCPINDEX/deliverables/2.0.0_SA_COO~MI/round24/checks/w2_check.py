"""w2_check.py <w2.AC1|w2.AC2> [plan file]: the round-24 (workstream GATEWAY) criteria for cell MX-w-2 (the NOT-RUN PLAN), run from the repository root.
Prints a DENOMINATOR line, one line per arm, then RESULT: PASS|FAIL. ASCII only; python 3.9; stdlib only.
w2.AC1 = coverage and shape (exactly the tools graded not_run, once each; fields and enums).
w2.AC2 = the rules (senders never run, unrun cases covered, no placeholder input, test_send, reasons, cites) plus planted negatives.
The contract is decompositions/NFRA_MCPINDEX_DECOMP.round24-GATEWAY.md section R24.3 (W2)."""
import copy
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R24 = os.path.normpath(os.path.join(HERE, ".."))
D = os.path.normpath(os.path.join(R24, "..", ".."))
R23E = os.path.join(D, "2.0.0_SA_COO~MI", "round23", "evidence")
CENSUS = os.path.join(D, "2.0.0_SA_COO~MI", "round22", "evidence", "GATEWAY_SURFACE_CENSUS_20261019_v2.json")
GRADED = os.path.join(R23E, "BATTERY_GRADED_20261019.json")
CASES = os.path.join(R23E, "cases_all_20261019.json")
RESULTS = os.path.join(R23E, "results_all_20261019.json")
DEFAULT_PLAN = os.path.join(D, "0.9.0_WK_NFRA_MCPINDEX~78", "not_run_plan.json")
REAL_NO_CLASS = (None, "UNCLASSIFIED")
MUTATING_UNCLASSIFIED = ("opal_data_refresh_upload", "schwab_prepare_download")
PLANS = ("run", "preview-only", "c")
SEND_TO = ("tester mailbox", "tester chat")
CASE_FIELDS = ("case_id", "tool", "question", "args", "expect", "source_hint")
ENTRY_FIELDS = ("tool", "plan", "case_ids", "new_cases", "test_send", "reason", "cite")
PLACEHOLDER = re.compile(r"<[^<>]+>")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+")
LONG_DIGITS = re.compile(r"\d{9,}")
OK, BAD = [], []


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def jload(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def census_tools():
    out = {}

    def walk(o):
        if isinstance(o, dict):
            if isinstance(o.get("name"), str) and "write_class" in o:
                out[o["name"]] = o
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(jload(CENSUS))
    return out


def is_sender(t):
    return (t.get("write_class") not in REAL_NO_CLASS) or t.get("name") in MUTATING_UNCLASSIFIED


def words(s):
    return len(str(s).split())


def ascii_ok(s):
    return isinstance(s, str) and all(ord(ch) < 128 for ch in s)


def cite_ok(cite):
    m = re.match(r"^(.+):(\d+)$", str(cite or ""))
    if not m or ".." in m.group(1) or m.group(1).startswith("/"):
        return False
    p = m.group(1)
    if not os.path.isfile(p):
        return False
    try:
        with open(p, encoding="utf-8", errors="replace") as fh:
            n = sum(1 for _ in fh)
    except OSError:
        return False
    return 1 <= int(m.group(2)) <= n


def str_values(args):
    for v in (args or {}).values():
        if isinstance(v, str):
            yield v
        elif isinstance(v, (list, tuple)):
            for x in v:
                if isinstance(x, str):
                    yield x


def load_world():
    graded = jload(GRADED)
    not_run = sorted(t["tool"] for t in graded["tools"] if t.get("fail_class") == "not_run")
    cases = {c["case_id"]: c for c in jload(CASES)["cases"]}
    done = {r["case_id"] for r in jload(RESULTS)["results"]}
    tools = census_tools()
    return not_run, cases, done, tools


def load_plan(path):
    if not os.path.isfile(path):
        return None, "plan file absent: %s" % path
    try:
        doc = jload(path)
    except (OSError, ValueError) as exc:
        return None, "unreadable: %s" % exc
    return doc, ""


def shape_problems(doc, not_run):
    probs = []
    if not isinstance(doc, dict) or doc.get("schema") != "gateway_not_run_plan/1" or not isinstance(doc.get("plans"), list):
        return ["schema is not gateway_not_run_plan/1 with a plans list"]
    names = [p.get("tool") if isinstance(p, dict) else None for p in doc["plans"]]
    if sorted(n for n in names if n) != sorted(set(n for n in names if n)):
        probs.append("a tool appears twice: %r" % sorted({n for n in names if names.count(n) > 1}))
    missing, extra = sorted(set(not_run) - set(names)), sorted(set(n for n in names if n) - set(not_run))
    if missing:
        probs.append("tools with no plan: %r" % missing[:6])
    if extra:
        probs.append("plans for tools not graded not_run: %r" % extra[:6])
    for p in doc["plans"]:
        if not isinstance(p, dict):
            probs.append("a plan entry is not an object")
            continue
        if any(f not in p for f in ENTRY_FIELDS):
            probs.append("%s lacks fields %r" % (p.get("tool"), [f for f in ENTRY_FIELDS if f not in p]))
        elif p["plan"] not in PLANS or not isinstance(p["case_ids"], list) or not isinstance(p["new_cases"], list):
            probs.append("%s has a bad plan, case_ids or new_cases" % p.get("tool"))
    return probs


def rule_problems(doc, not_run, cases, done, tools):
    """Every rule of W2 on a plan document; returns a list of problems (empty = rules hold)."""
    probs = []
    seen_new = set()
    for p in doc.get("plans", []):
        tool, plan = p.get("tool"), p.get("plan")
        t = tools.get(tool, {"name": tool})
        sender = is_sender(t)
        ids, news = p.get("case_ids") or [], p.get("new_cases") or []
        staff = p.get("input_owner") == "staff"
        if sender and plan == "run":
            probs.append("%s is a sender and is planned run" % tool)
        if not (ascii_ok(p.get("reason")) and words(p.get("reason")) >= 8):
            probs.append("%s reason is not ASCII of at least eight words" % tool)
        if not cite_ok(p.get("cite")):
            probs.append("%s cite does not resolve: %r" % (tool, p.get("cite")))
        bad_ids = [i for i in ids if i not in cases or cases[i].get("tool") != tool]
        if bad_ids:
            probs.append("%s case_ids not cases of the tool: %r" % (tool, bad_ids[:4]))
        sup = set()
        for c in news:
            if not isinstance(c, dict) or any(f not in c for f in CASE_FIELDS) or not isinstance(c.get("args"), dict):
                probs.append("%s has a new case without its fields" % tool)
                continue
            if c["tool"] != tool or c["case_id"] in cases or c["case_id"] in seen_new:
                probs.append("%s new case %s names another tool or reuses an id" % (tool, c["case_id"]))
            seen_new.add(c["case_id"])
            if c.get("supersedes"):
                sup.add(c["supersedes"])
            vals = list(str_values(c["args"]))
            if any(EMAIL.search(v) or LONG_DIGITS.search(v) for v in vals):
                probs.append("%s new case %s holds an email address or an account-like number" % (tool, c["case_id"]))
            if any(PLACEHOLDER.search(v) for v in vals) and not (c.get("depends_on") or staff):
                probs.append("%s new case %s holds a placeholder input" % (tool, c["case_id"]))
        unrun = sorted(i for i, c in cases.items() if c.get("tool") == tool and i not in done)
        if plan == "run":
            for i in unrun:
                if i not in ids and i not in sup:
                    probs.append("%s: unrun case %s is neither listed nor superseded" % (tool, i))
            for i in ids:
                c = cases.get(i, {})
                vals = list(str_values(c.get("args")))
                if any(PLACEHOLDER.search(v) for v in vals) and not (c.get("depends_on") or staff or i in sup):
                    probs.append("%s: case %s still holds an unresolved placeholder input" % (tool, i))
        elif plan == "preview-only":
            if not ids:
                probs.append("%s preview-only lists no case" % tool)
            if sender and any(cases.get(i, {}).get("expect") != "preview" for i in ids):
                probs.append("%s sender preview-only lists a case that is not a preview" % tool)
            if not sender and "write" not in str(p.get("reason", "")).lower():
                probs.append("%s non-sender preview-only does not name the write" % tool)
        ts = p.get("test_send")
        if ts is not None:
            if not (sender and plan == "preview-only" and isinstance(ts, dict) and ts.get("to") in SEND_TO and ts.get("case_id") in ids):
                probs.append("%s test_send is not one case of a preview-only sender to the tester's own mailbox or chat" % tool)
    return probs


def plant(doc, kind, tools):
    """Mutate a deep copy of the plan in memory; returns None when the plan has no entry the mutation can use."""
    d = copy.deepcopy(doc)
    plans = d.get("plans", [])
    if kind == "sender-run":
        for p in plans:
            if is_sender(tools.get(p.get("tool"), {"name": p.get("tool")})):
                p["plan"] = "run"
                return d
    elif kind == "placeholder":
        for p in plans:
            if p.get("plan") == "run" and not p.get("input_owner"):
                p["new_cases"] = list(p.get("new_cases") or []) + [{"case_id": "W2-ZZ", "tool": p["tool"], "question": "A planted placeholder case", "args": {"x": "<an id>"},
                                                                     "expect": "nonempty", "source_hint": "planted"}]
                return d
    elif kind == "cite":
        if plans:
            plans[0]["cite"] = "no/such/file.py:1"
            return d
    elif kind == "short-reason":
        if plans:
            plans[0]["reason"] = "too short"
            return d
    elif kind == "bad-send":
        for p in plans:
            if is_sender(tools.get(p.get("tool"), {"name": p.get("tool")})) and p.get("case_ids"):
                p["test_send"] = {"case_id": p["case_ids"][0], "to": "a stranger"}
                return d
    return None


def ac1(path):
    not_run, cases, done, tools = load_world()
    doc, why = load_plan(path)
    n = len(doc.get("plans", [])) if isinstance(doc, dict) and isinstance(doc.get("plans"), list) else 0
    print("DENOMINATOR: %d tool(s) graded not_run in BATTERY_GRADED_20261019.json; the plan holds %d entr(y/ies) (%s)" % (len(not_run), n, os.path.basename(path)))
    arm("the plan file exists and reads as JSON", doc is not None, why)
    if doc is None:
        return
    probs = shape_problems(doc, not_run)
    arm("schema, one entry per not_run tool, once each, every field and enum present", not probs, "; ".join(probs[:4]))
    m = copy.deepcopy(doc)
    if m.get("plans"):
        m["plans"] = m["plans"][1:]
    arm("planted: dropping a tool is caught", bool(shape_problems(m, not_run)))
    m = copy.deepcopy(doc)
    if m.get("plans"):
        m["plans"] = m["plans"] + [m["plans"][0]]
    arm("planted: a duplicate tool is caught", bool(shape_problems(m, not_run)))


def ac2(path):
    not_run, cases, done, tools = load_world()
    doc, why = load_plan(path)
    n = len(doc.get("plans", [])) if isinstance(doc, dict) and isinstance(doc.get("plans"), list) else 0
    senders = sorted(t for t in not_run if is_sender(tools.get(t, {"name": t})))
    print("DENOMINATOR: %d plan entr(y/ies) graded against the rules; %d of the %d not_run tools are senders (%s); %d planned case(s) have no result" % (
        n, len(senders), len(not_run), ", ".join(senders[:3]) + (", ..." if len(senders) > 3 else ""), sum(1 for i in cases if i not in done)))
    arm("the plan file exists and reads as JSON", doc is not None, why)
    if doc is None:
        return
    probs = rule_problems(doc, not_run, cases, done, tools)
    arm("senders are never run; every unrun case is listed or superseded; no placeholder, email or account number input; test_send and reasons and cites hold", not probs, "; ".join(probs[:4]))
    for kind, label in (("sender-run", "a sender planned run"), ("placeholder", "a placeholder input in a new case"), ("cite", "a cite that does not exist"),
                        ("short-reason", "a reason under eight words"), ("bad-send", "a test_send to anyone but the tester")):
        m = plant(doc, kind, tools)
        arm("planted: %s is caught" % label, m is not None and bool(rule_problems(m, not_run, cases, done, tools)), "no entry to plant into" if m is None else "")


if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    if cid not in ("w2.AC1", "w2.AC2"):
        print("usage: w2_check.py <w2.AC1|w2.AC2> [plan file]")
        sys.exit(9)
    plan_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PLAN
    (ac1 if cid == "w2.AC1" else ac2)(plan_path)
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    sys.exit(0 if OK and not BAD else 1)
