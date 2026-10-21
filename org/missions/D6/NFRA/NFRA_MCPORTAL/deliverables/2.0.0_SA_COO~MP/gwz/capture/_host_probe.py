"""Host-side, read-only probe (runs on the gateway host with its own venv, from /opt/opal-gateway): computes the gateway's /api/admin/gateway/breakdown
body in process (the handler's own _compute, which reads the catalog and scans the grant store with the host role; it writes nothing) and prints ONE
scrubbed line `CAPTURE=<json>`: per channel, and for each SEGMENTED bucket per (vendor, firm) segment, per tool, the indexes the page's rule shows under
that segment (index_pairs whose (vendor, firm) is the segment's), recomputed independently from the catalog with the handler's own _index_pair.
Scrub: no holders, no people, no principal ids, no tenant ids; an index name has every digit run of 5 or more replaced by '****' + its last 4."""
import hashlib
import json
import re
import sys

sys.path.insert(0, "/opt/opal-gateway")
import app.server  # noqa: F401,E402 -- registers the served integrations (row Z-S48)
from app import admin_gateway_breakdown as g  # noqa: E402


def mask(name):
    return re.sub(r"\d{5,}", lambda m: "****" + m.group(0)[-4:], name)


body = g._compute()
rows = g._catalog_index_rows()
out = {"gateway_read_at": body["read_at"], "kill_switch": body["kill_switch"], "grant_store_status": body["grant_store"]["status"],
       "catalog_md5_12": hashlib.md5(open("/opt/opal-gateway/app/refs/DATA_CATALOG.yaml", "rb").read()).hexdigest()[:12], "channels": []}
total_shown = total_foreign_shown = total_hidden = unresolved_shown = 0
for ch in body["channels"]:
    entry = {"id": ch["id"], "kind": ch["kind"], "tools": len(ch["tools"]), "segmented": "segments" in ch}
    if "segments" in ch:
        tools = {t["name"]: t for t in ch["tools"]}
        segs = []
        for seg in ch["segments"]:
            pair = (seg["vendor"], seg["firm"])
            srows = []
            for tn in seg["tools"]:
                t = tools[tn]
                ip = t.get("index_pairs")
                allidx = t["indexes"]
                shown = allidx if ip is None else [p["index"] for p in ip if (p["vendor"], p["firm"]) == pair]
                foreign = [i for i in shown if tuple(g._index_pair(i, rows)) != pair]
                total_shown += len(shown)
                total_foreign_shown += len(foreign)
                total_hidden += len(allidx) - len(shown)
                unresolved_shown += sum(1 for i in shown if g.UNRESOLVED in g._index_pair(i, rows))
                srows.append({"tool": tn, "index_pairs_present": ip is not None, "indexes_total": len(allidx),
                              "shown": [mask(i) for i in shown], "hidden_other_pair": len(allidx) - len(shown),
                              "shown_not_of_this_segment": len(foreign)})
            segs.append({"vendor": seg["vendor"], "firm": seg["firm"], "tools": srows})
        entry["segments"] = segs
    out["channels"].append(entry)
out["totals"] = {"indexes_shown_under_segments": total_shown, "shown_not_of_their_segment": total_foreign_shown,
                 "hidden_by_the_rule": total_hidden, "shown_with_an_unresolved_vendor_or_firm": unresolved_shown}
print("CAPTURE=" + json.dumps(out, separators=(",", ":"), sort_keys=True))
