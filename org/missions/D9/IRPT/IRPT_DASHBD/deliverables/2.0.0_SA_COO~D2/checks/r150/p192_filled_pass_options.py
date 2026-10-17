"""IRPT_DASHBD round 150, workstream FILLPASS (issuer 2.0.0_SA_COO~D2) -- DB-b-326, the CODE of the filled-report switch-on pair (CTO msg 10295, IB-pr-551 hop 2): the filled-report pass in
`infra/aws/lambda/investor-reporting/reporting-publish/handler.py` takes OPTIONAL scoping so the first pass can be proven small before it is run whole: `clients` (a non-empty list of issued client ids), `dry_run`
(a boolean: every document is read, composed and validated, none is written) and `shard` with `shards` (both or neither; the stable `shard_of` hash). ABSENT, the pass is exactly what it is today: every directory
client, writing. Switch OFF: it returns at once whatever the options say. Malformed options are refused BEFORE any read or write. LOCAL code; nothing is deployed.

  DB192-1-AC1   the diff: only handler.py (inside the FILLED-REPORT-A markers) and the new test file changed; at most 20 lines removed and 80 added; no new write path (one put_object), nothing printed
  DB192-1-AC2   the behaviour on the real `filled_report_fire`: default unchanged, a named subset, a dry run writing nothing, seven shards partitioning exactly once, the intersection, malformed options refused with no read or write, the switch off first
  DB192-1-AC3   the tests: at least six NEW tests carry `options` in their name and the whole reporting-publish test directory passes

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest <reference_root>      green on a reference tree, red on single-fault mutants
"""
import os
import re
import subprocess
import sys
from pathlib import Path

PKG = "infra/aws/lambda/investor-reporting/reporting-publish/"
HANDLER = PKG + "handler.py"
TESTS = PKG + "tests/"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-326.filled-pass-options-clients-dry-run-shards.md"
BEGIN, END = "# BEGIN FILLED-REPORT-A", "# END FILLED-REPORT-A"
IDS = ["cli_S%02d" % i for i in range(1, 26)]


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def git(root, *a):
    r = subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True)
    return r.stdout.decode("utf-8", "replace"), r.returncode


def issued_to(root):
    m = re.search(r"<issued_to>([^<]+)</issued_to>", (Path(root) / ORDER_REL).read_text(encoding="utf-8"))
    need(m is not None, "the order has no issued_to")
    return m.group(1).strip()


def blocks(text):
    """The text outside every FILLED-REPORT-A block, and the block texts."""
    out, inner, pos = [], [], 0
    while True:
        i = text.find(BEGIN, pos)
        if i < 0:
            out.append(text[pos:])
            break
        j = text.index(END, i)
        out.append(text[pos:i])
        inner.append(text[i:j + len(END)])
        pos = j + len(END)
    return "".join(out), inner


# ------------------------------------------------------------------------------------------------ AC1
def check_diff(root):
    root = Path(root)
    serial = issued_to(root)
    first = git(root, "log", "--author=" + serial, "--format=%H", "--", HANDLER)[0].split()
    base = (first[-1] + "^") if first else "HEAD"
    old = git(root, "show", "%s:%s" % (base, HANDLER))[0]
    new = (root / HANDLER).read_bytes().decode("utf-8")
    need(old and "\r" not in new, "handler.py must keep LF line endings")
    own = ("org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", ORDER_REL)
    committed = {x for x in git(root, "log", "--author=" + serial, "--name-only", "--format=")[0].splitlines() if x.strip()}
    working = {x for x in (git(root, "diff", "--name-only", "HEAD")[0] + git(root, "ls-files", "--others", "--exclude-standard")[0]).splitlines() if x.strip() and x.strip() != "portal"}
    changed = committed | working
    extra = [f for f in changed if f != HANDLER and not f.startswith(own) and not (f.startswith(TESTS) and f.rsplit("/", 1)[-1].startswith("test_filled_report_pass_options"))]
    need(not extra, "files outside the agreed set changed: %s" % sorted(extra)[:4])
    need(HANDLER in changed and any(f.startswith(TESTS) for f in changed), "handler.py and a test_filled_report_pass_options* file must both be in the change")
    o_out, o_in = blocks(old)
    n_out, n_in = blocks(new)
    need(o_out == n_out, "handler.py changed OUTSIDE the FILLED-REPORT-A block")
    import difflib
    d = [ln for ln in difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm="", n=0) if ln[:1] in "+-" and ln[:3] not in ("+++", "---")]
    removed, added = [x for x in d if x[0] == "-"], [x for x in d if x[0] == "+"]
    need(len(removed) <= 20 and len(added) <= 80, "handler.py may remove at most 20 lines and add at most 80 (removed %d, added %d)" % (len(removed), len(added)))
    check_block("\n".join(n_in), added)
    return True


