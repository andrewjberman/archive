"""y2_check.py <id>: the round-25 (workstream GATEWAY) criteria of cell MX-y-2, run from the repository root.
Ids: y2.AC1 (a send is graded on the tester's read-back; the chat tool is preview-only), y2.AC2 (everything else is unchanged: byte-identical grades of the
round-22 and round-23 battery fixtures against baselines taken from the unchanged script, the refusals, determinism), y2.AC3 (pytest on the battery tests).
Prints a DENOMINATOR line, one line per arm, then ARMS and RESULT: PASS|FAIL. ASCII only; python 3.9.
The script directory is workflows/gateway_battery unless the environment names another (Y2_PKG_DIR); the issuer uses that to try a reference.
The contract is decompositions/NFRA_MCPINDEX_DECOMP.round25-GATEWAY.md R25.3 (Y2)."""
import copy
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
R25 = os.path.normpath(os.path.join(HERE, ".."))
FIX = os.path.join(R25, "fixtures")
DELIV = os.path.normpath(os.path.join(R25, "..", ".."))
R22FIX = os.path.join(DELIV, "2.0.0_SA_COO~MI", "round22", "fixtures")
R23FIX = os.path.join(DELIV, "2.0.0_SA_COO~MI", "round23", "fixtures")
PKG = os.environ.get("Y2_PKG_DIR") or os.path.join("workflows", "gateway_battery")
BATT = os.path.join(PKG, "tool_battery.py")
TESTS = [os.path.join(PKG, "tests", n) for n in ("test_tool_battery.py", "test_tool_battery_route.py", "test_tool_battery_send.py")]
MIN_PASSED = 28   # the 12 round-22 tests, the 10 round-23 route tests and at least 6 new ones
OK, BAD = [], []


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def fx(name):
    return os.path.join(FIX, name)


