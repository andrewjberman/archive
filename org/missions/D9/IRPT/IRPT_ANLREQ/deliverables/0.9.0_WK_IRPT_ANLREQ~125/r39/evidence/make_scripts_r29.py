"""AR-y-311 step 4: derive the three r29 host scripts from the three r28 scripts (AR-y-301 method).

Each substitution names an exact substring and the count it must match; any other count REFUSES.
Pure text derivation: nothing is run, nothing is uploaded, no AWS or host call.
usage: python -I make_scripts_r29.py <src dir (r28 scripts)> <dst dir (r29 scripts)>
ASCII only.
"""
import os
import sys

SRC, DST = sys.argv[1], sys.argv[2]

PRE = [
    ("# Ledger irpt-resident-r28-20261013, leg P1 (READ ONLY): the host state before the r28 install (expect the r19 root running, the library and wrapper unmoved, the r28 root absent).",
     "# Ledger irpt-resident-r29-20261014, leg P1 (READ ONLY): the host state before the r29 install (expect the r28 root running, the library and wrapper unmoved, the r29 root absent).", 1),
    ("# Written under IRPT_ANLREQ.TO-AR-y-301 (worker 0.9.0_WK_IRPT_ANLREQ~119).",
     "# Written under IRPT_ANLREQ.TO-AR-y-311 (worker 0.9.0_WK_IRPT_ANLREQ~125).", 1),
    ("# Derived from pre_read_r19.sh (release 19, the same five stop-reads). Changed: the roots, the reader and worker values, the receipt copy name, and STOP-READ-2's new-root condition.",
     "# Derived from pre_read_r28.sh (release 28, the same five stop-reads) by the AR-y-301 method. Changed: the roots (OLD = r28, NEW = r29), the reader values (the r28 values, with ops/status.py read back), the worker value (r28), the receipt ledger (r28), and the release-29 wording of the stop-reads.", 1),
    ("OLD=0485393f3a-r19\nNEW=0485393f3a-r28", "OLD=0485393f3a-r28\nNEW=0485393f3a-r29", 1),
    ("(want a643b0074258f3732abbb28e2712e60ee5433f6fc633d2c7ecc887ac5829113d, the release-19 worker; release 28 moves it to 190f0e14bceb97ca870b6eefeffbc6d96e6e63fb1eb3fcc905541d789b8e40d5)",
     "(want 190f0e14bceb97ca870b6eefeffbc6d96e6e63fb1eb3fcc905541d789b8e40d5, the release-28 worker; release 29 moves no worker)", 1),
    ("uploads.py $(sha256sum $RUN/intake/uploads.py | cut -d' ' -f1) template_reader.py",
     "uploads.py $(sha256sum $RUN/intake/uploads.py | cut -d' ' -f1) ops/status.py $(sha256sum $RUN/ops/status.py | cut -d' ' -f1) template_reader.py", 1),
    ("(want 176682cb1545435eec084376b3c37a578ca70d05f9ad5a376c0f2275f62b05ea and 83ab9b45d59065f53c640803df9fd07a0ddfcc97d89c13540c20622a6bf7bd58 and READER_VERSION = \\\"irpt-template-reader.r18.1\\\")",
     "(want 80ace2d376c854d6208bc0c17810e053bc538ff9e71ec5a96d8dc89629d01951 and 03fa9c78c9dd3ef2cd1321ad295ad4ea3df0ee996c473ee963652788332737d3 and a61cd0c622f8dd54864b8f2415cbe9968c0287d28087ce703073c7e392c1fc35 and READER_VERSION = \\\"irpt-template-reader.r19.3\\\")", 1),
    ("(want /opt/irpt-resident/$OLD and irpt-resident-r19-20261013)",
     "(want /opt/irpt-resident/$OLD and irpt-resident-r28-20261013)", 1),
    ("(as in the release-19 pre-read)", "(as in the release-28 pre-read)", 1),
    ("# STOP 2: the running root is the release-19 root and the release-28 root is absent",
     "# STOP 2: the running root is the release-28 root and the release-29 root is absent", 1),
    ("(release 28 reinstalls the same library bytes and moves no wrapper)",
     "(release 29 reinstalls the same library bytes and moves no wrapper)", 1),
    ("the library and the wrapper are the release-19 bytes", "the library and the wrapper are the release-28 bytes", 1),
    ("host library is the release-19 library\"", "host library is the release-28 library\"", 1),
    ("host library is not the release-19 library; do not install", "host library is not the release-28 library; do not install", 1),
    ("host wrapper is the release-19 wrapper\"", "host wrapper is the release-28 wrapper\"", 1),
    ("host wrapper is not the release-19 wrapper; do not install", "host wrapper is not the release-28 wrapper; do not install", 1),
    ("(expected before the r28 installer runs: its line 70 creates it with cp -p from the release-19 receipt)",
     "(expected before the r29 installer runs: its line 70 creates it with cp -p from the release-28 receipt)", 1),
]

