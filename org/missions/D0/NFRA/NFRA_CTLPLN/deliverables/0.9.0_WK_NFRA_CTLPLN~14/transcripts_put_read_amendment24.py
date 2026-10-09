"""Scratch: dell2 s3:PutObject on the transcripts prefixes, iam simulation only (read-only)."""
import sys
from pathlib import Path

import boto3

TESTS = Path(sys.argv[1])
sys.path.insert(0, str(TESTS))
import simulate_policy as sp  # noqa: E402

B = "arn:aws:s3:::opal-data-transcripts/"
PREFIXES = [
    ("TO-RUN-x9/b11 research fold", "teams/transcripts/silver/research_meeting/date=2026-10-08/x.parquet"),
    ("chat_assist archive", "teams/transcripts/bronze/chat_messages/date=2026-10-08/x.json"),
    ("chat_assist archive", "teams/transcripts/silver/chat_threads/date=2026-10-08/x.parquet"),
    ("chat_assist archive", "teams/transcripts/state/chat_assist/x.json"),
    ("pull.tf WriteAndReadTeamsTranscriptKeys", "teams/transcripts/bronze/transcripts/date=2026-10-08/x.json"),
    ("mail_pull.tf WriteAndReadMailTranscriptKeys", "outlook/transcripts/bronze/date=2026-10-08/x.json"),
]
iam = boto3.client("iam", region_name="us-east-1")
sets = sp.user_sets()
d2 = sets["dell2"]
refused = 0
n = 0
print("DELL2 effective set = group policies + bus + ssm as built (simulate-custom-policy), %d documents" % len(d2))
for label, key in PREFIXES:
    r = sp.eval_pair(iam, d2, "s3:PutObject", [B + key])
    dec = r[0]
    n += 1
    refused += dec != "allowed"
    print("PUT %-48s %-80s -> %s" % (label, "s3://opal-data-transcripts/" + key, dec))
print("CONTROLS")
for label, action, res in (("positive: dell2 PutObject on opal-data-assets (the ALLOWED list's own arm)", "s3:PutObject", "arn:aws:s3:::opal-data-assets/x"),
                           ("negative: dell2 DeleteObject on the transcripts bucket (DenyS3DeletesOnProductionData)", "s3:DeleteObject", B + "teams/transcripts/silver/research_meeting/x"),
                           ("negative: dell2 PutObject on a bucket outside opal-*", "s3:PutObject", "arn:aws:s3:::not-an-opal-bucket/x")):
    dec, per = sp.eval_pair(iam, d2, action, [res])
    print("%-95s -> %s %s" % (label, dec, sorted({s for _d, sids in per.values() for s in sids})))
print("LIVE principal (simulate-principal-policy, user as applied today)")
for label, key in PREFIXES[:1] + PREFIXES[-1:]:
    r = iam.simulate_principal_policy(PolicySourceArn="arn:aws:iam::313476888478:user/cloudops-dell2-agent-user", ActionNames=["s3:PutObject"], ResourceArns=[B + key])
    e = r["EvaluationResults"][0]
    print("LIVE PUT %-45s -> %s matched=%s" % (key, e["EvalDecision"], [m["SourcePolicyId"] for m in e.get("MatchedStatements", [])]))
print("TRANSCRIPT-PUT prefixes=%d dell_put_refused=%d" % (n, refused))
