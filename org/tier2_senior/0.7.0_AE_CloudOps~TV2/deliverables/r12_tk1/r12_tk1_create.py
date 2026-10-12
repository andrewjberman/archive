"""TCKT_VNEXT R12-tk-1 (TO-APPLY-R12-tk1): ONE create of a test ticket in tenant cottonwood as svc-commentary.

Token: read from the secret into memory, sent as a Bearer header only, never printed or written.
Exactly one POST, no retry. Output is filtered: no response body is printed raw (it carries routing addresses).
Usage: python r12_tk1_create.py --dry   (builds and prints the body, no network, no secret read)
       python r12_tk1_create.py         (the one write, then the read-back, then the result file)
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

AWS = os.path.abspath(".tools/aws.cmd")
HOST = "https://opalinvest.dev"
ROUTE = "/api/scoped/tickets"
SECRET = "opal/ticketing/svc-commentary"
OUT = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r12_tk1/R12_TEST_TICKET_20261012.json"
ADDR = re.compile(r"[\w.+-]+@[\w-]+(\.[\w-]+)+")

PRE_READ = {
    "earlier_ticket": {"ticket_id": "TCK-20261009-a1052909", "status": "open", "ticket_type": "analysis_request",
                       "created_by": "svc-commentary", "firm": "cottonwood"},
    "ticket_function": {"name": "opal-ticket-api", "COMMENTARY_ALLOWED_FIRMS": "49financial,cottonwood,inflection",
                        "CodeSha256": "4sDK8P5mtgodi1IkSfaFQZi1YgmJq6URLeypEcaULu8=",
                        "LastModified": "2026-10-12T01:50:30.000+0000"},
}


def body():
    label = "TEST r12-tk1 synthetic portfolio label"
    return {
        "ticket_type": "analysis_request",
        "title": "[TEST TCKT_VNEXT R12] synthetic ticket for the NFRA_TRNSPT TR-dp-24 pair",
        "source": "commentary:r12-tk-1",
        "answers": {"advisor": "Synthetic Advisor", "firm": "cottonwood", "report_type": "Overview",
                    "add_commentary": True},
        "attachment": {"upload_id": "test-r12-tk1-20261012",
                       "input_id": "portfolio_" + hashlib.sha256(label.encode("ascii")).hexdigest()},
    }


def aws(*args):
    return subprocess.run([AWS, *args], capture_output=True, text=True, timeout=120)


def clean(text):
    return ADDR.sub("<address>", text)


def main():
    b = body()
    assert "draft_commentary" not in b and "report_request_id" not in b
    if "--dry" in sys.argv:
        print(json.dumps(b, indent=2))
        return 0
    r = aws("secretsmanager", "get-secret-value", "--secret-id", SECRET, "--region", "us-east-1",
            "--query", "SecretString", "--output", "text")
    if r.returncode != 0:
        print("STOP secret read failed rc=%d: %s" % (r.returncode, clean(r.stderr)[:300]))
        return 2
    token = json.loads(r.stdout)["token"]
    req = urllib.request.Request(HOST + ROUTE, data=json.dumps(b).encode("utf-8"), method="POST",
                                 headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
    del token
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            status, text = resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        status, text = e.code, e.read().decode("utf-8", "replace")
    except Exception as e:  # timeout etc.: the write may or may not have landed; do NOT retry
        print("STOP no response (%s); not retried. The write state is UNKNOWN." % type(e).__name__)
        return 3
    if not 200 <= status < 300:
        print("STOP non-2xx status=%d response=%s" % (status, clean(text)[:600]))
        return 1
    tid = json.loads(text)["ticket"]["ticket_id"]
    print("POST status=%d ticket_id=%s" % (status, tid))
    g = aws("dynamodb", "get-item", "--table-name", "opal-tickets", "--key",
            json.dumps({"ticket_id": {"S": tid}}), "--region", "us-east-1", "--output", "json")
    item = json.loads(g.stdout)["Item"]
    rb = {"requester_firm": item["requester"]["M"]["firm"]["S"], "ticket_type": item["ticket_type"]["S"],
          "status": item["status"]["S"], "created_by": item["created_by"]["S"],
          "title_first_22": item["title"]["S"][:22],
          "has_draft_commentary": "draft_commentary" in item, "has_report_ref": "report_ref" in item}
    print("READBACK " + json.dumps(rb))
    doc = {"ticket_id": tid, "http_status": status, "write_set": ["ticket:" + tid], "deleted": False,
           "token_printed": False, "claim": "measured", "pre_read": PRE_READ, "read_back": rb,
           "body_keys_sent": sorted(b), "answers_keys_sent": sorted(b["answers"])}
    raw = json.dumps(doc, indent=2)
    assert "@" not in raw
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(raw + "\n")
    print("WROTE " + OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
