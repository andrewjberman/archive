#!/usr/bin/env python3
# IB-pr-606 ADDENDUM 1 candidate harness -- 0.9.0_WK_IRPT_BCKEND~442, 49 Financial ONLY. BUILD ONLY; READ ONLY on AWS.
#
# Phases, run in this order from the worktree root; the pin is a detached worktree of the minting pin OUTSIDE the repository:
#   candidate  the committed IB-pr-595 transplant files (49financial) are written into the pin tree; the diff of commit
#              0a745b842b for holdings_snapshot.py (three ABSENT-AT-SOURCE-D spans, insertions only) is applied to it with
#              git apply; the candidate is verified (strip the D spans -> the transplant byte for byte; the D spans equal
#              HEAD's; no one-date bypass; cusip_key present); the two candidate files are written under
#              deliverables/addendum/49financial/.
#   firm       the candidate bundle is built twice (BUILD ONLY, the minting pin's safe_deploy_core); the live bundle is read
#              (read only: head-object and get-object) and compared member by member; six offline test files are copied from
#              HEAD and run with pytest on the candidate tree (test_holdings_bypass_one_date.py is NOT run).
#   assemble   writes IB237-1_addendum_candidate.json beside this script.
#
# Prints counts only. No account, holding, value, object key or object version id is printed or written.
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

