"""IRPT_ANLREQ TO-APPLY-R33: the READ-ONLY state capture used for R0 (before) and V (after) of both functions.

usage: python r33_reads.py capture <irpt-status|irpt-ycharts-generate> <label> <work-dir-outside-repo> [--download]
       python r33_reads.py show <state_file.json>      (offline: prints a saved state in the masked form, no AWS call)

Captures, for one function: the configuration (CodeSha256, LastModified, memory, timeout, handler, layers, role name, environment);
the whole S3 version listing of its key (counted client-side) with the latest version downloaded and hashed against the
CodeSha256; the credential-less refusal envelope by a direct invoke of `{"headers":{}}` taken twice (status, FunctionError, body
sha256, bytes); for irpt-ycharts-generate also the role's inline policy list with sizes and the 11-row simulate battery (one
resource per call). Writes <work-dir>/state_<fn>_<label>.json (values included, never committed) and prints a masked summary.
Never prints a secret value; the environment of the generate function is printed as names with a value class, and the
account id is masked in everything printed. Writes nothing to AWS. The invoke is a refusal read with no side effect.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import subprocess
import sys

REGION = "us-east-1"
KEYS = {"irpt-status": "investor-reporting/irpt-status.zip", "irpt-ycharts-generate": "investor-reporting/irpt-ycharts-generate.zip"}
ROLE = "irpt-ycharts-generate-role"
TICKETS = "table/opal-tickets"


def mask(text):
    return str(text).replace(ACCT, "<acct>")


def aws(*args):
    r = subprocess.run(["aws", *args, "--region", REGION], capture_output=True, text=True)
    return r


def _account_id():
    r = aws("sts", "get-caller-identity", "--query", "Account", "--output", "text")
    if r.returncode or not r.stdout.strip().isdigit():
        raise SystemExit("ERROR: could not derive the account id from sts")
    return r.stdout.strip()


ACCT = _account_id()
BUCKET = "opal-%s-lambda-artifacts" % ACCT


def aws_json(*args):
    r = aws(*args, "--output", "json")
    if r.returncode:
        raise SystemExit("ERROR: aws %s rc=%d :: %s" % (" ".join(args[:3]), r.returncode, mask(r.stderr.strip())[:300]))
    return json.loads(r.stdout) if r.stdout.strip() else {}


def b64(data):
    return base64.b64encode(hashlib.sha256(data).digest()).decode()


def config(fn):
    c = aws_json("lambda", "get-function-configuration", "--function-name", fn)
    layers = sorted(layer["Arn"].split(":layer:")[-1] for layer in c.get("Layers", []))
    return {"CodeSha256": c["CodeSha256"], "LastModified": c["LastModified"], "MemorySize": c["MemorySize"], "Timeout": c["Timeout"],
            "Handler": c.get("Handler"), "Runtime": c.get("Runtime"), "Role": c["Role"].split("/")[-1], "Layers": layers,
            "Env": (c.get("Environment") or {}).get("Variables", {}), "State": c.get("State"), "LastUpdateStatus": c.get("LastUpdateStatus")}


def s3_state(fn, work, download):
    key = KEYS[fn]
    listing = aws_json("s3api", "list-object-versions", "--bucket", BUCKET, "--prefix", key)
    vers = [v for v in listing.get("Versions", []) if v["Key"] == key]
    marks = [m for m in listing.get("DeleteMarkers", []) if m["Key"] == key]
    latest = [v for v in vers if v.get("IsLatest")]
    if len(latest) != 1:
        raise SystemExit("ERROR: %d latest versions for %s" % (len(latest), key))
    lv = latest[0]
    out = {"key": key, "versions": len(vers), "delete_markers": len(marks), "latest_version_id": lv["VersionId"], "latest_size": lv["Size"],
           "latest_last_modified": lv["LastModified"], "listing_truncated": bool(listing.get("IsTruncated"))}
    path = os.path.join(work, "%s_%s.zip" % (fn, lv["VersionId"]))
    r = aws("s3api", "get-object", "--bucket", BUCKET, "--key", key, "--version-id", lv["VersionId"], path)
    if r.returncode:
        raise SystemExit("ERROR: get-object %s rc=%d" % (key, r.returncode))
    data = open(path, "rb").read()
    out["latest_sha256_hex"] = hashlib.sha256(data).hexdigest()
    out["latest_code_sha256"] = b64(data)
    out["latest_bytes"] = len(data)
    out["downloaded_to"] = path
    if not download:
        os.remove(path)
        out.pop("downloaded_to")
    return out


def envelope(fn, work, n):
    rows = []
    for i in range(n):
        p = os.path.join(work, "envelope_%s_%d.json" % (fn, i))
        r = aws("lambda", "invoke", "--function-name", fn, "--cli-binary-format", "raw-in-base64-out", "--payload", '{"headers":{}}', p,
                "--query", "[StatusCode,FunctionError]", "--output", "text")
        body = open(p, "rb").read() if os.path.exists(p) else b""
        if os.path.exists(p):
            os.remove(p)
        parts = (r.stdout or "").split()
        rows.append({"status": parts[0] if parts else "?", "function_error": parts[1] if len(parts) > 1 and parts[1] != "None" else None,
                     "body_sha256_16": hashlib.sha256(body).hexdigest()[:16], "bytes": len(body)})
    return rows


def role_state():
    names = aws_json("iam", "list-role-policies", "--role-name", ROLE)["PolicyNames"]
    attached = aws_json("iam", "list-attached-role-policies", "--role-name", ROLE)["AttachedPolicies"]
    docs, total = {}, 0
    for n in sorted(names):
        d = aws_json("iam", "get-role-policy", "--role-name", ROLE, "--policy-name", n, "--query", "PolicyDocument")
        size = len(json.dumps(d, separators=(",", ":")))
        docs[n] = {"compact_chars": size, "doc": d}
        total += size
    return {"inline_names": sorted(names), "attached_managed": len(attached), "aggregate_compact_chars": total, "docs": docs}


def intake_arn(docs):
    """A concrete object ARN inside the first s3:GetObject statement's wildcard resource of the role (the intake store prefix)."""
    for n, d in docs.items():
        st = d["doc"].get("Statement", [])
        for s in (st if isinstance(st, list) else [st]):
            acts = s.get("Action", [])
            acts = [acts] if isinstance(acts, str) else acts
            if s.get("Effect") == "Allow" and any(a in ("s3:GetObject", "s3:*") for a in acts):
                res = s.get("Resource", [])
                for r in ([res] if isinstance(res, str) else res):
                    if r.startswith("arn:aws:s3:::") and r.endswith("*") and "/" in r:
                        return r[:-1] + "r33-battery-probe"
    return None


