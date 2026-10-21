"""u2_check.py <id> [deliverable]: the round-27 (workstream GATEWAY) criteria of cell MX-u-2, run from the repository root.
Ids: u2.AC1 (schema, the feed and its newest partition equal the CRO census, the lag equals the round-26 report, producer kind
from the enum, the owner is a project of org/projects/),
u2.AC2 (the producer and schedule cites and at least two evidence entries resolve to a file and a line; the none-found form
needs three; the gap cause is a sentence of 12 words or more; the worker's one surprise row stands in the channel file).
Prints a DENOMINATOR line, one line per arm, then RESULT: PASS|FAIL. ASCII only; python 3.9.
The contract is decompositions/NFRA_MCPINDEX_DECOMP.round27-GATEWAY.md section R27.3 (U2)."""
import copy
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R27 = os.path.normpath(os.path.join(HERE, ".."))
DELIV = os.path.normpath(os.path.join(R27, "..", ".."))
CENSUS = os.path.join(DELIV, "4.0.0_SA_CRO~Y", "census.json")
REPORT = os.path.join(DELIV, "2.0.0_SA_COO~MI", "round26", "evidence", "ROUND26_REPORT.md")
CHANNEL = os.environ.get("U2_CHANNEL") or "org/missions/D9/NFRA/NFRA_MCPINDEX/surprise-channel/investigations/INVESTIGATION_v1.md"   # U2_CHANNEL: the issuer's scratch reference run only
DEFAULT = os.path.join("org", "missions", "D9", "NFRA", "NFRA_MCPINDEX", "deliverables", "0.9.0_WK_NFRA_MCPINDEX~95", "commonwealth_producer.json")
DECOMP = "org/missions/D9/NFRA/NFRA_MCPINDEX/decompositions/NFRA_MCPINDEX_DECOMP.round27-GATEWAY.md"
SCHEMA = "gateway_commonwealth_producer/1"
KINDS = ("lambda", "script", "glue", "ecs-task", "terraform-only", "manual", "other")
NONE_FOUND = "none-found"
FEED_ROOT = "commonwealth/cottonwood/silver/"
ROW_ID = re.compile(r"^NFRA_MCPINDEX-Z-W95-S[0-9]+$")
OK, BAD = [], []


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def jload(p):
    with open(p, encoding="utf-8", errors="replace") as fh:
        return json.load(fh)


def tload(p):
    with open(p, encoding="utf-8", errors="replace") as fh:
        return fh.read()


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
    """From the CRO census: the catalogued Commonwealth silver tables (their common prefix, their newest partition);
    from the round-26 report: the trading days behind."""
    entries = jload(CENSUS)
    cat = [e for e in entries if e.get("src") == "catalog" and e.get("bucket") == "opal-data-assets" and str(e.get("prefix", "")).startswith(FEED_ROOT)]
    common = os.path.commonprefix([e["prefix"] for e in cat]) if cat else ""
    common = common[: common.rfind("/") + 1] if common else ""
    dates = [e["newest_partition"] for e in cat if e.get("newest_partition")]
    days = None
    if os.path.isfile(REPORT):
        m = re.search(r"([0-9]+) trading days behind", tload(REPORT)) or re.search(r"([0-9]+) trading days", tload(REPORT))
        days = int(m.group(1)) if m else None
    return {"feed": ("opal-data-assets", common) if common else None, "newest": max(dates) if dates else None,
            "days": days, "n_tables": len(cat)}


def ac1_problems(doc, exp):
    out = []
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA:
        return ["schema is not %s" % SCHEMA]
    feed = doc.get("feed")
    if not isinstance(feed, dict) or (feed.get("bucket"), feed.get("prefix")) != exp["feed"]:
        out.append("feed %r is not the catalogued Commonwealth prefix %r" % (feed, exp["feed"]))
    if doc.get("newest_partition") != exp["newest"]:
        out.append("newest_partition %r is not the census value %r" % (doc.get("newest_partition"), exp["newest"]))
    td = doc.get("trading_days_behind")
    if isinstance(td, bool) or td != exp["days"]:
        out.append("trading_days_behind %r is not the round-26 report value %r" % (td, exp["days"]))
    prod, sch = doc.get("producer"), doc.get("schedule")
    if not isinstance(prod, dict) or prod.get("kind") not in KINDS:
        out.append("producer.kind %r is not one of %s" % ((prod or {}).get("kind") if isinstance(prod, dict) else None, "/".join(KINDS)))
    elif not (isinstance(prod.get("name"), str) and prod["name"].strip() and is_ascii(prod["name"])):
        out.append("producer.name is empty or not ASCII")
    if not isinstance(sch, dict) or not (isinstance(sch.get("expression"), str) and sch["expression"].strip() and is_ascii(sch["expression"])):
        out.append("schedule.expression is empty or not ASCII")
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