INSTALL = [
    ("# Ledger irpt-resident-r28-20261013, legs D2 + V1: fetch the signed r28 install script BY KEY",
     "# Ledger irpt-resident-r29-20261014, legs D2 + V1: fetch the signed r29 install script BY KEY", 1),
    ("(it binds the bytes), run it (it stages the tar, checks every member, reinstalls the library with the same bytes, keeps the r19 root and library",
     "(it binds the bytes), run it (it stages the tar, checks every member, reinstalls the library with the same bytes, keeps the r28 root and library", 1),
    ("# Written under IRPT_ANLREQ.TO-AR-y-301 (worker 0.9.0_WK_IRPT_ANLREQ~119).",
     "# Written under IRPT_ANLREQ.TO-AR-y-311 (worker 0.9.0_WK_IRPT_ANLREQ~125).", 1),
    ("# Derived from install_r19.sh (release 19). Changed: NEW, OLD, WANT, WANTSUM; the reader and worker read-backs take the release-28 values of the build record; the eight-member",
     "# Derived from install_r28.sh (release 28) by the AR-y-301 method. Changed: NEW, OLD, WANT, WANTSUM; the reader read-backs take the release-29 values of the build record (uploads.py and ops/status.py replaced); the eight-member", 1),
    ("# table (seven replaced members and the added calendar); the package sums (298 entries); READER_VERSION r19.3; the release-28 import and yfinance read-backs; the sums temp file.",
     "# table (two replaced members, six unchanged and read back at their release-28 values); the package sums (298 entries); READER_VERSION r19.3 unchanged; the import read-backs unchanged; the sums temp file.", 1),
    ("# Every fetch, sha256 and refusal guard of install_r19.sh is kept with its exit code.",
     "# Every fetch, sha256 and refusal guard of install_r28.sh is kept with its exit code.", 1),
    ("NEW=0485393f3a-r28\n", "NEW=0485393f3a-r29\n", 1),
    ("OLD=0485393f3a-r19\n", "OLD=0485393f3a-r28\n", 1),
    ("WANT=bbead0d2b560ca49be3ab1e758d3111c22174e755771a46bce23ae3977122832",
     "WANT=5fd383f988c825bcedd9058cc5ecaa9f0c429dcc8ac7f3acb199ada46c78e14a", 1),
    ("WANTSUM=7978dae9b299a1649fbb221098b1ea4438bf8d67f6d4ecbb8ef01fd9656f59a8",
     "WANTSUM=eebbf8cf794deccc65002870b26bbf5f961c61bf1751c25ba081a05ea7fbcfe0", 1),
    ("(want 80ace2d376c854d6208bc0c17810e053bc538ff9e71ec5a96d8dc89629d01951) template_reader.py",
     "(want f85e8c9bb5af6ceddc6ccd513e511368447966d21f805a09306ef8f3cda81494) template_reader.py", 1),
    ("release-28 members against the build record (RESIDENT_BUILD.json release_input new_sha256;",
     "release-29 members against the r29 build record (RESIDENT_BUILD.json release_input new_sha256;", 1),
    ('  "intake/uploads.py 80ace2d376c854d6208bc0c17810e053bc538ff9e71ec5a96d8dc89629d01951" \\',
     '  "intake/uploads.py f85e8c9bb5af6ceddc6ccd513e511368447966d21f805a09306ef8f3cda81494" \\', 1),
    ('  "ops/status.py 03fa9c78c9dd3ef2cd1321ad295ad4ea3df0ee996c473ee963652788332737d3" \\',
     '  "ops/status.py 87048c7f4d00ba33c87de1a223a36b53e3487ed7414d613ee744984bcaef6030" \\', 1),
    ("# release 28 (AR-y-301): the members this release adds or replaces, imported the way the producer and the reader are",
     "# release 29 (AR-y-311): the members release 28 added or replaced, imported the way the producer and the reader are", 1),
    ("(want /opt/irpt-resident/$NEW and irpt-resident-r28-20261013;", "(want /opt/irpt-resident/$NEW and irpt-resident-r29-20261014;", 1),
]

