"""CENSUS_A1 -- POSN_AGGFIX.TO-A1-1, cell AF1-s-2 (C-NEVER-WIDEN, C-FIVE-BOOKS-UNCHANGED). READ-ONLY.

  --writers           every writer of json/positioning/positioning_data.json and of current_holdings.AGG
  --book-aum-readers  every reader of a model book's aum (current_holdings.<code>.aum) and of the shared file
  --agg-readers       every reader of current_holdings.AGG (or of every book, AGG included)

INSTRUMENT (differs from the L5 comp-find read): `git grep -n -I` over the tracked workspace files at the
worktree's HEAD, and `git -C <main tree>/portal grep -n -I <pattern> edf85ce503 -- src` for the portal (not
checked out in this cone; read from the main tree's portal repo objects; the main tree is DERIVED from
`git worktree list`, never typed). Each hit is classified by reading its line (and, for a key constant,
the call site it feeds; for an aum line, the top-level scope that holds it). Denominators = files in the
searched tree. Author 0.9.0_WK_POSN_AGGFIX~1.

CLASSES: WRITER, READER, FIXTURE, DELIVERABLE, TYPE-DECLARATION (the order's five), plus
COMMENT (docstring, comment, log/echo/help text), LABEL (a provenance label string), DOC (README/prose/
catalogue outside org/), CONFIG (a registry, manifest or IAM grant naming the key), OTHER-OBJECT (a
different object: another key, a local file, another endpoint, another artifact's aum), KEY-CONSTANT (a
string constant whose use sites are resolved and classified separately), IMPORT (an accessor or type
imported), BOOK-ACCESS (a line that touches current_holdings; graded in the aum / AGG tables),
IN-MEMORY-CONSTRUCT (a client builds an object of the shape from another artifact; the served key is not
written or read), PRODUCER-INTERNAL (the producer computing what it writes), ETF-AUM (the per-holding ETF
aum, a different field), BOOK-AUM-READ, NOT-A-WRITE, PRESENCE-CHECK, KEYED-BOOK-READ (a book read by a
variable key whose domain is stated), AGG-READER, PASS-THROUGH (a whole-object relay that parses no book).
"""
import argparse
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PORTAL_REV = "edf85ce503"
SHARED_KEY = "json/positioning/positioning_data.json"
POSITIONING_DIR = "src/pages/Positioning/"
PRODUCER = "infra/aws/lambda/v2_portal/yang_pipeline/positioning/yang-generate-positioning/lambda_function.py"
SATELLITES = "data/assets/scripts/gold/build_satellites_characteristics.py"
PROXY_LAMBDA = "infra/aws/lambda/portal_data_proxy/lambda_function.py"
LINK_CLASSES = {"READER", "KEY-CONSTANT", "BOOK-ACCESS", "TYPE-DECLARATION", "IMPORT", "WRITER"}
LINK_TOKENS = ("current_holdings", "positioning_data", "getPositioningData", "PositioningDataResponse",
               "CurrentPortfolioHoldings", "CurrentHolding", "positioningData")
OTHER_AUM_TOKENS = ("/aum/", "aum-metrics", "aum-timeseries", "aum-flows", "aum_metrics", "AUMSummary",
                    "AUMMetrics", "AUMTimeSeries")


def run(cmd, ok=(0,)):
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode not in ok:
        raise SystemExit(f"ERROR: {' '.join(cmd)} rc={r.returncode}: {r.stderr.decode('utf-8', 'replace')[:400]}")
    return r.stdout.decode("utf-8", "replace")


WS = run(["git", "-C", HERE, "rev-parse", "--show-toplevel"]).strip()
WS_REV = run(["git", "-C", WS, "rev-parse", "--short=10", "HEAD"]).strip()


def main_tree():
    for ln in run(["git", "-C", WS, "worktree", "list", "--porcelain"]).splitlines():
        if ln.startswith("worktree "):
            return ln[len("worktree "):]
    raise SystemExit("ERROR: no main worktree listed")


