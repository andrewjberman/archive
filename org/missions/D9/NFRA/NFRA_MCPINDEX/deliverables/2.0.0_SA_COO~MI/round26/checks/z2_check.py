"""z2_check.py <id> [deliverable]: the round-26 (workstream GATEWAY) criteria of cell MX-z-2, run from the repository root.
Ids: z2.AC1 (schema, producer and copy prefixes equal the real census, enums, owners are project codes, lag days),
z2.AC2 (the copier and schedule cites and at least two evidence entries resolve to a file and a line; the none-found form
needs three evidence entries; lag cause is a sentence of 8 words or more).
Prints a DENOMINATOR line, one line per arm, then RESULT: PASS|FAIL. ASCII only; python 3.9.
The contract is decompositions/NFRA_MCPINDEX_DECOMP.round26-GATEWAY.md section R26.3 (Z2)."""
import copy
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R26 = os.path.normpath(os.path.join(HERE, ".."))
DELIV = os.path.normpath(os.path.join(R26, "..", ".."))
CENSUS = os.path.join(DELIV, "4.0.0_SA_CRO~Y", "census.json")
DEFAULT = os.path.join("org", "missions", "D9", "NFRA", "NFRA_MCPINDEX", "deliverables", "0.9.0_WK_NFRA_MCPINDEX~91", "eclipse_copier.json")
DECOMP = "org/missions/D9/NFRA/NFRA_MCPINDEX/decompositions/NFRA_MCPINDEX_DECOMP.round26-GATEWAY.md"
SCHEMA = "gateway_eclipse_copier/1"
KINDS = ("lambda", "script", "glue", "ecs-task", "terraform-only", "other")
NONE_FOUND = "none-found"
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


def project_exists(code):
    """A project code of org/projects/: read from the git tree, so a sparse worktree does not hide it."""
    if not (isinstance(code, str) and re.match(r"^[A-Z][A-Z0-9]*_[A-Z0-9_]+$", code)):
        return False
    path = "org/projects/%s.json" % code
    if os.path.isfile(path):
        return True
    return subprocess.run(["git", "cat-file", "-e", "HEAD:" + path], capture_output=True).returncode == 0


def real():
    """From the CRO census: the producer entry (live-extra, opal-data-inf silver/eclipse/) and the common prefix of the catalogued Eclipse tables."""
    entries = jload(CENSUS)
    prod = [e for e in entries if e.get("src") == "live-extra" and e.get("bucket") == "opal-data-inf" and e.get("prefix") == "silver/eclipse/"]
    cat = [e for e in entries if e.get("src") == "catalog" and e.get("bucket") == "opal-data-assets" and str(e.get("prefix", "")).startswith("eclipse/")]
    common = os.path.commonprefix([e["prefix"] for e in cat]) if cat else ""
    common = common[: common.rfind("/") + 1] if common else ""
    return {"producer": (prod[0]["bucket"], prod[0]["prefix"]) if prod else None,
            "copy": ("opal-data-assets", common) if common else None, "n_copy_tables": len(cat)}


def ac1_problems(doc, exp):
    out = []
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA:
        return ["schema is not %s" % SCHEMA]
    prod, cp = doc.get("producer"), doc.get("copy")
    if not isinstance(prod, dict) or (prod.get("bucket"), prod.get("prefix")) != exp["producer"]:
        out.append("producer %r is not the census producer %r" % (prod, exp["producer"]))
    elif not project_exists(prod.get("owner_project")):
        out.append("producer.owner_project %r is not a project of org/projects/" % prod.get("owner_project"))
    if not isinstance(cp, dict) or (cp.get("bucket"), cp.get("prefix")) != exp["copy"]:
        out.append("copy %r is not the catalogued Eclipse prefix %r" % (cp, exp["copy"]))
    cop, sch = doc.get("copier"), doc.get("schedule")
    if not isinstance(cop, dict) or cop.get("kind") not in KINDS:
        out.append("copier.kind %r is not one of %s" % ((cop or {}).get("kind") if isinstance(cop, dict) else None, "/".join(KINDS)))
    elif not (isinstance(cop.get("name"), str) and cop["name"].strip() and is_ascii(cop["name"])):
        out.append("copier.name is empty or not ASCII")
    if not isinstance(sch, dict) or not (isinstance(sch.get("expression"), str) and sch["expression"].strip() and is_ascii(sch["expression"])):
        out.append("schedule.expression is empty or not ASCII")
    lag = doc.get("lag")
    if not isinstance(lag, dict) or lag.get("trading_days") != 1 or isinstance(lag.get("trading_days"), bool):
        out.append("lag.trading_days is not the integer 1")
    if not project_exists(doc.get("owner")):
        out.append("owner %r is not a project of org/projects/" % doc.get("owner"))
    return out


def resolve_cite(ev):
    if not is_ascii(ev) or not ev.strip():
        return "cite is empty or not ASCII"
    m = re.match(r"^(.+):([0-9]+)$", ev)
    if not m:
        return "cite %r is not <path>:<line>" % ev
    path, lineno = m.group(1), int(m.group(2))
    if os.path.isabs(path) or ".." in path.replace("\\", "/").split("/"):
        return "cite path %r is absolute or climbs out" % path
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
    cop, sch, lag = doc.get("copier"), doc.get("schedule"), doc.get("lag")
    for label, node in (("copier", cop), ("schedule", sch)):
        why = resolve_cite(node.get("cite")) if isinstance(node, dict) else "%s is not an object" % label
        if why:
            out.append("%s.cite: %s" % (label, why))
    ev = doc.get("evidence")
    none_found = isinstance(cop, dict) and cop.get("name") == NONE_FOUND
    need = 3 if none_found else 2
    if not isinstance(ev, list) or len(ev) < need or not all(isinstance(x, str) for x in ev):
        out.append("evidence is not a list of at least %d strings%s" % (need, " (the none-found form)" if none_found else ""))
    else:
        if len(set(ev)) != len(ev):
            out.append("an evidence entry is repeated")
        for x in ev:
            why = resolve_cite(x)
            if why:
                out.append("evidence: " + why)
    if none_found and isinstance(cop, dict) and cop.get("kind") not in ("terraform-only", "other"):
        out.append("the none-found form needs copier.kind terraform-only or other")
    cause = lag.get("cause") if isinstance(lag, dict) else None
    if not is_ascii(cause) or words(cause) < 8:
        out.append("lag.cause is not ASCII or has fewer than 8 words")
    return out


