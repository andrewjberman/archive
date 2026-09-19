"""Driven control for LT-e-5's legs: an INJECTED graph (no AWS) where a Lambda carries NO token and is
reached ONLY by its trigger (X) or ONLY by its role's grant (Y); a third Lambda (Z) is reached by nothing.
Expect X and Y involved with the named leg, Z not involved, and the /aws/lambda log group excluded.
Then a MUTANT: remove the trigger edge -> X must drop out.

LT-e-6 (round 4) re-pointed the iam_grant leg onto the LIVE authorization plane, so this control moved
with it. It no longer stubs the grant MATCHER: it injects a census in the live census's own shape and
lets the real iam_grant_roles() parse it, which puts the re-pointed parser itself under the control
rather than only the wiring around it. One arm is new and is the re-point's DISCLOSED BLIND SPOT made
falsifiable -- a role whose only subject-naming statement is an attached-managed one the census records
UNRESOLVED must NOT be involved, because there is no Resources text to match. If that arm ever flips to
involved, the census started resolving managed policies and the definition's blind-spot sentence is
stale."""
import sys
import os
import tempfile

_here = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(_here, "lib", "opal_lgctfm.py")) and os.path.dirname(_here) != _here:
    _here = os.path.dirname(_here)
sys.path.insert(0, os.path.join(_here, "lib"))
import opal_lgctfm as m  # noqa: E402

A = "arn:aws:lambda:us-east-1:1:function:"
NODES = [
    {"id": "arn:rule/tok-49f-daily", "arn": "arn:rule/tok-49f-daily", "name": "tok-49f-daily", "t": "EVENT_RULE", "d": "DECLARED"},
    {"id": A + "plain-x", "arn": A + "plain-x", "name": "plain-x", "t": "LAMBDA", "d": "DECLARED"},
    {"id": A + "plain-y", "arn": A + "plain-y", "name": "plain-y", "t": "LAMBDA", "d": "DECLARED"},
    {"id": A + "plain-z", "arn": A + "plain-z", "name": "plain-z", "t": "LAMBDA", "d": "DECLARED"},
    {"id": A + "plain-m", "arn": A + "plain-m", "name": "plain-m", "t": "LAMBDA", "d": "DECLARED"},
    {"id": "arn:role/granting-role", "arn": "arn:role/granting-role", "name": "granting-role", "t": "IAM_ROLE", "d": "DECLARED"},
    {"id": "arn:role/other-role", "arn": "arn:role/other-role", "name": "other-role", "t": "IAM_ROLE", "d": "DECLARED"},
    {"id": "arn:role/managed-only-role", "arn": "arn:role/managed-only-role", "name": "managed-only-role", "t": "IAM_ROLE", "d": "DECLARED"},
    {"id": "arn:lg/x", "arn": "arn:lg/x", "name": "/aws/lambda/tok-49f-fn", "t": "LOG_GROUP", "d": "DECLARED"},
]
EDGES = [
    {"a": "arn:rule/tok-49f-daily", "e": "TRIGGERS", "b": A + "plain-x"},
    {"a": A + "plain-y", "e": "ASSUMES", "b": "arn:role/granting-role"},
    {"a": A + "plain-z", "e": "ASSUMES", "b": "arn:role/other-role"},
    {"a": A + "plain-m", "e": "ASSUMES", "b": "arn:role/managed-only-role"},
]
# the LIVE IAM census's own shape (comp_iam_census.build_census): inline documents expanded into
# {effect, actions, resources, source}; an attached-managed policy RECORDED as UNRESOLVED with no
# resources. `granting-role` names the subject in an inline Allow; `managed-only-role` names it only
# inside a statement the census could not resolve, so it carries no Resources text at all.
CENSUS = {"_meta": {"generated_utc": "2026-09-19T00:00:00Z"}, "roles": [
    {"role_name": "granting-role", "arn": "arn:role/granting-role", "statements": [
        {"effect": "allow", "actions": ["s3:GetObject"],
         "resources": ["arn:aws:s3:::opal-data-49financial/*"], "source": "inline:grant"}]},
    {"role_name": "other-role", "arn": "arn:role/other-role", "statements": [
        {"effect": "allow", "actions": ["s3:GetObject"],
         "resources": ["arn:aws:s3:::opal-data-cottonwood/*"], "source": "inline:other"}]},
    {"role_name": "deny-role", "arn": "arn:role/deny-role", "statements": [
        {"effect": "deny", "actions": ["s3:*"],
         "resources": ["arn:aws:s3:::opal-data-49financial/*"], "source": "inline:deny"}]},
    {"role_name": "managed-only-role", "arn": "arn:role/managed-only-role", "statements": [
        {"effect": "unresolved", "actions": [], "resources": [],
         "source": "managed:arn:aws:iam::1:policy/49financial-read"}]},
]}


