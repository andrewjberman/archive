"""ADVI_FIRMBKTS round 9 graders, issuer 2.0.0_SA_COO~B1.

  door6census --file F                      FB-p-1: the live consumer census of the Door 6 marker key, writers named or not.
  door6retire --file F                      FB-p-2: the Door 6 retirement act (rule gone, marker copied then gone, writer stopped).
  planq --file F --first N --last M --kind Q|NOMOVE
                                            FB-p-3, FB-p-4: the Inflection plan's entries N..M, each answered or carried with an owner.
  addendum --file F                         FB-p-5: S60 entered into the Cottonwood plan as a retire candidate, the delete marked Andrew's.
  key23 --file F                            FB-p-6: the 23rd named key on the floor day that drew no new version, named with why.
  triage --file F --ids IDS_FILE            FB-p-7, FB-p-8, FB-p-9: a verdict and its evidence for each of a fixed list of OPEN rows.
Plain ASCII; exit 0 on a pass. Proves SHAPE and read-only discipline, never that a finding is true.
"""
import argparse
import json
import re
import sys

CLAIMS = ("measured", "inferred", "held", "absent")
WRITE_VERBS = re.compile(
    r"(\s(put|delete|create|update|modify|attach|detach|start|stop|run|terminate|enable|disable|register|deregister|tag|untag|send|publish|invoke)-[a-z-]+)"
    r"|(\ss3(api)?\s+(cp|mv|rm|sync|put-object|delete-object)\b)|(\sterraform\s+(apply|destroy|import)\b)|(get-secret-value)")
ID_TOKEN = re.compile(r"(?<![0-9A-Za-z])[A-Za-z]?[0-9]{9,}(?![0-9A-Za-z])")
OK_TOKENS = ("313476888478",)


def _load(path, tag):
    try:
        raw = open(path, encoding="utf-8").read()
        return raw, json.loads(raw)
    except (OSError, ValueError) as e:
        print("%s: FAIL cannot read %s: %s" % (tag, path, type(e).__name__))
        return None, None


def _common(raw, d, keys):
    p = []
    if not isinstance(d, dict):
        return ["the record is not an object"]
    bad = [m for m in ID_TOKEN.findall(raw) if m not in OK_TOKENS]
    if bad:
        p.append("%d id-shaped token(s) of nine or more digits (replace with <id>)" % len(bad))
    miss = [k for k in keys if k not in d]
    if miss:
        return p + ["missing " + ",".join(miss)]
    if d["claim"] not in CLAIMS:
        p.append("claim outside the four")
    return p


def _calls_ok(d, p):
    c = d.get("calls")
    if not isinstance(c, list) or not c or not all(isinstance(x, str) and x.strip() for x in c):
        p.append("calls must be a non-empty list of strings")
    elif any(WRITE_VERBS.search(" " + x) for x in c):
        p.append("a call carries a write verb")


def _den_ok(d, p):
    den = d.get("denominators")
    if not isinstance(den, dict) or not den or not all(isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in den.values()) or not any(v > 0 for v in den.values()):
        p.append("denominators must be integers with at least one above zero")


def _s(x):
    return isinstance(x, str) and bool(x.strip())


def _finish(tag, p, ok_line):
    if p:
        print("%s: FAIL " % tag + "; ".join(p[:6]))
        return 1
    print(ok_line)
    return 0


def door6census(a):
    raw, d = _load(a.file, "DOOR6CENSUS")
    if d is None:
        return 1
    p = _common(raw, d, ("order", "read_at", "key", "calls", "denominators", "consumers", "writers", "writer_determined", "not_read", "claim"))
    if p and p[-1].startswith("missing"):
        print("DOOR6CENSUS: FAIL " + "; ".join(p))
        return 1
    _calls_ok(d, p)
    _den_ok(d, p)
    if "pipeline-complete.json" not in str(d["key"]):
        p.append("key must be the Door 6 marker")
    cs = d["consumers"]
    kinds = ("s3_notification", "eventbridge_rule", "code_reader", "iam_fence", "other")
    if not isinstance(cs, list) or not cs:
        p.append("consumers must be a non-empty list")
    else:
        for c in cs:
            if not isinstance(c, dict) or c.get("kind") not in kinds or c.get("status") not in ("RETIRING", "LIVE_OTHER", "ABSENT_LIVE") or not _s(c.get("name")) or not _s(c.get("evidence")):
                p.append("each consumer needs kind, name, status (RETIRING, LIVE_OTHER or ABSENT_LIVE) and evidence")
                break
    ws = d["writers"]
    if not isinstance(ws, list) or any(not isinstance(w, dict) or not _s(w.get("name")) or not _s(w.get("evidence")) for w in ws):
        p.append("each writer needs a name and evidence")
    elif d["writer_determined"] is True and not ws:
        p.append("writer_determined true needs at least one writer")
    elif d["writer_determined"] is False and not _s(d.get("writer_note")):
        p.append("writer_determined false needs a writer_note saying what was read")
    elif d["writer_determined"] not in (True, False):
        p.append("writer_determined must be true or false")
    if not isinstance(d["not_read"], list):
        p.append("not_read must be a list")
    live = sum(1 for c in cs if isinstance(c, dict) and c.get("status") == "LIVE_OTHER") if isinstance(cs, list) else 0
    return _finish("DOOR6CENSUS", p, "DOOR6CENSUS: OK consumers=%d live_other=%d" % (len(cs) if isinstance(cs, list) else 0, live))


