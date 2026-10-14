"""AR-y-324 step 5: derive the four release-30 scripts from the release-29 ones (AR-y-301 and AR-y-311 method).

usage: python -I make_scripts_r30.py <r29 scripts dir> <dst dir> <extracted r30 root> <extracted r29 root> <r30 tarball>
A release-number shift runs first on whole tokens only (r28 -> r29, r29 -> r30, release-28 -> release-29,
release-29 -> release-30). Every explicit substitution names an exact text and its count; any other count REFUSES.
Every sha is read from the extracted trees, never typed. Writes four files; nothing is run; ASCII only.
"""
import hashlib
import os
import re
import sys

SRC, DST, X30, X29, TAR = sys.argv[1:6]


def sha_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


SRC_SHA = {
    "pre_read_r29.sh": "fe35e6d43ac20cc6ac62e8ef4b6daea8da20663ee0f9b11db693f26bdc31ec86",
    "install_r29.sh": "0fb4fb27f36ecb4ff3fa13b4c717013645f27215fd6abca67fcca7a7c8245c0e",
    "rollback_r29.sh": "bef517d522994dc0b6382fbd5291db20076428138843b1b74f42e5664ad3b87a",
    "resident_host_install_0485393f3a-r29.sh": "5fd383f988c825bcedd9058cc5ecaa9f0c429dcc8ac7f3acb199ada46c78e14a",
}
for name, want in SRC_SHA.items():
    got = sha_file(os.path.join(SRC, name))
    if got != want:
        raise SystemExit("REFUSE source %s: %s (want %s)" % (name, got, want))

MEMBERS = {"upl": "intake/uploads.py", "int": "_scope/interactive_access.py",
           "comp": "ycharts/generate/composition_admission.py", "stat": "ops/status.py",
           "tmpl": "intake/template_reader.py", "worker": "ycharts/generate/resident_worker.py",
           "lib": "ycharts-host/ycharts_session.js", "wrap": "ycharts-host/run-ycharts-session.sh"}
N = {k: sha_file(os.path.join(X30, *v.split("/"))) for k, v in MEMBERS.items()}
OLDV = {k: sha_file(os.path.join(X29, *v.split("/"))) for k, v in MEMBERS.items()}
TAR_SHA = sha_file(TAR)
SUMS_SHA = sha_file(os.path.join(X30, "SHA256SUMS"))

# The values this derivation is written against (the r30 build record and the r29 record); a mismatch refuses.
EXPECT_N = {"upl": "48f39329ea4c947dc30cba02e07ed499d6f683726204710b16656c29d6f3c0c1",
            "int": "d416e3755d587b14a0b8ccbd2599b9183bada64c6aed5a9b56edc5a7ce19838b",
            "comp": "8d9b7aadc7c4db0b078737b155b4ec999d245d20c8bee83515c628639d0f64fd",
            "stat": "87048c7f4d00ba33c87de1a223a36b53e3487ed7414d613ee744984bcaef6030",
            "tmpl": "a61cd0c622f8dd54864b8f2415cbe9968c0287d28087ce703073c7e392c1fc35",
            "worker": "190f0e14bceb97ca870b6eefeffbc6d96e6e63fb1eb3fcc905541d789b8e40d5",
            "lib": "a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841",
            "wrap": "55ddb8f7947cba7cdca1b9139d4d0a1a3ad620e330c86ba3ab648d334763aff9"}
EXPECT_O = {"upl": "f85e8c9bb5af6ceddc6ccd513e511368447966d21f805a09306ef8f3cda81494",
            "int": "c28d9a74c9af2c5d5014ae54ffda388c2666d24e9c98ac42df3ace457e59e684",
            "comp": "50f5d11cd8ffb8161b9f42af61bdfcdffe698cfc4e66b5cc3338048572563606",
            "stat": "87048c7f4d00ba33c87de1a223a36b53e3487ed7414d613ee744984bcaef6030",
            "tmpl": "a61cd0c622f8dd54864b8f2415cbe9968c0287d28087ce703073c7e392c1fc35"}
