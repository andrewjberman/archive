import json
from lib.research.api import scoped_amgt
ev = {"rawPath": "/api/scoped/amgt/security/ASML_NA_Equity/peers", "queryStringParameters": None,
      "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
r = scoped_amgt.handler(ev)
served = json.loads(r.get("body") or "{}")
ms = served.get("members") or []
measured = [m["ticker"] for m in ms if (m.get("identity") or {}).get("resolution") == "MEASURED"]
print("status=%s served_members=%d MEASURED=%d tickers=%s" % (r.get("statusCode"), len(ms), len(measured), measured))
