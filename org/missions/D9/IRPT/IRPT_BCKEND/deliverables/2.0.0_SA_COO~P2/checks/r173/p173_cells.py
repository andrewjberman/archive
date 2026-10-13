"""IRPT_BCKEND round 173 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of two orders.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB173-1  IB-pr-503  OFFLINE REPLAY: the packaged irpt-holdings serve path on a synthetic snapshot whose ACCOUNT node carries account_id
    AC1  the record's arms: a node with account_id, a node without, a node with an unknown member; each verdict from the closed set; the node without reads unchanged
    AC2  every member the replay imported is a staged member of irpt-holdings at its pin and sha256 (or a source_dir file with the working-tree sha256)
    AC3  the replay script, run by this check, reproduces the record's arms, and the bound counters read 0
  IB173-2  IB-pr-504  the frozen export envelope carries facts.covered_account_ids (synthetic ids) and the fe-s-18 generator reproduces it
    AC1  running the fe-s-18 generator leaves the smoke, fe-s-16 and fe-s-32 fixture folders byte-equal to the committed files (end-of-line differences ignored)
    AC2  the six portal tests that consume the fe-s-18 maps pass (28 or more, none failed)
    AC3  the frozen export envelope's data validates against the v1 ExportReceipt schema and its covered_account_ids equal the wire fixture's
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_BCKEND/"
D = PROJ + "deliverables/"
SRCMAP = "infra/aws/lambda/ci/lambda-source-map.json"
PIR = "src/pages/InvestorReporting/"
SMOKE = "portal/" + PIR + "fixtures/smoke/"
REC = D + "0.9.0_WK_IRPT_BCKEND~354/IB173-1_holdings_passthrough_replay.json"
SCRIPT = D + "0.9.0_WK_IRPT_BCKEND~354/replay_503.py"
VERDICTS = {"passed_through", "dropped", "refused", "unchanged"}
BOUND_ZERO = ("functions_invoked", "sign_ins_made", "aws_writes_made", "accounts_written", "figures_written", "vendor_requests_sent")
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB173"))
    sys.exit(1)


def run(cmd, timeout=100, cwd=None):
    try:
        p = subprocess.run(cmd, cwd=str(cwd or ROOT), capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        fail("timeout: %s" % " ".join(map(str, cmd))[:100])
    except FileNotFoundError as e:
        fail("not found: %s" % e)
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def load(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def arms_of(rec):
    return {a.get("arm"): a.get("verdict") for a in (rec.get("arms") or [])}


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if cell == "IB173-1":
        r = load(REC)
        if arm == "AC1":
            a = arms_of(r)
            need = {"node_with_account_id", "node_without_account_id", "node_with_unknown_member"}
            if set(a) != need:
                fail("the arms must be exactly %s, read %s" % (sorted(need), sorted(a)))
            for k, v in a.items():
                if v not in VERDICTS:
                    fail("arm %s: verdict %r is not one of %s" % (k, v, sorted(VERDICTS)))
            if a["node_without_account_id"] != "unchanged":
                fail("a node without account_id must read unchanged, reads %r" % a["node_without_account_id"])
            if not str(r.get("entry_used", "")).strip() or not str(r.get("reading", "")).strip():
                fail("entry_used and reading (one sentence on what the serve path does with an unknown node member) are required")
            print("OK: three arms recorded: %s" % a)
        elif arm == "AC2":
            mem = r.get("packaged_members") or []
            if not mem:
                fail("packaged_members is empty")
            fns = load(SRCMAP).get("functions") or {}
            staged = {(x["repo_path"], x["pin"], x["sha256"]) for x in fns["irpt-holdings"]["staged_from"]}
            files = set(fns["irpt-holdings"].get("files") or [])
            sd = fns["irpt-holdings"]["source_dir"]
            for m in mem:
                rp, pin, sha = m.get("repo_path"), m.get("pin"), m.get("sha256")
                if (rp, pin, sha) in staged:
                    rc = subprocess.run(["git", "-C", str(ROOT), "show", "%s:%s" % (pin, rp)], capture_output=True, timeout=60)
                    if rc.returncode != 0 or hashlib.sha256(rc.stdout).hexdigest() != sha:
                        fail("%s at %s does not hash to the recorded sha256" % (rp, pin))
                elif pin == "WORKTREE" and rp.startswith(sd + "/") and rp[len(sd) + 1:] in files:
                    if hashlib.sha256((ROOT / rp).read_bytes()).hexdigest() != sha:
                        fail("%s (source_dir file) does not hash to the recorded sha256" % rp)
                else:
                    fail("%s @ %s is neither a staged member of irpt-holdings nor a source_dir file (pin WORKTREE)" % (rp, pin))
            print("OK: %d packaged member(s) match the source map" % len(mem))
        elif arm == "AC3":
            for k in BOUND_ZERO:
                if r.get(k) != 0:
                    fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
            if not (ROOT / SCRIPT).is_file():
                fail("no %s" % SCRIPT)
            rc, out = run([sys.executable, "-I", SCRIPT], timeout=100)
            if rc != 0:
                fail("the replay script exited %d: %s" % (rc, re.sub(r"\s+", " ", out)[-160:]))
            try:
                got = json.loads(out[out.index("{"):])
            except ValueError:
                fail("the replay script must print the record's JSON object to stdout")
            if arms_of(got) != arms_of(r):
                fail("the script reproduces %s, the record says %s" % (arms_of(got), arms_of(r)))
            print("OK: the replay script reproduces the recorded arms")
        else:
            fail("unknown criterion")
    elif cell == "IB173-2":
        gen = PIR + "__tests__/fe-s-18/gen-fixtures.ts"
        folders = [PIR + "fixtures/smoke", PIR + "__tests__/fe-s-16", PIR + "__tests__/fe-s-32"]
        if arm == "AC1":
            rc, out = run(["bun", "run", gen], timeout=100, cwd=ROOT / "portal")
            if rc != 0:
                fail("the fe-s-18 generator did not run: %s" % re.sub(r"\s+", " ", out)[-160:])
            pd = subprocess.run(["git", "-C", str(ROOT / "portal"), "diff", "--ignore-cr-at-eol", "--stat", "--"] + folders, capture_output=True, timeout=60)
            diff = pd.stdout.decode("utf-8", "replace")
            if pd.returncode != 0 or diff.strip():
                fail("the fe-s-18 generator drifts from the committed bytes: %s" % re.sub(r"\s+", " ", diff)[:200])
            print("OK: the fe-s-18 generator runs and reproduces the committed fixtures")
        elif arm == "AC2":
            T = PIR + "__tests__/"
            files = [T + "fe-s-18/paired.test.ts", T + "fe-s-18/manifest.test.ts", T + "fe-s-32/holdings-in-a-browser.test.ts",
                     T + "fe-s-19/mounted-from-wire.test.ts", T + "fe-s-31/every-page.test.ts", T + "fe-s-33/fixtures-reach.test.ts"]
            rc, out = run(["bun", "test"] + files, timeout=110, cwd=ROOT / "portal")
            out = re.sub(r"\x1b\[[0-9;]*m", "", out)
            m = re.search(r"(\d+) pass", out)
            f = re.search(r"(\d+) fail", out)
            if rc != 0 or not m or int(m.group(1)) < 28 or (f and int(f.group(1)) != 0):
                fail("the six portal tests: rc %s, %s pass, %s fail" % (rc, m.group(1) if m else "?", f.group(1) if f else "?"))
            print("OK: the six consuming portal tests pass")
        elif arm == "AC3":
            try:
                import jsonschema
            except ImportError:
                fail("jsonschema is not importable")
            sch = load("docs/contracts/investor-reporting/v1/ExportReceipt.schema.json")
            frozen = load(SMOKE + "fe-s-18-frozen.json")
            wire = load(SMOKE + "fe-s-13-wire.json")
            fk = [k for k in frozen if k.startswith("/api/scoped/investor-reporting/export/")]
            wk = [k for k in wire if k.startswith("/api/scoped/investor-reporting/export/")]
            if len(fk) != 1 or len(wk) != 1:
                fail("expected one export key in the frozen map and one in the wire, read %d and %d" % (len(fk), len(wk)))
            data = frozen[fk[0]].get("data") or {}
            errs = [e.message[:100] for e in jsonschema.Draft202012Validator(sch).iter_errors(data)]
            if errs:
                fail("the frozen export envelope's data does not validate against the v1 ExportReceipt schema: %s" % errs[:3])
            ids = (data.get("facts") or {}).get("covered_account_ids")
            want = ((wire[wk[0]].get("data") or {}).get("facts") or {}).get("covered_account_ids")
            if not ids or ids != want:
                fail("covered_account_ids must equal the wire fixture's synthetic list %r, reads %r" % (want, ids))
            print("OK: the frozen export envelope validates and carries the wire's synthetic covered_account_ids")
        else:
            fail("unknown criterion")
    else:
        fail("unknown criterion %r" % CID)
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
