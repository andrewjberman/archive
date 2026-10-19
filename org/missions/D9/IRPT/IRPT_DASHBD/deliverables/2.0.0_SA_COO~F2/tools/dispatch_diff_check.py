"""IRPT_DASHBD (workstream F-SHIP, ~F2): the READ-ONLY check of the live orion-gold-dispatch.sh object against the Inflection pair's dispatch pin (addendum 1, CTO ruling 20261019).

  python <this file>        run from the repository root of the release tree; GET requests and git reads only; line counts, hashes, version ids and one verdict line

The pair uploads the worktree's `data/inf/scripts/gold/orion-gold-dispatch.sh` (the PIN). The CTO's rule: the diff from the LIVE object to the pin must be exactly the pair's own change, and the
pair STOPS if the live object's hash is neither the expected pre-state nor the pin. The pair's own change is the diff `e7d5361cf9 -> 7b206030bfc7` of that file (the round-135 TXN block and the
round-137 ASCII cleanup: 145 changed lines); FB1's change (`4f669b761c -> 9bfa234989`, +3 -10) is common to the live object and the pin and so does not appear in the live-to-pin diff.
Prints, in order: the live latest version (id, time, size, sha256 first 12), whether it is the expected pre-state or the pin, the pin's sha256 first 12, the live-to-pin changed-line count and whether
it equals the pair's own change line for line, whether the live object and the pin carry the transaction launcher call, and the verdict (PRE-STATE-OK, ALREADY-AT-PIN, or STOP with the reason).
"""
import difflib
import hashlib
import subprocess
import sys
from pathlib import Path

import boto3

B, K = "opal-data-inf", "code/gold/orion-gold-dispatch.sh"
P = "data/inf/scripts/gold/orion-gold-dispatch.sh"
PRE_STATE_SHA12 = "9495cd56228b"     # FB1's upload of 2026-10-19T14:22:09Z (the expected pre-state)
PIN_SHA12 = "d2ff692abd23"           # the pair's dispatch pin
PAIR_BASE_REV, PAIR_TOP_REV = "e7d5361cf9", "7b206030bfc7"  # the pair's own change is the diff of these two file images (a commit and a file hash)
PAIR_BASE_COMMIT, PAIR_TOP_COMMIT = "e7d5361cf9", "4f669b761c"  # the commits that carried them
MARKER = "INF_G_01"


def lines_of(raw):
    return raw.decode("utf-8", "replace").splitlines()


def git_show(rev):
    r = subprocess.run(["git", "show", "%s:%s" % (rev, P)], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("git show %s:%s failed" % (rev, P))
    return r.stdout


def changes(a, b):
    out = []
    for ln in difflib.unified_diff(a, b, lineterm="", n=0):
        if ln[:3] in ("---", "+++") or ln.startswith("@@"):
            continue
        out.append(ln)
    return out


def main():
    s3 = boto3.client("s3")
    vers = [x for x in s3.list_object_versions(Bucket=B, Prefix=K).get("Versions", []) if x["Key"] == K]
    latest = next(x for x in vers if x["IsLatest"])
    live_raw = s3.get_object(Bucket=B, Key=K, VersionId=latest["VersionId"])["Body"].read()
    live_sha = hashlib.sha256(live_raw).hexdigest()
    pin_raw = Path(P).read_bytes()
    pin_sha = hashlib.sha256(pin_raw).hexdigest()
    print("live latest: version %s, %s, %d bytes, sha256 %s" % (latest["VersionId"], latest["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"), latest["Size"], live_sha[:12]))
    print("pin (worktree file): %d bytes, sha256 %s (expected %s)" % (len(pin_raw), pin_sha[:12], PIN_SHA12))
    live, pin = lines_of(live_raw), lines_of(pin_raw)
    pair = changes(lines_of(git_show(PAIR_BASE_COMMIT)), lines_of(git_show(PAIR_TOP_COMMIT)))
    d = changes(live, pin)
    equal = d == pair
    print("pair's own change (%s -> %s): %d changed lines" % (PAIR_BASE_COMMIT, PAIR_TOP_COMMIT, len(pair)))
    print("live -> pin: %d changed lines; equals the pair's own change line for line: %s" % (len(d), equal))
    print("transaction launcher call (%s) in live: %s; in pin: %s" % (MARKER, any(MARKER in x for x in live), any(MARKER in x for x in pin)))
    if pin_sha[:12] != PIN_SHA12:
        verdict = "STOP the pin is %s, not %s" % (pin_sha[:12], PIN_SHA12)
    elif live_sha[:12] == PIN_SHA12:
        verdict = "ALREADY-AT-PIN"
    elif live_sha[:12] != PRE_STATE_SHA12:
        verdict = "STOP the live object %s is neither the expected pre-state %s nor the pin" % (live_sha[:12], PRE_STATE_SHA12)
    elif not equal:
        verdict = "STOP the live-to-pin diff is not the pair's own change"
    elif any(MARKER in x for x in live):
        verdict = "STOP the live object already carries the transaction launcher call"
    else:
        verdict = "PRE-STATE-OK"
    print("VERDICT: %s" % verdict)
    return 0 if verdict in ("PRE-STATE-OK", "ALREADY-AT-PIN") else 1


if __name__ == "__main__":
    sys.exit(main())
