"""TO-AR-y-338 criterion AR338-y-AC2 (amended by AMENDMENT 1): the host-script check. Offline: nothing is executed on a host;
the only subprocesses are `bash -n` (syntax) and the gate dry run gate_dryrun_r31.sh (scratch copies only), each under timeout.

Prints `SCRIPTS-OK ...` only when every condition holds; otherwise `SCRIPTS-BAD <why>` and exit 1.
Conditions: each of the four scripts is ASCII-only and `bash -n` rc 0; every quoted member-check line equals the sha256 of the
same member in the extracted release-31 tarball, m of m, and m equals the number of differing members (AMENDMENT 1: acceptance.py
is one of them); the two tarball gates pin the tarball's values (WANT_TAR = the tarball sha256, WANTSUM = the tarball's
SHA256SUMS member), WANT = the host script's sha256; WANT_LIBRARY and WANT_WRAPPER equal the tarball's ycharts-host members;
the pre-read fails closed on a running root other than 0485393f3a-r29 before any read; the install refuses a wrong running
root (exit 34) and the unit's IRPT_ANALYSIS_READY_QUEUE_URL (exit 35) before the fetch; the gate dry run holds (unchanged rc 0,
one byte changed non-zero, both gates). ASCII only.
"""
import hashlib
import os
import re
import subprocess
import sys
import tarfile

DL = os.path.dirname(os.path.abspath(__file__))
STAGE = "C:/dev/irpt-release-r31"
TAR = STAGE + "/irpt-resident-0485393f3a-r31.tar.gz"
R29_TAR = "C:/dev/irpt-release-r29/irpt-resident-0485393f3a-r29.tar.gz"
SCRIPTS = ["pre_read_r31.sh", "install_r31.sh", "rollback_r31.sh", "resident_host_install_0485393f3a-r31.sh"]
HOST = "resident_host_install_0485393f3a-r31.sh"
INSTALL = "install_r31.sh"
PRE = "pre_read_r31.sh"
GATE = "gate_dryrun_r31.sh"
OLD = "0485393f3a-r29"
NEW = "0485393f3a-r31"


def bad(why):
    print("SCRIPTS-BAD " + why)
    sys.exit(1)


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    with open(path, "rb") as fh:
        return sha_bytes(fh.read())


def tar_members(path):
    out = {}
    with tarfile.open(path, "r:gz") as tar:
        for m in tar.getmembers():
            if not m.isfile():
                bad("non-file member %s" % m.name)
            name = m.name[2:] if m.name.startswith("./") else m.name
            out[name] = tar.extractfile(m).read()
    return out


def text_of(name):
    data = open(os.path.join(DL, name), "rb").read()
    if not all(c < 128 for c in data):
        bad("%s is not ASCII" % name)
    return data.decode("ascii")


# (1) ASCII-only and bash -n rc 0, for each of the four scripts
for name in SCRIPTS:
    text_of(name)
    proc = subprocess.run(["bash", "-n", os.path.join(DL, name)], capture_output=True, timeout=120)
    if proc.returncode != 0:
        bad("bash -n %s rc %d: %s" % (name, proc.returncode, proc.stderr.decode("ascii", "replace")[:200]))

# the extracted tarball: the differing members (against release 29) and the member bytes
t31 = tar_members(TAR)
t29 = tar_members(R29_TAR)
if len(t31) != 299 or len(t29) != 299:
    bad("member counts %d and %d, want 299" % (len(t31), len(t29)))
differing = sorted(n for n in t31 if n in t29 and sha_bytes(t31[n]) != sha_bytes(t29[n]))
if len(differing) != 15:
    bad("differing members %d, want 15" % len(differing))

# (2) every quoted member-check line equals the tarball's member sha256; m of m; m equals the differing count
host = text_of(HOST)
checks = re.findall(r'^check "([^"]+)" ([0-9a-f]{64})$', host, re.M)
for name, want in checks:
    if name not in t31:
        bad("member check names %s, which is not a tarball member" % name)
    got = sha_bytes(t31[name])
    if got != want:
        bad("member check %s wants %s, tarball has %s" % (name, want, got))
equal = len(checks)
if equal != len(differing) or sorted(n for n, _ in checks) != differing:
    bad("member checks name %d members; the differing set is %d" % (len(checks), len(differing)))

# (3) the tarball gates and the host gate
tar_sha = sha_file(TAR)
sums_sha = sha_bytes(t31["SHA256SUMS"])
want_tar = re.findall(r"^WANT_TAR=([0-9a-f]{64})$", host, re.M)
if want_tar != [tar_sha]:
    bad("host WANT_TAR %s, tarball sha256 %s" % (want_tar, tar_sha))
