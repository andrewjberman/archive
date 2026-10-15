"""IRPT_DASHBD round 116, workstream B-IN (issuer 2.0.0_SA_COO~I2) -- the Orion account-level performance read (CTO round-116 analysis, msg 7978).

  DB-i-4 (~304) does Orion's API, as the estate's pull code reaches it, expose an ACCOUNT-level performance or return series: the endpoint, the grain, the fields
              (return, period, gross or net) and whether the pull's credential reaches it. A READ of repo code, fixtures and docs: no vendor call.   DBI116-1-AC1

The checker RECOMPUTES the endpoint inventory (every `/api/vN/...` literal in the `*.py` files directly inside each directory under infra/aws/lambda/inf-pipeline/ and inside
infra/aws/lambda/investor-reporting/performance/), and VERIFIES every cited evidence line: the file exists, the line exists, and the quoted text is on that line.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]         the pure helpers on synthetic arms
"""
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("p114_bin", str(HERE.parent / "r114" / "p114_bin.py"))
P114 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P114)
Fail, need = P114.Fail, P114.need

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~304/ORION_ACCOUNT_PERFORMANCE_READ_R116.json"
ANSWERS = ("YES", "NO", "UNDETERMINED")
CRED = ("REACHES", "DOES_NOT_REACH", "UNDETERMINED")
GROSS_NET = ("GROSS", "NET", "BOTH", "UNDETERMINED")
SECTIONS = ("endpoint", "grain", "fields", "gross_or_net", "credential")
ENDPOINT_RX = re.compile(r"/api/v\d+/[A-Za-z0-9_/{}.\-]*")
POOLS = ("infra/aws/lambda/inf-pipeline", "infra/aws/lambda/investor-reporting/performance")


def norm(path):
    return path.rstrip("/.,")


def pool_files(root):
    """The *.py files directly inside each directory under inf-pipeline/, and inside investor-reporting/performance/."""
    r = Path(root)
    dirs = [p for p in sorted((r / POOLS[0]).iterdir()) if p.is_dir()] + [r / POOLS[1]]
    out = []
    for d in dirs:
        out += sorted(d.glob("*.py"))
    return out


def inventory(root):
    inv = set()
    files = pool_files(root)
    for f in files:
        for m in ENDPOINT_RX.findall(f.read_text(encoding="utf-8")):
            inv.add(norm(m))
    return sorted(inv), len(files)


def verify_evidence(root, ev, where):
    need(isinstance(ev, list) and ev, where + ": evidence must be a non-empty list")
    for e in ev:
        p = Path(root) / e["file"]
        need(p.is_file(), where + ": cited file absent: " + e["file"])
        lines = p.read_text(encoding="utf-8").splitlines()
        n = e["line"]
        need(isinstance(n, int) and 1 <= n <= len(lines), where + ": cited line out of range: %s:%s" % (e["file"], n))
        need(isinstance(e["quote"], str) and len(e["quote"]) >= 6 and e["quote"] in lines[n - 1],
             where + ": the quote is not on the cited line %s:%s" % (e["file"], n))


def check(root):
    rec = P114.load(root, REC_REL)
    P114.no_identifiers(rec)
    P114.common_flags(rec)
    need(isinstance(rec.get("basis_words"), str) and len(rec["basis_words"]) > 120, "basis_words missing")
    inv, nfiles = inventory(root)
    need(rec.get("pool_files_read") == nfiles, "pool_files_read differs from the recount (%d)" % nfiles)
    need(rec.get("endpoint_inventory") == inv, "endpoint_inventory differs from the checker's recount over the pool files")
    ans = rec.get("account_level_exists")
    need(ans in ANSWERS, "account_level_exists must be one of YES, NO, UNDETERMINED")
    for s in SECTIONS:
        sec = rec.get(s)
        need(isinstance(sec, dict), "section %s missing" % s)
        need(sec.get("claim") in P114.CLAIMS, "section %s: claim" % s)
        verify_evidence(root, sec.get("evidence"), s)
    if ans == "YES":
        ep = rec["endpoint"]
        need(norm(ep.get("path", "")) in inv, "endpoint.path is not in the endpoint inventory")
        need(ep.get("method") in ("GET", "POST"), "endpoint.method")
        need(isinstance(ep.get("host"), str) and ep["host"], "endpoint.host")
        need(isinstance(rec["grain"].get("words"), str) and len(rec["grain"]["words"]) > 20, "grain.words")
        need(isinstance(rec["fields"].get("names"), list) and rec["fields"]["names"], "fields.names")
    else:
        need(isinstance(rec.get("reason_words"), str) and len(rec["reason_words"]) > 40, "reason_words required when the answer is not YES")
    need(rec["gross_or_net"].get("answer") in GROSS_NET, "gross_or_net.answer")
    need(rec["credential"].get("answer") in CRED, "credential.answer")
    need(isinstance(rec["credential"].get("secret_named_not_read"), bool) and rec["credential"]["secret_named_not_read"], "credential.secret_named_not_read must be true: the secret is named, never read")


def selftest():
    arms = []

    def arm(name, ok):
        arms.append((name, ok))

    arm("norm", norm("/api/v1/Reporting/Scope.") == "/api/v1/Reporting/Scope" and norm("/api/v1/X/") == "/api/v1/X")
    arm("rx", ENDPOINT_RX.findall("post('/api/v1/Reporting/Scope', x) /api/v2/A/{id}/b") == ["/api/v1/Reporting/Scope", "/api/v2/A/{id}/b"])
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "a.py").write_text("line one\nthe quote here\n", encoding="utf-8")
        ok = {"file": "a.py", "line": 2, "quote": "the quote"}
        try:
            verify_evidence(td, [ok], "t")
            green = True
        except Fail:
            green = False
        arm("evidence green", green)
        red = False
        try:
            verify_evidence(td, [{"file": "a.py", "line": 1, "quote": "the quote"}], "t")
        except Fail:
            red = True
        arm("evidence red (quote on another line)", red)
        red2 = False
        try:
            verify_evidence(td, [], "t")
        except Fail:
            red2 = True
        arm("evidence red (empty)", red2)
    for n, v in arms:
        print(("ok   " if v else "FAIL ") + n)
    return all(v for _, v in arms)


def main(argv):
    if argv and argv[0] == "--selftest":
        sys.exit(0 if selftest() else 1)
    if len(argv) != 2 or argv[1] != "DBI116-1-AC1":
        print("usage: <root> DBI116-1-AC1")
        sys.exit(2)
    try:
        check(argv[0])
    except Fail as e:
        print("%s FAIL: %s" % (argv[1], e))
        print("%s FAIL" % argv[1])
        sys.exit(1)
    except Exception as e:  # a checker error is a FAIL, never a pass
        print("%s FAIL: checker error %s: %s" % (argv[1], type(e).__name__, e))
        print("%s FAIL" % argv[1])
        sys.exit(1)
    print("%s PASS" % argv[1])


if __name__ == "__main__":
    main(sys.argv[1:])
