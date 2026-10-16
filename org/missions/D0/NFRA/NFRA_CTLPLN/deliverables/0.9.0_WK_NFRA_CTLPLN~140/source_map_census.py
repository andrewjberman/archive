#!/usr/bin/env python3
"""source_map_census.py -- read-only census of every file that names the Lambda source map.

CT-bb-1 (NFRA_CTLPLN, stage 1 of the per-function split). Standard library only, ASCII only,
no network, no write outside this folder. It reads the COMMITTED tree (HEAD) through git, so a
sparse working copy cannot shrink the answer.

Usage:
  python source_map_census.py             write LAMBDA_SOURCE_MAP_CONSUMER_CENSUS.md, print the census line
  python source_map_census.py --selftest  planted temporary files only, print the selftest line
  python source_map_census.py --show CLASS  print the first hit of every file in CLASS (exploration aid)

Classes (what the file DOES with the map):
  READ_WHOLE  loads the whole JSON (jsondecode(file()), json.load(s), jq, fromjson, JSON.parse, readFileSync)
  READ_ONE    looks up one function entry by key
  WRITE       adds, edits or regenerates entries
  TEST        a test file (path)
  DOC         a document, comment, log, record or ledger that only names the file
  OTHER       the patterns could not decide and no reading settled it (makes ok False)

The line patterns are a first pass. The worker's reading table (READINGS_CONSUMERS.tsv, same folder)
overrides the pattern class for every file it lists; a disagreement is counted and printed.
"""
import json
import os
import re
import statistics
import subprocess
import sys
import tempfile

NEEDLE = "lambda-source-map"
MAP_REL = "infra/aws/lambda/ci/lambda-source-map.json"
DEPLOY_REL = "infra/aws/lambda/ci/record-terraform-deploy.sh"
OWNER_PREFIX = "0.7.0_AE_CloudOps"
HERE = os.path.dirname(os.path.abspath(__file__))
CELL = os.path.basename(HERE)
WINDOW = 4
CLASSES = ["READ_WHOLE", "READ_ONE", "WRITE", "TEST", "DOC", "OTHER"]
ORDER = ["WRITE", "READ_WHOLE", "READ_ONE", "UNDECIDED", "DOC"]
READINGS_DEPLOY = os.path.join(HERE, "READINGS_DEPLOY_COMMITS.tsv")
CENSUS_MD = os.path.join(HERE, "LAMBDA_SOURCE_MAP_CONSUMER_CENSUS.md")

READ_WHOLE_RE = [re.compile(p) for p in [
    r"jsondecode\(\s*file\(", r"\bfromjson\b", r"\bjson\.loads?\(", r"\bJSON\.parse\(",
    r"\breadFileSync\(", r"\bjq\b", r"\bread_json\(",
]]
WRITE_RE = [re.compile(p) for p in [
    r"\bjson\.dump\(", r"open\([^)]*['\"][wax]\+?['\"]", r"\bwrite_text\(", r"\bwrite_bytes\(",
    r"\bwriteFileSync\(", r"\bwriteFile\(", r"\bos\.replace\(", r"\bshutil\.(copy2?|move)\(",
    r"\bsed\s+-i\b", r"\btee\b", r">\s*\"?\$\{?[A-Z_]*SOURCE_MAP", r"\bgit\s+(add|commit|mv|rm)\b",
]]
READ_ONE_RE = [re.compile(p) for p in [
    r"\[\s*['\"][A-Za-z0-9_.-]+['\"]\s*\]", r"\.get\(\s*['\"]", r"\blookup\(",
]]
TEST_PATH = re.compile(r"(^|/)(tests?|__tests__)/|(^|/)test_[^/]*$|[^/]*_test\.[A-Za-z]+$|[^/]*\.test\.[A-Za-z]+$")
DOC_EXT = {".md", ".txt", ".log", ".rst", ".jsonl", ".json", ".diff", ".patch", ".out", ".xml",
           ".proposal", ".csv", ".html", ".tsv"}
TF_LAMBDA_RE = re.compile(r'resource\s+"aws_lambda_function"')


def ascii_only(s):
    return s.encode("ascii", "replace").decode("ascii")


def git(args, stdin=None, timeout=200):
    r = subprocess.run(["git"] + args, cwd=REPO, input=stdin, capture_output=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def repo_root():
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True, timeout=60)
    if r.returncode != 0:
        raise SystemExit("ERROR: not inside a git checkout")
    return r.stdout.decode("utf-8", "replace").strip()