def run(edges):
    def kuzu_rows(q, limit=0, timeout=0):
        return (NODES if "RETURN n.node_id" in q else edges), "fixture", ""
    m.kuzu_rows = kuzu_rows

    def run_aws_walk(ids, budget=0, case_insensitive=False):
        if "49f" in ids:
            fl = [{"node_type": "EVENT_RULE", "name": "tok-49f-daily", "arn_or_path": "arn:rule/tok-49f-daily", "drift": "DECLARED", "src": "comp-find"},
                  {"node_type": "LOG_GROUP", "name": "/aws/lambda/tok-49f-fn", "arn_or_path": "arn:lg/x", "drift": "DECLARED", "src": "comp-find"}]
            return fl, {"hits": 2, "scanned": 7, "vintage": "fixture"}
        return [], {"hits": 0, "scanned": 7, "vintage": "fixture"}
    m.run_aws_walk = run_aws_walk
    # LT-e-6: the PLANE is injected, the MATCHER is not -- the real iam_grant_roles() parses this census.
    m.live_iam_plane = lambda out_dir, timeout=600: (CENSUS, {"fixture": "injected live IAM census"}, "")
    m.source_text_lambdas = lambda ident: ({}, 0, 0)
    m.live_rule_targets = lambda budget=0: ({}, "")
    return m.discover_involved("49financial", ["opal-data-49financial"], {"triggers": []},
                               tempfile.gettempdir())


d = run(EDGES)
inv = {d["nodes"][k]["name"]: sorted(v["legs"]) for k, v in d["involved"].items()}
exc = [d["nodes"][k]["name"] for k in d["excluded"]]
print("involved:", inv)
print("excluded:", exc)
ok1 = inv.get("plain-x") == ["trigger_target"]
ok2 = inv.get("plain-y") == ["iam_grant"]
ok3 = "plain-z" not in inv
ok4 = exc == ["/aws/lambda/tok-49f-fn"]
# LT-e-6's three new arms, all on the re-pointed leg's own parser
ok6 = "granting-role" in inv and inv.get("granting-role") == ["iam_grant"]
ok7 = "deny-role" not in inv           # a DENY naming the subject is not a grant
ok8 = "managed-only-role" not in inv and "plain-m" not in inv
d2 = run([e for e in EDGES if e["e"] != "TRIGGERS"])
inv2 = {d2["nodes"][k]["name"] for k in d2["involved"]}
ok5 = "plain-x" not in inv2
# MUTANT on the re-point: a census whose subject-naming Allow is the WRONG firm must reach nobody
import copy  # noqa: E402
_mut = copy.deepcopy(CENSUS)
_mut["roles"][0]["statements"][0]["resources"] = ["arn:aws:s3:::opal-data-cottonwood/*"]
_saved, CENSUS = CENSUS, _mut
d3 = run(EDGES)
CENSUS = _saved
inv3 = {d3["nodes"][k]["name"] for k in d3["involved"]}
ok9 = "granting-role" not in inv3 and "plain-y" not in inv3
print("POSITIVE trigger-only Lambda rowed-as-involved: %s" % ok1)
print("POSITIVE grant-only Lambda involved: %s" % ok2)
print("NEGATIVE unlinked Lambda not involved: %s" % ok3)
print("EXCLUSION log sink excluded: %s" % ok4)
print("MUTANT trigger edge removed -> trigger-only Lambda drops out: %s" % ok5)
print("POSITIVE live-census Allow naming the subject -> role involved: %s" % ok6)
print("NEGATIVE a DENY naming the subject is not a grant: %s" % ok7)
print("BLIND SPOT attached-managed UNRESOLVED statement reaches nobody: %s" % ok8)
print("MUTANT census Allow re-pointed at another firm -> grant leg reaches nobody: %s" % ok9)
print("CONTROL: %s" % ("ALL-ARMS-HOLD" if all([ok1, ok2, ok3, ok4, ok5, ok6, ok7, ok8, ok9])
                       else "AN-ARM-FAILED"))
