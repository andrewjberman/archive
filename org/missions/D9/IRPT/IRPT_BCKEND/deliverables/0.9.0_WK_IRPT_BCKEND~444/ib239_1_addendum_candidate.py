#!/usr/bin/env python3
# IB-pr-608 (IB239-1) 49 Financial ADDENDUM 1 release CANDIDATE harness -- 0.9.0_WK_IRPT_BCKEND~444. BUILD ONLY; READ ONLY on AWS.
#
# Phases, run in this order from the worktree root (see the record's method field):
#   candidate   49financial only. The committed IB-pr-595 transplant files are the base. The change from e2700915d2 to
#               53c238604b in holdings_snapshot.py (the ABSENT-AT-SOURCE-D spans, nothing else) is applied as a three-way
#               merge (ours = the transplanted file, base = e2700915d2 blob, theirs = 53c238604b blob); publication.py is the
#               transplanted file UNCHANGED. Writes addendum/49financial/<name> under this folder and verifies: the D spans
#               strip back to the transplanted file byte for byte; the D spans equal HEAD's; no one-date bypass; cusip_key.
#   firm        in its own process: the committed addendum files are copied into the minting-pin worktree (outside the
#               repository), the bundle is built twice (BUILD ONLY, minting pin's safe_deploy_core build_bundle_payload),
#               the live bundle is read (read only: s3api head-object and get-object) and compared member by member, six
#               offline test files are copied from HEAD and run with pytest on the candidate tree (the one-date bypass
#               test is NOT run).
#   assemble    writes the record from the candidate and firm fragments.
#
# Prints counts only. Client data rule: no account, holding, value, object key or object version id is printed or written;
# member names are repository code paths. Scratch files live outside the repository.
import argparse
import difflib
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import re
import subprocess
import sys
import tarfile
import tempfile

