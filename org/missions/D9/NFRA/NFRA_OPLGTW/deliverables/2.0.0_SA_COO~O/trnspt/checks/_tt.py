"""OG-tt-1 reads: the ALB listener rule that lets EXACTLY /ms/taxsma-workbook reach the gateway without the OIDC sign-in
(the ms_ingest_capability exact-path pattern; the route's own capability bearer is the gate). Andrew-direct ~17:2xZ
(site Z runs the Tax SMA gateway release); 1.0.0_SA_CTO~O msg 27986.

usage: python _tt.py tf | live <describe_rules_json> <probe_json>
"""
import json
import re
import sys

TF = "infra/aws/terraform/opal-gateway/taxsma-capability.tf"
PATHS = ["/ms/taxsma-workbook"]


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
    done(len(rules) == 1 and not others and paths == PATHS and types == ["forward"]
         and "aws_lb_listener.https.arn" in s and "aws_lb_target_group.gw.arn" in s)


def live(rules_path, probe_path):
    d = json.load(open(rules_path, encoding="utf-8"))
    hits = []
    for r in d.get("Rules", []):
        pp = sorted(v for c in r.get("Conditions", []) if c.get("Field") == "path-pattern"
                    for v in (c.get("PathPatternConfig", {}).get("Values") or c.get("Values") or []))
        if "/ms/taxsma-workbook" in pp or any("taxsma" in p for p in pp):
            hits.append((r.get("Priority"), pp, [a.get("Type") for a in r.get("Actions", [])]))
    print("live rules carrying the Tax path: %d %s" % (len(hits), hits))
    ok = len(hits) == 1 and hits[0][1] == PATHS and hits[0][2] == ["forward"]
    p = json.load(open(probe_path, encoding="utf-8"))
    for k in ("tax", "ms_unknown", "root", "ms_sites"):
        print("probe %s: status %s, redirects to sign-in %s" % (k, p[k]["status"], p[k]["to_signin"]))
    ok &= isinstance(p["tax"]["status"], int) and not p["tax"]["to_signin"]
    ok &= p["ms_unknown"]["to_signin"] and p["root"]["to_signin"]  # no /ms/* wildcard; the default still signs in
    ok &= p["ms_sites"]["status"] == 401 and not p["ms_sites"]["to_signin"]  # rule 31 unchanged
    done(ok)


if __name__ == "__main__":
    if sys.argv[1] == "tf":
        tf()
    elif sys.argv[1] == "live":
        live(sys.argv[2], sys.argv[3])
    else:
        done(False)
