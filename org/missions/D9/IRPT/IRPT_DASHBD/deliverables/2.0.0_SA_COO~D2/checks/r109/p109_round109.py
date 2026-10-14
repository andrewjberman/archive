"""IRPT_DASHBD round 109 (issuer 2.0.0_SA_COO~D2) -- the issuance for 1.0.0_SA_CTO~DELL2's ROUND-109 ANALYSIS (@a80ef4f7c7; the first Inflection render).

  DB-b-213 (issuer, DIRECT ACT, done first) the W171-S4 read gate: the four alien Orion silver objects are Inflection's own surplus (ALIEN_READ_R109.json), so the render proceeds
                   with the guard state named.
  DB-b-214 (~173)  the Inflection SAMPLE: one household built in memory from Inflection's own silver (account_dim adapter + Orion/Eclipse reads), the household return stays absent by contract (the CTO's decision to fill it)
                   client-keyed performance with its source, account returns NO_SOURCE_YET in plain words, lots NO_LOTS in plain words, passing the whole-document rule.   DB109-1-AC1
  DB-b-215 (~173)  the RENDER of that sample through the 49 Financial layout and the whole-document and note-level rules, in the Inflection firm title; private folder only. DB109-2-AC1 (+ J1, the CVO's)
  DB-b-216 (~174)  the ACCOUNT-RETURN DERIVATION (the method of the existing daily TWR engine as a pure function, from Orion positions and transactions) and the TIE-OUT READ
                   (accounts aggregated per client against Orion's client return: the gap distribution per window, no tolerance assumed); nothing written.            DB109-3-AC1

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers on synthetic arms
"""
import hashlib
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


P7 = load_mod("p107", "r107/p107_round107.py")
P8 = load_mod("p108", "r108/p108_round108.py")
P6, P5, P3, P = P7.P6, P7.P5, P7.P3, P7.P
need, nes, is_int, sha = P.need, P.nes, P.is_int, P.sha
D = P.D
PRIV = P.PRIV
Fail = P.Fail
note_level = P7.note_level
is_chart, pages_of, chart_segment = P7.is_chart, P7.pages_of, P7.chart_segment
CHART_TABLES7, CHART3, REASON_FRAGMENTS = P7.CHART_TABLES7, P7.CHART3, P7.REASON_FRAGMENTS
whole_document_scan, accounts_of, figure_key = P6.whole_document_scan, P6.accounts_of, P6.figure_key
OUT_R9 = PRIV + "fwd21_sample_r109/"
SAMPLE_DIR9 = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~173/"
TWR_DIR = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~174/"
DIM_DRY = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~171/ACCOUNT_DIM_DRY_RUN.parquet"
ALIEN_REC = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/ALIEN_READ_R109.json"
ACCT_WORDS = "Account-level returns are not available for this firm yet."
LOTS_WORDS = "Lot-level detail is not available for this account yet."
BINS = ("lt_5bp", "5_25bp", "25_100bp", "ge_100bp")
TIE_WINDOWS = ("qtd", "ytd", "last_12_months", "since_inception")
TWR_MODULE = "data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_return_daily.py"
TWR_TEST = "data/assets/scripts/gold/irpt_reporting/tests/test_inflection_account_return_daily.py"
ENGINE = "data/assets/scripts/gold/irpt_reporting/account_return_daily.py"
RET_CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json"
ADAPTER = "data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_dim.py"


def firm_title():
    r = json.loads(Path(HERE.parents[8] / "data/firm_registry.json").read_text(encoding="utf-8"))
    for f in r["firms"]:
        if f.get("firm_id") == "inflection":
            return f["display_name"]
    raise Fail("the registry has no firm inflection")


FIRM_TITLE9 = None


# ---------------------------------------------------------------- pure helpers
def twr_expected(values, flows, trading_days):
    """THE METHOD, independently of the adapter: r_t = (V_t - F_t) / V_(t-1) - 1, t-1 the previous TRADING day, F_t the sum of the external flows over EVERY
    partition day d with t-1 < d <= t (the skipped-day rule: the flows of a closed day belong to the next performance day); None when a value is missing or V_(t-1) <= 0."""
    out = {}
    for i in range(1, len(trading_days)):
        t, p = trading_days[i], trading_days[i - 1]
        if t not in values or p not in values or values[p] <= 0:
            out[t] = None
            continue
        f = sum(x for d, x in flows.items() if p < d <= t)
        out[t] = (values[t] - f) / values[p] - 1.0
    return out


