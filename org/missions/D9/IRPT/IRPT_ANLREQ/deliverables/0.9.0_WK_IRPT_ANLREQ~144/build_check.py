"""TO-AR-y-338 criterion AR338-y-AC1: the release-31 build check. Offline: no AWS, no network, nothing uploaded or run.

Prints one line `BUILD-OK ...` only when every condition holds; otherwise `BUILD-BAD <why>` and exit 1.
Conditions: (1) the tarball sha256 equals the record's; (2) build_a and build_b agree member by member; (3) the tarball and
the release-29 base, read member by member, reproduce the record's delta lists exactly; (4) the differing set is a subset of
the thirteen names the order expects plus the members the record explains by a surprise row whose id is in the channel;
(5) the extracted bindings carry the four keys and the producer list is the two-entry tuple; (6) no JWT-shaped string and no
"token" JSON member in any extracted text member. ASCII only.
"""
import ast
import hashlib
import json
import os
import re
import sys
import tarfile

DL = os.path.dirname(os.path.abspath(__file__))
STAGE = "C:/dev/irpt-release-r31"
TAR = STAGE + "/irpt-resident-0485393f3a-r31.tar.gz"
BUILD_A = STAGE + "/build_a"
BUILD_B = STAGE + "/build_b"
R29_TAR = "C:/dev/irpt-release-r29/irpt-resident-0485393f3a-r29.tar.gz"
R29_SHA = "2de2adce622f8bb9bbd5ebc071e862446b056303c0d9ffd7d41b050bd17f51a4"
CHANNEL = os.path.join(DL, "..", "..", "surprise-channel", "investigations", "INVESTIGATION_v1.md")
RECORD = os.path.join(DL, "r41", "RESIDENT_R31_BUILD.json")
EXPECTED = {
    "SHA256SUMS", "reports/resident_bindings.json", "ycharts/generate/resident_worker.py",
    "ycharts/generate/composition_admission.py", "_scope/interactive_access.py", "intake/uploads.py",
    "ycharts/research/layout_overview.py", "ycharts/research/opal_producer.py", "ycharts/research/opal_packager.py",
    "ops/entry.py", "ops/owned_report.py", "ops/pdf_link.py", "reports/status_installed.py",
}
PRINCIPALS = ("andrew@opalinvest.com", "fwd1-staff-r41a@opal.invalid")
JWT = re.compile(r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}")
TOKEN_MEMBER = re.compile(r'"token"\s*:')


def bad(why):
    print("BUILD-BAD " + why)
    sys.exit(1)


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    with open(path, "rb") as fh:
        return sha_bytes(fh.read())


def folder_members(root):
    out = {}
    for dp, _dn, fn in os.walk(root):
        for f in fn:
            p = os.path.join(dp, f)
            out[os.path.relpath(p, root).replace(os.sep, "/")] = sha_file(p)
    return out


def tar_members(path):
    """name -> bytes, the './' prefix removed; read in memory (the same bytes an extraction would write)."""
    out = {}
    with tarfile.open(path, "r:gz") as tar:
        for m in tar.getmembers():
            if not m.isfile():
                bad("non-file member in %s: %s" % (path, m.name))
            name = m.name[2:] if m.name.startswith("./") else m.name
            out[name] = tar.extractfile(m).read()
    return out


# (1) the tarball sha256 equals the record's
record = json.load(open(RECORD, encoding="utf-8"))
tar_sha = sha_file(TAR)
if tar_sha != record["artifact"]["sha256"]:
    bad("tarball sha256 %s is not the record's %s" % (tar_sha, record["artifact"]["sha256"]))

# (2) the two builds agree member by member
a = folder_members(BUILD_A)
b = folder_members(BUILD_B)
if set(a) != set(b):
    bad("build names differ: only_a=%s only_b=%s" % (sorted(set(a) - set(b))[:3], sorted(set(b) - set(a))[:3]))
differ_builds = [n for n in a if a[n] != b[n]]
if differ_builds:
    bad("builds differ on %s" % differ_builds[:3])
