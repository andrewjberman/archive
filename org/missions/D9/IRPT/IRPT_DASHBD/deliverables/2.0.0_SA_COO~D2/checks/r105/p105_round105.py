"""IRPT_DASHBD round 105 (issuer 2.0.0_SA_COO~D2) -- the issuance for 1.0.0_SA_CTO~DELL2's ROUND-105 ANALYSIS (@9edfbc0784; the CVO graded DB104-1-J1 FAIL on clause 1).

  DB-b-202 (~167)  the data half of the absent kind: contract 0.4.2 (Carrier A, three kinds, the UNHELD value and its dash rule), the sample builder writes kind,
                   fills the activity members another table of the same report prints, and the CROSS-TABLE rule (a figure absent in one table and filled in
                   another for the same entity and window FAILS).                                                                                   DB105-1-AC1
  DB-b-203 (~167)  the render remedy and the view half: the view reads kind (absentKindOf deleted), no note claims a reason for a figure the report prints, slot names
                   become client words, an asterisk only with its footnote, one sentence per note; re-rendered, every page read.                      DB105-2-AC1 (+ J1, the CVO's)
  DB-b-204 (~168)  the model windows by build-time READ: a reader module (renamed), compounded windows carrying source and data_as_of, the series contract's claim
                   fields; the retired module and contract removed; nothing written.                                                                 DB105-3-AC1

Usage: python <this file> <repo_root> <criterion_id>     prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       runs the pure functions on synthetic arms (green and red)
"""
import datetime as dt
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


P3 = load_mod("p103", "r103/p103_round103.py")
P = P3.P
P97 = P.p97(None)
need, nes, is_int, sha = P.need, P.nes, P.is_int, P.sha
D = P.D
PRIV = P.PRIV
Fail = P.Fail
OUT_R = PRIV + "fwd21_sample_r105/"
SAMPLE_DIR = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~167/"
KINDS = ("NO_SOURCE_YET", "INSUFFICIENT_HISTORY", "SOURCE_BREAK")
UNHELD = "UNHELD"
V041_SHA = "c43306eb8681648025fbdbe548afc9de3d175d132ab9db81afcc42f0630124e5"
V042_SHA = "e9c389b75c1981bfe8a2aee9ebb8b0b21f45c686071b75950bb5db2e806e151d"
SERIES_V010_SHA = "40cef6203cbfa109cae26209a9d241b82d6b1071f316c9f71f39d16913853e94"
CONTRACT_REL = "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"
SERIES_REL = "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json"
CLASSES = {"cash", "fixed_income", "equity", "structured", "alternatives", "commodities", "unclassified"}
DASH = "–"
BARE = ("This figure needs more history than is available yet.", "This figure is not available yet.", "This figure does not apply.")
# the slot names the CVO found printed as client lines (round 104, clause 1 count 3)
SLOT_PHRASES = ("Since-inception column heading", "Footnote for a window not held for the entire period", "Class hierarchy",
                "each with its registration name and last four digits")
# the same figure printed by two tables of one report: (the activity member, the value-summary member it repeats)
HH_PAIRS = (("act.beginning_value.household", "pvs.last_12_months.beginning_value"),
            ("act.net_gain.household", "pvs.last_12_months.net_gain"),
            ("act.ending_value.household", "pvs.last_12_months.ending_value"))
ACCT_PAIRS = (("act.beginning_value.account", "avs.last_12_months.beginning_value"),
              ("act.net_gain.account", "avs.last_12_months.net_gain"),
              ("act.ending_value.account", "avs.last_12_months.ending_value"))
MODULE_REL = "data/assets/scripts/gold/irpt_reporting/adapters/model_series_windows.py"
TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_model_series_windows.py"
OLD_FILES = ("data/assets/scripts/gold/irpt_reporting/adapters/model_series_market_topic_daily.py",
             "data/assets/scripts/gold/irpt_reporting/tests/test_model_series_market_topic_daily.py",
             "org/standards/IRPT_DASHBD_MARKET_TOPIC_DAILY_CONTRACT.json")
STEMS = P3.STEMS
WINDOWS = P3.WINDOWS


# ---------------------------------------------------------------- the kind carrier (pure functions)
def is_absent_k(v):
    return isinstance(v, dict) and set(v.keys()) == {"absent", "kind"} and isinstance(v["absent"], str) and v["absent"].strip() != "" and v["kind"] in KINDS


def has_absent_key(v):
    return isinstance(v, dict) and "absent" in v


