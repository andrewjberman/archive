"""S46 read: which IAM principals hold lambda:InvokeFunction on the 20 functions behind the portal authorizer. READ ONLY."""
import fnmatch
import json
import os
import subprocess
import urllib.parse

S = os.path.dirname(os.path.abspath(__file__))
AWS = os.path.abspath(".tools/aws.cmd")
ACCT = "313476888478"
fns = json.load(open(os.path.join(S, "fns.json")))["authd"]
ARNS = ["arn:aws:lambda:us-east-1:%s:function:%s" % (ACCT, f) for f in fns]


def aws(*a):
    p = subprocess.run([AWS] + list(a) + ["--output", "json"], capture_output=True, text=True, timeout=300)
    if p.returncode != 0:
        raise SystemExit("aws %s rc=%d %s" % (a[:2], p.returncode, p.stderr[-300:]))
    return json.loads(p.stdout)


def doc(d):
    if isinstance(d, str):
        d = json.loads(urllib.parse.unquote(d))
    return d


def stmts(d):
    d = doc(d)
    s = d.get("Statement", [])
    return s if isinstance(s, list) else [s]


def lst(x):
    return x if isinstance(x, list) else ([] if x is None else [x])


def action_match(s):
    acts = [a.lower() for a in lst(s.get("Action"))]
    if "NotAction" in s:
        return "NOTACTION"
    return any(fnmatch.fnmatchcase("lambda:invokefunction", a) for a in acts)


def resource_hits(s):
    if "NotResource" in s:
        return ["NOTRESOURCE"]
    res = lst(s.get("Resource"))
    hits = []
    for arn in ARNS:
        for r in res:
            if fnmatch.fnmatchcase(arn, r) or r == "*":
                hits.append(arn.split(":function:")[1])
                break
    return hits


def grants(policy_docs):
    allow, deny, flags = set(), set(), set()
    for src, d in policy_docs:
        for s in stmts(d):
            am = action_match(s)
            if not am:
                continue
            hits = resource_hits(s)
            if not hits:
                continue
            if am == "NOTACTION" or hits == ["NOTRESOURCE"]:
                flags.add(src)
                continue
            if "Condition" in s:
                flags.add(src + " (Condition)")
            (allow if s.get("Effect") == "Allow" else deny).update((src, h) for h in hits)
    return allow, deny, flags


ad = aws("iam", "get-account-authorization-details", "--filter", "User", "Group", "Role", "LocalManagedPolicy", "AWSManagedPolicy")
# a user/role/group list is paginated by the CLI; the CLI auto-paginates and merges
pol = {}
for mp in ad.get("Policies", []):
    ver = [v for v in mp["PolicyVersionList"] if v["IsDefaultVersion"]]
    if ver:
        pol[mp["Arn"]] = ver[0]["Document"]
groups = {g["GroupName"]: g for g in ad.get("GroupDetailList", [])}


def docs_for(entity, kind):
    out = []
    for ip in entity.get("UserPolicyList" if kind == "user" else "RolePolicyList", []):
        out.append(("inline:" + ip["PolicyName"], ip["PolicyDocument"]))
    for a in entity.get("AttachedManagedPolicies", []):
        if a["PolicyArn"] in pol:
            out.append(("managed:" + a["PolicyName"], pol[a["PolicyArn"]]))
    return out


result = {"users": [], "roles": [], "groups": []}
den = {"users": len(ad.get("UserDetailList", [])), "roles": len(ad.get("RoleDetailList", [])), "groups": len(groups), "managed_policies": len(pol)}
for u in ad.get("UserDetailList", []):
    d = docs_for(u, "user")
    for gn in u.get("GroupList", []):
        g = groups.get(gn, {})
        for ip in g.get("GroupPolicyList", []):
            d.append(("group:%s:inline:%s" % (gn, ip["PolicyName"]), ip["PolicyDocument"]))
        for a in g.get("AttachedManagedPolicies", []):
            if a["PolicyArn"] in pol:
                d.append(("group:%s:managed:%s" % (gn, a["PolicyName"]), pol[a["PolicyArn"]]))
    allow, deny, flags = grants(d)
    if allow or flags:
        result["users"].append({"name": u["UserName"], "allow_fns": sorted({h for _, h in allow}), "via": sorted({s for s, _ in allow}), "deny": sorted({h for _, h in deny}), "flags": sorted(flags),
                                "boundary": bool(u.get("PermissionsBoundary"))})
for r in ad.get("RoleDetailList", []):
    d = docs_for(r, "role")
    allow, deny, flags = grants(d)
    if allow or flags:
        trust = [s.get("Principal") for s in stmts(r["AssumeRolePolicyDocument"])]
        result["roles"].append({"name": r["RoleName"], "path": r.get("Path"), "allow_fns": sorted({h for _, h in allow}), "via": sorted({s for s, _ in allow}), "deny": sorted({h for _, h in deny}), "flags": sorted(flags),
                                "trust": json.dumps(trust)[:200], "boundary": bool(r.get("PermissionsBoundary"))})
json.dump({"denominator": den, "functions": fns, "result": result}, open(os.path.join(S, "s46_result.json"), "w"), indent=1)
print("DENOMINATOR", den, "functions", len(fns))
print("users with grant:", len(result["users"]), [u["name"] for u in result["users"]])
print("roles with grant:", len(result["roles"]))
for r in result["roles"]:
    print("  ", r["name"], "fns", len(r["allow_fns"]), "deny", len(r["deny"]), "flags", len(r["flags"]), "trust", r["trust"][:90])
