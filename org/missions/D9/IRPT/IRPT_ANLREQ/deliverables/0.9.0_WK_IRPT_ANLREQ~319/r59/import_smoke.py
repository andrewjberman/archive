"""IRPT_ANLREQ release 37 version 2 smoke (cell AR-y-441, worker 0.9.0_WK_IRPT_ANLREQ~319). Stdlib only, ASCII only.

    python -I import_smoke.py <built irpt-ycharts-generate.zip> > IMPORT_SMOKE.txt

Extracts the built zip into a private folder (removed on exit) that is the only extra sys.path entry; python -I adds no
script or working-directory entry. Prints one result line per check. The behaviour check runs ticket_confirmation.make_confirm_ticket
over an in-memory DynamoDB-shaped fake: an analysis_request filed through /tickets (source portal, created_by = the principal)
must be confirmed for that principal and must not be confirmed for another principal. No network, no AWS call.
"""
import hashlib
import importlib
import os
import shutil
import sys
import tempfile
import zipfile

PRINCIPAL = "smoke.creator@example.test"
OTHER = "smoke.other@example.test"
TICKET = "TCK-20261020-0a1b2c3d"
TABLE = "tickets"


class FakeDynamo:
    def __init__(self, item):
        self.item = item

    def get_item(self, **kwargs):
        return {"Item": self.item}


def ticket_item():
    return {
        "ticket_id": {"S": TICKET},
        "ticket_type": {"S": "analysis_request"},
        "source": {"S": "portal"},
        "created_by": {"S": PRINCIPAL},
        "requester": {"M": {"email": {"S": "someone.else@example.test"}}},
    }


def attempt(label, action):
    try:
        action()
        print("%s=ok" % label)
    except Exception as exc:
        first = (str(exc).splitlines() or [""])[0][:160]
        print("%s=FAIL %s %s" % (label, type(exc).__name__, first))


def behave():
    try:
        module = importlib.import_module("ticket_confirmation")
        confirm = module.make_confirm_ticket(FakeDynamo(ticket_item()), TABLE)
        print("confirm_created_by=%s" % ("true" if confirm(TICKET, PRINCIPAL) is True else "false"))
        print("other=%s" % ("true" if confirm(TICKET, OTHER) is True else "false"))
    except Exception as exc:
        print("behaviour=FAIL %s" % type(exc).__name__)


def main(zip_path):
    with open(zip_path, "rb") as handle:
        digest = hashlib.sha256(handle.read()).hexdigest()
    print("# release 37 version 2 smoke: the BUILT %s sha256=%s, extracted to a private folder, python -I, that folder the only extra sys.path entry"
          % (os.path.basename(zip_path), digest))
    folder = tempfile.mkdtemp(prefix="r37v2_smoke_")
    try:
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(folder)
        sys.path.insert(0, folder)
        attempt("import_served", lambda: importlib.import_module("served"))
        attempt("import_generate_installed", lambda: importlib.import_module("generate_installed"))
        attempt("import_ticket_confirmation", lambda: importlib.import_module("ticket_confirmation"))
        behave()
    finally:
        shutil.rmtree(folder)
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("R37V2-SMOKE-USAGE import_smoke.py <zip>")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