for k, v in EXPECT_N.items():
    if N[k] != v:
        raise SystemExit("REFUSE new %s: %s (want %s)" % (k, N[k], v))
for k, v in EXPECT_O.items():
    if OLDV[k] != v:
        raise SystemExit("REFUSE old %s: %s (want %s)" % (k, OLDV[k], v))
if TAR_SHA != "a08864f9dbd3f3b832273c3a12bbdb2ccb5f9b492d5bd758762651011f4114f6":
    raise SystemExit("REFUSE tarball sha %s" % TAR_SHA)

SHIFT = re.compile(r"(?<![0-9A-Za-z])(r|release[- ])(28|29)(?![0-9])")


def shift(text):
    return SHIFT.sub(lambda m: m.group(1) + ("29" if m.group(2) == "28" else "30"), text)


def rep(text, old_raw, new_final, count=1):
    old = shift(old_raw)
    got = text.count(old)
    if got != count:
        raise SystemExit("REFUSE: %d matches (want %d) for %r" % (got, count, old_raw[:100]))
    return text.replace(old, new_final)


def write(name, text):
    if any(ord(c) > 127 for c in text):
        raise SystemExit("REFUSE %s: non-ASCII" % name)
    with open(os.path.join(DST, name), "wb") as fh:
        fh.write(text.encode("ascii"))
    print("wrote %s bytes=%d sha256=%s" % (name, len(text.encode("ascii")), sha_file(os.path.join(DST, name))))


def load(name):
    with open(os.path.join(SRC, name), "rb") as fh:
        return fh.read().decode("ascii")


UPL_LINE_R29 = '  "intake/uploads.py f85e8c9bb5af6ceddc6ccd513e511368447966d21f805a09306ef8f3cda81494" \\'
UPL_LINES_R30 = ('  "intake/uploads.py %s" \\\n'
                 '  "_scope/interactive_access.py %s" \\\n'
                 '  "ycharts/generate/composition_admission.py %s" \\') % (N["upl"], N["int"], N["comp"])

# ---------------------------------------------------------------- host script
host = load("resident_host_install_0485393f3a-r29.sh")
host = shift(host)
host = rep(host, "# Ledger irpt-resident-r29-20261014: resident root 0485393f3a-r28 -> 0485393f3a-r29 (the r28 member set with the trunk HEAD blobs of",
           "# Ledger irpt-resident-r30-20261014: resident root 0485393f3a-r29 -> 0485393f3a-r30 (the r29 member set with the trunk blobs of")
host = rep(host, "# intake/uploads.py and ops/status.py replaced (AR-y-308 Shares words; the rest of the r28 member set unchanged, base pin 0485393f3a, package pin f812980d12),",
           "# intake/uploads.py, _scope/interactive_access.py and ycharts/generate/composition_admission.py replaced (AR-y-318 and AR-y-319; the rest of the r29 member set unchanged, base pin 0485393f3a, package pin 109f4671bb9b24a2b19e3c81a69decdcb83acddf),")
host = rep(host, "# Copy of the r28 script with NEW, OLD, WANT_TAR, the two moved member checks, the ledger and this header changed; written by 0.9.0_WK_IRPT_ANLREQ~125",
           "# Copy of the r29 script with NEW, OLD, WANT_TAR, the moved member checks, the ledger and this header changed; written by 0.9.0_WK_IRPT_ANLREQ~132")
host = rep(host, "# for 2.0.0_SA_COO~Y2 (AR-y-311, build only); operator 0.7.0_AE_CloudOps~YC2.",
           "# for 2.0.0_SA_COO~Y2 (AR-y-324, build only); operator 0.7.0_AE_CloudOps~YC2.")
host = rep(host, "WANT_TAR=2de2adce622f8bb9bbd5ebc071e862446b056303c0d9ffd7d41b050bd17f51a4",
           "WANT_TAR=" + TAR_SHA)
