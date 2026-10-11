"""IRPT_BCKEND round 143 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY, CODE-ONLY order:
  IB143-1  IB-pr-446  the probe's transport: what `node-port` is and why the probe uses it and not the page; whether the vendor
                      calls a job makes AFTER a capture go the same way; what changed on our side since the session bundle of
                      2026-10-05, or that nothing did (CTO msg 5579). No request, no sign-in, no host command, no AWS call.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB143-1-AC1  what the transport is and why the probe uses it, each stated from cited code lines with its claim; every transport
               the library can use is listed with where it is chosen.
  IB143-1-AC2  every vendor call a job makes after a capture is listed with its transport and the code line; they are counted by
               transport with no remainder; whether they would meet the same refusal is answered with its claim.
  IB143-1-AC3  what changed since 2026-10-05 is listed per file with its commits (or the record says nothing changed and what was
               searched), for the repo AND for what the host runs; nothing was requested anywhere; nothing is proposed to be built.
"""
import json
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~304/"
OUT = D + "IB143-1_probe_transport_read.json"
READ = D + "IB143-1_PROBE_TRANSPORT_READ.md"
CLAIMS = ("measured", "inferred", "held", "absent")


def lines_ok(x):
    return isinstance(x, list) and bool(x) and all(":" in str(v) for v in x)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB143"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    if cid == "IB143-1-AC1":
        n = a.get("node_port") or {}
        if not n.get("what_it_is") or not lines_ok(n.get("code_lines")) or n.get("claim") not in CLAIMS:
            fail("node_port needs what_it_is, code_lines (file:line) and a claim")
        w = a.get("why_the_probe_uses_it") or {}
        if not w.get("in_words") or not lines_ok(w.get("code_lines")) or w.get("claim") not in CLAIMS \
                or w.get("stated_in_code_or_inferred") not in ("stated", "inferred"):
            fail("why_the_probe_uses_it needs in_words, code_lines, a claim, and whether the reason is stated in code or inferred")
        t = a.get("transports")
        if not isinstance(t, list) or not t or any(not x.get("name") or ":" not in str(x.get("chosen_at") or "")
                                                  or x.get("carries_the_browsers_cookies") not in (True, False, None) for x in t):
            fail("transports must list each transport with its name, where it is chosen, and whether it carries the browser's cookies")
        print("OK: %d transport(s) listed; node-port stated as %s; the reason is %s" % (len(t), n["claim"], w["stated_in_code_or_inferred"]))
    elif cid == "IB143-1-AC2":
        j = a.get("job_calls_after_a_capture") or {}
        calls = j.get("calls")
        if not isinstance(calls, list) or not calls or any(not x.get("call") or not x.get("transport") or ":" not in str(x.get("code_line") or "") for x in calls):
            fail("job_calls_after_a_capture.calls must list each vendor call with its transport and code line")
        by = j.get("by_transport")
        if not isinstance(by, dict) or sum(by.values()) != len(calls):
            fail("by_transport does not account for every listed call")
        if j.get("would_meet_the_same_refusal") not in (True, False, None) or "would_meet_the_same_refusal" not in j \
                or j.get("claim") not in CLAIMS or not j.get("reason"):
            fail("job_calls_after_a_capture needs would_meet_the_same_refusal (true, false or null), a claim and a reason")
        if j["would_meet_the_same_refusal"] is None and j["claim"] != "absent":
            fail("an untold answer must carry the claim absent")
        print("OK: %d vendor call(s) after a capture, by transport %s; would meet the same refusal: %r (%s)" % (
            len(calls), by, j["would_meet_the_same_refusal"], j["claim"]))
    elif cid == "IB143-1-AC3":
        c = a.get("changes_since_2026_10_05") or {}
        if c.get("nothing_changed_in_the_repo") not in (True, False) or not isinstance(c.get("files"), list) or not c.get("paths_searched"):
            fail("changes_since_2026_10_05 needs nothing_changed_in_the_repo, files and paths_searched")
        if c["nothing_changed_in_the_repo"] and c["files"]:
            fail("the record says nothing changed and lists changed files")
        if not c["nothing_changed_in_the_repo"] and any(not x.get("path") or not x.get("commits") or not x.get("bears_on_the_probe_or_its_transport_in_words") for x in c["files"]):
            fail("each changed file needs its path, its commits and a sentence on whether it bears on the probe or its transport")
        h = c.get("what_the_host_runs") or {}
        if not isinstance(h.get("releases_since"), list) or h.get("claim") not in CLAIMS or not h.get("read_from"):
            fail("what_the_host_runs needs releases_since, a claim and read_from (the records it was read from)")
        if not isinstance(a.get("not_established"), list):
            fail("not_established is not stated")
        for k in ("vendor_requests_made", "sign_ins_made", "host_commands_run", "aws_calls_made", "changes_proposed_to_how_the_vendor_is_reached"):
            if a.get(k) != 0:
                fail("%s must be 0" % k)
        if not (root / READ).is_file():
            fail("no %s" % READ)
        print("OK: since 2026-10-05: %d file(s) changed in the repo, %d host release(s) read from records; nothing requested, nothing proposed" % (
            len(c["files"]), len(h["releases_since"])))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
