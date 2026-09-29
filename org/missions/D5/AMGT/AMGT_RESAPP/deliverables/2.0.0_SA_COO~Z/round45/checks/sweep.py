"""AMGT_RESAPP round 49 (AMGT-xx-1; round 43's sweep, its page reader re-keyed) -- FWD-30's ONE GRADER: does the page's reading of a
security equal its rich export, figure by figure, cite by cite, absence by absence, case by case?

Per folder of the research library (universe.json snapshot, --live library, or --folders-file):
  key      scoped_amgt.resolve_identity(crosswalk.harvester_key(folder, pilots)[0]); a folder whose identity does not resolve is
           COUNTED as unidentified and printed, never a CAPTURE_FAILED row
  page     the deployed function's served routes, captured once into --cache by 0.9.0_WK_AMGT_RESAPP~158's capture_lib
           -> render_page_html (page_render.cjs: the SecurityAnalysis page rendered from that capture by react-dom/server)
           -> page_facts_from_html: FIGURES / CITES / ABSENCES / CASES read ONLY from the page's data attributes, never from
              its visible words, so a page rewrite that keeps its data leaves the grade where it was
  export   with --served the DEPLOYED body captured beside the page (print?format=rich); without it, scoped_amgt.handler
           (print?format=rich) run IN PROCESS on this tree's code, every reader stubbed from that capture
           -> rich_facts: the same four sets, in the same keys
  compare  compare_facts(page, rich) -> verdict + a reason naming EVERY class that differs and no other
The exportCompare.harness.cjs (another project's) is NOT called: it matched absence lines by their words.
Writes a TSV with rp-1's header (plus the CASES counts) to --out and prints the verdict counts and ONE grade line
`FWD-30 GRADE: equal E of I identified names; unidentified U of F folders; keyed on: data-attributes`. Reads AWS (lambda invoke,
crosswalk); writes nothing to it. Exit 0 only when E == I.
KEYS (page attribute -> rich line), one row per class:
  FIGURES   ("HEADER", m)          data-card-figure-mnemonic (data-card-figure-state=SERVED)   -> "## Header" table row m
            ("FISCAL", m, year)    data-model-row=m x data-model-cell, year = the sheet's column header -> "## Fiscal year Y" row m
            ("OFFICER", name)      data-exec-officer                                            -> "## Management/Board" table row
  CITES     ("THESIS", id)         data-thesis-passage                                          -> "> <id> -- accession ..."
            ("POSTURE", cite)      data-posture-cite (its data-cite-resolved is the page's own resolution, not compared)
                                                                                                -> "> cites: a, b"
  ABSENCES  ("MODEL_LINE", m, reason)  data-model-line-refusal in data-model-row=m              -> "m: REFUSED -- reason"
            ("MODEL_NOTE", reason)     data-model-absence                                       -> "## Model Notes" "...: ABSENT -- reason"
            ("PEERS_COLUMN", column)   data-absent-column                                       -> "## Peers" "column: ABSENT -- ..."
            ("EXEC", status[, because])  data-exec-status / data-exec-absent-because            -> "Exec Management: ABSENT (because)."
            ("EXEC_CEO_PROFILE", state)  data-ceo-profile (not CONFIRMED)                       -> "CEO public-profile reading: state"
            ("POSTURE", status, reason)  data-posture-status / data-posture-reason (not SERVED) -> "Posture: ABSENT -- reason"
            ("POSTURE_NO_CALL",)         data-posture-verdict="absent"                          -> "ABSENT -- no call was made: ..."
            ("DESCRIPTION", "ABSENT")    data-header-description="ABSENT"                       -> "Description: ABSENT -- ..."
  CASES     ("CASE", name, status, detail) data-model-case / -case-status / -case-reason (ABSENT) or -case-formula (SERVED)
                                                                                                -> "## Model Cases" line
FACTS THE PAGE CARRIES NO ATTRIBUTE FOR (rows in the AMGT_RESAPP surprise channel, Z-W173-S*): a figure's VALUE, the identity
line (sector / country / currency), a served case's VALUE, the reason of a peers absent column, of a description absence and of a
posture no-call, and the thesis-driver chart's absence (the page carries data-driver-chart-reason, the export names the driver's series
-- no shared key, so it is not graded; the export states it for an undrafted thesis whose page renders no chart). Each is graded on what the attributes DO carry (its identity), never on the page's words.
usage: PYTHONPATH=<repo root> python <this> --cache <dir outside the repo> --out <tsv> [--only KEY,...] [--served] [--live]"""
import argparse
import importlib.util
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path.cwd()
UNIVERSE = ROOT / "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~4/universe.json"
CAPTURE_LIB = ROOT / "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PAGE_RENDER = Path(__file__).resolve().parent / "page_render.cjs"
CLASSES = (("FIGURES", "fig"), ("CITES", "cit"), ("ABSENCES", "abs"), ("CASES", "cas"))
COUNTS = [s + "_" + c for _, s in CLASSES for c in ("page", "rich", "same", "missing", "extra")]
HEADER = ["folder", "security_key"] + COUNTS + ["verdict", "reason"]


