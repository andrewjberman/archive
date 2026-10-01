"""The six negative arms of OG-rl-1 against the served gateway. Never prints a bearer, a body or a value.

usage: python _arms.py <route_names.json>
ROUTE_NAMES.json (written by OG-hr-1 / OG-hr-2) carries per route key `prefix`, `secret_name` and `probes`:
  transcripts.probes.transcripts_of_meeting  e.g. "{prefix}/meetings/{meeting_id}/transcripts"
  mail.probes.message                        e.g. "{prefix}/messages/{message_id}"
  mail.probes.attachment                     e.g. "{prefix}/messages/{message_id}/attachments/{attachment_id}"
Prints one line per arm, then: ARMS <n> of 6 refused-or-metadata.
"""
import json
import os
import sys
import urllib.error
import urllib.request

import boto3

BASE = "https://mcp.opalinvest.dev"
REFUSED = (401, 403)
BYTE_KEYS = {"content", "contentBytes", "bytes_b64", "value", "data", "body_bytes"}

doc = json.load(open(sys.argv[1], encoding="utf-8"))
sm = boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION", "us-east-1"))
bearer = {k: sm.get_secret_value(SecretId=doc[k]["secret_name"])["SecretString"].strip() for k in ("transcripts", "mail")}


def get(path, who):
    req = urllib.request.Request(BASE + path, headers={"Authorization": "Bearer " + bearer[who]})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        return e.code, {}


def path(key, probe, **ids):
    return doc[key]["probes"][probe].format(prefix=doc[key]["prefix"], **ids)


arms = []
st, _ = get(path("transcripts", "transcripts_of_meeting", meeting_id="TRNSPT-NEG-ARM-NOT-ON-ALLOWLIST"), "mail")
arms.append(("mail bearer on the transcripts prefix", st in REFUSED, st))
st, _ = get(path("mail", "message", message_id="TRNSPT-NEG-ARM"), "transcripts")
arms.append(("transcripts bearer on the mail prefix", st in REFUSED, st))
st, _ = get(path("transcripts", "transcripts_of_meeting", meeting_id="TRNSPT-NEG-ARM-NOT-ON-ALLOWLIST"), "transcripts")
arms.append(("off-allowlist meeting, own bearer", st in REFUSED, st))
for label, env in (("off-table sender", "OG_RL_OFF_TABLE_MSG"), ("off-table sender in a table thread", "OG_RL_THREAD_MSG")):
    mid = os.environ.get(env)
    if not mid:
        arms.append((label + " (NOT RUN: %s unset)" % env, False, None))
        continue
    st, _ = get(path("mail", "message", message_id=mid), "mail")
    arms.append((label, st in REFUSED, st))
m, a = os.environ.get("OG_RL_NONPDF_MSG"), os.environ.get("OG_RL_NONPDF_ATT")
if m and a:
    st, body = get(path("mail", "attachment", message_id=m, attachment_id=a), "mail")
    leaked = sorted(BYTE_KEYS & set(body))
    arms.append(("non-PDF attachment metadata only (byte keys %s)" % (leaked or "none"), st == 200 and not leaked, st))
else:
    arms.append(("non-PDF attachment (NOT RUN: OG_RL_NONPDF_MSG/ATT unset)", False, None))

for label, ok, st in arms:
    print("arm %-58s status=%s %s" % (label, st, "OK" if ok else "FAIL"))
print("ARMS %d of %d refused-or-metadata" % (sum(1 for _l, ok, _s in arms if ok), len(arms)))