def run(args, timeout=120):
    if args and args[0].endswith(".py") and not os.path.isfile(args[0]):
        return 98, "", "script absent: %s" % args[0]
    try:
        p = subprocess.run([sys.executable] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        return 99, "", "%s: %s" % (type(exc).__name__, exc)
    return p.returncode, p.stdout.decode("utf-8", "replace").replace("\r", ""), p.stderr.decode("utf-8", "replace").replace("\r", "")


def jload(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return json.load(fh)


def jdump(obj, path):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1)


def line(out, prefix):
    for ln in out.splitlines():
        if ln.startswith(prefix):
            return ln.strip()
    return None


def tool_row(doc, name):
    for t in (doc or {}).get("tools", []):
        if t.get("tool") == name:
            return t
    return {}


def case_row(doc, cid):
    for c in (doc or {}).get("cases", []):
        if c.get("case_id") == cid:
            return c
    return {}


def get(res_doc, cid):
    return [x for x in res_doc["results"] if x["case_id"] == cid][0]


def grade(tmp, tag, results_doc, extra=()):
    rp = os.path.join(tmp, "res_%s.json" % tag)
    out = os.path.join(tmp, "graded_%s.json" % tag)
    jdump(results_doc, rp)
    rc, so, se = run([BATT, "grade", "--census", fx("y2_census.json"), "--cases", fx("y2_cases.json"), "--results", rp, "--out", out] + list(extra))
    return rc, so, se, (jload(out) if os.path.isfile(out) else None)


def ac1(tmp):
    print("DENOMINATOR: fixture y2 -- 5 tools in one native channel: send_email and create_draft each with a sent result carrying a read-back (S1, S2), reply_email "
          "and send_chat_message each with an unsent preview result (S3, S4), whoami a plain read (S5); 8 variants of the green results planted from that data")
    base = jload(fx("y2_results.json"))
    rc, so, se, doc = grade(tmp, "green", base)
    arm("green: send_email and create_draft are PASS on their agreeing read-back; reply_email and send_chat_message are PREVIEW-ONLY; no FAIL; rc 0",
        rc == 0 and doc is not None and tool_row(doc, "send_email").get("verdict") == "PASS" and tool_row(doc, "create_draft").get("verdict") == "PASS"
        and tool_row(doc, "reply_email").get("verdict") == "PREVIEW-ONLY" and tool_row(doc, "send_chat_message").get("verdict") == "PREVIEW-ONLY",
        "rc=%s %r %s" % (rc, line(so, "GRADE"), se[-200:]))
    arm("green: the GRADE line reads PASS=3 PREVIEW-ONLY=2 FAIL=0 and the REALIZED line names send_chat_message",
        line(so, "GRADE") == "GRADE tools=5 PASS=3 EMPTY-CORRECT=0 REFUSED-CORRECT=0 PREVIEW-ONLY=2 FAIL=0"
        and line(so, "PREVIEW-ONLY TOOLS") == "PREVIEW-ONLY TOOLS: reply_email, send_chat_message", "%r %r" % (line(so, "GRADE"), line(so, "PREVIEW-ONLY TOOLS")))
    arm("green: the graded file lists send_chat_message in preview_only and the sent case row reads PASS with no fail class",
        doc is not None and "send_chat_message" in doc.get("preview_only", []) and case_row(doc, "S1").get("verdict") == "PASS" and case_row(doc, "S1").get("fail_class") is None,
        "%r %r" % ((doc or {}).get("preview_only"), case_row(doc, "S1")))

    def variant(label, edit, want_rc, tool, want_class):
        r = copy.deepcopy(base)
        edit(r)
        rc2, so2, se2, d2 = grade(tmp, label.replace(" ", "_")[:20], r)
        arm("%s" % label, rc2 == want_rc and tool_row(d2, tool).get("fail_class") == want_class and (want_class is None or tool_row(d2, tool).get("verdict") == "FAIL"),
            "rc=%s %r" % (rc2, tool_row(d2, tool)))
        return d2

    variant("planted: a sent result with NO readback is FAIL send_unconfirmed", lambda r: get(r, "S1").pop("readback"), 1, "send_email", "send_unconfirmed")
    variant("planted: a sent result with readback null is FAIL send_unconfirmed", lambda r: get(r, "S1").update(readback=None), 1, "send_email", "send_unconfirmed")
    variant("planted: a readback that does not agree (false) is FAIL send_unconfirmed", lambda r: get(r, "S1")["readback"].update(agrees=False), 1, "send_email", "send_unconfirmed")
    variant("planted: a readback that could not be read (agrees null) is FAIL send_unconfirmed", lambda r: get(r, "S2")["readback"].update(agrees=None), 1, "create_draft", "send_unconfirmed")
    d = variant("planted: the chat tool with NO result is still PREVIEW-ONLY, not not_run", lambda r: r.update(results=[x for x in r["results"] if x["case_id"] != "S4"]),
                0, "send_chat_message", None)
    arm("planted: ... and that tool reads PREVIEW-ONLY", tool_row(d, "send_chat_message").get("verdict") == "PREVIEW-ONLY", "%r" % tool_row(d, "send_chat_message"))
    variant("planted: a chat SEND without a readback is FAIL send_unconfirmed (no longer a preview)", lambda r: get(r, "S4").update(sent=True, status="ok", rows=1),
            1, "send_chat_message", "send_unconfirmed")
    variant("planted: another tool with no result (reply_email) is still FAIL not_run", lambda r: r.update(results=[x for x in r["results"] if x["case_id"] != "S3"]),
            1, "reply_email", "not_run")
    rp = os.path.join(tmp, "routing_sent.json")
    jdump(jload(fx("y2_routing.json")), rp)
    rc3, so3, se3, d3 = grade(tmp, "routed", base, ["--routing", rp])
    arm("with --routing a sent PASS is not routed (route null) and still PASS; the plain read is routed",
        rc3 == 0 and case_row(d3, "S1").get("verdict") == "PASS" and case_row(d3, "S1").get("route") is None and case_row(d3, "S5").get("route") == "code-cited",
        "rc=%s %r %r" % (rc3, case_row(d3, "S1"), case_row(d3, "S5")))


def same_bytes(a, b):
    with open(a, "rb") as fa, open(b, "rb") as fb:
        return fa.read().replace(b"\r", b"") == fb.read().replace(b"\r", b"")


def ac2(tmp):
    print("DENOMINATOR: the round-22 fixtures (expected_census, cases_min, results_min) and the round-23 h6 fixtures graded by the script and compared byte for byte with "
          "baselines taken from the unchanged script (y2_base_*), 4 refusals, determinism, and the planted send of round 22 now classed send_unconfirmed")
    for tag, args in (("g22", ["--census", os.path.join(R22FIX, "expected_census.json"), "--cases", os.path.join(R22FIX, "cases_min.json"), "--results", os.path.join(R22FIX, "results_min.json")]),
                      ("h6", ["--census", os.path.join(R22FIX, "expected_census.json"), "--cases", os.path.join(R23FIX, "h6_cases.json"), "--results", os.path.join(R23FIX, "h6_results.json"),
                              "--channel", "opal-data-harvest", "--channel", "opal-data-assets", "--routing", os.path.join(R23FIX, "h6_routing.json")])):
        out = os.path.join(tmp, "g_%s.json" % tag)
        rc, so, se = run([BATT, "grade"] + args + ["--out", out])
        base_out, base_so = fx("y2_base_%s_graded.json" % tag), fx("y2_base_%s_stdout.txt" % tag)
        arm("%s fixtures: the graded file is byte-identical to the unchanged script's" % tag, os.path.isfile(out) and same_bytes(out, base_out), "differs or absent (rc=%s %s)" % (rc, se[-160:]))
        with open(base_so, encoding="utf-8", errors="replace") as fh:
            want_so = fh.read().replace("\r", "")
        arm("%s fixtures: the stdout is identical to the unchanged script's" % tag, so == want_so, "got %r" % so[:200])
    # the round-22 planted send: still a FAIL with rc 1, now of the new class
    r22 = jload(os.path.join(R22FIX, "results_min.json"))
    get(r22, "C8")["sent"] = True
    rp = os.path.join(tmp, "r22_sent.json")
    jdump(r22, rp)
    out = os.path.join(tmp, "g_r22sent.json")
    rc, so, se = run([BATT, "grade", "--census", os.path.join(R22FIX, "expected_census.json"), "--cases", os.path.join(R22FIX, "cases_min.json"), "--results", rp, "--out", out])
    doc = jload(out) if os.path.isfile(out) else None
    arm("the round-22 planted send (C8 sent, no readback) is still FAIL with rc 1, class send_unconfirmed (it was `sent`)",
        rc == 1 and tool_row(doc, "send_email").get("verdict") == "FAIL" and tool_row(doc, "send_email").get("fail_class") == "send_unconfirmed",
        "rc=%s %r" % (rc, tool_row(doc, "send_email")))
    base = jload(fx("y2_results.json"))

    def refused(label, edit):
        r = copy.deepcopy(base)
        edit(r)
        rp2 = os.path.join(tmp, "ref_%s.json" % abs(hash(label)))
        outp = os.path.join(tmp, "refout_%s.json" % abs(hash(label)))
        jdump(r, rp2)
        rc2, so2, se2 = run([BATT, "grade", "--census", fx("y2_census.json"), "--cases", fx("y2_cases.json"), "--results", rp2, "--out", outp])
        arm(label, rc2 == 2 and "REFUSED" in se2 and not os.path.isfile(outp), "rc=%s stderr=%r out=%s" % (rc2, se2[-160:], os.path.isfile(outp)))

    refused("refused (rc 2, REFUSED, no output file): a readback on a result that was not sent", lambda r: get(r, "S3").update(readback={"agrees": True, "instrument": "x"}))
    refused("refused: a readback whose agrees is not a boolean or null", lambda r: get(r, "S1")["readback"].update(agrees="yes"))
    refused("refused: a readback without an instrument", lambda r: get(r, "S1")["readback"].pop("instrument"))
    refused("refused: a readback that is not an object", lambda r: get(r, "S1").update(readback="seen"))
    rc1, so1, se1, d1 = grade(tmp, "det1", base)
    rc2, so2, se2, d2 = grade(tmp, "det2", base)
    arm("two runs on the same input give the same bytes", d1 is not None and json.dumps(d1, sort_keys=True) == json.dumps(d2, sort_keys=True) and so1 == so2, "differs or absent")


def ac3(tmp):
    missing = [t for t in TESTS if not os.path.isfile(t)]
    if missing:
        print("DENOMINATOR: test file(s) absent: %s" % ", ".join(missing))
        arm("pytest on the three battery test files passes with at least %d tests" % MIN_PASSED, False, "absent: %s" % ", ".join(os.path.basename(m) for m in missing))
        return
    p = subprocess.run([sys.executable, "-m", "pytest"] + TESTS + ["-q", "-p", "no:cacheprovider", "--color=no"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
    out = p.stdout.decode("utf-8", "replace").replace("\r", "")
    m = re.search(r"(\d+) passed", out)
    n = int(m.group(1)) if m else 0
    print("DENOMINATOR: pytest rc=%d passed=%d (minimum %d) files=%s" % (p.returncode, n, MIN_PASSED, ", ".join(os.path.basename(t) for t in TESTS)))
    arm("pytest on the three battery test files passes with at least %d tests" % MIN_PASSED, p.returncode == 0 and n >= MIN_PASSED, "rc=%d passed=%d" % (p.returncode, n))


IDS = {"y2.AC1": ac1, "y2.AC2": ac2, "y2.AC3": ac3}


def main(argv):
    if len(argv) < 2 or argv[1] not in IDS:
        print("usage: y2_check.py %s" % "|".join(sorted(IDS)))
        print("RESULT: FAIL")
        return 2
    with tempfile.TemporaryDirectory() as tmp:
        try:
            IDS[argv[1]](tmp)
        except Exception as exc:  # noqa: BLE001
            arm("the check ran to its end", False, "%s: %s" % (type(exc).__name__, exc))
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    return 0 if OK and not BAD else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
