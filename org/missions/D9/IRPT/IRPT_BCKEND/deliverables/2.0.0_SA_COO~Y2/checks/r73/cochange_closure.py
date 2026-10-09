"""Co-change closure of a Lambda's staged rows (IRPT_BCKEND round 73, issuer 2.0.0_SA_COO~Y2; row IRPT_BCKEND-D2-S18).

**What release 5 got wrong.** It shipped half of one commit. Rider f60e6f1d2a changed reports/retention.py
(RetentionPolicy.reference gained policy_revision) and its callers reports/composition.py and repository.py. Round 71 re-pinned the
callers and left retention.py at 3f29017cfc. The deployed repository therefore called reference() with 4 arguments against a
3-argument packaged retention.py. The symbol closure and the import census both passed, because arity is call-time.

**What this checks.** A commit C is SPLIT if both of these hold:
- C touches the repo_path of at least one staged row whose pin already contains C (C ships);
- C also touches the repo_path of another staged row whose pin does NOT contain C (C is missing there).

Usage: python cochange_closure.py <function> [map_path]

Prints:
- one `SPLIT` line per (commit, lagging row);
- `cochange_closure rows=<n> commits_checked=<k> split=<m>`;
- `cochange_closure PASS` or `cochange_closure FAIL` as the last line.

It reads only git; one `git show --name-only` per candidate commit.
"""
import json
import subprocess
import sys


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def contains(pin, c):
    return subprocess.run(["git", "merge-base", "--is-ancestor", c, pin], capture_output=True).returncode == 0


def main():
    if len(sys.argv) < 2:
        print("usage: cochange_closure.py <function> [map_path]")
        print("cochange_closure FAIL")
        sys.exit(2)
    fn = sys.argv[1]
    path = sys.argv[2] if len(sys.argv) > 2 else "infra/aws/lambda/ci/lambda-source-map.json"
    m = json.load(open(path, encoding="utf-8"))
    rows = (m.get("functions", m))[fn].get("staged_from", [])
    pins = {r["repo_path"]: r["pin"] for r in rows}
    # candidate commits: any commit after some row's pin that touches that row's path
    candidates = set()
    for rp, pin in pins.items():
        candidates.update(git("log", "--format=%H", "%s..HEAD" % pin, "--", rp).split())
    split = 0
    for c in sorted(candidates):
        touched = set(git("show", "--name-only", "--format=", c).split())
        staged_touched = [rp for rp in pins if rp in touched]
        ships = [rp for rp in staged_touched if contains(pins[rp], c)]
        lags = [rp for rp in staged_touched if not contains(pins[rp], c)]
        if ships and lags:
            for rp in lags:
                split += 1
                print("SPLIT %s ships via %s but %s is pinned at %s" % (c[:10], ", ".join(sorted(ships)), rp, pins[rp][:10]))
    print("cochange_closure rows=%d commits_checked=%d split=%d" % (len(rows), len(candidates), split))
    print("cochange_closure %s" % ("PASS" if split == 0 else "FAIL"))
    sys.exit(0 if split == 0 else 1)


if __name__ == "__main__":
    main()