def battery(role_arn, docs):
    rows = [("dynamodb:GetItem", "arn:aws:dynamodb:%s:%s:%s" % (REGION, ACCT, TICKETS))]
    rows += [(a, "arn:aws:dynamodb:%s:%s:%s" % (REGION, ACCT, TICKETS)) for a in ("dynamodb:Query", "dynamodb:Scan", "dynamodb:PutItem", "dynamodb:UpdateItem", "dynamodb:DeleteItem", "dynamodb:BatchGetItem")]
    rows += [("dynamodb:GetItem", "arn:aws:dynamodb:%s:%s:%s/index/status-index" % (REGION, ACCT, TICKETS)),
             ("dynamodb:GetItem", "arn:aws:dynamodb:%s:%s:table/irpt-requests" % (REGION, ACCT)),
             ("dynamodb:GetItem", "arn:aws:dynamodb:%s:%s:table/opal-users-v2" % (REGION, ACCT))]
    s3 = intake_arn(docs)
    if s3:
        rows.append(("s3:GetObject", s3))
    out = []
    for action, res in rows:
        d = aws_json("iam", "simulate-principal-policy", "--policy-source-arn", role_arn, "--action-names", action, "--resource-arns", res)
        out.append({"action": action, "resource": res.replace(ACCT, "<acct>"), "decision": d["EvaluationResults"][0]["EvalDecision"]})
    return out


