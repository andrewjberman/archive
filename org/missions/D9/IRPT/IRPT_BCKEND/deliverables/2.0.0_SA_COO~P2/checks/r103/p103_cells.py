"""IRPT_BCKEND round 103 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of two orders:
  IB103-1  IB-pr-401  apply irpt-narrative (IB-pr-399) on 0.7.0_AE_CloudOps~IB2 under COO half @08070100ee and CTO half @1428af7198
  IB103-2  IB-pr-402  FWD-14 NARROW per-firm holdings bundles (row D2-W265-S1, ruling D2-S37): each live per-firm bundle with ONLY
                      holdings_snapshot.py moved, by the FWD-14 commits 9af6811b61 + ce6e2a218e (worker ~266)

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB103-1-AC1  live irpt-narrative CodeSha256 == QiNRKpaCoX5g...; after-reads A1 ledger CLOSED stating pin cabad9008c and that sha256.
               Base: FAIL (live == es/S9azu...).
  IB103-1-AC2  A1 replay_rerun_before_ledger: >= 14 arms, all identical/expected-diff, one named no_row_internal_enforcer_scope reading
               identical. Base: FAIL (no A1).
  IB103-1-AC3  A1 narrative_census_row == "ONE" with its census_invocation stated (CTO half condition 4). Base: FAIL (no A1).
  IB103-2-AC1  census C2: build_only rc 0 on a clean tree; 3 artifacts (49financial, inflection, cottonwood), each built twice identical,
               live_before == the version read by ~265, and changed members (SHA256SUMS aside) == exactly holdings_snapshot.py.
               Base: FAIL (no C2).
  IB103-2-AC2  replay R2: arms all identical/expected-diff; per firm a real-input live-vs-built arm reading identical and a QA
               worse/restored arm reading expected-diff; >= 3 negative controls. Base: FAIL (no R2).
  IB103-2-AC3  packet P2 names Branch A, Branch B, the base commit, each built sha256 and each rollback version id. Base: FAIL (no P2).
"""
import json
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
A1 = D + "0.7.0_AE_CloudOps~IB2/IB103-1_narrative_release_after_reads.json"
W2 = D + "0.9.0_WK_IRPT_BCKEND~266/"
NARR_BUILT = "QiNRKpaCoX5gIGmt8ypj34l3noLeroXqwWLprr68Pmw="
HS = "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py"
LIVE_BEFORE = {"49financial": "3Q_W49U7kMa_xO30Q6LQE7QLsFu7ARur", "inflection": "SuRm8tIYq9AKTbRD91SxTJp2Fh80CqCo",
               "cottonwood": "NZIQjid2En9Wbe8kM8ibfsIjxjDWKEoT"}


def live(root, fn):
    p = subprocess.run(["bash", str(root / ".tools" / "aws"), "lambda", "get-function-configuration", "--function-name", fn,
                        "--query", "CodeSha256", "--output", "text"], capture_output=True, timeout=120)
    return p.stdout.decode("utf-8", "replace").strip() if p.returncode == 0 else ""


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB103"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    def ok(arms):
        return all(x.get("verdict") in ("identical", "expected-diff") for x in arms)

    if cid == "IB103-1-AC1":
        got = live(root, "irpt-narrative")
        if got != NARR_BUILT:
            fail("narrative live %r != built" % got)
        led = load(A1).get("ledger") or {}
        if led.get("state") != "CLOSED" or not str(led.get("pin", "")).startswith("cabad9008c") or led.get("sha256") != NARR_BUILT:
            fail("ledger %r" % led)
        print("OK: narrative live == built; ledger CLOSED with pin + sha256")
    elif cid == "IB103-1-AC2":
        arms = load(A1).get("replay_rerun_before_ledger") or []
        if len(arms) < 14 or not ok(arms):
            fail("%d arm(s) or a bad verdict" % len(arms))
        if not any(x.get("name") == "no_row_internal_enforcer_scope" and x.get("verdict") == "identical" for x in arms):
            fail("no identical no_row_internal_enforcer_scope arm")
        print("OK: %d arms before the ledger; enforcer scope identical" % len(arms))
    elif cid == "IB103-1-AC3":
        a = load(A1)
        if a.get("narrative_census_row") != "ONE" or not a.get("census_invocation"):
            fail("census row %r / invocation %r" % (a.get("narrative_census_row"), a.get("census_invocation")))
        print("OK: narrative census row ONE")
    elif cid == "IB103-2-AC1":
        c = load(W2 + "IB103-2_narrow_bundle_census.json")
        bo = c.get("build_only") or {}
        if bo.get("rc") != 0 or bo.get("tree_clean") is not True:
            fail("build_only %r" % bo)
        arts = {a.get("firm"): a for a in c.get("artifacts") or []}
        if set(arts) != set(LIVE_BEFORE):
            fail("firms %r" % sorted(arts))
        for f, a in arts.items():
            if a.get("built_twice_identical") is not True or not a.get("built_sha256"):
                fail("%s build %r" % (f, a.get("built_sha256")))
            if a.get("live_before") != LIVE_BEFORE[f]:
                fail("%s live_before moved: %r" % (f, a.get("live_before")))
            ch = sorted(m for m in a.get("changed_members") or [] if not m.endswith("SHA256SUMS"))
            if ch != [HS]:
                fail("%s changed members %r" % (f, ch))
        print("OK: 3 narrow bundles, each changes only holdings_snapshot.py")
    elif cid == "IB103-2-AC2":
        arms = load(W2 + "IB103-2_narrow_bundle_replay.json").get("arms") or []
        if not arms or not ok(arms):
            fail("arms")
        by = {x.get("name"): x.get("verdict") for x in arms}
        for f in LIVE_BEFORE:
            if by.get("real_%s_live_vs_built" % f) != "identical":
                fail("real_%s_live_vs_built %r" % (f, by.get("real_%s_live_vs_built" % f)))
            if by.get("fx_%s_worse_restored" % f) != "expected-diff":
                fail("fx_%s_worse_restored %r" % (f, by.get("fx_%s_worse_restored" % f)))
        if sum(1 for x in arms if x.get("negative_control")) < 3:
            fail("fewer than 3 negative controls")
        print("OK: %d arms; real inputs identical at 3 firms; QA pair refuses" % len(arms))
    elif cid == "IB103-2-AC3":
        c = load(W2 + "IB103-2_narrow_bundle_census.json")
        pp = root / (W2 + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-402.md")
        if not pp.is_file():
            fail("no packet")
        pk = pp.read_text(encoding="utf-8")
        need = ["Branch A", "Branch B", str(c.get("base_commit") or "")] + list(LIVE_BEFORE.values())
        need += [str(a.get("built_sha256") or "") for a in c.get("artifacts") or []]
        for s in need:
            if not s or s not in pk:
                fail("packet lacks %r" % s)
        print("OK: packet names both branches, the base, 3 built shas and 3 rollback versions")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
