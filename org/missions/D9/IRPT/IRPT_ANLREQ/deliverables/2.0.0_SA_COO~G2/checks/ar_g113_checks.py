"""IRPT_ANLREQ AR-g-113 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g113_checks.py g113   the irpt-status SOURCE for the failure-code release: the source map re-pins exactly two irpt-status rows
                                    (status.py, durable_job.py) to pins whose blobs equal HEAD's, byte-preserving, and nothing else moves; the
                                    generated package differs from the base build in exactly those two staged members
    python ar_g113_checks.py scope  the branch changed only the map and the cell's own files (against the merge-base with box/dell2)

Prints one RESULT line: AR-G113-OK / AR-G113-FAIL or AR-G113-SCOPE-OK / AR-G113-SCOPE-FAIL; rc 0 only on OK. ASCII only.
"""
import difflib
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

MAP = "infra/aws/lambda/ci/lambda-source-map.json"
IR = "infra/aws/lambda/investor-reporting/"
STATUS = "irpt-status"
EXPECT_REPIN = {"status.py": IR + "ops/status.py", "durable_job.py": IR + "ycharts/generate/durable_job.py"}
OWN = (MAP,)
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")
HEX40, HEX64 = re.compile(r"[0-9a-f]{40}"), re.compile(r"[0-9a-f]{64}")


def git_text(*args):
    out = subprocess.run(["git", *args], capture_output=True)
    return out.returncode, out.stdout


def merge_base():
    rc, out = git_text("merge-base", "HEAD", "box/dell2")
    return out.decode().strip() if rc == 0 else None


def blob_bytes(ref, path):
    rc, out = git_text("show", "%s:%s" % (ref, path))
    return out if rc == 0 else None


def members(smap, function):
    """The member bytes the builder would zip: staged rows from their pins, the rest from the working tree at the source dir."""
    entry = smap["functions"][function]
    src = entry["source_dir"].strip("/")
    staged = {}
    for row in entry.get("staged_from") or []:
        data = blob_bytes(row["pin"], row["repo_path"])
        if data is None:
            raise ValueError("blob missing for %s@%s" % (row["repo_path"], row["pin"][:10]))
        staged[row["packaged_as"]] = data
    return {f: staged[f] if f in staged else Path(src + "/" + f).read_bytes() for f in entry["files"]}


