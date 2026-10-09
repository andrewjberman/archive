"""Read-only: invoke the live opal-amgt-scoped-api /thesis for a key; print the served dossier description and sentence counts. usage: read_served.py KEY..."""
import json
import sys
import boto3
lam = boto3.client("lambda", region_name="us-east-1")
for key in sys.argv[1:]:
    ev = {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
    r = json.loads(lam.invoke(FunctionName="opal-amgt-scoped-api", Payload=json.dumps(ev).encode())["Payload"].read())
    b = json.loads(r.get("body") or "{}")
    cds = [x for x in (b.get("dossier_sections") or []) if x.get("field") == "company_description"]
    cd = cds[0] if cds else {}
    txt = cd.get("text") or ""
    secs = b.get("drafted_sections") or []
    desc = [s for s in secs if s.get("section_id") == "company_description"]
    nd = len(desc[0].get("sentences") or []) if desc else -1
    out = sum(len(s.get("sentences") or []) for s in secs if s.get("section_id") != "company_description")
    print("%s status %s | dossier_sections.company_description status=%s len=%d starts=%r | description_sentences %d | outside_company_description %d" % (
        key, r.get("statusCode"), cd.get("status"), len(txt), txt[:60], nd, out))
