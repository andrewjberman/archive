"""IB-pr-510: rebuild one candidate host package deterministically from the LIVE package and the candidate members.

Usage: python -I pack_candidate_package.py <firm_id> <live_package.tar.gz> <candidate_dir> <out.tar.gz>

<candidate_dir> holds the replaced members of this firm (the files stored under candidate/<firm>/ in this folder).
Every other member is taken unchanged from the live package. SHA256SUMS is regenerated for the replaced members
only (the live line format is kept: "<sha256>  <repo path>"). Output: sorted members, SHA256SUMS last (as in
the live package), uid/gid 0, mtime 0, mode 0644, gzip mtime 0. Prints the sha256 of the output.
"""
import gzip
import hashlib
import io
import os
import sys
import tarfile

REPLACED = {
    "49financial": {
        "data/assets/scripts/gold/investor_reporting/holdings_49f.py": "holdings_49f.py",
        "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py": "holdings_snapshot.py",
        "docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json": "HoldingsSnapshot.schema.json",
    },
    "inflection": {
        "data/assets/scripts/gold/investor_reporting/holdings_inf.py": "holdings_inf.py",
        "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py": "holdings_snapshot.py",
    },
}


def main():
    firm, live_tar, cand_dir, out = sys.argv[1:5]
    repl = REPLACED[firm]
    members = {}
    with tarfile.open(live_tar, "r:gz") as tf:
        for ti in tf.getmembers():
            if ti.isfile():
                members[ti.name] = tf.extractfile(ti).read()
    sums = members.pop("SHA256SUMS").decode("utf-8").split("\n")
    assert sums[-1] == ""
    lines = []
    for ln in sums[:-1]:
        h, path = ln.split("  ", 1)
        if path in repl:
            with open(os.path.join(cand_dir, repl[path]), "rb") as f:
                members[path] = f.read()
            lines.append("%s  %s" % (hashlib.sha256(members[path]).hexdigest(), path))
        else:
            assert hashlib.sha256(members[path]).hexdigest() == h, "live member %s does not match SHA256SUMS" % path
            lines.append(ln)
    members["SHA256SUMS"] = ("\n".join(lines) + "\n").encode("utf-8")
    names = sorted(n for n in members if n != "SHA256SUMS") + ["SHA256SUMS"]
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.GNU_FORMAT) as tf:
        for n in names:
            data = members[n]
            ti = tarfile.TarInfo(name=n)
            ti.size = len(data)
            ti.mtime = 0
            ti.mode = 0o644
            ti.uid = ti.gid = 0
            ti.uname = ti.gname = ""
            tf.addfile(ti, io.BytesIO(data))
    gz = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=gz, mtime=0) as g:
        g.write(raw.getvalue())
    with open(out, "wb") as f:
        f.write(gz.getvalue())
    print("members=%d sha256=%s" % (len(names), hashlib.sha256(gz.getvalue()).hexdigest()))


if __name__ == "__main__":
    main()
