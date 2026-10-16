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
    assert out1.strip() == "MINT-OK READBACK-OK" and out2.strip() == "MINT-OK READBACK-OK"
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
    assert out.strip() == "MINT-OK READBACK-OK"


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
