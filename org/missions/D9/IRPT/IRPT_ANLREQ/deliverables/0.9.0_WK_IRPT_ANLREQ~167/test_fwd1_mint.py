"""AR-y-373 offline tests for the FWD-1 mint helper (0.9.0_WK_IRPT_ANLREQ~167).

Loads fwd1_mint.py from the helper folder (0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver), or from the path in the
environment variable FWD1_MINT_PATH (mutant_check.py points it at a scratch copy). Tests item_for and readback_ok only:
no AWS, no network, no boto3 call (the helper imports boto3 only inside cmd_mint and cmd_remove).

Prints MINT-TESTS-OK <n> and exits 0 when every case passes; otherwise MINT-TESTS-BAD <why> and exits 1.
"""
import copy
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH = os.path.normpath(os.path.join(HERE, "..", "0.9.0_WK_IRPT_ANLREQ~149", "fwd1_driver", "fwd1_mint.py"))
PATH = os.environ.get("FWD1_MINT_PATH") or DEFAULT_PATH
BASE_ATTRS = ("PK", "SK", "email", "passwordHash", "status", "firmId", "role", "userType", "name", "exp")


def load():
    spec = importlib.util.spec_from_file_location("fwd1_mint_under_test", PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = load()
GOOD_LIST = {"L": [{"S": "49financial"}]}


def good_row():
    row = copy.deepcopy(M.item_for("hashed-value"))
    return row


def case_new_row_carries_one_firm_list():
    item = M.item_for("h")
    return item.get("allowedFirmIds") == GOOD_LIST


def case_row_keeps_every_base_attribute():
    item = M.item_for("h")
    return (all(k in item for k in BASE_ATTRS)
            and item["PK"] == {"S": "USER#fwd1-staff-r41b@opal.invalid"}
            and item["SK"] == {"S": "PROFILE"}
            and item["email"] == {"S": "fwd1-staff-r41b@opal.invalid"}
            and item["passwordHash"] == {"S": "h"}
            and item["status"] == {"S": "active"}
            and item["firmId"] == {"S": "opal-capital"}
            and item["role"] == {"S": "user"}
            and item["userType"] == {"S": "test-filer"}
            and item["exp"]["N"].isdigit())


def case_good_readback_passes():
    return M.readback_ok(good_row()) is True


def case_no_allowed_firm_ids_fails():
    row = good_row()
    del row["allowedFirmIds"]
    return M.readback_ok(row) is False


def case_two_firms_fails():
    row = good_row()
    row["allowedFirmIds"] = {"L": [{"S": "49financial"}, {"S": "opal-capital"}]}
    return M.readback_ok(row) is False


def case_string_scope_fails():
    row = good_row()
    row["allowedFirmIds"] = {"S": "49financial"}
    return M.readback_ok(row) is False


def case_scope_all_firms_fails():
    row = good_row()
    row["scope_all_firms"] = {"BOOL": True}
    return M.readback_ok(row) is False


def case_scope_all_firms_alone_fails():
    row = good_row()
    del row["allowedFirmIds"]
    row["scope_all_firms"] = {"BOOL": True}
    return M.readback_ok(row) is False


def case_mfa_enabled_fails():
    row = good_row()
    row["mfaEnabled"] = {"BOOL": False}
    return M.readback_ok(row) is False


def case_mfa_channel_fails():
    row = good_row()
    row["mfaChannel"] = {"S": "sms"}
    return M.readback_ok(row) is False


def case_status_not_active_fails():
    row = good_row()
    row["status"] = {"S": "inactive"}
    return M.readback_ok(row) is False


def case_empty_list_fails():
    row = good_row()
    row["allowedFirmIds"] = {"L": []}
    return M.readback_ok(row) is False


def case_wrong_firm_fails():
    row = good_row()
    row["allowedFirmIds"] = {"L": [{"S": "opal-capital"}]}
    return M.readback_ok(row) is False


def case_non_string_member_fails():
    row = good_row()
    row["allowedFirmIds"] = {"L": [{"N": "1"}]}
    return M.readback_ok(row) is False


def case_password_hash_absent_fails():
    row = good_row()
    del row["passwordHash"]
    return M.readback_ok(row) is False


CASES = [
    ("new row carries the one-firm list", case_new_row_carries_one_firm_list),
    ("new row keeps every base attribute", case_row_keeps_every_base_attribute),
    ("good read-back row passes", case_good_readback_passes),
    ("row with no allowedFirmIds fails", case_no_allowed_firm_ids_fails),
    ("allowedFirmIds with two firms fails", case_two_firms_fails),
    ("allowedFirmIds as a string fails", case_string_scope_fails),
    ("row with scope_all_firms fails", case_scope_all_firms_fails),
    ("scope_all_firms alone (no list) fails", case_scope_all_firms_alone_fails),
    ("row with mfaEnabled fails", case_mfa_enabled_fails),
    ("row with mfaChannel fails", case_mfa_channel_fails),
    ("status not active fails", case_status_not_active_fails),
    ("empty allowedFirmIds list fails", case_empty_list_fails),
    ("allowedFirmIds with another firm fails", case_wrong_firm_fails),
    ("non-string list member fails", case_non_string_member_fails),
    ("row with no passwordHash fails", case_password_hash_absent_fails),
]


def main():
    failed = []
    for name, fn in CASES:
        try:
            ok = bool(fn())
        except Exception as e:  # noqa: BLE001 -- a raising case is a failing case
            ok = False
            name = name + " (raised " + type(e).__name__ + ")"
        if not ok:
            failed.append(name)
    if failed:
        print("MINT-TESTS-BAD " + "; ".join(failed))
        return 1
    print("MINT-TESTS-OK " + str(len(CASES)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
