#!/usr/bin/env python3
# IB-pr-610 (IB241-1) ADDENDUM candidate harness -- 0.9.0_WK_IRPT_BCKEND~446. 49financial ONLY. BUILD ONLY; READ ONLY on AWS.
#
# A copy of the IB-pr-595 transplant harness (deliverables 0.9.0_WK_IRPT_BCKEND~434/ib228_1_transplant_candidate.py), reduced
# to one firm and to the addendum: the SIGNED transplant files of IB-pr-595 plus ONLY the ABSENT-AT-SOURCE-D spans of HEAD.
#
# Phases, run in this order from the worktree root (see the record's method field):
#   addendum  holdings_snapshot.py: git merge-file of ours = IB-pr-595's committed transplant, base = the blob of commit
#             e2700915d2, theirs = the blob of commit 1ff5e87e40 (HEAD's file); the merge is the D spans and nothing else.
#             publication.py: the signed transplant, copied byte for byte. Both written under addendum/49financial/.
#   firm      per firm (one firm here): copy the COMMITTED candidate files into the minting-pin worktree (outside the
#             repository), build the bundle twice (BUILD ONLY, minting pin's safe_deploy_core), read the live bundle
#             (read only) and compare member by member, copy six offline test files from HEAD, run pytest.
#   assemble  write IB241-1_addendum_candidate.json from the addendum and firm fragments.
#
# Prints counts only. Client data rule: no account, holding, value, object key or object version id is printed or written;
# member names are repository code paths.
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
BASE_HS = "e2700915d2"  # the commit before the D spans
D_HEAD = "1ff5e87e40"  # the commit that adds the D spans; HEAD's file has the same blob
TEST_FILES = [
    "data/assets/scripts/gold/investor_reporting/tests/test_absent_at_source_wiring.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_absent_at_source_exemption.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_absent_at_source_receipts.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_absent_at_source_smartx_evidence.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_holdings_publish_gate.py",
    "infra/aws/lambda/investor-reporting/holdings/tests/test_publication.py",
]
IB595_DIR = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~434"
IB595 = IB595_DIR + "/IB228-1_holdings_transplant_candidate.json"
DELIV_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~446"
ADDENDUM_REL = DELIV_REL + "/addendum/49financial"
RECORD_NAME = "IB241-1_addendum_candidate.json"
MINT_RECORD = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~IB2/IB199-2_mints_and_business_date_statement.json"
SUMS = "SHA256SUMS"
SPAN = re.compile(r"^[ \t]*# BEGIN ABSENT-AT-SOURCE-D\b.*?^[ \t]*# END ABSENT-AT-SOURCE-D\b[^\n]*\n", re.S | re.M)
BYPASS_MARKERS = ("allow_older_date", "ONE-DATE-ASSERT")
METHOD = (
    "Run from the worktree root in this order. First, addendum: the signed IB-pr-595 transplant files for 49financial "
    "(committed under its deliverables folder) were read and their sha256 checked against its record; holdings_snapshot.py "
    "was three-way merged with git merge-file (ours the signed transplant, base the blob of commit e2700915d2, theirs the blob "
    "of commit 1ff5e87e40, which is HEAD's file) and the merge was checked: every ABSENT-AT-SOURCE-D span stripped equals the "
    "signed transplant byte for byte, the spans equal HEAD's spans, the one-date bypass is absent; publication.py was copied "
    "unchanged from the signed transplant; both candidate files were committed in the addendum folder. Second, the firm phase: "
    "in the minting pin worktree (outside the repository, sparse checkout disabled there alone) the two candidate files were "
    "copied in, the bundle was built twice by the minting pin's safe_deploy_core build_bundle_payload (BUILD ONLY, no upload "
    "function called), the live bundle was read with s3api head-object and get-object (read only) and compared member by "
    "member, and six offline test files were copied from HEAD and run with pytest (the one-date bypass test was not run). "
    "Third, the assemble phase wrote the record. Nothing was uploaded, minted, deployed, signed or written to AWS."
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


def changed_lines(a_bytes, b_bytes):
    """Changed (+/-) lines between two texts; returns (added, removed)."""
    a_lines = a_bytes.decode("utf-8").splitlines(keepends=True)
    b_lines = b_bytes.decode("utf-8").splitlines(keepends=True)
    added = removed = 0
    for ln in difflib.unified_diff(a_lines, b_lines, n=0):
        if ln.startswith("+") and not ln.startswith("+++"):
            added += 1
        elif ln.startswith("-") and not ln.startswith("---"):
            removed += 1
    return added, removed


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


def cmd_addendum(a):
    repo, scratch = pathlib.Path(a.repo), pathlib.Path(a.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    sig = json.loads((repo / IB595).read_text(encoding="utf-8"))["firms"][FIRM]
    signed = {}
    for m in sig["changed_members"]:
        data = (repo / m["artifact"]).read_bytes()
        if sha(data) != m["sha256_transplanted"]:
            raise SystemExit("the signed transplant file %s differs from its IB-pr-595 record; STOP" % m["repo_path"])
        signed[m["repo_path"]] = data
    ours, pub = signed[HS], signed[PU]
    if sorted(signed) != sorted(OVERLAY_FILES):
        raise SystemExit("the signed packet does not name exactly the two overlay members; STOP")

    base = git_bytes(repo, ["show", BASE_HS + ":" + HS])
    theirs = git_bytes(repo, ["show", D_HEAD + ":" + HS])
    head = git_bytes(repo, ["show", "HEAD:" + HS])
    tmp = tempfile.mkdtemp(dir=str(scratch))
    merged, conflicts = merge3(ours, base, theirs, tmp)
    if conflicts:
        raise SystemExit("the D spans do not apply cleanly: %d conflicts; STOP" % conflicts)

    text = merged.decode("utf-8")
    stripped = SPAN.sub("", text).encode("utf-8")
    cand_spans = SPAN.findall(text)
    head_spans = SPAN.findall(head.decode("utf-8"))
    added, removed = changed_lines(ours, merged)
    out = repo / ADDENDUM_REL
    out.mkdir(parents=True, exist_ok=True)
    (out / "holdings_snapshot.py").write_bytes(merged)
    (out / "publication.py").write_bytes(pub)

    frag = {
        "head_blob_equals_1ff5e87e40": sha(head) == sha(theirs),
        "merge_conflicts": conflicts,
        "merge_lines_added": added,
        "merge_lines_removed": removed,
        "d_count": len(cand_spans),
        "d_equal_head": bool(cand_spans) and cand_spans == head_spans,
        "d_head_count": len(head_spans),
        "stripped_equals_signed": stripped == ours,
        "diff_outside": changed_lines(ours, stripped)[0] + changed_lines(ours, stripped)[1],
        "bypass_absent": not any(mk.encode("utf-8") in merged for mk in BYPASS_MARKERS),
        "cusip_port_present": b"cusip_key" in merged,
        "sha": {HS: sha(merged), PU: sha(pub)},
        "signed_candidate_bundle_sha256": sig["candidate_bundle_sha256"],
        "signed_live_bundle_sha256": sig["live_bundle_sha256"],
        "signed_members_total": sig["members_total"],
        "signed_pub_sha": sha(pub),
    }
    if not frag["stripped_equals_signed"] or not frag["d_equal_head"] or frag["diff_outside"] != 0:
        raise SystemExit("the candidate fails its own D-span checks; STOP")
    if not frag["bypass_absent"] or not frag["cusip_port_present"]:
        raise SystemExit("the candidate carries the bypass or lacks the CUSIP port; STOP")
    (scratch / "addendum.json").write_text(json.dumps(frag, indent=1) + "\n", encoding="utf-8")
    print("addendum: merge conflicts=%d; lines added=%d removed=%d; D spans=%d (HEAD %d); equal to HEAD=%s" % (
        conflicts, added, removed, frag["d_count"], frag["d_head_count"], frag["d_equal_head"]))
    print("addendum: stripped candidate equals the signed transplant=%s; diff lines outside spans=%d; bypass absent=%s; "
          "cusip port present=%s" % (frag["stripped_equals_signed"], frag["diff_outside"], frag["bypass_absent"],
                                     frag["cusip_port_present"]))
    return 0


def cmd_firm(a):
    root, repo, scratch = pathlib.Path(a.pin_root), pathlib.Path(a.repo), pathlib.Path(a.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    os.chdir(str(root))
    sys.path.insert(0, str(root))
    if git_text(root, ["rev-parse", "HEAD"]) != MINTING:
        raise SystemExit("pin worktree HEAD is not the minting pin; STOP")
    if git_text(root, ["config", "--worktree", "--get", "core.sparseCheckout"]) != "false":
        raise SystemExit("sparse checkout is not disabled in the pin worktree; STOP")
    # The pin commit carries CRLF blobs under an eol=lf attribute, so git status reports them modified although their
    # raw bytes equal the commit's blobs. Every such entry must be raw-equal to its commit; anything else stops the run.
    dirty = sorted(s[3:] for s in git_bytes(root, ["status", "--porcelain"]).decode("utf-8", "replace").splitlines())
    raw_bad = [f for f in dirty if git_text(root, ["hash-object", "--no-filters", "--", f])
               != git_text(root, ["rev-parse", "HEAD:" + f])]
    if raw_bad:
        raise SystemExit("the pin tree differs from its commit at %d files that are not line-ending entries; STOP" % len(raw_bad))
    print("firm: pin entries reported modified by the line-ending filter (raw bytes equal to the commit): %d" % len(dirty))

    # 1. the COMMITTED candidate files into the pin tree
    deliv = repo / ADDENDUM_REL
    cand_bytes = {}
    for p in OVERLAY_FILES:
        data = (deliv / os.path.basename(p)).read_bytes()
        (root / p).write_bytes(data)
        cand_bytes[p] = data
    status = sorted(s[3:] for s in git_bytes(root, ["status", "--porcelain"]).decode("utf-8", "replace").splitlines())
    if sorted(set(status) - set(dirty)) != sorted(OVERLAY_FILES):
        raise SystemExit("after the copy the pin tree differs from the two candidate files; STOP")
    print("firm: candidate copied into the pin tree; modified entries=%d (two candidate files and %d line-ending entries)" % (
        len(status), len(dirty)))

    # 2. build twice, BUILD ONLY
    core = load_core(root)
    if BUNDLE not in core.STANDALONE_BUNDLES:
        raise SystemExit("bundle %s is not declared at the minting pin; STOP" % BUNDLE)
    b = core.STANDALONE_BUNDLES[BUNDLE]
    pa, _, erra = core.build_bundle_payload(b)
    pb, _, errb = core.build_bundle_payload(b)
    if pa is None or pb is None:
        raise SystemExit("build failed (%s | %s); STOP" % (erra, errb))
    ma, mb = tar_map(pa), tar_map(pb)
    closure = set(b["members"])
    cand_map = {k: sha(v) for k, v in ma.items() if k != SUMS}
    if set(cand_map) != closure:
        raise SystemExit("the candidate closure differs from the declared members; STOP")
    identical_members = {k: sha(v) for k, v in ma.items()} == {k: sha(v) for k, v in mb.items()}
    identical_tar = sha(pa) == sha(pb)
    cand_sha = sha(pa)
    print("firm: candidate built twice; identical members=%s; identical tar bytes=%s; closure members=%d" % (
        identical_members, identical_tar, len(closure)))
    if not identical_members:
        raise SystemExit("the two builds differ; STOP")

    # 3. live bundle, read only
    head_out = aws_json(core, ["s3api", "head-object", "--bucket", b["bucket"], "--key", b["s3_key"], "--output", "json"])
    live_path = scratch / (FIRM + ".live.tar.gz")
    got = aws_json(core, ["s3api", "get-object", "--bucket", b["bucket"], "--key", b["s3_key"], str(live_path),
                          "--output", "json"])
    live_vid = got.get("VersionId", "")
    mint = json.loads((repo / MINT_RECORD).read_text(encoding="utf-8"))["mints"][FIRM]
    live_is_mint = bool(live_vid) and live_vid == mint["after_version_id"] and head_out.get("VersionId", "") == live_vid
    live = live_path.read_bytes()
    live_sha = sha(live)
    ml = tar_map(live)
    live_map = {k: sha(v) for k, v in ml.items() if k != SUMS}
    changed = sorted(n for n in closure if cand_map.get(n) != live_map.get(n))
    unexpected = [n for n in changed if n not in OVERLAY_FILES]
    members_equal = len(closure) - len(changed)
    sums_c = parse_sums(ma[SUMS]) if SUMS in ma else {}
    sums_l = parse_sums(ml[SUMS]) if SUMS in ml else {}
    sums_diff = sorted(k for k in set(sums_c) | set(sums_l) if sums_c.get(k) != sums_l.get(k))
    print("firm: live read; live equals mint record=%s; changed closure members=%d; unexpected=%d; equal=%d of %d" % (
        live_is_mint, len(changed), len(unexpected), members_equal, len(closure)))

    # 4. offline tests on the candidate tree (tests from HEAD; the one-date bypass test is not run)
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
    tests = {"passed": int(passed.group(1)) if passed else 0,
             "failed": (int(failed.group(1)) if failed else 0) + (int(errors.group(1)) if errors else 0)}
    print("firm: offline tests on the candidate tree: passed=%d failed=%d rc=%d" % (tests["passed"], tests["failed"], r.returncode))

    frag = {
        "candidate_bundle_sha256": cand_sha,
        "live_bundle_sha256": live_sha,
        "members_total": len(closure),
        "members_equal_to_live": members_equal,
        "changed_closure_members": changed,
        "unexpected_changed_members": unexpected,
        "sums_line_diff_equals_candidate": sums_diff == sorted(OVERLAY_FILES),
        "live_is_mint_record": live_is_mint,
        "build_arms_identical_members": identical_members,
        "build_arms_identical_tar_bytes": identical_tar,
        "tests": tests,
        "tests_rc": r.returncode,
    }
    (scratch / "firm.json").write_text(json.dumps(frag, indent=1) + "\n", encoding="utf-8")
    return 0


def cmd_assemble(a):
    repo, scratch = pathlib.Path(a.repo), pathlib.Path(a.scratch)
    ad = json.loads((scratch / "addendum.json").read_text(encoding="utf-8"))
    fr = json.loads((scratch / "firm.json").read_text(encoding="utf-8"))
    sig = json.loads((repo / IB595).read_text(encoding="utf-8"))["firms"][FIRM]
    deliv = repo / DELIV_REL
    changed = []
    for p in OVERLAY_FILES:
        name = os.path.basename(p)
        data = (deliv / "addendum" / FIRM / name).read_bytes()
        if sha(data) != ad["sha"][p]:
            raise SystemExit("committed candidate %s differs from the addendum phase bytes; STOP" % name)
        changed.append({"repo_path": p, "artifact": ADDENDUM_REL + "/" + name, "sha256_candidate": sha(data)})
    if sorted(c["repo_path"] for c in changed) != sorted(OVERLAY_FILES):
        raise SystemExit("the changed members are not exactly the two overlay files; STOP")
    if fr["unexpected_changed_members"]:
        raise SystemExit("an unexpected member differs from the live bundle; STOP")
    notes = [
        "Facts and their basis: the candidate holdings_snapshot.py is the signed IB-pr-595 transplant plus %d D-span lines "
        "merged with %d conflicts (%d lines added, %d removed); HEAD's file blob equals the blob of commit %s (%s)." % (
            ad["merge_lines_added"], ad["merge_conflicts"], ad["merge_lines_added"], ad["merge_lines_removed"], D_HEAD,
            ad["head_blob_equals_1ff5e87e40"]),
        "Measured on the minting pin with the two candidate files in place: %d closure members, %d changed against the live "
        "bundle (the two overlay members only), %d equal; the two builds were identical in members (%s) and in tar bytes (%s)." % (
            fr["members_total"], len(fr["changed_closure_members"]), fr["members_equal_to_live"],
            fr["build_arms_identical_members"], fr["build_arms_identical_tar_bytes"]),
        "Not read and not run: no S3 object was written, no Lambda invoked, no publish or mint function called, no sign-in "
        "made, no vendor contacted; the live version identifier is compared as a boolean and is not written. The one-date "
        "bypass test was not copied or run because it tests the bypass that is not shipped.",
        "Sparse directories: the base worktree gained data/assets/scripts/gold/investor_reporting/ only (local, never "
        "committed); the minting pin is a full detached checkout outside the repository, so no import-chain directory was added.",
        "Offline tests: six files copied from HEAD into the pin tree (tests are not bundle members) and run with pytest; "
        "passed=%d failed=%d (pytest rc=%d); any failing test is named in a row, not edited away." % (
            fr["tests"]["passed"], fr["tests"]["failed"], fr["tests_rc"]),
    ]
    record = {
        "base_commit": a.base_commit,
        "read_date": a.read_date,
        "claim": "measured",
        "method": METHOD,
        "firm": FIRM,
        "minting_pin": MINTING,
        "transplant_ref": {"candidate_bundle_sha256": sig["candidate_bundle_sha256"]},
        "live_bundle_sha256": fr["live_bundle_sha256"],
        "candidate_bundle_sha256": fr["candidate_bundle_sha256"],
        "members_total": fr["members_total"],
        "members_equal_to_live": fr["members_equal_to_live"],
        "cusip_port_present": ad["cusip_port_present"],
        "changed_members": changed,
        "d_spans": {"count": ad["d_count"], "equal_to_head": ad["d_equal_head"], "diff_lines_outside_spans": ad["diff_outside"]},
        "tests": {"passed": fr["tests"]["passed"], "failed": fr["tests"]["failed"]},
        "notes": notes,
        "functions_invoked": 0,
        "sign_ins_made": 0,
        "aws_writes_made": 0,
        "rows_written": 0,
        "figures_written": 0,
        "vendor_requests_sent": 0,
    }
    out = deliv / RECORD_NAME
    out.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    print("record written: members_total=%d; members_equal_to_live=%d; D spans=%d; tests passed=%d failed=%d" % (
        fr["members_total"], fr["members_equal_to_live"], ad["d_count"], fr["tests"]["passed"], fr["tests"]["failed"]))
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_ad = sub.add_parser("addendum")
    p_ad.add_argument("--repo", required=True)
    p_ad.add_argument("--scratch", required=True)
    p_fi = sub.add_parser("firm")
    p_fi.add_argument("--pin-root", required=True)
    p_fi.add_argument("--repo", required=True)
    p_fi.add_argument("--scratch", required=True)
    p_as = sub.add_parser("assemble")
    p_as.add_argument("--repo", required=True)
    p_as.add_argument("--scratch", required=True)
    p_as.add_argument("--base-commit", required=True)
    p_as.add_argument("--read-date", required=True)
    a = ap.parse_args()
    if a.cmd == "addendum":
        return cmd_addendum(a)
    if a.cmd == "firm":
        return cmd_firm(a)
    return cmd_assemble(a)


if __name__ == "__main__":
    sys.exit(main())
