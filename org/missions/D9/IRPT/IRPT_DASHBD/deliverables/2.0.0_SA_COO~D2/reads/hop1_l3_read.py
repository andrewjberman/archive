"""IRPT_DASHBD hop 1, the L3 read of the first scheduled fire after the apply (issuer 2.0.0_SA_COO~D2; CTO ROUND-124 ANALYSIS @7b6dccc88a: "the hop-1 proof is the read after Friday 10-16's ~11:41Z
fire, graded against the signed half"). READ ONLY: CloudWatch Logs filter, S3 LIST and GET of the new filled_report_values partition; prints COUNTS, DURATIONS and MEGABYTES only, never a
value or an identifier.

Usage: python hop1_l3_read.py <repo_root> [<since_iso_utc>]     (default since 2026-10-16T11:30:00Z)

What it prints, for the graded half (packet NEVER_WIDEN_PACKET_HOP1_FILLED_REPORT_VALUES_STAGE.md section 7 condition 4 and the CTO half): every REPORT line of the function since the cut (Duration,
Max Memory Used against the 8,192 MB size and the 5,734 MB line), the number of FILLED_SKIPPED lines, the number of FILLED_CHAINED lines, and the filled_report_values partitions: their dates, objects
and the row count of the newest. VERDICT lines: MEMORY_LINE (Max Memory Used over 5,734 MB triggers the grouped-read cell), TIMEOUT_LINE (a duration near 900 s), SKIPPED (any FILLED_SKIPPED).
"""
import datetime as dt
import io
import re
import sys

FUNCTION = "irpt-49f-reporting-gold-lambda"
LOG_GROUP = "/aws/lambda/" + FUNCTION
MEM_LINE_MB, MEM_SIZE_MB, TIMEOUT_MS = 5734, 8192, 900000


def events(logs, pattern, start_ms):
    out, tok = [], None
    for _ in range(200):
        kw = {"logGroupName": LOG_GROUP, "filterPattern": pattern, "startTime": start_ms}
        if tok:
            kw["nextToken"] = tok
        r = logs.filter_log_events(**kw)
        out += r.get("events", [])
        tok = r.get("nextToken")
        if not tok:
            break
    return out


def main(root, since):
    sys.path.insert(0, str(root))
    import boto3
    from lib import opal_naming
    logs, s3 = boto3.client("logs", region_name="us-east-1"), boto3.client("s3")
    start_ms = int(dt.datetime.fromisoformat(since.replace("Z", "+00:00")).timestamp() * 1000)
    reports = []
    for ev in events(logs, "REPORT", start_ms):
        m = re.search(r"Duration: ([\d.]+) ms.*?Memory Size: (\d+) MB\s+Max Memory Used: (\d+) MB", ev["message"], re.S)
        if m:
            reports.append((ev["timestamp"], float(m.group(1)), int(m.group(2)), int(m.group(3))))
    skipped = len(events(logs, "FILLED_SKIPPED", start_ms))
    chained = len(events(logs, "FILLED_CHAINED", start_ms))
    errors = len(events(logs, "?ERROR ?Traceback \"Task timed out\"", start_ms))
    print("since", since, "REPORT lines:", len(reports), "FILLED_SKIPPED:", skipped, "FILLED_CHAINED:", chained, "error-ish lines:", errors)
    for ts, dur, size, mx in sorted(reports):
        print("  %s duration %.1f s, memory size %d MB, Max Memory Used %d MB" % (dt.datetime.fromtimestamp(ts / 1000, dt.timezone.utc).strftime("%H:%M:%SZ"), dur / 1000, size, mx))
    peak = max((r[3] for r in reports), default=None)
    slow = max((r[1] for r in reports), default=None)
    uri = str(opal_naming.address("irpt", "49financial", "gold", "filled_report_values", "date=2000-01-03", "data.parquet"))
    bucket, key = uri[len("s3://"):].split("/", 1)
    prefix = key.rsplit("/date=", 1)[0] + "/"
    days, tok = {}, None
    while True:
        kw = {"Bucket": bucket, "Prefix": prefix}
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        for o in r.get("Contents", []):
            d = o["Key"][len(prefix) + 5:len(prefix) + 15]
            days.setdefault(d, []).append((o["Key"], o["Size"], o["LastModified"]))
        if not r.get("IsTruncated"):
            break
        tok = r.get("NextContinuationToken")
    print("filled_report_values partitions:", len(days), "newest:", max(days) if days else None)
    if days:
        newest = max(days)
        k = [x for x in days[newest] if x[0].endswith("data.parquet")]
        if k:
            import pyarrow.parquet as pq
            body = s3.get_object(Bucket=bucket, Key=k[0][0])["Body"].read()
            t = pq.read_table(io.BytesIO(body))
            print("  newest partition", newest, "rows", t.num_rows, "bytes", len(body), "objects", sorted(x[0].rsplit("/", 1)[1] for x in days[newest]))
    print("MEMORY_LINE:", "OVER the %d MB line (grouped-read cell)" % MEM_LINE_MB if peak is not None and peak > MEM_LINE_MB else "under (peak %s MB of %d)" % (peak, MEM_SIZE_MB))
    print("TIMEOUT_LINE:", "NEAR the 900 s timeout" if slow is not None and slow > 0.8 * TIMEOUT_MS else "clear (slowest %s ms)" % slow)
    print("SKIPPED:", "FILLED_SKIPPED present: %d" % skipped if skipped else "none")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "2026-10-16T11:30:00Z")
