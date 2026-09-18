"""Driven control for LT-e-5's legs: an INJECTED graph (no AWS) where a Lambda carries NO token and is
reached ONLY by its trigger (X) or ONLY by its role's grant (Y); a third Lambda (Z) is reached by nothing.
Expect X and Y involved with the named leg, Z not involved, and the /aws/lambda log group excluded.
Then a MUTANT: remove the trigger edge -> X must drop out."""
import sys
import os

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
    {"id": "arn:role/granting-role", "arn": "arn:role/granting-role", "name": "granting-role", "t": "IAM_ROLE", "d": "DECLARED"},
    {"id": "arn:role/other-role", "arn": "arn:role/other-role", "name": "other-role", "t": "IAM_ROLE", "d": "DECLARED"},
    {"id": "arn:lg/x", "arn": "arn:lg/x", "name": "/aws/lambda/tok-49f-fn", "t": "LOG_GROUP", "d": "DECLARED"},
]
EDGES = [
    {"a": "arn:rule/tok-49f-daily", "e": "TRIGGERS", "b": A + "plain-x"},
    {"a": A + "plain-y", "e": "ASSUMES", "b": "arn:role/granting-role"},
    {"a": A + "plain-z", "e": "ASSUMES", "b": "arn:role/other-role"},
]


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
    m.iam_grant_roles = lambda ident: ({"granting-role": ["arn:aws:s3:::opal-data-49financial/*"]}, 2, "")
    m.source_text_lambdas = lambda ident: ({}, 0, 0)
    m.live_rule_targets = lambda budget=0: ({}, "")
    return m.discover_involved("49financial", ["opal-data-49financial"], {"triggers": []})


d = run(EDGES)
inv = {d["nodes"][k]["name"]: sorted(v["legs"]) for k, v in d["involved"].items()}
exc = [d["nodes"][k]["name"] for k in d["excluded"]]
print("involved:", inv)
print("excluded:", exc)
ok1 = inv.get("plain-x") == ["trigger_target"]
ok2 = inv.get("plain-y") == ["iam_grant"]
ok3 = "plain-z" not in inv
ok4 = exc == ["/aws/lambda/tok-49f-fn"]
d2 = run([e for e in EDGES if e["e"] != "TRIGGERS"])
inv2 = {d2["nodes"][k]["name"] for k in d2["involved"]}
ok5 = "plain-x" not in inv2
print("POSITIVE trigger-only Lambda rowed-as-involved: %s" % ok1)
print("POSITIVE grant-only Lambda involved: %s" % ok2)
print("NEGATIVE unlinked Lambda not involved: %s" % ok3)
print("EXCLUSION log sink excluded: %s" % ok4)
print("MUTANT trigger edge removed -> trigger-only Lambda drops out: %s" % ok5)
print("CONTROL: %s" % ("ALL-ARMS-HOLD" if all([ok1, ok2, ok3, ok4, ok5]) else "AN-ARM-FAILED"))