class Repo:
    def __init__(self, label, path, rev, scope):
        self.label, self.path, self.rev, self.scope = label, path, rev, scope
        self._blobs = {}
        self._masks = {}

    def files(self):
        return [ln for ln in run(["git", "-C", self.path, "ls-tree", "-r", "--name-only", self.rev, "--", *self.scope]).splitlines() if ln]

    def grep(self, patterns, word=False, paths=None, fixed=True):
        cmd = ["git", "-C", self.path, "grep", "-n", "-I"]
        if fixed:
            cmd.append("-F")
        if word:
            cmd.append("-w")
        for p in patterns:
            cmd += ["-e", p]
        cmd.append(self.rev)
        cmd += ["--"] + (paths if paths is not None else self.scope)
        out = run(cmd, ok=(0, 1))
        hits = []
        for ln in out.splitlines():
            rest = ln[len(self.rev) + 1:]
            path, lno, text = rest.split(":", 2)
            hits.append((path, int(lno), text))
        return hits

    def lines(self, path):
        if path not in self._blobs:
            self._blobs[path] = run(["git", "-C", self.path, "show", f"{self.rev}:{path}"]).splitlines()
        return self._blobs[path]

    def mask(self, path):
        if path not in self._masks:
            self._masks[path] = comment_mask(self.lines(path), path)
        return self._masks[path]


# ---------------------------------------------------------------- classification helpers
DELIV_PREFIXES = ("org/", "docs/", "workflows/", "rcg/", "memory/", ".claude/")
DOC_EXT = (".md", ".txt", ".jsonl", ".ipynb", ".xml", ".csv", ".html", ".pdf")


def path_class(repo, path):
    low = path.lower()
    if repo.label == "ws" and path.startswith(DELIV_PREFIXES):
        return "DELIVERABLE"
    if "/tests/" in "/" + low or "__tests__" in low or ".test." in low or "fixture" in low or "/compproof/" in low:
        return "FIXTURE"
    if low.endswith(DOC_EXT) or "/refs/" in low or "_archive" in low:
        return "DOC"
    return None


def comment_mask(lines, path):
    mask = [False] * len(lines)
    ext = os.path.splitext(path)[1]
    if ext == ".py":
        in_doc = False
        for i, ln in enumerate(lines):
            s = ln.strip()
            n = ln.count('"""') + ln.count("'''")
            if in_doc:
                mask[i] = True
                if n % 2 == 1:
                    in_doc = False
            elif s.startswith("#"):
                mask[i] = True
            elif n % 2 == 1:
                mask[i] = True
                in_doc = True
            elif n >= 2 and s.startswith(('"""', "'''")):
                mask[i] = True
    elif ext in (".ts", ".tsx", ".js", ".mjs", ".cjs"):
        in_c = False
        for i, ln in enumerate(lines):
            s = ln.strip()
            if in_c:
                mask[i] = True
                if "*/" in s:
                    in_c = False
            elif s.startswith("//"):
                mask[i] = True
            elif s.startswith("/*"):
                mask[i] = True
                if "*/" not in s[2:]:
                    in_c = True
    elif ext in (".sh", ".tf", ".yaml", ".yml", ".ps1"):
        for i, ln in enumerate(lines):
            if ln.strip().startswith("#"):
                mask[i] = True
    return mask


def code_part(text, path):
    ext = os.path.splitext(path)[1]
    if ext in (".ts", ".tsx", ".js", ".mjs", ".cjs") and "//" in text:
        return text.split("//", 1)[0]
    if ext in (".py", ".sh", ".tf", ".yaml", ".yml") and " #" in text:
        return text.split(" #", 1)[0]
    return text


def enclosing_interface(lines, idx):
    for j in range(idx, max(-1, idx - 80), -1):
        m = re.search(r"(interface|type)\s+([A-Za-z0-9_]+)", lines[j])
        if m:
            return m.group(2)
    return None


PY_SCOPE = re.compile(r"^(?:async\s+def|def|class)\s+([A-Za-z0-9_]+)")
TS_SCOPE = re.compile(r"^(?:export\s+)?(?:default\s+)?(?:async\s+)?(?:function|interface|type|const|let|class|enum)\s+([A-Za-z0-9_]+)")


def top_scope(lines, idx, path):
    """(name, start, end) of the top-level declaration holding line idx; (None, 0, len) when none."""
    ext = os.path.splitext(path)[1]
    pat = PY_SCOPE if ext == ".py" else (TS_SCOPE if ext in (".ts", ".tsx", ".js", ".mjs", ".cjs") else None)
    if pat is None:
        return None, 0, len(lines)
    start = name = None
    for j in range(idx, -1, -1):
        m = pat.match(lines[j])
        if m:
            start, name = j, m.group(1)
            break
    if start is None:
        return None, 0, len(lines)
    end = len(lines)
    for j in range(idx + 1, len(lines)):
        if pat.match(lines[j]):
            end = j
            break
    return name, start, end


