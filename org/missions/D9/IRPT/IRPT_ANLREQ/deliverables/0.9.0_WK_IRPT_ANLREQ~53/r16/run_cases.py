"""AR-y-163: run the four cases of the internal firm reader in process, on the fakes of _authz/tests/test_allowed_firm_ids.py.

Usage: python run_cases.py <workspace root>
Offline: no AWS, no network. It drives served.Entry.handle with load_service_profile injected, as the folder's test does.
Prints one line per case: refused = the boundary answered FIRM_BINDING, admitted = the boundary called deps(<selected>).
"""
import os
import sys

root = sys.argv[1] if len(sys.argv) > 1 else "."
tests = os.path.join(root, "infra/aws/lambda/investor-reporting/_authz/tests")
sys.path.insert(0, tests)
import test_allowed_firm_ids as t  # noqa: E402

os.environ["IRPT_DIRECTORY_BUCKET_MAP"] = t._BUCKETS

CASES = [
    ("NO_ROW", None, "inflection"),
    ("NO_ROW", None, "opal-capital"),
    ("DISABLED_ROW status=disabled", {"status": "disabled"}, "inflection"),
    ("DISABLED_ROW status=inactive", {"status": "inactive"}, "inflection"),
    ("DISABLED_ROW disabled+list[cottonwood]", {"status": "disabled", "allowedFirmIds": ["cottonwood"]}, "inflection"),
    ("DISABLED_ROW disabled+list[cottonwood]", {"status": "disabled", "allowedFirmIds": ["cottonwood"]}, "cottonwood"),
    ("ACTIVE_ROW_OWN_FIRM no list", {"status": "active"}, "opal-capital"),
    ("ACTIVE_ROW_OWN_FIRM list[cottonwood]", {"status": "active", "allowedFirmIds": ["cottonwood"]}, "opal-capital"),
    ("ACTIVE_ROW_OTHER_FIRM no list", {"status": "active"}, "inflection"),
    ("ACTIVE_ROW_OTHER_FIRM listed", {"status": "active", "allowedFirmIds": ["inflection"]}, "inflection"),
    ("ACTIVE_ROW_OTHER_FIRM unlisted", {"status": "active", "allowedFirmIds": ["cottonwood"]}, "inflection"),
]
for label, row, sel in CASES:
    refused, admitted = t._run(row, selected=sel)
    print("CASE %-42s selected=%-13s refused=%-5s admitted=%-5s row_lookups=%d" % (label, sel, refused, admitted, len(t.LOOKUPS)))
