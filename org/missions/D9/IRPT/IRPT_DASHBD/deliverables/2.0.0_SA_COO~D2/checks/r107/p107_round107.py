"""IRPT_DASHBD round 107 (issuer 2.0.0_SA_COO~D2) -- the issuance for 1.0.0_SA_CTO~DELL2's ROUND-107 ANALYSIS (@4aedf6a687; the CVO graded DB106-2-J1 FAIL on two single lines).

  DB-b-209 (~170)  the render cell: the page-5 chart pointer reads "Chart not drawn in this report; the period totals are in the table on page N" (N computed), the
                   page-6 foot note drops the household-allocation clause, the repeated split-column line collapses to one household line plus "the same applies to each
                   account"; every note and every cell carries the keys the note-level rule reads.                                                     DB107-1-AC1 (+ J1, the CVO's)
  DB-b-210 (issuer) the NOTE-LEVEL extension of the whole-document rule: this file. Every note carries the member keys it names; a note that claims absence of a key a
                   printed cell carries FAILS; a note that points to "page N" FAILS unless page N prints a cell carrying its entity and member; N is computed from the
                   render, never typed. Two planted mutants (a wrong pointer, a note naming a printed figure) run inside the criterion. The denominator counts cells AND notes.

THE CONVENTION the render emits (pinned here, read by this file):
  - every note element:   data-note="absent"|"pointer"   data-note-keys="<member>|<entity>;<member>|<entity>"   (a pointer also data-note-page="N", export only)
  - every member cell/row/figure element (charts excepted): data-entity="household" | "<last four characters of the account id>" | "class:<asset class>"
  - virtual members a note may name although no cell exists: hold.class_rows.ending_value, hold.class_rows.net_gain, hold.class_rows.return (entity class:*)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure functions on synthetic arms (green and red) and the two planted mutants
"""
import importlib.util
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


P6 = load_mod("p106", "r106/p106_round106.py")
P5 = P6.P5
P3 = P6.P3
P = P6.P
need, nes, is_int, sha = P.need, P.nes, P.is_int, P.sha
D = P.D
PRIV = P.PRIV
Fail = P.Fail
OUT_R7 = PRIV + "fwd21_sample_r107/"
figure_key, state, cells_of, accounts_of, whole_document_scan = P6.figure_key, P6.state, P6.cells_of, P6.accounts_of, P6.whole_document_scan
is_chart, pages_of, chart_segment, Unmapped = P6.is_chart, P6.pages_of, P6.chart_segment, P6.Unmapped
REASON_FRAGMENTS = P6.REASON_FRAGMENTS
CHART3 = "accounts.chart.ending_value_and_net_additions_last_12_months"
# round 107: the household's 12-month totals print in the Portfolio Value Summary, so chart 3 points there ("period totals"); the allocation charts keep their tables
CHART_TABLES7 = dict(P6.CHART_TABLES)
CHART_TABLES7[CHART3] = ("pvs.last_12_months.net_additions", "pvs.last_12_months.ending_value")
POINTER_MEMBERS = {t for ts in CHART_TABLES7.values() for t in ts}
VIRTUAL = ("hold.class_rows.ending_value", "hold.class_rows.net_gain", "hold.class_rows.return")
NOTE_PHRASES = ("is not available yet", "is not available while", "needs more history", "Chart not drawn in this report", "does not split net additions", "same applies to each account")
NOTE_RE = re.compile(r"<(p|div|span|li|figcaption)\b([^>]*\bdata-note=\"(absent|pointer)\"[^>]*)>(.*?)</\1>", re.S)
CELL_RE = re.compile(r"<(\w+)\b([^>]*\bdata-member=\"([^\"]+)\"[^>]*)>", re.S)
PAGE_RE = re.compile(r"Page\s*(?:<[^>]*>\s*)*(\d+)\s*(?:<[^>]*>\s*)*of\s*(?:<[^>]*>\s*)*(\d+)")


# ---------------------------------------------------------------- the note-level rule (pure)
def attr(attrs, name):
    m = re.search(r'\b%s="([^"]*)"' % re.escape(name), attrs)
    return m.group(1) if m else None


def page_at(html, pos):
    n = PAGE_RE.search(html, pos)
    return int(n.group(1)) if n else None