def scope_linked(lines, start, end):
    return any(t in ln for ln in lines[start:end] for t in LINK_TOKENS)


def def_name(lines, idx):
    for j in range(idx, -1, -1):
        m = re.match(r"\s*(?:async\s+)?def\s+([A-Za-z0-9_]+)", lines[j])
        if m:
            return m.group(1)
    return None


CALL_WRITE = re.compile(r"(put_object|upload_file|upload_fileobj|copy_object)\s*\(")
CALL_READ = re.compile(r"(get_object|head_object|download_file|download_fileobj|select_object_content)\s*\(")


def resolve_call(lines, idx):
    for j in range(idx, max(-1, idx - 8), -1):
        m = CALL_WRITE.search(lines[j])
        if m:
            return "WRITER", j + 1, m.group(1)
        m = CALL_READ.search(lines[j])
        if m:
            return "READER", j + 1, m.group(1)
    return None


OTHER_OBJECT_TOKENS = ("platinum/etfs/positioning_data", "api/general/etfs/positioning_data", "api/shared/positioning",
                       "SERVE_LEAF", '"public"', "portal/public/data")


class Table:
    def __init__(self, title):
        self.title, self.rows = title, []

    def add(self, repo, path, lno, cls, text, note=""):
        self.rows.append((cls, repo.label, path, lno, text.strip(), note))

    def dump(self):
        print(f"-- {self.title}: {len(self.rows)} hit line(s) --")
        for cls, lab, path, lno, text, note in sorted(self.rows, key=lambda r: (r[0], r[1], r[2], r[3])):
            t = text if len(text) <= 150 else text[:150] + " ..."
            print(f"  {cls:<19} {lab}:{path}:{lno}: {t}" + (f"   [{note}]" if note else ""))
        c = Counter(r[0] for r in self.rows)
        print("  class counts: " + ", ".join(f"{k}={v}" for k, v in sorted(c.items())))
        print(f"  UNCLASSIFIED {c.get('UNCLASSIFIED', 0)}")
        return c


# ---------------------------------------------------------------- shared-key hits
def classify_key_hit(repo, path, lno, text, sites):
    """sites: dict (label,path,line) -> (cls, call, how) for resolved WRITER/READER call sites."""
    pc = path_class(repo, path)
    if pc:
        return pc, ""
    lines = repo.lines(path)
    idx = lno - 1
    if repo.mask(path)[idx]:
        return "COMMENT", ""
    code = code_part(text, path)
    if any(t in code for t in OTHER_OBJECT_TOKENS):
        return "OTHER-OBJECT", "a different object"
    ext = os.path.splitext(path)[1]
    if "positioning/positioning_data" not in code and "positioning_data.json" not in code:
        return "COMMENT", "match only in trailing comment"
    if ext in (".yaml", ".yml", ".json"):
        return "CONFIG", "registry/manifest names the key"
    if ext == ".tf":
        return "CONFIG", "IAM grant or description names the key"
    if re.search(r"(^|\s)(print|logger\.\w+|echo)\s*[(\"]|description\s*=|help\s*=", code):
        return "COMMENT", "log/echo/help text naming the file"
    if re.search(r"Path\(|open\(|output_dir|os\.path\.join", code):
        return "OTHER-OBJECT", "a local file path, not the S3 key"
    m = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*['\"][^'\"]*positioning/positioning_data[.]json['\"]\s*$", code)
    if m and m.group(1) not in ("Key", "Bucket"):
        name = m.group(1)
        use = re.compile(r"Key\s*=\s*" + re.escape(name) + r"(?![A-Za-z0-9_])")
        found = []
        for j, ln in enumerate(lines):
            if use.search(ln):
                r = resolve_call(lines, j)
                if r:
                    sites[(repo.label, path, r[1])] = (r[0], r[2], f"Key={name} at :{j + 1}, constant at :{lno}")
                    found.append(f"{r[0]} {r[2]} :{r[1]}")
        return "KEY-CONSTANT", f"{name}; use sites: {', '.join(found) if found else 'none resolved'}"
    if "Key=" in code.replace(" ", ""):
        r = resolve_call(lines, idx)
        if r:
            sites[(repo.label, path, r[1])] = (r[0], r[2], f"literal Key at :{lno}")
            return r[0], f"{r[2]} :{r[1]}"
    if "apiRequest" in code and "/api/general/positioning/positioning_data.json" in code:
        return "READER", "HTTP GET through the portal api client"
    if ext == ".sh" and code.strip().strip('"') == SHARED_KEY:
        return "READER", "validate script array element: an existence/age check on the key (metadata read)"
    if re.search(r"(aws\s+s3\s+(cp|sync|mv)).*s3://[^ ]*json/positioning", code):
        return "WRITER", "aws s3 write command"
    return "UNCLASSIFIED", ""


