"""Offline tests for fwd5_mint.py (AR-ty-56). No AWS, no network: a fake DynamoDB client records every call."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import fwd5_mint as m  # noqa: E402

PW = "cross-firm-test-password-0123456789"
PW_JSON = json.dumps({"password": PW})
FIRM = "firm-b"
IDS = "firm-a,firm-c"
IDS_LIST = ["firm-a", "firm-c"]


class FakeDDB:
    """Stores put_item rows by PK; get_row, when set, overrides what get_item returns (readback tests)."""

    def __init__(self, get_row=None, put_error=None):
        self.calls = []
        self.items = {}
        self.get_row = get_row
        self.put_error = put_error

    def put_item(self, **kw):
        self.calls.append(("put_item", kw))
        if self.put_error is not None:
            raise self.put_error
        self.items[kw["Item"]["PK"]["S"]] = kw["Item"]
        return {}

    def get_item(self, **kw):
        self.calls.append(("get_item", kw))
        if self.get_row is not None:
            return {"Item": self.get_row}
        item = self.items.get(kw["Key"]["PK"]["S"])
        return {"Item": item} if item is not None else {}

    def delete_item(self, **kw):
        self.calls.append(("delete_item", kw))
        self.items.pop(kw["Key"]["PK"]["S"], None)
        return {}

    def query(self, **kw):
        self.calls.append(("query", kw))
        return {"Count": 0}


def _mint_args(email="cf-a@opal.invalid", firm=FIRM, ids=IDS):
    return ["--email", email, "--firm", firm, "--allowed-firm-ids", ids]


def _run_mint(capsys, args, ddb, stdin_text=PW_JSON):
    rc = m.cmd_mint(args, stdin_text=stdin_text, ddb=ddb)
    return rc, capsys.readouterr().out


def test_cross_firm_mint_item_carries_parameter_firm_and_ids_as_list():
    item = m.item_for("cf-a@opal.invalid", FIRM, IDS_LIST, "$2b$12$" + "x" * 53)
    assert item["firmId"] == {"S": FIRM}
    assert item["allowedFirmIds"] == {"L": [{"S": "firm-a"}, {"S": "firm-c"}]}
    assert item["PK"] == {"S": "USER#cf-a@opal.invalid"}
    assert item["SK"] == {"S": "PROFILE"}
    assert item["status"] == {"S": "active"}


def test_cross_firm_mint_two_emails_give_two_keys(capsys):
    fake = FakeDDB()
    rc1, out1 = _run_mint(capsys, _mint_args(email="cf-a@opal.invalid"), fake)
    rc2, out2 = _run_mint(capsys, _mint_args(email="cf-b@opal.invalid"), fake)
    assert (rc1, rc2) == (0, 0)
    assert out1.splitlines()[0] == "MINT-OK READBACK-OK" and out2.splitlines()[0] == "MINT-OK READBACK-OK"
    assert sorted(fake.items) == ["USER#cf-a@opal.invalid", "USER#cf-b@opal.invalid"]


def test_cross_firm_mint_refuses_email_without_opal_invalid_before_client_call(capsys):
    fake = FakeDDB()
    for bad in ("someone@example.com", "cf-a@opal.invalid.evil.com", "@opal.invalid", "cf a@opal.invalid", ""):
        rc, out = _run_mint(capsys, _mint_args(email=bad), fake)
        assert rc == 1, bad
        assert out.strip() == "MINT-REFUSED args", bad
    assert fake.calls == []


def test_cross_firm_mint_refuses_empty_or_malformed_ids_before_client_call(capsys):
    fake = FakeDDB()
    for bad in ("", " , ", "firm-a,,firm-c", "firm-a, ,firm-c", "firm a"):
        rc, out = _run_mint(capsys, _mint_args(ids=bad), fake)
        assert rc == 1, bad
        assert out.strip() == "MINT-REFUSED args", bad
    assert fake.calls == []


def test_cross_firm_mint_refuses_fwd1_address_before_client_call(capsys):
    fake = FakeDDB()
    for addr in ("fwd1-staff-r41b@opal.invalid", "FWD1-STAFF-R41B@OPAL.INVALID"):
        rc, out = _run_mint(capsys, _mint_args(email=addr), fake)
        assert rc == 1, addr
        assert out.strip() == "MINT-REFUSED args", addr
    assert fake.calls == []


def test_cross_firm_mint_refuses_missing_or_empty_firm_before_client_call(capsys):
    fake = FakeDDB()
    missing = ["--email", "cf-a@opal.invalid", "--allowed-firm-ids", IDS]
    empty = _mint_args(firm="")
    for args in (missing, empty):
        rc, out = _run_mint(capsys, args, fake)
        assert rc == 1
        assert out.strip() == "MINT-REFUSED args"
    assert fake.calls == []


def test_cross_firm_mint_valid_arguments_are_accepted():
    parsed = m.parse_mint_args(_mint_args())
    assert parsed == {"email": "cf-a@opal.invalid", "firm": FIRM, "ids": IDS_LIST}


def test_cross_firm_mint_readback_bad_when_allowed_ids_absent(capsys):
    row = m.item_for("cf-a@opal.invalid", FIRM, IDS_LIST, "$2b$12$" + "x" * 53)
    row.pop("allowedFirmIds")
    assert m.readback_ok(row, FIRM, IDS_LIST) is False
    fake = FakeDDB(get_row=row)
    rc, out = _run_mint(capsys, _mint_args(), fake)
    assert rc == 1
    assert out.strip() == "MINT-OK READBACK-BAD shape"


def test_cross_firm_mint_readback_bad_when_ids_differ(capsys):
    row = m.item_for("cf-a@opal.invalid", FIRM, ["firm-a"], "$2b$12$" + "x" * 53)
    assert m.readback_ok(row, FIRM, IDS_LIST) is False
    rc, out = _run_mint(capsys, _mint_args(), FakeDDB(get_row=row))
    assert rc == 1
    assert out.strip() == "MINT-OK READBACK-BAD shape"


def test_cross_firm_mint_readback_ok_when_shape_matches(capsys):
    row = m.item_for("cf-a@opal.invalid", FIRM, IDS_LIST, "$2b$12$" + "x" * 53)
    assert m.readback_ok(row, FIRM, IDS_LIST) is True
    rc, out = _run_mint(capsys, _mint_args(), FakeDDB(get_row=row))
    assert rc == 0
    assert out.splitlines()[0] == "MINT-OK READBACK-OK"


def test_cross_firm_mint_item_holds_hash_not_password(capsys):
    fake = FakeDDB()
    rc, _ = _run_mint(capsys, _mint_args(), fake)
    assert rc == 0
    stored = fake.items["USER#cf-a@opal.invalid"]
    assert stored["passwordHash"]["S"].startswith("$2b$12$")
    assert PW not in json.dumps(stored)


def test_cross_firm_mint_never_prints_password_or_hash(capsys):
    fake = FakeDDB()
    _run_mint(capsys, _mint_args(), fake)
    out = capsys.readouterr().out
    assert PW not in out
    assert "$2b$" not in out


def test_cross_firm_mint_refuses_stdin_without_password_before_client_call(capsys):
    fake = FakeDDB()
    rc, out = _run_mint(capsys, _mint_args(), fake, stdin_text=json.dumps({"pw": "nope"}))
    assert rc == 1
    assert out.strip() == "MINT-REFUSED input ValueError"
    assert fake.calls == []


def test_cross_firm_mint_remove_refuses_bad_email_before_client_call(capsys):
    fake = FakeDDB()
    rc = m.cmd_remove(["--email", "someone@example.com"], ddb=fake)
    assert rc == 1
    assert capsys.readouterr().out.strip() == "REMOVE-REFUSED args"
    assert fake.calls == []


def test_cross_firm_mint_remove_deletes_the_named_principal_only(capsys):
    fake = FakeDDB()
    _run_mint(capsys, _mint_args(email="cf-a@opal.invalid"), fake)
    _run_mint(capsys, _mint_args(email="cf-b@opal.invalid"), fake)
    rc = m.cmd_remove(["--email", "cf-a@opal.invalid"], ddb=fake)
    out = capsys.readouterr().out
    assert rc == 0
    assert "REMOVE-OK deleted" in out
    assert sorted(fake.items) == ["USER#cf-b@opal.invalid"]


# --- AR-tz-69: the mint reads back its scope and its entitlement rows ---------------------------------------------

PROFILE_ONLY = {"Items": [{"SK": {"S": "PROFILE"}}]}


class ThrottledError(Exception):
    """Stands in for a client error on the scope query; only its type name is ever printed."""


class ScopeDDB(FakeDDB):
    """FakeDDB whose query answers with query_resp or raises query_error. The remove path keeps FakeDDB's query."""

    def __init__(self, query_resp=None, query_error=None, **kw):
        super().__init__(**kw)
        self.query_resp = query_resp
        self.query_error = query_error

    def query(self, **kw):
        self.calls.append(("query", kw))
        if self.query_error is not None:
            raise self.query_error
        if self.query_resp is not None:
            return self.query_resp
        return {"Count": 0}


