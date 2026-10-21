"""u1_check.py <id> [deliverable]: the round-27 (workstream GATEWAY) criteria of cell MX-u-1, run from the repository root.
Ids: u1.AC1 (schema, exactly the (tool, adapter) pairs the check derives from the real client_adapter_*.py source, sorted,
firm and field types), u1.AC2 (grounding: cites and evidence resolve in the adapter file, word counts, refusal codes and label
sources appear in the adapter file, no digit run of 7 or more anywhere, the Schwab known answer).
Prints a DENOMINATOR line, one line per arm, then RESULT: PASS|FAIL. ASCII only; python 3.9.
The contract is decompositions/NFRA_MCPINDEX_DECOMP.round27-GATEWAY.md section R27.3 (U1)."""
import copy
import json
import os
import re
import sys

APP = "infra/aws/ec2/opal-gateway/app"
DEFAULT = os.path.join("org", "missions", "D9", "NFRA", "NFRA_MCPINDEX", "deliverables", "0.9.0_WK_NFRA_MCPINDEX~94", "platform_labels.json")
SCHEMA = "gateway_platform_labels/1"
FN_TOOL = {"resolve_account": "client_resolve_account", "get_holdings": "client_get_holdings",
           "get_allocation": "client_get_allocation", "get_fees": "client_get_fees", "get_transactions": "client_get_transactions"}
