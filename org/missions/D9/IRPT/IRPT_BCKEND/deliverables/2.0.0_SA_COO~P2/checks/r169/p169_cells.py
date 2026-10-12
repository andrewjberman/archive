"""IRPT_BCKEND round 169 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of four orders.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB169-1  IB-pr-488  the ui-walk engine gains --firm "<label>" (select the header Firm option, fail loud if absent) and --first-client
    AC1  node --check walk.mjs passes (a bound: PASS at base)
    AC2  `walk.mjs --base http://example.com --firm Inflection --first-client` reaches the localhost refusal, not "unknown argument"
    AC3  SKILL.md documents both flags, walk.mjs names FIRM_OPTION_ABSENT, and nothing outside the grant changed
  IB169-2  IB-pr-489  one Inflection walk keeps ONE selection reference outside any git tree and disarms the walker
    AC1  the reference file holds exactly one line sel_ + 64 hex
    AC2  the walker status reads disabled / armed=no (a bound: PASS at base)
    AC3  the walk record carries only whitelisted keys and no client name
  IB169-3  IB-pr-490  the live read: one direct invoke of the deployed function with that reference, claim equals the offline prediction, counts present
    AC1  the record: the answer's claim equals the predicted claim for every window read, both counts present, figure sha256, at most 2 invokes
    AC2  the function's own log shows a COMPUTED path (not refused:*) after 22:35:06Z (a live AWS read)
    AC3  persisted retained revisions an integer 0..2, no long digit run, no client name key
  IB169-4  IB-pr-491  the producer's AnalysisReport contract fixtures send a section the extractor can send
    AC1  both fixtures: no section_type annualized_return, no units DECIMAL_FRACTION; units in the extractor's token set; section_type a census code; section_id starts with it
    AC2  both fixtures still validate against their schemas (a bound: PASS at base)
    AC3  nothing outside the grant changed
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
INV = "org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/"
TOS = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/"
CHK = D + "2.0.0_SA_COO~P2/checks/"
SKILL = ".claude/skills/ui-walk/"
WALK = SKILL + "walk.mjs"
REFFILE = r"C:\Users\Test\AppData\Local\Temp\claude\C--dev-ajb-workspace\f0005e69-69e0-455c-b522-7be87d97fcdc\scratchpad\inflection_sel_ref.txt"
WALK_REC = D + "0.9.0_WK_IRPT_BCKEND~341/IB169-2_walk_record.json"
LIVE_REC = D + "0.7.0_AE_CloudOps~IB2/IB169-3_inflection_live_read.json"
FIXT = "infra/aws/lambda/investor-reporting/_contracts/fixtures/"
FIX = [(FIXT + "AnalysisReport.valid.json", "infra/aws/lambda/investor-reporting/_contracts/AnalysisReport.schema.json"),
       (FIXT + "AnalysisReport.v2.ycharts.valid.json", "infra/aws/lambda/investor-reporting/_contracts/AnalysisReport.v2.schema.json")]
UNIT_TOKENS = {"count", "date", "enum", "number", "pct", "price", "ratio", "score", "text", "usd_billions", "years"}
APPLY_UTC_MS = 1791844506000  # 2026-10-12T22:35:06Z
FN_LOG = "/aws/lambda/irpt-performance-adapter"
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB169"))
    sys.exit(1)


def run(cmd, timeout=60):
    try:
        p = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        fail("timeout: %s" % " ".join(map(str, cmd))[:100])
    except FileNotFoundError as e:
        fail("not found: %s" % e)
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def load(rel, absolute=False):
    f = Path(rel) if absolute else ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def changed_outside(extra):
    rc, base = run(["git", "merge-base", "HEAD", "box/dell2"])
    if rc != 0:
        fail("merge-base HEAD box/dell2: %s" % base[:100])
    base = base.strip()
    rc, out = run(["git", "diff", "--name-only", base])
    if rc != 0:
        fail("git diff: %s" % out[:100])
    rc2, out2 = run(["git", "ls-files", "--others", "--exclude-standard"])
    names = [n.strip() for n in (out + "\n" + out2).splitlines() if n.strip()]
    rc3, lk = run(["git", "ls-files", "-s"])
    links = {ln.split("\t", 1)[1] for ln in lk.splitlines() if ln.startswith("160000")}
    ok = (INV, TOS, CHK) + tuple(extra)
    return [n for n in names if not n.startswith(ok) and n not in links]


def ensure_node_modules():
    """walk.mjs resolves playwright-core from <root>/portal/node_modules; a worker worktree has an empty portal gitlink dir, so join the main tree's
    node_modules by a directory junction (read-only use, nothing written into it)."""
    nm = ROOT / "portal" / "node_modules"
    if nm.exists():
        return
    rc, common = run(["git", "rev-parse", "--git-common-dir"])
    main = (Path(common.strip()) if Path(common.strip()).is_absolute() else ROOT / common.strip()).resolve().parent
    src = main / "portal" / "node_modules"
    if not src.is_dir():
        fail("no portal/node_modules in the worktree or the main tree (%s)" % src)
    (ROOT / "portal").mkdir(exist_ok=True)
    p = subprocess.run(["cmd", "/c", "mklink", "/J", str(nm), str(src)], capture_output=True)
    if p.returncode != 0 or not nm.exists():
        fail("could not join portal/node_modules: %s" % p.stdout.decode("utf-8", "replace")[:120])


def aws(*a):
    return run(["bash", str(ROOT / ".tools" / "aws")] + list(a), timeout=90)


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if cell == "IB169-1":
        if arm == "AC1":
            rc, out = run(["node", "--check", WALK])
            if rc != 0:
                fail("node --check %s: %s" % (WALK, out[:200]))
            print("OK: walk.mjs passes node --check")
        elif arm == "AC2":
            ensure_node_modules()
            rc, out = run(["node", WALK, "--base", "http://example.com", "--firm", "Inflection", "--first-client"], timeout=30)
            if "unknown argument" in out:
                fail("the walker does not parse the flags: %s" % out.strip().splitlines()[-1][:120])
            if "REFUSED: --base must be a localhost dev build" not in out:
                fail("expected the localhost refusal after a clean parse, got: %s" % out.strip()[:160])
            rc2, out2 = run(["node", WALK, "--base", "http://example.com", "--firm"], timeout=30)
            if "REFUSED: --base must be a localhost dev build" in out2:
                fail("a --firm with no label was accepted silently: it must fail loud on the missing label before the base refusal")
            print("OK: --firm and --first-client parse; the localhost refusal follows; --firm with no label is not silently accepted")
        elif arm == "AC3":
            sk = (ROOT / SKILL / "SKILL.md")
            wk = (ROOT / WALK)
            if not sk.is_file() or not wk.is_file():
                fail("no SKILL.md or walk.mjs")
            st, wt = sk.read_text(encoding="utf-8", errors="replace"), wk.read_text(encoding="utf-8", errors="replace")
            if "--firm" not in st or "--first-client" not in st:
                fail("SKILL.md must document --firm and --first-client in the invocation block")
            if "FIRM_OPTION_ABSENT" not in wt:
                fail("walk.mjs must fail loud with FIRM_OPTION_ABSENT when the option label is not on the page")
            out = changed_outside((SKILL, D + "0.9.0_WK_IRPT_BCKEND~341/"))
            if out:
                fail("changed outside the grant: %s" % out[:4])
            print("OK: both flags documented, FIRM_OPTION_ABSENT present, nothing outside the grant changed")
        else:
            fail("unknown criterion")
    elif cell == "IB169-2":
        if arm == "AC1":
            f = Path(REFFILE)
            if not f.is_file():
                fail("no reference file at the named scratch path")
            lines = [ln.strip() for ln in f.read_text(encoding="utf-8").splitlines() if ln.strip()]
            if len(lines) != 1 or not re.fullmatch(r"sel_[0-9a-f]{64}", lines[0]):
                fail("the file must hold exactly one line sel_ + 64 hex (%d line(s))" % len(lines))
            print("OK: one reference line of the right shape")
        elif arm == "AC2":
            rc, out = run(["python", str(ROOT / SKILL / "ui_walker_account.py"), "status"])
            if "status=disabled" not in out or "armed=no" not in out:
                fail("the walker account is not dormant: %s" % out.strip()[:160])
            print("OK: walker dormant (disabled, armed=no)")
        elif arm == "AC3":
            r = load(WALK_REC)
            allowed = {"firm_label", "performance_tab_reached", "performance_request_paths", "walker_disarmed", "walk_stamp", "reference_file_written"}
            if set(r) != allowed:
                fail("record keys must be exactly %s, got %s" % (sorted(allowed), sorted(r)))
            if r["firm_label"] != "Inflection" or r["performance_tab_reached"] is not True or r["walker_disarmed"] is not True or r["reference_file_written"] is not True:
                fail("firm_label Inflection, performance_tab_reached, walker_disarmed and reference_file_written must all be true")
            if not isinstance(r["performance_request_paths"], int) or r["performance_request_paths"] < 1:
                fail("performance_request_paths must be an integer >= 1")
            if not re.fullmatch(r"\d{8}T\d{6}Z", str(r["walk_stamp"])):
                fail("walk_stamp must be the walk folder stamp YYYYMMDDTHHMMSSZ")
            print("OK: the walk record carries the whitelisted keys only")
        else:
            fail("unknown criterion")
    elif cell == "IB169-3":
        if arm == "AC1":
            r = load(LIVE_REC)
            if r.get("invokes") not in (1, 2) or r.get("ref_count") != 1:
                fail("invokes must be 1 or 2 on ref_count 1")
            ws = r.get("windows") or []
            if not ws:
                fail("at least one window read")
            for w in ws:
                if w.get("claim_observed") != w.get("claim_predicted") or w.get("claim_predicted") not in ("measured", "inferred"):
                    fail("window %s: observed %r != predicted %r" % (w.get("window"), w.get("claim_observed"), w.get("claim_predicted")))
                for k in ("days_without_base", "days_with_return_left_out"):
                    if not isinstance(w.get(k), int) or isinstance(w.get(k), bool):
                        fail("window %s: %s must be an integer (the count is present)" % (w.get("window"), k))
                if not re.fullmatch(r"[0-9a-f]{64}", str(w.get("figure_sha256", ""))):
                    fail("window %s: figure_sha256" % w.get("window"))
            if r.get("path_class") != "computed":
                fail("path_class must read computed")
            print("OK: %d window(s), claim equals the prediction, both counts present, figure hashes recorded" % len(ws))
        elif arm == "AC2":
            rc, out = aws("logs", "filter-log-events", "--log-group-name", FN_LOG, "--start-time", str(APPLY_UTC_MS),
                          "--filter-pattern", "irpt_retained_phases", "--output", "json")
            if rc != 0:
                fail("log read failed (rc %s): %s" % (rc, out[:160]))
            try:
                msgs = [e.get("message", "") for e in json.loads(out).get("events", [])]
            except ValueError:
                fail("log read not JSON")
            computed = [m for m in msgs if "refused:" not in m]
            if not computed:
                fail("no irpt_retained_phases line since the apply names a computed path (denominator: %d line(s))" % len(msgs))
            te = aws("logs", "filter-log-events", "--log-group-name", FN_LOG, "--start-time", str(APPLY_UTC_MS), "--filter-pattern", "TypeError", "--query", "length(events)", "--output", "text")
            if te[0] != 0 or te[1].strip() != "0":
                fail("TypeError lines since the apply: %r" % te[1].strip()[:40])
            print("OK: %d computed line(s) of %d since the apply, 0 TypeError" % (len(computed), len(msgs)))
        elif arm == "AC3":
            r = load(LIVE_REC)
            pr = r.get("persisted_retained_revisions")
            if not isinstance(pr, int) or isinstance(pr, bool) or not 0 <= pr <= 2:
                fail("persisted_retained_revisions must be an integer 0..2")
            raw = json.dumps(r)
            if re.search(r"(?<![0-9a-fA-F])\d{10,}(?![0-9a-fA-F])", raw):
                fail("a long digit run (an account id or a figure?)")
            if re.search(r"sel_[0-9a-f]{64}", raw):
                fail("the reference must not be copied into the record")
            for k in ("client", "client_name", "account", "account_id", "name"):
                if k in r:
                    fail("record key %r is not allowed" % k)
            print("OK: bounded persists, no id, no reference, no client key")
        else:
            fail("unknown criterion")
    elif cell == "IB169-4":
        if arm == "AC1":
            for fx, _schema in FIX:
                d = load(fx)
                inst = d.get("instance", d)
                secs = inst.get("sections") if isinstance(inst, dict) else None
                if not secs:
                    fail("%s: no sections found" % fx)
                for s in secs:
                    if s.get("section_type") == "annualized_return" or s.get("units") == "DECIMAL_FRACTION":
                        fail("%s still sends section_type annualized_return or units DECIMAL_FRACTION" % fx)
                    if s.get("units") not in UNIT_TOKENS:
                        fail("%s: units %r is not an extractor token" % (fx, s.get("units")))
                    t = str(s.get("section_type", ""))
                    if not re.fullmatch(r"[0-9]+", t):
                        fail("%s: section_type %r is not a census code" % (fx, t))
                    if not str(s.get("section_id", "")).startswith(t + "."):
                        fail("%s: section_id %r must start with its code and a dot (the extractor's form)" % (fx, s.get("section_id")))
            print("OK: both fixtures send only what the extractor can send")
        elif arm == "AC2":
            try:
                import jsonschema
            except ImportError:
                fail("jsonschema missing")
            for fx, sc in FIX:
                d, s = load(fx), load(sc)
                try:
                    jsonschema.validate(d.get("instance", d), s)
                except Exception as e:  # noqa: BLE001
                    fail("%s no longer validates against %s: %s" % (fx, sc, str(e)[:140]))
            print("OK: both fixtures validate against their schemas")
        elif arm == "AC3":
            out = changed_outside((FIXT, D + "0.9.0_WK_IRPT_BCKEND~342/"))
            if out:
                fail("changed outside the grant: %s" % out[:4])
            print("OK: nothing outside the grant changed")
        else:
            fail("unknown criterion")
    else:
        fail("unknown criterion %r" % CID)
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