def is_figure_k(v):
    return is_absent_k(v) or (isinstance(v, (int, float)) and not isinstance(v, bool)) or isinstance(v, str)


def check_sample_shape_k(sample, contract, firm=None):
    """round 97's check_sample_shape with the kind-aware absent form: an absent form is exactly {absent, kind}; an asset-class by_row entry may be the text UNHELD."""
    need(isinstance(sample, dict) and set(sample.keys()) == {"household", "values"}, "the sample's top-level keys must be exactly household and values")
    h = sample["household"]
    need(isinstance(h, dict) and set(h.keys()) == {"household_ref", "as_of", "first_data_date", "accounts"}, "household keys %r" % (sorted(h.keys()) if isinstance(h, dict) else h))
    need(P97.ISO.fullmatch(str(h["as_of"])) and P97.ISO.fullmatch(str(h["first_data_date"])), "household as_of and first_data_date must be ISO dates")
    accs = h["accounts"]
    need(isinstance(accs, list) and len(accs) >= 2, "household.accounts must list 2 or more accounts")
    ids = []
    for a in accs:
        need(isinstance(a, dict) and set(a.keys()) == {"account_id", "last4", "first_data_date", "window_status"}, "an account entry's keys are account_id, last4, first_data_date, window_status")
        ws = a["window_status"]
        need(isinstance(ws, dict) and set(ws.keys()) == set(P97.WINDOWS) and all(x in P97.STATUSES for x in ws.values()), "window_status must carry the four windows with a status")
        ids.append(a["account_id"])
    need(ids == sorted(ids) and len(set(ids)) == len(ids), "accounts must be in account_id order, no duplicates")
    members = {m["id"]: m for m in contract["members"]}
    vals = sample["values"]
    need(isinstance(vals, dict) and set(vals.keys()) == set(members.keys()), "values must hold exactly the contract's %d members" % len(members))
    n_by_row = 0
    for k, v in vals.items():
        if isinstance(v, dict) and not has_absent_key(v):
            need(set(v.keys()) == {"by_row"} and isinstance(v["by_row"], dict) and v["by_row"], "member %s holds an unwrapped per-row map" % k)
            need(set(v["by_row"].keys()) <= (set(ids) | CLASSES), "member %s: by_row keys must be account ids or asset classes" % k)
            for key, x in v["by_row"].items():
                need(is_figure_k(x), "member %s entry %s: not a figure, a text or an absent form {absent, kind}" % (k, key))
                if x == UNHELD:
                    need(key in CLASSES, "member %s: the text UNHELD belongs to an asset-class entry, not %s" % (k, key))
            n_by_row += 1
        elif isinstance(v, list):
            need(all(isinstance(s, dict) and set(s.keys()) == {"name", "points"} for s in v), "member %s: a series is a list of {name, points}" % k)
        else:
            need(is_figure_k(v), "member %s holds a value that is not a figure, a text or an absent form {absent, kind}" % k)
        if members[k]["source"] == "ABSENT" and not (firm and firm in (members[k].get("firm_sources") or {})):
            need(is_absent_k(v), "member %s is ABSENT in the contract and must hold the absent form" % k)
    need(n_by_row >= 10, "only %d per-row members" % n_by_row)


def all_absent_forms(values):
    """every absent form of the sample at member grain and at by_row entry grain, as (member id, key or None, form)."""
    out = []
    for k, v in values.items():
        if has_absent_key(v):
            out.append((k, None, v))
        elif isinstance(v, dict) and "by_row" in v:
            for key, x in v["by_row"].items():
                if has_absent_key(x):
                    out.append((k, key, x))
    return out


def kind_problems(values, contract):
    out = []
    members = {m["id"]: m for m in contract["members"]}
    for k, key, x in all_absent_forms(values):
        if not is_absent_k(x):
            out.append("%s%s: an absent form must be exactly {absent, kind} with a kind of %s" % (k, "" if key is None else "[%s]" % key, KINDS))
            continue
        if x["absent"].startswith("history not yet built") and x["kind"] != "INSUFFICIENT_HISTORY":
            out.append("%s: a reason that begins 'history not yet built' must be INSUFFICIENT_HISTORY, got %s" % (k, x["kind"]))
        if x["absent"].startswith("no holding in this asset class"):
            out.append("%s[%s]: an unheld class is the value %s, never an absent form" % (k, key, UNHELD))
    for k, m in members.items():
        if m["source"] == "ABSENT" and k in values and is_absent_k(values[k]) and values[k]["kind"] != "NO_SOURCE_YET":
            out.append("%s: a member the contract sources to ABSENT must be NO_SOURCE_YET, got %s" % (k, values[k]["kind"]))
    return out


