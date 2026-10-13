"""IB-pr-499 worker 0.9.0_WK_IRPT_BCKEND~349: member-level diff of the BUILT zip against the LIVE zip.

Usage: python ib171_4_member_diff.py <built.zip> <live.zip> <repo_root> <pin_commit> <source_dir>
Reads both zips in memory. Prints counts and member names only (no client data is read).
For each member present in both zips whose bytes differ, prints the built member sha256 and the repo blob
sha256 at the pin (git show <pin>:<source_dir>/<name>, or the staged path when packaged from elsewhere is
not needed here: every member of this function is read from source_dir at the pin).
"""
import hashlib
import subprocess
import sys
import zipfile


def main():
    built_path, live_path, root, pin, src = sys.argv[1:6]
    bz = zipfile.ZipFile(built_path)
    lz = zipfile.ZipFile(live_path)
    bn = sorted(bz.namelist())
    ln = sorted(lz.namelist())
    print("built members=%d live members=%d" % (len(bn), len(ln)))
    only_b = sorted(set(bn) - set(ln))
    only_l = sorted(set(ln) - set(bn))
    print("only_in_built=%d only_in_live=%d" % (len(only_b), len(only_l)))
    for n in only_b:
        print("ONLY_BUILT: %s" % n)
    for n in only_l:
        print("ONLY_LIVE: %s" % n)
    same = 0
    changed = []
    for n in sorted(set(bn) & set(ln)):
        b = bz.read(n)
        lv = lz.read(n)
        if b == lv:
            same += 1
        else:
            changed.append((n, hashlib.sha256(b).hexdigest()))
    print("identical_members=%d changed_members=%d" % (same, len(changed)))
    for n, bsha in changed:
        blob = subprocess.run(["git", "-C", root, "show", "%s:%s/%s" % (pin, src, n)], capture_output=True)
        if blob.returncode != 0:
            print("CHANGED: %s built_sha256=%s repo_blob=NOT_AT_PIN(rc=%d)" % (n, bsha, blob.returncode))
            continue
        rsha = hashlib.sha256(blob.stdout).hexdigest()
        print("CHANGED: %s built_sha256=%s repo_blob_sha256_at_pin=%s equal=%s" % (n, bsha, rsha, bsha == rsha))


if __name__ == "__main__":
    main()