install = text_of(INSTALL)
want_host = re.findall(r"^WANT=([0-9a-f]{64})$", install, re.M)
if want_host != [sha_file(os.path.join(DL, HOST))]:
    bad("install WANT %s is not the host script sha256" % want_host)
want_sums = re.findall(r"^WANTSUM=([0-9a-f]{64})$", install, re.M)
if want_sums != [sums_sha]:
    bad("install WANTSUM %s, tarball SHA256SUMS member %s" % (want_sums, sums_sha))
if re.findall(r"^NEW=(\S+)$", host, re.M) != [NEW] or re.findall(r"^OLD=(\S+)$", host, re.M) != [OLD]:
    bad("host NEW/OLD are not %s/%s" % (NEW, OLD))

# (4) WANT_LIBRARY and WANT_WRAPPER equal the tarball's ycharts-host members
lib = re.findall(r"^WANT_LIBRARY=([0-9a-f]{64})$", host, re.M)
wrap = re.findall(r"^WANT_WRAPPER=([0-9a-f]{64})$", host, re.M)
if lib != [sha_bytes(t31["ycharts-host/ycharts_session.js"])]:
    bad("WANT_LIBRARY %s is not the tarball member ycharts-host/ycharts_session.js" % lib)
if wrap != [sha_bytes(t31["ycharts-host/run-ycharts-session.sh"])]:
    bad("WANT_WRAPPER %s is not the tarball member ycharts-host/run-ycharts-session.sh" % wrap)

# (5) the pre-read fails closed on a running root other than OLD, before any read of the unit's state
pre = text_of(PRE).split("\n")
if "OLD=%s" % OLD not in pre:
    bad("pre-read OLD is not %s" % OLD)
closed = [i for i, ln in enumerate(pre) if '"$RUN" = "$R/$OLD"' in ln and "exit 40" in ln]
if len(closed) != 1:
    bad("pre-read fail-closed running-root check lines: %d, want 1" % len(closed))
run_read = [i for i, ln in enumerate(pre) if ln.startswith("RUN=$(systemctl")]
if not run_read or run_read[0] > closed[0]:
    bad("pre-read fail-closed check is not after the running-root read")
first_member_read = min([i for i, ln in enumerate(pre) if "sha256sum" in ln] or [10 ** 9])
if closed[0] > first_member_read:
    bad("pre-read fail-closed check comes after a member read")

# (6) the install refuses a wrong running root (34) and the unit's IRPT_ANALYSIS_READY_QUEUE_URL (35) before the fetch
ins = install.split("\n")
g34 = [i for i, ln in enumerate(ins) if '"$RUN" = "$R/$OLD"' in ln and "exit 34" in ln]
g35 = [i for i, ln in enumerate(ins) if '"$UNITENV" = 0' in ln and "exit 35" in ln]
fetch = [i for i, ln in enumerate(ins) if ln.startswith('aws s3 cp "s3://opal-313476888478-lambda-artifacts/$KEY"')]
if len(g34) != 1 or len(g35) != 1 or len(fetch) != 1:
    bad("install guard lines: exit34=%d exit35=%d fetch=%d, want 1 each" % (len(g34), len(g35), len(fetch)))
if not (g34[0] < fetch[0] and g35[0] < fetch[0]):
    bad("install guards do not precede the fetch")
if "IRPT_ANALYSIS_READY_QUEUE_URL" not in "\n".join(ins[g35[0] - 1:g35[0] + 1]):
    bad("install unit guard does not name IRPT_ANALYSIS_READY_QUEUE_URL")

# (7) the gate dry run holds (scratch copies only; the host script is never executed)
proc = subprocess.run(["bash", os.path.join(DL, GATE)], capture_output=True, timeout=180)
out = proc.stdout.decode("ascii", "replace")
if proc.returncode != 0:
    bad("gate dry run rc %d" % proc.returncode)
got = {}
for label, value in re.findall(r"^(gate[12] [^:]+): rc=(\d+)$", out, re.M):
    got[label] = int(value)
need = {"gate1 unchanged host script copy": 0, "gate2 unchanged package sums copy": 0}
for label, want in need.items():
    if got.get(label) != want:
        bad("gate dry run: %s rc %s, want 0" % (label, got.get(label)))
flipped = [v for k, v in got.items() if "one-byte" in k]
if len(flipped) != 2 or any(v == 0 for v in flipped):
    bad("gate dry run: one-byte rc values %s, want two non-zero" % flipped)

print("SCRIPTS-OK %d scripts, member checks %d of %d equal the tarball, gates fail on one byte "
      "(gate1 one-byte rc %d, gate2 one-byte rc %d; WANT_TAR, WANT, WANTSUM, WANT_LIBRARY, WANT_WRAPPER equal)"
      % (len(SCRIPTS), equal, len(differing), flipped[0], flipped[1]))