def figure_state(x):
    if has_absent_key(x):
        return "absent"
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return "num"
    return "text" if isinstance(x, str) else "other"


def rows_of(v):
    """a by_row map's entries, or the single absent form standing for every account."""
    if isinstance(v, dict) and "by_row" in v:
        return dict(v["by_row"])
    return None


def cross_table_conflicts(values):
    """THE CROSS-TABLE RULE (the mechanical half of J1): a figure absent in one table and filled in another, for the same entity and window, FAILS; two filled values must agree."""
    out = []
    for a, b in HH_PAIRS:
        sa, sb = figure_state(values[a]), figure_state(values[b])
        if (sa == "absent") != (sb == "absent"):
            out.append("%s is %s while %s is %s" % (a, sa, b, sb))
        elif sa == sb == "num" and abs(values[a] - values[b]) > 0.01:
            out.append("%s and %s are both filled and differ" % (a, b))
    for a, b in ACCT_PAIRS:
        ra, rb = rows_of(values[a]), rows_of(values[b])
        if ra is None or rb is None:
            wa = "every account absent" if ra is None else "a per-account map"
            wb = "every account absent" if rb is None else "a per-account map"
            filled_b = rb is not None and any(figure_state(x) != "absent" for x in rb.values())
            filled_a = ra is not None and any(figure_state(x) != "absent" for x in ra.values())
            if (ra is None and filled_b) or (rb is None and filled_a):
                out.append("%s (%s) against %s (%s): one is absent for every account while the other is filled" % (a, wa, b, wb))
            continue
        for key in sorted(set(ra) | set(rb)):
            if key not in ra or key not in rb:
                out.append("%s and %s do not list the same accounts (%s)" % (a, b, key))
                continue
            sa, sb = figure_state(ra[key]), figure_state(rb[key])
            if (sa == "absent") != (sb == "absent"):
                out.append("%s[%s] is %s while %s[%s] is %s" % (a, key[-4:], sa, b, key[-4:], sb))
            elif sa == sb == "num" and abs(ra[key] - rb[key]) > 0.01:
                out.append("%s[%s] and %s[%s] are both filled and differ" % (a, key[-4:], b, key[-4:]))
    return out


def kind_counts(values):
    n = {k: 0 for k in KINDS}
    for _k, _key, x in all_absent_forms(values):
        if is_absent_k(x):
            n[x["kind"]] += 1
    return n


def unheld_count(values):
    return sum(1 for v in values.values() if isinstance(v, dict) and "by_row" in v for key, x in v["by_row"].items() if x == UNHELD and key in CLASSES)


def prior_contract(root, rel, want_sha):
    h = subprocess.run(["git", "-C", str(root), "log", "--format=%H", "-n", "80", "--", rel], capture_output=True, text=True)
    for cm in h.stdout.split():
        b0 = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (cm, rel)], capture_output=True)
        if b0.returncode == 0 and P3.hashlib_sha(b0.stdout) == want_sha:
            return json.loads(b0.stdout.decode("utf-8"))
    return None


