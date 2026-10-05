"""OG-rl-6 PHASE C-A2: render the RELEASE tree's deploy-to-ec2.sh `.env` printf with dummy arguments (no secret, no host) and read the result the way the
verify script reads the host's: key NAMES, and the YEARINREVIEW_VIEW_ALLOWED_EMAILS value as a sha256 only.
Proves (1) the template writes exactly the 51 names of r17/ENV_KEYS_R17B.txt (the r14 50 plus the one ruled key), (2) the new key's value digest equals
sha256("andrew@opalinvest.com"), and (3) the same value parses identically as a systemd EnvironmentFile line and as a shlex word (rl4.AC1 arm 2's check).
usage: python rl8_template_env.py <release gateway dir> <ENV_KEYS baseline file>
"""
import hashlib
import re
import shlex
import subprocess
import sys

gw, base = sys.argv[1], sys.argv[2]
src = open(gw + "/deploy-to-ec2.sh", encoding="utf-8").read().split("\n")
line = [ln for ln in src if ln.startswith("printf 'MOCK_GRAPH=0")]
assert len(line) == 1, len(line)
fmt = line[0][len("printf '"):line[0].index("' \"${REGION}\"")]
nargs = fmt.count("%s")
r = subprocess.run(["bash", "-c", 'printf "$@"', "x", fmt] + ["x"] * nargs, capture_output=True, text=True, encoding="utf-8")
assert r.returncode == 0, r.stderr
rendered = r.stdout.split("\n")
names = [m.group(1) for m in (re.match(r"^([A-Z0-9_]+)=", ln) for ln in rendered) if m]
want = [ln.strip() for ln in open(base, encoding="utf-8") if ln.strip() and not ln.startswith("#")]
print("printf conversions %d; rendered .env lines %d; key names %d (unique %d); baseline names %d" % (nargs, len([ln for ln in rendered if ln]), len(names), len(set(names)), len(want)))
print("names equal the baseline set: %s; only in template %s; only in baseline %s" % (sorted(names) == sorted(want), sorted(set(names) - set(want)), sorted(set(want) - set(names))))
val = [ln.split("=", 1)[1] for ln in rendered if ln.startswith("YEARINREVIEW_VIEW_ALLOWED_EMAILS=")]
print("YEARINREVIEW_VIEW_ALLOWED_EMAILS lines %d; value sha256 == sha256('andrew@opalinvest.com'): %s" % (len(val), len(val) == 1 and hashlib.sha256(val[0].encode()).hexdigest() == hashlib.sha256(b"andrew@opalinvest.com").hexdigest()))
hit = [ln for ln in rendered if ln.startswith("YEARINREVIEW_VIEW_ALLOWED_EMAILS=")]
sh = shlex.split(hit[0], posix=True) if hit else []
print("shlex word count %d, value equals the systemd (raw) value: %s" % (len(sh), len(sh) == 1 and sh[0].split("=", 1)[1] == val[0]))
ok = sorted(names) == sorted(want) and len(names) == 51 and len(val) == 1 and hashlib.sha256(val[0].encode()).hexdigest() == hashlib.sha256(b"andrew@opalinvest.com").hexdigest() and len(sh) == 1
print("RESULT: %s" % ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
