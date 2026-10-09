"""IB-pr-402 narrow packer: one live per-firm holdings bundle with ONE member replaced, every other member byte-identical.

Usage: python -I narrow_pack.py <repo_root> <live_tree_dir> <out_file> [<member_name> <replacement_file>]
  <live_tree_dir>  the live bundle extracted into its own directory (SHA256SUMS included; it is regenerated, not copied)
  no replacement   the CONTROL: repacks the live members unchanged; the output must equal the live bytes
It drives the mint's own deterministic builder (safe_deploy_core.build_bundle_payload, manifest-stamp mode: sorted members,
zeroed mtime/uid/gid, gzip mtime=0, SHA256SUMS appended) over a member set read from the live tree. Nothing is uploaded.
Prints one JSON line: sha256, md5, bytes, members, shas.
"""
import hashlib
import json
import os
import pathlib
import sys


def main():
    root, tree, out = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve(), pathlib.Path(sys.argv[3])
    repl = {sys.argv[4]: pathlib.Path(sys.argv[5]).resolve()} if len(sys.argv) > 5 else {}
    sys.path.insert(0, str(root / ".tools"))
    import safe_deploy_core as sdc

    names = []
    for dirpath, _dirs, files in os.walk(str(tree)):
        for fn in files:
            names.append(os.path.relpath(os.path.join(dirpath, fn), str(tree)).replace(os.sep, "/"))
    names = sorted(n for n in names if n != "SHA256SUMS")
    for m in repl:
        if m not in names:
            raise SystemExit("REFUSED: %s is not a member of the live bundle" % m)
    members = {}
    for n in names:
        members[n] = {"repo_path": str(repl[n]) if n in repl else str(tree / n.replace("/", os.sep))}
    sdc.WORKSPACE = pathlib.Path("/")  # every repo_path above is absolute, so the join keeps it as is
    payload, shas, err = sdc.build_bundle_payload({"stamp": "manifest", "members": members})
    if payload is None:
        raise SystemExit("REFUSED: " + err)
    out.write_bytes(payload)
    print(json.dumps({"sha256": hashlib.sha256(payload).hexdigest(), "md5": hashlib.md5(payload).hexdigest(),  # noqa: S324
                      "bytes": len(payload), "members": len(names), "shas": shas}))


if __name__ == "__main__":
    main()