def gap_bin(gap_bp):
    if gap_bp < 5:
        return "lt_5bp"
    if gap_bp < 25:
        return "5_25bp"
    if gap_bp < 100:
        return "25_100bp"
    return "ge_100bp"


def pick_household(rows):
    """the render's household: among households with 2 or more accounts, the lowest sha256 of the household id (utf-8, hex digest)."""
    by = {}
    for r in rows:
        if r.get("household_id"):
            by.setdefault(str(r["household_id"]), set()).add(str(r["account_id"]))
    elig = {h: a for h, a in by.items() if len(a) >= 2}
    if not elig:
        return None, set()
    h = min(elig, key=lambda x: hashlib.sha256(x.encode("utf-8")).hexdigest())
    return h, elig[h]


# ---------------------------------------------------------------- DB109-1-AC1 (the Inflection sample)
def check_sample(root):
    r = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~173/BUILD_R109.json")
    c = P.contract(root)
    ver = tuple(int(x) for x in str(c.get("contract_version") or "0.0.0").split("."))
    need(ver >= (0, 4, 3), "the contract must be 0.4.3 or later")
    s = r.get("sample") or {}
    sp = str(s.get("path") or "").replace("\\", "/")
    need(sp.startswith(SAMPLE_DIR9) and sp.endswith("HOUSEHOLD_SAMPLE.json") and Path(sp).is_file(), "sample.path must be the private HOUSEHOLD_SAMPLE.json under %s" % SAMPLE_DIR9)
    need(not sp.startswith(str(root.resolve()).replace("\\", "/").rstrip("/") + "/"), "the sample is inside the repo: client data never goes there")
    need(s.get("sha256") == sha(sp) and s.get("contract_sha256") == sha(root / P5.CONTRACT_REL), "sample.sha256 and sample.contract_sha256 must equal the sample bytes and the contract bytes")
    sm = P.sample_json(sp)
    P5.check_sample_shape_k(sm, c)
    prob = P5.kind_problems(sm["values"], c)
    need(not prob, "kind carrier: %s" % "; ".join(prob[:3]))
    acc = accounts_of(sm)
    conf, dis, st = whole_document_scan(sm["values"], acc)
    need(st["unmapped"] == 0 and not conf and not dis, "whole-document rule: unmapped %d, %s" % (st["unmapped"], "; ".join((conf + dis)[:3])))
    need(r.get("whole_document") == {"cells_scanned": st["cells_scanned"], "absent_cells": st["absent_cells"], "keys": st["keys"], "unmapped": 0, "conflicts": 0}, "whole_document must equal the checker's own denominator %s with unmapped 0 and conflicts 0" % st)
    pc, _pd, _ps = whole_document_scan(P6.plant_conflict(sm["values"], acc), acc)
    need(len(pc) >= 1, "CONTROL: the rule is blind to a planted conflict")
    vals = sm["values"]
    # the household: the deterministic rule, recomputed from the private account_dim dry run
    need(Path(DIM_DRY).is_file(), "the private account_dim dry run of round 108 is missing")
    import pyarrow.parquet as pq
    rows = pq.read_table(DIM_DRY).to_pylist()
    h, accts = pick_household(rows)
    need(h is not None, "no household with 2 or more accounts in the dry run")
    need(r.get("household_ref_sha256") == hashlib.sha256(h.encode("utf-8")).hexdigest(), "household_ref_sha256 must be the lowest sha256 among households of 2 or more accounts (the checker recomputes it)")
    need(sorted(acc) == sorted(accts), "the sample's accounts must be exactly the chosen household's accounts in the dry run (%d expected)" % len(accts))
    # the words: an account return is NO_SOURCE_YET in plain words; lots are NO_SOURCE_YET in plain words; the split columns as for 49 Financial
    for w in ("qtd", "ytd", "last_12_months", "since_inception"):
        v = vals["avs.%s.return_cumulative" % w]
        leaves = list(v["by_row"].values()) if isinstance(v, dict) and "by_row" in v else [v]
        need(all(P5.is_absent_k(x) and x["kind"] == "NO_SOURCE_YET" and x["absent"] == ACCT_WORDS for x in leaves), "avs.%s.return_cumulative: every account return reads NO_SOURCE_YET with the words %r" % (w, ACCT_WORDS))
    for mid in [m["id"] for m in c["members"] if m["id"].startswith(("trgl.", "glr."))]:
        v = vals[mid]
        leaves = list(v["by_row"].values()) if isinstance(v, dict) and "by_row" in v else [v]
        need(all(P5.is_absent_k(x) and x["kind"] == "NO_SOURCE_YET" and x["absent"].startswith(LOTS_WORDS) for x in leaves), "%s: every lot member reads NO_SOURCE_YET with the words %r" % (mid, LOTS_WORDS))
    for mid in P6.SPLIT_MEMBERS:
        v = vals[mid]
        leaves = list(v["by_row"].values()) if isinstance(v, dict) and "by_row" in v else [v]
        need(all(P5.is_absent_k(x) and x["kind"] == "NO_SOURCE_YET" for x in leaves), "%s: the split columns stay NO_SOURCE_YET (as for 49 Financial)" % mid)
    # the household return stays ABSENT BY CONTRACT (no sibling contract carries a household-grain return: returns do not add across accounts): NO_SOURCE_YET in plain words.
    # Filling it from Orion's client grain would change what the contract says for every firm, which is the CTO's decision, not this cell's.
    filled = [w for w in ("qtd", "ytd", "last_12_months", "since_inception") if not P5.has_absent_key(vals["pvs.%s.return_cumulative" % w])]
    need(filled == [] and r.get("household_return_windows") == [], "the contract sources every household return ABSENT: pvs.*.return_cumulative must read NO_SOURCE_YET and household_return_windows must be [] (the checker reads %s)" % filled)
    hn = r.get("household_return_note") or {}
    need(nes(hn.get("words")) and "contract" in str(hn.get("words")).lower() and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(hn.get("orion_client_series_through") or "")), "household_return_note: words that name the contract rule, and orion_client_series_through (ISO): what Orion's client grain would provide")
    # the as-of: the newest positions date on or before the last date of the served model series, so every source exists at as_of (T-1 law)
    asof = sm["household"]["as_of"]
    need(r.get("as_of") == asof and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(r.get("benchmark_data_as_of") or "")) and asof <= str(r["benchmark_data_as_of"]), "as_of must equal the sample's (%s) and not be later than benchmark_data_as_of (the last date of the served model series)" % asof)
    n_f, tot_f = P6.members_filled(vals, c)
    need(r.get("benchmark_members") == {"total": 32, "filled": n_f} and tot_f == 32, "benchmark_members must equal the checker's count {total 32, filled %d}" % n_f)
    need(all(not P5.has_absent_key(vals["pvs.%s.ending_value" % w]) for w in ("qtd", "ytd", "last_12_months", "since_inception")) and not P5.has_absent_key(vals["hold.ending_value"]), "the household ending value must fill (pvs.*.ending_value and hold.ending_value)")
    # the guard state is NAMED, from the issuer's direct-act record
    ar = json.loads((root / ALIEN_REC).read_bytes().decode("utf-8"))
    gs = ar["result"]["guard_state_for_render_record"]
    need(r.get("orion_guard") == gs, "orion_guard must equal the guard state of the issuer's read gate %s" % gs)
    b = r.get("builder") or {}
    bf = str(b.get("file") or "")
    need(bf == D + "0.9.0_WK_IRPT_DASHBD~173/build_sample_inflection.py" and (root / bf).is_file() and b.get("sha256") == sha(root / bf) and b.get("tracked") is True, "builder: the tracked build_sample_inflection.py in the worker's folder, hashed as recorded")
    src = (root / bf).read_text(encoding="utf-8")
    need("inflection_account_dim" in src and not P8.foreign_hits(src) and not P8.write_hits(src), "the builder must use the Inflection adapter, name no other firm's place and hold no write call")
    rd = r.get("reads") or {}
    need(rd.get("vendor_calls") == 0 and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0 and rd.get("secret_reads") == 0 and is_int(rd.get("s3_reads")), "reads: zero writes, vendor calls and secret reads, s3_reads an integer")
    need(r.get("files_in_repo") is False and r.get("served_values_changed") is False and r.get("pushed") is False and r.get("deployed") is False, "files_in_repo, served_values_changed, pushed and deployed must be false")
    need(not P.long_digit_runs({k: v for k, v in r.items() if k not in ("sample",)}), "the record holds a run of 8 or more digits")
    print("OK: Inflection sample for one household (%d accounts) chosen by the hash rule; whole-document rule over %d cells (%d absent, 0 unmapped): 0 conflicts, planted mutant caught; account returns and lots in plain words; household return NO_SOURCE_YET by contract; as_of %s with %d of 32 benchmark members filled; guard state named"
          % (len(acc), st["cells_scanned"], st["absent_cells"], asof, n_f))


