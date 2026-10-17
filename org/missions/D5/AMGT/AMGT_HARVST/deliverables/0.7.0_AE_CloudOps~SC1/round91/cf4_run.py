"""HVST-cf-4 driver, run from the pinned worktree (C:/tmp/cf4-build at 80d0701876). ASCII only.

Usage (each name is a SEPARATE foreground command, always `python -u`, output appended to cf4_run.log by the caller):
  python -u cf4_run.py build NAME     read only: continuation.build(NAME), print the two fields, compare with the census line
  python -u cf4_run.py write NAME     the order's steps 1(a)..(d) for ONE name; guarded (window, list, branch, manifest)
There is deliberately NO loop mode (CTO rule for long write runs, row D1-S44).

Guards (COO half C-1..C-10): the name must be in cf4_securities.txt (sha256 checked); a write needs UTC now inside
2026-10-17 22:00Z to 2026-10-18 00:00Z; every built name must equal its cf2_census line (fund_of_record ABSENT; position
absent for the four JP names, else the first 60 characters of the text and the stance); a built fund_of_record that is a fund
token is a STOP; any exception stops with its exact text, no retry. Every put is appended to cf4_written.out at once.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import sys

WT = r"C:\tmp\cf4-build"
sys.path.insert(0, WT)
os.chdir(WT)

from lib.research.corpus import continuation, dossier  # noqa: E402
from lib.research.harvest import store  # noqa: E402

ROOT = r"C:\dev\ajb_workspace"
DEL = os.path.join(ROOT, r"org\missions\D5\AMGT\AMGT_HARVST\deliverables")
OUT = os.path.join(DEL, r"0.7.0_AE_CloudOps~SC1\round91")
LIST = os.path.join(DEL, r"2.0.0_SA_COO_W1\round91\cf4_securities.txt")
CENSUS = os.path.join(DEL, r"0.9.0_WK_AMGT_HARVST~160\cf2_census.out")
LIST_SHA = "221a63c311c9d0f13baeff2a346169b62f27cec7d32c33270ba1b2e1ac58ee48"
WIN_START = datetime.datetime(2026, 10, 17, 22, 0, tzinfo=datetime.timezone.utc)
WIN_END = datetime.datetime(2026, 10, 18, 0, 0, tzinfo=datetime.timezone.utc)
MANIFEST = os.path.join(OUT, "cf4_written.out")
FUNDS = ("IDVZ", "PFOE", "DIVZ")


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def stamp():
    return now().strftime("%Y-%m-%dT%H:%M:%SZ")


def names():
    raw = open(LIST, "rb").read()
    if hashlib.sha256(raw).hexdigest() != LIST_SHA:
        print("STOP: cf4_securities.txt sha256 differs from the signed value")
        sys.exit(2)
    return [ln.strip() for ln in raw.decode("ascii").splitlines() if ln.strip()]


def census():
    out = {}
    pat = re.compile(r"^CHANGED (\S+) fund_before=.*? fund_after=(\S+) position_before=.*? position_after=(.*?) stance_after=(\S+)\s*$")
    for ln in open(CENSUS, encoding="utf-8", errors="replace"):
        m = pat.match(ln)
        if m:
            out[m.group(1)] = (m.group(2), m.group(3), m.group(4))
    return out


def entry_value(entry):
    if isinstance(entry, dict):
        return entry.get("value")
    return entry


def fields(doc):
    f = doc["fields"]
    fund, pos = f["fund_of_record"], f["last_stated_position"]
    fval, pval = entry_value(fund), entry_value(pos)
    ptext = pval.get("text") if isinstance(pval, dict) else pval
    stance = pval.get("stance") if isinstance(pval, dict) else None
    return fund, pos, fval, pval, ptext, stance


def show(label, doc):
    fund, pos, fval, pval, ptext, stance = fields(doc)
    print("%s method_version=%s content_sha256=%s inputs=%d" % (label, doc.get("method_version"), doc.get("content_sha256"), len(doc.get("inputs", []))))
    print("%s fund_of_record entry=%s" % (label, json.dumps(fund, sort_keys=True)[:300]))
    print("%s last_stated_position entry=%s" % (label, json.dumps(pos, sort_keys=True)[:420]))
    print("%s VALUES fund=%r position_text=%r stance=%r position_value=%r fund_absent=%r position_absent=%r" % (
        label, fval, ptext, stance, pval,
        fund.get("absent") if isinstance(fund, dict) else None, pos.get("absent") if isinstance(pos, dict) else None))


def check(name, doc, cen):
    """True when the build equals the name's census line (Branch A)."""
    fund, pos, fval, pval, ptext, stance = fields(doc)
    if fval in FUNDS:
        print("%s CHECK: built fund_of_record is a fund token %r -> STOP (contradicts the census)" % (name, fval))
        return False
    want = cen.get(name)
    if want is None:
        print("%s has no census line: STOP" % name)
        return False
    fund_after, pos_after, stance_after = want
    ok = fval in (None, "")
    if pos_after == "absent":
        ok = ok and pval in (None, "")
        got = "absent" if pval in (None, "") else (ptext or "")[:60]
        print("%s CENSUS CHECK fund=%r position=%r stance=%r | census fund_after=%s position_after=%s stance_after=%s -> %s" % (
            name, fval, got, stance, fund_after, pos_after, stance_after, "BRANCH A" if ok else "BRANCH B"))
        return ok
    ok = ok and (ptext or "")[:60] == pos_after[:60] and (stance or "none") == stance_after
    print("%s CENSUS CHECK fund=%r position[:60]=%r stance=%r | census fund_after=%s position_after[:60]=%r stance_after=%s -> %s" % (
        name, fval, (ptext or "")[:60], stance, fund_after, pos_after[:60], stance_after, "BRANCH A" if ok else "BRANCH B"))
    return ok