def row_problems(rows):
    """The worker's surprise row: among the rows with an id of slot 95, at least one is a valid gap row."""
    mine = [r for r in rows if isinstance(r, dict) and ROW_ID.match(str(r.get("id", "")))]
    if not mine:
        return ["no surprise row with an id NFRA_MCPINDEX-Z-W95-S<k> in the channel file"]
    why = []
    for r in mine:
        bad = []
        if r.get("class") != "OBSERVATION":
            bad.append("class is not OBSERVATION")
        if r.get("hazard_standing") != "INERT":
            bad.append("hazard_standing is not INERT")
        if r.get("disarm_owner") != "2.0.0_SA_COO~MI":
            bad.append("disarm_owner is not 2.0.0_SA_COO~MI")
        ol = r.get("one_line")
        if not (isinstance(ol, str) and "2026-06-23" in ol and re.search(r"(?<![0-9])83(?![0-9])", ol)):
            bad.append("one_line does not carry 2026-06-23 and 83")
        gr = r.get("grounding")
        if not (isinstance(gr, dict) and gr.get("status") == "GROUNDED"):
            bad.append("grounding.status is not GROUNDED")
        if not bad:
            return []
        why.append("%s: %s" % (r.get("id"), ", ".join(bad)))
    return ["; ".join(why)]


def channel_rows():
    if not os.path.isfile(CHANNEL):
        return []
    rows = []
    for m in re.finditer(r"```json\s*\n(.*?)\n```", tload(CHANNEL), re.S):
        try:
            obj = json.loads(m.group(1))
        except ValueError:
            continue
        rows += obj if isinstance(obj, list) else [obj]
    return rows


def ac2_problems(doc, exp, rows):
    out = []
    if not isinstance(doc, dict):
        return ["the document is not an object"]
    prod, sch = doc.get("producer"), doc.get("schedule")
    for label, node in (("producer", prod), ("schedule", sch)):
        why = resolve_cite(node.get("cite")) if isinstance(node, dict) else "%s is not an object" % label
        if why:
            out.append("%s.cite: %s" % (label, why))
    ev = doc.get("evidence")
    none_found = isinstance(prod, dict) and prod.get("name") == NONE_FOUND
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
    if none_found and isinstance(prod, dict) and prod.get("kind") not in ("manual", "other"):
        out.append("the none-found form needs producer.kind manual or other")
    cause = doc.get("gap_cause")
    if not is_ascii(cause) or words(cause) < 12:
        out.append("gap_cause is not ASCII or has fewer than 12 words")
    out += row_problems(rows)
    return out


def synthetic(exp):
    """A clean document built from the real values; its cites point at files every worktree holds (this order's decomposition)."""
    return {"schema": SCHEMA,
            "feed": {"bucket": exp["feed"][0], "prefix": exp["feed"][1]},
            "newest_partition": exp["newest"], "trading_days_behind": exp["days"],
            "producer": {"kind": "manual", "name": "synthetic-landing", "cite": DECOMP + ":10"},
            "schedule": {"expression": "none: a closed delivery landed by hand", "cite": DECOMP + ":12"},
            "owner": "OPAL_ASSETS",
            "gap_cause": "the feed is one closed vendor delivery that a person landed once and nothing schedules a later partition to follow it",
            "evidence": [DECOMP + ":14", DECOMP + ":16"]}


def synthetic_row():
    return {"id": "NFRA_MCPINDEX-Z-W95-S1", "class": "OBSERVATION", "hazard_standing": "INERT", "disarm_owner": "2.0.0_SA_COO~MI",
            "one_line": "Commonwealth silver newest partition 2026-06-23, 83 trading days behind the frontier",
            "grounding": {"status": "GROUNDED", "evidence": [DECOMP + ":10"]}}


def load_deliverable(path):
    if not os.path.isfile(path):
        return None, "deliverable %s absent" % path
    try:
        return jload(path), None
    except (ValueError, OSError) as exc:
        return None, "deliverable %s unreadable: %s" % (path, exc)


