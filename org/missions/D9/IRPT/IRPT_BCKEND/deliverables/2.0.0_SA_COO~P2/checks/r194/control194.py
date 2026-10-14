"""Positive control and negatives for p194_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control194.py <real_repo_root>
Builds a temp git repo (a live commit and a pin commit holding a docs-only change, a behaviour change, a line-endings-only change, a data
change, an added member, an importer, and the REAL old and new trading calendars), writes a synthetic record, packet and stop evidence,
runs every criterion in-process expecting PASS, then applies each mutation expecting the NAMED criterion to FAIL. The temp root is removed.
"""
import contextlib
import copy
import io
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r194"))
import p194_cells as P  # noqa: E402

FILES_LIVE = {
    "docs_only.py": "def f(x):\n    return x + 1\n",
    "behaviour.py": "def g(x):\n    return x * 2\n",
    "eol.json": '{"a": 1,\r\n "b": 2}\r\n',
    "data.json": '{"a": 1}\n',
}
FILES_PIN = {
    "docs_only.py": '"""now documented"""\n# a comment\ndef f(x):\n    """adds one"""\n    return x + 1\n',
    "behaviour.py": "def g(x):\n    return x * 3\n",
    "eol.json": '{"a": 1,\n "b": 2}\n',
    "data.json": '{"a": 2}\n',
    "added.py": "X = 1\n",
    "importer.py": "import opal_strategy_matcher\n",
}
CHANGED = ["docs_only.py", "behaviour.py", "data.json", "lib/trading_calendar.py"]
EOL = ["eol.json"]
ADDED = ["added.py"]


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def real_show(commit, path):
    return subprocess.run(["git", "-C", str(REAL), "show", "%s:%s" % (commit, path)], capture_output=True, check=True).stdout


def wb(root, rel, data):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))


def build():
    root = Path(tempfile.mkdtemp(prefix="c194_"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    for k, v in FILES_LIVE.items():
        wb(root, k, v)
    wb(root, "lib/trading_calendar.py", real_show("0cbb0ad174", "lib/trading_calendar.py"))
    git(root, "add", "-A")
    git(root, "commit", "-qm", "live")
    live = git(root, "rev-parse", "HEAD")
    for k, v in FILES_PIN.items():
        wb(root, k, v)
    wb(root, "lib/trading_calendar.py", real_show("HEAD", "lib/trading_calendar.py"))
    git(root, "add", "-A")
    git(root, "commit", "-qm", "pin")
    pin = git(root, "rev-parse", "HEAD")
    return root, live, pin


def row(root, live, pin, path, cls, state="changed", effect=""):
    pb = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (pin, path)], capture_output=True, check=True).stdout
    r = {"path": path, "state": state, "pin_commit": pin, "pin_folded_sha256": P.folded_sha(pb), "class": cls, "effect": effect}
    if state == "added":
        r.update({"live_commit": None, "live_folded_sha256": None})
    else:
        lb = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (live, path)], capture_output=True, check=True).stdout
        r.update({"live_commit": live, "live_folded_sha256": P.folded_sha(lb)})
    return r


def make(root, live, pin):
    rows = [row(root, live, pin, "docs_only.py", "docs"), row(root, live, pin, "behaviour.py", "behaviour", effect="the doubled figure becomes tripled in the served output"),
            row(root, live, pin, "data.json", "data", effect="the served registry value changes from one to two"),
            row(root, live, pin, "lib/trading_calendar.py", "data", effect="the trading calendar holiday set and T-1 dates move for the first fires"),
            row(root, live, pin, "eol.json", "line_endings"), row(root, live, pin, "added.py", "docs", state="added")]
    old, new = P.load_calendar(live), P.load_calendar(pin)
    lo, hi = P.WINDOW
    ho, hn = {d for d in P.holidays(old) if lo <= d <= hi}, {d for d in P.holidays(new) if lo <= d <= hi}
    t_old = {d: old.prev_trading_day(P.dt.date.fromisoformat(d)).isoformat() for d in P.FIRE_DATES}
    t_new = {d: new.prev_trading_day(P.dt.date.fromisoformat(d)).isoformat() for d in P.FIRE_DATES}
    rec = {"base_commit": "a" * 40, P.PIN_COMMIT_FIELD: pin, "members": {f: copy.deepcopy(rows) for f in P.FIRMS},
           "calendar": {"live_commit": live, "window": list(P.WINDOW), "holidays_added": sorted(hn - ho), "holidays_removed": sorted(ho - hn),
                        "fire_dates": list(P.FIRE_DATES), "t_minus_1_old": t_old, "t_minus_1_new": t_new,
                        "t_minus_1_differs_on": sorted(d for d in P.FIRE_DATES if t_old[d] != t_new[d])},
           "write_addresses": {f: {"old": ["s3://b/irpt/%s/platinum/holdings/current/manifest.json" % f, "s3://b/irpt/%s/gold/holdings/date=*/rev.parquet" % f],
                                   "new": ["s3://b/irpt/%s/platinum/holdings/current/manifest.json" % f, "s3://b/irpt/%s/gold/holdings/date=*/rev.parquet" % f], "equal": True} for f in P.FIRMS},
           "strategy_matcher": {"importer": "importer.py", "dropped": False, "evidence": "importer.py imports it"},
           "remeasure": {"pins": dict(P.PINS), "firms": {f: {"movers_canonical": v[0], "movers_fallback": v[1], "gate_before": v[2], "gate_after": v[3],
                                                             "lost_accounts_listed_after": v[4]} for f, v in P.PACKET_NUMBERS.items()}},
           "notes": ["synthetic control record"], **{k: 0 for k in P.BOUND}}
    evid = {"firms": {f: {"changed_by_content": list(CHANGED), "changed_by_line_endings_only": list(EOL), "added_in_built": list(ADDED)} for f in P.FIRMS}}
    paths = sorted({x["path"] for x in rows})
    packet = ("# Packet v2 (synthetic)\n\nBranch A, Branch B, the blast radius, the stop rule, the ledger, the manifest anchor rule, T-1 by the trading calendar, "
              "opal_strategy_matcher, the sha256 left for the signers, every moved member, line endings, every other date, the business date, "
              "the after the first fire reads.\n\nCOO half: UNSIGNED.\nCTO half: UNSIGNED.\n\n" + "\n".join("- " + p for p in paths) + "\n" + ("padding line of plain words\n" * 300))
    return rec, evid, packet


