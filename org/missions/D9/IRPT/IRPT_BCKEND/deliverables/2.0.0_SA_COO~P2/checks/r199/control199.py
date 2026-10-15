"""Positive control and negatives for p199_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control199.py <real_repo_root>
Builds a temp git root with synthetic records, a synthetic packet v3 (section 2 tables), a ledger file and a copy of lib/trading_calendar.py, runs every
criterion expecting PASS, then applies each mutation expecting the NAMED criterion to FAIL. The temp root is removed.
"""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r199/p199_cells.py"
sys.path.insert(0, str(CHECK.parent.parent / "r193"))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
sys.path.insert(0, str(CHECK.parent))
import p199_apply as PA  # noqa: E402
import p199_cells as P  # noqa: E402

P6 = P.P6
P3 = PA.P3
MEMBERS = {"49financial": ["data/a/holdings_snapshot.py", "data/a/x.py"], "cottonwood": ["data/a/holdings_snapshot.py", "data/a/y.py"],
           "inflection": ["data/a/holdings_snapshot.py", "data/a/z.py"]}


def w(root, rel, obj):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(obj if isinstance(obj, str) else json.dumps(obj, indent=1), encoding="utf-8")


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def packet():
    out = ["# packet v3", "", "## 2. Moved-member tables", ""]
    for f, ms in MEMBERS.items():
        out += ["### %s -- changed by content 2" % f, "", "| path | state |", "|---|---|"] + ["| %s | changed |" % m for m in ms] + [""]
    out += ["## 3. Calendar", ""]
    return "\n".join(out)


def members(f):
    return sorted(set(MEMBERS[f]) | {PA.OPAL_UNID, "SHA256SUMS"})


ORION = {
    "base_commit": "a" * 40,
    "dates": {d: {"trading_day": True, "claim": "measured", "empty_beforehand": {k: 0 for k in P.EMPTY_KEYS}} for d in P.DATES},
    "pull_path": {"stages": [
        {"kind": "vendor_pull", "claim": "measured", "producer": "pull/pull_orion.py:4", "identifier": "pull_positions", "trigger": "the scheduled 6 AM ET fold fires the pull daily"},
        {"kind": "silver_convert", "claim": "measured", "producer": "pull/convert.py:1", "identifier": "convert_day", "trigger": "an S3 object-created notification on the bronze feed"},
        {"kind": "trigger", "claim": "inferred", "producer": "", "identifier": "", "trigger": "the daily emitter names the day; not read in this record"}]},
    "skip_cause": {"claim": "inferred", "statement": "the vendor returned an empty feed for both days and the pull wrote nothing, so no object-created event fired",
                   "evidence": ["the bronze assets feed holds one file for each day while positions holds none", "the pull logs for both days were not retained past the retention window"]},
    "repull_method": {"writes": [P.PREFIX + "bronze/positions/2026-07-01/", P.PREFIX + "bronze/positions/2026-09-28/"], "writes_only_the_two_dates": True, "executed": False,
                      "read_back": "list each written key and compare its byte count with the vendor response before the silver conversion runs",
                      "rollback_per_key": "delete exactly the keys the re-pull created, listed in the record, after a version-id read of each", "vendor_calls_needed": 6},
    "notes": ["synthetic"], **{k: 0 for k in P6.BOUND}}

