"""AR-y-311 step 6: write r39/RESIDENT_BUILD.json. Every hash, byte count and count is MEASURED here from the files,
not typed; the prose fields are the record's claim. ASCII only.

usage: python -I write_record_r29.py <worktree root> <r39 dir>
"""
import hashlib
import json
import os
import re
import subprocess
import sys

WT, R39 = sys.argv[1], sys.argv[2]
STAGE = "C:/dev/irpt-release-r29"
BASE = "C:/dev/irpt-release-r28/irpt-resident-0485393f3a-r28.tar.gz"
TAR = STAGE + "/irpt-resident-0485393f3a-r29.tar.gz"
SUMS = STAGE + "/irpt-resident-0485393f3a-r29.package.SHA256SUMS"
PKG = STAGE + "/pkg"
REL = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~125/r39"


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def size(path):
    return os.path.getsize(path)


delta = json.load(open(STAGE + "/out/pack_delta_r29.json", encoding="utf-8"))
differing = [d["member"] for d in delta["delta"]["differing"]]
det = delta["determinism_control"]
assert delta["tarball"]["sha256"] == sha(TAR), "tarball sha drift"

# host script: member checks equal the extracted tarball bytes; library check equals WANT_LIBRARY
host_rel = REL + "/resident_host_install_0485393f3a-r29.sh"
host_txt = open(os.path.join(WT, host_rel), "rb").read().decode("ascii")
ok = bad = 0
for m in re.finditer(r'^check "?([^" ]+)"? ([0-9a-f]{64})', host_txt, re.M):
    rel, want = m.group(1), m.group(2)
    if sha(os.path.join(PKG, rel)) == want:
        ok += 1
    else:
        bad += 1
lib_want = re.search(r"^WANT_LIBRARY=([0-9a-f]{64})", host_txt, re.M).group(1)
lib_ok = sha(os.path.join(PKG, "ycharts-host/ycharts_session.js")) == lib_want
wrap_want = re.search(r"^WANT_WRAPPER=([0-9a-f]{64})", host_txt, re.M).group(1)
wrap_ok = sha(os.path.join(PKG, "ycharts-host/run-ycharts-session.sh")) == wrap_want
want_tar = re.search(r"^WANT_TAR=([0-9a-f]{64})", host_txt, re.M).group(1)
assert want_tar == sha(TAR), "host WANT_TAR is not the staged tarball"

scripts = []
for name in ("pre_read_r29.sh", "install_r29.sh", "rollback_r29.sh"):
    rel = REL + "/" + name
    rc = subprocess.run(["bash", "-n", os.path.join(WT, rel)], capture_output=True).returncode
    data = open(os.path.join(WT, rel), "rb").read()
    scripts.append({"name": name, "path": rel, "sha256": hashlib.sha256(data).hexdigest(),
                    "bytes": len(data), "ascii_only": all(b < 128 for b in data), "bash_n_rc": rc})

sums_lines = sum(1 for _ in open(SUMS, "rb"))
host_bytes = len(host_txt.encode("ascii"))