def put(root, rec, evid, packet):
    wb(root, P.REC, json.dumps(rec, indent=1))
    wb(root, P.EVIDENCE, json.dumps(evid, indent=1))
    wb(root, P.PACKET, packet)


def run(root, pin, cid):
    P.ROOT, P.CID, P.PIN = root, cid, pin
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            P.CHECKS[cid]()
        return cid + " PASS"
    except SystemExit:
        return cid + " FAIL"
    except Exception as e:  # noqa: BLE001 -- a crash is not a verdict
        return cid + " CRASH " + type(e).__name__ + ": " + str(e)[:120]


def setrow(rec, path, **kw):
    for f in P.FIRMS:
        for x in rec["members"][f]:
            if x["path"] == path:
                x.update(kw)


bad = 0
root, live, pin = build()
P.ROOT = root
rec0, evid0, packet0 = make(root, live, pin)
put(root, rec0, evid0, packet0)
for cid in P.CHECKS:
    r = run(root, pin, cid)
    ok = r == cid + " PASS"
    bad += 0 if ok else 1
    print("POSITIVE %s -> %s %s" % (cid, r, "" if ok else "<-- UNEXPECTED"))


def neg(label, cid, edit_rec=None, packet=None, evid=None):
    global bad
    rec = copy.deepcopy(rec0)
    if edit_rec:
        edit_rec(rec)
    put(root, rec, evid if evid is not None else evid0, packet if packet is not None else packet0)
    r = run(root, pin, cid)
    ok = r == cid + " FAIL"
    bad += 0 if ok else 1
    print("NEGATIVE %-12s %-52s -> %s %s" % (cid, label, r, "" if ok else "<-- DID NOT FAIL"))


neg("docs change classified as behaviour", "IB194-1-AC1", lambda r: setrow(r, "docs_only.py", **{"class": "behaviour", "effect": "claimed to change the served output somehow"}))
neg("a behaviour change classified as docs", "IB194-1-AC1", lambda r: setrow(r, "behaviour.py", **{"class": "docs", "effect": ""}))
neg("a line-endings class on a content change", "IB194-1-AC1", lambda r: setrow(r, "data.json", **{"class": "line_endings", "effect": ""}))
neg("an EOL-only file classified as data", "IB194-1-AC1", lambda r: setrow(r, "eol.json", **{"class": "data", "effect": "claimed data change in the served registry"}))
neg("a wrong pin blob hash", "IB194-1-AC1", lambda r: setrow(r, "behaviour.py", pin_folded_sha256="0" * 64))
neg("a moved member left out of the table", "IB194-1-AC1", lambda r: r["members"]["cottonwood"].pop(0))
neg("a behaviour line with no effect", "IB194-1-AC1", lambda r: setrow(r, "behaviour.py", effect=""))
neg("an added member with a live commit", "IB194-1-AC1", lambda r: setrow(r, "added.py", live_commit=live))
neg("a wrong T-1 (new)", "IB194-1-AC2", lambda r: r["calendar"]["t_minus_1_new"].update({P.FIRE_DATES[0]: "2020-01-01"}))
neg("a holiday delta that is not the calendars'", "IB194-1-AC2", lambda r: r["calendar"].update({"holidays_added": ["2026-12-31"]}))
neg("a changed write address", "IB194-1-AC2", lambda r: r["write_addresses"]["inflection"].update({"new": ["s3://b/other/current/manifest.json"], "equal": False}))
neg("a matcher importer that does not import it", "IB194-1-AC2", lambda r: r["strategy_matcher"].update({"importer": "behaviour.py"}))
neg("a gate that differs from the signed counts", "IB194-1-AC2", lambda r: r["remeasure"]["firms"]["inflection"].update({"gate_after": "REFUSED"}))
neg("the wrong re-measure pin", "IB194-1-AC2", lambda r: r["remeasure"]["pins"].update({"inflection": "2026-10-12"}))
neg("a packet that omits a member", "IB194-1-AC3", packet=packet0.replace("- behaviour.py", "- other"))
neg("a packet with one half signed", "IB194-1-AC3", packet=packet0.replace("CTO half: UNSIGNED.", "CTO half: signed."))
neg("a packet too short", "IB194-1-AC3", packet=packet0[:1500])
neg("a bound counter above 0", "IB194-1-AC3", lambda r: r.update({"aws_writes_made": 1}))
neg("a long digit run in the packet", "IB194-1-AC3", packet=packet0 + "\naccount 123456789012 listed\n")
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