def parse_notes(html):
    out = []
    for m in NOTE_RE.finditer(html):
        keys = []
        for part in (attr(m.group(2), "data-note-keys") or "").split(";"):
            if part.strip():
                mem, _, ent = part.partition("|")
                keys.append((mem.strip(), ent.strip()))
        pg = attr(m.group(2), "data-note-page")
        out.append({"kind": m.group(3), "keys": keys, "page": int(pg) if pg and pg.isdigit() else None, "text": P3.visible_text(m.group(4)), "span": (m.start(), m.end())})
    return out


def parse_cells(html):
    out = []
    for m in CELL_RE.finditer(html):
        if "data-note=" in m.group(2):
            continue
        out.append((m.group(3), attr(m.group(2), "data-entity"), m.start()))
    return out


def entity_data(label, sample):
    if label == "household":
        return "household"
    if label.startswith("class:"):
        return label[6:]
    ids = [a for a in accounts_of(sample) if a.endswith(label)]
    if len(ids) != 1:
        raise Unmapped("entity %s" % label)
    return ids[0]


def filled_keys(values, account_ids):
    ks = set()
    for mid, e, x in cells_of(values, account_ids):
        try:
            k = figure_key(mid, e)
        except Unmapped:
            continue
        if state(x) == "num":
            ks.add(k)
    return ks


def shown_pages(text):
    m = re.search(r"pages?\s+(\d+)(?:\s+and\s+(\d+))?", text)
    return [int(g) for g in m.groups() if g] if m else []


def cell_pages(html):
    out = {}
    for mem, ent, pos in parse_cells(html):
        if ent is not None:
            out.setdefault((mem, ent), set()).add(page_at(html, pos))
    return out


def note_rule(html, sample, is_export=True):
    """(failures, stats). The denominator is every cell of the sample plus every note of the document; an unkeyed note, an unmapped key and a wrong pointer FAIL."""
    values = sample["values"]
    acc = accounts_of(sample)
    fk = filled_keys(values, acc)
    notes = parse_notes(html)
    cells = parse_cells(html)
    fails = []
    cp = cell_pages(html) if is_export else {}
    noent = sorted({mem for mem, ent, _p in cells if ent is None and not is_chart(mem)})
    if noent:
        fails.append("%d member element(s) carry no data-entity (first: %s)" % (len(noent), noent[0]))
    rest = NOTE_RE.sub(" ", html)
    vt = P3.visible_text(rest)
    for ph in NOTE_PHRASES:
        if ph in vt:
            fails.append("a note outside every keyed element says %r: every note carries its keys" % ph)
    absent_notes = pointer_notes = 0
    for n in notes:
        if not n["keys"]:
            fails.append("a %s note carries no data-note-keys: %r" % (n["kind"], n["text"][:60]))
            continue
        if n["kind"] == "absent":
            absent_notes += 1
            for mem, ent in n["keys"]:
                if mem in VIRTUAL:
                    continue
                try:
                    k = figure_key(mem, entity_data(ent, sample))
                except Unmapped as e:
                    fails.append("an absent note names a key the grammar cannot map: %s|%s (%s)" % (mem, ent, e))
                    continue
                if k in fk:
                    fails.append("an absent note claims %s|%s is unavailable while a printed cell carries the key %s" % (mem, ent, k))
        else:
            pointer_notes += 1
            for mem, ent in n["keys"]:
                if mem not in POINTER_MEMBERS:
                    fails.append("a pointer note names %s, which is no chart table of the mapping" % mem)
            if not is_export:
                continue
            pg = sorted({p for key in n["keys"] for p in cp.get(key, set()) if p is not None})
            if not pg:
                fails.append("a pointer note names (%s) but no page of the document prints a cell carrying that entity and member" % ", ".join("%s|%s" % k for k in n["keys"])[:140])
                continue
            want = pg[0]
            shown = shown_pages(n["text"])
            if n["page"] != want or not shown or shown[0] != want:
                fails.append("a pointer note says page %s (attribute %s) but the page that prints its entity and member is %d (computed from the render)" % (shown, n["page"], want))
    stats = {"notes": len(notes), "absent_notes": absent_notes, "pointer_notes": pointer_notes}
    return fails, stats


