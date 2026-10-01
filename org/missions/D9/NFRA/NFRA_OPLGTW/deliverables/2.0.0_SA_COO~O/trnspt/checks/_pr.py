"""OG-pr-1 reads (CTO ruling R3 / C11, row Z-S24): the three gateway read secrets and their one exact-ARN grant; and
(for OG-rl-1) the release-template roster read.

usage: python _pr.py tf | simulate <sim_json_path> | template <deploy_template_path> | policy <policy_json_path>
Run from the worktree root. Prints evidence lines, then `RESULT: PASS|FAIL`. Never prints a principal value.
"""
import json
import re
import subprocess
import sys

SECRET = "gateway/principals/rosters"
SECRETS = ["gateway/transcripts/bearer", "gateway/mail/bearer", "gateway/principals/rosters"]
TF = "infra/aws/terraform/opal-gateway/gateway-read-secrets.tf"
GUID = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")


def done(ok):
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)


def tf():
    try:
        s = open(TF, encoding="utf-8").read()
    except OSError as e:
        print("%s unreadable: %s" % (TF, e))
        done(False)
    data = re.findall(r'data\s+"aws_secretsmanager_secret"\s+"(\w+)"\s*\{\s*name\s*=\s*"([^"]+)"', s)
    print("secret data sources: %d %s" % (len(data), sorted(n for _, n in data)))
    actions = re.findall(r'"(secretsmanager:[A-Za-z*]+|[a-z0-9]+:\*|\*)"', s)
    print("actions named: %s" % actions)
    res = re.findall(r"Resource\s*=\s*(\[[^\]]*\]|[^\n]+)", s)
    refs = re.findall(r"data\.aws_secretsmanager_secret\.(\w+)\.arn", " ".join(res))
    print("resource statements %d; ARN refs %s" % (len(res), sorted(refs)))
    version = "aws_secretsmanager_secret_version" in s
    print("secret_version resource present: %s" % version)
    ok = (sorted(n for _, n in data) == sorted(SECRETS) and actions == ["secretsmanager:GetSecretValue"]
          and len(res) == 1 and sorted(refs) == sorted(k for k, _ in data)
          and "aws_iam_role.gw.id" in s and not version and not GUID.search(s))
    done(ok)


def simulate(path):
    d = json.load(open(path, encoding="utf-8"))
    rows = [(r.get("EvalResourceName", ""), r.get("EvalDecision")) for r in d.get("EvaluationResults", [])]
    granted = [dec for arn, dec in rows if any(":secret:%s-" % n in arn for n in SECRETS)]
    sibling = [dec for arn, dec in rows if ":secret:gateway/" in arn and not any(":secret:%s-" % n in arn for n in SECRETS)]
    print("simulate: granted ARNs %d %s; sibling gateway/* ARNs %d %s" % (len(granted), granted, len(sibling), sibling))
    done(len(granted) == 3 and all(x == "allowed" for x in granted) and sibling == ["implicitDeny"])


def template(out):
    s = open(out, encoding="utf-8").read()
    print("GUID literals in the template: %d" % len(GUID.findall(s)))
    ok = not GUID.search(s)
    reads = SECRET in s
    print("template reads %s host-side: %s" % (SECRET, reads))
    shell_req = "OG_MASTER_ADMIN_PRINCIPALS is required" in s or "OG_WRITE_CAPABLE_PRINCIPALS is required" in s
    print("deploying-shell roster requirement still present: %s" % shell_req)
    render = [ln for ln in s.splitlines() if "/.env >/dev/null" in ln and "printf" in ln]
    if len(render) == 1:
        fmt = re.search(r"printf '([^']*)'", render[0]).group(1)
        args = render[0][render[0].index(fmt) + len(fmt) + 1:].split("|")[0]
        n_fmt, n_args = fmt.count("%s"), len(re.findall(r'"[^"]*"', args))
        print(".env render: %%s %d, args %d; MASTER_ADMIN_PRINCIPALS line %s, WRITE_CAPABLE_PRINCIPALS line %s"
              % (n_fmt, n_args, "MASTER_ADMIN_PRINCIPALS=" in fmt, "WRITE_CAPABLE_PRINCIPALS=" in fmt))
        ok &= n_fmt == n_args and "MASTER_ADMIN_PRINCIPALS=" in fmt and "WRITE_CAPABLE_PRINCIPALS=" in fmt
    else:
        print(".env render lines: %d (expected 1)" % len(render))
        ok = False
    b = subprocess.run(["bash", "-n", out], capture_output=True, text=True)
    print("bash -n rc=%d %s" % (b.returncode, b.stderr.strip()[:200]))
    ok &= reads and not shell_req and b.returncode == 0
    done(ok)


def policy(path):
    d = json.load(open(path, encoding="utf-8"))
    doc = d.get("PolicyDocument", d)
    st = doc.get("Statement", [])
    st = st if isinstance(st, list) else [st]
    acts = [a for x in st for a in (x.get("Action") if isinstance(x.get("Action"), list) else [x.get("Action")])]
    res = [r for x in st for r in (x.get("Resource") if isinstance(x.get("Resource"), list) else [x.get("Resource")])]
    print("live policy statements %d; actions %s; resources %s" % (len(st), acts, res))
    ok = (len(st) == 1 and acts == ["secretsmanager:GetSecretValue"] and len(res) == 1
          and (":secret:%s-" % SECRET) in (res[0] or "") and st[0].get("Effect") == "Allow")
    done(ok)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "tf":
        tf()
    elif mode == "simulate":
        simulate(sys.argv[2])
    elif mode == "template":
        template(sys.argv[2])
    elif mode == "policy":
        policy(sys.argv[2])
    else:
        print("unknown mode %r" % mode)
        done(False)
