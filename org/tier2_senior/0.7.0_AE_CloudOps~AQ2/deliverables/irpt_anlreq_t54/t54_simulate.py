"""IRPT_ANLREQ TO-APPLY-t54 step 2 (0.7.0_AE_CloudOps~AQ2): the simulate battery on the rendered inline policy S1 to S7.

  python t54_simulate.py <policy-after.json> <policy-before.json>

One `simulate-custom-policy` call per resource and per action (never two resources in one call). The jobs-table ARN is read from the S6 statement
of the policy itself. Prints the row, the expected verdict, the verdict read, and PASS or FAIL. Controls run as SEPARATE calls: a `*`/`*` policy
must ALLOW the S6-shaped update (the instrument is live), and the BEFORE policy (S1 to S5) must NOT allow it (S6 is what moves it).
S7's encryption context (kms:EncryptionContext:aws:dynamodb:tableName) cannot be simulated for a DynamoDB-mediated call: the proof's write is its evidence.
Exit 0 only if every row and both controls read as expected. Reads only; writes nothing.
"""
from __future__ import annotations

import json
import sys

REGION = "us-east-1"
SERVED = "49financial"
BASE = ["hop_failure", "tenant", "job"]


def ctx(keys, attrs, rv):
    return [
        {"ContextKeyName": "dynamodb:LeadingKeys", "ContextKeyValues": keys, "ContextKeyType": "stringList"},
        {"ContextKeyName": "dynamodb:Attributes", "ContextKeyValues": attrs, "ContextKeyType": "stringList"},
        {"ContextKeyName": "dynamodb:ReturnValues", "ContextKeyValues": [rv], "ContextKeyType": "string"},
    ]


def rows():
    ok = ctx([SERVED], BASE, "NONE")
    return [
        ("A1 UpdateItem hop_failure,tenant,job, served key, ReturnValues NONE", "dynamodb:UpdateItem", ok, "allowed"),
        ("A2 UpdateItem same, served key cottonwood", "dynamodb:UpdateItem", ctx(["cottonwood"], BASE, "NONE"), "allowed"),
        ("D1 PutItem", "dynamodb:PutItem", ok, "denied"),
        ("D2 DeleteItem", "dynamodb:DeleteItem", ok, "denied"),
        ("D3 GetItem", "dynamodb:GetItem", ok, "denied"),
        ("D4 Query", "dynamodb:Query", ok, "denied"),
        ("D5 Scan", "dynamodb:Scan", ok, "denied"),
        ("D6 UpdateItem naming another attribute (state)", "dynamodb:UpdateItem", ctx([SERVED], BASE + ["state"], "NONE"), "denied"),
        ("D7 UpdateItem on a leading key that is not a served firm", "dynamodb:UpdateItem", ctx(["notafirm"], BASE, "NONE"), "denied"),
        ("D8 UpdateItem with ReturnValues ALL_NEW", "dynamodb:UpdateItem", ctx([SERVED], BASE, "ALL_NEW"), "denied"),
    ]


def verdict(iam, doc, action, resource, entries):
    r = iam.simulate_custom_policy(PolicyInputList=[json.dumps(doc)], ActionNames=[action], ResourceArns=[resource], ContextEntries=entries)
    d = r["EvaluationResults"][0]["EvalDecision"]
    return "allowed" if d == "allowed" else "denied", d


def main(argv):
    import boto3
    after = json.load(open(argv[0], encoding="utf-8"))
    before = json.load(open(argv[1], encoding="utf-8"))
    iam = boto3.client("iam", region_name=REGION)
    s6 = [s for s in after["Statement"] if s["Sid"].startswith("S6")][0]
    table = s6["Resource"][0]
    bad = 0
    print("policy statements: %s" % [s["Sid"][:2] for s in after["Statement"]])
    for name, action, entries, want in rows():
        got, raw = verdict(iam, after, action, table, entries)
        res = "PASS" if got == want else "FAIL"
        bad += res == "FAIL"
        print("%s | expected %s | read %s | %s" % (name, want, raw, res))
    star = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": "*", "Resource": "*"}]}
    got, raw = verdict(iam, star, "dynamodb:UpdateItem", table, ctx([SERVED], BASE, "NONE"))
    print("CONTROL1 *:* policy, A1 shape | expected allowed | read %s | %s" % (raw, "PASS" if got == "allowed" else "FAIL"))
    bad += got != "allowed"
    got, raw = verdict(iam, before, "dynamodb:UpdateItem", table, ctx([SERVED], BASE, "NONE"))
    print("CONTROL2 BEFORE policy S1 to S5, A1 shape | expected denied | read %s | %s" % (raw, "PASS" if got == "denied" else "FAIL"))
    bad += got != "denied"
    print("S7 kms:EncryptionContext:aws:dynamodb:tableName CANNOT be simulated for a DynamoDB-mediated call; the proof's write is its evidence.")
    print("BATTERY %s (%d failing)" % ("OK" if not bad else "FAIL", bad))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
