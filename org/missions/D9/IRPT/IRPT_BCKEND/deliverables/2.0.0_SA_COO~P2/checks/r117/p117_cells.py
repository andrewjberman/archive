"""IRPT_BCKEND round 117 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of three orders:
  IB117-1  IB-pr-416  row D2-S60: irpt-narrative, irpt-performance-adapter and irpt-status rebuilt from ONE tree so every served.py
                      call fits its packaged callee; attribute-call limb added; never-widen packet (worker ~278)
  IB117-2  IB-pr-417  the 49F narrow bundle rebuilt as IB-pr-410's members + IB-pr-414's publish-gate memory fix; memory, replay,
                      packet (worker ~279; CTO ADDENDUM 20, re-points IB-pr-413)
  IB117-3  IB-pr-418  containment ruling @0e8209c33c item 3: no client account id in the 12 BCKEND code files or TO-IB-er-201; the
                      er-201 proof instance back in the tree redacted and VALID (worker ~280)
  IB117-4  IB-pr-419  row D2-S60, CTO msg 3732: one real GET through each route reaching a split, with each function's 24h CloudWatch
                      error counts; FAILING or LATENT per function (worker ~281)

Usage: python <this file> <repo_root> <criterion_id> [--set <private account-set json>]; prints "<id> PASS" or "<id> FAIL" last.
  IB117-1-AC1  census S: 3 functions, each built twice identical, signature_closure mismatched 0 and attribute-call mismatched 0 on the
               built zip; the same instruments on each LIVE zip report >= 1 mismatch (negative control). Base: FAIL (no S).
  IB117-1-AC2  packet P1 names Branch A, Branch B and each function's built sha256. Base: FAIL (no P1).
  IB117-2-AC1  census C: one artifact, firm 49financial, base_sha256 == the live 49F bytes, built twice identical, changed members
               (SHA256SUMS aside) == exactly holdings_snapshot.py + holdings_49f.py. Base: FAIL (no C).
  IB117-2-AC2  memory M + replay R + packet P2: built peak_rss_bytes < 0.85 x 4 GiB, wall_time_s <= 2 x pre404's 380.2 s; arms
               identical/expected-diff with `fwd14_gate_vs_b410` and `smartx_class_parity` identical and >= 1 negative control; P2 names
               Branch A, Branch B, base and built sha256. Base: FAIL (no M).
  IB117-3-AC1  no token in the 13 named files equals an account of the private set (--set, read outside the repo; absent -> FAIL);
               every named .py compiles. Base: FAIL (20 hits at HEAD @c75b937bb2).
  IB117-4-AC1  live read L: per function cloudwatch_24h {unexpected_keyword, errors_total} as ints, >= 1 real GET with route and
               status_code, verdict FAILING or LATENT. Base: FAIL (no L).
  IB117-3-AC2  the er-201 proof instance is in the tree and `proof-of-spec-check.py` reads it VALID. Base: FAIL (moved @12b257c3ab).
"""
import json
import py_compile
import re
import subprocess
import sys
from pathlib import Path

T = "org/missions/D9/IRPT/IRPT_BCKEND/"
W1 = T + "deliverables/0.9.0_WK_IRPT_BCKEND~278/"
W2 = T + "deliverables/0.9.0_WK_IRPT_BCKEND~279/"
W4 = T + "deliverables/0.9.0_WK_IRPT_BCKEND~281/"
FUNCS = ["irpt-narrative", "irpt-performance-adapter", "irpt-status"]
BASE49 = "3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901"
MEMBERS = sorted(["data/assets/scripts/gold/investor_reporting/holdings_snapshot.py",
                  "data/assets/scripts/gold/investor_reporting/holdings_49f.py"])