FIRM = "49financial"
MINTING = "b1d354cfc9341168a3b4c316a344876ce0049b97"
BUNDLE = "irpt_holdings_49f"
ADDED = "0a745b842b"
HS = "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py"
PU = "infra/aws/lambda/investor-reporting/holdings/publication.py"
OVERLAY = [HS, PU]
DELIV = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~442"
TRANSPLANT = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~434/transplant/49financial"
IB595 = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~434/IB228-1_holdings_transplant_candidate.json"
RECORD = "IB237-1_addendum_candidate.json"
TEST_FILES = [
    "data/assets/scripts/gold/investor_reporting/tests/test_absent_at_source_wiring.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_absent_at_source_exemption.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_absent_at_source_receipts.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_absent_at_source_smartx_evidence.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_holdings_publish_gate.py",
    "infra/aws/lambda/investor-reporting/holdings/tests/test_publication.py",
]
SUMS = "SHA256SUMS"
SPAN = re.compile(r"^[ \t]*# BEGIN ABSENT-AT-SOURCE-D\b.*?^[ \t]*# END ABSENT-AT-SOURCE-D\b[^\n]*\n", re.S | re.M)
METHOD = (
    "Run from the worktree root in this order. First, candidate: the committed IB-pr-595 transplant files for 49financial "
    "(holdings_snapshot.py and publication.py, checked against the sha256 values IB-pr-595's record names) were written into "
    "a detached worktree of the minting pin outside the repository (sparse checkout disabled there); the diff of commit "
    "0a745b842b for holdings_snapshot.py (the three ABSENT-AT-SOURCE-D spans) was applied to the transplanted file with "
    "git apply after git apply --check; the result was verified by stripping every D span and comparing the rest with the "
    "transplant byte for byte, comparing the D spans with HEAD's, and testing for the one-date bypass and the CUSIP key; "
    "the two candidate files were written under deliverables/addendum/49financial/. Second, firm: the candidate bundle was "
    "built twice by the minting pin's safe_deploy_core build_bundle_payload (BUILD ONLY, no upload function called), the "
    "live bundle was read with s3api head-object and get-object (read only) and compared member by member with the "
    "candidate, and six offline test files were copied from HEAD and run with pytest on the candidate tree (the one-date "
    "bypass test was not run). Third, assemble wrote the record. Nothing was uploaded, minted, deployed, signed or written to AWS."
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git_bytes(repo, args):
    r = subprocess.run(["git", "-C", str(repo)] + args, capture_output=True, timeout=600)
    if r.returncode != 0:
        raise SystemExit("git rc=%d %s" % (r.returncode, r.stderr.decode("utf-8", "replace").strip()[:200]))
    return r.stdout


def git_text(repo, args):
    return git_bytes(repo, args).decode("utf-8", "replace").strip()


def status_set(pin):
    out = git_bytes(pin, ["status", "--porcelain", "--untracked-files=no"]).decode("utf-8", "replace").splitlines()
    return {ln[3:] for ln in out}


def changed_outside(a_text, b_text):
    diff = difflib.unified_diff(a_text.splitlines(keepends=True), b_text.splitlines(keepends=True), n=0)
    return sum(1 for ln in diff if ln[:1] in ("+", "-") and not ln.startswith(("+++", "---")))


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
        raise SystemExit("aws read call rc=%d (stderr not printed)" % r.returncode)
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
    repo, pin, scratch = pathlib.Path(a.repo), pathlib.Path(a.pin), pathlib.Path(a.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    if git_text(pin, ["rev-parse", "HEAD"]) != MINTING:
        raise SystemExit("pin HEAD is not the minting pin")
    for p in OVERLAY:
        (pin / p).write_bytes(git_bytes(pin, ["show", "HEAD:" + p]))
    before = status_set(pin)
    tx = repo / TRANSPLANT
    t_hs = (tx / "holdings_snapshot.py").read_bytes()
    t_pu = (tx / "publication.py").read_bytes()
    rec595 = json.loads((repo / IB595).read_text(encoding="utf-8"))["firms"][FIRM]
    want = {m["repo_path"]: m["sha256_transplanted"] for m in rec595["changed_members"]}
    if sha(t_hs) != want[HS] or sha(t_pu) != want[PU]:
        raise SystemExit("the committed transplant files differ from IB-pr-595's record; STOP")
    (pin / HS).write_bytes(t_hs)
    (pin / PU).write_bytes(t_pu)

    dpath = scratch / "addedD.diff"
    dpath.write_bytes(git_bytes(repo, ["diff", ADDED + "^", ADDED, "--", HS]))
    chk = subprocess.run(["git", "-C", str(pin), "apply", "--check", str(dpath)], capture_output=True)
    if chk.returncode != 0:
        raise SystemExit("the D diff does not apply to the transplanted file (git apply --check rc=%d); STOP" % chk.returncode)
    subprocess.run(["git", "-C", str(pin), "apply", str(dpath)], check=True)
    hunks = sum(1 for ln in dpath.read_text(encoding="utf-8").splitlines() if ln.startswith("@@"))

    cand_hs = (pin / HS).read_bytes()
    cand_pu = (pin / PU).read_bytes()
    head_hs = git_bytes(repo, ["show", "HEAD:" + HS])
    ct, ht, tt = cand_hs.decode("utf-8"), head_hs.decode("utf-8"), t_hs.decode("utf-8")
    cs, hs_spans = SPAN.findall(ct), SPAN.findall(ht)
    stripped = SPAN.sub("", ct)
    d = {
        "count": len(cs),
        "equal_to_head": bool(cs) and cs == hs_spans,
        "diff_lines_outside_spans": changed_outside(tt, stripped),
    }
    strip_equals = stripped.encode("utf-8") == t_hs
    one_date_absent = b"allow_older_date" not in cand_hs and b"ONE-DATE-ASSERT" not in cand_hs
    cusip = b"cusip_key" in cand_hs
    pu_same = cand_pu == t_pu
    head_marks = ht.count("ABSENT-AT-SOURCE-D")
    if not (d["equal_to_head"] and strip_equals and one_date_absent and pu_same and d["diff_lines_outside_spans"] == 0):
        raise SystemExit("candidate verification failed (equal_to_head=%s strip_equals=%s one_date_absent=%s pu_same=%s); STOP"
                         % (d["equal_to_head"], strip_equals, one_date_absent, pu_same))
    added = status_set(pin) - before
    if added != set(OVERLAY):
        raise SystemExit("after the candidate the pin differs from the two files by %d entries; STOP" % len(added ^ set(OVERLAY)))

    dest = repo / DELIV / "addendum" / FIRM
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "holdings_snapshot.py").write_bytes(cand_hs)
    (dest / "publication.py").write_bytes(cand_pu)
    frag = {
        "d_spans": d, "cusip_port_present": cusip, "one_date_absent": one_date_absent, "strip_equals_transplant": strip_equals,
        "hunks_applied": hunks, "conflicts": 0, "head_marker_lines": head_marks,
        "candidate_hs_sha256": sha(cand_hs), "candidate_pu_sha256": sha(cand_pu),
    }
    (scratch / "frag_candidate.json").write_text(json.dumps(frag, indent=1) + "\n", encoding="utf-8")
    print("candidate: D spans=%d equal_to_head=%s diff_lines_outside_spans=%d strip_equals_transplant=%s one_date_absent=%s "
          "cusip_port_present=%s hunks_applied=%d conflicts=0 head_marker_lines=%d" % (
              d["count"], d["equal_to_head"], d["diff_lines_outside_spans"], strip_equals, one_date_absent, cusip, hunks,
              head_marks))
    return 0


def cmd_firm(a):
    repo, pin, scratch = pathlib.Path(a.repo), pathlib.Path(a.pin), pathlib.Path(a.scratch)
    if git_text(pin, ["rev-parse", "HEAD"]) != MINTING:
        raise SystemExit("pin HEAD is not the minting pin")
    dest = repo / DELIV / "addendum" / FIRM
    names = {HS: "holdings_snapshot.py", PU: "publication.py"}
    for p, name in names.items():
        if (pin / p).read_bytes() != (dest / name).read_bytes():
            raise SystemExit("the pin tree does not carry the committed candidate %s; STOP" % name)
    os.chdir(str(pin))
    core = load_core(pin)
    b = core.STANDALONE_BUNDLES[BUNDLE]
    pa, _, erra = core.build_bundle_payload(b)
    pb, _, errb = core.build_bundle_payload(b)
    if pa is None or pb is None:
        raise SystemExit("build failed (arm A error present=%s, arm B error present=%s)" % (bool(erra), bool(errb)))
    ma, mb = tar_map(pa), tar_map(pb)
    closure = set(b["members"])
    cand_map = {k: sha(v) for k, v in ma.items() if k != SUMS}
    if set(cand_map) != closure:
        raise SystemExit("candidate closure differs from the declared members; STOP")
    arms_members = {k: sha(v) for k, v in ma.items()} == {k: sha(v) for k, v in mb.items()}
    arms_tar = sha(pa) == sha(pb)
    cand_sha = sha(pa)

    aws_json(core, ["s3api", "head-object", "--bucket", b["bucket"], "--key", b["s3_key"], "--output", "json"])
    live_path = scratch / "live.tar.gz"
    aws_json(core, ["s3api", "get-object", "--bucket", b["bucket"], "--key", b["s3_key"], str(live_path), "--output", "json"])
    live = live_path.read_bytes()
    ml = tar_map(live)
    live_map = {k: sha(v) for k, v in ml.items() if k != SUMS}
    changed = sorted(n for n in closure if cand_map.get(n) != live_map.get(n))
    unexpected = [n for n in changed if n not in OVERLAY]
    if unexpected:
        raise SystemExit("%d unexpected member(s) differ from the live bundle; STOP" % len(unexpected))
    live_only = sorted(set(live_map) - closure)
    sums_c = parse_sums(ma[SUMS]) if SUMS in ma else {}
    sums_l = parse_sums(ml[SUMS]) if SUMS in ml else {}
    sums_diff = sorted(k for k in set(sums_c) | set(sums_l) if sums_c.get(k) != sums_l.get(k))

    for p in TEST_FILES:
        dst = pin / p
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(git_bytes(repo, ["show", "HEAD:" + p]))
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + TEST_FILES, cwd=str(pin),
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1200)
    out = r.stdout + r.stderr
    (scratch / "pytest.log").write_text(out, encoding="utf-8")
    lines = [ln for ln in out.splitlines() if ln.strip()]
    last = lines[-1] if lines else ""
    passed = re.search(r"(\d+) passed", last)
    failed = re.search(r"(\d+) failed", last)
    errors = re.search(r"(\d+) error", last)
    tests = {"passed": int(passed.group(1)) if passed else 0,
             "failed": (int(failed.group(1)) if failed else 0) + (int(errors.group(1)) if errors else 0)}
    frag = {
        "members_total": len(closure), "candidate_bundle_sha256": cand_sha, "live_bundle_sha256": sha(live),
        "changed": changed, "members_equal_to_live": len(closure) - len(changed), "live_only_members": len(live_only),
        "arms_identical_members": arms_members, "arms_identical_tar_bytes": arms_tar,
        "sums_line_diff": sums_diff, "tests": tests, "pytest_rc": r.returncode,
    }
    (scratch / "frag_firm.json").write_text(json.dumps(frag, indent=1) + "\n", encoding="utf-8")
    print("firm: members_total=%d changed_closure_members=%d members_equal_to_live=%d unexpected=0 live_only=%d "
          "arms_identical_members=%s arms_identical_tar_bytes=%s sums_line_diff=%d" % (
              len(closure), len(changed), len(closure) - len(changed), len(live_only), arms_members, arms_tar,
              len(sums_diff)))
    print("firm: offline tests on the candidate tree passed=%d failed=%d pytest_rc=%d" % (
        tests["passed"], tests["failed"], r.returncode))
    return 0


