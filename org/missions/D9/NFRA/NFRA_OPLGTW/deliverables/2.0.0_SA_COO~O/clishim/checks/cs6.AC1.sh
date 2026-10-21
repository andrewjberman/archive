#!/usr/bin/env bash
# OPLGTW OG-cs-6 AC1 (cli-shim workstream, wave 3): infra/aws/terraform/opal-gateway/folder_reader_iam.tf, the folder reader's IAM TEXT (nothing is applied by this cell). One fresh process, text only.
#  (a) the file exists and its braces and brackets balance; it creates exactly one aws_iam_role named gateway-folder-read-role and the gateway's assume policy gateway-assume-folder-reader-policy (names from lib/opal_naming.py name(), the same strings this probe reads back from the builder);
#  (b) the ALLOW statements name only the three served buckets: the GetObject/GetObjectVersion Allow resources are exactly the three "arn:aws:s3:::<bucket>/*" forms and the ListBucket Allow resources are exactly the three bucket arns; no Allow carries a bare "*" resource and no Allow carries an action outside s3:GetObject, s3:GetObjectVersion, s3:ListBucket (the assume policy's sts:AssumeRole aside);
#  (c) a DENY on s3:GetObject and s3:GetObjectVersion names, for EACH of the three buckets, the four forms bucket/bronze/*, bucket/*/bronze/*, bucket/raw/*, bucket/*/raw/* (the CVO's cure at PRD v3.19: no grant reaches a bronze or raw prefix), and a DENY of every non-read action (NotAction) is present;
#  (d) the trust of the role admits only the gateway role and carries an sts:ExternalId condition read from a secret resource this file declares (a new secret; the existing schwab ExternalId secret is not read here).
. "$(dirname "$0")/../../r47/checks/_gwtests.sh"
res=$(python3 -I - "$(native "$GW")" <<'PYEOF'
import os, re, sys
G = sys.argv[1]
ok = True
REPO = os.path.abspath(os.path.join(G, "..", "..", "..", ".."))
TF = os.path.join(REPO, "infra", "aws", "terraform", "opal-gateway", "folder_reader_iam.tf")
if len(sys.argv) > 2:
    TF = sys.argv[2]


def say(label, cond):
    global ok
    ok = ok and bool(cond)
    print("%s: %s" % (label, "ok" if cond else "NOT OK"))


try:
    txt = open(TF, encoding="utf-8").read()
except OSError:
    print("folder_reader_iam.tf is absent")
    print("NO")
    sys.exit(0)
sys.path.insert(0, os.path.join(REPO, "lib"))
import opal_naming as n
ROLE = n.name("gateway", None, "folder-read", "role")
POL = n.name("gateway", None, "assume-folder-reader", "policy")
BUCKETS = ["opal-data-assets", "opal-data-etfs", "opal-data-portal-v2"]
bal = all(txt.count(a) == txt.count(b) for a, b in (("{", "}"), ("[", "]"), ("(", ")")))
roles = re.findall(r'resource\s+"aws_iam_role"\s+"([^"]+)"', txt)
say("balanced, one aws_iam_role (%s), role %s and policy %s named" % (roles, ROLE, POL), bal and len(roles) == 1 and ROLE in txt and POL in txt)
# split the policy statements: each Sid = "..." opens a statement; take the text up to the next Sid
sids = [(m.group(1), m.start()) for m in re.finditer(r'Sid\s*=\s*"([^"]+)"', txt)]
stmts = {}
for i, (s, st) in enumerate(sids):
    stmts[s] = txt[st:(sids[i + 1][1] if i + 1 < len(sids) else len(txt))]
allows = {s: t for s, t in stmts.items() if re.search(r'Effect\s*=\s*"Allow"', t)}
denies = {s: t for s, t in stmts.items() if re.search(r'Effect\s*=\s*"Deny"', t)}
objarn = sorted("arn:aws:s3:::%s/*" % b for b in BUCKETS)
bktarn = sorted("arn:aws:s3:::%s" % b for b in BUCKETS)
bad_actions, bad_res, obj_ok, list_ok = [], [], False, False
for s, t in allows.items():
    acts = re.findall(r'"(s3:[A-Za-z*]+|sts:AssumeRole|sts:\*|\*)"', t)
    if any(a not in ("s3:GetObject", "s3:GetObjectVersion", "s3:ListBucket", "sts:AssumeRole") for a in acts):
        bad_actions.append(s)
    arns = sorted(set(re.findall(r'"(arn:aws:s3:::[^"]+)"', t)))
    if re.search(r'Resource\s*=\s*"\*"', t) or re.search(r'Resource\s*=\s*\[\s*"\*"', t):
        bad_res.append(s)
    if "s3:GetObject" in acts and arns == objarn:
        obj_ok = True
    if "s3:ListBucket" in acts and arns == bktarn:
        list_ok = True
say("the Allow statements: object reads on exactly %s, listing on exactly the three bucket arns, no bare *, no other action (bad actions %s, bare * %s)" % (objarn, bad_actions, bad_res), obj_ok and list_ok and not bad_actions and not bad_res)
forms = []
for b in BUCKETS:
    for seg in ("bronze", "raw"):
        forms += ["arn:aws:s3:::%s/%s/*" % (b, seg), "arn:aws:s3:::%s/*/%s/*" % (b, seg)]
hit = [s for s, t in denies.items() if "s3:GetObject" in t and "s3:GetObjectVersion" in t and all('"%s"' % f in t for f in forms)]
say("a Deny of GetObject and GetObjectVersion names all %d bronze and raw forms (statement %s)" % (len(forms), hit), bool(hit))
say("a Deny of every non-read action (NotAction) is present", any(re.search(r"NotAction", t) for t in denies.values()))
trust = re.search(r"assume_role_policy\s*=\s*jsonencode\(.*?\n  \}\)", txt, re.S)
tt = trust.group(0) if trust else ""
sec = re.findall(r'resource\s+"aws_secretsmanager_secret"\s+"([^"]+)"', txt)
say("the trust admits only the gateway role under an sts:ExternalId read from a secret declared here (secrets %s)" % sec, "aws_iam_role.gw.arn" in tt and "sts:ExternalId" in tt and len(sec) >= 1 and "schwab_external_ids" not in tt)
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
