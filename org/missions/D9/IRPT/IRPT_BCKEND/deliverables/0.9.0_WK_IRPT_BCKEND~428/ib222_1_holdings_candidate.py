#!/usr/bin/env python3
# IB-pr-589 candidate harness -- 0.9.0_WK_IRPT_BCKEND~428. BUILD ONLY and READ ONLY.
#
# Arm 1 (build): loads .tools/safe_deploy_core.py FROM THE PIN WORKTREE (so its WORKSPACE is the pin) and calls
#   build_bundle_payload() on each declared holdings bundle, twice. No upload, mint, put or copy function is called.
# Arm 2 (live, read only): aws s3api head-object and get-object on the declared key, into scratch outside the repo.
# Arm 3 (compare): member name and sha256, candidate versus live; changed members recomputed from git at the pin.
#
# Prints counts only. Writes the record JSON to --record. Client data rule: no account, holding, value or object key
# that carries an account is printed or written; member names are repository code paths.
import argparse
import datetime
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import subprocess
import sys
import tarfile

FIRM_OF = {"irpt_holdings_49f": "49financial", "irpt_holdings_cot": "cottonwood", "irpt_holdings_inf": "inflection"}
SNAPSHOT = "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py"
SUMS = "SHA256SUMS"

METHOD = (
    "Run from the base worktree root. Step 1: git worktree add --detach of the pin into a scratch directory outside "
    "the repository. Step 2: load .tools/safe_deploy_core.py from that pin in process (WORKSPACE is the pin) and call "
    "build_bundle_payload() on each declared holdings bundle, twice (arm A and arm B), with no upload function called. "
    "Step 3: read each live bundle with s3api head-object and get-object (read only) into scratch. Step 4: compare "
    "member name and sha256 of the candidate tarball against the live tarball; changed members have sha256_at_pin from "
    "git show of the pin blob. Step 5: check the live version id against the IB-pr-549 mint record after_version_id. "
    "Only the arm order above was run; nothing was written to AWS."
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git_bytes(repo, args):
    env = dict(os.environ, MSYS_NO_PATHCONV="1")
    r = subprocess.run(["git", "-C", str(repo)] + args, capture_output=True, timeout=300, env=env)
    if r.returncode != 0:
        raise SystemExit("git rc=%d %s" % (r.returncode, r.stderr.decode("utf-8", "replace").strip()[:200]))
    return r.stdout


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
                       timeout=300, env=core._aws_env())
    if r.returncode != 0:
        raise SystemExit("aws rc=%d %s" % (r.returncode, r.stderr.strip()[:300]))
    return json.loads(r.stdout) if r.stdout.strip() else {}


def tar_map(data):
    out = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        for m in tf.getmembers():
            if m.isfile():
                body = tf.extractfile(m).read()
                out[m.name] = body
    return out