FIRM = "49financial"
MINTING = "b1d354cfc9341168a3b4c316a344876ce0049b97"
BUNDLE = "irpt_holdings_49f"
HS = "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py"
PU = "infra/aws/lambda/investor-reporting/holdings/publication.py"
OVERLAY_FILES = [HS, PU]
D_FROM = "e2700915d2"
D_TO = "53c238604b"
TX_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~434/transplant/49financial"
IB595_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~434/IB228-1_holdings_transplant_candidate.json"
DELIV_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~444"
ADD_REL = DELIV_REL + "/addendum/49financial"
RECORD_NAME = "IB239-1_addendum_candidate.json"
SUMS = "SHA256SUMS"
BASE_COMMIT = "68dd5cdcc909e5eaf84167f69233fe7fcba371d7"
READ_DATE = "2026-10-15"
SPAN = re.compile(r"^[ \t]*# BEGIN ABSENT-AT-SOURCE-D\b.*?^[ \t]*# END ABSENT-AT-SOURCE-D\b[^\n]*\n", re.S | re.M)
TEST_FILES = [
    "data/assets/scripts/gold/investor_reporting/tests/test_absent_at_source_wiring.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_absent_at_source_exemption.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_absent_at_source_receipts.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_absent_at_source_smartx_evidence.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_holdings_publish_gate.py",
    "infra/aws/lambda/investor-reporting/holdings/tests/test_publication.py",
]
METHOD = (
    "Run from the worktree root in this order. First, candidate: the committed IB-pr-595 49financial transplant files were "
    "read (their sha256 checked against IB-pr-595's record); the change from e2700915d2 to 53c238604b in holdings_snapshot.py "
    "was taken as a three-way merge onto the transplanted file (ours transplant, base e2700915d2, theirs 53c238604b) with the "
    "conflicts counted; publication.py was kept unchanged; the candidate was written to the addendum folder and checked (the "
    "D spans stripped equal the transplant byte for byte, the D spans equal HEAD's, no one-date bypass, cusip_key present). "
    "Second, firm: the committed addendum files were copied into the minting-pin worktree, the bundle was built twice by the "
    "minting pin safe_deploy_core build_bundle_payload (BUILD ONLY, arm A and arm B), the live bundle was read with s3api "
    "head-object and get-object (read only) and compared member by member with the candidate, and six offline test files "
    "copied from HEAD were run with pytest on the candidate tree (the one-date bypass test was not run). Third, assemble "
    "wrote the record. Nothing was uploaded, minted, deployed, signed or written to AWS."
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git_bytes(repo, args):
    env = dict(os.environ, MSYS_NO_PATHCONV="1")
    r = subprocess.run(["git", "-C", str(repo)] + args, capture_output=True, timeout=600, env=env)
    if r.returncode != 0:
        raise SystemExit("git rc=%d %s" % (r.returncode, r.stderr.decode("utf-8", "replace").strip()[:200]))
    return r.stdout


def git_text(repo, args):
    return git_bytes(repo, args).decode("utf-8", "replace").strip()


def merge3(ours, base, theirs, tmp):
    """git merge-file -p: returns (merged bytes, conflict count)."""
    paths = []
    for name, data in (("ours", ours), ("base", base), ("theirs", theirs)):
        p = os.path.join(tmp, name)
        with open(p, "wb") as fh:
            fh.write(data)
        paths.append(p)
    r = subprocess.run(["git", "merge-file", "-p", "-L", "ours", "-L", "base", "-L", "theirs"] + paths,
                       capture_output=True, timeout=120)
    if r.returncode < 0 or r.returncode >= 128:
        raise SystemExit("git merge-file failed rc=%d" % r.returncode)
    return r.stdout, r.returncode


def strip_d(text):
    """The text with every ABSENT-AT-SOURCE-D span removed (BEGIN line to END line, both included)."""
    return SPAN.sub("", text)


def changed_lines(a_lines, b_lines):
    diff = list(difflib.unified_diff(a_lines, b_lines, n=0))
    return [ln for ln in diff if (ln.startswith("+") or ln.startswith("-")) and not ln.startswith(("+++", "---"))]


def load_core(pin_root):
    path = pathlib.Path(pin_root) / ".tools" / "safe_deploy_core.py"
    spec = importlib.util.spec_from_file_location("safe_deploy_core_at_pin", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if pathlib.Path(mod.WORKSPACE).resolve() != pathlib.Path(pin_root).resolve():
        raise SystemExit("WORKSPACE is not the pin root")
    return mod


def aws_json(core, args):
    aws = core._find_aws()
    if not aws:
        raise SystemExit("aws CLI not found")
    r = subprocess.run([aws] + args, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=600, env=core._aws_env())
    if r.returncode != 0:
        raise SystemExit("aws rc=%d %s" % (r.returncode, r.stderr.strip()[:200]))
    return json.loads(r.stdout) if r.stdout.strip() else {}


def tar_map(data):
    out = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        for m in tf.getmembers():
            if m.isfile():
                out[m.name] = tf.extractfile(m).read()
    return out


def parse_sums(body):
    lines = {}
    for line in body.decode("utf-8").splitlines():
        digest, name = line.split("  ", 1)
        lines[name] = digest
    return lines


def cmd_candidate(a):
    repo, scratch = pathlib.Path(a.repo), pathlib.Path(a.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    tmp = tempfile.mkdtemp(dir=str(scratch))
    if git_text(repo, ["rev-parse", "HEAD"]) != BASE_COMMIT:
        raise SystemExit("worktree HEAD is not the base commit")

    # the signed transplant (IB-pr-595, 49financial): its committed files must still carry the recorded digests
    rec595 = json.loads((repo / IB595_REL).read_text(encoding="utf-8"))["firms"][FIRM]
    signed = {}
    for m in rec595["changed_members"]:
        data = (repo / m["artifact"]).read_bytes()
        if sha(data) != m["sha256_transplanted"]:
            raise SystemExit("IB-pr-595's committed transplant file differs from its record")
        signed[m["repo_path"]] = data
    tx_hs, tx_pu = signed[HS], signed[PU]

    # the D change: HEAD's file is the 53c238604b blob, and HEAD's file with the D spans stripped is the e2700915d2 blob
    head_hs = (repo / HS).read_bytes()
    base_hs = git_bytes(repo, ["show", D_FROM + ":" + HS])
    theirs_hs = git_bytes(repo, ["show", D_TO + ":" + HS])
    if head_hs != theirs_hs:
        raise SystemExit("HEAD's holdings_snapshot.py is not the 53c238604b blob; STOP")
    if strip_d(head_hs.decode("utf-8")).encode("utf-8") != base_hs:
        raise SystemExit("HEAD's file with the D spans stripped is not the e2700915d2 blob; STOP")
    print("premise: HEAD equals 53c238604b; HEAD with D spans stripped equals e2700915d2")

    merged, conflicts = merge3(tx_hs, base_hs, theirs_hs, tmp)
    if conflicts:
        raise SystemExit("the three-way merge has %d conflict(s); STOP (not resolved by this harness)" % conflicts)
    cand = merged
    text = cand.decode("utf-8")
    spans = SPAN.findall(text)
    head_spans = SPAN.findall(head_hs.decode("utf-8"))
    d_equal = bool(spans) and spans == head_spans
    stripped = strip_d(text)
    diff_out = changed_lines(tx_hs.decode("utf-8").splitlines(keepends=True), stripped.splitlines(keepends=True))
    checks = {
        "strip_equals_transplant_bytes": stripped.encode("utf-8") == tx_hs,
        "d_spans_equal_head": d_equal,
        "diff_lines_outside_spans": len(diff_out),
        "one_date_absent": ("allow_older_date" not in text) and ("ONE-DATE-ASSERT" not in text),
        "cusip_port_present": "cusip_key" in text,
    }
    print("candidate: D spans=%d; conflicts=%d; strip equals transplant=%s; spans equal HEAD=%s; diff lines outside spans=%d; "
          "one-date absent=%s; cusip port present=%s" % (
              len(spans), conflicts, checks["strip_equals_transplant_bytes"], checks["d_spans_equal_head"],
              checks["diff_lines_outside_spans"], checks["one_date_absent"], checks["cusip_port_present"]))
    if not (checks["strip_equals_transplant_bytes"] and checks["d_spans_equal_head"] and checks["diff_lines_outside_spans"] == 0
            and checks["one_date_absent"] and checks["cusip_port_present"]):
        raise SystemExit("a candidate check failed; STOP")

    out = repo / ADD_REL
    out.mkdir(parents=True, exist_ok=True)
    (out / "holdings_snapshot.py").write_bytes(cand)
    (out / "publication.py").write_bytes(tx_pu)
    frag = {
        "firm": FIRM,
        "minting_pin": MINTING,
        "transplant_candidate_bundle_sha256": rec595["candidate_bundle_sha256"],
        "transplant_live_bundle_sha256": rec595["live_bundle_sha256"],
        "conflicts": conflicts,
        "d_spans": {"count": len(spans), "equal_to_head": d_equal, "diff_lines_outside_spans": len(diff_out)},
        "cusip_port_present": checks["cusip_port_present"],
        "sha256": {HS: sha(cand), PU: sha(tx_pu)},
    }
    (scratch / ("cand_" + FIRM + ".json")).write_text(json.dumps(frag, indent=1) + "\n", encoding="utf-8")
    return 0


def cmd_firm(a):
    root, repo, scratch = pathlib.Path(a.pin_root), pathlib.Path(a.repo), pathlib.Path(a.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    os.chdir(str(root))
    sys.path.insert(0, str(root))
    cand_frag = json.loads((scratch / ("cand_" + FIRM + ".json")).read_text(encoding="utf-8"))
    if git_text(root, ["rev-parse", "HEAD"]) != MINTING:
        raise SystemExit("pin worktree HEAD is not the minting pin")
    if git_text(root, ["config", "--worktree", "--get", "core.sparseCheckout"]) != "false":
        raise SystemExit("sparse checkout is not disabled in the pin worktree")
    if git_text(root, ["status", "--porcelain"]):
        raise SystemExit("pin worktree is not clean before the candidate is placed")
    frag = {"firm": FIRM, "minting_pin": MINTING}

    # 1. the COMMITTED addendum files into the pin tree
    placed = {}
    for p in OVERLAY_FILES:
        data = (repo / ADD_REL / os.path.basename(p)).read_bytes()
        (root / p).write_bytes(data)
        placed[p] = sha(data)
        if placed[p] != cand_frag["sha256"][p]:
            raise SystemExit("a committed addendum file differs from the candidate phase bytes")
    status = git_bytes(root, ["status", "--porcelain"]).decode("utf-8", "replace").splitlines()
    frag["overlay_status_entries"] = len(status)
    if sorted(s[3:] for s in status) != sorted(OVERLAY_FILES):
        raise SystemExit("after placement the pin tree differs from the two addendum files")
    print("placed: modified entries in the pin worktree=%d" % len(status))

    # 2. build twice, BUILD ONLY
    core = load_core(root)
    if BUNDLE not in core.STANDALONE_BUNDLES:
        raise SystemExit("bundle %s is not declared at the candidate tree" % BUNDLE)
    b = core.STANDALONE_BUNDLES[BUNDLE]
    pa, _, erra = core.build_bundle_payload(b)
    pb, _, errb = core.build_bundle_payload(b)
    if pa is None or pb is None:
        raise SystemExit("build failed (%s | %s)" % (erra, errb))
    ma, mb = tar_map(pa), tar_map(pb)
    closure = set(b["members"])
    cand_map = {k: sha(v) for k, v in ma.items() if k != SUMS}
    if set(cand_map) != closure:
        raise SystemExit("candidate closure differs from the declared members")
    frag["build_arms_identical_members"] = {k: sha(v) for k, v in ma.items()} == {k: sha(v) for k, v in mb.items()}
    frag["build_arms_identical_tar_bytes"] = sha(pa) == sha(pb)
    frag["members_total"] = len(closure)
    frag["candidate_bundle_sha256"] = sha(pa)
    print("candidate built twice; identical members=%s; identical tar bytes=%s; closure members=%d" % (
        frag["build_arms_identical_members"], frag["build_arms_identical_tar_bytes"], len(closure)))
    (scratch / (FIRM + ".candidate.tar.gz")).write_bytes(pa)

    # 3. live bundle, read only (head-object and get-object)
    aws_json(core, ["s3api", "head-object", "--bucket", b["bucket"], "--key", b["s3_key"], "--output", "json"])
    live_path = scratch / (FIRM + ".live.tar.gz")
    aws_json(core, ["s3api", "get-object", "--bucket", b["bucket"], "--key", b["s3_key"], str(live_path),
                    "--output", "json"])
    live = live_path.read_bytes()
    frag["live_bundle_sha256"] = sha(live)
    ml = tar_map(live)
    live_map = {k: sha(v) for k, v in ml.items() if k != SUMS}
    changed = sorted(n for n in closure if cand_map.get(n) != live_map.get(n))
    frag["members_equal_to_live"] = len(closure) - len(changed)
    frag["changed_members"] = changed
    frag["unexpected_changed_members"] = [n for n in changed if n not in OVERLAY_FILES]
    frag["live_only_members"] = len(set(live_map) - closure)
    sums_c = parse_sums(ma[SUMS]) if SUMS in ma else {}
    sums_l = parse_sums(ml[SUMS]) if SUMS in ml else {}
    frag["sums_line_diff_equals_addendum"] = sorted(k for k in set(sums_c) | set(sums_l) if sums_c.get(k) != sums_l.get(k)) \
        == sorted(OVERLAY_FILES)
    print("live read; changed closure members=%d; unexpected=%d; equal=%d of %d" % (
        len(changed), len(frag["unexpected_changed_members"]), frag["members_equal_to_live"], len(closure)))

    # 4. offline tests on the candidate tree (copied from HEAD; not bundle members; the one-date bypass test is not run)
    for p in TEST_FILES:
        data = git_bytes(repo, ["show", "HEAD:" + p])
        dst = root / p
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + TEST_FILES, cwd=str(root),
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1200)
    (scratch / (FIRM + ".pytest.log")).write_text(r.stdout + r.stderr, encoding="utf-8")
    lines = [ln for ln in (r.stdout + r.stderr).splitlines() if ln.strip()]
    last = lines[-1] if lines else ""
    passed = re.search(r"(\d+) passed", last)
    failed = re.search(r"(\d+) failed", last)
    errors = re.search(r"(\d+) error", last)
    frag["tests"] = {"passed": int(passed.group(1)) if passed else 0,
                     "failed": (int(failed.group(1)) if failed else 0) + (int(errors.group(1)) if errors else 0)}
    frag["tests_rc"] = r.returncode
    frag["failing_test_names"] = [ln.split(" ", 1)[1].split(" - ")[0] for ln in lines if ln.startswith("FAILED ")]
    frag["last_line"] = last
    print("offline tests on the candidate tree: passed=%d failed=%d rc=%d; last line: %s" % (
        frag["tests"]["passed"], frag["tests"]["failed"], r.returncode, last))
    (scratch / ("firm_" + FIRM + ".json")).write_text(json.dumps(frag, indent=1) + "\n", encoding="utf-8")
    return 0


def cmd_assemble(a):
    repo, scratch = pathlib.Path(a.repo), pathlib.Path(a.scratch)
    cand = json.loads((scratch / ("cand_" + FIRM + ".json")).read_text(encoding="utf-8"))
    f = json.loads((scratch / ("firm_" + FIRM + ".json")).read_text(encoding="utf-8"))
    if sorted(f["changed_members"]) != sorted(OVERLAY_FILES) or f["unexpected_changed_members"]:
        raise SystemExit("the changed members are not EXACTLY the two addendum files; STOP")
    changed = []
    for p in sorted(OVERLAY_FILES):
        art = ADD_REL + "/" + os.path.basename(p)
        data = (repo / art).read_bytes()
        if sha(data) != cand["sha256"][p]:
            raise SystemExit("committed addendum file differs from the candidate phase bytes")
        changed.append({"repo_path": p, "artifact": DELIV_REL + "/addendum/" + FIRM + "/" + os.path.basename(p),
                        "sha256_candidate": sha(data)})
    notes = [
        "Facts and their basis: the base is IB-pr-595's committed 49financial transplant, checked against its record; the D change is "
        "git diff e2700915d2 53c238604b of holdings_snapshot.py (56 inserted lines, no deleted line), applied as a three-way merge with "
        "%d conflicts; HEAD equals the 53c238604b blob and HEAD with the D spans stripped equals the e2700915d2 blob." % cand["conflicts"],
        "Not read and not run: no Lambda was invoked and no publish, mint, land, refusal-record or upload function was called; "
        "build_bundle_payload was called twice in BUILD ONLY mode and its output stayed in scratch; no sign-in and no vendor contact; "
        "the live object version identifier is not written; test_holdings_bypass_one_date.py was not run because it tests the one-date "
        "bypass that is not shipped.",
        "Sparse directories: the base worktree's sparse set gained data/assets/scripts/gold/investor_reporting/ only (local, never "
        "committed); the minting pin is a full detached worktree outside the repository, with sparse checkout disabled there alone; "
        "the candidate tree's tests were copied in from HEAD and are not bundle members.",
        "Tests: six offline files from HEAD run on the candidate tree: %d passed, %d failed, pytest rc %d; the failing test names, if any, "
        "are recorded in the criteria output and the channel rows." % (f["tests"]["passed"], f["tests"]["failed"], f["tests_rc"]),
        "The counters functions_invoked, sign_ins_made, aws_writes_made, rows_written, figures_written and vendor_requests_sent are zero: "
        "they count publish, mint, sign-in, write and vendor calls, and none was made.",
        "Client data gate: the commit gate of the candidate files printed a WARN that the hashed account-id list is absent on this box, "
        "so those files and this record were NOT checked against it (absent is not empty); this record carries counts, hashes and "
        "repository paths only, and the harness prints no account, holding, value or object key.",
    ]
    record = {
        "base_commit": a.base_commit,
        "read_date": a.read_date,
        "claim": "measured",
        "method": METHOD,
        "firm": FIRM,
        "minting_pin": MINTING,
        "transplant_ref": {"candidate_bundle_sha256": cand["transplant_candidate_bundle_sha256"]},
        "live_bundle_sha256": f["live_bundle_sha256"],
        "candidate_bundle_sha256": f["candidate_bundle_sha256"],
        "members_total": f["members_total"],
        "members_equal_to_live": f["members_equal_to_live"],
        "cusip_port_present": cand["cusip_port_present"],
        "changed_members": changed,
        "d_spans": {"count": cand["d_spans"]["count"], "equal_to_head": cand["d_spans"]["equal_to_head"],
                    "diff_lines_outside_spans": cand["d_spans"]["diff_lines_outside_spans"]},
        "tests": {"passed": f["tests"]["passed"], "failed": f["tests"]["failed"]},
        "notes": notes,
        "functions_invoked": 0,
        "sign_ins_made": 0,
        "aws_writes_made": 0,
        "rows_written": 0,
        "figures_written": 0,
        "vendor_requests_sent": 0,
    }
    out = repo / DELIV_REL / RECORD_NAME
    out.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    print("record written: members_total=%d; equal_to_live=%d; changed=%d; d_spans=%d; tests passed=%d failed=%d" % (
        f["members_total"], f["members_equal_to_live"], len(changed), cand["d_spans"]["count"],
        f["tests"]["passed"], f["tests"]["failed"]))
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_c = sub.add_parser("candidate")
    p_c.add_argument("--repo", required=True)
    p_c.add_argument("--scratch", required=True)
    p_f = sub.add_parser("firm")
    p_f.add_argument("--pin-root", required=True)
    p_f.add_argument("--repo", required=True)
    p_f.add_argument("--scratch", required=True)
    p_a = sub.add_parser("assemble")
    p_a.add_argument("--repo", required=True)
    p_a.add_argument("--scratch", required=True)
    p_a.add_argument("--base-commit", default=BASE_COMMIT)
    p_a.add_argument("--read-date", default=READ_DATE)
    a = ap.parse_args()
    if a.cmd == "candidate":
        return cmd_candidate(a)
    if a.cmd == "firm":
        return cmd_firm(a)
    return cmd_assemble(a)


if __name__ == "__main__":
    sys.exit(main())
