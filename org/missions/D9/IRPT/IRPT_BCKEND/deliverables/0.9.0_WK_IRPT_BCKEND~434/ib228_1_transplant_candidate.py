#!/usr/bin/env python3
# IB-pr-595 holdings TRANSPLANT candidate harness -- 0.9.0_WK_IRPT_BCKEND~434. BUILD ONLY; READ ONLY on AWS.
#
# Phases, run in this order from the worktree root (see the record's method field):
#   transplant  per firm and per file: start from the minting pin's file (pin worktree, outside the repository) and apply
#               the five EXEMPTION commits in order, each as a three-way merge (base = the commit's parent blob, theirs =
#               the commit's blob). The one conflict per firm (the 1ad921000c hunk beside the one-date bypass, whose lines
#               are context only) is resolved by keeping the exemption side up to the bypass boundary and dropping the
#               bypass lines. Writes transplant/<firm>/<name> under this folder and a fragment in scratch.
#   firm        per firm in its own process: copy the COMMITTED transplant files into the pin tree, build the bundle twice
#               (BUILD ONLY, minting pin's safe_deploy_core), read the live bundle (read only) and compare member by member,
#               copy five offline test files from the overlay pin (the one-date bypass test is NOT run) and run pytest.
#   assemble    write the record from the transplant and firm fragments.
#
# Prints counts only. Client data rule: no account, holding, value, object key or object version id is printed or
# written; member names are repository code paths.
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