def capture(fn, label, work, download):
    os.makedirs(work, exist_ok=True)
    st = {"fn": fn, "label": label, "config": config(fn), "s3": s3_state(fn, work, download), "envelope": envelope(fn, work, 2)}
    if fn == "irpt-ycharts-generate":
        rs = role_state()
        arn = aws_json("iam", "get-role", "--role-name", ROLE)["Role"]["Arn"]
        st["role"] = rs
        st["battery"] = battery(arn, rs["docs"])
    path = os.path.join(work, "state_%s_%s.json" % (fn, label))
    json.dump(st, open(path, "w"), indent=1, sort_keys=True)
    print_state(st)
    return st


def print_state(st):
    """The masked printed form of a captured state (also used offline by `show` on a saved state file)."""
    fn, label = st["fn"], st["label"]
    c, s = st["config"], st["s3"]
    print("STATE %s %s (saved outside the repo)" % (fn, label))
    print("  CodeSha256 %s LastModified %s memory %s timeout %s handler %s runtime %s state %s/%s" % (c["CodeSha256"], c["LastModified"], c["MemorySize"], c["Timeout"], c["Handler"], c["Runtime"], c["State"], c["LastUpdateStatus"]))
    print("  role %s layers %s" % (c["Role"], c["Layers"]))
    print("  S3 %s: %d versions, %d delete markers, listing_truncated=%s, latest %s (%d bytes, modified %s)" % (s["key"], s["versions"], s["delete_markers"], s["listing_truncated"], s["latest_version_id"], s["latest_size"], s["latest_last_modified"]))
    print("  S3 latest sha256 %s base64 %s equals CodeSha256: %s" % (s["latest_sha256_hex"], s["latest_code_sha256"], s["latest_code_sha256"] == c["CodeSha256"]))
    if "downloaded_to" in s:
        print("  downloaded (PRE-WINDOW ZIP): %s" % s["downloaded_to"])
    for i, e in enumerate(st["envelope"]):
        print("  envelope read %d: invoke status %s FunctionError %s body sha256 %s.. %d bytes" % (i + 1, e["status"], e["function_error"], e["body_sha256_16"], e["bytes"]))
    if fn == "irpt-ycharts-generate":
        print("  environment: %d names" % len(c["Env"]))
        for k in sorted(c["Env"]):
            v = c["Env"][k]
            looks = bool(re.search(r"(?i)secret|token|key|password|arn:aws:secretsmanager", k + " " + str(v)))
            print("    %s = %s%s" % (k, "(value withheld, name or value looks secret-bearing)" if looks else mask(v), ""))
        r = st["role"]
        print("  role inline policies (%d): %s; attached managed %d; aggregate compact chars %d (limit 10240 for a role's inline policies)" % (len(r["inline_names"]), r["inline_names"], r["attached_managed"], r["aggregate_compact_chars"]))
        for n in r["inline_names"]:
            print("    %s compact chars %d" % (n, r["docs"][n]["compact_chars"]))
        print("  BATTERY %s (%d rows):" % (label, len(st["battery"])))
        for row in st["battery"]:
            print("    %-20s %-70s %s" % (row["action"], row["resource"], row["decision"]))
    return st


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "show":
        print_state(json.load(open(sys.argv[2])))
    elif len(sys.argv) >= 5 and sys.argv[1] == "capture" and sys.argv[2] in KEYS:
        capture(sys.argv[2], sys.argv[3], sys.argv[4], "--download" in sys.argv)
    else:
        raise SystemExit(__doc__)
