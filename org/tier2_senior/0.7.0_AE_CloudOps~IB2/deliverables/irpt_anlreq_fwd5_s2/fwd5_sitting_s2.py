"""IRPT_ANLREQ.TO-RUN-FWD5.live-cross-firm-s2-ib2: steps 2 to 7 as ONE process, so each password exists only in this process's memory and reaches only the helper
or the driver that needs it, on STDIN as one JSON object. No password is printed, logged, written, or placed in argv or the environment.

  python fwd5_sitting.py       (run from the repository root)

Order: mint BOTH (one each, no retry) -> poll the email index -> CONTROL run (exit 0 required) -> FIRM-B run only after a control exit 0 -> the three checks
-> REMOVE BOTH always (a finally) -> the absent check. Prints the helpers' and the driver's own lines and the check lines (route names, statuses, verdicts).
"""
import base64
import json
import secrets
import subprocess
import sys
import time

A = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/"
MINT = A + "0.9.0_WK_IRPT_ANLREQ~219/fwd5_driver/fwd5_mint.py"
DRIVER = A + "0.9.0_WK_IRPT_ANLREQ~231/fwd5_driver/fwd5_driver.py"
CHECKS = "org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R56_CHECKS/r56_checks.py"
OUT = "org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_fwd5_s2/"
GO = "IRPT_ANLREQ.TO-RUN-FWD5.live-cross-firm-s2-ib2"
TICKET, REQ = "TCK-20261015-944c84f8", "REQ-d47252fe74634d0c5cdd8067"
RUN_EMAIL, CTL_EMAIL = "fwd5-cottonwood-r60@opal.invalid", "fwd5-control-r60@opal.invalid"
LOG = []


def say(tag, text):
    line = "%s %s" % (tag, text)
    LOG.append(line)
    print(line, flush=True)


def pw():
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("ascii").rstrip("=")


def run(argv, stdin_obj=None, timeout=900):
    r = subprocess.run([sys.executable] + argv, input=(json.dumps(stdin_obj) if stdin_obj is not None else None), capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout or "").strip().splitlines(), (r.stderr or "").strip().splitlines()


def served_identity(label):
    """The checkout 5174 serves, read WITHOUT touching the server (git reads of its checkout folder)."""
    w = "C:/dev/smoke-template-5174"
    head = subprocess.run(["git", "-C", w, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    origin = subprocess.run(["git", "-C", w, "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
    dirty = len(subprocess.run(["git", "-C", w, "status", "--short"], capture_output=True, text=True).stdout.splitlines())
    say("SERVED %s" % label, "checkout %s HEAD %s origin %s uncommitted_paths %d" % (w, head, origin.rsplit("/", 1)[-1], dirty))
    return head


def index_count(email):
    import boto3
    d = boto3.client("dynamodb", region_name="us-east-1")
    return d.query(TableName="opal-users-v2", IndexName="email-index", KeyConditionExpression="email = :e", ExpressionAttributeValues={":e": {"S": email}}, Select="COUNT")["Count"]


def main():
    pws = {RUN_EMAIL: pw(), CTL_EMAIL: pw()}
    minted = []
    control_rc = firm_b_rc = None
    try:
        for email, firm, ids, tag in ((RUN_EMAIL, "cottonwood", "cottonwood", "run"), (CTL_EMAIL, "opal-capital", "49financial", "control")):
            minted.append(email)  # removal is attempted for every address a mint was tried for
            rc, out, err = run([MINT, "mint", "--email", email, "--firm", firm, "--allowed-firm-ids", ids], {"password": pws[email]})
            for ln in out:
                say("MINT %s" % tag, ln.replace(email, "<%s principal>" % tag))
            ok = rc == 0 and any("MINT-OK READBACK-OK" in x for x in out) and any(("MINT-SCOPE allowedFirmIds=%s entitlement_rows=0" % ids) in x for x in out)
            say("MINT %s" % tag, "rc=%s verdict=%s" % (rc, "OK" if ok else "RED"))
            if not ok:
                say("STOP", "a mint did not read as ordered; no request is made; going to the removal")
                return
        for email, tag in ((RUN_EMAIL, "run"), (CTL_EMAIL, "control")):
            n, t0 = 0, time.time()
            while time.time() - t0 < 120:
                n = index_count(email)
                if n == 1:
                    break
                time.sleep(10)
            say("INDEX %s" % tag, "email-index count %s after %d s" % (n, int(time.time() - t0)))
        head_before = served_identity("before step 4")
        base = ["--base", "http://localhost:5174", "--ticket", TICKET, "--request-id", REQ, "--job-id", REQ, "--out", OUT, "--go", GO]
        rc, out, err = run([DRIVER, "--control", "--email", CTL_EMAIL, "--firm-a", "opal-capital", "--firm-b", "49financial"] + base, {"password": pws[CTL_EMAIL]})
        control_rc = rc
        for ln in out:
            say("CONTROL", ln.replace(CTL_EMAIL, "<control principal>"))
        for ln in err[-3:]:
            say("CONTROL stderr", ln.replace(CTL_EMAIL, "<control principal>")[:200])
        say("CONTROL", "exit=%s" % rc)
        if rc != 0:
            say("STOP", "the control did not exit 0, so the firm-B run is NOT made (a broken control grades nothing)")
            return
        rc, out, err = run([DRIVER, "--email", RUN_EMAIL, "--firm-a", "cottonwood", "--firm-b", "49financial"] + base, {"password": pws[RUN_EMAIL]})
        firm_b_rc = rc
        for ln in out:
            say("FIRM-B", ln.replace(RUN_EMAIL, "<run principal>"))
        for ln in err[-3:]:
            say("FIRM-B stderr", ln.replace(RUN_EMAIL, "<run principal>")[:200])
        say("FIRM-B", "exit=%s (0 all REFUSED; 1 a LEAK; 2 an UNREACHED call)" % rc)
        say("SERVED changed", "%s" % (served_identity("after step 5") != head_before))
        for which in ("control", "report", "fence"):
            rc, out, err = run([CHECKS, which])
            for ln in out[-3:]:
                say("CHECK %s" % which, ln)
    finally:
        pws.clear()
        for email in minted:
            rc, out, err = run([MINT, "remove", "--email", email], timeout=700)
            for ln in out:
                say("REMOVE", ln.replace(email, "<principal>"))
            say("REMOVE", "rc=%s" % rc)
        rc, out, err = run([CHECKS, "absent"])
        for ln in out[-3:]:
            say("CHECK absent", ln)
        say("EXITS", "control=%s firm_b=%s" % (control_rc, firm_b_rc))


if __name__ == "__main__":
    main()
