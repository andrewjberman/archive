"""Compare the member sha256 of a built zip against a live zip (read-only, stdlib only).

Usage: python -I members_cmp.py <built.zip> <live.zip> <out.json>
"""
import hashlib
import json
import sys
import zipfile


def members(zf):
    out = {}
    for info in zf.infolist():
        if info.is_dir():
            continue
        out[info.filename] = hashlib.sha256(zf.read(info)).hexdigest()
    return out


def main():
    built = members(zipfile.ZipFile(sys.argv[1]))
    live = members(zipfile.ZipFile(sys.argv[2]))
    print("built members", len(built), "live members", len(live))
    print("only_in_built", sorted(set(built) - set(live)))
    print("only_in_live", sorted(set(live) - set(built)))
    diff = sorted(k for k in set(built) & set(live) if built[k] != live[k])
    print("differing", len(diff))
    for name in diff:
        print("  DIFF", name, "built", built[name], "live", live[name])
    with open(sys.argv[3], "w") as fh:
        json.dump({"built": built, "live": live}, fh, indent=1)


if __name__ == "__main__":
    main()
