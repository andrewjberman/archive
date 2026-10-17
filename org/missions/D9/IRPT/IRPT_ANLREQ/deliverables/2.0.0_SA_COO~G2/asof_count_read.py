"""READ ONLY (row IRPT_ANLREQ-D2-S163, CTO msg 10242): which delivered Opal reports carry a price as_of that the trading-calendar T-1 rule would change.
Lists each firm's run records (irpt/<firm>/state/ycharts_runs/request=*/run.json), reads each, and prints COUNTS and DATES only: no holdings, no client names, no request ids."""
import datetime
import json
import sys

import boto3

sys.path.insert(0, "lib")
import opal_naming as n  # noqa: E402
import trading_calendar as tc  # noqa: E402

s3 = boto3.client("s3", region_name="us-east-1")
FIRMS = ("cottonwood", "49financial", "inflection")


def list_page(firm, bucket, prefix, token):
    """One page of the listing, or None when the listing raised (the class is printed)."""
    try:
        if token:
            return s3.list_objects_v2(Bucket=bucket, Prefix=prefix, ContinuationToken=token)
        return s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    except Exception as exc:  # a read prints what is raised
        print("LIST %s %s.%s" % (firm, type(exc).__module__, type(exc).__name__))
        return None


def weekday_rule(day):
    """resident_installed._t_minus_1 on the UTC date of the run: minus one day, minus further days while Saturday or Sunday."""
    d = day - datetime.timedelta(days=1)
    while d.weekday() >= 5:
        d -= datetime.timedelta(days=1)
    return d


def main():
    listed_total, rows = 0, []
    for firm in FIRMS:
        uri = n.address("irpt", firm, "state", "ycharts_runs", "request=X", object="run.json")
        bucket, _, key = uri[len("s3://"):].partition("/")
        prefix = key.split("request=")[0]
        token, keys = None, []
        while True:
            resp = list_page(firm, bucket, prefix, token)
            if resp is None:
                break
            keys += [(o["Key"], o["LastModified"]) for o in resp.get("Contents", []) if o["Key"].endswith("/run.json")]
            token = resp.get("NextContinuationToken")
            if not token:
                break
        listed_total += len(keys)
        print("FIRM %s bucket=%s run.json objects listed=%d" % (firm, bucket, len(keys)))
        for k, modified in keys:
            try:
                doc = json.loads(s3.get_object(Bucket=bucket, Key=k)["Body"].read().decode("utf-8"))
            except Exception as exc:
                rows.append((firm, modified.date().isoformat(), "UNREADABLE:" + type(exc).__name__, None, None))
                continue
            settings = doc.get("settings") or {}
            price_as_of = settings.get("price_as_of")
            inputs = doc.get("inputs") or []
            run_date = (inputs[0].get("as_of") if inputs and isinstance(inputs[0], dict) else None) or modified.date().isoformat()
            rows.append((firm, run_date, "PRICED" if price_as_of else "UNPRICED", price_as_of, modified.isoformat()[:19]))
    print("DENOMINATOR run.json objects listed across firms: %d; read: %d" % (listed_total, len(rows)))
    priced = [r for r in rows if r[2] == "PRICED"]
    print("UNPRICED (no price_as_of in settings): %d; PRICED: %d; UNREADABLE: %d" % (sum(1 for r in rows if r[2] == "UNPRICED"), len(priced), sum(1 for r in rows if r[2].startswith("UNREADABLE"))))
    changed = []
    for firm, run_date, status, price_as_of, modified in priced:
        day = datetime.date.fromisoformat(run_date[:10])
        cal = tc.prev_trading_day(tc.expected_last_trading_day(day)).isoformat()
        wk = weekday_rule(day).isoformat()
        changed.append((firm, run_date[:10], day.strftime("%a"), price_as_of, wk, cal, price_as_of != cal, wk != price_as_of))
    for r in sorted(changed, key=lambda x: x[1]):
        print("PRICED firm=%s run_date=%s %s price_as_of=%s weekday_rule=%s calendar=%s CHANGES=%s weekday_rule_matches_stored=%s" % (r[0], r[1], r[2], r[3], r[4], r[5], r[6], not r[7]))
    print("WOULD CHANGE under the calendar rule: %d of %d priced reports" % (sum(1 for r in changed if r[6]), len(changed)))
    print("LAST modified of any run.json: %s" % (max((r[4] for r in rows if r[4]), default=None),))


if __name__ == "__main__":
    main()
