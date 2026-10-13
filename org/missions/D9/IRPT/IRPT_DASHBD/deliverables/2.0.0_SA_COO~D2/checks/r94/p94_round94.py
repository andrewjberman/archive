"""IRPT_DASHBD round 94 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msg 7181 / 7192, round-94 analysis: FWD-21, the default performance report in one Opal Shape,
on the baseline of the Black Diamond 49 Financial Performance Report (structure only, deliverables/1.0.0_SA_CTO~DELL2/BD_FINANCIAL_PERFORMANCE_REPORT_BASELINE_SCHEMA_20261013.md).

Cells (all LOCAL or DEV-only; none touches the gold Lambda; counts and synthetic data only in the repo):
  DB-b-174 (~140) the contract org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json and its gap table.            DB94-1-AC1
  DB-b-175 (~141) one 49 Financial household built into the contract shape from gold; writes nothing served.             DB94-2-AC1
  DB-b-176 (~142) the Performance tab renders the contract shape in the baseline's section order (portal candidate).     DB94-3-AC1
  DB-b-177 (~143) the export document renders the same shape in the same order (portal candidate).                       DB94-4-AC1
  DB-b-178 (~144) the smoke fixes: export status chain and modal width; FDRXX is CASH; YTD from the first measured day.  DB94-5-AC1

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
       python <this file> <repo_root> --ids   prints the 117 member ids the contract must hold, one per line.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_DASHBD/"
D = PROJ + "deliverables/"
CONTRACT = "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"
SECTIONS = ("cover", "portfolio_overview", "summary_of_portfolio_accounts", "holdings_overview", "taxable_realized_gain_loss_ytd", "account_overview",
            "gain_loss_review_by_account", "disclosure")
VS_COLS = ("qtd", "ytd", "last_12_months", "since_inception")
VS_ROWS = ("beginning_value", "net_additions", "net_gain", "ending_value", "return_cumulative", "benchmark_ultra_short_term", "benchmark_short_term",
           "benchmark_intermediate_term", "benchmark_long_term")
ACT_COLS = ("beginning_value", "contributions", "withdrawals", "net_gain", "income", "ending_value")
ACT_ROWS = ("household", "account")
HOLD_COLS = ("ending_value", "allocation") + tuple("%s_%s" % (m, w) for w in ("last_12_months", "ytd", "qtd", "mtd", "since_inception") for m in ("net_gain", "return"))
TRGL_COLS = ("cost_basis", "proceeds", "realized_short_term", "realized_long_term", "total_realized_gl")
GLR_COLS = ("cost_basis", "ending_value", "total_realized_gl", "total_unrealized_gl")
EXTRA = ("cover.household_name", "cover.account_list", "cover.as_of_date", "overview.chart.allocation_by_asset_class", "overview.chart.portfolio_performance_last_12_months",
         "accounts.chart.allocation_by_account", "accounts.chart.ending_value_and_net_additions_last_12_months", "holdings.rows.class_hierarchy",
         "convention.fee_basis_label", "convention.inception_per_household_and_account", "convention.not_held_for_entire_period", "disclosure.page")


def required_ids():
    ids = []
    for t in ("pvs", "avs"):
        ids += ["%s.%s.%s" % (t, c, r) for r in VS_ROWS for c in VS_COLS]
    ids += ["act.%s.%s" % (c, r) for r in ACT_ROWS for c in ACT_COLS]
    ids += ["hold.%s" % c for c in HOLD_COLS]
    ids += ["trgl.%s" % c for c in TRGL_COLS]
    ids += ["glr.%s" % c for c in GLR_COLS]
    ids += list(EXTRA)
    return ids


VENDOR = re.compile(r"black\s*diamond|blackdiamond|orion|schwab|commonwealth|bloomberg|ycharts|fidelity", re.I)
RUN = re.compile(r"\d{8,}")
HEX64 = re.compile(r"[0-9a-f]{64}")
HEX40 = re.compile(r"[0-9a-f]{40}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def long_digit_runs(obj, name=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not str(k).endswith("sha256") and str(k) not in ("commit", "portal_commit"):
                hits += long_digit_runs(v, name + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += long_digit_runs(v, "%s/%d" % (name, i))
    elif isinstance(obj, str) and RUN.search(obj):
        hits.append(name)
    return hits


def load(root, rel):
    p = root / rel
    need(p.is_file(), "no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def code_ok(root, code, under=PROJ):
    f = str((code or {}).get("file") or "")
    need(f.startswith(under) and code.get("tracked") is True and HEX64.fullmatch(str(code.get("sha256") or "")), "code %r" % code)
    need((root / f).is_file() and hashlib.sha256((root / f).read_bytes()).hexdigest() == code["sha256"], "code file missing or its sha256 differs from the record")
    return f


def contract_members(root):
    """(contract dict, {member id: member}, sha256 of its bytes). Validates the contract against the baseline structure."""
    p = root / CONTRACT
    need(p.is_file(), "no %s" % CONTRACT)
    raw = p.read_bytes()
    c = json.loads(raw.decode("utf-8"))
    need(c.get("project") == "IRPT_DASHBD" and isinstance(c.get("contract_version"), str) and c["contract_version"], "contract needs project IRPT_DASHBD and a contract_version")
    secs = c.get("sections")
    need(isinstance(secs, list) and tuple(s.get("id") for s in secs) == SECTIONS, "sections must be exactly %r, in this order" % (SECTIONS,))
    need(not VENDOR.search(raw.decode("utf-8")), "the contract names a vendor or a custodian (it is vendor-agnostic)")
    doc = c.get("document")
    need(isinstance(doc, dict) and str(doc.get("shape") or "").strip() and isinstance(doc.get("row_dimensions"), dict) and {"account", "class_hierarchy"} <= set(doc["row_dimensions"]),
         "document {shape, row_dimensions {account, class_hierarchy, ...}} is required: how a FILLED report is laid out (the sample builder writes it, the tab and the export read it)")
    ms = c.get("members")
    need(isinstance(ms, list) and ms, "members must be a non-empty list")
    by = {}
    for m in ms:
        i = m.get("id")
        need(isinstance(i, str) and i not in by, "member id %r is missing or duplicated" % (i,))
        by[i] = m
    req = required_ids()
    miss = [i for i in req if i not in by]
    extra = [i for i in by if i not in set(req)]
    need(not miss, "members missing for baseline cells: %s (%d missing)" % (miss[:4], len(miss)))
    need(not extra, "members the baseline does not have: %s" % extra[:4])
    for i, m in by.items():
        need(m.get("section") in SECTIONS, "member %s needs a section from the list" % i)
        s = m.get("source")
        if s == "ABSENT":
            need(str(m.get("reason") or "").strip() != "", "member %s is ABSENT and needs a reason" % i)
            need("default" not in m and m.get("value") in (None, ""), "member %s is ABSENT and must carry no value (never zero)" % i)
        else:
            need(isinstance(s, dict) and str(s.get("contract") or "").startswith("org/standards/") and str(s.get("field") or "").strip() != "", "member %s needs a source {contract, field} or ABSENT" % i)
            sp = root / s["contract"]
            need(sp.is_file(), "member %s names a source contract that does not exist: %s" % (i, s["contract"]))
            need(s["field"] in sp.read_bytes().decode("utf-8"), "member %s: field %r is not in %s" % (i, s["field"], s["contract"]))
    sha = hashlib.sha256(raw).hexdigest()
    lin = c.get("lineage")
    accepted = {sha}
    if lin is not None:
        need(isinstance(lin, list) and all(isinstance(x, dict) and HEX64.fullmatch(str(x.get("sha256") or "")) and str(x.get("contract_version") or "").strip() for x in lin),
             "lineage must be a list of {contract_version, sha256}")
        accepted |= {x["sha256"] for x in lin}
    CONTRACT_ACCEPTED[:] = sorted(accepted)
    return c, by, sha


CONTRACT_ACCEPTED = []
RETURN_CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json"
V010_SHA = "53fce40546882c90b634decb91ec5176a54ddf3c3b4622270bfc5cc35f66991b"
WINDOWS = ("qtd", "ytd", "last_12_months", "since_inception")
RESOURCED_ROWS = ("beginning_value", "ending_value", "net_additions", "net_gain")


def resourced_ids():
    ids = ["%s.%s.%s" % (t, w, r) for t in ("pvs", "avs") for w in WINDOWS for r in RESOURCED_ROWS]
    ids += ["avs.%s.return_cumulative" % w for w in WINDOWS]
    return ids


def check_resource(root):
    """DB94-6: the contract is re-sourced to account_return_daily for every window figure that table can derive (CTO msg 7289)."""
    c, by, sha = contract_members(root)
    ver = str(c.get("contract_version") or "")
    need(ver != "0.1.0" and ver.count(".") == 2 and tuple(int(x) for x in ver.split(".")) > (0, 1, 0), "contract_version %r must be above 0.1.0" % ver)
    need(V010_SHA in {x["sha256"] for x in (c.get("lineage") or [])}, "lineage must list the 0.1.0 contract's sha256 (%s...)" % V010_SHA[:12])
    n = 0
    for i in resourced_ids():
        m = by[i]
        s = m["source"]
        need(isinstance(s, dict) and s.get("contract") == RETURN_CONTRACT and str(s.get("fold") or "").strip() != "", "member %s must be sourced from the account return table, with a fold text" % i)
        n += 1
    contrib = [i for i in by if i.startswith("act.") and by[i]["source"] != "ABSENT" and by[i]["source"]["contract"] != "org/standards/IRPT_DASHBD_ACCOUNT_ACTIVITY_DAILY_CONTRACT.json"]
    need(not contrib, "activity-summary members %s must keep their own source or ABSENT" % contrib[:3])
    folder = D + "0.9.0_WK_IRPT_DASHBD~145"
    g = load(root, folder + "/GAP_TABLE.json")
    absent = sum(1 for m in by.values() if m["source"] == "ABSENT")
    t = g.get("totals") or {}
    need(g.get("contract_sha256") == sha and t.get("members") == len(by) and t.get("absent") == absent and t.get("sourced") == len(by) - absent, "the regenerated gap table must be bound to the contract's bytes and equal its totals")
    need(is_int(g.get("resourced_members")) and g["resourced_members"] == n, "gap table resourced_members %r must equal %d" % (g.get("resourced_members"), n))
    need(isinstance(g.get("identity_by_window_sketch"), str) and g["identity_by_window_sketch"].strip() != "", "gap table needs identity_by_window_sketch (how net gain follows from the three other rows)")
    rd = g.get("reads") or {}
    need(rd.get("vendor_calls") == 0 and rd.get("s3_reads") == 0 and rd.get("s3_writes") == 0 and rd.get("secret_reads") == 0 and g.get("served_values_changed") is False, "reads %r" % rd)
    hits = long_digit_runs(g)
    need(not hits, "the gap table holds a run of 8 or more digits at %s" % hits[:3])
    print("OK: contract %s re-sourced: %d window members now read the account return table; %d of %d members sourced, %d ABSENT" % (ver, n, len(by) - absent, len(by), absent))


def check_contract(root):
    folder = D + "0.9.0_WK_IRPT_DASHBD~140"
    c, by, sha = contract_members(root)
    # a re-sourced contract (DB-b-179) carries the newest gap table in the later folder, bound to the current bytes
    if (root / (D + "0.9.0_WK_IRPT_DASHBD~145/GAP_TABLE.json")).is_file():
        folder = D + "0.9.0_WK_IRPT_DASHBD~145"
    g = load(root, folder + "/GAP_TABLE.json")
    n = len(by)
    absent = sum(1 for m in by.values() if m["source"] == "ABSENT")
    need(g.get("contract_sha256") == sha, "gap table is not bound to the contract's bytes")
    t = g.get("totals") or {}
    need(t.get("members") == n and t.get("absent") == absent and t.get("sourced") == n - absent, "gap table totals %r differ from the contract (members %d, sourced %d, absent %d)" % (t, n, n - absent, absent))
    bs = g.get("by_section") or {}
    need(set(bs) == set(SECTIONS), "by_section must hold exactly the eight sections")
    for s in SECTIONS:
        ms = [m for m in by.values() if m["section"] == s]
        a = sum(1 for m in ms if m["source"] == "ABSENT")
        need(bs[s] == {"members": len(ms), "sourced": len(ms) - a, "absent": a}, "by_section[%s] %r differs from the contract" % (s, bs[s]))
    need(g.get("vendor_free") is True and g.get("baseline_cells_required") == n, "vendor_free true and baseline_cells_required equal to the member count are required")
    need(isinstance(g.get("fwd20_map_folded"), bool), "fwd20_map_folded must be a bool (true when the FWD-20 map was found and folded in)")
    need(isinstance(g.get("sibling_contracts_read"), list) and len(g["sibling_contracts_read"]) >= 3 and all((root / x).is_file() for x in g["sibling_contracts_read"]), "sibling_contracts_read must list 3 or more existing contracts")
    rd = g.get("reads") or {}
    need(rd.get("vendor_calls") == 0 and rd.get("s3_reads") == 0 and rd.get("s3_writes") == 0 and rd.get("secret_reads") == 0 and g.get("served_values_changed") is False, "reads %r" % rd)
    hits = long_digit_runs(g)
    need(not hits, "the gap table holds a run of 8 or more digits at %s" % hits[:3])
    print("OK: contract of %d members over %d sections (%d sourced, %d ABSENT), vendor-free, bound by hash" % (n, len(SECTIONS), n - absent, absent))


def check_sample(root):
    folder = D + "0.9.0_WK_IRPT_DASHBD~141"
    _c, by, sha = contract_members(root)
    r = load(root, folder + "/HOUSEHOLD_SAMPLE_BUILD.json")
    code_ok(root, r.get("code"))
    need(r.get("contract_sha256") in CONTRACT_ACCEPTED, "the record is not bound to the contract's bytes or to one of its lineage versions")
    hh = r.get("household") or {}
    need(is_int(hh.get("accounts")) and hh["accounts"] >= 2 and HEX64.fullmatch(str(hh.get("household_ref_sha256") or "")), "household %r needs 2 or more accounts and a hashed reference" % hh)
    m = r.get("members") or {}
    need(m.get("total") == len(by) and is_int(m.get("filled")) and is_int(m.get("absent")) and m["filled"] + m["absent"] == m["total"], "members %r must sum to the contract's %d" % (m, len(by)))
    contract_absent = sum(1 for x in by.values() if x["source"] == "ABSENT")
    need(m["absent"] >= contract_absent, "absent %d cannot be fewer than the contract's own ABSENT members (%d)" % (m["absent"], contract_absent))
    need(r.get("absent_members_never_zero") is True and r.get("shape_valid_against_contract") is True, "absent_members_never_zero and shape_valid_against_contract must be true")
    idn = r.get("identity") or {}
    need(is_int(idn.get("checks")) and idn["checks"] >= 4 and idn.get("passed") == idn["checks"] and idn.get("tolerance_dollars") == 1, "identity %r: every beginning + net additions + net gain = ending check must pass within 1 dollar" % idn)
    rd = r.get("reads") or {}
    need(is_int(rd.get("s3_reads")) and rd["s3_reads"] > 0 and rd.get("s3_writes") == 0 and rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0, "reads %r" % rd)
    need(r.get("sample_kept_private") is True and r.get("served_values_changed") is False, "sample_kept_private true and served_values_changed false are required")
    hits = long_digit_runs(r)
    need(not hits, "the record holds a run of 8 or more digits at %s" % hits[:3])
    print("OK: one household of %d accounts built into the contract shape: %d members filled, %d ABSENT; %d identity checks passed" % (hh["accounts"], m["filled"], m["absent"], idn["checks"]))


def build_gates(r, allowed):
    t = r.get("test") or {}
    need(str(t.get("file") or "").strip() and t.get("mutant_failed") is True, "test needs its file and a mutant that failed")
    need(r.get("lint_errors") == 0 and r.get("typecheck_errors") == 0, "lint_errors %r, typecheck_errors %r" % (r.get("lint_errors"), r.get("typecheck_errors")))
    sb, sa = r.get("suite_base") or {}, r.get("suite_after") or {}
    need(is_int(sb.get("fail")) and is_int(sa.get("fail")) and sa["fail"] <= sb["fail"] and sa.get("new_failing_ids") == [], "suite: base fail %r, after fail %r, new_failing_ids %r" % (sb.get("fail"), sa.get("fail"), sa.get("new_failing_ids")))
    need(HEX40.fullmatch(str(r.get("portal_commit") or "")), "portal_commit %r" % r.get("portal_commit"))
    pf = [str(x).replace("\\", "/") for x in (r.get("product_files_changed") or [])]
    need(pf and all(any(a in x for a in allowed) for x in pf), "product_files_changed %r must be non-empty and each under %s" % (pf, allowed))
    need(r.get("synthetic_fixture_only") is True and r.get("pushed") is False, "synthetic_fixture_only true and pushed false are required")
    hits = long_digit_runs(r)
    need(not hits, "the record holds a run of 8 or more digits at %s" % hits[:3])


def shots_ok(r, folder):
    shots = r.get("screenshots") or []
    need(shots and r.get("screenshot_read") is True and all((folder / str(x)).is_file() for x in shots), "screenshots must each exist in the worker's folder and be read")


def check_render(root, which):
    w, name, allowed = {"tab": ("0.9.0_WK_IRPT_DASHBD~142", "TAB_RENDER.json", ("portal/src/pages/InvestorReporting/dashboard/report/", "src/pages/InvestorReporting/dashboard/report/")),
                        "export": ("0.9.0_WK_IRPT_DASHBD~143", "EXPORT_RENDER.json", ("portal/src/pages/InvestorReporting/render/performance/report/", "src/pages/InvestorReporting/render/performance/report/"))}[which]
    folder = root / (D + w)
    r = load(root, D + w + "/" + name)
    _c, by, sha = contract_members(root)
    need(r.get("contract_sha256") in CONTRACT_ACCEPTED, "the record is not bound to the contract's bytes or to one of its lineage versions")
    need(tuple(r.get("sections_rendered_in_order") or ()) == SECTIONS, "sections_rendered_in_order must be %r" % (SECTIONS,))
    for k in ("absent_rendered_in_words", "fee_basis_label_present", "no_blank_figure", "same_layout_for_every_firm"):
        need(r.get(k) is True, "%s must be true" % k)
    need(is_int(r.get("members_rendered")) and r["members_rendered"] == len(by), "members_rendered %r must equal the contract's %d" % (r.get("members_rendered"), len(by)))
    if which == "export":
        need(r.get("sections_match_tab_record") is True, "sections_match_tab_record must be true")
    build_gates(r, allowed)
    shots_ok(r, folder)
    print("OK: %s renders %d members in the baseline's %d sections; test with a mutant, lint 0, typecheck 0, suite not worse, screenshots read" % (which, r["members_rendered"], len(SECTIONS)))


def check_smoke(root):
    w = D + "0.9.0_WK_IRPT_DASHBD~144"
    folder = root / w
    r = load(root, w + "/SMOKE_FIXES.json")
    ex, yt, fd = r.get("export") or {}, r.get("ytd") or {}, r.get("fdrxx") or {}
    fc = ex.get("failing_call") or {}
    need(str(fc.get("file") or "").strip() and is_int(fc.get("line")) and isinstance(ex.get("portal_side"), bool), "export.failing_call {file, line} and export.portal_side are required: the status chain is read to the failing call")
    if ex["portal_side"]:
        need(ex.get("fixed") is True and (ex.get("test") or {}).get("mutant_failed") is True, "a portal-side export failure must be fixed, with a test and a mutant that failed")
    else:
        need(str(ex.get("blocking_row") or "").strip() != "" and ex.get("fixed") is False, "an export failure outside the portal is named in a row and not fixed here")
    mo = ex.get("modal") or {}
    need(is_int(mo.get("width_px_before")) and is_int(mo.get("width_px_after")) and mo["width_px_after"] > mo["width_px_before"] and mo.get("horizontal_scroll_after") is False and mo.get("tested") is True,
         "modal %r: wider after than before, no horizontal scroll after, tested" % mo)
    need(str(yt.get("label_example") or "").lower().startswith("ytd (from") and yt.get("never_blank") is True and yt.get("no_day_stays_not_measured") is True and (yt.get("test") or {}).get("mutant_failed") is True,
         "ytd: a label 'YTD (from ...)', never blank, a window with no measured day stays 'not measured', tested with a mutant")
    if fd.get("assignment_site_in_portal") is True:
        need(fd.get("money_market_maps_to_cash") is True and (fd.get("test") or {}).get("mutant_failed") is True, "fdrxx: a portal-side mapping must send money-market funds to CASH, tested with a mutant")
    else:
        site = fd.get("assignment_site") or {}
        need(str(site.get("file") or "").strip() and is_int(site.get("line")) and str(fd.get("blocking_row") or "").strip() != "" and fd.get("money_market_maps_to_cash") is False,
             "fdrxx: a class assigned outside the portal is named (file, line) in a row and left unchanged here")
    build_gates(r, ("portal/src/pages/InvestorReporting/", "src/pages/InvestorReporting/"))
    shots_ok(r, folder)
    print("OK: export failing call read (portal side %s), modal %d px to %d px, YTD label %r, FDRXX in the portal: %s"
          % (ex["portal_side"], mo["width_px_before"], mo["width_px_after"], yt["label_example"][:40], str(fd.get("assignment_site_in_portal") is True).lower()))


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    if cid == "--ids":
        for i in required_ids():
            print(i)
        return
    fns = {"DB94-1-AC1": check_contract, "DB94-2-AC1": check_sample, "DB94-3-AC1": lambda r: check_render(r, "tab"),
           "DB94-4-AC1": lambda r: check_render(r, "export"), "DB94-5-AC1": check_smoke, "DB94-6-AC1": check_resource}
    try:
        need(cid in fns, "unknown criterion %r" % cid)
        fns[cid](root)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (cid or "DB94"))
        sys.exit(1)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
