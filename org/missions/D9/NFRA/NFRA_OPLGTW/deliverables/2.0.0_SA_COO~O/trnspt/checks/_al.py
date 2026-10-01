"""OG-al-1 reads: the ALB listener rule that lets the two headless prefixes reach the gateway without the OIDC sign-in
(the ms_ingest_capability pattern; the app's own bearer is the gate).

usage: python _al.py tf | live <describe_rules_json> <probe_json>
Prints evidence lines, then `RESULT: PASS|FAIL`.
"""
import json
import re
import sys

TF = "infra/aws/terraform/opal-gateway/hx-capability.tf"
PATHS = ["/hx/mail/*", "/hx/transcripts/*"]


def done(ok):
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)


def tf():
    try:
        s = open(TF, encoding="utf-8").read()
    except OSError as e:
        print("%s unreadable: %s" % (TF, e))
        done(False)
    rules = re.findall(r'resource\s+"aws_lb_listener_rule"\s+"(\w+)"', s)
    others = re.findall(r'resource\s+"(?!aws_lb_listener_rule)(\w+)"', s)
    vals = re.findall(r"values\s*=\s*\[([^\]]*)\]", s)
    paths = sorted(v.strip().strip('"') for blk in vals for v in blk.split(",") if v.strip())
    types = re.findall(r'type\s*=\s*"(\w[\w-]*)"', s)
    print("listener rules %d %s; other resources %s" % (len(rules), rules, others))
    print("path patterns %s" % paths)
    print("action types %s" % types)
    ok = (len(rules) == 1 and not others and paths == PATHS and types == ["forward"]
          and "aws_lb_listener.https.arn" in s and "aws_lb_target_group.gw.arn" in s)
    done(ok)


def live(rules_path, probe_path):
    d = json.load(open(rules_path, encoding="utf-8"))
    hits = []
    for r in d.get("Rules", []):
        pp = sorted(v for c in r.get("Conditions", []) if c.get("Field") == "path-pattern"
                    for v in (c.get("PathPatternConfig", {}).get("Values") or c.get("Values") or []))
        if any(p.startswith("/hx/") for p in pp):
            hits.append((r.get("Priority"), pp, [a.get("Type") for a in r.get("Actions", [])]))
    print("live rules carrying /hx/: %d %s" % (len(hits), hits))
    ok = len(hits) == 1 and hits[0][1] == PATHS and hits[0][2] == ["forward"]
    p = json.load(open(probe_path, encoding="utf-8"))
    for k in ("hx_mail", "hx_transcripts", "control"):
        print("probe %s: status %s, redirects to sign-in %s" % (k, p[k]["status"], p[k]["to_signin"]))
    ok &= not p["hx_mail"]["to_signin"] and not p["hx_transcripts"]["to_signin"]
    ok &= p["control"]["to_signin"]  # negative control: a non-/hx path still meets the OIDC sign-in
    done(ok)


if __name__ == "__main__":
    if sys.argv[1] == "tf":
        tf()
    elif sys.argv[1] == "live":
        live(sys.argv[2], sys.argv[3])
    else:
        print("unknown mode")
        done(False)