def extra_inflection(root, r, k, vals, tab, exp):
    """the Inflection clauses added to round 107's render clauses: the words, and the guard state named in the render record."""
    for name, text in (("tab_html", tab), ("export_html", exp)):
        vt = P3.visible_text(text)
        need(ACCT_WORDS in vt, "%s must say in plain words: %r" % (name, ACCT_WORDS))
        need(LOTS_WORDS in vt, "%s must say in plain words: %r" % (name, LOTS_WORDS))
    ar = json.loads((root / ALIEN_REC).read_bytes().decode("utf-8"))
    gs = ar["result"]["guard_state_for_render_record"]
    need(r.get("orion_guard") == gs and (k.get("orion_guard") == gs), "the render record must name the Orion guard state %s (the issuer's read gate)" % gs)


def mutate_printed_note(html, sample):
    """a copy with one more note that claims absence of a figure the sample DOES print: the first printed cell whose key is filled."""
    fk = P7.filled_keys(sample["values"], P7.accounts_of(sample))
    for mem, ent, _pos in P7.parse_cells(html):
        if ent is None or mem in P7.VIRTUAL:
            continue
        try:
            k = P7.figure_key(mem, P7.entity_data(ent, sample))
        except Exception:
            continue
        if k in fk:
            extra = '<p data-note="absent" data-note-keys="%s|%s">This figure is not available yet, because Opal has no source for it.</p>' % (mem, ent)
            n = html.rfind("</body>")
            return html[:n] + extra + html[n:] if n > 0 else html + extra
    return None