REPO = repo_root()


def is_comment(line):
    s = line.lstrip()
    return s.startswith(("#", "//", "--", "/*", "*/", ";", "<!--")) or s == "*"


def hit_class(lines, i):
    """Class of one line that names the map, from the line itself (a comment) or its window (code)."""
    line = lines[i]
    if is_comment(line):
        if any(p.search(line) for p in WRITE_RE):
            return "WRITE"
        if any(p.search(line) for p in READ_WHOLE_RE):
            return "READ_WHOLE"
        if any(p.search(line) for p in READ_ONE_RE):
            return "READ_ONE"
        return "DOC"
    text = "\n".join(lines[max(0, i - WINDOW): i + WINDOW + 1])
    if any(p.search(text) for p in WRITE_RE):
        return "WRITE"
    if any(p.search(text) for p in READ_WHOLE_RE):
        return "READ_WHOLE"
    if any(p.search(text) for p in READ_ONE_RE):
        return "READ_ONE"
    return "UNDECIDED"


def classify_file(path, text):
    """Return (class, basis, first_hit_line_no, first_hit_text) for one committed file."""
    lines = text.splitlines()
    hits = [i for i, ln in enumerate(lines) if NEEDLE in ln]
    ext = os.path.splitext(path)[1].lower()
    first = (0, "") if not hits else (hits[0] + 1, ascii_only(lines[hits[0]].strip())[:160])
    if ext in DOC_EXT:
        return "DOC", "pattern:doc-extension", first[0], first[1]
    if TEST_PATH.search(path):
        return "TEST", "pattern:test-path", first[0], first[1]
    if not hits:
        return "UNDECIDED", "pattern:no-text-line", 0, ""
    best = None
    for i in hits:
        c = hit_class(lines, i)
        if best is None or ORDER.index(c) < ORDER.index(best[0]):
            best = (c, i)
    cls, i = best
    return cls, "pattern", i + 1, ascii_only(lines[i].strip())[:160]


def load_tsv(path, columns):
    rows = {}
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8") as f:
        for n, raw in enumerate(f, 1):
            raw = raw.rstrip("\n")
            if not raw or raw.startswith("#") or raw.startswith("path\t") or raw.startswith("commit\t"):
                continue
            cells = raw.split("\t")
            if len(cells) != len(columns):
                raise SystemExit("ERROR: %s line %d has %d cells, want %d" % (path, n, len(cells), len(columns)))
            row = dict(zip(columns, cells))
            rows[row[columns[0]]] = row
    return rows


CONSUMER_COLUMNS = ["path", "class", "hit_line", "what_it_does", "per_function_effect"]


def load_consumer_readings():
    rows = {}
    for name in sorted(os.listdir(HERE)):
        if name.startswith("READINGS_CONSUMERS") and name.endswith(".tsv"):
            for k, v in load_tsv(os.path.join(HERE, name), CONSUMER_COLUMNS).items():
                if k in rows:
                    raise SystemExit("ERROR: two reading rows for %s" % k)
                rows[k] = v
    return rows


def grep_set():
    rc, out, err = git(["grep", "-l", "-z", "-F", "-e", NEEDLE, "HEAD", "--"])
    if rc not in (0, 1):
        raise SystemExit("ERROR: git grep rc=%d %s" % (rc, err.decode("utf-8", "replace")[:300]))
    names = [x.decode("utf-8", "replace") for x in out.split(b"\0") if x]
    bad = [x for x in names if not x.startswith("HEAD:")]
    if bad:
        raise SystemExit("ERROR: unexpected git grep line %r" % bad[0])
    return sorted(x[len("HEAD:"):] for x in names)


def read_blobs(paths):
    spec = "".join("HEAD:%s\n" % p for p in paths).encode("utf-8")
    rc, out, err = git(["cat-file", "--batch"], stdin=spec)
    if rc != 0:
        raise SystemExit("ERROR: git cat-file rc=%d" % rc)
    blobs, pos = {}, 0
    for p in paths:
        nl = out.index(b"\n", pos)
        head = out[pos:nl].decode("utf-8", "replace").split()
        pos = nl + 1
        if len(head) == 3 and head[1] == "blob":
            size = int(head[2])
            blobs[p] = out[pos:pos + size]
            pos += size + 1
        else:
            blobs[p] = None
    return blobs