LIMIT = int(0.85 * 4 * 1024 ** 3)
WALL = 2 * 380.2
P2C = T + "deliverables/2.0.0_SA_COO~P/checks/"
NAMED = [T + "deliverables/0.9.0_WK_IRPT_BCKEND~142/make_fixtures_p340.py",
         P2C + "r19/p19_1_ac1_implausible_fixture.py", P2C + "r19/p19_1_ac2_live_seam.py",
         P2C + "r19/p19_2_ac1_since_inception_fixture.py", P2C + "r19/p19_2_ac2_live_seam.py",
         P2C + "r19/p19_4_ac1_reopen_fixture.py", P2C + "r1e/e1_ac1_thread_day_recompute.py",
         P2C + "r1e/e1_ac2_thread_ytd_coverage.py", P2C + "r20/p20_1_ac1_gold_fixture.py", P2C + "r20/p20_1_ac2_gold_live.py",
         P2C + "r22/p22_1_ac1_inf_gold_fixture.py", P2C + "r27/p27_3_blast_radius.py",
         T + "task-orders/IRPT_BCKEND.TO-IB-er-201.holdings-gold-thread-one-49f-account.md"]
ER201_PROOF = (T + "deliverables/0.4.0_DS_ClientPlatform~E/"
               "IRPT_BCKEND.TO-IB-er-201.holdings-gold-thread-one-49f-account.proof_of_spec.json")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    opt = sys.argv[3:]

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB117"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    def packet(rel, shas):
        pp = root / rel
        if not pp.is_file():
            fail("no %s" % rel)
        pk = pp.read_text(encoding="utf-8")
        for s in ["Branch A", "Branch B"] + list(shas):
            if not s or s not in pk:
                fail("%s lacks %r" % (rel, s))

    if cid == "IB117-1-AC1":
        rows = {r.get("function"): r for r in load(W1 + "IB117-1_signature_census.json").get("functions") or []}
        if sorted(rows) != sorted(FUNCS):
            fail("functions %r" % sorted(rows))
        for f in FUNCS:
            r = rows[f]
            if r.get("built_twice_identical") is not True or not r.get("built_sha256"):
                fail("%s build %r" % (f, {k: r.get(k) for k in ("built_twice_identical", "built_sha256")}))
            if r.get("built_signature_mismatched") != 0 or r.get("built_attribute_mismatched") != 0:
                fail("%s built mismatches sig %r attr %r" % (f, r.get("built_signature_mismatched"), r.get("built_attribute_mismatched")))
            live = (r.get("live_signature_mismatched") or 0) + (r.get("live_attribute_mismatched") or 0)
            if not isinstance(live, int) or live < 1:
                fail("%s negative control: live zip reads %r mismatches" % (f, live))
        print("OK: 3 functions built twice identical, 0 signature and 0 attribute mismatches; every live zip reads >= 1")
    elif cid == "IB117-1-AC2":
        rows = load(W1 + "IB117-1_signature_census.json").get("functions") or []
        packet(W1 + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-416.md", [str(r.get("built_sha256") or "") for r in rows] or [""])
        print("OK: packet names both branches and %d built sha256" % len(rows))
    elif cid == "IB117-2-AC1":
        c = load(W2 + "IB117-2_49f_bundle_census.json")
        bo, arts = c.get("build_only") or {}, c.get("artifacts") or []
        if bo.get("rc") != 0 or bo.get("tree_clean") is not True or len(arts) != 1:
            fail("census %r / %d artifact(s)" % (bo, len(arts)))
        a = arts[0]
        if a.get("firm") != "49financial" or a.get("base_sha256") != BASE49 or a.get("built_twice_identical") is not True \
                or not a.get("built_sha256"):
            fail("artifact %r" % {k: a.get(k) for k in ("firm", "base_sha256", "built_twice_identical", "built_sha256")})
        ch = sorted(m for m in a.get("changed_members") or [] if not m.endswith("SHA256SUMS"))
        if ch != MEMBERS:
            fail("changed members %r" % ch)
        print("OK: one 49F bundle on the live base; changes exactly holdings_snapshot.py + holdings_49f.py")
    elif cid == "IB117-2-AC2":
        m = load(W2 + "IB117-2_49f_bundle_memory.json")
        peak, wall = m.get("peak_rss_bytes"), m.get("wall_time_s")
        if not isinstance(peak, int) or peak >= LIMIT:
            fail("built peak %r vs limit %d" % (peak, LIMIT))
        if not isinstance(wall, (int, float)) or wall > WALL:
            fail("built wall %r vs %.1f" % (wall, WALL))
        arms = load(W2 + "IB117-2_49f_bundle_replay.json").get("arms") or []
        by = {x.get("name"): x.get("verdict") for x in arms}
        if not arms or not all(v in ("identical", "expected-diff") for v in by.values()):
            fail("arms %r" % by)
        for name in ("fwd14_gate_vs_b410", "smartx_class_parity"):
            if by.get(name) != "identical":
                fail("%s reads %r" % (name, by.get(name)))
        if not any(x.get("negative_control") for x in arms):
            fail("no negative control")
        c = load(W2 + "IB117-2_49f_bundle_census.json")
        packet(W2 + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-417.md",
               [BASE49, str(((c.get("artifacts") or [{}])[0]).get("built_sha256") or "")])
        print("OK: peak %d < %d, wall %.1f <= %.1f; %d arms; packet complete" % (peak, LIMIT, wall, WALL, len(arms)))
    elif cid == "IB117-3-AC1":
        if len(opt) != 2 or opt[0] != "--set" or not Path(opt[1]).is_file():
            fail("--set <private account-set json> required (read outside the repo)")
        acct = set(re.findall(r"(?<!\d)\d{10}(?!\d)", Path(opt[1]).read_text(encoding="utf-8")))
        if len(acct) < 1000:
            fail("account set reads %d ids" % len(acct))
        hits = 0
        for rel in NAMED:
            f = root / rel
            if not f.is_file():
                continue
            t = f.read_text(encoding="utf-8", errors="replace")
            n = len(set(re.findall(r"(?<!\d)\d{10}(?!\d)", t)) & acct)
            if n:
                hits += 1
                print("HIT: %s (%d)" % (rel, n))
            if rel.endswith(".py"):
                try:
                    py_compile.compile(str(f), doraise=True)
                except py_compile.PyCompileError as e:
                    fail("%s does not compile: %s" % (rel, e))
        if hits:
            fail("%d of %d named files carry an account id" % (hits, len(NAMED)))
        print("OK: 0 of %d named files carry an account id (set of %d)" % (len(NAMED), len(acct)))
    elif cid == "IB117-4-AC1":
        rows = {r.get("function"): r for r in load(W4 + "IB117-4_live_call_read.json").get("functions") or []}
        if sorted(rows) != sorted(FUNCS):
            fail("functions %r" % sorted(rows))
        for f in FUNCS:
            r = rows[f]
            cw = r.get("cloudwatch_24h") or {}
            if not isinstance(cw.get("unexpected_keyword"), int) or not isinstance(cw.get("errors_total"), int):
                fail("%s cloudwatch_24h %r" % (f, cw))
            gets = r.get("gets") or []
            if not gets or not all(isinstance(g.get("status_code"), int) and g.get("route") for g in gets):
                fail("%s gets %r" % (f, gets))
            if r.get("verdict") not in ("FAILING", "LATENT"):
                fail("%s verdict %r" % (f, r.get("verdict")))
        print("OK: %s" % ", ".join("%s %s" % (f, rows[f]["verdict"]) for f in FUNCS))
    elif cid == "IB117-3-AC2":
        if not (root / ER201_PROOF).is_file():
            fail("no %s" % ER201_PROOF)
        p = subprocess.run([sys.executable, str(root / ".tools/proof-of-spec-check.py"), ER201_PROOF], cwd=str(root),
                           capture_output=True, timeout=280)
        last = (p.stdout + p.stderr).decode("utf-8", "replace").strip().splitlines()
        if p.returncode != 0:
            fail("proof-of-spec-check rc %d: %s" % (p.returncode, last[-1] if last else ""))
        print("OK: er-201 proof instance VALID")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
