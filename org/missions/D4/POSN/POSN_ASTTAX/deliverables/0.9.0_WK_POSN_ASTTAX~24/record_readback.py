#!/usr/bin/env python3
"""RECORD_READBACK -- POSN_ASTTAX.TO-W1-1, criterion W1-AC14 (re-cut).

MEASURES the deploy record made by cell AT6-s-1. It WRITES NOTHING, deploys
nothing and re-records nothing: every limb is a read of a file already
committed on this worker's branch (a031c56c74, 9633bb9e7e, 3c5c3bba93).

Limb 1  the lambda source map's entry for cot-satellites-characteristics-producer:
        its deployed code sha256 (must EQUAL W1-AC10's LIVE CodeSha256) and its
        recorded commit. The key path read is NAMED, not implied.
Limb 2  the cot-pipeline CHANGELOG's HEAD entry: deployed_commit_short,
        functions_updated (exactly the one function) and deployed_at.
Limb 3  the CHANGELOG file's non-ASCII count, len(b) - len(b.decode('utf-8'))
        -- 0 on a pure-ASCII file; compared against the count this cell
        recorded on both sides of its hand-written entry.

Every limb prints its DENOMINATOR beside its number and its own EQUAL /
NOT-EQUAL verdict, so a wrong value cannot read as a pass.
"""

import json
import subprocess
import sys
from pathlib import Path

# --- what the record must agree with (all measured earlier in this cell) ---
FUNCTION = "cot-satellites-characteristics-producer"
EXPECT_CODE_SHA256 = "rN/jcmeQk4F/HJsQHfasjdWFgIjWXOrYHeBPkf5TbOU="  # W1-AC10, LIVE plane
EXPECT_COMMIT_SHORT = "2a62019b"                                    # the cell's code commit
EXPECT_NONASCII_CHANGELOG = 18                                      # printed BEFORE and AFTER the hand-written entry

SOURCE_MAP_REL = "infra/aws/lambda/ci/lambda-source-map.json"
CHANGELOG_REL = "infra/aws/terraform/cot-pipeline/CHANGELOG.json"

# the helper's 10-key shape (record-terraform-deploy.sh:600-700)
HELPER_SHAPE = [
    "version", "deployed_at", "deployed_commit", "deployed_commit_short",
    "previous_commit", "branch", "agent", "functions_updated", "commits",
    "artifacts",
]


def resolve_root():
    """Derive the workspace root -- never hardcode a device path (NEVER#7)."""
    here = Path(__file__).resolve().parent
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(here), capture_output=True, text=True, timeout=30,
        )
        if out.returncode == 0 and out.stdout.strip():
            cand = Path(out.stdout.strip())
            if (cand / SOURCE_MAP_REL).is_file():
                return cand, "git rev-parse --show-toplevel (cwd = this script's dir)"
    except Exception as exc:  # noqa: BLE001 -- resolver falls through, loudly
        print("WARN: git resolver unavailable: %s" % exc)
    for cand in list(here.parents) + [Path.cwd()]:
        if (cand / SOURCE_MAP_REL).is_file():
            return cand, "parent walk from this script's dir"
    print("ERROR: workspace root not resolvable from %s" % here)
    sys.exit(2)


def nonascii_count(path):
    """len(b) - len(b.decode('utf-8')) -- 0 iff the file is pure ASCII."""
    b = path.read_bytes()
    return len(b) - len(b.decode("utf-8")), len(b)


def verdict(ok):
    return "EQUAL" if ok else "NOT-EQUAL"