def note_level9(root, r, c, sm, exp, tab):
    """round 107's note-level rule, with the absent-note control planted on a key this sample prints (the sample prints no household year-to-date net gain)."""
    f, st = P7.note_rule(exp, sm, True)
    need(not f, "note-level rule (export): %s" % "; ".join(f[:3]))
    ft, _stt = P7.note_rule(tab, sm, False)
    need(not ft, "note-level rule (tab): %s" % "; ".join(ft[:3]))
    _conf, _dis, wd = P7.whole_document_scan(sm["values"], P7.accounts_of(sm))
    need(st["notes"] >= 1 and st["pointer_notes"] >= 1, "the export carries %d keyed notes and %d pointer notes: both kinds must be keyed" % (st["notes"], st["pointer_notes"]))
    nl = r.get("note_level") or {}
    need(nl == {"cells_scanned": wd["cells_scanned"], "absent_cells": wd["absent_cells"], "notes": st["notes"], "pointer_notes": st["pointer_notes"]},
         "note_level must equal the checker's denominator {cells_scanned %d, absent_cells %d, notes %d, pointer_notes %d}" % (wd["cells_scanned"], wd["absent_cells"], st["notes"], st["pointer_notes"]))
    m1 = P7.mutate_pointer(exp, sm)
    need(m1 is not None and P7.note_rule(m1, sm, True)[0], "CONTROL: the rule is blind to a pointer to the wrong page (the planted mutant was not reported)")
    m2 = mutate_printed_note(exp, sm)
    need(m2 is not None and P7.note_rule(m2, sm, True)[0], "CONTROL: the rule is blind to a note that names a printed figure (the planted mutant was not reported)")


