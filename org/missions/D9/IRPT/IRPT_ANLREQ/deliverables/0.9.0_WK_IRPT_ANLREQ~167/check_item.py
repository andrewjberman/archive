"""AR-y-373 item check (0.9.0_WK_IRPT_ANLREQ~167): the item_for() row carries exactly the ten base attributes of the
worker-149 helper plus allowedFirmIds, and nothing else. Loads fwd1_mint.py from the helper folder; no AWS.

Prints ITEM-OK <n> attributes and exits 0 only when the attribute set is the base set plus allowedFirmIds (n = 11) and
allowedFirmIds is the one-firm list; otherwise ITEM-BAD <why> and exits 1.
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HELPER = os.path.normpath(os.path.join(HERE, "..", "0.9.0_WK_IRPT_ANLREQ~149", "fwd1_driver", "fwd1_mint.py"))
BASE_ATTRS = {"PK", "SK", "email", "passwordHash", "status", "firmId", "role", "userType", "name", "exp"}
EXPECTED = BASE_ATTRS | {"allowedFirmIds"}


def main():
    spec = importlib.util.spec_from_file_location("fwd1_mint_item_check", HELPER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    item = mod.item_for("x")
    names = set(item.keys())
    if names != EXPECTED:
        extra = sorted(names - EXPECTED)
        missing = sorted(EXPECTED - names)
        print("ITEM-BAD attribute set differs: extra=" + repr(extra) + " missing=" + repr(missing))
        return 1
    if len(item) != 11:
        print("ITEM-BAD count " + str(len(item)))
        return 1
    if item["allowedFirmIds"] != {"L": [{"S": "49financial"}]}:
        print("ITEM-BAD allowedFirmIds is not the one-firm list")
        return 1
    print("ITEM-OK " + str(len(item)) + " attributes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
