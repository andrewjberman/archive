"""FB-k-2 read-only summariser: reads a saved `aws iam get-account-authorization-details --filter Role
LocalManagedPolicy` file and reports every role whose inline or customer-managed policy statements grant
the Inflection legacy bucket (opal-data-inf, NOT opal-data-inflection) or the Inflection scope of the shared
Black Diamond lake. Prints role name, policy name, policy source, action classes and resource shapes only.
Usage: python -I planinv_iam_grants.py <authz-details.json>
"""
import json
import re
import sys

LEGACY_INF = re.compile(r"opal-data-inf(?!lection)")
BD_INF_SCOPE = re.compile(r"opal-data-bd[^\"]*?(inflection|/inf/|inf-)", re.I)
WRITE_ACT = re.compile(r"^(s3:)?(Put|Delete|Create|Update|Restore|Abort|Replicate|Tag|Untag)", re.I)
READ_ACT = re.compile(r"^(s3:)?(Get|List|Head)", re.I)


def as_list(x):
    if x is None:
        return []
    return x if isinstance(x, list) else [x]


def classes(stmt):
    acts = [str(a) for a in as_list(stmt.get("Action")) + as_list(stmt.get("NotAction"))]
    out = set()
    for a in acts:
        if a == "*" or a == "s3:*":
            out.add("ALL")
        elif WRITE_ACT.search(a):
            out.add("write")
        elif READ_ACT.search(a):
            out.add("read")
        else:
            out.add("other")
    return "/".join(sorted(out)) or "none"


def shapes(stmt):
    res = [str(r) for r in as_list(stmt.get("Resource"))]
    keep = []
    for r in res:
        if LEGACY_INF.search(r) or BD_INF_SCOPE.search(r) or r == "*":
            # print the resource SHAPE only (bucket and prefix), never an id-bearing key
            keep.append(re.sub(r"[0-9]{9,}", "<id>", r)[:120])
    return keep


def scan_doc(doc):
    hits = []
    for st in as_list(doc.get("Statement")):
        if not isinstance(st, dict):
            continue
        blob = json.dumps(st)
        if LEGACY_INF.search(blob) or BD_INF_SCOPE.search(blob):
            eff = st.get("Effect", "?")
            hits.append((eff, classes(st), shapes(st) or ["(via condition)"]))
    return hits


def main(path):
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    roles = d.get("RoleDetailList", [])
    pols = {p["Arn"]: p for p in d.get("Policies", [])}
    rows = []
    for r in roles:
        rname = r.get("RoleName", "")
        for ip in r.get("RolePolicyList", []) or []:
            doc = ip.get("PolicyDocument") or {}
            if isinstance(doc, str):
                try:
                    doc = json.loads(doc)
                except ValueError:
                    doc = {}
            for eff, cls, shp in scan_doc(doc):
                rows.append((rname, "inline:" + ip.get("PolicyName", ""), eff, cls, shp))
        for ap in r.get("AttachedManagedPolicies", []) or []:
            arn = ap.get("PolicyArn", "")
            pol = pols.get(arn)
            if not pol:
                continue
            for v in pol.get("PolicyVersionList", []) or []:
                if not v.get("IsDefaultVersion"):
                    continue
                doc = v.get("Document") or {}
                if isinstance(doc, str):
                    try:
                        doc = json.loads(doc)
                    except ValueError:
                        doc = {}
                for eff, cls, shp in scan_doc(doc):
                    rows.append((rname, "managed:" + ap.get("PolicyName", ""), eff, cls, shp))
    print("DENOMINATOR roles=%d customer_policies=%d" % (len(roles), len(pols)))
    for row in sorted(set((a, b, c, dd, tuple(e)) for a, b, c, dd, e in rows)):
        print("GRANT role=%s | policy=%s | effect=%s | actions=%s | resource=%s" % (
            row[0], row[1], row[2], row[3], "; ".join(row[4])))
    print("GRANT-ROWS=%d roles_with_grant=%d" % (len(set(rows)), len(set(r[0] for r in rows))))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: planinv_iam_grants.py <authz-details.json>")
    main(sys.argv[1])