def door6retire(a):
    raw, d = _load(a.file, "DOOR6RETIRE")
    if d is None:
        return 1
    p = _common(raw, d, ("order", "read_at", "census_ref", "decision", "steps", "pair", "rollback", "ledger_closed", "claim"))
    if p and p[-1].startswith("missing"):
        print("DOOR6RETIRE: FAIL " + "; ".join(p))
        return 1
    if not _s(d["census_ref"]):
        p.append("census_ref must name the census record and its commit")
    dc = d["decision"]
    if not isinstance(dc, dict) or not _s(dc.get("text")) or not _s(dc.get("replaced_by")):
        p.append("decision needs text and replaced_by ('nothing' or what replaced it)")
    st = d["steps"]
    if not isinstance(st, dict):
        p.append("steps must be an object")
    else:
        r = st.get("accelerator_rule")
        if not isinstance(r, dict) or r.get("read_after") != "ResourceNotFound":
            p.append("accelerator_rule.read_after must be ResourceNotFound")
        m = st.get("marker")
        if not isinstance(m, dict) or m.get("copy_saved") is not True or m.get("read_after") != "404" or not _s(m.get("copy_path")):
            p.append("marker needs copy_saved true, copy_path and read_after 404")
        w = st.get("writer")
        if not isinstance(w, dict) or w.get("stopped") is not True or not _s(w.get("evidence")):
            p.append("writer needs stopped true and evidence (no new marker version after the next chain day)")
    pair = d["pair"]
    if not isinstance(pair, dict) or not _s(pair.get("coo_half")) or not _s(pair.get("cto_half")):
        p.append("pair needs coo_half and cto_half commits")
    rb = d["rollback"]
    if not isinstance(rb, dict) or rb.get("recorded") is not True or not _s(rb.get("how")):
        p.append("rollback needs recorded true and how")
    if d["ledger_closed"] is not True:
        p.append("the ledger entry is not closed")
    return _finish("DOOR6RETIRE", p, "DOOR6RETIRE: OK steps=3 replaced_by=%s" % d["decision"]["replaced_by"] if not p else "")


def planq(a):
    tag = "PLANQ"
    raw, d = _load(a.file, tag)
    if d is None:
        return 1
    p = _common(raw, d, ("order", "read_at", "entries", "calls", "denominators", "not_read", "claim"))
    if p and p[-1].startswith("missing"):
        print("PLANQ: FAIL " + "; ".join(p))
        return 1
    _calls_ok(d, p)
    _den_ok(d, p)
    allowed = ("ANSWERED", "CARRIED") if a.kind == "Q" else ("CONFIRMED", "CONTRADICTED", "CARRIED")
    es = d["entries"]
    want = list(range(a.first, a.last + 1))
    if not isinstance(es, list) or sorted(e.get("n") if isinstance(e, dict) else -1 for e in es) != want:
        p.append("entries must cover exactly %d..%d once each" % (a.first, a.last))
    else:
        for e in es:
            v = e.get("verdict")
            if v not in allowed or not _s(e.get("id")):
                p.append("entry %s needs an id and a verdict in %s" % (e.get("n"), "/".join(allowed)))
            elif v == "CARRIED" and not (_s(e.get("owner")) and _s(e.get("next_move"))):
                p.append("entry %s is CARRIED and needs owner and next_move" % e.get("n"))
            elif v != "CARRIED" and not _s(e.get("evidence")):
                p.append("entry %s needs evidence" % e.get("n"))
    n_c = sum(1 for e in es if isinstance(e, dict) and e.get("verdict") == "CARRIED") if isinstance(es, list) else 0
    return _finish(tag, p, "PLANQ: OK entries=%d carried=%d" % (len(es) if isinstance(es, list) else 0, n_c))


def addendum(a):
    raw, d = _load(a.file, "ADDENDUM")
    if d is None:
        return 1
    p = _common(raw, d, ("order", "read_at", "row", "retire_entry", "census", "calls", "not_read", "claim"))
    if p and p[-1].startswith("missing"):
        print("ADDENDUM: FAIL " + "; ".join(p))
        return 1
    _calls_ok(d, p)
    if not isinstance(d["row"], dict) or d["row"].get("id") != "D1-S60":
        p.append("row.id must be D1-S60")
    re_ = d["retire_entry"]
    if not isinstance(re_, dict) or not _s(re_.get("operation")) or "opal/bd/cottonwood/credentials" not in str(re_.get("operation")):
        p.append("retire_entry.operation must name the secret")
    elif re_.get("delete_by") != "andrew" or re_.get("delete_performed") is not False or not _s(re_.get("decision")):
        p.append("retire_entry needs delete_by 'andrew', delete_performed false and a decision")
    ce = d["census"]
    if not isinstance(ce, dict) or not isinstance(ce.get("roles_scanned"), int) or ce["roles_scanned"] <= 0 or not isinstance(ce.get("roles_with_read"), int) or not _s(ce.get("last_accessed")):
        p.append("census needs roles_scanned above 0, roles_with_read and last_accessed")
    return _finish("ADDENDUM", p, "ADDENDUM: OK consumers=%s delete=andrew" % (ce.get("roles_with_read") if isinstance(ce, dict) else "?"))