def check_render(root):
    r = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~173/RENDER_R109.json")
    k = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~173/BUILD_R109.json")
    c = P.contract(root)
    ids = [m["id"] for m in c["members"]]
    unit = {m["id"]: m["unit"] for m in c["members"]}
    label = {m["id"]: m["label"] for m in c["members"]}
    sp = str((k.get("sample") or {}).get("path") or "")
    need(Path(sp).is_file() and sha(sp) == (k["sample"] or {}).get("sha256") and r.get("sample_sha256") == sha(sp), "the render record must be bound to the round-109 Inflection sample the data cell built (its sha256)")
    sm = P.sample_json(sp)
    vals = sm["values"]
    outs = r.get("outputs") or {}
    paths = {x: P.private_file(root, outs.get(x), OUT_R9, ext, x) for x, ext in (("tab_html", ".html"), ("export_html", ".html"), ("export_pdf", ".pdf"))}
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
    l4 = [str(a.get("last4")) for a in sm["household"]["accounts"]]
    need(all(re.fullmatch(r"[0-9]{4}", x) for x in l4) and len(set(l4)) == len(l4), "each account's last4 label must be four digits and the labels distinct within the household (%d accounts, %d distinct, %d all-digit)" % (len(l4), len(set(l4)), sum(1 for x in l4 if re.fullmatch(r"[0-9]{4}", x))))
    uc = P5.unheld_count(vals)
    # the Inflection sample places no asset class (the allocation is absent in words), so it may hold no UNHELD entry: the dash count below must then be 0
    pass
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
        need("Sample Firm" not in vt and FIRM_TITLE9 in vt, "%s must print the registry's firm title" % name)
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
        need(vt.count("Opal does not split net additions") == 1 and "same applies to each account" in vt, "%s must print the split sentence ONCE (household level) followed by the same applies to each account (it printed %d times)" % (name, vt.count("Opal does not split net additions")))
        need("household allocation" not in vt.lower(), "%s still calls the household allocation unavailable (the table prints the class shares and no household row of 100 percent is wanted)" % name)
        # a chart takes no kind note and never claims a reason; its note is computed, or its slot is dropped
        for cid in chart_ids:
            if not P5.has_absent_key(vals[cid]):
                continue
            seg = chart_segment(text, cid)
            need(not any(f in seg.lower() for f in REASON_FRAGMENTS), "%s: the absent chart %s claims a reason in its slot (%r): a chart is not a figure" % (name, cid, seg[:120]))
            tabs = CHART_TABLES7[cid]
            lead = "the period totals are" if cid == CHART3 else "the values are"
            filled = all(not P5.has_absent_key(vals[t]) and not (isinstance(vals[t], dict) and "by_row" in vals[t] and all(P5.has_absent_key(x) for x in vals[t]["by_row"].values())) for t in tabs)
            slot = next((x for x in (r.get("chart_slots") or []) if isinstance(x, dict) and x.get("id") == cid), None)
            need(slot is not None and slot.get("action") in ("note", "dropped"), "chart_slots must hold {id, action note|dropped} for the absent chart %s" % cid)
            if filled and name == "tab_html":
                # the tab has no pagination: the note names the table without a page number; the computed page is the export's
                if slot["action"] == "note":
                    need("Chart not drawn in this report; %s in the table" % lead in seg, "%s: chart %s must read 'Chart not drawn in this report; %s in the table...'" % (name, cid, lead))
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
                        exp_note = "Chart not drawn in this report; %s in the table on page %d" % (lead, pg[0])
                    else:
                        exp_note = "Chart not drawn in this report; %s in the tables on pages %d and %d" % (lead, pg[0], pg[1])
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
    extra_inflection(root, r, k, vals, tab, exp)
    note_level9(root, r, c, sm, exp, tab)
    P.footer_ok(exp, sm["household"]["as_of"])
    pages = P.pdf_pages(paths["export_pdf"])
    need(pages >= 8, "the PDF holds %d pages" % pages)
    P.check_pdf_read(r, pages)
    need(sum(1 for x in r["pdf_clipping"] if x["clipped"]) == 0, "a page is recorded clipped: fix it and re-render")
    pt = r.get("portal") or {}
    need(pt.get("branch") == "wk-IRPT_DASHBD-173-portal" and P.HEXC.fullmatch(str(pt.get("commit") or "")), "portal %r: the branch wk-IRPT_DASHBD-173-portal and a commit" % pt)
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