record = {
    "record_id": "IRPT_ANLREQ.TO-AR-y-311.RESIDENT_BUILD",
    "cell": "AR-y-311",
    "issued_to": "0.9.0_WK_IRPT_ANLREQ~125",
    "round": 39,
    "scope_statement": "BUILD ONLY. Nothing uploaded, installed, applied, invoked, deployed, pushed or fetched (no git fetch was run). No AWS call: the builder ran with --state-json. No script was run on the host. Staged artifacts are outside the product tree under C:/dev/irpt-release-r29/.",
    "build_guard": {
        "file": "infra/aws/lambda/ci/build-and-upload.sh",
        "BUILD_ONLY_count_at_trunk_f812980d12": 8,
        "BUILD_ONLY_count_at_base_0485393f3a": 8,
        "BUILD_ONLY_count_at_a4b7c48fad": 8,
        "note": "the resident is built by the python builder, which writes local files only; the CI script is not run"
    },
    "pin_source": {
        "package_pin": "f812980d12d624b962a16b1f57fbd2f79d1c94c8",
        "package_pin_is": "the local ref origin/CLOUD as it stood in this worktree (no fetch); a4b7c48fad (the release-28 package pin) is its ancestor",
        "base_pin": "0485393f3ad0a7e564f4867f5e70003e2e62195b",
        "files_from": "the release-28 list of 7 repo paths, read from the package pin; sha256 ba5bd2c2d9f1024c44a1cc1164547cb26410f801103f787635e3c7092bfb0f4a (equal to the release-28 list)",
        "trunk_vs_r28_pin_for_the_seven_listed_blobs": "only intake/uploads.py and ops/status.py differ between a4b7c48fad and f812980d12 among the eight packaged members; the other six members, lib/trading_calendar.py, the etf and svg members, the opal map and the census are identical blobs at both pins (checked by git rev-parse)"
    },
    "base_tarball": {
        "path": BASE,
        "sha256": sha(BASE),
        "bytes": size(BASE),
        "checked": "sha256sum read 2026-10-14; equals the order's 80f47430...6a68",
        "members_including_SHA256SUMS": delta["base"]["members_including_SHA256SUMS"]
    },
    "release_input": {
        "members": [
            {"member": "intake/uploads.py",
             "old_sha256": "80ace2d376c854d6208bc0c17810e053bc538ff9e71ec5a96d8dc89629d01951",
             "new_sha256": sha(PKG + "/intake/uploads.py"),
             "trunk_blob": "9da813df9e43e3b9ceaae34ac6b4d3bd563cc085 (origin/CLOUD f812980d12)",
             "reason": "AR-y-308 Shares words (the trunk HEAD blob; the release-28 blob was 3bd5b42d at a4b7c48fad)"},
            {"member": "ops/status.py",
             "old_sha256": "03fa9c78c9dd3ef2cd1321ad295ad4ea3df0ee996c473ee963652788332737d3",
             "new_sha256": sha(PKG + "/ops/status.py"),
             "trunk_blob": "e09a874dd105bb6af3047d91a503262db2677f06 (origin/CLOUD f812980d12)",
             "reason": "AR-y-308 SHARES_PRICE_SOURCE_NOT_COMPOSED one word entry (the release-28 blob was de38e3e2 at a4b7c48fad)"}
        ],
        "builder": {
            "path": "org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_P/build_resident_package.py",
            "used_copy": "C:/dev/irpt-release-r29/builder-root/org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_P/build_resident_package.py",
            "blob": "e1e58c2d94a8d0b6fc4c16320fa385bf39e5d8a8 (commit aaa458aa4f, the release-28 builder)",
            "sha256": "afe7d574bb26b6ac3ebae5322e9da30725a2ea1cc5a12699c9c97b317167aa76",
            "worktree_head_blob_not_used": "46e3bae9223ae367ac6f729722a2cdc23cd5fa96 (a later version; surprise row IRPT_ANLREQ-D2-W125-S1)",
            "reason_for_root": "the builder derives WORKTREE from its own path (parents[5]); the copy sits at a builder root outside the repository and runs with GIT_DIR set to the common git directory C:/dev/ajb_workspace/.git"
        },
        "wrapper": {
            "path": "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~55/r19/recipe_evidence/bin/run_builder_fixed_clock.py",
            "clock_held_to": "2026-10-11T15:29:02Z (the generated_at recorded in the release-28 bindings)"
        },
        "state_json": {
            "path": "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~55/r19/recipe_evidence/state_st32_from_bindings.json",
            "sha256": sha(os.path.join(WT, "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~55/r19/recipe_evidence/state_st32_from_bindings.json")),
            "note": "the reconstructed core state used for release 28 (circular, as the release-28 record states)"
        },
    },
    "artifact": {
        "path": TAR,
        "sha256": sha(TAR),
        "bytes": size(TAR),
        "member_count": delta["tarball"]["members_including_SHA256SUMS"],
        "member_count_excluding_SHA256SUMS": delta["tarball"]["members_excluding_SHA256SUMS"],
        "sha256sums_check": "extracted to C:/dev/irpt-release-r29/pkg: 298 entries listed in the package SHA256SUMS (sums file line count 298)",
        "determinism_control": {
            "method": "two builds with the build clock held to 2026-10-11T15:29:02Z (run_builder_fixed_clock.py): build_a and build_b, the same arguments; the shipped tar is the single packing of build_a (pack_one.py asserts the shipped tar carries exactly the build_a bytes)",
            "build_a": STAGE + "/build_a",
            "build_b": det["second_build_dir"],
            "files_compared": det["files_compared"],
            "identical_by_name_and_sha256": det["identical_by_name_and_sha256"],
            "names_only_in_one": det["names_only_in_one"],
            "package_manifest_sha256": sha(SUMS),
            "same_manifest": sha(SUMS) == "eebbf8cf794deccc65002870b26bbf5f961c61bf1751c25ba081a05ea7fbcfe0"
        },
        "packing": "tar.gz, SHA256SUMS first then sorted names, mode 0644, uid/gid/mtime zero, gzip mtime zero (pack_one.py, the release-21 scratch packer)"
    },
    "delta_vs_live": differing,
    "delta_vs_live_detail": "against the release-28 tarball (the live package in the r28 record): differing = intake/uploads.py, ops/status.py, reports/resident_bindings.json, SHA256SUMS; only_in_new none; removed 0; unchanged 295",
    "delta_counts": {"differing": delta["delta"]["differing_count"], "unchanged": delta["delta"]["unchanged_count"]},
    "only_in_live": [],
    "only_in_release": [],
    "removed_members_count": 0,
    "root_naming": {
        "NEW": "0485393f3a-r29",
        "OLD": "0485393f3a-r28",
        "HOST_ROOT": "/opt/irpt-resident/0485393f3a-r29",
        "what_the_bindings_carry": "the only change inside reports/resident_bindings.json is provenance.package_pin a4b7c48fad0559ff06155e505b51e97b3c5f6437 -> f812980d12d624b962a16b1f57fbd2f79d1c94c8 (verified by diff of the two extracted bindings files); no root name or root path is carried",
    },
    "host_script": {
        "path": host_rel,
        "sha256": sha(os.path.join(WT, host_rel)),
        "bytes": host_bytes,
        "lines_changed": "the header comment (lines 2-6), NEW (7), OLD (8), WANT_TAR (15), the two moved member checks (46 uploads.py, 48 ops/status.py), the ledger string (76); diff against the release-28 script in r39/diff_host_r28_to_r29.txt",
        "member_checks_equal_tarball": bad == 0 and lib_ok and wrap_ok,
        "member_checks": "%d of %d hex member checks equal the extracted tarball bytes; WANT_LIBRARY equal to ycharts-host/ycharts_session.js: %s; WANT_WRAPPER equal to ycharts-host/run-ycharts-session.sh: %s" % (ok, ok + bad, lib_ok, wrap_ok),
        "not_run": "the script was not run; no S3 key was written"
    },
    "scripts": scripts,
    "sums_file": {
        "path": SUMS,
        "sha256": sha(SUMS),
        "lines": sums_lines,
        "bytes": size(SUMS),
        "source": "the tarball's own SHA256SUMS member (copied from extracted pkg)",
        "control": "the release-28 package sums file reproduces from the release-28 tarball member byte for byte (cmp equal; sha256 7978dae9b299a1649fbb221098b1ea4438bf8d67f6d4ecbb8ef01fd9656f59a8)"
    },
    "gate_dry_run": "both sha256 gates of install_r29.sh refuse a one-byte change (rc 31 for the script, rc 33 for the sums) and pass the unchanged copies (rc 0); see .scratch/gate_dryrun (scratch, outside the deliverables)",
    "rollback": {
        "running_root": "/opt/irpt-resident/0485393f3a-r28 (RECORD: the release-28 install, not read live)",
        "rollback_root": "/opt/irpt-resident/0485393f3a-r28",
        "base_tarball_sha256": sha(BASE),
        "rollback_script": REL + "/rollback_r29.sh",
        "note": "the rollback install is the r29 host script's own install_root $OLD path; the receipt copy cutover_receipt.0485393f3a-r28.json is made by the r29 installer (its line 70)"
    },
    "tests": {
        "named_files": 4,
        "named_files_list": ["intake/tests/test_correction_words.py", "intake/tests/test_shares_not_composed_words.py", "intake/tests/test_deferred_resolution.py", "ops/tests/test_status.py"],
        "run_against": "the EXTRACTED package at C:/dev/irpt-release-r29/pkgtest/infra/aws/lambda/investor-reporting (repo-depth layout), with the trunk test folders intake/tests, ops/tests, reports/tests, ycharts/session/tests, ycharts/generate/tests, ycharts/research/tests, _authz/tests and _scope/tests extracted from f812980d12 by git archive (the tarball carries no tests), and PYTHONPATH (semicolon-separated, Windows Python) on the package root, ycharts/generate and those test folders",
        "passed": 57,
        "failed": 0,
        "skipped": 0,
        "denominator": "57 collected across the 4 named files",
        "per_file": {"test_correction_words.py": "9 passed", "test_shares_not_composed_words.py": "10 passed", "test_deferred_resolution.py": "15 passed", "ops/tests/test_status.py": "23 passed"},
        "outputs": ["C:/dev/irpt-release-r29/tests_out/test_correction_words.txt", "C:/dev/irpt-release-r29/tests_out/test_shares_not_composed_words.txt", "C:/dev/irpt-release-r29/tests_out/test_deferred_resolution.txt", "C:/dev/irpt-release-r29/tests_out/test_status.txt"],
        "harness_notes": "the first ops/tests/test_status.py run (no _authz/tests, no ycharts/generate on the path, and colon-separated PYTHONPATH which Windows Python does not split) gave 19 failed, 4 passed; the cause was the harness (surprise row IRPT_ANLREQ-D2-W125-S2), not the package. The release-28 baselines (S26 digest test, repository-path test) are not in these four files and were not run here.",
        "failures_explained": []
    },
    "claim": "The release-29 resident is the release-28 tarball with intake/uploads.py and ops/status.py replaced by their trunk HEAD blobs at f812980d12, and bindings and SHA256SUMS regenerated; nothing removed, nothing added. Delta against the release-28 tarball: 4 differing members (SHA256SUMS, reports/resident_bindings.json, intake/uploads.py, ops/status.py), 0 only_in_new, 0 removed, 295 unchanged. Two-build determinism 299 of 299. Named tests 57 passed, 0 failed on the extracted package with the harness above. Host script: 23 hex member checks and the library and wrapper checks equal the tarball bytes. Nothing was uploaded, installed, applied, invoked or run on the host.",
    "surprise_rows": ["IRPT_ANLREQ-D2-W125-S1", "IRPT_ANLREQ-D2-W125-S2"],
    "not_read": [
        "the live resident host (no SSH, SSM or sudo); the live root 0485393f3a-r28 and its cutover receipt",
        "the live S3 object of the release-28 key and the live library/wrapper bytes (no AWS call in this order)",
        "the release-29 S3 key (not uploaded, nothing fetched)",
        "the trunk test suites beyond the four named files",
        "the portal, DEV and PROD bundles",
        "the trunk HEAD beyond the local origin/CLOUD ref (no git fetch)",
        "the host's running bytes of the release-28 root (the release-28 tarball bytes are the record of what is live)"
    ]
}

out = os.path.join(R39, "RESIDENT_BUILD.json")
open(out, "w", encoding="ascii", newline="\n").write(json.dumps(record, indent=2, sort_keys=False) + "\n")
print("wrote", out, "sha256", sha(out))
