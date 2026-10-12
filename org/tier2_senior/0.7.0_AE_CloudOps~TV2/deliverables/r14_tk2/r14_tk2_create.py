"""TCKT_VNEXT R14-tk-2 (TO-APPLY-R14-tk2): ONE create of a test ticket in tenant 49financial as svc-commentary.

Step 1 (pre-read) runs live and is printed; the write proceeds only if the control reads as the order states.
Token: read from the secret into memory, sent as a Bearer header only, never printed or written.
Exactly one POST, no retry. No response body is printed raw (it carries routing addresses).
Usage: python r14_tk2_create.py --dry   (pre-read + body, no secret read, no write)
       python r14_tk2_create.py         (pre-read, the one write, the read-back, the result file)
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
FIRM = "49financial"
OUT = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r14_tk2/R14_TEST_TICKET_20261012.json"
ADDR = re.compile(r"[\w.+-]+@[\w-]+(\.[\w-]+)+")


def body():
    label = "TEST r14-tk2 synthetic portfolio label"
    return {
        "ticket_type": "analysis_request",
        "title": "[TEST TCKT_VNEXT R14] synthetic ticket for the NFRA_TRNSPT TR-dp-24 pair",
        "source": "commentary:r14-tk-2",
        "answers": {"advisor": "Synthetic Advisor", "firm": FIRM, "report_type": "Overview",
                    "add_commentary": True},
        "attachment": {"upload_id": "test-r14-tk2-20261012",
                       "input_id": "portfolio_" + hashlib.sha256(label.encode("ascii")).hexdigest()},
    }


def aws(*args):
    return subprocess.run([AWS, *args], capture_output=True, text=True, timeout=120)


def clean(text):
    return ADDR.sub("<address>", text)


def pre_read():
    g = aws("dynamodb", "get-item", "--table-name", "opal-tickets", "--key",
            json.dumps({"ticket_id": {"S": "TCK-20261009-a1052909"}}), "--region", "us-east-1", "--output", "json")
    it = json.loads(g.stdout)["Item"]
    earlier = {"ticket_id": it["ticket_id"]["S"], "status": it["status"]["S"], "ticket_type": it["ticket_type"]["S"],
               "created_by": it["created_by"]["S"], "firm": it["requester"]["M"]["firm"]["S"]}
    c = aws("lambda", "get-function-configuration", "--function-name", "opal-ticket-api", "--region", "us-east-1",
            "--query", "{f:Environment.Variables.COMMENTARY_ALLOWED_FIRMS,sha:CodeSha256,lm:LastModified}",
            "--output", "json")
    cfg = json.loads(c.stdout)
    fn = {"name": "opal-ticket-api", "COMMENTARY_ALLOWED_FIRMS": cfg["f"], "CodeSha256": cfg["sha"],
          "LastModified": cfg["lm"]}
    return {"earlier_ticket": earlier, "ticket_function": fn}


def main():
    b = body()
    assert "draft_commentary" not in b and "report_request_id" not in b
    pre = pre_read()
    print("PREREAD " + json.dumps(pre))
    if pre["earlier_ticket"]["status"] != "open" or FIRM not in pre["ticket_function"]["COMMENTARY_ALLOWED_FIRMS"].split(","):
        print("STOP pre-read control did not read as the order states; nothing written")
        return 2
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
           "token_printed": False, "claim": "measured", "pre_read": pre, "read_back": rb,
           "body_keys_sent": sorted(b), "answers_keys_sent": sorted(b["answers"])}
    raw = json.dumps(doc, indent=2)
    assert "@" not in raw
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(raw + "\n")
    print("WROTE " + OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