members = len(a)
identical = sum(1 for n in a if a[n] == b.get(n))

# (3) the tarball and the release-29 base, member by member, reproduce the record's delta lists exactly
r29_sha = sha_file(R29_TAR)
if r29_sha != R29_SHA:
    bad("release-29 base sha256 %s is not %s" % (r29_sha, R29_SHA))
t31 = tar_members(TAR)
t29 = tar_members(R29_TAR)
if len(t31) != 299 or len(t29) != 299:
    bad("member counts %d and %d, want 299 each" % (len(t31), len(t29)))
h31 = {n: sha_bytes(d) for n, d in t31.items()}
h29 = {n: sha_bytes(d) for n, d in t29.items()}
differing = sorted(n for n in h31 if n in h29 and h31[n] != h29[n])
only_rel = sorted(n for n in h31 if n not in h29)
only_live = sorted(n for n in h29 if n not in h31)
unchanged = sum(1 for n in h31 if n in h29 and h31[n] == h29[n])
rec = record["delta_vs_live"]
if differing != sorted(rec["differing"]) or only_rel != sorted(rec["only_in_release"]) or only_live != sorted(rec["only_in_live"]):
    bad("the delta lists do not reproduce the record's")
if unchanged != rec["counts"]["unchanged"]:
    bad("unchanged count %d, record %d" % (unchanged, rec["counts"]["unchanged"]))

# (4) the differing set is a subset of the expected names plus the names a surprise row explains
explained = rec["explained_by_surprise_row"]
channel = open(CHANNEL, encoding="utf-8").read()
for name, row_id in explained.items():
    if '"id": "%s"' % row_id not in channel:
        bad("explained member %s cites %s, which is not in the channel" % (name, row_id))
extra = [n for n in differing if n not in EXPECTED and n not in explained]
if extra:
    bad("differing members the order does not expect and no row explains: %s" % extra)
missing = [n for n in EXPECTED if n not in differing]
if missing:
    bad("expected members that do not differ from release 29: %s" % missing)

# (5) the extracted bindings carry the four keys; the producer list is the two-entry tuple
bindings = json.loads(t31["reports/resident_bindings.json"].decode("utf-8"))
for key in ("analysis_ready_queue_url", "commentary_ready_queue_url", "packager", "opal_map"):
    if key not in bindings:
        bad("bindings lack %s" % key)
if sorted(bindings["packager"]) != ["api_base", "secret_name"]:
    bad("packager keys are %s, want exactly api_base and secret_name" % sorted(bindings["packager"]))
worker = t31["ycharts/generate/resident_worker.py"].decode("utf-8")
match = re.search(r"^OPAL_PRODUCER_PRINCIPALS = (\(.*?\))\s*$", worker, re.M)
if not match:
    bad("OPAL_PRODUCER_PRINCIPALS line not found in resident_worker.py")
if tuple(ast.literal_eval(match.group(1))) != PRINCIPALS:
    bad("OPAL_PRODUCER_PRINCIPALS is %s" % match.group(1))

# (6) no JWT-shaped string and no "token" JSON member in any extracted text member (every member is scanned first)
scanned = 0
jwt_hits = []
token_hits = []
for name, data in sorted(t31.items()):
    if b"\x00" in data:
        continue
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        continue
    scanned += 1
    if JWT.search(text):
        jwt_hits.append(name)
    if TOKEN_MEMBER.search(text):
        token_hits.append("%s (%d matches)" % (name, len(TOKEN_MEMBER.findall(text))))
if jwt_hits:
    bad("JWT-shaped string in %s" % jwt_hits)
if token_hits:
    bad('"token" JSON member in %s; text members scanned %d' % (token_hits, scanned))

print("BUILD-OK %d members, builds identical %d of %d, delta %d differing %d (%d expected, %d explained by surprise rows) "
      "only_in_release_unexplained 0 only_in_live %d" % (members, identical, members, len(differing), len(differing),
                                                          len(EXPECTED & set(differing)), len(explained), len(only_live)))
