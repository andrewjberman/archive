"""Count the principals whose ALLOW statements grant on each named S3 bucket.

Issuer-authored check for NFRA_IAMROLES202609 round 9 (2.0.0_SA_COO~ZI). Input: the JSON of
`aws iam get-account-authorization-details --output json` (auto-paginated by the CLI). Reads role,
user and group inline policies and each customer-managed policy's DEFAULT version. A Deny or a
NotResource is not a grant and is not counted. Prints one line per name, then the denominator;
exits 2 when no document was read, so a failed retrieval never reads as a zero.

usage: python allow_names.py <auth.json> <bucket> [<bucket> ...]
"""
import json
import sys


def _list(v):
    return v if isinstance(v, list) else [v]


def _docs(d):
    for key, name_key in (("RoleDetailList", "RoleName"), ("UserDetailList", "UserName"),
                          ("GroupDetailList", "GroupName")):
        for p in d.get(key, []):
            plist = p.get("RolePolicyList") or p.get("UserPolicyList") or p.get("GroupPolicyList") or []
            for pol in plist:
                yield key[:-10] + "/" + p[name_key], pol.get("PolicyDocument") or {}
    for mp in d.get("Policies", []):
        for v in mp.get("PolicyVersionList", []):
            if v.get("IsDefaultVersion"):
                yield "policy/" + mp["PolicyName"], v.get("Document") or {}


def main(argv):
    if len(argv) < 3:
        print("ERROR: usage: allow_names.py <auth.json> <bucket> [<bucket> ...]")
        return 2
    with open(argv[1], encoding="utf-8") as fh:
        d = json.load(fh)
    names = argv[2:]
    hits = {n: set() for n in names}
    owners, docs = set(), 0
    for owner, doc in _docs(d):
        if isinstance(doc, str):
            doc = json.loads(doc)
        owners.add(owner)
        docs += 1
        for st in _list(doc.get("Statement", [])):
            if st.get("Effect") != "Allow" or "Resource" not in st:
                continue
            for r in _list(st["Resource"]):
                if not r.startswith("arn:aws:s3:::"):
                    continue
                bucket = r[len("arn:aws:s3:::"):].split("/", 1)[0]
                if bucket in hits:
                    hits[bucket].add(owner)
    if docs == 0:
        print("ERROR: 0 policy documents read -- a failed retrieval, not a zero")
        return 2
    for n in names:
        print("%s=%d %s" % (n, len(hits[n]), ",".join(sorted(hits[n]))))
    print("DENOMINATOR: principals=%d documents=%d" % (len(owners), docs))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
