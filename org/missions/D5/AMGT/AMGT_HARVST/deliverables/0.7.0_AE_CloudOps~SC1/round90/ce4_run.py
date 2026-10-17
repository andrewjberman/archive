"""HVST-ce-4 driver, run from the pinned worktree (C:/tmp/ce4-build at 344ea6a5fc). ASCII only.

Usage:
  python ce4_run.py build NAME          read only: continuation.build(NAME), print fund/position, scan for the two Mexico ids
  python ce4_run.py write NAME          the order's steps 1(a)..(d) for ONE name, serially, guarded (window, list, branch checks)
  python ce4_run.py rest                the other 29 in file order, stopping at the FIRST name that does not finish OK

Guards (COO half C-1..C-8): the name must be in ce4_securities.txt (sha256 checked); UTC now must be inside
2026-10-17 17:20Z to 19:30Z; UNH must build PFOE/'Maintain positions in PFOE and DIVZ' with line_only true; KMB's built
continuation and dossier must hold 0 of each Mexico id; every other name's built fund token and first 60 characters of the
position must equal its ce2_census line (else Branch B: stop before the write); any exception stops with its exact text,
no retry. Every put is appended to ce4_written.out the moment it lands (key, VersionId, bytes, sha256, UTC time).
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import sys

WT = r"C:\tmp\ce4-build"
sys.path.insert(0, WT)
os.chdir(WT)

from lib.research.corpus import continuation, dossier  # noqa: E402
from lib.research.harvest import store  # noqa: E402

ROOT = r"C:\dev\ajb_workspace"
OUT = os.path.join(ROOT, r"org\missions\D5\AMGT\AMGT_HARVST\deliverables\0.7.0_AE_CloudOps~SC1\round90")
LIST = os.path.join(ROOT, r"org\missions\D5\AMGT\AMGT_HARVST\deliverables\2.0.0_SA_COO_W1\round90\ce4_securities.txt")
CENSUS = os.path.join(ROOT, r"org\missions\D5\AMGT\AMGT_HARVST\deliverables\0.9.0_WK_AMGT_HARVST~156\ce2_census.out")
LIST_SHA = "7881772da6e204818fd50a02050cc7456b7de5a6d0912b6d663817f12930c67b"
BAD = ("fbd50086c4065785", "1a3b56044db679a5")
WIN_START = datetime.datetime(2026, 10, 17, 17, 20, tzinfo=datetime.timezone.utc)
WIN_END = datetime.datetime(2026, 10, 17, 19, 30, tzinfo=datetime.timezone.utc)
MANIFEST = os.path.join(OUT, "ce4_written.out")


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def stamp():
    return now().strftime("%Y-%m-%dT%H:%M:%SZ")


def names():
    raw = open(LIST, "rb").read()
    if hashlib.sha256(raw).hexdigest() != LIST_SHA:
        print("STOP: ce4_securities.txt sha256 differs from the signed value")
        sys.exit(2)
    return [ln.strip() for ln in raw.decode("ascii").splitlines() if ln.strip()]


def census():
    out = {}
    for ln in open(CENSUS, encoding="utf-8", errors="replace"):
        m = re.match(r"^CHANGED (\S+) fund_before=\S+ fund_after=(\S+) position_before=.*? position_after=(.*?) report_id=\S+\s*$", ln)
        if m:
            out[m.group(1)] = (m.group(2), m.group(3))
    return out


def entry_value(entry):
    if isinstance(entry, dict):
        return entry.get("value")
    return entry


def show(label, doc):
    f = doc["fields"]
    fund, pos = f["fund_of_record"], f["last_stated_position"]
    print("%s method_version=%s content_sha256=%s inputs=%d" % (label, doc.get("method_version"), doc.get("content_sha256"), len(doc.get("inputs", []))))
    print("%s fund_of_record entry=%s" % (label, json.dumps(fund, sort_keys=True)[:420]))
    print("%s last_stated_position entry=%s" % (label, json.dumps(pos, sort_keys=True)[:520]))
    print("%s VALUES fund=%r position=%r line_only=%s fund_absent=%r position_absent=%r" % (
        label, entry_value(fund), entry_value(pos),
        bool(isinstance(entry_value(pos), dict) and entry_value(pos).get("line_only")),
        fund.get("absent") if isinstance(fund, dict) else None, pos.get("absent") if isinstance(pos, dict) else None))
    return fund, pos


def scan(label, doc):
    text = json.dumps(doc, sort_keys=True)
    counts = [text.count(b) for b in BAD]
    print("%s MEXICO-ID SCAN fbd50086c4065785=%d 1a3b56044db679a5=%d" % (label, counts[0], counts[1]))
    return counts


def record(client, kind, name, uri, performed, existed, payload=None):
    bucket, key = uri[len("s3://"):].split("/", 1)
    head = client.head_object(Bucket=bucket, Key=key)
    body = client.get_object(Bucket=bucket, Key=key)["Body"].read()
    verb = "WROTE" if performed else "EXISTED-NOT-REWRITTEN"
    line = "%s %s %s %s key=%s VersionId=%s bytes=%d sha256=%s put_performed=%s existed=%s" % (
        stamp(), verb, kind, name, key, head.get("VersionId"), len(body), hashlib.sha256(body).hexdigest(), performed, existed)
    with open(MANIFEST, "a", encoding="ascii") as fh:
        fh.write(line + "\n")
    print(line)


def check_branch(name, doc, cen):
    fund, pos = doc["fields"]["fund_of_record"], doc["fields"]["last_stated_position"]
    fval, pval = entry_value(fund), entry_value(pos)
    ptext = pval.get("text") if isinstance(pval, dict) else pval
    lo = bool(isinstance(pval, dict) and pval.get("line_only"))
    if name == "UNH_US_Equity":
        ok = fval == "PFOE" and ptext == "Maintain positions in PFOE and DIVZ" and lo
        print("UNH CHECK fund=%r position_text=%r line_only=%s -> %s" % (fval, ptext, lo, "OK" if ok else "MISMATCH"))
        return ok
    if name == "KMB_US_Equity":
        branch = "X (absent)" if fval in (None, "") else "Y (value)"
        print("KMB branch %s fund=%r position_text=%r" % (branch, fval, ptext))
        return True
    want = cen.get(name)
    if want is None:
        print("%s has no census line: STOP" % name)
        return False
    ok = fval == want[0] and (ptext or "")[:60] == want[1][:60]
    print("%s CENSUS CHECK built fund=%r position[:60]=%r census fund=%r position[:60]=%r line_only=%s -> %s" % (
        name, fval, (ptext or "")[:60], want[0], want[1][:60], lo, "BRANCH A" if ok else "BRANCH B"))
    return ok


def do_build(name):
    cdoc = continuation.build(name)
    show("BUILD " + name, cdoc)
    counts = scan("BUILD " + name, cdoc)
    return cdoc, counts


def do_write(name):
    if not (WIN_START <= now() < WIN_END):
        print("STOP: now %s is outside the window 17:20Z to 19:30Z" % stamp())
        return 3
    if name not in names():
        print("STOP: %s is not in the signed list" % name)
        return 2
    client = store._default_client()
    cen = census()
    print("=== %s start %s ===" % (name, stamp()))
    cdoc = continuation.build(name, client=client)
    show("1a " + name, cdoc)
    counts = scan("1a " + name, cdoc)
    if name == "KMB_US_Equity" and counts != [0, 0]:
        print("STOP: KMB built continuation still holds a Mexico id; nothing written")
        return 4
    if not check_branch(name, cdoc, cen):
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
    dfund = ddoc["fields"].get("fund_of_record") if isinstance(ddoc.get("fields"), dict) else None
    dpos = ddoc["fields"].get("last_stated_position") if isinstance(ddoc.get("fields"), dict) else None
    print("1c %s dossier fund_of_record entry=%s" % (name, json.dumps(dfund, sort_keys=True)[:300]))
    print("1c %s dossier last_stated_position entry=%s" % (name, json.dumps(dpos, sort_keys=True)[:400]))
    dcounts = scan("1c " + name, ddoc)
    if name == "KMB_US_Equity" and dcounts != [0, 0]:
        print("STOP: KMB built dossier still holds a Mexico id; the dossier is NOT written")
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
    if len(argv) < 2:
        print(__doc__)
        return 2
    mode = argv[1]
    if mode == "build":
        names()
        do_build(argv[2])
        return 0
    if mode == "write":
        return do_write(argv[2])
    if mode == "rest":
        for name in names():
            if name in ("UNH_US_Equity", "KMB_US_Equity"):
                continue
            if os.path.exists(MANIFEST) and (" WROTE dossier %s " % name) in open(MANIFEST, encoding="ascii").read():
                print("SKIP %s: its dossier is already in the manifest" % name)
                continue
            if now() >= WIN_END:
                print("STOP at a name boundary: past 19:30Z before %s" % name)
                return 3
            rc = do_write(name)
            if rc != 0:
                print("STOPPED at %s rc=%d; no further name is written" % (name, rc))
                return rc
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