def mutate_pointer(html, sample):
    """a copy whose first pointer note points to a page that does not print its entity and member."""
    notes = [n for n in parse_notes(html) if n["kind"] == "pointer" and n["page"] is not None]
    if not notes:
        return None
    n = notes[0]
    cp = cell_pages(html)
    have = {p for k in n["keys"] for p in cp.get(k, set())}
    total = max([int(m.group(2)) for m in PAGE_RE.finditer(html)] or [1])
    bad = next((p for p in range(1, total + 2) if p not in have), total + 1)
    s, e = n["span"]
    seg = html[s:e]
    seg2 = re.sub(r'data-note-page="\d+"', 'data-note-page="%d"' % bad, seg)
    seg2 = re.sub(r"(pages?\s+)%d\b" % n["page"], lambda m: m.group(1) + str(bad), seg2, count=1)
    return html[:s] + seg2 + html[e:]


def mutate_absent_note(html):
    """a copy with one more note that claims absence of a figure the sample prints (the household's year-to-date Net Gain)."""
    extra = '<p data-note="absent" data-note-keys="hold.net_gain_ytd|household">Household, Net Gain for Year To Date: is not available yet, because Opal has no source for it.</p>'
    k = html.rfind("</body>")
    return html[:k] + extra + html[k:] if k > 0 else html + extra


def note_level(root, r, c, sm, exp, tab):
    f, st = note_rule(exp, sm, True)
    need(not f, "note-level rule (export): %s" % "; ".join(f[:3]))
    ft, _stt = note_rule(tab, sm, False)
    need(not ft, "note-level rule (tab): %s" % "; ".join(ft[:3]))
    _conf, _dis, wd = whole_document_scan(sm["values"], accounts_of(sm))
    need(st["notes"] >= 1 and st["pointer_notes"] >= 1, "the export carries %d keyed notes and %d pointer notes: both kinds must be keyed" % (st["notes"], st["pointer_notes"]))
    nl = r.get("note_level") or {}
    need(nl == {"cells_scanned": wd["cells_scanned"], "absent_cells": wd["absent_cells"], "notes": st["notes"], "pointer_notes": st["pointer_notes"]},
         "note_level must equal the checker's denominator {cells_scanned %d, absent_cells %d, notes %d, pointer_notes %d}" % (wd["cells_scanned"], wd["absent_cells"], st["notes"], st["pointer_notes"]))
    m1 = mutate_pointer(exp, sm)
    need(m1 is not None and note_rule(m1, sm, True)[0], "CONTROL: the rule is blind to a pointer to the wrong page (the planted mutant was not reported)")
    m2 = mutate_absent_note(exp)
    need(note_rule(m2, sm, True)[0], "CONTROL: the rule is blind to a note that names a printed figure (the planted mutant was not reported)")


# ---------------------------------------------------------------- DB107-1-AC1: round 106's render clauses, re-bound, plus the round-107 wording and the note-level rule
def check_render_base(root):
    r = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~170/RENDER_R107.json")
    k = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~169/BUILD_R106.json")
    c = P.contract(root)
    ids = [m["id"] for m in c["members"]]
    unit = {m["id"]: m["unit"] for m in c["members"]}
    label = {m["id"]: m["label"] for m in c["members"]}
    sp = str((k.get("sample") or {}).get("path") or "")
    need(Path(sp).is_file() and sha(sp) == (k["sample"] or {}).get("sha256") and r.get("sample_sha256") == sha(sp), "the render record must be bound to the round-106 sample the data cell built (round 107 re-renders it) (its sha256)")
    sm = P.sample_json(sp)
    vals = sm["values"]
    outs = r.get("outputs") or {}
    paths = {x: P.private_file(root, outs.get(x), OUT_R7, ext, x) for x, ext in (("tab_html", ".html"), ("export_html", ".html"), ("export_pdf", ".pdf"))}
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
    note_level(root, r, c, sm, exp, tab)
    P.footer_ok(exp, sm["household"]["as_of"])
    pages = P.pdf_pages(paths["export_pdf"])
    need(pages >= 8, "the PDF holds %d pages" % pages)
    P.check_pdf_read(r, pages)
    need(sum(1 for x in r["pdf_clipping"] if x["clipped"]) == 0, "a page is recorded clipped: fix it and re-render")
    pt = r.get("portal") or {}
    need(pt.get("branch") == "wk-IRPT_DASHBD-170-portal" and P.HEXC.fullmatch(str(pt.get("commit") or "")), "portal %r: the branch wk-IRPT_DASHBD-170-portal and a commit" % pt)
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


