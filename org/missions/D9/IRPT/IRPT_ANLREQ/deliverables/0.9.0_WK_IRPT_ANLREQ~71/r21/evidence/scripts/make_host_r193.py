"""Make the r21 host script from the release-19 host script: change ONLY the lines that name the release (ASCII only).

usage: python -I make_host_r193.py <r19 script> <out script>
Each replacement must match exactly once or the script stops.
"""
import sys

SRC, OUT = sys.argv[1:3]
text = open(SRC, "rb").read().decode("ascii")
R19_SHA = "84df6479655c07ae6000af40404e53eb056b4c403aa9134bbe9c1521317d497a"
NEW_SHA = "bb1f774922e05abada3895ad3c45c6ea131c688ffebf3f211209aa9d3d7c7fbc"
READER_SHA = "a61cd0c622f8dd54864b8f2415cbe9968c0287d28087ce703073c7e392c1fc35"
REPL = [
    ("# Ledger irpt-resident-r19-20261013: resident root 0485393f3a-st32 -> 0485393f3a-r19 (st32's recipe with ONLY intake/uploads.py and intake/template_reader.py\n"
     "# taken from the release pin 069b8f797e; the other 294 members, the host capture library and the wrapper are st32's bytes). The\n"
     "# 0485393f3a-st32 root and the library stay on the host for rollback. Copy of the st32 script with NEW, OLD, WANT_TAR, written_by and ledger changed;\n"
     "# written by 2.0.0_SA_COO~Y2 (pair irpt-reader-release-r19); operator 0.7.0_AE_CloudOps~YC2.\n",
     "# Ledger irpt-resident-r193-20261013: resident root 0485393f3a-r19 -> 0485393f3a-r193 (the release-19 package with ONLY intake/template_reader.py\n"
     "# moved to the trunk HEAD blob 7c2c761d (READER_VERSION irpt-template-reader.r19.3); the other 296 members, the host capture library and the wrapper\n"
     "# are the release-19 bytes. The 0485393f3a-r19 root and the library stay on the host for rollback. Copy of the release-19 script with NEW, OLD,\n"
     "# WANT_TAR and ledger changed, plus one check line for the moved reader; prepared by 0.9.0_WK_IRPT_ANLREQ~71 under AR-y-227 (NOT RUN).\n"
     "# operator 0.7.0_AE_CloudOps~YC2 (to be confirmed when the ledger is opened).\n", 1),
    ("NEW=0485393f3a-r19\n", "NEW=0485393f3a-r193\n", 1),
    ("OLD=0485393f3a-st32\n", "OLD=0485393f3a-r19\n", 1),
    ("WANT_TAR=" + R19_SHA + "\n", "WANT_TAR=" + NEW_SHA + "\n", 1),
    ('check "ycharts/generate/resident_main.py"',
     'check "intake/template_reader.py" ' + READER_SHA + '\ncheck "ycharts/generate/resident_main.py"', 1),
    ('"ledger": "irpt-resident-r19-20261013"', '"ledger": "irpt-resident-r193-20261013"', 1),
]
for old, new, n in REPL:
    count = text.count(old)
    if count != n:
        raise SystemExit("ERROR: %d matches for %r" % (count, old[:60]))
    text = text.replace(old, new)
open(OUT, "wb").write(text.encode("ascii"))
print("OK: wrote %s" % OUT)
