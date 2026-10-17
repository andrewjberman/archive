"""IRPT_ANLREQ AR-g-158 check (issuer 2.0.0_SA_COO~G2): verify a release-34k BUILD (two code members changed, two added, the bindings' provenance) without trusting its record. Run from the repository root.

    python ar_g160_checks.py verify <stage folder> <RESIDENT_R34K_BUILD.json> [<expected tarball sha256>]

Everything is recomputed from the staged tarball, the r34h tarball and the git objects at the recorded pin: the artifact hash, the delta against r34h
(it must be exactly the expected sets), every changed or added member against `git show <pin>:<path>`, every unchanged member against r34h, the
bindings (the three added keys, the pins verified by the installer's own loader), the producer list, the two builds, the four host scripts
(ASCII, `bash -n`, the pins, the fail-closed guards, one member check per changed or added member) and the two sha256 gates. Prints one RESULT
line: AR-G160-OK ... or AR-G160-FAIL <why>; rc 0 only on OK. ASCII only. It reads no network and writes nothing but a temp folder.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

BASE_TAR = "C:/dev/irpt-release-r34r/irpt-resident-0485393f3a-r34h.tar.gz"  # the r34h tarball: the root that runs when the r34k install starts
BASE_TAR_SHA = "60cc8d1d68627c993121df7eca946a40046f1d7f63ddfd2968f83e27077b93c0"
IR = "infra/aws/lambda/investor-reporting/"
MAPS = "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps/"
POOL_SRC = "org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34/swap_pool.json"
CHANGED = sorted(["SHA256SUMS", "reports/resident_bindings.json", "intake/yfinance_check.py", "ycharts/research/price_adapter_ycharts.py", "ycharts/generate/resident_main.py"])
ADDED = ["ycharts/research/price_form_ycharts.py", "ycharts/research/ycharts_client.py"]
ESTATE_CLIENT = "infra/aws/lambda/ycharts-market-data-pull/ycharts_client.py"  # added from outside the investor-reporting tree, at the pin
FROM_MAP = {"ycharts/research/ycharts_client.py": ESTATE_CLIENT, "ycharts/research/overview_map.json": MAPS + "overview_map.json", "ycharts/research/comparison_map.json": MAPS + "comparison_map.json",
            "ycharts/research/multi_map.json": MAPS + "multi_map.json", "lib/trading_calendar.py": "lib/trading_calendar.py",
            "ycharts/research/etf_classifications_dynamodb.py": "infra/aws/lambda/v2_portal/_shared/etf_classifications_dynamodb.py",
            "ycharts/research/swap_pool.json": POOL_SRC}
ADDRESS = '("andrew@opalinvest.com", "fwd1-staff-r41b@opal.invalid")'
JWT = re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")
TOKEN_MEMBER = re.compile(r'"token"\s*:')


def fail(why):
    print("AR-G160-FAIL %s" % why)
    sys.exit(1)


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    with open(path, "rb") as fh:
        return sha_bytes(fh.read())


def walk(root):
    out = {}
    for dp, _dn, fn in os.walk(root):
        for f in fn:
            p = os.path.join(dp, f)
            out[os.path.relpath(p, root).replace(os.sep, "/")] = sha_file(p)
    return out


def git_show(pin, path):
    out = subprocess.run(["git", "show", "%s:%s" % (pin, path)], capture_output=True)
    if out.returncode != 0:
        fail("git show %s:%s failed" % (pin[:10], path))
    return out.stdout


def main(stage, record_path, want_tar=None):
    stage = stage.replace("\\", "/")
    rec = json.load(open(record_path, encoding="utf-8"))
    pin = rec["release_input"]["pin_full_sha"]
    tar_path = rec["artifact"]["path"]
    if not tar_path.startswith(stage + "/") or os.path.abspath(stage).startswith(os.path.abspath(".")):
        fail("the artifact is not inside the stage folder, or the stage folder is inside the repository")
    # 1. the artifact
    if sha_file(tar_path) != rec["artifact"]["sha256"] or os.path.getsize(tar_path) != rec["artifact"]["bytes"]:
        fail("the tarball's sha256 or size differs from the record")
    if sha_file(BASE_TAR) != BASE_TAR_SHA:
        fail("the r34h base tarball is not the one recorded")
    tmp = tempfile.mkdtemp(prefix="ar_g160_")
    if want_tar and sha_file(tar_path) != want_tar:
        fail("the tarball's sha256 is not the issuer's own build of the same pin (%s)" % want_tar)
    try:
        xnew, xold = tmp + "/xnew", tmp + "/xold"
        tarfile.open(tar_path).extractall(xnew)
        tarfile.open(BASE_TAR).extractall(xold)
        wnew, wold = walk(xnew), walk(xold)
        if len(wnew) != rec["artifact"]["member_count"] or len(wnew) != 317:
            fail("member count %d (record %d), want 317" % (len(wnew), rec["artifact"]["member_count"]))
        # 2. the delta is exactly the expected sets
        changed = sorted(n for n in wnew if n in wold and wnew[n] != wold[n])
        added = sorted(set(wnew) - set(wold))
        removed = sorted(set(wold) - set(wnew))
        if changed != CHANGED or added != ADDED or removed:
            fail("delta differs from the expected: changed %s added %s removed %s" % (
                sorted(set(changed) ^ set(CHANGED)), sorted(set(added) ^ set(ADDED)), removed))
        if rec["delta_vs_r34h"]["changed"] != changed or rec["delta_vs_r34h"]["added"] != added:
            fail("the record's delta lists differ from the recomputed ones")
        # 3. every member that comes from the pin equals the git blob; every other member equals r34h
        for name in changed + added:
            if name in (("SHA256SUMS"), "reports/resident_bindings.json"):
                continue
            src = FROM_MAP.get(name, IR + name)
            if sha_bytes(git_show(pin, src)) != wnew[name]:
                fail("member %s differs from git show %s:%s" % (name, pin[:10], src))
        for name in sorted(wnew):
            if name not in changed and name not in added and wnew[name] != wold[name]:
                fail("unchanged member %s differs" % name)
        # 4. the sums file covers every member and the staged copy equals the member
        sums = open(xnew + "/SHA256SUMS", encoding="utf-8").read().splitlines()
        listed = {ln.split("  ", 1)[1]: ln.split("  ", 1)[0] for ln in sums}
        if set(listed) != set(wnew) - {"SHA256SUMS"} or any(listed[n] != wnew[n] for n in listed):
            fail("SHA256SUMS does not match the members")
        if sha_file(rec["artifact"]["sha256sums_file"]["path"]) != wnew["SHA256SUMS"]:
            fail("the staged package sums file is not the tarball's SHA256SUMS member")
        # 5. the bindings
        bnew = json.load(open(xnew + "/reports/resident_bindings.json", encoding="utf-8"))
        bold = json.load(open(xold + "/reports/resident_bindings.json", encoding="utf-8"))
        if sorted(set(bnew) - set(bold)) or sorted(set(bold) - set(bnew)):
            fail("binding keys differ from r34h: added %s removed %s" % (sorted(set(bnew) - set(bold)), sorted(set(bold) - set(bnew))))
        if bnew["ycharts_window_budget"] != {"calls": 6, "window_s": 390} or bold["ycharts_window_budget"] != bnew["ycharts_window_budget"]:
            fail("ycharts_window_budget is %s -> %s (want 6 calls, 390 s, unchanged)" % (bold["ycharts_window_budget"], bnew["ycharts_window_budget"]))
        if sorted(k for k in bnew if k in bold and bnew[k] != bold[k]) != ["provenance"]:
            fail("binding keys changed: %s" % sorted(k for k in bnew if k in bold and bnew[k] != bold[k]))
        prov = sorted(k for k in set(bnew["provenance"]) | set(bold["provenance"]) if bnew["provenance"].get(k) != bold["provenance"].get(k))
        if prov != ["files_from_count", "files_from_sha256", "members_added", "package_pin"] or bnew["provenance"]["package_pin"] != pin:
            fail("provenance differs beyond package_pin and the files-from list's count and sha256 (or package_pin is not the record pin): %s" % prov)
        if bnew["provenance"]["files_from_count"] != bold["provenance"]["files_from_count"] + 2:
            fail("the files-from list should have grown by exactly two lines (price_form_ycharts.py and resident_main.py)")
        if bnew["provenance"]["members_added"] != bold["provenance"]["members_added"] + [{"packaged": "ycharts/research/ycharts_client.py", "repo_path": ESTATE_CLIENT, "sha256": wnew["ycharts/research/ycharts_client.py"]}]:
            fail("members_added is not the r34h list plus exactly the estate client at its pinned blob")
        for key, member in (("opal_map", "overview_map.json"), ("opal_map_comparison", "comparison_map.json"), ("opal_map_multicomp", "multi_map.json"),
                            ("opal_swap_pool", "swap_pool.json")):
            want = {"path": "../ycharts/research/" + member, "sha256": wnew["ycharts/research/" + member]}
            if bnew[key] != want:
                fail("binding %s is %s, want %s" % (key, bnew[key], want))
        if bnew["opal_pricing"] != {"enabled": True, "tiers": ["estate", "yfinance", "ycharts"]} or bold["opal_pricing"] != bnew["opal_pricing"]:
            fail("opal_pricing is %s -> %s (want estate, yfinance, ycharts, enabled, in both r34h and r34k)" % (bold["opal_pricing"], bnew["opal_pricing"]))
        pool = json.load(open(xnew + "/ycharts/research/swap_pool.json", encoding="utf-8"))
        if (pool["schema"], pool["pool_claim"], pool["pool_as_of"], len(pool["rows"])) != ("irpt-swap-pool.v1", "held", "2026-10-16", 4419):
            fail("the shipped pool is %s" % ((pool["schema"], pool["pool_claim"], pool["pool_as_of"], len(pool["rows"])),))
        if wnew["ycharts/research/swap_pool.json"] != sha_bytes(git_show(pin, POOL_SRC)):
            fail("the shipped pool differs from the committed AQ2 snapshot")
        if rec["swap_pool"]["sha256"] != wnew["ycharts/research/swap_pool.json"] or rec["swap_pool"]["rows"] != 4419:
            fail("the record's swap_pool entry differs from the shipped pool")
        sys.path[:0] = [xnew + "/reports", xnew + "/ycharts/generate", xnew + "/ycharts/session", xnew + "/ycharts/extract", xnew + "/_scope", xnew + "/_ids",
                        xnew + "/_keys", xnew + "/_authz", xnew + "/intake", xnew + "/ops", xnew + "/lib"]
        import resident_installed as ri  # the EXTRACTED package's own installer
        if not os.path.abspath(ri.__file__).startswith(os.path.abspath(xnew)):
            fail("the installer imported is not the extracted one")
        ri.load_bindings(xnew + "/reports/resident_bindings.json")
        load = ri._opal_map_loader(bnew, xnew + "/reports")
        types = {v: load(v)["report_type"] for v in ("overview", "comparison", "multicomp")}
        if types != {"overview": "OVERVIEW", "comparison": "COMPARISON", "multicomp": "MULTI"}:
            fail("the shipped pins load %s" % types)
        # 6. the producer list
        worker = open(xnew + "/ycharts/generate/resident_worker.py", encoding="utf-8").read()
        if not re.search(r"^OPAL_PRODUCER_PRINCIPALS = " + re.escape(ADDRESS) + r"$", worker, re.M):
            fail("the producer list is not exactly %s" % ADDRESS)
        # 7. the two builds
        if walk(stage + "/build_a") != walk(stage + "/build_b") or walk(stage + "/build_a") != wnew:
            fail("build_a, build_b and the tarball do not agree")
        # 8. no credential-shaped text in a changed or added member or a script
        scripts_dir = stage + "/scripts"
        texts = [(n, open(xnew + "/" + n, "rb").read().decode("utf-8", "replace")) for n in changed + added if n != "SHA256SUMS"]
        names = ["pre_read_r34.sh", "install_r34.sh", "rollback_r34.sh", "resident_host_install_0485393f3a-r34k.sh"]
        for n in names:
            texts.append((n, open("%s/%s" % (scripts_dir, n), "rb").read().decode("ascii")))
        for n, t in texts:
            if JWT.search(t) or TOKEN_MEMBER.search(t):
                fail("credential-shaped text in %s" % n)
        # 9. the scripts
        sc = {n: open("%s/%s" % (scripts_dir, n), "rb").read() for n in names}
        for n, data in sc.items():
            if any(c > 127 for c in data) or subprocess.run(["bash", "-n", "%s/%s" % (scripts_dir, n)]).returncode != 0:
                fail("%s is not ASCII or fails bash -n" % n)
        host, install, pre, rb = (sc[names[3]].decode(), sc[names[1]].decode(), sc[names[0]].decode(), sc[names[2]].decode())
        if "WANT_TAR=" + sha_file(tar_path) not in host:
            fail("the host script does not pin the tarball")
        checks = [ln for ln in host.split("\n") if ln.startswith('check "')]
        want_checks = sorted('check "%s" %s' % (n, wnew[n]) for n in changed + added)
        if sorted(checks) != want_checks:
            fail("the host script's member checks differ from the recomputed ones (%d vs %d)" % (len(checks), len(want_checks)))
        if "NEW=0485393f3a-r34k\nOLD=0485393f3a-r34h\n" not in host or "NEW=0485393f3a-r34k\nOLD=0485393f3a-r34h\n" not in install:
            fail("NEW/OLD are not r34k/r34h in the host or install script")
        if "WANT=" + sha_bytes(sc[names[3]]) not in install or "WANTSUM=" + wnew["SHA256SUMS"] not in install:
            fail("the install script's WANT or WANTSUM is not the host script's or the sums' sha256")
        if "exit 34" not in install or "exit 40" not in pre or "OLD=0485393f3a-r34h" not in pre or "OLD=0485393f3a-r34h" not in rb:
            fail("a fail-closed guard (running root must be r34h) is missing")
        for n in changed + added:
            if n in (("SHA256SUMS"), "reports/resident_bindings.json") or n.endswith(".json"):
                continue
            if n in wold and wold[n] not in pre:
                fail("the pre-read does not carry the r34h value of %s" % n)
        if "fwd1-staff-r41b@opal.invalid" not in install:
            fail("the install lacks the producer list text")
        markers = (("ycharts/research/price_form_ycharts.py", "def request_path"), ("ycharts/research/price_adapter_ycharts.py", "price_form_ycharts.request_path"),
                   ("intake/yfinance_check.py", "expected_last_trading_day"), ("ycharts/research/ycharts_client.py", "def fund_data"),
                   ("ycharts/session/operation_lease.py", "OPERATION_WINDOW_BUDGET"), ("ycharts/generate/resident_main.py", '"lib"'))
        for member, marker in markers:
            if marker not in open(xnew + "/" + member, encoding="utf-8").read():
                fail("the shipped %s does not carry %r" % (member, marker))
        # 9b. THE IMPORT SMOKE, re-run here (not read from the record): every module the static walk marks LIVE imports under the service's own sys.path, python -I
        smoke = subprocess.run([sys.executable, "-I", "org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/smoke_imports_r34.py", xnew,
                                "org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r32/r32_reachability.py"], capture_output=True, text=True)
        smoke_head = [ln for ln in smoke.stdout.splitlines() if ln.startswith("SMOKE live=")]
        if smoke.returncode != 0 or not smoke_head or " fail=0 " not in smoke_head[0] + " ":
            fail("the import smoke over the built tree failed: %s" % " | ".join(ln for ln in smoke.stdout.splitlines() if ln.startswith("SMOKE"))[:300])
        if rec.get("import_smoke") != [ln for ln in smoke.stdout.splitlines() if ln.startswith("SMOKE")]:
            fail("the record's import_smoke lines differ from the re-run")
        # 10. the two sha256 gates
        want = re.search(r"^WANT=([0-9a-f]{64})$", install, re.M).group(1)
        want_sum = re.search(r"^WANTSUM=([0-9a-f]{64})$", install, re.M).group(1)
        g1 = [ln for ln in install.split("\n") if "sha256sum $T |" in ln]
        g2 = [ln for ln in install.split("\n") if "sha256sum $S |" in ln]
        if len(g1) != 1 or len(g2) != 1:
            fail("gate lines found %d and %d" % (len(g1), len(g2)))
        host_path = "%s/%s" % (scripts_dir, names[3])
        bad_host, bad_sums = tmp + "/host_bad", tmp + "/sums_bad"
        for src, dst, off in ((host_path, bad_host, 100), (rec["artifact"]["sha256sums_file"]["path"], bad_sums, 50)):
            data = bytearray(open(src, "rb").read())
            data[off] ^= 1
            open(dst, "wb").write(bytes(data))

        def gate(line, t, s):
            script = 'WANT=%s\nWANTSUM=%s\nT="%s"\nS="%s"\nrm() { :; }\n%s\n' % (want, want_sum, t, s, line)
            return subprocess.run(["bash", "-c", script], capture_output=True).returncode
        sums_path = rec["artifact"]["sha256sums_file"]["path"]
        got = (gate(g1[0], host_path, sums_path), gate(g1[0], bad_host, sums_path), gate(g2[0], host_path, sums_path), gate(g2[0], host_path, bad_sums))
        if got != (0, 31, 0, 33):
            fail("the gates answer %s, want (0, 31, 0, 33)" % (got,))
        print("AR-G160-OK members=%d changed=%d added=%d removed=0 builds_identical=%d scripts=4 gates=ok tar=%s" % (
            len(wnew), len(changed), len(added), len(wnew), sha_file(tar_path)))
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def scope(base, folder, order):
    """BUILD ONLY: the worker's branch changes nothing outside its own folder, its order, the channel file and the issuer's own issuance files."""
    diff = subprocess.run(["git", "diff", "--name-only", base + "...HEAD"], capture_output=True, text=True, check=True).stdout.split()
    allowed = (folder.rstrip("/") + "/", order, "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md",
               "org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/",
               "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/")
    stray = [p for p in diff if not p.startswith(allowed)]
    porcelain = subprocess.run(["git", "status", "--porcelain", "--", "infra"], capture_output=True, text=True, check=True).stdout.strip()
    if stray or porcelain:
        fail("scope: paths outside the grant %s; infra status %r" % (stray[:5], porcelain[:80]))
    print("AR-G160-SCOPE-OK %d changed paths, none under infra/, none outside the grant" % len(diff))
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "scope":
        sys.exit(scope(sys.argv[2], sys.argv[3], sys.argv[4]))
    if len(sys.argv) == 5 and sys.argv[1] == "verify":
        sys.exit(main(sys.argv[2], sys.argv[3], sys.argv[4]))
    if len(sys.argv) != 4 or sys.argv[1] != "verify":
        print("usage: ar_g160_checks.py verify <stage folder> <record json> [<expected tarball sha256>] | scope <base ref> <worker folder> <order path>")
        sys.exit(2)
    sys.exit(main(sys.argv[2], sys.argv[3], None))
