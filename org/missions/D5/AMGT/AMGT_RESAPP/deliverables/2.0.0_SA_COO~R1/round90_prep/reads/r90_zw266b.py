import json
import re
import boto3
from lib.research.filings import analyze
s3 = boto3.client("s3", region_name="us-east-1")
def ex(name, acc):
    return json.loads(s3.get_object(Bucket="opal-data-harvest", Key="filings/v1/%s/%s.source.json" % (name, acc))["Body"].read())["excerpt"]["text"]
print("regex:", analyze._WHOLE_NUMBER_RE.pattern)
for t in ["2.99", "21.05", "21,05", "2,99"]:
    print(" _WHOLE_NUMBER_RE matches", repr(t), "->", [m.group(0) for m in analyze._WHOLE_NUMBER_RE.finditer(t)])
for name, acc, needles in [("PBR_US_Equity", "000129281426002168", ["2.99", "2,99", "2.9", "total production", "Total oil and gas production"]),
                           ("SAP_GY_Equity", "000110465926020058", ["21.05", "21,05", "21.0", "current cloud backlog"])]:
    t = ex(name, acc)
    print("=====", name, len(t))
    for n in needles:
        pos = [m.start() for m in re.finditer(re.escape(n), t, re.I)]
        print("  needle %r: %d hit(s)" % (n, len(pos)))
        for p in pos[:2]:
            print("     ...", t[max(0, p - 110): p + 130].replace("\n", " | "))