def load_capture_lib():
    spec = importlib.util.spec_from_file_location("capture_lib", str(CAPTURE_LIB))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def captured(cache, key, cl):
    if not key:
        raise ValueError("no security key: the folder's identity does not resolve")
    d = Path(cache) / re.sub(r"[^A-Za-z0-9_.-]", "_", key)
    served = d / "served"
    fx = next(iter(sorted(served.glob("served_fixture.*.json"))), None) if served.exists() else None
    if fx is None:
        # The page routes and the model block are read at the SAME moment, so a cached pair never mixes vintages: the
        # store moves under a round (measured 2026-09-25 ~05:0xZ, when AMGT_CORPUS re-pulled the blocks after capture).
        from lib.research.api import scoped_amgt as sa
        cl.capture(key, str(d))
        (d / "model_block.json").write_text(json.dumps(sa.read_model_block(key)), encoding="utf-8")
        fx = next(iter(sorted(served.glob("served_fixture.*.json"))), None)
    return d, fx


def rebuild(key, fixture_path, out_path):
    # The MODEL BLOCK is the store's own block (scoped_amgt.read_model_block, what the deployed function reads), saved in the
    # cache at capture time beside the page routes: the thesis payload's fiscal_year_figures are a SUBSET of the block
    # (measured on 992_HK_Equity: 2016-2026 against the block's 2016-2029), so a block rebuilt from the thesis understates the
    # export. Every other reader is stubbed from the capture.
    from lib.research.api import scoped_amgt as sa
    from lib.research.print import render_pack as rp
    bundle = json.loads(Path(fixture_path).read_text(encoding="utf-8"))
    thesis = bundle["thesis"]
    overlay = bundle.get("overlay") or {}
    names = ("resolve_identity", "read_model_block", "read_thesis_bundle", "read_peer_set", "read_posture", "read_description")
    saved = {n: getattr(sa, n) for n in names}
    saved_key = rp.security_key
    try:
        # LOCAL ONLY: Windows refuses '*' in a file name (WALMEX*_MM_Equity); the Lambda's Linux temp dir takes it as is.
        rp.security_key = lambda security: saved_key(security).replace("*", "-")
        sa.resolve_identity = lambda requested: {"security_key": key, "requested": requested, "identity_status": "RESOLVED"}
        block = json.loads((Path(fixture_path).parent.parent / "model_block.json").read_text(encoding="utf-8"))
        sa.read_model_block = lambda security_key: block
        sa.read_thesis_bundle = lambda security_key, identity=None: thesis
        sa.read_peer_set = lambda security_key: bundle.get("peers")
        sa.read_posture = lambda security_key, identity=None: thesis.get("posture")
        sa.read_description = lambda security_key, identity=None, model_block=None, drafting=None: overlay.get("description")
        event = {"rawPath": "/api/scoped/amgt/security/%s/print" % key, "httpMethod": "GET",
                 "headers": {"X-Firm-Id": "opal-capital"}, "queryStringParameters": {"format": "rich"}}
        resp = sa.handler(event)
    finally:
        for n, f in saved.items():
            setattr(sa, n, f)
        rp.security_key = saved_key
    if resp.get("statusCode") != 200:
        return "rebuild statusCode=%s body=%s" % (resp.get("statusCode"), str(resp.get("body"))[:120])
    Path(out_path).write_text(resp["body"], encoding="utf-8")
    return None


