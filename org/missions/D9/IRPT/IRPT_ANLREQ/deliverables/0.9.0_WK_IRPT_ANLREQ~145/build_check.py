"""AR339-y-AC1 -- build check for irpt-status (TO-AR-y-339, worker 0.9.0_WK_IRPT_ANLREQ~145).

Prints BUILD-OK only when the staged zip and its record agree; otherwise BUILD-BAD <why> and exit 1.
Reads the record r41/IRPT_STATUS_R31_BUILD.json next to this file. Read-only: no AWS call, no upload.
"""
import base64
import hashlib
import json
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REC_PATH = os.path.join(HERE, "r41", "IRPT_STATUS_R31_BUILD.json")
# Members the order expects to differ (zip member names). A differing member outside this set
# must be explained by a surprise row named in the record (delta_vs_live.explained_by_surprise).
EXPECTED_DIFFERING = {"entry.py", "owned_report.py", "pdf_link.py", "status_installed.py"}


def bad(why):
    print("BUILD-BAD " + why)
    sys.exit(1)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def b64_sha256_file(path):
    with open(path, "rb") as fh:
        return base64.b64encode(hashlib.sha256(fh.read()).digest()).decode("ascii")


def zip_manifest(path):
    out = {}
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            out[info.filename] = hashlib.sha256(z.read(info.filename)).hexdigest()
    return out


def main():
    if not os.path.isfile(REC_PATH):
        bad("record missing: " + REC_PATH)
    rec = json.load(open(REC_PATH, encoding="utf-8"))
    art = rec.get("artifact", {})
    zpath = art.get("path")
    if not zpath or not os.path.isfile(zpath):
        bad("no staged zip (record artifact.path=%r): %s" % (zpath, art.get("status_reason", "")))

    # 1. the staged zip is the one the record names
    if sha256_file(zpath) != art.get("sha256"):
        bad("staged zip sha256 differs from the record")
    if b64_sha256_file(zpath) != art.get("code_sha256_base64"):
        bad("staged zip CodeSha256 (base64) differs from the record")

    # 2. two builds agree member by member and in CodeSha256
    tb = rec.get("two_builds", {})
    paths = tb.get("paths", [])
    if len(paths) != 2 or not all(os.path.isfile(p) for p in paths):
        bad("two builds not both present (two_builds.completed=%r)" % tb.get("completed"))
    m1, m2 = zip_manifest(paths[0]), zip_manifest(paths[1])
    if m1 != m2:
        bad("the two builds differ by member name or sha256")
    if b64_sha256_file(paths[0]) != b64_sha256_file(paths[1]):
        bad("the two builds differ by CodeSha256")

    # 3. the staged zip's members and the downloaded live zip reproduce the record's delta lists
    live_path = rec["live_read"]["download_path"]
    if not os.path.isfile(live_path):
        bad("downloaded live zip missing: " + live_path)
    if sha256_file(live_path) != rec["live_read"]["download_sha256_hex"]:
        bad("downloaded live zip sha256 differs from the record")
    if b64_sha256_file(live_path) != rec["live_read"]["CodeSha256"]:
        bad("downloaded live zip CodeSha256 differs from the record's live CodeSha256")
    ml = zip_manifest(live_path)
    unchanged = sorted(n for n in m1 if n in ml and m1[n] == ml[n])
    differing = sorted(n for n in m1 if n in ml and m1[n] != ml[n])
    only_rel = sorted(n for n in m1 if n not in ml)
    only_live = sorted(n for n in ml if n not in m1)
    d = rec["delta_vs_live"]
    if (sorted(d["differing"]) != differing or sorted(d["only_in_release"]) != only_rel
            or sorted(d["only_in_live"]) != only_live or d["unchanged"] != len(unchanged)):
        bad("delta lists recomputed from the zips differ from the record")

    # 4. every differing member is expected (step 3) or explained by a named surprise row
    explained = d.get("explained_by_surprise", {})
    stray = [n for n in differing if n not in EXPECTED_DIFFERING and n not in explained]
    if stray:
        bad("differing member(s) not expected and not explained by a surprise row: " + ", ".join(stray))

    print("BUILD-OK %d members, builds identical, CodeSha256 %s, delta %d differing"
          % (len(m1), art["code_sha256_base64"][:8], len(differing)))


if __name__ == "__main__":
    main()
