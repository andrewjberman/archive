"""IB-pr-402: extract a downloaded bundle tar.gz into its own NEW, EMPTY directory (refuses anything else).
Usage: python -I extract_bundle.py <bundle.tar.gz> <empty_dir>
Plain-file members only; a link, an absolute path or a `..` part is refused. (The box tar cannot read a C: path.)
"""
import os
import sys
import tarfile


def main():
    src, dst = sys.argv[1], sys.argv[2]
    if not os.path.isdir(dst) or os.listdir(dst):
        raise SystemExit("REFUSED: %s is not an existing empty directory" % dst)
    with tarfile.open(src) as tar:
        for m in tar.getmembers():
            if not m.isfile() or m.name.startswith("/") or ".." in m.name.split("/"):
                raise SystemExit("REFUSED: member %r" % m.name)
            path = os.path.join(dst, *m.name.split("/"))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as fh:
                fh.write(tar.extractfile(m).read())
    print("extracted", src, "->", dst)


if __name__ == "__main__":
    main()
