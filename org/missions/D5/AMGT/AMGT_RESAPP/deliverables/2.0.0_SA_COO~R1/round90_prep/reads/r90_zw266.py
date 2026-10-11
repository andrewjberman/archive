import json
import re
import boto3
import sys
from lib.research.filings import analyze
s3 = boto3.client("s3", region_name="us-east-1")
NAMES = {"BABA_US_Equity": "000119312526231755", "PBR_US_Equity": "000129281426002168", "SAP_GY_Equity": "000110465926020058"}
def get(k):
    return json.loads(s3.get_object(Bucket="opal-data-harvest", Key=k)["Body"].read())
out = {}
for name, acc in NAMES.items():
    src = get("filings/v1/%s/%s.source.json" % (name, acc))
    ana = get("filings/v1/%s/%s.analysis.json" % (name, acc))
    ex = src["excerpt"]["text"]
    td = ana.get("thesis_driver") or {}
    print("=====", name, acc, "excerpt chars", len(ex), "| driver:", td.get("series"), "|", td.get("unit"), "| resolution", td.get("resolution"))
    print("  points", [(p["period"], p["value"], p.get("span")) for p in td.get("points", [])], "held", len(td.get("held_uncited", [])))
    rows = []
    for h in td.get("held_uncited", []):
        period, value, reason = str(h["period"]), h["value"], h["reason"]
        tok = analyze.locate_period_labels([period], ex)
        tok_near = {}
        # alternative surface forms of the same period
        digits = re.sub(r"\D", "", period)
        for alt in {digits, "FY" + digits, "FY " + digits, "March 31, " + digits, "December 31, " + digits}:
            if alt and alt != period:
                m = re.search(r"(?<!\d)" + re.escape(alt) + r"(?!\d)", ex)
                if m:
                    tok_near[alt] = m.start()
        # whole-number occurrences of the value anywhere in the excerpt
        occ = []
        for m in analyze._WHOLE_NUMBER_RE.finditer(ex):
            if analyze._numeric_value(m.group(0)) == analyze._numeric_value(value):
                occ.append(m.start())
        ctx = []
        for pos in occ[:3]:
            ctx.append(ex[max(0, pos - 140): pos + 80].replace("\n", " | "))
        # does the series name occur near the value?
        series_words = [w for w in re.findall(r"[A-Za-z]{4,}", str(td.get("series")))][:3]
        row = {"period": period, "value": value, "reason": reason, "period_token_located": bool(tok),
               "alt_period_forms_in_excerpt": tok_near, "value_whole_number_occurrences": len(occ), "contexts": ctx}
        rows.append(row)
        print("  --", period, value, "|", reason)
        print("     period token as emitted located:", bool(tok), "| alt forms present:", tok_near)
        print("     value whole-number occurrences in excerpt:", len(occ))
        for c in ctx:
            print("       ctx:", c[:230])
    out[name] = rows
json.dump(out, open(sys.argv[1], "w"), indent=1)