def key_census(repos, table, sites, patterns):
    for repo in repos:
        for path, lno, text in repo.grep(patterns):
            cls, note = classify_key_hit(repo, path, lno, text, sites)
            table.add(repo, path, lno, cls, text, note)


# ---------------------------------------------------------------- modes
def mode_writers(ws, portal):
    print("== WRITERS ==")
    sites = {}
    t = Table("(a1) shared key: patterns 'positioning/positioning_data' and 'positioning_data.json' (fixed strings)")
    key_census([ws, portal], t, sites, ["positioning/positioning_data", "positioning_data.json"])
    t.dump()
    print()
    t2 = Table("(a2) prefix writers: pattern 'json/positioning' (fixed), lines not already in (a1)")
    seen = {(r[1], r[2], r[3]) for r in t.rows}
    for repo in (ws, portal):
        for path, lno, text in repo.grep(["json/positioning"]):
            if (repo.label, path, lno) in seen:
                continue
            pc = path_class(repo, path)
            if pc:
                t2.add(repo, path, lno, pc, text)
                continue
            if repo.mask(path)[lno - 1]:
                t2.add(repo, path, lno, "COMMENT", text)
                continue
            code = code_part(text, path)
            if re.search(r"aws\s+s3\s+(cp|sync|mv)", code) or CALL_WRITE.search(code):
                t2.add(repo, path, lno, "UNCLASSIFIED", text, "write-shaped line on the prefix: read it")
            else:
                t2.add(repo, path, lno, "OTHER-OBJECT", text, "another key under json/positioning/")
    t2.dump()
    print()
    w_sites = sorted((k, v) for k, v in sites.items() if v[0] == "WRITER")
    r_sites = sorted((k, v) for k, v in sites.items() if v[0] == "READER")
    print("WRITE SITES for s3://opal-data-portal-v2/" + SHARED_KEY + " (call sites resolved from the classified lines):")
    for (lab, path, ln), (cls, call, how) in w_sites:
        repo = ws if lab == "ws" else portal
        print(f"  WRITER {lab}:{path}:{ln} {call}  ({how}) inside def {def_name(repo.lines(path), ln - 1)}()")
    print(f"WRITERS {len(w_sites)}")
    print(f"(read sites resolved on the same key: {len(r_sites)} -- listed under --book-aum-readers)")
    pos = [ln for (_, p, ln), v in w_sites if p == PRODUCER and "OUTPUT_KEY" in v[2]]
    print("POSITIVE CONTROL the producer's lambda_handler put_object with Key=OUTPUT_KEY: "
          + (f"FOUND at {PRODUCER}:{pos[0]} (the order cites :2627-2634, OUTPUT_KEY :2529)" if pos else "NOT FOUND"))

    print()
    t3 = Table("(b) current_holdings.AGG writes: patterns 'current_holdings' and AGG-literal keys in code files carrying current_holdings")
    agg_w = []
    for repo in (ws, portal):
        ch_files = sorted({p for p, _, _ in repo.grep(["current_holdings"])})
        code_files = [p for p in ch_files if not path_class(repo, p)]
        hits = repo.grep(["current_holdings", "'AGG'", '"AGG"'], paths=code_files) if code_files else []
        for path, lno, text in hits:
            code = code_part(text, path)
            if repo.mask(path)[lno - 1]:
                t3.add(repo, path, lno, "COMMENT", text)
            elif re.search(r"current_holdings\s*\[\s*['\"]AGG['\"]\s*\]\s*=(?!=)", code):
                t3.add(repo, path, lno, "WRITER", text, "literal AGG book assignment")
                agg_w.append((repo.label, path, lno))
            elif re.search(r"current_holdings\s*\[\s*[A-Za-z_][A-Za-z0-9_]*\s*\]\s*=(?!=)", code):
                cls = "IN-MEMORY-CONSTRUCT" if repo.label == "portal" else "WRITER"
                t3.add(repo, path, lno, cls, text, "book assignment by variable key (per-model books, not AGG)")
            elif repo.label == "portal" and re.search(r"(etfAdapter|satelliteAdapter)[.]ts$", path):
                t3.add(repo, path, lno, "IN-MEMORY-CONSTRUCT", text, "client-side adapter object, never the served key")
            else:
                t3.add(repo, path, lno, "NOT-A-WRITE", text, "no assignment to a book on this line")
    t3.dump()
    print("AGG WRITE SITES: " + ", ".join(f"{a}:{b}:{c}" for a, b, c in agg_w))
    print(f"AGG WRITERS {len(agg_w)}")
    return 0