def main():
    root, how = resolve_root()
    print("=" * 78)
    print("RECORD READBACK -- POSN_ASTTAX.TO-W1-1 / W1-AC14 (re-cut)")
    print("  MEASURES the record. Writes nothing, deploys nothing, re-records nothing.")
    print("  workspace root: %s" % root)
    print("  resolver: %s" % how)
    print("=" * 78)

    ok = []

    # ------------------------------------------------------------------ limb 1
    sm_path = root / SOURCE_MAP_REL
    sm = json.loads(sm_path.read_text(encoding="utf-8"))
    funcs = sm.get("functions", {})
    print("")
    print("LIMB 1 -- THE LAMBDA SOURCE MAP")
    print("  file        : %s" % SOURCE_MAP_REL)
    print("  KEY PATH READ: $.functions[%r]" % FUNCTION)
    print("  denominator : %d function(s) in the map; 1 of 1 read" % len(funcs))
    if FUNCTION not in funcs:
        print("  ERROR: %s ABSENT from the map -- the record is NOT there" % FUNCTION)
        ok.append(False)
    else:
        e = funcs[FUNCTION]
        got_sha = e.get("deployed_code_sha256")
        got_commit = e.get("last_deployed_commit")
        sha_ok = got_sha == EXPECT_CODE_SHA256
        print("  deployed_code_sha256 (recorded) : %s" % got_sha)
        print("  W1-AC10 live CodeSha256 (expect): %s" % EXPECT_CODE_SHA256)
        print("  VERDICT sha256                  : %s" % verdict(sha_ok))
        print("  last_deployed_commit  : %s" % got_commit)
        short_ok = bool(got_commit) and got_commit.startswith(EXPECT_COMMIT_SHORT)
        print("  starts with %s          : %s" % (EXPECT_COMMIT_SHORT, short_ok))
        print("  last_deployed_at      : %s" % e.get("last_deployed_at"))
        print("  recorded_by           : %s" % e.get("recorded_by"))
        print("  deploy_ledger         : %s" % e.get("deploy_ledger"))
        print("  tf_resource           : %s" % e.get("tf_resource"))
        print("  iam_role              : %s" % e.get("iam_role"))
        print("  $._last_deploy_recorded: %s" % sm.get("_last_deploy_recorded"))
        ok.append(sha_ok and short_ok)
    sm_na, sm_bytes = nonascii_count(sm_path)
    print("  source map non-ASCII count: %d (of %d bytes; 0 == pure ASCII)" % (sm_na, sm_bytes))

    # ------------------------------------------------------------------ limb 2
    cl_path = root / CHANGELOG_REL
    cl = json.loads(cl_path.read_text(encoding="utf-8"))
    entries = cl.get("entries", [])
    print("")
    print("LIMB 2 -- THE cot-pipeline CHANGELOG, HEAD ENTRY")
    print("  file        : %s" % CHANGELOG_REL)
    print("  KEY PATH READ: $.entries[0]")
    print("  denominator : %d entr(ies); the HEAD one read (1 of %d)" % (len(entries), len(entries)))
    if not entries:
        print("  ERROR: no entries -- nothing recorded")
        ok.append(False)
    else:
        h = entries[0]
        short = h.get("deployed_commit_short")
        fns = h.get("functions_updated", [])
        short_ok = short == EXPECT_COMMIT_SHORT
        fns_ok = fns == [FUNCTION]
        print("  deployed_at            : %s" % h.get("deployed_at"))
        print("  deployed_commit_short  : %s   (expect %s) -> %s"
              % (short, EXPECT_COMMIT_SHORT, verdict(short_ok)))
        print("  deployed_commit        : %s" % h.get("deployed_commit"))
        print("  previous_commit        : %s" % h.get("previous_commit"))
        print("  branch                 : %s" % h.get("branch"))
        print("  agent                  : %s" % h.get("agent"))
        print("  functions_updated      : %s" % json.dumps(fns))
        print("  EXACTLY the one function: %s (%d of %d entr(y|ies) in the list)"
              % (fns_ok, len(fns), len(fns)))
        present = [k for k in HELPER_SHAPE if k in h]
        extra = [k for k in h if k not in HELPER_SHAPE]
        print("  helper shape           : %d of %d keys present; %d unexpected key(s) %s"
              % (len(present), len(HELPER_SHAPE), len(extra), extra))
        arts = h.get("artifacts", [])
        for a in arts:
            print("  artifact               : %s -> sha256 %s  (matches W1-AC10: %s)"
                  % (a.get("function"), a.get("sha256"),
                     a.get("sha256") == EXPECT_CODE_SHA256))
        ok.append(short_ok and fns_ok and len(present) == len(HELPER_SHAPE))

    # ------------------------------------------------------------------ limb 3
    cl_na, cl_bytes = nonascii_count(cl_path)
    na_ok = cl_na == EXPECT_NONASCII_CHANGELOG
    print("")
    print("LIMB 3 -- THE CHANGELOG'S NON-ASCII COUNT (the silent-corruption detector)")
    print("  detector   : len(b) - len(b.decode('utf-8'))")
    print("  file bytes : %d" % cl_bytes)
    print("  count NOW  : %d" % cl_na)
    print("  recorded by this cell BEFORE and AFTER its hand-written entry: %d"
          % EXPECT_NONASCII_CHANGELOG)
    print("  VERDICT    : %s (unchanged by this cell)" % verdict(na_ok))
    ok.append(na_ok)

    # ------------------------------------------------------------------ summary
    print("")
    print("=" * 78)
    print("SUMMARY: %d of %d limbs agree with the record this cell made." % (sum(ok), len(ok)))
    print("=" * 78)
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
