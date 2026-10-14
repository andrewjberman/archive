"""TO-AR-y-338 step 4: derive the four release-31 host scripts from the release-30 set (the AR-y-324 method, shifted to release 31).

usage: python -I make_scripts_r31.py <r30 scripts dir> <dst dir> <extracted r31 root> <extracted r29 root> <r31 tarball>

Every source script is verified against its sha256 in the AR-y-324 record first. The member set is read from the two
extracted trees (never typed): the members whose bytes differ between release 29 and release 31 are the member checks.
Every explicit substitution names its exact text and its count; any other count REFUSES. Writes four files and nothing
else; nothing is run; ASCII only.
"""
import hashlib
import os
import re
import sys

SRC, DST, X31, X29, TAR = sys.argv[1:6]
SUMS = "SHA256SUMS"
BINDINGS = "reports/resident_bindings.json"
EXPECT_TAR = "cc6581ed3ff040046c04b202f110a2cb7dc679d79dafb1a6380c64a52c330db8"
EXPECT_LIB = "a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841"
EXPECT_WRAP = "55ddb8f7947cba7cdca1b9139d4d0a1a3ad620e330c86ba3ab648d334763aff9"
SRC_SHA = {
    "pre_read_r30.sh": "5e64d565617d9aa9e3f365e7743fecf827ac81a139341af7541f177f0400d49f",
    "install_r30.sh": "d8c260c8a1f48599acede8201483eb6ed03aefee0a5b1d50cbb9fb9a603c5748",
    "rollback_r30.sh": "b1760649af38b162de9b3e094038f9357eb9881297a611c839172f2e8ab8825c",
    "resident_host_install_0485393f3a-r30.sh": "2e72c822c05f1522dc44f4764e2a24dc1f02f4b6c684ed7a0b460bfd0d0efdb9",
}


def sha_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def refuse(why):
    raise SystemExit("REFUSE: " + why)


for name, want in SRC_SHA.items():
    got = sha_file(os.path.join(SRC, name))
    if got != want:
        refuse("source %s sha256 %s, want %s" % (name, got, want))
if sha_file(TAR) != EXPECT_TAR:
    refuse("tarball sha256 %s, want %s" % (sha_file(TAR), EXPECT_TAR))
for name, want in (("ycharts-host/ycharts_session.js", EXPECT_LIB), ("ycharts-host/run-ycharts-session.sh", EXPECT_WRAP)):
    if sha_file(os.path.join(X31, *name.split("/"))) != want:
        refuse("extracted %s is not the built member" % name)