APPLY = {
    "gates": {"packet_sha256": PA.V3_SHA, "coo_half_signed": True, "cto_half_signed": True, "pins": dict(PA.FIRM_PIN), "holdings_snapshot_blob": dict(PA.FIRM_BLOB)},
    "remeasure": {"pins": dict(P6.PINS), "firms": {f: {"total_changed_nodes": PA.FIRM_TOTAL[f], "unattributed": 0, "all_signed_cash_rule": True,
                                                      "gate_attribution": "signed_exemption_repair" if f == "cottonwood" else "same",
                                                      "served_state": {"latest_date": "2026-10-12"}, "matches_packet": True} for f in P6.FIRMS}},
    "branch_b_reread": {f: {"bundle_version_id": P3.BRANCH_B_BUNDLE[f], "manifest_version_id": P3.BRANCH_B_MANIFEST[f],
                            "manifest_anchor_at_mint": ({"version_id": P3.BRANCH_B_MANIFEST[f], "newer_versions": 0} if f == "cottonwood" else
                                                        {"version_id": "FIREWRITTEN_" + f, "newer_versions": 1, "written_by_scheduled_fire": True,
                                                         "fire_date": "2026-10-15", "published_date": "2026-10-14"})} for f in P6.FIRMS},
    "digest_gate": {f: {"changed_members": members(f), "holdings_snapshot_blob": PA.FIRM_BLOB[f]} for f in P6.FIRMS},
    "window": {"last_fire_all_success_utc": "2026-10-15T14:31:00Z", "mint_start_utc": "2026-10-15T15:10:00Z", "mint_end_utc": "2026-10-15T15:40:00Z",
               "next_fire_utc": "2026-10-16T14:15:00Z"},
    "ledger": {"entry": "org/critical_paths/change_management/20261015_holdings_release.md", "legs": 5, "opened_before_first_mint": True},
    "mints": {f: {"bundle": P3.BUNDLES[f], "minted_from_pin": PA.FIRM_PIN[f], "before_version_id": P3.BRANCH_B_BUNDLE[f], "after_version_id": "NEWVERSION_" + f,
                  "after_sha256_equals_built": True} for f in P6.FIRMS},
    "business_date_statement": {"stated_at_utc": "2026-10-16T09:00:00Z", "fire_date": "2026-10-16", "t_minus_1": "2026-10-15", "per_firm_expected": {f: "2026-10-15" for f in P6.FIRMS}},
    "after_read": {
        "49financial": {"outcome": "STAMPED_T_MINUS_1", "stamp": "2026-10-15", "t1_partition_under_it": True},
        "cottonwood": {"outcome": "STAMPED_T_MINUS_1", "stamp": "2026-10-15", "t1_partition_under_it": True, "lost_accounts_listed": 1},
        "inflection": {"outcome": "HELD_NO_NEW_PUBLICATION", "absent_partition_named": "silver/positions snapshot_date=2026-10-15 absent", "frontier_unchanged": True,
                       "served_latest_date_before": "2026-10-13", "served_latest_date_after": "2026-10-13"}},
    "rule_after_read": {"cash_sub_read_cash": True}, "gap_2026_10_08": {"unchanged": True},
    "kernel_log_count": {"memory_read_done": True, "oom_count": 0}, "rollback_performed": False, "stop": None, "counters": dict(PA.APPLY_COUNTERS)}


def make_root(orion=None, apply=None, pkt=None, ledger=True):
    root = Path(tempfile.mkdtemp(prefix="c199_"))
    (root / "lib").mkdir()
    shutil.copy(REAL / "lib/trading_calendar.py", root / "lib/trading_calendar.py")
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    w(root, "pull/pull_orion.py", "import x\n\n\ndef pull_positions():\n    return 1\n")
    w(root, "pull/convert.py", "def convert_day():\n    return 2\n")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "base")
    w(root, P.REC, orion or ORION)
    w(root, PA.APPLY_REC, apply or APPLY)
    w(root, PA.V3, pkt if pkt is not None else packet())
    if ledger:
        w(root, "org/critical_paths/change_management/20261015_holdings_release.md", "ledger")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "work")
    return root


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=200)
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


bad = 0
root = make_root()
for cid in P.CHECKS:
    r = run(root, cid)
    ok = r == cid + " PASS"
    bad += 0 if ok else 1
    print("POSITIVE %s -> %s %s" % (cid, r, "" if ok else "<-- UNEXPECTED"))
shutil.rmtree(root, ignore_errors=True)


def neg(label, cid, orion=None, apply=None, pkt=None, ledger=True):
    global bad
    rt = make_root(orion, apply, pkt, ledger)
    r = run(rt, cid)
    ok = r == cid + " FAIL"
    bad += 0 if ok else 1
    print("NEGATIVE %-12s %-52s -> %s %s" % (cid, label, r, "" if ok else "<-- DID NOT FAIL"))
    shutil.rmtree(rt, ignore_errors=True)


def mo(fn):
    o = copy.deepcopy(ORION)
    fn(o)
    return o


def ma(fn):
    a = copy.deepcopy(APPLY)
    fn(a)
    return a


