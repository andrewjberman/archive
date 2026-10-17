"""IRPT_DASHBD round 139, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- the Inflection bundle manifest's PIN SPLIT (cell DB-f-2701; the CTO's round-138 analysis ruling 4).

  Ruling: the manifest's members split into OWNED members (pinned at cut, as now) and SHARED registry members (lib/opal_naming.py, lib/trading_calendar.py, the registry and the naming
  schema, which other lanes write), listed WITHOUT a cut pin. For a shared member the release-day cell records the pin in a RECEIPT and `build_bundle` compares against the receipt's
  pin, never a cut pin. Today two shared members have drifted and `build_bundle` refuses, so nine launcher tests are red on the trunk; a red baseline hides the next real failure.

  Mechanism asked of the cell (the checker grades behaviour, not names, except these): the manifest marks each shared member `"shared": true` and carries no `sha256` for it;
  `build_bundle(root, out_path, receipt=None)` takes an optional receipt dict `{"shared_pins": {<path>: <sha256>}}`; the runtime check of the zip (`bootstrap`) reads the expected
  bundle sha256 from a receipt file beside the zip (the release uploads it), so the launcher no longer carries a constant that other lanes' edits can invalidate.

  DBF139-1-AC1  the launcher test file reads green at HEAD: 0 failed, 0 errors (the nine red tests)
  DBF139-1-AC2  a planted edit to an OWNED member still refuses, naming the member
  DBF139-1-AC3  a planted edit to a SHARED member does not refuse while no receipt pin exists; with a receipt pin that the edited file differs from it refuses, naming the member; with a
                receipt pin equal to the edited file it builds

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LAUNCHER = "data/inf/scripts/gold/INF_G_01.account_transaction_gold.py"
MANIFEST = "data/inf/scripts/gold/INF_G_01.bundle.json"
TESTS = "data/inf/scripts/gold/tests/test_INF_G_01_account_transaction_gold.py"
OWNED = ["data/assets/scripts/gold/irpt_reporting/account_return_daily.py", "data/assets/scripts/gold/irpt_reporting/account_transaction.py",
         "data/assets/scripts/gold/irpt_reporting/account_transaction_inflection.py", "data/assets/scripts/gold/irpt_reporting/transaction_words.json",
         "data/assets/scripts/lib/stream_parquet.py"]
SHARED = ["infra/logic/registry/exemptions.json", "infra/logic/registry/feeds.json", "infra/logic/registry/firm_pages.json", "infra/logic/registry/legacy_addresses.json",
          "infra/logic/registry/platinum_destinations.json", "infra/logic/registry/remediations.json", "infra/logic/registry/reporting_policies.json",
          "infra/logic/registry/resources.json", "infra/logic/registry/scopes.json", "infra/logic/registry/systems.json", "infra/logic/registry/tiers.json",
          "lib/opal_naming.py", "lib/trading_calendar.py", "org/standards/NAMING_SCHEMA.json"]


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def manifest_problems(manifest):
    """The split: exactly OWNED members carry a sha256; exactly SHARED members carry shared:true and no sha256; nothing else is a member."""
    pr = []
    files = manifest.get("files", [])
    paths = [f.get("path") for f in files]
    if sorted(paths) != sorted(OWNED + SHARED):
        pr.append("the manifest's members must be exactly the %d owned and %d shared ones" % (len(OWNED), len(SHARED)))
    for f in files:
        p = f.get("path")
        if p in OWNED and (f.get("shared") or not re.fullmatch(r"[0-9a-f]{64}", str(f.get("sha256", "")))):
            pr.append("%s is OWNED: it must carry a 64-hex sha256 and no shared flag" % p)
        if p in SHARED and (f.get("shared") is not True or "sha256" in f):
            pr.append("%s is SHARED: it must carry shared:true and NO sha256" % p)
    return pr


def load_launcher(root):
    spec = importlib.util.spec_from_file_location("inf_g_01_split_%d" % id(root), str(Path(root, LAUNCHER)))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def scratch_repo(root, td):
    """A copy of just the manifest, the launcher and the members, in the repo layout, so a member can be planted without touching the real tree."""
    t = Path(td, "repo")
    for rel in [LAUNCHER, MANIFEST] + OWNED + SHARED:
        dst = t / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(Path(root, rel), dst)
    return t


def try_build(L, repo, out, receipt=None):
    """('ok', sha256) or ('refused', text)."""
    try:
        d = L.build_bundle(repo, out) if receipt is None else L.build_bundle(repo, out, receipt=receipt)
        return "ok", d
    except SystemExit as e:
        return "refused", str(e)


def ac1(root):
    r = subprocess.run([sys.executable, "-m", "pytest", TESTS, "-q", "-p", "no:cacheprovider", "--color=no"], cwd=str(root), capture_output=True, text=True, timeout=900)
    out = (r.stdout or "") + (r.stderr or "")
    m = re.search(r"(\d+) passed", out)
    need(r.returncode == 0 and m and not re.search(r"\d+ (failed|error)", out), "the launcher test file must read green: %s" % out.strip().splitlines()[-1][:200] if out.strip() else "no pytest output")


def ac2(root):
    man = json.loads(Path(root, MANIFEST).read_text(encoding="utf-8"))
    need(not manifest_problems(man), "; ".join(manifest_problems(man)))
    L = load_launcher(root)
    with tempfile.TemporaryDirectory() as td:
        repo = scratch_repo(root, td)
        kind, text = try_build(L, repo, Path(td, "clean.zip"))
        need(kind == "ok", "the unedited tree must build: %s" % text[:200])
        planted = OWNED[1]
        Path(repo, planted).write_bytes(Path(repo, planted).read_bytes() + b"\n# planted\n")
        kind, text = try_build(L, repo, Path(td, "owned.zip"))
        need(kind == "refused" and planted in text, "a planted edit to the owned member %s must refuse naming it (got %s: %s)" % (planted, kind, text[:160]))


def ac3(root):
    L = load_launcher(root)
    with tempfile.TemporaryDirectory() as td:
        repo = scratch_repo(root, td)
        p = SHARED[11]  # lib/opal_naming.py
        orig = sha(Path(repo, p).read_bytes())
        Path(repo, p).write_bytes(Path(repo, p).read_bytes() + b"\n# planted\n")
        edited = sha(Path(repo, p).read_bytes())
        kind, text = try_build(L, repo, Path(td, "a.zip"))
        need(kind == "ok", "a planted edit to the shared member %s must NOT refuse while no receipt pin exists (got %s: %s)" % (p, kind, text[:160]))
        kind, text = try_build(L, repo, Path(td, "b.zip"), receipt={"shared_pins": {p: orig}})
        need(kind == "refused" and p in text, "with a receipt pin the edited file differs from, the build must refuse naming %s (got %s: %s)" % (p, kind, text[:160]))
        kind, text = try_build(L, repo, Path(td, "c.zip"), receipt={"shared_pins": {p: edited}})
        need(kind == "ok", "with a receipt pin equal to the edited file the build must succeed (got %s: %s)" % (kind, text[:160]))


def selftest():
    bad = count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    h = "a" * 64
    good = {"files": [{"path": p, "sha256": h} for p in OWNED] + [{"path": p, "shared": True} for p in SHARED]}
    arm("members-count", (len(OWNED), len(SHARED)), (5, 14))
    arm("no-overlap", set(OWNED) & set(SHARED), set())
    arm("manifest-green", manifest_problems(good), [])
    arm("manifest-shared-with-sha", len(manifest_problems({"files": [dict(f, sha256=h) if f.get("shared") else f for f in good["files"]]})) >= 1, True)
    arm("manifest-owned-without-sha", len(manifest_problems({"files": [{"path": OWNED[0]}] + good["files"][1:]})) >= 1, True)
    arm("manifest-extra-member", len(manifest_problems({"files": good["files"] + [{"path": "x.py", "sha256": h}]})) >= 1, True)
    arm("manifest-missing-member", len(manifest_problems({"files": good["files"][:-1]})) >= 1, True)
    arm("sha", len(sha(b"x")), 64)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3 or argv[2] not in ("DBF139-1-AC1", "DBF139-1-AC2", "DBF139-1-AC3"):
        print("usage: p139_split.py <repo_root> DBF139-1-AC1|AC2|AC3 | --selftest")
        return 2
    try:
        {"DBF139-1-AC1": ac1, "DBF139-1-AC2": ac2, "DBF139-1-AC3": ac3}[argv[2]](argv[1])
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % argv[2])
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % argv[2])
        return 1
    print("%s PASS" % argv[2])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