def ac1(path):
    exp = real()
    doc, err = load_deliverable(path)
    print("DENOMINATOR: the Commonwealth feed %s and its newest partition %s read from the CRO census (%d catalogued tables), %s trading days behind read from the round-26 report; 6 planted negatives" % (
        "/".join(exp["feed"] or ("?", "?")), exp["newest"], exp["n_tables"], exp["days"]))
    arm("the census holds the Commonwealth tables and the report holds the lag", bool(exp["feed"]) and bool(exp["newest"]) and exp["n_tables"] >= 1 and exp["days"] is not None, "read %r" % (exp,))
    good = synthetic(exp)
    arm("control: a clean synthetic document passes", ac1_problems(good, exp) == [], "; ".join(ac1_problems(good, exp))[:300])
    for name, mut in [
            ("wrong schema", lambda d: d.update(schema="gateway_commonwealth_producer/0")),
            ("feed prefix altered", lambda d: d["feed"].update(prefix="commonwealth/cottonwood/bronze/")),
            ("newest partition altered", lambda d: d.update(newest_partition="2026-10-16")),
            ("lag of 78 trading days", lambda d: d.update(trading_days_behind=78)),
            ("a producer kind outside the enum", lambda d: d["producer"].update(kind="cron")),
            ("an owner that is not a project", lambda d: d.update(owner="NOT_A_PROJECT_U2"))]:
        d = copy.deepcopy(good)
        mut(d)
        arm("planted negative refused: %s" % name, bool(ac1_problems(d, exp)))
    if err:
        arm("deliverable present and readable", False, err)
        return
    probs = ac1_problems(doc, exp)
    arm("the deliverable names the census feed, its newest partition, the report's lag, a producer kind from the enum and a project owner", not probs, "; ".join(probs)[:600])


def ac2(path):
    exp = real()
    doc, err = load_deliverable(path)
    rows = channel_rows()
    n = len(doc.get("evidence", [])) if isinstance(doc, dict) and isinstance(doc.get("evidence"), list) else 0
    print("DENOMINATOR: producer cite, schedule cite and %d evidence entr(y/ies) in the deliverable to ground, each <path>:<line> of an existing repository file; two evidence entries (three in the none-found form); gap cause at least 12 ASCII words; the worker's surprise row among %d channel rows; 9 planted negatives" % (n, len(rows)))
    good, grow = synthetic(exp), [synthetic_row()]
    arm("control: a clean synthetic document and row pass", ac2_problems(good, exp, grow) == [], "; ".join(ac2_problems(good, exp, grow))[:300])

    def none_found_two(d):
        d["producer"].update(kind="other", name=NONE_FOUND)

    for name, mut, rmut in [
            ("a producer cite naming a missing file", lambda d: d["producer"].update(cite="workflows/gateway_battery/no_such_file_u2.py:1"), None),
            ("a schedule cite past the end of the file", lambda d: d["schedule"].update(cite=DECOMP + ":999999"), None),
            ("only one evidence entry", lambda d: d.update(evidence=d["evidence"][:1]), None),
            ("an evidence entry repeated", lambda d: d.update(evidence=[d["evidence"][0], d["evidence"][0]]), None),
            ("the none-found form with only two evidence entries", none_found_two, None),
            ("gap cause shorter than 12 words", lambda d: d.update(gap_cause="a closed delivery with nothing after it"), None),
            ("no surprise row of slot 95", None, lambda r: r.update(id="NFRA_MCPINDEX-Z-W96-S1")),
            ("a surprise row without the measured gap", None, lambda r: r.update(one_line="the Commonwealth feed is stale")),
            ("a surprise row that is not GROUNDED", None, lambda r: r.update(grounding={"status": "INFERRED"}))]:
        d, rr = copy.deepcopy(good), copy.deepcopy(grow)
        if mut:
            mut(d)
        if rmut:
            rmut(rr[0])
        arm("planted negative refused: %s" % name, bool(ac2_problems(d, exp, rr)))
    if err:
        arm("deliverable present and readable", False, err)
        return
    probs = ac2_problems(doc, exp, rows)
    arm("the producer and schedule cites and the evidence entries resolve, the none-found form has three, the gap cause is a sentence of 12 words or more, and the surprise row stands", not probs, "; ".join(probs)[:600])


CHECKS = {"u2.AC1": ac1, "u2.AC2": ac2}

if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    if cid not in CHECKS:
        print("usage: u2_check.py <%s> [deliverable]" % "|".join(sorted(CHECKS)))
        sys.exit(9)
    CHECKS[cid](sys.argv[2] if len(sys.argv) > 2 else DEFAULT)
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    sys.exit(0 if OK and not BAD else 1)
