"""Compare a local rebuild directory with the recorded st32 release tar, by NAME and by CONTENT.

Read-only on both inputs. Prints one JSON document. ASCII only.
usage: python -I compare_st32.py <st32 tar> <rebuild dir> <out json>
"""
import hashlib
import json
import os
import sys
import tarfile

TAR, REBUILD, OUT = sys.argv[1], sys.argv[2], sys.argv[3]


def sha(data):
    return hashlib.sha256(data).hexdigest()


tar_members = {}
with tarfile.open(TAR, "r:gz") as t:
    for m in t.getmembers():
        if not m.isfile():
            continue
        name = m.name[2:] if m.name.startswith("./") else m.name
        tar_members[name] = t.extractfile(m).read()

local = {}
for dp, dn, fn in os.walk(REBUILD):
    for f in fn:
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, REBUILD).replace(os.sep, "/")
        with open(p, "rb") as fh:
            local[rel] = fh.read()

tar_names = set(tar_members)
loc_names = set(local)
common = sorted(tar_names & loc_names)
matched_by_name = len(common)
matched_by_content = []
differing = []
for n in common:
    if sha(tar_members[n]) == sha(local[n]):
        matched_by_content.append(n)
    else:
        differing.append({"name": n, "st32_sha256": sha(tar_members[n]), "rebuild_sha256": sha(local[n])})

# The two generated members: explain the difference, do not hide it.
explain = {}
bind_diff = [d for d in differing if d["name"] == "reports/resident_bindings.json"]
if bind_diff:
    a = json.loads(tar_members["reports/resident_bindings.json"].decode("utf-8"))
    b = json.loads(local["reports/resident_bindings.json"].decode("utf-8"))
    keys_differ = []
    for k in sorted(set(a) | set(b)):
        if k == "provenance":
            pa, pb = dict(a.get(k, {})), dict(b.get(k, {}))
            for kk in sorted(set(pa) | set(pb)):
                if pa.get(kk) != pb.get(kk):
                    keys_differ.append("provenance." + kk)
        elif a.get(k) != b.get(k):
            keys_differ.append(k)
    explain["bindings_differing_keys"] = keys_differ
    explain["bindings_st32_generated_at"] = a.get("provenance", {}).get("generated_at")
    explain["bindings_rebuild_generated_at"] = b.get("provenance", {}).get("generated_at")

st32_only = sorted(tar_names - loc_names)
rebuild_only = sorted(loc_names - tar_names)

# SHA256SUMS: the st32 member sums are checked against the st32 members themselves (self-consistency),
# and the rebuild's sums are compared with st32's line by line.
def parse_sums(text):
    out = {}
    for line in text.decode("utf-8").splitlines():
        if line.strip():
            d, p = line.split("  ", 1)
            out[p] = d
    return out

st32_sums = parse_sums(tar_members["SHA256SUMS"])
st32_self = {n: sha(tar_members[n]) for n in tar_members if n != "SHA256SUMS"}
self_bad = sorted(n for n in st32_self if st32_sums.get(n) != st32_self[n])
self_missing = sorted(set(st32_sums) - set(st32_self))
reb_sums = parse_sums(local["SHA256SUMS"])
sums_differ = sorted(n for n in set(st32_sums) | set(reb_sums) if st32_sums.get(n) != reb_sums.get(n))

result = {
    "st32_tar_members_including_SHA256SUMS": len(tar_names),
    "rebuild_members_including_SHA256SUMS": len(loc_names),
    "matched_by_name": matched_by_name,
    "matched_by_content": len(matched_by_content),
    "differing_by_content": differing,
    "st32_only_names": st32_only,
    "rebuild_only_names": rebuild_only,
    "st32_sha256sums_self_check": {"members_checked": len(st32_self), "bad": self_bad, "listed_but_absent": self_missing},
    "sha256sums_lines_differing_from_st32": sums_differ,
    "explain": explain,
}
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(result, fh, indent=1, sort_keys=True)
    fh.write("\n")
print(json.dumps({k: v for k, v in result.items() if k not in ("st32_only_names", "rebuild_only_names")}, indent=1, sort_keys=True))
print("st32_only_names", len(st32_only), "rebuild_only_names", len(rebuild_only))
