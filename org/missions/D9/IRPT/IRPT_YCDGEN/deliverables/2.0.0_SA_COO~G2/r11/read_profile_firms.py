"""IRPT_YCDGEN round 11, cell YCD-d-11 (row IRPT_YCDGEN-D2-S4): ONE read of one user's PROFILE row, firm ids only.

    python read_profile_firms.py andrew@opalinvest.com cottonwood

Prints the row's allowedFirmIds (firm ids), status and userType, and whether the named firm is among them. It finds the row as the product does (the email index, then the
PROFILE item by the PK the index names), reads four attributes by name and never the password hash or any other attribute,
and prints the form of the PK, never its value. It writes nothing. ASCII only.
"""
import sys

import boto3

TABLE = "opal-users-v2"


def main(argv):
    if len(argv) != 3 or "@" not in argv[1] or not argv[2].strip():
        print("usage: read_profile_firms.py <email> <firm id>")
        return 2
    email, firm = argv[1].strip().lower(), argv[2].strip()
    ddb = boto3.client("dynamodb", region_name="us-east-1")
    # The lookup the product itself makes (_scope/canonical_profile_reads.py get_user): the email GSI names the row's PK,
    # then the PROFILE item is read by that PK. A person's PK is NOT assumed to be "USER#<email>": the first version of
    # this script assumed it and read an absence that was only its own key.
    found = ddb.query(TableName=TABLE, IndexName="email-index", KeyConditionExpression="email = :email",
                      ExpressionAttributeValues={":email": {"S": email}}, Limit=2)
    rows = found.get("Items", [])
    print("INDEX email-index rows=%d more=%s" % (len(rows), "YES" if found.get("LastEvaluatedKey") else "NO"))
    if not rows:
        print("USER-NOT-IN-INDEX %s" % email)
        return 0
    if len(rows) > 1 or found.get("LastEvaluatedKey"):
        print("USER-AMBIGUOUS-IN-INDEX %s" % email)
        return 0
    pk = (rows[0].get("PK") or {}).get("S")
    sk = (rows[0].get("SK") or {}).get("S")
    print("INDEX-KEY pk_form=%s sk=%s" % ("USER#<email>" if pk == "USER#" + email else "OTHER", sk))
    item = ddb.get_item(TableName=TABLE, Key={"PK": {"S": pk}, "SK": {"S": "PROFILE"}}, ConsistentRead=True,
                        ProjectionExpression="allowedFirmIds, #s, userType, firmId",
                        ExpressionAttributeNames={"#s": "status"}).get("Item")
    if item is None:
        print("PROFILE-ROW-ABSENT %s" % email)
        return 0
    raw = item.get("allowedFirmIds")
    if raw is None:
        firms, shape = [], "ABSENT"
    elif "S" in raw:
        firms, shape = [f.strip() for f in raw["S"].split(",") if f.strip()], "STRING"
    elif "L" in raw:
        firms, shape = [list(v.values())[0] for v in raw["L"]], "LIST"
    elif "SS" in raw:
        firms, shape = sorted(raw["SS"]), "STRING_SET"
    else:
        firms, shape = [], "OTHER:" + ",".join(sorted(raw))
    flat = {k: list(v.values())[0] for k, v in item.items() if k != "allowedFirmIds"}
    print("PROFILE %s status=%s userType=%s firmId=%s" % (email, flat.get("status"), flat.get("userType"), flat.get("firmId")))
    print("ALLOWED-FIRMS shape=%s count=%d ids=%s" % (shape, len(firms), ",".join(str(f) for f in firms) or "-"))
    print("FIRM-NAMED %s %s" % (firm, "YES" if firm in firms else "NO"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
