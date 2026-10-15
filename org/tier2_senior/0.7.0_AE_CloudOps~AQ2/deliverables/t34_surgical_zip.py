"""IRPT_ANLREQ TO-APPLY-t34 amendment 1 (route B): assemble the SURGICAL zip and print the three proofs.

usage: python t34_surgical_zip.py <live.zip> <out.zip> <repo> <pin> <work-dir-outside-repo>

Takes the fetched LIVE zip, copies every member (same order, same ZipInfo, same bytes) and replaces EXACTLY the three
commentary members with the bytes of `git cat-file blob <pin>:<path>`. Adds nothing, removes nothing. Not a build.sh output.
Prints: the live and surgical base64 sha256 and member counts; proof (i) the three replaced members byte-equal to the pin's
blobs (sha256 each, git blob id re-derived); proof (ii) every other member byte-equal to the live zip's (count that differs);
proof (iii) a clean `python -I` import of the three modules from the extract, working directory outside the repo.
Reads and writes outside the repo only (the out zip and the work dir). Exit 0 only when every proof holds.
"""
from __future__ import annotations

import base64
import hashlib
import io
import os
import subprocess
import sys
import zipfile

MEMBERS = (
    "data/transcripts/scripts/commentary/lambda_handler.py",
    "data/transcripts/scripts/commentary/drafter.py",
    "data/transcripts/scripts/commentary/entry.py",
)


def b64(data):
    return base64.b64encode(hashlib.sha256(data).digest()).decode()


def git_blob(repo, pin, path):
    r = subprocess.run(["git", "-C", repo, "cat-file", "blob", "%s:%s" % (pin, path)], capture_output=True)
    if r.returncode:
        raise SystemExit("ERROR: git cat-file blob %s:%s rc=%s" % (pin, path, r.returncode))
    want = subprocess.run(["git", "-C", repo, "rev-parse", "%s:%s" % (pin, path)], capture_output=True, text=True).stdout.strip()
    got = hashlib.sha1(b"blob %d\0" % len(r.stdout) + r.stdout).hexdigest()
    if got != want:
        raise SystemExit("ERROR: blob id mismatch for %s (got %s want %s)" % (path, got, want))
    return r.stdout


def main(argv):
    live_path, out_path, repo, pin, work = argv[1:6]
    live = open(live_path, "rb").read()
    zl = zipfile.ZipFile(io.BytesIO(live))
    infos = zl.infolist()
    names = [i.filename for i in infos]
    for m in MEMBERS:
        if names.count(m) != 1:
            raise SystemExit("ERROR: %s appears %d times in the live zip" % (m, names.count(m)))
    new = {m: git_blob(repo, pin, m) for m in MEMBERS}
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zo:
        for i in infos:
            data = new[i.filename] if i.filename in new else zl.read(i.filename)
            zi = zipfile.ZipInfo(i.filename, i.date_time)
            zi.compress_type = i.compress_type
            zi.external_attr = i.external_attr
            zi.create_system = i.create_system
            zo.writestr(zi, data)
    out = buf.getvalue()
    open(out_path, "wb").write(out)
    zs = zipfile.ZipFile(io.BytesIO(out))
    print("LIVE      bytes %d members %d base64 sha256 %s" % (len(live), len(infos), b64(live)))
    print("SURGICAL  bytes %d members %d base64 sha256 %s" % (len(out), len(zs.infolist()), b64(out)))
    ok = True
    # (i) the three replaced members are byte-equal to the pin's blobs
    hit = 0
    for m in MEMBERS:
        s = hashlib.sha256(zs.read(m)).hexdigest()
        same = zs.read(m) == new[m]
        hit += 1 if same else 0
        print("PROOF-i   %s sha256 %s %s" % (m, s, "EQUAL-TO-PIN" if same else "DIFFERS-FROM-PIN"))
    print("PROOF-i   %d of 3 byte-equal to git blob at %s" % (hit, pin))
    ok = ok and hit == 3
    # (ii) every other member byte-equal to the live zip's; same names in the same order
    same_order = [i.filename for i in zs.infolist()] == names
    differ = [n for n in names if zl.read(n) != zs.read(n)]
    print("PROOF-ii  members %d, same names and order %s, members that differ from live: %d %s" % (len(names), same_order, len(differ), sorted(differ)))
    ok = ok and same_order and sorted(differ) == sorted(MEMBERS)
    # (iii) clean-interpreter import of the three modules from the extract, cwd outside the repo
    ext = os.path.join(work, "surgical_x")
    zs.extractall(ext)
    for m in ("lambda_handler", "drafter", "entry"):
        code = "import sys; sys.path.insert(0, %r); import data.transcripts.scripts.commentary.%s as x; print('IMPORT-OK commentary.%s from', x.__file__.replace(chr(92), '/').split('surgical_x/')[-1])" % (ext, m, m)
        r = subprocess.run([sys.executable, "-I", "-c", code], cwd=work, capture_output=True, text=True)
        line = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
        print("PROOF-iii rc=%d %s%s" % (r.returncode, line, "" if r.returncode == 0 else " :: " + r.stderr.strip()[-200:]))
        ok = ok and r.returncode == 0 and line.startswith("IMPORT-OK")
    print("ALL-PROOFS-HOLD" if ok else "PROOF-MISS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
