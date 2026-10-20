"""Grade a built resident tarball against the running r34m tarball: the one bindings value that changes is packager.api_base (READ ONLY: nothing is built, uploaded, installed or run; offline).

usage: python -I check_packager_base.py <new tarball> <old tarball>

Prints PACKAGER-BASE-OK api_base=https://opalinvest.dev secret=opal/ticketing/svc-irpt-packager other_members_equal=yes (rc 0) only when:
the new bindings packager.api_base equals https://opalinvest.dev; the old packager.api_base is the direct API Gateway host (so the value did change);
packager.secret_name is unchanged and equals opal/ticketing/svc-irpt-packager; every other top-level bindings key equals the old value;
the two tarballs hold the same member names and every member other than SHA256SUMS and reports/resident_bindings.json has the same sha256.
Otherwise prints PACKAGER-BASE-BAD <why> and exits 1. ASCII only.
"""
import hashlib
import json
import sys
import tarfile

API_BASE = "https://opalinvest.dev"
OLD_API_BASE = "https://7k3ed8px20.execute-api.us-east-1.amazonaws.com"
SECRET = "opal/ticketing/svc-irpt-packager"
BINDINGS = "reports/resident_bindings.json"
SUMS = "SHA256SUMS"


def bad(why):
    print("PACKAGER-BASE-BAD %s" % why)
    return 1


def member_name(raw):
    return raw[2:] if raw.startswith("./") else raw


def read_bindings(path):
    with tarfile.open(path, "r:gz") as tar:
        for mem in tar.getmembers():
            if mem.isfile() and member_name(mem.name) == BINDINGS:
                return json.loads(tar.extractfile(mem).read().decode("utf-8"))
    return None


def member_digests(path):
    out = {}
    with tarfile.open(path, "r:gz") as tar:
        for mem in tar.getmembers():
            if mem.isfile():
                data = tar.extractfile(mem).read()
                out[member_name(mem.name)] = hashlib.sha256(data).hexdigest()
    return out


def main(argv):
    if len(argv) != 2:
        print("usage: check_packager_base.py <new tarball> <old tarball>")
        return 2
    new_path, old_path = argv
    new_b, old_b = read_bindings(new_path), read_bindings(old_path)
    if new_b is None or old_b is None:
        return bad("%s is absent from a tarball (new present %s, old present %s)" % (BINDINGS, new_b is not None, old_b is not None))
    new_p, old_p = new_b.get("packager"), old_b.get("packager")
    if not isinstance(new_p, dict) or not isinstance(old_p, dict):
        return bad("packager is not an object in both bindings: new %r old %r" % (new_p, old_p))
    if new_p.get("api_base") != API_BASE:
        return bad("new packager.api_base is %r, want %s" % (new_p.get("api_base"), API_BASE))
    if old_p.get("api_base") != OLD_API_BASE:
        return bad("old packager.api_base is %r, want the direct host %s" % (old_p.get("api_base"), OLD_API_BASE))
    if new_p.get("secret_name") != old_p.get("secret_name") or new_p.get("secret_name") != SECRET:
        return bad("packager.secret_name new %r old %r, want unchanged %s" % (new_p.get("secret_name"), old_p.get("secret_name"), SECRET))
    if set(new_p) != set(old_p):
        return bad("packager keys differ: new %s old %s" % (sorted(new_p), sorted(old_p)))
    for key in sorted(set(new_b) | set(old_b)):
        if key != "packager" and new_b.get(key) != old_b.get(key):
            return bad("bindings key %s differs from the old value" % key)
    new_m, old_m = member_digests(new_path), member_digests(old_path)
    only_new = sorted(set(new_m) - set(old_m))
    only_old = sorted(set(old_m) - set(new_m))
    if only_new or only_old:
        return bad("member names differ: only new %s, only old %s" % (only_new[:5], only_old[:5]))
    differ = sorted(n for n in new_m if n not in (SUMS, BINDINGS) and new_m[n] != old_m[n])
    if differ:
        return bad("members differ beyond SHA256SUMS and the bindings: %s" % differ[:10])
    print("PACKAGER-BASE-OK api_base=%s secret=%s other_members_equal=yes" % (API_BASE, SECRET))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
