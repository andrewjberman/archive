"""IRPT_ANLREQ round 60 (issuer 2.0.0_SA_COO~G2): the checks of the r34u resident release build. READ ONLY: builds nothing, uploads nothing,
calls no AWS. Run from the repository root with a python that has jsonschema and referencing (not `-I`) for the tree arm.

    python ar_release_s_checks.py record  <RESIDENT_R34U_BUILD.json>
    python ar_release_s_checks.py tree    <r34u tarball> <full 40-hex pin>
    python ar_release_s_checks.py scripts <stage folder>

r34u = r34t plus: (1) the host capture library moves to the trunk file (W328-S1: WAF_CHALLENGE ends the run with no second sign-in): the package member
ycharts-host/ycharts_session.js (a1c28801 -> db43e9f9) and bindings capture.library_sha256; (2) the swap record carries the class pair and the model's number and a
low-confidence sentence (AR-y-497): ycharts/research/swap_pass.py; (3) the Overview names every replaced swap under the left-out line (AR-y-498) and the comparison
chart draws six distinct series colours (AR-g-195): ycharts/research/layout_overview.py. No member added, no registry move, no IAM change.
record / tree / scripts: as r34t's checker, over five movers; the scripts arm also requires the host script to want the NEW library and the rollback to restore the kept old one.
Prints one RESULT line: AR-RELS-<arm>-OK or AR-RELS-<arm>-FAIL <why>; rc 0 only on OK. ASCII only.
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
R34T_TAR = "C:/dev/irpt-release-r34t-g2/irpt-resident-0485393f3a-r34t.tar.gz"
R34T_SHA = "35a4f044c2bcae4d567c57132b833c101ab1872d9880bafd45cb0a4afe6af21d"
REG = "infra/logic/registry/reporting_policies.json"
NEW_REVISION = "irpt-anlreq-audit-x10-v1"
CHANGED = ["SHA256SUMS", "reports/resident_bindings.json", "ycharts-host/ycharts_session.js", "ycharts/research/layout_overview.py", "ycharts/research/swap_pass.py"]
ADDED = []
LIB_OLD = "a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841"
LIB_NEW = "db43e9f9744e697098120e11dd862a1348ffea05c6307f980dc24e7ea530a216"
SOURCE = {"SHA256SUMS": None, "reports/resident_bindings.json": None,
          "ycharts-host/ycharts_session.js": "infra/aws/ec2/investor-reporting-ycharts/ycharts_session.js"}
PROV_MOVES = {"package_pin"}
MEMBERS_NOW = 325
FILES_FROM = 51


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
    delta = rec.get("delta_vs_r34t") or {}
    if sorted(delta.get("changed") or []) != sorted(CHANGED):
        fails.append("changed is %s want %s" % (sorted(delta.get("changed") or []), CHANGED))
    if sorted(delta.get("added") or []) != sorted(ADDED) or delta.get("removed"):
        fails.append("added %s removed %s want added %s and none removed" % (delta.get("added"), delta.get("removed"), ADDED))
    if delta.get("r34t_tarball_sha256") != R34T_SHA:
        fails.append("the base tarball sha256 is %s" % delta.get("r34t_tarball_sha256"))
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
    if bd.get("keys_added") != [] or bd.get("keys_changed") != ["capture", "provenance"] or set(bd.get("provenance_keys_changed") or []) != PROV_MOVES:
        fails.append("bindings_diff is %s want no key added, changed capture and provenance %s" % (bd, sorted(PROV_MOVES)))
    tb = rec.get("two_builds") or {}
    if not tb.get("files_compared") or tb.get("files_compared") != tb.get("identical"):
        fails.append("two_builds not identical: %s" % tb)
    smoke = " ".join(rec.get("import_smoke") or [])
    if " fail=0 " not in smoke + " " or "live=87 imported=87" not in smoke:
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
    if sha(open(R34T_TAR, "rb").read()) != R34T_SHA or sha(open(R34N_TAR, "rb").read()) != R34N_SHA:
        fails.append("a base tarball is not the one that ran")
    new, old = read_tar(tar_path), read_tar(R34T_TAR)
    if len(new) != MEMBERS_NOW:
        fails.append("%d members, want %d" % (len(new), MEMBERS_NOW))
    changed = sorted(n for n in new if n in old and new[n] != old[n])
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    if changed != sorted(CHANGED) or added != sorted(ADDED) or removed:
        fails.append("tree delta changed=%s added=%s removed=%s" % (changed, added, removed))
    for name in CHANGED + ADDED:
        if name in ("SHA256SUMS", "reports/resident_bindings.json") or name not in new:
            continue
        src = git_show(pin, SOURCE.get(name) or LAM + name)
        if src is None or src.replace(b"\r\n", b"\n") != new[name].replace(b"\r\n", b"\n"):
            fails.append("%s is not the pinned source" % name)
    b_new = json.loads(new["reports/resident_bindings.json"])
    b_old = json.loads(old["reports/resident_bindings.json"])
    added_keys = sorted(set(b_new) - set(b_old))
    moved = sorted(k for k in b_new if k in b_old and b_new[k] != b_old[k])
    if (added_keys != [] or b_new.get("opal_swap_model") != {"enabled": True} or b_old.get("opal_swap_model") != {"enabled": True} or moved != ["capture", "provenance"] or b_new["capture"].get("library_sha256") != LIB_NEW or b_old["capture"].get("library_sha256") != LIB_OLD or b_new.get("tickets_table") != "opal-tickets" or b_old.get("tickets_table") != "opal-tickets"
            or b_new["provenance"].get("package_pin") != pin or b_new["provenance"].get("files_from_count") != FILES_FROM):
        fails.append("bindings: added %s moved %s tickets_table %r (want opal_swap_model {enabled: true} in both, capture.library_sha256 old -> new and provenance moved, tickets_table opal-tickets in both, the pin, %d files-from)" % (
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
        ph_q, err3 = policy_hashes(R34T_TAR)
        if ph_q is None or ph_new != ph_q:
            fails.append("the registry revisions and hashes are not r34t's (r34u moves no registry): %s" % err3)
        if added_revs != [NEW_REVISION] or ph_new.get(NEW_REVISION, ["?"])[0] != "ACTIVE":
            fails.append("revisions added %s (want only %s, ACTIVE; state %s)" % (added_revs, NEW_REVISION, (ph_new.get(NEW_REVISION) or ["absent"])[0]))
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(tar_path) as tf:
            tf.extractall(tmp)
        dirs = [tmp + "/" + d for d in ("", "reports", "ycharts/generate", "ycharts/research", "ycharts/session", "intake", "ops", "lib",
                                        "_scope", "_ids", "_keys", "_authz", "_contracts")]
        code = ("import sys; sys.path[:0]=%r\n"
                "import ticket_audit_source, analysis_audit, model_source, comparables, swap_model, etf_classification_model\n"
                "print('LAZY-OK')\n" % (dirs,))
        r = subprocess.run([sys.executable, "-I", "-B", "-c", code], capture_output=True, text=True, cwd=tmp)
        if "LAZY-OK" not in r.stdout:
            fails.append("lazy imports failed: %s" % (r.stderr.strip().splitlines() or ["?"])[-1][:200])
    r = subprocess.run([sys.executable, os.path.join(HERE, "ar_admission_replay.py"), tar_path], capture_output=True, text=True)
    if "AR-ADMIT-OK" not in r.stdout:
        fails.append("the admission replay of the Multi-Comp composition: %s" % (r.stdout.strip() or r.stderr.strip()[-160:])[:200])
    # the S249 replays: the tarball's OWN modules (extracted) must pass the frozen-read, comparables and retained-line checks
    with tempfile.TemporaryDirectory() as root:
        with tarfile.open(tar_path) as tf:
            tf.extractall(root)
        for script, arm, ok in (("ar_prepare_checks.py", "frozen", "AR-PREP-frozen-OK"), ("ar_prepare_checks.py", "worker", "AR-PREP-worker-OK"),
                                ("ar_reason_checks.py", "reason", "AR-REASON-reason-OK")):
            r = subprocess.run([sys.executable, os.path.join(HERE, script), arm, "--root", root], capture_output=True, text=True)
            if ok not in r.stdout:
                fails.append("%s %s on the tarball: %s" % (script, arm, (r.stdout.strip() or r.stderr.strip()[-160:])[:200]))
        shipped = {}
        for name in ("ycharts/generate/resident_worker.py", "ycharts/research/model_source.py", "ycharts/research/opal_producer.py",
                     "ycharts/research/layout_overview.py", "reports/resident_installed.py", "ycharts/research/swap_model.py", "ycharts/research/swap_pass.py",
                     "ycharts-host/ycharts_session.js"):
            shipped[name] = open(os.path.join(root, name), encoding="utf-8").read() if os.path.isfile(os.path.join(root, name)) else ""
        want = (("ycharts/generate/resident_worker.py", '"ticker": key if c.get("security_type") == "etf" else None', "the typed-ETF ticker is the catalogue key"),
                ("ycharts/research/model_source.py", "as_of_by_code", "the per-model positioning dates"),
                ("ycharts/research/opal_producer.py", 'alloc_doc["as_of_by_code"][code]', "the producer reads each model's own date"),
                ("ycharts/research/layout_overview.py", "def _excluded_line(", "the left-out line"),
                ("ycharts/research/layout_overview.py", "Left out of all figures:", "the left-out wording"),
                ("ycharts/research/layout_overview.py", 'acc.get("kind") == "table"', "the table elements take the column path"),
                ("reports/resident_installed.py", "SWAP_MODEL_BINDING_INVALID", "the swap-model binding rule"),
                ("ycharts/research/swap_model.py", "def make_swap_model(", "the swap model adapter"),
                ("ycharts/research/swap_pass.py", "model_confidence", "the model's number in the swap record (AR-y-497)"),
                ("ycharts/research/layout_overview.py", "Replaced in all figures:", "the replaced-swap line (AR-y-498)"),
                ("ycharts/research/layout_overview.py", '"#D95F02"', "the six chart series colours (AR-g-195)"),
                ("ycharts-host/ycharts_session.js", "WAF_CHALLENGE", "the WAF_CHALLENGE repair of the capture library (W328-S1)"))
        for name, needle, what in want:
            if needle not in shipped[name]:
                fails.append("the shipped %s lacks %s" % (name, what))
    return fails


def arm_scripts(stage):
    fails = []
    tar = stage + "/irpt-resident-0485393f3a-r34u.tar.gz"
    if not os.path.isfile(tar):
        return ["no r34u tarball in %s" % stage]
    want = sha(open(tar, "rb").read())
    for name in ("pre_read_r34.sh", "install_r34.sh", "rollback_r34.sh", "resident_host_install_0485393f3a-r34u.sh"):
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
        if name != "resident_host_install_0485393f3a-r34u.sh" and ("NEW=0485393f3a-r34u" not in text or "OLD=0485393f3a-r34t" not in text):
            fails.append("%s does not name NEW r34u and OLD r34t" % name)
        if name == "resident_host_install_0485393f3a-r34u.sh" and ("WANT_LIBRARY=" + LIB_NEW not in text or "WANT_LIBRARY=" + LIB_OLD in text):
            fails.append("the host script does not want the NEW capture library alone")
        if name == "install_r34.sh" and ("| want " + LIB_NEW not in text or "(want " + LIB_OLD + ")" not in text):
            fails.append("install_r34.sh V1 does not want the NEW library on the host and the OLD one in the kept copy")
        if name == "pre_read_r34.sh" and (LIB_OLD not in text or LIB_NEW in text):
            fails.append("pre_read_r34.sh must read the OLD library only")
        if name == "rollback_r34.sh" and not all(s in text for s in (LIB_OLD, LIB_NEW, "ycharts_session.js.before-$NEW", "exit 13", "exit 14")):
            fails.append("rollback_r34.sh does not restore the kept old library before the old root's installer")
        if name == "rollback_r34.sh" and text.find("ycharts_session.js.before-$NEW $H/ycharts_session.js") > text.find("install-resident.sh"):
            fails.append("rollback_r34.sh restores the library AFTER the old root's installer")
        if name == "resident_host_install_0485393f3a-r34u.sh":
            if "WANT_TAR=" + want not in text:
                fails.append("the host script WANT_TAR is not the tarball sha256")
            n = len(re.findall(r'^check "', text, re.M))
            if n != len(CHANGED) + len(ADDED):
                fails.append("the host script carries %d member checks, want %d" % (n, len(CHANGED) + len(ADDED)))
        if name == "install_r34.sh":
            host_p = "%s/scripts/resident_host_install_0485393f3a-r34u.sh" % stage
            if "WANT=" + sha(open(host_p, "rb").read()) not in text:
                fails.append("install_r34.sh WANT is not the host script sha256")
            sums = read_tar(tar).get("SHA256SUMS", b"")
            if "WANTSUM=" + sha(sums) not in text:
                fails.append("install_r34.sh WANTSUM is not the tarball's SHA256SUMS member sha256")
            n = len(re.findall(r'^  "[^ "]+ [0-9a-f]{64}"', text, re.M))
            if n != len(CHANGED) - 2 + len(ADDED):
                fails.append("install_r34.sh carries %d member entries, want %d" % (n, len(CHANGED) - 2 + len(ADDED)))
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
        print("usage: ar_release_s_checks.py record <record> | tree <tar> <pin> | scripts <stage>")
        sys.exit(2)
    if fails:
        print("AR-RELS-%s-FAIL %s" % (arm, "; ".join(fails)[:900]))
        sys.exit(1)
    print("AR-RELS-%s-OK" % arm)


if __name__ == "__main__":
    main()