OK, BAD = [], []


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def read_text(p):
    with open(p, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def is_ascii(s):
    return isinstance(s, str) and all(ord(ch) < 128 for ch in s)


def words(s):
    return len(s.split()) if isinstance(s, str) else 0


def adapter_files():
    names = sorted(n for n in os.listdir(APP) if re.match(r"^client_adapter_[a-z0-9]+\.py$", n))
    return [(n[len("client_adapter_"):-3], "%s/%s" % (APP, n)) for n in names]


def real():
    """From the source: every client adapter file, which of the five tools' functions take a `platform` parameter, the
    firm each binds, a refusal code and the line anchors the synthetic document needs."""
    pairs, info = [], {}
    for adapter, path in adapter_files():
        text = read_text(path)
        lines = text.split("\n")
        firm = None
        m = re.search(r'FIRMS = \(lookup\("([a-z0-9]+)"\)\["key"\],\)', text)
        if m:
            firm = m.group(1)
        def_line = {}
        for fn, tool in FN_TOOL.items():
            dm = re.search(r"^def %s\(([^)]*)\)" % fn, text, re.M)
            if dm and re.search(r"\bplatform\b", dm.group(1)):
                pairs.append((tool, adapter))
                def_line[tool] = text[: dm.start()].count("\n") + 1
        codes = re.findall(r'AdapterRefusal\(\s*"([a-z0-9_]+)"', text)
        info[adapter] = {"path": path, "firm": firm, "n_lines": len(lines), "def_line": def_line, "text": text,
                         "code": "platform_not_source_label" if "platform_not_source_label" in codes else (codes[0] if codes else None),
                         "firms_line": next((i + 1 for i, ln in enumerate(lines) if ln.startswith("FIRMS =")), 1)}
    return {"pairs": sorted(pairs), "info": info}


def schwab_refuses_all(info):
    """Known answer from the source: Schwab's _check_platform has one bare return (the None case), so every other value is refused."""
    text = (info.get("schwab") or {}).get("text", "")
    m = re.search(r"def _check_platform\(platform\)[^\n]*\n((?:[ \t]+[^\n]*\n|\n)+)", text)
    if not m:
        return None
    body = m.group(1)
    return len(re.findall(r"\breturn\b", body)) == 1 and "raise AdapterRefusal" in body


def resolve_cite(ev, adapter_path=None):
    if not is_ascii(ev) or not ev.strip():
        return "cite is empty or not ASCII"
    m = re.match(r"^(.+):([0-9]+)$", ev)
    if not m:
        return "cite %r is not <path>:<line>" % ev
    path, lineno = m.group(1), int(m.group(2))
    if os.path.isabs(path) or ".." in path.replace("\\", "/").split("/"):
        return "cite path %r is absolute or climbs out" % path
    if adapter_path is not None and path != adapter_path:
        return "cite path %r is not the adapter file %s" % (path, adapter_path)
    if not os.path.isfile(path):
        return "file %r does not exist" % path
    n = read_text(path).count("\n") + 1
    if not 1 <= lineno <= n:
        return "line %d is outside %s (%d lines)" % (lineno, path, n)
    return None


def strings_of(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield str(k)
            for s in strings_of(v):
                yield s
    elif isinstance(o, list):
        for v in o:
            for s in strings_of(v):
                yield s


def ac1_problems(doc, exp):
    out = []
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA:
        return ["schema is not %s" % SCHEMA]
    items = doc.get("items")
    if not isinstance(items, list) or not all(isinstance(x, dict) for x in items):
        return ["items is not a list of objects"]
    got = [(x.get("tool"), x.get("adapter")) for x in items]
    want = exp["pairs"]
    missing = sorted(set(want) - set(got))
    extra = sorted(set(got) - set(want), key=str)
    dup = sorted({g for g in got if got.count(g) > 1}, key=str)
    if missing:
        out.append("missing pair(s) %s" % missing[:3])
    if extra:
        out.append("foreign pair(s) %s" % extra[:3])
    if dup:
        out.append("repeated pair(s) %s" % dup[:3])
    if not (missing or extra or dup) and got != sorted(got):
        out.append("items are not sorted by (tool, adapter)")
    for x in items:
        key = (x.get("tool"), x.get("adapter"))
        info = exp["info"].get(x.get("adapter"))
        if info is not None and x.get("firm") != info["firm"]:
            out.append("firm of %s is %r, the adapter binds %r" % (key, x.get("firm"), info["firm"]))
        if not isinstance(x.get("accepts_platform"), bool):
            out.append("accepts_platform of %s is not a boolean" % (key,))
        ls = x.get("label_source")
        if ls is not None and not (isinstance(ls, dict) and isinstance(ls.get("table"), str) and ls["table"].strip()
                                   and isinstance(ls.get("column"), str) and ls["column"].strip()):
            out.append("label_source of %s is neither null nor {table, column}" % (key,))
        rf = x.get("refusals")
        if not (isinstance(rf, list) and all(isinstance(r, dict) and isinstance(r.get("code"), str) and isinstance(r.get("when"), str) for r in rf)):
            out.append("refusals of %s is not a list of {code, when}" % (key,))
        for f in ("platform_meaning", "omit_means", "cite"):
            if not isinstance(x.get(f), str):
                out.append("%s of %s is not a string" % (f, key))
        if not (isinstance(x.get("evidence"), list) and x["evidence"] and all(isinstance(e, str) for e in x["evidence"])):
            out.append("evidence of %s is not a non-empty list of strings" % (key,))
    return out


def ac2_problems(doc, exp):
    out = []
    if not isinstance(doc, dict) or not isinstance(doc.get("items"), list):
        return ["the document is not an object with items"]
    for s in strings_of(doc):
        if re.search(r"[0-9]{7,}", s):
            out.append("a string carries a digit run of 7 or more (account data?): %r" % s[:40])
            break
    for x in doc["items"]:
        if not isinstance(x, dict):
            continue
        key = (x.get("tool"), x.get("adapter"))
        info = exp["info"].get(x.get("adapter"))
        path = info["path"] if info else None
        why = resolve_cite(x.get("cite"), path) if path else "adapter %r is not a client adapter file" % x.get("adapter")
        if why:
            out.append("%s cite: %s" % (key, why))
        ev = x.get("evidence")
        if isinstance(ev, list):
            for e in ev:
                w = resolve_cite(e)
                if w:
                    out.append("%s evidence: %s" % (key, w))
            if not any(isinstance(e, str) and e != x.get("cite") for e in ev):
                out.append("%s evidence holds no entry different from the cite" % (key,))
        for f, need in (("platform_meaning", 8), ("omit_means", 8)):
            v = x.get(f)
            if not is_ascii(v) or words(v) < need:
                out.append("%s %s is not ASCII or has fewer than %d words" % (key, f, need))
        rf = x.get("refusals")
        if isinstance(rf, list):
            for r in rf:
                if not isinstance(r, dict):
                    continue
                if info and not re.search(r'"%s"' % re.escape(str(r.get("code"))), info["text"]):
                    out.append("%s refusal code %r does not appear in %s" % (key, r.get("code"), path))
                if not is_ascii(r.get("when")) or words(r.get("when")) < 5:
                    out.append("%s refusal condition is not ASCII or has fewer than 5 words" % (key,))
        if x.get("accepts_platform") is False and not rf:
            out.append("%s refuses every platform yet lists no refusal" % (key,))
        ls = x.get("label_source")
        if isinstance(ls, dict) and info:
            for f in ("table", "column"):
                if str(ls.get(f)) not in info["text"]:
                    out.append("%s label_source %s %r does not appear in %s" % (key, f, ls.get(f), path))
    if schwab_refuses_all(exp["info"]):
        for x in doc["items"]:
            if isinstance(x, dict) and x.get("adapter") == "schwab" and x.get("accepts_platform") is not False:
                out.append("%s: the Schwab _check_platform refuses every non-null value (one bare return), so accepts_platform must be false" % ((x.get("tool"), "schwab"),))
    return out


def synthetic(exp):
    """A clean document built from the source: cites on the real def lines, evidence on the FIRMS line, a refusal code the file raises."""
    items = []
    for tool, adapter in exp["pairs"]:
        info = exp["info"][adapter]
        cite_line = info["def_line"][tool]
        items.append({"tool": tool, "adapter": adapter, "firm": info["firm"], "accepts_platform": adapter != "schwab",
                      "platform_meaning": "the platform argument is a label this adapter checks against its own source before any read",
                      "label_source": None,
                      "omit_means": "when platform is omitted the adapter reads every account of the firm without any label filter",
                      "refusals": [{"code": info["code"], "when": "a platform value that the adapter does not accept is passed"}],
                      "cite": "%s:%d" % (info["path"], cite_line),
                      "evidence": ["%s:%d" % (info["path"], info["firms_line"])]})
    return {"schema": SCHEMA, "items": items}


def load_deliverable(path):
    if not os.path.isfile(path):
        return None, "deliverable %s absent" % path
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return json.load(fh), None
    except (ValueError, OSError) as exc:
        return None, "deliverable %s unreadable: %s" % (path, exc)


def controls(fn, exp, mutants):
    """Each mutant is planted into a clean synthetic document and must be refused for the planted defect itself (its tag appears in a problem)."""
    good = synthetic(exp)
    base = fn(good, exp)
    arm("control: a clean synthetic document passes", base == [], "; ".join(base)[:300])
    for name, tag, mut in mutants:
        d = copy.deepcopy(good)
        mut(d)
        probs = fn(d, exp)
        arm("planted negative refused for its defect: %s" % name, any(tag in p for p in probs), "problems: %s" % ("; ".join(probs)[:200] or "none"))


def first_of(d, adapter):
    return next(x for x in d["items"] if x["adapter"] == adapter)


def ac1(path):
    exp = real()
    doc, err = load_deliverable(path)
    n_ad = len({a for _, a in exp["pairs"]})
    print("DENOMINATOR: %d (tool, adapter) pairs derived from the %d client adapter files that take a platform argument (5 tools x %d adapters: %s); 9 planted negatives" % (
        len(exp["pairs"]), len(exp["info"]), n_ad, ", ".join(sorted({a for _, a in exp["pairs"]}))))
    arm("the source yields 5 tools x at least 1 adapter with a bound firm each", len(exp["pairs"]) >= 5 and all(v["firm"] for v in exp["info"].values()),
        "pairs %d, firms %r" % (len(exp["pairs"]), {a: v["firm"] for a, v in exp["info"].items()}))

    def drop(d):
        d["items"].pop(3)

    def twice(d):
        d["items"].append(copy.deepcopy(d["items"][0]))

    def swap(d):
        d["items"][0], d["items"][5] = d["items"][5], d["items"][0]

    controls(ac1_problems, exp, [
        ("wrong schema", "schema is not", lambda d: d.update(schema="gateway_platform_labels/0")),
        ("a pair dropped", "missing pair", drop),
        ("a pair twice", "repeated pair", twice),
        ("a foreign tool", "foreign pair", lambda d: d["items"][0].update(tool="client_no_such_tool")),
        ("a foreign adapter", "foreign pair", lambda d: d["items"][0].update(adapter="nosuchvendor")),
        ("items out of order", "not sorted", swap),
        ("a wrong firm", "firm of", lambda d: d["items"][0].update(firm="cottonwood" if d["items"][0]["firm"] != "cottonwood" else "inflection")),
        ("accepts_platform as a string", "accepts_platform", lambda d: d["items"][0].update(accepts_platform="yes")),
        ("a label_source without a column", "label_source", lambda d: d["items"][0].update(label_source={"table": "fact_x"}))])
    if err:
        arm("deliverable present and readable", False, err)
        return
    probs = ac1_problems(doc, exp)
    arm("the deliverable holds exactly the derived (tool, adapter) pairs, sorted, with the firm each adapter binds and well-typed fields", not probs, "; ".join(probs)[:600])


def ac2(path):
    exp = real()
    doc, err = load_deliverable(path)
    n = len(doc["items"]) if isinstance(doc, dict) and isinstance(doc.get("items"), list) else 0
    print("DENOMINATOR: %d item(s) in the deliverable to ground against the adapter files; each cite is <path>:<line> of its own adapter file, evidence holds a different line, meaning and omit text of 8 ASCII words or more, refusal codes and label sources found in the file, no digit run of 7 or more; 11 planted negatives" % n)
    arm("the Schwab known answer is readable from the source (one bare return in _check_platform)", schwab_refuses_all(exp["info"]) is True)

    def other_file_cite(d):
        x = d["items"][0]
        other = next(v["path"] for a, v in exp["info"].items() if a != x["adapter"])
        x["cite"] = "%s:%s" % (other, x["cite"].rsplit(":", 1)[1])

    controls(ac2_problems, exp, [
        ("a cite in another adapter's file", "is not the adapter file", other_file_cite),
        ("a cite past the end of the file", "is outside", lambda d: d["items"][0].update(cite="%s:999999" % exp["info"][d["items"][0]["adapter"]]["path"])),
        ("evidence equal to the cite only", "no entry different", lambda d: d["items"][0].update(evidence=[d["items"][0]["cite"]])),
        ("evidence naming a missing file", "does not exist", lambda d: d["items"][0].update(evidence=["workflows/gateway_battery/no_such_file_u1.py:1"])),
        ("a platform meaning of three words", "platform_meaning", lambda d: d["items"][0].update(platform_meaning="a custodian label")),
        ("an omit text that is not ASCII", "omit_means", lambda d: d["items"][0].update(omit_means="when platform is omitted the adapter reads every account of the firm caf" + chr(233))),
        ("a refusal code the file never raises", "does not appear in", lambda d: d["items"][0]["refusals"][0].update(code="no_such_code_u1")),
        ("a refusal condition of three words", "refusal condition", lambda d: d["items"][0]["refusals"][0].update(when="bad platform value")),
        ("a digit run of eight in a text", "digit run", lambda d: d["items"][0].update(omit_means="when platform is omitted the adapter reads account 12345678 of the firm without a filter")),
        ("accepts_platform false with no refusal", "lists no refusal", lambda d: (d["items"][0].update(accepts_platform=False), d["items"][0].update(refusals=[]))),
        ("Schwab marked as accepting a platform", "Schwab _check_platform", lambda d: first_of(d, "schwab").update(accepts_platform=True))])
    if err:
        arm("deliverable present and readable", False, err)
        return
    probs = ac2_problems(doc, exp)
    arm("every cite and evidence entry resolves in the adapter file, texts are long enough, refusal codes and label sources appear in the file, no account data, Schwab refuses all", not probs, "; ".join(probs)[:600])


CHECKS = {"u1.AC1": ac1, "u1.AC2": ac2}

if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    if cid not in CHECKS:
        print("usage: u1_check.py <%s> [deliverable]" % "|".join(sorted(CHECKS)))
        sys.exit(9)
    CHECKS[cid](sys.argv[2] if len(sys.argv) > 2 else DEFAULT)
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    sys.exit(0 if OK and not BAD else 1)
