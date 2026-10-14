"""Independent member-by-member comparison of the r29 live tarball and the staged r30 tarball (ASCII only).

usage: python -I compare_r30.py <live tar.gz> <release tar.gz> <extract dir for live (new, empty)> <extract dir for release (new, empty)> <out json>
Reads both tarballs with tarfile, extracts each into its own new empty folder, and compares by member name and sha256.
"""
import hashlib
import json
import os
import sys
import tarfile

LIVE, REL, EX_LIVE, EX_REL, OUT = sys.argv[1:6]


def load(tar_path, dest):
    if os.path.exists(dest) and os.listdir(dest):
        raise SystemExit("extract dir is not empty: " + dest)
    os.makedirs(dest, exist_ok=True)
    members = {}
    with tarfile.open(tar_path, "r:gz") as tf:
        for m in tf.getmembers():
            if not m.isfile():
                raise SystemExit("non-file member: " + m.name)
            name = m.name[2:] if m.name.startswith("./") else m.name
            if name in members:
                raise SystemExit("duplicate member: " + name)
            data = tf.extractfile(m).read()
            target = os.path.join(dest, *name.split("/"))
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as fh:
                fh.write(data)
            members[name] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "mode": oct(m.mode)}
    return members


live = load(LIVE, EX_LIVE)
rel = load(REL, EX_REL)
differing = sorted(n for n in live if n in rel and live[n]["sha256"] != rel[n]["sha256"])
only_in_live = sorted(n for n in live if n not in rel)
only_in_release = sorted(n for n in rel if n not in live)
unchanged = sum(1 for n in live if n in rel and live[n]["sha256"] == rel[n]["sha256"])
modes = sorted({v["mode"] for v in rel.values()})

sums_live = live["SHA256SUMS"]
sums_rel = rel["SHA256SUMS"]


def read_text(base, name):
    with open(os.path.join(base, *name.split("/")), "r", encoding="utf-8") as fh:
        return fh.read()


bind_live = json.loads(read_text(EX_LIVE, "reports/resident_bindings.json"))
bind_rel = json.loads(read_text(EX_REL, "reports/resident_bindings.json"))


def flat(obj, prefix=""):
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(flat(v, prefix + "." + k if prefix else k))
    elif isinstance(obj, list):
        out[prefix] = json.dumps(obj, sort_keys=True)
    else:
        out[prefix] = json.dumps(obj, sort_keys=True)
    return out


fl, fr = flat(bind_live), flat(bind_rel)
bindings_changed = sorted(k for k in set(fl) | set(fr) if fl.get(k) != fr.get(k))

result = {
    "live_members_including_SHA256SUMS": len(live),
    "release_members_including_SHA256SUMS": len(rel),
    "unchanged": unchanged,
    "delta_vs_live": differing,
    "delta_count": len(differing),
    "only_in_live": only_in_live,
    "only_in_release": only_in_release,
    "removed_members_count": len(only_in_live),
    "release_member_modes": modes,
    "bindings_changed_keys": bindings_changed,
    "bindings_live_provenance": bind_live.get("provenance"),
    "bindings_release_provenance": bind_rel.get("provenance"),
    "release_sha256sums_sha256": sums_rel["sha256"],
    "live_sha256sums_sha256": sums_live["sha256"],
    "release_sha256sums_bytes": sums_rel["bytes"],
    "release_sha256sums_lines": None,
}
with open(os.path.join(EX_REL, "SHA256SUMS"), "r", encoding="utf-8") as fh:
    result["release_sha256sums_lines"] = sum(1 for _ in fh)
with open(OUT, "w", encoding="ascii", newline="\n") as fh:
    json.dump(result, fh, indent=1, sort_keys=True)
    fh.write("\n")
print(json.dumps({k: v for k, v in result.items() if not k.startswith("bindings_") or k == "bindings_changed_keys"}, indent=1, sort_keys=True))