def top_folder(path):
    return path.split("/", 1)[0] if "/" in path else "(root file)"


def map_shape(blob):
    d = json.loads(blob.decode("utf-8"))
    tops = list(d.keys())
    funcs = d.get("functions", {})
    keyset = set()
    for v in funcs.values():
        keyset |= set(v.keys()) if isinstance(v, dict) else {"<non-object>"}
    sizes = [len(json.dumps(v, indent=2, ensure_ascii=True)) for v in funcs.values()]
    first_name = next(iter(funcs))
    return {
        "bytes": len(blob), "tops": tops, "meta_keys": [k for k in tops if k != "functions"],
        "functions": len(funcs), "keyset": sorted(keyset), "keysets_distinct": len(set(
            tuple(sorted(v.keys())) for v in funcs.values() if isinstance(v, dict))),
        "min": min(sizes), "median": statistics.median(sizes), "max": max(sizes),
        "example_name": first_name,
        "example": json.dumps({first_name: funcs[first_name]}, indent=2, ensure_ascii=True),
    }


def deploy_history():
    rc, out, err = git(["log", "--follow", "--format=%H%x1f%an%x1f%cn%x1f%s", "HEAD", "--", DEPLOY_REL])
    if rc != 0:
        raise SystemExit("ERROR: git log rc=%d" % rc)
    rows = []
    for ln in out.decode("utf-8", "replace").splitlines():
        if ln.strip():
            h, an, cn, subj = ln.split("\x1f", 3)
            rows.append({"hash": h, "author": an, "committer": cn, "subject": ascii_only(subj)})
    return rows


def md_cell(s):
    return ascii_only(str(s)).replace("|", "/").replace("\n", " ")