# ---------------------------------------------------------------- DB109-3-AC1 (the account-return derivation and the tie-out read)
def check_twr(root):
    r = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~174/TWR_TIEOUT_R109.json")
    m = r.get("module") or {}
    need(m.get("file") == TWR_MODULE and (root / TWR_MODULE).is_file() and m.get("sha256") == sha(root / TWR_MODULE) and m.get("tracked") is True, "module: the tracked file %s hashed as recorded" % TWR_MODULE)
    src = (root / TWR_MODULE).read_text(encoding="utf-8")
    need(not P8.foreign_hits(src) and not P8.write_hits(src), "the module names another firm's place or holds a write call")
    need(all(any(x.startswith(p) for p in P8.ALLOWED_PREFIXES) for x in P8.s3_literals(src)), "every s3:// literal of the module must sit under a granted Inflection prefix")
    en = r.get("engine") or {}
    need(en.get("file") == ENGINE and en.get("sha256") == sha(root / ENGINE) and en.get("unchanged") is True and nes(en.get("how_used")), "engine: the existing %s hashed as it stands (unchanged), and how_used in words (the method, or the functions called)" % ENGINE)
    g = subprocess.run(["git", "-C", str(root), "diff", "--quiet", "HEAD", "--", ENGINE], capture_output=True)
    need(g.returncode == 0, "the engine file differs from HEAD: it is not yours to edit")
    t = r.get("tests") or {}
    need(t.get("file") == TWR_TEST and (root / TWR_TEST).is_file() and is_int(t.get("passed")) and t["passed"] >= 6 and t.get("failed") == 0 and t.get("mutant_failed") is True, "tests: %s, 6 or more passing, none failing, a failing mutant" % TWR_TEST)
    q = subprocess.run([sys.executable, "-I", "-m", "pytest", "-q", str((root / TWR_TEST).resolve())], capture_output=True, text=True, cwd=str(root))
    need(q.returncode == 0, "the test file does not pass when the checker runs it")
    # the METHOD, tested against the checker's own independent computation on a synthetic week with a closed day (Thursday) that carries a deposit
    spec = importlib.util.spec_from_file_location("itwr", str(root / TWR_MODULE))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["itwr"] = mod
    spec.loader.exec_module(mod)
    need(hasattr(mod, "daily_returns") and hasattr(mod, "window_return"), "the module must expose daily_returns(values, flows, trading_days) and window_return(daily, start, end)")
    td = ["2026-03-02", "2026-03-03", "2026-03-04", "2026-03-06", "2026-03-09"]
    vals = {"2026-03-02": 1000.0, "2026-03-03": 1010.0, "2026-03-04": 1012.0, "2026-03-05": 1112.0, "2026-03-06": 1125.0, "2026-03-09": 1130.0}
    flows = {"2026-03-05": 100.0, "2026-03-09": -20.0}
    want = twr_expected(vals, flows, td)
    got = mod.daily_returns(vals, flows, td)
    for d in td[1:]:
        need(got.get(d) is not None and abs(got[d] - want[d]) < 1e-9, "daily_returns on %s = %r, the method gives %r (the deposit on the closed day 2026-03-05 belongs to 2026-03-06)" % (d, got.get(d), want[d]))
    got2 = mod.daily_returns({k: v for k, v in vals.items() if k != "2026-03-03"}, flows, td)
    need(got2.get("2026-03-03") is None and got2.get("2026-03-04") is None, "a missing value must give None, never zero (got %r, %r)" % (got2.get("2026-03-03"), got2.get("2026-03-04")))
    prod = 1.0
    for d in td[1:]:
        prod *= 1.0 + want[d]
    wr = mod.window_return(got, "2026-03-03", "2026-03-09")
    need(wr is not None and abs(wr - (prod - 1.0)) < 1e-9, "window_return must be the product of (1 + daily return) minus 1 (got %r)" % wr)
    # the derived table and the tie-out file, recounted
    import pyarrow.parquet as pq
    dr = r.get("derived") or {}
    dp = str(dr.get("path") or "").replace("\\", "/")
    need(dp.startswith(TWR_DIR) and dp.endswith(".parquet") and Path(dp).is_file() and dr.get("sha256") == sha(dp), "derived.path must be a private .parquet under %s, hashed as recorded" % TWR_DIR)
    rc = json.loads((root / RET_CONTRACT).read_bytes().decode("utf-8"))
    tb = pq.read_table(dp)
    ph = hashlib.sha256("\n".join(sorted("%s:%s" % (f.name, f.type) for f in tb.schema)).encode()).hexdigest()
    need(ph == rc["schema_hash"] and dr.get("schema_hash") == rc["schema_hash"], "the derived table's schema hash must equal the account_return_daily contract's")
    need(tb.num_rows > 0 and dr.get("rows") == tb.num_rows and r.get("label") == "OPAL_COMPUTED", "derived.rows must equal the table's rows and the label must be OPAL_COMPUTED")
    dim = {str(x["account_id"]) for x in pq.read_table(DIM_DRY).to_pylist() if x.get("account_id")}
    dacc = {str(x) for x in tb.column("account_id").to_pylist()}
    need(dacc <= dim and dr.get("accounts") == len(dacc), "every derived account must be an Inflection account of the dry run; derived.accounts must equal %d" % len(dacc))
    households = {str(x["household_id"]) for x in pq.read_table(DIM_DRY).to_pylist() if x.get("household_id")}
    tp = str(((r.get("tie_out") or {}).get("gaps_file") or {}).get("path") or "").replace("\\", "/")
    need(tp.startswith(TWR_DIR) and tp.endswith(".parquet") and Path(tp).is_file() and r["tie_out"]["gaps_file"].get("sha256") == sha(tp), "tie_out.gaps_file must be a private .parquet under %s, hashed as recorded" % TWR_DIR)
    gaps = pq.read_table(tp).to_pylist()
    wins = r["tie_out"].get("windows") or {}
    need(sorted(wins) == sorted(TIE_WINDOWS), "tie_out.windows must hold exactly %s" % list(TIE_WINDOWS))
    for w in TIE_WINDOWS:
        rows_w = [x for x in gaps if x["window"] == w]
        hh = {x["household_sha256"] for x in rows_w}
        need(len(rows_w) == len(households) and len(hh) == len(households), "%s: every household of the dry run (%d) must have exactly one row in the gaps file (the denominator), got %d rows" % (w, len(households), len(rows_w)))
        cmp_ = [x for x in rows_w if x.get("gap_bp") is not None]
        counts = {b: 0 for b in BINS}
        for x in cmp_:
            counts[gap_bin(abs(float(x["gap_bp"])))] += 1
        rec = wins[w]
        need(rec.get("clients_compared") == len(cmp_) and rec.get("not_comparable") == len(rows_w) - len(cmp_) and rec.get("bins") == counts and sum(counts.values()) == len(cmp_), "%s: the record's compared, not_comparable and bins must equal the checker's recount %s over %d households" % (w, counts, len(rows_w)))
        need(all(nes(x.get("reason")) for x in rows_w if x.get("gap_bp") is None), "%s: every household with no gap carries a reason in words" % w)
    need(sum(wins[w]["clients_compared"] for w in TIE_WINDOWS) > 0, "no window compared any client: the tie-out read measured nothing")
    need(r["tie_out"].get("tolerance_assumed") is None and nes(r["tie_out"].get("basis_words")), "no tolerance is assumed (tolerance_assumed null): the CTO rules it on this read; basis_words in words")
    rd = r.get("reads") or {}
    need(rd.get("vendor_calls") == 0 and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0 and rd.get("secret_reads") == 0 and is_int(rd.get("s3_reads")), "reads: zero writes, vendor calls and secret reads, s3_reads an integer")
    need(r.get("files_in_repo") is False and r.get("served_values_changed") is False and r.get("pushed") is False and r.get("deployed") is False, "files_in_repo, served_values_changed, pushed and deployed must be false")
    need(not P.long_digit_runs({k: v for k, v in r.items() if k not in ("derived", "tie_out", "engine", "module")}), "the record holds a run of 8 or more digits")
    print("OK: the TWR method equals the checker's independent computation (closed-day deposit carried to the next day, missing value gives None); %d derived accounts, %d rows (label OPAL_COMPUTED, schema hash equal to the contract's); tie-out over %d households in %d windows, bins recounted, no tolerance assumed"
          % (len(dacc), tb.num_rows, len(households), len(TIE_WINDOWS)))


