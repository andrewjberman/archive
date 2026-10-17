"""Read-only verifier of the HMAC list producer's live state (issuer 2.0.0_SA_COO~P2): my own reads for grading IB-hm-5 and the first scheduled fire.

Usage: python hm5_verify_read.py <repo_root>

Prints one line per fact, "FACT <name> <PASS|FAIL|NOT_YET> <short reason>", then a summary. Reads only (S3 head, Lambda configuration, IAM get-role, Secrets Manager describe and version ids). It never reads the secret VALUE, never prints a number by firm (existence and freshness only), and never writes.
"""
import datetime as dt
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(".").resolve()
AWS = str(ROOT / ".tools" / "aws")
BUNDLE_BEFORE = "W2WragrP52i8M7MfL22oXVPuHsTjyVLO"
ZIP_PIN = "I7T8wRYmv11nytYpD7i+4XCwwvy6JUaB3fdsgtHyXmA="
ENV_KEYS = {"IRPT_HMAC_SECRET_ID", "IRPT_HMAC_ROLE_ARN", "IRPT_HMAC_LIST_URI_MAP"}
ROLE = "irpt-hmac-list-stage-role"
SECRET = "irpt/hmac-list/key"
facts = []


def aws(*args):
    p = subprocess.run(["bash", AWS, *args], capture_output=True, text=True, timeout=90)
    return p.returncode, p.stdout, p.stderr


def jaws(*args):
    rc, out, err = aws(*args, "--output", "json")
    if rc != 0:
        return None, err.strip().splitlines()[-1][:120] if err.strip() else "rc=%d" % rc
    try:
        return json.loads(out), ""
    except ValueError:
        return None, "unparseable"


def fact(name, state, why=""):
    facts.append((name, state))
    print("FACT %s %s %s" % (name, state, why))


# 1. the runner bundle
d, e = jaws("s3api", "head-object", "--bucket", "opal-data-mdpf", "--key", "code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz")
if d is None:
    fact("bundle_head", "FAIL", e)
else:
    v = d.get("VersionId")
    fact("bundle_version_changed", "PASS" if v and v != BUNDLE_BEFORE else "NOT_YET", "version is %s the pre-apply version" % ("not" if v != BUNDLE_BEFORE else "still"))

# 2. the refresh Lambda: code digest and the three environment key names
d, e = jaws("lambda", "get-function-configuration", "--function-name", "irpt-directory-refresh")
if d is None:
    fact("lambda_config", "FAIL", e)
else:
    fact("lambda_code_equals_pin", "PASS" if d.get("CodeSha256") == ZIP_PIN else "NOT_YET", "CodeSha256 %s the pin" % ("equals" if d.get("CodeSha256") == ZIP_PIN else "differs from"))
    keys = set((d.get("Environment") or {}).get("Variables", {}).keys())
    fact("lambda_env_has_three_keys", "PASS" if ENV_KEYS <= keys else "NOT_YET", "%d of 3 key names present" % len(ENV_KEYS & keys))

# 3. the stage role: exists, trust names exactly one principal
d, e = jaws("iam", "get-role", "--role-name", ROLE)
if d is None:
    fact("stage_role_exists", "NOT_YET", e)
else:
    st = d["Role"]["AssumeRolePolicyDocument"]["Statement"]
    st = st if isinstance(st, list) else [st]
    one = len(st) == 1 and isinstance(st[0].get("Principal", {}).get("AWS"), str) and "*" not in st[0]["Principal"]["AWS"] and st[0].get("Action") == "sts:AssumeRole"
    fact("stage_role_exists", "PASS", "role present")
    fact("stage_role_trust_single_principal", "PASS" if one else "FAIL", "trust has %d statement(s), single non-wildcard AWS principal: %s" % (len(st), one))

# 4. the secret: container exists, exactly one version, value never read
d, e = jaws("secretsmanager", "list-secret-version-ids", "--secret-id", SECRET)
if d is None:
    fact("secret_container", "NOT_YET", e)
else:
    n = len(d.get("Versions", []))
    fact("secret_container", "PASS", "container present")
    fact("secret_one_version", "PASS" if n == 1 else ("NOT_YET" if n == 0 else "FAIL"), "version count %d" % n)

# 5. the list keys: existence and freshness (no counts, no per-firm figure beyond present/absent)
spec = importlib.util.spec_from_file_location("opal_naming_v", str(ROOT / "lib" / "opal_naming.py"))
mod = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(ROOT / "lib"))
spec.loader.exec_module(mod)
reg = json.loads((ROOT / "data" / "firm_registry.json").read_text(encoding="utf-8"))
firms = [x["firm_id"] for x in (reg["firms"] if isinstance(reg, dict) else reg) if x.get("kind") == "client"]
now = dt.datetime.now(dt.timezone.utc)
present = 0
fresh = 0
for f in firms:
    uri = mod.address("globgrph", f, "silver", "account_id_list", "hmac")
    bucket, key = uri[5:].split("/", 1)
    d, e = jaws("s3api", "head-object", "--bucket", bucket, "--key", key)
    if d is not None:
        present += 1
        lm = dt.datetime.fromisoformat(d["LastModified"].replace("Z", "+00:00"))
        if (now - lm).total_seconds() < 36 * 3600:
            fresh += 1
fact("list_keys_present", "PASS" if present == len(firms) else ("NOT_YET" if present == 0 else "PARTIAL"), "present for %s of the client firms" % ("all" if present == len(firms) else ("none" if present == 0 else "some")))
fact("list_keys_fresh_36h", "PASS" if fresh == len(firms) else ("NOT_YET" if fresh == 0 else "PARTIAL"), "fresh for %s of the client firms" % ("all" if fresh == len(firms) else ("none" if fresh == 0 else "some")))

print("SUMMARY " + " ".join("%s=%s" % f for f in facts))