def cases():
    out = []

    def case(name, ok, why=""):
        out.append((name, bool(ok), why))

    base_ref = merge_base()
    if base_ref is None:
        raise ValueError("no merge-base with box/dell2")
    base_text = blob_bytes(base_ref, MAP).decode("utf-8")
    new_bytes = Path(MAP).read_bytes()
    new_text = new_bytes.decode("utf-8")
    base_map, new_map = json.loads(base_text), json.loads(new_text)
    problems = []
    for fn in set(base_map["functions"]) | set(new_map["functions"]):
        b, n = base_map["functions"].get(fn), new_map["functions"].get(fn)
        if fn != STATUS:
            if b != n:
                problems.append("function changed: " + fn)
            continue
        if {k: v for k, v in b.items() if k != "staged_from"} != {k: v for k, v in n.items() if k != "staged_from"}:
            problems.append("fields changed in " + fn)
        brows = {r["packaged_as"]: r for r in b["staged_from"]}
        nrows = {r["packaged_as"]: r for r in n["staged_from"]}
        if set(brows) != set(nrows) or len(n["staged_from"]) != len(nrows):
            problems.append("the set of staged rows changed")
        for name in set(brows) & set(nrows):
            if name in EXPECT_REPIN:
                if (brows[name]["repo_path"], brows[name]["packaged_as"]) != (nrows[name]["repo_path"], nrows[name]["packaged_as"]):
                    problems.append("row identity changed: " + name)
                if brows[name] == nrows[name]:
                    problems.append("row not re-pinned: " + name)
            elif brows[name] != nrows[name]:
                problems.append("an unexpected row changed: " + name)
    for key in set(base_map) | set(new_map):
        if key != "functions" and base_map.get(key) != new_map.get(key):
            problems.append("top-level key changed: " + key)
    case("M1-only-the-two-expected-rows-change", not problems, "; ".join(problems)[:240])
    bad, checked = [], 0
    for row in new_map["functions"][STATUS]["staged_from"]:
        if row["packaged_as"] not in EXPECT_REPIN:
            continue
        checked += 1
        pin, path = row["pin"], row["repo_path"]
        blob = blob_bytes(pin, path) if HEX40.fullmatch(pin) else None
        head = Path(path).read_bytes() if Path(path).is_file() else None
        if blob is None or head is None:
            bad.append("%s: pin or file missing" % row["packaged_as"])
        elif not (hashlib.sha256(blob).hexdigest() == row["sha256"] == hashlib.sha256(head).hexdigest()) or not HEX64.fullmatch(row["sha256"]):
            bad.append("%s: blob, sha256 and the tree differ" % row["packaged_as"])
        elif subprocess.run(["git", "merge-base", "--is-ancestor", pin, "HEAD"]).returncode != 0:
            bad.append("%s: pin is not an ancestor of HEAD" % row["packaged_as"])
        else:
            last = git_text("log", "-1", "--format=%H", "--", path)[1].decode().strip()
            if blob_bytes(last, path) != blob:
                bad.append("%s: the pin's blob is not the blob of the last commit touching the path" % row["packaged_as"])
    case("M2-pins-are-full-commits-whose-blob-equals-the-tree", not bad and checked == 2, "%d rows; %s" % (checked, "; ".join(bad)[:200]))
    allowed = [re.compile(p) for p in (r'^\s*"pin": "[0-9a-f]{40}",$', r'^\s*"sha256": "[0-9a-f]{64}"$')]
    diff = [ln for ln in difflib.unified_diff(base_text.split("\n"), new_text.split("\n"), lineterm="", n=0) if ln[:1] in "+-" and ln[:3] not in ("+++", "---")]
    odd = [ln for ln in diff if not any(p.match(ln[1:]) for p in allowed)]
    case("M3-byte-preserving-edit", not odd and len(diff) == 8 and new_bytes.count(b"\r") == base_text.encode("utf-8").count(b"\r")
         and new_bytes.endswith(b"\n") == base_text.endswith("\n"), "%d changed lines (want 8), %d odd: %s" % (len(diff), len(odd), odd[:3]))
    try:
        bst, nst = members(base_map, STATUS), members(new_map, STATUS)
        dst = sorted(k for k in set(bst) | set(nst) if bst.get(k) != nst.get(k))
        case("M4-status-staged-delta-is-exactly-status-py-and-durable-job-py", dst == ["durable_job.py", "status.py"], str(dst))
    except Exception as exc:
        case("M4-packages-build", False, "%s: %s" % (type(exc).__name__, str(exc)[:160]))
    return out


def g113():
    try:
        out = cases()
    except Exception as exc:
        print("AR-G113-FAIL the cases could not run: %s: %s" % (type(exc).__name__, str(exc)[:200]))
        return 1
    failed = [(n, why) for n, ok, why in out if not ok]
    for name, why in failed:
        print("CASE-FAIL", name, why)
    if failed:
        print("AR-G113-FAIL %d of %d cases failed: %s" % (len(failed), len(out), str([n for n, _ in failed])[:300]))
        return 1
    print("AR-G113-OK %d cases" % len(out))
    return 0


def scope():
    base_ref = merge_base()
    rc, raw = git_text("diff", "--name-only", "box/dell2...HEAD")
    diff = raw.decode().split() if rc == 0 else []
    folder = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~"
    order = "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-113."
    stray = [p for p in diff if p not in OWN and not p.startswith(ISSUER) and not p.startswith(folder) and not p.startswith(order)]
    if base_ref is None or stray:
        print("AR-G113-SCOPE-FAIL stray=%s" % str(stray[:5]))
        return 1
    print("AR-G113-SCOPE-OK %d changed paths, all the cell's own" % len(diff))
    return 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "g113":
        sys.exit(g113())
    if mode == "scope":
        sys.exit(scope())
    print("usage: ar_g113_checks.py g113 | scope")
    sys.exit(2)
