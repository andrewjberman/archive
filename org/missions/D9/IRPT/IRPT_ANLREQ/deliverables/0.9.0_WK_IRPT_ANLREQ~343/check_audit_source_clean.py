"""IRPT_ANLREQ AR-y-469 AC3: does the live audit source return an e-mail address or a display name in any value?

Stdlib only, offline, no AWS call. Runs ycharts/generate/ticket_audit_source.make_audit_source against a fake DynamoDB
client whose analysis_request item carries an e-mail address (requester.email, created_by) and a display name
(requester.name). Prints AUDIT-SOURCE-CLEAN-OK no_email=yes no_name=yes only when the source answered a value AND no
string in that value (key or value, at any depth) contains the address or the name. Otherwise AUDIT-SOURCE-CLEAN-BAD <why>.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
GENERATE = ROOT / "infra" / "aws" / "lambda" / "investor-reporting" / "ycharts" / "generate"
sys.path.insert(0, str(GENERATE))

from ticket_audit_source import make_audit_source  # noqa: E402

TICKET = "TCK-20261020-9f8e7d6c"
FIRM = "ACME"
EMAIL = "adv.ops@acme-capital.example"
NAME = "Dana Requester"


class FakeDynamo:
    def __init__(self, item):
        self.item = item

    def get_item(self, **kwargs):
        return {"Item": self.item}


def fake_item():
    return {
        "ticket_id": {"S": TICKET},
        "ticket_type": {"S": "analysis_request"},
        "created_by": {"S": EMAIL},
        "created_at": {"S": "2026-10-20T18:46:38.123Z"},
        "source": {"S": "dashboard_form:" + FIRM},
        "requester": {"M": {"email": {"S": EMAIL}, "name": {"S": NAME}, "firm": {"S": FIRM}}},
        "answers": {"M": {"firm": {"S": FIRM}, "advisor": {"S": "A-100"}, "household": {"S": "HH-7"},
                          "report_type": {"S": "standard"}}},
    }


def strings(value):
    """Every string in a nested value, keys and values alike."""
    if isinstance(value, dict):
        for key, part in value.items():
            yield from strings(key)
            yield from strings(part)
    elif isinstance(value, (list, tuple)):
        for part in value:
            yield from strings(part)
    elif isinstance(value, str):
        yield value
    else:
        yield str(value)


def main():
    got = make_audit_source(FakeDynamo(fake_item()), "tickets-table")(FIRM, TICKET)
    if got is None:
        print("AUDIT-SOURCE-CLEAN-BAD no_output (the source answered None, so nothing was tested)")
        return 1
    seen = list(strings(got))
    email_hit = any(EMAIL in text for text in seen)
    name_hit = any(NAME in text for text in seen)
    if email_hit or name_hit:
        print("AUDIT-SOURCE-CLEAN-BAD email_in_output=%s name_in_output=%s" % (email_hit, name_hit))
        return 1
    print("AUDIT-SOURCE-CLEAN-OK no_email=yes no_name=yes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
