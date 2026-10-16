"""IRPT_DASHBD round 149, workstream FILLEDPASS (issuer 2.0.0_SA_COO~D2) -- DB-b-305, the hop-2 pass survives a household the reader refuses (worker row IRPT_DASHBD-D2-W243-S1): `run_filled_report` catches
`publisher.PublishRefused` raised by the READER, records the client in `refused` and goes on to the next client, as it already does for a document the publisher refuses at publish. Nothing else moves.

  DB173-1-AC1  the diff: handler.py differs from the base only inside run_filled_report; publisher.py and locals.tf are byte-identical to the base
  DB173-1-AC2  the behaviour: a reader that raises PublishRefused for one client leaves the pass writing the others; NotYetAvailable still records not_available; any other exception still propagates; the switch off reads and writes nothing
  DB173-1-AC3  the tests: at least three NEW tests whose names carry reader_refused, and both filled-report test files pass

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest <reference_root>      green on a reference tree, red on single-fault mutants of its handler
"""
import re
import subprocess
import sys
from pathlib import Path

BASE = "aec0df87fc7ea13e95017bcb9ce92a6bdc840430"
LAMBDA = "infra/aws/lambda/investor-reporting/reporting-publish/"
HANDLER = LAMBDA + "handler.py"
PUBLISHER = LAMBDA + "publisher.py"
LOCALS = "infra/aws/terraform/investor-reporting/reporting-publish/locals.tf"
T_PUBLISH = LAMBDA + "tests/test_filled_report_publish.py"
T_READER = LAMBDA + "tests/test_filled_report_reader.py"
FIRM = "49financial"


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def git_show(root, rel):
    r = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (BASE, rel)], capture_output=True)
    need(r.returncode == 0, "cannot read %s at the base %s" % (rel, BASE[:10]))
    return r.stdout


def rd(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    return p.read_bytes()


def func_span(text, name):
    m = re.search(r"^def %s\(.*?(?=^def |^class |^# END FILLED-REPORT-A|\Z)" % re.escape(name), text, flags=re.S | re.M)
    need(m, "no def %s" % name)
    return m.group(0)


def check_diff(root):
    new_h, old_h = rd(root, HANDLER).decode("utf-8"), git_show(root, HANDLER).decode("utf-8")
    need("\r" not in new_h, "handler.py must keep LF line endings")
    new_f, old_f = func_span(new_h, "run_filled_report"), func_span(old_h, "run_filled_report")
    need(new_f != old_f, "run_filled_report is unchanged")
    need(new_h.replace(new_f, "<<f>>") == old_h.replace(old_f, "<<f>>"), "handler.py differs from the base outside run_filled_report")
    need("PublishRefused" in new_f and new_f.count("except") >= 3, "run_filled_report must catch PublishRefused around the reader as well as around the publish")
    for rel in (PUBLISHER, LOCALS):
        need(rd(root, rel) == git_show(root, rel), "%s must be byte-identical to the base" % rel.rsplit("/", 1)[-1])
    return True


def check_behaviour(root):
    root = Path(root)
    sys.path[:0] = [str(root / LAMBDA.rstrip("/")), str(root)]
    for m in ("handler", "publisher"):
        sys.modules.pop(m, None)
    import handler as h  # noqa: E402
    import publisher as p  # noqa: E402
    doc = {"household": {"household_ref": "hh1", "as_of": "2026-10-15", "first_data_date": "2024-01-02",
                         "accounts": [{"account_id": "a", "last4": "0001", "first_data_date": "2024-01-02", "window_status": {w: "MEASURED" for w in ("qtd", "ytd", "last_12_months", "since_inception")}}]}, "values": {}}
    calls = []

    def reader(firm, cid):
        calls.append(cid)
        if cid == "cli_A":
            raise p.PublishRefused("a household that cannot be composed")
        if cid == "cli_B":
            raise h.NotYetAvailable("no rows")
        if cid == "cli_X":
            raise RuntimeError("an unexpected failure must not be swallowed")
        return doc
    puts = {}
    put = lambda a, b: puts.__setitem__(a, b)  # noqa: E731
    on = {"FILLED_REPORT_PASS": "1"}
    out = h.run_filled_report(FIRM, ["cli_C", "cli_A", "cli_B", "cli_D"], put, reader=reader, environ=on)
    need(out["refused"] == ["cli_A"] and out["not_available"] == ["cli_B"] and out["written"] == 2 and out["clients"] == 4, "a reader refusal must be recorded and the pass must go on: %s" % out)
    need(sorted(puts) == sorted(p.report_address(FIRM, c) for c in ("cli_C", "cli_D")) and calls == ["cli_A", "cli_B", "cli_C", "cli_D"], "the clients after the refused one must still be read and written")
    try:
        h.run_filled_report(FIRM, ["cli_X"], put, reader=reader, environ=on)
    except RuntimeError:
        pass
    else:
        raise Fail("an unexpected reader exception was swallowed")
    puts.clear()
    calls.clear()
    off = h.run_filled_report(FIRM, ["cli_C", "cli_A"], put, reader=reader, environ={})
    need(off["enabled"] is False and not calls and not puts, "the switch off must read and write nothing")
    bad = dict(doc, notes="extra")
    out2 = h.run_filled_report(FIRM, ["cli_E"], put, reader=lambda f, c: bad, environ=on)
    need(out2["refused"] == ["cli_E"] and out2["written"] == 0 and not puts, "a document the publisher refuses is still recorded as refused and not written")
    return True


def check_tests(root):
    root = Path(root)
    new = set()
    for rel in (T_PUBLISH, T_READER):
        txt = rd(root, rel).decode("utf-8")
        try:
            base_txt = git_show(root, rel).decode("utf-8")
        except Fail:
            base_txt = ""
        new |= set(re.findall(r"^def (test_\w+)\(", txt, flags=re.M)) - set(re.findall(r"^def (test_\w+)\(", base_txt, flags=re.M))
    need(len([n for n in new if "reader_refused" in n]) >= 3, "at least three NEW tests carry reader_refused in their name, found %s" % sorted(new))
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "--color=no", str(root / T_PUBLISH), str(root / T_READER)], capture_output=True, text=True, cwd=str(root))
    need(r.returncode == 0, "pytest failed: %s" % (r.stdout + r.stderr)[-400:].replace("\n", " | "))
    need(re.search(r"\d+ passed", r.stdout) is not None, "pytest printed no pass count")
    return True


