"""IRPT_BCKEND round 194 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB194-1  IB-pr-538  packet v2 of the holdings-producer release: the FULL pin mint, every moved bundle member CHARACTERIZED (READ ONLY)
    AC1  the moved members: per firm exactly the members of the stop evidence, each classified by a rule the check recomputes from git
    AC2  the mandatory reads: the calendar delta and T-1 old against new (recomputed from the two committed calendars), the write addresses
         old against new (a change is a STOP), the importer of the added matcher, and the re-measure equal to the signed counts
    AC3  packet v2: both halves UNSIGNED, the table, Branch A and B, the rules of rounds 193 and 194, no long digit run, the six bound counters 0
"""
import ast
import datetime as dt
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
REC = D + "0.9.0_WK_IRPT_BCKEND~383/IB194-1_packet_v2_record.json"
PACKET = D + "0.9.0_WK_IRPT_BCKEND~383/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-532_V2.md"
EVIDENCE = D + "0.7.0_AE_CloudOps~IB2/IB193-1_digest_gate_stop.json"
PIN = "49467335d288d5c0012fe339c4cafcb74bd43fb5"
CAL = "lib/trading_calendar.py"
PIN_COMMIT_FIELD = "pin"
FIRMS = ["49financial", "cottonwood", "inflection"]
PACKET_NUMBERS = {"49financial": (32, 0, "PUBLISHED", "PUBLISHED", 0), "cottonwood": (38, 211, "REFUSED", "PUBLISHED", 1), "inflection": (774, 67, "PUBLISHED", "PUBLISHED", 0)}
PINS = {"49financial": "2026-10-12", "cottonwood": "2026-10-12", "inflection": "2026-10-13"}
FIRE_DATES = ["2026-10-14", "2026-10-15", "2026-10-16"]
WINDOW = ("2026-10-01", "2027-12-31")
CLASSES = ("behaviour", "data", "line_endings", "docs")
BOUND = ("functions_invoked", "sign_ins_made", "aws_writes_made", "rows_written", "figures_written", "vendor_requests_sent")
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB194"))
    sys.exit(1)