ROLLBACK = [
    ("# Ledger irpt-resident-r28-20261013, leg X1 (NOT run unless the issuer orders it): put the resident back on the r19 root.",
     "# Ledger irpt-resident-r29-20261014, leg X1 (NOT run unless the issuer orders it): put the resident back on the r28 root.", 1),
    ("# release 28 (a1c288, reinstalled by the r28 install from the package)",
     "# release 29 (a1c288, reinstalled by the r29 install from the package)", 1),
    ("# Written under IRPT_ANLREQ.TO-AR-y-301 (worker 0.9.0_WK_IRPT_ANLREQ~119).",
     "# Written under IRPT_ANLREQ.TO-AR-y-311 (worker 0.9.0_WK_IRPT_ANLREQ~125).", 1),
    ("Derived from rollback_r19.sh (release 19), which derives", "Derived from rollback_r28.sh (release 28) by the AR-y-301 method, which derives", 1),
    ("(the release-19 values)", "(the release-28 values, with ops/status.py read back)", 1),
    ("Every refusal guard of rollback_r19.sh", "Every refusal guard of rollback_r28.sh", 1),
    ("NEW=0485393f3a-r28\n", "NEW=0485393f3a-r29\n", 1),
    ("OLD=0485393f3a-r19\n", "OLD=0485393f3a-r28\n", 1),
    ("the host library is not the release-19 library; nothing moved", "the host library is not the release-28 library; nothing moved", 1),
    ("(want 176682cb1545435eec084376b3c37a578ca70d05f9ad5a376c0f2275f62b05ea)",
     "(want 80ace2d376c854d6208bc0c17810e053bc538ff9e71ec5a96d8dc89629d01951)", 1),
    ("template_reader.py $(sha256sum $RUN/intake/template_reader.py | cut -d' ' -f1) (want 83ab9b45d59065f53c640803df9fd07a0ddfcc97d89c13540c20622a6bf7bd58)",
     "ops/status.py $(sha256sum $RUN/ops/status.py | cut -d' ' -f1) (want 03fa9c78c9dd3ef2cd1321ad295ad4ea3df0ee996c473ee963652788332737d3) template_reader.py $(sha256sum $RUN/intake/template_reader.py | cut -d' ' -f1) (want a61cd0c622f8dd54864b8f2415cbe9968c0287d28087ce703073c7e392c1fc35)", 1),
    ("(want /opt/irpt-resident/$OLD and irpt-resident-r19-20261013)", "(want /opt/irpt-resident/$OLD and irpt-resident-r28-20261013)", 1),
]

JOBS = [
    ("pre_read_r28.sh", "pre_read_r29.sh", PRE),
    ("install_r28.sh", "install_r29.sh", INSTALL),
    ("rollback_r28.sh", "rollback_r29.sh", ROLLBACK),
]

for src_name, dst_name, subs in JOBS:
    text = open(os.path.join(SRC, src_name), "rb").read().decode("ascii")
    for old, new, want in subs:
        got = text.count(old)
        if got != want:
            raise SystemExit("REFUSE %s: %d matches (want %d) for: %r" % (src_name, got, want, old[:90]))
        text = text.replace(old, new)
    if any(ord(c) > 127 for c in text):
        raise SystemExit("REFUSE %s: non-ASCII" % src_name)
    open(os.path.join(DST, dst_name), "wb").write(text.encode("ascii"))
    print("wrote %s (%d substitutions)" % (dst_name, len(subs)))
