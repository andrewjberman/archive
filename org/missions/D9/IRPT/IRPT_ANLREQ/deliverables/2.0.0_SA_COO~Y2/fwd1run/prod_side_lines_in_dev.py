import subprocess

REPO = "C:/dev/ajb_workspace/portal"


def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace").stdout


base = git("merge-base", "origin/DEV", "origin/PROD").strip()
print("merge-base", base[:10])
files = [f for f in git("diff", "--name-only", base, "origin/PROD").split("\n") if f.strip()]
print("files changed on the PROD side since the merge base:", len(files))
tot_added = 0
tot_missing = 0
for f in files:
    diff = git("diff", "-U0", base, "origin/PROD", "--", f)
    added = [ln[1:] for ln in diff.split("\n") if ln.startswith("+") and not ln.startswith("+++")]
    added = [ln for ln in added if ln.strip()]
    dev_lines = set(row.rstrip() for row in git("show", "origin/DEV:" + f).split("\n"))
    miss = [ln for ln in added if ln.rstrip() not in dev_lines]
    tot_added += len(added)
    tot_missing += len(miss)
    if miss:
        print("  %-62s added %4d  PROD-only lines %3d" % (f[-62:], len(added), len(miss)))
        for m in miss[:6]:
            print("       -", m.strip()[:110])
print("TOTAL added lines on the PROD side:", tot_added, "| not present in the DEV file:", tot_missing)
