"""Live-bytes read of one investor-reporting Lambda (CTO msg 4621, row IRPT_ANLREQ-D2-S39). READ ONLY.

Hashes every member of a downloaded LIVE zip and says, per member, which commits' blobs it equals: the tree at HEAD, each
distinct pin of the function's source-map entry, and the sha256 the entry itself declares for that member.

Usage: python live_bytes_read.py <repo_root> <function> <live_zip> [out_json]
Bytes are compared raw and, where that misses, with CRLF folded to LF (reported as `lf`). No AWS call; ASCII only.
"""
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git_blob(root, ref, path):
    p = subprocess.run(["git", "show", "%s:%s" % (ref, path)], cwd=str(root), capture_output=True, timeout=60)
    return p.stdout if p.returncode == 0 else None


def main():
    root = Path(sys.argv[1]).resolve()
    fn, zpath = sys.argv[2], sys.argv[3]
    out = sys.argv[4] if len(sys.argv) > 4 else None
    entry = json.loads((root / "infra/aws/lambda/ci/lambda-source-map.json").read_text(encoding="utf-8"))["functions"][fn]
    staged = {r["packaged_as"]: r for r in entry.get("staged_from") or []}
    native = {f: entry["source_dir"].rstrip("/") + "/" + f for f in entry.get("files") or []}
    pins = sorted({r["pin"] for r in staged.values()})
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(root), capture_output=True).stdout.decode().strip()
    refs = [("HEAD", head)] + [(p[:10], p) for p in pins]
    zf = zipfile.ZipFile(zpath)
    names = [n for n in zf.namelist() if not n.endswith("/")]
    rows, counts = [], {"declared_equal": 0, "head_equal": 0, "some_pin_only": 0, "none": 0, "not_in_map": 0}
    cache = {}
    for n in sorted(names):
        data = zf.read(n)
        digests = {sha(data), sha(data.replace(b"\r\n", b"\n"))}
        if n in staged:
            repo_path, declared, own_pin = staged[n]["repo_path"], staged[n].get("sha256"), staged[n]["pin"][:10]
        elif n in native:
            repo_path, declared, own_pin = native[n], None, None
        else:
            rows.append({"member": n, "in_map": False, "sha256": sha(data)[:16]})
            counts["not_in_map"] += 1
            continue
        matched = []
        for label, ref in refs:
            key = (ref, repo_path)
            if key not in cache:
                b = git_blob(root, ref, repo_path)
                cache[key] = None if b is None else {sha(b), sha(b.replace(b"\r\n", b"\n"))}
            if cache[key] and (cache[key] & digests):
                matched.append(label)
        dec = None if declared is None else (declared in digests)
        row = {"member": n, "in_map": True, "kind": "staged" if n in staged else "native", "repo_path": repo_path,
               "sha256": sha(data)[:16], "declared_pin": own_pin, "equals_declared_sha": dec, "equals_head": "HEAD" in matched,
               "equals_own_pin": (own_pin in matched) if own_pin else None, "matching_pins": [m for m in matched if m != "HEAD"]}
        rows.append(row)
        if dec:
            counts["declared_equal"] += 1
        if "HEAD" in matched:
            counts["head_equal"] += 1
        elif matched:
            counts["some_pin_only"] += 1
        else:
            counts["none"] += 1
    missing = sorted(set(staged) | set(native) - set(names)) if False else sorted((set(staged) | set(native)) - set(names))
    result = {"function": fn, "live_zip_sha256_b64": __import__("base64").b64encode(hashlib.sha256(Path(zpath).read_bytes()).digest()).decode(),
              "head": head[:10], "pins": [p[:10] for p in pins], "members_in_zip": len(names), "map_members": len(staged) + len(native),
              "map_members_missing_from_zip": missing, "counts": counts, "rows": rows}
    if out:
        Path(out).write_text(json.dumps(result, indent=2) + "\n", encoding="ascii")
    print("function %s  live zip sha256 %s  HEAD %s  distinct pins %d" % (fn, result["live_zip_sha256_b64"], head[:10], len(pins)))
    print("DENOMINATOR: %d members in the live zip; %d members declared by the map (%d staged, %d native); %d declared members missing from the zip" % (
        len(names), len(staged) + len(native), len(staged), len(native), len(missing)))
    print("equal to the tree at HEAD: %d | equal to some pin but not HEAD: %d | equal to NO commit read: %d | in the zip but not in the map: %d" % (
        counts["head_equal"], counts["some_pin_only"], counts["none"], counts["not_in_map"]))
    print("staged members equal to the sha256 the map declares: %d of %d" % (counts["declared_equal"], len([r for r in rows if r.get("kind") == "staged"])))
    for r in rows:
        if not r.get("in_map"):
            print("  NOT-IN-MAP  %s  %s" % (r["member"], r["sha256"]))
        elif not r["equals_head"]:
            print("  %-9s %s  own pin %s equal=%s  matches %s  declared-sha equal=%s" % (
                "PIN-ONLY" if r["matching_pins"] else "NO-MATCH", r["member"], r["declared_pin"], r["equals_own_pin"],
                r["matching_pins"] or "none", r["equals_declared_sha"]))
    for m in missing:
        print("  MISSING-FROM-ZIP  %s" % m)


if __name__ == "__main__":
    main()