def test_scope_line_printed_on_green_mint(capsys):
    rc, out = _run_mint(capsys, _mint_args(), ScopeDDB(query_resp=PROFILE_ONLY))
    assert rc == 0
    assert out.splitlines() == ["MINT-OK READBACK-OK", "MINT-SCOPE allowedFirmIds=firm-a,firm-c entitlement_rows=0"]


def test_scope_missing_items_key_counts_as_zero(capsys):
    rc, out = _run_mint(capsys, _mint_args(), FakeDDB())
    assert rc == 0
    assert out.splitlines()[-1] == "MINT-SCOPE allowedFirmIds=firm-a,firm-c entitlement_rows=0"


def test_scope_profile_only_items_count_as_zero():
    assert m.entitlement_rows(PROFILE_ONLY) == 0
    assert m.entitlement_rows({"Items": []}) == 0
    assert m.entitlement_rows({"Count": 0}) == 0


def test_scope_non_profile_items_are_counted_and_profile_is_not(capsys):
    resp = {"Items": [{"SK": {"S": "PROFILE"}}, {"SK": {"S": "GRANT#x"}}, {"SK": {"S": "GRANT#y"}}]}
    assert m.entitlement_rows(resp) == 2
    assert m.entitlement_rows({"Items": [{"SK": {}}]}) == 1


