"""IB-rti-1 battery -- the capture tool repaired (S125 command, S126 readiness, S127 origin).

Arms: command | readiness | origin | diagnostic | packet | publish.  Run from any cwd inside the worktree.
Everything is exercised under stubs (harness_ib_rti_1.cjs runs the REAL capture-session.cjs source in a VM
with Playwright/fs/readline stubbed): no browser, network, credential, host action or real file write.
ASCII only.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
SRC_DIR = "infra/aws/ec2/investor-reporting-export"
CAP = SRC_DIR + "/capture-session.cjs"
CAPSH = SRC_DIR + "/capture-session.sh"
README = SRC_DIR + "/README.md"
RENDER = SRC_DIR + "/render_export.cjs"
DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R8_CAPTURE_DIAGNOSTIC.cjs"
HARNESS = os.path.join(HERE, "harness_ib_rti_1.cjs")
BASELINE = os.path.join(HERE, "IB-rti-1_baseline_diagnostic_output.txt")
PACKET_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~9/IB-rti-1_NEVER_WIDEN_PACKET.md"
PUBLISH_FILES = [CAP, CAPSH]
BASE_COMMIT = "eecaad4985"
S3_PREFIX = "s3://opal-313476888478-lambda-artifacts/ec2/investor-reporting-export/"
LEDGER_SENTINEL = "org/critical_paths/.open_deploys/irpt-rti-1-capture-tool-publish.json"

ORIGIN = "https://opalinvest.dev"
IID = "i-0167fd745ad906a66"
CHECK = ORIGIN + "/investor-reporting/print"


def git(args):
    p = subprocess.run(["git", "-C", REPO] + args, capture_output=True)
    return p.returncode, p.stdout, p.stderr.decode("utf-8", "replace")


def run_harness(cfg, source=CAP):
    p = subprocess.run(["node", HARNESS, os.path.join(REPO, source), json.dumps(cfg)],
                       capture_output=True, text=True, timeout=60, cwd=REPO)
    if p.returncode != 0 or not p.stdout.strip():
        raise RuntimeError("harness rc=%s stderr=%s" % (p.returncode, p.stderr[:400]))
    return json.loads(p.stdout.strip().splitlines()[-1])


def base_cfg(**kw):
    c = dict(origin=ORIGIN, instanceId=IID, status=200, passwordCount=0, markerCount=1,
             finalUrl=CHECK, hops=[CHECK], storageState={"cookies": [], "origins": []})
    c.update(kw)
    return c


def success(r):
    return "OK: session state captured" in r["output"]


def check(label, ok, detail=""):
    print("  [%s] %s %s" % ("ok" if ok else "FAIL", label, detail))
    return ok


def cmd_line(output):
    m = re.search(r"^ {2}aws ssm start-session .*$", output, re.M)
    return m.group(0).strip() if m else None


def normalize(c):
    c = re.sub(r"i-[0-9a-f]{8,17}", "ID", c)
    return re.sub(r'"(\d{2,5})"', '"PORT"', c)


def arm_command():
    print("=== ARM command (S125): the emitted command is executable verbatim ===")
    ok = True
    r = run_harness(base_cfg())
    line = cmd_line(r["output"])
    print("  emitted:", line)
    ok &= check("a command line was emitted", line is not None)
    if line:
        ok &= check("zero '<' or '>' in the emitted command", "<" not in line and ">" not in line)
        ok &= check("names the real instance id", ("--target " + IID + " ") in line)
        ok &= check("names the port (9333) as portNumber and localPortNumber",
                    '"portNumber":["9333"]' in line and '"localPortNumber":["9333"]' in line)
    ok &= check("zero '<' or '>' anywhere in the tool's stdout", "<" not in r["output"] and ">" not in r["output"])
    r2 = run_harness(base_cfg(portEnv="9444"))
    l2 = cmd_line(r2["output"]) or ""
    ok &= check("a non-default port is carried into the command", '"portNumber":["9444"]' in l2)
    bad = [("absent", None), ("empty", ""), ("placeholder", "<instance-id>"), ("not-i-prefixed", "abc12345"),
           ("too-short", "i-12345"), ("non-hex", "i-0167fd745ad906a6z"), ("too-long", "i-0167fd745ad906a660")]
    for name, val in bad:
        cfg = base_cfg()
        if val is None:
            del cfg["instanceId"]
        else:
            cfg["instanceId"] = val
        rb = run_harness(cfg)
        ok &= check("id %s refused (exit 1, no command, browser never launched, 0 writes)" % name,
                    rb["exitCode"] == 1 and cmd_line(rb["output"]) is None and "<instance-id>" not in rb["output"]
                    and rb["launched"] == 0 and len(rb["fileWrites"]) == 0 and "INSTANCE_ID" in rb["errors"])
    print("  denominator: %d invalid/absent-id cases + 1 valid + 1 port case" % len(bad))
    readme = open(os.path.join(REPO, README), encoding="utf-8").read()
    rl = [x.strip("# ").strip() for x in readme.splitlines()
          if "aws ssm start-session --target" in x and "AWS-StartPortForwardingSession" in x and "--parameters" in x]
    print("  README command lines:", len(rl))
    ok &= check("README step 3 shows the SAME form as the emitted command",
                len(rl) == 1 and line is not None and normalize(rl[0]) == normalize(line))
    if rl:
        print("  README:", rl[0])
    if ok:
        print("IBR91-EMITTED-COMMAND-EXECUTABLE-VERBATIM")
        return 0
    print("FAIL: command arm")
    return 1


def arm_readiness():
    print("=== ARM readiness (S126): positive readiness; 500 / redirect / 4xx / marker-absent refuse ===")
    ok = True
    r = run_harness(base_cfg())
    ok &= check("POSITIVE (2xx, same origin, no password, marker present): exactly 1 write + success",
                len(r["fileWrites"]) == 1 and success(r) and r["exitCode"] is None)
    refusals = [
        ("HTTP 500, no password input (marker present, only status differs)", base_cfg(status=500)),
        ("redirect to a sign-in path (marker present, 200, only path differs)",
         base_cfg(finalUrl=ORIGIN + "/login", hops=[CHECK, ORIGIN + "/login"])),
        ("HTTP 404 page", base_cfg(status=404)),
        ("HTTP 403 page", base_cfg(status=403)),
        ("marker absent (200, same origin, no password -- only the marker differs)", base_cfg(markerCount=0)),
        ("password input present (marker present)", base_cfg(passwordCount=1)),
    ]
    for name, cfg in refusals:
        rr = run_harness(cfg)
        ok &= check("REFUSED: %s" % name,
                    len(rr["fileWrites"]) == 0 and rr["storageStateCalls"] == 0 and not success(rr) and rr["exitCode"] == 1,
                    "(writes=%d exit=%s)" % (len(rr["fileWrites"]), rr["exitCode"]))
    print("  denominator: 1 positive + %d refusals" % len(refusals))
    if ok:
        print("IBR91-READINESS-IS-POSITIVE-AND-REFUSES-500-REDIRECT-ERROR")
        return 0
    print("FAIL: readiness arm")
    return 1


def list_from(text, name):
    m = re.search(r"const %s = \[(.*?)\];" % name, text, re.S)
    return re.findall(r"'([^']+)'", m.group(1)) if m else None


def arm_origin():
    print("=== ARM origin (S127): the origin is enforced, state is origin-scoped, allowlist equals the renderer's ===")
    ok = True
    for name, o in [("example.invalid", "https://example.invalid"), ("vendor ycharts.com", "https://ycharts.com"),
                    ("vendor subdomain", "https://x.api.ycharts.com"), ("plain http", "http://opalinvest.dev")]:
        rr = run_harness(base_cfg(origin=o, finalUrl=o + "/investor-reporting/print", hops=[o + "/investor-reporting/print"]))
        ok &= check("origin %s refused: 0 navigations, 0 writes, browser never launched, exit 1" % name,
                    len(rr["navigations"]) == 0 and len(rr["fileWrites"]) == 0 and rr["launched"] == 0 and rr["exitCode"] == 1,
                    "(navigations=%d)" % len(rr["navigations"]))
    rr = run_harness(base_cfg(checkRoute="https://example.invalid/x"))
    ok &= check("a check route that resolves off-origin is refused before any navigation",
                len(rr["navigations"]) == 0 and len(rr["fileWrites"]) == 0 and rr["exitCode"] == 1)
    rr = run_harness(base_cfg(finalUrl="https://example.invalid/land", hops=[CHECK, "https://example.invalid/land"]))
    ok &= check("cross-origin redirect hop (final URL foreign) refused", len(rr["fileWrites"]) == 0 and rr["exitCode"] == 1 and not success(rr))
    rr = run_harness(base_cfg(hops=["https://example.invalid/hop", CHECK]))
    ok &= check("cross-origin INTERMEDIATE hop (final URL back on origin -- only the hop differs) refused",
                len(rr["fileWrites"]) == 0 and rr["exitCode"] == 1 and not success(rr))
    rr = run_harness(base_cfg(firstUrl="https://example.invalid/first"))
    ok &= check("first navigation landing off-origin refused before the command is printed",
                len(rr["fileWrites"]) == 0 and rr["exitCode"] == 1 and cmd_line(rr["output"]) is None)
    state = {"cookies": [
        {"name": "a", "domain": "opalinvest.dev"}, {"name": "b", "domain": ".opalinvest.dev"},
        {"name": "c", "domain": "evil.example"}, {"name": "d", "domain": ".example.invalid"}],
        "origins": [{"origin": ORIGIN, "localStorage": []}, {"origin": "https://evil.example", "localStorage": []}]}
    rr = run_harness(base_cfg(storageState=state))
    written = json.loads(rr["fileWrites"][0]["data"]) if len(rr["fileWrites"]) == 1 else None
    ok &= check("saved state holds ONLY the configured origin's entries (in: 4 cookies/2 origins)",
                written is not None and [c["name"] for c in written["cookies"]] == ["a", "b"]
                and [o["origin"] for o in written["origins"]] == [ORIGIN],
                "(out: %s cookies / %s origins)" % (len(written["cookies"]) if written else "?", len(written["origins"]) if written else "?"))
    cap = open(os.path.join(REPO, CAP), encoding="utf-8").read()
    ren = open(os.path.join(REPO, RENDER), encoding="utf-8").read()
    a, b = list_from(cap, "VENDOR_HOSTS"), list_from(ren, "VENDOR_HOSTS")
    print("  helper   VENDOR_HOSTS (%s entries): %s" % (len(a or []), a))
    print("  renderer VENDOR_HOSTS (%s entries): %s" % (len(b or []), b))
    ok &= check("helper's vendor list EQUALS render_export.cjs's (drift detector)", a is not None and a == b and len(a) > 0)
    print("  helper ALLOWED_ORIGINS:", list_from(cap, "ALLOWED_ORIGINS"),
          "(render_export.cjs holds NO fixed origin allowlist -- row IRPT_BCKEND-W9-S1)")
    if ok:
        print("IBR91-ORIGIN-ENFORCED-FOREIGN-REFUSED-STATE-ORIGIN-SCOPED")
        return 0
    print("FAIL: origin arm")
    return 1


def run_diag(diag_path):
    p = subprocess.run(["node", diag_path], capture_output=True, text=True, timeout=120, cwd=REPO)
    if p.returncode != 0:
        raise RuntimeError("diagnostic rc=%s %s" % (p.returncode, p.stderr[:300]))
    return json.loads(p.stdout)


def brief(res):
    return [(x["label"], "status=%s pw=%s writes=%s navs=%d success=%s placeholder=%s"
             % (x["responseStatus"], x["passwordCount"], x["writes"], len(x["navigations"]),
                x["captureSuccessPrinted"], x["literalInstancePlaceholder"]), x["errors"]) for x in res["results"]]


def arm_diagnostic():
    print("=== ARM diagnostic (R91-AC4): the CVO~B diagnostic, UNMODIFIED, against the REPAIRED source ===")
    ok = True
    print("--- BASELINE recorded at arm (a) (unchanged source), from %s ---" % os.path.basename(BASELINE))
    if os.path.isfile(BASELINE):
        base = json.loads(open(BASELINE, encoding="utf-8").read())
        for row in brief(base):
            print("  BASE ", row[0], "|", row[1])
    else:
        ok &= check("baseline file present", False)
    res = run_diag(os.path.join(REPO, DIAG))
    print("--- REPAIRED source, unmodified diagnostic (sha256 of source %s) ---" % res["sourceSha256"][:16])
    for row in brief(res):
        print("  POST ", row[0], "|", row[1], "| errors:", row[2][:90])
    r_pw, r_500, r_orig = res["results"]
    ok &= check("password-present control still writes nothing", r_pw["writes"] == 0 and not r_pw["captureSuccessPrinted"])
    ok &= check("HTTP 500 counterexample REFUSES (0 writes, no success)", r_500["writes"] == 0 and not r_500["captureSuccessPrinted"])
    ok &= check("arbitrary-origin counterexample REFUSES (0 writes, no success, 0 navigations)",
                r_orig["writes"] == 0 and not r_orig["captureSuccessPrinted"] and len(r_orig["navigations"]) == 0)
    ok &= check("no case prints the literal instance placeholder", not any(x["literalInstancePlaceholder"] for x in res["results"]))
    # The unmodified diagnostic supplies NO instance id, so cases 1-2 refuse for the S125 reason rather than the
    # reason they are named for (row IRPT_BCKEND-W9-S2). This copy differs from the diagnostic ONLY by the env
    # line, so those cases reach the readiness code; the CVO's file itself is never edited.
    src = open(os.path.join(REPO, DIAG), encoding="utf-8").read()
    needle = "env: { IRPT_CAPTURE_PORTAL_ORIGIN: origin }"
    ok &= check("diagnostic env line present for the instance-id-supplied copy", src.count(needle) == 1)
    mod = src.replace(needle, "env: { IRPT_CAPTURE_PORTAL_ORIGIN: origin, IRPT_CAPTURE_INSTANCE_ID: '%s' }" % IID)
    with tempfile.NamedTemporaryFile("w", suffix=".cjs", delete=False, dir=REPO) as tf:
        tf.write(mod)
        tmp = tf.name
    try:
        res2 = run_diag(tmp)
    finally:
        os.unlink(tmp)
    print("--- REPAIRED source, diagnostic copy that ONLY adds IRPT_CAPTURE_INSTANCE_ID (reaches the readiness code) ---")
    for row in brief(res2):
        print("  POST+ID", row[0], "|", row[1], "| errors:", row[2][:90])
    p1, p2, p3 = res2["results"]
    ok &= check("with an id supplied: 500 counterexample still REFUSES", p2["writes"] == 0 and not p2["captureSuccessPrinted"] and len(p2["navigations"]) >= 2)
    ok &= check("with an id supplied: password case still writes nothing", p1["writes"] == 0 and not p1["captureSuccessPrinted"])
    ok &= check("with an id supplied: foreign origin still 0 navigations, 0 writes", p3["writes"] == 0 and len(p3["navigations"]) == 0)
    r = run_harness(base_cfg())
    ok &= check("arm (e) authenticated POSITIVE (2xx, same origin, no password, marker present): exactly 1 write + success",
                len(r["fileWrites"]) == 1 and success(r))
    if ok:
        print("IBR91-CVOB-DIAGNOSTIC-COUNTEREXAMPLES-REFUSE-POSITIVE-CONTROL-PASSES")
        return 0
    print("FAIL: diagnostic arm")
    return 1


def blob(path):
    rc, out, _ = git(["rev-parse", "HEAD:" + path])
    return out.decode().strip() if rc == 0 else None


def blob_sha256(path):
    rc, out, _ = git(["show", "HEAD:" + path])
    return hashlib.sha256(out).hexdigest() if rc == 0 else None


def halves():
    rc, out, _ = git(["ls-tree", "-r", "--name-only", "HEAD", "--", "org/tier1_exec/"])
    paths = out.decode().splitlines()
    pb = blob(PACKET_REL)
    found = {}
    for who, tag in (("1.0.0_SA_CTO", "CTO_HALF"), ("2.0.0_SA_COO", "COO_HALF")):
        found[who] = None
        for p in paths:
            if who in p and "IB-rti-1" in p and tag in p and pb:
                _, txt, _ = git(["show", "HEAD:" + p])
                t = txt.decode("utf-8", "replace")
                if pb in t and re.search(r"\bsign(?:ed|s)\b", t, re.I) and not re.search(r"VERDICT.{0,40}REFUSED", t, re.S | re.I):
                    found[who] = p
                    break
    return pb, found


def arm_packet():
    print("=== ARM packet (R91-AC5): the never-widen packet, git-blob hashes ===")
    ok = True
    pb = blob(PACKET_REL)
    ok &= check("packet committed at HEAD (%s)" % PACKET_REL, pb is not None, "blob %s" % pb)
    if pb is None:
        print("FAIL: packet arm")
        return 1
    rc, out, _ = git(["show", "HEAD:" + PACKET_REL])
    text = out.decode("utf-8", "replace")
    rc, out, _ = git(["diff", "--name-only", BASE_COMMIT, "HEAD", "--", SRC_DIR + "/"])
    changed = sorted(out.decode().split())
    host_run = [f for f in changed if not f.endswith("README.md")]
    print("  changed under %s since %s: %s" % (SRC_DIR, BASE_COMMIT, changed))
    ok &= check("packet's publish set == the changed host-run files (README excluded)", sorted(PUBLISH_FILES) == sorted(host_run),
                "(%s)" % host_run)
    rows = re.findall(r"^\|\s*`(%s/[^`]+)`\s*\|\s*`([0-9a-f]{40})`\s*\|\s*`([0-9a-f]{64})`\s*\|" % re.escape(SRC_DIR), text, re.M)
    print("  packet rows: %d (denominator = %d files to publish)" % (len(rows), len(PUBLISH_FILES)))
    ok &= check("packet names exactly the publish set", sorted(r[0] for r in rows) == sorted(PUBLISH_FILES))
    for path, b1, s256 in rows:
        ok &= check("%s blob equals git rev-parse HEAD:<path>" % path, blob(path) == b1, "(%s)" % b1)
        ok &= check("%s sha256-of-blob-bytes re-derived" % path, blob_sha256(path) == s256, "(%s...)" % s256[:16])
    pbh, found = halves()
    print("  packet blob at HEAD: %s" % pbh)
    print("  CTO half at HEAD naming the packet blob, signed: %s" % found["1.0.0_SA_CTO"])
    print("  COO half at HEAD naming the packet blob, signed: %s" % found["2.0.0_SA_COO"])
    print("  BOTH HALVES OBTAINED: %s (stated, not required for this token)" % all(found.values()))
    if ok:
        print("IBR91-PACKET-WRITTEN-WITH-GIT-BLOB-HASHES")
        return 0
    print("FAIL: packet arm")
    return 1


def arm_publish():
    print("=== ARM publish (R91-AC6): gated on BOTH halves at HEAD naming the packet blob ===")
    pb, found = halves()
    print("  packet blob at HEAD: %s" % pb)
    print("  CTO half: %s" % found["1.0.0_SA_CTO"])
    print("  COO half: %s" % found["2.0.0_SA_COO"])
    if not all(found.values()):
        print("GATE NOT MET: both halves (2.0.0_SA_COO~B and 1.0.0_SA_CTO) are not at HEAD naming the packet blob.")
        print("This arm does NOT run: no ledger entry opened, no S3 write. No token. Status: UNCOMPUTABLE-BY-CONSTRUCTION.")
        return 0
    if blob(LEDGER_SENTINEL) is None:
        print("GATE MET but the deploy-ledger sentinel %s is not committed at HEAD: open it BEFORE the act. No S3 write." % LEDGER_SENTINEL)
        return 1
    rows = re.findall(r"^\|\s*`(%s/[^`]+)`\s*\|\s*`([0-9a-f]{40})`\s*\|\s*`([0-9a-f]{64})`\s*\|" %
                      re.escape(SRC_DIR), git(["show", "HEAD:" + PACKET_REL])[1].decode("utf-8", "replace"), re.M)
    ok = True
    for path, b1, s256 in rows:
        _, data, _ = git(["show", "HEAD:" + path])
        if hashlib.sha256(data).hexdigest() != s256 or blob(path) != b1:
            print("FAIL: %s bytes at HEAD differ from the packet" % path)
            return 1
        with tempfile.TemporaryDirectory() as td:
            up = os.path.join(td, "up")
            dn = os.path.join(td, "dn")
            open(up, "wb").write(data)
            key = S3_PREFIX + os.path.basename(path)
            r1 = subprocess.run([os.path.join(REPO, ".tools/aws"), "s3", "cp", up, key], capture_output=True, text=True)
            r2 = subprocess.run([os.path.join(REPO, ".tools/aws"), "s3", "cp", key, dn], capture_output=True, text=True)
            got = hashlib.sha256(open(dn, "rb").read()).hexdigest() if r2.returncode == 0 and os.path.isfile(dn) else None
            ok &= check("S3 %s readback sha256 == packet" % key, r1.returncode == 0 and got == s256, "(%s)" % got)
    print("  NOTE: the host is STOPPED and was not started; there is NO on-host byte readback here.")
    if ok:
        print("IBR91-PUBLISHED-S3-BYTES-EQUAL-PACKET-BLOBS")
        return 0
    return 1


ARMS = {"command": arm_command, "readiness": arm_readiness, "origin": arm_origin,
        "diagnostic": arm_diagnostic, "packet": arm_packet, "publish": arm_publish}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "--arm" or sys.argv[2] not in ARMS:
        print("usage: battery_ib_rti_1.py --arm {%s}" % "|".join(ARMS))
        sys.exit(2)
    sys.exit(ARMS[sys.argv[2]]())
