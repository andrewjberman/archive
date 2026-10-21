"""IRPT_ANLREQ round 60 (issuer 2.0.0_SA_COO~G2): the checks of the r34q resident release build. READ ONLY: builds nothing, uploads nothing,
calls no AWS. Run from the repository root with a python that has jsonschema and referencing (not `-I`) for the tree arm.

    python ar_release_q_checks.py record  <RESIDENT_R34Q_BUILD.json>
    python ar_release_q_checks.py tree    <r34q tarball> <full 40-hex pin>
    python ar_release_q_checks.py scripts <stage folder>

r34q = r34p plus: (1) the S245 fix, ycharts/generate/submission.py (the packaged copy lacked commentary_requested, so a Comparison or Multi-Comp
request was refused at the resident's replay of the frozen composition); (2) 2.0.0_SA_COO~Y2's tickets_table binding (AR-y-483/484: the
resident reads the optional binding, the builder writes "opal-tickets") and the audit modules that go with it (reports/analysis_audit.py,
reports/resident_installed.py, reports/build_resident_package.py); (3) the registry file with the NEW revision irpt-anlreq-audit-x10-v1 ACTIVE.
record: the delta against the running r34p tarball is exactly the seven members; nothing added or removed; the artifact on disk has the
recorded sha256, size and 323 members; the bindings gained only tickets_table and moved only in provenance; the two builds are identical;
smoke fail=0; gate dry runs 0, 31, 0, 33.
tree: the tarball read by this file's own code: every other member equals r34p's bytes; each mover equals `git show <pin>:<source>`; EVERY
revision the r34n registry carried keeps its policy_sha256 in the packaged registry (the one tolerated exception: irpt-dashbd-x10-v1, PENDING_ENFORCEMENT in both trees, which can hold no retention rows) (computed by the tarball's own lib/opal_naming.py in a
fresh interpreter), irpt-anlreq-audit-x10-v1 is present and ACTIVE and is the only addition; the bindings carry the pin, 49 files-from lines
and tickets_table `opal-tickets`; the lazy imports import; and THE ADMISSION REPLAY (ar_admission_replay.py on 7H's retained synthetic
Multi-Comp composition) passes all five steps, which the r34o and r34p tarballs fail at step 3.
scripts: the four host scripts exist, are ASCII, pass bash -n, name r34q as NEW and r34p as OLD, bind the tarball, the host script and the
package sums by sha256, and carry exactly one member check per mover (7 with the sums and the bindings; 5 member entries).
Prints one RESULT line: AR-RELQ-<arm>-OK or AR-RELQ-<arm>-FAIL <why>; rc 0 only on OK. ASCII only.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LAM = "infra/aws/lambda/investor-reporting/"
R34N_TAR = "C:/dev/irpt-release-r35h/irpt-resident-0485393f3a-r34n.tar.gz"
R34N_SHA = "89cad47247e6785e6b61e60112b04dfaa3cd2d5de88aef6023959692da76d899"
R34P_TAR = "C:/dev/irpt-release-r34p-g2/irpt-resident-0485393f3a-r34p.tar.gz"
R34P_SHA = "4991c7bcba0f01cb47b06bfa8c4e30f3fe47a6cbd6e9b9f479d1d39b77b49ea4"
REG = "infra/logic/registry/reporting_policies.json"
NEW_REVISION = "irpt-anlreq-audit-x10-v1"
CHANGED = ["SHA256SUMS", REG, "reports/analysis_audit.py", "reports/build_resident_package.py", "reports/resident_bindings.json",
           "reports/resident_installed.py", "ycharts/generate/submission.py"]
SOURCE = {"SHA256SUMS": None, "reports/resident_bindings.json": None, REG: REG}
PROV_MOVES = {"package_pin", "files_from_count", "files_from_sha256"}
MEMBERS_NOW = 323
FILES_FROM = 49


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


def git_show(pin, path):
    r = subprocess.run(["git", "show", "%s:%s" % (pin, path)], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def policy_hashes(tar_path):
    """{revision: [state, policy_sha256]} computed by the tarball's own lib/opal_naming.py over its own registry."""
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(tar_path) as tf:
            tf.extractall(tmp)
        doc = json.load(open(tmp + "/" + REG, encoding="utf-8"))
        pol = doc["policies"]
        revs = sorted(x["policy_revision"] for x in pol) if isinstance(pol, list) else sorted(pol)
        code = ("import sys, json; sys.path[:0]=[%r, %r]\n"
                "import opal_naming as n\n"
                "out = {}\n"
                "for rev in %r:\n"
                "    x = n.reporting_policy(rev)\n"
                "    out[rev] = [x.get('state'), x.get('policy_sha256')]\n"
                "print(json.dumps(out))\n" % (tmp + "/lib", tmp, revs))
        r = subprocess.run([sys.executable, "-I", "-B", "-c", code], capture_output=True, text=True, cwd=tmp)
        if r.returncode != 0:
            return None, (r.stderr.strip().splitlines() or ["?"])[-1][:200]
        return json.loads(r.stdout.strip().splitlines()[-1]), ""


