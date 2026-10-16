"""Offline tests for fwd1_advisor.py (AR380-y-AC1). Stubs only: no boto3 client, no network, no AWS call.

Prints ONE line on stdout: ADVISOR-TESTS-OK <n> when every case passes, else ADVISOR-TESTS-BAD <why> (exit 1).
Failure detail goes to stderr only.
"""
import copy
import sys

import fwd1_advisor as fa

NOW = 1792000000
DATE = "20261016"
ADDR = "irpt-w5-advisor-20261016@opal.invalid"
PARTNER_TABLE = "opal-partner-49financial"
USER_ATTRS = {"PK", "SK", "email", "firmId", "status", "name", "role", "tier", "allowedFirmIds",
              "createdAt", "createdBy", "updatedAt", "exp"}
PARTNER_ATTRS = {"email", "advisorKey", "advisorName", "advisorRole", "firmRole", "createdAt", "createdBy", "updatedAt"}


class StubError(Exception):
    def __init__(self, code):
        Exception.__init__(self, code)
        self.response = {"Error": {"Code": code}}


class StubDDB:
    """In-memory stand-in for the boto3 dynamodb client: only the calls fwd1_advisor makes."""

    def __init__(self, users=None, partner=None, gsi=None, stuck=False):
        self.users = users
        self.partner = partner
        self.gsi = gsi if gsi is not None else (1 if users is not None else 0)
        self.stuck = stuck      # True: a delete reports success but the row and the index entry stay
        self.mangle = None      # optional function applied to a users item as it is stored
        self.calls = []
        self.puts = []
        self.deletes = []

    def get_item(self, TableName, Key, ConsistentRead=False):
        self.calls.append(("get_item", TableName, bool(ConsistentRead)))
        item = self.users if TableName == fa.USERS else self.partner
        return {"Item": copy.deepcopy(item)} if item is not None else {}

    def query(self, TableName, IndexName, KeyConditionExpression, ExpressionAttributeValues, Select):
        self.calls.append(("query", TableName, IndexName, Select))
        return {"Count": self.gsi}

    def put_item(self, TableName, Item, ConditionExpression):
        self.calls.append(("put_item", TableName, ConditionExpression))
        self.puts.append((TableName, copy.deepcopy(Item), ConditionExpression))
        if TableName == fa.USERS:
            if self.users is not None:
                raise StubError("ConditionalCheckFailedException")
            stored = copy.deepcopy(Item)
            self.users = self.mangle(stored) if self.mangle else stored
            self.gsi = 1
        else:
            if self.partner is not None:
                raise StubError("ConditionalCheckFailedException")
            self.partner = copy.deepcopy(Item)

    def delete_item(self, TableName, Key, ConditionExpression):
        self.calls.append(("delete_item", TableName, ConditionExpression))
        self.deletes.append((TableName, ConditionExpression))
        if TableName == fa.USERS:
            if self.users is None:
                raise StubError("ConditionalCheckFailedException")
            if not self.stuck:
                self.users = None
                self.gsi = 0
        else:
            if self.partner is None:
                raise StubError("ConditionalCheckFailedException")
            if not self.stuck:
                self.partner = None


class FakeClock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t

    def sleep(self, seconds):
        self.t += seconds


def case_address_from_date():
    assert fa.address_for(DATE) == ADDR, fa.address_for(DATE)
    assert fa.address_for("20250102").endswith("@opal.invalid")
    assert fa.FIRM == "49financial" and fa.partner_table() == PARTNER_TABLE


def case_bad_date_refused():
    for bad in ("2026-10-16", "2026101", "202610161", "abcdefgh", "20261316", "20261016\n", "", None):
        try:
            fa.parse_date(bad)
        except ValueError:
            continue
        raise AssertionError("date accepted: %r" % (bad,))