def key23(a):
    raw, d = _load(a.file, "KEY23")
    if d is None:
        return 1
    p = _common(raw, d, ("order", "read_at", "floor_day", "key", "writer", "publisher_condition", "why", "last_version_at", "publisher_window", "versions_in_publisher_window", "versions_on_floor_day_total", "calls", "claim"))
    if p and p[-1].startswith("missing"):
        print("KEY23: FAIL " + "; ".join(p))
        return 1
    _calls_ok(d, p)
    for k in ("key", "writer", "publisher_condition", "why", "last_version_at"):
        if not _s(d[k]):
            p.append("%s must be a non-empty string" % k)
    w = d["publisher_window"]
    if d["floor_day"] != "2026-10-16" or not isinstance(w, dict) or w.get("from") != "2026-10-16T13:30:00Z" or w.get("to") != "2026-10-16T13:35:00Z":
        p.append("floor_day must be 2026-10-16 and publisher_window 2026-10-16T13:30:00Z to 2026-10-16T13:35:00Z")
    v = d["versions_in_publisher_window"]
    if isinstance(v, bool) or v != 0:
        p.append("versions_in_publisher_window must be 0")
    t = d["versions_on_floor_day_total"]
    if isinstance(t, bool) or not isinstance(t, int) or t < 0:
        p.append("versions_on_floor_day_total must be an integer, 0 or more")
    return _finish("KEY23", p, "KEY23: OK key=%s" % d["key"])


def triage(a):
    raw, d = _load(a.file, "TRIAGE")
    if d is None:
        return 1
    p = _common(raw, d, ("order", "read_at", "group", "rows", "calls", "denominators", "not_read", "claim"))
    if p and p[-1].startswith("missing"):
        print("TRIAGE: FAIL " + "; ".join(p))
        return 1
    _calls_ok(d, p)
    _den_ok(d, p)
    try:
        want = [ln.split("\t")[0].strip() for ln in open(a.ids, encoding="ascii").read().splitlines() if ln.strip()]
    except OSError as e:
        print("TRIAGE: FAIL cannot read ids: %s" % type(e).__name__)
        return 1
    rows = d["rows"]
    got = [r.get("id") if isinstance(r, dict) else None for r in rows] if isinstance(rows, list) else []
    if sorted(got) != sorted(want) or len(set(got)) != len(got):
        p.append("rows must cover exactly the %d listed ids once each (got %d, %d unlisted or repeated)" % (len(want), len(got), len(set(got) ^ set(want))))
    cnt = {"MET": 0, "RE_OWN": 0, "DISMISS": 0, "CARRY": 0}
    for r in rows if isinstance(rows, list) else []:
        v = r.get("verdict") if isinstance(r, dict) else None
        if v not in cnt:
            p.append("%s: verdict must be MET, RE_OWN, DISMISS or CARRY" % (r.get("id") if isinstance(r, dict) else "?"))
            continue
        cnt[v] += 1
        need = {"MET": "evidence", "RE_OWN": "new_owner", "DISMISS": "reason", "CARRY": "carrier"}[v]
        if not _s(r.get(need)):
            p.append("%s: %s needs %s" % (r.get("id"), v, need))
        if v != "MET" and not _s(r.get("evidence")):
            p.append("%s: %s still needs the evidence read" % (r.get("id"), v))
    return _finish("TRIAGE", p, "TRIAGE: OK rows=%d met=%d re_own=%d dismiss=%d carry=%d" % (len(got), cnt["MET"], cnt["RE_OWN"], cnt["DISMISS"], cnt["CARRY"]))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for nm in ("door6census", "door6retire", "addendum", "key23"):
        sub.add_parser(nm).add_argument("--file", required=True)
    q = sub.add_parser("planq")
    q.add_argument("--file", required=True)
    q.add_argument("--first", type=int, required=True)
    q.add_argument("--last", type=int, required=True)
    q.add_argument("--kind", choices=("Q", "NOMOVE"), required=True)
    t = sub.add_parser("triage")
    t.add_argument("--file", required=True)
    t.add_argument("--ids", required=True)
    a = ap.parse_args()
    return {"door6census": door6census, "door6retire": door6retire, "planq": planq, "addendum": addendum, "key23": key23, "triage": triage}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
