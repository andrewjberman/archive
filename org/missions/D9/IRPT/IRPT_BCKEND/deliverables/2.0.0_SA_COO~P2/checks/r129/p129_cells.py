"""IRPT_BCKEND round 129 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY order:
  IB129-1  IB-pr-431  why the YCharts host's session capture failed to sign in, and when a YCharts-path job last reached
                      READY on that host (CTO msg 4916). No sign-in is attempted.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no record).
  IB129-1-AC1  the record states the capture failure: every capture attempt found in the window with its time and code, and a
               cause statement carrying its claim (measured / inferred / held / absent) and the evidence lines behind it.
  IB129-1-AC2  the record states the last READY of a YCharts-path job on the host, or that none is in the window, with the
               window's start, the lines scanned and READY counts per day.
  IB129-1-AC3  the bounds held, by the record's own command list: every host command is listed verbatim with its SSM command id
               and terminal status; none starts, stops or restarts a unit, runs the session runner, reads or writes a secret
               value, touches a queue or calls the vendor; and no output file carries a cookie or password member.
The expectations are shape and bounds only: how many attempts there were, what the cause is and when the last READY was are
UNMEASURED by the issuer and are not fixed here.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~IB2/"
REC = D + "IB129-1_capture_failure_read.json"
CLAIMS = ("measured", "inferred", "held", "absent")
FORBIDDEN = (r"systemctl\s+(start|stop|restart|reload|enable|disable|kill)", r"(?<![\w./-])(bash|sh|node|nodejs)\s+\S*(run-ycharts-session|ycharts_session)",
             r"get-secret-value", r"put-secret-value", r"update-secret", r"sqs\s+(send|receive|delete|purge)", r"\bcurl\b", r"\bwget\b",
             r"\bkill\b", r"\brm\s", r"\bmv\s", r"(?:^|[\s;|&()0-9])>>?\s*/(?!dev/null)", r"\btee\b", r"dynamodb\s+(put|update|delete)")
SECRETISH = re.compile(r"(?i)(\"(password|passwd|sessionid|csrftoken|set-cookie|cookie)\"\s*:\s*\"[^\"]{4,})|(sessionid=[A-Za-z0-9]{8,})")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB129"))
        sys.exit(1)

    f = root / REC
    if not f.is_file():
        fail("no %s" % REC)
    a = json.loads(f.read_text(encoding="utf-8"))
    if cid == "IB129-1-AC1":
        att = a.get("capture_attempts")
        if not isinstance(att, list):
            fail("capture_attempts is not a list")
        for r in att:
            if not r.get("at_utc") or not r.get("code") or not r.get("source_line"):
                fail("a capture attempt lacks at_utc, code or source_line")
        c = a.get("cause") or {}
        if c.get("claim") not in CLAIMS or not c.get("statement") or not isinstance(c.get("evidence_lines"), list):
            fail("cause needs statement, claim in %s and evidence_lines" % (CLAIMS,))
        if c["claim"] == "measured" and not c["evidence_lines"]:
            fail("a measured cause carries no evidence line")
        if not isinstance(a.get("not_established"), list):
            fail("not_established is not stated")
        print("OK: %d capture attempt(s) listed; cause stated as %s with %d evidence line(s)" % (len(att), c["claim"], len(c["evidence_lines"])))
    elif cid == "IB129-1-AC2":
        r = a.get("last_ready") or {}
        if r.get("claim") not in CLAIMS or "at_utc" not in r:
            fail("last_ready needs at_utc (a time or null) and claim in %s" % (CLAIMS,))
        if r["at_utc"] is None and r["claim"] == "measured":
            fail("a null last READY cannot be measured; it is absent within the window")
        w = a.get("journal_window") or {}
        if not w.get("since_utc") or not w.get("read_at_utc") or not isinstance(w.get("lines_scanned"), int) or not w.get("host_tz"):
            fail("journal_window needs since_utc, read_at_utc, lines_scanned and host_tz")
        if not isinstance(a.get("ready_by_day"), dict) or not isinstance(a.get("refused_by_day"), dict):
            fail("ready_by_day and refused_by_day are not stated")
        print("OK: last READY %s (%s); window since %s, %d lines; %d day(s) with a READY" % (
            r["at_utc"], r["claim"], w["since_utc"], w["lines_scanned"], sum(1 for v in a["ready_by_day"].values() if v)))
    elif cid == "IB129-1-AC3":
        cmds = a.get("host_commands")
        if not isinstance(cmds, list) or not cmds:
            fail("host_commands is empty")
        for c in cmds:
            if not c.get("ssm_command_id") or c.get("status") != "Success" or not c.get("script"):
                fail("a host command lacks its id, its script or a Success status read from the instance")
            for pat in FORBIDDEN:
                if re.search(pat, c["script"]):
                    fail("host command %s matches the forbidden pattern %r" % (c["ssm_command_id"], pat))
        if a.get("sign_in_attempted") is not False or a.get("secret_values_read") != 0:
            fail("sign_in_attempted must be false and secret_values_read 0")
        outs = a.get("output_files")
        if not isinstance(outs, list) or not outs:
            fail("output_files is empty")
        hits = 0
        for rel in outs + [REC]:
            p = root / rel
            if not p.is_file():
                fail("output file %s is absent" % rel)
            hits += len(SECRETISH.findall(p.read_text(encoding="utf-8", errors="replace")))
        if hits:
            fail("%d cookie or password member(s) in the output files" % hits)
        print("OK: %d host command(s), all Success, none forbidden; no sign-in; 0 secret-like members in %d file(s)" % (len(cmds), len(outs) + 1))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