def parse_sums(body):
    lines = {}
    for line in body.decode("utf-8").splitlines():
        digest, name = line.split("  ", 1)
        lines[name] = digest
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pin-root", required=True)
    ap.add_argument("--pin", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--mint-record", required=True)
    ap.add_argument("--record", required=True)
    ap.add_argument("--base-commit", required=True)
    ap.add_argument("--read-date", required=True)
    a = ap.parse_args()

    pin = a.pin
    pin_root = pathlib.Path(a.pin_root)
    if git_bytes(pin_root, ["rev-parse", "HEAD"]).decode().strip() != pin:
        raise SystemExit("pin worktree HEAD is not the pin")
    blob = git_bytes(pin_root, ["rev-parse", pin + ":" + SNAPSHOT]).decode().strip()
    snap_text = git_bytes(pin_root, ["show", pin + ":" + SNAPSHOT]).decode("utf-8", "replace")
    absent = {k: snap_text.count("ABSENT-AT-SOURCE-" + k) for k in "ABC"}
    print("pin HEAD verified; ABSENT-AT-SOURCE block lines A=%d B=%d C=%d" % (absent["A"], absent["B"], absent["C"]))

    core = load_core(pin_root)
    scratch = pathlib.Path(a.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    mints = json.loads(pathlib.Path(a.mint_record).read_text(encoding="utf-8"))["mints"]

    bundles = {k: v for k, v in core.STANDALONE_BUNDLES.items() if k in FIRM_OF}
    if sorted(bundles) != sorted(FIRM_OF):
        raise SystemExit("declared bundles differ: %s" % sorted(core.STANDALONE_BUNDLES))
    print("declared holdings bundles: %d" % len(bundles))

    firms_out = {}
    notes_stats = {"identical_members": 0, "identical_tar_bytes": 0, "version_match": 0, "worktree_eq_blob": 0,
                   "worktree_total": 0, "live_eq_src": 0, "live_total": 0, "sums_consistent": 0}
    snapshot_flagged = {}
    extra_total = 0
    for bname in sorted(bundles):
        firm = FIRM_OF[bname]
        b = bundles[bname]
        pa, _, erra = core.build_bundle_payload(b)
        pb, _, errb = core.build_bundle_payload(b)
        if pa is None or pb is None:
            raise SystemExit("build failed for a firm: %s %s" % (erra, errb))
        ma, mb = tar_map(pa), tar_map(pb)
        same_members = {k: sha(v) for k, v in ma.items()} == {k: sha(v) for k, v in mb.items()}
        same_bytes = sha(pa) == sha(pb)
        notes_stats["identical_members"] += int(same_members)
        notes_stats["identical_tar_bytes"] += int(same_bytes)
        cand_sha = sha(pa)
        (scratch / (bname + ".candidate.tar.gz")).write_bytes(pa)
        print("%s: candidate built twice; identical members=%s; identical tar bytes=%s; members in tar=%d" % (
            firm, same_members, same_bytes, len(ma)))

        head = aws_json(core, ["s3api", "head-object", "--bucket", b["bucket"], "--key", b["s3_key"],
                               "--output", "json"])
        live_path = scratch / (bname + ".live.tar.gz")
        got = aws_json(core, ["s3api", "get-object", "--bucket", b["bucket"], "--key", b["s3_key"],
                              str(live_path), "--output", "json"])
        live_vid = got.get("VersionId", "")
        version_ok = live_vid == mints[firm]["after_version_id"] and head.get("VersionId", "") == live_vid
        notes_stats["version_match"] += int(version_ok)
        live = live_path.read_bytes()
        live_sha = sha(live)
        print("%s: live object read; live version equals IB-pr-549 mint record=%s" % (firm, version_ok))

        ml = tar_map(live)
        cand_map = {k: sha(v) for k, v in ma.items()}
        live_map = {k: sha(v) for k, v in ml.items()}
        names = sorted(set(cand_map) | set(live_map))
        changed = [n for n in names if cand_map.get(n) != live_map.get(n)]
        closure = set(b["members"])
        cand_closure = set(n for n in cand_map if n != SUMS)
        if cand_closure != closure:
            raise SystemExit("candidate closure differs from the declared members")

        src_pin = mints[firm]["minted_from_pin"]
        changed_members = []
        extra = {}
        for n in changed:
            if n == SUMS:
                continue
            if n not in closure:
                extra["live-only:" + n] = "live-only member, not in the candidate closure"
                continue
            repo_path = b["members"][n]["repo_path"]
            pin_bytes = git_bytes(pin_root, ["show", pin + ":" + repo_path])
            worktree_bytes = (pin_root / repo_path).read_bytes()
            notes_stats["worktree_total"] += 1
            notes_stats["worktree_eq_blob"] += int(worktree_bytes == pin_bytes)
            changed_members.append({"repo_path": repo_path, "sha256_at_pin": sha(pin_bytes)})
            if repo_path == SNAPSHOT:
                snapshot_flagged[firm] = True
                continue
            n_commits = len(git_bytes(pin_root, ["log", "--format=%H", src_pin + ".." + pin, "--", repo_path])
                            .decode().split())
            live_eq_src = None
            try:
                src_bytes = git_bytes(pin_root, ["show", src_pin + ":" + repo_path])
                live_eq_src = ml[n] == src_bytes
            except SystemExit:
                live_eq_src = None
            cl, cp = ml[n].count(b"\r\n"), pin_bytes.count(b"\r\n")
            reason = ("live bundle copy differs from this pin (live sha256 and pin sha256 differ); the file changed "
                      "in %d commits between the minting pin and this pin; live copy equals the minting pin blob=%s; "
                      "CRLF line breaks live=%d pin=%d" % (n_commits, live_eq_src, cl, cp))
            extra[repo_path] = reason
        # live-equals-source-pin arm over the whole closure (measured, not reasoned)
        for n in closure:
            repo_path = b["members"][n]["repo_path"]
            notes_stats["live_total"] += 1
            try:
                src_bytes = git_bytes(pin_root, ["show", src_pin + ":" + repo_path])
                notes_stats["live_eq_src"] += int(n in ml and ml[n] == src_bytes)
            except SystemExit:
                pass

        sums_cand = parse_sums(ma[SUMS]) if SUMS in ma else {}
        sums_live = parse_sums(ml[SUMS]) if SUMS in ml else {}
        sums_diff = sorted(k for k in set(sums_cand) | set(sums_live) if sums_cand.get(k) != sums_live.get(k))
        consistent = sums_diff == sorted(k for k in changed if k in closure and k != SUMS)
        notes_stats["sums_consistent"] += int(consistent)
        print("%s: changed members=%d (closure %d); SHA256SUMS line diff=%d; SHA256SUMS diff equals changed closure=%s" % (
            firm, len(changed), len(changed_members) + sum(1 for n in changed if n in closure and n == SUMS),
            len(sums_diff), consistent))
        if extra:
            extra_total += len(extra)

        firms_out[firm] = {
            "live_bundle_sha256": live_sha,
            "candidate_bundle_sha256": cand_sha,
            "members_total": len(b["members"]),
            "changed_members": changed_members,
            "extra_changed_reasons": {k: v for k, v in extra.items() if not k.startswith("live-only:")},
        }
        if any(k.startswith("live-only:") for k in extra):
            firms_out[firm]["extra_changed_reasons"].update(
                {k.split(":", 1)[1]: v for k, v in extra.items() if k.startswith("live-only:")})
        print("%s: extra changed members named with reasons=%d; holdings_snapshot among changed=%s" % (
            firm, len(firms_out[firm]["extra_changed_reasons"]), snapshot_flagged.get(firm, False)))

    stats = notes_stats
    notes = [
        "Pin and blob: the pin is the base HEAD; holdings_snapshot.py at the pin carries ABSENT-AT-SOURCE A, B and C "
        "blocks (line counts A=%d B=%d C=%d) and the blob is read by git rev-parse, not inferred." % (
            absent["A"], absent["B"], absent["C"]),
        "Builds: each firm candidate was built twice in process; identical member names and sha256 in %d of %d firms; "
        "tarball bytes identical across the two arms in %d of %d firms; the member hashes are the identity the order "
        "names and they agree in both arms. members_total is the closure count, the member-count the bundle stamps; each "
        "tarball also holds SHA256SUMS, so it has one more entry." % (stats["identical_members"], len(bundles),
                                                                       stats["identical_tar_bytes"], len(bundles)),
        "Live: each live bundle was read read-only; its live version id equals the IB-pr-549 mint record "
        "after_version_id in %d of %d firms. The IB-pr-549 record states after_sha256_equals_built as true but does not "
        "state a sha256 value, so live_bundle_sha256 is measured and not compared with a stated value (a surprise row "
        "is filed for the gap)." % (stats["version_match"], len(bundles)),
        "Sparse checkout: the base worktree gained data/assets/scripts/gold/investor_reporting/ locally and it is not "
        "committed. The pin worktree first inherited core.sparseCheckout from the shared repository config, so its "
        "closure was missing; sparse checkout was disabled in the pin worktree alone (its own config.worktree) before the "
        "run, and the pin is a full detached checkout outside the repository. The harness imports safe_deploy_core only.",
        "Counters: functions_invoked is 0 because no Lambda was invoked; build_bundle_payload is the local builder "
        "function the order names and was called in process. No sign-in, no AWS write, no figure written, no vendor "
        "request. The surprise rows filed under the channel are the only writes.",
        "SHA256SUMS is the manifest member generated inside each bundle, not a repository member; it is excluded from "
        "changed_members and it differs whenever a closure member differs (SHA256SUMS line-diff consistent with the "
        "changed closure members in %d of %d firms)." % (stats["sums_consistent"], len(bundles)),
        "Worktree versus blob: the builder reads worktree bytes; for the changed closure members the pin worktree bytes "
        "equal the git blob in %d of %d checks, so sha256_at_pin is the blob sha256 and the candidate uses worktree "
        "bytes; the two are reconciled by this count." % (stats["worktree_eq_blob"], stats["worktree_total"]),
        "Live versus minting pin: across the closure, the live member bytes equal the minting pin blob in %d of %d "
        "checks, which measures the live bundle's content source directly." % (stats["live_eq_src"], stats["live_total"]),
    ]
    record = {
        "pin": pin,
        "holdings_snapshot_blob": blob,
        "firms": firms_out,
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
    out.write_text(json.dumps(record, indent=1, sort_keys=False) + "\n", encoding="utf-8")
    print("record written: firms=%d; notes=%d; extra reasons total=%d; generated %s" % (
        len(firms_out), len(notes), extra_total, datetime.datetime.now(datetime.timezone.utc).strftime("%FT%TZ")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