host = rep(host, 'check "intake/uploads.py" f85e8c9bb5af6ceddc6ccd513e511368447966d21f805a09306ef8f3cda81494',
           'check "intake/uploads.py" ' + N["upl"])
ANCHOR_TMPL = 'check "ycharts/generate/templates.json" 54656584f476b616622368d60c227b1519a70f3e9aced14edb88c776f9823866'
host = rep(host, ANCHOR_TMPL, ANCHOR_TMPL + '\ncheck "ycharts/generate/composition_admission.py" ' + N["comp"])
ANCHOR_MS = 'check "_scope/maintained_sources.py" 29c35dbfba72ca031a7d172d74f401b5976ef383d5fc4ef5deaa3a21ab2d1587'
host = rep(host, ANCHOR_MS, ANCHOR_MS + '\ncheck "_scope/interactive_access.py" ' + N["int"])
HOST_NAME = "resident_host_install_0485393f3a-r30.sh"
write(HOST_NAME, host)
HOST_SHA = sha_file(os.path.join(DST, HOST_NAME))
checks = [ln for ln in host.split("\n") if ln.startswith('check "')]
print("host member checks (quoted, in the script): %d" % len(checks))

# ---------------------------------------------------------------- pre-read
pre = shift(load("pre_read_r29.sh"))
pre = rep(pre, "template_reader.py $(sha256sum $RUN/intake/template_reader.py | cut -d' ' -f1) READER_VERSION line",
          "template_reader.py $(sha256sum $RUN/intake/template_reader.py | cut -d' ' -f1) interactive_access.py $(sha256sum $RUN/_scope/interactive_access.py | cut -d' ' -f1) composition_admission.py $(sha256sum $RUN/ycharts/generate/composition_admission.py | cut -d' ' -f1) READER_VERSION line")
pre = rep(pre, "(want 80ace2d376c854d6208bc0c17810e053bc538ff9e71ec5a96d8dc89629d01951 and 03fa9c78c9dd3ef2cd1321ad295ad4ea3df0ee996c473ee963652788332737d3 and a61cd0c622f8dd54864b8f2415cbe9968c0287d28087ce703073c7e392c1fc35 and READER_VERSION",
          "(want " + OLDV["upl"] + " and " + OLDV["stat"] + " and " + OLDV["tmpl"] + " and " + OLDV["int"] + " and " + OLDV["comp"] + " and READER_VERSION")
pre = rep(pre, "the reader values (the r28 values, with ops/status.py read back)",
          "the reader values (the r29 values, with ops/status.py read back, and _scope/interactive_access.py and ycharts/generate/composition_admission.py read back)")
pre = rep(pre, "# Written under IRPT_ANLREQ.TO-AR-y-311 (worker 0.9.0_WK_IRPT_ANLREQ~125).",
          "# Written under IRPT_ANLREQ.TO-AR-y-324 (worker 0.9.0_WK_IRPT_ANLREQ~132).")
pre = rep(pre, "(want /opt/irpt-resident/$OLD and irpt-resident-r28-20261013)",
          "(want /opt/irpt-resident/$OLD and irpt-resident-r29-20261014)")
write("pre_read_r30.sh", pre)

# ---------------------------------------------------------------- install
ins = shift(load("install_r29.sh"))
ins = rep(ins, "# Written under IRPT_ANLREQ.TO-AR-y-311 (worker 0.9.0_WK_IRPT_ANLREQ~125).",
          "# Written under IRPT_ANLREQ.TO-AR-y-324 (worker 0.9.0_WK_IRPT_ANLREQ~132).")
ins = rep(ins, "# Derived from install_r28.sh (release 28) by the AR-y-301 method. Changed: NEW, OLD, WANT, WANTSUM; the reader read-backs take the release-29 values of the build record (uploads.py and ops/status.py replaced); the eight-member",
          "# Derived from install_r29.sh (release 29) by the AR-y-301 method. Changed: NEW, OLD, WANT, WANTSUM; the reader read-backs take the release-30 values of the build record (uploads.py replaced; _scope/interactive_access.py and ycharts/generate/composition_admission.py read back); the ten-member")