def cmd_assemble(a):
    repo, scratch = pathlib.Path(a.repo), pathlib.Path(a.scratch)
    cand = json.loads((scratch / "frag_candidate.json").read_text(encoding="utf-8"))
    fr = json.loads((scratch / "frag_firm.json").read_text(encoding="utf-8"))
    rec595 = json.loads((repo / IB595).read_text(encoding="utf-8"))["firms"][FIRM]
    dest = repo / DELIV / "addendum" / FIRM
    names = {HS: "holdings_snapshot.py", PU: "publication.py"}
    changed = []
    for n in sorted(fr["changed"]):
        data = (dest / names[n]).read_bytes()
        changed.append({"repo_path": n, "artifact": DELIV + "/addendum/" + FIRM + "/" + names[n],
                        "sha256_candidate": sha(data)})
    d = cand["d_spans"]
    notes = [
        "Facts and their basis: the transplant files are IB-pr-595's committed 49financial files, checked against the sha256 "
        "values in its record before use; the D spans are commit 0a745b842b's three insertions, applied by git apply after a "
        "clean git apply --check (%d hunks, %d conflicts)." % (cand["hunks_applied"], cand["conflicts"]),
        "Measured here: %d D spans in the candidate equal HEAD's three spans text for text; stripping them leaves the signed "
        "transplant byte for byte; %d lines differ outside the spans; the one-date bypass is absent and cusip_key is present."
        % (d["count"], d["diff_lines_outside_spans"]),
        "Not read and not run: no upload, mint, publish, deploy, sign-in or vendor call was made; the live bundle was read only "
        "with head-object and get-object; test_holdings_bypass_one_date.py was not run because it tests the bypass that is "
        "not shipped. Sparse directories: data/assets/scripts/gold/investor_reporting/ was added to the base worktree "
        "(local, never committed); the pin is a full checkout outside the repository.",
        "Pin tree state: the minting pin's index had 36 entries whose line endings differ from its .gitattributes eol=lf "
        "rule, so git status lists them before any change; they are not bundle changes and the status comparison in this "
        "run was taken against that baseline, adding only the two candidate files.",
    ]
    record = {
        "base_commit": a.base_commit,
        "read_date": a.read_date,
        "method": METHOD,
        "claim": "measured",
        "firm": FIRM,
        "minting_pin": MINTING,
        "transplant_ref": {"candidate_bundle_sha256": rec595["candidate_bundle_sha256"]},
        "live_bundle_sha256": fr["live_bundle_sha256"],
        "candidate_bundle_sha256": fr["candidate_bundle_sha256"],
        "members_total": fr["members_total"],
        "members_equal_to_live": fr["members_equal_to_live"],
        "cusip_port_present": cand["cusip_port_present"],
        "changed_members": changed,
        "d_spans": {"count": d["count"], "equal_to_head": d["equal_to_head"],
                    "diff_lines_outside_spans": d["diff_lines_outside_spans"]},
        "tests": fr["tests"],
        "notes": notes,
        "functions_invoked": 0,
        "sign_ins_made": 0,
        "aws_writes_made": 0,
        "rows_written": 0,
        "figures_written": 0,
        "vendor_requests_sent": 0,
    }
    out = repo / DELIV / RECORD
    out.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    print("record written: changed_members=%d members_equal_to_live=%d of %d tests passed=%d failed=%d d_spans=%d" % (
        len(changed), fr["members_equal_to_live"], fr["members_total"], fr["tests"]["passed"], fr["tests"]["failed"],
        d["count"]))
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("candidate", "firm"):
        p = sub.add_parser(name)
        p.add_argument("--repo", required=True)
        p.add_argument("--pin", required=True)
        p.add_argument("--scratch", required=True)
    p_asm = sub.add_parser("assemble")
    p_asm.add_argument("--repo", required=True)
    p_asm.add_argument("--scratch", required=True)
    p_asm.add_argument("--base-commit", default="e9c48c49b711bc7eb18723dad69f034547d6715f")
    p_asm.add_argument("--read-date", default="2026-10-15")
    a = ap.parse_args()
    if a.cmd == "candidate":
        return cmd_candidate(a)
    if a.cmd == "firm":
        return cmd_firm(a)
    return cmd_assemble(a)


if __name__ == "__main__":
    sys.exit(main())
