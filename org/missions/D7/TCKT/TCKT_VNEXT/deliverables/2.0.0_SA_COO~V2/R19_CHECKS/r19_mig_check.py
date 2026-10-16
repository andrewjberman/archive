"""TCKT_VNEXT round 19 -- R19-MIG: every active internal staff PROFILE row carries a usable firm scope.

Read-only AWS read (us-east-1) of opal-users-v2: the PROFILE rows with firmId = opal-capital (the internal rows). Prints
MIG-OK <detail> or MIG-BAD <reason>; exit 0/1. No address is read or printed (projection: status, allowedFirmIds,
scope_all_firms only). The check compares the live table with the result file the applier writes.
"""
import json
import os
import subprocess
import sys

RES = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r19_mig/R19_MIG_RESULT.json"
TABLE = "opal-users-v2"
AWS = os.path.abspath(".tools/aws.cmd")


def aws(*args):
    out = subprocess.run([AWS] + list(args) + ["--region", "us-east-1", "--output", "json"],
                         capture_output=True, text=True, timeout=180)
    if out.returncode != 0:
        raise RuntimeError("aws %s rc=%d" % (" ".join(args[:2]), out.returncode))
    if not out.stdout.strip():
        raise RuntimeError("aws %s printed nothing" % " ".join(args[:2]))
    return json.loads(out.stdout)


def locked_out_by_release(r):
    """PURE. True iff an ACTIVE internal row is admitted today and refused once `_profile_scope` fails closed (R19-ps-3).

    Today a row with no allowedFirmIds attribute, an empty list, or a NULL attribute reads as EVERY firm; after the release
    each is refused ("firm scope not configured") unless the row carries scope_all_firms exactly BOOL true. A non-empty
    list is scoped and keeps its scope. An attribute of any OTHER type (a string, a number, a map) is refused as
    "firm scope malformed" BOTH before and after the release, so the release changes nothing for it and it is not counted.
    """
    if (r.get("status") or {}).get("S") != "active":
        return False
    flag = r.get("scope_all_firms")
    if isinstance(flag, dict) and flag.get("BOOL") is True:
        return False
    if "allowedFirmIds" not in r:
        return True
    attr = r["allowedFirmIds"]
    if "NULL" in attr:
        return True
    if "L" in attr:
        return len(attr["L"]) == 0
    return False


def main():
    try:
        res = json.load(open(RES, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("MIG-BAD cannot read the migration result file: %s" % e)
        return 1
    n = res.get("rows_written")
    keys = res.get("row_keys")
    if not isinstance(n, int) or n < 0 or not isinstance(keys, list) or len(keys) != n:
        print("MIG-BAD the result file needs rows_written (int) and row_keys (a list of that length)")
        return 1
    if not res.get("change_ledger") or not res.get("pair"):
        print("MIG-BAD the result file lacks change_ledger or pair")
        return 1
    try:
        d = aws("dynamodb", "scan", "--table-name", TABLE,
                "--filter-expression", "SK = :p AND firmId = :f",
                "--expression-attribute-values", '{":p":{"S":"PROFILE"},":f":{"S":"opal-capital"}}',
                "--projection-expression", "#s, allowedFirmIds, scope_all_firms",
                "--expression-attribute-names", '{"#s":"status"}')
    except (RuntimeError, ValueError, OSError, subprocess.SubprocessError) as e:
        print("MIG-BAD live read failed: %s" % e)
        return 1
    items = d.get("Items") or []
    if not items:
        print("MIG-BAD the scan returned no internal PROFILE rows (a zero is not a pass); ScannedCount=%s" % d.get("ScannedCount"))
        return 1
    both = unscoped = markers = 0
    for r in items:
        has_list = "allowedFirmIds" in r
        flag = r.get("scope_all_firms")
        is_marker = isinstance(flag, dict) and flag.get("BOOL") is True
        if has_list and flag is not None:
            both += 1
        if is_marker and not has_list:
            markers += 1
        if locked_out_by_release(r):
            unscoped += 1
    if both:
        print("MIG-BAD %d row(s) carry both a list and the marker" % both)
        return 1
    if unscoped:
        print("MIG-BAD %d active internal row(s) have neither a non-empty list nor the marker (they would be locked out)" % unscoped)
        return 1
    if markers < n:
        print("MIG-BAD live marker rows %d are fewer than the %d the result file records" % (markers, n))
        return 1
    print("MIG-OK rows_written=%d markers_live=%d internal_rows_scanned=%d" % (n, markers, len(items)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