def record(client, kind, name, uri, performed, existed):
    bucket, key = uri[len("s3://"):].split("/", 1)
    head = client.head_object(Bucket=bucket, Key=key)
    body = client.get_object(Bucket=bucket, Key=key)["Body"].read()
    verb = "WROTE" if performed else "EXISTED-NOT-REWRITTEN"
    line = "%s %s %s %s key=%s VersionId=%s bytes=%d sha256=%s put_performed=%s existed=%s" % (
        stamp(), verb, kind, name, key, head.get("VersionId"), len(body), hashlib.sha256(body).hexdigest(), performed, existed)
    with open(MANIFEST, "a", encoding="ascii") as fh:
        fh.write(line + "\n")
    print(line)


def do_write(name):
    if not (WIN_START <= now() < WIN_END):
        print("STOP: now %s is outside the window 22:00Z to 00:00Z" % stamp())
        return 3
    if name not in names():
        print("STOP: %s is not in the signed list" % name)
        return 2
    client = store._default_client()
    cen = census()
    print("=== %s start %s ===" % (name, stamp()))
    cdoc = continuation.build(name, client=client)
    show("1a " + name, cdoc)
    if not check(name, cdoc, cen):
        print("STOP: branch check failed for %s; nothing written for it" % name)
        return 4
    try:
        document, result, _src = continuation.write_one(name, client=client)
    except Exception as exc:  # noqa: BLE001
        print("STOP (continuation write): %s: %s" % (type(exc).__name__, exc))
        return 5
    if document.get("content_sha256") != cdoc.get("content_sha256"):
        print("NOTE: the document written differs from the document checked (content_sha256 %s vs %s)" % (document.get("content_sha256"), cdoc.get("content_sha256")))
    record(client, "continuation", name, result["uri"], result["put_performed"], result["existed"])
    try:
        ddoc = dossier.build(name, client=client)
    except Exception as exc:  # noqa: BLE001
        print("STOP (dossier build): %s: %s" % (type(exc).__name__, exc))
        return 5
    show("1c " + name + " dossier", ddoc)
    if not check(name, ddoc, cen):
        print("STOP: dossier branch check failed for %s; the dossier is NOT written" % name)
        return 4
    try:
        dres = dossier.write_one(name, client=client)
    except Exception as exc:  # noqa: BLE001
        print("STOP (dossier write): %s: %s" % (type(exc).__name__, exc))
        return 5
    if dres.get("wrote"):
        record(client, "dossier", name, dres["uri"], True, False)
    else:
        line = "%s NOT-WRITTEN dossier %s (unchanged inputs_sha16 %s)" % (stamp(), name, dres.get("inputs_sha16"))
        open(MANIFEST, "a", encoding="ascii").write(line + "\n")
        print(line)
    print("=== %s done %s ===" % (name, stamp()))
    return 0


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    mode, name = argv[1], argv[2]
    if mode == "build":
        names()
        cdoc = continuation.build(name)
        show("BUILD " + name, cdoc)
        if name in census():
            check(name, cdoc, census())
        return 0
    if mode == "write":
        return do_write(name)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
