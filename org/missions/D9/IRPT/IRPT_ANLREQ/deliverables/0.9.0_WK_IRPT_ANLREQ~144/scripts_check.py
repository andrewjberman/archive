"""TO-AR-y-338 criterion AR338-y-AC2: the four host-side scripts against the staged tarball. Offline: nothing uploaded or run.

Prints `SCRIPTS-OK ...` only when: each script is ASCII-only and `bash -n` returns 0; every quoted member-check line of the
host script equals the sha256 of the same member in the extracted release-31 tarball, and their number equals the number of
members that differ from release 29; the two tarball gates' pinned sha256 values equal the tarball's (WANT_TAR, WANTSUM) and
the host script's own sha256 (WANT); WANT_LIBRARY and WANT_WRAPPER equal the tarball's ycharts-host members; the pre-read
fails closed unless the running root is 0485393f3a-r29; and the two gate lines, copied from install_r31.sh and evaluated on
scratch copies, return 0 unchanged and non-zero for a one-byte change. Otherwise `SCRIPTS-BAD <why>`, exit 1. ASCII only.
"""
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tarfile

DL = os.path.dirname(os.path.abspath(__file__))
STAGE = "C:/dev/irpt-release-r31"
TAR = STAGE + "/irpt-resident-0485393f3a-r31.tar.gz"
RECORD = os.path.join(DL, "r41", "RESIDENT_R31_BUILD.json")
SCRATCH = STAGE + "/check-scratch/scripts"
NAMES = ["pre_read_r31.sh", "install_r31.sh", "rollback_r31.sh", "resident_host_install_0485393f3a-r31.sh"]
HOST = "resident_host_install_0485393f3a-r31.sh"


def bad(why):
    print("SCRIPTS-BAD " + why)
    sys.exit(1)


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    with open(path, "rb") as fh:
        return sha_bytes(fh.read())


def read_text(name):
    with open(os.path.join(DL, name), "rb") as fh:
        data = fh.read()
    if any(b > 127 for b in data):
        bad("%s is not ASCII" % name)
    return data.decode("ascii")


def tar_members(path):
    out = {}
    with tarfile.open(path, "r:gz") as tar:
        for m in tar.getmembers():
            name = m.name[2:] if m.name.startswith("./") else m.name
            out[name] = tar.extractfile(m).read()
    return out


record = json.load(open(RECORD, encoding="utf-8"))
differing = set(record["delta_vs_live"]["differing"])
members = tar_members(TAR)
mh = {n: sha_bytes(d) for n, d in members.items()}

# ASCII and bash -n for the four scripts
for name in NAMES:
    text = read_text(name)
    proc = subprocess.run(["bash", "-n", os.path.join(DL, name)], capture_output=True)
    if proc.returncode != 0:
        bad("bash -n %s rc=%d %s" % (name, proc.returncode, proc.stderr.decode("ascii", "replace")[:160]))

host = read_text(HOST)
install = read_text("install_r31.sh")
pre = read_text("pre_read_r31.sh")

# every quoted member-check line equals the tarball's member; their number equals the differing count
checks = re.findall(r'^check "([^"]+)" ([0-9a-f]{64})$', host, re.M)
for name, want in checks:
    if name not in mh:
        bad("check names a member the tarball lacks: %s" % name)
    if mh[name] != want:
        bad("check %s is %s, the tarball's member is %s" % (name, want, mh[name]))
if len(checks) != len(differing):
    bad("quoted member checks %d, differing members %d" % (len(checks), len(differing)))
if set(n for n, _ in checks) != differing:
    bad("the checked names are not the differing set")

# the pinned sha256 values
want_tar = re.search(r"^WANT_TAR=([0-9a-f]{64})$", host, re.M)
if not want_tar or want_tar.group(1) != sha_file(TAR):
    bad("host WANT_TAR is not the tarball's sha256")
want_lib = re.search(r"^WANT_LIBRARY=([0-9a-f]{64})$", host, re.M)
want_wrap = re.search(r"^WANT_WRAPPER=([0-9a-f]{64})$", host, re.M)
if not want_lib or want_lib.group(1) != sha_bytes(members["ycharts-host/ycharts_session.js"]):
    bad("WANT_LIBRARY is not the tarball's ycharts-host library")
if not want_wrap or want_wrap.group(1) != sha_bytes(members["ycharts-host/run-ycharts-session.sh"]):
    bad("WANT_WRAPPER is not the tarball's ycharts-host wrapper")
