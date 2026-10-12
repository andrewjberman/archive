"""ar16d_checks.py -- the mechanical checks of IRPT_ANLREQ.TO-AR-y-166 (the synthetic-request submitting script, BUILD ONLY).

Usage:  python ar16d_checks.py y166-self --root <worker worktree>
        python ar16d_checks.py y166-plan --root <worker worktree>

y166-self : the script exists, its --self-test exits 0 and prints SUBMIT-SELFTEST-OK, it is ASCII, and its boto3 surface is
            READ-OR-INVOKE ONLY (no put/update/delete/send/create call name anywhere in it).        -> Y166-SELF-OK
y166-plan : `--plan` with tenant cottonwood and a well-formed ticket id prints both events as JSON without any network call
            (run with AWS credentials blanked), the ticket id is in the submission body, the filer is on a reserved domain;
            a tenant other than cottonwood and a malformed ticket id each exit non-zero.            -> Y166-PLAN-OK
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SCRIPT = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~53/r16/submit_synthetic_request.py"
TICKET = "TCK-20261012-0123abcd"
FORBIDDEN_CALLS = re.compile(
    r"\.(put_item|update_item|delete_item|batch_write_item|transact_write_items|put_object|delete_object|copy_object|"
    r"create_multipart_upload|send_message|send_message_batch|publish|put_event|put_events|start_execution|create_\w+|"
    r"update_function_\w+|put_parameter|put_secret_value|admin_\w+|put_rule|put_targets)\(")


def run(script, args, root, env=None):
    return subprocess.run([sys.executable, "-I", str(script)] + args, cwd=str(root), capture_output=True, text=True,
                          env=env or os.environ.copy(), timeout=300)


def main(argv):
    if len(argv) < 2 or "--root" not in argv:
        print("usage: ar16d_checks.py y166-self|y166-plan --root <worktree>")
        return 2
    mode = argv[1]
    root = Path(argv[argv.index("--root") + 1])
    script = root / SCRIPT
    problems = []
    if not script.is_file():
        print("FAIL: no %s" % SCRIPT)
        print("Y166-%s-FAIL" % ("SELF" if mode == "y166-self" else "PLAN"))
        return 1
    if mode == "y166-self":
        text = script.read_text(encoding="utf-8")
        if any(ord(ch) > 127 for ch in text):
            problems.append("the script holds non-ASCII")
        for match in FORBIDDEN_CALLS.finditer(text):
            problems.append("a write-shaped call in the script: %s" % match.group(0))
        done = run(script, ["--self-test"], root)
        if done.returncode != 0 or "SUBMIT-SELFTEST-OK" not in done.stdout:
            problems.append("--self-test rc=%s, last line %r" % (done.returncode, (done.stdout.strip().splitlines() or [""])[-1][:120]))
        tag = "Y166-SELF"
    elif mode == "y166-plan":
        blank = dict(os.environ, AWS_ACCESS_KEY_ID="x", AWS_SECRET_ACCESS_KEY="x", AWS_SESSION_TOKEN="", AWS_PROFILE="__none__",
                     AWS_SHARED_CREDENTIALS_FILE=os.devnull, AWS_CONFIG_FILE=os.devnull, AWS_DEFAULT_REGION="us-east-1")
        ok = run(script, ["--plan", "--tenant", "cottonwood", "--ticket", TICKET], root, blank)
        if ok.returncode != 0:
            problems.append("--plan with cottonwood and a good ticket exits %s" % ok.returncode)
        else:
            events = [json.loads(line) for line in ok.stdout.splitlines() if line.strip().startswith("{")]
            routes = [e.get("routeKey") for e in events]
            if len(events) != 2 or not all(isinstance(r, str) and r.startswith("POST ") for r in routes):
                problems.append("--plan must print exactly two POST events as JSON lines; saw routes %r" % routes)
            elif TICKET not in events[1].get("body", ""):
                problems.append("the submission event's body does not carry the ticket id")
            if not re.search(r"@[a-z0-9.-]*\.invalid\b", ok.stdout):
                problems.append("the filer is not on the reserved domain .invalid")
        bad_tenant = run(script, ["--plan", "--tenant", "49financial", "--ticket", TICKET], root, blank)
        if bad_tenant.returncode == 0:
            problems.append("a tenant other than cottonwood was accepted")
        bad_ticket = run(script, ["--plan", "--tenant", "cottonwood", "--ticket", "TCK-1"], root, blank)
        if bad_ticket.returncode == 0:
            problems.append("a malformed ticket id was accepted")
        tag = "Y166-PLAN"
    else:
        print("unknown mode %s" % mode)
        return 2
    for problem in problems:
        print("FAIL: %s" % problem)
    print("%s-%s" % (tag, "FAIL" if problems else "OK"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
