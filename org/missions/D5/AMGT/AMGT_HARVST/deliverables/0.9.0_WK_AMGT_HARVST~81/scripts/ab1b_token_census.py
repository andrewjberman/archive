"""HVST-ab-1 phase B: the per-publisher token-source census. NAMES and PATHS only.

For each publisher: the Secrets secret NAME its sign-in reads, the Secrets secret NAME of its stored
session (if it has one), and the saved-session file (existence and mtime, never opened). Secrets are
touched by LIST and DESCRIBE only -- `get_secret_value` is never called (asserted: the client below
refuses it), so no secret VALUE is read, printed, logged or written.

This runs in its own process (called by ab1_ac2_seed_and_replay.py) because the AC2 process blocks
sockets for the whole replay; these are AWS control-plane calls, not a publisher call.
"""

import datetime as dt
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[7]
sys.path.insert(0, str(REPO))

from lib.opal_data_harvest.credentials import CREDENTIAL_SECRETS, PUBLISHERS, SESSION_SECRETS, SecretsReader  # noqa: E402

RUNTIME = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / ".runtime/opal-data-harvest"
TOKENS = ("session", "dowjones", "wsj", "barrons")


class ListDescribeOnly:
    """Wraps the Secrets client: counts list/describe calls and REFUSES every other call."""

    def __init__(self, client):
        self._client, self.calls = client, {}

    def __getattr__(self, name):
        if name not in ("list_secrets", "describe_secret"):
            raise AssertionError("census may only list/describe, not %s" % name)
        self.calls[name] = self.calls.get(name, 0)

        def call(**kwargs):
            self.calls[name] += 1
            return getattr(self._client, name)(**kwargs)
        return call


def main():
    import boto3
    guarded = ListDescribeOnly(boto3.client("secretsmanager", region_name="us-east-1"))
    reader = SecretsReader(client=guarded)
    census = reader.census()
    print("secrets in the account (list_secrets, names only): %d" % census["listed"])
    names, token = [], None
    while True:
        page = guarded.list_secrets(**({"NextToken": token} if token else {}))
        names += [entry["Name"] for entry in page.get("SecretList", [])]
        token = page.get("NextToken")
        if not token:
            break
    related = sorted(n for n in names if any(part in n.lower() for part in TOKENS))
    print("secret names mentioning session/dowjones/wsj/barrons (%d of %d): %s" % (len(related), len(names), ", ".join(related)))
    for publisher in PUBLISHERS:
        credential, session = CREDENTIAL_SECRETS[publisher], SESSION_SECRETS.get(publisher)
        file = RUNTIME / "secrets" / (publisher + ".dpapi")
        row_c = census["secrets"][credential]
        line = "%-8s credentials=%s [%s, changed %s]" % (publisher, credential, "exists" if row_c["described"] else "ABSENT",
                                                        row_c["last_changed"])
        if session:
            row_s = census["secrets"][session]
            line += " | stored session=%s [%s, changed %s]" % (session, "exists" if row_s["described"] else "ABSENT", row_s["last_changed"])
            line += " | token order: Secrets session, then saved-session file"
        else:
            line += " | stored session=none in Secrets | token order: saved-session file"
        if file.exists():
            mtime = dt.datetime.fromtimestamp(file.stat().st_mtime, dt.timezone.utc).isoformat()
            line += " | saved-session file=%s [exists, mtime %s]" % (file.as_posix(), mtime)
        else:
            line += " | saved-session file=%s [ABSENT]" % file.as_posix()
        print(line)
    print("AWS control-plane calls: %s; get_secret_value calls: 0 (the client refuses it); publisher calls: 0"
          % ", ".join("%s=%d" % item for item in sorted(guarded.calls.items())))


if __name__ == "__main__":
    main()