# ---------------------------------------------------------------- DB105-1-AC1 (the data half)
def check_kind(root):
    r = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~167/KIND_CARRIER_R105.json")
    c = P.contract(root)
    doc = c["document"]
    ver = tuple(int(x) for x in str(c.get("contract_version") or "0.0.0").split("."))
    need(ver >= (0, 4, 2) and any(x.get("sha256") == V041_SHA for x in c.get("lineage") or []), "the contract must be 0.4.2 or later (a later text edit keeps this round's change) with the 0.4.1 bytes (sha256 %s...) in its lineage" % V041_SHA[:12])
    need(doc.get("absent_kinds") == list(KINDS), "document.absent_kinds must be exactly %s" % list(KINDS))
    ur = str(doc.get("unheld_rule") or "")
    need(UNHELD in ur and "dash" in ur.lower() and "by_row" in ur, "document.unheld_rule must say that a by_row asset-class entry holding the text UNHELD prints the baseline's dash")
    need("kind" in str(doc.get("absent_rule") or "") and "NOT_HELD" not in json.dumps(doc), "document.absent_rule must name the kind field, and NOT_HELD leaves the axis")
    prior = prior_contract(root, CONTRACT_REL, V041_SHA)
    need(prior is not None, "the 0.4.1 contract bytes were not found in the file's git history")
    need(c["members"] == prior["members"], "no member may change in 0.4.2 (the members are byte-for-byte the 0.4.1 members)")
    s = r.get("sample") or {}
    sp = str(s.get("path") or "").replace("\\", "/")
    need(sp.startswith(SAMPLE_DIR) and sp.endswith("HOUSEHOLD_SAMPLE.json") and Path(sp).is_file(), "sample.path must be the private HOUSEHOLD_SAMPLE.json under %s" % SAMPLE_DIR)
    need(not sp.startswith(str(root.resolve()).replace("\\", "/").rstrip("/") + "/"), "the sample is inside the repo: client data never goes there")
    # a record bound to the 0.4.2 bytes stays valid through the lineage after a later text-only edit (0.4.3)
    need(s.get("sha256") == sha(sp) and s.get("contract_sha256") in (sha(root / CONTRACT_REL), V042_SHA), "sample.sha256 and sample.contract_sha256 must equal the sample bytes and the contract bytes (current, or the 0.4.2 bytes this round built against)")
    sm = P.sample_json(sp)
    check_sample_shape_k(sm, c)
    prob = kind_problems(sm["values"], c)
    need(not prob, "kind carrier: %s" % "; ".join(prob[:3]))
    conf = cross_table_conflicts(sm["values"])
    need(not conf, "cross-table rule: %s" % "; ".join(conf[:3]))
    kc = kind_counts(sm["values"])
    need(r.get("absent_by_kind") == kc and sum(kc.values()) == len(all_absent_forms(sm["values"])), "absent_by_kind must equal the checker's own count %s over %d absent forms (remainder 0)" % (kc, len(all_absent_forms(sm["values"]))))
    need(sum(1 for v in kc.values() if v > 0) >= 2, "the sample should carry at least two kinds; one kind for every absence means the kind was not assigned from the reason")
    uc = unheld_count(sm["values"])
    need(uc >= 1 and r.get("unheld_entries") == uc, "unheld_entries must equal the checker's count %d (at least 1)" % uc)
    cr = r.get("cross_table") or {}
    need(cr.get("pairs_checked") == len(HH_PAIRS) + len(ACCT_PAIRS) and cr.get("conflicts") == 0, "cross_table must state pairs_checked %d and conflicts 0" % (len(HH_PAIRS) + len(ACCT_PAIRS)))
    b = r.get("builder") or {}
    bf = str(b.get("file") or "")
    need(bf == D + "0.9.0_WK_IRPT_DASHBD~167/build_sample.py" and (root / bf).is_file() and b.get("sha256") == sha(root / bf) and b.get("tracked") is True, "builder: the tracked copy build_sample.py in the worker's folder, hashed as recorded")
    src = (root / bf).read_text(encoding="utf-8")
    need('"kind"' in src or "'kind'" in src, "the builder must write the kind field")
    P.zero_effects(r)
    print("OK: contract 0.4.2; %d absent forms by kind %s, %d unheld class entries; %d cross-table pairs, 0 conflicts" % (sum(kc.values()), kc, uc, len(HH_PAIRS) + len(ACCT_PAIRS)))


# ---------------------------------------------------------------- DB105-2-AC1 (the render remedy)
def example_printed(example, vt):
    """a kind note's example is printed in the export; an account's last four digits are recorded as #### and match any four digits."""
    if "####" not in example:
        return example in vt
    rx = re.escape(example).replace(re.escape("####"), r"\d{4}")
    return re.search(rx, vt) is not None


