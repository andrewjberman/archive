"""IB-pr-597 harness (0.9.0_WK_IRPT_BCKEND~435; ASCII; derived from the IB-pr-585 harness in deliverables/0.9.0_WK_IRPT_BCKEND~427).
Run from the worktree root, with a scratch directory OUTSIDE the repository:
    python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~435/irpt435_perf_candidate_harness.py <scratch_dir_windows_path>
Steps: (1) read the live CodeSha256 of irpt-holdings-performance-lambda (get-function-configuration, read-only) and download the live
zip (get-function, read-only), check its sha256; (2) write the candidate source map with make_candidate_map_perf.py (the real
lambda-source-map.json is not edited); (3) BUILD ONLY twice with BAU_SOURCE_MAP_OVERRIDE (nothing uploaded, deployed or invoked) and
check the two zips are byte-identical; (4) compare the candidate zip members with the live zip member by member; (5) measure the
two members at the base pin; (6) write IB230-1_perf_candidate.json next to this file. Prints names, counts and hashes only.
Exit 2 = a STOP condition (live CodeSha256 is not the expected one, or the two candidate builds differ); nothing is written then."""
import base64
import datetime
import hashlib
import json
import os
import subprocess
import sys
import zipfile

FN = "irpt-holdings-performance-lambda"
EXPECTED_LIVE = "o9UugRAVhYmF3Q2ULtU6eaaNiLFRAFWW4tjjQPyj2Ok="
PREVIOUS_CANDIDATE = "fvmE5j1hkNA16csMEtB3/WydmovkAucF/AmBxLCIqEg="
MEMBERS = {
    "holdings_performance.py": "data/assets/scripts/gold/irpt_holdings_performance/holdings_performance.py",
    "sources.json": "data/assets/scripts/gold/irpt_holdings_performance/sources.json",
}
SIBLINGS = ["irpt-inf-holdings-performance-lambda", "irpt-cot-holdings-performance-lambda"]
HERE = os.path.dirname(os.path.abspath(__file__))
SERIAL = "0.9.0_WK_IRPT_BCKEND~435"


def sh(args, **kw):
    return subprocess.run(args, capture_output=True, **kw)


def posix(p):
    p = p.replace("\\", "/")
    if len(p) > 2 and p[1] == ":":
        p = "/" + p[0].lower() + p[2:]
    return p


def members(path):
    out = {}
    with zipfile.ZipFile(path) as z:
        for i in z.infolist():
            if not i.is_dir():
                out[i.filename] = hashlib.sha256(z.read(i)).hexdigest()
    return out


def zip_b64(path):
    return base64.b64encode(hashlib.sha256(open(path, "rb").read()).digest()).decode()