# ---------------------------------------------------------------- self test
def selftest():
    n = 0

    def arm(name, cond):
        nonlocal n
        n += 1
        if not cond:
            print("SELFTEST FAIL: %s" % name)
            sys.exit(1)

    td = ["2026-03-02", "2026-03-03", "2026-03-04", "2026-03-06", "2026-03-09"]
    vals = {"2026-03-02": 1000.0, "2026-03-03": 1010.0, "2026-03-04": 1012.0, "2026-03-05": 1112.0, "2026-03-06": 1125.0, "2026-03-09": 1130.0}
    flows = {"2026-03-05": 100.0, "2026-03-09": -20.0}
    w = twr_expected(vals, flows, td)
    arm("twr: a plain day", abs(w["2026-03-03"] - (1010.0 / 1000.0 - 1.0)) < 1e-12)
    arm("twr: the skipped-day rule (a deposit on the closed day 2026-03-05 is carried to 2026-03-06, not lost)", abs(w["2026-03-06"] - ((1125.0 - 100.0) / 1012.0 - 1.0)) < 1e-12)
    arm("twr: a withdrawal on a trading day", abs(w["2026-03-09"] - ((1130.0 + 20.0) / 1125.0 - 1.0)) < 1e-12)
    arm("twr: a missing value gives None, never zero", twr_expected({k: v for k, v in vals.items() if k != "2026-03-03"}, flows, td)["2026-03-03"] is None)
    arm("twr: a zero previous value gives None", twr_expected({"2026-03-02": 0.0, "2026-03-03": 5.0}, {}, ["2026-03-02", "2026-03-03"])["2026-03-03"] is None)
    arm("bins: the four edges", [gap_bin(x) for x in (0.0, 4.99, 5.0, 24.99, 25.0, 99.99, 100.0, 5000.0)] == ["lt_5bp", "lt_5bp", "5_25bp", "5_25bp", "25_100bp", "25_100bp", "ge_100bp", "ge_100bp"])
    rows = [{"household_id": "h1", "account_id": "a1"}, {"household_id": "h1", "account_id": "a2"}, {"household_id": "h2", "account_id": "a3"}, {"household_id": "h3", "account_id": "a4"}, {"household_id": "h3", "account_id": "a5"}]
    h, a = pick_household(rows)
    want = min(("h1", "h3"), key=lambda x: hashlib.sha256(x.encode()).hexdigest())
    arm("household rule: the lowest hash among households of two or more accounts (h2 has one account and is out)", h == want and len(a) == 2)
    arm("household rule: none eligible", pick_household([{"household_id": "h", "account_id": "a"}])[0] is None)
    arm("the Inflection words are fixed sentences", ACCT_WORDS.endswith("for this firm yet.") and LOTS_WORDS.endswith("for this account yet."))
    print("SELFTEST OK: %d arms" % n)


FNS = {"DB109-1-AC1": check_sample, "DB109-2-AC1": check_render, "DB109-3-AC1": check_twr}


def main():
    global FIRM_TITLE9
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        selftest()
        return
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    try:
        need(cid in FNS, "unknown criterion %r" % cid)
        FIRM_TITLE9 = firm_title()
        FNS[cid](root)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (cid or "DB109"))
        sys.exit(1)
    except (KeyError, TypeError, ValueError, AttributeError, IndexError, ImportError) as e:
        print("FAIL: malformed record: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % cid)
        sys.exit(1)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
