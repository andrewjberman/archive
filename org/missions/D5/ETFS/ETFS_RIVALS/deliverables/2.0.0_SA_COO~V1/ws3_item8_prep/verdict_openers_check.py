"""WS3 item 8 (Direction Verdict prompt) -- the opener-diversity check, prepared before the cut.

    python verdict_openers_check.py <page index.html: a local path, or s3://bucket/key>

Reads every Direction Verdict on the page, de-duplicates repeated renders of one verdict, and takes each verdict's
opening four words. PASS when no single four-word opening is shared by more than a quarter of the distinct verdicts
(Andrew-direct 2026-10-09, comment 7: "more than half of the analyses lead with something like ..."). Exit 0 = PASS,
1 = FAIL, 2 = no verdict on the page (NO MEASUREMENT, never a pass).
"""
import collections
import re
import sys

SRC = sys.argv[1]
if SRC.startswith("s3://"):
    import boto3
    bucket, key = SRC[5:].split("/", 1)
    html = boto3.client("s3", region_name="us-east-1").get_object(Bucket=bucket, Key=key)["Body"].read().decode("utf-8", "replace")
else:
    html = open(SRC, encoding="utf-8", errors="replace").read()

text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))
seen, openers = set(), []
for m in re.finditer(r"Direction verdict (?:Grounded on an earlier build(?:: [^.]*\.[^.]*\.)? )?(.{0,400})", text):
    body = m.group(1).strip()
    if not body or body[:120] in seen:
        continue
    seen.add(body[:120])
    openers.append(" ".join(re.sub(r"\d{4}-\d{2}-\d{2}", "<date>", body).split()[:4]).lower())  # dates differ per fund; the lead does not

if not openers:
    print(f"NO-MEASUREMENT: 0 Direction Verdicts on {SRC}")
    sys.exit(2)
top, n = collections.Counter(openers).most_common(1)[0]
limit = len(openers) / 4
print(f"distinct verdicts: {len(openers)}; most shared opening: '{top}' x{n}; limit {limit:.2f} (one quarter)")
print("PASS" if n <= limit else "FAIL")
sys.exit(0 if n <= limit else 1)