def main():
    scratch = sys.argv[1]
    os.makedirs(os.path.join(scratch, "tmp"), exist_ok=True)
    env = dict(os.environ, OPAL_AGENT_SERIAL=SERIAL)
    base = sh(["git", "rev-parse", "HEAD"], env=env).stdout.decode().strip()
    print("base_commit: %s" % base)

    # (1) live identity, read-only
    cfg = sh(["bash", ".tools/aws", "lambda", "get-function-configuration", "--function-name", FN,
              "--query", "CodeSha256", "--output", "text"], env=env)
    live_sha = cfg.stdout.decode().strip()
    print("live CodeSha256 rc=%d matches_expected=%s" % (cfg.returncode, live_sha == EXPECTED_LIVE))
    if live_sha != EXPECTED_LIVE:
        print("STOP: live CodeSha256 is not the expected value")
        return 2
    loc = sh(["bash", ".tools/aws", "lambda", "get-function", "--function-name", FN,
              "--query", "Code.Location", "--output", "text"], env=env).stdout.decode().strip()
    live_zip = os.path.join(scratch, "live.zip")
    dl = sh(["curl", "-sS", "-o", live_zip, loc])
    if dl.returncode or zip_b64(live_zip) != EXPECTED_LIVE:
        print("STOP: downloaded live zip does not match the live CodeSha256")
        return 2
    print("live zip OK bytes=%d sha256-b64 matches CodeSha256" % os.path.getsize(live_zip))

    # (2) candidate map
    cmap = os.path.join(scratch, "candidate_map.json")
    rep = os.path.join(scratch, "repins.json")
    w = sh([sys.executable, os.path.join(HERE, "make_candidate_map_perf.py"), base, cmap, rep], env=env)
    print(w.stdout.decode().strip())
    if w.returncode:
        print("STOP: candidate map writer rc=%d" % w.returncode)
        return 2

    # (3) BUILD ONLY twice
    tmp = os.path.join(scratch, "tmp")
    built = []
    for n in (1, 2):
        benv = dict(env, BUILD_ONLY="1", BAU_SOURCE_MAP_OVERRIDE=posix(cmap), TMPDIR=posix(tmp))
        b = sh(["bash", "infra/aws/lambda/ci/build-and-upload.sh", "investor-reporting", FN], env=benv)
        line = [x for x in b.stdout.decode(errors="replace").splitlines() if x.startswith("BUILD_ONLY:")]
        print("build %d rc=%d %s" % (n, b.returncode, line[-1].split(" key=")[0].split(" sha256=")[1] if line else "NO BUILD_ONLY LINE"))
        src = os.path.join(tmp, "lambda-artifact-%s.zip" % FN)
        if b.returncode or not line or not os.path.exists(src):
            print("STOP: build %d failed" % n)
            return 2
        dst = os.path.join(scratch, "cand_build%d.zip" % n)
        open(dst, "wb").write(open(src, "rb").read())
        built.append((dst, line[-1].split(" sha256=")[1].split(" key=")[0]))
    if open(built[0][0], "rb").read() != open(built[1][0], "rb").read():
        print("STOP: the two candidate zips are not byte-identical")
        return 2
    cand_b64 = built[0][1]
    if zip_b64(built[0][0]) != cand_b64 or cand_b64 == EXPECTED_LIVE:
        print("STOP: candidate digest inconsistent or equal to live")
        return 2
    print("candidate zips byte-identical; candidate sha256-b64 differs from live: %s" % (cand_b64 != EXPECTED_LIVE))
    print("candidate sha256-b64 differs from previous candidate (IB-pr-585): %s" % (cand_b64 != PREVIOUS_CANDIDATE))

    # (4) member comparison
    lm = members(live_zip)
    cm = members(built[0][0])
    names = sorted(set(lm) | set(cm))
    moved = [n for n in names if lm.get(n) != cm.get(n)]
    added = [n for n in moved if n not in lm]
    removed = [n for n in moved if n not in cm]
    print("live members=%d candidate members=%d moved=%d added=%d removed=%d" % (len(lm), len(cm), len(moved), len(added), len(removed)))
    target = set(MEMBERS.values())
    missing_targets = sorted(t for t in target if t not in moved)
    extra = sorted(n for n in moved if n not in target)
    print("both split members moved: %s" % (not missing_targets))
    print("extra moved members (need a reason each): %d" % len(extra))
    for n in extra:
        print("  EXTRA " + n)
    if missing_targets:
        print("STOP: a split member did not move")
        return 2

    # (5) members at the base pin
    mem = {}
    for key, rp in MEMBERS.items():
        blob = sh(["git", "show", "%s:%s" % (base, rp)], env=env).stdout
        ent = {"repo_path": rp, "pin": base, "sha256_now": hashlib.sha256(blob).hexdigest()}
        text = blob.decode("utf-8", errors="replace")
        if key == "holdings_performance.py":
            lines = text.splitlines()
            ent["split_blocks_a"] = sum(1 for x in lines if "BEGIN SPLIT-ADJUST-A" in x)
            ent["split_blocks_b"] = sum(1 for x in lines if "BEGIN SPLIT-ADJUST-B" in x)
            ent["split_blocks_c"] = sum(1 for x in lines if "BEGIN SPLIT-ADJUST-C" in x)
        else:
            d = json.loads(text)
            ent["split_adjust_declared"] = any(isinstance(v, dict) and "split_adjust" in v for v in d.values())
        mem[key] = ent
        print("member %s: %s" % (key, json.dumps({k: v for k, v in ent.items() if k != "repo_path"})))

    # (6) record
    rec = {
        "function": FN,
        "live_codesha256": live_sha,
        "override_map_used": True,
        "candidate": {"codesha256": cand_b64, "moved_count": len(moved), "total_members": len(cm),
                      "moved_members": moved},
        "members": mem,
        "siblings_unmoved": SIBLINGS,
        "extra_moved_reasons": {},
        "previous_candidate_codesha256": PREVIOUS_CANDIDATE,
        "base_commit": base,
        "read_date": datetime.datetime.now(datetime.timezone.utc).date().isoformat(),
        "method": ("Ran from the worktree at the base commit, in order: get-function-configuration for CodeSha256 (equal to the "
                   "expected live value); get-function for the live zip (read-only) and sha256 check against that value; "
                   "make_candidate_map_perf.py wrote a candidate source map re-pinning only the two split member rows of the "
                   "holdings function to the base commit; build-and-upload.sh with BUILD_ONLY=1 ran twice with "
                   "BAU_SOURCE_MAP_OVERRIDE pointing at that map; the two zips were compared byte for byte; the members were "
                   "compared by name and sha256 against the live zip; split markers were counted at the base pin."),
        "claim": "measured",
        "notes": [
            "Live identity: CodeSha256 read by get-function-configuration equals the expected value and the downloaded zip hashes to it; the zip is in scratch outside the repository.",
            "Not read or called: no put, delete, copy, invoke, publish, sign-in or vendor request; the two sibling functions were named and not built or downloaded, so siblings_unmoved is a claim from the map, not a measurement.",
            "Sparse directories added locally, never committed: data/assets/scripts/gold/irpt_holdings_performance, data/assets/scripts/silver, data/mdpf/scripts/gold, data/mdpf/scripts/silver, infra/aws/lambda/ci, infra/aws/lambda/investor-reporting, infra/aws/lambda/v2_portal/_shared, docs/contracts/investor-reporting, lib.",
            "The new candidate differs from the previous one (IB-pr-585) because the base now carries the SPLIT-ADJUST-C blocks of IB-pr-592 in holdings_performance.py, counted in split_blocks_c of that member; the difference in digest is measured, the cause is read from the block count.",
        ],
        "functions_invoked": 0,
        "sign_ins_made": 0,
        "aws_writes_made": 0,
        "rows_written": 0,
        "figures_written": 0,
        "vendor_requests_sent": 0,
    }
    out = os.path.join(HERE, "IB230-1_perf_candidate.json")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, indent=2) + "\n")
    print("record written: %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