def test_scope_entitlement_rows_refused_with_bad_word(capsys):
    resp = {"Items": [{"SK": {"S": "PROFILE"}}, {"SK": {"S": "GRANT#x"}}, {"SK": {"S": "GRANT#y"}}]}
    rc, out = _run_mint(capsys, _mint_args(), ScopeDDB(query_resp=resp))
    assert rc == 1
    assert out.splitlines() == ["MINT-OK READBACK-BAD entitlement",
                                "MINT-SCOPE allowedFirmIds=firm-a,firm-c entitlement_rows=2"]


def test_scope_query_error_refused_with_type_name(capsys):
    rc, out = _run_mint(capsys, _mint_args(), ScopeDDB(query_error=ThrottledError("boom")))
    assert rc == 1
    assert out.strip() == "MINT-OK READBACK-BAD query ThrottledError"
    assert "MINT-SCOPE" not in out


def test_scope_two_ids_comma_joined_and_one_id_bare(capsys):
    rc, out = _run_mint(capsys, _mint_args(ids="firm-a,firm-c"), ScopeDDB(query_resp=PROFILE_ONLY))
    assert rc == 0 and "MINT-SCOPE allowedFirmIds=firm-a,firm-c entitlement_rows=0" in out.splitlines()
    rc, out = _run_mint(capsys, _mint_args(ids="firm-a"), ScopeDDB(query_resp=PROFILE_ONLY))
    assert rc == 0 and "MINT-SCOPE allowedFirmIds=firm-a entitlement_rows=0" in out.splitlines()


def test_scope_password_and_hash_never_printed(capsys):
    fake = ScopeDDB(query_resp={"Items": [{"SK": {"S": "GRANT#x"}}]})
    rc, out = _run_mint(capsys, _mint_args(), fake)
    stored_hash = fake.items["USER#cf-a@opal.invalid"]["passwordHash"]["S"]
    assert rc == 1
    assert PW not in out
    assert "$2b$" not in out
    assert stored_hash not in out
    assert "passwordHash" not in out


def test_scope_shape_bad_prints_no_scope_line_and_no_query(capsys):
    row = m.item_for("cf-a@opal.invalid", FIRM, IDS_LIST, "$2b$12$" + "x" * 53)
    row.pop("allowedFirmIds")
    fake = ScopeDDB(get_row=row, query_resp=PROFILE_ONLY)
    rc, out = _run_mint(capsys, _mint_args(), fake)
    assert rc == 1
    assert out.strip() == "MINT-OK READBACK-BAD shape"
    assert not any(name == "query" for name, _ in fake.calls)


def test_scope_query_keys_the_principal_partition_consistently(capsys):
    fake = ScopeDDB(query_resp=PROFILE_ONLY)
    rc, _ = _run_mint(capsys, _mint_args(), fake)
    assert rc == 0
    (name, kw), = [c for c in fake.calls if c[0] == "query"]
    assert kw["KeyConditionExpression"] == "PK = :p"
    assert kw["ExpressionAttributeValues"] == {":p": {"S": "USER#cf-a@opal.invalid"}}
    assert kw["ConsistentRead"] is True
    assert kw["ProjectionExpression"] == "SK"
