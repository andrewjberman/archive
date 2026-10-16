"""IRPT_ANLREQ TO-APPLY-t54 (0.7.0_AE_CloudOps~AQ2): READ-ONLY state capture of the four Lambdas, the draft-store role and the commentary mapping.

  python t54_reads.py state <label> <work-dir-outside-repo> [--download]   capture; --download fetches each deployed zip (the rollback artifacts)
  python t54_reads.py zipdiff <zip-a> <zip-b>                               member-by-member compare (names and sha256), offline

Prints, per function: CodeSha256, LastModified, MemorySize, Timeout, Handler, environment NAMES only, layer count, and (with --download) the
deployed zip's sha256 (hex), base64 sha256 and member count. For the role: the inline policy names and the Sid of every statement. For the
commentary function: its event source mappings (count, State). Writes nothing to AWS. No value of an environment variable is printed.
"""
from __future__ import annotations

import base64
import hashlib
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

REGION = "us-east-1"
FUNCS = ("irpt-commentary-draft-store-lambda", "outlook-global-commentary-draft-lambda",
         "teams-global-transcripts-pull-lambda", "outlook-global-transcripts-pull-lambda")
ROLE = "irpt-commentary-draft-store-role"


def b64(raw):
    return base64.b64encode(hashlib.sha256(raw).digest()).decode()


def members(path):
    with zipfile.ZipFile(path) as z:
        return {i.filename: hashlib.sha256(z.read(i.filename)).hexdigest() for i in z.infolist() if not i.is_dir()}


def zipdiff(a, b):
    ma, mb = members(a), members(b)
    names = sorted(set(ma) | set(mb))
    changed = [n for n in names if n in ma and n in mb and ma[n] != mb[n]]
    added = [n for n in names if n not in ma]
    removed = [n for n in names if n not in mb]
    print("members a=%d b=%d union=%d changed=%s added_in_b=%s removed_in_b=%s" % (len(ma), len(mb), len(names), changed, added, removed))
    return changed, added, removed


def state(label, workdir, download):
    import boto3
    lam = boto3.client("lambda", region_name=REGION)
    iam = boto3.client("iam", region_name=REGION)
    out = {"label": label, "functions": {}}
    wd = Path(workdir)
    wd.mkdir(parents=True, exist_ok=True)
    for fn in FUNCS:
        g = lam.get_function(FunctionName=fn)
        c = g["Configuration"]
        row = {"CodeSha256": c["CodeSha256"], "LastModified": c["LastModified"], "MemorySize": c["MemorySize"], "Timeout": c["Timeout"],
               "Handler": c.get("Handler"), "Runtime": c.get("Runtime"), "CodeSize": c["CodeSize"],
               "env_names": sorted((c.get("Environment") or {}).get("Variables", {})), "layers": len(c.get("Layers") or []),
               "role": c["Role"].rsplit("/", 1)[-1]}
        if download:
            raw = urllib.request.urlopen(g["Code"]["Location"], timeout=120).read()
            p = wd / ("deployed_%s_%s.zip" % (fn, label))
            p.write_bytes(raw)
            row.update(zip_sha256_hex=hashlib.sha256(raw).hexdigest(), zip_sha256_b64=b64(raw), zip_bytes=len(raw), zip_members=len(members(p)),
                       zip_equals_CodeSha256=b64(raw) == c["CodeSha256"])
        out["functions"][fn] = row
    maps = lam.list_event_source_mappings(FunctionName="outlook-global-commentary-draft-lambda")["EventSourceMappings"]
    out["commentary_mappings"] = [{"State": m["State"], "BatchSize": m.get("BatchSize")} for m in maps]
    pols = iam.list_role_policies(RoleName=ROLE)["PolicyNames"]
    out["role_policies"] = {}
    for pn in pols:
        doc = iam.get_role_policy(RoleName=ROLE, PolicyName=pn)["PolicyDocument"]
        st = doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]
        out["role_policies"][pn] = [s.get("Sid") for s in st]
    out["attached"] = [p["PolicyName"] for p in iam.list_attached_role_policies(RoleName=ROLE)["AttachedPolicies"]]
    (wd / ("state_%s.json" % label)).write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    for fn, r in out["functions"].items():
        print(fn, json.dumps(r, sort_keys=True))
    print("commentary mappings:", len(out["commentary_mappings"]), out["commentary_mappings"])
    print("role inline policies:", json.dumps(out["role_policies"]), "attached:", out["attached"])
    return 0


def main(argv):
    if len(argv) >= 3 and argv[0] == "state":
        return state(argv[1], argv[2], "--download" in argv)
    if len(argv) == 3 and argv[0] == "zipdiff":
        zipdiff(argv[1], argv[2])
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