def case_user_item_shape():
    item = fa.user_item(ADDR, NOW)
    assert set(item) == USER_ATTRS and len(item) == 13, sorted(item)
    assert item["status"] == {"S": "active"} and item["firmId"] == {"S": "49financial"}
    assert item["role"] == {"S": "user"} and item["tier"] == {"S": "advisor"}
    assert item["allowedFirmIds"] == {"L": [{"S": "49financial"}]}
    assert item["exp"] == {"N": str(NOW + 3 * 3600)}, item["exp"]


def case_partner_item_shape():
    item = fa.partner_item(ADDR, DATE, NOW)
    assert set(item) == PARTNER_ATTRS and len(item) == 8, sorted(item)
    assert item["advisorKey"] == {"S": "irpt-w5-adv-20261016"}
    assert item["advisorRole"] == {"S": "viewer"} and item["firmRole"] == {"S": "user"}


def case_no_credential_in_items():
    for item in (fa.user_item(ADDR, NOW), fa.partner_item(ADDR, DATE, NOW)):
        assert not any(k in item for k in fa.CREDENTIAL_KEYS), sorted(item)
        assert "$2" not in repr(item)


def case_user_readback_accepts_written_and_refuses_wider():
    row = fa.user_item(ADDR, NOW)
    assert fa.user_readback_ok(row, ADDR)
    wider = dict(row, allowedFirmIds={"L": [{"S": "49financial"}, {"S": "cottonwood"}]})
    assert not fa.user_readback_ok(wider, ADDR)
    assert not fa.user_readback_ok(dict(row, status={"S": "disabled"}), ADDR)
    assert not fa.user_readback_ok(dict(row, firmId={"S": "cottonwood"}), ADDR)
    assert not fa.user_readback_ok(dict(row, passwordHash={"S": "x"}), ADDR)
    assert not fa.user_readback_ok(None, ADDR)


def case_partner_readback():
    row = fa.partner_item(ADDR, DATE, NOW)
    assert fa.partner_readback_ok(row, ADDR, DATE)
    assert not fa.partner_readback_ok(None, ADDR, DATE)
    assert not fa.partner_readback_ok(dict(row, advisorRole={"S": "admin"}), ADDR, DATE)


def case_mint_writes_users_then_partner_with_conditions():
    ddb = StubDDB()
    rc, lines = fa.mint(ddb, DATE, NOW)
    assert rc == 0, lines
    assert [p[0] for p in ddb.puts] == [fa.USERS, PARTNER_TABLE], ddb.puts
    assert ddb.puts[0][2] == "attribute_not_exists(PK)" and ddb.puts[1][2] == "attribute_not_exists(email)"
    assert lines == ["ADVISOR-MINT-OK " + ADDR, "ADVISOR-READBACK-OK users partner"], lines


def case_mint_prestate_users_present_writes_nothing():
    ddb = StubDDB(users=fa.user_item(ADDR, NOW))
    rc, lines = fa.mint(ddb, DATE, NOW)
    assert rc == 1 and lines == ["ADVISOR-MINT-REFUSED prestate users-row-present"], lines
    assert ddb.puts == []


def case_mint_prestate_index_present_writes_nothing():
    ddb = StubDDB(gsi=1)
    rc, lines = fa.mint(ddb, DATE, NOW)
    assert rc == 1 and lines == ["ADVISOR-MINT-REFUSED prestate email-index-count=1"], lines
    assert ddb.puts == []


def case_mint_prestate_partner_present_writes_nothing():
    ddb = StubDDB(partner=fa.partner_item(ADDR, DATE, NOW))
    rc, lines = fa.mint(ddb, DATE, NOW)
    assert rc == 1 and lines == ["ADVISOR-MINT-REFUSED prestate partner-row-present"], lines
    assert ddb.puts == []


def case_mint_prereads_are_consistent():
    ddb = StubDDB()
    fa.mint(ddb, DATE, NOW)
    assert ("get_item", fa.USERS, True) in ddb.calls
    assert ("get_item", PARTNER_TABLE, True) in ddb.calls
    assert ("query", fa.USERS, "email-index", "COUNT") in ddb.calls