def render_page_html(fixture_path):
    """The SecurityAnalysis page rendered from a captured served fixture (node, cwd=portal/, react-dom/server), every tab plus each
    header card's and thesis card's window, as one HTML string. Nothing is read out of it here."""
    p = subprocess.run(["node", str(PAGE_RENDER), str(Path(fixture_path).resolve())], cwd=str(ROOT / "portal"),
                       capture_output=True, text=True, encoding="utf-8")
    if p.returncode != 0 or not p.stdout.strip():
        raise RuntimeError("page render rc=%s: %s" % (p.returncode, (p.stderr or "").strip()[-200:]))
    return p.stdout


class _PageReader(HTMLParser):
    """Walks the rendered page and collects facts from data attributes ONLY. The one piece of text it ever reads is the Model
    sheet's own column headers (the years), which are the coordinate of a cell that carries no year attribute."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.f = {"FIGURES": set(), "CITES": set(), "ABSENCES": set(), "CASES": set()}
        self.in_sheet = self.in_thead = self.in_th = False
        self.years = []
        self.row = None          # the data-model-row mnemonic being walked
        self.td = 0              # td index inside that row (0 = the label cell)
        self.row_cells = []      # td index of every data-model-cell td in the row
        self.row_refused = False
        self.row_refusals = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        f = self.f
        if tag == "table":
            self.in_sheet = "data-model-sheet" in a
        elif self.in_sheet and tag == "thead":
            self.in_thead = True
        elif self.in_thead and tag == "th":
            self.in_th = True
            self.years.append("")
        elif self.in_sheet and tag == "tr" and "data-model-row" in a:
            self.row, self.td, self.row_cells, self.row_refused, self.row_refusals = a["data-model-row"], -1, [], False, []
        elif self.row is not None and tag == "td":
            self.td += 1
            if a.get("data-model-refused") in ("", "true"):  # a boolean marker: any other value is not that marker
                self.row_refused = True
            elif "data-model-cell" in a:
                self.row_cells.append(self.td)
        if "data-model-line-refusal" in a and self.row is not None:
            self.row_refusals.append(a["data-model-line-refusal"].strip())
        if tag == "tr" and "data-exec-officer" in a:
            f["FIGURES"].add(("OFFICER", a["data-exec-officer"]))
        if a.get("data-card-figure-state") == "SERVED" and a.get("data-card-figure-mnemonic"):
            f["FIGURES"].add(("HEADER", a["data-card-figure-mnemonic"]))
        if a.get("data-thesis-passage"):
            f["CITES"].add(("THESIS", a["data-thesis-passage"]))
        if a.get("data-posture-cite"):
            f["CITES"].add(("POSTURE", a["data-posture-cite"]))
        if "data-model-absence" in a:
            f["ABSENCES"].add(("MODEL_NOTE", a["data-model-absence"].strip()))
        if "data-absent-column" in a:
            f["ABSENCES"].add(("PEERS_COLUMN", a["data-absent-column"]))
        st = a.get("data-exec-status")
        if st and st != "SERVED":
            if st == "ABSENT":
                f["ABSENCES"].add(("EXEC", "ABSENT", a.get("data-exec-absent-because", "null")))
            else:
                f["ABSENCES"].add(("EXEC", st))
        cp = a.get("data-ceo-profile")
        if cp and cp != "CONFIRMED":
            f["ABSENCES"].add(("EXEC_CEO_PROFILE", cp))
        ps = a.get("data-posture-status")
        if ps and ps != "SERVED":
            f["ABSENCES"].add(("POSTURE", ps, "" if ps == "NOT_READ" else a.get("data-posture-reason", "").strip()))
        if a.get("data-posture-verdict") == "absent":
            f["ABSENCES"].add(("POSTURE_NO_CALL",))
        if a.get("data-header-description") == "ABSENT":
            f["ABSENCES"].add(("DESCRIPTION", "ABSENT"))
        if "data-model-case" in a and "data-model-case-status" in a:
            status = a["data-model-case-status"]
            detail = a.get("data-model-case-formula", "") if status == "SERVED" else a.get("data-model-case-reason", "").strip()
            f["CASES"].add(("CASE", a["data-model-case"], status, detail))

    def handle_data(self, data):
        if self.in_th:
            self.years[-1] += data.strip()

    def handle_endtag(self, tag):
        if tag == "th":
            self.in_th = False
        elif tag == "thead":
            self.in_thead = False
        elif tag == "table":
            self.in_sheet = False
        elif tag == "tr" and self.row is not None:
            if self.row_refused:
                if self.row_refusals:
                    self.f["ABSENCES"].add(("MODEL_LINE", self.row, self.row_refusals[0]))
            else:
                for i in self.row_cells:
                    if 1 <= i <= len(self.years) - 1:
                        self.f["FIGURES"].add(("FISCAL", self.row, self.years[i]))
            self.row = None


def page_facts_from_html(html):
    """FIGURES / CITES / ABSENCES / CASES of the rendered page, read only from its data attributes. Keys: see the module docstring."""
    r = _PageReader()
    r.feed(html)
    r.close()
    return r.f


IDENTITY_LINE = ("GICS_SECTOR_NAME", "CNTRY_OF_DOMICILE", "CRNCY")  # on the page as plain text with NO attribute (row Z-W173-S1)
MID_DOT = "·"


def _bundle(fixture):
    if isinstance(fixture, dict):
        return fixture
    return json.loads(Path(fixture).read_text(encoding="utf-8")) if fixture else {}


def rich_facts(rich_text, fixture=None):
    """The same four sets from the rich export's own lines. `fixture` (the captured served payload, a path or its dict) is read only
    for what the rich text cannot say: which case a labelled case line ("Historical-multiple reference") is."""
    f = {"FIGURES": set(), "CITES": set(), "ABSENCES": set(), "CASES": set()}
    cases = ((_bundle(fixture).get("thesis") or {}).get("model_cases") or {})
    label_name = {}
    for nm in ("upside", "base", "downside"):
        c = cases.get(nm)
        if isinstance(c, dict) and c.get("label"):
            label_name[c["label"]] = nm.capitalize()
    section = None
    for raw in rich_text.split("\n"):
        line = raw.strip()
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        m = re.match(r"^> (\S+) -- accession ", line)
        if m:
            f["CITES"].add(("THESIS", m.group(1)))
            continue
        m = re.match(r"^> cites: (.+)$", line)
        if m:
            for c in m.group(1).split(", "):
                f["CITES"].add(("POSTURE", c.strip()))
            continue
        m = re.match(r"^(\S+): REFUSED -- (.+)$", line)
        if m:
            f["ABSENCES"].add(("MODEL_LINE", m.group(1), m.group(2).strip()))
            continue
        if section == "Header" or (section or "").startswith("Fiscal year "):
            m = re.match(r"^\|\s*(\S+)\s*\|\s*(.+?)\s*\|$", line)
            if m and MID_DOT in m.group(2) and "[REFUSED:" not in m.group(2):
                if section == "Header":
                    if m.group(1) not in IDENTITY_LINE:
                        f["FIGURES"].add(("HEADER", m.group(1)))
                else:
                    f["FIGURES"].add(("FISCAL", m.group(1), section.split(" ", 2)[2]))
            continue
        if section == "Management/Board":
            m = re.match(r"^Exec Management: ABSENT \((.+)\)\.$", line)
            if m:
                f["ABSENCES"].add(("EXEC", "ABSENT", m.group(1)))
            elif line == "Exec Management: the read did not complete.":
                f["ABSENCES"].add(("EXEC", "READ_FAILED"))
            elif line == "Exec Management: not carried on this payload.":
                f["ABSENCES"].add(("EXEC", "NOT_READ"))
            m = re.match(r"^CEO public-profile reading: (\S+)$", line)
            if m and m.group(1) != "CONFIRMED":
                f["ABSENCES"].add(("EXEC_CEO_PROFILE", m.group(1)))
            m = re.match(r"^\|\s*(.+?)\s*\|.*\|$", line)
            if m and m.group(1) != "Name" and not set(line) <= set("|- "):
                f["FIGURES"].add(("OFFICER", m.group(1)))
            continue
        if section == "Peers":
            m = re.match(r"^(.+?): ABSENT -- (.+)$", line)
            if m:
                f["ABSENCES"].add(("PEERS_COLUMN", m.group(1)))
            continue
        if section == "Analyst Posture":
            m = re.match(r"^Posture: ABSENT -- (.+?)(?:\. Nothing is rendered in its place\.)?$", line)
            if m:
                f["ABSENCES"].add(("POSTURE", "ABSENT", m.group(1).strip()))
            elif line == "Posture: not carried on this payload.":
                f["ABSENCES"].add(("POSTURE", "NOT_READ", ""))
            elif line.startswith("Posture: the read did not complete"):
                f["ABSENCES"].add(("POSTURE", "READ_FAILED", ""))
            elif line.startswith("ABSENT -- no call was made:"):
                f["ABSENCES"].add(("POSTURE_NO_CALL",))
            continue
        if section == "Model Notes":
            if line.startswith("The chart: ABSENT"):
                continue  # the export names the driver's series; the page's data-driver-chart-reason is the served reason: no shared key (row Z-W173-S4)
            m = re.match(r"^.+?: ABSENT -- (.+)$", line)
            if m:
                f["ABSENCES"].add(("MODEL_NOTE", m.group(1).strip()))
            continue
        if section == "Model Cases":
            m = re.match(r"^(.+?): (SERVED|ABSENT) -- (.+)$", line)
            if m:
                head, status, detail = m.groups()
                name = head[:-5] if head.endswith(" case") else label_name.get(head, head)
                if status == "SERVED":
                    cut = detail.find(" (")
                    detail = detail[cut + 2:-1] if cut != -1 and detail.endswith(")") else ""
                f["CASES"].add(("CASE", name, status, detail.strip()))
    # a description absence is stated in the header and again inside the thesis: one fact (a set), wherever it sits
    if re.search(r"^Description: ABSENT -- ", rich_text, re.M):
        f["ABSENCES"].add(("DESCRIPTION", "ABSENT"))
    return f


def compare_facts(page, rich):
    """One comparison that names what differs: the verdict, a reason naming EVERY class that differs and no other ("" when OK), and
    per-class counts (page / rich / same / missing / extra) under the TSV's column names."""
    row, bad = {}, []
    for label, s in CLASSES:
        p, r = set(page.get(label) or ()), set(rich.get(label) or ())
        row.update({s + "_page": len(p), s + "_rich": len(r), s + "_same": len(p & r), s + "_missing": len(p - r),
                    s + "_extra": len(r - p)})
        if p != r:
            bad.append(label)
    row["verdict"] = "NOT_OK" if bad else "OK"
    row["reason"] = ("%s differ" % "+".join(bad)) if bad else ""
    return row


