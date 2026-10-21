"""IRPT_ANLREQ round 60 (issuer 2.0.0_SA_COO~G2): the checks of the r34p resident release build (cell AR-g-180). READ ONLY: builds nothing,
uploads nothing, calls no AWS. Run from the repository root.

    python ar_release_p_checks.py record  <RESIDENT_R34P_BUILD.json>
    python ar_release_p_checks.py tree    <r34p tarball> <full 40-hex pin>
    python ar_release_p_checks.py scripts <stage folder>

r34p is r34o minus the registry change (CTO msg 11639, ruling A): a policy revision that has retention rows is never edited, and r34o's
edit of reporting_policies.json moved the irpt-anlreq-x10-v1 and irpt-dashbd-x10-v1 policy hashes in place (run 7e: RetentionRefused).
record: the delta against the running r34o tarball is exactly SHA256SUMS, the registry file and the bindings; nothing added or removed;
the artifact on disk has the recorded sha256, size and 323 members; the bindings moved only in provenance (package_pin, files_from_count,
files_from_sha256); the two builds are identical; smoke fail=0; gate dry runs 0, 31, 0, 33.
tree: the tarball read by this file's own code: every other member equals r34o's bytes; the registry file equals r34n's bytes; EVERY
reporting policy revision of the packaged registry has the same policy_sha256 as in the r34n tarball (computed by the packaged
lib/opal_naming.py in a fresh -I interpreter); the lazy imports import; the bindings carry the pin and 47 files-from lines.
scripts: the four host scripts exist, are ASCII, pass bash -n, name r34p as NEW and r34o as OLD, bind the tarball, the host script and the
package sums by sha256, and carry exactly one member check per mover (3 with the sums and the bindings; 1 member entry).
Prints one RESULT line: AR-RELP-<arm>-OK or AR-RELP-<arm>-FAIL <why>; rc 0 only on OK. ASCII only.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile

R34N_TAR = "C:/dev/irpt-release-r35h/irpt-resident-0485393f3a-r34n.tar.gz"
R34N_SHA = "89cad47247e6785e6b61e60112b04dfaa3cd2d5de88aef6023959692da76d899"
R34O_TAR = "C:/dev/irpt-release-r34o-g3/irpt-resident-0485393f3a-r34o.tar.gz"
R34O_SHA = "df070b09230f1e2dd1068291f6fe1f7e2078413dae6ea263b95242e09e25670b"
REG = "infra/logic/registry/reporting_policies.json"
CHANGED = ["SHA256SUMS", REG, "reports/resident_bindings.json"]
PROV_MOVES = {"package_pin", "files_from_count", "files_from_sha256"}
MEMBERS_NOW = 323
FILES_FROM = 47


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_tar(path):
    out = {}
    with tarfile.open(path) as tf:
        for m in tf.getmembers():
            if m.isfile():
                name = m.name[2:] if m.name.startswith("./") else m.name
                out[name] = tf.extractfile(m).read()
    return out


def policy_hashes(tar_path):
    """{revision: (state, policy_sha256)} computed by the tarball's own lib/opal_naming.py over its own registry."""
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(tar_path) as tf:
            tf.extractall(tmp)
        doc = json.load(open(tmp + "/" + REG, encoding="utf-8"))
        pol = doc["policies"]
        revs = sorted(x["policy_revision"] for x in pol) if isinstance(pol, list) else sorted(pol)
        code = ("import sys, json; sys.path[:0]=[%r, %r]\nimport opal_naming as n\nout = {}\nfor rev in %r:\n"
                "    x = n.reporting_policy(rev)\n    out[rev] = [x.get('state'), x.get('policy_sha256')]\nprint(json.dumps(out))\n" % (tmp + "/lib", tmp, revs))
        r = subprocess.run([sys.executable, "-I", "-B", "-c", code], capture_output=True, text=True, cwd=tmp)
        if r.returncode != 0:
            return None, (r.stderr.strip().splitlines() or ["?"])[-1][:200]
        return json.loads(r.stdout.strip().splitlines()[-1]), ""


