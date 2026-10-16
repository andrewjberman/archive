"""ap28 helper: grade the deploy script's env hunk between two refs. Prints one line of key=value pairs."""
import difflib
import re
import subprocess
import sys

SCRIPT = "infra/aws/ec2/opal-gateway/deploy-to-ec2.sh"
KEY = "BLACKDIAMOND49FLIVE_READER_ROLE_ARN"
ROLE = "gateway-49f-blackdiamond-live-read-role"
ARG = re.compile(r'"((?:[^"\\]|\\.)*)"')
PF = "printf 'MOCK_GRAPH"


def show(ref):
    if ref.startswith("file:"):  # dry-run arm: a script file instead of a ref
        return open(ref[5:], encoding="utf-8", newline="").read().replace("\r", "")
    r = subprocess.run(["git", "show", "%s:%s" % (ref, SCRIPT)], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "")


def printf_line(text):
    for ln in text.split("\n"):
        if ln.startswith(PF):
            return ln
    return ""


def parse(ln):
    cut = ln.index("' \"")
    fmt, rest = ln[:cut], ln[cut + 2:]
    rest = rest.split(" | sudo", 1)[0]
    return fmt, ARG.findall(rest)


base, rel = show(sys.argv[1]), show(sys.argv[2])
bl, rl = printf_line(base), printf_line(rel)
out = {}
if not bl or not rl:
    out.update(parsed="no", removed_other=-1, aligned="no", role_assigned=0, syntax="no", key_added=0)
else:
    bf, ba = parse(bl)
    rf, ra = parse(rl)
    out["parsed"] = "yes"
    # every %s has an arg, in the release and in the base
    out["pct_equals_args"] = "yes" if (rf.count("%s") == len(ra) and bf.count("%s") == len(ba)) else "no"
    seg = KEY + "=%s" + chr(92) + "n"
    out["key_added"] = 1 if seg in rf else 0
    out["aligned"] = "no"
    if seg in rf:
        slot = rf[:rf.index(seg)].count("%s")  # the new key's positional slot among ALL %s
        out["aligned"] = "yes" if (rf.replace(seg, "") == bf and ra[:slot] + ra[slot + 1:] == ba
                                    and "49FLIVE" in ra[slot].upper().replace("_", "")) else "no"
    diff = list(difflib.unified_diff(base.split("\n"), rel.split("\n"), lineterm="", n=0))
    removed = [ln[1:] for ln in diff if ln.startswith("-") and not ln.startswith("---")]
    added = [ln[1:] for ln in diff if ln.startswith("+") and not ln.startswith("+++")]
    out["removed_other"] = len([ln for ln in removed if not ln.startswith(PF)])
    out["role_assigned"] = len([ln for ln in added if ROLE in ln and "_vr_arn" in ln])
    out["added_other"] = len([ln for ln in added if not ln.startswith(PF) and ROLE not in ln])
    p = subprocess.run(["bash", "-n"], input=rel.encode("utf-8"), capture_output=True)
    out["syntax"] = "yes" if p.returncode == 0 else "no"
print(" ".join("%s=%s" % kv for kv in out.items()))