def check_render(root):
    r = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~167/RENDER_R105.json")
    k = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~167/KIND_CARRIER_R105.json")
    c = P.contract(root)
    ids = [m["id"] for m in c["members"]]
    unit = {m["id"]: m["unit"] for m in c["members"]}
    sp = str((k.get("sample") or {}).get("path") or "")
    need(Path(sp).is_file() and sha(sp) == (k["sample"] or {}).get("sha256") and r.get("sample_sha256") == sha(sp), "the render record must be bound to the round-105 sample the data cell built (its sha256)")
    sm = P.sample_json(sp)
    outs = r.get("outputs") or {}
    paths = {x: P.private_file(root, outs.get(x), OUT_R, ext, x) for x, ext in (("tab_html", ".html"), ("export_html", ".html"), ("export_pdf", ".pdf"))}
    tab = Path(paths["tab_html"]).read_text(encoding="utf-8")
    exp = Path(paths["export_html"]).read_text(encoding="utf-8")
    texts = (("tab_html", tab), ("export_html", exp))
    for name, text in texts:
        need(set(re.findall(r'data-member="([^"]+)"', text)) == set(ids), "%s must hold all %d member ids" % (name, len(ids)))
    want, scaled = set(), set()
    for kk, v in sm["values"].items():
        if unit[kk] != "percent":
            continue
        vals = [v] if isinstance(v, (int, float)) and not isinstance(v, bool) else ([x for x in v["by_row"].values() if isinstance(x, (int, float)) and not isinstance(x, bool)] if isinstance(v, dict) and "by_row" in v else [])
        for x in vals:
            want.add(("%.1f%%" % x).replace("-0.0%", "0.0%"))
            scaled.add(("%.1f%%" % (x * 100)).replace("-0.0%", "0.0%"))
    scaled -= want
    uc = unheld_count(sm["values"])
    need(uc >= 1, "the sample holds no unheld class entry to check")
    present = {x["kind"] for _a, _b, x in all_absent_forms(sm["values"]) if is_absent_k(x)}
    kn = r.get("kind_notes")
    need(isinstance(kn, list) and sorted(x.get("kind") for x in kn if isinstance(x, dict)) == sorted(present) and all(nes(x.get("example")) and x.get("names_figure") is True for x in kn),
         "kind_notes must hold exactly one {kind, example, names_figure true} for each kind the sample carries (%s)" % sorted(present))
    need(len({x["example"] for x in kn}) == len(kn), "the kind notes must read differently for different kinds")
    for name, text in texts:
        vt = P3.visible_text(text)
        need(all(x in vt for x in want) and not any(x in vt for x in scaled), "%s: a stored percent prints off its stored scale" % name)
        for rx in P3.BANNED:
            m = rx.search(vt)
            need(not m, "%s carries build language: %r" % (name, m.group(0) if m else ""))
        need("Sample Firm" not in vt and P3.FIRM_TITLE in vt, "%s must print the registry's firm title" % name)
        need(UNHELD not in vt and "no holding" not in vt.lower(), "%s prints the unheld value or its reason as text" % name)
        need(vt.count(DASH) >= uc, "%s must print the baseline's dash (an en dash) in at least %d unheld-class cells" % (name, uc))
        for b in BARE:
            need(b not in vt, "%s prints a note with no referent: %r" % (name, b))
        need(not re.search(r";[^.]{0,240}:\s*(is|are)?\s*not available yet", vt, re.I), "%s prints a semicolon run closed by 'is not available yet': one sentence per note" % name)
        for ph in SLOT_PHRASES:
            need(ph.lower() not in vt.lower(), "%s prints a template slot name as a client line: %r" % (name, ph))
        lab = len(re.findall(r"[A-Za-z\)]\*", vt))
        foot = len(re.findall(r"(?<![A-Za-z\)])\*\s+[A-Z]", vt))
        need(lab == 0 or foot >= 1, "%s prints an asterisk on a label (%d) with no footnote line (%d)" % (name, lab, foot))
    vt = P3.visible_text(exp)
    need(all(example_printed(x["example"], vt) for x in kn) and all(";" not in x["example"] for x in kn), "each kind note's example must be printed in the export, as one sentence with no semicolon run")
    need(not any(re.search(r"ending\s+\d{4}(?!\d)", x["example"]) for x in kn), "an example must write an account's last four digits as ####, never the digits (client data stays out of the repo)")
    chart = "overview.chart.portfolio_performance_last_12_months"
    names = [str(s.get("name", "")) for s in (sm["values"][chart] if isinstance(sm["values"][chart], list) else []) if isinstance(s, dict)]
    at = exp.find('data-member="%s"' % chart)
    nxt = exp.find('data-member="', at + 10)
    seg = P3.visible_text(exp[at: nxt if nxt > 0 else at + 4000])
    if not any("household" in n.lower() for n in names):
        need("household" not in seg.lower(), "the 12-month chart is titled for a household line the sample does not carry")
    fee = "convention.fee_basis_label"
    need(has_absent_key(sm["values"][fee]) is False or "before advisory fees" not in vt.lower(), "the before-fee line prints while its member is absent")
    need(r.get("disclosure_pointer_kept") is True and r.get("kind_read_from_field") is True and r.get("fee_line_follows_member") is True, "disclosure_pointer_kept, kind_read_from_field and fee_line_follows_member must be true")
    P.footer_ok(exp, sm["household"]["as_of"])
    pages = P.pdf_pages(paths["export_pdf"])
    need(pages >= 8, "the PDF holds %d pages" % pages)
    P.check_pdf_read(r, pages)
    need(sum(1 for x in r["pdf_clipping"] if x["clipped"]) == 0, "a page is recorded clipped: fix it and re-render")
    pt = r.get("portal") or {}
    need(pt.get("branch") == "wk-IRPT_DASHBD-167-portal" and P.HEXC.fullmatch(str(pt.get("commit") or "")), "portal %r: the branch wk-IRPT_DASHBD-167-portal and a commit" % pt)
    g = subprocess.run(["git", "-C", str(root / "portal"), "cat-file", "-t", pt["commit"]], capture_output=True, text=True)
    need(g.returncode == 0 and g.stdout.strip() == "commit" and isinstance(pt.get("files_changed"), list) and pt["files_changed"] and all(str(f).startswith("src/pages/InvestorReporting/") for f in pt["files_changed"]), "portal commit and files under src/pages/InvestorReporting/")
    g1 = subprocess.run(["git", "-C", str(root / "portal"), "grep", "-c", "absentKindOf", pt["commit"], "--", "src/pages/InvestorReporting"], capture_output=True, text=True)
    need(g1.returncode == 1 and g1.stdout.strip() == "", "absentKindOf must be deleted from src/pages/InvestorReporting at the portal commit (rc %d)" % g1.returncode)
    g2 = subprocess.run(["git", "-C", str(root / "portal"), "grep", "-l", "-w", "kind", pt["commit"], "--", "src/pages/InvestorReporting/dashboard/report", "src/pages/InvestorReporting/render/performance/report"], capture_output=True, text=True)
    need(g2.returncode == 0 and g2.stdout.strip() != "", "the report components must read the kind field")
    t = r.get("tests") or {}
    need(nes(t.get("new_file")) and t.get("mutant_failed") is True and t.get("lint_errors") == 0 and t.get("typecheck_errors") == 0 and (t.get("suite_after") or {}).get("new_failing_ids") == [], "tests: a new file, a failing mutant, lint 0, typecheck 0, no new failing test")
    P.zero_effects(r)
    print("OK: %d unheld cells print the dash; kind notes for %s read from the field; no slot name, bare note or semicolon run; %d PDF pages read, none clipped" % (uc, sorted(present), pages))