def synthetic(exp):
    """A clean document built from the census values; its cites point at files every worktree holds (this order's decomposition)."""
    return {"schema": SCHEMA,
            "producer": {"bucket": exp["producer"][0], "prefix": exp["producer"][1], "owner_project": "OPAL_ASSETS"},
            "copy": {"bucket": exp["copy"][0], "prefix": exp["copy"][1]},
            "copier": {"kind": "lambda", "name": "synthetic-mirror", "cite": DECOMP + ":10"},
            "schedule": {"expression": "cron(5 13 * * ? *)", "cite": DECOMP + ":12"},
            "lag": {"trading_days": 1, "cause": "the first mirror slot runs before the producer lands its partition for the day"},
            "owner": "OPAL_ASSETS",
            "evidence": [DECOMP + ":14", DECOMP + ":16"]}


def load_deliverable(path):
    if not os.path.isfile(path):
        return None, "deliverable %s absent" % path
    try:
        return jload(path), None
    except (ValueError, OSError) as exc:
        return None, "deliverable %s unreadable: %s" % (path, exc)


def controls(fn, exp, mutants):
    good = synthetic(exp)
    arm("control: a clean synthetic document passes", fn(good, exp) == [], "; ".join(fn(good, exp))[:300])
    for name, mut in mutants:
        d = copy.deepcopy(good)
        mut(d)
        arm("planted negative refused: %s" % name, bool(fn(d, exp)))


def ac1(path):
    exp = real()
    doc, err = load_deliverable(path)
    print("DENOMINATOR: producer %s and the catalogued copy %s read from the CRO census (%d catalogued Eclipse tables); 6 planted negatives" % (
        "/".join(exp["producer"] or ("?", "?")), "/".join(exp["copy"] or ("?", "?")), exp["n_copy_tables"]))
    arm("the census holds the producer entry and the catalogued Eclipse tables", bool(exp["producer"]) and bool(exp["copy"]) and exp["n_copy_tables"] >= 1, "read %r" % (exp,))
    controls(ac1_problems, exp, [
        ("wrong schema", lambda d: d.update(schema="gateway_eclipse_copier/0")),
        ("producer prefix altered", lambda d: d["producer"].update(prefix="silver/orion/")),
        ("copy prefix altered", lambda d: d["copy"].update(prefix="eclipse/inflection/bronze/")),
        ("a copier kind outside the enum", lambda d: d["copier"].update(kind="cron")),
        ("an owner that is not a project", lambda d: d.update(owner="NOT_A_PROJECT_Z2")),
        ("lag of two trading days", lambda d: d["lag"].update(trading_days=2))])
    if err:
        arm("deliverable present and readable", False, err)
        return
    probs = ac1_problems(doc, exp)
    arm("the deliverable names the census producer and copy, a copier kind from the enum, project owners and one trading day of lag", not probs, "; ".join(probs)[:600])


def ac2(path):
    exp = real()
    doc, err = load_deliverable(path)
    n = len(doc.get("evidence", [])) if isinstance(doc, dict) and isinstance(doc.get("evidence"), list) else 0
    print("DENOMINATOR: copier cite, schedule cite and %d evidence entr(y/ies) in the deliverable to ground, each <path>:<line> of an existing repository file; two evidence entries (three in the none-found form); lag cause at least 8 ASCII words; 7 planted negatives" % n)

    def none_found_two(d):
        d["copier"].update(kind="other", name=NONE_FOUND)

    controls(ac2_problems, exp, [
        ("a copier cite naming a missing file", lambda d: d["copier"].update(cite="workflows/gateway_battery/no_such_file_z2.py:1")),
        ("a schedule cite past the end of the file", lambda d: d["schedule"].update(cite=DECOMP + ":999999")),
        ("only one evidence entry", lambda d: d.update(evidence=d["evidence"][:1])),
        ("an evidence entry repeated", lambda d: d.update(evidence=[d["evidence"][0], d["evidence"][0]])),
        ("the none-found form with only two evidence entries", none_found_two),
        ("lag cause shorter than 8 words", lambda d: d["lag"].update(cause="runs early")),
        ("lag cause not ASCII", lambda d: d["lag"].update(cause="the first mirror slot runs before the producer lands its partition caf" + chr(233)))])
    if err:
        arm("deliverable present and readable", False, err)
        return
    probs = ac2_problems(doc, exp)
    arm("the copier and schedule cites and the evidence entries resolve, the none-found form has three, and the lag cause is a sentence of 8 words or more", not probs, "; ".join(probs)[:600])


CHECKS = {"z2.AC1": ac1, "z2.AC2": ac2}

if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    if cid not in CHECKS:
        print("usage: z2_check.py <%s> [deliverable]" % "|".join(sorted(CHECKS)))
        sys.exit(9)
    CHECKS[cid](sys.argv[2] if len(sys.argv) > 2 else DEFAULT)
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    sys.exit(0 if OK and not BAD else 1)