def run_census():
    names = grep_set()
    g = len(names)
    blobs = read_blobs(names)
    readings = load_consumer_readings()
    for p, r in readings.items():
        if r["class"] not in CLASSES:
            raise SystemExit("ERROR: reading for %s has class %r, not one of %s" % (p, r["class"], CLASSES))
    final, disagree, pattern_only_undecided = {}, [], []
    basis_count = {"reading": 0, "pattern": 0}
    per_file = {}
    for p in names:
        blob = blobs[p]
        text = blob.decode("utf-8", "replace") if blob is not None else ""
        pc, basis, ln, hit = classify_file(p, text)
        if p in readings:
            rc_ = readings[p]["class"]
            basis_count["reading"] += 1
            if pc != "UNDECIDED" and pc != rc_:
                disagree.append((p, pc, rc_))
            cls, basis = rc_, "reading"
        else:
            cls = pc if pc != "UNDECIDED" else "OTHER"
            if pc == "UNDECIDED":
                pattern_only_undecided.append(p)
            basis_count["pattern"] += 1
        per_file[p] = (cls, basis, ln, hit)
        final[p] = cls
    stale = sorted(set(readings) - set(names))
    buckets = {c: [p for p in names if final[p] == c] for c in CLASSES}
    n = sum(len(v) for v in buckets.values())
    # independent check: every counted file's committed blob really contains the needle
    contains = sum(1 for p in names if blobs[p] is not None and NEEDLE.encode("ascii") in blobs[p])
    reconciled = (n == g) and (set(final) == set(names)) and (contains == g)
    if contains != g:
        print("NOT-CONTAINED %d of %d grep files have no needle in their blob" % (g - contains, g))
    other = len(buckets["OTHER"])
    ok = reconciled and other == 0
    counts = {c: len(buckets[c]) for c in CLASSES}
    folders = {}
    for p in names:
        folders.setdefault(top_folder(p), {c: 0 for c in CLASSES})[final[p]] += 1
    for f in sorted(folders):
        fc = folders[f]
        print("FOLDER %s files=%d %s" % (f, sum(fc.values()), " ".join("%s=%d" % (c.lower(), fc[c]) for c in CLASSES)))

    # map shape and the two function counts
    mrc, mblob, merr = git(["cat-file", "-p", "HEAD:%s" % MAP_REL])
    if mrc != 0 or not mblob:
        raise SystemExit("ERROR: cannot read the map at HEAD")
    shape = map_shape(mblob)
    tf_names = [p for p in names if p.endswith(".tf")]
    tf_lambda = 0
    for p in tf_names:
        tf_lambda += len(TF_LAMBDA_RE.findall(blobs[p].decode("utf-8", "replace") if blobs[p] else ""))
    # repository-wide Terraform side: every committed .tf file that declares an aws_lambda_function
    rc_tf, out_tf, err_tf = git(["grep", "-c", "-F", "-e", 'resource "aws_lambda_function"', "HEAD", "--", "*.tf"])
    if rc_tf not in (0, 1):
        raise SystemExit("ERROR: git grep -c rc=%d" % rc_tf)
    tf_repo_files, tf_repo_resources = 0, 0
    for ln in out_tf.decode("utf-8", "replace").splitlines():
        if not ln.strip():
            continue
        cnt = int(ln.rsplit(":", 1)[1])
        tf_repo_files += 1
        tf_repo_resources += cnt

    hist = deploy_history()
    dep_read = load_tsv(READINGS_DEPLOY, ["commit", "class", "what_changed", "data_home"])
    owner = [h for h in hist if h["author"].startswith(OWNER_PREFIX)]
    nonowner = [h for h in hist if not h["author"].startswith(OWNER_PREFIX)]
    unread = []
    data_n = code_n = 0
    for h in nonowner:
        key = [k for k in dep_read if h["hash"].startswith(k)]
        if len(key) != 1:
            unread.append(h["hash"][:10])
            continue
        if dep_read[key[0]]["class"] == "DATA":
            data_n += 1
        else:
            code_n += 1

    lines_out = []
    lines_out.append("# LAMBDA_SOURCE_MAP_CONSUMER_CENSUS -- CT-bb-1 (stage 1, read-only)")
    lines_out.append("")
    lines_out.append("Generated by `source_map_census.py` (this folder). Reads the committed tree at HEAD through git; no")
    lines_out.append("working-copy reads, no network, no write outside this folder. Scope: the whole repository.")
    lines_out.append("Map: `%s`. Deploy script: `%s`." % (MAP_REL, DEPLOY_REL))
    lines_out.append("")
    lines_out.append("Method: the line patterns class every file that names the map (window of +/-%d lines around each"
                     " hit; a comment line is classed by its own text; a document extension is DOC). The worker then read"
                     " every READ_WHOLE, WRITE and undecided file: every line naming the map plus every line that opens,"
                     " loads or writes a file, at HEAD (`git show HEAD:<path>`; the worktree is sparse, so the whole"
                     " repository is read from the commit, never from the working copy). A reading overrides the pattern"
                     " class; a file neither the patterns nor the reading could class is OTHER." % WINDOW)
    lines_out.append("")
    lines_out.append("## 1. Counts")
    lines_out.append("")
    lines_out.append("- git grep -l (whole repository, HEAD): **%d** files" % g)
    lines_out.append("- classed: **%d** files; reconciled=%s; other=%d; ok=%s" % (n, reconciled, other, ok))
    lines_out.append("- classes: " + ", ".join("%s=%d" % (c.lower(), counts[c]) for c in CLASSES))
    lines_out.append("- basis: %d by reading table, %d by line pattern" % (basis_count["reading"], basis_count["pattern"]))
    lines_out.append("- stale reading rows (path not in the grep set): %d" % len(stale))
    lines_out.append("- pattern class disagreed with the reading table: %d" % len(disagree))
    lines_out.append("")
    lines_out.append("### Per top-level folder")
    lines_out.append("")
    lines_out.append("| folder | files | " + " | ".join(c.lower() for c in CLASSES) + " |")
    lines_out.append("|---|---|" + "---|" * len(CLASSES))
    for f in sorted(folders):
        fc = folders[f]
        lines_out.append("| %s | %d | %s |" % (md_cell(f), sum(fc.values()), " | ".join(str(fc[c]) for c in CLASSES)))
    lines_out.append("")
    lines_out.append("### Disagreements (reading wins)")
    lines_out.append("")
    if disagree:
        lines_out.append("| file | pattern class | reading class |")
        lines_out.append("|---|---|---|")
        for p, pc, rcl in disagree:
            lines_out.append("| %s | %s | %s |" % (md_cell(p), pc, rcl))
    else:
        lines_out.append("None.")
    lines_out.append("")
    lines_out.append("## 2. Reading table (every READ_WHOLE, WRITE and undecided file, read by the worker)")
    lines_out.append("")
    lines_out.append("Source: `READINGS_CONSUMERS.tsv` in this folder. Columns: file | class | the line that loads or writes it | what a per-function folder changes for it.")
    lines_out.append("")
    lines_out.append("| file | class | the line that loads or writes it | what a per-function folder changes for it |")
    lines_out.append("|---|---|---|---|")
    for p in sorted(readings):
        r = readings[p]
        lines_out.append("| %s | %s | %s | %s |" % (md_cell(p), r["class"], md_cell(r["what_it_does"]), md_cell(r["per_function_effect"])))
    lines_out.append("")
    lines_out.append("## 3. The map's own shape (HEAD)")
    lines_out.append("")
    lines_out.append("- bytes: %d; top-level keys: %d (%s)" % (shape["bytes"], len(shape["tops"]), ", ".join(shape["tops"])))
    lines_out.append("- metadata keys (not functions): %s" % ", ".join(shape["meta_keys"]))
    lines_out.append("- function entries (keys of `functions`): **%d**" % shape["functions"])
    lines_out.append("- distinct key sets across entries: %d; union of entry keys: %d" % (shape["keysets_distinct"], len(shape["keyset"])))
    lines_out.append("- entry size (json indent 2, bytes): min %d, median %s, max %d" % (shape["min"], shape["median"], shape["max"]))
    lines_out.append("- Terraform, the two counts: (a) the .tf files that NAME the map (%d files) declare **%d** `aws_lambda_function` resources;"
                     " (b) the whole repository's committed .tf files declare **%d** `aws_lambda_function` resources in %d files."
                     % (len(tf_names), tf_lambda, tf_repo_resources, tf_repo_files))
    lines_out.append("- difference, map keys (%d) minus (b) repository Terraform resources (%d): %d; minus (a): %d"
                     % (shape["functions"], tf_repo_resources, shape["functions"] - tf_repo_resources,
                        shape["functions"] - tf_lambda))
    lines_out.append("- the map is not one-to-one with the Terraform resources: a function may have a map row and no resource (a deployed-only or image-built row), or a resource and no row; this is measured, not reconciled, here")
    lines_out.append("")
    lines_out.append("Union of entry keys: " + ", ".join(shape["keyset"]))
    lines_out.append("")
    lines_out.append("Example entry (`%s`, first key in file order):" % shape["example_name"])
    lines_out.append("")
    lines_out.append("```json")
    lines_out.append(ascii_only(shape["example"]))
    lines_out.append("```")
    lines_out.append("")
    lines_out.append("## 4. The deploy script's history (`%s`)" % DEPLOY_REL)
    lines_out.append("")
    lines_out.append("Every commit that changed the file (`git log --follow HEAD`). Owner = author starts with `%s`." % OWNER_PREFIX)
    lines_out.append("")
    lines_out.append("| commit | author | committer | owner | class | what changed | data would live |")
    lines_out.append("|---|---|---|---|---|---|---|")
    for h in hist:
        is_owner = h["author"].startswith(OWNER_PREFIX)
        key = [k for k in dep_read if h["hash"].startswith(k)]
        rd = dep_read[key[0]] if len(key) == 1 else None
        lines_out.append("| %s | %s | %s | %s | %s | %s | %s |" % (
            h["hash"][:10], md_cell(h["author"]), md_cell(h["committer"]), "yes" if is_owner else "NO",
            rd["class"] if rd else ("-" if is_owner else "UNREAD"),
            md_cell(rd["what_changed"]) if rd else md_cell(h["subject"][:120]),
            md_cell(rd["data_home"]) if rd else "-"))
    lines_out.append("")
    lines_out.append("owner_commits=%d non_owner_commits=%d non_owner_data=%d non_owner_code=%d unread=%d"
                     % (len(owner), len(nonowner), data_n, code_n, len(unread)))
    lines_out.append("")
    lines_out.append("## 5. Every file, with its class and the basis of the class")
    lines_out.append("")
    lines_out.append("| class | file | basis | first line naming the map |")
    lines_out.append("|---|---|---|---|")
    for p in names:
        cls, basis, ln, hit = per_file[p]
        lines_out.append("| %s | %s | %s | %d: %s |" % (cls, md_cell(p), basis, ln, md_cell(hit)))
    lines_out.append("")
    body = "\n".join(lines_out)
    with open(CENSUS_MD, "w", encoding="ascii", newline="\n") as f:
        f.write(body)

    for p, pc, rcl in disagree:
        print("DISAGREE %s pattern=%s reading=%s" % (p, pc, rcl))
    for h in unread:
        print("UNREAD non-owner deploy commit %s" % h)
    for p in stale:
        print("STALE reading row %s" % p)
    print("OWNER_COMMITS owner_commits=%d non_owner_commits=%d non_owner_data=%d non_owner_code=%d unread=%d"
          % (len(owner), len(nonowner), data_n, code_n, len(unread)))
    print("MAP_SHAPE functions=%d top_keys=%d tf_named_resources=%d tf_named_files=%d repo_tf_resources=%d repo_tf_files=%d entry_bytes=%d/%s/%d"
          % (shape["functions"], len(shape["tops"]), tf_lambda, len(tf_names), tf_repo_resources, tf_repo_files,
             shape["min"], shape["median"], shape["max"]))
    print("SOURCEMAP-CENSUS files=%d grep_files=%d reconciled=%s map_functions=%d classes=%s ok=%s" % (
        n, g, reconciled, shape["functions"],
        ",".join("%s:%d" % (c.lower(), counts[c]) for c in
                 ["READ_WHOLE", "READ_ONE", "WRITE", "TEST", "DOC", "OTHER"]), ok))
    return 0 if ok else 1


