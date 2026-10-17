"""AR381-y-AC2: the display-name check for the synthetic advisor helper (0.9.0_WK_IRPT_ANLREQ~173, TO-AR-y-381).

Imports fwd1_advisor from the ~172 folder (the edited helper) and builds both items for a fixed date and a fixed clock.
It also builds the same two items from the merged, pre-edit helper, read as bytes from git at the pinned commit
e3e0873d5990d6e930bbb6d699ac635c3a44fe6f (checked against sha256 cc8b8bd5...) and executed in memory: nothing is written
to disk, no AWS call, no boto3 import, no network.

Prints NAME-OK only when the users name and the partner advisorName both equal SYNTHETIC TEST ADVISOR and every other
attribute of both items equals the merged version's; otherwise NAME-BAD <why> and exit 1. The denominator is the count of
other attributes compared across the two items.
"""
import hashlib
import os
import subprocess
import sys
import types

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
HELPER_DIR = os.path.abspath(os.path.join(HERE, "..", "0.9.0_WK_IRPT_ANLREQ~172"))
REL = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~172/fwd1_advisor.py"
MERGED_COMMIT = "e3e0873d5990d6e930bbb6d699ac635c3a44fe6f"
MERGED_SHA256 = "cc8b8bd5f120f3e54bb73b9c82d97ba390207a65e95e769ddf1a2e1706906a34"
WANT = "SYNTHETIC TEST ADVISOR"
DATE = "20261016"
NOW = 1792000000


def bad(why):
    print("NAME-BAD " + why)
    return 1


def merged_source():
    proc = subprocess.run(["git", "show", MERGED_COMMIT + ":" + REL], cwd=HERE, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError("git show rc=%d" % proc.returncode)
    return proc.stdout


def load_merged(raw):
    mod = types.ModuleType("fwd1_advisor_merged")
    mod.__file__ = "<git %s:%s>" % (MERGED_COMMIT, REL)
    exec(compile(raw.decode("utf-8"), mod.__file__, "exec"), mod.__dict__)
    return mod


def build(mod):
    addr = mod.address_for(DATE)
    return mod.user_item(addr, NOW), mod.partner_item(addr, DATE, NOW)


def main():
    try:
        raw = merged_source()
    except Exception as exc:  # noqa: BLE001 -- the reason only; the bytes are not echoed
        return bad("merged helper unreadable from git: %s" % type(exc).__name__)
    got = hashlib.sha256(raw).hexdigest()
    if got != MERGED_SHA256:
        return bad("merged helper sha256 %s, want %s" % (got, MERGED_SHA256))
    sys.path.insert(0, HELPER_DIR)
    import fwd1_advisor as new
    old = load_merged(raw)
    users, partner = build(new)
    old_users, old_partner = build(old)
    if users.get("name") != {"S": WANT} or partner.get("advisorName") != {"S": WANT}:
        return bad("display name is not exact: users.name=%r partner.advisorName=%r"
                   % (users.get("name"), partner.get("advisorName")))
    if set(users) != set(old_users) or set(partner) != set(old_partner):
        return bad("attribute sets differ from the merged helper")
    compared = [("users", k) for k in old_users if k != "name"] + [("partner", k) for k in old_partner if k != "advisorName"]
    changed = []
    for side, key in compared:
        new_item, old_item = (users, old_users) if side == "users" else (partner, old_partner)
        if new_item[key] != old_item[key]:
            changed.append(side + "." + key)
    if changed:
        return bad("other attributes changed: " + ", ".join(changed))
    print("NAME-OK users.name=%s partner.advisorName=%s other attributes unchanged (%d of %d)"
          % (WANT, WANT, len(compared) - len(changed), len(compared)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
