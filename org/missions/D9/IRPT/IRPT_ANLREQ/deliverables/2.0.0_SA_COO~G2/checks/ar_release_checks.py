"""IRPT_ANLREQ round 60 (issuer 2.0.0_SA_COO~G2): the checks of the r34o resident release build (cell AR-g-176). READ ONLY: builds nothing,
uploads nothing, calls no AWS. Run from the repository root.

    python ar_release_checks.py record  <RESIDENT_R34O_BUILD.json>
    python ar_release_checks.py tree    <r34o tarball> <full 40-hex pin>
    python ar_release_checks.py scripts <stage folder>

record: the build record's delta against the running r34n tarball is exactly the measured set; the artifact on disk has the recorded sha256,
size and member count; the bindings moved only in opal_map (the Overview map's sha256) and provenance.package_pin / files_from_count / files_from_sha256; the two builds are identical;
the import smoke read fail=0; the gate dry runs read 0, 31, 0, 33.
tree: the tarball itself, read by this file with its own code: every member it shares with r34n equals r34n's bytes except the expected movers;
each mover and each added lambda-tree or contract member equals `git show <pin>:<source path>`; lib/trading_calendar.py and the Overview map
equal their pinned sources; the lazy imports the smoke cannot see (ticket_audit_source, analysis_audit with its schema, model_source, comparables)
import in a fresh -I interpreter over the extracted tree and model_code_map.json is the pinned file.
scripts: the four host scripts exist, are ASCII, pass bash -n, name r34o as NEW and r34n as OLD, bind the tarball (host script WANT_TAR), the host script (install WANT) and the package sums (install WANTSUM) by sha256, and carry
exactly one member check per mover or added member (17 with the sums and the bindings).
Prints one RESULT line: AR-REL-<arm>-OK or AR-REL-<arm>-FAIL <why>; rc 0 only on OK. ASCII only.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tarfile

LAM = "infra/aws/lambda/investor-reporting/"
R34N_TAR = "C:/dev/irpt-release-r35h/irpt-resident-0485393f3a-r34n.tar.gz"
R34N_SHA = "89cad47247e6785e6b61e60112b04dfaa3cd2d5de88aef6023959692da76d899"
MAP_SRC = "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps/overview_map.json"
CHANGED = ["SHA256SUMS", "lib/trading_calendar.py", "ops/owned_report.py", "reports/resident_bindings.json", "reports/resident_installed.py",
           "ycharts/generate/resident_worker.py", "ycharts/generate/ticket_confirmation.py", "ycharts/research/layout_overview.py",
           "ycharts/research/opal_packager.py", "ycharts/research/opal_producer.py", "ycharts/research/overview_map.json"]
ADDED = ["_contracts/AnalysisAudit.v1.schema.json", "reports/analysis_audit.py", "ycharts/generate/ticket_audit_source.py",
         "ycharts/research/comparables.py", "ycharts/research/model_code_map.json", "ycharts/research/model_source.py"]
SPECIAL = {"SHA256SUMS": None, "reports/resident_bindings.json": None, "lib/trading_calendar.py": "lib/trading_calendar.py",
           "ycharts/research/overview_map.json": MAP_SRC}
PROV_MOVES = {"package_pin", "files_from_count", "files_from_sha256", "members_added"}  # members_added: only the trading_calendar sha
MEMBERS_NOW = 323  # 317 of r34n + 6 added


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


def source_path(name):
    if name in SPECIAL:
        return SPECIAL[name]
    if name.startswith("docs/") or name.startswith("data/") or name.startswith("census/"):
        return name
    return LAM + name


def arm_record(path):
    fails = []
    if not os.path.isfile(path):
        return ["record absent: %s" % path]
    rec = json.load(open(path, encoding="utf-8"))
    delta = rec.get("delta_vs_r34n") or {}
    if sorted(delta.get("changed") or []) != sorted(CHANGED):
        fails.append("changed is %s want %s" % (sorted(delta.get("changed") or []), CHANGED))
    if sorted(delta.get("added") or []) != sorted(ADDED):
        fails.append("added is %s want %s" % (sorted(delta.get("added") or []), ADDED))
    if delta.get("removed"):
        fails.append("removed is %s want none" % (delta.get("removed"),))
    if delta.get("r34n_tarball_sha256") != R34N_SHA:
        fails.append("the base tarball sha256 is %s" % delta.get("r34n_tarball_sha256"))
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
    if bd.get("keys_added") or sorted(bd.get("keys_changed") or []) != ["opal_map", "provenance"] or set(bd.get("provenance_keys_changed") or []) != PROV_MOVES:
        fails.append("bindings_diff is %s want keys opal_map (the Overview map pin) and provenance %s" % (bd, sorted(PROV_MOVES)))
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
    new, old = read_tar(tar_path), read_tar(R34N_TAR)
    if sha(open(R34N_TAR, "rb").read()) != R34N_SHA:
        fails.append("the r34n base tarball is not the running one")
    if len(new) != MEMBERS_NOW:
        fails.append("%d members, want %d" % (len(new), MEMBERS_NOW))
    changed = sorted(n for n in new if n in old and new[n] != old[n])
    added = sorted(set(new) - set(old))
    if changed != sorted(CHANGED) or added != sorted(ADDED) or set(old) - set(new):
        fails.append("tree delta changed=%s added=%s removed=%s" % (changed, added, sorted(set(old) - set(new))))
    for name in sorted(set(CHANGED) | set(ADDED)):
        if name in ("SHA256SUMS", "reports/resident_bindings.json") or name not in new:
            continue
        src = git_show(pin, source_path(name))
        if src is None or src.replace(b"\r\n", b"\n") != new[name].replace(b"\r\n", b"\n"):
            fails.append("%s is not the pinned source %s" % (name, source_path(name)))
    b_new = json.loads(new["reports/resident_bindings.json"]) if "reports/resident_bindings.json" in new else {}
    b_old = json.loads(old["reports/resident_bindings.json"])
    moved = sorted(k for k in b_new if b_new.get(k) != b_old.get(k))
    if moved != ["opal_map", "provenance"] or b_new.get("provenance", {}).get("package_pin") != pin:
        fails.append("bindings moved %s (want opal_map and provenance) or package_pin is not the pin" % moved)
    else:
        if b_new["opal_map"].get("sha256") != sha(new["ycharts/research/overview_map.json"]) or b_new["opal_map"].get("path") != b_old["opal_map"].get("path"):
            fails.append("opal_map is not the packaged Overview map's sha256 under the same path")
        pm = {k for k in set(b_new["provenance"]) | set(b_old["provenance"]) if b_new["provenance"].get(k) != b_old["provenance"].get(k)}
        if pm != PROV_MOVES:
            fails.append("provenance moved %s want %s" % (sorted(pm), sorted(PROV_MOVES)))
        ma_new, ma_old = b_new["provenance"]["members_added"], b_old["provenance"]["members_added"]
        want_ma = [dict(e, sha256=sha(new["lib/trading_calendar.py"])) if e["packaged"] == "lib/trading_calendar.py" else e for e in ma_old]
        if ma_new != want_ma:
            fails.append("members_added moved in more than the lib/trading_calendar.py sha256")
    # the lazy imports the smoke cannot see, in a fresh interpreter over the extracted tree
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(tar_path) as tf:
            tf.extractall(tmp)
        dirs = [tmp + "/" + d for d in ("", "reports", "ycharts/generate", "ycharts/research", "ycharts/session", "intake", "ops", "lib",
                                        "_scope", "_ids", "_keys", "_authz", "_contracts")]
        code = ("import sys; sys.path[:0]=%r\n"
                "import ticket_audit_source, analysis_audit, model_source, comparables\n"
                "import os\n"
                "assert os.path.isfile(analysis_audit._schema_path()) if hasattr(analysis_audit, '_schema_path') else True\n"
                "print('LAZY-OK')\n" % (dirs,))
        r = subprocess.run([sys.executable, "-I", "-B", "-c", code], capture_output=True, text=True, cwd=tmp)
        if "LAZY-OK" not in r.stdout:
            fails.append("lazy imports failed: %s" % (r.stderr.strip().splitlines() or ["?"])[-1][:200])
    return fails


def arm_scripts(stage):
    fails = []
    tar = stage + "/irpt-resident-0485393f3a-r34o.tar.gz"
    if not os.path.isfile(tar):
        return ["no r34o tarball in %s" % stage]
    want = sha(open(tar, "rb").read())
    for name in ("pre_read_r34.sh", "install_r34.sh", "rollback_r34.sh", "resident_host_install_0485393f3a-r34o.sh"):
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
        if name != "resident_host_install_0485393f3a-r34o.sh" and ("NEW=0485393f3a-r34o" not in text or "OLD=0485393f3a-r34n" not in text):
            fails.append("%s does not name NEW r34o and OLD r34n" % name)
        if name == "resident_host_install_0485393f3a-r34o.sh":
            if "WANT_TAR=" + want not in text:
                fails.append("the host script WANT_TAR is not the tarball sha256")
            if len(re.findall(r'^check "', text, re.M)) != len(CHANGED) + len(ADDED):
                fails.append("the host script carries %d member checks, want %d" % (len(re.findall(r'^check "', text, re.M)), len(CHANGED) + len(ADDED)))
        if name == "install_r34.sh":
            host_p = "%s/scripts/resident_host_install_0485393f3a-r34o.sh" % stage
            if "WANT=" + sha(open(host_p, "rb").read()) not in text:
                fails.append("install_r34.sh WANT is not the host script sha256")
            sums = read_tar(tar).get("SHA256SUMS", b"")
            if "WANTSUM=" + sha(sums) not in text:
                fails.append("install_r34.sh WANTSUM is not the tarball's SHA256SUMS member sha256")
            if len(re.findall(r'^  "[^ "]+ [0-9a-f]{64}"', text, re.M)) != len(CHANGED) + len(ADDED) - 2:
                fails.append("install_r34.sh carries %d member entries, want %d" % (len(re.findall(r'^  "[^ "]+ [0-9a-f]{64}"', text, re.M)), len(CHANGED) + len(ADDED) - 2))
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
        print("usage: ar_release_checks.py record <record> | tree <tar> <pin> | scripts <stage>")
        sys.exit(2)
    if fails:
        print("AR-REL-%s-FAIL %s" % (arm, "; ".join(fails)[:900]))
        sys.exit(1)
    print("AR-REL-%s-OK" % arm)


if __name__ == "__main__":
    main()
