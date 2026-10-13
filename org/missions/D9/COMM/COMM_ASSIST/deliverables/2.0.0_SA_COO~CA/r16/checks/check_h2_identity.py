"""CA-h-2 AC1: the running AWS identity is a dell2 agent user that sits in AdministratorAccessOpalCapital.

Prints one line:  H2-IDENTITY ok=<True|False> user=<name> in_group=<True|False> reason=<text>
Read-only: sts get-caller-identity and iam list-groups-for-user. Exits 0 whatever the verdict.
"""
import json
import shutil
import subprocess
import sys

GROUP = "AdministratorAccessOpalCapital"


def aws(*args):
    exe = shutil.which("aws")
    if not exe:
        raise RuntimeError("aws not found on PATH")
    r = subprocess.run([exe] + list(args) + ["--output", "json"], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError("aws %s rc=%s: %s" % (args[0], r.returncode, (r.stderr or "")[:160].strip()))
    return json.loads(r.stdout)


def main():
    user, in_group, why = "NA", False, ""
    try:
        arn = aws("sts", "get-caller-identity")["Arn"]
        user = arn.rsplit("/", 1)[-1]
        groups = [g["GroupName"] for g in aws("iam", "list-groups-for-user", "--user-name", user)["Groups"]]
        in_group = GROUP in groups
        if "dell2" not in user.lower():
            why = "caller %s is not a dell2 user" % user
        elif not in_group:
            why = "%s is not in %s (groups=%d)" % (user, GROUP, len(groups))
    except Exception as exc:  # a failed read is a failed check, never a pass
        why = str(exc)[:200]
    ok = in_group and "dell2" in user.lower() and not why
    print("H2-IDENTITY ok=%s user=%s in_group=%s reason=%s" % (ok, user, in_group, why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
