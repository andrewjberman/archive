"""CA-k-2: the mode-default gate. A safe-apply of module.ldo_001 REFUSES when the trunk's chat_assist_ingress_mark_mode default
differs from the live INGRESS_MARK_MODE (CTO ruling, ROUND_ANALYSIS.round18 section 3 ruling 3). A gate, not an alert.

Run from the root of the checkout under test, by RELATIVE path (the repo is found from the working directory, never from this file):
    python "org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/r19/checks/check_l2_gate.py"
Prints one line per failed arm and  L2-GATE ok=<True|False> arms=<k> of <n>.

No AWS call is made: the live configuration is a JSON file (--live-json for the script, LDO001_MODE_LIVE_JSON for safe-apply), and
terraform is a stub that records every call. The contract this pins (the worker's interface):
  .tools/ldo001-mode-default-check.py [--tf PATH] [--live-json PATH]
      last stdout line:  LDO001-MODE verdict=<OK|REFUSED|NO-VERDICT> default=<v> live=<v>      rc 0 only for OK
      the default is read from the variable "chat_assist_ingress_mark_mode" in --tf; the live value is INGRESS_MARK_MODE of the
      handler and the ingress function (lambda get-function-configuration through the .tools/aws shim, or the JSON seam: a dict, or
      a list of dicts, each shaped like that call's output); equal everywhere -> OK; a difference, between default and live or
      between the two functions -> REFUSED; anything unreadable (file, JSON, key, variable, default) -> NO-VERDICT.
  .tools/safe-apply.sh: when the apply covers module.ldo_001 (a -target of module.ldo_001 or below, written -target=X or -target X; or
      no -target and the -chdir tree declares module "ldo_001"), run that script with --tf <tree>/chat_assist.tf BEFORE the seat
      gates and print "safe-apply: [ldo001-mode] <its last line>" to stderr. rc != 0 -> exit 10 with "BLOCKED" on stderr and
      terraform never called, unless LDO001_MODE_OVERRIDE="reason" is set: then one line naming LDO001_MODE_OVERRIDE, the actor, the
      reason goes to the override audit file ($GAO_REL) and the apply goes on. SAFE_LDO001_MODE_CHECK_ONLY=1 makes a covered apply
      exit 0 right after the check (the test seam, as SAFE_NAMED_COMMIT_CHECK_ONLY is). An apply that does not cover the module runs
      nothing of this and prints no [ldo001-mode] line.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def toplevel():
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise SystemExit("L2-GATE ok=False arms=0 of 0 (not inside a git checkout)")
    return Path(r.stdout.strip()).resolve()


ROOT = toplevel()
sys.path.insert(0, str(ROOT / ".tools"))
os.chdir(str(ROOT))
SCRIPT = ROOT / ".tools" / "ldo001-mode-default-check.py"
APPLY = ROOT / ".tools" / "safe-apply.sh"
DEVICE = "l2chk"
AUDIT = ROOT / "org" / ("git-author-override-audit.%s.log" % DEVICE)
MARK = "[ldo001-mode]"

TF = '''variable "chat_assist_ingress_mark_mode" {
  description = "fixture"
  type        = string
  default     = "%s"
}

module "ldo_001" {
  source = "../modules/ldo"
}
'''
TF_NO_VAR = 'module "ldo_001" {\n  source = "../modules/ldo"\n}\n'
TF_NO_DEFAULT = 'variable "chat_assist_ingress_mark_mode" {\n  type = string\n}\n\nmodule "ldo_001" {\n  source = "x"\n}\n'
TF_OTHER = 'resource "aws_s3_bucket" "b" {\n  bucket = "fixture"\n}\n'
STUB = '#!/bin/bash\necho "$@" >> "$STUB_LOG"\nexit 1\n'


def cfg(mode):
    return {"FunctionName": "f", "Environment": {"Variables": {"INGRESS_MARK_MODE": mode, "GATEWAY_BASE": "x"}}}


def put(path, text):
    path.write_text(text, encoding="ascii", newline="\n")
    return path


def run_script(tf, live):
    args = [sys.executable, str(SCRIPT), "--tf", str(tf), "--live-json", str(live)]
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", timeout=90)
    lines = [x for x in (r.stdout or "").splitlines() if x.strip()]
    return r.returncode, (lines[-1] if lines else ""), (r.stderr or "")


def bash():
    from git_bash_resolver import git_bash
    b = git_bash()
    if not b:
        raise SystemExit("L2-GATE ok=False arms=0 of 0 (no Git Bash)")
    return b


def run_apply(tree, targets, live, env_extra, tmp, stub, empty):
    """One safe-apply.sh run against a fixture tree with the stub terraform. Returns (rc, stderr, stub calls)."""
    log = tmp / "stub.log"
    if log.exists():
        log.unlink()
    env = dict(os.environ)
    env.update({"SAFE_APPLY_TERRAFORM": stub.as_posix(), "STUB_LOG": log.as_posix(), "OPAL_SEAT_GATES_ENFORCE_DIR": empty.as_posix(),
                "AGENTBUS_DEVICE": DEVICE, "OPAL_AGENT_SERIAL": "2.0.0_SA_COO~CA.l2chk"})
    for k in ("LDO001_MODE_LIVE_JSON", "LDO001_MODE_OVERRIDE", "SAFE_LDO001_MODE_CHECK_ONLY", "DEPLOY_COMMIT", "TAGAUTHZ_OVERRIDE"):
        env.pop(k, None)
    if live is not None:
        env["LDO001_MODE_LIVE_JSON"] = live.as_posix()
    env.update(env_extra)
    # --dry-seat-gates ends every run that was not stopped earlier right after the seat gates: no halt gate, plan or terraform follows,
    # so the run is bounded and deterministic at the base (no hook) as well as with the hook
    args = [bash(), str(APPLY), "-chdir=" + tree.as_posix(), "apply"] + targets + ["--dry-seat-gates"]
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", timeout=120, env=env, cwd=str(ROOT))
    calls = log.read_text(encoding="utf-8", errors="replace").splitlines() if log.exists() else []
    return r.returncode, (r.stderr or "") + (r.stdout or ""), calls


def main():
    fails = []
    n = 0

    def arm(name, ok, why=""):
        nonlocal n
        n += 1
        if not ok:
            fails.append("ARM %s FAILED %s" % (name, why))

    audit_before = AUDIT.exists()
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        tf_enf = put(tmp / "enforce.tf", TF % "enforce")
        put(tmp / "record.tf", TF % "record")
        live_enf = put(tmp / "live_enforce.json", json.dumps(cfg("enforce")))
        live_rec = put(tmp / "live_record.json", json.dumps(cfg("record")))
        live_two = put(tmp / "live_two.json", json.dumps([cfg("enforce"), cfg("record")]))
        if not SCRIPT.exists():
            for name in ("mismatch-refuses", "equal-ok", "live-unreadable-no-verdict", "tf-unparsable-no-verdict", "functions-disagree-refuses"):
                arm(name, False, "(.tools/ldo001-mode-default-check.py does not exist)")
        else:
            rc, line, _ = run_script(tf_enf, live_rec)
            arm("mismatch-refuses", rc != 0 and line == "LDO001-MODE verdict=REFUSED default=enforce live=record", "rc=%s line=%r" % (rc, line))
            rc, line, _ = run_script(tf_enf, live_enf)
            arm("equal-ok", rc == 0 and line == "LDO001-MODE verdict=OK default=enforce live=enforce", "rc=%s line=%r" % (rc, line))
            bad = []
            put(tmp / "garbled.json", "{not json")
            put(tmp / "nokey.json", json.dumps({"Environment": {"Variables": {"GATEWAY_BASE": "x"}}}))
            for what, path in (("missing-file", tmp / "absent.json"), ("bad-json", tmp / "garbled.json"), ("no-key", tmp / "nokey.json")):
                rc, line, _ = run_script(tf_enf, path)
                if not (rc != 0 and line.startswith("LDO001-MODE verdict=NO-VERDICT")):
                    bad.append("%s rc=%s line=%r" % (what, rc, line))
            arm("live-unreadable-no-verdict", not bad, "; ".join(bad))
            bad = []
            for what, text in (("no-variable", TF_NO_VAR), ("no-default", TF_NO_DEFAULT)):
                rc, line, _ = run_script(put(tmp / (what + ".tf"), text), live_enf)
                if not (rc != 0 and line.startswith("LDO001-MODE verdict=NO-VERDICT")):
                    bad.append("%s rc=%s line=%r" % (what, rc, line))
            rc, line, _ = run_script(tmp / "absent.tf", live_enf)
            if not (rc != 0 and line.startswith("LDO001-MODE verdict=NO-VERDICT")):
                bad.append("absent-tf rc=%s line=%r" % (rc, line))
            arm("tf-unparsable-no-verdict", not bad, "; ".join(bad))
            rc, line, _ = run_script(tf_enf, live_two)
            arm("functions-disagree-refuses", rc != 0 and line.startswith("LDO001-MODE verdict=REFUSED"), "rc=%s line=%r" % (rc, line))

        # safe-apply: the stub terraform records every call; the empty dir keeps the seat gates in WARN mode
        stub = put(tmp / "terraform-stub.sh", STUB)
        empty = tmp / "noswitch"
        empty.mkdir()
        ldo_tree, other_tree = tmp / "ldo", tmp / "other"
        ldo_tree.mkdir()
        other_tree.mkdir()
        put(ldo_tree / "chat_assist.tf", TF % "enforce")
        put(other_tree / "main.tf", TF_OTHER)
        only = {"SAFE_LDO001_MODE_CHECK_ONLY": "1"}

        rc, err, calls = run_apply(ldo_tree, ["-target=module.ldo_001"], live_rec, only, tmp, stub, empty)
        arm("apply-mismatch-blocks-before-terraform", rc != 0 and MARK in err and "verdict=REFUSED default=enforce live=record" in err
            and "BLOCKED" in err and not calls, "rc=%s marker=%s blocked=%s terraform_calls=%s" % (rc, MARK in err, "BLOCKED" in err, calls))
        rc, err, calls = run_apply(ldo_tree, ["-target=module.ldo_001"], live_enf, only, tmp, stub, empty)
        arm("apply-match-passes-the-block", rc == 0 and MARK in err and "verdict=OK default=enforce live=enforce" in err and "BLOCKED" not in err,
            "rc=%s marker=%s" % (rc, MARK in err))
        rc, err, calls = run_apply(ldo_tree, ["-target", "module.ldo_001.aws_lambda_function.handler"], live_rec, only, tmp, stub, empty)
        arm("apply-two-token-target-below-the-module-blocks", rc != 0 and MARK in err and "BLOCKED" in err and not calls, "rc=%s marker=%s calls=%s" % (rc, MARK in err, calls))
        rc, err, calls = run_apply(ldo_tree, [], live_rec, only, tmp, stub, empty)
        arm("apply-unscoped-in-a-tree-with-the-module-blocks", rc != 0 and MARK in err and "BLOCKED" in err and not calls, "rc=%s marker=%s calls=%s" % (rc, MARK in err, calls))
        rc, err, calls = run_apply(ldo_tree, ["-target=aws_s3_bucket.b"], live_rec, only, tmp, stub, empty)
        arm("apply-of-another-target-never-runs-the-check", rc == 0 and MARK not in err and "ldo001" not in err.lower() and not calls,
            "rc=%s marker=%s calls=%s" % (rc, MARK in err, calls))
        rc, err, calls = run_apply(other_tree, [], live_rec, only, tmp, stub, empty)
        arm("apply-in-a-tree-without-the-module-never-runs-the-check", rc == 0 and MARK not in err and "ldo001" not in err.lower() and not calls,
            "rc=%s marker=%s calls=%s" % (rc, MARK in err, calls))
        rc, err, calls = run_apply(ldo_tree, ["-target=module.ldo_001"], tmp / "absent_live.json", only, tmp, stub, empty)
        arm("apply-with-no-verdict-blocks", rc != 0 and "verdict=NO-VERDICT" in err and "BLOCKED" in err and not calls, "rc=%s err=%r calls=%s" % (rc, err[-200:], calls))
        before = AUDIT.read_text(encoding="utf-8", errors="replace") if AUDIT.exists() else ""
        rc, err, calls = run_apply(ldo_tree, ["-target=module.ldo_001"], live_rec, dict(only, LDO001_MODE_OVERRIDE="issuer-check-reason-42"), tmp, stub, empty)
        after = AUDIT.read_text(encoding="utf-8", errors="replace") if AUDIT.exists() else ""
        new = after[len(before):] if after.startswith(before) else after
        arm("override-lets-the-apply-go-on-and-writes-an-audit-line", rc == 0 and "BLOCKED" not in err and "LDO001_MODE_OVERRIDE" in new
            and "issuer-check-reason-42" in new and "2.0.0_SA_COO~CA.l2chk" in new and MARK in err, "rc=%s audit_new=%r" % (rc, new[-200:]))
    if not audit_before and AUDIT.exists():
        AUDIT.unlink()
    for line in fails:
        print(line)
    ok = not fails
    print("L2-GATE ok=%s arms=%d of %d" % (ok, n - len(fails), n))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
