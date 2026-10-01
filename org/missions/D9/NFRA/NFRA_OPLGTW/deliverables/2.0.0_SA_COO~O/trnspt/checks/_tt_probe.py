"""Unauthenticated probes for OG-tt-1, WITHOUT following redirects. No bearer is sent. Prints one JSON object."""
import json
import urllib.error
import urllib.request

BASE = "https://mcp.opalinvest.dev"
PROBES = {"tax": "/ms/taxsma-workbook", "ms_unknown": "/ms/ttprobe-not-a-route", "root": "/", "ms_sites": "/ms/sites"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


opener = urllib.request.build_opener(NoRedirect)
out = {}
for k, path in PROBES.items():
    try:
        r = opener.open(urllib.request.Request(BASE + path), timeout=15)
        st, loc = r.status, r.headers.get("Location", "")
    except urllib.error.HTTPError as e:
        st, loc = e.code, e.headers.get("Location", "") if e.headers else ""
    except Exception as e:  # noqa: BLE001 -- a transport failure is recorded, never read as a pass
        st, loc = "ERR:%s" % type(e).__name__, ""
    out[k] = {"status": st, "to_signin": isinstance(st, int) and 300 <= st < 400 and "login.microsoftonline.com" in loc}
print(json.dumps(out))
