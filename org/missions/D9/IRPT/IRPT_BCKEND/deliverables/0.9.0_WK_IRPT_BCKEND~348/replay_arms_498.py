"""IB-pr-498 replay arms (offline; prints only; reads zip bytes and one fixture file; no AWS, no invoke).

Usage: python -I replay_arms_498.py <valid_fixture.json> <built_zip> <live_zip>
Each arm: the fixture's `instance` document, validated (jsonschema Draft 2020-12) against the zip's packaged
contracts/HoldingsSnapshot.schema.json. Verdict valid when no error, refused otherwise.
"""
import copy
import json
import sys
import zipfile

from jsonschema import Draft202012Validator

FIX, BUILT, LIVE = sys.argv[1], sys.argv[2], sys.argv[3]
inst = json.load(open(FIX, encoding="utf-8"))["instance"]
assert inst["nodes"] and "account_id" in inst["nodes"][0], "fixture node carries no account_id"


def schema_of(zp):
    return json.loads(zipfile.ZipFile(zp).read("contracts/HoldingsSnapshot.schema.json").decode("utf-8"))


def arms():
    a = copy.deepcopy(inst)
    b = copy.deepcopy(inst)
    del b["nodes"][0]["account_id"]
    c = copy.deepcopy(inst)
    c["nodes"][0]["unknown_member"] = "x"
    return [("node_with_account_id", a), ("node_without_account_id", b), ("node_with_unknown_member", c)]


def verdicts(schema):
    v = Draft202012Validator(schema)
    out = []
    for name, doc in arms():
        errs = list(v.iter_errors(doc))
        out.append((name, "valid" if not errs else "refused", len(errs)))
    return out


Draft202012Validator.check_schema(schema_of(BUILT))
for label, zp in (("BUILT", BUILT), ("LIVE", LIVE)):
    for name, verdict, n in verdicts(schema_of(zp)):
        print("%s arm=%s verdict=%s errors=%d" % (label, name, verdict, n))