want_host = re.search(r"^WANT=([0-9a-f]{64})$", install, re.M)
if not want_host or want_host.group(1) != sha_file(os.path.join(DL, HOST)):
    bad("install WANT is not the host script's sha256")
want_sums = re.search(r"^WANTSUM=([0-9a-f]{64})$", install, re.M)
if not want_sums or want_sums.group(1) != mh["SHA256SUMS"]:
    bad("install WANTSUM is not the tarball's SHA256SUMS sha256")

# the pre-read fails closed on a running root other than 0485393f3a-r29
if not re.search(r"^OLD=0485393f3a-r29$", pre, re.M):
    bad("pre-read does not name the running root 0485393f3a-r29")
if not re.search(r'^\[ "\$RUN" = "\$R/\$OLD" \] \|\| \{ echo .*; exit [1-9][0-9]*; \}$', pre, re.M):
    bad("pre-read has no fail-closed running-root refusal")

# the gate dry run, from the install's own gate lines, on scratch copies
if os.path.isdir(SCRATCH):
    shutil.rmtree(SCRATCH)
os.makedirs(SCRATCH)
g1 = [ln for ln in install.split("\n") if "sha256sum $T |" in ln]
g2 = [ln for ln in install.split("\n") if "sha256sum $S |" in ln]
if len(g1) != 1 or len(g2) != 1:
    bad("gate lines found %d and %d, want 1 and 1" % (len(g1), len(g2)))
host_bytes = open(os.path.join(DL, HOST), "rb").read()
sums_bytes = members["SHA256SUMS"]


def write(name, data):
    p = os.path.join(SCRATCH, name)
    with open(p, "wb") as fh:
        fh.write(data)
    return p.replace("C:/", "/c/").replace("\\", "/")


flip_host = bytearray(host_bytes)
flip_host[100] ^= 0x01
flip_sums = bytearray(sums_bytes)
flip_sums[50] ^= 0x01
paths = {"host_ok": write("host_ok.sh", host_bytes), "host_bad": write("host_bad.sh", bytes(flip_host)),
         "sums_ok": write("sums_ok", sums_bytes), "sums_bad": write("sums_bad", bytes(flip_sums))}
script = "\n".join([
    "G1=%s" % shlex.quote(g1[0].strip()),
    "G2=%s" % shlex.quote(g2[0].strip()),
    "WANT=%s" % want_host.group(1),
    "WANTSUM=%s" % want_sums.group(1),
    "gate1() { ( T=\"$1\"; eval \"$G1\" ); }",
    "gate2() { ( S=\"$1\"; T=\"$2\"; eval \"$G2\" ); }",
    "gate1 %s >/dev/null 2>&1; echo \"rc1_ok=$?\"" % paths["host_ok"],
    "gate1 %s >/dev/null 2>&1; echo \"rc1_bad=$?\"" % paths["host_bad"],
    "gate2 %s %s >/dev/null 2>&1; echo \"rc2_ok=$?\"" % (paths["sums_ok"], paths["host_ok"]),
    "gate2 %s %s >/dev/null 2>&1; echo \"rc2_bad=$?\"" % (paths["sums_bad"], paths["host_bad"]),
    "",
])
script_path = os.path.join(SCRATCH, "gate.sh")
with open(script_path, "w", encoding="ascii", newline="\n") as fh:
    fh.write(script)
proc = subprocess.run(["bash", script_path.replace("C:/", "/c/").replace("\\", "/")], capture_output=True)
rcs = dict(item.split("=") for item in proc.stdout.decode("ascii", "replace").split() if "=" in item)
if rcs.get("rc1_ok") != "0" or rcs.get("rc2_ok") != "0":
    bad("an unchanged copy did not pass its gate: %s" % rcs)
if rcs.get("rc1_bad") in (None, "0") or rcs.get("rc2_bad") in (None, "0"):
    bad("a one-byte change did not fail its gate: %s" % rcs)

print("SCRIPTS-OK %d scripts, member checks %d of %d equal the tarball, gates fail on one byte "
      "(rc1 unchanged %s, one byte %s; rc2 unchanged %s, one byte %s)" % (
          len(NAMES), len(checks), len(checks), rcs["rc1_ok"], rcs["rc1_bad"], rcs["rc2_ok"], rcs["rc2_bad"]))
