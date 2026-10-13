"""AMGT_RESAPP round-94 PREP -- the content-diff the ff-4 redeploy's build may print, member by member, by blob.

  python r94_admission_table.py [<ref>] [--pin 6a6c5c49d0]

The live package was built at `--pin` (round 92 qq-5, CodeSha256 SOzAz9/gfKE..). For every non-test file under `lib/` and every registry file (`infra/logic/registry/*.json`) the function
packages, print its blob at the pin, its blob at `<ref>` (default HEAD) and the added and removed line counts. A member absent at the pin prints ABSENT. This is
the table the pair's blast-radius section is written from: any member the pair does not admit, or a blob that differs from the table's column, is a STOP at the GO.
Read-only (git plumbing only).
"""
import subprocess
import sys

REGISTRY = ("infra/logic/registry/scopes.json", "infra/logic/registry/systems.json")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=False).stdout


def blob(ref, path):
    out = git("rev-parse", "--short=12", "%s:%s" % (ref, path)).strip()
    return out if out and " " not in out else "ABSENT"


def main():
    args = [a for a in sys.argv[1:]]
    pin = "6a6c5c49d0"
    if "--pin" in args:
        i = args.index("--pin")
        pin = args[i + 1]
        del args[i:i + 2]
    ref = args[0] if args else "HEAD"
    names = git("diff", "--name-only", pin, ref, "--", "lib/").split()
    names = [n for n in names if "/tests/" not in n and not n.endswith("_test.py")]
    # round 102 (row AMGT_RESAPP-D1-S27, RA1): EVERY registry file the builder loads is a package member, not only scopes.json and systems.json (exemptions.json was the twelfth member)
    reg = [p for p in git("ls-files", "infra/logic/registry/").split("\n") if p.endswith(".json")]
    for p in reg:
        if blob(pin, p) != blob(ref, p):
            names.append(p)
    print("pin %s ref %s (%s) | members whose bytes differ: %d" % (pin, ref, git("rev-parse", "--short=10", ref).strip(), len(names)))
    stat = {}
    for line in git("diff", "--numstat", pin, ref, "--", "lib/", "infra/logic/registry/").splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            stat[parts[2]] = (parts[0], parts[1])
    for n in sorted(names):
        added, removed = stat.get(n, ("?", "?"))
        print("| `%s` | %s | %s | +%s -%s |" % (n, blob(pin, n), blob(ref, n), added, removed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