def arm_record(path):
    fails = []
    if not os.path.isfile(path):
        return ["record absent: %s" % path]
    rec = json.load(open(path, encoding="utf-8"))
    delta = rec.get("delta_vs_r34o") or {}
    if sorted(delta.get("changed") or []) != sorted(CHANGED):
        fails.append("changed is %s want %s" % (sorted(delta.get("changed") or []), CHANGED))
    if delta.get("added") or delta.get("removed"):
        fails.append("added %s removed %s want none" % (delta.get("added"), delta.get("removed")))
    if delta.get("r34o_tarball_sha256") != R34O_SHA:
        fails.append("the base tarball sha256 is %s" % delta.get("r34o_tarball_sha256"))
    art = rec.get("artifact") or {}
    p = art.get("path", "")
    if not os.path.isfile(p):
        fails.append("the artifact is not on disk: %s" % p)
    else:
        data = open(p, "rb").read()
        if sha(data) != art.get("sha256") or len(data) != art.get("bytes"):
            fails.append("the artifact on disk is not the recorded sha256 and size")
        if len(read_tar(p)) != art.get("member_count") or art.get("member_count") != MEMBERS_NOW:
            fails.append("member_count is %s (want %d and the tarball's own count)" % (art.get("member_count"), MEMBERS_NOW))
    bd = rec.get("bindings_diff") or {}
    if bd.get("keys_added") or bd.get("keys_changed") != ["provenance"] or set(bd.get("provenance_keys_changed") or []) != PROV_MOVES:
        fails.append("bindings_diff is %s want only provenance %s" % (bd, sorted(PROV_MOVES)))
    tb = rec.get("two_builds") or {}
    if not tb.get("files_compared") or tb.get("files_compared") != tb.get("identical"):
        fails.append("two_builds not identical: %s" % tb)
    smoke = " ".join(rec.get("import_smoke") or [])
    if " fail=0 " not in smoke + " " or "live=86 imported=86" not in smoke:
        fails.append("import smoke reads %r" % smoke)
    g = rec.get("gate_dry_run") or {}
    if (g.get("gate1_unchanged_rc"), g.get("gate1_one_byte_rc"), g.get("gate2_unchanged_rc"), g.get("gate2_one_byte_rc")) != (0, 31, 0, 33):
        fails.append("gate dry runs read %s want 0, 31, 0, 33" % g)
    return fails


def arm_tree(tar_path, pin):
    fails = []
    if not re.fullmatch(r"[0-9a-f]{40}", pin or ""):
        return ["the pin is not 40-hex"]
    if not os.path.isfile(tar_path):
        return ["tarball absent: %s" % tar_path]
    if sha(open(R34O_TAR, "rb").read()) != R34O_SHA or sha(open(R34N_TAR, "rb").read()) != R34N_SHA:
        fails.append("a base tarball is not the one that ran")
    new, old, r34n = read_tar(tar_path), read_tar(R34O_TAR), read_tar(R34N_TAR)
    if len(new) != MEMBERS_NOW:
        fails.append("%d members, want %d" % (len(new), MEMBERS_NOW))
    changed = sorted(n for n in new if n in old and new[n] != old[n])
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    if changed != sorted(CHANGED) or added or removed:
        fails.append("tree delta changed=%s added=%s removed=%s" % (changed, added, removed))
    if new.get(REG) != r34n.get(REG):
        fails.append("the registry file is not byte-equal to r34n's")
    b_new = json.loads(new["reports/resident_bindings.json"])
    b_old = json.loads(old["reports/resident_bindings.json"])
    moved = sorted(k for k in b_new if b_new.get(k) != b_old.get(k))
    if moved != ["provenance"] or b_new["provenance"].get("package_pin") != pin or b_new["provenance"].get("files_from_count") != FILES_FROM:
        fails.append("bindings moved %s (want provenance only), or package_pin is not the pin, or files_from_count is not %d" % (moved, FILES_FROM))
    else:
        pm = {k for k in set(b_new["provenance"]) | set(b_old["provenance"]) if b_new["provenance"].get(k) != b_old["provenance"].get(k)}
        if pm != PROV_MOVES:
            fails.append("provenance moved %s want %s" % (sorted(pm), sorted(PROV_MOVES)))
    ph_new, err = policy_hashes(tar_path)
    ph_old, err2 = policy_hashes(R34N_TAR)
    if ph_new is None or ph_old is None:
        fails.append("policy hashes unreadable: %s %s" % (err, err2))
    elif ph_new != ph_old:
        fails.append("a reporting policy hash differs from r34n's: %s" % sorted(k for k in set(ph_new) | set(ph_old) if ph_new.get(k) != ph_old.get(k)))
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(tar_path) as tf:
            tf.extractall(tmp)
        dirs = [tmp + "/" + d for d in ("", "reports", "ycharts/generate", "ycharts/research", "ycharts/session", "intake", "ops", "lib",
                                        "_scope", "_ids", "_keys", "_authz", "_contracts")]
        code = ("import sys; sys.path[:0]=%r\n"
                "import ticket_audit_source, analysis_audit, model_source, comparables\n"
                "print('LAZY-OK')\n" % (dirs,))
        r = subprocess.run([sys.executable, "-I", "-B", "-c", code], capture_output=True, text=True, cwd=tmp)
        if "LAZY-OK" not in r.stdout:
            fails.append("lazy imports failed: %s" % (r.stderr.strip().splitlines() or ["?"])[-1][:200])
    return fails


