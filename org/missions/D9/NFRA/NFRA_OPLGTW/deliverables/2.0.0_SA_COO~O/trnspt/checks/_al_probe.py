"""Unauthenticated probes of the public gateway URL for OG-al-1, WITHOUT following redirects: does a request on each
/hx/ prefix reach the gateway, or is it sent to the Entra sign-in? Prints one JSON object. No bearer is sent."""
import json
import urllib.error
import urllib.request

BASE = "https://mcp.opalinvest.dev"
PROBES = {"hx_mail": "/hx/mail/messages/AL-PROBE", "hx_transcripts": "/hx/transcripts/meetings/AL-PROBE/transcripts",
          "control": "/hxal-control-not-a-route"}


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
