import collections
import json
import sys
sys.path.insert(0, ".")
from lib.research.api import scoped_amgt
from lib.research.coverage import covered_universe
PREFIX = "/api/scoped/amgt"
def call(path):
    r = scoped_amgt.handler({"rawPath": path, "requestContext": {"http": {"method": "GET"}},
                             "headers": {"x-firm-id": "opal"}, "queryStringParameters": None})
    try:
        return r.get("statusCode"), json.loads(r.get("body") or "null")
    except ValueError:
        return r.get("statusCode"), None
def cause(reason):
    r = reason.lower()
    if r.startswith("we hold no stored company data"):
        return "no stored company data for the name"
    if r.startswith("bloomberg returned no value"):
        return "Bloomberg answered the question and returned nothing"
    if "not in the latest stored pull" in r:
        return "figure not in the latest stored pull"
    return "other: " + reason
st, fr = call(PREFIX + "/freshness")
unc = sorted({r["security_key"] for r in fr["rows"] if isinstance(r, dict) and r.get("covered") is False and r.get("security_key")})
cov = sorted(covered_universe.covered_security_keys())
names, tot = [], collections.Counter()
causes = collections.Counter()
for group, keys in (("covered", cov), ("uncovered", unc)):
    for key in keys:
        st, ov = call("%s/security/%s/overlay" % (PREFIX, key))
        allfigs = (ov or {}).get("header_figures") or [] if st == 200 else []
        figs = []
        for label, mn, _d in scoped_amgt.HEADER_SEVEN:
            ents = [f for f in allfigs if f.get("mnemonic") in mn]
            if not ents:
                continue
            hv = [f for f in ents if f.get("value") is not None]
            figs.append(hv[0] if hv else ents[0])
        val = [f.get("mnemonic") for f in figs if f.get("value") is not None]
        rea = [{"mnemonic": f.get("mnemonic"), "reason": f.get("reason"), "cause": cause(str(f.get("reason")))}
               for f in figs if f.get("value") is None and str(f.get("reason") or "").strip()]
        bare = [f.get("mnemonic") for f in figs if f.get("value") is None and not str(f.get("reason") or "").strip()]
        names.append({"security_key": key, "group": group, "status": st, "entries": len(figs),
                      "with_value": len(val), "null_with_reason": len(rea), "null_no_reason": len(bare),
                      "reasons": rea})
        tot[group + "_names"] += 1
        tot[group + "_with_value"] += len(val)
        tot[group + "_null_with_reason"] += len(rea)
        tot[group + "_null_no_reason"] += len(bare)
        if st != 200:
            tot[group + "_non200"] += 1
        for r in rea:
            causes[(group, r["cause"])] += 1
doc = {"cell": "AMGT-av-1", "population": {"covered": len(cov), "uncovered_with_key_on_freshness": len(unc)},
       "totals": dict(tot), "causes": [{"group": g, "cause": c, "count": n} for (g, c), n in sorted(causes.items())],
       "names": names}
out = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~237/HEADER_CENSUS"
open(out + ".json", "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1, sort_keys=True) + "\n")
L = ["# HEADER_CENSUS -- AMGT-av-1 (worker 0.9.0_WK_AMGT_RESAPP~237)", "",
     "Read locally through `scoped_amgt.handler` `/security/<key>/overlay` `header_figures` over the 95 covered names and the %d uncovered names with a key on `/freshness`." % len(unc), "",
     "## Totals", "", "| group | names | non-200 | figures with a value | null with a plain reason | null with NO reason |", "|---|---|---|---|---|---|"]
for g in ("covered", "uncovered"):
    L.append("| %s | %d | %d | %d | %d | %d |" % (g, tot[g + "_names"], tot[g + "_non200"], tot[g + "_with_value"], tot[g + "_null_with_reason"], tot[g + "_null_no_reason"]))
L += ["", "## Reason causes", "", "| group | cause | count |", "|---|---|---|"]
for (g, c), n in sorted(causes.items()):
    L.append("| %s | %s | %d |" % (g, c, n))
L += ["", "## Per name", "", "| security_key | group | status | with value | null with reason | null no reason | causes |", "|---|---|---|---|---|---|---|"]
for n in names:
    cs = "; ".join(sorted({r["cause"] for r in n["reasons"]}))
    L.append("| %s | %s | %s | %d | %d | %d | %s |" % (n["security_key"], n["group"], n["status"], n["with_value"], n["null_with_reason"], n["null_no_reason"], cs))
open(out + ".md", "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print(json.dumps(doc["totals"], sort_keys=True))
print(json.dumps(doc["causes"]))