CHECKS = {"DB173-1-AC1": check_diff, "DB173-1-AC2": check_behaviour, "DB173-1-AC3": check_tests}


def selftest(ref_root):
    ref = Path(ref_root)
    for fn in CHECKS.values():
        fn(ref)
    handler = ref / HANDLER
    original = handler.read_bytes()
    txt = original.decode("utf-8")
    anchor = "        except publisher.PublishRefused:\n            out[\"refused\"].append(cid)\n            continue\n        try:"
    muts = {
        "the reader refusal is not caught": (anchor, "        try:"),
        "every exception is swallowed": ("        except NotYetAvailable:\n            out[\"not_available\"].append(cid)\n            continue\n", "        except NotYetAvailable:\n            out[\"not_available\"].append(cid)\n            continue\n        except Exception:\n            out[\"refused\"].append(cid)\n            continue\n"),
        "a reader refusal is counted as not available": (anchor, "        except publisher.PublishRefused:\n            out[\"not_available\"].append(cid)\n            continue\n        try:"),
    }
    n = 0
    try:
        for label, (a, b) in muts.items():
            need(a in txt, "selftest: the reference lacks the anchor for '%s'" % label)
            handler.write_bytes(txt.replace(a, b, 1).encode("utf-8"))
            try:
                check_behaviour(ref)
            except (Fail, AssertionError, Exception):  # noqa: BLE001
                n += 1
                continue
            raise AssertionError("mutant passed: " + label)
        handler.write_bytes(txt.replace("def lambda_handler(event, context=None):", "def lambda_handler(event, context=None):  # touched", 1).encode("utf-8"))
        try:
            check_diff(ref)
        except Fail:
            n += 1
        else:
            raise AssertionError("diff mutant passed")
    finally:
        handler.write_bytes(original)
    print("selftest: green on the reference and red on %d single-fault mutants" % n)
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest(sys.argv[2])
        sys.exit(0)
    try:
        CHECKS[sys.argv[2]](sys.argv[1])
        print({"DB173-1-AC1": "OK: handler.py differs from the base only inside run_filled_report, which now catches PublishRefused around the reader; publisher.py and locals.tf are byte-identical to the base",
               "DB173-1-AC2": "OK: a reader refusal is recorded and the pass goes on to the next clients; NotYetAvailable is still recorded as not available; an unexpected exception still propagates; the switch off reads and writes nothing; a document the publisher refuses is still counted refused",
               "DB173-1-AC3": "OK: three or more new reader_refused tests exist and both filled-report test files pass"}[sys.argv[2]])
        print(sys.argv[2] + " PASS")
    except Exception as ex:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(ex))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