def link_census(ws, portal, title):
    """Every hit that ties a file to the shared file: its key, its accessor, its types, its books."""
    pats = ["positioning_data.json", "getPositioningData", "PositioningDataResponse", "CurrentPortfolioHoldings", "current_holdings"]
    t = Table(title)
    sites = {}
    link_files = defaultdict(set)
    for repo in (ws, portal):
        for path, lno, text in repo.grep(pats):
            pc = path_class(repo, path)
            if pc:
                t.add(repo, path, lno, pc, text)
                continue
            code = code_part(text, path)
            if repo.mask(path)[lno - 1]:
                t.add(repo, path, lno, "COMMENT", text)
                continue
            if "positioning_data.json" in code:
                cls, note = classify_key_hit(repo, path, lno, text, sites)
            elif re.search(r"['\"]positioning_data[.]current_holdings['\"]", code):
                cls, note = "LABEL", "a provenance label string written into another artifact"
            elif re.search(r"^\s*import\b", code) or re.search(r"^\s*(getPositioningData|type\s+PositioningDataResponse),?\s*$", code):
                cls, note = "IMPORT", ""
            elif re.search(r"export\s+(async\s+)?function\s+getPositioningData", code):
                cls, note = "READER", "the accessor: canonicalises every book's code keys and returns the whole response"
            elif re.search(r"(interface|type)\s+(PositioningDataResponse|CurrentPortfolioHoldings)", code) or re.search(r"current_holdings\?\s*:", code):
                cls, note = "TYPE-DECLARATION", ""
            elif "queryFn: getPositioningData" in code or re.search(r"getPositioningData\(\)", code):
                cls, note = "READER", "fetches the shared file"
            elif "PositioningDataResponse" in code or "CurrentPortfolioHoldings" in code:
                cls, note = "TYPE-DECLARATION", "type annotation"
            else:
                cls, note = "BOOK-ACCESS", "touches current_holdings: graded in the aum / AGG tables"
            if cls in LINK_CLASSES:
                link_files[repo.label].add(path)
            t.add(repo, path, lno, cls, text, note)
    for (lab, path, _), _v in sites.items():
        link_files[lab].add(path)
    return t, sites, link_files


def classify_aum_line(repo, path, lno, text):
    lines = repo.lines(path)
    idx = lno - 1
    code = code_part(text, path)
    if repo.mask(path)[idx]:
        return "COMMENT", ""
    if any(tok in code for tok in OTHER_AUM_TOKENS):
        return "OTHER-OBJECT", "another aum artifact or endpoint named on the line"
    if re.search(r"^\s*(total_)?aum\??\s*:\s*number", code):
        iface = enclosing_interface(lines, idx)
        if iface == "CurrentPortfolioHoldings":
            return "TYPE-DECLARATION", f"BOOK-level field of {iface}" + (" (the AGG book's total)" if "total_aum" in code else " (a model book's aum)")
        if iface and "Holding" in iface and not iface.startswith("Etf"):
            return "ETF-AUM", f"type field of {iface} (a holding row)"
        return "OTHER-OBJECT", f"type field of {iface} (another artifact's type)"
    if path == PRODUCER:
        if re.search(r"['\"]aum['\"]\s*:\s*aum_data", code):
            return "WRITER", "writes a model book's aum"
        if re.search(r"['\"]total_aum['\"]\s*:", code):
            return "WRITER", "writes the AGG book's total_aum"
        if re.search(r"holding\[['\"]aum['\"]\]", code):
            return "ETF-AUM", "producer writes a holding's ETF aum"
        return "PRODUCER-INTERNAL", "the producer computing what it writes"
    if path == SATELLITES:
        return "ETF-AUM", "per-ticker row field (yang_index / bbg), never a book's aum"
    if repo.label == "portal" and re.search(r"(etfAdapter|satelliteAdapter)[.]ts$", path):
        return "IN-MEMORY-CONSTRUCT", "adapter copies another artifact's aum into the response shape"
    name, start, end = top_scope(lines, idx, path)
    if name is not None and not scope_linked(lines, start, end):
        return "OTHER-OBJECT", f"aum of another artifact (top-level scope {name} never touches the shared file)"
    if re.search(r"current_holdings[^;]*[.?]\s*aum\b|current_holdings[^;]*\[['\"]aum['\"]\]|(book|ph|currentHoldings|portfolioHoldings)\??\.(total_)?aum\b", code):
        return "BOOK-AUM-READ", f"scope {name}"
    if re.search(r"\b(h|t|holding|row|etf|r)\??\.aum\b|\[['\"]aum['\"]\]", code):
        return "ETF-AUM", "a holding/row's aum"
    return "UNCLASSIFIED", f"scope {name}"


