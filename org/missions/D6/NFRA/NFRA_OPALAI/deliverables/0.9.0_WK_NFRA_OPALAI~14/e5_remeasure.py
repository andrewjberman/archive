"""OA-e-5 measure-only: reads through the teams watch's own read path. No cursor writes, no message text, no token persisted."""
import sys
import os
import json
import time
import datetime
import importlib.util
import urllib.error
sys.argv = [sys.argv[0], "--server", "opal-gateway-bbg"]
ROOT = os.path.abspath(__file__)
while not os.path.isdir(os.path.join(ROOT, '.claude', 'skills')):
    ROOT = os.path.dirname(ROOT)
spec = importlib.util.spec_from_file_location("teams_watch", os.path.join(ROOT, ".claude", "skills", "teams-assist", "teams-watch.py"))
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)

def exp_ms(pin="opal-gateway-bbg"):
    d = json.load(open(w.CREDS, encoding="utf-8"))
    r = [v for v in d.get("mcpOAuth", {}).values() if pin in str(v.get("serverName", "")).lower()]
    print("records:", sorted(str(v.get("serverName")) for v in r))
    return max([v.get("expiresAt", 0) for v in r] or [0])

now = datetime.datetime.now(datetime.timezone.utc)
tok = w.read_token()
ident = w.self_id(tok) if tok else None
print("token live:", bool(tok), "identity:", ident)
out = dict(measured_at=now.strftime("%Y-%m-%dT%H:%M:%SZ"), served_commit="fe94911257", gap_b_in_served=True,
           identity=ident or "", chats=0, reads_attempted=0, reads_ok=0, reads_failed=0, reads_token_expired=0,
           failure_signatures={})
def sig(e):
    if isinstance(e, urllib.error.HTTPError):
        return f"HTTPError {e.code}"
    return type(e).__name__
if tok:
    since = (now - datetime.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        res = w.poll(tok, since)
    except Exception as e:
        res = None
        print("poll failed:", sig(e))
    ids = []
    for m in (res or {}).get("new_messages", []):
        c = m.get("chat_id")
        if c and c not in ids:
            ids.append(c)
    print("touched chats:", len(ids))
    ids = ids[:10]
    out["chats"] = len(ids)
    for c in ids:
        out["reads_attempted"] += 1
        if exp_ms() / 1000 <= time.time():
            out["reads_token_expired"] += 1
            continue
        try:
            pg = w.read_chat(tok, c)
        except Exception as e:
            out["reads_failed"] += 1
            s = sig(e)
            out["failure_signatures"][s] = out["failure_signatures"].get(s, 0) + 1
            continue
        if isinstance(pg, dict) and "value" in pg:
            out["reads_ok"] += 1
        else:
            s = "ErrorShapedPage keys=" + (",".join(sorted(str(k) for k in pg)) if isinstance(pg, dict) else "None")
            if isinstance(pg, dict):
                for k in ("code", "status", "error"):
                    if isinstance(pg.get(k), (str, int)) and len(str(pg[k])) < 40:
                        s += f" {k}={pg[k]}"
            out["reads_failed"] += 1
            out["failure_signatures"][s] = out["failure_signatures"].get(s, 0) + 1
ok, fl = out["reads_ok"], out["reads_failed"]
out["verdict"] = "INCONCLUSIVE" if ok + fl == 0 else ("NOT-CLEARED" if fl else "CLEARED")
if out["verdict"] == "CLEARED":
    out["next"] = "Reads succeed on a live token; remaining work is blocker (1), the token refresh the watch should own (PRD C8)."
elif out["verdict"] == "NOT-CLEARED":
    out["next"] = "Dominant failure signature: " + max(out["failure_signatures"].items(), key=lambda kv: kv[1])[0]
else:
    out["next"] = "No read ran on a live token; re-run after the issuer warms the token."
keys = ["measured_at","served_commit","gap_b_in_served","identity","chats","reads_attempted","reads_ok","reads_failed","reads_token_expired","failure_signatures","verdict","next"]
json.dump({k: out[k] for k in keys}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "E5_TEAMS_WATCH_REMEASURE.json"), "w"), indent=2)
print(json.dumps({k: out[k] for k in keys}, indent=2))