def compare(fixture_path, rich_path):
    try:
        page = page_facts_from_html(render_page_html(fixture_path))
    except RuntimeError as exc:
        return None, str(exc)
    rich = rich_facts(Path(rich_path).read_text(encoding="utf-8"), fixture_path)
    row = compare_facts(page, rich)
    row["_diff"] = {lab: (sorted(map(str, page[lab] - rich[lab])), sorted(map(str, rich[lab] - page[lab]))) for lab, _ in CLASSES}
    return row, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", default="")
    ap.add_argument("--served", action="store_true")
    # --live: the population is the LIVE research library (1.0.0_SA_CTO~Z ruling @ea24753b1b: 94 on 2026-09-25), read with
    # the producer's own reader at run time and printed with its read time -- never pinned. Default stays the 89 snapshot.
    ap.add_argument("--live", action="store_true")
    # --require-cases (R-8, round 42 analysis): the harness must print a CASES line for every compared name, and across the
    # sweep the page must show at least one case value, every one reaching the export, with none extra.
    ap.add_argument("--require-cases", action="store_true")
    # --folders-file: a PINNED population, one folder per line (# comments allowed) -- the live library AS OF a stated read.
    ap.add_argument("--folders-file", default="")
    # --diff: print, per NOT_OK name, the facts the page has that the export lacks and the export has that the page lacks.
    ap.add_argument("--diff", action="store_true")
    a = ap.parse_args()
    from lib.research.identity import crosswalk
    from lib.research.api import scoped_amgt as sa
    cl = load_capture_lib()
    pilots = crosswalk.load_pilots()
    if a.folders_file:
        lines = open(a.folders_file, encoding="utf-8").read().splitlines()
        folders = [ln for ln in lines if ln.strip() and not ln.startswith("#")]
        print("population: PINNED %s, %d folders" % (a.folders_file, len(folders)), flush=True)
    elif a.live:
        import datetime
        from lib.research.corpus import library
        root = library.library_root()
        folders = list(library.list_folders(root))
        print("population: LIVE research library %s, %d folders, read_at %s" % (
            root, len(folders), datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")), flush=True)
    else:
        folders = [n["folder"] for n in json.load(open(UNIVERSE, encoding="utf-8"))["names"]]
        print("population: universe.json snapshot (read 2026-09-10T23:18Z), %d folders" % len(folders), flush=True)
    only = set(x for x in a.only.split(",") if x)
    rows, unidentified = [], []
    for i, folder in enumerate(folders, 1):
        try:
            key = sa.resolve_identity(crosswalk.harvester_key(folder, pilots)[0]).get("security_key")
        except Exception:
            key = None
        if not key:
            # a folder whose identity does not resolve is COUNTED and printed, never a CAPTURE_FAILED row or a TypeError
            unidentified.append(folder)
            print("%d/%d %s UNIDENTIFIED (identity does not resolve; not graded)" % (i, len(folders), folder), flush=True)
            continue
        if only and key not in only:
            continue
        row = {"folder": folder, "security_key": key}
        try:
            d, fx = captured(a.cache, key, cl)
            if a.served:
                rich = next(iter(sorted((d / "served").glob("*.rich.md"))), None)
                err = None if rich else "no served rich body captured"
            else:
                rich = d / "local.rich.md"
                err = rebuild(key, fx, rich)
            if not err:
                cmp_row, err = compare(fx, rich)
            if err:
                row.update({c: "" for c in COUNTS})
                row.update(verdict="CAPTURE_FAILED", reason=err)
            else:
                row.update(cmp_row)
        except Exception as exc:  # a failed read is a row, never a silent skip
            row.update({c: "" for c in COUNTS})
            row.update(verdict="CAPTURE_FAILED", reason="%s: %s" % (type(exc).__name__, str(exc)[:160]))
        rows.append(row)
        print("%d/%d %s %s %s" % (i, len(folders), key, row["verdict"], row["reason"]), flush=True)
        if a.diff and row.get("_diff") and row["verdict"] == "NOT_OK":
            for lab, (only_page, only_rich) in row["_diff"].items():
                for x in only_page:
                    print("    %s page-only: %s" % (lab, x[:200]))
                for x in only_rich:
                    print("    %s rich-only: %s" % (lab, x[:200]))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\t".join(HEADER) + "\n")
        for r in rows:
            fh.write("\t".join(str(r.get(h, "")) for h in HEADER) + "\n")
    n = {v: sum(1 for r in rows if r["verdict"] == v) for v in ("OK", "NOT_OK", "CAPTURE_FAILED")}
    print(("served" if a.served else "local rebuild") + " over %d of %d folders: OK %d, NOT_OK %d, CAPTURE_FAILED %d" % (
        len(rows), len(folders), n["OK"], n["NOT_OK"], n["CAPTURE_FAILED"]))
    compared = [r for r in rows if r["verdict"] in ("OK", "NOT_OK")]
    cas = [sum(int(r["cas_" + c]) for r in compared) for c in ("page", "rich", "same", "missing", "extra")]
    print("cases over %d of %d compared names: page=%d rich=%d same=%d missing=%d extra=%d" % (
        len(compared), len(compared), cas[0], cas[1], cas[2], cas[3], cas[4]))
    if unidentified:
        print("unidentified folders (%d of %d): %s" % (len(unidentified), len(folders), "; ".join(unidentified)))
    equal, identified = n["OK"], len(rows)
    print("FWD-30 GRADE: equal %d of %d identified names; unidentified %d of %d folders; keyed on: data-attributes" % (
        equal, identified, len(unidentified), len(folders)))
    ok = identified > 0 and equal == identified
    if a.require_cases:
        ok = ok and len(compared) == identified and cas[0] > 0 and cas[3] == 0 and cas[4] == 0
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
