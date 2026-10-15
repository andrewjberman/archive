#!/usr/bin/env python3
# IB-pr-590 overlay candidate harness -- 0.9.0_WK_IRPT_BCKEND~431. BUILD ONLY and READ ONLY on AWS.
#
# Per firm (one process per firm, so no module imported for one firm's pin can be reused for another):
#   1. overlay: the firm's MINTING pin, full detached worktree outside the repository (sparse checkout disabled in that
#      worktree alone); exactly two files are overlaid from the OVERLAY pin (holdings_snapshot.py, publication.py).
#   2. build: the firm's bundle is built from that overlay tree twice with the builder of the minting pin's
#      .tools/safe_deploy_core.py (build_bundle_payload; no upload, mint, put or copy function is called).
#   3. live: the live bundle is read with s3api head-object and get-object (read only) into scratch; compared member by
#      member with the candidate. The changed closure members must be EXACTLY the two overlaid files.
#   4. tests: six offline test files are copied from the overlay pin into the overlay tree and run with pytest.
# Then the parent writes the record from the three fragments (phase "assemble").
#
# Prints counts only. Client data rule: no account, holding, value, object key or object version id is printed or
# written; member names are repository code paths.
import argparse
import datetime
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

FIRMS = ["49financial", "cottonwood", "inflection"]
MINTING = {
    "49financial": "b1d354cfc9341168a3b4c316a344876ce0049b97",
    "cottonwood": "5fad7eaaa8fb4c512190fa406b78c683c4b6ad1f",
    "inflection": "5fad7eaaa8fb4c512190fa406b78c683c4b6ad1f",
}
BUNDLE_OF = {"49financial": "irpt_holdings_49f", "cottonwood": "irpt_holdings_cot", "inflection": "irpt_holdings_inf"}
HS = "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py"
PUB = "infra/aws/lambda/investor-reporting/holdings/publication.py"
OVERLAY_FILES = [HS, PUB]
TEST_FILES = [
    "data/assets/scripts/gold/investor_reporting/tests/test_absent_at_source_wiring.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_absent_at_source_exemption.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_absent_at_source_receipts.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_holdings_publish_gate.py",
    "data/assets/scripts/gold/investor_reporting/tests/test_holdings_bypass_one_date.py",
    "infra/aws/lambda/investor-reporting/holdings/tests/test_publication.py",
]
SUMS = "SHA256SUMS"
MINT_RECORD = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~IB2/IB199-2_mints_and_business_date_statement.json"
HERE = pathlib.Path(__file__).resolve().parent
RECORD_NAME = "IB224-1_holdings_overlay_candidate.json"

