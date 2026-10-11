"""IRPT_BCKEND round 132 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one BUILD-ONLY order:
  IB132-1  IB-pr-434  the YCharts session capture says what its sign-in did: the receipt's login_submission and probe_pair are
                      persisted as closed, secret-free members; the signed-out-app-chrome diagnosis fires after a submission
                      too, under its own code; the capture's stderr is kept per run (CTO msg 5025; rows D2-IB2-S1).
                      No request is sent, nothing is deployed.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB132-1-AC1  the runner's new offline test passes and the existing offline suite still passes (both under the netguard
               preload). Base: FAIL (the new test is absent); the existing suite alone reads rc 0 at base.
  IB132-1-AC2  the persisted receipt of a planted run (a synthetic sample the build's own test writes) carries login_submission
               and probe_pair, every leaf of them is a boolean, an integer, null or a short name, and none of the planted secret
               strings appears anywhere in the sample; the session test folder passes with no failure and at least 118 passed.
               Base: FAIL (no sample).
  IB132-1-AC3  the record carries the rule-24 record and token census of the new reason code, the per-run stderr retention with
               its bound, the files changed, and how the change reaches the host. Base: FAIL (no record).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~292/"
REC = D + "IB132-1_capture_receipt_record.json"
SAMPLE = D + "IB132-1_persisted_receipt_sample.json"
E = "infra/aws/ec2/investor-reporting-ycharts"
PKG = "infra/aws/lambda/investor-reporting"
NEW_JS = "tests/receipt_after_submit.js"
NAME = re.compile(r"^[A-Za-z0-9_.#\[\]=\"' :()>*~^$|-]{0,120}$")
BASE_SESSION_PASSED = 118


def leaves(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, path + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, path + "/%d" % i)
    else:
        yield path, o


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB132"))
        sys.exit(1)

    if cid == "IB132-1-AC1":
        if not (root / E / NEW_JS).is_file():
            fail("no %s/%s" % (E, NEW_JS))
        for script in (NEW_JS, "tests/run_offline_suite.js"):
            p = subprocess.run(["node", "--require", "./tests/netguard.js", script], cwd=str(root / E), capture_output=True, timeout=100)
            if p.returncode != 0:
                fail("%s exits %d: %s" % (script, p.returncode, p.stdout.decode("utf-8", "replace")[-200:].replace("\n", " ")))
        print("OK: %s and the existing offline suite both exit 0 under the netguard preload" % NEW_JS)
    elif cid == "IB132-1-AC2":
        s, r = root / SAMPLE, root / REC
        if not s.is_file() or not r.is_file():
            fail("no persisted receipt sample or no record")
        text = s.read_text(encoding="utf-8")
        doc = json.loads(text)
        found = {}
        for path, _ in leaves(doc):
            for key in ("login_submission", "probe_pair"):
                if "/" + key + "/" in path + "/":
                    found[key] = found.get(key, 0) + 1
        if sorted(found) != ["login_submission", "probe_pair"]:
            fail("the sample carries %r, both login_submission and probe_pair are required" % sorted(found))
        bad = []
        for path, v in leaves(doc):
            if "/login_submission" not in path and "/probe_pair" not in path:
                continue
            if isinstance(v, bool) or v is None or isinstance(v, int):
                continue
            if not isinstance(v, str) or not NAME.match(v) or "http" in v.lower() or "@" in v or "%" in v:
                bad.append(path)
        if bad:
            fail("%d leaf value(s) of the two members are not a boolean, an integer, null or a short name: %s" % (len(bad), bad[:4]))
        planted = json.loads(r.read_text(encoding="utf-8")).get("planted_secrets")
        if not isinstance(planted, list) or len(planted) < 4 or any(not isinstance(x, str) or len(x) < 8 for x in planted):
            fail("the record must list the planted secret strings of the sample run (username, password, a cookie value, a tokenized URL)")
        leaked = [x[:4] + "..." for x in planted if x in text]
        if leaked:
            fail("%d planted secret string(s) appear in the persisted sample: %s" % (len(leaked), leaked))
        p = subprocess.run([sys.executable, "-m", "pytest", "ycharts/session/tests", "-q", "-p", "no:cacheprovider", "--color=no"],
                           cwd=str(root / PKG), capture_output=True, timeout=110)
        out = p.stdout.decode("utf-8", "replace")
        m, f = re.search(r"(\d+) passed", out), re.search(r"(\d+) failed", out)
        if f or not m or int(m.group(1)) < BASE_SESSION_PASSED:
            fail("session tests: %s" % out.strip().splitlines()[-1][:160])
        print("OK: both members persisted, %d leaf value(s) closed, 0 of %d planted secrets in the sample; session tests %s passed, 0 failed" % (
            sum(found.values()), len(planted), m.group(1)))
    elif cid == "IB132-1-AC3":
        r = root / REC
        if not r.is_file():
            fail("no %s" % REC)
        a = json.loads(r.read_text(encoding="utf-8"))
        code = a.get("new_reason_code") or {}
        post = code.get("four_postulates") or {}
        if not code.get("name") or sorted(post) != ["i_mece", "ii_same_grain", "iii_one_intent", "iv_state_coherence"] \
                or not isinstance(code.get("token_census"), dict) or "scope" not in code["token_census"]:
            fail("new_reason_code needs name, the four postulates and a token_census with its scope")
        st = a.get("stderr_per_run") or {}
        if not st.get("file_name_rule") or not isinstance(st.get("runs_kept"), int) or not isinstance(st.get("max_bytes_per_run"), int):
            fail("stderr_per_run needs file_name_rule, runs_kept and max_bytes_per_run")
        if not isinstance(a.get("files_changed"), list) or not a["files_changed"] or not a.get("host_reach"):
            fail("files_changed and host_reach are not stated")
        if a.get("request_sent") is not False or a.get("deployed") is not False:
            fail("request_sent and deployed must both read false")
        print("OK: reason code %s with its record and census; stderr kept for %d run(s), %d bytes each; %d files changed" % (
            code["name"], st["runs_kept"], st["max_bytes_per_run"], len(a["files_changed"])))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