FIRMS = ["49financial", "cottonwood", "inflection"]
MINTING = {
    "49financial": "b1d354cfc9341168a3b4c316a344876ce0049b97",
    "cottonwood": "5fad7eaaa8fb4c512190fa406b78c683c4b6ad1f",
    "inflection": "5fad7eaaa8fb4c512190fa406b78c683c4b6ad1f",
}
BUNDLE_OF = {"49financial": "irpt_holdings_49f", "cottonwood": "irpt_holdings_cot", "inflection": "irpt_holdings_inf"}
HS = "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py"
PU = "infra/aws/lambda/investor-reporting/holdings/publication.py"
OVERLAY_FILES = [HS, PU]
# the five exemption commits (authored by ~419, ~420, ~424), oldest first; each one's parent blob is the previous one's blob
CHAIN = ["b1f767053e", "1b184295b6", "738bf3d07f", "1ad921000c", "381be2ca6c"]
OVERLAY_PIN = "fa2502c5b116dba01a3f7b2522f5f0e6b107b821"
BASE_COMMIT = "d327c250bc61c17aadf83741a5bd69d5a3aa1e4b"
READ_DATE = "2026-10-15"
TEST_FILES = [
    "data/assets/scripts/gold/investor_reporting/tests/test_absent_at_source_wiring.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_absent_at_source_exemption.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_absent_at_source_receipts.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_holdings_publish_gate.py",
    "infra/aws/lambda/investor-reporting/holdings/tests/test_publication.py",
]
SUMS = "SHA256SUMS"
MINT_RECORD = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~IB2/IB199-2_mints_and_business_date_statement.json"
DELIV_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~434"
RECORD_NAME = "IB228-1_holdings_transplant_candidate.json"
BYPASS_BOUNDARY = "if allow_older_date is not None:"
BLOCK_BEGIN = "# BEGIN ABSENT-AT-SOURCE-"
BLOCK_END = "# END ABSENT-AT-SOURCE-"
METHOD = (
    "Run from the worktree root in this order. First, transplant: for each firm, the minting pin's holdings_snapshot.py and "
    "publication.py (full detached worktrees outside the repository, sparse checkout disabled there alone) were taken and the "
    "five exemption commits b1f767053e, 1b184295b6, 738bf3d07f, 1ad921000c and 381be2ca6c were applied in that order, each as "
    "a three-way merge against its own parent blob, with the one-date bypass lines dropped from the single conflict per firm; "
    "the transplanted files were written to the deliverables folder, committed, and checked (ABSENT-AT-SOURCE blocks stripped "
    "and diffed against the pin). Second, the firm phase ran once per firm in its own process: the committed transplant files "
    "were copied into the pin tree, the firm bundle was built twice by the minting pin safe_deploy_core build_bundle_payload "
    "(arm A and arm B, no upload function called), the live bundle was read with s3api head-object and get-object (read only) "
    "and compared member by member with the candidate, and five offline test files were copied from the overlay pin and run "
    "with pytest on the transplant tree (the one-date bypass test was not run). Third, the assemble phase wrote the record. "
    "Nothing was uploaded, minted, deployed, signed or written to AWS."
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


def resolve(merged, tag):
    """Resolve each conflict to the exemption side up to the one-date bypass boundary. Any conflict without that boundary,
    or whose kept side names the bypass, stops the transplant."""
    lines = merged.decode("utf-8").splitlines(keepends=True)
    out, info, i = [], [], 0
    while i < len(lines):
        if lines[i].startswith("<<<<<<< "):
            j = next(t for t in range(i + 1, len(lines)) if lines[t].startswith("======="))
            k = next(t for t in range(j + 1, len(lines)) if lines[t].startswith(">>>>>>> "))
            ours, theirs = lines[i + 1:j], lines[j + 1:k]
            cut = next((t for t, ln in enumerate(theirs) if ln.strip() == BYPASS_BOUNDARY), None)
            if cut is None:
                raise SystemExit("%s: a conflict without the bypass boundary; STOP" % tag)
            if any("allow_older_date" in ln or "ONE-DATE" in ln for ln in theirs[:cut]):
                raise SystemExit("%s: the kept side names the bypass; STOP" % tag)
            out.extend(theirs[:cut])
            info.append({"ours_lines": len(ours), "kept_theirs_lines": cut, "dropped_bypass_lines": len(theirs) - cut})
            i = k + 1
        else:
            out.append(lines[i])
            i += 1
    return "".join(out).encode("utf-8"), info


def strip_blocks(text):
    """The text with every ABSENT-AT-SOURCE A, B and C block removed (BEGIN and END lines included)."""
    out, inside = [], False
    for ln in text.splitlines(keepends=True):
        if BLOCK_BEGIN in ln:
            inside = True
            continue
        if inside:
            if BLOCK_END in ln:
                inside = False
            continue
        out.append(ln)
    if inside:
        raise SystemExit("an ABSENT-AT-SOURCE block is not closed; STOP")
    return "".join(out)


def changed_lines(a_lines, b_lines):
    diff = list(difflib.unified_diff(a_lines, b_lines, n=0))
    return [ln for ln in diff if (ln.startswith("+") or ln.startswith("-")) and not ln.startswith(("+++", "---"))], diff


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


def cmd_transplant(a):
    repo, scratch = pathlib.Path(a.repo), pathlib.Path(a.scratch)
    deliv = repo / DELIV_REL / "transplant"
    tmp = tempfile.mkdtemp(dir=str(scratch))
    for firm in FIRMS:
        pin = scratch / "pins" / firm
        if git_text(pin, ["rev-parse", "HEAD"]) != MINTING[firm]:
            raise SystemExit("%s: pin HEAD is not the minting pin" % firm)
        frag = {"firm": firm, "minting_pin": MINTING[firm], "conflicts": 0, "resolutions": []}
        for path in OVERLAY_FILES:
            name = os.path.basename(path)
            pin_bytes = (pin / path).read_bytes()
            cur = pin_bytes
            for c in CHAIN:
                base = git_bytes(repo, ["show", c + "^:" + path])
                theirs = git_bytes(repo, ["show", c + ":" + path])
                merged, rc = merge3(cur, base, theirs, tmp)
                if rc:
                    merged, info = resolve(merged, "%s %s %s" % (firm, name, c))
                    if len(info) != rc:
                        raise SystemExit("%s: conflict count does not match the resolutions" % firm)
                    frag["conflicts"] += rc
                    frag["resolutions"] += [dict(i, commit=c, file=name) for i in info]
                cur = merged
            target = deliv / firm / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(cur)
            if name == os.path.basename(HS):
                text = cur.decode("utf-8")
                stripped = strip_blocks(text)
                lines, diff = changed_lines(pin_bytes.decode("utf-8").splitlines(keepends=True),
                                            stripped.splitlines(keepends=True))
                (scratch / ("foreign_diff_%s.diff" % firm)).write_text("".join(diff), encoding="utf-8")
                frag["foreign_diff_lines"] = len(lines)
                frag["one_date_bypass_absent"] = ("allow_older_date" not in text) and ("ONE-DATE-ASSERT" not in text)
                frag["cusip_port_present"] = "cusip_key" in text
                frag["blocks_stripped_lines"] = len(text.splitlines()) - len(stripped.splitlines())
                frag["transplanted_lines"] = len(text.splitlines())
                frag["pin_lines"] = len(pin_bytes.decode("utf-8").splitlines())
                frag["changed_hunks"] = sum(1 for ln in diff if ln.startswith("@@"))
            frag.setdefault("transplanted_files", []).append(name)
        (scratch / ("tx_" + firm + ".json")).write_text(json.dumps(frag, indent=1) + "\n", encoding="utf-8")
        print("%s: conflicts resolved=%d; resolutions=%d; foreign_diff_lines=%d; hunks=%d; one_date_bypass_absent=%s; "
              "cusip_port_present=%s; blocks_stripped_lines=%d" % (
                  firm, frag["conflicts"], len(frag["resolutions"]), frag["foreign_diff_lines"], frag["changed_hunks"],
                  frag["one_date_bypass_absent"], frag["cusip_port_present"], frag["blocks_stripped_lines"]))
    return 0


def cmd_firm(a):
    firm = a.firm
    root = pathlib.Path(a.pin_root)
    repo = pathlib.Path(a.repo)
    scratch = pathlib.Path(a.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    os.chdir(str(root))
    sys.path.insert(0, str(root))
    frag = {"firm": firm, "minting_pin": MINTING[firm]}
    if git_text(root, ["rev-parse", "HEAD"]) != MINTING[firm]:
        raise SystemExit("%s: pin worktree HEAD is not the minting pin" % firm)
    if git_text(root, ["config", "--worktree", "--get", "core.sparseCheckout"]) != "false":
        raise SystemExit("%s: sparse checkout is not disabled in the pin worktree" % firm)
    if git_text(root, ["status", "--porcelain"]):
        raise SystemExit("%s: pin worktree is not clean before the transplant" % firm)

    # 1. the COMMITTED transplant files into the pin tree
    deliv = repo / DELIV_REL / "transplant" / firm
    transplanted = {}
    for p in OVERLAY_FILES:
        data = (deliv / os.path.basename(p)).read_bytes()
        (root / p).write_bytes(data)
        transplanted[p] = sha(data)
    status = git_bytes(root, ["status", "--porcelain"]).decode("utf-8", "replace").splitlines()
    frag["overlay_status_entries"] = len(status)
    if sorted(s[3:] for s in status) != sorted(OVERLAY_FILES):
        raise SystemExit("%s: after the transplant the tree differs from the two transplanted files" % firm)
    print("%s: transplant applied; modified entries in the pin worktree=%d" % (firm, len(status)))

    # 2. build twice, BUILD ONLY
    core = load_core(root)
    bname = BUNDLE_OF[firm]
    if bname not in core.STANDALONE_BUNDLES:
        raise SystemExit("%s: bundle %s is not declared at the transplant tree" % (firm, bname))
    b = core.STANDALONE_BUNDLES[bname]
    pa, _, erra = core.build_bundle_payload(b)
    pb, _, errb = core.build_bundle_payload(b)
    if pa is None or pb is None:
        raise SystemExit("%s: build failed (%s | %s)" % (firm, erra, errb))
    ma, mb = tar_map(pa), tar_map(pb)
    closure = set(b["members"])
    cand_map = {k: sha(v) for k, v in ma.items() if k != SUMS}
    if set(cand_map) != closure:
        raise SystemExit("%s: candidate closure differs from the declared members" % firm)
    frag["build_arms_identical_members"] = {k: sha(v) for k, v in ma.items()} == {k: sha(v) for k, v in mb.items()}
    frag["build_arms_identical_tar_bytes"] = sha(pa) == sha(pb)
    frag["members_total"] = len(closure)
    frag["candidate_bundle_sha256"] = sha(pa)
    print("%s: candidate built twice; identical members=%s; identical tar bytes=%s; closure members=%d" % (
        firm, frag["build_arms_identical_members"], frag["build_arms_identical_tar_bytes"], len(closure)))
    (scratch / (firm + ".candidate.tar.gz")).write_bytes(pa)

    # 3. live bundle, read only
    head_out = aws_json(core, ["s3api", "head-object", "--bucket", b["bucket"], "--key", b["s3_key"], "--output", "json"])
    live_path = scratch / (firm + ".live.tar.gz")
    got = aws_json(core, ["s3api", "get-object", "--bucket", b["bucket"], "--key", b["s3_key"], str(live_path),
                          "--output", "json"])
    live_vid = got.get("VersionId", "")
    mint = json.loads((repo / MINT_RECORD).read_text(encoding="utf-8"))["mints"][firm]
    frag["live_version_equals_mint_record"] = bool(live_vid) and live_vid == mint["after_version_id"] \
        and head_out.get("VersionId", "") == live_vid
    live = live_path.read_bytes()
    frag["live_bundle_sha256"] = sha(live)
    ml = tar_map(live)
    live_map = {k: sha(v) for k, v in ml.items() if k != SUMS}
    changed = sorted(n for n in closure if cand_map.get(n) != live_map.get(n))
    frag["members_equal_to_live"] = len(closure) - len(changed)
    unexpected = [n for n in changed if n not in OVERLAY_FILES]
    frag["changed_closure_members"] = len(changed)
    frag["unexpected_changed_members"] = unexpected
    frag["live_only_members"] = len(set(live_map) - closure)
    sums_c = parse_sums(ma[SUMS]) if SUMS in ma else {}
    sums_l = parse_sums(ml[SUMS]) if SUMS in ml else {}
    sums_diff = sorted(k for k in set(sums_c) | set(sums_l) if sums_c.get(k) != sums_l.get(k))
    frag["sums_line_diff_equals_transplant"] = sums_diff == sorted(OVERLAY_FILES)
    frag["changed_members"] = [{"repo_path": p, "transplanted_sha256": transplanted[p]} for p in sorted(changed)]
    print("%s: live read; live version equals mint record=%s; changed closure members=%d; unexpected=%d; equal=%d of %d" % (
        firm, frag["live_version_equals_mint_record"], len(changed), len(unexpected), frag["members_equal_to_live"],
        len(closure)))

    # 4. offline tests on the transplant tree (the one-date bypass test is not run)
    for p in TEST_FILES:
        data = git_bytes(repo, ["show", OVERLAY_PIN + ":" + p])
        dst = root / p
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + TEST_FILES, cwd=str(root),
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1200)
    (scratch / (firm + ".pytest.log")).write_text(r.stdout + r.stderr, encoding="utf-8")
    lines = [ln for ln in (r.stdout + r.stderr).splitlines() if ln.strip()]
    last = lines[-1] if lines else ""
    passed = re.search(r"(\d+) passed", last)
    failed = re.search(r"(\d+) failed", last)
    errors = re.search(r"(\d+) error", last)
    frag["overlay_tests"] = {"passed": int(passed.group(1)) if passed else 0,
                             "failed": (int(failed.group(1)) if failed else 0) + (int(errors.group(1)) if errors else 0)}
    frag["overlay_tests_rc"] = r.returncode
    print("%s: offline tests on the transplant tree: passed=%d failed=%d rc=%d" % (
        firm, frag["overlay_tests"]["passed"], frag["overlay_tests"]["failed"], r.returncode))
    (scratch / ("frag_" + firm + ".json")).write_text(json.dumps(frag, indent=1) + "\n", encoding="utf-8")
    return 0


def cmd_assemble(a):
    repo, scratch = pathlib.Path(a.repo), pathlib.Path(a.scratch)
    deliv = repo / DELIV_REL
    firms = {}
    for firm in FIRMS:
        f = json.loads((scratch / ("frag_" + firm + ".json")).read_text(encoding="utf-8"))
        t = json.loads((scratch / ("tx_" + firm + ".json")).read_text(encoding="utf-8"))
        changed = []
        for m in f["changed_members"]:
            name = os.path.basename(m["repo_path"])
            data = (deliv / "transplant" / firm / name).read_bytes()
            if sha(data) != m["transplanted_sha256"]:
                raise SystemExit("%s: committed transplant file differs from the transplant phase bytes" % firm)
            changed.append({"repo_path": m["repo_path"],
                            "artifact": DELIV_REL + "/transplant/" + firm + "/" + name,
                            "sha256_transplanted": sha(data)})
        firms[firm] = {
            "minting_pin": f["minting_pin"],
            "live_bundle_sha256": f["live_bundle_sha256"],
            "candidate_bundle_sha256": f["candidate_bundle_sha256"],
            "members_total": f["members_total"],
            "members_equal_to_live": f["members_equal_to_live"],
            "changed_members": changed,
            "transplant": {
                "one_date_bypass_absent": t["one_date_bypass_absent"],
                "cusip_port_present": t["cusip_port_present"],
                "foreign_diff_lines": t["foreign_diff_lines"],
                "foreign_diff_reading": a.reading[firm],
            },
            "overlay_tests": f["overlay_tests"],
            "transplant_conflicts_resolved": t["conflicts"],
            "overlay_status_entries": f["overlay_status_entries"],
            "build_arms_identical_members": f["build_arms_identical_members"],
            "build_arms_identical_tar_bytes": f["build_arms_identical_tar_bytes"],
            "live_version_equals_mint_record": f["live_version_equals_mint_record"],
            "unexpected_changed_members": len(f["unexpected_changed_members"]),
            "live_only_members": f["live_only_members"],
            "sums_line_diff_equals_transplant": f["sums_line_diff_equals_transplant"],
        }
    notes = [
        "Facts and their basis: the overlay pin fa2502c5b1 is the base of the IB-pr-590 candidate; the five exemption commits "
        "b1f767053e, 1b184295b6, 738bf3d07f, 1ad921000c and 381be2ca6c are the ones that touch the two files and are authored by "
        "workers 419, 420 and 424, and the chain is linear for both files (each parent blob equals the previous commit's blob).",
        "Transplant conflicts: the only conflict is the 1ad921000c hunk in run_firm beside the one-date bypass; its bypass lines "
        "are context in the commit and are dropped, the exemption call-site lines are kept. The pin text outside the exemption "
        "blocks is kept. No hunk of 15e0361375, de08782c38 or 5fad7eaaa8 is applied; the 49F CUSIP port stays live in the 49F pin.",
        "Not read and not run: no Lambda was invoked, no publish or mint function was called, no sign-in was made and no vendor "
        "was contacted. The live object version was compared with the IB-pr-549 mint record as a boolean only; the version "
        "identifier is not written. test_holdings_bypass_one_date.py was not run because it tests the bypass that is not shipped.",
        "Sparse directories: the base worktree's sparse set gained data/assets/scripts/gold/investor_reporting/ only (local, "
        "never committed); the three pin worktrees are full detached checkouts outside the repository, so the import-chain "
        "directories were not needed there. The transplant commit's gates printed a WARN that the client-data account-id list "
        "is absent on this box, so that commit was not checked against it; its six files carry code only.",
    ]
    record = {
        "overlay_pin": OVERLAY_PIN,
        "firms": firms,
        "base_commit": a.base_commit,
        "read_date": a.read_date,
        "method": METHOD,
        "claim": "measured",
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
    for firm in FIRMS:
        fr = firms[firm]
        print("%s: members_equal_to_live=%d of %d; changed=%d; unexpected=%d; overlay_tests=%s" % (
            firm, fr["members_equal_to_live"], fr["members_total"], len(fr["changed_members"]),
            fr["unexpected_changed_members"], fr["overlay_tests"]))
    print("record written: firms=%d" % len(firms))
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_tx = sub.add_parser("transplant")
    p_tx.add_argument("--repo", required=True)
    p_tx.add_argument("--scratch", required=True)
    p_firm = sub.add_parser("firm")
    p_firm.add_argument("--firm", required=True, choices=FIRMS)
    p_firm.add_argument("--pin-root", required=True)
    p_firm.add_argument("--repo", required=True)
    p_firm.add_argument("--scratch", required=True)
    p_asm = sub.add_parser("assemble")
    p_asm.add_argument("--repo", required=True)
    p_asm.add_argument("--scratch", required=True)
    p_asm.add_argument("--base-commit", default=BASE_COMMIT)
    p_asm.add_argument("--read-date", default=READ_DATE)
    p_asm.add_argument("--reading-file", required=True)
    a = ap.parse_args()
    if a.cmd == "transplant":
        return cmd_transplant(a)
    if a.cmd == "firm":
        return cmd_firm(a)
    a.reading = json.loads(pathlib.Path(a.reading_file).read_text(encoding="utf-8"))
    return cmd_assemble(a)


if __name__ == "__main__":
    sys.exit(main())
