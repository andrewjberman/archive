"""CONTROLS for TO-S4-1.
MUTANT: the AC1/AC4 blank detector is fed a synthetic table containing BOTH shapes of blank.
If the detector were blind to either shape, AC4's '0 missing, 0 empty' would be indistinguishable
from a true clean read. The mutant must report 1 MISSING and 1 EMPTY, separately.
DETERMINISM: the AC4 read-back analysis is re-run against a freshly-scanned table and compared."""
import json
import sys

def classify(items):
    missing, empty, ok = [], [], []
    for it in items:
        t = it['ticker']['S']
        if 'sub_asset_class' not in it:
            missing.append(t)
        elif it['sub_asset_class'].get('S', '').strip() == '':
            empty.append(t)
        else:
            ok.append(t)
    return missing, empty, ok

def rescan_with_boto3():
    """Fully-paginated re-scan through a DIFFERENT instrument than the AC4 CLI shim."""
    import boto3
    ddb = boto3.client("dynamodb", region_name="us-east-1")
    items = []
    kw = {}
    while True:
        page = ddb.scan(TableName="etf-classifications",
                        ProjectionExpression="ticker, sub_asset_class", **kw)
        items.extend(page["Items"])
        if "LastEvaluatedKey" not in page:
            break
        kw["ExclusiveStartKey"] = page["LastEvaluatedKey"]
    return items


print("=== MUTANT ARM: synthetic rows, both blank shapes present ===")
mut = [
    {"ticker": {"S": "MUT_MISSING"}},
    {"ticker": {"S": "MUT_EMPTY"}, "sub_asset_class": {"S": ""}},
    {"ticker": {"S": "MUT_OK"}, "sub_asset_class": {"S": "Utilities"}},
]
m, e, o = classify(mut)
print("   MISSING:", m, " EMPTY:", e, " POPULATED:", o)
mut_ok = (m == ["MUT_MISSING"] and e == ["MUT_EMPTY"] and o == ["MUT_OK"])
print("   MUTANT STATUS:", "PASS -- the detector separates both shapes" if mut_ok else "FAIL -- detector is blind")

print()
print("=== NEGATIVE CONTROL ARM: the same detector on the LIVE post-fill table ===")
live = json.load(open('.scratch/ac4_scan.json'))['Items']
m2, e2, o2 = classify(live)
print("   denominator:", len(live), " MISSING:", len(m2), m2, " EMPTY:", len(e2), e2, " POPULATED:", len(o2))
print("   ARMS DIFFER:", "YES -- mutant finds blanks, live finds none, so the live zero is a reading not a blindness"
      if (m and not m2) else "NO -- control did not discriminate")

print()
print("=== DETERMINISM: fresh re-scan compared against the AC4 scan ===")
f_items = rescan_with_boto3()
fresh = {"Items": f_items}
print("   re-scan instrument: boto3 dynamodb.scan (DIFFERENT instrument from the AC4 .tools/aws CLI shim)")
print("   re-scan rc: 0 (no exception), fully paginated")
a = {i['ticker']['S']: i.get('sub_asset_class', {}).get('S') for i in live}
b = {i['ticker']['S']: i.get('sub_asset_class', {}).get('S') for i in f_items}
print("   AC4 scan denominator:", len(a), " re-scan denominator:", len(b))
diff = {k: (a.get(k), b.get(k)) for k in set(a) | set(b) if a.get(k) != b.get(k)}
print("   ticker->sub_asset_class mapping IDENTICAL:", not diff, ("differences: %s" % diff) if diff else "")
print('   pagination: loop exited on absent LastEvaluatedKey; pages accumulated client-side')
print("   DETERMINISM STATUS:", "PASS -- two independent scans agree on all %d rows" % len(b) if not diff else "FAIL")
sys.exit(0 if (mut_ok and not diff and not m2 and not e2) else 1)