# ---------------------------------------------------------------- DB105-3-AC1 (the model windows reader)
def expected_windows(rows, R, hh_first, tc):
    out = {}
    q0 = dt.date(R.year, 3 * ((R.month - 1) // 3) + 1, 1)
    los = {"qtd": q0, "ytd": dt.date(R.year, 1, 1), "last_12_months": dt.date(R.year - 1, R.month, R.day) + dt.timedelta(days=1),
           "since_inception": dt.date.fromisoformat(str(hh_first)[:10]) + dt.timedelta(days=1)}
    have = {d for d, _ in rows}
    for w, lo in los.items():
        if not rows or rows[0][0] > lo or any(d not in have for d in tc.trading_days_between(lo, R)):
            out[w] = None
            continue
        prod = 1.0
        for d, x in rows:
            if lo <= d <= R:
                prod *= 1.0 + x
        out[w] = round((prod - 1.0) * 100.0, 1)
    return out


def synth_series(tc, start, end, drop=None):
    rows = []
    i = 0
    for d in tc.trading_days_between(start, end):
        if drop is not None and d == drop:
            continue
        rows.append((d, 0.0003 + 0.0002 * ((i * 7) % 5) - 0.0003 * (i % 3 == 0)))
        i += 1
    return rows


def check_reader(root):
    r = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~168/MODEL_WINDOWS_READER.json")
    for old in OLD_FILES:
        need(not (root / old).exists(), "%s is retired and must be removed" % old)
    m = r.get("module") or {}
    need(m.get("file") == MODULE_REL and (root / MODULE_REL).is_file() and m.get("sha256") == sha(root / MODULE_REL) and m.get("tracked") is True, "module: the tracked file %s hashed as recorded" % MODULE_REL)
    t = r.get("tests") or {}
    need(t.get("file") == TEST_REL and (root / TEST_REL).is_file() and is_int(t.get("passed")) and t["passed"] >= 4 and t.get("failed") == 0 and t.get("mutant_failed") is True, "tests: %s, 4 or more passing, none failing, a failing mutant" % TEST_REL)
    q = subprocess.run([sys.executable, "-I", "-m", "pytest", "-q", str((root / TEST_REL).resolve())], capture_output=True, text=True, cwd=str(root))
    need(q.returncode == 0, "the test file does not pass when the checker runs it")
    sc = json.loads((root / SERIES_REL).read_bytes().decode("utf-8"))
    ver = tuple(int(x) for x in str(sc.get("contract_version") or "0.0.0").split("."))
    need(ver > (0, 1, 0) and any(x.get("sha256") == SERIES_V010_SHA for x in sc.get("lineage") or []), "the series contract must be above 0.1.0 with the 0.1.0 bytes (sha256 %s...) in its lineage" % SERIES_V010_SHA[:12])
    stext = json.dumps(sc)
    need('"source"' in stext and '"data_as_of"' in stext, "the series contract must carry the claim fields source and data_as_of for the model windows")
    sys.path.insert(0, str(root / "lib"))
    import trading_calendar as tc
    spec = importlib.util.spec_from_file_location("msw", str(root / MODULE_REL))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    need(hasattr(mod, "windows_from_series") and hasattr(mod, "source_claim") and hasattr(mod, "read_served_series"), "the module must expose read_served_series, windows_from_series and source_claim")
    R = dt.date(2026, 10, 12)
    hh = "2024-07-08"
    rows = synth_series(tc, dt.date(2024, 6, 3), R)
    series = {s: list(rows) for s in STEMS}
    got = mod.windows_from_series(series, R, hh)
    want = expected_windows(rows, R, hh, tc)
    need(isinstance(got, dict) and sorted(got) == sorted(STEMS), "windows_from_series must return one entry per stem %s" % list(STEMS))
    for s in STEMS:
        for w in WINDOWS:
            need(got[s].get(w) == want[w], "windows_from_series %s %s = %r, independent compounding gives %r" % (s, w, got[s].get(w), want[w]))
    gap = dt.date(2026, 10, 6)
    rows2 = synth_series(tc, dt.date(2024, 6, 3), R, drop=gap)
    got2 = mod.windows_from_series({s: list(rows2) for s in STEMS}, R, hh)
    need(all(got2[s][w] is None for s in STEMS for w in WINDOWS), "a window that holds a missing trading day must be None (never interpolated); got %r" % got2[STEMS[0]])
    cl = mod.source_claim("json/benchmarks/model_portfolio_timeseries.json", "VERSIONXYZ123", "2026-10-13")
    need(isinstance(cl, dict) and "json/benchmarks/model_portfolio_timeseries.json" in str(cl.get("source")) and "VERSIONXYZ123" in str(cl.get("source")) and cl.get("data_as_of") == "2026-10-13", "source_claim must return {source (key and VersionId), data_as_of}")
    lr = r.get("live_read") or {}
    need(nes(lr.get("version_id")) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(lr.get("data_as_of") or "")) and lr.get("members_total") == 32 and is_int(lr.get("members_filled")) and lr["members_filled"] <= 32, "live_read: version_id, data_as_of (ISO), members_total 32 and members_filled (the count printed)")
    need(r.get("writes_in_this_cell") is False and r.get("no_other_key_moves") is True and nes(r.get("note")), "writes_in_this_cell false, no_other_key_moves true and a one-sentence note")
    P.zero_effects(r)
    print("OK: reader %s compounds the four windows for %d stems equal to independent compounding; a gap day gives None; %d of 32 benchmark members fill on the live read" % (MODULE_REL.rsplit("/", 1)[1], len(STEMS), lr["members_filled"]))


# ---------------------------------------------------------------- self test of the pure functions
def selftest():
    c = P.contract(Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path(".").resolve())
    def ok(kind):
        return {"absent": "why", "kind": kind}

    vals = {m["id"]: {"absent": "x", "kind": "NO_SOURCE_YET"} for m in c["members"] if m["source"] == "ABSENT"}
    n = 0

    def arm(name, cond):
        nonlocal n
        n += 1
        if not cond:
            print("SELFTEST FAIL: %s" % name)
            sys.exit(1)

    pair_hh = {"act.beginning_value.household": 5.0, "pvs.last_12_months.beginning_value": 5.0, "act.net_gain.household": 1.0, "pvs.last_12_months.net_gain": 1.0, "act.ending_value.household": 6.0, "pvs.last_12_months.ending_value": 6.0}
    pair_ac = {}
    for a, b in ACCT_PAIRS:
        pair_ac[a] = {"by_row": {"1111111111": 2.0, "2222222222": 3.0}}
        pair_ac[b] = {"by_row": {"1111111111": 2.0, "2222222222": 3.0}}
    green = dict(pair_hh, **pair_ac)
    arm("green: matching pairs, no conflict", cross_table_conflicts(green) == [])
    red = dict(green)
    red["act.beginning_value.household"] = ok("INSUFFICIENT_HISTORY")
    arm("red: absent in the activity table, filled in the value summary", len(cross_table_conflicts(red)) == 1)
    red2 = dict(green)
    red2["act.net_gain.account"] = {"by_row": {"1111111111": ok("INSUFFICIENT_HISTORY"), "2222222222": 3.0}}
    arm("red: one account absent in one table and filled in the other", len(cross_table_conflicts(red2)) == 1)
    red3 = dict(green)
    red3["act.ending_value.account"] = ok("SOURCE_BREAK")
    arm("red: a whole account member absent while its pair is filled", len(cross_table_conflicts(red3)) == 1)
    red4 = dict(green)
    red4["act.ending_value.household"] = 99.0
    arm("red: both filled, different", len(cross_table_conflicts(red4)) == 1)
    both_absent = dict(green)
    both_absent["act.beginning_value.household"] = ok("INSUFFICIENT_HISTORY")
    both_absent["pvs.last_12_months.beginning_value"] = ok("INSUFFICIENT_HISTORY")
    arm("green: absent in both tables (the same truth twice)", cross_table_conflicts(both_absent) == [])
    arm("is_absent_k: an old absent form with no kind is refused", not is_absent_k({"absent": "x"}) and is_absent_k(ok("SOURCE_BREAK")) and not is_absent_k({"absent": "x", "kind": "NOT_HELD"}))
    kv = dict(vals)
    kv["hold.net_gain_ytd"] = {"absent": "history not yet built: gold account_activity_daily holds 20 trading days", "kind": "NO_SOURCE_YET"}
    arm("red: 'history not yet built' with a kind other than INSUFFICIENT_HISTORY", any("history not yet built" in p for p in kind_problems(kv, c)))
    kv2 = dict(vals)
    kv2["hold.allocation"] = {"by_row": {"cash": 1.0, "alternatives": {"absent": "no holding in this asset class on as_of", "kind": "NO_SOURCE_YET"}}}
    arm("red: an unheld class as an absent form", any("unheld class" in p for p in kind_problems(kv2, c)))
    kv3 = dict(vals)
    first = next(k for k, m in ((m["id"], m) for m in c["members"]) if m["source"] == "ABSENT")
    kv3[first] = ok("SOURCE_BREAK")
    arm("red: a contract-ABSENT member that is not NO_SOURCE_YET", any("ABSENT" in p for p in kind_problems(kv3, c)))
    arm("green: kind_problems on well-formed forms", kind_problems({first: {"absent": "no source", "kind": "NO_SOURCE_YET"}}, c) == [])
    arm("kind_counts and unheld_count", kind_counts({"a": ok("SOURCE_BREAK"), "b": {"by_row": {"x": ok("NO_SOURCE_YET")}}}) == {"NO_SOURCE_YET": 1, "INSUFFICIENT_HISTORY": 0, "SOURCE_BREAK": 1}
        and unheld_count({"h": {"by_row": {"cash": 1.0, "alternatives": UNHELD, "9999999999": UNHELD}}}) == 1)
    arm("example_printed: a masked last four digits match any four digits", example_printed("Account ending ####: x.", "a b Account ending 1234: x. c") and not example_printed("Account ending ####: x.", "Account ending 12: x.") and example_printed("Plain note.", "see Plain note. here") and not example_printed("Plain note.", "other"))
    sys.path.insert(0, str(Path(sys.argv[2]).resolve() / "lib" if len(sys.argv) > 2 else Path("lib").resolve()))
    import trading_calendar as tc
    R = dt.date(2026, 10, 12)
    rows = synth_series(tc, dt.date(2024, 6, 3), R)
    w = expected_windows(rows, R, "2024-07-08", tc)
    arm("expected_windows opens all four windows on a full series", all(isinstance(w[x], float) for x in WINDOWS))
    w2 = expected_windows(synth_series(tc, dt.date(2024, 6, 3), R, drop=dt.date(2026, 10, 6)), R, "2024-07-08", tc)
    arm("expected_windows gives None for every window that holds a missing trading day", all(w2[x] is None for x in WINDOWS))
    print("SELFTEST OK: %d arms" % n)


FNS = {"DB105-1-AC1": check_kind, "DB105-2-AC1": check_render, "DB105-3-AC1": check_reader}


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
        print("%s FAIL" % (cid or "DB105"))
        sys.exit(1)
    except (KeyError, TypeError, ValueError, AttributeError, IndexError, ImportError) as e:
        print("FAIL: malformed record: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % cid)
        sys.exit(1)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