def case_mint_readback_mismatch_stops_before_partner():
    ddb = StubDDB()
    ddb.mangle = lambda it: dict(it, allowedFirmIds={"L": [{"S": "49financial"}, {"S": "cottonwood"}]})
    rc, lines = fa.mint(ddb, DATE, NOW)
    assert rc == 1 and lines == ["ADVISOR-READBACK-BAD users (the users row is written; run remove)"], lines
    assert all(p[0] == fa.USERS for p in ddb.puts), ddb.puts


def case_remove_deletes_with_conditions_and_prints_absent():
    ddb = StubDDB(users=fa.user_item(ADDR, NOW), partner=fa.partner_item(ADDR, DATE, NOW))
    clk = FakeClock()
    rc, lines = fa.remove(ddb, DATE, clock=clk, sleep=clk.sleep)
    assert ddb.deletes == [(fa.USERS, "attribute_exists(PK)"), (PARTNER_TABLE, "attribute_exists(email)")], ddb.deletes
    assert rc == 0, lines
    assert lines[-3:] == ["ABSENT GSI " + ADDR, "ABSENT CONSISTENT " + ADDR, "ABSENT PARTNER " + ADDR], lines


def case_remove_stuck_rows_exit_one_at_deadline():
    ddb = StubDDB(users=fa.user_item(ADDR, NOW), partner=fa.partner_item(ADDR, DATE, NOW), stuck=True)
    clk = FakeClock()
    start = clk.t
    rc, lines = fa.remove(ddb, DATE, clock=clk, sleep=clk.sleep)
    assert rc == 1, lines
    assert "PRESENT CONSISTENT " + ADDR in lines and "PRESENT GSI " + ADDR in lines, lines
    assert clk.t - start >= fa.REMOVE_WINDOW_S, clk.t - start


def case_remove_missing_rows_is_noop_then_absent():
    ddb = StubDDB()
    clk = FakeClock()
    rc, lines = fa.remove(ddb, DATE, clock=clk, sleep=clk.sleep)
    assert rc == 0, lines
    assert "REMOVE-NOOP users" in lines and "REMOVE-NOOP partner" in lines, lines


def case_remove_polls_both_stores_consistently():
    ddb = StubDDB()
    fa.remove(ddb, DATE, clock=FakeClock(), sleep=FakeClock().sleep)
    assert ("get_item", fa.USERS, True) in ddb.calls and ("get_item", PARTNER_TABLE, True) in ddb.calls
    assert ("query", fa.USERS, "email-index", "COUNT") in ddb.calls


def case_module_import_touches_no_aws():
    assert "boto3" not in sys.modules, "boto3 was imported before the helper's tests ran"


CASES = (case_address_from_date, case_bad_date_refused, case_user_item_shape, case_partner_item_shape,
         case_no_credential_in_items, case_user_readback_accepts_written_and_refuses_wider, case_partner_readback,
         case_mint_writes_users_then_partner_with_conditions, case_mint_prestate_users_present_writes_nothing,
         case_mint_prestate_index_present_writes_nothing, case_mint_prestate_partner_present_writes_nothing,
         case_mint_prereads_are_consistent, case_mint_readback_mismatch_stops_before_partner,
         case_remove_deletes_with_conditions_and_prints_absent, case_remove_stuck_rows_exit_one_at_deadline,
         case_remove_missing_rows_is_noop_then_absent, case_remove_polls_both_stores_consistently,
         case_module_import_touches_no_aws)


def run():
    failed = []
    for case in CASES:
        try:
            case()
        except Exception as exc:  # noqa: BLE001 -- every case is judged, none stops the run
            failed.append("%s (%s: %s)" % (case.__name__, type(exc).__name__, exc))
    if failed:
        for f in failed:
            sys.stderr.write("FAILED " + f + "\n")
        print("ADVISOR-TESTS-BAD " + str(len(failed)) + " of " + str(len(CASES)) + " cases failed")
        return 1
    print("ADVISOR-TESTS-OK %d" % len(CASES))
    return 0


if __name__ == "__main__":
    sys.exit(run())