def walk(root):
    names = []
    for dp, _dn, fn in os.walk(root):
        for f in fn:
            names.append(os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/"))
    return sorted(names)


n31, n29 = walk(X31), walk(X29)
if set(n31) != set(n29):
    refuse("member sets differ: only31=%s only29=%s" % (sorted(set(n31) - set(n29)), sorted(set(n29) - set(n31))))
R31 = {n: sha_file(os.path.join(X31, *n.split("/"))) for n in n31}
R29 = {n: sha_file(os.path.join(X29, *n.split("/"))) for n in n29}
DIFF = [n for n in n31 if R31[n] != R29[n]]
if len(DIFF) != 14:
    refuse("differing members %d, want 14: %s" % (len(DIFF), DIFF))
PKG = [n for n in DIFF if n not in (SUMS, BINDINGS)]
if len(PKG) != 12:
    refuse("package members differing %d, want 12" % len(PKG))
TAR_SHA = sha_file(TAR)
SUMS_SHA = R31[SUMS]
SHIFT = re.compile(r"(?<![0-9A-Za-z])(r|release[- ])30(?![0-9])")


def shift(text):
    return SHIFT.sub(lambda m: m.group(1) + "31", text)


def rep(text, old, new, count=1):
    got = text.count(old)
    if got != count:
        refuse("%d matches (want %d) for %r" % (got, count, old[:90]))
    return text.replace(old, new)


def write(name, text):
    if any(ord(c) > 127 for c in text):
        refuse("%s: non-ASCII" % name)
    data = text.encode("ascii")
    path = os.path.join(DST, name)
    with open(path, "wb") as fh:
        fh.write(data)
    print("wrote %s bytes=%d sha256=%s" % (name, len(data), sha_file(path)))
    return path


def load(name):
    with open(os.path.join(SRC, name), "rb") as fh:
        return fh.read().decode("ascii")


def split_header(text, anchor):
    """Lines before the first line starting with anchor are the old header; the rest is kept."""
    lines = text.split("\n")
    idx = next(i for i, ln in enumerate(lines) if ln.startswith(anchor))
    return lines[idx:]


def loop_block(label, entries, body):
    out = ['echo "%s"' % label, "for ent in \\"]
    for i, n in enumerate(entries):
        tail = "; do" if i == len(entries) - 1 else " \\"
        out.append('  "%s %s"%s' % (n, R31[n] if body == "r31" else R29[n], tail))
    return out


def loop_body(prefix, label_src):
    return ["  set -- $ent", '  GOT=$(sha256sum $RUN/$1 | cut -d\' \' -f1)',
            '  echo "%s member $1 sha256 $GOT (want $2) $([ "$GOT" = "$2" ] && echo MATCH || echo MISMATCH)"' % prefix,
            "done"]


def replace_line_block(lines, first_prefix, new_lines, must_end_with=None):
    """Replace the single line starting with first_prefix by new_lines (exactly one such line)."""
    hits = [i for i, ln in enumerate(lines) if ln.startswith(first_prefix)]
    if len(hits) != 1:
        refuse("%d lines start with %r, want 1" % (len(hits), first_prefix[:70]))
    i = hits[0]
    return lines[:i] + new_lines + lines[i + 1:]


# ---------------------------------------------------------------- host script
host_src = load("resident_host_install_0485393f3a-r30.sh")
host = shift(host_src)
host = rep(host, "WANT_TAR=a08864f9dbd3f3b832273c3a12bbdb2ccb5f9b492d5bd758762651011f4114f6", "WANT_TAR=" + TAR_SHA)
lines = host.split("\n")
assert lines[0] == "set -uo pipefail", lines[0]
body = split_header(host, "NEW=")
HOST_HEADER = [
    "# Ledger irpt-resident-r31-20261014: resident root 0485393f3a-r29 -> 0485393f3a-r31 (the r29 member set with the trunk blobs of the",
    "# twelve package members that the merged cells of AR-y-318, AR-y-319, AR-y-327, AR-y-330, AR-y-331, AR-y-333 and AR-y-336 change, the package sums and the",
    "# bindings replaced; base pin 0485393f3a, package pin c4c2afe89639071f41242fc9f663cadaffa0ffd8), and the 0485393f3a-r29 root and its library stay on the host for rollback.",
    "# Copy of the r30 script with NEW, WANT_TAR, the member checks (one per differing member, equal to the extracted r31 tarball), the ledger and this header changed;",
    "# written by 0.9.0_WK_IRPT_ANLREQ~144 for 2.0.0_SA_COO~Y2 (TO-AR-y-338, build only); operator 0.7.0_AE_CloudOps~YC2. Authoring this script uploaded, installed and applied nothing.",
]
body = [ln for ln in body if not ln.startswith('check "')]
anchor = "check ycharts-host/ycharts_session.js $WANT_LIBRARY"
pos = [i for i, ln in enumerate(body) if ln == anchor]
if len(pos) != 1:
    refuse("library check line count %d" % len(pos))
checks = ['check "%s" %s' % (n, R31[n]) for n in sorted(DIFF)]
body = body[:pos[0]] + checks + body[pos[0]:]
host_text = "\n".join(["set -uo pipefail"] + HOST_HEADER + body)
HOST_NAME = "resident_host_install_0485393f3a-r31.sh"
host_path = write(HOST_NAME, host_text)
HOST_SHA = sha_file(host_path)
quoted = [ln for ln in host_text.split("\n") if ln.startswith('check "')]
print("host quoted member-check lines: %d" % len(quoted))

# ---------------------------------------------------------------- install
ins = shift(load("install_r30.sh"))
ilines = ins.split("\n")
ibody = split_header(ins, "NEW=")
INS_HEADER = [
    "# Ledger irpt-resident-r31-20261014, legs D2 + V1: fetch the signed r31 install script BY KEY (the host role holds GetObject, not GetObjectVersion), verify its sha256",
    "# (it binds the bytes), run it (it stages the tar, checks every changed member, reinstalls the library with the same bytes, keeps the r29 root and library for rollback and rolls both",
    "# back itself on a failed start), then read the running package back. Sent through Systems Manager by host_read.py. No vendor call.",
    "# Written under IRPT_ANLREQ.TO-AR-y-338 (worker 0.9.0_WK_IRPT_ANLREQ~144). NOT RUN: the applier 0.7.0_AE_CloudOps~YC2 runs it under a later order.",
    "# Derived from install_r30.sh (release 30) by the AR-y-301 method. Changed: NEW, WANT, WANTSUM; a guard before the fetch that refuses unless the running root is",
    "# 0485393f3a-r29 (exit 34) and the unit carries no IRPT_ANALYSIS_READY_QUEUE_URL (exit 35); the release-31 member table (twelve members, each at its release-31 sha256);",
    "# the expected producer list printed and read back; the imports of layout_overview and opal_producer. Every fetch, sha256 and refusal guard of install_r30.sh is kept with its exit code.",
]
ibody = [ln for ln in ibody]
ibody = rep("\n".join(ibody), "WANT=2e72c822c05f1522dc44f4764e2a24dc1f02f4b6c684ed7a0b460bfd0d0efdb9", "WANT=" + HOST_SHA).split("\n")
ibody = rep("\n".join(ibody), "WANTSUM=1ae1df0d147f529fdfc0d05f09dff83f23f156ec17d982b3419492f8531f4812", "WANTSUM=" + SUMS_SHA).split("\n")
GUARD = [
    'RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)',
    '[ "$RUN" = "$R/$OLD" ] || { echo "ERROR: the running root is ${RUN:-none}, not $R/$OLD; nothing moved"; exit 34; }',
    "UNITENV=$(systemctl show $UNIT -p Environment --value | grep -c IRPT_ANALYSIS_READY_QUEUE_URL)",
    '[ "$UNITENV" = 0 ] || { echo "ERROR: the unit carries IRPT_ANALYSIS_READY_QUEUE_URL; nothing moved"; exit 35; }',
    'echo "R31 guard: running root $RUN (want $R/$OLD); unit IRPT_ANALYSIS_READY_QUEUE_URL count $UNITENV (want 0)"',
]
ibody = replace_line_block(ibody, 'aws s3 cp "s3://opal-313476888478-lambda-artifacts/$KEY" $T', GUARD + ['aws s3 cp "s3://opal-313476888478-lambda-artifacts/$KEY" $T'])
ibody = replace_line_block(ibody, 'echo "V1 P2b release-31 members', [
    'echo "V1 P2b release-31 members (each wanted value is the release-31 build record sha256 of the member):"'])
# the for-loop that the label line introduces: replace the old ten-member list and its body
start = next(i for i, ln in enumerate(ibody) if ln == 'for ent in \\')
end = next(i for i in range(start, len(ibody)) if ibody[i].endswith("; do"))
old_body_end = next(i for i in range(end, len(ibody)) if ibody[i] == "done")
new_loop = loop_block("", PKG, "r31")[1:]
ibody = ibody[:start] + new_loop + loop_body("V1 P2b", "")[0:0] + ibody[end + 1:]
# the body after '; do' is the set/GOT/echo/done lines: keep them as they were (they are generic)
ibody = rep("\n".join(ibody), 'import opal_packager  # noqa: F401',
            'import opal_packager  # noqa: F401\nimport layout_overview  # noqa: F401\nimport opal_producer  # noqa: F401').split("\n")
ibody = replace_line_block(ibody, 'echo "V1 worker sha256 ', [
    'echo "V1 worker sha256 $(sha256sum $RUN/ycharts/generate/resident_worker.py | cut -d\' \' -f1) (want %s; release-29 %s)"' % (R31["ycharts/generate/resident_worker.py"], R29["ycharts/generate/resident_worker.py"]),
    'echo "V1 expected producer list (release 31, two entries): andrew@opalinvest.com fwd1-staff-r41a@opal.invalid; running: $(grep -m1 \'^OPAL_PRODUCER_PRINCIPALS\' $RUN/ycharts/generate/resident_worker.py)"',
])
install_text = "\n".join(["set -u"] + INS_HEADER + ibody)
write("install_r31.sh", install_text)

# ---------------------------------------------------------------- pre-read
pre = shift(load("pre_read_r30.sh"))
plines = split_header(pre, "R=/opt/irpt-resident")
PRE_HEADER = [
    "set -u",
    "# Ledger irpt-resident-r31-20261014, leg P1 (READ ONLY): the host state before the r31 install (expect the r29 root running, the library and wrapper unmoved, the r31 root absent). No write, no vendor call.",
    "# Written under IRPT_ANLREQ.TO-AR-y-338 (worker 0.9.0_WK_IRPT_ANLREQ~144). NOT RUN: the applier 0.7.0_AE_CloudOps~YC2 runs it under a later order.",
    "# Derived from pre_read_r30.sh by the AR-y-301 method, shifted to release 31. Changed: the fail-closed running-root read (STOP-READ-0, exit 40), the release-31 member read-back",
    "# (the twelve members the release changes, each at its release-29 sha256), the worker read-back (release 29), the receipt ledger (r29), and the release-31 wording of the stop-reads.",
]
ptext = "\n".join(plines)
ptext = rep(ptext, "RUN=$(systemctl show $UNIT -p ExecStart | grep -o \"$R/[0-9a-z-]*\" | head -1)",
            "RUN=$(systemctl show $UNIT -p ExecStart | grep -o \"$R/[0-9a-z-]*\" | head -1)\n"
            "[ \"$RUN\" = \"$R/$OLD\" ] || { echo \"P1 STOP-READ-0 FAIL: the running root is ${RUN:-none}, not $R/$OLD; the read stops here, do not install\"; exit 40; }\n"
            "echo \"P1 STOP-READ-0 PASS: the running root is $R/$OLD\"")
plines = ptext.split("\n")
plines = replace_line_block(plines, 'echo "P1 reader members at the running root:', [
    'echo "P1 members that release 31 changes, read at the running root (each wanted value is the release-29 sha256):"'] + loop_block("", PKG, "r29")[1:]
    + ['  set -- $ent', '  GOT=$(sha256sum $RUN/$1 | cut -d\' \' -f1)',
       '  echo "P1 member $1 sha256 $GOT (want $2) $([ "$GOT" = "$2" ] && echo MATCH || echo MISMATCH)"',
       'done',
       'echo "P1 READER_VERSION line $(grep -m1 \'^READER_VERSION\' $RUN/intake/template_reader.py) (want READER_VERSION = \\"irpt-template-reader.r19.3\\")"'])
ptext = "\n".join(plines)
ptext = rep(ptext, "release 31 moves no worker", "release 31 moves the worker (its producer list)")
ptext = rep(ptext, "its line 70 creates it", "its cp -p step creates it")
pre_text = "\n".join(PRE_HEADER + ptext.split("\n"))
write("pre_read_r31.sh", pre_text)

# ---------------------------------------------------------------- rollback
rb = shift(load("rollback_r30.sh"))
rlines = split_header(rb, "NEW=")
RB_HEADER = [
    "set -u",
    "# Ledger irpt-resident-r31-20261014, leg X1 (NOT run unless the issuer orders it): put the resident back on the r29 root. The library bytes are the same before and after",
    "# release 31 (a1c288, reinstalled by the r31 install from the package), so no library step is needed beyond the refusal check.",
    "# Written under IRPT_ANLREQ.TO-AR-y-338 (worker 0.9.0_WK_IRPT_ANLREQ~144). NOT RUN: the applier 0.7.0_AE_CloudOps~YC2 runs it only if the issuer orders it.",
    "# Derived from rollback_r30.sh by the AR-y-301 method. Changed: NEW, the reader read-back (the twelve members the release changes, each at its release-29 sha256, the values the",
    "# rollback target must hold), and the wording. Every refusal guard of rollback_r30.sh is kept with its exit code.",
]
rtext = "\n".join(rlines)
rlines = rtext.split("\n")
rlines = replace_line_block(rlines, 'echo "X1 reader members:', [
    'echo "X1 members that release 31 changes, read at the running root (each wanted value is the release-29 sha256):"'] + loop_block("", PKG, "r29")[1:]
    + ['  set -- $ent', '  GOT=$(sha256sum $RUN/$1 | cut -d\' \' -f1)',
       '  echo "X1 member $1 sha256 $GOT (want $2) $([ "$GOT" = "$2" ] && echo MATCH || echo MISMATCH)"',
       'done'])
rb_text = "\n".join(RB_HEADER + rlines)
write("rollback_r31.sh", rb_text)

# ---------------------------------------------------------------- record of the derivation (printed, not written as a report)
print("TAR_SHA %s" % TAR_SHA)
print("SUMS_SHA %s" % SUMS_SHA)
print("HOST_SHA %s" % HOST_SHA)
print("DIFF %s" % " ".join(sorted(DIFF)))
print("PKG_CHANGED %d" % len(PKG))