def mode_book_aum(ws, portal):
    print("== BOOK-AUM READERS ==")
    t, sites, link_files = link_census(ws, portal, "(1) links to the shared file: key, accessor, types, current_holdings")
    t.dump()
    print()
    print("SHARED-FILE READ SITES (resolved S3 calls + reader lines, one per call site; a reader line within 8 lines of a resolved call is that call):")
    rs = {}
    for (lab, path, ln), (cls, call, how) in sites.items():
        if cls == "READER":
            rs[(lab, path, ln)] = f"{call} ({how})"
    for cls, lab, path, lno, text, note in sorted(t.rows, key=lambda r: (r[1], r[2], r[3])):
        if cls != "READER":
            continue
        if any(k[0] == lab and k[1] == path and abs(k[2] - lno) <= 8 for k in rs):
            continue
        rs[(lab, path, lno)] = note
    outside = {k: v for k, v in rs.items() if not (k[0] == "portal" and k[1].startswith(POSITIONING_DIR))}
    for (lab, path, ln), how in sorted(rs.items()):
        where = "inside Positioning" if (lab, path, ln) not in outside else "outside Positioning"
        print(f"  READER {lab}:{path}:{ln} [{where}] {how}")
    print(f"SHARED-FILE READERS outside portal/src/pages/Positioning {len(outside)} site(s) in "
          f"{len({(k[0], k[1]) for k in outside})} file(s); inside it {len(rs) - len(outside)}")

    print()
    t2 = Table("(2) 'aum' / 'total_aum' (word) in every code file linked to the shared file")
    book_sites = []
    for repo in (ws, portal):
        paths = sorted(link_files[repo.label])
        if not paths:
            continue
        for path, lno, text in repo.grep(["aum", "total_aum"], word=True, paths=paths):
            cls, note = classify_aum_line(repo, path, lno, text)
            t2.add(repo, path, lno, cls, text, note)
            if cls == "BOOK-AUM-READ":
                book_sites.append((repo.label, path, lno))
    t2.dump()
    for s in book_sites:
        print(f"  BOOK-AUM READ SITE {s[0]}:{s[1]}:{s[2]}")
    out_b = [s for s in book_sites if not (s[0] == "portal" and s[1].startswith(POSITIONING_DIR))]
    print(f"linked code files scanned: ws {len(link_files['ws'])}, portal {len(link_files['portal'])}")
    print(f"BOOK-AUM READERS {len(book_sites)} (outside portal/src/pages/Positioning: {len(out_b)}); "
          f"ETF-AUM lines excluded from n: {sum(1 for r in t2.rows if r[0] == 'ETF-AUM')}")

    print()
    print("(3) files carrying the word aum that are NOT linked to the shared file (excluded from (2), listed so the excluded set is visible):")
    allf = Counter(p for p, _, _ in portal.grep(["aum", "total_aum"], word=True))
    rest = {p: n for p, n in allf.items() if p not in link_files["portal"]}
    for p, n in sorted(rest.items()):
        print(f"  portal:{p} {n}")
    print(f"  portal: {len(rest)} unlinked file(s) with an aum word; {len(allf)} file(s) with an aum word in total")
    ws_n = len({p for p, _, _ in ws.grep(["aum"], word=True)})
    print(f"  ws: {ws_n} file(s) carry the word aum; {len(link_files['ws'])} of them are linked code files, scanned in (2)")
    return 0


