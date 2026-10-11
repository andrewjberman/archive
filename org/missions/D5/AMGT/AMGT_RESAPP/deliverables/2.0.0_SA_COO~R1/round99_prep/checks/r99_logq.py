import sys
import time

import boto3

LG = "/aws/lambda/opal-amgt-scoped-api"
q = sys.argv[1]
hours = float(sys.argv[2]) if len(sys.argv) > 2 else 24
n = int(sys.argv[3]) if len(sys.argv) > 3 else 20
end = int(time.time())
cw = boto3.client("logs", region_name="us-east-1")
qid = cw.start_query(logGroupName=LG, startTime=end - int(hours * 3600), endTime=end, queryString=q, limit=10000)["queryId"]
d = {}
for _ in range(100):
    time.sleep(3)
    d = cw.get_query_results(queryId=qid)
    if d["status"] in ("Complete", "Failed", "Cancelled", "Timeout"):
        break
print("status", d["status"], "| statistics", d.get("statistics"))
for row in d.get("results", [])[:n]:
    print({c["field"]: c["value"] for c in row if c["field"] != "@ptr"})