def arm_record(path):
    fails = []
    if not os.path.isfile(path):
        return ["record absent: %s" % path]
    rec = json.load(open(path, encoding="utf-8"))
    delta = rec.get("delta_vs_r34p") or {}
    if sorted(delta.get("changed") or []) != sorted(CHANGED):
        fails.append("changed is %s want %s" % (sorted(delta.get("changed") or []), CHANGED))
    if delta.get("added") or delta.get("removed"):
        fails.append("added %s removed %s want none" % (delta.get("added"), delta.get("removed")))
    if delta.get("r34p_tarball_sha256") != R34P_SHA:
        fails.append("the base tarball sha256 is %s" % delta.get("r34p_tarball_sha256"))
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
    if bd.get("keys_added") != ["tickets_table"] or bd.get("keys_changed") != ["provenance"] or set(bd.get("provenance_keys_changed") or []) != PROV_MOVES:
        fails.append("bindings_diff is %s want keys_added tickets_table, changed provenance %s" % (bd, sorted(PROV_MOVES)))
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
    if sha(open(R34P_TAR, "rb").read()) != R34P_SHA or sha(open(R34N_TAR, "rb").read()) != R34N_SHA:
        fails.append("a base tarball is not the one that ran")
    new, old = read_tar(tar_path), read_tar(R34P_TAR)
    if len(new) != MEMBERS_NOW:
        fails.append("%d members, want %d" % (len(new), MEMBERS_NOW))
    changed = sorted(n for n in new if n in old and new[n] != old[n])
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    if changed != sorted(CHANGED) or added or removed:
        fails.append("tree delta changed=%s added=%s removed=%s" % (changed, added, removed))
    for name in CHANGED:
        if name in ("SHA256SUMS", "reports/resident_bindings.json") or name not in new:
            continue
        src = git_show(pin, SOURCE.get(name) or LAM + name)
        if src is None or src.replace(b"\r\n", b"\n") != new[name].replace(b"\r\n", b"\n"):
            fails.append("%s is not the pinned source" % name)
    b_new = json.loads(new["reports/resident_bindings.json"])
    b_old = json.loads(old["reports/resident_bindings.json"])
    added_keys = sorted(set(b_new) - set(b_old))
    moved = sorted(k for k in b_new if k in b_old and b_new[k] != b_old[k])
    if (added_keys != ["tickets_table"] or moved != ["provenance"] or b_new.get("tickets_table") != "opal-tickets"
            or b_new["provenance"].get("package_pin") != pin or b_new["provenance"].get("files_from_count") != FILES_FROM):
        fails.append("bindings: added %s moved %s tickets_table %r (want tickets_table added, provenance moved, the pin, %d files-from)" % (
            added_keys, moved, b_new.get("tickets_table"), FILES_FROM))
    else:
        pm = {k for k in set(b_new["provenance"]) | set(b_old["provenance"]) if b_new["provenance"].get(k) != b_old["provenance"].get(k)}
        if pm != PROV_MOVES:
            fails.append("provenance moved %s want %s" % (sorted(pm), sorted(PROV_MOVES)))
    ph_new, err = policy_hashes(tar_path)
    ph_old, err2 = policy_hashes(R34N_TAR)
    if ph_new is None or ph_old is None:
        fails.append("policy hashes unreadable: %s %s" % (err, err2))
    else:
        moved_revs = sorted(k for k in ph_old if ph_new.get(k) != ph_old[k])
        added_revs = sorted(set(ph_new) - set(ph_old))
        # tolerated: the dashbd revision, PENDING_ENFORCEMENT in both trees (it can hold no retention rows); any ACTIVE revision that moved fails
        bad_moved = [k for k in moved_revs if k != "irpt-dashbd-x10-v1" or ph_old[k][0] != "PENDING_ENFORCEMENT" or ph_new[k][0] != "PENDING_ENFORCEMENT"]
        if bad_moved:
            fails.append("a revision r34n carried changed its policy hash and is not tolerated: %s" % bad_moved)
        if added_revs != [NEW_REVISION] or ph_new.get(NEW_REVISION, ["?"])[0] != "ACTIVE":
            fails.append("revisions added %s (want only %s, ACTIVE; state %s)" % (added_revs, NEW_REVISION, (ph_new.get(NEW_REVISION) or ["absent"])[0]))
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
    r = subprocess.run([sys.executable, os.path.join(HERE, "ar_admission_replay.py"), tar_path], capture_output=True, text=True)
    if "AR-ADMIT-OK" not in r.stdout:
        fails.append("the admission replay of the Multi-Comp composition: %s" % (r.stdout.strip() or r.stderr.strip()[-160:])[:200])
    return fails


def arm_scripts(stage):
    fails = []
    tar = stage + "/irpt-resident-0485393f3a-r34q.tar.gz"
    if not os.path.isfile(tar):
        return ["no r34q tarball in %s" % stage]
    want = sha(open(tar, "rb").read())
    for name in ("pre_read_r34.sh", "install_r34.sh", "rollback_r34.sh", "resident_host_install_0485393f3a-r34q.sh"):
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
        if name != "resident_host_install_0485393f3a-r34q.sh" and ("NEW=0485393f3a-r34q" not in text or "OLD=0485393f3a-r34p" not in text):
            fails.append("%s does not name NEW r34q and OLD r34p" % name)
        if name == "resident_host_install_0485393f3a-r34q.sh":
            if "WANT_TAR=" + want not in text:
                fails.append("the host script WANT_TAR is not the tarball sha256")
            n = len(re.findall(r'^check "', text, re.M))
            if n != len(CHANGED):
                fails.append("the host script carries %d member checks, want %d" % (n, len(CHANGED)))
        if name == "install_r34.sh":
            host_p = "%s/scripts/resident_host_install_0485393f3a-r34q.sh" % stage
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
        print("usage: ar_release_q_checks.py record <record> | tree <tar> <pin> | scripts <stage>")
        sys.exit(2)
    if fails:
        print("AR-RELQ-%s-FAIL %s" % (arm, "; ".join(fails)[:900]))
        sys.exit(1)
    print("AR-RELQ-%s-OK" % arm)


if __name__ == "__main__":
    main()