ins = rep(ins, "# table (two replaced members, six unchanged and read back at their release-28 values); the package sums (298 entries); READER_VERSION r19.3 unchanged; the import read-backs unchanged; the sums temp file.",
          "# table (uploads.py replaced; _scope/interactive_access.py and ycharts/generate/composition_admission.py added; seven unchanged and read back at their release-30 values); the package sums (298 entries); READER_VERSION r19.3 unchanged; the import read-backs unchanged; the sums temp file.")
ins = rep(ins, "WANT=5fd383f988c825bcedd9058cc5ecaa9f0c429dcc8ac7f3acb199ada46c78e14a", "WANT=" + HOST_SHA)
ins = rep(ins, "WANTSUM=eebbf8cf794deccc65002870b26bbf5f961c61bf1751c25ba081a05ea7fbcfe0", "WANTSUM=" + SUMS_SHA)
ins = rep(ins, "(want f85e8c9bb5af6ceddc6ccd513e511368447966d21f805a09306ef8f3cda81494) template_reader.py",
          "(want " + N["upl"] + ") template_reader.py")
ins = rep(ins, UPL_LINE_R29, UPL_LINES_R30)
ins = rep(ins, "# release 29 (AR-y-311): the members release 28 added or replaced, imported the way the producer and the reader are",
          "# release 30 (AR-y-324): the members this release adds or replaces, imported the way the producer and the reader are")
write("install_r30.sh", ins)

# ---------------------------------------------------------------- rollback
rb = shift(load("rollback_r29.sh"))
rb = rep(rb, "# Written under IRPT_ANLREQ.TO-AR-y-311 (worker 0.9.0_WK_IRPT_ANLREQ~125).",
         "# Written under IRPT_ANLREQ.TO-AR-y-324 (worker 0.9.0_WK_IRPT_ANLREQ~132).")
rb = rep(rb, "# reader read-backs (the release-28 values, with ops/status.py read back), and the rollback root's receipt copy name. Every refusal guard of rollback_r28.sh is kept with its exit code.",
         "# reader read-backs (the release-29 values, with ops/status.py read back, and _scope/interactive_access.py and ycharts/generate/composition_admission.py read back), and the rollback root's receipt copy name. Every refusal guard of rollback_r29.sh is kept with its exit code.")
rb = rep(rb, "(want 80ace2d376c854d6208bc0c17810e053bc538ff9e71ec5a96d8dc89629d01951) ops/status.py",
         "(want " + OLDV["upl"] + ") ops/status.py")
rb = rep(rb, "(want 03fa9c78c9dd3ef2cd1321ad295ad4ea3df0ee996c473ee963652788332737d3) template_reader.py",
         "(want " + OLDV["stat"] + ") template_reader.py")
rb = rep(rb, "(want a61cd0c622f8dd54864b8f2415cbe9968c0287d28087ce703073c7e392c1fc35)",
         "(want " + OLDV["tmpl"] + ") interactive_access.py $(sha256sum $RUN/_scope/interactive_access.py | cut -d' ' -f1) (want " + OLDV["int"] + ") composition_admission.py $(sha256sum $RUN/ycharts/generate/composition_admission.py | cut -d' ' -f1) (want " + OLDV["comp"] + ")")
# the r29 receipt ledger is the one the r29 host script wrote (its line 76): irpt-resident-r29-20261014
rb = rep(rb, "(want /opt/irpt-resident/$OLD and irpt-resident-r28-20261013)",
         "(want /opt/irpt-resident/$OLD and irpt-resident-r29-20261014)")
write("rollback_r30.sh", rb)

print("HOST_SHA %s" % HOST_SHA)
print("TAR_SHA %s" % TAR_SHA)
print("SUMS_SHA %s" % SUMS_SHA)
