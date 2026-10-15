"""TCKT_VNEXT round 18 -- R18-mt-4 / R18-tf-5: the ticket service release is LIVE and reads back as built.

Read-only AWS reads (us-east-1). Prints REL-OK <detail> or REL-BAD <reason>; exit 0/1.
It compares the live Lambda configuration, the API route table and the role policy with the builder record
(ATTACH_ADDRESS.json) and the release result file the applier writes, never with the applier's own claim alone.
"""
import json
import os
import subprocess
import sys

REC = "org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~43/ATTACH_ADDRESS.json"
RES = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r18_rel/R18_REL_RESULT.json"
FUNCTION = "opal-ticket-api"
ROLE = "opal-ticket-api-role"
API_ID = "7k3ed8px20"
ROUTES = ("POST /api/scoped/tickets/{ticketId}/meeting",
          "POST /api/scoped/tickets/attachment-upload",
          "GET /api/scoped/tickets/{ticketId}/attachment")
COORDINATOR = "jeanette@opalinvest.com"
SID = "TicketAttachmentsTradeForm"
FIRMS = ("49financial", "inflection", "cottonwood")
AWS = os.path.abspath(".tools/aws.cmd")


def aws(*args):
    out = subprocess.run([AWS] + list(args) + ["--region", "us-east-1", "--output", "json"],
                         capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise RuntimeError("aws %s rc=%d" % (" ".join(args[:2]), out.returncode))
    if not out.stdout.strip():
        raise RuntimeError("aws %s printed nothing" % " ".join(args[:2]))
    return json.loads(out.stdout)


def main():
    try:
        rec = json.load(open(REC, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("REL-BAD cannot read the builder record: %s" % e)
        return 1
    try:
        res = json.load(open(RES, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("REL-BAD cannot read the release result file: %s" % e)
        return 1
    for k in ("code_sha256_before", "code_sha256_after", "change_ledger", "pair"):
        if not res.get(k):
            print("REL-BAD the result file lacks %r" % k)
            return 1
    if res["code_sha256_before"] == res["code_sha256_after"]:
        print("REL-BAD the code hash did not change")
        return 1
    try:
        cfg = aws("lambda", "get-function-configuration", "--function-name", FUNCTION)
        env = (cfg.get("Environment") or {}).get("Variables") or {}
        if cfg.get("CodeSha256") != res["code_sha256_after"]:
            print("REL-BAD live CodeSha256 %s is not the recorded after-hash" % cfg.get("CodeSha256"))
            return 1
        if env.get("TICKET_ATTACH_BUCKET_TEMPLATE") != rec["bucket_template"] or env.get("TICKET_ATTACH_KEY_TEMPLATE") != rec["key_template"]:
            print("REL-BAD the two attachment environment variables differ from the builder record")
            return 1
        matrix = json.loads(env.get("ROUTING_MATRIX") or "{}")
        if (matrix.get("meeting_request") or {}).get("primary") != [COORDINATOR]:
            print("REL-BAD meeting_request routing primary is not exactly the coordinator")
            return 1
        keys = aws("apigatewayv2", "get-routes", "--api-id", API_ID, "--query", "Items[].RouteKey")
        for rk in ROUTES:
            if keys.count(rk) != 1:
                print("REL-BAD route %r appears %d times" % (rk, keys.count(rk)))
                return 1
        names = aws("iam", "list-role-policies", "--role-name", ROLE).get("PolicyNames", [])
        found = []
        for n in names:
            doc = aws("iam", "get-role-policy", "--role-name", ROLE, "--policy-name", n)["PolicyDocument"]
            stmts = doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]
            found += [s for s in stmts if s.get("Sid") == SID]
        if len(found) != 1:
            print("REL-BAD statement %s appears %d times" % (SID, len(found)))
            return 1
        st = found[0]
        acts = st["Action"] if isinstance(st["Action"], list) else [st["Action"]]
        if sorted(acts) != ["s3:GetObject", "s3:PutObject"]:
            print("REL-BAD the statement's actions are %r" % (acts,))
            return 1
        want = sorted("arn:aws:s3:::%s/%s*" % (rec["buckets"][f], rec["key_template"].format(firm=f)) for f in FIRMS)
        have = st["Resource"] if isinstance(st["Resource"], list) else [st["Resource"]]
        if sorted(have) != want:
            print("REL-BAD the statement's resources differ from the three firm prefixes")
            return 1
    except (RuntimeError, ValueError, KeyError, OSError, subprocess.SubprocessError) as e:
        print("REL-BAD live read failed: %s" % e)
        return 1
    print("REL-OK code %s, 2 env, 3 routes once each, coordinator routing, %s on 3 prefixes" % (res["code_sha256_after"][:12], SID))
    return 0


if __name__ == "__main__":
    sys.exit(main())