def load(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def is_hex(x, n):
    return isinstance(x, str) and re.fullmatch(r"[0-9a-f]{%d}" % n, x) is not None


def is_date(x):
    return isinstance(x, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", x) is not None


def no_long_digits(txt):
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", txt):
        fail("a long digit run (an identifier or a figure) is present")


def git_show(commit, path):
    p = subprocess.run(["git", "-C", str(ROOT), "show", "%s:%s" % (commit, path)], capture_output=True, timeout=60)
    return p.stdout if p.returncode == 0 else None


def folded_sha(b):
    return hashlib.sha256(b.replace(b"\r\n", b"\n")).hexdigest()


def ast_without_docstrings(b):
    try:
        tree = ast.parse(b.decode("utf-8"))
    except (SyntaxError, UnicodeDecodeError, ValueError):
        return None
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(getattr(first, "value", None), ast.Constant) and isinstance(first.value.value, str):
                node.body = node.body[1:] or [ast.Pass()]
    return ast.dump(tree)


def evidence_sets():
    ev = load(EVIDENCE)
    out = {}
    for firm in FIRMS:
        f = (ev.get("firms") or {}).get(firm) or fail("the stop evidence holds no %s" % firm)
        out[firm] = {"changed": set(f["changed_by_content"]), "eol": set(f["changed_by_line_endings_only"]), "added": set(f["added_in_built"])}
    return out


# ----------------------------------------------------------------------------- AC1
def ac1():
    r = load(REC)
    pin = r.get(PIN_COMMIT_FIELD)
    if pin != PIN:
        fail("pin must be %s" % PIN)
    if not is_hex(r.get("base_commit"), 40):
        fail("base_commit must be 40 hex")
    ev = evidence_sets()
    for firm in FIRMS:
        rows = (r.get("members") or {}).get(firm)
        if not isinstance(rows, list) or not rows:
            fail("no member table for %s" % firm)
        paths = [x.get("path") for x in rows]
        if len(set(paths)) != len(paths):
            fail("%s: a path appears twice" % firm)
        want = ev[firm]["changed"] | ev[firm]["eol"] | ev[firm]["added"]
        if set(paths) != want:
            fail("%s: the table differs from the stop evidence: missing %r extra %r" % (firm, sorted(want - set(paths))[:3], sorted(set(paths) - want)[:3]))
        for x in rows:
            path, cls = x["path"], x.get("class")
            if cls not in CLASSES:
                fail("%s %s: class %r is not one of %r" % (firm, path, cls, CLASSES))
            blob = git_show(PIN, path)
            if blob is None or folded_sha(blob) != x.get("pin_folded_sha256"):
                fail("%s %s: pin_folded_sha256 is not the pin blob's" % (firm, path))
            if not is_hex(x.get("pin_commit"), 40) or git_show(x["pin_commit"], path) is None or folded_sha(git_show(x["pin_commit"], path)) != x["pin_folded_sha256"]:
                fail("%s %s: pin_commit does not carry the pin blob" % (firm, path))
            if path in ev[firm]["added"]:
                if x.get("state") != "added" or x.get("live_commit") is not None:
                    fail("%s %s: an added member has state added and no live commit" % (firm, path))
            else:
                if x.get("state") != "changed":
                    fail("%s %s: state must be changed" % (firm, path))
                lc = x.get("live_commit")
                if lc is None:
                    if cls != "behaviour" or not x.get("effect"):
                        fail("%s %s: with no live commit found the class is behaviour with an effect line" % (firm, path))
                    continue
                lb = git_show(lc, path) if is_hex(lc, 40) else None
                if lb is None or folded_sha(lb) != x.get("live_folded_sha256"):
                    fail("%s %s: live_folded_sha256 is not the live commit's blob" % (firm, path))
                same = x["live_folded_sha256"] == x["pin_folded_sha256"]
                if same != (cls == "line_endings"):
                    fail("%s %s: class %s but the folded contents %s" % (firm, path, cls, "are equal" if same else "differ"))
                if cls != "line_endings" and path.endswith(".py"):
                    a, b = ast_without_docstrings(lb), ast_without_docstrings(blob)
                    if a is not None and b is not None and (a == b) != (cls == "docs"):
                        fail("%s %s: class %s but the code %s apart from comments and docstrings" % (firm, path, cls, "is identical" if a == b else "differs"))
            if cls in ("behaviour", "data") and (not isinstance(x.get("effect"), str) or len(x["effect"]) < 25):
                fail("%s %s: a %s line must name its effect on the served output" % (firm, path, cls))
    print("OK: the member tables equal the stop evidence and every class recomputes from git")


# ----------------------------------------------------------------------------- AC2
def load_calendar(commit):
    b = git_show(commit, CAL)
    if b is None:
        fail("no %s at %s" % (CAL, commit))
    td = tempfile.mkdtemp(prefix="cal194_")
    f = Path(td) / ("cal_%s.py" % commit[:8])
    f.write_bytes(b)
    spec = importlib.util.spec_from_file_location("cal_" + commit[:8], str(f))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def holidays(mod):
    for name in ("NYSE_HOLIDAYS_FALLBACK", "_NYSE_HOLIDAYS_FALLBACK"):
        h = getattr(mod, name, None)
        if h is not None:
            return {(x.isoformat() if hasattr(x, "isoformat") else str(x)) for x in h}
    fail("the calendar exposes no holiday set")


def ac2():
    r = load(REC)
    c = r.get("calendar") or {}
    lc = c.get("live_commit")
    if not is_hex(lc, 40):
        fail("calendar.live_commit must be 40 hex")
    old, new = load_calendar(lc), load_calendar(PIN)
    lo, hi = WINDOW
    ho, hn = {d for d in holidays(old) if lo <= d <= hi}, {d for d in holidays(new) if lo <= d <= hi}
    if c.get("fire_dates") != FIRE_DATES:
        fail("calendar.fire_dates must be %r" % FIRE_DATES)
    if sorted(c.get("holidays_added", [])) != sorted(hn - ho) or sorted(c.get("holidays_removed", [])) != sorted(ho - hn):
        fail("the holiday delta differs from the two committed calendars: added %r removed %r" % (sorted(hn - ho), sorted(ho - hn)))
    t_old = {d: old.prev_trading_day(dt.date.fromisoformat(d)).isoformat() for d in FIRE_DATES}
    t_new = {d: new.prev_trading_day(dt.date.fromisoformat(d)).isoformat() for d in FIRE_DATES}
    if c.get("t_minus_1_old") != t_old or c.get("t_minus_1_new") != t_new:
        fail("T-1 differs from the committed calendars: old %r new %r" % (t_old, t_new))
    if sorted(c.get("t_minus_1_differs_on", [])) != sorted(d for d in FIRE_DATES if t_old[d] != t_new[d]):
        fail("t_minus_1_differs_on is wrong")
    wa = r.get("write_addresses") or {}
    for firm in FIRMS:
        v = wa.get(firm) or fail("no write_addresses for %s" % firm)
        o, n = v.get("old"), v.get("new")
        if not isinstance(o, list) or not o or not isinstance(n, list) or not n or not any("current/manifest.json" in x for x in o):
            fail("%s: write addresses old and new are required, with the manifest key" % firm)
        if set(o) != set(n) or v.get("equal") is not True:
            fail("%s: a changed write address is a STOP and a separate pair" % firm)
    m = r.get("strategy_matcher") or {}
    imp = m.get("importer")
    if imp:
        src = git_show(PIN, imp)
        if src is None or b"opal_strategy_matcher" not in src:
            fail("the named importer does not import opal_strategy_matcher at the pin")
    elif m.get("dropped") is not True or not isinstance(m.get("evidence"), str) or len(m["evidence"]) < 40:
        fail("with no importer the matcher is dropped, with evidence")
    rm = r.get("remeasure") or {}
    if rm.get("pins") != PINS:
        fail("the re-measure pins must be %r" % PINS)
    for firm, (can, fb, gb, ga, listed) in PACKET_NUMBERS.items():
        v = (rm.get("firms") or {}).get(firm) or fail("no re-measure for %s" % firm)
        if (v.get("movers_canonical"), v.get("movers_fallback"), v.get("gate_before"), v.get("gate_after"), v.get("lost_accounts_listed_after")) != (can, fb, gb, ga, listed):
            fail("%s re-measure differs from the signed counts: the packet cannot be re-signed on them" % firm)
    print("OK: calendar delta and T-1 recomputed, write addresses equal, matcher importer, re-measure")


# ----------------------------------------------------------------------------- AC3
def ac3():
    r = load(REC)
    f = ROOT / PACKET
    if not f.is_file():
        fail("no packet v2")
    txt = f.read_text(encoding="utf-8")
    if len(txt) < 6000:
        fail("the packet must be 6,000 characters or more")
    low = txt.lower()
    for need in ("branch a", "branch b", "blast radius", "stop rule", "ledger", "manifest anchor", "t-1", "trading calendar", "opal_strategy_matcher",
                 "sha256", "moved member", "line endings", "every other date", "business date", "after the first fire"):
        if need not in low:
            fail("the packet does not carry %r" % need)
    if len(re.findall(r"unsigned", low)) < 2 or "coo half" not in low or "cto half" not in low:
        fail("both halves must read UNSIGNED at the packet bytes")
    for firm in FIRMS:
        for x in r["members"][firm]:
            if x["path"] not in txt:
                fail("the packet does not list the member %s" % x["path"])
    for k in BOUND:
        if r.get(k) != 0:
            fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
    if not isinstance(r.get("notes"), list) or not r["notes"]:
        fail("notes are required")
    no_long_digits(txt)
    no_long_digits(json.dumps(r))
    print("OK: packet v2 body, halves unsigned, counters")


CHECKS = {"IB194-1-AC1": ac1, "IB194-1-AC2": ac2, "IB194-1-AC3": ac3}


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p194_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    ROOT = Path(sys.argv[1])
    CID = sys.argv[2]
    CHECKS[CID]()
    print("%s PASS" % CID)