check_render = check_render_base


# ---------------------------------------------------------------- self test
def selftest():
    n = 0

    def arm(name, cond):
        nonlocal n
        n += 1
        if not cond:
            print("SELFTEST FAIL: %s" % name)
            sys.exit(1)

    def ab():
        return {"absent": "x", "kind": "NO_SOURCE_YET"}

    sample = {"household": {"accounts": [{"account_id": "1111111111", "last4": "1111"}, {"account_id": "2222222222", "last4": "2222"}]},
              "values": {"pvs.last_12_months.net_additions": 5.0, "pvs.last_12_months.ending_value": 9.0, "pvs.ytd.net_gain": 3.0, "hold.net_gain_ytd": 3.0,
                         "hold.net_gain_mtd": ab(), "hold.return_ytd": ab(), "act.ending_value.account": {"by_row": {"1111111111": 4.0, "2222222222": 5.0}}}}

    def page(n_, inner):
        return "<section>%s<footer>Page <b>%d</b> of 2</footer></section>" % (inner, n_)

    ptr = ('<p data-note="pointer" data-note-keys="pvs.last_12_months.net_additions|household;pvs.last_12_months.ending_value|household" data-note-page="1">'
           "Chart not drawn in this report; the period totals are in the table on page 1</p>")
    absn = ('<p data-note="absent" data-note-keys="hold.net_gain_mtd|household;hold.return_ytd|household">'
            "Household, Net Gain for Month To Date and Return for Year To Date: is not available yet, because Opal has no source for it.</p>")
    virt = '<p data-note="absent" data-note-keys="hold.class_rows.net_gain|class:*">Net gain for each asset class: is not available yet.</p>'
    green = ("<html><body>" + page(1, '<table><tr><td data-member="pvs.last_12_months.net_additions" data-entity="household">$5</td></tr></table>' + ptr)
             + page(2, '<td data-member="pvs.last_12_months.ending_value" data-entity="household">$9</td><td data-member="act.ending_value.account" data-entity="1111">$4</td>' + absn + virt)
             + "</body></html>")
    f, st = note_rule(green, sample, True)
    arm("green: keyed notes, a computed pointer, a virtual member, every cell with an entity (%s, fails %s)" % (st, f), f == [] and st["notes"] == 3 and st["pointer_notes"] == 1)
    m1 = mutate_pointer(green, sample)
    arm("PLANTED MUTANT 1: a pointer to a page that lacks its entity and member is reported", m1 is not None and len(note_rule(m1, sample, True)[0]) >= 1)
    m2 = mutate_absent_note(green)
    arm("PLANTED MUTANT 2: a note naming a printed figure is reported", len(note_rule(m2, sample, True)[0]) >= 1)
    r1 = green.replace(virt, "<p>Net gain for each asset class: is not available yet.</p>")
    arm("red: an unkeyed note phrase is reported", len(note_rule(r1, sample, True)[0]) >= 1)
    r2 = green.replace("hold.net_gain_mtd|household", "mystery.member|household")
    arm("red: a key the grammar cannot map is reported (never skipped)", len(note_rule(r2, sample, True)[0]) >= 1)
    r3 = green.replace('data-entity="household">$5', ">$5")
    arm("red: a cell with no data-entity is reported", len(note_rule(r3, sample, True)[0]) >= 1)
    r5 = green.replace("on page 1", "on page 2")
    arm("red: the shown page differs from the computed page", len(note_rule(r5, sample, True)[0]) >= 1)
    r6 = green.replace('data-note-keys="pvs.last_12_months.net_additions|household;pvs.last_12_months.ending_value|household"', 'data-note-keys="hold.net_gain_ytd|household"')
    arm("red: a pointer note naming a member that is no chart table is reported", len(note_rule(r6, sample, True)[0]) >= 1)
    arm("tab: a pointer note needs no page", note_rule(green.replace(' data-note-page="1"', ""), sample, False)[0] == [])
    print("SELFTEST OK: %d arms" % n)


FNS = {"DB107-1-AC1": check_render}


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
        print("%s FAIL" % (cid or "DB107"))
        sys.exit(1)
    except (KeyError, TypeError, ValueError, AttributeError, IndexError, ImportError) as e:
        print("FAIL: malformed record: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % cid)
        sys.exit(1)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