def selftest():
    arms = []

    def arm(name, cond, detail=""):
        arms.append((name, bool(cond)))
        print("%s: %s %s" % ("PASS" if cond else "FAIL", name, detail))

    planted = [
        ("arm_a_read_whole", "infra/planted/consumer.tf",
         ['locals {', '  m = jsondecode(file("x/lambda-source-map.json"))', '}'], "READ_WHOLE"),
        ("arm_b_read_one", "infra/planted/lookup.py",
         ['MAP = "x/lambda-source-map.json"', 'entry = MAP_DATA["fn"]'], "READ_ONE"),
        ("arm_c_write", "infra/planted/writer.py",
         ['with open("x/lambda-source-map.json", "w") as f:', '    json.dump(m, f)'], "WRITE"),
        ("arm_d_test", "infra/planted/tests/test_consumer.py",
         ['# reads x/lambda-source-map.json', 'x = 1'], "TEST"),
        ("arm_e_doc", "infra/planted/notes.md",
         ['The lambda-source-map.json file is described here.'], "DOC"),
        ("arm_g_comment_doc", "infra/planted/comment_only.py",
         ['# the lambda-source-map.json is named in this comment only', 'pass'], "DOC"),
    ]
    with tempfile.TemporaryDirectory() as tmp:
        for name, path, lines, want in planted:
            full = os.path.join(tmp, os.path.basename(path))
            with open(full, "w", encoding="ascii") as f:
                f.write("\n".join(lines) + "\n")
            with open(full, encoding="ascii") as f:
                text = f.read()
            got, basis, ln, hit = classify_file(path, text)
            arm(name, got == want, "got=%s want=%s basis=%s" % (got, want, basis))
        unknown = os.path.join(tmp, "weird.py")
        with open(unknown, "w", encoding="ascii") as f:
            f.write("frobnicate(lambda-source-map)\n")
        with open(unknown, encoding="ascii") as f:
            text = f.read()
        got, basis, ln, hit = classify_file("infra/planted/weird.py", text)
        arm("arm_f_unknown_shape_reads_undecided", got == "UNDECIDED", "got=%s" % got)
        final_cls = "OTHER" if got == "UNDECIDED" else got
        arm("arm_h_unknown_shape_is_other_so_ok_is_false", final_cls == "OTHER",
            "final=%s" % final_cls)
        mini_other = sum(1 for c in [final_cls] if c == "OTHER")
        arm("arm_i_other_count_blocks_ok", (mini_other == 0) is False, "other=%d" % mini_other)
    k = sum(1 for _, c in arms if c)
    n = len(arms)
    print("SOURCEMAP-SELFTEST arms=%d/%d ok=%s" % (k, n, k == n))
    return 0 if k == n else 1


def show(cls):
    names = grep_set()
    blobs = read_blobs(names)
    for p in names:
        blob = blobs[p]
        text = blob.decode("utf-8", "replace") if blob is not None else ""
        c, basis, ln, hit = classify_file(p, text)
        if c == cls:
            print("%s\t%d\t%s" % (p, ln, hit))
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--show" in sys.argv:
        sys.exit(show(sys.argv[sys.argv.index("--show") + 1]))
    sys.exit(run_census())
