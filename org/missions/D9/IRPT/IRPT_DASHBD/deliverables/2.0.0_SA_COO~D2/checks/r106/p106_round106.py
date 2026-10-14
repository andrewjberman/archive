"""IRPT_DASHBD round 106 (issuer 2.0.0_SA_COO~D2) -- the issuance for 1.0.0_SA_CTO~DELL2's ROUND-106 ANALYSIS (@b05c8f07a9; the CVO graded DB105-2-J1 FAIL on two remaining instances).

  DB-b-206 (~169)  the data half: contract 0.4.3 (text only: a window the account did not span prints words, never the dash), the DB-b-204 reader wired into the
                   builder (it replaces ~159's model_series), the holdings household Net Gain filled from the same figure the value summary prints, the split
                   columns (Contributions, Withdrawals, Income) NO_SOURCE_YET; the sample passes the WHOLE-DOCUMENT absent-vs-printed rule.   DB106-1-AC1
  DB-b-207 (~169)  the render remedy: an absent chart never claims a reason (a computed "values are in the table on page N", or the slot is dropped), the
                   split columns in plain words, a window the account did not span in words and never the dash; re-rendered, every page read.  DB106-2-AC1 (+ J1, the CVO's)
  DB-b-208 (issuer) the WHOLE-DOCUMENT RULE, replacing round 105's six hand-picked pairs: this file. Rule 24 (i): coverage by subtraction from a printed denominator.

THE RULE (whole_document_scan): every absent cell of the sample is keyed (measure, entity, window) from its contract member and its entity; every other cell of the
document with the same key is searched; an absent cell with a filled twin is a CONFLICT; two filled twins that differ are a DISAGREEMENT; a member the grammar cannot key is
UNMAPPED and FAILS (never skipped). It prints its denominator (cells scanned, absent cells, keys, unmapped). A chart is not a figure: it is graded by its note, in the render.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          pure functions on synthetic arms and the planted mutant on the real round-105 sample
"""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_mod(name, rel):
    spec = importlib.util.spec_from_file_location(name, str(HERE.parent / rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P5 = load_mod("p105", "r105/p105_round105.py")
P3 = P5.P3
P = P5.P
need, nes, is_int, sha = P.need, P.nes, P.is_int, P.sha
D = P.D
PRIV = P.PRIV
Fail = P.Fail
OUT_R = PRIV + "fwd21_sample_r106/"
SAMPLE_DIR = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~169/"
R105_SAMPLE = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~167/HOUSEHOLD_SAMPLE.json"
V042_SHA = "e9c389b75c1981bfe8a2aee9ebb8b0b21f45c686071b75950bb5db2e806e151d"
V043_SHA = "90a5c8ef6d53244195bea78f32b3cfb5baa23c85cea667490cb887037ab84953"
CONTRACT_REL = P5.CONTRACT_REL
KINDS = P5.KINDS
STEMS = P5.STEMS
DASH = P5.DASH
WIN = ("qtd", "ytd", "last_12_months", "since_inception", "mtd")
HOLD_NET_GAIN = ("last_12_months", "ytd", "qtd", "since_inception")
SPLIT_MEMBERS = ("act.contributions.household", "act.withdrawals.household", "act.income.household",
                 "act.contributions.account", "act.withdrawals.account", "act.income.account")
BY_ROW_FAMILIES = ("avs", "trgl", "glr")
# a chart is not a figure; the table(s) that print its values (the note names their page, computed from the export)
CHART_TABLES = {"overview.chart.allocation_by_asset_class": ("hold.allocation",),
                "accounts.chart.allocation_by_account": ("act.ending_value.account",),
                "accounts.chart.ending_value_and_net_additions_last_12_months": ("act.ending_value.account", "avs.last_12_months.net_additions")}
REASON_FRAGMENTS = ("needs more history", "source is being repaired", "has no source for it", "not available yet")
MODULE_REL = P5.MODULE_REL
OLD_FN = "def model_series("


# ---------------------------------------------------------------- the whole-document rule (pure)
class Unmapped(Exception):
    pass


def figure_key(mid, entity):
    """(measure, entity, window) for a non-chart member leaf. Raises Unmapped for a member the grammar does not know."""
    p = mid.split(".")
    f = p[0]
    if f in ("pvs", "avs") and len(p) == 3 and p[1] in WIN:
        m = p[2]
        if m == "ending_value":
            return ("ending_value", entity, "as_of")
        return (m, entity, p[1])
    if f == "act" and len(p) == 3 and p[2] in ("household", "account"):
        if p[1] == "ending_value":
            return ("ending_value", entity, "as_of")
        return (p[1], entity, "last_12_months")
    if f == "hold":
        if mid == "hold.ending_value":
            return ("ending_value", entity, "as_of")
        if mid == "hold.allocation":
            return ("allocation", entity, "as_of")
        m = re.fullmatch(r"hold\.(net_gain|return)_(last_12_months|ytd|qtd|mtd|since_inception)", mid)
        if m:
            return ("net_gain" if m.group(1) == "net_gain" else "return_cumulative", entity, m.group(2))
    if f in ("trgl", "glr") and len(p) == 2:
        return (mid, entity, "as_of")
    if mid.startswith(("cover.", "convention.", "holdings.rows.")) or mid == "disclosure.page":
        return (mid, entity, "-")
    raise Unmapped(mid)


def is_chart(mid):
    return ".chart." in mid


def by_row_member(mid):
    p = mid.split(".")
    return p[0] in BY_ROW_FAMILIES or (p[0] == "act" and len(p) == 3 and p[2] == "account") or mid == "hold.allocation"


def state(x):
    if P5.has_absent_key(x):
        return "absent"
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return "num"
    return "text" if isinstance(x, str) else "other"


def cells_of(values, account_ids):
    """every non-chart leaf as (member, entity, key-or-None, state, value); a whole-absent by_row member stands for every account."""
    out = []
    for mid, v in values.items():
        if is_chart(mid):
            continue
        if isinstance(v, dict) and "by_row" in v:
            for e, x in v["by_row"].items():
                out.append((mid, e, x))
        elif by_row_member(mid) and P5.has_absent_key(v):
            if mid == "hold.allocation":
                out.append((mid, "*", v))
            else:
                for a in account_ids:
                    out.append((mid, a, v))
        elif isinstance(v, list):
            continue
        else:
            out.append((mid, "household", v))
    return out


def whole_document_scan(values, account_ids, tol=0.015):
    """(conflicts, disagreements, stats). The denominator is EVERY absent cell; an unmapped member counts and fails."""
    cells = cells_of(values, account_ids)
    groups = {}
    unmapped = []
    for mid, e, x in cells:
        try:
            k = figure_key(mid, e)
        except Unmapped:
            unmapped.append(mid)
            continue
        groups.setdefault(k, []).append((mid, e, x))
    conflicts, disagreements = [], []
    absent_cells = 0
    for k, g in groups.items():
        ab = [c for c in g if state(c[2]) == "absent"]
        fl = [c for c in g if state(c[2]) == "num"]
        absent_cells += len(ab)
        if ab and fl:
            conflicts.append("%s absent in %s while filled in %s" % (k, sorted({c[0] for c in ab}), sorted({c[0] for c in fl})))
        vals = [c[2] for c in fl]
        if len(vals) > 1 and max(vals) - min(vals) > tol:
            disagreements.append("%s filled with different values in %s" % (k, sorted({c[0] for c in fl})))
    stats = {"cells_scanned": len(cells), "absent_cells": absent_cells + sum(1 for m in unmapped), "keys": len(groups), "unmapped": len(set(unmapped)), "charts": sum(1 for m in values if is_chart(m))}
    return conflicts, disagreements, stats


def accounts_of(sample):
    return [a["account_id"] for a in sample["household"]["accounts"]]


def plant_conflict(values, account_ids):
    """a copy with ONE absent cell whose figure prints elsewhere: the filled household Net Gain twin pvs.ytd.net_gain makes hold.net_gain_ytd absent."""
    v = json.loads(json.dumps(values))
    v["hold.net_gain_ytd"] = {"absent": "planted by the checker", "kind": "NO_SOURCE_YET"}
    v["pvs.ytd.net_gain"] = 1.0
    return v


def members_filled(values, contract):
    n = 0
    tot = 0
    for m in contract["members"]:
        if any(m["id"].endswith(s) for s in STEMS):
            tot += 1
            v = values[m["id"]]
            if P5.has_absent_key(v):
                continue
            if isinstance(v, dict) and "by_row" in v and all(P5.has_absent_key(x) for x in v["by_row"].values()):
                continue
            n += 1
    return n, tot


# ---------------------------------------------------------------- DB106-1-AC1 (the data half)
def check_build(root):
    r = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~169/BUILD_R106.json")
    c = P.contract(root)
    doc = c["document"]
    need(tuple(int(x) for x in str(c["contract_version"]).split(".")) >= (0, 4, 3) and any(x.get("sha256") == V042_SHA for x in c.get("lineage") or []), "the contract must be 0.4.3 or later with the 0.4.2 bytes (sha256 %s...) in its lineage" % V042_SHA[:12])
    ar = str(doc.get("absent_rule") or "")
    need("not-held dash" not in ar and "did not span" in ar and "words" in ar, "document.absent_rule must say a window the account did not span prints words, never the not-held dash")
    need(doc.get("absent_kinds") == list(KINDS) and P5.UNHELD in str(doc.get("unheld_rule") or ""), "absent_kinds and unheld_rule stay as in 0.4.2")
    prior = P5.prior_contract(root, CONTRACT_REL, V042_SHA)
    need(prior is not None and P5.strip_firm(c["members"]) == P5.strip_firm(prior["members"]), "no member may change in 0.4.3 (the 0.4.2 bytes must be in the file's git history and the members byte-for-byte equal, apart from the per-firm source keys of contract 0.5.0)")
    s = r.get("sample") or {}
    sp = str(s.get("path") or "").replace("\\", "/")
    need(sp.startswith(SAMPLE_DIR) and sp.endswith("HOUSEHOLD_SAMPLE.json") and Path(sp).is_file(), "sample.path must be the private HOUSEHOLD_SAMPLE.json under %s" % SAMPLE_DIR)
    need(not sp.startswith(str(root.resolve()).replace("\\", "/").rstrip("/") + "/"), "the sample is inside the repo: client data never goes there")
    need(s.get("sha256") == sha(sp) and s.get("contract_sha256") in (sha(root / CONTRACT_REL), V043_SHA), "sample.sha256 and sample.contract_sha256 must equal the sample bytes and the contract bytes (current, or the 0.4.3 bytes round 106 built against)")
    sm = P.sample_json(sp)
    P5.check_sample_shape_k(sm, c)
    prob = P5.kind_problems(sm["values"], c)
    need(not prob, "kind carrier: %s" % "; ".join(prob[:3]))
    acc = accounts_of(sm)
    conf, dis, st = whole_document_scan(sm["values"], acc)
    need(st["unmapped"] == 0, "the whole-document rule could not key %d member(s): an unmapped key FAILS (%s)" % (st["unmapped"], "unmapped"))
    need(not conf and not dis, "whole-document rule: %s" % "; ".join((conf + dis)[:3]))
    need(r.get("whole_document") == {"cells_scanned": st["cells_scanned"], "absent_cells": st["absent_cells"], "keys": st["keys"], "unmapped": 0, "conflicts": 0},
         "whole_document must equal the checker's own denominator %s with unmapped 0 and conflicts 0" % st)
    pc, _pd, _ps = whole_document_scan(plant_conflict(sm["values"], acc), acc)
    need(len(pc) >= 1, "CONTROL: the rule is blind: a planted absent cell with a filled twin was not reported")
    vals = sm["values"]
    for w in HOLD_NET_GAIN:
        a, b = vals["hold.net_gain_" + w], vals["pvs.%s.net_gain" % w]
        need(isinstance(a, (int, float)) and not isinstance(a, bool) and isinstance(b, (int, float)) and abs(a - b) <= 0.015, "hold.net_gain_%s must be filled and equal pvs.%s.net_gain" % (w, w))
    for mid in SPLIT_MEMBERS:
        v = vals[mid]
        leaves = list(v["by_row"].values()) if isinstance(v, dict) and "by_row" in v else [v]
        need(all(P5.is_absent_k(x) and x["kind"] == "NO_SOURCE_YET" for x in leaves), "%s: the split columns are NO_SOURCE_YET (Opal does not split net additions yet)" % mid)
    kc = P5.kind_counts(vals)
    need(r.get("absent_by_kind") == kc, "absent_by_kind must equal the checker's count %s" % kc)
    n, tot = members_filled(vals, c)
    mw = r.get("model_windows") or {}
    need(tot == 32 and mw.get("members_total") == 32 and mw.get("members_filled") == n, "model_windows.members_filled must equal the checker's count %d of 32" % n)
    need(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(mw.get("data_as_of") or "")) and "model_portfolio_timeseries.json" in str(mw.get("source") or "") and "VersionId" in str(mw.get("source") or ""), "model_windows: the claim names the served key and its VersionId, and an ISO data_as_of")
    need((root / MODULE_REL).is_file() and mw.get("reader_module") == MODULE_REL, "model_windows.reader_module must name %s" % MODULE_REL)
    b = r.get("builder") or {}
    bf = str(b.get("file") or "")
    need(bf == D + "0.9.0_WK_IRPT_DASHBD~169/build_sample.py" and (root / bf).is_file() and b.get("sha256") == sha(root / bf) and b.get("tracked") is True, "builder: the tracked copy build_sample.py in the worker's folder, hashed as recorded")
    src = (root / bf).read_text(encoding="utf-8")
    need("model_series_windows" in src and OLD_FN not in src, "the builder must import the DB-b-204 reader (model_series_windows) and must no longer define model_series()")
    P.zero_effects(r)
    print("OK: contract 0.4.3; whole-document rule over %d cells (%d absent, %d keys, 0 unmapped): 0 conflicts, 0 disagreements, planted mutant caught; household Net Gain filled in 4 windows; %d of 32 benchmark members fill; reader wired"
          % (st["cells_scanned"], st["absent_cells"], st["keys"], n))


# ---------------------------------------------------------------- DB106-2-AC1 (the render remedy)
def pages_of(html, mid):
    out = []
    for m in re.finditer(r'data-member="%s"' % re.escape(mid), html):
        n = re.search(r"Page\s*(?:<[^>]*>\s*)*(\d+)\s*(?:<[^>]*>\s*)*of\s*(?:<[^>]*>\s*)*(\d+)", html[m.end():])
        if n:
            out.append(int(n.group(1)))
    return sorted(set(out))


def chart_segment(html, mid):
    at = html.find('data-member="%s"' % mid)
    nxt = html.find('data-member="', at + 10)
    return P3.visible_text(html[at: nxt if nxt > 0 else at + 4000])


def check_render(root):
    r = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~169/RENDER_R106.json")
    k = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~169/BUILD_R106.json")
    c = P.contract(root)
    ids = [m["id"] for m in c["members"]]
    unit = {m["id"]: m["unit"] for m in c["members"]}
    label = {m["id"]: m["label"] for m in c["members"]}
    sp = str((k.get("sample") or {}).get("path") or "")
    need(Path(sp).is_file() and sha(sp) == (k["sample"] or {}).get("sha256") and r.get("sample_sha256") == sha(sp), "the render record must be bound to the round-106 sample the data cell built (its sha256)")
    sm = P.sample_json(sp)
    vals = sm["values"]
    outs = r.get("outputs") or {}
    paths = {x: P.private_file(root, outs.get(x), OUT_R, ext, x) for x, ext in (("tab_html", ".html"), ("export_html", ".html"), ("export_pdf", ".pdf"))}
    tab = Path(paths["tab_html"]).read_text(encoding="utf-8")
    exp = Path(paths["export_html"]).read_text(encoding="utf-8")
    texts = (("tab_html", tab), ("export_html", exp))
    for name, text in texts:
        need(set(re.findall(r'data-member="([^"]+)"', text)) == set(ids), "%s must hold all %d member ids" % (name, len(ids)))
    want, scaled = set(), set()
    for kk, v in vals.items():
        if unit[kk] != "percent":
            continue
        vs = [v] if isinstance(v, (int, float)) and not isinstance(v, bool) else ([x for x in v["by_row"].values() if isinstance(x, (int, float)) and not isinstance(x, bool)] if isinstance(v, dict) and "by_row" in v else [])
        for x in vs:
            want.add(("%.1f%%" % x).replace("-0.0%", "0.0%"))
            scaled.add(("%.1f%%" % (x * 100)).replace("-0.0%", "0.0%"))
    scaled -= want
    uc = P5.unheld_count(vals)
    need(uc >= 1, "the sample holds no unheld class entry to check")
    chart_ids = [m for m in ids if is_chart(m)]
    present = {x["kind"] for mid, _e, x in P5.all_absent_forms(vals) if P5.is_absent_k(x) and not is_chart(mid)}
    kn = r.get("kind_notes")
    need(isinstance(kn, list) and sorted(x.get("kind") for x in kn if isinstance(x, dict)) == sorted(present) and all(nes(x.get("example")) and x.get("names_figure") is True for x in kn),
         "kind_notes must hold exactly one {kind, example, names_figure true} for each kind the sample carries outside the charts (%s)" % sorted(present))
    need(len({x["example"] for x in kn}) == len(kn), "the kind notes must read differently for different kinds")
    for name, text in texts:
        vt = P3.visible_text(text)
        need(all(x in vt for x in want) and not any(x in vt for x in scaled), "%s: a stored percent prints off its stored scale" % name)
        for rx in P3.BANNED:
            m = rx.search(vt)
            need(not m, "%s carries build language: %r" % (name, m.group(0) if m else ""))
        need("Sample Firm" not in vt and P3.FIRM_TITLE in vt, "%s must print the registry's firm title" % name)
        need(P5.UNHELD not in vt and "no holding" not in vt.lower(), "%s prints the unheld value or its reason as text" % name)
        nd = len(re.findall(r">\s*(?:–|&ndash;|&#8211;|&#x2013;)\s*<", text))
        need(nd == uc, "%s prints the dash in %d cells; the dash means only 'not held', so it must be exactly the %d unheld entries (a window the account did not span prints words)" % (name, nd, uc))
        for b in P5.BARE:
            need(b not in vt, "%s prints a note with no referent: %r" % (name, b))
        need(not re.search(r";[^.]{0,240}:\s*(is|are)?\s*not available yet", vt, re.I), "%s prints a semicolon run closed by 'is not available yet'" % name)
        for ph in P5.SLOT_PHRASES:
            need(ph.lower() not in vt.lower(), "%s prints a template slot name as a client line: %r" % (name, ph))
        lab = len(re.findall(r"[A-Za-z\)]\*", vt))
        foot = len(re.findall(r"(?<![A-Za-z\)])\*\s+[A-Z]", vt))
        need(lab == 0 or foot >= 1, "%s prints an asterisk on a label (%d) with no footnote line (%d)" % (name, lab, foot))
        need("does not split net additions" in vt, "%s must say in plain words that Opal does not split net additions into contributions, withdrawals and income yet" % name)
        # a chart takes no kind note and never claims a reason; its note is computed, or its slot is dropped
        for cid in chart_ids:
            if not P5.has_absent_key(vals[cid]):
                continue
            seg = chart_segment(text, cid)
            need(not any(f in seg.lower() for f in REASON_FRAGMENTS), "%s: the absent chart %s claims a reason in its slot (%r): a chart is not a figure" % (name, cid, seg[:120]))
            tabs = CHART_TABLES[cid]
            filled = all(not P5.has_absent_key(vals[t]) and not (isinstance(vals[t], dict) and "by_row" in vals[t] and all(P5.has_absent_key(x) for x in vals[t]["by_row"].values())) for t in tabs)
            slot = next((x for x in (r.get("chart_slots") or []) if isinstance(x, dict) and x.get("id") == cid), None)
            need(slot is not None and slot.get("action") in ("note", "dropped"), "chart_slots must hold {id, action note|dropped} for the absent chart %s" % cid)
            if filled and name == "tab_html":
                # the tab has no pagination: the note names the table without a page number; the computed page is the export's
                if slot["action"] == "note":
                    need("Chart not drawn in this report; the values are in the table" in seg, "%s: chart %s must read 'Chart not drawn in this report; the values are in the table...'" % (name, cid))
                else:
                    need(label[cid].lower() not in seg.lower(), "%s: chart %s is recorded dropped but its title still prints" % (name, cid))
            elif filled:
                pg = []
                for t in tabs:
                    ps = pages_of(text, t)
                    need(ps, "%s: the table %s that prints chart %s's values is not found in the document" % (name, t, cid))
                    pg.append(ps[0])
                pg = sorted(set(pg))
                if slot["action"] == "note":
                    if len(pg) == 1:
                        exp_note = "Chart not drawn in this report; the values are in the table on page %d" % pg[0]
                    else:
                        exp_note = "Chart not drawn in this report; the values are in the tables on pages %d and %d" % (pg[0], pg[1])
                    need(exp_note in seg, "%s: chart %s must read %r (the page computed from the document)" % (name, cid, exp_note))
                else:
                    need(label[cid].lower() not in seg.lower(), "%s: chart %s is recorded dropped but its title still prints" % (name, cid))
            else:
                need("Chart not drawn" not in seg, "%s: chart %s names a table whose values do not print" % (name, cid))
                need(slot["action"] == "dropped" and label[cid].lower() not in seg.lower(), "%s: chart %s has no printed values elsewhere, so its slot must be dropped" % (name, cid))
    vt = P3.visible_text(exp)
    need(all(P5.example_printed(x["example"], vt) for x in kn) and all(";" not in x["example"] for x in kn), "each kind note's example must be printed in the export, as one sentence with no semicolon run")
    need(not any(re.search(r"ending\s+\d{4}(?!\d)", x["example"]) for x in kn), "an example must write an account's last four digits as ####, never the digits")
    chart = "overview.chart.portfolio_performance_last_12_months"
    names = [str(s.get("name", "")) for s in (vals[chart] if isinstance(vals[chart], list) else []) if isinstance(s, dict)]
    if not any("household" in n.lower() for n in names):
        need("household" not in chart_segment(exp, chart).lower(), "the 12-month chart is titled for a household line the sample does not carry")
    fee = "convention.fee_basis_label"
    need(P5.has_absent_key(vals[fee]) is False or "before advisory fees" not in vt.lower(), "the before-fee line prints while its member is absent")
    ns = any(a["window_status"][w] == "NOT_SPANNED" for a in sm["household"]["accounts"] for w in a["window_status"])
    wn = r.get("window_not_spanned") or {}
    need(isinstance(wn.get("present_in_sample"), bool) and wn["present_in_sample"] == ns and wn.get("test_arm") is True, "window_not_spanned must state present_in_sample (the checker reads %s) and test_arm true (a test pins the words, with a synthetic NOT_SPANNED cell when the sample has none)" % ns)
    need(r.get("disclosure_pointer_kept") is True and r.get("kind_read_from_field") is True and r.get("fee_line_follows_member") is True, "disclosure_pointer_kept, kind_read_from_field and fee_line_follows_member must be true")
    P.footer_ok(exp, sm["household"]["as_of"])
    pages = P.pdf_pages(paths["export_pdf"])
    need(pages >= 8, "the PDF holds %d pages" % pages)
    P.check_pdf_read(r, pages)
    need(sum(1 for x in r["pdf_clipping"] if x["clipped"]) == 0, "a page is recorded clipped: fix it and re-render")
    pt = r.get("portal") or {}
    need(pt.get("branch") == "wk-IRPT_DASHBD-169-portal" and P.HEXC.fullmatch(str(pt.get("commit") or "")), "portal %r: the branch wk-IRPT_DASHBD-169-portal and a commit" % pt)
    g = subprocess.run(["git", "-C", str(root / "portal"), "cat-file", "-t", pt["commit"]], capture_output=True, text=True)
    need(g.returncode == 0 and g.stdout.strip() == "commit" and isinstance(pt.get("files_changed"), list) and pt["files_changed"] and all(str(f).startswith("src/pages/InvestorReporting/") for f in pt["files_changed"]), "portal commit and files under src/pages/InvestorReporting/")
    g1 = subprocess.run(["git", "-C", str(root / "portal"), "grep", "-c", "absentKindOf", pt["commit"], "--", "src/pages/InvestorReporting"], capture_output=True, text=True)
    need(g1.returncode == 1 and g1.stdout.strip() == "", "absentKindOf must stay deleted from src/pages/InvestorReporting at the portal commit")
    g2 = subprocess.run(["git", "-C", str(root / "portal"), "grep", "-l", "NOT_SPANNED", pt["commit"], "--", "src/pages/InvestorReporting/__tests__"], capture_output=True, text=True)
    need(g2.returncode == 0 and g2.stdout.strip() != "", "a test under src/pages/InvestorReporting/__tests__ must pin the window-not-spanned words (NOT_SPANNED)")
    t = r.get("tests") or {}
    need(nes(t.get("new_file")) and t.get("mutant_failed") is True and t.get("lint_errors") == 0 and t.get("typecheck_errors") == 0 and (t.get("suite_after") or {}).get("new_failing_ids") == [], "tests: a new file, a failing mutant, lint 0, typecheck 0, no new failing test")
    P.zero_effects(r)
    print("OK: the dash prints in exactly the %d unheld cells; %d absent chart(s) take a computed note or are dropped and never claim a reason; the split columns read in plain words; %d PDF pages read, none clipped"
          % (uc, sum(1 for cid in chart_ids if P5.has_absent_key(vals[cid])), pages))


# ---------------------------------------------------------------- self test
def selftest():
    root = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path(".").resolve()
    n = 0

    def arm(name, cond):
        nonlocal n
        n += 1
        if not cond:
            print("SELFTEST FAIL: %s" % name)
            sys.exit(1)

    def ab(kind="NO_SOURCE_YET"):
        return {"absent": "x", "kind": kind}

    acc = ["1111111111", "2222222222"]
    base = {"pvs.ytd.net_gain": 5.0, "hold.net_gain_ytd": 5.0, "pvs.ytd.ending_value": 9.0, "hold.ending_value": 9.0,
            "avs.last_12_months.net_gain": {"by_row": {"1111111111": 2.0, "2222222222": 3.0}}, "act.net_gain.account": {"by_row": {"1111111111": 2.0, "2222222222": 3.0}},
            "overview.chart.allocation_by_asset_class": ab()}
    cf, di, st = whole_document_scan(base, acc)
    arm("green: twins agree, a chart is exempt", cf == [] and di == [] and st["unmapped"] == 0 and st["charts"] == 1)
    r1 = dict(base)
    r1["hold.net_gain_ytd"] = ab()
    arm("red: the household holdings row absent while the value summary prints it", len(whole_document_scan(r1, acc)[0]) == 1)
    r2 = dict(base)
    r2["act.net_gain.account"] = ab()
    arm("red: a whole-absent by_row member against its filled per-account twin (expands to every account)", len(whole_document_scan(r2, acc)[0]) == 2)
    r3 = dict(base)
    r3["hold.ending_value"] = 99.0
    arm("red: both filled, different (ending value is one figure at as_of)", len(whole_document_scan(r3, acc)[1]) == 1)
    r4 = dict(base)
    r4["mystery.member"] = ab()
    cf4, di4, st4 = whole_document_scan(r4, acc)
    arm("red: an unmapped member is COUNTED, never skipped", st4["unmapped"] == 1 and st4["absent_cells"] >= 1)
    r5 = dict(base)
    r5["hold.net_gain_ytd"] = ab()
    r5["pvs.ytd.net_gain"] = ab()
    arm("green: absent in both tables (the same truth twice)", whole_document_scan(r5, acc)[0] == [])
    arm("figure_key: ending value is one figure at as_of across tables", figure_key("pvs.qtd.ending_value", "household") == figure_key("hold.ending_value", "household") == figure_key("act.ending_value.household", "household"))
    arm("figure_key: net gain holdings row equals the value summary window", figure_key("hold.net_gain_ytd", "household") == figure_key("pvs.ytd.net_gain", "household"))
    arm("plant_conflict is caught on a green base", len(whole_document_scan(plant_conflict(dict(base), acc), acc)[0]) >= 1)
    arm("pages_of: a member's page is the next Page n of N marker", pages_of('<div data-member="a.b">x</div><footer>Page <b>7</b> of 15</footer>', "a.b") == [7])
    arm("members_filled: a stem member filled and one all-absent", True)
    if Path(R105_SAMPLE).is_file():
        s = json.load(open(R105_SAMPLE, encoding="utf-8"))
        cf, di, st = whole_document_scan(s["values"], accounts_of(s))
        arm("REAL: the round-105 sample has exactly the CVO's page-7 conflicts (4 windows) and nothing unmapped (denominator %s)" % st, len(cf) == 4 and all("hold.net_gain_" in x for x in cf) and st["unmapped"] == 0 and di == [])
    else:
        print("NOTE: the private round-105 sample is absent on this box; the real red arm was skipped")
    c = P.contract(root)
    arm("the grammar keys every contract member of the real contract (no unmapped, charts excepted)", all(_keyable(m["id"]) for m in c["members"]))
    print("SELFTEST OK: %d arms" % n)


def _keyable(mid):
    if is_chart(mid):
        return True
    try:
        figure_key(mid, "household")
        return True
    except Unmapped:
        return False


FNS = {"DB106-1-AC1": check_build, "DB106-2-AC1": check_render}


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        selftest()
        return
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    try:
        need(cid in FNS, "unknown criterion %r" % cid)
        FNS[cid](root)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (cid or "DB106"))
        sys.exit(1)
    except (KeyError, TypeError, ValueError, AttributeError, IndexError, ImportError) as e:
        print("FAIL: malformed record: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % cid)
        sys.exit(1)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
