"""Package a builder output directory as a tar.gz (names './<member>', deterministic metadata) and compute the
delta between the recorded st32 tar (old) and the release tar (new). Prints one JSON document. ASCII only.

usage: python -I pack_and_delta.py <dir> <out tar.gz> <st32 tar> <A1 builder-only tar> <out json> <sources json>
"""
import hashlib
import io
import json
import os
import sys
import tarfile

DIR, OUT_TAR, ST32_TAR, A1_TAR, OUT_JSON = sys.argv[1:6]
SOURCES = json.load(open(sys.argv[6], encoding="utf-8"))


def sha(b):
    return hashlib.sha256(b).hexdigest()


# 1. package the release directory: names './<member>' as in the st32 artifact; sorted; uid/gid/mtime zero
members = {}
for dp, dn, fn in os.walk(DIR):
    for f in fn:
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, DIR).replace(os.sep, "/")
        with open(p, "rb") as fh:
            members[rel] = fh.read()
with tarfile.open(OUT_TAR, "w:gz") as tar:
    for name in sorted(members, key=lambda n: ("" if n == "SHA256SUMS" else n)):
        data = members[name]
        ti = tarfile.TarInfo(name="./" + name)
        ti.size = len(data)
        ti.mode = 0o644
        ti.mtime = 0
        tar.addfile(ti, io.BytesIO(data))
pack_sha = hashlib.sha256(open(OUT_TAR, "rb").read()).hexdigest()


def read_tar(path):
    out = {}
    with tarfile.open(path, "r:gz") as t:
        for m in t.getmembers():
            if m.isfile():
                n = m.name[2:] if m.name.startswith("./") else m.name
                out[n] = t.extractfile(m).read()
    return out


new = members
old = read_tar(ST32_TAR)
a1 = read_tar(A1_TAR)

GEN = {"SHA256SUMS"}
old_names = set(old) - GEN
new_names = set(new) - GEN
only_old = sorted(old_names - new_names)
only_new = sorted(new_names - old_names)
both = sorted(old_names & new_names)
differing = []
for n in both:
    if sha(old[n]) != sha(new[n]):
        differing.append({"member": n,
                          "old_sha256": sha(old[n]), "new_sha256": sha(new[n]),
                          "old_source": SOURCES.get(n, {}).get("old_source"),
                          "new_source": SOURCES.get(n, {}).get("new_source")})
sums_differs = sha(old["SHA256SUMS"]) != sha(new["SHA256SUMS"])

readers = ["intake/template_reader.py", "intake/uploads.py"]
moved = [d for d in differing if d["member"] in readers]
other = [d for d in differing if d["member"] not in readers]

recipe_vs_builder_alone = {
    "in_recipe_release_not_in_builder_alone": sorted(set(new) - set(a1)),
    "in_builder_alone_not_in_recipe_release": sorted(set(a1) - set(new)),
}

result = {
    "old_tar": ST32_TAR,
    "new_tar": OUT_TAR,
    "new_tar_sha256": pack_sha,
    "old_members_including_SHA256SUMS": len(old),
    "new_members_including_SHA256SUMS": len(new),
    "old_members_excluding_SHA256SUMS": len(old_names),
    "new_members_excluding_SHA256SUMS": len(new_names),
    "unchanged_count": len(both) - len(differing),
    "only_in_old": [{"member": n, "old_sha256": sha(old[n])} for n in only_old],
    "only_in_new": [{"member": n, "new_sha256": sha(new[n])} for n in only_new],
    "differing_count": len(differing),
    "differing": differing,
    "SHA256SUMS_differs": sums_differs,
    "moved_by_this_release": moved,
    "other_differing": other,
    "builder_alone_comparison": recipe_vs_builder_alone,
}
with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(result, fh, indent=1, sort_keys=True)
    fh.write("\n")
print("new tar sha256", pack_sha)
print("old members", len(old), "new members", len(new), "old names", len(old_names), "new names", len(new_names))
print("only_in_old", len(only_old), "only_in_new", len(only_new), "differing", len(differing), "moved", len(moved), "other", len(other), "unchanged", result["unchanged_count"])
print("SHA256SUMS differs", sums_differs)