def check_block(block, added):
    need(block.count("put_object(") == 1 and "FILLED_REPORT_SWITCH = \"FILLED_REPORT_PASS\"" in block, "the block holds exactly one put_object and the unchanged switch name")
    need(not [x for x in added if re.search(r"\bprint\(|logging|\.delete_object|\.copy_object|\.put_object_|os\.environ\[", x)], "no print, log, delete, copy or environment write may be added")
    return True


# ------------------------------------------------------------------------------------------------ AC2
def check_behaviour(root):
    root = Path(root)
    pkg = str(root / PKG.rstrip("/"))
    for p in (pkg, str(root)):
        if p not in sys.path:
            sys.path.insert(0, p)
    for m in [m for m in list(sys.modules) if m in ("handler", "publisher")]:
        sys.modules.pop(m, None)
    import handler as h
    doc = {
        "household": {"household_ref": "hh_SYNTH1", "as_of": "2026-09-30", "first_data_date": "2024-01-02",
                      "accounts": [{"account_id": "acc_0000000000000000000000a1", "account_id_form": "minted", "last4": "0001", "first_data_date": "2024-01-02",
                                    "window_status": {"qtd": "MEASURED", "ytd": "MEASURED", "last_12_months": "MEASURED", "since_inception": "MEASURED"}}]},
        "values": {"pvs.ytd.total_return": 1.5, "label.household": "Synthetic household"},
    }

    class S3:
        def __init__(self):
            self.puts = []

        def put_object(self, Bucket, Key, Body, ContentType):  # noqa: N803
            self.puts.append(Key)
    reads = []
    saved = (h.resolve_firm, h.read_filled_report_gold, os.environ.get("FILLED_REPORT_PASS"))
    h.resolve_firm = lambda source=None: ("src", "49financial")

    def reader(firm, cid, **kw):
        reads.append(cid)
        return doc
    h.read_filled_report_gold = reader
    directory = {"entries": [{"ids": {"client_id": c, "account_ids": ["acc_%024d" % i]}} for i, c in enumerate(IDS)]}
    try:
        os.environ["FILLED_REPORT_PASS"] = "1"

        def fire(event):
            s3 = S3()
            del reads[:]
            return h.filled_report_fire(event, None, s3=s3, directory=directory), s3
        out, s3 = fire({"filled_report": True})
        need(out == {"enabled": True, "clients": 25, "written": 25, "not_available": [], "refused": []} and len(set(s3.puts)) == 25, "default: every directory client written once, the response keys unchanged")
        out, s3 = fire({"filled_report": True, "clients": [IDS[3], IDS[1], IDS[3]]})
        need(out["clients"] == 2 and out["written"] == 2 and len(s3.puts) == 2 and sorted(reads) == sorted([IDS[1], IDS[3]]), "clients: exactly the named clients, once each")
        out, s3 = fire({"filled_report": True, "dry_run": True})
        need(s3.puts == [] and out.get("dry_run") is True and out["written"] == 25 and len(reads) == 25, "dry run: every client read and validated, nothing written, marked dry_run")
        seen = []
        for k in range(7):
            out, s3 = fire({"filled_report": True, "shard": k, "shards": 7})
            need(out["shard"] == k and out["shards"] == 7, "a sharded response names its shard")
            seen += s3.puts
        need(len(seen) == 25 and len(set(seen)) == 25, "seven shards must write every client exactly once")
        total = 0
        for k in range(3):
            o, _ = fire({"filled_report": True, "clients": IDS[:10], "shard": k, "shards": 3})
            total += o["written"]
        need(total == 10, "clients and shards combine as an intersection")
        o, s3 = fire({"filled_report": True, "clients": [IDS[0]], "dry_run": True, "shard": 0, "shards": 1})
        need(o["written"] == 1 and s3.puts == [], "all three options together")
        bad = [{"shard": 1}, {"shards": 3}, {"shard": 3, "shards": 3}, {"shard": -1, "shards": 3}, {"shard": 0, "shards": 0}, {"shard": "0", "shards": 3}, {"shard": True, "shards": 3},
               {"dry_run": "yes"}, {"clients": []}, {"clients": "cli_S01"}, {"clients": ["S01"]}, {"clients": [IDS[0], "cli_NOT_THERE"]}]
        for extra in bad:
            s3 = S3()
            del reads[:]
            try:
                h.filled_report_fire(dict(extra, filled_report=True), None, s3=s3, directory=directory)
            except SystemExit as e:
                need("REFUSED" in str(e), "a malformed option must be refused with a REFUSED line: %s" % extra)
            else:
                raise Fail("a malformed option was accepted: %s" % extra)
            need(s3.puts == [] and reads == [], "a refused option must read and write nothing: %s" % extra)
        os.environ["FILLED_REPORT_PASS"] = "0"
        s3 = S3()
        del reads[:]
        o = h.filled_report_fire({"filled_report": True, "shard": 99, "clients": "garbage"}, None, s3=s3, directory=directory)
        need(o == {"enabled": False, "clients": 0, "written": 0, "not_available": [], "refused": []} and s3.puts == [] and reads == [], "switch off: returns at once whatever the options")
    finally:
        h.resolve_firm, h.read_filled_report_gold = saved[0], saved[1]
        if saved[2] is None:
            os.environ.pop("FILLED_REPORT_PASS", None)
        else:
            os.environ["FILLED_REPORT_PASS"] = saved[2]
    return True