def mode_agg(ws, portal):
    print("== AGG READERS ==")
    t, sites, link_files = link_census(ws, portal, "(1) links to the shared file (the same census as --book-aum-readers)")
    c = Counter(r[0] for r in t.rows)
    print(f"-- (1) {len(t.rows)} link hit line(s); class counts: " + ", ".join(f"{k}={v}" for k, v in sorted(c.items())))
    print(f"   linked code files: ws {len(link_files['ws'])} -> {sorted(link_files['ws'])}")
    print(f"   linked code files: portal {len(link_files['portal'])} -> {sorted(link_files['portal'])}")
    print()
    t2 = Table("(2) every current_holdings / total_aum / AGG (word) line in the linked code files")
    agg_sites = []
    for repo in (ws, portal):
        paths = sorted(link_files[repo.label])
        if not paths:
            continue
        hits = repo.grep(["current_holdings", "total_aum"], paths=paths) + repo.grep(["AGG"], word=True, paths=paths)
        seen = set()
        for path, lno, text in sorted(hits):
            if (path, lno) in seen:
                continue
            seen.add((path, lno))
            lines = repo.lines(path)
            code = code_part(text, path)
            idx = lno - 1
            if repo.mask(path)[idx]:
                t2.add(repo, path, lno, "COMMENT", text)
                continue
            if "current_holdings" not in code and "total_aum" not in code and not re.search(r"\bAGG\b", code):
                t2.add(repo, path, lno, "COMMENT", text, "match only in trailing comment")
                continue
            if re.search(r"['\"]positioning_data[.]current_holdings['\"]", code):
                t2.add(repo, path, lno, "LABEL", text, "a provenance label string written into another artifact")
                continue
            if path == PRODUCER:
                if re.search(r"current_holdings\s*\[\s*['\"]AGG['\"]\s*\]\s*=", code) or re.search(r"['\"]total_aum['\"]\s*:", code):
                    t2.add(repo, path, lno, "WRITER", text, "the producer writes the AGG book")
                elif "current_holdings" in code or "total_aum" in code:
                    t2.add(repo, path, lno, "PRODUCER-INTERNAL", text)
                else:
                    t2.add(repo, path, lno, "OTHER-OBJECT", text, "AGG the ETF ticker / benchmark / log text, not the AGG book")
                continue
            if path == SATELLITES and re.search(r"books\s*=\s*positioning\.get\(['\"]current_holdings['\"]\)", code):
                t2.add(repo, path, lno, "AGG-READER", text, "yang_index walks every book, AGG included (:413-415 for book_name in books)")
                agg_sites.append((repo.label, path, lno))
                continue
            if re.search(r"Object\.(entries|keys|values)\([^)]*current_holdings|for\s+\w+\s+in\s+[^:]*current_holdings|current_holdings[^;]*\.(items|values|keys)\(", code):
                t2.add(repo, path, lno, "AGG-READER", text, "iterates every book, AGG included")
                agg_sites.append((repo.label, path, lno))
                continue
            if re.search(r"current_holdings\s*\??\.?\s*\[\s*['\"]AGG['\"]\s*\]|current_holdings\??\.AGG\b", code):
                t2.add(repo, path, lno, "AGG-READER", text, "literal AGG book read")
                agg_sites.append((repo.label, path, lno))
                continue
            if re.search(r"total_aum\??\s*:\s*number", code):
                iface = enclosing_interface(lines, idx)
                if iface == "CurrentPortfolioHoldings":
                    t2.add(repo, path, lno, "TYPE-DECLARATION", text, "the AGG book's total_aum field")
                else:
                    t2.add(repo, path, lno, "OTHER-OBJECT", text, f"type field of {iface} (another artifact's type)")
                continue
            if re.search(r"current_holdings\?\s*:", code):
                t2.add(repo, path, lno, "TYPE-DECLARATION", text)
                continue
            if "total_aum" in code and "current_holdings" not in code:
                name, start, end = top_scope(lines, idx, path)
                if name is not None and not scope_linked(lines, start, end):
                    t2.add(repo, path, lno, "OTHER-OBJECT", text, f"total_aum of another artifact (top-level scope {name})")
                    continue
            if repo.label == "portal" and path.endswith("tabs/HoldingsTab.tsx") and "current_holdings" in code:
                if "buildCustomCurrentHoldings" in code:
                    note = "CSM blend: buildCustomCurrentHoldings reads currentHoldings[id] for id in MODEL_IDS only (:84-105)"
                else:
                    note = "keyed by selectedPortfolio (MODEL_BOOKS UST/ST/INT/LT/ULT or CSM); file docstring :46-48 'Nothing in this file reads it'"
                t2.add(repo, path, lno, "KEYED-BOOK-READ", text, note)
                continue
            if repo.label == "portal" and path.endswith("panels/PositioningSummary.tsx"):
                if "Boolean(" in code:
                    t2.add(repo, path, lno, "PRESENCE-CHECK", text)
                elif re.search(r"current_holdings\?\.\[code\]", code):
                    t2.add(repo, path, lno, "KEYED-BOOK-READ", text, "only when SUBCATEGORY_SOURCE[bookMode]=='current_holdings' (etfs/satellites; bookSet.ts:137-141), book codes of that mode")
                else:
                    t2.add(repo, path, lno, "PRESENCE-CHECK", text, "source-selector comparison")
                continue
            if repo.label == "portal" and re.search(r"(etfAdapter|satelliteAdapter)[.]ts$", path):
                t2.add(repo, path, lno, "IN-MEMORY-CONSTRUCT", text, "adapter builds a response of the shape from another artifact")
                continue
            if repo.label == "portal" and path == "src/api/portal-proxy.ts":
                if re.search(r"^\s*current_holdings\s*:\s*resp\.current_holdings", code) or re.search(r":\s*resp\.current_holdings,?\s*$", code):
                    t2.add(repo, path, lno, "PRESENCE-CHECK", text, "accessor: block present? then canonicalise, else pass it through")
                elif "FactorTiltPortfolioId" in code:
                    t2.add(repo, path, lno, "OTHER-OBJECT", text, "factor-tilts artifact portfolio id, not the positioning book")
                else:
                    t2.add(repo, path, lno, "UNCLASSIFIED", text)
                continue
            if "SUBCATEGORY_SOURCE" in code or re.search(r"['\"]current_holdings['\"]", code):
                t2.add(repo, path, lno, "PRESENCE-CHECK", text, "a source-selector string, not a book read")
                continue
            if re.search(r"\bAGG\b", code) and "current_holdings" not in code:
                t2.add(repo, path, lno, "OTHER-OBJECT", text, "AGG as an ETF ticker / other id")
                continue
            t2.add(repo, path, lno, "UNCLASSIFIED", text)
    t2.dump()
    print()
    print("PASS-THROUGH relays of the whole shared file (parse no book; AGG passes through unmodified):")
    pt = 0
    for (lab, path, ln), (cls, call, how) in sorted(sites.items()):
        if cls == "READER" and call == "get_object" and path == PROXY_LAMBDA:
            print(f"  PASS-THROUGH {lab}:{path}:{ln} {call} ({how}) inside def {def_name(ws.lines(path), ln - 1)}()")
            pt += 1
    print(f"PASS-THROUGH {pt}")
    for s in agg_sites:
        print(f"  AGG READ SITE {s[0]}:{s[1]}:{s[2]}")
    print(f"AGG READERS {len(agg_sites)}")
    pos = any(p == SATELLITES for _, p, _ in agg_sites)
    print(f"POSITIVE CONTROL {SATELLITES} yang_index: {'PRESENT' if pos else 'ABSENT'}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--writers", action="store_true")
    g.add_argument("--book-aum-readers", action="store_true")
    g.add_argument("--agg-readers", action="store_true")
    ap.add_argument("--portal-repo", default=None, help="default: <main worktree>/portal, derived")
    args = ap.parse_args()
    portal_path = args.portal_repo or os.path.join(main_tree(), "portal")
    ws = Repo("ws", WS, WS_REV, [])
    portal = Repo("portal", portal_path, PORTAL_REV, ["src"])
    ws_n = len(ws.files())
    p_files = portal.files()
    p_pos = len([f for f in p_files if f.startswith(POSITIONING_DIR)])
    full = run(["git", "-C", portal_path, "rev-parse", PORTAL_REV]).strip()
    print("INSTRUMENT git grep -n -I (fixed strings unless stated)")
    print(f"DENOMINATOR workspace: {ws_n} tracked files at {WS_REV} ({WS})")
    print(f"DENOMINATOR portal:    {len(p_files)} files under src at {full[:10]} ({portal_path}); {p_pos} of them under {POSITIONING_DIR}")
    print()
    if args.writers:
        return mode_writers(ws, portal)
    if args.book_aum_readers:
        return mode_book_aum(ws, portal)
    return mode_agg(ws, portal)


if __name__ == "__main__":
    sys.exit(main())
