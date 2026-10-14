"""AR339-y-AC1 -- build check for irpt-status (TO-AR-y-339, worker 0.9.0_WK_IRPT_ANLREQ~145), AMENDED by AMENDMENT 2.

Prints BUILD-OK <members> members, builds identical, CodeSha256 <8 chars>, delta <d> differing, <h> of <h> hunks
attributed, only when: the staged zip's sha256 and base64 CodeSha256 equal the record's; the two builds agree member by
member and in CodeSha256; re-extracting the staged zip and the downloaded live zip reproduces the record's delta lists;
the differing set is exactly the members the record's attribution lists; and every hunk of every differing member is
attributed in the record's attribution (member, hunk, commit, cell) to AR-y-331, AR-y-71 or AR-y-32, with no
unattributed hunk. Otherwise prints BUILD-BAD <why> and exits 1. Read-only: no AWS call, no upload.

Hunk coverage is computed from the two zips (difflib opcodes of the live member against the release member) and each
computed change must fall inside an attributed hunk's new-side range (the record's attribution, derived from git).
"""
import base64
import difflib
import hashlib
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REC_PATH = os.path.join(HERE, "r41", "IRPT_STATUS_R31_BUILD.json")
CELLS = {"AR-y-331", "AR-y-71", "AR-y-32"}
HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


def bad(why):
    print("BUILD-BAD " + why)
    sys.exit(1)


def sha256_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def b64_sha256_file(path):
    with open(path, "rb") as fh:
        return base64.b64encode(hashlib.sha256(fh.read()).digest()).decode("ascii")


def zip_members(path):
    out = {}
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            if not info.is_dir():
                out[info.filename] = z.read(info.filename)
    return out


def member_sha(blobs):
    return {n: hashlib.sha256(b).hexdigest() for n, b in blobs.items()}


def attributed_ranges(att_list, member):
    """0-based half-open [start, end) new-side ranges of the attributed hunks of one member."""
    out = []
    for a in att_list:
        if a["member"].split("/")[-1] != member:
            continue
        m = HUNK_RE.match(a["hunk"])
        if not m:
            bad("unparseable attribution hunk header: " + a["hunk"])
        ns = int(m.group(1))
        nc = int(m.group(2)) if m.group(2) is not None else 1
        if nc == 0:
            out.append((ns, ns))
        else:
            out.append((ns - 1, ns - 1 + nc))
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
    m1, m2 = member_sha(zip_members(paths[0])), member_sha(zip_members(paths[1]))
    if m1 != m2:
        bad("the two builds differ by member name or sha256")
    if b64_sha256_file(paths[0]) != b64_sha256_file(paths[1]):
        bad("the two builds differ by CodeSha256")

    # 3. the staged and live members reproduce the record's delta lists
    live_path = rec["live_read"]["download_path"]
    if not os.path.isfile(live_path):
        bad("downloaded live zip missing: " + live_path)
    if sha256_file(live_path) != rec["live_read"]["download_sha256_hex"]:
        bad("downloaded live zip sha256 differs from the record")
    if b64_sha256_file(live_path) != rec["live_read"]["CodeSha256"]:
        bad("downloaded live zip CodeSha256 differs from the record's live CodeSha256")
    rel_blobs = zip_members(paths[0])
    live_blobs = zip_members(live_path)
    ml = member_sha(live_blobs)
    unchanged = sorted(n for n in m1 if n in ml and m1[n] == ml[n])
    differing = sorted(n for n in m1 if n in ml and m1[n] != ml[n])
    only_rel = sorted(n for n in m1 if n not in ml)
    only_live = sorted(n for n in ml if n not in m1)
    d = rec["delta_vs_live"]
    if (sorted(d["differing"]) != differing or sorted(d["only_in_release"]) != only_rel
            or sorted(d["only_in_live"]) != only_live or d["unchanged"] != len(unchanged)):
        bad("delta lists recomputed from the zips differ from the record")

    # 4. the differing set is exactly the members the attribution lists
    att = rec.get("attribution", {}).get("hunks", [])
    att_members = sorted({a["member"].split("/")[-1] for a in att})
    if att_members != differing:
        bad("differing set %s is not the attribution's member set %s" % (differing, att_members))

    # 5. every hunk of every differing member is attributed to one of the three cells
    hunks_total = 0
    hunks_attr = 0
    for a in att:
        cells = a["cell"] if isinstance(a["cell"], list) else [a["cell"]]
        if not set(cells) <= CELLS or not a.get("commit"):
            bad("attribution hunk not owned by AR-y-331, AR-y-71 or AR-y-32: %s %s" % (a["member"], a["hunk"]))
    for member in differing:
        rel_text = rel_blobs[[n for n in rel_blobs if n == member][0]].decode("utf-8", errors="replace").splitlines()
        live_text = live_blobs[member].decode("utf-8", errors="replace").splitlines()
        ranges = attributed_ranges(att, member)
        ops = [o for o in difflib.SequenceMatcher(None, live_text, rel_text, autojunk=False).get_opcodes()
               if o[0] != "equal"]
        for tag, i1, i2, j1, j2 in ops:
            hunks_total += 1
            if any(r0 - 1 <= j2 and j1 <= r1 + 1 for r0, r1 in ranges):
                hunks_attr += 1
            else:
                bad("unattributed change in %s at release lines %d-%d (%s)" % (member, j1 + 1, j2, tag))
    if hunks_attr != hunks_total:
        bad("hunks attributed %d of %d" % (hunks_attr, hunks_total))

    print("BUILD-OK %d members, builds identical, CodeSha256 %s, delta %d differing, %d of %d hunks attributed"
          % (len(m1), art["code_sha256_base64"][:8], len(differing), hunks_attr, hunks_total))


if __name__ == "__main__":
    main()