METHOD = (
    "Run from the base worktree root in this order. First, three full detached worktrees of the minting pins were made "
    "outside the repository (49financial at b1d354, Cottonwood and Inflection at 5fad7e), each with sparse checkout "
    "disabled in that worktree alone. Second, the firm phase ran once per firm in its own process (49financial, then "
    "cottonwood, then inflection): exactly two files, holdings_snapshot.py and publication.py, are overlaid from the "
    "overlay pin by git show; the firm bundle is built twice by the minting pin safe_deploy_core build_bundle_payload "
    "(arm A and arm B, no upload function called); the live bundle is read with s3api head-object and get-object (read "
    "only) and compared member by member with the candidate; six offline test files are copied from the overlay pin and "
    "run with pytest on the overlay tree. Third, the assemble phase wrote the record from the three firm fragments. "
    "Nothing was uploaded, minted, deployed or written to AWS."
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


def ensure_pin(scratch, firm, overlay_pin_unused=None):
    """Create the firm's full detached worktree of its minting pin outside the repository (once)."""
    wt = pathlib.Path(scratch) / firm
    if (wt / ".git").exists():
        return wt
    base = pathlib.Path(os.getcwd())
    subprocess.run(["git", "-C", str(base), "worktree", "add", "--no-checkout", "--detach", str(wt), MINTING[firm]],
                   check=True, capture_output=True, timeout=600)
    subprocess.run(["git", "-C", str(wt), "config", "--worktree", "core.sparseCheckout", "false"],
                   check=True, capture_output=True, timeout=120)
    subprocess.run(["git", "-C", str(wt), "checkout", "-q", "-f", "HEAD"], check=True, capture_output=True, timeout=3600)
    return wt


def phase_firm(a):
    firm = a.firm
    root = pathlib.Path(a.pin_root)
    frag = {"firm": firm, "minting_pin": MINTING[firm]}
    head = git_text(root, ["rev-parse", "HEAD"])
    if head != MINTING[firm]:
        raise SystemExit("%s: pin worktree HEAD is not the minting pin" % firm)
    if git_text(root, ["config", "--worktree", "--get", "core.sparseCheckout"]) != "false":
        raise SystemExit("%s: sparse checkout is not disabled in the pin worktree" % firm)
    if git_text(root, ["status", "--porcelain"]):
        raise SystemExit("%s: pin worktree is not clean before the overlay" % firm)

    # 1. overlay exactly two files from the overlay pin
    overlay_at_pin = {}
    for p in OVERLAY_FILES:
        data = git_bytes(root, ["show", a.overlay_pin + ":" + p])
        (root / p).write_bytes(data)
        if sha((root / p).read_bytes()) != sha(data):
            raise SystemExit("%s: overlaid bytes differ from the overlay pin blob for one file" % firm)
        overlay_at_pin[p] = sha(data)
    status = git_bytes(root, ["status", "--porcelain"]).decode("utf-8", "replace").splitlines()
    frag["overlay_status_entries"] = len(status)
    if sorted(s[3:] for s in status) != sorted(OVERLAY_FILES):
        raise SystemExit("%s: after the overlay the tree differs from the two overlaid files" % firm)
    print("%s: overlay applied; modified entries in the pin worktree=%d" % (firm, len(status)))

    # 2. build twice, BUILD ONLY
    core = load_core(root)
    bname = BUNDLE_OF[firm]
    if bname not in core.STANDALONE_BUNDLES:
        raise SystemExit("%s: bundle %s is not declared at the overlay tree" % (firm, bname))
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
    cand_sha = sha(pa)
    frag["members_total"] = len(closure)
    frag["candidate_bundle_sha256"] = cand_sha
    print("%s: candidate built twice; identical members=%s; identical tar bytes=%s; closure members=%d" % (
        firm, frag["build_arms_identical_members"], frag["build_arms_identical_tar_bytes"], len(closure)))
    scratch = pathlib.Path(a.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    (scratch / (firm + ".candidate.tar.gz")).write_bytes(pa)

    # 3. live bundle, read only
    head_out = aws_json(core, ["s3api", "head-object", "--bucket", b["bucket"], "--key", b["s3_key"], "--output", "json"])
    live_path = scratch / (firm + ".live.tar.gz")
    got = aws_json(core, ["s3api", "get-object", "--bucket", b["bucket"], "--key", b["s3_key"], str(live_path),
                          "--output", "json"])
    live_vid = got.get("VersionId", "")
    mint = json.loads((pathlib.Path(a.repo) / MINT_RECORD).read_text(encoding="utf-8"))["mints"][firm]
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
    frag["sums_line_diff_equals_overlay"] = sums_diff == sorted(OVERLAY_FILES)
    frag["changed_members"] = [{"repo_path": p, "sha256_at_pin": overlay_at_pin[p]} for p in sorted(changed)]
    print("%s: live read; live version equals mint record=%s; changed closure members=%d; unexpected=%d; equal=%d of %d" % (
        firm, frag["live_version_equals_mint_record"], len(changed), len(unexpected), frag["members_equal_to_live"],
        len(closure)))

    # 4. offline tests on the overlay tree
    for p in TEST_FILES:
        data = git_bytes(root, ["show", a.overlay_pin + ":" + p])
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
    print("%s: offline tests on the overlay tree: passed=%d failed=%d rc=%d" % (
        firm, frag["overlay_tests"]["passed"], frag["overlay_tests"]["failed"], r.returncode))

    out = pathlib.Path(a.fragment)
    out.write_text(json.dumps(frag, indent=1) + "\n", encoding="utf-8")
    return 0


def phase_run(a):
    scratch = pathlib.Path(a.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    frags = {}
    for firm in FIRMS:
        pin = ensure_pin(scratch, firm)
        frag_path = scratch / ("frag_" + firm + ".json")
        r = subprocess.run([sys.executable, str(pathlib.Path(__file__).resolve()), "firm", "--firm", firm,
                            "--pin-root", str(pin), "--overlay-pin", a.overlay_pin, "--scratch", str(scratch),
                            "--fragment", str(frag_path), "--repo", a.repo], timeout=3600)
        if r.returncode != 0:
            raise SystemExit("%s: firm phase rc=%d" % (firm, r.returncode))
        frags[firm] = json.loads(frag_path.read_text(encoding="utf-8"))
    return assemble(a, frags)


def assemble(a, frags):
    firms = {}
    for firm in FIRMS:
        f = frags[firm]
        firms[firm] = {
            "minting_pin": f["minting_pin"],
            "live_bundle_sha256": f["live_bundle_sha256"],
            "candidate_bundle_sha256": f["candidate_bundle_sha256"],
            "members_total": f["members_total"],
            "members_equal_to_live": f["members_equal_to_live"],
            "changed_members": f["changed_members"],
            "overlay_tests": f["overlay_tests"],
            "overlay_status_entries": f["overlay_status_entries"],
            "build_arms_identical_members": f["build_arms_identical_members"],
            "build_arms_identical_tar_bytes": f["build_arms_identical_tar_bytes"],
            "live_version_equals_mint_record": f["live_version_equals_mint_record"],
            "unexpected_changed_members": len(f["unexpected_changed_members"]),
            "live_only_members": f["live_only_members"],
            "sums_line_diff_equals_overlay": f["sums_line_diff_equals_overlay"],
        }
    notes = [
        "Facts and their basis: the overlay pin is the base HEAD; the ABSENT-AT-SOURCE A, B and C blocks in its "
        "holdings_snapshot.py are graded by the AC1 check at run time, not by this harness. Each firm bundle is built from "
        "its minting pin tree with only the two overlaid files changed; the live bundle is read with head-object and "
        "get-object (read only) and compared member by member.",
        "Build arms: each firm candidate was built twice in process from its pin tree; build_arms_identical_members and "
        "build_arms_identical_tar_bytes are recorded per firm as booleans (tar bytes may differ by timestamp, the members may not). "
        "SHA256SUMS is the manifest member inside the bundle and is not a closure member; its line difference is recorded "
        "as equal to the overlay pair or not.",
        "Not read and not run: no Lambda was invoked, no publish or mint function was called, no sign-in was made and no "
        "vendor was contacted. The live object version was compared with the IB-pr-549 mint record as a boolean only and the "
        "version identifier is not written. The pin worktrees are full detached checkouts outside the repository; the first "
        "49financial firm attempt stopped at the overlay status check before any build or AWS call and was re-run after the "
        "two overlaid files were restored in that pin.",
        "Counters: the six counters are zero because nothing was invoked, signed in, written to AWS, written as rows or "
        "figures, or sent to a vendor; the surprise rows filed in the channel are the only writes and are not counted here.",
    ]
    record = {
        "overlay_pin": a.overlay_pin,
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
    out = pathlib.Path(a.record)
    out.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    for firm in FIRMS:
        f = frags[firm]
        print("%s: members_equal_to_live=%d of %d; changed=%d; unexpected=%d; overlay_tests=%s; mint version=%s" % (
            firm, f["members_equal_to_live"], f["members_total"], len(f["changed_members"]),
            len(f["unexpected_changed_members"]), f["overlay_tests"], f["live_version_equals_mint_record"]))
    print("record written: firms=%d; generated %s" % (len(firms), datetime.datetime.now(datetime.timezone.utc).strftime("%FT%TZ")))
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_run = sub.add_parser("run")
    p_run.add_argument("--scratch", required=True)
    p_run.add_argument("--overlay-pin", required=True)
    p_run.add_argument("--base-commit", required=True)
    p_run.add_argument("--read-date", required=True)
    p_run.add_argument("--record", required=True)
    p_run.add_argument("--repo", default=str(pathlib.Path(os.getcwd())))
    p_asm = sub.add_parser("assemble")
    p_asm.add_argument("--scratch", required=True)
    p_asm.add_argument("--overlay-pin", required=True)
    p_asm.add_argument("--base-commit", required=True)
    p_asm.add_argument("--read-date", required=True)
    p_asm.add_argument("--record", required=True)
    p_firm = sub.add_parser("firm")
    p_firm.add_argument("--firm", required=True, choices=FIRMS)
    p_firm.add_argument("--pin-root", required=True)
    p_firm.add_argument("--overlay-pin", required=True)
    p_firm.add_argument("--scratch", required=True)
    p_firm.add_argument("--fragment", required=True)
    p_firm.add_argument("--repo", required=True)
    a = ap.parse_args()
    if a.cmd == "firm":
        return phase_firm(a)
    if a.cmd == "assemble":
        scratch = pathlib.Path(a.scratch)
        frags = {f: json.loads((scratch / ("frag_" + f + ".json")).read_text(encoding="utf-8")) for f in FIRMS}
        return assemble(a, frags)
    return phase_run(a)


if __name__ == "__main__":
    sys.exit(main())
