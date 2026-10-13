"""AR-y-227 scratch packer and delta (outside the product tree's shipped output; prints one JSON document, ASCII only).

usage: python -I pack_one.py <build dir> <out tar.gz> <r19 base tar.gz> <second build dir or -> <out json>
- packs <build dir> as names './<member>', SHA256SUMS first, sorted, mode 0644, uid/gid/mtime zero, gzip mtime zero
- delta vs the release-19 tarball (member bytes by name), and the two-build determinism control when a second dir is given
"""
import gzip
import hashlib
import io
import json
import os
import sys
import tarfile

BUILD, OUT_TAR, BASE_TAR, SECOND, OUT_JSON = sys.argv[1:6]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read_dir(d):
    out = {}
    for dp, dn, fn in os.walk(d):
        for f in fn:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, d).replace(os.sep, "/")
            with open(p, "rb") as fh:
                out[rel] = fh.read()
    return out


def read_tar(path):
    out = {}
    with tarfile.open(path, "r:gz") as t:
        for m in t.getmembers():
            if m.isfile():
                n = m.name[2:] if m.name.startswith("./") else m.name
                out[n] = t.extractfile(m).read()
    return out


members = read_dir(BUILD)
with open(OUT_TAR, "wb") as raw:
    with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w") as tar:
            for name in sorted(members, key=lambda n: ("" if n == "SHA256SUMS" else n)):
                data = members[name]
                ti = tarfile.TarInfo(name="./" + name)
                ti.size = len(data)
                ti.mode = 0o644
                ti.mtime = 0
                ti.uid = ti.gid = 0
                ti.uname = ti.gname = ""
                tar.addfile(ti, io.BytesIO(data))
tar_sha = sha(open(OUT_TAR, "rb").read())
shipped = read_tar(OUT_TAR)
assert shipped == members, "the shipped tar does not carry exactly the build dir's bytes"

base = read_tar(BASE_TAR)
differing = []
for name in sorted(set(base) & set(members)):
    if base[name] != members[name]:
        differing.append({"member": name, "old_sha256": sha(base[name]), "new_sha256": sha(members[name])})
only_old = sorted(set(base) - set(members))
only_new = sorted(set(members) - set(base))

doc = {
    "tarball": {"path": OUT_TAR, "sha256": tar_sha, "members_including_SHA256SUMS": len(shipped),
                "members_excluding_SHA256SUMS": len(shipped) - 1},
    "base": {"path": BASE_TAR, "sha256": sha(open(BASE_TAR, "rb").read()), "members_including_SHA256SUMS": len(base)},
    "delta": {"differing": differing, "differing_count": len(differing), "only_in_old": only_old,
              "only_in_new": only_new, "removed_members_count": len(only_old),
              "unchanged_count": len(set(base) & set(members)) - len(differing)},
}
if SECOND != "-":
    other = read_dir(SECOND)
    same = [n for n in members if n in other and other[n] == members[n]]
    doc["determinism_control"] = {"second_build_dir": SECOND, "files_compared": len(members),
                                  "identical_by_name_and_sha256": len(same),
                                  "names_only_in_one": sorted(set(members) ^ set(other))}
open(OUT_JSON, "w", encoding="utf-8").write(json.dumps(doc, indent=1, sort_keys=True) + "\n")
print(json.dumps(doc, indent=1, sort_keys=True))
