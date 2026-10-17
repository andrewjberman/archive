"""Ask the door (globgrph-trino-access-lambda, MEMBER alias) to rebuild the silver table for some Eastern dates, from the raw store.

For a member of globgrph-trino-access-group, from an MFA session (aws sts get-session-token ... then export the three keys, unset AWS_PROFILE):
    python derive_days.py 2026-10-16 2026-10-15 2026-10-14

One door call per date, all at once (a busy day takes 60 to 100 seconds on the door). Prints the date and the row count only: no record, no account.
Safe to repeat: derive rewrites the same partition from the same raw objects. The collector does this itself on its own fires; this is for a member who wants the
newest days now. Round-1 stopgap of SOC2_MSLOGS (issuer 2.0.0_SA_COO~S1).
"""
import concurrent.futures
import json
import re
import sys

DOOR = "globgrph-trino-access-lambda"


def derive(client, date):
    reply = client.invoke(FunctionName=DOOR, Qualifier="member", Payload=json.dumps({"op": "derive_silver", "date": date}).encode())
    body = json.loads(reply["Payload"].read())
    if reply.get("FunctionError") or not body.get("ok"):
        return date, "REFUSED (%s)" % (body.get("error") or reply.get("FunctionError") or "no reason given")
    return date, "ok rows=%s" % body.get("rows")


def main(argv):
    dates = argv[1:]
    if not dates or not all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", d) for d in dates):
        print("usage: python derive_days.py YYYY-MM-DD [YYYY-MM-DD ...]")
        return 2
    import boto3
    from botocore.config import Config

    client = boto3.client("lambda", config=Config(read_timeout=290, connect_timeout=10, retries={"max_attempts": 1, "mode": "standard"}))
    code = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(8, len(dates))) as pool:
        for date, verdict in pool.map(lambda d: derive(client, d), dates):
            print(date, verdict)
            if not verdict.startswith("ok"):
                code = 1
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