# ------------------------------------------------------------------------------------------------ AC3
def check_tests(root):
    root = Path(root)
    new = set()
    for f in (root / TESTS).glob("test_filled_report_pass_options*.py"):
        new |= set(re.findall(r"^def (test_\w+)\(", f.read_bytes().decode("utf-8"), flags=re.M))
    need(len([n for n in new if "options" in n]) >= 6, "at least six NEW tests carry options in their name, found %s" % sorted(new))
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", str(root / TESTS.rstrip("/"))], capture_output=True, text=True, cwd=str(root))
    need(r.returncode == 0, "pytest failed: %s" % (r.stdout + r.stderr)[-500:].replace("\n", " | "))
    need(re.search(r"\d+ passed", r.stdout) is not None, "pytest printed no pass count")
    return True


CHECKS = {"DB192-1-AC1": check_diff, "DB192-1-AC2": check_behaviour, "DB192-1-AC3": check_tests}


def selftest(ref_root):
    ref = Path(ref_root)
    for fn in CHECKS.values():
        try:
            fn(ref)
        except Fail as e:
            if fn is check_diff and "no issued_to" in str(e):
                continue  # the reference tree carries no order file
            raise
    h = ref / HANDLER
    s0 = h.read_bytes()
    txt = s0.decode("utf-8")
    muts = {
        "the dry run still writes": ("        if dry:\n            return\n", ""),
        "the shard filter is skipped": ("    if shards is not None:\n        ids = [c for c in ids if shard_of(c, shards) == shard]\n", ""),
        "an unknown named client is accepted": ("        if unknown:\n            raise SystemExit(\"REFUSED: %d named client(s) are not in the directory\" % len(unknown))\n", ""),
        "dry_run is not validated": ("    if dry is not None and not isinstance(dry, bool):\n        raise SystemExit(\"REFUSED: dry_run must be a boolean or absent\")\n", ""),
        "shard without shards is accepted": ("    shard, shards = event.get(\"shard\"), event.get(\"shards\")\n    if (shard is None) != (shards is None):\n        raise SystemExit(\"REFUSED: shard and shards come together\")\n    if shards is not None:\n        ints", "    shard, shards = event.get(\"shard\"), event.get(\"shards\")\n    if shards is not None:\n        ints"),
        "the options are read before the switch": ("    if not filled_report_enabled():\n        return run_filled_report(None, [], None)\n    named, dry, shard, shards = _filled_options(event)", "    named, dry, shard, shards = _filled_options(event)\n    if not filled_report_enabled():\n        return run_filled_report(None, [], None)"),
        "the named list is not deduplicated": ("        ids = sorted(set(named))", "        ids = sorted(named)"),
    }
    n = 0
    try:
        for label, (a, b) in muts.items():
            assert txt.count(a) == 1, "selftest: the anchor for '%s' must occur exactly once in the reference (found %d)" % (label, txt.count(a))
            h.write_bytes(txt.replace(a, b, 1).encode("utf-8"))
            try:
                check_behaviour(ref)
            except (Fail, AssertionError, Exception, SystemExit):  # noqa: BLE001 -- a refusal that escapes the switch-off arm is also a red mutant
                n += 1
                continue
            raise AssertionError("mutant passed the behaviour check: " + label)
    finally:
        h.write_bytes(s0)
    block = "\n".join(blocks(txt)[1])
    put = 's3.put_object(Bucket=b, Key=k, Body=body, ContentType="application/json")'
    for label, blk, add in (("a second write path", block.replace(put, put + "\n        " + put.replace("Key=k", "Key=k + '.c'")), []),
                            ("a print", block, ["+    print(out)"]), ("a delete", block, ["+    s3.delete_object(Bucket=b, Key=k)"])):
        try:
            check_block(blk, add)
        except Fail:
            n += 1
            continue
        raise AssertionError("mutant passed the block check: " + label)
    check_block(block, [])
    print("selftest: green on the reference and red on %d single-fault mutants" % n)
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest(sys.argv[2])
        sys.exit(0)
    try:
        CHECKS[sys.argv[2]](sys.argv[1])
        print({"DB192-1-AC1": "OK: only handler.py (inside the FILLED-REPORT-A block) and the new test file changed; one put_object; nothing printed",
               "DB192-1-AC2": "OK: default unchanged; a named subset; a dry run writing nothing; seven shards partition once; the intersection; malformed options refused with no read or write; the switch off first",
               "DB192-1-AC3": "OK: six or more new options tests exist and the whole reporting-publish test directory passes"}[sys.argv[2]])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read or run is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