neg("a gap date not a trading day", "IB199-1-AC1", mo(lambda o: o["dates"]["2026-07-01"].update({"trading_day": False})))
neg("a target partition not empty", "IB199-1-AC1", mo(lambda o: o["dates"]["2026-09-28"]["empty_beforehand"].update({"silver_fact_positions": 1})))
neg("only one date", "IB199-1-AC1", mo(lambda o: o["dates"].pop("2026-09-28")))
neg("a measured stage with a wrong identifier", "IB199-1-AC2", mo(lambda o: o["pull_path"]["stages"][0].update({"identifier": "nope_function"})))
neg("a measured stage with a line past the file", "IB199-1-AC2", mo(lambda o: o["pull_path"]["stages"][1].update({"producer": "pull/convert.py:40"})))
neg("no silver_convert stage", "IB199-1-AC2", mo(lambda o: o["pull_path"].update({"stages": o["pull_path"]["stages"][:1]})))
neg("a cause with an unknown claim", "IB199-1-AC2", mo(lambda o: o["skip_cause"].update({"claim": "certain"})))
neg("an inferred cause with one evidence line", "IB199-1-AC2", mo(lambda o: o["skip_cause"].update({"evidence": ["one line of evidence only here"]})))
neg("a re-pull that writes another date", "IB199-1-AC3", mo(lambda o: o["repull_method"]["writes"].append(P.PREFIX + "bronze/positions/2026-09-29/")))
neg("a re-pull that writes outside the prefix", "IB199-1-AC3", mo(lambda o: o["repull_method"].update({"writes": ["s3://opal-data-assets/other/2026-07-01/"]})))
neg("a re-pull marked executed", "IB199-1-AC3", mo(lambda o: o["repull_method"].update({"executed": True})))
neg("a vendor request already sent", "IB199-1-AC3", mo(lambda o: o.update({"vendor_requests_sent": 1})))
neg("a long digit run", "IB199-1-AC3", mo(lambda o: o.update({"notes": ["account 123456789012"]})))
neg("a packet sha that is not v3's", "IB199-2-AC1", apply=ma(lambda a: a["gates"].update({"packet_sha256": "0" * 64})))
neg("the CTO half unsigned", "IB199-2-AC1", apply=ma(lambda a: a["gates"].update({"cto_half_signed": False})))
neg("49financial on pin 2", "IB199-2-AC1", apply=ma(lambda a: a["gates"]["pins"].update({"49financial": PA.PIN2})))
neg("49financial at 119", "IB199-2-AC1", apply=ma(lambda a: a["remeasure"]["firms"]["49financial"].update({"total_changed_nodes": 119})))
neg("an unattributed change", "IB199-2-AC1", apply=ma(lambda a: a["remeasure"]["firms"]["inflection"].update({"unattributed": 1})))
neg("a gate difference called nothing", "IB199-2-AC1", apply=ma(lambda a: a["remeasure"]["firms"]["49financial"].update({"gate_attribution": "signed_exemption_repair"})))
neg("a Branch B version off the packet", "IB199-2-AC1", apply=ma(lambda a: a["branch_b_reread"]["cottonwood"].update({"bundle_version_id": "OTHER"})))
neg("two newer manifest versions", "IB199-2-AC1", apply=ma(lambda a: a["branch_b_reread"]["inflection"]["manifest_anchor_at_mint"].update({"newer_versions": 2})))
neg("a newer manifest not dated T-1", "IB199-2-AC1", apply=ma(lambda a: a["branch_b_reread"]["inflection"]["manifest_anchor_at_mint"].update({"published_date": "2026-10-15"})))
neg("a member beyond the packet's moved set", "IB199-2-AC1", apply=ma(lambda a: a["digest_gate"]["cottonwood"]["changed_members"].append("data/a/extra.py")))
neg("a moved member missing from the mint", "IB199-2-AC1", apply=ma(lambda a: a["digest_gate"]["inflection"]["changed_members"].remove(PA.OPAL_UNID)))
neg("a mint inside 30 minutes of the fire", "IB199-2-AC2", apply=ma(lambda a: a["window"].update({"mint_end_utc": "2026-10-16T13:50:00Z"})))
neg("a mint before the day's fires", "IB199-2-AC2", apply=ma(lambda a: a["window"].update({"mint_start_utc": "2026-10-15T14:00:00Z"})))
neg("four ledger legs", "IB199-2-AC2", apply=ma(lambda a: a["ledger"].update({"legs": 4})))
neg("no ledger file", "IB199-2-AC2", ledger=False)
neg("a firm minted from the other pin", "IB199-2-AC2", apply=ma(lambda a: a["mints"]["49financial"].update({"minted_from_pin": PA.PIN2})))
neg("a mint that did not move the bundle", "IB199-2-AC2", apply=ma(lambda a: a["mints"]["inflection"].update({"after_version_id": P3.BRANCH_B_BUNDLE["inflection"]})))
neg("a wrong T-1", "IB199-2-AC2", apply=ma(lambda a: a["business_date_statement"].update({"t_minus_1": "2026-10-14"})))
neg("a statement after the fire", "IB199-2-AC2", apply=ma(lambda a: a["business_date_statement"].update({"stated_at_utc": "2026-10-16T15:00:00Z"})))
neg("a firm stamped the wrong date", "IB199-2-AC3", apply=ma(lambda a: a["after_read"]["49financial"].update({"stamp": "2026-10-14"})))
neg("a hold with the frontier moved", "IB199-2-AC3", apply=ma(lambda a: a["after_read"]["inflection"].update({"served_latest_date_after": "2026-10-14"})))
neg("Cottonwood with no lost account", "IB199-2-AC3", apply=ma(lambda a: a["after_read"]["cottonwood"].update({"lost_accounts_listed": 0})))
neg("the gap changed", "IB199-2-AC3", apply=ma(lambda a: a.update({"gap_2026_10_08": {"unchanged": False}})))
neg("a kernel count read with no count", "IB199-2-AC3", apply=ma(lambda a: a.update({"kernel_log_count": {"memory_read_done": True}})))
neg("a rollback performed", "IB199-2-AC3", apply=ma(lambda a: a.update({"rollback_performed": True})))
neg("a counter above its bound", "IB199-2-AC3", apply=ma(lambda a: a["counters"].update({"lambda_invokes": 1})))
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