def arm_scripts(stage):
    fails = []
    tar = stage + "/irpt-resident-0485393f3a-r34p.tar.gz"
    if not os.path.isfile(tar):
        return ["no r34p tarball in %s" % stage]
    want = sha(open(tar, "rb").read())
    for name in ("pre_read_r34.sh", "install_r34.sh", "rollback_r34.sh", "resident_host_install_0485393f3a-r34p.sh"):
        p = "%s/scripts/%s" % (stage, name)
        if not os.path.isfile(p):
            fails.append("%s absent" % name)
            continue
        data = open(p, "rb").read()
        if any(c > 127 for c in data):
            fails.append("%s is not ASCII" % name)
        if subprocess.run(["bash", "-n", p], capture_output=True).returncode != 0:
            fails.append("%s fails bash -n" % name)
        text = data.decode("ascii", "replace")
        if name != "resident_host_install_0485393f3a-r34p.sh" and ("NEW=0485393f3a-r34p" not in text or "OLD=0485393f3a-r34o" not in text):
            fails.append("%s does not name NEW r34p and OLD r34o" % name)
        if name == "resident_host_install_0485393f3a-r34p.sh":
            if "WANT_TAR=" + want not in text:
                fails.append("the host script WANT_TAR is not the tarball sha256")
            n = len(re.findall(r'^check "', text, re.M))
            if n != len(CHANGED):
                fails.append("the host script carries %d member checks, want %d" % (n, len(CHANGED)))
        if name == "install_r34.sh":
            host_p = "%s/scripts/resident_host_install_0485393f3a-r34p.sh" % stage
            if "WANT=" + sha(open(host_p, "rb").read()) not in text:
                fails.append("install_r34.sh WANT is not the host script sha256")
            sums = read_tar(tar).get("SHA256SUMS", b"")
            if "WANTSUM=" + sha(sums) not in text:
                fails.append("install_r34.sh WANTSUM is not the tarball's SHA256SUMS member sha256")
            n = len(re.findall(r'^  "[^ "]+ [0-9a-f]{64}"', text, re.M))
            if n != len(CHANGED) - 2:
                fails.append("install_r34.sh carries %d member entries, want %d" % (n, len(CHANGED) - 2))
    return fails


def main():
    arm = sys.argv[1] if len(sys.argv) > 1 else ""
    if arm == "record" and len(sys.argv) == 3:
        fails = arm_record(sys.argv[2])
    elif arm == "tree" and len(sys.argv) == 4:
        fails = arm_tree(sys.argv[2], sys.argv[3])
    elif arm == "scripts" and len(sys.argv) == 3:
        fails = arm_scripts(sys.argv[2].replace("\\", "/"))
    else:
        print("usage: ar_release_p_checks.py record <record> | tree <tar> <pin> | scripts <stage>")
        sys.exit(2)
    if fails:
        print("AR-RELP-%s-FAIL %s" % (arm, "; ".join(fails)[:900]))
        sys.exit(1)
    print("AR-RELP-%s-OK" % arm)


if __name__ == "__main__":
    main()
